"""Códigos de saída, iguais em todos os subcomandos, e a regra de gravidade."""

import enum


class Saida(enum.IntEnum):
    OK = 0
    REPROVADO = 1
    USO = 2
    CONFIGURACAO = 3
    PROTOCOLO_ILEGIVEL = 4
    DADOS = 5
    PARCIAL = 6
    FONTE_EXTERNA = 7


QUANDO = {
    Saida.OK: "a operação terminou e nada reprovou",
    Saida.REPROVADO: "uma conferência ou condição de aceite reprovou o conteúdo",
    Saida.USO: "argumento ou subcomando inválido",
    Saida.CONFIGURACAO: "config.toml ausente, inválido ou incompleto, ou protocolo inexistente",
    Saida.PROTOCOLO_ILEGIVEL: "protocolo ou ficha fora da gramática que o leitor exige",
    Saida.DADOS: "arquivo alimentado, exportação ou arquivo de entrada ausente ou ilegível",
    Saida.PARCIAL: "autoteste sem falha, com casos não executados",
    Saida.FONTE_EXTERNA: "fonte externa com erro, bloqueio, captcha ou limite excedido",
}

# Da mais grave para a menos grave: quando mais de uma condição ocorre, vale a primeira.
GRAVIDADE = (Saida.CONFIGURACAO, Saida.PROTOCOLO_ILEGIVEL, Saida.DADOS, Saida.FONTE_EXTERNA,
             Saida.REPROVADO, Saida.PARCIAL, Saida.USO, Saida.OK)


def mais_grave(*codigos):
    """O código de maior gravidade entre `codigos`; OK se não houver nenhum."""
    presentes = {Saida(c) for c in codigos if c is not None}
    return next((c for c in GRAVIDADE if c in presentes), Saida.OK)


def tabela():
    """A tabela de códigos, para a ajuda e para o README."""
    return "\n".join(f"  {c.value}  {c.name:<19} {QUANDO[c]}" for c in Saida)


def linha_final(codigo):
    """Última linha de toda saída diferente de OK: o nome do código."""
    codigo = Saida(codigo)
    return f"Código de saída: {codigo.value} {codigo.name}"
