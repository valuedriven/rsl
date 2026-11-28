"""Contexto explícito de uma execução: a configuração, o texto do protocolo, dos
procedimentos de busca gerados, da fonte de cada procedimento, do arquivo de sementes, do
arquivo de exceções de flexão e da cópia da coleção do Zotero.

O subcomando cria o contexto e o passa às funções; não há estado de módulo. O autoteste
cria contextos sobre cópias em memória (texto alterado, procedimento de busca alterado, configuração
alterada) sem reimportar nada.
"""

from . import config as _config

# Registros da validação ainda não lidos (None quer dizer "ausente").
_NAO_LIDA = object()


class Contexto:
    def __init__(self, cfg, texto=None, procedimentos=None, sementes=None, fontes=None,
                 flexoes=None, decisoes=_NAO_LIDA, resultado=_NAO_LIDA, zotero=None):
        self.config = cfg
        self._texto = texto
        self._procedimentos = dict(procedimentos or {})
        self._sementes = sementes
        self._fontes = dict(fontes or {})
        self._flexoes = flexoes
        self._decisoes = decisoes
        self._resultado = resultado
        self._zotero = zotero
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

    def procedimento(self, sigla, caminho):
        """Texto do procedimento de busca gravado de uma base (saída de geração): o da cópia
        em memória, ou o do arquivo; None se não existe."""
        if sigla in self._procedimentos:
            return self._procedimentos[sigla]
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

    def _texto_registro(self, chave, atributo, rotulo):
        """Texto de um dos registros da validação; None se o arquivo não existe."""
        if getattr(self, atributo) is _NAO_LIDA:
            from .erros import DadosInvalidos                       # noqa: PLC0415
            arquivo = self.config.caminho(chave)
            try:
                setattr(self, atributo, (arquivo.read_text(encoding="utf-8")
                                         if arquivo.exists() else None))
            except (OSError, UnicodeDecodeError) as e:
                raise DadosInvalidos(f"{_config.relativo(arquivo)}: {rotulo} ilegível "
                                     f"({e})") from None
        return getattr(self, atributo)

    @property
    def texto_decisoes(self):
        """Texto do arquivo de decisões do ReT (`[dados] validacao`); None se não existe."""
        return self._texto_registro("dados.validacao", "_decisoes", "arquivo de decisões")

    @property
    def texto_resultado(self):
        """Texto do resultado técnico (`[dados] consulta_terminologica`); None se não existe."""
        return self._texto_registro("dados.consulta_terminologica", "_resultado",
                                    "resultado técnico")

    @property
    def zotero(self):
        """A cópia da coleção do Zotero (`[dados] zotero`): a em memória, ou a do arquivo.
        DadosInvalidos se ausente ou ilegível, com a indicação de `sementes copiar`."""
        if self._zotero is None:
            from .zotero import le_copia                            # noqa: PLC0415
            self._zotero = le_copia(self.config.caminho("dados.zotero"))
        return self._zotero

    def protocolo(self):
        """O protocolo lido, uma vez por contexto (ProtocoloInvalido se ilegível)."""
        if self._protocolo is None:
            from .leitura import analisa                            # noqa: PLC0415
            self._protocolo = analisa(self)
        return self._protocolo

    # ---------------------------------------------------------------------- cópias
    def _copia(self, **mudou):
        atual = {"cfg": self.config, "texto": self._texto, "procedimentos": self._procedimentos,
                 "sementes": self._sementes, "fontes": self._fontes,
                 "flexoes": self._flexoes, "decisoes": self._decisoes,
                 "resultado": self._resultado, "zotero": self._zotero}
        atual.update(mudou)
        return Contexto(**atual)

    def com_texto(self, texto):
        return self._copia(texto=texto)

    def com_procedimentos(self, procedimentos):
        return self._copia(procedimentos={**self._procedimentos, **procedimentos})

    def com_fontes(self, fontes):
        """Cópia com a fonte de algumas bases em memória: {sigla: {"toml", "fragmentos",
        "arquivos"}}; "toml" pode ser o dict já lido."""
        return self._copia(fontes={**self._fontes, **fontes})

    def com_flexoes(self, texto):
        return self._copia(flexoes=texto)

    def com_decisoes(self, texto):
        """Cópia com o arquivo de decisões em memória; None: arquivo ausente."""
        return self._copia(decisoes=texto)

    def com_resultado(self, texto):
        """Cópia com o resultado técnico em memória; None: arquivo ausente."""
        return self._copia(resultado=texto)

    def com_sementes(self, texto):
        return self._copia(sementes=texto)

    def com_zotero(self, doc):
        """Cópia com a cópia da coleção do Zotero em memória (dict já lido)."""
        return self._copia(zotero=doc)

    def com_config(self, cfg):
        return self._copia(cfg=cfg)
