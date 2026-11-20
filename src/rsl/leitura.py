"""Leitura do protocolo: questões, facetas, quadro, instrumentos, strings, expressões,
critérios, fontes e sementes.

O protocolo (chave `protocolo` do config.toml) é a fonte única desses valores. Parâmetros
estruturais — composição das expressões, instrumentos, bases, conjunto-semente e idiomas do
quadro — vêm só do protocolo: ausência ou valor inválido reprova. Os demais têm padrão no
config.toml; o que o protocolo declara prevalece, e trecho presente e ilegível reprova, sem
cair no padrão. A forma exigida está em `gramatica.py`.

Cada leitor registra em `d["locais"]` a linha (índice em `texto.split("\\n")`) de onde leu
cada valor: é dela que o autoteste gera as cópias defeituosas.
"""

import re
import urllib.parse

from . import gramatica as G
from .erros import ProtocoloInvalido
from .markdown import (blocos_de_tabela, celulas, desescapa, le_tabela, linhas,
                       linhas_de_tabela, lista, normaliza, paragrafos, secao,
                       tabela_da_secao)

CAMADAS = tuple(r.interno for r in G.CAMADAS)
ORIGEM_PROTOCOLO = "protocolo"


def origem_padrao(cfg):
    return f"padrão ({cfg.nome})"


# ------------------------------------------------------------------------ parâmetros
def _parametro(ctx, params, nome, valor_protocolo, chave_padrao):
    """O do protocolo, se declarado (não None); senão, o padrão do config.toml.

    `params` acumula valor e origem, que `mostrar` exibe. Trecho do protocolo presente e
    ilegível não chega aqui: o leitor levanta ProtocoloInvalido antes.
    """
    if valor_protocolo is not None:
        valor, origem = valor_protocolo, ORIGEM_PROTOCOLO
    else:
        valor, origem = ctx.config.valor(chave_padrao), origem_padrao(ctx.config)
    params[nome] = {"valor": valor, "origem": origem}
    return valor


def _estrutural(params, nome, valor):
    """Parâmetro estrutural: só do protocolo. O leitor já reprovou a ausência."""
    params[nome] = {"valor": valor, "origem": ORIGEM_PROTOCOLO}
    return valor


def numeracao(ids, identificador, onde, documento=G.PROTOCOLO):
    """Identificadores em sequência a partir de 1: `prefixo1`, `prefixo2`, ..."""
    prefixo = identificador.prefixo
    esperado = [f"{prefixo}{k}" for k in range(1, len(ids) + 1)]
    if not ids:
        raise ProtocoloInvalido(identificador, f"{onde}: nenhum {prefixo}n encontrado",
                                documento)
    if ids != esperado:
        raise ProtocoloInvalido(identificador, f"{onde} fora da numeração {prefixo}1 a "
                                               f"{prefixo}{len(ids)}: {ids}", documento)


def percentual(s):
    return float(s.replace(",", ".")) / 100


def sem_repeticao(seq):
    vistos, saida = set(), []
    for x in seq:
        k = normaliza(x)
        if k and k not in vistos:
            vistos.add(k)
            saida.append(x)
    return saida


# ------------------------------------------------------------------------ questões
def questoes(t, locais):
    bloco = secao(t, G.S_QGR)
    paras = paragrafos(bloco)
    if not paras:
        raise ProtocoloInvalido(G.S_QGR, "questão geral de revisão vazia")
    m = G.M_QGR.padrao.match(paras[0])
    if not m:
        raise ProtocoloInvalido(G.M_QGR, "questão geral sem o identificador QGR")
    locais["qgr"] = next(i for i, l in linhas(bloco) if G.M_QGR.padrao.match(l))
    pergunta = m.group(1).strip()
    estrutura = ""
    fim_estrutura = re.compile(r"\s*" + re.escape(G.S_QER.titulo) + r":\s*$")
    for p in paras[1:]:
        if G.M_ESTRUTURA.padrao.match(p):
            estrutura = fim_estrutura.sub("", p).strip()
    if not estrutura:
        raise ProtocoloInvalido(G.M_ESTRUTURA, "estrutura PICo da questão não declarada")
    locais["estrutura"] = next(i for i, l in linhas(bloco) if G.M_ESTRUTURA.padrao.match(l))

    especificas, locais["qer"] = [], {}
    for idx, linha in linhas(secao(t, G.S_QER)):
        m = G.F_QER.padrao.match(linha)
        if m:
            especificas.append({"id": m.group(1), "texto": m.group(2).strip()})
            locais["qer"][m.group(1)] = idx
    numeracao([e["id"] for e in especificas], G.I_QER, "questões específicas")
    return {"id": "QGR", "questao_principal": pergunta, "estrutura_pico": estrutura,
            "questoes_especificas": especificas}


