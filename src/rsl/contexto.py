"""Contexto explícito de uma execução: a configuração, o texto do protocolo, dos
procedimentos de busca gerados, da fonte de cada procedimento, do arquivo de sementes e do
arquivo de exceções de flexão.

O subcomando cria o contexto e o passa às funções; não há estado de módulo. O autoteste
cria contextos sobre cópias em memória (texto alterado, procedimento de busca alterado, configuração
alterada) sem reimportar nada.
"""

from . import config as _config

# Planilha de validação ainda não lida (None quer dizer "ausente").
_NAO_LIDA = object()


class Contexto:
    def __init__(self, cfg, texto=None, fichas=None, sementes=None, fontes=None,
                 flexoes=None, validacao=_NAO_LIDA):
        self.config = cfg
        self._texto = texto
        self._fichas = dict(fichas or {})
        self._sementes = sementes
        self._fontes = dict(fontes or {})
        self._flexoes = flexoes
        self._validacao = validacao
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
        """Texto do procedimento de busca gravado de uma base (saída de geração): o da cópia
        em memória, ou o do arquivo; None se não existe."""
        if sigla in self._fichas:
            return self._fichas[sigla]
        arquivo = _config.RAIZ / caminho
        return arquivo.read_text(encoding="utf-8") if arquivo.exists() else None

    def fonte_bruta(self, sigla, pasta):
        """A fonte de uma base, sem validar: {"toml": texto ou dict já lido, "fragmentos":
        {nome: texto}, "arquivos": [nomes na pasta]}, a da cópia em memória ou a da pasta;
        None se a pasta ou `procedimento.toml` não existe."""
        if sigla in self._fontes:
            return self._fontes[sigla]
        raiz = _config.RAIZ / pasta
        dados = raiz / "procedimento.toml"
        if not dados.is_file():
            return None
        nomes = sorted(x.name for x in raiz.iterdir() if x.is_file())
        fragmentos = {n: (raiz / n).read_text(encoding="utf-8") for n in nomes
                      if n.endswith(".md")}
        return {"toml": dados.read_text(encoding="utf-8"), "fragmentos": fragmentos,
                "arquivos": nomes}

    @property
    def texto_flexoes(self):
        """Texto do arquivo de exceções de flexão; None se não existe (nenhuma exceção)."""
        if self._flexoes is None:
            arquivo = self.config.caminho("documentos.flexoes")
            self._flexoes = arquivo.read_text(encoding="utf-8") if arquivo.exists() else ""
        return self._flexoes

    @property
    def texto_validacao(self):
        """Texto da planilha de validação terminológica; None se não existe.
        DadosInvalidos se existe e não pode ser lida como texto."""
        if self._validacao is _NAO_LIDA:
            from .erros import DadosInvalidos                       # noqa: PLC0415
            arquivo = self.config.caminho("dados.validacao")
            try:
                self._validacao = (arquivo.read_text(encoding="utf-8-sig")
                                   if arquivo.exists() else None)
            except (OSError, UnicodeDecodeError) as e:
                raise DadosInvalidos(f"{_config.relativo(arquivo)}: planilha de validação "
                                     f"ilegível ({e})") from None
        return self._validacao

    def protocolo(self):
        """O protocolo lido, uma vez por contexto (ProtocoloInvalido se ilegível)."""
        if self._protocolo is None:
            from .leitura import analisa                            # noqa: PLC0415
            self._protocolo = analisa(self)
        return self._protocolo

    # ---------------------------------------------------------------------- cópias
    def _copia(self, **mudou):
        atual = {"cfg": self.config, "texto": self._texto, "fichas": self._fichas,
                 "sementes": self._sementes, "fontes": self._fontes,
                 "flexoes": self._flexoes, "validacao": self._validacao}
        atual.update(mudou)
        return Contexto(**atual)

    def com_texto(self, texto):
        return self._copia(texto=texto)

    def com_fichas(self, fichas):
        return self._copia(fichas={**self._fichas, **fichas})

    def com_fontes(self, fontes):
        """Cópia com a fonte de algumas bases em memória: {sigla: {"toml", "fragmentos",
        "arquivos"}}; "toml" pode ser o dict já lido."""
        return self._copia(fontes={**self._fontes, **fontes})

    def com_flexoes(self, texto):
        return self._copia(flexoes=texto)

    def com_validacao(self, texto):
        """Cópia com a planilha de validação em memória; None: planilha ausente."""
        return self._copia(validacao=texto)

    def com_sementes(self, texto):
        return self._copia(sementes=texto)

    def com_config(self, cfg):
        return self._copia(cfg=cfg)
