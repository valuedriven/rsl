"""Autoteste do planejamento da validação terminológica por instrumento."""

import copy

from .. import gramatica as G
from ..leitura import instrumentos_do_termo
from ..markdown import lista
from ..termos.clientes.tbci import item_exato
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


    # Cliente do TBCI: o identificador vem do item que casou, e não do primeiro da resposta.
    # A resposta põe de propósito o outro conceito antes do que casa.
    resposta = {"result": {
        "1": {"term_id": 157, "string": "sistemas de organização do conhecimento"},
        "2": {"term_id": 613, "string": "organização do conhecimento"}}}
    achado = item_exato(resposta, "organização do conhecimento")
    g.testa("tbci: identificador do item que casou, não o primeiro da resposta",
            achado == ("organização do conhecimento", "613"), f"devolveu {achado}")
    g.testa("tbci: sem casamento exato não há identificador",
            item_exato(resposta, "conhecimento") == (None, None))

# ------------------------------------------------- decisão do ReT e linha do termo no CT
def _planilha(linhas):
    """Texto CSV mínimo da planilha de validação, com as colunas exigidas."""
    from ..termos.decisao import COLUNAS_EXIGIDAS                   # noqa: PLC0415
    colunas = list(COLUNAS_EXIGIDAS) + ["status_proposto"]
    corpo = [";".join(colunas)]
    corpo += [";".join(r.get(c, "") for c in colunas) for r in linhas]
    return "\n".join(corpo) + "\n"


