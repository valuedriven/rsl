"""Configuração: o `config.toml` da raiz, carregado sob demanda e validado pelo esquema.

O único caminho fixado é o do próprio `config.toml`, na raiz do projeto. A variável de
ambiente `RSL_CONFIG` aponta outro arquivo; existe para ensaio e autoteste (configuração
inválida, saídas num diretório temporário) e não é parâmetro do projeto.

Caminhos da configuração são relativos à raiz do projeto; caminho absoluto vale como está.
"""

import copy
import os
import pathlib
import re
import tomllib

from .erros import ConfiguracaoInvalida

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
VARIAVEL = "RSL_CONFIG"
NOME = "config.toml"

# Esquema do arquivo: seção → chaves. É a forma da configuração, não parâmetro do projeto.
# Chave fora do esquema reprova: chave com erro de grafia seria ignorada em silêncio.
ESQUEMA = {
    "": ("protocolo",),
    "padroes": ("recorte_ano_min", "limiar_aderencia", "sensibilidade",
                "divergencia_fidelidade"),
    "conferencia": ("dimensoes_criterio", "dimensao_recorte"),
    "busca": ("ano_recencia", "amostra_sensibilidade"),
    "dados": ("registro", "validacao", "consulta_terminologica", "execucoes", "evidencia",
              "zotero", "temporarios"),
    "saidas": ("pasta", "registros", "contagens", "ordem_triagem", "fidelidade",
               "sensibilidade", "anatomia", "anatomia_consultas", "candidatos"),
    "documentos": ("procedimento", "procedimento_fonte", "flexoes", "sementes"),
    "zotero": ("biblioteca", "colecao", "acesso", "library", "search_collection"),
}
# Chaves do esquema que podem faltar: a coleção das buscas só existe depois de o pesquisador
# criá-la no Zotero. Quem precisa dela pede `Configuracao.exige`, que reprova nomeando a chave.
OPCIONAIS = {"zotero.search_collection", "zotero.library"}
# Vias de acesso ao Zotero: a máquina do pesquisador ou a API web.
ACESSOS = ("local", "web")
# Chaves retiradas: a presença de qualquer uma reprova com mensagem própria, para que não
# haja segunda fonte que divirja em silêncio. Cada motivo termina com a correção: retirar
# a chave, ou renomeá-la quando o valor continua sob outro nome.
_RETIRAR = "; retirá-la"
_ESTRUTURAL = "o valor vem do protocolo (parâmetro estrutural, sem padrão)" + _RETIRAR
RETIRADAS = {
    "padroes.composicao": _ESTRUTURAL, "cores": _ESTRUTURAL, "fichas": _ESTRUTURAL,
    "instrumentos": _ESTRUTURAL, "idiomas": _ESTRUTURAL,
    "padroes.ancoras": "as âncoras vêm da coluna 'Âncora obrigatória' da tabela de facetas "
                       "do protocolo (parâmetro estrutural, sem padrão)" + _RETIRAR,
    "expressoes": "executada e sonda são identificadas pela composição das expressões "
                  "do protocolo; o cabeçalho da tabela é forma e vem da gramática "
                  "(`python3 -m rsl documentos gramatica`)" + _RETIRAR,
    "padroes.executada": "a executada é identificada pela composição (a única expressão "
                         "com grupo OR)" + _RETIRAR,
    "padroes.sonda": "a sonda é identificada pela composição (a única expressão formada "
                     "só pelas âncoras)" + _RETIRAR,
    "conferencia.minimo_termos_string": "o mínimo de termos por string foi retirado, e o "
                                        "tamanho da STR resulta do controle terminológico "
                                        "(decisão de 2026-11-24)" + _RETIRAR,
    "documentos.ficha": "renomeada para `[documentos] procedimento`; renomeá-la, mantendo "
                        "o valor",
    "saidas.aderencia": "a planilha de aderência foi retirada: a indexação declarada é o "
                        "campo `bases` do arquivo de sementes, a recuperação se calcula com "
                        "`aderencia medir` e o ensaio seco é `aderencia ensaiar`" + _RETIRAR,
    # Primeiro a chave, depois a seção: o caso mais provável é o config.toml antigo, com a
    # lista de colunas; a mensagem nomeia as duas chaves que substituem o formato antigo.
    "planilha.campos_validacao": "a lista de colunas do formato antigo foi retirada: a "
                                 "decisão do ReT fica em `[dados] validacao` (TOML) e o "
                                 "resultado técnico em `[dados] consulta_terminologica` "
                                 "(JSON)" + _RETIRAR,
    "planilha": "a seção `[planilha]` foi retirada: a decisão do ReT fica em "
                "`[dados] validacao` (TOML) e o resultado técnico em "
                "`[dados] consulta_terminologica` (JSON)" + _RETIRAR,
}
# Marcadores que cada padrão de caminho tem de conter. A fidelidade é por base e por
# expressão: sem a base no nome, a conferência de uma base sobrescreveria a de outra.
MARCADORES = {"documentos.procedimento": "{sigla}",
              "documentos.procedimento_fonte": "{sigla}",
              "saidas.fidelidade": ("{base}", "{expressao}"),
              "saidas.sensibilidade": "{base}",
              "saidas.anatomia": "{base}",
              "saidas.anatomia_consultas": "{base}",
              "saidas.candidatos": "{base}"}