# ------------------------------------------------------------------------- facetas
def palavras(t, locais=None):
    """Nome e papel de cada faceta: `Faceta n (FCTn): nome [(âncora obrigatória k)]`.

    O nome é todo o resto da linha, hífens incluídos; o sufixo de âncora, entre parênteses,
    é opcional. Travessão residual (forma antiga, com cor) e parêntese de âncora mal formado
    reprovam: leitura tolerante faria a cor ou o sufixo entrarem no nome em silêncio.
    """
    locais = {} if locais is None else locais
    locais["faceta"] = {}
    saida = []
    for idx, linha in linhas(secao(t, G.S_PALAVRAS)):
        m = G.F_FACETA.padrao.match(linha)
        if not m:
            continue
        n = int(m.group(1))
        codigo = m.group(2) or ""
        esperado = f"{G.I_FCT.prefixo}{n}"
        if codigo != esperado:
            achado = codigo if codigo else "ausente"
            raise ProtocoloInvalido(G.I_FCT, f"faceta {n}: identificador {achado!r} não "
                                             f"corresponde a {esperado}")
        corpo = desescapa(m.group(3)).strip()
        if "—" in corpo:
            raise ProtocoloInvalido(G.F_FACETA, f"faceta {esperado}: travessão na linha "
                                                f"({corpo!r}); a forma é `{G.F_FACETA.texto}`")
        ma = G.F_ANCORA.padrao.search(corpo)
        nome = corpo[:ma.start()].strip() if ma else corpo
        if re.search(G.PALAVRA_ANCORA, nome, re.I):
            raise ProtocoloInvalido(G.F_ANCORA, f"faceta {esperado}: âncora fora da forma "
                                                f"`{G.F_ANCORA.texto}` no fim da linha: "
                                                f"{corpo!r}")
        if not nome:
            raise ProtocoloInvalido(G.F_FACETA, f"faceta {esperado}: sem nome")
        saida.append({"id": esperado, "nome": nome, "ancora": bool(ma)})
        locais["faceta"][esperado] = idx
    numeracao([f["id"] for f in saida], G.I_FCT, "facetas")
    return saida


def _termos_celula(celula):
    """Termos de uma célula, separados por `\\- `. O hífen interno vem sem escape."""
    partes = re.split(G.SEPARADOR_TERMOS, celula)
    return [desescapa(p).strip() for p in partes if p.strip()]


def tabelas(t, pal, locais):
    """As tabelas do controle terminológico, uma por faceta, com as camadas por idioma.

    O cabeçalho `| FCTn | pt | en | es |` dá a faceta e os idiomas: o idioma de cada coluna
    é o nome no cabeçalho, não a posição. O primeiro quadro fixa a ordem dos idiomas do
    projeto; os demais têm de ter o mesmo conjunto, em qualquer ordem. As três camadas são
    linhas exigidas, pelo rótulo.

    Devolve (tabelas, idiomas).
    """
    nomes = {f["id"]: f for f in pal}
    locais["quadro"] = {}
    saida, idiomas = [], None
    for bloco in blocos_de_tabela(secao(t, G.S_CONTROLE)):
        m = G.I_FCT.casa(celulas(bloco[0])[0])
        if not m:
            continue
        ident = f"{G.I_FCT.prefixo}{int(m.group(1))}"
        if ident not in nomes:
            raise ProtocoloInvalido(G.T_QUADRO, f"tabela da faceta {ident} sem palavra "
                                                f"significativa")
        cab, linhas_ = le_tabela(bloco, G.T_QUADRO, exigidas=())
        proprios = cab[1:]
        if not proprios or any(not i for i in proprios):
            raise ProtocoloInvalido(G.T_QUADRO, f"quadro de {ident}: coluna de idioma sem "
                                                f"nome no cabeçalho {cab}")
        if idiomas is None:
            idiomas = tuple(proprios)
        elif set(proprios) != set(idiomas):
            raise ProtocoloInvalido(
                G.T_QUADRO, f"quadro de {ident}: idiomas {sorted(proprios)} diferem dos "
                            f"idiomas {sorted(idiomas)} do quadro de {saida[0]['id']} — "
                            f"faltam {sorted(set(idiomas) - set(proprios))}, sobram "
                            f"{sorted(set(proprios) - set(idiomas))}")
        atual = {"id": ident, "nome": nomes[ident]["nome"], "ancora": nomes[ident]["ancora"],
                 "camadas": {i: {c: [] for c in CAMADAS} for i in idiomas}}
        saida.append(atual)
        local = {"cabecalho": bloco.primeira}
        for linha in linhas_:
            rotulo = linha[cab[0]].strip("* ").strip()
            camada = next((r for r in G.CAMADAS if rotulo.startswith(r.texto)), None)
            if camada is None:
                continue
            local[camada.interno] = linha["_linha"]
            for idioma in idiomas:
                atual["camadas"][idioma][camada.interno] = _termos_celula(linha[idioma])
        faltam = [r for r in G.CAMADAS if r.interno not in local]
        if faltam:
            raise ProtocoloInvalido(faltam[0], f"quadro de {ident}: falta a linha "
                                               f"'{faltam[0].texto}…'")
        locais["quadro"][ident] = local

    ids = [f["id"] for f in saida]
    if sorted(ids) != sorted(nomes) or len(set(ids)) != len(ids):
        raise ProtocoloInvalido(G.T_QUADRO, f"esperava uma tabela por faceta "
                                            f"({sorted(nomes)}), achei {ids}")
    for f in saida:
        f["termos"] = {i: sem_repeticao(
            [x for c in CAMADAS for x in f["camadas"][i][c]]) for i in idiomas}
    return saida, idiomas


