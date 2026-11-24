"""Cobertura de cada base: os blocos compostos da fonte do procedimento de busca medidos
contra a string (STR) do protocolo.

As conferências leem o derivado da base (`fichas.base_derivada`): a fonte e a estrutura dos
blocos que o compositor monta, com os termos de cada faceta em cada consulta. Nada se
reconhece pelo texto do bloco. Continuam independentes do código de composição: o que o
compositor deveria ter posto é recalculado aqui, da STR, da fonte e da flexão, para que um
compositor errado reprove.

A cobertura é medida contra o vocabulário vigente — os termos da STR do protocolo, nos
idiomas que o procedimento de busca declara, sem filtro por linha do CT — e contra a redução própria da base,
declarada termo a termo: termo vigente ausente e não declarado reprova, e termo da base que
não derive da STR também, inclusive o que só conste do quadro terminológico. A cobertura por
faceta sai como número, porque é ela que mede o preço da forma de cada base.
"""

import re

from . import gramatica as G
from .flexao import Indecidivel, formas, formas_de_numero, nao_contavel, vetadas
from .geracao import subsume
from .fichas import MODO_CURADA, MODOS_EXECUCAO
from .leitura import LINHAS, sem_repeticao
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
    idiomas que o procedimento de busca declara, em todas as linhas do CT, classificados pelo
    quadro; `fora_da_string` são os termos do quadro da faceta, em qualquer idioma, que a
    STR não traz. O quadro é vocabulário de referência; o que vale para a busca é a STR.
    """
    f = next(x for x in d["tabelas"] if x["id"] == fid)
    idiomas = decl.get("idiomas", {}).get(fid) or list(d["idiomas"])
    na_str = {normaliza(x) for x in d["strings"][fid]["termos"]}
    # Repetição exata, não normalizada: `ontologia` (pt) e `ontología` (es) são termos
    # distintos da STR, e a base pode distinguir o acento.
    tabela = list(dict.fromkeys(x for i in idiomas for c in LINHAS
                                for x in f["linhas"][i][c]))
    vigentes = [x for x in tabela if normaliza(x) in na_str]
    quadro = sem_repeticao([x for i in d["idiomas"] for c in LINHAS
                             for x in f["linhas"][i][c]])
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


def _idiomas_do_termo(d, fid):
    f = next(x for x in d["tabelas"] if x["id"] == fid)
    saida = {}
    for i in d["idiomas"]:
        for c in LINHAS:
            for x in f["linhas"][i][c]:
                saida.setdefault(x, set()).add(i)
    return saida


def listas_a_mao(base):
    """[(faceta, rótulo, [termos])] das listas de termos que se escrevem à mão na fonte: os
    blocos de string e de subconjunto e as consultas da forma curada (termos entre aspas)."""
    saida = [(s["faceta"], s["id"], s["termos"]) for s in base["facetas"]
             if not s.get("radical")]
    faceta_de = {}
    for c in base.get("curadas", []):
        for fid in c["facetas"]:
            faceta_de.setdefault(fid, []).append(c)
    for fid, cs in faceta_de.items():
        termos = [m for c in cs for m in re.findall(r'"([^"]+)"', c["consulta"])]
        saida.append((fid, "forma curada", termos))
    return saida


def numero_unico_na_base(base, d, excecoes):
    """[(faceta, termo da STR, idioma, lista)] presentes numa lista da base numa só forma de
    número, em idioma de plural explícito. Não conta o termo `nao_contavel`, o de forma
    vetada, o indecidível sem exceção (que já reprova a geração) e o alcançado por
    truncamento."""
    decl = base.get("declaracao") or {}
    plural = decl.get("plural") or {}
    saida = []
    for fid in sorted(d["strings"]):
        idioma_de = _idiomas_do_termo(d, fid)
        da_faceta = decl.get("idiomas", {}).get(fid, [])
        for f_, rotulo, termos in listas_a_mao(base):
            if f_ != fid:
                continue
            presentes = {normaliza(x) for x in termos}
            literais = d["strings"][fid]["literais"]
            ja = formas_de_numero(literais, lambda x: idioma_de.get(x, ()), excecoes)
            for t in literais:
                if normaliza(t) not in presentes or _truncamento_alcanca(t, termos) or t in ja:
                    continue
                for i in sorted(idioma_de.get(t, ())):
                    if i not in da_faceta or plural.get(i) != G.PLURAL_EXPLICITO:
                        continue
                    if nao_contavel(t, i, excecoes) or vetadas(t, i, excecoes):
                        continue
                    try:
                        fs = [x for x, _ in formas(t, i, excecoes)]
                    except Indecidivel:
                        continue
                    if fs and not any(normaliza(x) in presentes for x in fs):
                        saida.append((fid, t, i, rotulo))
    return saida


def consultas_executaveis(base):
    """[(expressão, rótulo, texto)] de cada consulta que vai à base."""
    return [(ident, c["rotulo"] or c["id"], c["texto"])
            for ident, e in sorted(base["expressoes"].items()) for c in e["consultas"]]


def maior_consulta(base):
    """(comprimento, expressão, rótulo) da consulta executável mais longa, ou None."""
    consultas = consultas_executaveis(base)
    if not consultas:
        return None
    ident, rotulo, texto = max(consultas, key=lambda c: len(c[2]))
    return len(texto), ident, rotulo


def esperado_por_faceta(base, d, excecoes):
    """{faceta: termos} que os blocos da base têm de trazer, recalculado sem o compositor:
    os vigentes da STR com as formas de número, ou a forma radical declarada, mais os
    subconjuntos declarados."""
    fonte = base["fonte"]
    dado = fonte["dado"]
    decl = base["declaracao"]
    radical = {r["faceta"]: r["termos"] for r in dado.get("radical", [])}
    saida = {}
    for fid in d["strings"]:
        if fid in radical:
            saida[fid] = set(radical[fid])
            continue
        vigentes_, _ = _vocabulario(fid, d, decl)
        reduzidos = {normaliza(e["termo"]) for e in decl.get("exclusoes", [])
                     if e["faceta"] == fid}
        termos = [x for x in vigentes_ if normaliza(x) not in reduzidos]
        saida[fid] = set(_com_plurais(termos, fid, d, decl, excecoes))
    for s in dado.get("subconjuntos", []):
        saida[s["faceta"]] |= set(_com_plurais(s["termos"], s["faceta"], d, decl, excecoes))
    return saida


def _com_plurais(termos, fid, d, decl, excecoes):
    idioma_de = _idiomas_do_termo(d, fid)
    ja = formas_de_numero(list(d["strings"][fid]["literais"]) + list(termos),
                          lambda x: idioma_de.get(x, ()), excecoes)
    saida = list(termos)
    for t in termos:
        if t in ja:
            continue
        for i in idioma_de.get(t, ()):
            if i in decl["idiomas"].get(fid, []) and \
                    decl["plural"].get(i) == G.PLURAL_EXPLICITO:
                try:
                    saida += [x for x, _ in formas(t, i, excecoes)]
                except Indecidivel:
                    pass
    return saida


def _facetas_da_composicao(d, ident):
    """Facetas exigidas por uma expressão, pela composição lida do protocolo."""
    faceta_de = {s["id"]: fid for fid, s in d["strings"].items()}
    return sorted({faceta_de[x] for g in d["expressoes"][ident] for x in g})


def _ordem_criterio(cid):
    return int(cid[2:])


def cobertura_base(base, d, excecoes=None):
    """Problemas da base: critérios, vocabulário, plural, teto, expressões e execução."""
    excecoes = excecoes or {}
    problemas = []
    decl = base.get("declaracao") or {}
    modos = set(decl.get("derivacoes") or [])
    fonte = f"fonte {base['base']['fonte']}"

    # Os IDs de [[criterios]] são os do protocolo: renumerar o protocolo sem atualizar a
    # fonte deixaria a triagem aplicando um critério que o documento já não nomeia.
    protocolo = {c["id"] for c in d["criterios"]}
    citados = set(base.get("criterios") or [])
    for cid in sorted(citados - protocolo, key=_ordem_criterio):
        problemas.append(f"{fonte}: cita {cid}, que não existe na tabela de critérios do "
                         f"protocolo")
    for cid in sorted(protocolo - citados, key=_ordem_criterio):
        problemas.append(f"{fonte}: não cita {cid}, que o protocolo declara")

    esperado_flexionado = esperado_por_faceta(base, d, excecoes or {})
    for fid in sorted(d["strings"]):
        if not decl.get("idiomas", {}).get(fid):
            problemas.append(f"{fid}: a declaração de cobertura não declara idiomas")
        esperados, fora = _vocabulario(fid, d, decl)
        achados = [x for s in base["facetas"] if s["faceta"] == fid for x in s["termos"]]
        excluidos = [e["termo"] for e in decl.get("exclusoes", []) if e["faceta"] == fid]
        for termo in esperados:
            if any(_mesmo_termo(termo, a) for a in achados):
                continue
            if G.DERIVACAO_RADICAL in modos and any(_radical_alcanca(termo, a) for a in achados):
                continue
            if any(_mesmo_termo(termo, e) for e in excluidos):
                continue
            problemas.append(f"{fid}: {termo!r} está no protocolo, não está nos blocos desta "
                             f"base e não consta da redução declarada")
        for termo in achados:
            # A forma de número por regra ou por exceção vem do recálculo independente do
            # compositor (`esperado_por_faceta`); a heurística de `_mesmo_termo` não conhece
            # todas as terminações (-m/-ns, -ão/-ões, -il/-is, -z/-ces).
            if termo in esperado_flexionado.get(fid, ()):
                continue
            if any(_mesmo_termo(termo, p) for p in esperados):
                continue
            so_quadro = next((p for p in fora if _mesmo_termo(termo, p)), None)
            if so_quadro and _subsumido_por(so_quadro, fid, d):
                continue
            if so_quadro:
                problemas.append(f"{fid}: {termo!r} está nos blocos desta base e não está na "
                                 f"string do protocolo (consta só do quadro: {so_quadro!r})")
                continue
            if G.DERIVACAO_RADICAL in modos and any(_radical_alcanca(p, termo) for p in esperados):
                continue
            problemas.append(f"{fid}: {termo!r} está nos blocos desta base e não deriva do "
                             f"protocolo")
    for e, porque in _radical_sem_alcance(base):
        problemas.append(f"{e['faceta']}: {e['termo']!r} consta da redução como alcançado "
                         f"pela forma radical, e {porque}")

    # Termo só no singular, em idioma de plural explícito, reprova (as listas escritas à
    # mão na fonte: subconjuntos e forma curada; nos blocos gerados, a flexão o impede).
    for fid, termo, idioma, rotulo in numero_unico_na_base(base, d, excecoes):
        problemas.append(f"{fid}: {termo!r} ({idioma}) só no singular em {rotulo}, com "
                         f"plural explícito; acrescentar o plural ou declarar exceção")

    # Plural pela lematização é afirmação sobre a base: só com a lematização daquele idioma
    # medida e a medição citada.
    sintaxe = base.get("sintaxe") or []
    for idioma, valor in sorted((decl.get("plural") or {}).items()):
        if valor != G.PLURAL_LEMATIZACAO:
            continue
        lemas = [s for s in sintaxe if s["categoria"] == G.CATEGORIA_LEMATIZACAO
                 and s.get("idioma") in (None, idioma)]
        medidos = [s for s in lemas if s["situacao"] == G.SITUACAO_MEDICAO and s.get("citacao")]
        if not medidos:
            nomes = ", ".join(repr(s["elemento"]) for s in lemas) or "nenhum elemento"
            problemas.append(f"{fonte}: declara plural {G.PLURAL_LEMATIZACAO!r} em {idioma}, "
                             f"e a lematização não está medida com citação ({nomes} na "
                             f"categoria {G.CATEGORIA_LEMATIZACAO!r})")

    # Teto de caracteres: invariante da partição.
    teto = decl.get("teto")
    if teto is not None:
        for ident, rotulo, texto in consultas_executaveis(base):
            if len(texto) > teto:
                problemas.append(f"{ident}: consulta {rotulo[:60]!r} tem {len(texto)} "
                                 f"caracteres, acima do teto de caracteres declarado ({teto})")

    previstas = sorted(d["expressoes"])
    if sorted(base["expressoes"]) != previstas:
        problemas.append(f"expressões {sorted(base['expressoes'])} não são as do protocolo "
                         f"{previstas}")
    ancoras_ = set(d["ancoras"])
    esperado = esperado_por_faceta(base, d, excecoes)
    for ident, expr in sorted(base["expressoes"].items()):
        if ident not in d["expressoes"]:
            continue
        compostas = _facetas_da_composicao(d, ident)
        if expr["facetas"] != compostas:
            problemas.append(f"{ident}: facetas {expr['facetas']} não são {compostas} do "
                             f"protocolo")
        if not ancoras_ <= set(expr["facetas"]):
            problemas.append(f"{ident}: falta âncora obrigatória ({sorted(ancoras_)})")
        com_bloco = expr["estatuto"] in G.ESTATUTOS_COM_BLOCO
        if com_bloco and not expr["consultas"]:
            problemas.append(f"{ident}: expressão que se executa sem consulta nesta base")
        if not com_bloco and expr["consultas"]:
            problemas.append(f"{ident}: expressão derivada não se executa e não leva bloco")
        consultas = [c for c in expr["consultas"] if c.get("termos") is not None]
        if not consultas:
            continue
        # Os termos dos blocos são os das strings que a expressão declara: a união, por
        # faceta, sobre as consultas da expressão, recalculada sem o compositor.
        for fid in expr["facetas"]:
            uniao = {x for c in consultas for x in c["termos"].get(fid, [])}
            for termo in sorted(esperado.get(fid, set()) - uniao):
                problemas.append(f"{ident}: termo {termo!r} de {fid} não está no bloco")
            for termo in sorted(uniao - esperado.get(fid, set())):
                problemas.append(f"{ident}: termo {termo!r} do bloco não consta das facetas "
                                 f"declaradas ({', '.join(expr['facetas'])})")

    execucao = base["execucao"]
    if execucao["expressao"] != d["executada"]:
        problemas.append(f"a base executa {execucao['expressao']}, e o protocolo declara "
                         f"executada {d['executada']}")
    if execucao["modo"] not in MODOS_EXECUCAO:
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
