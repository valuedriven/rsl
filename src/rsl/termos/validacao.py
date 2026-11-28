"""Validação terminológica assistida: confronta os termos do quadro terminológico com os
instrumentos que o protocolo declara na tabela de instrumentos.

Sigla, modo, idiomas e facetas de cada instrumento vêm do protocolo. Um termo é planejado
para cada instrumento da sua faceta que cubra o seu idioma (`planejamento.py`). Instrumento
`Automático` é consultado pelo cliente TemaTres (`tematres.py`) no endereço resolvido do seu
`Caminho`; instrumento `Manual` não é consultado, e as suas linhas nascem pendentes de
validação manual.

O REGISTRO são dois arquivos (`registro.py`): as decisões do ReT (`[dados] validacao`,
TOML) e o resultado técnico (`[dados] consulta_terminologica`, JSON). Toda resposta bruta é
gravada na pasta de evidência (`[dados] evidencia`), por instrumento; linha consultada sem
evidência correspondente é linha inválida.

REABERTURA (`carrega`): linha sem decisão do ReT, de instrumento `Automático`, que esteja
pendente de validação manual, cuja `url_consultada` não pertença ao endereço resolvido
vigente, ou que seja termo livre não localizado sem `sugestao_similar` (consultada antes da
consulta de similaridade) volta a aguardar consulta; a evidência anterior fica na pasta de
evidência até a reconsulta, que a substitui no mesmo arquivo (o nome vem de instrumento,
idioma e termo). Linha nessa situação com decisão é preservada e listada na saída. A regra
mora na reconstrução dos registros: mudar o `Caminho` reabre as linhas afetadas sem passo
manual.

FRONTEIRA DE USO (protocolo): este módulo RECUPERA e REGISTRA. Não decide.
  - nenhum termo é excluído, reescrito ou incorporado automaticamente;
  - termo não localizado NÃO é erro: é termo livre, e assim é classificado;
  - TR e TE revelados pela consulta entram como CANDIDATOS, nunca nas strings;
  - o campo `decisao_ReT` fica vazio: a decisão é do pesquisador, com o VT, e o seu domínio
    é fechado (`decisao.py`): dela resulta a linha do termo no CT.

Fonte externa com erro de rede, bloqueio, captcha, limite ou resposta fora do formato
interrompe a validação na hora, sem nova tentativa e sem consultar o termo seguinte: o que
já foi consultado fica gravado, a linha do termo interrompido registra a condição e o
subcomando sai com FONTE_EXTERNA.
"""

import datetime
import json
import time

from .. import gramatica as G
from ..config import relativo
from ..erros import DadosInvalidos, FonteExterna, Reprovado, Uso
from ..leitura import endereco, instrumentos_do_termo
from ..saida import Saida
from . import registro as R
from . import tematres
from .decisao import fora_do_dominio
from .planejamento import (STATUS_CANDIDATO, STATUS_MANUAL, STATUS_NAO_LOCALIZADO,
                           estado_inicial)

CAMPOS_DECISAO = R.CAMPOS_DECISAO
CAMPOS_RESPOSTA = R.CAMPOS_RESPOSTA
CAMPOS_TECNICOS = R.CAMPOS_TECNICOS
# Sem esta coluna, toda linha não localizada pareceria nunca consultada pela similaridade e
# seria reaberta a cada execução: a configuração que não a traz é recusada.
COLUNA_SIMILAR = "sugestao_similar"
GRAVA_A_CADA = 20


def agora():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


