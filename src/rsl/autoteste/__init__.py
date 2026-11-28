"""Autoteste: prova que cada conferência reprova o defeito que lhe cabe, com o código esperado.

Cada defeito é injetado numa cópia em memória — do protocolo, da fonte de um procedimento,
da configuração ou do arquivo de sementes — gerada a partir da estrutura lida do documento
corrente (a última semente lida, a primeira base da tabela, a linha em que a faixa foi
encontrada), não de literais do texto vigente. Defeito não detectado, detectado por outro
motivo ou com outro código faz o autoteste falhar; mutação que não se aplica também.

Grupos executados numa só chamada, cada um com a sua contagem: defeitos injetados no
protocolo, precedência, configuração, arquivo de sementes, leitura estrutural que aprova,
planejamento da validação, cliente TemaTres e reabertura, classificação do controle
terminológico, registro da validação, arquivos alimentados, cobertura por base, fonte do
procedimento, geração dos procedimentos, sondagens, consulta de sondagem por
referência, flexão dos termos,
composição da derivação, aderência sobre o conjunto, casamento local pelos termos da base,
corpus da derivação, anatomia da perda, análise da sensibilidade, geração das strings, gramática do protocolo,
catálogo de apoio, nomes antigos recusados e contagem dos casos não executados.

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
        self.blocos_pulados = 0
        self.motivos = []

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

    def nao_executa(self, motivo, *, quantos=None):
        """Casos que não rodam, com o motivo.

        Com `quantos`, os casos são contados: um caso trocado pelo aviso (1), ou um número
        calculado dos dados. Sem `quantos`, o restante do bloco não roda e não se conta: um
        número escrito à mão ao lado de um retorno antecipado desatualiza a cada caso novo
        do bloco, e o relato diria menos do que deixou de provar."""
        if not isinstance(motivo, str):
            raise TypeError(f"nao_executa: o motivo é texto, não {motivo!r}; o número de "
                            f"casos, quando se conta, vai em `quantos=`")
        self.motivos.append(motivo)
        if quantos is None:
            self.blocos_pulados += 1
            print(f"  [--] restante do bloco NÃO executado: {motivo}")
        else:
            self.nao_executados += quantos
            print(f"  [--] {quantos} caso(s) NÃO executado(s): {motivo}")

    @property
    def pulou(self):
        return bool(self.nao_executados or self.blocos_pulados)

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
                   nomes_antigos, procedimentos, protocolo, sementes, validacao, zotero)
    return [
        ("defeitos injetados no protocolo", protocolo.mutacoes),
        ("precedência", protocolo.precedencia),
        ("configuração", configuracao.casos),
        ("arquivo de sementes", sementes.casos),
        ("junção com a cópia do Zotero", sementes.juncao),
        ("regra do et al.", sementes.et_al),
        ("ensaio seco por campo", sementes.ensaio),
        ("Zotero e OpenAlex, com servidor simulado", zotero.casos),
        ("leitura estrutural que aprova", protocolo.estrutural),
        ("planejamento da validação", validacao.casos),
        ("cliente TemaTres e reabertura", validacao.cliente),
        ("classificação do controle terminológico", validacao.classificacao),
        ("registro da validação", validacao.registros),
        ("conferências dos arquivos alimentados", dados.casos),
        ("geração das strings", geracao.casos),
        ("cobertura por base, sobre a fonte", derivado.casos),
        ("fonte do procedimento de busca", procedimentos.fonte),
        ("geração dos procedimentos", procedimentos.geracao),
        ("sondagens por base", procedimentos.sondagens),
        ("consulta de sondagem por referência", procedimentos.referencias),
        ("flexão dos termos", procedimentos.flexao),
        ("prova da composição da derivação", busca.composicao),
        ("aderência sobre o conjunto", busca.aderencia),
        ("casamento local pelos termos da base", busca.casamento),
        ("corpus da derivação é a executada", busca.corpus),
        ("anatomia da perda", busca.anatomia),
        ("análise da sensibilidade", busca.sensibilidade_analise),
        ("exportação do cache, sem consultar o Zotero", busca.exportacao_do_cache),
        ("leitura RIS do original e da reexportação do Zotero", busca.leitor_ris),
        ("identificador da execução", busca.identificador),
        ("gramática do protocolo", gramatica.casos),
        ("catálogo de apoio", catalogo.casos),
        ("nomes antigos recusados", nomes_antigos.casos),
        ("contagem dos casos não executados", contagem),
    ]


def cmd_autoteste(ctx, a=None):
    corrente = conferir(ctx)
    if corrente:
        for p in corrente:
            print("  -", p)
        print("O documento corrente já está reprovado; o autoteste não teria o que provar.")
        return Saida.REPROVADO
    z = ctx.protocolo()["zotero"]
    print(f"Cópia da coleção do Zotero: versão {z['versao']}, lida em {z['lida_em']}.")
    feitos = []
    for nome, funcao in grupos():
        print(f"\n== {nome}")
        g = Grupo(nome)
        funcao(ctx, g)
        feitos.append(g)
    print("\nResumo por grupo:")
    for g in feitos:
        extra = f", {g.nao_executados} NÃO executado(s)" if g.nao_executados else ""
        extra += (f", {g.blocos_pulados} bloco(s) NÃO executado(s)" if g.blocos_pulados
                  else "")
        falhou = f", {g.falhas} FALHA(S)" if g.falhas else ""
        print(f"  {g.nome:<42} {g.n:>3} executado(s){falhou}{extra}")
    codigo, texto = conclusao(feitos)
    print(f"\n{texto}")
    return codigo


def conclusao(feitos):
    """(código, última mensagem) do autoteste a partir dos grupos executados. O número de
    casos não executados é só o contado (`quantos=`); o bloco pulado se relata como bloco,
    sem número."""
    falhas = sum(g.falhas for g in feitos)
    executados = sum(g.n for g in feitos)
    nao_exec = sum(g.nao_executados for g in feitos)
    blocos = sum(g.blocos_pulados for g in feitos)
    parcial = ""
    if nao_exec or blocos:
        motivos = "; ".join(f"{g.nome}: {' / '.join(g.motivos)}" for g in feitos if g.pulou)
        partes = []
        if nao_exec:
            partes.append(f"{nao_exec} caso(s) contado(s)")
        if blocos:
            partes.append(f"{blocos} bloco(s) inteiro(s), de tamanho não contado")
        parcial = (f"\nAUTOTESTE PARCIAL: NÃO foram executados {' e '.join(partes)} "
                   f"({motivos}). Esses casos não foram aprovados nem reprovados: "
                   f"não se sabe se as conferências correspondentes reprovam os defeitos que "
                   f"deveriam.")
    if falhas:
        return Saida.REPROVADO, f"{falhas} de {executados} caso(s) executado(s) falharam.{parcial}"
    if nao_exec or blocos:
        return (Saida.PARCIAL,
                f"Os {executados} casos executados tiveram o resultado esperado.{parcial}")
    return Saida.OK, f"Todos os {executados} casos tiveram o resultado esperado."


def contagem(ctx, g):
    """Contrato dos casos não executados, com grupos fictícios em memória: o bloco pulado
    dá PARCIAL sem número, o número só vem de `quantos=`, a falha prevalece e a forma
    antiga, com o número escrito à mão como primeiro argumento, é recusada."""
    import contextlib
    import io

    def fictício(*chamadas, falha=False):
        f = Grupo("fictício")
        with contextlib.redirect_stdout(io.StringIO()):
            f.ok("caso que passa")
            if falha:
                f.falha("caso que falha")
            for motivo, quantos in chamadas:
                f.nao_executa(motivo, quantos=quantos)
        return conclusao([f])

    cod, texto = fictício(("sem dado de ensaio", None))
    g.testa("bloco pulado: PARCIAL, relatado como bloco, sem número de casos",
            cod == Saida.PARCIAL and "1 bloco(s) inteiro(s), de tamanho não contado" in texto
            and "caso(s) contado(s)" not in texto, f"{cod.name} {texto[:160]}")
    cod, texto = fictício(("dois casos trocados", 2))
    g.testa("casos contados: PARCIAL com o número de `quantos=`",
            cod == Saida.PARCIAL and "2 caso(s) contado(s)" in texto
            and "bloco(s)" not in texto, f"{cod.name} {texto[:160]}")
    cod, texto = fictício(("bloco", None), ("um caso", 1))
    g.testa("bloco e contagem juntos: PARCIAL com os dois",
            cod == Saida.PARCIAL and "1 caso(s) contado(s) e 1 bloco(s)" in texto,
            f"{cod.name} {texto[:160]}")
    cod, texto = fictício(("um caso", 1), falha=True)
    g.testa("falha com casos não executados: REPROVADO, informando os não executados",
            cod == Saida.REPROVADO and "1 caso(s) contado(s)" in texto,
            f"{cod.name} {texto[:160]}")
    cod, texto = fictício()
    g.testa("contraprova: sem caso pulado nem falha, OK", cod == Saida.OK, cod.name)
    for nome, chamada in (("nao_executa(3, \"…\")", lambda f: f.nao_executa(3, "…")),
                          ("nao_executa(3)", lambda f: f.nao_executa(3))):
        f = Grupo("fictício")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                chamada(f)
            recusada = False
        except TypeError:
            recusada = True
        g.testa(f"forma antiga recusada: {nome}", recusada and not f.pulou,
                f"aceita: {f.nao_executados} contado(s), {f.blocos_pulados} bloco(s)")
