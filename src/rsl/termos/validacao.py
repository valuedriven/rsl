"""Validação terminológica assistida: confronta os termos do quadro terminológico com os
instrumentos que o protocolo declara na tabela de instrumentos.

Sigla, modo, idiomas e facetas de cada instrumento vêm do protocolo. Um termo é planejado
para cada instrumento da sua faceta que cubra o seu idioma (`planejamento.py`). Instrumento
`Automático` é consultado pelo cliente TemaTres (`tematres.py`) no endereço resolvido do seu
`Caminho`; instrumento `Manual` não é consultado, e as suas linhas nascem pendentes de
validação manual.

REABERTURA (`carrega`): linha sem decisão do ReT, de instrumento `Automático`, que esteja
pendente de validação manual, cuja `url_consultada` não pertença ao endereço resolvido
vigente, ou que seja termo livre não localizado sem `sugestao_similar` (consultada antes da
consulta de similaridade) volta a aguardar consulta; a evidência anterior fica na pasta de
evidência até a reconsulta, que a substitui no mesmo arquivo (o nome vem de instrumento,
idioma e termo). Linha nessa situação com decisão é preservada e listada na saída. A regra mora na reconstrução da
planilha: mudar o `Caminho` reabre as linhas afetadas sem passo manual.

FRONTEIRA DE USO (protocolo): este módulo RECUPERA e REGISTRA. Não decide.
  - nenhum termo é excluído, reescrito ou incorporado automaticamente;
  - termo não localizado NÃO é erro: é termo livre, e assim é classificado;
  - TR e TE revelados pela consulta entram como CANDIDATOS, nunca nas strings;
  - a coluna `decisao_ReT` sai em branco: a decisão é do pesquisador, com o VT, e o seu
    domínio é fechado (`decisao.py`): dela resulta a linha do termo no CT.

O REGISTRO é a própria planilha de validação (`[dados] validacao`). Toda resposta bruta é
gravada na pasta de evidência (`[dados] evidencia`), por instrumento; linha sem evidência
correspondente é linha inválida.

Fonte externa com erro de rede, bloqueio, captcha, limite ou resposta fora do formato
interrompe a validação na hora, sem nova tentativa e sem consultar o termo seguinte: o que
já foi consultado fica gravado, a linha do termo interrompido registra a condição e o
subcomando sai com FONTE_EXTERNA.
"""

import collections
import csv
import datetime
import hashlib
import json
import time

from .. import gramatica as G
from ..config import relativo
from ..erros import ConfiguracaoInvalida, DadosInvalidos, FonteExterna, Reprovado, Uso
from ..leitura import endereco, instrumentos_do_termo
from ..markdown import normaliza
from ..saida import Saida
from . import tematres
from .decisao import fora_do_dominio
from .planejamento import (STATUS_CANDIDATO, STATUS_MANUAL, STATUS_NAO_LOCALIZADO,
                           estado_inicial)

CAMPOS_DECISAO = ("decisao_ReT", "justificativa_ReT", "data_decisao")
CAMPOS_RESPOSTA = ("rotulo_autorizado", "forma_no_instrumento", "sugestao_similar",
                   "uri_conceito",
                   "equivalentes_USE_UP", "termos_genericos_TG", "termos_especificos_TE",
                   "termos_relacionados_TR", "nota_de_escopo")
# Campos que a consulta preenche: limpos quando a linha volta a aguardar consulta.
CAMPOS_CONSULTA = ("consultado_em", "versao_instrumento", "url_consultada", "status_proposto",
                   "arquivo_evidencia", "observacao_tecnica") + CAMPOS_RESPOSTA
# Sem esta coluna, toda linha não localizada pareceria nunca consultada pela similaridade e
# seria reaberta a cada execução: a configuração que não a traz é recusada.
COLUNA_SIMILAR = "sugestao_similar"
GRAVA_A_CADA = 20


def agora():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


