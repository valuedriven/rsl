"""Cobertura de cada base: a string do procedimento de busca medida contra a string (STR) do
protocolo.

A cobertura é medida contra o vocabulário vigente — os termos da STR do protocolo, nos
idiomas e camadas que o procedimento de busca declara — e contra a redução própria da base,
declarada termo a termo: termo vigente ausente e não declarado reprova, e termo da base que
não derive da STR também, inclusive o que só conste do quadro terminológico. A cobertura por
faceta sai como número, porque é ela que mede o preço da forma de cada base.
"""

import re

from . import gramatica as G
from .geracao import subsume
from .fichas import MODO_CURADA, MODOS_EXECUCAO, consultas_executaveis, termos_bloco
from .leitura import CAMADAS, sem_repeticao
from .markdown import normaliza

# Palavras de ligação não distinguem termo de termo: "característica do aluno" e
# "características dos alunos" são o mesmo termo qualificado, não dois.
FUNCIONAIS = {"de", "do", "da", "dos", "das", "del", "de", "los", "las", "el", "la",
              "of", "and", "the", "in", "for", "to", "a", "e", "o", "os", "as", "no",
              "na", "nos", "nas", "em", "en", "y", "con", "com", "por", "para"}


def _tokens(s):
    return normaliza(s).split()


def _conteudo(s):
    """Tokens de conteúdo: a palavra de ligação sai, o termo fica."""
    return [t for t in _tokens(s) if t not in FUNCIONAIS]


def _candidatos(tok):
    """Formas de singular do token; duas palavras casam se as formas se tocam.

    Não é lematização: é reconhecimento de flexão de número e de gênero sobre a forma já sem
    acento — plural em -s, -es, -ies, -ais, -eis e -coes —, que é o que os procedimentos de
    busca declaram como desdobramento morfológico.
    """
    c = {tok}
    for sufixo, troca in (("ies", "y"), ("coes", "cao"), ("ais", "al"), ("eis", "el")):
        if tok.endswith(sufixo) and len(tok) > len(sufixo) + 1:
            c.add(tok[:-len(sufixo)] + troca)
    if tok.endswith("s") and len(tok) > 3:
        c.add(tok[:-1])
    if tok.endswith("es") and len(tok) > 4:
        c.add(tok[:-2])
    return c


def _mesmo_termo(a, b):
    """Mesmo termo, admitida a flexão de número e gênero e a palavra de ligação."""
    ta, tb = _conteudo(a), _conteudo(b)
    if not ta or not tb:
        return False
    def cobre(xs, ys):
        return all(any(_candidatos(x) & _candidatos(y) for y in ys) for x in xs)
    return cobre(ta, tb) and cobre(tb, ta)


def _radical_alcanca(termo, consulta):
    """O termo `consulta`, da string da base, alcança `termo` pela forma radical.

    Alcança quando `consulta` está contido em `termo`, por inteiro e na mesma ordem: palavra
    solta casa a palavra em qualquer posição do termo, e frase entre aspas só casa o termo que
    a contém inteira. Partilhar uma palavra não é alcance — `"ontology engineering"` não
    alcança `ontological engineering` —, e a flexão admitida é a de número e gênero de
    `_candidatos`, não a derivação: `ontology` não alcança `ontological`.
    """
    tt, tc = _conteudo(termo), _conteudo(consulta)
    if not tt or not tc or len(tc) > len(tt):
        return False
    return any(all(_candidatos(tt[i + j]) & _candidatos(tc[j]) for j in range(len(tc)))
               for i in range(len(tt) - len(tc) + 1))


