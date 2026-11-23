"""Contexto explícito de uma execução: a configuração, o texto do protocolo, dos
procedimentos de busca e do arquivo de sementes.

O subcomando cria o contexto e o passa às funções; não há estado de módulo. O autoteste
cria contextos sobre cópias em memória (texto alterado, procedimento de busca alterado, configuração
alterada) sem reimportar nada.
"""

from . import config as _config


class Contexto:
    def __init__(self, cfg, texto=None, fichas=None, sementes=None):
        self.config = cfg
        self._texto = texto
        self._fichas = dict(fichas or {})
        self._sementes = sementes
        self._protocolo = None

    @classmethod
    def carrega(cls, caminho_config=None):
        """Contexto da configuração em uso (ConfiguracaoInvalida se ela falhar)."""
        return cls(_config.carrega(caminho_config))

    # ------------------------------------------------------------------- documentos
    @property
    def texto(self):
        """Texto do protocolo: o da cópia em memória, ou o do arquivo configurado."""
        if self._texto is None:
            self._texto = self.config.protocolo().read_text(encoding="utf-8")
        return self._texto

    @property
    def caminho_protocolo(self):
        return self.config.valor("protocolo")

    @property
    def texto_sementes(self):
        """Texto do arquivo de sementes: o da cópia em memória, ou o do arquivo configurado
        (ConfiguracaoInvalida se ausente)."""
        if self._sementes is None:
            self._sementes = self.config.sementes().read_text(encoding="utf-8")
        return self._sementes

    @property
    def caminho_sementes(self):
        return self.config.valor("documentos.sementes")

    def ficha(self, sigla, caminho):
        """Texto do procedimento de busca de uma base: o da cópia em memória, ou o do arquivo."""
        if sigla in self._fichas:
            return self._fichas[sigla]
        return (_config.RAIZ / caminho).read_text(encoding="utf-8")

    def protocolo(self):
        """O protocolo lido, uma vez por contexto (ProtocoloInvalido se ilegível)."""
        if self._protocolo is None:
            from .leitura import analisa                            # noqa: PLC0415
            self._protocolo = analisa(self)
        return self._protocolo

    # ---------------------------------------------------------------------- cópias
    def com_texto(self, texto):
        return Contexto(self.config, texto, self._fichas, self._sementes)

    def com_fichas(self, fichas):
        return Contexto(self.config, self._texto, {**self._fichas, **fichas}, self._sementes)

    def com_sementes(self, texto):
        return Contexto(self.config, self._texto, self._fichas, texto)

    def com_config(self, cfg):
        return Contexto(cfg, self._texto, self._fichas, self._sementes)
