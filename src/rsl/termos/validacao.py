"""Validação terminológica assistida: confronta os termos do quadro terminológico com os
instrumentos que o protocolo declara na tabela de instrumentos.

Sigla, modo, idiomas e facetas de cada instrumento vêm do protocolo. Um termo é planejado
para cada instrumento da sua faceta que cubra o seu idioma (`planejamento.py`). Instrumento
`Automático` é consultado pelo cliente da sua sigla (`clientes/`); instrumento `Manual`
não tem cliente, e as suas linhas nascem pendentes de validação manual.

FRONTEIRA DE USO (protocolo): este módulo RECUPERA e REGISTRA. Não decide.
  - nenhum termo é excluído, reescrito ou incorporado automaticamente;
  - termo não localizado NÃO é erro: é termo livre, e assim é classificado;
  - TR e TE revelados pela consulta entram como CANDIDATOS, nunca nas strings;
  - a coluna `decisao_ReT` sai em branco: a decisão é do pesquisador, com o VT.

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
from ..erros import DadosInvalidos, FonteExterna, Uso
from ..leitura import instrumentos_do_termo
from ..markdown import normaliza
from ..saida import Saida
from . import clientes
from .planejamento import STATUS_MANUAL, estado_inicial

CAMPOS_DECISAO = ("decisao_ReT", "justificativa_ReT", "data_decisao")
CAMPOS_RESPOSTA = ("rotulo_autorizado", "uri_conceito", "equivalentes_USE_UP",
                   "termos_genericos_TG", "termos_especificos_TE",
                   "termos_relacionados_TR", "nota_de_escopo")
GRAVA_A_CADA = 20


def agora():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


class Planilha:
    """A planilha de validação e a pasta de evidência, pelos caminhos da configuração."""

    def __init__(self, ctx):
        self.caminho = ctx.config.caminho("dados.validacao")
        self.evidencia = ctx.config.caminho("dados.evidencia")
        self.campos = list(ctx.config.valor("planilha.campos_validacao"))
        self.colunas = ["faceta", "faceta_nome", "ancora", "idioma", "termo"] + self.campos

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


def carrega(ctx, d, planilha):
    """O registro reconstruído do protocolo e da planilha existente.

    Termo novo nasce aguardando consulta, ou pendente de validação manual se o instrumento
    não tem cliente; linha já registrada é preservada campo a campo, inclusive decisão do
    ReT e evidência. Devolve as linhas na ordem do protocolo: faceta, idioma, termo,
    instrumento.
    """
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
                    linhas.append({"faceta": f["id"], "faceta_nome": meta.get("nome", ""),
                                   "ancora": "sim" if meta.get("ancora") else "não",
                                   "idioma": idioma, "termo": termo, "_v": v})
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
    print(f"{relativo(planilha.caminho)}: {len(saida)} linhas — {a_validar} a validar por "
          f"cliente automatizado, {manuais} {STATUS_MANUAL}.")
    if orfaos:
        print(f"  {len(orfaos)} linha(s) fora do protocolo preservada(s) na planilha — "
              f"decidir: manter com registro ou retirar à mão.")


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
    for k, ln in enumerate(pendentes):
        v = ln["_v"]
        inst, termo = v["instrumento"], ln["termo"]
        cliente = clientes.cliente(inst)
        try:
            reg, status, dados_inst, obs, url, versao = cliente.valida(
                termo, d["instrumentos"][inst])
        except FonteExterna as e:
            v["observacao_tecnica"] = f"CONSULTA INTERROMPIDA em {agora()}: {e}"
            grava_planilha(planilha, linhas)
            restantes = len(pendentes) - k
            raise FonteExterna(
                f"instrumento {inst}, termo {termo!r}: {e}. Validação interrompida sem nova "
                f"tentativa; {feitos} termo(s) consultado(s) e gravado(s) nesta execução, "
                f"{restantes} sem consulta (inclusive este). Rode  python3 -m rsl termos "
                f"sonda  antes de retomar.") from None
        v["url_consultada"] = url
        v["versao_instrumento"] = versao
        v["consultado_em"] = agora()
        v["status_proposto"] = status
        v["observacao_tecnica"] = obs
        for c in CAMPOS_RESPOSTA:
            v[c] = dados_inst.get(c, "")
        v["arquivo_evidencia"] = planilha.grava_evidencia(inst.lower(), f"{inst}|{termo}", reg)
        feitos += 1
        print(f"[{feitos:>3}] {inst:<7} {termo[:48]:<50} {status}")
        if feitos % GRAVA_A_CADA == 0:
            grava_planilha(planilha, linhas)
        time.sleep(cliente.PAUSA)

    grava_planilha(planilha, linhas)
    print(f"\n{feitos} termos consultados. Evidência bruta em {relativo(planilha.evidencia)}/.")
    print("As colunas decisao_ReT, justificativa_ReT e data_decisao ficam em branco: "
          "a classificação final e a incorporação de TR/TE são do pesquisador, com o VT.")
    return Saida.OK


# ----------------------------------------------------------------------- comandos
def cmd_sonda(ctx, a=None):
    d = ctx.protocolo()
    print("SONDAGEM — nada é gravado. Confira cada resposta antes de validar.\n")
    for sigla in automaticos(d):
        print(f"== {sigla} ==")
        clientes.cliente(sigla).sonda(d, d["instrumentos"][sigla], print)
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