def caminho_padrao():
    """O config.toml em uso: o de `RSL_CONFIG`, se definido; senão, o da raiz."""
    outro = os.environ.get(VARIAVEL)
    return pathlib.Path(outro) if outro else RAIZ / NOME


def _tem(dado, chave):
    atual = dado
    for parte in chave.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            return False
        atual = atual[parte]
    return True


_BIBLIOTECA = re.compile(r"(groups|users)/\d+")
_BIBLIOTECA_URL = re.compile(r"https?://(?:www\.)?zotero\.org/(groups/\d+)(?:/[^/?#]*)*/?")


def biblioteca_zotero(valor):
    """A biblioteca na forma da API (`groups/<id>` ou `users/<id>`), a partir dessa forma ou
    do endereço da biblioteca de grupo no site (`https://www.zotero.org/groups/<id>/<nome>`);
    None quando não é nenhuma das duas. A biblioteca de usuário no site não traz o número, e
    por isso só vale na forma `users/<id>`."""
    if not isinstance(valor, str):
        return None
    valor = valor.strip()
    if _BIBLIOTECA.fullmatch(valor):
        return valor
    m = _BIBLIOTECA_URL.fullmatch(valor)
    return m.group(1) if m else None


def linha_ignorada(gitignore, nome, pasta=False):
    """O `.gitignore` lista `nome` como linha própria (`nome` ou `/nome`; para pasta, também
    `nome/` e `/nome/`, que no `.gitignore` só casam com pasta)."""
    gitignore = pathlib.Path(gitignore)
    if not gitignore.exists():
        return False
    nome = nome.strip("/")
    aceitas = {nome, f"/{nome}"} | ({f"{nome}/", f"/{nome}/"} if pasta else set())
    return any(l.strip() in aceitas
               for l in gitignore.read_text(encoding="utf-8").splitlines())


def _temporarios(dado, nome, gitignore):
    """A pasta de temporários fica fora do controle de versão, e o cache das exportações
    dentro dela: impedido na carga, e não detectado depois de gravado em `data/`. A exigência
    do `.gitignore` só vale para pasta dentro da raiz: fora dela, a pasta não entra no controle
    de versão, e o `.gitignore` da raiz não a alcança."""
    temporarios, execucoes = dado["dados"]["temporarios"], dado["dados"]["execucoes"]
    for chave, valor in (("temporarios", temporarios), ("execucoes", execucoes)):
        if not isinstance(valor, str) or not valor.strip():
            raise ConfiguracaoInvalida(f"{nome}: `[dados] {chave}` vazia ou de outro tipo")
    pasta = (RAIZ / temporarios).resolve()
    try:
        relativa = pasta.relative_to(RAIZ)
    except ValueError:
        relativa = None
    if relativa is not None and not linha_ignorada(gitignore, relativa.as_posix(), pasta=True):
        raise ConfiguracaoInvalida(
            f"{nome}: a pasta de `[dados] temporarios` ({temporarios!r}) não está listada no "
            f"{pathlib.Path(gitignore).name} da raiz: o cache iria ao controle de versão. "
            f"Acrescentar `{relativa.as_posix()}/` ao .gitignore")
    if not (RAIZ / execucoes).resolve().is_relative_to(pasta):
        raise ConfiguracaoInvalida(
            f"{nome}: `[dados] execucoes` ({execucoes!r}) fora de `[dados] temporarios` "
            f"({temporarios!r}): o cache das exportações não se grava fora da pasta de "
            f"temporários")


