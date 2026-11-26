"""Teste de aderência ao conjunto-semente, sobre as consultas registradas."""

import math

from ..markdown import normaliza
from ..saida import Saida
from ..sementes import COL_INDEXADA, COL_RECUPERADA
from . import Busca
from .registro import coleta, consultas_do_corpus, exige_registros, identifica


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
    """Contagem e decisão sobre o conjunto. `recuperadas` é o conjunto de IDs recuperados.

    Um numerador e um denominador: a proporção, o intervalo de Wilson a 95% sobre eles e a
    comparação com o limiar, que é a que decide a passagem.
    """
    ids = [e["id"] for e in sementes if e["id"] in recuperadas]
    total = len(sementes)
    proporcao = len(ids) / total if total else 0.0
    return {"total": total, "recuperadas": len(ids), "ids": ids, "proporcao": proporcao,
            "intervalo": wilson(len(ids), total),
            "aprovada": total > 0 and proporcao >= limiar, "limiar": limiar}


def registros_unicos(b):
    """Registros únicos do corpus: só as execuções da executada, com o relato das lidas."""
    return [r for r in exige_registros(identifica(coleta(consultas_do_corpus(b))))
            if not r["duplicata_de"]]


def casa_sementes(sementes, regs):
    """[(semente, casamentos exatos, candidatos por prefixo)], na ordem das sementes."""
    idx = {}
    for r in regs:
        idx.setdefault(chave_titulo(r.get("titulo")), []).append(r)
    return [(e, *casa_titulo(idx, chave_titulo(e["titulo"]))) for e in sementes]


def aderencia(b):
    """Mede recall: quantos dos estudos-semente aparecem na exportação. NÃO aplica o
    recorte temporal — o conjunto-semente valida o desenho da busca, não os critérios de
    elegibilidade.

    Relata uma única aderência, sobre o conjunto, com o intervalo de Wilson a 95%, e a
    compara ao limiar: é a que decide a passagem. A coluna de indexação da planilha de
    aderência (`sementes.COL_INDEXADA`) é o denominador definitivo e precisa ser preenchida
    à mão, base por base, buscando cada semente pelo título: ausência por falta de
    indexação não é falha da string.

    A aderência abaixo do limiar é relatada, sem reprovar, porque o denominador definitivo
    é o da planilha; o conjunto vazio já reprova na leitura do arquivo de sementes.
    """
    sementes = b.d["sementes"]
    regs = registros_unicos(b)

    print(f"\nADERÊNCIA AO CONJUNTO-SEMENTE — {len(sementes)} estudos, "
          f"{len(regs)} registros únicos\n")
    recuperadas, indicios = set(), set()
    for e, exatas, prefixo in casa_sementes(sementes, regs):
        if exatas:
            recuperadas.add(e["id"])
            bases = ", ".join(sorted({r.get("base", "?") for r in exatas}))
            print(f"  [OK ] {e['id']:>4}. {e['ano']} "
                  f"{e['titulo'][:48]:<50} {bases}")
        elif prefixo:
            indicios.add(e["id"])
            bases = ", ".join(sorted({r.get("base", "?") for r in prefixo}))
            print(f"  [? ] {e['id']:>4}. {e['ano']} "
                  f"{e['titulo'][:48]:<50} {bases} — prefixo; conferir à mão")
        else:
            print(f"  [   ] {e['id']:>4}. {e['ano']} "
                  f"{e['titulo'][:48]:<50} esperado em: {', '.join(e['bases'])}")

    av = avalia_aderencia(sementes, recuperadas, b.d["limiar"])
    print(f"\n  ADERÊNCIA — {av['recuperadas']}/{av['total']} sementes recuperadas = "
          f"{av['proporcao']:.1%}")
    lo, hi = av["intervalo"]
    print(f"    intervalo de Wilson a 95%: {lo:.1%}–{hi:.1%}")
    print(f"    limiar do protocolo: {av['limiar']:.0%} — "
          f"{'APROVADA' if av['aprovada'] else 'REPROVADA'}; esta é a aderência que "
          f"decide a passagem")
    if indicios:
        print(f"\n  INDÍCIO POR PREFIXO — {len(indicios)} semente(s) NÃO contabilizada(s): "
              f"{', '.join(sorted(indicios))}")
        print(f"    prefixo não é acerto: conferir à mão e registrar na coluna "
              f"`{COL_RECUPERADA}`.")
    print("\n  ATENÇÃO: a razão acima é sobre as sementes informadas. O denominador definitivo")
    print(f"  são as sementes que cada base INDEXA, apurado à mão na coluna `{COL_INDEXADA}`")
    print("  da planilha. Semente ausente por não ser indexada não conta contra a string.")
    print("  Cada ausência acima exige diagnóstico: qual termo a teria alcançado?")
    return Saida.OK


def cmd_aderencia(ctx, a=None):
    return aderencia(Busca(ctx))
