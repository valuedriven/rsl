"""Autoteste das conferências dos arquivos alimentados.

Os casos são declarados antes de rodar: sem os arquivos alimentados, nenhum roda, e todos
são contados como não executados — nunca como aprovados.
"""

import copy

from .. import gramatica as G
from ..config import relativo
from ..dados import le_json, problemas_citacoes_registro, problemas_registro
from ..fichas import ficha


def casos(ctx, g):
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
        """A citação injetada na ficha de `alvo` reprova só essa base."""
        def caso():
            texto = ficha(ctx, d, alvo).rstrip("\n") + "\n\n" + linha + "\n"
            p = problemas_citacoes_registro(ctx.com_fichas({alvo: texto}), d, reg)
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