def valida(dado, nome=NOME, gitignore=None):
    """Confere o esquema; levanta ConfiguracaoInvalida no primeiro defeito. Devolve o dado.
    `gitignore` substitui o `.gitignore` da raiz (autoteste)."""
    for chave, motivo in RETIRADAS.items():
        if _tem(dado, chave):
            raise ConfiguracaoInvalida(
                f"{nome}: a chave `{chave}` não pertence mais à configuração — {motivo}")
    for secao, chaves in ESQUEMA.items():
        alvo = dado if not secao else dado.get(secao)
        if secao and not isinstance(alvo, dict):
            raise ConfiguracaoInvalida(f"{nome}: falta a seção `[{secao}]`")
        for chave in chaves:
            completa = f"{secao}.{chave}" if secao else chave
            if chave not in alvo and completa not in OPCIONAIS:
                raise ConfiguracaoInvalida(f"{nome}: falta a chave `{completa}`")
    for chave, valor in dado.items():
        if chave in ESQUEMA and chave:
            desconhecidas = sorted(set(valor) - set(ESQUEMA[chave]))
            if desconhecidas:
                raise ConfiguracaoInvalida(
                    f"{nome}: chave desconhecida em `[{chave}]`: {desconhecidas}")
        elif chave not in ESQUEMA[""]:
            raise ConfiguracaoInvalida(f"{nome}: chave ou seção desconhecida `{chave}`")
    for chave, marcas in MARCADORES.items():
        secao, campo = chave.split(".")
        valor = dado[secao][campo]
        for marca in (marcas,) if isinstance(marcas, str) else marcas:
            if not isinstance(valor, str) or marca not in valor:
                raise ConfiguracaoInvalida(f"{nome}: `{chave}` {valor!r} não contém {marca}")
    for chave in ("biblioteca", "library"):
        if chave in dado["zotero"] and biblioteca_zotero(dado["zotero"][chave]) is None:
            raise ConfiguracaoInvalida(
                f"{nome}: `zotero.{chave}` {dado['zotero'][chave]!r} fora da forma groups/<id>, "
                f"users/<id> ou https://www.zotero.org/groups/<id>/<nome>")
    for chave in ("colecao", "search_collection"):
        if chave in dado["zotero"] and (not isinstance(dado["zotero"][chave], str)
                                        or not dado["zotero"][chave].strip()):
            raise ConfiguracaoInvalida(f"{nome}: `zotero.{chave}` vazia ou de outro tipo")
    if dado["zotero"]["acesso"] not in ACESSOS:
        raise ConfiguracaoInvalida(f"{nome}: `[zotero] acesso` {dado['zotero']['acesso']!r} "
                                   f"fora dos valores aceitos: {', '.join(ACESSOS)}")
    _temporarios(dado, nome, RAIZ / ".gitignore" if gitignore is None else gitignore)
    lo, hi = dado["padroes"]["sensibilidade"]
    if not lo < hi:
        raise ConfiguracaoInvalida(f"{nome}: `padroes.sensibilidade` com inferior ≥ "
                                   f"superior: {[lo, hi]}")
    return dado


