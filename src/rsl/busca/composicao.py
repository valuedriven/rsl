"""Álgebra da composição: pertinência a uma expressão, deriváveis e a prova das relações.

Cada expressão é um AND de grupos; cada grupo é uma disjunção de facetas. As relações
entre as expressões vêm dos papéis calculados na leitura (`leitura.papeis`), não de
identificadores fixados.
"""

import itertools


def grupos_em_facetas(expressoes, faceta_de):
    """Composição em STRn → composição em facetas (FCTn)."""
    return {eb: [[faceta_de[s] for s in g] for g in gs] for eb, gs in expressoes.items()}


def combinacoes(facetas):
    """Todas as combinações das facetas com string (2^n)."""
    facetas = sorted(set(facetas))
    return [set(c) for r in range(len(facetas) + 1)
            for c in itertools.combinations(facetas, r)]


def satisfaz_em(grupos, ident, fac):
    """Pertinência a uma expressão: todo grupo satisfeito, cada grupo por uma faceta."""
    return all(any(f in fac for f in grupo) for grupo in grupos[ident])


def derivaveis(grupos, executada, facetas):
    """Expressões cujo conjunto está contido na executada, provado sobre as combinações.

    A sonda é superconjunto da executada: a pertinência a ela NÃO se calcula sobre a
    exportação da executada, porque os registros que só a sonda recupera não estão nesse
    arquivo. Ela entra com execução própria, e por isso fica fora desta lista.
    """
    conjuntos = {eb: set() for eb in grupos}
    for fac in combinacoes(facetas):
        for eb in grupos:
            if satisfaz_em(grupos, eb, fac):
                conjuntos[eb].add(frozenset(fac))
    alvo = conjuntos[executada]
    return {eb for eb, s in conjuntos.items() if eb != executada and s <= alvo}


def prova_da_composicao(grupos, papeis, faceta_de):
    """Confere a álgebra das expressões sobre todas as combinações de faceta.

    As relações vêm dos papéis: a executada é a união das específicas; a sonda contém toda
    expressão; cada geral está contida em cada específica cuja string distintiva ela exige;
    as deriváveis são a composição menos executada e sonda.

    A prova existe porque o caso degenerado passa em silêncio: com a lista de facetas
    errada, todas as combinações dão falso, a união vale trivialmente e o erro só aparece
    quando a busca roda. Por isso toda expressão precisa ser satisfeita por ao menos uma
    combinação, além das contenções.
    """
    exec_, sonda = papeis["executada"], papeis["sonda"]
    especificas = {eb: faceta_de[s] for eb, s in papeis["especificas"].items()}
    gerais = {eb: {faceta_de[g[0]] for g in alem if len(g) == 1}
              for eb, alem in papeis["gerais"].items()}
    facetas = set(faceta_de.values())
    combos = combinacoes(facetas)
    problemas = []
    faltam = sorted(({exec_, sonda} | set(especificas) | set(gerais)) - set(grupos))
    if faltam:
        return [f"expressões dos papéis ausentes da composição: {faltam}"]
    if not especificas:
        problemas.append(f"nenhuma expressão específica: a executada {exec_} não tem de "
                         f"que ser a união")
    for eb in grupos:
        if not any(satisfaz_em(grupos, eb, f) for f in combos):
            problemas.append(f"{eb} não é satisfeita por nenhuma combinação de facetas — "
                             f"mapeamento de faceta provavelmente errado")
    for f in combos:
        s = {eb: satisfaz_em(grupos, eb, f) for eb in grupos}
        uniao = any(s[e] for e in especificas)
        if especificas and s[exec_] != uniao:
            problemas.append(f"{exec_} ≠ {' ∪ '.join(sorted(especificas))} em {sorted(f)}")
        for eb in grupos:
            if eb != sonda and s[eb] and not s[sonda]:
                problemas.append(f"{sonda} não contém {eb} em {sorted(f)}")
        for g, exige in gerais.items():
            contem = [e for e, fac in especificas.items() if fac in exige]
            if s[g] and not all(s[e] for e in contem):
                problemas.append(f"{g} não está contida em {' e '.join(sorted(contem))} "
                                 f"em {sorted(f)}")
    esperadas = set(grupos) - {exec_, sonda}
    deriv = derivaveis(grupos, exec_, facetas)
    if deriv != esperadas:
        problemas.append(f"deriváveis de {exec_} deveriam ser {sorted(esperadas)} "
                         f"(composição menos executada e sonda), não {sorted(deriv)}")
    return problemas
