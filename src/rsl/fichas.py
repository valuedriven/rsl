"""Leitura das fichas de busca por base.

A ficha da base é a fonte da FORMA; o protocolo é a fonte do VOCABULÁRIO. O leitor não
conhece sintaxe de base além do necessário para separar termo de campo e de operador:
campo, tag e operador são lidos do texto da ficha. O que ele conhece é o contrato de
extração — onde a string está e como o termo se separa —, declarado em `gramatica.py`.
"""

import re

from . import gramatica as G
from .erros import ProtocoloInvalido
from .leitura import sem_repeticao
from .markdown import celulas, desescapa, linhas_de_tabela, normaliza, secao

OPERADORES = {"OR", "AND", "NOT"}
# Campos de busca de string reconhecidos nas sintaxes das bases (conhecimento da sintaxe,
# não parâmetro do projeto).
CAMPOS_STRING = ("title", "abstract", "descriptor", "TS", "TI", "AB", "AK")
MODOS_EXECUCAO = tuple(G.D_EXECUCAO.valores.values())
MODO_CURADA = "curada"


def documento(caminho):
    return f"ficha {caminho}"


def base_de(d, sigla):
    """A base de sigla `sigla`, da tabela de bases lida em `d`."""
    achada = next((b for b in d["bases"] if b["sigla"] == sigla), None)
    if achada is None:
        raise ProtocoloInvalido(G.T_BASES, f"base {sigla!r} não consta da tabela "
                                           f"({[b['sigla'] for b in d['bases']]})")
    return achada


def ficha(ctx, d, sigla):
    b = base_de(d, sigla)
    return ctx.ficha(sigla, b["ficha"])


def forma_execucao(t_ficha, caminho):
    """Forma de execução declarada na ficha: exatamente uma linha do marcador de execução.

    Sem padrão: linha ausente, repetida ou com valor fora do domínio reprova, nomeando a
    ficha. Devolve o valor interno.
    """
    doc = documento(caminho)
    achados = G.MF_EXECUCAO.padrao.findall(t_ficha)
    admitidos = list(G.D_EXECUCAO.valores)
    if not achados:
        raise ProtocoloInvalido(G.MF_EXECUCAO, f"falta a linha `{G.MF_EXECUCAO.texto}` "
                                               f"(formas admitidas: {admitidos})", doc)
    if len(achados) > 1:
        raise ProtocoloInvalido(G.MF_EXECUCAO, f"linha repetida {achados}", doc)
    valor = desescapa(achados[0]).strip()
    if valor not in G.D_EXECUCAO.valores:
        raise ProtocoloInvalido(G.D_EXECUCAO, f"forma de execução {valor!r} fora das "
                                              f"admitidas {admitidos}", doc)
    return G.D_EXECUCAO.valores[valor]


def criterios_da_ficha(t_ficha, caminho):
    """IDs de critério citados na seção de critérios da ficha, coluna de ID.

    A ficha declara o que a base aplica e onde; a chave é o ID. Agrupamento na mesma
    célula (`CEn / CEm`) conta os dois. Seção ausente, ou sem nenhum ID, é ficha
    ilegível: sem ela não se sabe o que a base aplica.
    """
    doc = documento(caminho)
    ids = []
    for _, linha in linhas_de_tabela(secao(t_ficha, G.SF_CRITERIOS, doc)):
        cels = celulas(linha)
        if len(cels) < 2:
            continue
        ids += [f"{G.I_CE.prefixo}{n}" for n in G.I_CE.padrao.findall(cels[1])]
    if not ids:
        raise ProtocoloInvalido(G.TF_CRITERIOS, f"sem IDs de critério na coluna "
                                                f"{G.TF_CRITERIOS.colunas[1]}", doc)
    return sorted(set(ids), key=lambda x: int(x[len(G.I_CE.prefixo):]))


def _rotulo(linha):
    """Rótulo legível: desfaz ênfase do Markdown, corta a lista de facetas e a pontuação."""
    s = re.sub(r"[*`_]", "", (linha or "")).strip()
    s = re.split(r"\s*" + re.escape(G.MARCA_FACETAS), s)[0]
    return re.sub(r"\s+", " ", s).rstrip(":;.").strip()