def _radical_sem_alcance(base):
    """Linhas da redução cujo motivo invoca a forma radical sem que a string as alcance.

    O motivo escrito é afirmação sobre a busca, e afirmação se confere: linha declarada como
    alcançada pela forma radical que nenhum termo da string alcança é perda de recall com o
    rótulo de cobertura.
    """
    decl = base.get("declaracao") or {}
    radical = G.DERIVACAO_RADICAL in set(decl.get("derivacoes") or [])
    saida = []
    for e in decl.get("exclusoes", []):
        if G.MOTIVO_RADICAL not in normaliza(e["motivo"]):
            continue
        achados = [x for s in base["facetas"] if s["faceta"] == e["faceta"] for x in s["termos"]]
        if not radical:
            saida.append((e, "o procedimento de busca não declara a derivação radical"))
        elif not any(_radical_alcanca(e["termo"], a) for a in achados):
            saida.append((e, "nenhum termo da string o contém"))
    return saida


def _vocabulario(fid, d, decl):
    """Vocabulário de uma faceta para uma base.

    Devolve (vigentes, fora_da_string): `vigentes` são os termos da STR do protocolo nos
    idiomas e camadas que o procedimento de busca declara, classificados pelo quadro;
    `fora_da_string` são os termos do quadro da faceta, em qualquer idioma ou camada, que a
    STR não traz. O quadro é vocabulário de referência; o que vale para a busca é a STR.
    """
    f = next(x for x in d["tabelas"] if x["id"] == fid)
    idiomas = decl.get("idiomas", {}).get(fid) or list(d["idiomas"])
    camadas = CAMADAS if decl.get("camadas") == G.CAMADAS_TODAS else (G.R_NUCLEO.interno,)
    na_str = {normaliza(x) for x in d["strings"][fid]["termos"]}
    tabela = sem_repeticao([x for i in idiomas for c in camadas
                             for x in f["camadas"][i][c]])
    vigentes = [x for x in tabela if normaliza(x) in na_str]
    quadro = sem_repeticao([x for i in d["idiomas"] for c in CAMADAS
                             for x in f["camadas"][i][c]])
    fora = [x for x in quadro if normaliza(x) not in na_str]
    return vigentes, fora


def _subsumido_por(termo_quadro, fid, d):
    """Termo da STR da faceta que subsume o termo do quadro, na regra da geração; ou None."""
    return next((x for x in d["strings"][fid]["literais"] if subsume(x, termo_quadro)), None)


def subsumidos_na_base(base, d):
    """[(faceta, termo da base, termo do quadro, termo da STR que o subsume)].

    É relato, não reprovação: o subsumido no mesmo campo do termo que o subsume é
    redundância a retirar do procedimento de busca; em campo próprio, é especificidade de campo.
    """
    saida = []
    for fid in sorted(d["strings"]):
        _, fora = _vocabulario(fid, d, base.get("declaracao") or {})
        for s in base["facetas"]:
            if s["faceta"] != fid:
                continue
            for termo in s["termos"]:
                p = next((x for x in fora if _mesmo_termo(termo, x)), None)
                por = p and _subsumido_por(p, fid, d)
                if por:
                    saida.append((fid, s.get("id", fid), termo, por))
    return saida


def _truncamento_alcanca(termo, achados):
    """Algum termo truncado (`radical*`) da string alcança o termo, em qualquer número."""
    alvo = normaliza(termo)
    for a in achados:
        if a.endswith("*"):
            prefixo = normaliza(a.rstrip("*"))
            if prefixo and re.search(r"(?:^| )" + re.escape(prefixo), alvo):
                return True
    return False


# Plural irregular de origem latina ou grega (`thesaurus`/`thesauri`, `analysis`/`analyses`).
# Só serve ao relato de número único: a derivação conferida em `cobertura_base` continua
# com a flexão de `_candidatos`, e um par a mais aqui só cala um relato, nunca aprova termo.
_PLURAIS_IRREGULARES = (("us", "i"), ("um", "a"), ("on", "a"), ("is", "es"),
                        ("ex", "ices"), ("ix", "ices"))


def _par_irregular(a, b):
    """`a` e `b` são o mesmo termo em números diferentes por plural irregular da última
    palavra, com as demais palavras iguais."""
    pa, pb = normaliza(a).split(), normaliza(b).split()
    if len(pa) != len(pb) or not pa or pa[:-1] != pb[:-1]:
        return False
    x, y = pa[-1], pb[-1]
    for sing, plur in _PLURAIS_IRREGULARES:
        for s, p in ((x, y), (y, x)):
            if (s.endswith(sing) and p.endswith(plur) and len(s) > len(sing) + 1
                    and s[:-len(sing)] == p[:-len(plur)]):
                return True
    return False


