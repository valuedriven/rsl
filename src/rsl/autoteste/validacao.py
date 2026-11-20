"""Autoteste do planejamento da validação terminológica por instrumento."""

import copy

from .. import gramatica as G
from ..leitura import instrumentos_do_termo
from ..markdown import lista
from ..termos.planejamento import STATUS_MANUAL, estado_inicial
from .textos import celula, coluna, troca_celula


def casos(ctx, g):
    """Sobre o protocolo e cópias alteradas: todos os instrumentos da faceta são
    planejados, instrumento cuja coluna FCTs perde a faceta não é, só nos idiomas que o
    instrumento cobre, e o modo `Manual` faz a linha nascer pendente de validação manual."""
    t, d = ctx.texto, ctx.protocolo()
    L = d["locais"]

    def planejados(dd, fid):
        return {i["sigla"] for idioma in dd["idiomas"]
                for i in instrumentos_do_termo(dd, fid, idioma)}

    # Vários instrumentos: a faceta com mais instrumentos tem todos planejados. Sem faceta
    # com mais de um, o caso não prova nada e falha.
    por_faceta = d["instrumentos_por_faceta"]
    fid = max(por_faceta, key=lambda f: len(por_faceta[f]))
    declarados = {i["sigla"] for i in por_faceta[fid] if set(i["idiomas"]) & set(d["idiomas"])}
    g.testa(f"faceta com vários instrumentos ({fid}) planeja todos",
            len(declarados) > 1 and planejados(d, fid) == declarados,
            f"declarados {sorted(declarados)}, planejados {sorted(planejados(d, fid))}")

    # Instrumento retirado: a faceta sai da coluna FCTs da linha dele, na cópia do texto.
    if len(por_faceta[fid]) < 2:
        g.falha(f"instrumento retirado de {fid}: a faceta não tem dois instrumentos para "
                f"retirar um")
    else:
        sigla = por_faceta[fid][-1]["sigla"]
        idx, cab = L["instrumento"][sigla], L["cabecalho_instrumentos"]
        k = coluna(t, cab, G.T_INSTRUMENTOS.colunas[5])
        mutante = troca_celula(t, idx, k, ", ".join(
            f for f in lista(celula(t, idx, k)) if f != fid))
        dm = ctx.com_texto(mutante).protocolo()
        g.testa(f"faceta {fid} retirada da coluna FCTs de {sigla}: {sigla} não é planejado",
                mutante != t and sigla not in planejados(dm, fid)
                and planejados(dm, fid) == planejados(d, fid) - {sigla},
                f"planejados {sorted(planejados(dm, fid))}")

    # Filtro por idioma: um instrumento passa a cobrir só um dos idiomas.
    dm = copy.deepcopy(d)
    inst = dm["instrumentos_por_faceta"][fid][0]
    so = inst["idiomas"][0]
    inst["idiomas"] = [so]
    fora = [i for i in dm["idiomas"] if i != so]
    g.testa(f"{inst['sigla']} restrito a {so} só é planejado em {so}",
            bool(fora)
            and inst["sigla"] in {i["sigla"] for i in instrumentos_do_termo(dm, fid, so)}
            and all(inst["sigla"] not in {i["sigla"] for i in instrumentos_do_termo(dm, fid, x)}
                    for x in fora))

    # Modo manual: um instrumento automático declarado Manual nasce pendente.
    dm = copy.deepcopy(d)
    autos = [i for i in dm["instrumentos_por_faceta"][fid] if i["modo"] != G.MODO_MANUAL]
    if not autos:
        g.falha(f"instrumento manual em {fid}: nenhum instrumento automático")
    else:
        autos[0]["modo"] = G.MODO_MANUAL
        plano = [i for idioma in dm["idiomas"] for i in instrumentos_do_termo(dm, fid, idioma)
                 if i["sigla"] == autos[0]["sigla"]]
        g.testa(f"{autos[0]['sigla']} declarado {G.MODO_MANUAL} nasce pendente de validação "
                f"manual", bool(plano) and all(
                    i["modo"] == G.MODO_MANUAL
                    and estado_inicial(i).get("status_proposto") == STATUS_MANUAL
                    for i in plano))
    manuais = [i for i in d["instrumentos"].values() if i["modo"] == G.MODO_MANUAL]
    g.testa("instrumento manual do protocolo nasce pendente e o automático não",
            bool(manuais)
            and all(estado_inicial(i).get("status_proposto") == STATUS_MANUAL for i in manuais)
            and all(estado_inicial(i).get("status_proposto") != STATUS_MANUAL
                    for i in d["instrumentos"].values() if i["modo"] != G.MODO_MANUAL))