def cercados(bloco):
    """Blocos ```...``` do trecho, cada um com o rótulo da última linha que o precede."""
    saida, ultimo = [], ""
    linhas = bloco.splitlines()
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        if linha.strip().startswith("```"):
            i += 1
            corpo = []
            while i < len(linhas) and not linhas[i].strip().startswith("```"):
                corpo.append(linhas[i])
                i += 1
            texto_bloco = "\n".join(corpo).strip()
            if texto_bloco:
                saida.append({"rotulo": _rotulo(ultimo), "texto": texto_bloco})
            ultimo = ""
        elif linha.strip():
            ultimo = linha.strip()
        i += 1
    return saida


def _campo_string(texto):
    """Campo em que a string é buscada. Lido do próprio texto, não de tabela do script."""
    t = texto.strip()
    if re.match(r"^TS\s*=", t, re.I):
        return "TS"
    if re.match(r"^TITLE-ABS-KEY", t, re.I):
        return "TITLE-ABS-KEY"
    prefixos = {p.lower() for p in re.findall(r"(?<![\w-])([A-Za-z]+)\s*:", t)}
    campos = {p for p in prefixos if p in CAMPOS_STRING}
    if len(campos) == 1:
        return campos.pop()
    if len(campos) > 1:
        return "misto"
    return "todos os campos"


def _termos_string(texto, doc):
    """Termos de uma string de base: separados por OR e AND, sem operador nem campo."""
    t = re.sub(r"^\s*(?:TS|TITLE-ABS-KEY)\s*[=(]\s*", "", texto.strip(), flags=re.I)
    if t.endswith(")"):
        t = t[:-1]
    saida = []
    for parte in re.split(r"\s+(?:OR|AND|NOT)\s+", t):
        p = re.sub(r"^[()\s]+", "", parte)
        p = re.sub(r"[()\s]+$", "", p)
        p = re.sub(r"^(?:title|abstract|descriptor|TS|TI|AB|AK)\s*:\s*", "", p, flags=re.I)
        p = p.strip().strip('"').strip()
        p = re.sub(r"^[()\s]+|[()\s]+$", "", p).strip(" .;")
        if not p or p.upper() in OPERADORES:
            continue
        if '"' in p or "(" in p or " NEAR/" in p.upper() or " W/" in p.upper():
            raise ProtocoloInvalido(G.F_STRING_BASE, f"termo fora do padrão esperado: {p!r}",
                                    doc)
        saida.append(p)
    if not saida:
        raise ProtocoloInvalido(G.F_STRING_BASE, "string sem termo legível", doc)
    return sem_repeticao(saida)


def termos_bloco(texto):
    """Termos de um bloco de expressão, sem campo, operador, proximidade nem filtro.

    O bloco é o que se submete à base: dele saem o campo (`TS=`, `TITLE-ABS-KEY(`,
    `title:`), o operador (`AND`, `OR`, `NOT`, `NEAR/n`, `W/n`), os parênteses e o valor
    de cláusula de filtro (`PY=`, `LA=`, `DT=`, `PUBYEAR`, `LANGUAGE(`, `DOCTYPE(`), que
    não é termo de busca. O que resta é o conjunto de termos que a conferência compara com
    as strings das facetas declaradas.
    """
    t = re.sub(r"\b(?:PY|LA|LANGUAGE|DT|DOCTYPE)\s*=?\s*\([^)]*\)", " ", texto, flags=re.I)
    t = re.sub(r"\bPUBYEAR\s*[<>]=?\s*\d{4}", " ", t, flags=re.I)
    t = re.sub(r"\b(?:NEAR|PRE|W)\s*/\s*\d+", " ", t, flags=re.I)
    t = re.sub(r"\b(?:TS|TITLE-ABS-KEY)\s*[=(]", " ", t, flags=re.I)
    t = re.sub(r"\b(?:title|abstract|descriptorx?|TI|AB|AK|SU|WC|KP|SO|DO|ALL)\s*:\s*",
               " ", t, flags=re.I)
    saida = []
    for m in re.finditer(r'"([^"]+)"|([^\s()]+)', t):
        termo = (m.group(1) or m.group(2) or "").strip()
        if not termo or termo.upper() in OPERADORES:
            continue
        saida.append(termo)
    return sem_repeticao(saida)


