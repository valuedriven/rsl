"""Derivação local: a pertinência de cada registro da exportação da executada às demais
expressões, as contagens da busca e a ordem de triagem."""

import csv
import re

from ..config import relativo
from ..markdown import normaliza
from ..saida import Saida
from . import Busca
from .composicao import satisfaz_em
from .leitores import CAMPOS
from .registro import aplica_recorte, carrega_consultas, coleta, exige_registros, identifica


def padrao(termo):
    """Casamento por palavra inteira, com flexão simples de plural.

    O '*' do termo vira prefixo livre. Cada palavra admite sufixo de plural
    opcional (s/es), o que aproxima — sem reproduzir — a lematização que as bases
    aplicam em TS= e TITLE-ABS-KEY. É justamente essa aproximação que o teste de
    fidelidade mede: ela é a origem esperada da divergência."""
    t = normaliza(termo.replace("*", "\x00"))
    partes = []
    for palavra in t.split():
        if "\x00" in palavra:
            partes.append(re.escape(palavra).replace("\x00", r"\w*"))
        else:
            partes.append(re.escape(palavra) + r"(?:e?s)?")
    return re.compile(r"(?<!\w)" + r"\s+".join(partes) + r"(?!\w)")


def carrega_facetas(b):
    """Facetas e padrões de casamento, da lista executada de cada faceta no protocolo."""
    facetas = {}
    for fid, v in b.d["strings"].items():
        vistos, limpos = set(), []
        for t in v["termos"]:
            k = t.lower()
            if k not in vistos:
                vistos.add(k)
                limpos.append(t)
        nome = next((f["nome"] for f in b.d["facetas"] if f["id"] == fid), "")
        facetas[fid] = {"nome": nome, "termos": limpos,
                        "padroes": [padrao(t) for t in limpos]}
    return facetas


def texto_do(reg):
    return normaliza(" ".join((reg["titulo"], reg["resumo"], reg["palavras_chave"])))


def facetas_atingidas(reg, facetas):
    alvo = texto_do(reg)
    return {n for n, f in facetas.items() if any(p.search(alvo) for p in f["padroes"])}


def expressoes_de(b, fac):
    """Expressões do corpus a que o registro pertence — a sonda fica de fora.

    A sonda não compõe o corpus e só se mede contra a exportação própria; listá-la aqui
    diria que todo registro da executada pertence a ela, o que é verdade e não informa nada.
    """
    return [n for n in b.grupos if n != b.sonda and satisfaz_em(b.grupos, n, fac)]


def chave_ordem(b, reg, exprs):
    """Ordem de leitura da 1ª filtragem: pertinência às expressões ricas primeiro, depois
    recência (`[busca] ano_recencia`), depois o ano.

    Riqueza é o número de grupos de facetas exigidos pela expressão mais rica atingida.
    É a ordem de leitura, não critério de elegibilidade."""
    riqueza = max((len(b.grupos[e]) for e in exprs), default=0)
    try:
        ano = int(re.search(r"(19|20)\d{2}", reg["ano"] or "").group(0))
    except Exception:                                               # noqa: BLE001
        ano = 0
    recente = 1 if ano >= b.config.valor("busca.ano_recencia") else 0
    return (-riqueza, -recente, -ano)


