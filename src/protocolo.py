#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O protocolo como fonte: lê o documento, confere e sincroniza o que é alimentado.

O documento `docs/03_protocolo_estrategia_pesquisa.md` é a fonte única da questão, das
facetas, do vocabulário, das strings, das expressões, dos critérios, das fontes e do
conjunto-semente. A forma de cada base está na respectiva ficha, em
`docs/busca_base_N_*.md`. Este script lê as duas fontes em memória e NÃO grava derivado
algum: os documentos markdown são a fonte, e um JSON que apenas os repetisse seria uma
segunda cópia a defasar.

Em `data/` vivem só os arquivos que são alimentados:

  sementes.json          AUTORAL — metadados de conferência de cada semente. Referências,
                         ano, DOI, bases e chave de citação vêm do protocolo.
                         `--sincronizar` casa por DOI ou título e preserva o conferido.
  registro_execucao.json AUTORAL — registro documental das execuções, por base, e
                         rastro técnico de cada execução registrada por
                         `derivar_expressoes.py --registrar`.

Não há `descritores.json`, `consultas.json` nem `pendencias.json`: o estatuto da
validação vive na planilha `data/validacao_termologica.csv`, as execuções vivem no
`registro_execucao.json` e as pendências, nas fichas e no próprio registro.

A cobertura de cada base é medida contra o vocabulário que a ficha declara usar
(`idiomas`, `camadas`, `derivações`) e contra a redução que ela declara termo a termo:
termo do protocolo ausente e não declarado reprova, e termo na string que não derive do
protocolo também. A conferência é medida, não aprovação: a cobertura por faceta sai como
número, porque é ela que mede o preço da forma de cada base.

Uso
  python3 src/protocolo.py --conferir              # confere o documento
  python3 src/protocolo.py --conferir-dados        # confere os arquivos alimentados
  python3 src/protocolo.py --conferir --autoteste  # prova que as conferências reprovam
  python3 src/protocolo.py --sincronizar           # reconcilia sementes.json
  python3 src/protocolo.py --mostrar               # resume o que leu
  python3 src/protocolo.py --pendencias            # relata pendências, sem escrever

