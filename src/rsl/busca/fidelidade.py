"""Teste de fidelidade: o conjunto derivado localmente comparado com a execução direta da
mesma expressão na base."""

import csv
import pathlib

from ..config import relativo
from ..erros import DadosInvalidos, Uso
from ..saida import Saida
from . import Busca
from .composicao import satisfaz_em
from .derivacao import carrega_facetas, facetas_atingidas
from .leitores import le_arquivo
from .registro import chave_dedup, coleta, consultas_do_corpus, identifica


def fidelidade(b, expr, caminho):
    ident = b.exige_expressao(expr)
    if ident == b.sonda:
        raise Uso(f"{b.sonda} é a sonda de sensibilidade, não expressão de conferência: o "
                  f"conjunto dela é superconjunto de {b.executada} e não se deriva da "
                  f"exportação da executada. Use  python3 -m rsl conferencia sensibilidade <base>.")
    arq = pathlib.Path(caminho)
    if not arq.exists():
        raise DadosInvalidos(f"Arquivo não encontrado: {arq}")

    direto = {chave_dedup(r) for r in le_arquivo(arq)}
    if not direto:
        raise DadosInvalidos("Nenhum registro lido do arquivo de conferência.")

    lidas = consultas_do_corpus(b)
    facetas = carrega_facetas(b, (c["base"] for c in lidas))
    derivado = set()
    for r in identifica(coleta(lidas)):
        if r["duplicata_de"]:
            continue
        fac = facetas_atingidas(r, facetas)
        if satisfaz_em(b.grupos, ident, fac):
            derivado.add(chave_dedup(r))

    so_direto = direto - derivado
    so_derivado = derivado - direto
    uniao = direto | derivado
    div = (len(so_direto) + len(so_derivado)) / len(uniao) if uniao else 0

    print(f"\nTESTE DE FIDELIDADE — {ident}")
    print(f"  execução direta na base : {len(direto)}")
    print(f"  conjunto derivado       : {len(derivado)}")
    print(f"  só na execução direta   : {len(so_direto)}")
    print(f"  só no conjunto derivado : {len(so_derivado)}")
    print(f"  divergência simétrica   : {div:.1%}  (limite: {b.limite_divergencia:.0%})")
    rel = b.config.saida("fidelidade", expressao=ident)
    rel.parent.mkdir(parents=True, exist_ok=True)
    with rel.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["chave", "situacao"])
        for k in sorted(so_direto):
            w.writerow([k, "só na execução direta"])
        for k in sorted(so_derivado):
            w.writerow([k, "só no conjunto derivado"])
    print(f"  divergências listadas em {relativo(rel)}")
    if div > b.limite_divergencia:
        print("\n  REPROVADO. A derivação não pode ser aceita: volte às execuções separadas "
              "por expressão e registre emenda ao protocolo.")
        return Saida.REPROVADO
    print("\n  APROVADO para esta expressão. Repita para a outra expressão de conferência "
          "antes de aceitar as contagens derivadas.")
    return Saida.OK


def cmd_fidelidade(ctx, a):
    return fidelidade(Busca(ctx), a.expressao, a.arquivo)
