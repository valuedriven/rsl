"""Flexão de número dos termos: regra regular de pt, en e es, exceções declaradas pelo
pesquisador e recusa do que a regra não decide.

A regra é conservadora de propósito: a terminação que admite mais de um plural (o -ão do
português, o -s final, o -f do inglês), a palavra de classe adjetiva, o gerúndio e o termo
com conjunção são indecidíveis, e a flexão NÃO escolhe uma das formas. O indecidível reprova
a geração até haver exceção declarada no arquivo de exceções (`[documentos] flexoes`), com a
origem que a sustenta. A exceção prevalece sobre a regra.

Regra por idioma:
  en  flexiona-se a última palavra;
  pt  flexionam-se a primeira palavra e as que a seguem até a primeira preposição, artigo ou
  es  contração; o plural tem a grafia do idioma, com o acento que a flexão tira ou põe.
"""

import tomllib
import unicodedata

from . import gramatica as G
from .erros import ProtocoloInvalido
from .fonte import valida_esquema

ORIGEM_REGRA, ORIGEM_EXCECAO = "regra", "exceção"

# Palavras que encerram o trecho flexionado em pt e es (preposição, artigo, contração).
PARADAS = {
    "pt": {"de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "ao", "aos", "à",
           "às", "a", "o", "os", "as", "por", "pelo", "pela", "pelos", "pelas", "para",
           "com", "sem", "sob", "sobre", "entre", "num", "numa"},
    "es": {"de", "del", "la", "las", "el", "los", "en", "a", "al", "por", "para", "con",
           "sin", "sobre", "entre"},
    "en": set(),
}
CONJUNCOES = {"pt": {"e", "ou"}, "es": {"y", "e", "o", "u"}, "en": {"and", "or"}}
# Preposições do inglês: na locução com preposição o núcleo não é a última palavra
# (`situation of use`), e a regra "flexiona-se a última palavra" erraria.
PREPOSICOES_EN = {"of", "for", "in", "to", "on", "at", "by", "with", "from", "into"}
# Terminações de adjetivo em inglês: a última palavra adjetiva não é núcleo flexionável.
ADJETIVO_EN = ("al", "ic", "ive", "ous", "ful", "less", "able", "ible", "ed", "aware")
# Terminações de adjetivo em pt e es. Só valem para o termo de uma palavra (adjetivo
# isolado): na locução, a primeira palavra é o núcleo, e o adjetivo que a segue concorda com
# ela. O adjetivo isolado não tem núcleo explícito, e a regra não decide se o plural se usa.
ADJETIVO_PT_ES = {"pt": ("al", "ar", "ico", "ica", "ivo", "iva", "oso", "osa", "vel"),
                  "es": ("al", "ar", "ico", "ica", "ivo", "iva", "oso", "osa", "ble")}


class Indecidivel(Exception):
    def __init__(self, termo, idioma, motivo):
        self.termo, self.idioma, self.motivo = termo, idioma, motivo
        super().__init__(f"{termo!r} ({idioma}): {motivo}")


def _sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _tem_acento(s):
    return _sem_acento(s) != s


# ---------------------------------------------------------------------- por palavra
def _plural_en(p, termo):
    base = p.split("-")[-1].lower()
    pre = p[:len(p) - len(base)]
    if base.endswith("ing"):
        raise Indecidivel(termo, "en", "terminação -ing (gerúndio, em geral não contável)")
    if base.endswith(ADJETIVO_EN) and not base.endswith(("ion",)):
        raise Indecidivel(termo, "en", "classe adjetiva")
    if base.endswith("s"):
        raise Indecidivel(termo, "en", "terminação -s")
    if base.endswith(("f", "fe")):
        raise Indecidivel(termo, "en", "terminação -f")
    if base.endswith(("um", "ex", "ix")) or (base.endswith("on") and not base.endswith("ion")):
        raise Indecidivel(termo, "en", f"terminação -{base[-2:]} (plural latino ou grego)")
    if base.endswith("o"):
        raise Indecidivel(termo, "en", "terminação -o")
    if base.endswith("y") and len(base) > 1 and base[-2] not in "aeiou":
        return pre + base[:-1] + "ies"
    if base.endswith(("x", "z", "ch", "sh")):
        return pre + base + "es"
    return pre + base + "s"


def _plural_pt(p, termo):
    w = p.lower()
    if w.endswith("ão"):
        raise Indecidivel(termo, "pt", "terminação -ão")
    if w.endswith("s") or w.endswith("x"):
        raise Indecidivel(termo, "pt", f"terminação -{w[-1]}")
    if w.endswith("il"):
        raise Indecidivel(termo, "pt", "terminação -il")
    if w.endswith("al"):
        return p[:-2] + "ais"
    if w.endswith("el"):
        return p[:-2] + ("eis" if _tem_acento(w[:-2]) else "éis")
    if w.endswith("ol"):
        return p[:-2] + ("ois" if _tem_acento(w[:-2]) else "óis")
    if w.endswith("ul"):
        return p[:-2] + "uis"
    if w.endswith("m"):
        return p[:-1] + "ns"
    if w.endswith(("r", "z")):
        return p + "es"
    if w[-1] in "aeiouáéóâêôã":
        return p + "s"
    raise Indecidivel(termo, "pt", f"terminação -{w[-1]}")