Só biblioteca padrão.
"""

import argparse
import copy
import csv
import json
import pathlib
import re
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOC = RAIZ / "docs" / "03_protocolo_estrategia_pesquisa.md"
DATA = RAIZ / "data"

# A forma de busca é de cada base e vive na ficha da base; o vocabulário é do protocolo.
# O script lê as duas fontes e não conhece sintaxe de base alguma: campo, tag e operador
# saem do texto da ficha.
FICHAS = {
    "wos": {"bd": "BD1", "arquivo": "docs/busca_base_1_web_of_science.md"},
    "scopus": {"bd": "BD2", "arquivo": "docs/busca_base_2_scopus.md"},
    "eric": {"bd": "BD3", "arquivo": "docs/busca_base_3_eric.md"},
    "brapci": {"bd": "BD4", "arquivo": "docs/busca_base_4_brapci.md"},
}

# Arquivos alimentados: não são derivados de markdown e não se regeram.
SEMENTES = DATA / "sementes.json"
REGISTRO = DATA / "registro_execucao.json"
# O estatuto da validação terminológica vive nesta planilha, não em JSON.
CSV_VALIDACAO = DATA / "validacao_termologica.csv"

IDIOMAS = ("pt", "en", "es")
CAMADAS = ("nucleo", "proximos", "relacionados")
BASES = ("WoS", "Scopus", "ERIC", "BRAPCI")

ROTULO_CAMADA = {
    "Termos centrais": "nucleo",
    "Descritores potenciais": "proximos",
    "Termos relacionados": "relacionados",
}

INSTRUMENTO_POR_IDIOMA = {"pt": ("TBCI",), "en": ("UNESCO",), "es": ("UNESCO",)}

STATUS_LIVRE_DECISAO = "termo livre (faceta declarada termo livre por decisão de protocolo)"
JUSTIFICATIVA_LIVRE = (
    "Decisão do ReT: os fatores situacionais são tratados como termos livres, dispensada a "
    "validação contra instrumento, e constam assim do protocolo.")

# Colunas da planilha de validação, na ordem em que ela é escrita. A própria planilha
# é o registro: não há JSON intermediário; `validar_termos.py` a lê e a regrava.
CAMPOS_VALIDACAO = (
    "instrumento", "consultado_em", "versao_instrumento", "url_consultada",
    "status_proposto", "rotulo_autorizado", "uri_conceito",
    "equivalentes_USE_UP", "termos_genericos_TG", "termos_especificos_TE",
    "termos_relacionados_TR", "nota_de_escopo",
    "arquivo_evidencia", "observacao_tecnica",
    "decisao_ReT", "justificativa_ReT", "data_decisao",
)

# Metadados que o documento não guarda e que a sincronização NUNCA sobrescreve.
CAMPOS_AUTORAIS = ("verificacao", "escopo", "tipo", "alinhamento", "nota",
                   "veiculo_conferido", "eric")

# Emenda v2 (17/11/2026). As listas são a decisão registrada na Nota de emenda: o termo
# retirado não pode voltar à string, e o composto acrescentado não pode sumir. Elas são
# por string (FCT), porque o mesmo conceito pode ter sido retirado de uma faceta e mantido
# em outra — `nível de ensino`, por exemplo, saiu de STR2 e permanece em STR4.
RETIRADOS_V2 = {
    "FCT1": (
        "ontológico", "ontológica", "ontological", "taxonomia",
        "modelo conceitual", "modelagem conceitual", "esquema conceitual",
        "modelo semântico", "representação formal", "análise facetada",
        "análise de facetas", "conceptual model", "conceptual modeling", "conceptual modelling",
        "conceptual schema", "semantic model", "formal representation", "facet analysis",
        "modelo conceptual", "modelado conceptual", "esquema conceptual",
        "modelo semántico", "representación formal", "análisis facetado",
        "análisis de facetas",
    ),
    "FCT2": (
        "estudante", "aluno", "professor", "docente", "currículo",
        "instituição de ensino", "nível de ensino", "modalidade de ensino", "educativo",
        "student", "learner", "teacher", "instructor", "curriculum",
        "educational institution", "educational level", "education modality",
        "estudiante", "alumno", "currículo", "institución educativa",
        "nivel educativo", "modalidad educativa",
    ),
    "FCT4": (
        "contexto de aplicação", "contexto de uso", "ambiente de aprendizagem",
        "application context", "context of use", "learning environment",
        "contexto de aplicación", "contexto de uso", "entorno de aprendizaje",
    ),
}
ACRESCENTADOS_V2 = {
    "FCT1": (
        "ontologia educacional", "ontologia de aprendizagem", "ontologia de ensino",
        "modelo ontológico educacional", "ontologia de prática educacional",
        "ontologia de design instrucional", "ontologia de currículo", "ontologia facetada",
        "educational ontology", "learning ontology", "teaching ontology",
        "educational ontological model", "educational practice ontology",
        "instructional design ontology", "curriculum ontology", "faceted ontology",
        "ontología educativa", "ontología de aprendizaje", "ontología de enseñanza",
        "modelo ontológico educativo", "ontología de práctica educativa",
        "ontología de diseño instruccional", "ontología de currículo",
        "ontología facetada",
    ),
}

LEIA = {
    "sementes": "AUTORAL. Metadados de conferência de cada semente. As referências, o ano, o "
                "DOI, as bases esperadas e a chave de citação vêm de "
                "docs/03_protocolo_estrategia_pesquisa.md. `ligacao` é a ligação com o "
                "protocolo, por DOI ou título — não é conteúdo bibliográfico e não se edita; "
                "`id` é rótulo e pode mudar sem perder o metadado. "
                "`--sincronizar` casa por DOI ou título e preserva o que foi conferido. "
                "Semente retirada do protocolo permanece, e `--pendencias` a reporta.",
}


class ProtocoloInvalido(Exception):
    """O documento não tem a forma que o leitor sabe interpretar."""


# --------------------------------------------------------------------- utilidades
def texto(caminho=DOC):
    return pathlib.Path(caminho).read_text(encoding="utf-8")


def desescapa(s):
    """Desfaz os escapes do Markdown de origem (`\\-`, `\\(`, `\\.`, `\\_`)."""
    for de, para in (("\\-", "-"), ("\\_", "_"), ("\\*", "*"), ("\\(", "("),
                     ("\\)", ")"), ("\\.", "."), ("\\+", "+"), ("\\[", "["),
                     ("\\]", "]"), ("\\|", "|")):
        s = s.replace(de, para)
    return s


def normaliza(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def celulas(linha):
    """Células de uma linha de tabela, sem os pipes das pontas."""
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def secao(t, titulo):
    """Texto entre um cabeçalho `titulo` e o próximo cabeçalho de nível igual ou maior."""
    marca = re.search(r"^(#+)\s+" + re.escape(titulo) + r"\s*$", t, re.M)
    if not marca:
        raise ProtocoloInvalido(f"seção não encontrada: {titulo}")
    nivel = len(marca.group(1))
    resto = t[marca.end():]
    fim = re.search(r"^#{1,%d}\s+\S" % nivel, resto, re.M)
    return resto[:fim.start()] if fim else resto


def paragrafos(bloco):
    return [re.sub(r"\s+", " ", p).strip()
            for p in re.split(r"\n\s*\n", bloco) if p.strip()]


# ------------------------------------------------------------------------ questões
def questoes(t):
    bloco = secao(t, "Questão de revisão")
    geral = secao(bloco, "Questão geral de revisão")
    paras = paragrafos(geral)
    if not paras:
        raise ProtocoloInvalido("questão geral de revisão vazia")
    m = re.match(r"^-\s*QGR:\s*(.+)$", paras[0])
    if not m:
        raise ProtocoloInvalido("questão geral sem o identificador QGR")
    pergunta = m.group(1).strip()
    estrutura = ""
    for p in paras[1:]:
        if p.startswith("Estrutura da questão"):
            estrutura = re.sub(r"\s*Questões específicas de revisão:\s*$", "", p).strip()
    if not estrutura:
        raise ProtocoloInvalido("estrutura PICo da questão não declarada")

    especificas = []
    for m in re.finditer(r"^-\s*(QER\d+):\s*(.+)$", secao(bloco, "Questões específicas de revisão"),
                         re.M):
        especificas.append({"id": m.group(1), "texto": m.group(2).strip()})
    if len(especificas) != 4:
        raise ProtocoloInvalido(f"esperava QER1 a QER4, achei {len(especificas)}")
    if [e["id"] for e in especificas] != ["QER1", "QER2", "QER3", "QER4"]:
        raise ProtocoloInvalido(f"questões específicas fora de ordem: "
                                f"{[e['id'] for e in especificas]}")
    return {"id": "QGR", "questao_principal": pergunta, "estrutura_pico": estrutura,
            "questoes_especificas": especificas}


# ------------------------------------------------------------------------ facetas
def palavras(t):
    """Nome, cor e papel de cada faceta, da lista de palavras significativas."""
    bloco = secao(t, "Palavras significativas da questão de revisão")
    saida = []
    for m in re.finditer(r"^-\s*Faceta\s+(\d+)\s*(?:\((FCT\d+)\))?\s*:\s*(.+)$", bloco, re.M):
        n = int(m.group(1))
        codigo = m.group(2) or ""
        if codigo != f"FCT{n}":
            achado = codigo if codigo else "ausente"
            raise ProtocoloInvalido(
                f"faceta {n}: identificador {achado!r} não corresponde a FCT{n}")
        corpo = m.group(3)
        partes = [p.strip() for p in corpo.split("—")]
        if len(partes) < 2:
            raise ProtocoloInvalido(f"faceta {n}: nome e cor não separados por travessão")
        saida.append({
            "id": f"FCT{n}", "nome": partes[0], "cor": partes[1],
            "ancora": bool(re.search(r"âncora obrigatória\s+" + str(n), corpo)),
        })
    if len(saida) != 4:
        raise ProtocoloInvalido(f"esperava 4 facetas, achei {len(saida)}")
    ids = [f["id"] for f in saida]
    if ids != ["FCT1", "FCT2", "FCT3", "FCT4"]:
        raise ProtocoloInvalido(f"facetas fora da numeração FCT1 a FCT4: {ids}")
    return saida


def _termos_celula(celula):
    """Termos de uma célula, separados por `\\- `. O hífen interno vem sem escape."""
    partes = re.split(r"\\-\s*", celula)
    return [desescapa(p).strip() for p in partes if p.strip()]


def _sem_repeticao(seq):
    vistos, saida = set(), []
    for x in seq:
        k = normaliza(x)
        if k and k not in vistos:
            vistos.add(k)
            saida.append(x)
    return saida


def tabelas(t):
    """As quatro tabelas do controle terminológico, com camadas e instrumentos."""
    nomes = {f["id"]: f for f in palavras(t)}
    bloco = secao(t, "Controle terminológico")
    linhas = bloco.splitlines()

    saida, atual = [], None
    for linha in linhas:
        cab = re.match(r"^\|\s*FCT(\d+)\s*\|", linha)
        if cab:
            ident = f"FCT{int(cab.group(1))}"
            if ident not in nomes:
                raise ProtocoloInvalido(f"tabela da faceta {ident} sem palavra significativa")
            atual = {"id": ident, "nome": nomes[ident]["nome"],
                     "ancora": nomes[ident]["ancora"], "cor": nomes[ident]["cor"],
                     "instrumentos": "",
                     "camadas": {i: {c: [] for c in CAMADAS} for i in IDIOMAS}}
            saida.append(atual)
            continue
        if atual is None or not linha.startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 4:
            continue
        rotulo = cels[0].strip("* ").strip()
        if rotulo.startswith("Instrumentos"):
            atual["instrumentos"] = desescapa(cels[1]).strip()
            continue
        camada = next((v for k, v in ROTULO_CAMADA.items() if rotulo.startswith(k)), None)
        if camada is None:
            continue
        for idioma, cel in zip(IDIOMAS, cels[1:4]):
            atual["camadas"][idioma][camada] = _termos_celula(cel)

    if len(saida) != 4:
        raise ProtocoloInvalido(f"esperava 4 tabelas de faceta, achei {len(saida)}")
    for f in saida:
        f["termos"] = {i: _sem_repeticao(
            [x for c in CAMADAS for x in f["camadas"][i][c]]) for i in IDIOMAS}
        f["livre"] = bool(re.search(r"DISPENSADA|TERMOS LIVRES", f["instrumentos"], re.I))
    return saida


# ------------------------------------------------------------------------- strings
def strings(t):
    """Termos executados de cada faceta, extraídos das strings entre aspas."""
    bloco = secao(t, "Strings de busca por faceta")
    ids_faceta = {f["id"] for f in palavras(t)}
    saida = {}
    for linha in bloco.splitlines():
        if not linha.lstrip().startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 3:
            continue
        mi, mf = re.match(r"^STR(\d+)$", cels[0]), re.match(r"^FCT(\d+)$", cels[1])
        if not (mi and mf):
            continue
        n, nf = int(mi.group(1)), int(mf.group(1))
        if n != nf:
            raise ProtocoloInvalido(
                f"{cels[0]} está declarada como {cels[1]}: identificadores não casam")
        id_faceta = f"FCT{n}"
        if id_faceta not in ids_faceta:
            raise ProtocoloInvalido(f"STR{n} sem faceta {id_faceta} nas palavras significativas")
        celula = cels[2]
        termos = re.findall(r'"([^"]+)"', celula)
        if not termos:
            raise ProtocoloInvalido(f"string da faceta {n} sem termos entre aspas")
        residuo = re.sub(r'"[^"]+"', "", celula)
        residuo = residuo.replace("OR", " ").replace("(", " ").replace(")", " ")
        if residuo.strip(" .;|"):
            raise ProtocoloInvalido(
                f"string da faceta {n} tem conteúdo fora do padrão \"termo\" OR ...: "
                f"{residuo.strip()[:60]!r}")
        saida[id_faceta] = {"id": f"STR{n}", "texto": celula, "termos": termos}
    if sorted(saida) != ["FCT1", "FCT2", "FCT3", "FCT4"]:
        raise ProtocoloInvalido(f"esperava uma string por faceta, achei {sorted(saida)}")
    return saida


# ---------------------------------------------------------------------- expressões
def _grupos_de_composicao(comb, ident):
    """Composição como AND de ORs: `STR1 + STR2 + (STR3 OR STR4)`.

    A forma devolvida é uma lista de grupos; todo grupo tem de ser satisfeito e, dentro do
    grupo, basta um dos STRn. A composição puramente conjuntiva é o caso particular em que
    todo grupo tem um único elemento.
    """
    partes, profundidade, atual = [], 0, ""
    for ch in comb:
        if ch == "(":
            profundidade += 1
        elif ch == ")":
            profundidade -= 1
            if profundidade < 0:
                raise ProtocoloInvalido(f"expressão {ident}: parêntese fechado sem abrir")
        if ch == "+" and profundidade == 0:
            partes.append(atual)
            atual = ""
        else:
            atual += ch
    partes.append(atual)
    if profundidade:
        raise ProtocoloInvalido(f"expressão {ident}: parêntese aberto sem fechar")

    grupos = []
    for parte in partes:
        p = parte.strip()
        if not p:
            raise ProtocoloInvalido(f"expressão {ident}: operador `+` sem operando")
        m = re.fullmatch(r"\(\s*(STR\d+(?:\s+OR\s+STR\d+)+)\s*\)", p)
        if m:
            membros = [x.strip() for x in m.group(1).split("OR")]
        elif re.fullmatch(r"STR\d+", p):
            membros = [p]
        else:
            raise ProtocoloInvalido(
                f"expressão {ident}: composição fora do padrão STRn + STRn ou "
                f"(STRn OR STRn): {comb!r}")
        grupos.append(membros)
    return grupos


def expressoes(t):
    """Composição de EB1 a EB5, qual se executa e qual é sonda de sensibilidade."""
    bloco = secao(t, "Expressões de busca")
    composicao, executada, sonda = {}, set(), set()
    for linha in bloco.splitlines():
        if not linha.lstrip().startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 4:
            continue
        if not re.match(r"^EB\d+$", cels[0]):
            continue
        ident = cels[0]
        comb = desescapa(cels[2]).replace("\\", " ").strip()
        if not re.search(r"STR\d+", comb):
            raise ProtocoloInvalido(f"expressão {ident} sem composição legível")
        composicao[ident] = _grupos_de_composicao(comb, ident)
        natureza = normaliza(cels[1])
        if natureza == "cobertura restrita":
            executada.add(ident)
        elif natureza == "controle de sensibilidade":
            sonda.add(ident)
    if sorted(composicao) != ["EB1", "EB2", "EB3", "EB4", "EB5"]:
        raise ProtocoloInvalido(f"esperava EB1 a EB5, achei {sorted(composicao)}")
    if len(executada) != 1:
        raise ProtocoloInvalido(f"esperava exatamente uma expressão executada, achei {executada}")
    if len(sonda) != 1:
        raise ProtocoloInvalido(f"esperava exatamente uma sonda de sensibilidade, achei {sonda}")
    return composicao, executada.pop(), sonda.pop()


# ---------------------------------------------------------------------- critérios
def criterios(t):
    bloco = secao(t, "Critérios de elegibilidade")
    saida, dimensao, ids = [], "", []
    for linha in bloco.splitlines():
        if not linha.strip().startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 6:
            continue
        m = re.match(r"^CE(\d+)$", cels[0])
        if not m:
            continue
        acao = desescapa(cels[2]).strip()
        if acao not in ("Incluir", "Excluir"):
            raise ProtocoloInvalido(f"{cels[0]}: ação {acao!r} não é Incluir nem Excluir")
        rotulo = desescapa(cels[1].strip("* ")).strip()
        if rotulo:
            dimensao = rotulo
        ids.append(int(m.group(1)))
        saida.append({"id": f"CE{int(m.group(1))}", "dimensao": dimensao, "acao": acao,
                      "criterio": desescapa(cels[3]).strip(),
                      "justificativa": desescapa(cels[5]).strip()})
    if len(saida) != 9:
        raise ProtocoloInvalido(f"esperava 9 critérios, achei {len(saida)}")
    if ids != list(range(1, len(saida) + 1)):
        raise ProtocoloInvalido(f"critérios fora da numeração CE1 a CE9: {ids}")
    if not any(c["dimensao"] == "Intervalo temporal" and c["acao"] == "Incluir"
               for c in saida):
        raise ProtocoloInvalido("critério de recorte temporal não declarado")
    return saida


def recorte(t):
    """Recorte temporal: ano inicial e teto, com o texto que o declara."""
    for c in criterios(t):
        if c["dimensao"] == "Intervalo temporal" and c["acao"] == "Incluir":
            m = re.search(r"após o ano\s+(\d{4})", c["criterio"])
            if not m:
                raise ProtocoloInvalido("recorte temporal sem ano legível")
            # "após o ano 2016" é inclusivo a partir de 2017. O teto é a data de execução
            # da busca, e por isso fica em None: o consumidor o resolve pelo ano corrente,
            # que é o ano em que a revisão executa.
            return {"ano_min": int(m.group(1)) + 1, "ano_max": None, "texto": c["criterio"]}
    raise ProtocoloInvalido("recorte temporal não declarado")


def limiar(t):
    bloco = secao(t, "Acervos pessoais")
    m = re.search(r"recuperação inferior a\s+(\d+)\s*%", bloco)
    if not m:
        raise ProtocoloInvalido("limiar de aderência não declarado")
    return int(m.group(1)) / 100


# ------------------------------------------------------------------------- fontes
def fontes(t):
    bloco = secao(t, "Fontes de informação")
    bases_bloco = secao(bloco, "Bases de dados")

    bases, ids = [], []
    for linha in bases_bloco.splitlines():
        if not linha.lstrip().startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 3:
            continue
        m = re.match(r"^BD(\d+)$", cels[0])
        if not m:
            continue
        ids.append(int(m.group(1)))
        bases.append({"id": f"BD{int(m.group(1))}",
                      "nome": desescapa(cels[1]).strip(),
                      "papel": desescapa(cels[2]).strip()})
    if len(bases) != 4:
        raise ProtocoloInvalido(f"esperava 4 bases de dados, achei {len(bases)}")
    if ids != [1, 2, 3, 4]:
        raise ProtocoloInvalido(f"bases fora da numeração BD1 a BD4: {ids}")

    acesso = next((p for p in paragrafos(bases_bloco)
                   if p.startswith("Ordem de execução")), "")
    if not acesso:
        raise ProtocoloInvalido("ordem de execução das bases não declarada")
    m = re.search(r"Ordem de execução:\s*(.+?),?\s*nesta sequência\.?\s*", acesso)
    if not m:
        raise ProtocoloInvalido("ordem de execução sem lista legível")
    ordem = []
    for nome in [x.strip() for x in re.split(r",| e ", m.group(1)) if x.strip()]:
        cand = [b for b in bases if normaliza(b["nome"]).startswith(normaliza(nome))]
        if len(cand) != 1:
            raise ProtocoloInvalido(f"base {nome!r} da ordem de execução não identificada")
        ordem.append(cand[0]["nome"])
    if sorted(ordem) != sorted(b["nome"] for b in bases):
        raise ProtocoloInvalido(f"ordem de execução incompleta: {ordem}")
    via = acesso[m.end():].strip()

    ferramenta = []
    for fm in re.finditer(r"^-\s*(.+?):\s*(.+)$",
                          secao(t, "Ferramenta de gestão bibliográfica"), re.M):
        ferramenta.append({"tema": desescapa(fm.group(1)).strip(),
                           "texto": desescapa(fm.group(2)).strip()})
    if len(ferramenta) != 3:
        raise ProtocoloInvalido(f"esperava 3 itens de ferramenta de gestão, achei {len(ferramenta)}")

    return {
        "bases": bases,
        "ordem_execucao": ordem,
        "via_de_acesso": via,
        "acervos_especiais": " ".join(paragrafos(secao(bloco, "Acervos especiais"))).strip(),
        "ferramenta_gestao": ferramenta,
    }


# ------------------------------------------------------------------------- sementes
def _titulo(resto):
    """O título termina no primeiro ponto seguido de maiúscula ou de dígito."""
    m = re.search(r"[.!?]\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9“\"])", resto)
    return (resto[:m.start() + 1] if m else resto).strip()


def _doi(texto_ref):
    m = re.search(r"DOI:\s*(10\.\S+?)\s*$", texto_ref.rstrip())
    if not m:
        return ""
    return m.group(1).rstrip(".")


def _mapa(bloco):
    """Mapa por estudo: (n, autor, ano, bases) da frase de distribuição."""
    linha = next((l for l in bloco.splitlines() if "Mapa por estudo" in l), "")
    return [(int(n), aut, int(ano), [b.strip() for b in bases.split("+")])
            for n, aut, ano, bases in re.findall(
                r"\((\d+)\)\s+([A-Za-zÀ-ÿ][\wÀ-ÿ'’-]*(?:\s+[A-Za-zÀ-ÿ][\wÀ-ÿ'’-]*)*)\s+"
                r"(\d{4})\s+—\s+([^;.]+)", linha)]


def sementes(t):
    """Referências, bases esperadas e distribuição declarada do conjunto-semente."""
    bloco = secao(t, "Acervos pessoais")
    refs = re.findall(r"^- (SE\d+):\s+(.+)$", bloco, re.M)
    if not refs:
        raise ProtocoloInvalido("nenhuma referência identificada em Acervos pessoais")

    mapa = {n: (aut, ano, bases) for n, aut, ano, bases in _mapa(bloco)}
    estudos = []
    for ident, bruto in refs:
        n = int(ident[2:])
        ref = desescapa(bruto).strip()
        m = re.match(r"^(.*?)\s*\((\d{4})\)\.\s*(.*)$", ref)
        if not m:
            raise ProtocoloInvalido(f"referência {n} sem autoria e ano no padrão esperado")
        autores, ano, resto = m.groups()
        aut_mapa, ano_mapa, bases = mapa.get(n, ("", 0, []))
        primeiro = autores.split(",")[0].strip()
        if aut_mapa and normaliza(primeiro) != normaliza(aut_mapa):
            raise ProtocoloInvalido(
                f"referência {n}: mapa diz {aut_mapa!r} e a lista diz {primeiro!r}")
        if ano_mapa and int(ano) != ano_mapa:
            raise ProtocoloInvalido(f"referência {n}: mapa diz {ano_mapa}, lista diz {ano}")
        estudos.append({
            "id": ident, "autores": autores.strip(), "ano": int(ano),
            "titulo": _titulo(resto), "doi": _doi(ref),
            "bases": bases, "chave": f"{primeiro} {ano}",
        })
    ids = [e["id"] for e in estudos]
    if ids != [f"SE{k}" for k in range(1, len(estudos) + 1)]:
        raise ProtocoloInvalido(f"referências fora da numeração SE1 a SE{len(estudos)}: {ids}")
    return estudos


def distribuicao(t, estudos):
    """Recalcula a distribuição do mapa e confere contra o parágrafo."""
    bloco = secao(t, "Acervos pessoais")
    por_base = {b: 0 for b in BASES}
    for e in estudos:
        for b in e["bases"]:
            if b not in por_base:
                raise ProtocoloInvalido(f"semente {e['id']}: base desconhecida {b!r}")
            por_base[b] += 1
    incidencias = sum(por_base.values())
    multi = sum(1 for e in estudos if len(e["bases"]) > 1)

    declarado = {}
    m = re.search(r"Scopus,\s*(\d+);\s*WoS,\s*(\d+);\s*ERIC,\s*(\d+);\s*BRAPCI,\s*(\d+)", bloco)
    if m:
        for b, v in zip(("Scopus", "WoS", "ERIC", "BRAPCI"), m.groups()):
            declarado[b] = int(v)
    m = re.search(r"A soma das incidências é\s*(\d+)\s*para\s*(\d+)\s*REGISTROS ÚNICOS", bloco)
    declarado_inc = int(m.group(1)) if m else None
    declarado_unicos = int(m.group(2)) if m else None
    m = re.search(r"(\d+)\s*estudos estão em mais de uma base e\s*(\d+)\s*em uma só", bloco)
    declarado_multi = int(m.group(1)) if m else None
    declarado_so_um = int(m.group(2)) if m else None

    return {
        "por_base": por_base, "incidencias": incidencias, "registros": len(estudos),
        "em_mais_de_uma_base": multi, "em_uma_so": len(estudos) - multi,
        "declarado": {
            "por_base": declarado, "incidencias": declarado_inc,
            "registros": declarado_unicos, "em_mais_de_uma_base": declarado_multi,
            "em_uma_so": declarado_so_um,
        },
    }


# ------------------------------------------------------------------- fichas por base
# A ficha da base é a fonte da FORMA; o protocolo é a fonte do VOCABULÁRIO. O script não
# conhece sintaxe de base: campo, tag e operador são lidos do texto da ficha. O que ele
# conhece é o contrato de extração — onde a string está e como o termo se separa.

COR_FACETA = {"🟦": "FCT1", "🟨": "FCT2", "🟥": "FCT3", "🟧": "FCT4"}
OPERADORES = {"OR", "AND", "NOT"}
CAMPOS_STRING = ("title", "abstract", "descriptor", "TS", "TI", "AB", "AK")
SECOES_FICHA = ("3. Strings por faceta", "4. Expressões de busca",
                "Declaração de cobertura")
MODOS_DERIVACAO = ("morfologia", "radical")


def ficha(slug):
    return (RAIZ / FICHAS[slug]["arquivo"]).read_text(encoding="utf-8")


def _rotulo(linha):
    """Rótulo legível: desfaz ênfase do Markdown, corta a lista de facetas e a pontuação."""
    s = re.sub(r"[*`_]", "", (linha or "")).strip()
    s = re.split(r"\s*Facetas:", s)[0]
    return re.sub(r"\s+", " ", s).rstrip(":;.").strip()


def _cercados(bloco):
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


def _termos_string(texto):
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
            raise ProtocoloInvalido(f"termo fora do padrão esperado na ficha: {p!r}")
        saida.append(p)
    if not saida:
        raise ProtocoloInvalido("string sem termo legível")
    return _sem_repeticao(saida)


def _facetas_do_texto(resto):
    m = re.search(r"Facetas:\s*\**\s*(.+)", resto)
    if not m:
        return []
    return sorted({f"FCT{n}" for n in re.findall(r"FCT(\d)", m.group(1))})


def _estatuto_do_texto(resto):
    baixo = normaliza(resto[:1600])
    if "sonda de sensibilidade" in baixo or "controle de sensibilidade" in baixo:
        return "sonda"
    if "nao se executa" in baixo or "derivada localmente" in baixo:
        return "derivada"
    if "executada e exportada" in baixo or "esta que se executa" in baixo:
        return "executada"
    if "teste de fidelidade" in baixo:
        return "fidelidade"
    return "nao declarado"


def facetas_base(t):
    """As strings por faceta da ficha: STRn, faceta, conjunto, campo, termos."""
    bloco = secao(t, SECOES_FICHA[0])
    saida = []
    for parte in re.split(r"^###\s+", bloco, flags=re.M)[1:]:
        cab, _, resto = parte.partition("\n")
        m = re.match(r"`(STR\d+[a-z]?)`", cab.strip())
        if not m:
            continue
        ident = m.group(1)
        mf = re.search(r"FCT(\d)", cab)
        if not mf:
            raise ProtocoloInvalido(f"{ident}: seção da string não declara a faceta")
        blocos = _cercados(resto)
        if len(blocos) != 1:
            raise ProtocoloInvalido(
                f"{ident}: esperava um bloco de string, achei {len(blocos)}")
        texto_string = blocos[0]["texto"]
        mc = re.search(r"conjunto\s+`(#\w+)`", cab)
        saida.append({
            "id": ident, "faceta": f"FCT{int(mf.group(1))}",
            "conjunto": mc.group(1) if mc else "",
            "campo": _campo_string(texto_string),
            "texto": texto_string,
            "termos": _termos_string(texto_string),
        })
    if not saida:
        raise ProtocoloInvalido("ficha sem strings por faceta legíveis")
    return saida


def _expressoes_em_negrito(resto):
    """Expressões rotuladas em negrito, com o bloco que as segue (forma longa da BRAPCI)."""
    saida = {}
    for m in re.finditer(r"\*\*(EB\d)\*\*(.*?)(?=\n\*\*EB\d\*\*|\Z)", resto, re.S):
        ident, corpo = m.group(1), m.group(2)
        facetas = sorted({f"FCT{n}" for n in re.findall(r"FCT(\d)", corpo.split("```")[0])})
        cabeca = _rotulo(corpo.split("\n")[0])
        saida[ident] = {"id": ident, "titulo": f"{ident} {cabeca}".strip(),
                        "estatuto": "derivada", "facetas": facetas,
                        "blocos": _cercados(corpo)}
    return saida


def consultas_curadas(bloco):
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
            facetas = {f"FCT{n}" for n in re.findall(r"FCT(\d)", cels[2] if len(cels) > 2 else "")}
            for cor, fid in COR_FACETA.items():
                if len(cels) > 2 and cor in cels[2]:
                    facetas.add(fid)
            if facetas:
                item["facetas"] = sorted(facetas)
            saida.append(item)
    if not saida:
        raise ProtocoloInvalido("forma curada declarada sem consulta legível")
    return saida


def expressoes_base(t, slug):
    """As cinco expressões na forma desta base, a forma curada e a âncora em proximidade."""
    bloco = secao(t, SECOES_FICHA[1])
    expressoes, curadas, ancoras = {}, [], None
    for parte in re.split(r"^###\s+", bloco, flags=re.M)[1:]:
        cab, _, resto = parte.partition("\n")
        titulo = _rotulo(cab)
        baixo = titulo.lower()
        if baixo.startswith(("como executar", "variantes", "como esta base")):
            continue
        if re.match(r"EB\d", titulo):
            ident = re.match(r"(EB\d)", titulo).group(1)
            expressoes[ident] = {"id": ident, "titulo": titulo,
                                 "estatuto": _estatuto_do_texto(resto),
                                 "facetas": _facetas_do_texto(resto),
                                 "blocos": _cercados(resto)}
            continue
        if "proximidade" in baixo:
            # O conjunto das duas âncoras é definido uma vez e reusado pelas expressões;
            # sem ele, a forma por conjuntos cita um conjunto que o derivado não define.
            blocos = _cercados(resto)
            if blocos:
                ancoras = {"rotulo": titulo, "formas": blocos}
            continue
        if "curadas" in baixo:
            curadas = consultas_curadas(resto)
            continue
        if "forma longa" in baixo:
            expressoes.update(_expressoes_em_negrito(resto))
            continue
    return expressoes, curadas, ancoras


def execucao_base(slug, expressoes, curadas):
    """O que se executa nesta base: uma, particionada em subconsultas ou curada."""
    if curadas:
        modo = "curada"
    elif slug == "eric":
        modo = "particionada"
    else:
        modo = "unica"
    if modo == "curada":
        itens = curadas
        expressao = "EB4"
    else:
        ex = expressoes["EB4"]
        expressao = "EB4"
        itens = [{"rotulo": b["rotulo"], "consulta": b["texto"]} for b in ex["blocos"]
                 if "nao e a forma executada" not in normaliza(b["rotulo"])]
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


def declaracao_base(t):
    """Idiomas, camadas, derivações e redução declarada — o que a string pode deixar de fora."""
    bloco = secao(t, SECOES_FICHA[2])
    idiomas, camadas, derivacoes, exclusoes = {}, "", "", []
    for linha in bloco.splitlines():
        if not linha.strip().startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 2:
            continue
        rot = normaliza(cels[0])
        if rot == "idiomas":
            for par in cels[1].split(";"):
                m = re.match(r"\s*(FCT\d)\s*:\s*(.+)$", par.strip())
                if not m:
                    raise ProtocoloInvalido(f"declaração de idiomas ilegível: {par!r}")
                idiomas[m.group(1)] = [x.strip() for x in m.group(2).split(",") if x.strip()]
        elif rot == "camadas":
            camadas = normaliza(cels[1])
        elif rot.startswith("derivacoes"):
            derivacoes = normaliza(cels[1])
    for linha in bloco.splitlines():
        if not linha.strip().startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) >= 3 and re.match(r"^FCT\d$", cels[0].strip()):
            exclusoes.append({"faceta": cels[0].strip(),
                              "termo": desescapa(cels[1]).strip(),
                              "motivo": desescapa(cels[2]).strip()})
    if not idiomas:
        raise ProtocoloInvalido("declaração de cobertura sem idiomas por faceta")
    if camadas not in ("todas", "nucleo"):
        raise ProtocoloInvalido(f"camadas {camadas!r} não é 'todas' nem 'nucleo'")
    for fid in idiomas:
        for i in idiomas[fid]:
            if i not in IDIOMAS:
                raise ProtocoloInvalido(f"declaração de {fid}: idioma {i!r} desconhecido")
    modos = [m.strip() for m in re.split(r"\s*(?:,|;| e )\s*", derivacoes) if m.strip()]
    for m in modos:
        if m not in MODOS_DERIVACAO:
            raise ProtocoloInvalido(f"derivação declarada desconhecida: {m!r}; "
                                    f"admitidas: {MODOS_DERIVACAO}")
    return {"idiomas": idiomas, "camadas": camadas, "derivacoes": modos,
            "exclusoes": exclusoes}


def base_derivada(slug, d, t_ficha=None):
    """O derivado de uma base. A forma vem da ficha; o vocabulário, do protocolo."""
    t = ficha(slug) if t_ficha is None else t_ficha
    nome = next((b["nome"] for b in d["fontes"]["bases"]
                 if b["id"] == FICHAS[slug]["bd"]), FICHAS[slug]["bd"])
    expressoes, curadas, ancoras = expressoes_base(t, slug)
    execucao = execucao_base(slug, expressoes, curadas)
    return {
        "base": {"id": FICHAS[slug]["bd"], "slug": slug, "nome": nome,
                 "ficha": FICHAS[slug]["arquivo"]},
        "facetas": facetas_base(t),
        "ancoras": ancoras,
        "expressoes": {k: expressoes[k] for k in sorted(expressoes)},
        "execucao": execucao,
        "filtros": filtros_base(execucao),
        "declaracao": declaracao_base(t),
    }


# ------------------------------------------------------------------ cobertura da base
COMPOSICAO = {
    "EB1": ["FCT1", "FCT2", "FCT3", "FCT4"],
    "EB2": ["FCT1", "FCT2", "FCT3"],
    "EB3": ["FCT1", "FCT2", "FCT4"],
    "EB4": ["FCT1", "FCT2", "FCT3", "FCT4"],
    "EB5": ["FCT1", "FCT2"],
}

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

    Não é lematização: é reconhecimento de flexão de número e de gênero sobre a forma
    já sem acento — plural em -s, -es, -ies, -ais, -eis e -coes —, que é o que as fichas
    declaram como desdobramento morfológico.
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
    radical = "radical" in set(decl.get("derivacoes") or [])
    saida = []
    for e in decl.get("exclusoes", []):
        if "radical" not in normaliza(e["motivo"]):
            continue
        achados = [x for s in base["facetas"] if s["faceta"] == e["faceta"] for x in s["termos"]]
        if not radical:
            saida.append((e, "a ficha não declara a derivação radical"))
        elif not any(_radical_alcanca(e["termo"], a) for a in achados):
            saida.append((e, "nenhum termo da string o contém"))
    return saida


def cobertura_base(slug, base, facetas_vocab):
    """Problemas de forma da base: vocabulário, âncoras, composição, execução."""
    problemas = []
    por_faceta = {f["id"]: f for f in facetas_vocab}
    decl = base.get("declaracao") or {}
    modos = set(decl.get("derivacoes") or [])

    for fid in sorted(por_faceta):
        f = por_faceta[fid]
        idiomas = decl.get("idiomas", {}).get(fid)
        if not idiomas:
            problemas.append(f"{fid}: a declaração de cobertura não declara idiomas")
            idiomas = list(IDIOMAS)
        camadas = CAMADAS if decl.get("camadas") == "todas" else ("nucleo",)
        tabela = [x for i in idiomas for c in camadas for x in f["camadas"][i][c]]
        esperados = _sem_repeticao(tabela)
        unidade = [s for s in base["facetas"] if s["faceta"] == fid]
        achados = [x for s in unidade for x in s["termos"]]
        excluidos = [e["termo"] for e in decl.get("exclusoes", []) if e["faceta"] == fid]
        for termo in esperados:
            if any(_mesmo_termo(termo, a) for a in achados):
                continue
            # A forma radical declara que uma palavra-raiz presente alcança a expressão
            # inteira. É declaração da ficha, não omissão silenciosa: a cobertura literal
            # continua sendo reportada, e o que a regra não alcança tem de estar na tabela.
            if "radical" in modos and any(_radical_alcanca(termo, a) for a in achados):
                continue
            if any(_mesmo_termo(termo, e) for e in excluidos):
                continue
            problemas.append(f"{fid}: {termo!r} está no protocolo, não está na string desta "
                             f"base e não consta da redução declarada")
        for termo in achados:
            # O termo retirado continua no quadro — é registro do vocabulário, e a
            # validação o mantém —, de modo que "deriva do protocolo" não basta: a string
            # da base não pode executá-lo, nem em flexão.
            retirado = next((r for r in RETIRADOS_V2.get(fid, ()) if _mesmo_termo(termo, r)),
                            None)
            if retirado:
                problemas.append(f"{fid}: {termo!r} está na string desta base e foi retirado "
                                 f"na emenda v2 ({retirado!r})")
                continue
            if any(_mesmo_termo(termo, p) for p in tabela):
                continue
            # Derivar por radical é ser raiz de um termo do protocolo: estar contido nele.
            if "radical" in modos and any(_radical_alcanca(p, termo) for p in tabela):
                continue
            problemas.append(f"{fid}: {termo!r} está na string desta base e não deriva do "
                             f"protocolo")
    for e, porque in _radical_sem_alcance(base):
        problemas.append(f"{e['faceta']}: {e['termo']!r} consta da redução como alcançado "
                         f"pela forma radical, e {porque}")

    if sorted(base["expressoes"]) != ["EB1", "EB2", "EB3", "EB4", "EB5"]:
        problemas.append(f"expressões fora de EB1 a EB5: {sorted(base['expressoes'])}")
    for ident, expr in sorted(base["expressoes"].items()):
        if ident not in COMPOSICAO:
            continue
        if expr["facetas"] != COMPOSICAO[ident]:
            problemas.append(f"{ident}: facetas {expr['facetas']} não são "
                             f"{COMPOSICAO[ident]} do protocolo")
        if not {"FCT1", "FCT2"} <= set(expr["facetas"]):
            problemas.append(f"{ident}: falta âncora obrigatória (FCT1 ou FCT2)")
        # Expressão derivada e não materializada nesta base — a sonda da ERIC — não
        # precisa de forma: o que se executa ou se confere tem de ter.
        precisa_forma = expr["estatuto"] in ("executada", "fidelidade", "sonda")
        if precisa_forma and not expr["blocos"]:
            problemas.append(f"{ident}: expressão sem forma legível nesta base")

    execucao = base["execucao"]
    if execucao["expressao"] != "EB4":
        problemas.append(f"a base executa {execucao['expressao']}, esperado EB4")
    if execucao["modo"] not in ("unica", "particionada", "curada"):
        problemas.append(f"modo de execução desconhecido: {execucao['modo']!r}")
    if not execucao["itens"]:
        problemas.append("execução sem consulta legível")
    return problemas


def cobertura_por_faceta(slug, base, facetas_vocab):
    """Números de cobertura por faceta. É medida, não aprovação.

    Separa o que está literalmente na string do que só é alcançado pela forma radical
    declarada: a diferença é o preço de recall que a base assume.
    """
    por_faceta = {f["id"]: f for f in facetas_vocab}
    decl = base.get("declaracao") or {}
    modos = set(decl.get("derivacoes") or [])
    saida = {}
    for fid in sorted(por_faceta):
        idiomas = decl.get("idiomas", {}).get(fid) or list(IDIOMAS)
        camadas = CAMADAS if decl.get("camadas") == "todas" else ("nucleo",)
        tabela = _sem_repeticao([x for i in idiomas for c in camadas
                                 for x in por_faceta[fid]["camadas"][i][c]])
        achados = [x for s in base["facetas"] if s["faceta"] == fid for x in s["termos"]]
        excluidos = [e["termo"] for e in decl.get("exclusoes", []) if e["faceta"] == fid]
        cobertos = sum(1 for t in tabela if any(_mesmo_termo(t, a) for a in achados))
        por_radical = sum(1 for t in tabela
                          if not any(_mesmo_termo(t, a) for a in achados)
                          and "radical" in modos
                          and any(_radical_alcanca(t, a) for a in achados))
        declarados = sum(1 for t in tabela
                         if not any(_mesmo_termo(t, a) for a in achados)
                         and not ("radical" in modos
                                  and any(_radical_alcanca(t, a) for a in achados))
                         and any(_mesmo_termo(t, e) for e in excluidos))
        saida[fid] = {"esperados": len(tabela), "na_string": len(achados),
                      "cobertos": cobertos, "por_radical": por_radical,
                      "declarados": declarados,
                      "descobertos": len(tabela) - cobertos - por_radical - declarados}
    return saida


# -------------------------------------------------------------------------- análise
def analisa(t=None):
    t = texto() if t is None else t
    pal = palavras(t)
    tb = tabelas(t)
    st = strings(t)
    for n in st:
        # A string repete termo entre camadas; a lista executada é deduplicada. É ela
        # que a derivação local usa, e é ela que o relatório conta.
        st[n]["termos"] = _sem_repeticao(st[n]["termos"])
    comp, exec_, sonda = expressoes(t)
    crit = criterios(t)
    est = sementes(t)
    return {
        "questoes": questoes(t),
        "facetas": pal,
        "tabelas": tb,
        "strings": st,
        "expressoes": comp,
        "executada": exec_,
        "sonda": sonda,
        "criterios": crit,
        "recorte": recorte(t),
        "fontes": fontes(t),
        "limiar": limiar(t),
        "sementes": est,
        "distribuicao": distribuicao(t, est),
    }


# ---------------------------------------------------------------------- conferência
def conferir(t=None):
    """Problemas encontrados. Lista vazia = documento na forma esperada."""
    t = texto() if t is None else t
    problemas = []
    try:
        d = analisa(t)
    except ProtocoloInvalido as e:
        return [str(e)]

    for f in d["tabelas"]:
        for i in IDIOMAS:
            for c in CAMADAS:
                if not f["camadas"][i][c]:
                    problemas.append(f"faceta {f['id']}: camada {c} vazia em {i}")
        # Repetição entre camadas é legítima e existe no documento (o mesmo termo
        # aparece em núcleo e em relacionados); a lista final é deduplicada. Dentro
        # da mesma camada, é defeito.
        for i in IDIOMAS:
            for c in CAMADAS:
                vistos = set()
                for termo in f["camadas"][i][c]:
                    k = normaliza(termo)
                    if k in vistos:
                        problemas.append(
                            f"faceta {f['id']} {i}/{c}: {termo!r} repetido na mesma camada")
                    vistos.add(k)

    for f in d["facetas"]:
        if not f["cor"]:
            problemas.append(f"faceta {f['id']}: cor não declarada")
    ancoras = sorted(f["id"] for f in d["facetas"] if f["ancora"])
    if ancoras != ["FCT1", "FCT2"]:
        problemas.append(f"âncoras deveriam ser FCT1 e FCT2, são {ancoras}")

    # A string só pode usar termo que a tabela do controle terminológico contém.
    # É a remissão que impede string e vocabulário de divergirem em silêncio.
    tabelados = {normaliza(x) for f in d["tabelas"]
                 for i in IDIOMAS for x in f["termos"][i]}
    for n, s in d["strings"].items():
        if len(s["termos"]) < 20:
            problemas.append(f"faceta {n}: string com menos de {len(s['termos'])} termos "
                             f"(mínimo 20)")
        for termo in s["termos"]:
            if normaliza(termo) not in tabelados:
                problemas.append(f"faceta {n}: termo {termo!r} da string não consta da tabela")

    comp, exec_, sonda = d["expressoes"], d["executada"], d["sonda"]
    previsto = {
        "EB1": [["STR1"], ["STR2"], ["STR3"], ["STR4"]],
        "EB2": [["STR1"], ["STR2"], ["STR3"]],
        "EB3": [["STR1"], ["STR2"], ["STR4"]],
        "EB4": [["STR1"], ["STR2"], ["STR3", "STR4"]],
        "EB5": [["STR1"], ["STR2"]],
    }
    if comp != previsto:
        problemas.append(f"composição das expressões fora do previsto: {comp}")
    if exec_ != "EB4":
        problemas.append(f"a expressão executada deveria ser EB4, é {exec_}")
    if sonda != "EB5":
        problemas.append(f"a sonda de sensibilidade deveria ser EB5, é {sonda}")
    # EB4 = EB2 ∪ EB3: mesmas duas primeiras facetas, e a terceira é a união das que
    # distinguem as duas específicas. EB5 = STR1 + STR2 contém EB4.
    if comp.get("EB2", [])[:2] != comp.get("EB3", [])[:2] or \
            comp.get("EB2", [])[:2] != comp.get("EB4", [])[:2]:
        problemas.append("EB2, EB3 e EB4 não partilham as duas primeiras facetas")
    else:
        uniao = sorted(set(comp["EB2"][2]) | set(comp["EB3"][2]))
        if comp.get("EB4", [])[2:] != [uniao]:
            problemas.append(f"EB4 não é EB2 ∪ EB3: terceiro grupo {comp.get('EB4')} "
                             f"não é {uniao}")
    if comp.get("EB5") != comp.get("EB4", [])[:2]:
        problemas.append("EB5 não é a conjunção das duas âncoras (STR1 + STR2)")

    dimensoes = {c["dimensao"] for c in d["criterios"]}
    for esperada in ("Intervalo temporal", "Idioma(s)", "Tipo documental",
                     "Localização de itens", "Adequação temática",
                     "Domínio de aplicação", "Outros critérios"):
        if esperada not in dimensoes:
            problemas.append(f"critério de {esperada!r} não declarado")
    if d["recorte"]["ano_min"] != 2017:
        problemas.append(f"recorte inicia em {d['recorte']['ano_min']}, esperado 2017")
    if abs(d["limiar"] - 0.80) > 1e-9:
        problemas.append(f"limiar é {d['limiar']:.0%}, esperado 80%")

    if d["fontes"]["ordem_execucao"] != [b["nome"] for b in d["fontes"]["bases"]]:
        problemas.append(f"ordem de execução fora do previsto: {d['fontes']['ordem_execucao']}")

    if not d["questoes"]["questao_principal"]:
        problemas.append("questão geral vazia")
    if len(d["questoes"]["questoes_especificas"]) != 4:
        problemas.append("questões específicas não são quatro")

    if len(d["sementes"]) < 8:
        problemas.append(f"{len(d['sementes'])} sementes; a faixa do protocolo é 8 a 10")
    for e in d["sementes"]:
        if not e["titulo"] or len(e["titulo"]) < 12:
            problemas.append(f"semente {e['id']}: título não legível ({e['titulo']!r})")
        if not e["bases"]:
            problemas.append(f"semente {e['id']}: sem base esperada no mapa")

    dist = d["distribuicao"]
    dec = dist["declarado"]
    for b, v in dec["por_base"].items():
        if dist["por_base"].get(b) != v:
            problemas.append(
                f"distribuição em {b}: prosa diz {v}, mapa soma {dist['por_base'].get(b)}")
    for campo, rotulo in (("incidencias", "incidências"), ("registros", "registros únicos"),
                          ("em_mais_de_uma_base", "estudos em mais de uma base"),
                          ("em_uma_so", "estudos em uma só base")):
        if dec[campo] is not None and dist[campo] != dec[campo]:
            problemas.append(f"{rotulo}: prosa diz {dec[campo]}, mapa dá {dist[campo]}")

    # Emenda v2: o que foi retirado não pode voltar à string, e o composto acrescentado
    # não pode sumir. O teste é por faceta, porque o mesmo conceito pode ter saído de uma
    # e permanecido em outra.
    norm = {fid: {normaliza(x) for x in s["termos"]} for fid, s in d["strings"].items()}
    # A lista de retirados só protege se nomear a forma que o quadro registra: grafia que
    # não está no quadro não casa com nada e deixa a forma verdadeira passar em silêncio.
    quadro = {f["id"]: {normaliza(x) for c in f["camadas"].values() for ts in c.values()
                        for x in ts} for f in d["tabelas"]}
    for fid, retirados in RETIRADOS_V2.items():
        for termo in retirados:
            if normaliza(termo) not in quadro.get(fid, set()):
                problemas.append(f"emenda v2: {termo!r}, retirado de {fid}, não consta do "
                                 f"quadro terminológico dessa faceta")
    for fid, retirados in RETIRADOS_V2.items():
        for termo in retirados:
            if normaliza(termo) in norm[fid]:
                problemas.append(f"emenda v2 violada: {termo!r} voltou à string de {fid}")
    for fid, acrescentados in ACRESCENTADOS_V2.items():
        for termo in acrescentados:
            if normaliza(termo) not in norm[fid]:
                problemas.append(f"emenda v2 violada: {termo!r} sumiu da string de {fid}")

    return problemas


def _composicao_legivel(grupos):
    """`[["STR1"],["STR2"],["STR3","STR4"]]` como `1+2+(3|4)`."""
    partes = []
    for g in grupos:
        nomes = [x[3:] for x in g]
        partes.append(nomes[0] if len(nomes) == 1 else "(" + "|".join(nomes) + ")")
    return "+".join(partes)


def relatorio(d):
    L = []
    L.append(f"  questão: 1 geral, {len(d['questoes']['questoes_especificas'])} específicas")
    for f in d["tabelas"]:
        n_string = len(d["strings"][f["id"]]["termos"])
        n_bruto = sum(len(f["termos"][i]) for i in IDIOMAS)
        L.append(f"  faceta {f['id']} — {f['nome'][:52]:<54} "
                 f"tabela {n_bruto:>3} formas / string {n_string:>3} termos   "
                 f"instrumento: {f['instrumentos'][:36]}")
    crit = d["criterios"]
    L.append(f"  critérios: {len(crit)} ({sum(1 for c in crit if c['acao']=='Incluir')} incluir, "
             f"{sum(1 for c in crit if c['acao']=='Excluir')} excluir)")
    L.append(f"  fontes: {len(d['fontes']['bases'])} bases, ordem "
             f"{d['fontes']['ordem_execucao']}; {len(d['fontes']['ferramenta_gestao'])} "
             f"itens de ferramenta")
    dist = d["distribuicao"]
    L.append(f"  sementes: {len(d['sementes'])}  "
             f"incidências: {dist['incidencias']}  "
             f"por base: " + ", ".join(f"{b} {v}" for b, v in dist["por_base"].items()))
    L.append(f"  expressões: " + ", ".join(
        f"{n}=" + _composicao_legivel(c)
        for n, c in sorted(d["expressoes"].items())) +
        f"   executada: {d['executada']}   sonda: {d['sonda']}")
    recorte = (f"{d['recorte']['ano_min']} a {d['recorte']['ano_max']}"
               if d["recorte"]["ano_max"]
               else f"{d['recorte']['ano_min']} até a data de execução")
    L.append(f"  recorte: {recorte}   limiar: {d['limiar']:.0%}")
    return "\n".join(L)


def relatorio_bases(bases, d):
    """Uma linha por base. Cobertura é número, não aprovação: mede o preço de cada forma."""
    L = ["", "  Bases — forma lida da ficha; cobertura medida contra o vocabulário declarado:"]
    for slug, base in bases:
        cob = cobertura_por_faceta(slug, base, d["tabelas"])
        total_e = sum(v["esperados"] for v in cob.values())
        total_c = sum(v["cobertos"] for v in cob.values())
        total_r = sum(v["por_radical"] for v in cob.values())
        total_d = sum(v["declarados"] for v in cob.values())
        total_x = sum(v["descobertos"] for v in cob.values())
        strings = " ".join(s["id"] for s in base["facetas"])
        decl = base["declaracao"]
        ressalva = f" +{total_r} radical +{total_d} declarados" if (total_r or total_d) else ""
        if total_x:
            ressalva += f" · {total_x} DESCOBERTOS"
        L.append(f"  {base['base']['id']} {slug:<8} {base['base']['nome'][:34]:<36} "
                 f"execução: {base['execucao']['modo']:<12} "
                 f"literal {total_c}/{total_e}{ressalva}")
        L.append(f"      strings: {strings}   camadas: {decl['camadas']}   "
                 f"idiomas: " + ", ".join(f"{k[3:]}:{'/'.join(v)}"
                                          for k, v in sorted(decl["idiomas"].items())))
        L.append("      " + "  ".join(
            f"{k} {v['cobertos']}/{v['esperados']}" for k, v in sorted(cob.items())))
    return "\n".join(L)


# ------------------------------------------------------------ arquivos alimentados
# Nada aqui é derivado de markdown. São arquivos que se alimentam: o estatuto de cada
# termo, os metadados de cada semente, o registro documental e o rastro das execuções.
# O que o protocolo já diz não se copia para JSON — lê-se do documento.

def _le_json(caminho):
    """Carrega um JSON alimentado. Devolve (dado, erro); erro None quando legível."""
    caminho = pathlib.Path(caminho)
    if not caminho.exists():
        return None, f"{caminho.relative_to(RAIZ)} ausente"
    try:
        return json.loads(caminho.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"{caminho.relative_to(RAIZ)} ilegível: {e}"


def _chave_semente(e):
    """Ligação com o protocolo: DOI quando houver; senão, título normalizado."""
    doi = (e.get("doi") or "").strip().lower()
    return ("doi:" + doi) if doi else ("ti:" + normaliza(e.get("titulo", ""))[:120])


def ligacao_semente(e):
    """Ligação pública de uma semente: DOI quando houver; senão, título normalizado.

    É a chave que `--sincronizar` usa e que os consumidores devem usar: o `id` é rótulo,
    não identidade, e pode mudar sem que o metadado autoral se perca.
    """
    return _chave_semente(e)


def _indice_sementes(dado):
    return {e.get("id"): e for e in (dado or {}).get("estudos", []) if e.get("id")}


def _problemas_sementes(dado, d):
    problemas, avisos = [], []
    if not isinstance(dado, dict) or "estudos" not in dado:
        return ["sementes.json sem a chave `estudos`"], []
    idx = _indice_sementes(dado)
    protocolo = {e["id"]: e for e in d["sementes"]}
    for ident, e in protocolo.items():
        meta = idx.get(ident)
        if meta is None:
            problemas.append(f"sementes: {ident} ({_chave_semente(e)}) sem metadados")
            continue
        if meta.get("ligacao") and meta["ligacao"] != _chave_semente(e):
            avisos.append(f"sementes: {ident} tem ligação {meta['ligacao']!r} e o protocolo "
                          f"{_chave_semente(e)!r} — conferir")
        for campo in CAMPOS_AUTORAIS:
            if campo not in meta:
                problemas.append(f"sementes: {ident} sem o campo {campo!r}")
    for ident, meta in idx.items():
        if ident not in protocolo:
            avisos.append(f"sementes: {ident} fora do protocolo, metadados preservados — "
                          f"decidir")
    return problemas, avisos


def _problemas_registro(dado):
    """Confere o registro documental e as execuções que declaram arquivo exportado."""
    if not isinstance(dado, dict):
        return ["registro_execucao.json não é um objeto"]
    bases = dado.get("bases")
    if not isinstance(bases, dict):
        return ["registro_execucao.json sem a chave `bases`"]
    faltam = [b for b in ("BD1", "BD2", "BD3", "BD4") if b not in bases]
    if faltam:
        return [f"registro_execucao.json sem as bases {faltam}"]

    problemas = []
    for bd in ("BD1", "BD2", "BD3", "BD4"):
        base = bases[bd]
        execucoes = base.get("execucoes")
        if not isinstance(execucoes, list):
            problemas.append(f"registro_execucao.json: {bd} sem a lista `execucoes`")
            continue
        ids = [e.get("id") for e in execucoes if isinstance(e, dict)]
        repetidos = sorted({x for x in ids if ids.count(x) > 1})
        if repetidos:
            problemas.append(f"registro_execucao.json: {bd} com execuções repetidas "
                             f"{repetidos}")
        for e in execucoes:
            if not isinstance(e, dict):
                problemas.append(f"registro_execucao.json: {bd} com execução que não é objeto")
                continue
            arq = str(e.get("arquivo") or "").strip()
            if not arq:
                continue
            caminho = pathlib.Path(arq)
            if not caminho.is_absolute():
                caminho = RAIZ / caminho
            if not caminho.exists():
                problemas.append(f"registro_execucao.json: {bd}/{e.get('id')} aponta arquivo "
                                 f"ausente {arq!r}")
            if not isinstance(e.get("registros_lidos"), int):
                problemas.append(f"registro_execucao.json: {bd}/{e.get('id')} declara arquivo "
                                 f"sem `registros_lidos` inteiro")
            status = e.get("status")
            if status and status not in ("valida", "divergente_justificada"):
                problemas.append(f"registro_execucao.json: {bd}/{e.get('id')} com status "
                                 f"{status!r} desconhecido")
    return problemas


def _problemas_bases(d):
    problemas = []
    for slug in FICHAS:
        try:
            base = base_derivada(slug, d)
            problemas += [f"{slug}: {p}" for p in cobertura_base(slug, base, d["tabelas"])]
        except ProtocoloInvalido as e:
            problemas.append(f"{slug}: {e}")
    return problemas


def conferir_dados():
    """Confere os arquivos alimentados contra o documento. Devolve (problemas, avisos)."""
    problemas, avisos = [], []
    try:
        d = analisa()
    except ProtocoloInvalido as e:
        return [f"documento ilegível: {e}"], []

    dado, erro = _le_json(SEMENTES)
    if erro:
        problemas.append(erro + " — rode  --sincronizar")
    else:
        p, a = _problemas_sementes(dado, d)
        problemas += p
        avisos += a

    dado, erro = _le_json(REGISTRO)
    if erro:
        problemas.append(erro)
    else:
        problemas += _problemas_registro(dado)

    problemas += _problemas_bases(d)
    return problemas, avisos


# ------------------------------------------------------------------- sincronização
def _sincroniza_sementes(d, existente):
    """Casa por DOI ou título, com o id como último recurso; preserva o conferido."""
    antigos = (existente or {}).get("estudos", [])
    por_ligacao = {}
    for e in antigos:
        por_ligacao.setdefault(e.get("ligacao"), []).append(e)
    usados, estudos, novos, religados = set(), [], [], []
    for e in d["sementes"]:
        ligacao = _chave_semente(e)
        escolhido = None
        for cand in por_ligacao.get(ligacao, []):
            if id(cand) not in usados:
                escolhido = cand
                break
        if escolhido is None:
            for cand in antigos:
                if id(cand) in usados or cand.get("id") != e["id"]:
                    continue
                escolhido = cand
                religados.append(f"{e['id']}: ligação atualizada de "
                                 f"{cand.get('ligacao')!r} para {ligacao!r}")
                break
        if escolhido is None:
            meta = {"id": e["id"], "ligacao": ligacao}
            meta.update({campo: "" for campo in CAMPOS_AUTORAIS})
            novos.append(e["id"])
            estudos.append(meta)
            continue
        usados.add(id(escolhido))
        meta = {"id": e["id"], "ligacao": ligacao}
        for campo in CAMPOS_AUTORAIS:
            meta[campo] = escolhido.get(campo, "")
        estudos.append(meta)
    orfaos = [x for x in antigos if id(x) not in usados]
    return ({"_leia": LEIA["sementes"], "versao": 2, "estudos": estudos},
            novos, religados, orfaos)


def _escreve(caminho, dado):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")


def sincronizar(t=None):
    """Reconcilia `sementes.json` com o protocolo. Não cria nem grava derivado."""
    t = texto() if t is None else t
    problemas = conferir(t)
    if problemas:
        print("Documento fora da forma esperada; nada foi sincronizado:")
        for p in problemas:
            print("  -", p)
        return 1
    d = analisa(t)

    sem, erro = _le_json(SEMENTES)
    if erro and "ausente" not in erro:
        print(erro)
        return 1
    dados_s, novos_s, religados, orfaos = _sincroniza_sementes(d, sem or {})

    atual, _ = _le_json(SEMENTES)
    if atual == dados_s:
        print("  sementes.json: sem mudança")
        mudou = False
    else:
        _escreve(SEMENTES, dados_s)
        print("  sementes.json: gravado")
        mudou = True

    if novos_s:
        print(f"\n  semente(s) acrescentada(s): {', '.join(novos_s)}")
    if religados:
        print("\n  ligação de semente refeita:")
        for x in religados:
            print("    ~", x)
    if orfaos:
        print(f"\n  semente(s) fora do protocolo, metadados preservados: "
              f"{', '.join(x.get('id', '?') for x in orfaos)}")
    if not mudou:
        print("\nNada a gravar: o metadado das sementes já reflete o protocolo.")
    return 0


# ---------------------------------------------------------------------- pendências
CAMPOS_PENDENTES = (("verificacao", "verificação"), ("escopo", "escopo"),
                    ("tipo", "tipo"), ("alinhamento", "alinhamento"))


def pendencias_relatorio():
    """Relata o que está aberto, sem escrever arquivo algum."""
    linhas = []
    try:
        d = analisa()
    except ProtocoloInvalido as e:
        print(f"Documento ilegível: {e}")
        return 1

    for caminho, acao in ((SEMENTES, "rode --sincronizar"),
                          (REGISTRO, "reconstitua o registro a partir das fichas e do que a "
                                     "base exibiu")):
        if not caminho.exists():
            linhas.append(f"[ausente] {caminho.relative_to(RAIZ)} — {acao}")

    s, erro = _le_json(SEMENTES)
    if erro is None:
        protocolo = {e["id"]: e for e in d["sementes"]}
        for ident, meta in _indice_sementes(s).items():
            if ident not in protocolo:
                linhas.append(f"[semente fora do protocolo] {ident} — decidir: remover com "
                              f"registro ou reincluir no protocolo")
                continue
            vazios = []
            for campo, rotulo in CAMPOS_PENDENTES:
                v = str(meta.get(campo) or "")
                if not v or v.startswith(("A CONFERIR", "a conferir")) or "PENDÊNCIA" in v:
                    vazios.append(rotulo)
            if vazios:
                chave = protocolo[ident]["chave"]
                linhas.append(f"[semente {ident} {chave}] pendente: {', '.join(vazios)}")
        faltam = [e["id"] for e in d["sementes"] if e["id"] not in _indice_sementes(s)]
        if faltam:
            linhas.append(f"[sementes] {len(faltam)} sem metadados: {', '.join(faltam)} — "
                          f"rodar --sincronizar")

    registro, erro = _le_json(REGISTRO)
    if erro is not None:
        linhas.append(erro)
    else:
        bases = registro.get("bases") or {}
        com_arquivo = 0
        for bd in ("BD1", "BD2", "BD3", "BD4"):
            base = bases.get(bd) or {}
            nome = base.get("base") or bd
            for p in base.get("pendencias") or []:
                linhas.append(f"[{bd} {nome}] {p}")
            for e in base.get("execucoes") or []:
                if not isinstance(e, dict):
                    continue
                if e.get("arquivo"):
                    com_arquivo += 1
                    if e.get("status") not in ("valida", "divergente_justificada"):
                        linhas.append(
                            f"[{bd} {e.get('id')}] execução registrada com status "
                            f"{e.get('status')!r} — reconferir ou reregistrar")
        if not com_arquivo:
            linhas.append("[registro] nenhuma execução com exportação registrada — use "
                          "src/derivar_expressoes.py --registrar")

    if not CSV_VALIDACAO.exists():
        linhas.append(f"[validação] {CSV_VALIDACAO.relative_to(RAIZ)} ausente — rode "
                      f"src/validar_termos.py --exportar")
    else:
        with CSV_VALIDACAO.open(encoding="utf-8-sig", newline="") as fh:
            linhas_validacao = list(csv.DictReader(fh, delimiter=";"))
        sem_status = sum(1 for r in linhas_validacao
                         if not (r.get("status_proposto") or "").strip())
        if sem_status:
            linhas.append(f"[validação] {sem_status} linha(s) sem `status_proposto` — rode "
                          f"src/validar_termos.py --validar")

    # Lacuna que a própria ficha declara e deixa em aberto. A decisão é do pesquisador:
    # acrescentar o termo à string, com nova execução e novo teste de aderência, ou manter
    # a perda e declará-la no relatório.
    for slug in FICHAS:
        try:
            b = base_derivada(slug, d)
        except ProtocoloInvalido as e:
            linhas.append(f"[{slug}] ficha ilegível: {e}")
            continue
        pendentes = [e for e in b["declaracao"]["exclusoes"]
                     if "pendente" in normaliza(e["motivo"])]
        if pendentes:
            linhas.append(
                f"[{b['base']['nome']}] {len(pendentes)} termo(s) declarado(s) como lacuna, "
                f"com decisão pendente: " +
                ", ".join(f"{e['termo']} ({e['faceta']})" for e in pendentes[:6]))
    if not linhas:
        print("Nenhuma pendência detectada nos artefatos de data/.")
    else:
        print(f"{len(linhas)} pendência(s) detectada(s) — relato, nada foi escrito:\n")
        for l in linhas:
            print("  " + l)
    return 0


# ------------------------------------------------------------------------ autoteste
def _mutacoes(t):
    """Cópias defeituosas: cada uma tem de ser reprovada por `conferir`."""
    linhas = t.splitlines()
    i_rel = next(i for i, l in enumerate(linhas)
                 if l.startswith("| *Termos relacionados") and "modelo conceitual" in l)
    sem_linha = linhas[:i_rel] + linhas[i_rel + 1:]

    i_str = next(i for i, l in enumerate(linhas) if l.startswith("| STR2 |"))
    string_quebrada = list(linhas)
    string_quebrada[i_str] = string_quebrada[i_str].replace(" OR ", ", ", 1)

    sem_semente = [l for l in linhas if not l.startswith("- SE10:")]

    dist_errada = [l.replace("Scopus, 6;", "Scopus, 7;", 1) for l in linhas]

    i_nuc = next(i for i, l in enumerate(linhas) if l.startswith("| *Termos centrais")
                 and "representação do conhecimento" in l)
    duplicada = list(linhas)
    duplicada[i_nuc] = duplicada[i_nuc].replace(
        "\\- representação do conhecimento \\- organização do conhecimento",
        "\\- representação do conhecimento \\- representação do conhecimento "
        "\\- organização do conhecimento", 1)

    sem_geral = [l for l in linhas if l.strip() != "### Questão geral de revisão"]
    sem_qs4 = [l for l in linhas if not l.startswith("- QER4:")]
    sem_idioma = [l for l in linhas if "| **Idioma(s)** |" not in l]
    sem_brapci = [l for l in linhas if not l.startswith("| BD4 |")]

    # Defeitos que só os identificadores novos denunciam.
    sem_qgr = [l.replace("- QGR:", "", 1) for l in linhas]
    faceta_trocada = [l.replace("Faceta 2 (FCT2)", "Faceta 2 (FCT3)", 1) for l in linhas]
    str_trocada = [l.replace("| STR2 | FCT2", "| STR2 | FCT3", 1) for l in linhas]
    criterio_repetido = [l.replace("| CE3 |", "| CE2 |", 1) for l in linhas]
    base_repetida = [l.replace("| BD3 |", "| BD2 |", 1) for l in linhas]
    semente_fora_de_ordem = [l.replace("- SE10:", "- SE11:", 1) for l in linhas]
    comp_trocada = [l.replace("STR3", "STR4", 1) if l.startswith("| EB2 |") else l
                    for l in linhas]

    return {
        "linha de faceta removida": "\n".join(sem_linha),
        "string fora do padrão OR": "\n".join(string_quebrada),
        "semente ausente": "\n".join(sem_semente),
        "distribuição contradita": "\n".join(dist_errada),
        "termo duplicado na faceta": "\n".join(duplicada),
        "questão geral removida": "\n".join(sem_geral),
        "QER4 removida": "\n".join(sem_qs4),
        "critério de idioma removido": "\n".join(sem_idioma),
        "base BRAPCI removida": "\n".join(sem_brapci),
        "questão geral sem QGR": "\n".join(sem_qgr),
        "faceta com identificador trocado": "\n".join(faceta_trocada),
        "string apontando para outra faceta": "\n".join(str_trocada),
        "critério com identificador repetido": "\n".join(criterio_repetido),
        "base com identificador repetido": "\n".join(base_repetida),
        "semente fora de numeração": "\n".join(semente_fora_de_ordem),
        "expressão com composição trocada": "\n".join(comp_trocada),
    }


def _autoteste_dados(d):
    """Prova que a conferência dos arquivos alimentados reprova cada defeito esperado."""
    sem, erro_s = _le_json(SEMENTES)
    reg, erro_r = _le_json(REGISTRO)
    if erro_s or erro_r:
        print("  [--] arquivos alimentados ausentes: o teste das conferências não foi "
              "executado")
        return 0
    falhas = 0

    def testa(nome, condicao):
        nonlocal falhas
        if condicao:
            print(f"  [ok] reprovou: {nome}")
        else:
            print(f"  [FALHA] aprovou indevidamente: {nome}")
            falhas += 1

    base_ps, _ = _problemas_sementes(sem, d)
    base_pr = _problemas_registro(reg)
    if base_ps or base_pr:
        print(f"  [FALHA] o arquivo corrente já está reprovado: "
              f"{(base_ps or base_pr)[0]}")
        falhas += 1

    copia = copy.deepcopy(sem)
    copia["estudos"] = copia["estudos"][1:]
    p, _ = _problemas_sementes(copia, d)
    testa("semente do protocolo sem metadados", bool(p))

    copia = copy.deepcopy(sem)
    copia["estudos"][0].pop("verificacao", None)
    p, _ = _problemas_sementes(copia, d)
    testa("semente sem campo de conferência", bool(p))

    copia = copy.deepcopy(sem)
    copia["estudos"].append({"id": "SE99", "ligacao": "ti:semente inventada",
                             **{c: "" for c in CAMPOS_AUTORAIS}})
    _, a = _problemas_sementes(copia, d)
    testa("semente fora do protocolo com metadados preservados", bool(a))

    copia = copy.deepcopy(reg)
    del copia["bases"]["BD1"]
    testa("registro sem uma das quatro bases", bool(_problemas_registro(copia)))

    copia = copy.deepcopy(reg)
    copia["bases"]["BD1"]["execucoes"].append({
        "id": "EX99", "expressao": "EB4", "arquivo": "data/execucoes/ausente.ris",
        "registros_lidos": 1, "status": "valida"})
    testa("execução apontando arquivo de exportação ausente",
          bool(_problemas_registro(copia)))

    copia = copy.deepcopy(reg)
    copia["bases"]["BD1"]["execucoes"].append({
        "id": "EX99", "expressao": "EB4", "arquivo": "data/registro_execucao.json",
        "registros_lidos": "um", "status": "valida"})
    testa("execução com `registros_lidos` que não é inteiro",
          bool(_problemas_registro(copia)))
    return falhas


def _autoteste_bases(d):
    """Prova que a cobertura da base reprova ficha divergente do protocolo.

    Cada defeito é injetado numa cópia do texto da ficha e a conferência tem de recusá-lo.
    Defeito que a conferência não pega é defeito que passa em silêncio na fonte.
    """
    falhas, n = 0, 0
    slug = "wos"
    original = ficha(slug)

    def problemas_de(s, t_ficha):
        try:
            base = base_derivada(s, d, t_ficha)
            return cobertura_base(s, base, d["tabelas"])
        except ProtocoloInvalido as e:
            return [str(e)]

    def testa(nome, t_ficha, s=None, base_texto=None, espera=None):
        nonlocal falhas, n
        n += 1
        if base_texto is not None and t_ficha == base_texto:
            # Mutação que não se aplicou não prova nada: a ficha mudou e o teste tem de mudar.
            print(f"  [FALHA] mutação não aplicada: {nome}")
            falhas += 1
            return
        problemas = problemas_de(s or slug, t_ficha)
        if espera is not None:
            # Reprovar por outro motivo não prova a conferência que o caso exercita.
            problemas = [p for p in problemas if espera in p]
        if problemas:
            print(f"  [ok] reprovou: {nome} — {problemas[0][:88]}")
        else:
            print(f"  [FALHA] aprovou indevidamente: {nome}")
            falhas += 1

    testa("termo do protocolo retirado da string da base",
          original.replace('TS=("representação do conhecimento" OR ', 'TS=(', 1))
    testa("termo inventado acrescentado à string da base",
          original.replace('TS=("representação do conhecimento" OR ',
                           'TS=("invented search term" OR "representação do conhecimento" OR ',
                           1))
    # O termo retirado permanece no quadro; a conferência antiga o aceitava na string da
    # base por derivar do quadro, e foi assim que a BRAPCI executou `educativo` depois da v2.
    testa("termo retirado na emenda v2 devolvido à string da base",
          original.replace('TS=("representação do conhecimento" OR ',
                           'TS=("modelo conceitual" OR "representação do conhecimento" OR ', 1),
          espera="retirado na emenda v2")
    brapci = ficha("brapci")
    testa("termo retirado na emenda v2, em flexão, na string da BRAPCI",
          brapci.replace('("educação" OR ', '("educação" OR "educativos" OR ', 1),
          "brapci", brapci, "retirado na emenda v2")
    testa("expressão com faceta trocada",
          original.replace("**Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧)",
                           "**Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥)", 1))
    testa("declaração de cobertura restringindo as camadas",
          original.replace("| camadas | todas |", "| camadas | nucleo |", 1))

    # Forma radical, na ficha que a declara. O controle é a ficha corrente com toda linha
    # falsamente declarada como radical reetiquetada como redução: tem de passar, ou os
    # defeitos injetados sobre ele não provam nada.
    eric = ficha("eric")
    controle = eric
    for e, _ in _radical_sem_alcance(base_derivada("eric", d, eric)):
        controle = re.sub(r"^(\|\s*" + re.escape(e["faceta"]) + r"\s*\|\s*"
                          + re.escape(e["termo"]) + r"\s*\|)[^\n]*$",
                          r"\1 redução desta base (controle do autoteste) |",
                          controle, count=1, flags=re.M)
    n += 1
    restantes = problemas_de("eric", controle)
    if restantes:
        print(f"  [FALHA] controle da forma radical reprovado: {restantes[0][:80]}")
        falhas += 1
    else:
        print("  [ok] controle da forma radical aprovado")

    # Frase que partilha uma palavra com outra não a alcança: `"faceted classification"`
    # não alcança `faceted taxonomy`. O leitor antigo aprovava esta linha.
    m1 = controle.replace(' OR title:"faceted taxonomy"', "", 1)
    m1 = re.sub(r"^(\| FCT1 \|)", "| FCT1 | faceted taxonomy | alcançado pela forma radical "
                "declarada |\n\\1", m1, count=1, flags=re.M) if m1 != controle else m1
    testa("redução declarada como radical sem termo da string que a alcance", m1,
          "eric", controle, "consta da redução como alcançado")
    # Termo da string que só partilha uma palavra com o protocolo não deriva dele.
    testa("termo inventado que partilha uma palavra com o protocolo",
          controle.replace('title:"domain model"', 'title:"domain model" OR '
                           'title:"ontology mapping"', 1), "eric", controle,
          "'ontology mapping' está na string")
    # Motivo radical em ficha que não declara a derivação radical.
    testa("motivo radical sem derivação radical declarada",
          controle.replace("| derivações | morfologia e radical |",
                           "| derivações | morfologia |", 1), "eric", controle,
          "não declara a derivação radical")
    return falhas, n


def autoteste(t=None):
    t = texto() if t is None else t
    if conferir(t):
        print("O documento corrente já está reprovado; o autoteste não teria o que provar.")
        return 1
    falhas = 0
    mut = _mutacoes(t)
    for nome, mutante in mut.items():
        problemas = conferir(mutante)
        if problemas:
            print(f"  [ok] reprovou: {nome} — {problemas[0][:90]}")
        else:
            print(f"  [FALHA] aprovou indevidamente: {nome}")
            falhas += 1
    falhas += _autoteste_dados(analisa(t))
    falhas_b, n_bases = _autoteste_bases(analisa(t))
    falhas += falhas_b
    if falhas:
        return 1
    print(f"\n{len(mut)} defeitos injetados no documento, 6 nas conferências dos arquivos "
          f"alimentados e {n_bases} casos nas fichas das bases, todos com o resultado esperado.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--conferir", action="store_true", help="lê o documento e relata problemas")
    ap.add_argument("--conferir-dados", action="store_true",
                    help="confere os arquivos alimentados de data/ contra o documento")
    ap.add_argument("--autoteste", action="store_true",
                    help="injeta defeitos em cópias e exige que as conferências os reprovem")
    ap.add_argument("--sincronizar", action="store_true",
                    help="reconcilia sementes.json com o documento")
    ap.add_argument("--mostrar", action="store_true", help="resume o que foi lido")
    ap.add_argument("--pendencias", action="store_true",
                    help="relata pendências encontradas nos artefatos, sem escrever")
    a = ap.parse_args()

    if a.sincronizar:
        return sincronizar()
    if a.pendencias:
        return pendencias_relatorio()
    if a.conferir_dados:
        problemas, avisos = conferir_dados()
        for v in avisos:
            print("AVISO:", v)
        if problemas:
            print("PROBLEMAS:")
            for p in problemas:
                print("  -", p)
            return 1
        print("Arquivos alimentados de data/ na forma esperada.")
        return 0
    if a.conferir or a.autoteste:
        problemas = conferir()
        if problemas:
            print("PROBLEMAS:")
            for p in problemas:
                print("  -", p)
            return 1
        print("Documento na forma esperada.\n")
        print(relatorio(analisa()))
        return autoteste() if a.autoteste else 0
    if a.mostrar:
        print(relatorio(analisa()))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
