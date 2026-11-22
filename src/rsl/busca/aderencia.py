"""Teste de aderência ao conjunto-semente, por papel, sobre as consultas registradas."""

import math

from .. import gramatica as G
from ..markdown import normaliza
from ..saida import Saida
from ..sementes import COL_INDEXADA, COL_RECUPERADA
from . import Busca
from .registro import carrega_consultas, coleta, exige_registros, identifica


def chave_titulo(t):
    """Título normalizado para casamento: sem acento, caixa ou pontuação."""
    return normaliza(t)


def casa_titulo(idx, chave):
    """Casamento exato e candidatos por prefixo. Prefixo é indício, não recuperação."""
    if not chave:
        return [], []
    exatas = idx.get(chave)
    if exatas:
        return exatas, []
    prefixo = [r for k, v in idx.items() if k.startswith(chave[:60]) for r in v]
    return [], prefixo


def wilson(k, n, z=1.96):
    """Intervalo de Wilson a 95% para k sucessos em n tentativas.

    Com n pequeno e proporção perto de 1, o intervalo normal sai assimétrico de forma
    errada e ultrapassa 100%; o Wilson tem cobertura adequada nessa faixa e usa só a
    biblioteca padrão.
    """
    if n <= 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / denom
    meio = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, centro - meio), min(1.0, centro + meio)


def avalia_aderencia(sementes, recuperadas, limiar):
    """Contagem e decisão por papel. `recuperadas` é o conjunto de IDs recuperados.

    Só a validação é comparada ao limiar; o desenvolvimento é relatado como não
    decisório e não compensa a validação.
    """
    por_papel = {p: {"total": 0, "recuperadas": 0, "ids": []}
                 for p in G.D_PAPEL.valores.values()}
    for e in sementes:
        p = e["papel"]
        por_papel[p]["total"] += 1
        if e["id"] in recuperadas:
            por_papel[p]["recuperadas"] += 1
            por_papel[p]["ids"].append(e["id"])
    for p in por_papel:
        total = por_papel[p]["total"]
        por_papel[p]["proporcao"] = por_papel[p]["recuperadas"] / total if total else 0.0
    val = por_papel[G.PAPEL_VALIDACAO]
    val["intervalo"] = wilson(val["recuperadas"], val["total"])
    val["aprovada"] = val["total"] > 0 and val["proporcao"] >= limiar
    return {"por_papel": por_papel, "decide": val, "limiar": limiar}


def aderencia(b):
    """Mede recall: quantos dos estudos-semente aparecem na exportação. NÃO aplica o
    recorte temporal — o conjunto-semente valida o desenho da busca, não os critérios de
    elegibilidade.

    Relata validação e desenvolvimento separadamente. Só a validação é comparada ao
    limiar e traz o intervalo de Wilson a 95%; o desenvolvimento é não decisório e não
    compensa a validação. A coluna de indexação da planilha de aderência
    (`sementes.COL_INDEXADA`) é o denominador definitivo e precisa ser preenchida à mão,
    base por base, buscando cada semente pelo título: ausência por falta de indexação não é
    falha da string.

    Sai com REPROVADO só quando não há semente de validação (sem denominador); a aderência
    abaixo do limiar é relatada, porque o denominador definitivo é o da planilha.
    """
    sementes = b.d["sementes"]
    _, validas = carrega_consultas(b)
    regs = [r for r in exige_registros(identifica(coleta(validas))) if not r["duplicata_de"]]

    idx = {}
    for r in regs:
        idx.setdefault(chave_titulo(r.get("titulo")), []).append(r)

    print(f"\nADERÊNCIA AO CONJUNTO-SEMENTE — {len(sementes)} estudos, "
          f"{len(regs)} registros únicos\n")
    recuperadas, indicios = set(), set()
    for e in sementes:
        k = chave_titulo(e["titulo"])
        exatas, prefixo = casa_titulo(idx, k)
        if exatas:
            recuperadas.add(e["id"])
            bases = ", ".join(sorted({r.get("base", "?") for r in exatas}))
            print(f"  [OK ] {e['id']:>4}. {e['ano']} [{e['papel']}] "
                  f"{e['titulo'][:48]:<50} {bases}")
        elif prefixo:
            indicios.add(e["id"])
            bases = ", ".join(sorted({r.get("base", "?") for r in prefixo}))
            print(f"  [? ] {e['id']:>4}. {e['ano']} [{e['papel']}] "
                  f"{e['titulo'][:48]:<50} {bases} — prefixo; conferir à mão")
        else:
            print(f"  [   ] {e['id']:>4}. {e['ano']} [{e['papel']}] "
                  f"{e['titulo'][:48]:<50} esperado em: {', '.join(e['bases'])}")

    av = avalia_aderencia(sementes, recuperadas, b.d["limiar"])
    val, dev = av["decide"], av["por_papel"][G.PAPEL_DESENVOLVIMENTO]
    print(f"\n  TOTAL — {len(recuperadas)}/{len(sementes)} sementes recuperadas "
          f"({len(recuperadas) / len(sementes):.0%}); informativo, não decide")
    print(f"\n  ADERÊNCIA DE VALIDAÇÃO — {val['recuperadas']}/{val['total']} = "
          f"{val['proporcao']:.1%}")
    if val["intervalo"]:
        lo, hi = val["intervalo"]
        print(f"    intervalo de Wilson a 95%: {lo:.1%}–{hi:.1%}")
    else:
        print("    sem sementes de validação: a aderência não tem denominador")
    print(f"    limiar do protocolo: {av['limiar']:.0%} — "
          f"{'APROVADA' if val['aprovada'] else 'REPROVADA'}; esta é a aderência que "
          f"decide a passagem")
    print(f"\n  ADERÊNCIA DE DESENVOLVIMENTO — {dev['recuperadas']}/{dev['total']} = "
          f"{dev['proporcao']:.1%}")
    print("    não decisória: não compensa a validação nem altera a passagem")
    if indicios:
        print(f"\n  INDÍCIO POR PREFIXO — {len(indicios)} semente(s) NÃO contabilizada(s): "
              f"{', '.join(sorted(indicios))}")
        print(f"    prefixo não é acerto: conferir à mão e registrar na coluna "
              f"`{COL_RECUPERADA}`.")
    print("\n  ATENÇÃO: a razão acima é sobre as sementes informadas. O denominador definitivo")
    print(f"  são as sementes que cada base INDEXA, apurado à mão na coluna `{COL_INDEXADA}`")
    print("  da planilha. Semente ausente por não ser indexada não conta contra a string.")
    print("  Cada ausência acima exige diagnóstico: qual termo a teria alcançado?")
    return Saida.OK if val["total"] else Saida.REPROVADO


def cmd_aderencia(ctx, a=None):
    return aderencia(Busca(ctx))
