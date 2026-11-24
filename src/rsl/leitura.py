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
import tomllib
import urllib.parse

from . import gramatica as G
from .erros import ProtocoloInvalido
from .markdown import (blocos_de_tabela, celulas, desescapa, le_tabela, linhas,
                       linhas_de_tabela, lista, normaliza, paragrafos, secao,
                       tabela_da_secao)

LINHAS = tuple(r.interno for r in G.LINHAS_CT)
ORIGEM_PROTOCOLO = "protocolo"


def origem_padrao(cfg):
    return f"padrão ({cfg.nome})"


# ------------------------------------------------------------------------ parâmetros
def _parametro(ctx, params, nome, valor_protocolo, chave_padrao):
    """O do protocolo, se declarado (não None); senão, o padrão do config.toml.

    `params` acumula valor e origem, que `configuracao mostrar` exibe. Trecho do protocolo
    presente e ilegível não chega aqui: o leitor levanta ProtocoloInvalido antes.
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
        k = next(k for k, (x, y) in enumerate(zip(ids, esperado)) if x != y)
        raise ProtocoloInvalido(identificador, f"{onde} fora da numeração {prefixo}1 a "
                                               f"{prefixo}{len(ids)}: {ids} — {ids[k]} "
                                               f"onde se esperava {esperado[k]}", documento)


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
def facetas(t, locais=None):
    """Nome e papel de cada faceta, da tabela de facetas (cabeçalho exato).

    O nome é a célula inteira, hífens incluídos. A âncora vem da coluna, só `Sim` ou `Não`,
    sem distinção de caixa: valor fora do domínio reprova, em vez de virar `Não` em
    silêncio. Sem nenhuma âncora a sonda não seria identificável: reprova aqui.
    """
    T = G.T_FACETAS
    c_id, c_nome, c_ancora = T.colunas
    locais = {} if locais is None else locais
    blocos = blocos_de_tabela(secao(t, G.S_FACETAS))
    if not blocos:
        raise ProtocoloInvalido(T, "tabela ausente")
    bloco = blocos[0]
    lido = [desescapa(c).strip() for c in celulas(bloco[0])]
    if lido != list(T.colunas):
        raise ProtocoloInvalido(T, f"cabeçalho {lido} difere do esperado {list(T.colunas)}")
    _, tabela = le_tabela(bloco, T)
    locais["cabecalho_facetas"] = bloco.primeira
    locais["faceta"] = {}
    dominio = {k.casefold(): v for k, v in G.D_ANCORA.valores.items()}
    saida = []
    for linha in tabela:
        ident = desescapa(linha[c_id]).strip()
        if not G.I_FCT.casa(ident):
            raise ProtocoloInvalido(G.I_FCT, f"{c_id} {ident!r} fora da forma "
                                             f"{G.I_FCT.prefixo}n")
        nome = desescapa(linha[c_nome]).strip()
        if not nome:
            raise ProtocoloInvalido(T, f"faceta {ident}: {c_nome} vazia")
        valor = desescapa(linha[c_ancora]).strip()
        if valor.casefold() not in dominio:
            raise ProtocoloInvalido(G.D_ANCORA, f"faceta {ident}: {c_ancora} {valor!r} fora "
                                                f"dos admitidos {list(G.D_ANCORA.valores)}")
        saida.append({"id": ident, "nome": nome, "ancora": dominio[valor.casefold()]})
        locais["faceta"][ident] = linha["_linha"]
    numeracao([f["id"] for f in saida], G.I_FCT, "facetas")
    if not any(f["ancora"] for f in saida):
        raise ProtocoloInvalido(T, f"nenhuma faceta marcada como {c_ancora}: a sonda não "
                                   f"seria identificável")
    return saida


def _termos_celula(celula, onde):
    """Termos de uma célula, separados por vírgula. O separador antigo (`\\- `) reprova:
    lido com a vírgula, a célula inteira viraria um termo só, em silêncio."""
    if re.search(G.SEPARADOR_ANTIGO, celula):
        raise ProtocoloInvalido(G.T_QUADRO, f"{onde}: termos separados por `\\- `; o "
                                            f"separador é a vírgula")
    partes = re.split(G.SEPARADOR_TERMOS, celula)
    return [desescapa(p).strip() for p in partes if p.strip()]


def _subsecoes_ct(trecho):
    """[(título ou None, índice da linha do título, [blocos de tabela])] da seção do controle
    terminológico, divididas pelos títulos de nível 3. O primeiro item, de título None, é o
    que vem antes do primeiro título."""
    partes = [(None, None, [])]
    atual = []
    for idx, linha in linhas(trecho):
        m = G.F_TITULO_CT.padrao.match(linha)
        if m:
            partes[-1][2].extend(blocos_de_tabela(_trecho_de(atual)))
            partes.append((m.group(1), idx, []))
            atual = []
        else:
            atual.append((idx, linha))
    partes[-1][2].extend(blocos_de_tabela(_trecho_de(atual)))
    return partes


def _trecho_de(pares):
    """Trecho com as linhas (índice, linha) consecutivas, preservando o índice da primeira."""
    from .markdown import Trecho                                    # noqa: PLC0415
    if not pares:
        return Trecho("", 0)
    return Trecho("\n".join(l for _, l in pares), pares[0][0])


def _faceta_do_titulo(titulo, nomes):
    """(CTn, FCTn) do título `CTn (FCTn)`; reprova título fora da forma, mais de uma faceta,
    faceta inexistente e número divergente."""
    forma = G.F_TITULO_CT.texto
    m = G.FORMA_TITULO_CT.fullmatch(titulo)
    if not m or not G.I_CT.casa(m.group(1)):
        raise ProtocoloInvalido(G.F_TITULO_CT, f"título {titulo!r} fora da forma `{forma}`")
    ct = m.group(1)
    dentro = [x.strip() for x in m.group(2).split(",")]
    if len(dentro) != 1:
        raise ProtocoloInvalido(G.F_TITULO_CT, f"{ct} declara {dentro}: cada CT tem uma "
                                               f"única faceta")
    fct = dentro[0]
    if not G.I_FCT.casa(fct):
        raise ProtocoloInvalido(G.F_TITULO_CT, f"título {titulo!r}: {fct!r} fora da forma "
                                               f"{G.I_FCT.prefixo}n")
    if fct not in nomes:
        raise ProtocoloInvalido(G.F_TITULO_CT, f"{ct} cita a faceta {fct}, sem linha na "
                                               f"{G.T_FACETAS.rotulo}")
    if int(G.I_CT.casa(ct).group(1)) != int(G.I_FCT.casa(fct).group(1)):
        raise ProtocoloInvalido(G.I_CT, f"{ct} e {fct} com números diferentes: o CT tem o "
                                        f"número da sua faceta")
    return ct, fct


def tabelas(t, pal, locais):
    """As tabelas do controle terminológico, uma por faceta, com as linhas por idioma.

    Cada tabela fica sob um título `### CTn (FCTn)`, que dá a faceta. O cabeçalho
    `| Termo | pt | en | es |` dá os idiomas, a partir da segunda célula: o idioma de cada coluna é
    o nome no cabeçalho, não a posição. O primeiro quadro fixa a ordem dos idiomas do
    projeto; os demais têm de ter o mesmo conjunto, em qualquer ordem. As três linhas são
    exigidas, pelo rótulo inteiro. Nenhuma tabela da seção é ignorada: a que está fora da
    forma reprova.

    Devolve (tabelas, idiomas).
    """
    nomes = {f["id"]: f for f in pal}
    locais["quadro"] = {}
    saida, idiomas, por_ct = [], None, {}
    forma = G.F_TITULO_CT.texto
    for titulo, idx_titulo, blocos in _subsecoes_ct(secao(t, G.S_CONTROLE)):
        if titulo is None or len(blocos) > 1:
            if titulo is None and not blocos:
                continue
            bloco = blocos[0 if titulo is None else 1]
            antiga = G.I_FCT.casa(desescapa(celulas(bloco[0])[0]).strip())
            onde = f"tabela da linha {bloco.primeira + 1}"
            raise ProtocoloInvalido(
                G.F_TITULO_CT, f"{onde} sem título `{forma}`" +
                (" (cabeçalho na forma antiga `| FCTn | … |`)" if antiga else ""))
        ct, ident = _faceta_do_titulo(titulo, nomes)
        if ct in por_ct:
            raise ProtocoloInvalido(G.I_CT, f"{ct} repetido")
        por_ct[ct] = ident
        if not blocos:
            raise ProtocoloInvalido(G.T_QUADRO, f"{ct} ({ident}) sem tabela")
        bloco = blocos[0]
        primeira = desescapa(celulas(bloco[0])[0]).strip()
        if G.I_FCT.casa(primeira):
            raise ProtocoloInvalido(G.T_QUADRO, f"{ct}: cabeçalho na forma antiga "
                                                f"`| {primeira} | … |`; a faceta vem do "
                                                f"título `{forma}`, e a primeira célula do "
                                                f"cabeçalho é `{G.CAB_QUADRO}`")
        if primeira.strip("*_ \t") != G.CAB_QUADRO:
            raise ProtocoloInvalido(G.T_QUADRO, f"{ct}: primeira célula do cabeçalho "
                                                f"{primeira!r}; a forma é "
                                                f"`| {G.CAB_QUADRO} | idioma | … |`")
        cab, linhas_ = le_tabela(bloco, G.T_QUADRO, exigidas=())
        proprios = cab[1:]
        if not proprios or any(not i for i in proprios):
            raise ProtocoloInvalido(G.T_QUADRO, f"{ct}: coluna de idioma sem nome no "
                                                f"cabeçalho {cab}")
        if idiomas is None:
            idiomas = tuple(proprios)
        elif set(proprios) != set(idiomas):
            raise ProtocoloInvalido(
                G.T_QUADRO, f"{ct} ({ident}): idiomas {sorted(proprios)} diferem dos "
                            f"idiomas {sorted(idiomas)} do quadro de {saida[0]['id']} — "
                            f"faltam {sorted(set(idiomas) - set(proprios))}, sobram "
                            f"{sorted(set(proprios) - set(idiomas))}")
        atual = {"id": ident, "ct": ct, "nome": nomes[ident]["nome"],
                 "ancora": nomes[ident]["ancora"],
                 "linhas": {i: {c: [] for c in LINHAS} for i in idiomas}}
        saida.append(atual)
        local = {"titulo": idx_titulo, "cabecalho": bloco.primeira}
        desconhecidos = []
        for linha in linhas_:
            bruto = desescapa(celulas(bloco[linha["_linha"] - bloco.primeira])[0])
            rotulo = next((r for r in G.LINHAS_CT if r.casa(bruto)), None)
            if rotulo is None:
                desconhecidos.append(G.rotulo_da_celula(bruto))
                continue
            if rotulo.interno in local:
                raise ProtocoloInvalido(rotulo, f"{ct}: linha '{rotulo.texto}' repetida")
            local[rotulo.interno] = linha["_linha"]
            for idioma in idiomas:
                atual["linhas"][idioma][rotulo.interno] = _termos_celula(
                    linha[idioma], f"{ct} ({ident}), {rotulo.texto}, {idioma}")
        faltam = [r for r in G.LINHAS_CT if r.interno not in local]
        if faltam:
            raise ProtocoloInvalido(faltam[0], f"{ct}: falta a linha '{faltam[0].texto}'")
        if desconhecidos:
            raise ProtocoloInvalido(G.T_QUADRO, f"{ct}: rótulo de linha desconhecido "
                                                f"{desconhecidos[0]!r}; admitidos "
                                                f"{[r.texto for r in G.LINHAS_CT]}")
        locais["quadro"][ident] = local

    ids = [f["id"] for f in saida]
    if sorted(ids) != sorted(nomes):
        raise ProtocoloInvalido(G.T_QUADRO, f"esperava uma tabela por faceta "
                                            f"({sorted(nomes)}), achei {ids}")
    for f in saida:
        f["termos"] = {i: sem_repeticao(
            [x for c in LINHAS for x in f["linhas"][i][c]]) for i in idiomas}
    return saida, idiomas


# -------------------------------------------------------------------- instrumentos
def instrumentos(t, ids_facetas, idiomas, locais):
    """Instrumentos da tabela de instrumentos, pelo nome da coluna.

    Devolve (por sigla, por faceta). Sem padrão: toda faceta do quadro tem de constar da
    coluna FCTs de algum instrumento. `Caminho` é o endereço do serviço consultado e só
    admite o marcador `{idioma}`, resolvido por `endereco()`.
    """
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
        marcadores = sorted(set(re.findall(r"\{[^{}]*\}", valores[c_caminho]))
                            - {G.MARCADOR_IDIOMA})
        if marcadores:
            raise ProtocoloInvalido(T, f"linha {sigla}: {c_caminho} com marcador "
                                       f"desconhecido {', '.join(marcadores)}; só se admite "
                                       f"{G.MARCADOR_IDIOMA}")
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
    por_faceta = {fid: [i for i in por_sigla.values() if fid in i["facetas"]]
                  for fid in ids_facetas}
    faltam = [f for f, lista_ in por_faceta.items() if not lista_]
    if faltam:
        raise ProtocoloInvalido(T, f"faceta(s) sem instrumento na coluna {c_fcts}: {faltam}")
    return por_sigla, por_faceta


def endereco(instrumento, idioma):
    """Endereço resolvido do instrumento no idioma: o `Caminho` com `{idioma}` trocado."""
    return instrumento["caminho"].replace(G.MARCADOR_IDIOMA, idioma)


def instrumentos_do_termo(d, fid, idioma):
    """Instrumentos em que se valida um termo da faceta `fid` no `idioma`, cada um com o
    endereço resolvido para esse idioma (`endereco`)."""
    return [{**i, "endereco": endereco(i, idioma)}
            for i in d["instrumentos_por_faceta"][fid] if idioma in i["idiomas"]]


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
            raise ProtocoloInvalido(G.I_STR, f"{id_string} sem faceta {id_faceta} na "
                                             f"{G.T_FACETAS.rotulo}")
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


ORIGEM_COMPOSICAO = "protocolo (composição)"


def notas(t, locais):
    """Notas explicativas (`- Nn — texto`) da subseção opcional das expressões.

    Devolve {Nn: texto}. Sem a subseção, nenhuma nota. Nota repetida reprova: a faixa lida
    dependeria de qual das duas valesse.
    """
    locais["nota"] = {}
    if not re.search(r"^#+\s+" + re.escape(G.S_NOTAS.titulo) + r"\s*$",
                     secao(t, G.S_EXPRESSOES), re.M):
        return {}
    saida = {}
    for idx, linha in linhas(secao(t, G.S_NOTAS)):
        m = G.F_NOTA.padrao.match(linha)
        if not m:
            continue
        if m.group(1) in saida:
            raise ProtocoloInvalido(G.F_NOTA, f"nota {m.group(1)} repetida")
        saida[m.group(1)] = desescapa(m.group(2)).strip()
        locais["nota"][m.group(1)] = idx
    return saida


def _papel_pela_composicao(papel, candidatas, criterio):
    """O único candidato; nenhum ou mais de um reprova, nomeando os candidatos."""
    if len(candidatas) == 1:
        return candidatas[0]
    achado = (f"nenhuma candidata a {papel}" if not candidatas
              else f"{len(candidatas)} candidatas a {papel}: {candidatas}")
    raise ProtocoloInvalido(G.T_EXPRESSOES, f"{achado}; a {papel} é a única expressão "
                                            f"{criterio}")


def expressoes(ctx, t, params, locais, ancoras_, strings_):
    """Composição das expressões, a executada, a sonda e a faixa de sensibilidade.

    Devolve (composição, executada, sonda, sensibilidade). A composição é estrutural: sem a
    tabela, a leitura reprova. Executada e sonda são identificadas pela composição e pelas
    âncoras, sem texto da tabela: a executada é a única com grupo `OR`; a sonda, a única
    formada exatamente pelas STR das âncoras. A faixa vem das notas citadas pela executada
    e segue a precedência.
    """
    T = G.T_EXPRESSOES
    bloco = secao(t, G.S_EXPRESSOES)
    composicao, funcao = {}, {}
    # A primeira tabela da seção: as demais (critérios, bases) são de subseções.
    tabelas_ = blocos_de_tabela(bloco)
    linhas_tabela = ([(tabelas_[0].primeira + k, l) for k, l in enumerate(tabelas_[0])]
                     if tabelas_ else [])
    if not linhas_tabela:
        raise ProtocoloInvalido(T, "tabela ausente")
    # O cabeçalho diz o que cada coluna é: lido por posição, um cabeçalho trocado
    # faria a expressão vir de outra coluna, em silêncio.
    lido = [desescapa(c).strip() for c in celulas(linhas_tabela[0][1])]
    if lido != list(T.colunas):
        raise ProtocoloInvalido(T, f"cabeçalho {lido} difere do esperado {list(T.colunas)}")
    locais["cabecalho_expressoes"] = linhas_tabela[0][0]
    locais["expressao"] = {}
    for idx, linha in linhas_tabela:
        cels = celulas(linha)
        if len(cels) < len(T.colunas) or not G.I_EB.casa(cels[0]):
            continue
        ident = cels[0]
        comb = desescapa(cels[1]).replace("\\", " ").strip()
        if not G.F_COMPOSICAO.padrao.search(comb):
            raise ProtocoloInvalido(G.F_COMPOSICAO, f"expressão {ident} sem composição "
                                                    f"legível")
        composicao[ident] = grupos_de_composicao(comb, ident)
        funcao[ident] = desescapa(cels[2])
        locais["expressao"][ident] = idx
    numeracao(list(composicao), G.I_EB, "expressões")
    comp = _estrutural(params, "composicao", composicao)

    nts = notas(t, locais)
    citadas = {}
    for ident, texto in funcao.items():
        citadas[ident] = G.F_REF_NOTA.padrao.findall(texto)
        faltam = [n for n in citadas[ident] if n not in nts]
        if faltam:
            raise ProtocoloInvalido(G.F_REF_NOTA, f"expressão {ident} cita a nota "
                                                  f"{', '.join(faltam)}, que não existe em "
                                                  f"'{G.S_NOTAS.titulo}'")

    executada = _papel_pela_composicao(
        "executada", sorted(k for k, v in comp.items() if any(len(g) > 1 for g in v)),
        "com grupo OR")
    str_de = {fid: s_["id"] for fid, s_ in strings_.items()}
    alvo = sorted([str_de[a]] for a in ancoras_ if a in str_de)
    sonda = _papel_pela_composicao(
        "sonda", sorted(k for k, v in comp.items() if sorted(v) == alvo),
        f"formada só pelas âncoras ({' AND '.join(g[0] for g in alvo)})")
    for nome, valor in (("executada", executada), ("sonda", sonda)):
        params[nome] = {"valor": valor, "origem": ORIGEM_COMPOSICAO}

    # Faixa de sensibilidade: "< N%" e "> M%" nas notas citadas pela executada.
    limites, onde = {}, {}
    for n in citadas[executada]:
        for m in G.F_FAIXA.padrao.finditer(nts[n]):
            if m.group(1) not in limites:
                limites[m.group(1)], onde[m.group(1)] = m.group(2), n
    baixo, alto = limites.get("<"), limites.get(">")
    if bool(baixo) != bool(alto):
        nota = onde["<" if baixo else ">"]
        raise ProtocoloInvalido(G.F_FAIXA, f"faixa ilegível na nota {nota} da executada "
                                           f"{executada}: falta o limite "
                                           f"{'superior' if baixo else 'inferior'}")
    faixa = [percentual(baixo), percentual(alto)] if baixo else None
    if faixa:
        locais["faixa"] = locais["nota"][onde["<"]]
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


def ancoras(pal, params):
    """Facetas marcadas `Sim`, na ordem da tabela. Estrutural: a leitura já reprovou a
    tabela sem âncora."""
    return _estrutural(params, "ancoras", [f["id"] for f in pal if f["ancora"]])


# ------------------------------------------------------------------------- fontes
def bases_de_dados(ctx, t, locais):
    """Bases da tabela de bases: identificador, sigla, nome e procedimento de busca."""
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
        # O procedimento gravado é saída e a fonte se lê por base (`fonte.py`): a falta de
        # uma ou de outra reprova só aquela base, não a leitura do protocolo.
        ficha_ = ctx.config.ficha(sigla)
        ident = f"{G.I_BD.prefixo}{int(m.group(1))}"
        bases.append({"id": ident, "sigla": sigla, "nome": valores[c_nome], "ficha": ficha_,
                      "fonte": ctx.config.fonte(sigla)})
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

    return {
        "bases": bases,
        "ordem_execucao": ordem,
        "via_de_acesso": via,
        "acervos_especiais": " ".join(paragrafos(secao(t, G.S_ACERVOS))).strip(),
    }


# ------------------------------------------------------------------------ sementes
def _semente_invalida(elemento, ident, detalhe):
    return ProtocoloInvalido(elemento, f"semente {ident}: {detalhe}")


def _lista_de_siglas(item, campo, ident, admitidas, rotulo_tabela, vazia_reprova):
    """Lista de siglas sem espaço sobrando: cada uma da tabela (grafia exata), sem
    repetição."""
    valores = [x.strip() for x in item.get(campo.chave, [])]
    if vazia_reprova and not valores:
        raise _semente_invalida(campo, ident, f"campo '{campo.chave}' vazio: semente sem "
                                              f"base")
    fora = [x for x in valores if x not in admitidas]
    if fora:
        raise _semente_invalida(campo, ident, f"{campo.chave} {fora} não é sigla da "
                                              f"{rotulo_tabela} {list(admitidas)}")
    if len(set(valores)) != len(valores):
        raise _semente_invalida(campo, ident, f"{campo.chave} com repetição {valores}")
    return valores


def sementes(texto, siglas, facetas_, locais):
    """Sementes do arquivo de sementes (TOML), campo a campo.

    O esquema é o da gramática (`TT_SEMENTES` e os seus campos): campo exigido ausente,
    campo de outro tipo ou campo desconhecido reprova, nomeando a semente e o campo. Cada
    base citada tem de ser sigla da tabela de bases, e cada faceta, `FCTn` da tabela de
    facetas, na grafia exata e sem repetição; o papel tem de estar no domínio; o `id`, em
    sequência a partir de SE1. Autoria, ano, título e DOI são os campos: nada se extrai
    por padrão de texto. Campo opcional ausente vale vazio.
    """
    T = G.TT_SEMENTES
    campos = {c.chave: c for c in T.campos}
    try:
        dado = tomllib.loads(texto)
    except tomllib.TOMLDecodeError as e:
        raise ProtocoloInvalido(T, f"não é TOML válido: {e}") from None
    fora = sorted(set(dado) - {T.chave})
    if fora:
        raise ProtocoloInvalido(T, f"chave fora do esquema no arquivo: {fora}")
    itens = dado.get(T.chave)
    if not isinstance(itens, list) or not itens or not all(isinstance(x, dict)
                                                         for x in itens):
        raise ProtocoloInvalido(T, f"tabela [[{T.chave}]] ausente ou vazia")
    locais["semente"] = {}
    estudos, vistos = [], set()
    for k, item in enumerate(itens, 1):
        bruto = item.get(G.C_ID.chave)
        ident = bruto if isinstance(bruto, str) and bruto.strip() else f"nº {k}"
        desconhecidos = sorted(set(item) - set(campos))
        if desconhecidos:
            raise _semente_invalida(T, ident, f"campo desconhecido {desconhecidos}; campos "
                                              f"do esquema {list(campos)}")
        for c in T.campos:
            if c.chave not in item:
                if c.exigido:
                    raise _semente_invalida(c, ident, f"falta o campo '{c.chave}'")
                continue
            if not c.aceita(item[c.chave]):
                raise _semente_invalida(c, ident, f"campo '{c.chave}' não é "
                                                  f"{c.tipo_valor}: {item[c.chave]!r}")
        ident = item[G.C_ID.chave].strip()
        if not G.I_SE.casa(ident):
            raise _semente_invalida(G.I_SE, ident, f"campo '{G.C_ID.chave}' fora da forma "
                                                   f"{G.I_SE.prefixo}n")
        if ident in vistos:
            raise _semente_invalida(G.C_ID, ident, f"campo '{G.C_ID.chave}' repetido")
        vistos.add(ident)
        e = {"id": ident}
        for c in T.campos:
            if c is G.C_ID:
                continue
            valor = item.get(c.chave, [] if c.tipo_valor == "lista de textos" else "")
            e[c.chave] = valor.strip() if isinstance(valor, str) else valor
        for c in (G.C_TITULO, G.C_VEICULO):
            if not e[c.chave]:
                raise _semente_invalida(c, ident, f"campo '{c.chave}' vazio")
        e[G.C_AUTORES.chave] = [a.strip() for a in e[G.C_AUTORES.chave]]
        if not e[G.C_AUTORES.chave] or not all(e[G.C_AUTORES.chave]):
            raise _semente_invalida(G.C_AUTORES, ident, f"campo '{G.C_AUTORES.chave}' vazio "
                                                        f"ou com autor vazio")
        if e[G.C_DOI.chave] and not G.F_DOI.padrao.match(e[G.C_DOI.chave]):
            raise _semente_invalida(G.F_DOI, ident, f"campo '{G.C_DOI.chave}' "
                                                    f"{e[G.C_DOI.chave]!r} fora da forma "
                                                    f"{G.F_DOI.texto.split()[0]}")
        papel = e[G.C_PAPEL.chave]
        if papel not in G.D_PAPEL.valores:
            raise _semente_invalida(G.D_PAPEL, ident, f"campo '{G.C_PAPEL.chave}' {papel!r} "
                                                      f"fora dos admitidos "
                                                      f"{list(G.D_PAPEL.valores)}")
        e[G.C_PAPEL.chave] = G.D_PAPEL.valores[papel]
        e[G.C_BASES.chave] = _lista_de_siglas(item, G.C_BASES, ident, siglas,
                                              G.T_BASES.rotulo, vazia_reprova=True)
        e[G.C_FACETAS.chave] = _lista_de_siglas(item, G.C_FACETAS, ident, facetas_,
                                                G.T_FACETAS.rotulo, vazia_reprova=False)
        primeiro = e[G.C_AUTORES.chave][0].split(",")[0].strip()
        e["chave"] = f"{primeiro} {e[G.C_ANO.chave]}"
        estudos.append(e)
        locais["semente"][ident] = k - 1
    numeracao([e["id"] for e in estudos], G.I_SE, "sementes", G.SEMENTES)
    return estudos


def referencia(e):
    """A semente como referência legível, montada dos campos na ordem autores, ano, título,
    veículo, volume, número, páginas e DOI; campo vazio não deixa marcador. É exibição:
    não se grava."""
    partes = [f"{'; '.join(e['autores'])} ({e['ano']}). {e['titulo']}. {e['veiculo']}"]
    for campo, marca in (("volume", "v. "), ("numero", "n. "), ("paginas", "p. ")):
        if e.get(campo):
            partes.append(f"{marca}{e[campo]}")
    texto = ", ".join(partes) + "."
    if e.get("doi"):
        texto += f" DOI: {e['doi']}"
    return texto


def distribuicao(estudos, siglas):
    """Distribuição das sementes pelas bases e por papel, calculada do arquivo de sementes.

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
    # Toda seção exigida, antes de qualquer tabela: sem o cabeçalho de uma seção, as tabelas
    # dela caem na seção anterior, e a reprovação nomearia a tabela, não a seção que falta.
    for e in G.exigidos(G.PROTOCOLO):
        if isinstance(e, G.Secao):
            secao(t, e)
    pal = facetas(t, locais)
    tb, idiomas = tabelas(t, pal, locais)
    _estrutural(params, "idiomas", list(idiomas))
    ids_facetas = [f["id"] for f in pal]
    insts, insts_faceta = instrumentos(t, ids_facetas, idiomas, locais)
    _estrutural(params, "instrumentos", [
        f"{s} ({i['modo']}; {'/'.join(i['idiomas'])}; {','.join(i['facetas'])})"
        for s, i in insts.items()])
    st = strings(t, set(ids_facetas), locais)
    for n in st:
        # A string repete termo entre idiomas; a lista executada é deduplicada. É ela
        # que a derivação local usa, e é ela que o relatório conta.
        # A grafia lida, sem a deduplicação sem acento, é a que se compara com a STR
        # gerada do quadro (`geracao.py`): lá o acento distingue.
        st[n]["literais"] = list(dict.fromkeys(st[n]["termos"]))
        # A deduplicação apagaria a repetição antes da comparação: a forma repetida, na
        # grafia lida, fica registrada para que a STR com termo em duplicidade reprove.
        st[n]["repetidos"] = {x: st[n]["termos"].count(x) for x in st[n]["literais"]
                              if st[n]["termos"].count(x) > 1}
        st[n]["termos"] = sem_repeticao(st[n]["termos"])
    anc = ancoras(pal, params)
    comp, exec_, sonda, sens = expressoes(ctx, t, params, locais, anc, st)
    crit = criterios(t, locais)
    fts = fontes(ctx, t, locais)
    siglas = [b["sigla"] for b in fts["bases"]]
    _estrutural(params, "bases", [f"{b['id']} {b['sigla']} → {b['ficha']}"
                                  for b in fts["bases"]])
    est = sementes(ctx.texto_sementes, siglas, ids_facetas, locais)
    params["sementes"] = {"valor": [f"{e['id']} ({e['papel']}): {', '.join(e['bases'])}"
                                    for e in est],
                          "origem": f"arquivo de sementes ({ctx.caminho_sementes})"}
    d = {
        "questoes": questoes(t, locais),
        "facetas": pal,
        "ancoras": anc,
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
    _parametro(ctx, params, "dimensoes_criterio", None, "conferencia.dimensoes_criterio")
    d["parametros"] = params
    d["papeis"] = papeis(d)
    d["locais"] = locais
    return d
