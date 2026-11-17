#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O protocolo como fonte: lê o documento e deriva os artefatos de máquina.

O documento `docs/2_protocolo/03_protocolo_estrategia_pesquisa.md` é a fonte única
da questão, das facetas, do vocabulário, das strings, das expressões, dos critérios,
das fontes e do conjunto-semente. Este script lê as seções e grava, em `data/`:

  questoes.json      questão principal, questões específicas e estrutura PICo
  facetas.json       palavras significativas: nome, cor e âncora de cada faceta
  descritores.json   controle terminológico por faceta; MISTO — as tabelas são
                     derivadas, o estatuto de validação de cada termo é autoral
  strings.json       string de cada faceta e composição das quatro expressões
  criterios.json     critérios de inclusão e de exclusão e recorte temporal
  fontes.json        bases, ordem de execução, acervos especiais, ferramenta
  sementes.json      conjunto-semente; MISTO — referências e mapa por base são
                     derivados, a conferência de cada referência é autoral

Arquivos auxiliares, criados só se ausentes e nunca reescritos:

  consultas.json     registros de execução, escritos por
                     `derivar_expressoes.py --registrar`
  pendencias.json    estado das pendências abertas, escrito pelo pesquisador

Garantia contra defasagem, em dois níveis:

  fonte.sha256       detecta documento alterado sem `--gerar` (como antes)
  derivado.sha256    detecta campo DERIVADO editado à mão; cobre exatamente o
                     subconjunto que cada arquivo declara em `SUBSETS`. Campo
                     autoral pode ser editado livremente.

Uso
  python3 src/protocolo.py --conferir              # confere o documento
  python3 src/protocolo.py --conferir-dados        # confere os JSON de data/
  python3 src/protocolo.py --conferir --autoteste  # prova que as conferências reprovam
  python3 src/protocolo.py --gerar                 # deriva os JSON
  python3 src/protocolo.py --mostrar               # resume o que leu
  python3 src/protocolo.py --pendencias            # relata pendências, sem escrever