def _plural_es(p, termo):
    w = p.lower()
    if w.endswith(("s", "x", "y")):
        raise Indecidivel(termo, "es", f"terminação -{w[-1]}")
    if w.endswith("z"):
        return p[:-1] + "ces"
    if w[-1] in "aeoáéó":
        return p + "s"
    if w[-1] in "iuíú":
        raise Indecidivel(termo, "es", f"terminação -{w[-1]}")
    if w.endswith("n"):
        # Oxítona acentuada perde o acento (situación → situaciones, patrón → patrones);
        # sem acento, a paroxítona ganha acento (imagen → imágenes): indecidível.
        if w[-2] in "áéíóú":
            return p[:-2] + _sem_acento(p[-2]) + "nes"
        raise Indecidivel(termo, "es", "terminação -n sem acento")
    if w[-1] in "lrdj":
        return p + "es"
    raise Indecidivel(termo, "es", f"terminação -{w[-1]}")


def plural_por_regra(termo, idioma):
    """O plural regular de `termo` em `idioma`, ou Indecidivel."""
    palavras = termo.split()
    if not palavras:
        raise Indecidivel(termo, idioma, "termo vazio")
    if idioma not in PARADAS:
        raise Indecidivel(termo, idioma, "idioma sem regra")
    if any(p.lower() in CONJUNCOES[idioma] for p in palavras):
        raise Indecidivel(termo, idioma, "termo com conjunção")
    if idioma == "en":
        if any(p.lower() in PREPOSICOES_EN for p in palavras[:-1]):
            raise Indecidivel(termo, idioma, "locução com preposição")
        return " ".join(palavras[:-1] + [_plural_en(palavras[-1], termo)])
    if len(palavras) == 1 and palavras[0].lower().endswith(ADJETIVO_PT_ES[idioma]):
        raise Indecidivel(termo, idioma, "classe adjetiva (adjetivo isolado)")
    funcao = _plural_pt if idioma == "pt" else _plural_es
    saida, parado = [], False
    for p in palavras:
        if not parado and p.lower() in PARADAS[idioma]:
            parado = True
        saida.append(p if parado else funcao(p, termo))
    return " ".join(saida)


# ------------------------------------------------------------------- exceções
def le_excecoes(ctx):
    """{(termo, idioma): exceção}, do arquivo `[documentos] flexoes`; vazio sem o arquivo.
    Exceção sem `origem`, de tipo fora do domínio ou repetida reprova com
    PROTOCOLO_ILEGIVEL."""
    texto = ctx.texto_flexoes
    doc = f"{G.FLEXOES} ({ctx.config.valor('documentos.flexoes')})"
    if not texto.strip():
        return {}
    try:
        dado = tomllib.loads(texto)
    except tomllib.TOMLDecodeError as e:
        raise ProtocoloInvalido(G.T_EXCECOES, f"não é TOML válido: {e}", doc) from None
    valida_esquema(dado, doc, raiz=G.T_RAIZ_FLEXOES)
    saida = {}
    for i, e in enumerate(dado.get("excecoes", []), 1):
        chave = (e["termo"], e["idioma"])
        onde = f"excecoes[{i}] {e['termo']!r} ({e['idioma']})"
        if chave in saida:
            raise ProtocoloInvalido(G.T_EXCECOES, f"{onde}: exceção repetida para o termo e "
                                                  f"o idioma", doc)
        if not e["origem"].strip():
            raise ProtocoloInvalido(G.T_EXCECOES, f"{onde}: `origem` vazia", doc)
        if e["tipo"] in (G.EXC_IRREGULAR, G.EXC_VETADA) and not e.get("formas"):
            raise ProtocoloInvalido(G.T_EXCECOES, f"{onde}: tipo {e['tipo']!r} sem "
                                                  f"`formas`", doc)
        if e["tipo"] == G.EXC_NAO_CONTAVEL and e.get("formas"):
            raise ProtocoloInvalido(G.T_EXCECOES, f"{onde}: `nao_contavel` não tem `formas`",
                                    doc)
        saida[chave] = e
    return saida


def orfas(excecoes, d, a_mao=()):
    """Exceções de termo que não está em nenhuma STR nem em lista escrita à mão na fonte de
    uma base (`a_mao`: termos de subconjuntos e da forma curada), para relato."""
    usados = {t for s in d["strings"].values() for t in s["literais"]} | set(a_mao)
    return [k for k in excecoes if k[0] not in usados]


def formas(termo, idioma, excecoes):
    """[(forma de plural, origem)] de `termo` em `idioma`; [] se não contável. A exceção
    prevalece sobre a regra; a vetada tira da regra a forma que não se usa."""
    e = excecoes.get((termo, idioma))
    if e is not None:
        if e["tipo"] == G.EXC_IRREGULAR:
            return [(f, ORIGEM_EXCECAO) for f in e["formas"]]
        if e["tipo"] == G.EXC_NAO_CONTAVEL:
            return []
        try:
            regra = plural_por_regra(termo, idioma)
        except Indecidivel:
            return []
        return [] if regra in e["formas"] else [(regra, ORIGEM_REGRA)]
    return [(plural_por_regra(termo, idioma), ORIGEM_REGRA)]


def formas_de_numero(termos, idiomas_de, excecoes):
    """Formas de plural (regra ou exceção) dos termos da lista: um termo que já é forma de
    número de outro (`thesauri` de `thesaurus`) não se flexiona de novo."""
    saida = set()
    for t in termos:
        for i in idiomas_de(t):
            try:
                saida |= {f for f, _ in formas(t, i, excecoes)}
            except Indecidivel:
                pass
    return saida


def vetadas(termo, idioma, excecoes):
    e = excecoes.get((termo, idioma))
    return list(e["formas"]) if e and e["tipo"] == G.EXC_VETADA else []


def nao_contavel(termo, idioma, excecoes):
    e = excecoes.get((termo, idioma))
    return bool(e) and e["tipo"] == G.EXC_NAO_CONTAVEL