def numero_unico_na_base(base, d):
    """[(faceta, termo da STR)] presentes na string da base numa só forma de número.

    Só em procedimento de busca com `plural: explícito`, e fora do alcance de truncamento. O
    termo cujo par de plural irregular também está na string da base não é relatado: as duas
    formas de número estão lá. É relato, não reprovação: substantivo não contável
    (`education`, `pedagogia`) não tem plural de uso.
    """
    decl = base.get("declaracao") or {}
    if decl.get("plural") != G.PLURAL_EXPLICITO:
        return []
    saida = []
    for fid in sorted(d["strings"]):
        vigentes, _ = _vocabulario(fid, d, decl)
        achados = [x for s in base["facetas"] if s["faceta"] == fid for x in s["termos"]]
        for t in vigentes:
            formas = {normaliza(a) for a in achados if _mesmo_termo(t, a)}
            if len(formas) != 1 or _truncamento_alcanca(t, achados):
                continue
            if any(_par_irregular(t, a) for a in achados):
                continue
            saida.append((fid, t))
    return saida


def maior_consulta(base):
    """(comprimento, expressão, rótulo) da consulta executável mais longa, ou None."""
    consultas = consultas_executaveis(base)
    if not consultas:
        return None
    ident, rotulo, texto = max(consultas, key=lambda c: len(c[2]))
    return len(texto), ident, rotulo


def _facetas_da_composicao(d, ident):
    """Facetas exigidas por uma expressão, pela composição lida do protocolo."""
    faceta_de = {s["id"]: fid for fid, s in d["strings"].items()}
    return sorted({faceta_de[x] for g in d["expressoes"][ident] for x in g})


def _ordem_criterio(cid):
    return int(cid[2:])