# -------------------------------------------------------------------- instrumentos
def instrumentos(t, ids_facetas, idiomas, locais):
    """Instrumentos da tabela de instrumentos, pelo nome da coluna.

    Devolve (por sigla, por faceta). Sem padrão: toda faceta do quadro tem de constar da
    coluna FCTs de algum instrumento, e instrumento `Automático` tem de ter cliente com o
    nome da sua sigla.
    """
    from .termos.clientes import siglas as clientes_automaticos          # noqa: PLC0415
    T = G.T_INSTRUMENTOS
    c_sigla, c_nome, c_modo, c_caminho, c_idiomas, c_fcts = T.colunas
    bloco, tabela = tabela_da_secao(t, T)
    locais["cabecalho_instrumentos"] = bloco.primeira
    locais["instrumento"] = {}
    por_sigla = {}
    for linha in tabela:
        valores = {c: desescapa(linha[c]).strip() for c in T.colunas}
        sigla = valores[c_sigla] or "?"
        vazios = [c for c, v in valores.items() if not v]
        if vazios:
            raise ProtocoloInvalido(T, f"linha {sigla}: campo vazio {vazios}")
        if sigla in por_sigla:
            raise ProtocoloInvalido(T, f"sigla repetida {sigla!r}")
        if valores[c_modo] not in G.D_MODO.valores:
            raise ProtocoloInvalido(G.D_MODO, f"linha {sigla}: {c_modo} {valores[c_modo]!r} "
                                              f"fora dos admitidos {list(G.D_MODO.valores)}")
        url = urllib.parse.urlparse(valores[c_caminho])
        if url.scheme not in ("http", "https") or not url.netloc:
            raise ProtocoloInvalido(T, f"linha {sigla}: {c_caminho} {valores[c_caminho]!r} "
                                       f"não é URL http(s) bem formada")
        langs, fcts = lista(linha[c_idiomas]), lista(linha[c_fcts])
        for campo, itens in ((c_idiomas, langs), (c_fcts, fcts)):
            repetidos = sorted({x for x in itens if itens.count(x) > 1})
            if repetidos:
                raise ProtocoloInvalido(T, f"linha {sigla}: {campo} com valor repetido "
                                           f"{repetidos}")
        fora = [i for i in langs if i not in idiomas]
        if fora:
            raise ProtocoloInvalido(T, f"linha {sigla}: idioma {fora} fora dos idiomas do "
                                       f"quadro terminológico {list(idiomas)}")
        fora = [f for f in fcts if f not in ids_facetas]
        if fora:
            raise ProtocoloInvalido(T, f"linha {sigla}: {c_fcts} {fora} não é faceta do "
                                       f"protocolo {list(ids_facetas)}")
        por_sigla[sigla] = {"sigla": sigla, "nome": valores[c_nome],
                            "modo": G.D_MODO.valores[valores[c_modo]],
                            "caminho": valores[c_caminho], "idiomas": langs, "facetas": fcts}
        locais["instrumento"][sigla] = linha["_linha"]
    if not por_sigla:
        raise ProtocoloInvalido(T, "sem instrumento")
    automaticos = [s for s, i in por_sigla.items() if i["modo"] == G.MODO_AUTOMATICO]
    if automaticos:
        clientes = clientes_automaticos()
        sem = [s for s in automaticos if s not in clientes]
        if sem:
            raise ProtocoloInvalido(G.D_MODO, f"instrumento {G.MODO_AUTOMATICO} sem cliente "
                                              f"automatizado: {sem}; clientes existentes: "
                                              f"{clientes}")
    por_faceta = {fid: [i for i in por_sigla.values() if fid in i["facetas"]]
                  for fid in ids_facetas}
    faltam = [f for f, lista_ in por_faceta.items() if not lista_]
    if faltam:
        raise ProtocoloInvalido(T, f"faceta(s) sem instrumento na coluna {c_fcts}: {faltam}")
    return por_sigla, por_faceta


def instrumentos_do_termo(d, fid, idioma):
    """Instrumentos em que se valida um termo da faceta `fid` no `idioma`."""
    return [i for i in d["instrumentos_por_faceta"][fid] if idioma in i["idiomas"]]