class Planilha:
    """A planilha de validação e a pasta de evidência, pelos caminhos da configuração."""

    def __init__(self, ctx):
        self.caminho = ctx.config.caminho("dados.validacao")
        self.evidencia = ctx.config.caminho("dados.evidencia")
        self.campos = list(ctx.config.valor("planilha.campos_validacao"))
        if COLUNA_SIMILAR not in self.campos:
            raise ConfiguracaoInvalida(
                f"planilha.campos_validacao não traz {COLUNA_SIMILAR!r}: sem ela, a linha "
                f"não localizada já consultada não se distingue da nunca consultada")
        self.colunas = ["faceta", "faceta_nome", "ancora", "idioma", "termo"] + self.campos
        self.reabertas = 0
        self.preservadas = []      # (termo, instrumento, idioma, motivo, evidência)
        self._relatado = False

    @staticmethod
    def chave(faceta, idioma, termo, instrumento):
        return (str(faceta), idioma, normaliza(termo), instrumento)

    def existente(self):
        """Linhas já registradas, por faceta, idioma, termo normalizado e instrumento."""
        if not self.caminho.exists():
            return {}
        with self.caminho.open(encoding="utf-8-sig", newline="") as fh:
            return {self.chave(r.get("faceta", ""), r.get("idioma", ""), r.get("termo", ""),
                               r.get("instrumento", "")): r
                    for r in csv.DictReader(fh, delimiter=";")}

    def grava_evidencia(self, instrumento, chave, payload):
        pasta = self.evidencia / instrumento
        pasta.mkdir(parents=True, exist_ok=True)
        caminho = pasta / (hashlib.sha1(chave.encode("utf-8")).hexdigest()[:16] + ".json")
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


def carrega(ctx, d, planilha):
    """O registro reconstruído do protocolo e da planilha existente.

    Termo novo nasce aguardando consulta, ou pendente de validação manual se o instrumento
    é `Manual`; linha já registrada é preservada campo a campo, inclusive decisão do ReT e
    evidência, salvo a reabertura (docstring do módulo). Devolve as linhas na ordem do
    protocolo: faceta, idioma, termo, instrumento; cada uma com o endereço resolvido.
    """
    planilha.reabertas, planilha.preservadas = 0, []
    existente = planilha.existente()
    info = {f["id"]: f for f in d["facetas"]}
    linhas = []
    for f in d["tabelas"]:
        meta = info.get(f["id"], {})
        for idioma in d["idiomas"]:
            insts = instrumentos_do_termo(d, f["id"], idioma)
            for termo in f["termos"][idioma]:
                for i in insts:
                    r = existente.get(planilha.chave(f["id"], idioma, termo, i["sigla"]))
                    v = {c: ((r.get(c) or "").strip() if r else "") for c in planilha.campos}
                    v["instrumento"] = i["sigla"]
                    if r is None:
                        v.update(estado_inicial(i))
                    elif (motivo := motivo_reabertura(v, i)):
                        if v.get("decisao_ReT"):
                            planilha.preservadas.append(
                                (termo, i["sigla"], idioma, motivo,
                                 v.get("url_consultada") or v.get("arquivo_evidencia")))
                        else:
                            for c in CAMPOS_CONSULTA:
                                v[c] = ""
                            v.update(estado_inicial(i))
                            planilha.reabertas += 1
                    linhas.append({"faceta": f["id"], "faceta_nome": meta.get("nome", ""),
                                   "ancora": "sim" if meta.get("ancora") else "não",
                                   "idioma": idioma, "termo": termo,
                                   "endereco": i["endereco"], "_v": v})
    return linhas


def grava_planilha(planilha, linhas):
    """Grava o registro na planilha, preservando as linhas fora do protocolo."""
    planilha.caminho.parent.mkdir(parents=True, exist_ok=True)
    saida = [{**{k: ln[k] for k in ("faceta", "faceta_nome", "ancora", "idioma", "termo")},
              **{c: ln["_v"].get(c, "") for c in planilha.campos}} for ln in linhas]
    chaves = {planilha.chave(l["faceta"], l["idioma"], l["termo"], l["instrumento"])
              for l in saida}
    orfaos = [r for k, r in planilha.existente().items() if k not in chaves]
    with planilha.caminho.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=planilha.colunas, delimiter=";")
        w.writeheader()
        w.writerows(saida)
        for r in orfaos:
            w.writerow({c: r.get(c, "") for c in planilha.colunas})
    manuais = sum(1 for l in saida if l["status_proposto"] == STATUS_MANUAL)
    a_validar = sum(1 for l in saida if not l["status_proposto"])
    candidatas = sum(1 for l in saida if l["status_proposto"] == STATUS_CANDIDATO)
    print(f"{relativo(planilha.caminho)}: {len(saida)} linhas — {a_validar} a validar por "
          f"cliente automatizado, {manuais} {STATUS_MANUAL}, {candidatas} "
          f"{STATUS_CANDIDATO}.")
    if orfaos:
        print(f"  {len(orfaos)} linha(s) fora do protocolo preservada(s) na planilha — "
              f"decidir: manter com registro ou retirar à mão.")
    if planilha._relatado:
        return
    planilha._relatado = True
    if planilha.reabertas:
        print(f"  {planilha.reabertas} linha(s) sem decisão voltaram a aguardar consulta "
              f"(pendentes de validação manual, consultadas fora do endereço vigente ou "
              f"não localizadas sem consulta de similaridade); a evidência anterior fica "
              f"em {relativo(planilha.evidencia)}/ até a reconsulta, que a substitui.")
    if planilha.preservadas:
        print(f"  {len(planilha.preservadas)} linha(s) com decisão do ReT tomada sobre "
              f"consulta que hoje seria refeita (motivo em cada linha), preservada(s) sem "
              f"reconsulta — decidir se mantêm a decisão:")
        for termo, sigla, idioma, motivo, evid in planilha.preservadas:
            print(f"    - {termo!r} ({idioma}) em {sigla}: {motivo}; evidência: "
                  f"{evid or 'sem registro'}")