def cobertura_base(base, d):
    """Problemas de forma da base: critérios, vocabulário, âncoras, composição, execução."""
    problemas = []
    decl = base.get("declaracao") or {}
    modos = set(decl.get("derivacoes") or [])

    # A seção 2 cita os critérios que a base aplica. Renumerar o protocolo sem atualizar a
    # procedimento de busca deixaria a triagem aplicando um critério que o documento já não nomeia.
    caminho = base["base"]["ficha"]
    protocolo = {c["id"] for c in d["criterios"]}
    citados = set(base.get("criterios") or [])
    for cid in sorted(citados - protocolo, key=_ordem_criterio):
        problemas.append(f"procedimento de busca {caminho}: cita {cid}, que não existe na "
                         f"tabela de critérios do protocolo")
    for cid in sorted(protocolo - citados, key=_ordem_criterio):
        problemas.append(f"procedimento de busca {caminho}: não cita {cid}, que o protocolo "
                         f"declara")

    for fid in sorted(d["strings"]):
        if not decl.get("idiomas", {}).get(fid):
            problemas.append(f"{fid}: a declaração de cobertura não declara idiomas")
        esperados, fora = _vocabulario(fid, d, decl)
        unidade = [s for s in base["facetas"] if s["faceta"] == fid]
        achados = [x for s in unidade for x in s["termos"]]
        excluidos = [e["termo"] for e in decl.get("exclusoes", []) if e["faceta"] == fid]
        for termo in esperados:
            if any(_mesmo_termo(termo, a) for a in achados):
                continue
            # A forma radical declara que uma palavra-raiz presente alcança a expressão
            # inteira. É declaração do procedimento de busca, não omissão silenciosa: a
            # cobertura literal continua sendo reportada, e o que a regra não alcança tem de
            # estar na tabela.
            if G.DERIVACAO_RADICAL in modos and any(_radical_alcanca(termo, a) for a in achados):
                continue
            if any(_mesmo_termo(termo, e) for e in excluidos):
                continue
            problemas.append(f"{fid}: {termo!r} está no protocolo, não está na string desta "
                             f"base e não consta da redução declarada")
        for termo in achados:
            if any(_mesmo_termo(termo, p) for p in esperados):
                continue
            # Termo do quadro que a STR não traz não é vigente: a base não pode executá-lo,
            # nem em flexão.
            so_quadro = next((p for p in fora if _mesmo_termo(termo, p)), None)
            # O subsumido por termo vigente deriva da STR: o procedimento de busca pode
            # usá-lo em campo próprio, como a `STR1b` da ERIC no resumo. É relatado, não
            # reprovado.
            if so_quadro and _subsumido_por(so_quadro, fid, d):
                continue
            if so_quadro:
                problemas.append(f"{fid}: {termo!r} está na string desta base e não está na "
                                 f"string do protocolo (consta só do quadro: {so_quadro!r})")
                continue
            # Derivar por radical é ser raiz de um termo vigente: estar contido nele.
            if G.DERIVACAO_RADICAL in modos and any(_radical_alcanca(p, termo) for p in esperados):
                continue
            problemas.append(f"{fid}: {termo!r} está na string desta base e não deriva do "
                             f"protocolo")
    for e, porque in _radical_sem_alcance(base):
        problemas.append(f"{e['faceta']}: {e['termo']!r} consta da redução como alcançado "
                         f"pela forma radical, e {porque}")

    # Plural pela lematização é afirmação sobre a base, e afirmação se confere: só com a
    # lematização medida e a execução que a mediu citada.
    if decl.get("plural") == G.PLURAL_LEMATIZACAO:
        linha, medida, citacao = base.get("lematizacao") or (None, False, None)
        texto = next(k for k, v in G.D_PLURAL.valores.items() if v == G.PLURAL_LEMATIZACAO)
        rotulo = f"declara plural {texto!r}"
        if linha is None:
            problemas.append(f"procedimento de busca {caminho}: {rotulo}, e a seção "
                             f"'{G.SF_SINTAXE.titulo}' não tem a linha "
                             f"'{G.RF_LEMATIZACAO.texto}'")
        elif not medida:
            problemas.append(f"procedimento de busca {caminho}: {rotulo}, e a linha "
                             f"'{G.RF_LEMATIZACAO.texto}' não está verificada por medição: "
                             f"{linha[:90]!r}")
        elif not citacao:
            problemas.append(f"procedimento de busca {caminho}: {rotulo}, e a linha "
                             f"'{G.RF_LEMATIZACAO.texto}' não cita a execução que a mediu "
                             f"(BDn/<id>)")

    # O teto de caracteres é parâmetro da base: a consulta mais longa que ele seria recusada
    # pela interface ou, pior, truncada em silêncio.
    teto = decl.get("teto")
    if teto is not None:
        for ident, rotulo, texto in consultas_executaveis(base):
            if len(texto) > teto:
                problemas.append(f"{ident}: consulta {rotulo[:60]!r} tem {len(texto)} "
                                 f"caracteres, acima do teto de caracteres declarado "
                                 f"({teto}); particionar sem retirar termo")

    previstas = sorted(d["expressoes"])
    if sorted(base["expressoes"]) != previstas:
        problemas.append(f"expressões {sorted(base['expressoes'])} não são as do protocolo "
                         f"{previstas}")
    ancoras_ = set(d["ancoras"])
    for ident, expr in sorted(base["expressoes"].items()):
        if ident not in d["expressoes"]:
            continue
        esperado = _facetas_da_composicao(d, ident)
        if expr["facetas"] != esperado:
            problemas.append(f"{ident}: facetas {expr['facetas']} não são "
                             f"{esperado} do protocolo")
        if not ancoras_ <= set(expr["facetas"]):
            problemas.append(f"{ident}: falta âncora obrigatória ({sorted(ancoras_)})")
        # Expressão derivada e não materializada nesta base — a sonda da ERIC — não
        # precisa de forma: o que se executa ou se confere tem de ter.
        precisa_forma = expr["estatuto"] in ("executada", "fidelidade", "sonda")
        if precisa_forma and not expr["blocos"]:
            problemas.append(f"{ident}: expressão sem forma legível nesta base")
        # Bloco só onde há execução: a derivada padrão não é forma que se submete. A
        # forma longa é representação não executada e fica fora desta regra.
        if expr["estatuto"] == "derivada" and not expr.get("forma_longa"):
            if expr["blocos"]:
                problemas.append(f"{ident}: expressão derivada não se executa e não leva bloco")
            continue
        if not precisa_forma or not expr["blocos"]:
            continue
        # Bloco que se submete é literal: referência a conjunto depende da numeração da
        # sessão e não se reproduz a partir do procedimento de busca.
        referencias = sorted({r for b in expr["blocos"]
                              for r in re.findall(r"#\d+", b["texto"])})
        if referencias:
            problemas.append(f"{ident}: referência a conjunto {', '.join(referencias)} no "
                             f"bloco — a expressão que se executa é bloco literal")
            continue
        # O conjunto de termos do bloco tem de ser o das strings que a expressão declara:
        # é o que impede a segunda cópia de defasar da seção 3.
        esperados = sem_repeticao([t for s in base["facetas"]
                                    if s["faceta"] in expr["facetas"] for t in s["termos"]])
        achados = sem_repeticao([t for b in expr["blocos"]
                                  for t in termos_bloco(b["texto"])])
        por_norm = {normaliza(t): t for t in esperados}
        no_bloco = {normaliza(t): t for t in achados}
        for k, termo in por_norm.items():
            if k not in no_bloco:
                problemas.append(f"{ident}: termo {termo!r} das facetas declaradas não está "
                                 f"no bloco")
        for k, termo in no_bloco.items():
            if k not in por_norm:
                problemas.append(f"{ident}: termo {termo!r} do bloco não consta das facetas "
                                 f"declaradas ({', '.join(expr['facetas'])})")

    execucao = base["execucao"]
    if execucao["expressao"] != d["executada"]:
        problemas.append(f"a base executa {execucao['expressao']}, e o protocolo declara "
                         f"executada {d['executada']}")
    if execucao["modo"] not in (MODO_CURADA,) + MODOS_EXECUCAO:
        problemas.append(f"modo de execução desconhecido: {execucao['modo']!r}")
    if not execucao["itens"]:
        problemas.append("execução sem consulta legível")
    return problemas


