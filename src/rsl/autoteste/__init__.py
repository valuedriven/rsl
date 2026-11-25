"""Autoteste: prova que cada conferência reprova o defeito que lhe cabe, com o código esperado.

Cada defeito é injetado numa cópia em memória — do protocolo, da fonte de um procedimento,
da configuração ou do arquivo de sementes — gerada a partir da estrutura lida do documento
corrente (a última semente lida, a primeira base da tabela, a linha em que a faixa foi
encontrada), não de literais do texto vigente. Defeito não detectado, detectado por outro
motivo ou com outro código faz o autoteste falhar; mutação que não se aplica também.

Grupos executados numa só chamada, cada um com a sua contagem: defeitos injetados no
protocolo, precedência, configuração, arquivo de sementes, leitura estrutural que aprova,
planejamento da validação, cliente TemaTres e reabertura, arquivos alimentados, cobertura por base, fonte do
procedimento, geração dos procedimentos, sondagens, consulta de sondagem por
referência, flexão dos termos,
composição da derivação, aderência por papel, geração das strings, gramática do protocolo,
catálogo de apoio e nomes antigos recusados.

Sem os arquivos alimentados, os casos que dependem deles não rodam: o resultado é PARCIAL,
nunca OK.
"""

from ..coerencia import conferir
from ..erros import ErroRSL
from ..saida import Saida


class Grupo:
    """Contagem e relato dos casos de um grupo."""

    def __init__(self, nome):
        self.nome = nome
        self.falhas = 0
        self.n = 0
        self.nao_executados = 0
        self.motivo = ""

    def ok(self, texto):
        self.n += 1
        print(f"  [ok] {texto}")

    def falha(self, texto):
        self.n += 1
        self.falhas += 1
        print(f"  [FALHA] {texto}")

    def testa(self, nome, condicao, detalhe=""):
        if condicao:
            self.ok(nome)
        else:
            self.falha(f"{nome}{' — ' + detalhe if detalhe else ''}")

    def nao_executa(self, quantos, motivo):
        self.nao_executados += quantos
        self.motivo = motivo
        print(f"  [--] {quantos} caso(s) NÃO executado(s): {motivo}")

    def espera(self, nome, mutante, original, executa, codigo, trecho=None):
        """Executa `executa(mutante)` e exige o `codigo` com uma mensagem que contenha
        `trecho` (texto ou tupla de textos, todos exigidos)."""
        if mutante is None or mutante == original:
            self.falha(f"mutação não aplicada: {nome}")
            return
        cod, mensagens = resultado(lambda: executa(mutante))
        trechos = (trecho,) if isinstance(trecho, str) else tuple(trecho or ())
        faltam = [x for x in trechos if not any(x in m for m in mensagens)]
        achados = [m for m in mensagens if any(x in m for x in trechos)] or mensagens
        if cod != codigo:
            self.falha(f"{nome}: código {cod.name}, esperado {Saida(codigo).name} — "
                       f"{mensagens[:1]}")
        elif faltam:
            self.falha(f"não reprovou pelo motivo esperado ({faltam}): {nome} — "
                       f"{mensagens[:1]}")
        else:
            self.ok(f"reprovou ({cod.name}): {nome} — {achados[0][:88] if achados else ''}")


def resultado(funcao):
    """(código, mensagens) de uma conferência ou leitura: o Resultado devolvido, ou a
    exceção tipada levantada."""
    try:
        r = funcao()
    except ErroRSL as e:
        return Saida(e.codigo), [str(e)]
    if isinstance(r, list):
        return getattr(r, "codigo", Saida.REPROVADO if r else Saida.OK), [str(x) for x in r]
    if isinstance(r, int):
        return Saida(r), []
    return Saida.OK, []


def conferir_texto(ctx):
    """Executor de mutação no protocolo: conferir sobre a cópia."""
    return lambda mutante: conferir(ctx.com_texto(mutante))


def grupos():
    from . import (busca, catalogo, configuracao, dados, derivado, geracao, gramatica,
                   nomes_antigos, procedimentos, protocolo, sementes, validacao)
    return [
        ("defeitos injetados no protocolo", protocolo.mutacoes),
        ("precedência", protocolo.precedencia),
        ("configuração", configuracao.casos),
        ("arquivo de sementes", sementes.casos),
        ("leitura estrutural que aprova", protocolo.estrutural),
        ("planejamento da validação", validacao.casos),
        ("cliente TemaTres e reabertura", validacao.cliente),
        ("classificação do controle terminológico", validacao.classificacao),
        ("conferências dos arquivos alimentados", dados.casos),
        ("geração das strings", geracao.casos),
        ("cobertura por base, sobre a fonte", derivado.casos),
        ("fonte do procedimento de busca", procedimentos.fonte),
        ("geração dos procedimentos", procedimentos.geracao),
        ("sondagens por base", procedimentos.sondagens),
        ("consulta de sondagem por referência", procedimentos.referencias),
        ("flexão dos termos", procedimentos.flexao),
        ("prova da composição da derivação", busca.composicao),
        ("aderência por papel", busca.aderencia),
        ("gramática do protocolo", gramatica.casos),
        ("catálogo de apoio", catalogo.casos),
        ("nomes antigos recusados", nomes_antigos.casos),
    ]


def cmd_autoteste(ctx, a=None):
    corrente = conferir(ctx)
    if corrente:
        for p in corrente:
            print("  -", p)
        print("O documento corrente já está reprovado; o autoteste não teria o que provar.")
        return Saida.REPROVADO
    feitos = []
    for nome, funcao in grupos():
        print(f"\n== {nome}")
        g = Grupo(nome)
        funcao(ctx, g)
        feitos.append(g)
    falhas = sum(g.falhas for g in feitos)
    executados = sum(g.n for g in feitos)
    nao_exec = sum(g.nao_executados for g in feitos)
    print("\nResumo por grupo:")
    for g in feitos:
        extra = f", {g.nao_executados} NÃO executado(s)" if g.nao_executados else ""
        falhou = f", {g.falhas} FALHA(S)" if g.falhas else ""
        print(f"  {g.nome:<42} {g.n:>3} executado(s){falhou}{extra}")
    parcial = ""
    if nao_exec:
        motivos = "; ".join(f"{g.nome}: {g.motivo}" for g in feitos if g.nao_executados)
        parcial = (f"\nAUTOTESTE PARCIAL: {nao_exec} de {executados + nao_exec} casos NÃO foram "
                   f"executados ({motivos}). Esses casos não foram aprovados nem reprovados: "
                   f"não se sabe se as conferências correspondentes reprovam os defeitos que "
                   f"deveriam.")
    if falhas:
        print(f"\n{falhas} de {executados} caso(s) executado(s) falharam.{parcial}")
        return Saida.REPROVADO
    if nao_exec:
        print(f"\nOs {executados} casos executados tiveram o resultado esperado.{parcial}")
        return Saida.PARCIAL
    print(f"\nTodos os {executados} casos tiveram o resultado esperado.")
    return Saida.OK