# ------------------------------------------------------------------------- strings
def strings(t, ids_faceta, locais):
    """Termos executados de cada faceta, extraídos das strings entre aspas."""
    locais["string"] = {}
    saida = {}
    for idx, linha in linhas_de_tabela(secao(t, G.S_STRINGS)):
        cels = celulas(linha)
        if len(cels) < 3:
            continue
        mi, mf = G.I_STR.casa(cels[0]), G.I_FCT.casa(cels[1])
        if not (mi and mf):
            continue
        n, nf = int(mi.group(1)), int(mf.group(1))
        if n != nf:
            raise ProtocoloInvalido(G.I_STR, f"{cels[0]} está declarada como {cels[1]}: "
                                             f"identificadores não casam")
        id_faceta = f"{G.I_FCT.prefixo}{n}"
        id_string = f"{G.I_STR.prefixo}{n}"
        if id_faceta not in ids_faceta:
            raise ProtocoloInvalido(G.I_STR, f"{id_string} sem faceta {id_faceta} nas "
                                             f"palavras significativas")
        celula = cels[2]
        termos = G.F_STRING.padrao.findall(celula)
        if not termos:
            raise ProtocoloInvalido(G.F_STRING, f"string da faceta {n} sem termos entre "
                                                f"aspas")
        residuo = G.F_STRING.padrao.sub("", celula)
        residuo = residuo.replace("OR", " ").replace("(", " ").replace(")", " ")
        if residuo.strip(" .;|"):
            raise ProtocoloInvalido(
                G.F_STRING, f"string da faceta {n} tem conteúdo fora do padrão "
                            f"{G.F_STRING.texto}: {residuo.strip()[:60]!r}")
        saida[id_faceta] = {"id": id_string, "texto": celula, "termos": termos}
        locais["string"][id_faceta] = idx
    if sorted(saida) != sorted(ids_faceta):
        raise ProtocoloInvalido(G.T_STRINGS, f"esperava uma string por faceta "
                                             f"({sorted(ids_faceta)}), achei {sorted(saida)}")
    return saida


# ---------------------------------------------------------------------- expressões
def grupos_de_composicao(comb, ident):
    """Composição na forma estrita `STRa AND STRb AND (STRc OR STRd)`.

    A forma devolvida é uma lista de grupos; todo grupo tem de ser satisfeito e, dentro do
    grupo, basta um dos STRn. `AND`, em maiúsculas, é a única conjunção; `OR`, em
    maiúsculas, só aparece dentro de parênteses, sem aninhamento. Qualquer outra forma —
    `+`, operador em minúscula, `OR` fora de parênteses — reprova: a expressão do protocolo
    é a que se executa, e leitura tolerante esconderia a divergência.
    """
    E, forma = G.F_COMPOSICAO, G.F_COMPOSICAO.texto
    comb = " ".join(comb.split())
    if "+" in comb:
        raise ProtocoloInvalido(E, f"expressão {ident}: `+` não é conjunção da forma "
                                   f"estrita {forma}; use AND: {comb!r}")
    minusculas = sorted({m.group(0) for m in re.finditer(r"\b(?:and|or|not)\b", comb,
                                                          re.I)} - {"AND", "OR"})
    if minusculas:
        raise ProtocoloInvalido(E, f"expressão {ident}: operador fora da forma estrita "
                                   f"{forma} {minusculas}: {comb!r}")
    partes, profundidade, atual = [], 0, ""
    for tok in re.split(r"(\(|\)|\bAND\b)", comb):
        if tok == "(":
            profundidade += 1
            if profundidade > 1:
                raise ProtocoloInvalido(E, f"expressão {ident}: parênteses aninhados fora "
                                           f"da forma estrita {forma}: {comb!r}")
        elif tok == ")":
            profundidade -= 1
            if profundidade < 0:
                raise ProtocoloInvalido(E, f"expressão {ident}: parêntese fechado sem abrir")
        if tok == "AND" and profundidade == 0:
            partes.append(atual)
            atual = ""
        else:
            atual += tok
    partes.append(atual)
    if profundidade:
        raise ProtocoloInvalido(E, f"expressão {ident}: parêntese aberto sem fechar")

    grupos = []
    for parte in partes:
        p = parte.strip()
        if not p:
            raise ProtocoloInvalido(E, f"expressão {ident}: operador AND sem operando")
        s_ = G.I_STR.prefixo
        m = re.fullmatch(rf"\(\s*({s_}\d+(?:\s+OR\s+{s_}\d+)+)\s*\)", p)
        if m:
            membros = [x.strip() for x in m.group(1).split("OR")]
        elif re.fullmatch(rf"{s_}\d+", p):
            membros = [p]
        else:
            raise ProtocoloInvalido(E, f"expressão {ident}: composição fora da forma "
                                       f"estrita {forma}: {comb!r}")
        grupos.append(membros)
    return grupos


