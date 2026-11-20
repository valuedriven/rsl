"""Autoteste da busca: a prova da composição reprova cada relação quebrada, e a aderência é
relatada por papel, com o intervalo de Wilson."""

import copy

from .. import gramatica as G
from ..busca.aderencia import avalia_aderencia, casa_titulo, chave_titulo, wilson
from ..busca.composicao import grupos_em_facetas, prova_da_composicao
from ..leitura import papeis


def composicao(ctx, g):
    """Cada defeito é injetado numa cópia da composição lida (em STRn, como no protocolo);
    os papéis são recalculados sobre a cópia, como a leitura faria, e a prova tem de
    reprovar pelo motivo esperado. Os identificadores vêm dos papéis do protocolo."""
    d = ctx.protocolo()
    p = d["papeis"]
    exec_, sonda, ancoras = p["executada"], p["sonda"], p["ancoras"]
    faceta_de = {v["id"]: fid for fid, v in d["strings"].items()}

    def prova(expressoes):
        dm = copy.deepcopy(d)
        dm["expressoes"] = expressoes
        return prova_da_composicao(grupos_em_facetas(expressoes, faceta_de), papeis(dm),
                                   faceta_de)

    def testa(nome, expressoes, espera):
        if expressoes == d["expressoes"]:
            g.falha(f"mutação não aplicada: {nome}")
            return
        achados = [x for x in prova(expressoes) if espera in x]
        if achados:
            g.ok(f"reprovou: {nome} — {achados[0][:88]}")
        else:
            g.falha(f"não reprovou pelo motivo esperado ({espera!r}): {nome}")

    controle = prova(copy.deepcopy(d["expressoes"]))
    g.testa("composição do protocolo aprovada pela prova", not controle,
            controle[0][:80] if controle else "")
    if not p["especificas"] or not p["gerais"]:
        g.falha(f"o protocolo não tem específica e geral para mutar: {p}")
        return
    uma = sorted(p["especificas"].values())[0]
    geral = sorted(p["gerais"])[0]

    m = copy.deepcopy(d["expressoes"])
    m[exec_] = ancoras + [[uma]]
    testa(f"executada {exec_} reduzida a uma só específica ({uma})", m, f"{exec_} ≠ ")
    # A falha nomeia a combinação de facetas em que a relação não vale.
    g.testa("a reprovação da executada nomeia a combinação de facetas",
            any(" em [" in x for x in prova(m) if f"{exec_} ≠ " in x))
    m = copy.deepcopy(d["expressoes"])
    m[sonda] = ancoras + [[uma]]
    testa(f"sonda {sonda} restrita por {uma}", m, f"{sonda} não contém")
    m = copy.deepcopy(d["expressoes"])
    m[geral] = [x for x in m[geral] if x != ancoras[-1]]
    testa(f"geral {geral} sem a âncora {ancoras[-1][0]}", m, "não está contida")
    m = copy.deepcopy(d["expressoes"])
    m["MUT1"] = copy.deepcopy(ancoras)
    testa("expressão a mais fora da executada", m, "deriváveis de")


def aderencia(ctx, g):
    """Relato por papel e intervalo de Wilson, com dados sintéticos."""
    lo, hi = wilson(8, 10)
    g.testa("Wilson 8/10 = 80% com intervalo 49,0%–94,3%",
            abs(lo - 0.490) < 0.001 and abs(hi - 0.943) < 0.001, f"{lo:.3%}–{hi:.3%}")
    g.testa("Wilson sem tentativa não tem intervalo", wilson(0, 0) is None)

    idx = {chave_titulo("Um título completo para o teste"): [{"base": "x"}]}
    exatas, prefixo = casa_titulo(idx, chave_titulo("Um título completo para o teste"))
    g.testa("título exato é recuperação", bool(exatas) and not prefixo)
    exatas, prefixo = casa_titulo(idx, chave_titulo("Um título completo"))
    g.testa("prefixo é indício, não recuperação", not exatas and bool(prefixo))

    val, dev = G.PAPEL_VALIDACAO, G.PAPEL_DESENVOLVIMENTO
    sementes = ([{"id": f"V{k}", "papel": val} for k in range(1, 7)]
                + [{"id": f"D{k}", "papel": dev} for k in range(1, 5)])
    recuperadas = {f"V{k}" for k in range(1, 6)} | {f"D{k}" for k in range(1, 5)}
    av = avalia_aderencia(sementes, recuperadas, limiar=0.8)
    v, dv = av["decide"], av["por_papel"][dev]
    g.testa("5/6 de validação e 4/4 de desenvolvimento são relatados separados",
            v["recuperadas"] == 5 and v["total"] == 6
            and dv["recuperadas"] == 4 and dv["total"] == 4,
            f"validação {v['recuperadas']}/{v['total']}, "
            f"desenvolvimento {dv['recuperadas']}/{dv['total']}")
    g.testa("total recuperado independe do papel",
            sum(x["recuperadas"] for x in av["por_papel"].values()) == len(recuperadas))
    # 4/6 de validação = 66,7%; 4/4 de desenvolvimento leva o total a 80%, mas o
    # desenvolvimento não compensa: a validação continua abaixo do limiar.
    recuperadas = {f"V{k}" for k in range(1, 5)} | {f"D{k}" for k in range(1, 5)}
    av = avalia_aderencia(sementes, recuperadas, limiar=0.8)
    g.testa("desenvolvimento não compensa validação",
            av["decide"]["recuperadas"] == 4 and av["decide"]["total"] == 6
            and not av["decide"]["aprovada"] and av["por_papel"][dev]["proporcao"] == 1.0,
            f"validação {av['decide']['proporcao']:.1%}")