def cobertura_por_faceta(base, d):
    """Números de cobertura por faceta. É medida, não aprovação.

    Separa o que está literalmente na string do que só é alcançado pela forma radical
    declarada: a diferença é o preço de recall que a base assume.
    """
    decl = base.get("declaracao") or {}
    modos = set(decl.get("derivacoes") or [])
    saida = {}
    for fid in sorted(d["strings"]):
        tabela, _ = _vocabulario(fid, d, decl)
        achados = [x for s in base["facetas"] if s["faceta"] == fid for x in s["termos"]]
        excluidos = [e["termo"] for e in decl.get("exclusoes", []) if e["faceta"] == fid]
        cobertos = sum(1 for t in tabela if any(_mesmo_termo(t, a) for a in achados))
        por_radical = sum(1 for t in tabela
                          if not any(_mesmo_termo(t, a) for a in achados)
                          and G.DERIVACAO_RADICAL in modos
                          and any(_radical_alcanca(t, a) for a in achados))
        declarados = sum(1 for t in tabela
                         if not any(_mesmo_termo(t, a) for a in achados)
                         and not (G.DERIVACAO_RADICAL in modos
                                  and any(_radical_alcanca(t, a) for a in achados))
                         and any(_mesmo_termo(t, e) for e in excluidos))
        saida[fid] = {"esperados": len(tabela), "na_string": len(achados),
                      "cobertos": cobertos, "por_radical": por_radical,
                      "declarados": declarados,
                      "descobertos": len(tabela) - cobertos - por_radical - declarados}
    return saida
