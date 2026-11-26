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
from ..dados import CMD_REGISTRAR
from .registro import (carrega_consultas, chave_dedup, coleta, consultas_do_corpus,
                       identifica)
from .sensibilidade import registros_da_expressao


def fidelidade(b, base, expr, caminho=None):
    """Compara, numa base, a execução direta de uma expressão de conferência com o conjunto
    derivado das exportações da executada DAQUELA base. A base é argumento obrigatório: o
    corpus de outra base não entra no derivado, porque a execução direta só pode conter
    registros da sua própria base, e os da outra contariam como divergência.

    Sem ARQUIVO, a execução direta são as exportações registradas da expressão na base."""
    ident = b.exige_expressao(expr)
    bd, sigla = b.exige_bd(base)
    if ident == b.sonda:
        raise Uso(f"{b.sonda} é a sonda de sensibilidade, não expressão de conferência: o "
                  f"conjunto dela é superconjunto de {b.executada} e não se deriva da "
                  f"exportação da executada. Use  python3 -m rsl conferencia sensibilidade <base>.")
    if ident == b.executada:
        raise Uso(f"{b.executada} é a executada: o conjunto derivado é ela mesma. Confira "
                  f"uma expressão derivável.")

    if caminho is None:
        _, validas = carrega_consultas(b)
        regs = registros_da_expressao(sigla, ident, validas)
        if not regs:
            raise DadosInvalidos(
                f"{sigla} ({bd}) sem execução direta de {ident} registrada. Registre-a "
                f"ou informe o arquivo:\n  {CMD_REGISTRAR} {sigla} {ident} <arquivo> "
                f"--retorno <n>")
        origem = f"execução registrada de {ident} em {sigla}"
    else:
        arq = pathlib.Path(caminho)
        if not arq.exists():
            raise DadosInvalidos(f"Arquivo não encontrado: {arq}")
        regs = le_arquivo(arq)
        origem = relativo(arq) if arq.is_absolute() else str(arq)
    direto = {chave_dedup(r) for r in regs}
    if not direto:
        raise DadosInvalidos("Nenhum registro lido da execução direta.")

    lidas = [c for c in consultas_do_corpus(b) if c.get("base") == sigla]
    if not lidas:
        raise DadosInvalidos(
            f"{sigla} ({bd}) sem execução de {b.executada} (a executada) registrada: o "
            f"conjunto derivado vem só da executada da mesma base.\n"
            f"  {CMD_REGISTRAR} {sigla} {b.executada} <arquivo> --retorno <n>")
    print(f"Base da conferência: {sigla} ({bd}) — o conjunto derivado usa só as "
          f"exportações de {b.executada} desta base.")
    facetas = carrega_facetas(b, [sigla])
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

    print(f"\nTESTE DE FIDELIDADE — {ident} em {sigla}")
    print(f"  execução direta lida de: {origem}")
    print(f"  execução direta na base : {len(direto)}")
    print(f"  conjunto derivado       : {len(derivado)}")
    print(f"  só na execução direta   : {len(so_direto)}")
    print(f"  só no conjunto derivado : {len(so_derivado)}")
    print(f"  divergência simétrica   : {div:.1%}  (limite: {b.limite_divergencia:.0%})")
    rel = b.config.saida("fidelidade", base=sigla, expressao=ident)
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
    return fidelidade(Busca(ctx), a.base, a.expressao, a.arquivo)