def derivar(b):
    facetas = carrega_facetas(b)
    _, validas = carrega_consultas(b)
    print("Lendo exportações registradas:")
    regs = exige_registros(identifica(coleta(validas)))
    regs, fora = aplica_recorte(b, regs)
    unicos = [r for r in regs if not r["duplicata_de"]]

    destinos = {k: b.config.saida(k) for k in ("registros", "contagens", "ordem_triagem")}
    for p in destinos.values():
        p.parent.mkdir(parents=True, exist_ok=True)
    por_registro = {}
    for r in regs:
        fac = facetas_atingidas(r, facetas)
        exprs = expressoes_de(b, fac)
        if b.executada not in exprs:
            # O registro veio da executada na base, mas o casamento local não confirma as
            # âncoras: é divergência esperada (Keywords Plus, lematização), não descarte.
            exprs = sorted(set(exprs) | {b.executada})
        por_registro[r["registro"]] = (fac, exprs, chave_ordem(b, r, exprs))

    unicos.sort(key=lambda r: por_registro[r["registro"]][2])
    ordem = {}
    for i, r in enumerate(unicos, 1):
        ordem[r["registro"]] = i
    linhas = unicos + [r for r in regs if r["duplicata_de"]]

    contagens, brutas = {}, {}
    for r in unicos:
        for n in por_registro[r["registro"]][1]:
            contagens[(r["base"], n)] = contagens.get((r["base"], n), 0) + 1
    for r in regs:
        for n in por_registro[r["registro"]][1]:
            brutas[(r["base"], n)] = brutas.get((r["base"], n), 0) + 1

    cols = list(CAMPOS) + ["base", "arquivo_origem", "consulta", "registro", "duplicata_de",
                           "facetas", "expressoes", "ancoras_confirmadas", "recorte", "ordem"]
    with destinos["registros"].open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter=";")
        w.writeheader()
        for r in linhas:
            fac, exprs, _ = por_registro[r["registro"]]
            w.writerow({**{k: r[k] for k in CAMPOS},
                        "base": r["base"], "arquivo_origem": r["arquivo_origem"],
                        "consulta": r["consulta"], "registro": r["registro"],
                        "duplicata_de": r["duplicata_de"],
                        "facetas": " ".join(sorted(fac)),
                        "expressoes": " ".join(sorted(exprs)),
                        "ancoras_confirmadas": "sim" if b.ancoras <= fac else "não",
                        "recorte": r.get("recorte", ""),
                        "ordem": ordem.get(r["registro"], "")})

    bases = sorted({r["base"] for r in regs})
    with destinos["contagens"].open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["base", "expressao", "facetas_exigidas", "registros",
                    "registros_com_duplicatas", "procedencia"])
        for base in bases:
            for n in sorted(b.grupos):
                composicao = " AND ".join(
                    grupo[0] if len(grupo) == 1 else "(" + " OR ".join(grupo) + ")"
                    for grupo in b.grupos[n])
                if n == b.sonda:
                    w.writerow([base, n, composicao, "", "",
                                "SONDA — fora do corpus, executada à parte"])
                elif n == b.executada:
                    w.writerow([base, n, composicao, contagens.get((base, n), 0),
                                brutas.get((base, n), 0), "EXECUTADA"])
                else:
                    w.writerow([base, n, composicao, contagens.get((base, n), 0),
                                brutas.get((base, n), 0), "DERIVADA"])

    with destinos["ordem_triagem"].open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["ordem", "base", "ano", "expressoes", "titulo", "doi"])
        for r in unicos:
            _, exprs, _ = por_registro[r["registro"]]
            w.writerow([ordem[r["registro"]], r["base"], r["ano"],
                        " ".join(sorted(exprs)), r["titulo"], r["doi"]])

    print(f"\n{len(linhas)} registros processados, {len(unicos)} únicos.")
    print(", ".join(relativo(p) for p in destinos.values()) + " gravados.")
    sem_ancora = sum(1 for r in unicos if not (b.ancoras <= por_registro[r["registro"]][0]))
    if sem_ancora:
        pct = 100 * sem_ancora / len(unicos)
        print(f"\nAVISO: em {sem_ancora} registros ({pct:.1f}%) o casamento local não confirmou "
              "as âncoras. É divergência esperada — a base casou por Keywords Plus ou por "
              "lematização. Nenhum registro foi descartado. Se esse percentual for alto, o teste "
              "de fidelidade tende a reprovar.")
    print("\nAs contagens das expressões não executadas são DERIVADAS. Declará-las como tal "
          "nas contagens da busca e no relatório, "
          "e só aceitá-las após o teste de fidelidade (busca fidelidade).")
    return Saida.OK


def cmd_derivar(ctx, a=None):
    return derivar(Busca(ctx))