class Configuracao:
    """A configuração validada, com os caminhos resolvidos contra a raiz do projeto."""

    def __init__(self, dado, arquivo=None):
        self.arquivo = pathlib.Path(arquivo) if arquivo else RAIZ / NOME
        self.nome = self.arquivo.name
        self.dado = valida(dado, self.nome)

    def valor(self, chave):
        atual = self.dado
        for parte in chave.split("."):
            atual = atual[parte]
        return copy.deepcopy(atual)

    def caminho(self, chave):
        """Caminho da chave, resolvido contra a raiz (absoluto vale como está)."""
        return RAIZ / self.valor(chave)

    def saida(self, chave, **marcas):
        """Arquivo de saída `[saidas] <chave>`, dentro de `[saidas] pasta`; os marcadores
        (`{expressao}`, `{base}`) são preenchidos em minúsculas."""
        nome = self.valor(f"saidas.{chave}").format(
            **{k: str(v).lower() for k, v in marcas.items()})
        return self.caminho("saidas.pasta") / nome

    def procedimento(self, sigla):
        """Caminho do procedimento de busca de uma base (saída de `procedimentos gerar`),
        relativo à raiz, pelo padrão `[documentos] procedimento`."""
        return self.valor("documentos.procedimento").replace(
            MARCADORES["documentos.procedimento"], sigla)

    def fonte(self, sigla):
        """Pasta da fonte do procedimento de busca de uma base, relativa à raiz, pelo padrão
        `[documentos] procedimento_fonte`."""
        return self.valor("documentos.procedimento_fonte").replace(
            MARCADORES["documentos.procedimento_fonte"], sigla)

    def protocolo(self):
        return RAIZ / self.valor("protocolo")

    def sementes(self):
        """Arquivo de sementes; ausente termina com CONFIGURACAO, nomeando chave e caminho."""
        caminho = self.caminho("documentos.sementes")
        if not caminho.exists():
            raise ConfiguracaoInvalida(f"{self.nome}: a chave `documentos.sementes` aponta "
                                       f"{self.valor('documentos.sementes')!r}, que não existe")
        return caminho

    def biblioteca(self, chave="zotero.biblioteca"):
        """A biblioteca da chave, na forma da API (`groups/<id>` ou `users/<id>`)."""
        return biblioteca_zotero(self.valor(chave))

    def buscas(self):
        """(biblioteca, nome) da coleção das buscas: a biblioteca de
        `[zotero] library` ou, sem ela, a de `[zotero] biblioteca`; o nome de
        `[zotero] search_collection`, que, ausente, é CONFIGURACAO."""
        nome = self.exige("zotero.search_collection").strip()
        chave = ("zotero.library" if "library" in self.dado["zotero"]
                 else "zotero.biblioteca")
        return self.biblioteca(chave), nome

    def exige(self, chave):
        """Valor de chave opcional do esquema; ausente é CONFIGURACAO, nomeando a chave."""
        secao, campo = chave.split(".")
        if campo not in self.dado.get(secao, {}):
            raise ConfiguracaoInvalida(f"{self.nome}: falta a chave `[{secao}] {campo}`")
        return self.valor(chave)

    def com(self, chave, valor):
        """Cópia com uma chave alterada, sem validar (para o autoteste)."""
        dado = copy.deepcopy(self.dado)
        alvo = dado
        partes = chave.split(".")
        for p in partes[:-1]:
            alvo = alvo.setdefault(p, {})
        alvo[partes[-1]] = valor
        return dado

    def sem(self, chave):
        """Cópia com uma chave retirada, sem validar (para o autoteste)."""
        dado = copy.deepcopy(self.dado)
        alvo = dado
        partes = chave.split(".")
        for p in partes[:-1]:
            alvo = alvo[p]
        del alvo[partes[-1]]
        return dado


def relativo(caminho):
    """Caminho relativo à raiz quando possível; absoluto quando não."""
    try:
        return str(pathlib.Path(caminho).resolve().relative_to(RAIZ))
    except ValueError:
        return str(caminho)


def carrega(caminho=None):
    """Lê e valida o config.toml; confere que o protocolo apontado existe."""
    caminho = pathlib.Path(caminho) if caminho else caminho_padrao()
    if not caminho.exists():
        raise ConfiguracaoInvalida(f"{caminho.name} ausente em {caminho.parent}")
    try:
        with caminho.open("rb") as fh:
            dado = tomllib.load(fh)
    except tomllib.TOMLDecodeError as e:
        raise ConfiguracaoInvalida(f"{caminho} não é TOML válido: {e}") from None
    cfg = Configuracao(dado, caminho)
    if not cfg.protocolo().exists():
        raise ConfiguracaoInvalida(f"{cfg.nome}: a chave `protocolo` aponta "
                                   f"{cfg.valor('protocolo')!r}, que não existe")
    return cfg
