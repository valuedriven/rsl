"""Configuração: o `config.toml` da raiz, carregado sob demanda e validado pelo esquema.

O único caminho fixado é o do próprio `config.toml`, na raiz do projeto. A variável de
ambiente `RSL_CONFIG` aponta outro arquivo; existe para ensaio e autoteste (configuração
inválida, saídas num diretório temporário) e não é parâmetro do projeto.

Caminhos da configuração são relativos à raiz do projeto; caminho absoluto vale como está.
"""

import copy
import os
import pathlib
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
    "dados": ("registro", "validacao", "execucoes", "evidencia"),
    "saidas": ("pasta", "registros", "contagens", "ordem_triagem", "fidelidade",
               "sensibilidade", "aderencia"),
    "documentos": ("procedimento", "procedimento_fonte", "flexoes", "sementes"),
    "planilha": ("campos_validacao",),
}
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
}
# Marcadores que cada padrão de caminho tem de conter.
MARCADORES = {"documentos.procedimento": "{sigla}",
              "documentos.procedimento_fonte": "{sigla}", "saidas.fidelidade": "{expressao}",
              "saidas.sensibilidade": "{base}"}


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


def valida(dado, nome=NOME):
    """Confere o esquema; levanta ConfiguracaoInvalida no primeiro defeito. Devolve o dado."""
    for chave, motivo in RETIRADAS.items():
        if _tem(dado, chave):
            raise ConfiguracaoInvalida(
                f"{nome}: a chave `{chave}` não pertence mais à configuração — {motivo}")
    for secao, chaves in ESQUEMA.items():
        alvo = dado if not secao else dado.get(secao)
        if secao and not isinstance(alvo, dict):
            raise ConfiguracaoInvalida(f"{nome}: falta a seção `[{secao}]`")
        for chave in chaves:
            if chave not in alvo:
                completa = f"{secao}.{chave}" if secao else chave
                raise ConfiguracaoInvalida(f"{nome}: falta a chave `{completa}`")
    for chave, valor in dado.items():
        if chave in ESQUEMA and chave:
            desconhecidas = sorted(set(valor) - set(ESQUEMA[chave]))
            if desconhecidas:
                raise ConfiguracaoInvalida(
                    f"{nome}: chave desconhecida em `[{chave}]`: {desconhecidas}")
        elif chave not in ESQUEMA[""]:
            raise ConfiguracaoInvalida(f"{nome}: chave ou seção desconhecida `{chave}`")
    for chave, marca in MARCADORES.items():
        secao, campo = chave.split(".")
        valor = dado[secao][campo]
        if not isinstance(valor, str) or marca not in valor:
            raise ConfiguracaoInvalida(f"{nome}: `{chave}` {valor!r} não contém {marca}")
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

    def ficha(self, sigla):
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