def _facetas(texto):
    return sorted({f"{G.I_FCT.prefixo}{n}" for n in G.I_FCT.padrao.findall(texto)})


def _facetas_do_texto(resto):
    m = G.MF_FACETAS.padrao.search(resto)
    if not m:
        return []
    return _facetas(m.group(1))


def _estatuto_do_texto(resto):
    baixo = normaliza(resto[:1600])
    # A fidelidade vem antes da derivação: a expressão derivada que se executa no teste
    # de fidelidade é bloco que se submete, e o estatuto tem de dizer isso.
    for estatuto, frases in G.ESTATUTOS:
        if any(f in baixo for f in frases):
            return estatuto
    return "nao declarado"


def facetas_base(t, doc):
    """As strings por faceta da ficha: STRn, faceta, conjunto, campo, termos."""
    bloco = secao(t, G.SF_STRINGS, doc)
    saida = []
    for parte in re.split(r"^###\s+", bloco, flags=re.M)[1:]:
        cab, _, resto = parte.partition("\n")
        m = re.match(G.F_STRING_BASE.padrao, cab.strip())
        if not m:
            continue
        ident = m.group(1)
        mf = G.I_FCT.padrao.search(cab)
        if not mf:
            raise ProtocoloInvalido(G.F_STRING_BASE, f"{ident}: seção da string não declara "
                                                     f"a faceta", doc)
        blocos = cercados(resto)
        if len(blocos) != 1:
            raise ProtocoloInvalido(G.F_STRING_BASE, f"{ident}: esperava um bloco de string, "
                                                     f"achei {len(blocos)}", doc)
        texto_string = blocos[0]["texto"]
        mc = G.F_CONJUNTO.padrao.search(cab)
        saida.append({
            "id": ident, "faceta": f"{G.I_FCT.prefixo}{int(mf.group(1))}",
            "conjunto": mc.group(1) if mc else "",
            "campo": _campo_string(texto_string),
            "texto": texto_string,
            "termos": _termos_string(texto_string, doc),
        })
    if not saida:
        raise ProtocoloInvalido(G.F_STRING_BASE, "ficha sem strings por faceta legíveis", doc)
    return saida


def _expressoes_em_negrito(resto):
    """Expressões rotuladas em negrito, com o bloco que as segue (forma longa)."""
    saida = {}
    eb = G.I_EB.prefixo
    for m in re.finditer(rf"\*\*({eb}\d+)\*\*(.*?)(?=\n\*\*{eb}\d+\*\*|\Z)", resto, re.S):
        ident, corpo = m.group(1), m.group(2)
        facetas = _facetas(corpo.split("```")[0])
        cabeca = _rotulo(corpo.split("\n")[0])
        saida[ident] = {"id": ident, "titulo": f"{ident} {cabeca}".strip(),
                        "estatuto": "derivada", "facetas": facetas,
                        "blocos": cercados(corpo), "forma_longa": True}
    return saida


def consultas_curadas(bloco, doc=None):
    """Forma curada: uma consulta por linha de tabela, agrupada pelo subtítulo."""
    saida = []
    for parte in re.split(r"^####\s+", bloco, flags=re.M)[1:]:
        cab, _, resto = parte.partition("\n")
        grupo = _rotulo(cab)
        for linha in resto.splitlines():
            if not linha.strip().startswith("|"):
                continue
            cels = celulas(linha)
            if len(cels) < 2 or not re.match(r"^\d+$", cels[0]):
                continue
            mc = re.search(r"`([^`]+)`", cels[1])
            consulta = (mc.group(1) if mc else desescapa(cels[1])).strip()
            item = {"grupo": grupo, "n": int(cels[0]),
                    "rotulo": f"{grupo} — consulta {int(cels[0])}",
                    "consulta": consulta}
            # A faceta é identificada só pelo código FCTn; símbolo gráfico não conta.
            facetas = _facetas(cels[2] if len(cels) > 2 else "")
            if facetas:
                item["facetas"] = facetas
            saida.append(item)
    if not saida:
        raise ProtocoloInvalido(G.M_SUBTITULOS, "forma curada declarada sem consulta "
                                                "legível", doc)
    return saida