class Registro:
    """Os dois registros da validação e a pasta de evidência, pelos caminhos da configuração."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.caminho = ctx.config.caminho("dados.validacao")
        self.caminho_resultado = ctx.config.caminho("dados.consulta_terminologica")
        self.evidencia = ctx.config.caminho("dados.evidencia")
        self.reabertas = 0
        self.preservadas = []      # (termo, instrumento, idioma, motivo, evidência)
        self._relatado = False

    @staticmethod
    def chave(faceta, idioma, termo, instrumento):
        return R.chave(faceta, idioma, termo, instrumento)

    def decisoes(self):
        """Tabelas do arquivo de decisões (ou cópia em memória); [] se ausente."""
        return R.le_decisoes(self.ctx.texto_decisoes, relativo(self.caminho))

    def resultado(self):
        """Objetos do resultado técnico (ou cópia em memória); [] se ausente."""
        return R.le_resultado(self.ctx.texto_resultado, relativo(self.caminho_resultado))

    def existente(self):
        """({chave: decisão}, {chave: linha técnica}) dos registros correntes."""
        return ({self.chave(r["faceta"], r["idioma"], r["termo"], r["instrumento"]): r
                 for r in self.decisoes()},
                {self.chave(r["faceta"], r["idioma"], r["termo"], r["instrumento"]): r
                 for r in self.resultado()})

    def grava_evidencia(self, instrumento, idioma, termo, payload):
        """Grava a resposta bruta no caminho calculado por `registro.caminho_evidencia` e
        devolve o caminho relativo à pasta-mãe da evidência."""
        caminho = R.caminho_evidencia(self.evidencia, instrumento, idioma, termo)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        chave = f"{instrumento}|{idioma}|{termo}"
        caminho.write_text(
            json.dumps({"chave": chave, "recuperado_em": agora(), "payload": payload},
                       ensure_ascii=False, indent=2),
            encoding="utf-8")
        return str(caminho.relative_to(self.evidencia.parent))


def pertence(url, endereco_):
    """A `url_consultada` é do endereço resolvido: ele mesmo ou ele com consulta."""
    return url == endereco_ or url.startswith(endereco_ + "?")


def motivo_reabertura(v, instrumento):
    """Por que a linha de um instrumento `Automático` não vale como consulta vigente, ou
    None. `instrumento` traz o endereço resolvido para o idioma da linha."""
    if instrumento["modo"] != G.MODO_AUTOMATICO:
        return None
    if v.get("status_proposto") == STATUS_MANUAL:
        return STATUS_MANUAL
    url = v.get("url_consultada", "")
    if url and not pertence(url, instrumento["endereco"]):
        return f"consultada fora do endereço vigente {instrumento['endereco']}"
    if v.get("status_proposto") == STATUS_NAO_LOCALIZADO and not v.get(COLUNA_SIMILAR):
        return f"{STATUS_NAO_LOCALIZADO} sem consulta de similaridade"
    return None


def carrega(ctx, d, registro):
    """Os registros reconstruídos do protocolo, das decisões e do resultado técnico.

    Termo novo nasce aguardando consulta, ou pendente de validação manual se o instrumento
    é `Manual`; linha já registrada é preservada campo a campo, inclusive decisão do ReT e
    evidência, salvo a reabertura (docstring do módulo). Devolve as linhas na ordem do
    protocolo: faceta, idioma, termo, instrumento; cada uma com o endereço resolvido.
    """
    registro.reabertas, registro.preservadas = 0, []
    decisoes, resultado = registro.existente()
    info = {f["id"]: f for f in d["facetas"]}
    linhas = []
    for f in d["tabelas"]:
        meta = info.get(f["id"], {})
        for idioma in d["idiomas"]:
            insts = instrumentos_do_termo(d, f["id"], idioma)
            for termo in f["termos"][idioma]:
                for i in insts:
                    k = registro.chave(f["id"], idioma, termo, i["sigla"])
                    v = {c: "" for c in CAMPOS_TECNICOS + CAMPOS_DECISAO}
                    dec = decisoes.get(k)
                    tec = resultado.get(k)
                    if dec:
                        v.update({c: dec.get(c, "") for c in CAMPOS_DECISAO})
                    if tec:
                        v.update({c: tec.get(c, "") for c in CAMPOS_TECNICOS})
                    v["instrumento"] = i["sigla"]
                    if tec is None:
                        v.update(estado_inicial(i))
                    elif (motivo := motivo_reabertura(v, i)):
                        if v.get("decisao_ReT"):
                            registro.preservadas.append(
                                (termo, i["sigla"], idioma, motivo,
                                 v.get("url_consultada") or v.get("arquivo_evidencia")))
                        else:
                            for c in CAMPOS_TECNICOS:
                                v[c] = ""
                            v.update(estado_inicial(i))
                            registro.reabertas += 1
                    linhas.append({"faceta": f["id"], "faceta_nome": meta.get("nome", ""),
                                   "ancora": "sim" if meta.get("ancora") else "não",
                                   "idioma": idioma, "termo": termo,
                                   "endereco": i["endereco"], "_v": v})
    return linhas


def _objetos(linhas, d):
    """Linhas técnicas dos registros reconstruídos, na ordem do protocolo."""
    tecnicas = []
    for ln in linhas:
        v = ln["_v"]
        i = d["instrumentos"][v["instrumento"]]
        if R.tem_linha_tecnica(v, i):
            objeto = {c: v.get(c, "") for c in CAMPOS_TECNICOS}
            objeto.update({c: ln[c] for c in ("faceta", "idioma", "termo")})
            objeto["instrumento"] = v["instrumento"]
            tecnicas.append(objeto)
    return tecnicas


def _decisoes_para_gravar(registro, linhas):
    """Decisões na ordem do protocolo; tabela de chave fora do protocolo não é gravada.

    Devolve também as tabelas removidas, só para o relato da execução: não se guarda
    histórico de termos."""
    lidas = registro.decisoes()
    por_chave = {registro.chave(r["faceta"], r["idioma"], r["termo"], r["instrumento"]): r
                 for r in lidas}
    chaves_protocolo = {registro.chave(ln["faceta"], ln["idioma"], ln["termo"],
                                       ln["_v"]["instrumento"]) for ln in linhas}
    saida = []
    for ln in linhas:
        k = registro.chave(ln["faceta"], ln["idioma"], ln["termo"],
                           ln["_v"]["instrumento"])
        r = por_chave.get(k)
        if r and any((r.get(c) or "").strip() for c in CAMPOS_DECISAO):
            saida.append(r)
    removidas = [r for r in lidas if registro.chave(
        r["faceta"], r["idioma"], r["termo"], r["instrumento"]) not in chaves_protocolo]
    return saida, removidas


def _resumo(registro, linhas, d):
    manuais = sum(1 for ln in linhas
                  if d["instrumentos"][ln["_v"]["instrumento"]]["modo"] == G.MODO_MANUAL)
    a_validar = sum(1 for ln in linhas if not ln["_v"].get("status_proposto"))
    candidatas = sum(1 for ln in linhas
                     if ln["_v"].get("status_proposto") == STATUS_CANDIDATO)
    print(f"{relativo(registro.caminho_resultado)}: {len(linhas)} linhas — {a_validar} a "
          f"validar por cliente automatizado, {manuais} {STATUS_MANUAL}, {candidatas} "
          f"{STATUS_CANDIDATO}.")
    if registro._relatado:
        return
    registro._relatado = True
    if registro.reabertas:
        print(f"  {registro.reabertas} linha(s) sem decisão voltaram a aguardar consulta "
              f"(pendentes de validação manual, consultadas fora do endereço vigente ou "
              f"não localizadas sem consulta de similaridade); a evidência anterior fica "
              f"em {relativo(registro.evidencia)}/ até a reconsulta, que a substitui.")
    if registro.preservadas:
        print(f"  {len(registro.preservadas)} linha(s) com decisão do ReT tomada sobre "
              f"consulta que hoje seria refeita (motivo em cada linha), preservada(s) sem "
              f"reconsulta — decidir se mantêm a decisão:")
        for termo, sigla, idioma, motivo, evid in registro.preservadas:
            print(f"    - {termo!r} ({idioma}) em {sigla}: {motivo}; evidência: "
                  f"{evid or 'sem registro'}")


def grava_registros(registro, linhas, d):
    """Grava os dois arquivos, confere a evidência e expurga a evidência de chave retirada."""
    decisoes, removidas = _decisoes_para_gravar(registro, linhas)
    tecnicas = _objetos(linhas, d)
    protocolo_chaves = {registro.chave(ln["faceta"], ln["idioma"], ln["termo"],
                                       ln["_v"]["instrumento"]) for ln in linhas}
    removidas_tecnicas = [r for r in registro.resultado()
                          if registro.chave(r["faceta"], r["idioma"], r["termo"],
                                            r["instrumento"]) not in protocolo_chaves]
    chaves_tecnicas = {registro.chave(o["faceta"], o["idioma"], o["termo"],
                                      o["instrumento"]) for o in tecnicas}
    sem_consulta = [r for r in decisoes
                    if registro.chave(r["faceta"], r["idioma"], r["termo"],
                                      r["instrumento"]) not in chaves_tecnicas]
    R.confere_evidencia(registro.evidencia, tecnicas)
    R.grava_decisoes(registro.caminho, decisoes)
    R.grava_resultado(registro.caminho_resultado, tecnicas)
    R.expurga(registro.evidencia, R.caminhos_esperados(registro.evidencia, d))
    _resumo(registro, linhas, d)
    if sem_consulta:
        print(f"  {len(sem_consulta)} decisão(ões) sem linha no resultado técnico "
              f"(consulta não registrada), preservada(s):")
        for r in sem_consulta:
            print(f"    - {r['termo']!r} ({r['faceta']}, {r['idioma']}, "
                  f"{r['instrumento']})")
    if removidas:
        print(f"  {len(removidas)} decisão(ões) de termo fora do protocolo removida(s).")
    if removidas_tecnicas:
        print(f"  {len(removidas_tecnicas)} linha(s) técnica(s) de termo fora do protocolo "
              f"removida(s).")


def grava_resultado(registro, linhas, d):
    """Grava só o resultado técnico e a evidência; nunca toca no arquivo de decisões."""
    tecnicas = _objetos(linhas, d)
    R.confere_evidencia(registro.evidencia, tecnicas)
    R.grava_resultado(registro.caminho_resultado, tecnicas)
    if not registro._relatado:
        _resumo(registro, linhas, d)


def automaticos(d):
    """Siglas dos instrumentos `Automático` do protocolo, na ordem da tabela."""
    return [s for s, i in d["instrumentos"].items() if i["modo"] == G.MODO_AUTOMATICO]


def validar(ctx, quais, faceta=None):
    """Consulta, um termo por vez, os termos ainda sem estatuto nos instrumentos `quais`."""
    d = ctx.protocolo()
    registro = Registro(ctx)
    linhas = carrega(ctx, d, registro)
    pendentes = [ln for ln in linhas
                 if not ln["_v"].get("status_proposto")
                 and (not faceta or ln["faceta"] == f"{G.I_FCT.prefixo}{faceta}")
                 and ln["_v"].get("instrumento") in quais]
    feitos = 0
    versoes = {}
    for k, ln in enumerate(pendentes):
        v = ln["_v"]
        inst, termo, end = v["instrumento"], ln["termo"], ln["endereco"]
        try:
            if end not in versoes:
                versoes[end] = tematres.versao(end)
                time.sleep(tematres.PAUSA)
            versao_, reg_versao = versoes[end]
            reg, status, dados_inst, obs, url, versao = tematres.valida(termo, end, versao_)
            reg["fetchVocabularyData"] = reg_versao
        except FonteExterna as e:
            v["observacao_tecnica"] = f"CONSULTA INTERROMPIDA em {agora()}: {e}"
            grava_resultado(registro, linhas, d)
            restantes = len(pendentes) - k
            raise FonteExterna(
                f"instrumento {inst}, termo {termo!r}: {e}. Validação interrompida sem nova "
                f"tentativa; {feitos} termo(s) consultado(s) e gravado(s) nesta execução, "
                f"{restantes} sem consulta (inclusive este). Rode  python3 -m rsl termos "
                f"sondar  antes de retomar.") from None
        v["url_consultada"] = url
        v["versao_instrumento"] = versao
        v["consultado_em"] = agora()
        v["status_proposto"] = status
        v["observacao_tecnica"] = obs
        for c in CAMPOS_RESPOSTA:
            v[c] = dados_inst.get(c, "")
        v["arquivo_evidencia"] = registro.grava_evidencia(
            inst, ln["idioma"], termo, reg)
        feitos += 1
        print(f"[{feitos:>3}] {inst:<7} {termo[:48]:<50} {status}")
        if feitos % GRAVA_A_CADA == 0:
            grava_resultado(registro, linhas, d)
        time.sleep(tematres.PAUSA)

    grava_resultado(registro, linhas, d)
    print(f"\n{feitos} termos consultados. Evidência bruta em {relativo(registro.evidencia)}/.")
    print("A validação não altera o arquivo de decisões: a classificação final e a "
          "incorporação de TR/TE são do pesquisador, com o VT.")
    return Saida.OK


# ----------------------------------------------------------------------- comandos
def cmd_sonda(ctx, a=None):
    """Cada endereço resolvido de cada instrumento `Automático`, um por idioma, em ordem e
    com pausa; o primeiro FonteExterna interrompe a sonda inteira."""
    d = ctx.protocolo()
    print("SONDAGEM — nada é gravado. Confira cada resposta antes de validar.\n")
    primeiro = True
    for sigla in automaticos(d):
        i = d["instrumentos"][sigla]
        for idioma in i["idiomas"]:
            if not primeiro:
                time.sleep(tematres.PAUSA)
            primeiro = False
            end = endereco(i, idioma)
            print(f"== {sigla} ({idioma}) — {end} ==")
            tematres.sonda(d, i, idioma, end, print)
            print()
    return Saida.OK


def cmd_exportar(ctx, a=None):
    """Reconstrói os dois registros a partir do protocolo, sem rede."""
    registro = Registro(ctx)
    d = ctx.protocolo()
    grava_registros(registro, carrega(ctx, d, registro), d)
    return Saida.OK


def cmd_importar(ctx, a=None):
    """Reconcilia os registros com o protocolo, preservando decisões e retirando a técnica
    órfã."""
    registro = Registro(ctx)
    if not registro.caminho.exists():
        raise DadosInvalidos(f"{relativo(registro.caminho)} não existe. Rode  "
                             f"python3 -m rsl termos exportar  antes.")
    lidas = registro.decisoes()
    # Decisão fora do domínio reprova antes de qualquer gravação: preservá-la seria levar
    # adiante uma classificação que a conferência do CT não sabe ler.
    invalidas = fora_do_dominio(lidas)
    if invalidas:
        raise Reprovado("arquivo de decisões com decisão do ReT fora do domínio; nada "
                        "foi gravado:\n  - " + "\n  - ".join(invalidas))
    d = ctx.protocolo()
    linhas_ = carrega(ctx, d, registro)
    gravadas, _ = _decisoes_para_gravar(registro, linhas_)
    grava_registros(registro, linhas_, d)
    com_decisao = sum(1 for r in gravadas if (r.get("decisao_ReT") or "").strip())
    print(f"{len(gravadas)} tabela(s) de chave do protocolo, {com_decisao} decisão(ões) "
          f"preservada(s).")
    return Saida.OK


def cmd_validar(ctx, a):
    d = ctx.protocolo()
    admitidos = automaticos(d)
    if a.sigla == "todos":
        quais = admitidos
    elif a.sigla in admitidos:
        quais = [a.sigla]
    else:
        raise Uso(f"termos validar {a.sigla!r}: não é sigla de instrumento "
                  f"{G.MODO_AUTOMATICO} do protocolo. Use {', '.join(admitidos)} ou todos.")
    return validar(ctx, quais, a.faceta)