def expressoes(ctx, t, params, locais):
    """Composição das expressões, a executada, a sonda e a faixa de sensibilidade.

    Devolve (composição, executada, sonda, sensibilidade). A composição é estrutural: sem a
    tabela, a leitura reprova; executada, sonda e faixa seguem a precedência.
    """
    T = G.T_EXPRESSOES
    bloco = secao(t, G.S_EXPRESSOES)
    composicao, natureza, detalhe = {}, {}, {}
    linhas_tabela = linhas_de_tabela(bloco)
    if not linhas_tabela:
        raise ProtocoloInvalido(T, "tabela ausente")
    # O cabeçalho diz o que cada coluna é: lido por posição, um cabeçalho trocado
    # faria a natureza ou a expressão vir de outra coluna, em silêncio.
    lido = [desescapa(c).strip() for c in celulas(linhas_tabela[0][1])]
    if lido != list(T.colunas):
        raise ProtocoloInvalido(T, f"cabeçalho {lido} difere do esperado {list(T.colunas)}")
    locais["cabecalho_expressoes"] = linhas_tabela[0][0]
    locais["expressao"] = {}
    for idx, linha in linhas_tabela:
        cels = celulas(linha)
        if len(cels) < 4 or not G.I_EB.casa(cels[0]):
            continue
        ident = cels[0]
        comb = desescapa(cels[2]).replace("\\", " ").strip()
        if not G.F_COMPOSICAO.padrao.search(comb):
            raise ProtocoloInvalido(G.F_COMPOSICAO, f"expressão {ident} sem composição "
                                                    f"legível")
        composicao[ident] = grupos_de_composicao(comb, ident)
        natureza[ident] = normaliza(cels[1])
        detalhe[ident] = desescapa(cels[3])
        locais["expressao"][ident] = idx
    numeracao(list(composicao), G.I_EB, "expressões")
    comp = _estrutural(params, "composicao", composicao)

    def papel(nome, chave_natureza):
        declarada = ctx.config.valor(f"expressoes.{chave_natureza}")
        alvo = normaliza(declarada)
        achados = sorted(k for k, v in natureza.items() if v == alvo)
        if len(achados) > 1:
            raise ProtocoloInvalido(T, f"mais de uma expressão com natureza "
                                       f"{declarada!r}: {achados}")
        valor = _parametro(ctx, params, nome, achados[0] if achados else None,
                           f"padroes.{nome}")
        if valor not in comp:
            raise ProtocoloInvalido(T, f"a {nome} {valor!r} não é expressão da composição")
        return valor
    executada = papel("executada", "natureza_executada")
    sonda = papel("sonda", "natureza_sonda")

    # Faixa de sensibilidade: "< N%" e "> M%" no detalhamento da sonda.
    limites = {}
    for m in G.F_FAIXA.padrao.finditer(detalhe.get(sonda, "")):
        limites.setdefault(m.group(1), m.group(2))
    baixo, alto = limites.get("<"), limites.get(">")
    if bool(baixo) != bool(alto):
        raise ProtocoloInvalido(G.F_FAIXA, f"faixa ilegível no detalhamento de {sonda}: "
                                           f"falta o limite "
                                           f"{'superior' if baixo else 'inferior'}")
    faixa = [percentual(baixo), percentual(alto)] if baixo else None
    if faixa:
        locais["faixa"] = locais["expressao"][sonda]
    sens = _parametro(ctx, params, "sensibilidade", faixa, "padroes.sensibilidade")
    return comp, executada, sonda, sens


# ---------------------------------------------------------------------- critérios
def criterios(t, locais):
    T = G.T_CRITERIOS
    locais["criterio"] = {}
    saida, dimensao = [], ""
    for idx, linha in linhas_de_tabela(secao(t, G.S_CRITERIOS)):
        cels = celulas(linha)
        if len(cels) < len(T.colunas):
            continue
        m = G.I_CE.casa(cels[G.COL_CRIT_ID])
        if not m:
            continue
        acao = desescapa(cels[G.COL_CRIT_ACAO]).strip()
        if acao not in G.D_ACAO.valores:
            raise ProtocoloInvalido(G.D_ACAO, f"{cels[G.COL_CRIT_ID]}: ação {acao!r} não é "
                                              f"{' nem '.join(G.D_ACAO.valores)}")
        rotulo = desescapa(cels[G.COL_CRIT_DIMENSAO].strip("* ")).strip()
        if rotulo:
            dimensao = rotulo
        ident = f"{G.I_CE.prefixo}{int(m.group(1))}"
        saida.append({"id": ident, "dimensao": dimensao, "acao": acao,
                      "criterio": desescapa(cels[G.COL_CRIT_CRITERIO]).strip(),
                      "justificativa": desescapa(cels[G.COL_CRIT_JUST]).strip()})
        locais["criterio"][ident] = idx
    numeracao([c["id"] for c in saida], G.I_CE, "critérios")
    return saida