def expressoes_base(t, doc):
    """As expressões na forma desta base, a forma curada e a âncora em proximidade."""
    bloco = secao(t, G.SF_EXPRESSOES, doc)
    expressoes, curadas, ancoras = {}, [], None
    for parte in re.split(G.M_SUBTITULOS.padrao, bloco)[1:]:
        cab, _, resto = parte.partition("\n")
        titulo = _rotulo(cab)
        baixo = titulo.lower()
        if baixo.startswith(G.SUBTITULOS_IGNORADOS):
            continue
        m = G.F_EXPRESSAO_BASE.padrao.match(titulo)
        if m:
            ident = m.group(1)
            expressoes[ident] = {"id": ident, "titulo": titulo,
                                 "estatuto": _estatuto_do_texto(resto),
                                 "facetas": _facetas_do_texto(resto),
                                 "blocos": cercados(resto)}
            continue
        if G.SUBTITULO_PROXIMIDADE in baixo:
            # O conjunto das duas âncoras é definido uma vez e reusado pelas expressões;
            # sem ele, a forma por conjuntos cita um conjunto que o derivado não define.
            blocos = cercados(resto)
            if blocos:
                ancoras = {"rotulo": titulo, "formas": blocos}
            continue
        if G.SUBTITULO_CURADAS in baixo:
            curadas = consultas_curadas(resto, doc)
            continue
        if G.SUBTITULO_FORMA_LONGA in baixo:
            expressoes.update(_expressoes_em_negrito(resto))
            continue
    return expressoes, curadas, ancoras


def execucao_base(forma, expressoes, curadas, executada, doc):
    """O que se executa nesta base: uma, particionada em subconsultas ou curada.

    A expressão é a que o protocolo declara executada; a forma (única ou particionada)
    é a declarada na ficha, e a curada, a da própria ficha.
    """
    expressao = executada
    if curadas:
        modo = MODO_CURADA
        itens = curadas
    else:
        modo = forma
        if executada not in expressoes:
            raise ProtocoloInvalido(G.F_EXPRESSAO_BASE, f"a ficha não traz a expressão "
                                                        f"executada {executada}", doc)
        ex = expressoes[executada]
        itens = [{"rotulo": b["rotulo"], "consulta": b["texto"]} for b in ex["blocos"]
                 if G.ROTULO_NAO_EXECUTADA not in normaliza(b["rotulo"])]
        if not itens:
            itens = [{"rotulo": b["rotulo"], "consulta": b["texto"]} for b in ex["blocos"]]
    return {"modo": modo, "expressao": expressao, "itens": itens}


def filtros_base(execucao):
    """Filtros que a consulta carrega — e, por omissão, o que ficou na interface."""
    texto_consultas = " ".join(i.get("consulta", "") for i in execucao["itens"])

    def achado(padrao):
        return sorted({x.strip() for x in re.findall(padrao, texto_consultas) if x.strip()})
    ano = achado(r"PY=\(([^)]*)\)") + achado(r"PUBYEAR\s*[<>]=?\s*\d{4}")
    idioma = achado(r"(?:LA|LANGUAGE)=?\(([^)]*)\)")
    tipo = achado(r"(?:DT|DOCTYPE)=?\(([^)]*)\)")
    return {"ano": ano, "idioma": idioma, "tipo": tipo,
            "onde": "consulta" if (ano or idioma or tipo) else "interface"}


