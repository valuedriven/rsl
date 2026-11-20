"""Leitura de Markdown: seções, tabelas, escapes e a normalização de texto.

`Trecho` é o texto de uma seção com a linha (índice em `texto.splitlines()` do documento)
em que começa: a localização de cada valor lido sai daí, e o autoteste gera as cópias
defeituosas a partir dela, não de literais do documento.
"""

import re
import unicodedata

from .erros import ProtocoloInvalido


class Trecho(str):
    """Texto com a linha do documento em que começa (0 para o documento inteiro) e, para
    uma seção, a linha do seu cabeçalho."""

    def __new__(cls, texto, linha0=0, cabecalho=None):
        obj = super().__new__(cls, texto)
        obj.linha0 = linha0
        obj.cabecalho = cabecalho
        return obj


def documento(texto):
    return texto if isinstance(texto, Trecho) else Trecho(texto, 0)


def normaliza(s):
    """Caixa baixa, sem acento (decomposição de compatibilidade NFKD), só letras e dígitos
    separados por um espaço. É a única normalização do pacote."""
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def desescapa(s):
    """Desfaz os escapes do Markdown de origem (`\\-`, `\\(`, `\\.`, `\\_`)."""
    for de, para in (("\\-", "-"), ("\\_", "_"), ("\\*", "*"), ("\\(", "("),
                     ("\\)", ")"), ("\\.", "."), ("\\+", "+"), ("\\[", "["),
                     ("\\]", "]"), ("\\|", "|")):
        s = s.replace(de, para)
    return s


def celulas(linha):
    """Células de uma linha de tabela, sem os pipes das pontas."""
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def monta_linha(cels):
    return "| " + " | ".join(cels) + " |"


def e_linha_de_tabela(linha):
    return linha.lstrip().startswith("|")


def _cabecalhos(t, titulo):
    return list(re.finditer(r"^(#+)\s+" + re.escape(titulo) + r"\s*$", t, re.M))


def secao(t, elemento, documento_=None):
    """O trecho da seção `elemento` (gramatica.Secao): do fim do cabeçalho até o próximo
    cabeçalho de nível igual ou maior. Seção com pai é procurada dentro do pai."""
    t = documento(t)
    if elemento.pai is not None:
        t = secao(t, elemento.pai, documento_)
    marcas = _cabecalhos(t, elemento.titulo)
    marca = next((m for m in marcas if len(m.group(1)) == elemento.nivel), None)
    if marca is None:
        if marcas:
            raise ProtocoloInvalido(elemento, f"cabeçalho no nível {len(marcas[0].group(1))}"
                                              f"; a gramática exige o nível {elemento.nivel}",
                                    documento_)
        onde = f" dentro de '{elemento.pai.titulo}'" if elemento.pai else ""
        raise ProtocoloInvalido(elemento, f"seção não encontrada{onde}", documento_)
    resto = t[marca.end():]
    fim = re.search(r"^#{1,%d}\s+\S" % elemento.nivel, resto, re.M)
    # O trecho começa em marca.end(), que pode já estar na linha seguinte ao cabeçalho
    # (`\s*$` consome a quebra): a linha é a da posição, não a do cabeçalho.
    linha0 = t.linha0 + t.count("\n", 0, marca.end())
    cabecalho = t.linha0 + t.count("\n", 0, marca.start())
    return Trecho(resto[:fim.start()] if fim else resto, linha0, cabecalho)


def linha_do_cabecalho(t, elemento):
    """Índice da linha do cabeçalho da seção, no documento `t`."""
    return secao(t, elemento).cabecalho


def paragrafos(bloco):
    return [re.sub(r"\s+", " ", p).strip()
            for p in re.split(r"\n\s*\n", bloco) if p.strip()]


def linhas(trecho):
    """(índice da linha no documento, linha) de cada linha do trecho."""
    trecho = documento(trecho)
    return [(trecho.linha0 + k, l) for k, l in enumerate(trecho.split("\n"))]


# ------------------------------------------------------------------------- tabelas
class Bloco(list):
    """Linhas consecutivas de uma tabela, com o índice da primeira no documento."""

    def __init__(self, linhas_, primeira):
        super().__init__(linhas_)
        self.primeira = primeira


def blocos_de_tabela(trecho):
    """Tabelas Markdown de um trecho: cada uma, a lista das suas linhas consecutivas."""
    saida, atual, inicio = [], [], None
    for idx, linha in linhas(trecho):
        if e_linha_de_tabela(linha):
            if not atual:
                inicio = idx
            atual.append(linha)
        elif atual:
            saida.append(Bloco(atual, inicio))
            atual = []
    if atual:
        saida.append(Bloco(atual, inicio))
    return saida


def linhas_de_tabela(trecho):
    """(índice, linha) das linhas de tabela do trecho, em qualquer tabela."""
    return [(i, l) for i, l in linhas(trecho) if e_linha_de_tabela(l)]


def separador(cels):
    return bool(cels) and all(re.fullmatch(r":?-+:?", c) for c in cels)


def le_tabela(bloco, elemento, exigidas=None, documento_=None):
    """Linhas de uma tabela como dicionários indexados pelo nome da coluna.

    Devolve (cabeçalho, linhas). Coluna exigida ausente ou coluna repetida reprova; coluna
    extra é ignorada. Cada linha leva em `_linha` o índice da linha no documento. Os valores
    são as células brutas: o escape do Markdown fica para quem lê cada coluna.
    """
    exigidas = elemento.colunas if exigidas is None else exigidas
    cab = [desescapa(c).strip() for c in celulas(bloco[0])]
    repetidas = sorted({c for c in cab if c and cab.count(c) > 1})
    if repetidas:
        raise ProtocoloInvalido(elemento, f"coluna repetida {repetidas}", documento_)
    faltam = [c for c in exigidas if c not in cab]
    if faltam:
        raise ProtocoloInvalido(elemento, f"falta a coluna {faltam}; cabeçalho lido {cab}",
                                documento_)
    corpo = [(bloco.primeira + k, l) for k, l in enumerate(bloco)][1:]
    if corpo and separador(celulas(corpo[0][1])):
        corpo = corpo[1:]
    saida = []
    for idx, linha in corpo:
        cels = celulas(linha)
        sobra = [c for c in cels[len(cab):] if c]
        if sobra:
            raise ProtocoloInvalido(elemento, f"linha com mais células que o cabeçalho: "
                                              f"{linha.strip()[:60]!r}", documento_)
        valores = {c: (cels[i] if i < len(cels) else "") for i, c in enumerate(cab) if c}
        valores["_linha"] = idx
        saida.append(valores)
    return cab, saida


def tabela_da_secao(t, elemento, documento_=None):
    """A primeira tabela da seção do elemento, lida pelo cabeçalho. Devolve (bloco, linhas)."""
    tabelas_ = blocos_de_tabela(secao(t, elemento.secao, documento_))
    if not tabelas_:
        raise ProtocoloInvalido(elemento, "tabela ausente", documento_)
    return tabelas_[0], le_tabela(tabelas_[0], elemento, documento_=documento_)[1]


def lista(celula):
    """Itens de uma célula separados por vírgula."""
    return [x.strip() for x in desescapa(celula).split(",") if x.strip()]