def recorte(ctx, crit, params, locais):
    """Recorte temporal: ano inicial e teto, com o texto que o declara."""
    dimensao = ctx.config.valor("conferencia.dimensao_recorte")
    declarado = next((c for c in crit
                      if c["dimensao"] == dimensao and c["acao"] == G.ACAO_INCLUIR), None)
    ano = None
    if declarado:
        m = G.F_RECORTE.padrao.search(declarado["criterio"])
        if not m:
            raise ProtocoloInvalido(G.F_RECORTE, f"recorte temporal declarado sem ano "
                                                 f"legível ('{G.F_RECORTE.texto}')")
        # "após o ano AAAA" inclui a partir de AAAA + 1. O teto é a data de execução.
        ano = int(m.group(1)) + 1
        locais["recorte"] = locais["criterio"][declarado["id"]]
    ano = _parametro(ctx, params, "recorte_ano_min", ano, "padroes.recorte_ano_min")
    return {"ano_min": ano, "ano_max": None,
            "texto": declarado["criterio"] if declarado else ""}


def limiar(ctx, t, params, locais):
    bloco = secao(t, G.S_SEMENTES)
    valor = None
    if G.M_REGRA.padrao.search(bloco):
        m = G.F_LIMIAR.padrao.search(bloco)
        if not m:
            raise ProtocoloInvalido(G.F_LIMIAR, f"regra de ajuste sem limiar legível "
                                                f"('{G.F_LIMIAR.texto}')")
        valor = percentual(m.group(1))
        locais["limiar"] = next(i for i, l in linhas(bloco) if G.F_LIMIAR.padrao.search(l))
    return _parametro(ctx, params, "limiar_aderencia", valor, "padroes.limiar_aderencia")


def ancoras(ctx, pal, params):
    marcadas = [f["id"] for f in pal if f["ancora"]] or None
    return _parametro(ctx, params, "ancoras", marcadas, "padroes.ancoras")


# ------------------------------------------------------------------------- fontes
def bases_de_dados(ctx, t, locais):
    """Bases da tabela de bases: identificador, sigla, nome e ficha."""
    from .config import RAIZ                                        # noqa: PLC0415
    T = G.T_BASES
    c_id, c_sigla, c_nome = T.colunas
    bloco, tabela = tabela_da_secao(t, T)
    locais["cabecalho_bases"] = bloco.primeira
    locais["base"] = {}
    bases = []
    for linha in tabela:
        valores = {c: desescapa(linha[c]).strip() for c in T.colunas}
        ident = valores[c_id] or "?"
        vazios = [c for c, v in valores.items() if not v]
        if vazios:
            raise ProtocoloInvalido(T, f"linha {ident}: campo vazio {vazios}")
        m = G.I_BD.casa(ident)
        if not m:
            raise ProtocoloInvalido(G.I_BD, f"{c_id} {ident!r} fora da forma "
                                            f"{G.I_BD.prefixo}n")
        sigla = valores[c_sigla]
        if not re.fullmatch(r"[\w-]+", sigla):
            raise ProtocoloInvalido(T, f"linha {ident}: {c_sigla} {sigla!r} não serve de "
                                       f"chave (letras, dígitos, `_` ou `-`)")
        if any(b["sigla"] == sigla for b in bases):
            raise ProtocoloInvalido(T, f"sigla repetida {sigla!r}")
        ficha_ = ctx.config.ficha(sigla)
        if not (RAIZ / ficha_).exists():
            raise ProtocoloInvalido(T, f"linha {ident}: ficha da sigla {sigla!r} não existe "
                                       f"— procurada em {ficha_} (`documentos.ficha` do "
                                       f"{ctx.config.nome})")
        ident = f"{G.I_BD.prefixo}{int(m.group(1))}"
        bases.append({"id": ident, "sigla": sigla, "nome": valores[c_nome], "ficha": ficha_})
        locais["base"][ident] = linha["_linha"]
    numeracao([b["id"] for b in bases], G.I_BD, "bases")
    return bases


