"""Exibição: o resumo do que foi lido (`mostrar`) e o contrato da gramática (`gramatica`)."""

from . import gramatica as G
from .erros import ProtocoloInvalido
from .fichas import ficha, forma_execucao
from .saida import Saida


def composicao_legivel(grupos):
    """Grupos de STRn na forma estrita do protocolo, com o número da STR: grupo unitário
    vira o número; grupo com mais de uma, a disjunção entre parênteses."""
    partes = []
    for g in grupos:
        nomes = [x[len(G.I_STR.prefixo):] for x in g]
        partes.append(nomes[0] if len(nomes) == 1 else "(" + " OR ".join(nomes) + ")")
    return " AND ".join(partes)


def _legivel(valor):
    if isinstance(valor, float):
        return f"{valor:.0%}"
    if isinstance(valor, list) and valor and all(isinstance(x, float) for x in valor):
        return " a ".join(f"{x:.0%}" for x in valor)
    if isinstance(valor, dict):
        return ", ".join(f"{k}={composicao_legivel(v)}" for k, v in sorted(valor.items()))
    if isinstance(valor, list):
        return ", ".join(str(x) for x in valor)
    return str(valor)


def execucao_das_fichas(ctx, d):
    """Forma de execução de cada base, com origem na ficha: (nome, valor, origem).

    Ficha ilegível nesse ponto aparece como tal, sem derrubar a exibição das demais.
    """
    saida = []
    for b in d["bases"]:
        try:
            valor = forma_execucao(ficha(ctx, d, b["sigla"]), b["ficha"])
        except (ProtocoloInvalido, OSError) as e:
            valor = f"ILEGÍVEL — {e}"
        saida.append((f"execucao.{b['sigla']}", valor, f"ficha {b['ficha']}"))
    return saida


def relatorio(ctx, d):
    L = [f"  protocolo: {ctx.caminho_protocolo}  (chave `protocolo` do {ctx.config.nome})"]
    L.append(f"  questão: 1 geral, {len(d['questoes']['questoes_especificas'])} específicas")
    for f in d["tabelas"]:
        n_string = len(d["strings"][f["id"]]["termos"])
        n_bruto = sum(len(f["termos"][i]) for i in d["idiomas"])
        insts = ", ".join(f"{i['sigla']}({'/'.join(i['idiomas'])}"
                          f"{', manual' if i['modo'] == G.MODO_MANUAL else ''})"
                          for i in d["instrumentos_por_faceta"][f["id"]])
        L.append(f"  faceta {f['id']} — {f['nome'][:52]:<54} "
                 f"tabela {n_bruto:>3} formas / string {n_string:>3} termos   "
                 f"instrumentos: {insts}")
    crit = d["criterios"]
    L.append(f"  critérios: {len(crit)} "
             f"({sum(1 for c in crit if c['acao'] == G.ACAO_INCLUIR)} incluir, "
             f"{sum(1 for c in crit if c['acao'] == G.ACAO_EXCLUIR)} excluir)")
    L.append(f"  fontes: {len(d['fontes']['bases'])} bases, ordem "
             f"{d['fontes']['ordem_execucao']}")
    dist = d["distribuicao"]
    L.append(f"  sementes: {len(d['sementes'])}  "
             f"incidências: {dist['incidencias']}  "
             f"por base: " + ", ".join(f"{b} {v}" for b, v in dist["por_base"].items()))
    papeis = "  ".join(
        f"{p}: {dist['por_papel'][p]} estudo(s), "
        f"{sum(dist['por_base_papel'][b][p] for b in dist['por_base'])} incidência(s) "
        f"(" + ", ".join(f"{b} {dist['por_base_papel'][b][p]}"
                         for b in dist["por_base"]) + ")"
        for p in G.D_PAPEL.valores.values())
    L.append(f"  sementes por papel: {papeis}")
    L.append("  expressões: " + ", ".join(
        f"{n}=" + composicao_legivel(c)
        for n, c in sorted(d["expressoes"].items())) +
        f"   executada: {d['executada']}   sonda: {d['sonda']}")
    recorte = (f"{d['recorte']['ano_min']} a {d['recorte']['ano_max']}"
               if d["recorte"]["ano_max"]
               else f"{d['recorte']['ano_min']} até a data de execução")
    L.append(f"  recorte: {recorte}   limiar: {d['limiar']:.0%}")
    L.append("  parâmetros em uso:")
    for nome, p in d["parametros"].items():
        L.append(f"    {nome:<24} {_legivel(p['valor'])[:70]:<72} [{p['origem']}]")
    for nome, valor, origem in execucao_das_fichas(ctx, d):
        L.append(f"    {nome:<24} {valor[:70]:<72} [{origem}]")
    return "\n".join(L)


def cmd_mostrar(ctx, a=None):
    print(relatorio(ctx, ctx.protocolo()))
    return Saida.OK


def cmd_gramatica(ctx=None, a=None):
    print(G.contrato())
    return Saida.OK