def automaticos(d):
    """Siglas dos instrumentos `Automático` do protocolo, na ordem da tabela."""
    return [s for s, i in d["instrumentos"].items() if i["modo"] == G.MODO_AUTOMATICO]


def validar(ctx, quais, faceta=None):
    """Consulta, um termo por vez, os termos ainda sem estatuto nos instrumentos `quais`."""
    d = ctx.protocolo()
    planilha = Planilha(ctx)
    linhas = carrega(ctx, d, planilha)
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
            grava_planilha(planilha, linhas)
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
        v["arquivo_evidencia"] = planilha.grava_evidencia(
            inst.lower(), f"{inst}|{ln['idioma']}|{termo}", reg)
        feitos += 1
        print(f"[{feitos:>3}] {inst:<7} {termo[:48]:<50} {status}")
        if feitos % GRAVA_A_CADA == 0:
            grava_planilha(planilha, linhas)
        time.sleep(tematres.PAUSA)

    grava_planilha(planilha, linhas)
    print(f"\n{feitos} termos consultados. Evidência bruta em {relativo(planilha.evidencia)}/.")
    print("As colunas decisao_ReT, justificativa_ReT e data_decisao ficam em branco: "
          "a classificação final e a incorporação de TR/TE são do pesquisador, com o VT.")
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
    """Reconstrói a planilha a partir do protocolo, sem rede."""
    planilha = Planilha(ctx)
    grava_planilha(planilha, carrega(ctx, ctx.protocolo(), planilha))
    return Saida.OK


def cmd_importar(ctx, a=None):
    """Reconcilia a planilha com o protocolo, preservando decisões e linhas órfãs."""
    planilha = Planilha(ctx)
    if not planilha.caminho.exists():
        raise DadosInvalidos(f"{relativo(planilha.caminho)} não existe. Rode  "
                             f"python3 -m rsl termos exportar  antes.")
    linhas_ = carrega(ctx, ctx.protocolo(), planilha)
    idx = {planilha.chave(ln["faceta"], ln["idioma"], ln["termo"],
                          ln["_v"].get("instrumento")): ln["_v"] for ln in linhas_}
    with planilha.caminho.open(encoding="utf-8-sig", newline="") as fh:
        lidas = list(csv.DictReader(fh, delimiter=";"))
    # Decisão fora do domínio reprova antes de qualquer gravação: preservá-la seria levar
    # adiante uma classificação que a conferência do CT não sabe ler.
    invalidas = fora_do_dominio(lidas)
    if invalidas:
        raise Reprovado("planilha de validação com decisão do ReT fora do domínio; nada "
                        "foi gravado:\n  - " + "\n  - ".join(invalidas))
    casadas, sem_casa, com_decisao = 0, [], 0
    for r in lidas:
        k = planilha.chave(r.get("faceta", ""), r.get("idioma", ""), r.get("termo", ""),
                           r.get("instrumento", ""))
        v = idx.get(k)
        if v is None:
            sem_casa.append(k)
            continue
        casadas += 1
        for c in CAMPOS_DECISAO:
            valor = (r.get(c) or "").strip()
            if valor:
                v[c] = valor
                if c == "decisao_ReT":
                    com_decisao += 1
    grava_planilha(planilha, linhas_)
    print(f"{casadas} linha(s) casada(s), {com_decisao} decisão(ões) preservada(s), "
          f"{len(sem_casa)} fora do protocolo (preservadas).")
    duplas = [k for k, n in collections.Counter(
        (r.get("faceta"), r.get("idioma"), normaliza(r.get("termo"))) for r in lidas).items()
        if n > 1]
    if duplas:
        print(f"AVISO: {len(duplas)} termo(s) aparecem mais de uma vez na planilha; a última "
              "linha lida prevalece.")
    for k in sem_casa[:10]:
        print(f"  fora do protocolo: {k}")
    return Saida.OK if not sem_casa else Saida.REPROVADO


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