def classificacao(ctx, g):
    """Domínio de `decisao_ReT`, regra da linha esperada e conferência cruzada CT × planilha,
    sobre planilhas em memória e cópias do protocolo. Tudo gerado da estrutura lida: o
    primeiro termo livre da primeira faceta, os instrumentos planejados para ele."""
    from ..conferencia import conferir                              # noqa: PLC0415
    from ..saida import Saida                                       # noqa: PLC0415
    from ..termos.decisao import (esperada, fora_do_dominio, le_planilha,  # noqa: PLC0415
                                  linhas_esperadas)
    from . import resultado                                         # noqa: PLC0415
    from .textos import edita_celula                                # noqa: PLC0415
    t, d = ctx.texto, ctx.protocolo()
    L = d["locais"]
    livre, desc, rel = (r.interno for r in G.LINHAS_CT)
    # Um termo com dois instrumentos planejados, para provar a precedência entre eles.
    alvo = None
    for f in d["tabelas"]:
        for i in d["idiomas"]:
            insts = [x["sigla"] for x in instrumentos_do_termo(d, f["id"], i)]
            if f["linhas"][i][livre] and len(insts) > 1:
                alvo = (f, i, f["linhas"][i][livre][0], insts)
                break
        if alvo:
            break
    if alvo is None:
        g.falha("nenhum termo com dois instrumentos planejados: a precedência não é provada")
        return
    f, idioma, termo, insts = alvo
    fid = f["id"]
    nao_planejado = next((s for s in d["instrumentos"] if s not in insts), None)

    def linha(decisoes, status=None):
        rs = [{"faceta": fid, "idioma": idioma, "termo": termo, "instrumento": s,
               "decisao_ReT": v, "status_proposto": (status or {}).get(s, "")}
              for s, v in decisoes.items()]
        return esperada(linhas_esperadas(d, rs), fid, idioma, termo)

    a, b = insts[0], insts[1]
    g.testa("precedência: descritor num instrumento e sinônimo noutro → descritores",
            linha({a: "sinônimo ou relacionado", b: "descritor"}) == desc)
    g.testa("descritor num instrumento e termo livre noutro → descritores",
            linha({a: "descritor", b: "termo livre"}) == desc)
    g.testa("só sinônimo ou relacionado → relacionados",
            linha({a: "sinônimo ou relacionado"}) == rel)
    g.testa("decisão com outra caixa (`Descritor`) é lida como descritor",
            linha({a: "Descritor"}) == desc)
    g.testa("pendência manual sem decisão → livre",
            linha({a: ""}, {a: STATUS_MANUAL}) == livre)
    g.testa("proposta da máquina sem decisão do ReT → livre",
            linha({a: ""}, {a: "descritor autorizado (a conferir pelo ReT)"}) == livre)
    g.testa("planilha ausente → livre", esperada(linhas_esperadas(d, None), fid, idioma,
                                                termo) == livre)
    if nao_planejado:
        g.testa(f"decisão em instrumento não planejado para o termo ({nao_planejado}) não "
                f"classifica", linha({nao_planejado: "descritor"}) == livre)
    fora = [{"faceta": fid, "idioma": idioma, "termo": termo, "instrumento": a,
             "decisao_ReT": "autorizado"}]
    g.testa("valor fora do domínio é reprovado (o que `termos importar` usa)",
            bool(fora_do_dominio(fora)) and "autorizado" in fora_do_dominio(fora)[0])
    cod, msgs = resultado(lambda: le_planilha("faceta;termo\nFCT1;x\n", "planilha"))
    g.testa("planilha sem as colunas exigidas é ilegível (DADOS)", cod == Saida.DADOS,
            f"{cod.name} {msgs[:1]}")

    # Conferência cruzada: cópias do protocolo e planilhas em memória.
    q = L["quadro"][fid]
    k = coluna(t, q["cabecalho"], idioma)
    movido = edita_celula(edita_celula(t, q[livre], k,
                                       lambda c: ", ".join(x.strip() for x in c.split(",")
                                                           if x.strip() != termo)),
                          q[desc], k, lambda c: termo)

    def com(texto, plan):
        return lambda m: conferir(ctx.com_texto(m).com_validacao(texto if plan is None
                                                                   else _planilha(plan)))
    decide = [{"faceta": fid, "idioma": idioma, "termo": termo, "instrumento": a,
               "decisao_ReT": "descritor"}]
    R = Saida.REPROVADO
    g.espera("termo sem decisão movido para Descritores, sem planilha", movido, t,
             com(None, None), R, (repr(termo), "a linha esperada é 'Termo livre'"))
    g.espera("termo sem decisão movido para Descritores, com planilha sem decisão", movido, t,
             com(None, [{**decide[0], "decisao_ReT": ""}]), R,
             (repr(termo), "a linha esperada é 'Termo livre'", "pela decisão do ReT"))
    g.espera("descritor decidido ainda em Termo livre", t + "\n", t,
             com(None, decide), R,
             (repr(termo), f"a linha esperada é {G.R_DESCRITORES.texto!r}"))
    # Reclassificado, o termo muda de posição na STR: a única reprovação é a da ordem, que
    # `strings gerar --gravar` corrige ("Termo reclassificado", geracao-das-strings).
    cod, msgs = resultado(lambda: com(None, decide)(movido))
    g.testa("descritor decidido na linha de descritores: nenhuma reprovação de classificação, "
            "só a STR em outra ordem",
            bool(msgs) and all("ordem diferente" in m for m in msgs), f"{cod.name} {msgs[:2]}")
    g.espera("decisão fora do domínio na planilha", t + "\n", t,
             com(None, [{**decide[0], "decisao_ReT": "autorizado"}]), R,
             ("fora do domínio", "'autorizado'", repr(termo)))
    g.espera("planilha ilegível", t + "\n", t,
             lambda m: conferir(ctx.com_texto(m).com_validacao("faceta;termo\nx;y\n")),
             Saida.DADOS, "ilegível")
    repetido = edita_celula(t, q[desc], k, lambda c: termo)
    g.espera("termo em duas linhas do mesmo CT e idioma", repetido, t, com(None, None), R,
             (repr(termo), "mais de uma linha", f["ct"]))
    outro = next((i for i in d["idiomas"] if i != idioma), None)
    if outro:
        k2 = coluna(t, q["cabecalho"], outro)
        mesma = edita_celula(t, q[livre], k2, lambda c: f"{c}, {termo}" if c else termo)
        cod, msgs = resultado(lambda: conferir(ctx.com_texto(mesma).com_validacao(None)))
        g.testa("mesma forma em Termo livre de dois idiomas não reprova por repetição",
                mesma != t and not any("mais de uma linha" in m for m in msgs),
                f"{msgs[:1]}")
    # Célula vazia admitida: o próprio documento corrente, aprovado para o autoteste rodar,
    # tem de ter alguma célula vazia; senão o caso não prova nada e falha.
    vazias = [(x["id"], i, c) for x in d["tabelas"] for i in d["idiomas"]
              for c in (desc, rel) if not x["linhas"][i][c]]
    cod, msgs = resultado(lambda: conferir(ctx))
    g.testa("célula vazia no CT não reprova (documento corrente com células vazias aprova)",
            bool(vazias) and cod == Saida.OK, f"{len(vazias)} vazias, {cod.name} {msgs[:1]}")