def fontes(ctx, t, locais):
    bases_bloco = secao(t, G.S_BASES)
    bases = bases_de_dados(ctx, t, locais)

    acesso = next((p for p in paragrafos(bases_bloco) if p.startswith(G.MARCA_ORDEM)), "")
    if not acesso:
        raise ProtocoloInvalido(G.F_ORDEM, "ordem de execução das bases não declarada")
    locais["ordem"] = next(i for i, l in linhas(bases_bloco) if l.startswith(G.MARCA_ORDEM))
    m = G.F_ORDEM.padrao.search(acesso)
    if not m:
        raise ProtocoloInvalido(G.F_ORDEM, "ordem de execução sem lista legível")
    ordem = []
    for nome in [x.strip() for x in re.split(r",| e ", m.group(1)) if x.strip()]:
        cand = [b for b in bases if normaliza(b["nome"]).startswith(normaliza(nome))]
        if len(cand) != 1:
            raise ProtocoloInvalido(G.F_ORDEM, f"base {nome!r} da ordem de execução não "
                                               f"identificada")
        ordem.append(cand[0]["nome"])
    if sorted(ordem) != sorted(b["nome"] for b in bases):
        raise ProtocoloInvalido(G.F_ORDEM, f"ordem de execução incompleta: {ordem}")
    via = acesso[m.end():].strip()

    ferramenta = []
    for fm in G.F_FERRAMENTA.padrao.finditer(secao(t, G.S_FERRAMENTA)):
        ferramenta.append({"tema": desescapa(fm.group(1)).strip(),
                           "texto": desescapa(fm.group(2)).strip()})

    return {
        "bases": bases,
        "ordem_execucao": ordem,
        "via_de_acesso": via,
        "acervos_especiais": " ".join(paragrafos(secao(t, G.S_ACERVOS))).strip(),
        "ferramenta_gestao": ferramenta,
    }


# ------------------------------------------------------------------------ sementes
def _titulo(resto):
    """O título termina no primeiro ponto seguido de maiúscula ou de dígito."""
    m = re.search(r"[.!?]\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9“\"])", resto)
    return (resto[:m.start() + 1] if m else resto).strip()


def _doi(texto_ref):
    m = G.F_DOI.padrao.search(texto_ref.rstrip())
    if not m:
        return ""
    return m.group(1).rstrip(".")


def sementes(t, siglas, locais):
    """Referências, bases esperadas e papel, da tabela do conjunto-semente.

    Cada base citada tem de ser sigla da tabela de bases, na grafia exata; semente sem base
    reprova. O papel tem de estar no domínio; ausente ou fora reprova, nomeando a semente.
    """
    T = G.T_SEMENTES
    c_id, c_ref, c_bases, c_papel = T.colunas
    bloco, tabela = tabela_da_secao(t, T)
    locais["cabecalho_sementes"] = bloco.primeira
    locais["semente"] = {}
    estudos = []
    for linha in tabela:
        ident = desescapa(linha[c_id]).strip()
        if not G.I_SE.casa(ident):
            raise ProtocoloInvalido(G.I_SE, f"{c_id} {ident!r} fora da forma "
                                            f"{G.I_SE.prefixo}n")
        papel = desescapa(linha[c_papel]).strip()
        admitidos = list(G.D_PAPEL.valores)
        if not papel:
            raise ProtocoloInvalido(G.D_PAPEL, f"linha {ident}: papel da semente vazio; "
                                               f"admitidos {admitidos}")
        if papel not in G.D_PAPEL.valores:
            raise ProtocoloInvalido(G.D_PAPEL, f"linha {ident}: papel {papel!r} fora dos "
                                               f"admitidos {admitidos}")
        ref = desescapa(linha[c_ref]).strip()
        m = G.F_REFERENCIA.padrao.match(ref)
        if not m:
            raise ProtocoloInvalido(G.F_REFERENCIA, f"linha {ident}: referência sem autoria "
                                                    f"e ano no padrão esperado")
        autores, ano, resto = m.groups()
        bases = lista(linha[c_bases])
        if not bases:
            raise ProtocoloInvalido(T, f"linha {ident}: semente sem base")
        fora = [b for b in bases if b not in siglas]
        if fora:
            raise ProtocoloInvalido(T, f"linha {ident}: base {fora} não é sigla da "
                                       f"{G.T_BASES.rotulo} {list(siglas)}")
        if len(set(bases)) != len(bases):
            raise ProtocoloInvalido(T, f"linha {ident}: base repetida {bases}")
        primeiro = autores.split(",")[0].strip()
        estudos.append({
            "id": ident, "autores": autores.strip(), "ano": int(ano),
            "titulo": _titulo(resto), "doi": _doi(ref),
            "bases": bases, "papel": G.D_PAPEL.valores[papel], "chave": f"{primeiro} {ano}",
        })
        locais["semente"][ident] = linha["_linha"]
    numeracao([e["id"] for e in estudos], G.I_SE, "referências")
    return estudos


def distribuicao(estudos, siglas):
    """Distribuição das sementes pelas bases e por papel, calculada da tabela.

    Não confere prosa. `por_base` e `por_base_papel` contam incidências: a semente
    indexada em duas bases conta nas duas, como manda a leitura do conjunto-semente.
    `por_papel` conta estudos distintos.
    """
    papeis_ = tuple(G.D_PAPEL.valores.values())
    por_base = {b: 0 for b in siglas}
    por_base_papel = {b: {p: 0 for p in papeis_} for b in siglas}
    for e in estudos:
        for b in e["bases"]:
            por_base[b] += 1
            por_base_papel[b][e["papel"]] += 1
    multi = sum(1 for e in estudos if len(e["bases"]) > 1)
    return {
        "por_base": por_base, "incidencias": sum(por_base.values()),
        "registros": len(estudos), "em_mais_de_uma_base": multi,
        "em_uma_so": len(estudos) - multi,
        "por_papel": {p: sum(1 for e in estudos if e["papel"] == p) for p in papeis_},
        "por_base_papel": por_base_papel,
        "validacao_vazia": not any(e["papel"] == G.PAPEL_VALIDACAO for e in estudos),
    }


