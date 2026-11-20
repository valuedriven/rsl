"""Exceções tipadas. Cada uma corresponde a um código de saída; só `__main__` converte.

Nenhum módulo do pacote encerra o processo: a falha sobe como exceção, e o ponto de
entrada imprime a mensagem e termina com o código da exceção.
"""

from .saida import Saida


class ErroRSL(Exception):
    """Falha que encerra o subcomando com um código próprio."""

    codigo = Saida.REPROVADO


class Uso(ErroRSL):
    """Argumento inválido para o subcomando (sigla, expressão, faceta)."""

    codigo = Saida.USO


class ConfiguracaoInvalida(ErroRSL):
    """O config.toml não existe, não é TOML válido, não tem uma chave exigida ou tem chave
    desconhecida, ou a chave `protocolo` aponta arquivo inexistente."""

    codigo = Saida.CONFIGURACAO


class ProtocoloInvalido(ErroRSL):
    """O protocolo ou uma ficha não tem a forma que o leitor sabe interpretar.

    `elemento` é a declaração da gramática violada (ver `gramatica.py`); a mensagem leva o
    documento e o nome do elemento, com o mesmo nome que `rsl gramatica` exibe.
    """

    codigo = Saida.PROTOCOLO_ILEGIVEL

    def __init__(self, elemento, detalhe, documento=None):
        self.elemento = elemento
        self.detalhe = detalhe
        self.documento = documento or getattr(elemento, "documento", "")
        super().__init__(self._texto())

    def _texto(self):
        nome = getattr(self.elemento, "rotulo", None) or str(self.elemento or "")
        partes = [p for p in (self.documento, nome) if p]
        return f"{' › '.join(partes)}: {self.detalhe}" if partes else str(self.detalhe)


class DadosInvalidos(ErroRSL):
    """Arquivo alimentado, exportação ou arquivo de entrada ausente ou ilegível."""

    codigo = Saida.DADOS


class FonteExterna(ErroRSL):
    """Fonte externa com erro de rede, bloqueio, captcha, limite ou resposta fora do
    formato esperado. Interrompe sem nova tentativa."""

    codigo = Saida.FONTE_EXTERNA


class Reprovado(ErroRSL):
    """O conteúdo não satisfaz uma condição de aceite e a operação não pode seguir (ex.:
    composição das expressões incoerente para a derivação)."""

    codigo = Saida.REPROVADO
