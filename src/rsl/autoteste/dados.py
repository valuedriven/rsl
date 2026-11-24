"""Autoteste das conferências dos arquivos alimentados.

Os casos são declarados antes de rodar: sem os arquivos alimentados, nenhum roda, e todos
são contados como não executados — nunca como aprovados. O relato do registro ausente, em
`projeto pendencias`, roda sempre, com o registro apontado para um diretório temporário.
"""

import contextlib
import copy
import io
import pathlib
import tempfile

from .. import gramatica as G
from ..config import Configuracao, relativo
from ..dados import (CMD_REGISTRAR, cmd_pendencias, le_json, problemas_citacoes_registro,
                     problemas_registro)
from .fontes import com_fonte, fonte_de


def registro_ausente(ctx, g):
    """Sem o registro de execução, `projeto pendencias` orienta registrar a primeira
    execução com `busca registrar`, e não reconstituir o registro."""
    cfg = ctx.config
    with tempfile.TemporaryDirectory() as tmp:
        ausente = pathlib.Path(tmp) / pathlib.Path(cfg.valor("dados.registro")).name
        cx = ctx.com_config(Configuracao(cfg.com("dados.registro", str(ausente)), cfg.arquivo))
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            cmd_pendencias(cx)
    linha = next((x.strip() for x in saida.getvalue().splitlines()
                  if "[ausente]" in x and ausente.name in x), "")
    g.testa("registro ausente: `projeto pendencias` orienta a primeira execução com "
            "`busca registrar`",
            CMD_REGISTRAR in linha and "reconstitu" not in linha,
            linha or "a ausência não foi relatada")


def casos(ctx, g):
    registro_ausente(ctx, g)
    d = ctx.protocolo()
    cfg = ctx.config
    bds = [b["id"] for b in d["bases"]]
    siglas = [b["sigla"] for b in d["bases"]]
    caminho_reg = str(cfg.valor("dados.registro"))
    reg = None

    def registro_reprova(transforma):
        def caso():
            copia = copy.deepcopy(reg)
            transforma(copia)
            return bool(problemas_registro(ctx, copia, bds))
        return caso

    def execucao_extra(arquivo, lidos):
        return lambda c: c["bases"][bds[0]]["execucoes"].append({
            "id": "EX-autoteste", "expressao": d["executada"], "arquivo": arquivo,
            "registros_lidos": lidos, "status": "valida"})

    def so_a_base(alvo, linha):
        """A citação injetada na fonte de `alvo` (nota do primeiro elemento de sintaxe)
        reprova só essa base."""
        def caso():
            dado, frag, arqs = fonte_de(ctx, d, alvo)
            dado["sintaxe"][0]["nota"] = linha
            p = problemas_citacoes_registro(com_fonte(ctx, alvo, dado, frag, arqs), d, reg)
            return bool(p) and not [x for x in p if not x.startswith(alvo + ":")]
        return caso

    def inexistente():
        ids = {e.get("id") for base in reg.get("bases", {}).values()
               for e in base.get("execucoes", []) if isinstance(e, dict)}
        x = "execucao-inexistente-99"
        while x in ids:
            x += "-x"
        return x

    def outra_bd(sigla):
        """BDn de uma base diferente da de `sigla` (com uma só base, um BDn inexistente)."""
        return next((x for x in bds if x != bd_de[sigla]),
                    f"{G.I_BD.prefixo}{len(bds) + 1}")

    alvo = [siglas[k % len(siglas)] for k in range(4)]
    bd_de = dict(zip(siglas, bds))
    lista = [
        ("registro sem uma das bases",
         lambda: registro_reprova(lambda c: c["bases"].pop(bds[0]))()),
        ("execução apontando arquivo de exportação ausente",
         lambda: registro_reprova(execucao_extra(
             f"{cfg.valor('dados.execucoes')}/ausente-autoteste.ris", 1))()),
        ("execução com `registros_lidos` que não é inteiro",
         lambda: registro_reprova(execucao_extra(relativo(cfg.caminho("dados.registro")),
                                                 "um"))()),
        (f"citação do registro sem identificador de execução ({alvo[0]})",
         lambda: so_a_base(alvo[0], f"Verificado por medição — `{caminho_reg}` "
                                    f"({bd_de[alvo[0]]})")()),
        (f"citação de execução inexistente no registro ({alvo[1]})",
         lambda: so_a_base(alvo[1], f"Medido — `{caminho_reg}` "
                                    f"({bd_de[alvo[1]]}/{inexistente()})")()),
        (f"citação de execução de outra base ({alvo[2]})",
         lambda: so_a_base(alvo[2], f"Medido — `{caminho_reg}` "
                                    f"({outra_bd(alvo[2])}/de-outra-base)")()),
        (f"citação do registro em prosa sem identificador ({alvo[3]})",
         lambda: so_a_base(alvo[3], f"Comportamento apurado por medição, com as sondagens "
                                    f"em `{caminho_reg}`.")()),
        # A citação sem o caminho do registro (a nota de lematização que sustenta
        # `pela lematização`) se confere do mesmo modo.
        (f"citação de execução inexistente na linha Lematização, sem o caminho ({alvo[0]})",
         lambda: so_a_base(alvo[0], f"Lematização verificada por medição "
                                    f"({bd_de[alvo[0]]}/{inexistente()})")()),
        (f"citação de outra base na linha Lematização, sem o caminho ({alvo[1]})",
         lambda: so_a_base(alvo[1], f"Lematização verificada por medição "
                                    f"({outra_bd(alvo[1])}/de-outra-base)")()),
    ]

    reg, erro_r = le_json(cfg.caminho("dados.registro"))
    if erro_r:
        g.nao_executa(len(lista), erro_r)
        return
    base_pr = problemas_registro(ctx, reg, bds)
    if base_pr:
        g.falha(f"o arquivo alimentado corrente já está reprovado: {base_pr[0]}")
    for nome, caso in lista:
        g.testa(f"reprovou: {nome}", caso(), "aprovou indevidamente")