# ------------------------------------------------------------------------- análise
def papeis(d):
    """Papéis das expressões, calculados uma única vez a partir da composição e das âncoras.

    Função pura sobre o resultado de `analisa()` (precisa de `expressoes`, `executada`,
    `sonda`, `ancoras` e `strings`). Devolve:
      ancoras             grupos unitários das STR das facetas-âncora, na ordem declarada
      ancoras_sem_string  âncoras que não são faceta com string (a conferência reprova)
      especificas         {expressão: STR distintiva} — exceto executada e sonda, com
                          exatamente um grupo unitário além das âncoras
      gerais              {expressão: grupos além das âncoras} — exceto executada e sonda,
                          com mais de um grupo além das âncoras
      executada, sonda    os identificadores declarados
    É este cálculo que a conferência de coerência e a derivação usam; não se recalcula.
    """
    comp, exec_, sonda = d["expressoes"], d["executada"], d["sonda"]
    str_de = {fid: s["id"] for fid, s in d["strings"].items()}
    ancora = [[str_de[a]] for a in d["ancoras"] if a in str_de]
    especificas, gerais = {}, {}
    for k, v in comp.items():
        if k in (exec_, sonda):
            continue
        alem = [g for g in v if g not in ancora]
        if len(alem) == 1 and len(alem[0]) == 1:
            especificas[k] = alem[0][0]
        elif len(alem) > 1:
            gerais[k] = alem
    return {
        "ancoras": ancora,
        "ancoras_sem_string": [a for a in d["ancoras"] if a not in str_de],
        "especificas": especificas,
        "gerais": gerais,
        "executada": exec_,
        "sonda": sonda,
    }


def analisa(ctx):
    """O protocolo lido. ProtocoloInvalido na primeira violação da gramática."""
    t = ctx.texto
    params, locais = {}, {}
    pal = palavras(t, locais)
    tb, idiomas = tabelas(t, pal, locais)
    _estrutural(params, "idiomas", list(idiomas))
    ids_facetas = [f["id"] for f in pal]
    insts, insts_faceta = instrumentos(t, ids_facetas, idiomas, locais)
    _estrutural(params, "instrumentos", [
        f"{s} ({i['modo']}; {'/'.join(i['idiomas'])}; {','.join(i['facetas'])})"
        for s, i in insts.items()])
    st = strings(t, set(ids_facetas), locais)
    for n in st:
        # A string repete termo entre camadas; a lista executada é deduplicada. É ela
        # que a derivação local usa, e é ela que o relatório conta.
        st[n]["termos"] = sem_repeticao(st[n]["termos"])
    comp, exec_, sonda, sens = expressoes(ctx, t, params, locais)
    crit = criterios(t, locais)
    fts = fontes(ctx, t, locais)
    siglas = [b["sigla"] for b in fts["bases"]]
    _estrutural(params, "bases", [f"{b['id']} {b['sigla']} → {b['ficha']}"
                                  for b in fts["bases"]])
    est = sementes(t, siglas, locais)
    _estrutural(params, "sementes", [f"{e['id']} ({e['papel']}): {', '.join(e['bases'])}"
                                     for e in est])
    d = {
        "questoes": questoes(t, locais),
        "facetas": pal,
        "ancoras": ancoras(ctx, pal, params),
        "idiomas": idiomas,
        "tabelas": tb,
        "instrumentos": insts,
        "instrumentos_por_faceta": insts_faceta,
        "strings": st,
        "expressoes": comp,
        "executada": exec_,
        "sonda": sonda,
        "sensibilidade": sens,
        "criterios": crit,
        "recorte": recorte(ctx, crit, params, locais),
        "fontes": fts,
        "bases": fts["bases"],
        "limiar": limiar(ctx, t, params, locais),
        "sementes": est,
        "distribuicao": distribuicao(est, siglas),
    }
    # O protocolo não declara estes; valem os do config.toml, com a origem registrada.
    d["divergencia"] = _parametro(ctx, params, "divergencia_fidelidade", None,
                                  "padroes.divergencia_fidelidade")
    d["calibracao_triagem"] = _parametro(ctx, params, "calibracao_triagem", None,
                                         "padroes.calibracao_triagem")
    _parametro(ctx, params, "minimo_termos_string", None, "conferencia.minimo_termos_string")
    _parametro(ctx, params, "dimensoes_criterio", None, "conferencia.dimensoes_criterio")
    d["parametros"] = params
    d["papeis"] = papeis(d)
    d["locais"] = locais
    return d