Só biblioteca padrão.
"""

import argparse
import copy
import hashlib
import json
import pathlib
import re
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOC = RAIZ / "docs" / "2_protocolo" / "03_protocolo_estrategia_pesquisa.md"
DATA = RAIZ / "data"

ARQ = {
    "questoes": DATA / "questoes.json",
    "facetas": DATA / "facetas.json",
    "descritores": DATA / "descritores.json",
    "strings": DATA / "strings.json",
    "criterios": DATA / "criterios.json",
    "fontes": DATA / "fontes.json",
    "sementes": DATA / "sementes.json",
}
AUX = {
    "consultas": DATA / "consultas.json",
    "pendencias": DATA / "pendencias.json",
}

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

# Colunas da planilha de validação, na ordem em que ela é exportada. O JSON guarda
# as mesmas chaves, omitindo as vazias; `validar_termos.py` as preenche de volta.
CAMPOS_VALIDACAO = (
    "instrumento", "consultado_em", "versao_instrumento", "url_consultada",
    "status_proposto", "rotulo_autorizado", "uri_conceito",
    "equivalentes_USE_UP", "termos_genericos_TG", "termos_especificos_TE",
    "termos_relacionados_TR", "nota_de_escopo",
    "arquivo_evidencia", "observacao_tecnica",
    "decisao_ReT", "justificativa_ReT", "data_decisao",
)

# Metadados que o documento não guarda e que a geração NUNCA sobrescreve.
CAMPOS_AUTORAIS = ("verificacao", "escopo", "tipo", "alinhamento", "nota",
                   "veiculo_conferido", "eric")

LEIA = {
    "questoes": "DERIVADO de docs/2_protocolo/03_protocolo_estrategia_pesquisa.md por "
                "src/protocolo.py --gerar. Não editar: regerar.",
    "facetas": "DERIVADO do protocolo por src/protocolo.py --gerar. Palavras significativas: "
               "nome, cor e âncora de cada faceta. Termos e strings ficam em "
               "descritores.json e strings.json.",
    "descritores": "MISTO. As tabelas (camadas, termos, instrumentos, livre) são DERIVADAS "
                   "do protocolo por src/protocolo.py --gerar. O bloco `estatuto` é AUTORAL: "
                   "guarda a validação de cada termo e a decisão do pesquisador. --gerar "
                   "preserva o estatuto e só acrescenta termo novo. Termo retirado do "
                   "protocolo permanece com no_protocolo=false.",
    "strings": "DERIVADO do protocolo por src/protocolo.py --gerar. String executada de cada "
               "faceta, composição de E1 a E4 e qual delas é a executada. É deste arquivo "
               "que a derivação local lê a lista de termos executados.",
    "criterios": "DERIVADO do protocolo por src/protocolo.py --gerar. Critérios de inclusão e "
                 "de exclusão por dimensão e recorte temporal. Regra de borda, regra de "
                 "exceção e regra única de inclusão vivem no IO 1, não aqui.",
    "fontes": "DERIVADO do protocolo por src/protocolo.py --gerar. Bases, ordem de execução, "
              "via de acesso, acervos especiais e ferramenta de gestão. O conjunto-semente "
              "fica em sementes.json.",
    "sementes": "MISTO. Referências, mapa por base, distribuição e limiar são DERIVADOS do "
                "protocolo por src/protocolo.py --gerar. Os campos de conferência "
                "(verificação, escopo, tipo, alinhamento, nota, veículo, eric) são AUTORAIS "
                "e nunca são sobrescritos. Semente retirada do protocolo permanece com "
                "no_protocolo=false.",
}

LEIA_AUX = {
    "consultas": (
        "Registro das execuções. Escrito por src/derivar_expressoes.py --registrar, que lê a "
        "exportação, conta os registros e recusa registrar quando o retorno declarado pela "
        "base diverge do que o arquivo contém, salvo justificativa explícita. `--derivar` só "
        "processa consulta válida ou divergente justificada. A data e a hora aqui são "
        "OPERACIONAIS: a data oficial de execução continua sendo a do IO 7."),
    "pendencias": (
        "Estado das tarefas e pendências abertas do projeto. Escrito pelo pesquisador. Não é "
        "histórico: o histórico é o Anexo A, docs/1_gestao/historico.md. src/protocolo.py "
        "--pendencias apenas relata o que encontra, sem escrever aqui."),
}


class ProtocoloInvalido(Exception):
    """O documento não tem a forma que o leitor sabe interpretar."""


# --------------------------------------------------------------------- utilidades
def texto(caminho=DOC):
    return pathlib.Path(caminho).read_text(encoding="utf-8")


def sha256(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def canonico(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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


def caminhos(obj, prefixo=""):
    """Caminhos das folhas, para declarar exatamente o que a assinatura cobre."""
    saida = set()
    if isinstance(obj, dict):
        if not obj:
            saida.add(prefixo + "{}")
        for k, v in obj.items():
            saida |= caminhos(v, f"{prefixo}.{k}" if prefixo else k)
    elif isinstance(obj, list):
        if not obj:
            saida.add(prefixo + "[]")
        for v in obj:
            saida |= caminhos(v, prefixo + "[]")
    else:
        saida.add(prefixo)
    return saida


# ------------------------------------------------------------------------ questões
def questoes(t):
    bloco = secao(t, "Questão de revisão")
    principal = secao(bloco, "Questão principal de revisão")
    paras = paragrafos(principal)
    if not paras:
        raise ProtocoloInvalido("questão principal de revisão vazia")
    pergunta = paras[0]
    estrutura = ""
    for p in paras[1:]:
        if p.startswith("Estrutura da questão"):
            estrutura = re.sub(r"\s*Questões específicas de revisão:\s*$", "", p).strip()
    if not estrutura:
        raise ProtocoloInvalido("estrutura PICo da questão não declarada")

    especificas = []
    for m in re.finditer(r"^-\s*(QS\d+):\s*(.+)$", secao(bloco, "Questões específicas de revisão"),
                         re.M):
        especificas.append({"id": m.group(1), "texto": m.group(2).strip()})
    if len(especificas) != 4:
        raise ProtocoloInvalido(f"esperava QS1 a QS4, achei {len(especificas)}")
    if [e["id"] for e in especificas] != ["QS1", "QS2", "QS3", "QS4"]:
        raise ProtocoloInvalido(f"questões específicas fora de ordem: "
                                f"{[e['id'] for e in especificas]}")
    return {"questao_principal": pergunta, "estrutura_pico": estrutura,
            "questoes_especificas": especificas}


# ------------------------------------------------------------------------ facetas
def palavras(t):
    """Nome, cor e papel de cada faceta, da lista de palavras significativas."""
    bloco = secao(t, "Palavras significativas da questão de revisão")
    saida = []
    for m in re.finditer(r"^-\s*Faceta\s+(\d+):\s*(.+)$", bloco, re.M):
        n = int(m.group(1))
        corpo = m.group(2)
        partes = [p.strip() for p in corpo.split("—")]
        if len(partes) < 2:
            raise ProtocoloInvalido(f"faceta {n}: nome e cor não separados por travessão")
        saida.append({
            "n": n, "nome": partes[0], "cor": partes[1],
            "ancora": bool(re.search(r"âncora obrigatória\s+" + str(n), corpo)),
        })
    if len(saida) != 4:
        raise ProtocoloInvalido(f"esperava 4 facetas, achei {len(saida)}")
    if [f["n"] for f in saida] != [1, 2, 3, 4]:
        raise ProtocoloInvalido(f"facetas fora de numeração: {[f['n'] for f in saida]}")
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
    nomes = {f["n"]: f for f in palavras(t)}
    bloco = secao(t, "Controle terminológico")
    linhas = bloco.splitlines()

    saida, atual = [], None
    for linha in linhas:
        cab = re.match(r"^\|\s*Faceta\s+n[º°]?\s*(\d+)\s*\|", linha)
        if cab:
            n = int(cab.group(1))
            if n not in nomes:
                raise ProtocoloInvalido(f"tabela da faceta {n} sem palavra significativa")
            atual = {"n": n, "nome": nomes[n]["nome"], "ancora": nomes[n]["ancora"],
                     "cor": nomes[n]["cor"], "instrumentos": "",
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
    saida = {}
    for linha in bloco.splitlines():
        m = re.match(r"^\|\s*String faceta\s+(\d+)\b", linha)
        if not m:
            continue
        n = int(m.group(1))
        celula = linha.split(" | ", 1)[1].strip().rstrip("|").strip() if " | " in linha else linha
        termos = re.findall(r'"([^"]+)"', celula)
        if not termos:
            raise ProtocoloInvalido(f"string da faceta {n} sem termos entre aspas")
        residuo = re.sub(r'"[^"]+"', "", celula)
        residuo = residuo.replace("OR", " ").replace("(", " ").replace(")", " ")
        if residuo.strip(" .;|"):
            raise ProtocoloInvalido(
                f"string da faceta {n} tem conteúdo fora do padrão \"termo\" OR ...: "
                f"{residuo.strip()[:60]!r}")
        saida[n] = {"texto": celula, "termos": termos}
    if len(saida) != 4:
        raise ProtocoloInvalido(f"esperava 4 strings de faceta, achei {len(saida)}")
    return saida


# ---------------------------------------------------------------------- expressões
ORDINAIS = {"primeira": 1, "segunda": 2, "terceira": 3, "quarta": 4}


def expressoes(t):
    """Composição de E1 a E4 e qual delas é a executada."""
    bloco = secao(t, "Expressões de busca")
    composicao, executada = {}, set()
    for linha in bloco.splitlines():
        m = re.match(r"^\|\s*(Primeira|Segunda|Terceira|Quarta)\s+expressão", linha, re.I)
        if not m:
            continue
        n = ORDINAIS[m.group(1).lower()]
        comp = re.search(r"strings\s+((?:\d\s*(?:\\?\+)?\s*)+)", linha)
        if not comp:
            raise ProtocoloInvalido(f"expressão {n} sem composição legível")
        composicao[n] = [int(x) for x in re.findall(r"\d", comp.group(1))]
        if "NÃO É EXECUTADA" not in linha:
            executada.add(n)
    if sorted(composicao) != [1, 2, 3, 4]:
        raise ProtocoloInvalido(f"esperava E1 a E4, achei {sorted(composicao)}")
    if len(executada) != 1:
        raise ProtocoloInvalido(f"esperava exatamente uma expressão executada, achei {executada}")
    return composicao, executada.pop()


# ---------------------------------------------------------------------- critérios
def criterios(t):
    bloco = secao(t, "Critérios de elegibilidade")
    saida, dimensao = [], ""
    for linha in bloco.splitlines():
        if not linha.strip().startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 5:
            continue
        acao = desescapa(cels[1]).strip()
        if acao not in ("Incluir", "Excluir"):
            continue
        rotulo = desescapa(cels[0].strip("* ")).strip()
        if rotulo:
            dimensao = rotulo
        saida.append({"dimensao": dimensao, "acao": acao,
                      "criterio": desescapa(cels[2]).strip(),
                      "justificativa": desescapa(cels[4]).strip()})
    if len(saida) != 9:
        raise ProtocoloInvalido(f"esperava 9 critérios, achei {len(saida)}")
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
            # "após o ano 2016" é inclusivo a partir de 2017; o protocolo não declara teto.
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

    bases = []
    for m in re.finditer(r"^- \((\d+)\)\s*(.+?)\s+—\s+(.+)$", bases_bloco, re.M):
        bases.append({"n": int(m.group(1)),
                      "nome": desescapa(m.group(2)).strip(),
                      "papel": desescapa(m.group(3)).strip()})
    if len(bases) != 4:
        raise ProtocoloInvalido(f"esperava 4 bases de dados, achei {len(bases)}")

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
    refs = re.findall(r"^- (\d+)\\?\.\s+(.+)$", bloco, re.M)
    if not refs:
        raise ProtocoloInvalido("nenhuma referência numerada em Acervos pessoais")

    mapa = {n: (aut, ano, bases) for n, aut, ano, bases in _mapa(bloco)}
    estudos = []
    for n, bruto in refs:
        n = int(n)
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
            "n": n, "autores": autores.strip(), "ano": int(ano),
            "titulo": _titulo(resto), "doi": _doi(ref),
            "bases": bases, "chave": f"{primeiro} {ano}",
        })
    if [e["n"] for e in estudos] != list(range(1, len(estudos) + 1)):
        raise ProtocoloInvalido("referências fora de numeração sequencial")
    return estudos


def distribuicao(t, estudos):
    """Recalcula a distribuição do mapa e confere contra o parágrafo."""
    bloco = secao(t, "Acervos pessoais")
    por_base = {b: 0 for b in BASES}
    for e in estudos:
        for b in e["bases"]:
            if b not in por_base:
                raise ProtocoloInvalido(f"semente {e['n']}: base desconhecida {b!r}")
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
    comp, exec_ = expressoes(t)
    crit = criterios(t)
    est = sementes(t)
    return {
        "questoes": questoes(t),
        "facetas": pal,
        "tabelas": tb,
        "strings": st,
        "expressoes": comp,
        "executada": exec_,
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
                    problemas.append(f"faceta {f['n']}: camada {c} vazia em {i}")
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
                            f"faceta {f['n']} {i}/{c}: {termo!r} repetido na mesma camada")
                    vistos.add(k)

    for f in d["facetas"]:
        if not f["cor"]:
            problemas.append(f"faceta {f['n']}: cor não declarada")
    ancoras = sorted(f["n"] for f in d["facetas"] if f["ancora"])
    if ancoras != [1, 2]:
        problemas.append(f"âncoras deveriam ser as facetas 1 e 2, são {ancoras}")

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

    comp, exec_ = d["expressoes"], d["executada"]
    if comp != {1: [1, 2, 3, 4], 2: [1, 2, 3], 3: [1, 2, 4], 4: [1, 2]}:
        problemas.append(f"composição das expressões fora do previsto: {comp}")
    if exec_ != 4:
        problemas.append(f"a expressão executada deveria ser E4, é E{exec_}")
    for a in (2, 3):
        if not set(comp[4]) < set(comp[a]):
            problemas.append(f"E4 não é subconjunto estrito de E{a}")
    if set(comp[4]) != set(comp[2]) & set(comp[3]):
        problemas.append("E4 não é a interseção de E2 com E3")

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
        problemas.append("questão principal vazia")
    if len(d["questoes"]["questoes_especificas"]) != 4:
        problemas.append("questões específicas não são quatro")

    if len(d["sementes"]) < 8:
        problemas.append(f"{len(d['sementes'])} sementes; a faixa do protocolo é 8 a 10")
    for e in d["sementes"]:
        if not e["titulo"] or len(e["titulo"]) < 12:
            problemas.append(f"semente {e['n']}: título não legível ({e['titulo']!r})")
        if not e["bases"]:
            problemas.append(f"semente {e['n']}: sem base esperada no mapa")

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

    # Decisões registradas que se podem codificar como teste. `taxonomy` e o plural
    # saíram da expressão por RETIRA; `taxonomia` em português permanece, por decisão.
    termos = {normaliza(x) for f in d["strings"].values() for x in f["termos"]}
    for proibido in ("taxonomy", "taxonomies"):
        if proibido in termos:
            problemas.append(f"RETIRA violado: {proibido!r} presente nas strings")
    if "taxonomia" not in termos:
        problemas.append("a forma portuguesa 'taxonomia' sumiu das strings, "
                         "contra a decisão registrada")

    return problemas


def relatorio(d):
    L = []
    L.append(f"  questão: 1 principal, {len(d['questoes']['questoes_especificas'])} específicas")
    for f in d["tabelas"]:
        n_string = len(d["strings"][f["n"]]["termos"])
        n_bruto = sum(len(f["termos"][i]) for i in IDIOMAS)
        L.append(f"  faceta {f['n']} — {f['nome'][:52]:<54} "
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
        f"E{n}=" + "+".join(map(str, c)) for n, c in sorted(d["expressoes"].items())) +
        f"   executada: E{d['executada']}")
    L.append(f"  recorte: {d['recorte']['ano_min']} em diante   limiar: {d['limiar']:.0%}")
    return "\n".join(L)


# -------------------------------------------------------------------- assinaturas
def _sub_questoes(d):
    return {k: d[k] for k in ("questao_principal", "estrutura_pico", "questoes_especificas")}


def _sub_facetas(d):
    return {"facetas": d["facetas"]}


def _sub_descritores(d):
    """Tudo é derivado, exceto `estatuto[].validacoes`; a chave e o termo ficam."""
    saida = {"facetas": []}
    for f in d["facetas"]:
        g = {k: v for k, v in f.items() if k != "estatuto"}
        g["estatuto"] = {
            idioma: {k: {"termo": e.get("termo", ""),
                         "no_protocolo": bool(e.get("no_protocolo", True))}
                     for k, e in termos.items()}
            for idioma, termos in f.get("estatuto", {}).items()}
        saida["facetas"].append(g)
    return saida


def _sub_strings(d):
    return {k: d[k] for k in ("facetas", "expressoes", "executada")}


def _sub_criterios(d):
    return {k: d[k] for k in ("recorte", "criterios")}


def _sub_fontes(d):
    return {k: d[k] for k in ("bases", "ordem_execucao", "via_de_acesso",
                              "acervos_especiais", "ferramenta_gestao")}


def _sub_sementes(d):
    saida = {"limiar": d["limiar"], "distribuicao": d["distribuicao"], "estudos": []}
    for e in d["estudos"]:
        g = {k: v for k, v in e.items()
             if k not in CAMPOS_AUTORAIS}
        saida["estudos"].append(g)
    return saida


SUBSETS = {
    "questoes.json": _sub_questoes,
    "facetas.json": _sub_facetas,
    "descritores.json": _sub_descritores,
    "strings.json": _sub_strings,
    "criterios.json": _sub_criterios,
    "fontes.json": _sub_fontes,
    "sementes.json": _sub_sementes,
}


def assina(nome, dado):
    chave = nome if nome.endswith(".json") else nome + ".json"
    sub = SUBSETS[chave](dado)
    return {"sha256": hashlib.sha256(canonico(sub).encode("utf-8")).hexdigest(),
            "chaves": sorted(caminhos(sub))}


def verifica_dado(caminho, dado, doc=DOC):
    """Problemas de procedência de um JSON já carregado. Lista vazia = íntegro."""
    nome = pathlib.Path(caminho).name
    problemas = []
    esperado = (dado.get("fonte") or {}).get("sha256")
    if not esperado:
        problemas.append("sem bloco `fonte`")
    elif esperado != sha256(texto(doc)):
        problemas.append("documento do protocolo mudou depois da última derivação; "
                         "rode  python3 src/protocolo.py --gerar")
    sub = SUBSETS.get(nome)
    if sub is None:
        problemas.append(f"arquivo sem definição de subconjunto derivado: {nome}")
        return problemas
    calculado = hashlib.sha256(canonico(sub(dado)).encode("utf-8")).hexdigest()
    if calculado != (dado.get("derivado") or {}).get("sha256"):
        problemas.append("campo DERIVADO editado à mão; rode  python3 src/protocolo.py "
                         "--gerar  para regerar sem tocar no que é autoral")
    return problemas


def carrega(caminho):
    """Carrega um JSON de data/ e recusa seguir se estiver defasado ou adulterado."""
    caminho = pathlib.Path(caminho)
    if not caminho.exists():
        raise SystemExit(f"{caminho.name} não encontrado: rode  python3 src/protocolo.py --gerar")
    try:
        dado = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"{caminho.name} ilegível: {e}. Regenere com --gerar.")
    problemas = verifica_dado(caminho, dado)
    if problemas:
        raise SystemExit("\n".join(f"{caminho.name}: {p}" for p in problemas))
    return dado


def conferir_dados():
    """Confere os JSON de data/ entre si e contra o documento. Devolve (problemas, avisos)."""
    problemas, avisos = [], []
    dados = {}
    for nome, caminho in ARQ.items():
        if not caminho.exists():
            problemas.append(f"{nome}: ausente — rode  --gerar")
            continue
        try:
            dado = json.loads(caminho.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problemas.append(f"{nome}: ilegível ({e})")
            continue
        dados[nome] = dado
        problemas += [f"{nome}: {p}" for p in verifica_dado(caminho, dado)]

    if len(dados) != len(ARQ):
        return problemas, avisos

    doc = analisa()
    conjuntos = {
        "facetas": {f["n"] for f in dados["facetas"]["facetas"]},
        "descritores": {f["n"] for f in dados["descritores"]["facetas"]},
        "strings": {f["n"] for f in dados["strings"]["facetas"]},
    }
    if len({tuple(sorted(v)) for v in conjuntos.values()}) != 1:
        problemas.append(f"facetas divergem entre arquivos: {conjuntos}")

    tabelados = {normaliza(x) for f in dados["descritores"]["facetas"]
                 for i in IDIOMAS for x in f["termos"][i]}
    for f in dados["strings"]["facetas"]:
        for termo in f["termos"]:
            if normaliza(termo) not in tabelados:
                problemas.append(f"strings: termo {termo!r} da faceta {f['n']} não consta "
                                 f"de descritores.json")

    protocolo_n = [e["n"] for e in dados["sementes"]["estudos"] if "n" in e]
    if len(protocolo_n) != len(doc["sementes"]):
        avisos.append(f"sementes.json tem {len(protocolo_n)} estudos e o protocolo "
                      f"{len(doc['sementes'])}; ver no_protocolo=false")

    # Estatuto: termo do protocolo sem bloco de validação seria termo silenciosamente
    # não validado. O bloco pode estar vazio de conteúdo, mas tem de existir.
    for f in dados["descritores"]["facetas"]:
        for idioma in IDIOMAS:
            for termo in f["termos"][idioma]:
                k = normaliza(termo)
                e = f.get("estatuto", {}).get(idioma, {}).get(k)
                if e is None:
                    problemas.append(f"descritores: faceta {f['n']} {idioma} {termo!r} "
                                     f"sem bloco de estatuto")
    if AUX["consultas"].exists():
        for c in json.loads(AUX["consultas"].read_text(encoding="utf-8")).get("consultas", []):
            arq = RAIZ / c.get("arquivo", "")
            if not c.get("arquivo") or not arq.exists():
                problemas.append(f"consultas: {c.get('id')} aponta arquivo ausente "
                                 f"{c.get('arquivo')!r}")
    return problemas, avisos


# --------------------------------------------------------------------------- gerar
def _fonte(t):
    return {"arquivo": str(DOC.relative_to(RAIZ)), "sha256": sha256(t)}


def _grava(caminho, nome, conteudo, fonte):
    dado = {"_leia": LEIA[nome], "fonte": fonte,
            "derivado": assina(nome, conteudo)}
    dado.update(conteudo)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")


def _existente(caminho):
    if not caminho.exists():
        return {}
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"{caminho} ilegível: {e}. Corrija ou remova antes de gerar.")


def _instrumentos(idioma):
    return INSTRUMENTO_POR_IDIOMA[idioma]


OCUPADO = ("status_proposto", "consultado_em", "arquivo_evidencia", "decisao_ReT")


def _estatuto_novo(termo, idioma, livre):
    validacoes = []
    for inst in _instrumentos(idioma):
        v = {"instrumento": inst}
        if livre:
            v.update(status_proposto=STATUS_LIVRE_DECISAO,
                     observacao_tecnica="não consultado: decisão de protocolo",
                     justificativa_ReT=JUSTIFICATIVA_LIVRE)
        else:
            v["observacao_tecnica"] = "aguardando consulta"
        validacoes.append(v)
    return {"termo": termo, "no_protocolo": True, "validacoes": validacoes}


def _garante_validacoes(validacoes, idioma, livre):
    """Completa o instrumento que faltar, sem tocar no que já foi registrado."""
    vistos = {v.get("instrumento") for v in validacoes}
    for inst in _instrumentos(idioma):
        if inst in vistos:
            continue
        novo = {"instrumento": inst}
        if livre:
            novo.update(status_proposto=STATUS_LIVRE_DECISAO,
                        observacao_tecnica="não consultado: decisão de protocolo",
                        justificativa_ReT=JUSTIFICATIVA_LIVRE)
        else:
            novo["observacao_tecnica"] = "aguardando consulta"
        validacoes.append(novo)
    for v in validacoes:
        for c in CAMPOS_VALIDACAO:
            v.setdefault(c, "")
        # Linha intocada recebe o marcador que a planilha sempre teve. Linha com
        # qualquer registro — inclusive decisão do pesquisador — não é tocada.
        if not any(v.get(c) for c in OCUPADO) and not v.get("observacao_tecnica"):
            v["observacao_tecnica"] = "aguardando consulta"
    return validacoes


def _merge_descritores(facetas_novas, existente):
    """Preserva o estatuto por (faceta, idioma, termo normalizado)."""
    anterior = {f["n"]: f for f in existente.get("facetas", [])}
    facetas = []
    for f in facetas_novas:
        est_ant = anterior.get(f["n"], {}).get("estatuto", {})
        f = {k: v for k, v in f.items()}
        f["estatuto"] = {}
        for idioma in IDIOMAS:
            atual = {}
            for termo in f["termos"][idioma]:
                k = normaliza(termo)
                e = copy.deepcopy(est_ant.get(idioma, {}).get(k))
                if e is None:
                    e = _estatuto_novo(termo, idioma, f["livre"])
                else:
                    e["termo"] = termo
                    e["no_protocolo"] = True
                    e["validacoes"] = _garante_validacoes(e.get("validacoes", []),
                                                          idioma, f["livre"])
                atual[k] = e
            # Termo retirado do protocolo não apaga o estatuto: fica marcado e é
            # reportado por --pendencias, para decisão, não para descarte automático.
            for k, e in est_ant.get(idioma, {}).items():
                if k in atual:
                    continue
                e = copy.deepcopy(e)
                e["no_protocolo"] = False
                atual[k] = e
            f["estatuto"][idioma] = atual
        facetas.append(f)
    return facetas


def _chaves_semente(e):
    d = (e.get("doi") or "").strip().lower()
    return ("doi:" + d if d else "ti:" + normaliza(e.get("titulo", ""))[:80],
            "ti:" + normaliza(e.get("titulo", ""))[:80])


def _merge_sementes(estudos_novos, existente):
    """Preserva os campos autorais por DOI ou, na falta dele, por título normalizado."""
    antigos = existente.get("estudos", [])
    usados = set()
    saida = []
    for e in estudos_novos:
        k_doi, k_tit = _chaves_semente(e)
        escolhido = None
        if k_doi.startswith("doi:"):
            escolhido = next((i for i, a in enumerate(antigos)
                              if i not in usados and _chaves_semente(a)[0] == k_doi), None)
        if escolhido is None:
            escolhido = next((i for i, a in enumerate(antigos)
                              if i not in usados and _chaves_semente(a)[1] == k_tit), None)
        ant = antigos[escolhido] if escolhido is not None else {}
        if escolhido is not None:
            usados.add(escolhido)
        novo = dict(e)
        for c in CAMPOS_AUTORAIS:
            novo[c] = ant.get(c, "")
        novo["no_protocolo"] = True
        saida.append(novo)

    # Semente que saiu do protocolo não é apagada: o metadado conferido é evidência.
    for i, ant in enumerate(antigos):
        if i in usados:
            continue
        novo = copy.deepcopy(ant)
        for c in CAMPOS_AUTORAIS:
            novo.setdefault(c, "")
        novo["no_protocolo"] = False
        saida.append(novo)
    return saida


def gerar(t=None):
    t = texto() if t is None else t
    problemas = conferir(t)
    if problemas:
        print("Documento fora da forma esperada; nada foi gerado:")
        for p in problemas:
            print("  -", p)
        return 1

    d = analisa(t)
    fonte = _fonte(t)

    _grava(ARQ["questoes"], "questoes", d["questoes"], fonte)
    _grava(ARQ["facetas"], "facetas", {"facetas": d["facetas"]}, fonte)
    _grava(ARQ["criterios"], "criterios",
           {"recorte": d["recorte"], "criterios": d["criterios"]}, fonte)
    _grava(ARQ["fontes"], "fontes", d["fontes"], fonte)
    _grava(ARQ["strings"], "strings",
           {"facetas": [{"n": f["n"], "string": d["strings"][f["n"]]["texto"],
                         "termos": _sem_repeticao(d["strings"][f["n"]]["termos"])}
                        for f in d["facetas"]],
            "expressoes": {str(n): c for n, c in sorted(d["expressoes"].items())},
            "executada": d["executada"]}, fonte)

    existentes = _existente(ARQ["descritores"])
    _grava(ARQ["descritores"], "descritores",
           {"facetas": _merge_descritores(d["tabelas"], existentes)}, fonte)

    existentes_s = _existente(ARQ["sementes"])
    _grava(ARQ["sementes"], "sementes",
           {"limiar": d["limiar"], "distribuicao": d["distribuicao"],
            "estudos": _merge_sementes(d["sementes"], existentes_s)}, fonte)

    criados = []
    for nome, caminho in AUX.items():
        if not caminho.exists():
            caminho.parent.mkdir(parents=True, exist_ok=True)
            chave = "consultas" if nome == "consultas" else "tarefas"
            caminho.write_text(json.dumps(
                {"_leia": LEIA_AUX[nome], "versao": 1, chave: []},
                ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            criados.append(caminho)

    print("Derivados gravados:")
    for nome, caminho in ARQ.items():
        print(f"  {caminho.relative_to(RAIZ)}")
    if criados:
        for c in criados:
            print(f"  {c.relative_to(RAIZ)}  (auxiliar criado; não é regerado)")
    print(relatorio(d))
    return 0


# ---------------------------------------------------------------------- pendências
CAMPOS_PENDENTES = (("verificacao", "verificação"), ("escopo", "escopo"),
                    ("tipo", "tipo"), ("alinhamento", "alinhamento"))


def pendencias_relatorio():
    """Relata o que está aberto, sem escrever. O destino é data/pendencias.json."""
    linhas = []
    for nome, caminho in ARQ.items():
        if not caminho.exists():
            linhas.append(f"[ausente] {caminho.relative_to(RAIZ)} — rode --gerar")
    if ARQ["sementes"].exists():
        s = carrega(ARQ["sementes"])
        for e in s["estudos"]:
            if e.get("no_protocolo") is False:
                linhas.append(f"[semente fora do protocolo] {e.get('n')} {e.get('chave','')} "
                              f"— decidir: remover com registro ou reincluir no protocolo")
                continue
            vazios = []
            for campo, rotulo in CAMPOS_PENDENTES:
                v = str(e.get(campo) or "")
                if not v or v.startswith(("A CONFERIR", "a conferir")) or "PENDÊNCIA" in v:
                    vazios.append(rotulo)
            if vazios:
                linhas.append(f"[semente {e['n']} {e.get('chave','')}] pendente: "
                              f"{', '.join(vazios)}")
    if ARQ["descritores"].exists():
        d = carrega(ARQ["descritores"])
        sem_estatuto = 0
        for f in d["facetas"]:
            for idioma in IDIOMAS:
                for termo in f["termos"][idioma]:
                    e = f.get("estatuto", {}).get(idioma, {}).get(normaliza(termo), {})
                    if not any(v.get("status_proposto") for v in e.get("validacoes", [])):
                        sem_estatuto += 1
        if sem_estatuto:
            linhas.append(f"[descritores] {sem_estatuto} termo(s) sem estatuto de validação "
                          f"— rodar src/validar_termos.py --validar")
        orfaos = [f"{f['n']}/{i}:{e.get('termo')}" for f in d["facetas"]
                  for i, termos in f.get("estatuto", {}).items()
                  for e in termos.values() if e.get("no_protocolo") is False]
        if orfaos:
            linhas.append(f"[descritores] {len(orfaos)} termo(s) fora do protocolo com "
                          f"estatuto preservado — decidir: {', '.join(orfaos[:6])}")
    if AUX["consultas"].exists():
        c = json.loads(AUX["consultas"].read_text(encoding="utf-8"))
        if not c.get("consultas"):
            linhas.append("[consultas] nenhuma execução registrada")
        for x in c.get("consultas", []):
            if x.get("status") not in ("valida", "divergente_justificada"):
                linhas.append(f"[consulta {x.get('id')}] status {x.get('status')!r}")
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

    i_str = next(i for i, l in enumerate(linhas) if l.startswith("| String faceta 2"))
    string_quebrada = list(linhas)
    string_quebrada[i_str] = string_quebrada[i_str].replace(" OR ", ", ", 1)

    sem_semente = [l for l in linhas if not l.startswith("- 10\\.")]

    dist_errada = [l.replace("Scopus, 6;", "Scopus, 7;", 1) for l in linhas]

    i_nuc = next(i for i, l in enumerate(linhas) if l.startswith("| *Termos centrais")
                 and "representação do conhecimento" in l)
    duplicada = list(linhas)
    duplicada[i_nuc] = duplicada[i_nuc].replace(
        "\\- representação do conhecimento \\- organização do conhecimento",
        "\\- representação do conhecimento \\- representação do conhecimento "
        "\\- organização do conhecimento", 1)

    sem_principal = [l for l in linhas if l.strip() != "### Questão principal de revisão"]
    sem_qs4 = [l for l in linhas if not l.startswith("- QS4:")]
    sem_idioma = [l for l in linhas if "| **Idioma(s)** |" not in l]
    sem_brapci = [l for l in linhas if not l.startswith("- (4) BRAPCI")]

    return {
        "linha de faceta removida": "\n".join(sem_linha),
        "string fora do padrão OR": "\n".join(string_quebrada),
        "semente ausente": "\n".join(sem_semente),
        "distribuição contradita": "\n".join(dist_errada),
        "termo duplicado na faceta": "\n".join(duplicada),
        "questão principal removida": "\n".join(sem_principal),
        "QS4 removida": "\n".join(sem_qs4),
        "critério de idioma removido": "\n".join(sem_idioma),
        "base BRAPCI removida": "\n".join(sem_brapci),
    }


def _autoteste_dados():
    """Prova que a assinatura reprova edição de campo derivado e aprova a autoral."""
    if not all(p.exists() for p in ARQ.values()):
        print("  [--] sem data/ completo: o teste das assinaturas não foi executado")
        return 0
    falhas = 0

    adulterado = json.loads(ARQ["facetas"].read_text(encoding="utf-8"))
    adulterado["facetas"][0]["nome"] = "nome adulterado à mão"
    if verifica_dado(ARQ["facetas"], adulterado):
        print("  [ok] reprovou: campo derivado adulterado em facetas.json")
    else:
        print("  [FALHA] aprovou: campo derivado adulterado em facetas.json")
        falhas += 1

    autoral = json.loads(ARQ["descritores"].read_text(encoding="utf-8"))
    idioma = next(i for i in IDIOMAS if autoral["facetas"][0]["estatuto"].get(i))
    chave = next(iter(autoral["facetas"][0]["estatuto"][idioma]))
    autoral["facetas"][0]["estatuto"][idioma][chave]["validacoes"][0]["decisao_ReT"] = \
        "decisão do pesquisador"
    if not verifica_dado(ARQ["descritores"], autoral):
        print("  [ok] aprovou: campo autoral editado em descritores.json")
    else:
        print("  [FALHA] reprovou indevidamente: campo autoral em descritores.json")
        falhas += 1

    defasado = json.loads(ARQ["strings"].read_text(encoding="utf-8"))
    defasado["fonte"]["sha256"] = "0" * 64
    if verifica_dado(ARQ["strings"], defasado):
        print("  [ok] reprovou: fonte defasada em strings.json")
    else:
        print("  [FALHA] aprovou: fonte defasada em strings.json")
        falhas += 1
    return falhas


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
    falhas += _autoteste_dados()
    if falhas:
        return 1
    print(f"\n{len(mut)} defeitos injetados no documento e 3 nas assinaturas, "
          f"todos com o resultado esperado.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--conferir", action="store_true", help="lê o documento e relata problemas")
    ap.add_argument("--conferir-dados", action="store_true",
                    help="confere os JSON de data/ entre si e contra o documento")
    ap.add_argument("--autoteste", action="store_true",
                    help="injeta defeitos em cópias e exige que as conferências os reprovem")
    ap.add_argument("--gerar", action="store_true", help="deriva os JSON a partir do documento")
    ap.add_argument("--mostrar", action="store_true", help="resume o que foi lido")
    ap.add_argument("--pendencias", action="store_true",
                    help="relata pendências encontradas nos artefatos, sem escrever")
    a = ap.parse_args()

    if a.gerar:
        return gerar()
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
        print("Artefatos de data/ na forma esperada.")
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