def declaracao_base(t, idiomas_quadro, doc):
    """Idiomas, camadas, derivações e redução declarada — o que a string pode deixar de fora."""
    bloco = secao(t, G.SF_DECLARACAO, doc)
    rotulos = {normaliza(r.texto): r for r in (G.RF_IDIOMAS, G.RF_CAMADAS, G.RF_DERIVACOES)}
    idiomas, camadas, derivacoes, exclusoes, achados = {}, None, "", [], set()
    for _, linha in linhas_de_tabela(bloco):
        cels = celulas(linha)
        if len(cels) < 2:
            continue
        rot = rotulos.get(normaliza(cels[0]))
        if rot is None:
            rot = next((r for k, r in rotulos.items() if normaliza(cels[0]).startswith(k)
                        and r is G.RF_DERIVACOES), None)
        if rot is G.RF_IDIOMAS:
            achados.add(rot)
            for par in cels[1].split(";"):
                m = re.match(rf"\s*({G.I_FCT.prefixo}\d+)\s*:\s*(.+)$", par.strip())
                if not m:
                    raise ProtocoloInvalido(G.RF_IDIOMAS, f"declaração ilegível: {par!r}",
                                            doc)
                idiomas[m.group(1)] = [x.strip() for x in m.group(2).split(",") if x.strip()]
        elif rot is G.RF_CAMADAS:
            achados.add(rot)
            camadas = normaliza(cels[1])
        elif rot is G.RF_DERIVACOES:
            achados.add(rot)
            derivacoes = normaliza(cels[1])
    for _, linha in linhas_de_tabela(bloco):
        cels = celulas(linha)
        if len(cels) >= 3 and G.F_REDUCAO.padrao.match(cels[0].strip()):
            exclusoes.append({"faceta": cels[0].strip(),
                              "termo": desescapa(cels[1]).strip(),
                              "motivo": desescapa(cels[2]).strip()})
    if G.RF_IDIOMAS not in achados or not idiomas:
        raise ProtocoloInvalido(G.RF_IDIOMAS, "declaração de cobertura sem idiomas por "
                                              "faceta", doc)
    if G.RF_CAMADAS not in achados:
        raise ProtocoloInvalido(G.RF_CAMADAS, "declaração de cobertura sem a linha de "
                                              "camadas", doc)
    if camadas not in G.D_CAMADAS.valores:
        raise ProtocoloInvalido(G.D_CAMADAS, f"camadas {camadas!r} não é "
                                             f"{' nem '.join(map(repr, G.D_CAMADAS.valores))}",
                                doc)
    for fid in idiomas:
        for i in idiomas[fid]:
            if i not in idiomas_quadro:
                raise ProtocoloInvalido(G.RF_IDIOMAS, f"declaração de {fid}: idioma {i!r} "
                                                      f"desconhecido", doc)
    modos = [m.strip() for m in re.split(r"\s*(?:,|;| e )\s*", derivacoes) if m.strip()]
    for m in modos:
        if m not in G.D_DERIVACOES.valores:
            raise ProtocoloInvalido(G.D_DERIVACOES, f"derivação declarada desconhecida: "
                                                    f"{m!r}; admitidas: "
                                                    f"{tuple(G.D_DERIVACOES.valores)}", doc)
    return {"idiomas": idiomas, "camadas": G.D_CAMADAS.valores[camadas], "derivacoes": modos,
            "exclusoes": exclusoes}


def base_derivada(ctx, d, sigla, t_ficha=None):
    """O derivado de uma base. A forma vem da ficha; o vocabulário, do protocolo."""
    b = base_de(d, sigla)
    doc = documento(b["ficha"])
    t = ficha(ctx, d, sigla) if t_ficha is None else t_ficha
    forma = forma_execucao(t, b["ficha"])
    expressoes, curadas, ancoras = expressoes_base(t, doc)
    execucao = execucao_base(forma, expressoes, curadas, d["executada"], doc)
    return {
        "base": {"id": b["id"], "sigla": sigla, "nome": b["nome"], "ficha": b["ficha"],
                 "execucao_declarada": forma},
        "facetas": facetas_base(t, doc),
        "criterios": criterios_da_ficha(t, b["ficha"]),
        "ancoras": ancoras,
        "expressoes": {k: expressoes[k] for k in sorted(expressoes)},
        "execucao": execucao,
        "filtros": filtros_base(execucao),
        "declaracao": declaracao_base(t, d["idiomas"], doc),
    }
