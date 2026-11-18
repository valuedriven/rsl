#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O protocolo como fonte: lê o documento, confere e sincroniza o que é alimentado.

O documento do protocolo (caminho na chave `protocolo` do `config.toml`) é a fonte única
da questão, das facetas, do vocabulário, das strings, das expressões, dos critérios, das
fontes, dos instrumentos de controle terminológico e do conjunto-semente. A forma de cada
base está na respectiva ficha (`[fichas]` do `config.toml`). Este script lê as fontes em
memória e NÃO grava derivado algum.

Parâmetros: todo parâmetro tem valor padrão no `config.toml`; o que o protocolo declara
prevalece. Trecho do protocolo presente e ilegível reprova, sem cair no padrão.
`--mostrar` exibe o valor em uso e a origem de cada parâmetro.

Em `data/` vivem só os arquivos alimentados (`[dados]` do `config.toml`):

  sementes.json          AUTORAL — metadados de conferência de cada semente. Referências,
                         ano, DOI, bases e chave de citação vêm do protocolo.
                         `--sincronizar` casa por DOI ou título e preserva o conferido.
  registro_execucao.json AUTORAL — registro documental das execuções, por base.

O estatuto da validação terminológica vive na planilha de validação.

A cobertura de cada base é medida contra o vocabulário vigente — os termos da string (STR)
do protocolo, nos idiomas e camadas que a ficha declara — e contra a redução própria da
base, declarada termo a termo: termo vigente ausente e não declarado reprova, e termo da
base que não derive da STR também, inclusive o que só conste do quadro terminológico.
A ficha é documento OPERACIONAL: forma vigente e instruções de execução.

A conferência verifica a coerência interna do documento, não valores esperados; a
cobertura por faceta sai como número, porque é ela que mede o preço da forma de cada base.

Uso
  python3 src/protocolo.py --conferir              # confere o documento
  python3 src/protocolo.py --conferir-dados        # confere os arquivos alimentados
  python3 src/protocolo.py --conferir --autoteste  # prova que as conferências reprovam
  python3 src/protocolo.py --sincronizar           # reconcilia sementes.json
  python3 src/protocolo.py --mostrar               # resume o que leu e os parâmetros
  python3 src/protocolo.py --pendencias            # relata pendências, sem escrever

Só biblioteca padrão, Python 3.11+.
"""

import argparse
import copy
import csv
import json
import pathlib
import re
import sys
import unicodedata

if sys.version_info < (3, 11):
    raise SystemExit("src/protocolo.py exige Python 3.11 ou superior (tomllib, para ler "
                     "config.toml).")
import tomllib                                                      # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
# Único caminho fixado: o da configuração, na raiz. Todo o resto sai dela.
CONFIG = RAIZ / "config.toml"

# Chaves exigidas do config.toml. É o esquema do arquivo, não parâmetro do projeto.
CHAVES_CONFIG = (
    "protocolo", "idiomas",
    "padroes.recorte_ano_min", "padroes.limiar_aderencia", "padroes.sensibilidade",
    "padroes.ancoras", "padroes.executada", "padroes.sonda",
    "padroes.divergencia_fidelidade", "padroes.calibracao_triagem", "padroes.composicao",
    "expressoes.natureza_executada", "expressoes.natureza_sonda",
    "conferencia.minimo_termos_string", "conferencia.dimensoes_criterio",
    "dados.sementes", "dados.registro", "dados.validacao",
    "fichas", "cores", "instrumentos",
    "planilha.campos_validacao", "planilha.campos_autorais",
)
CHAVES_FICHA = ("bd", "sigla", "arquivo", "execucao")
CHAVES_INSTRUMENTO = ("sigla", "modo", "idiomas")
MODOS_INSTRUMENTO = ("tbci", "unesco", "manual")
MODOS_EXECUCAO = ("unica", "particionada")


class ConfiguracaoInvalida(Exception):
    """O config.toml não existe, não é TOML válido ou não tem uma chave exigida."""


def _valor(cfg, chave):
    atual = cfg
    for parte in chave.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            raise ConfiguracaoInvalida(f"{CONFIG.name}: falta a chave `{chave}`")
        atual = atual[parte]
    return atual


def valida_config(cfg):
    """Confere o esquema da configuração; levanta ConfiguracaoInvalida no primeiro defeito."""
    for chave in CHAVES_CONFIG:
        _valor(cfg, chave)
    if not cfg["fichas"]:
        raise ConfiguracaoInvalida(f"{CONFIG.name}: `fichas` vazio")
    for slug, f in cfg["fichas"].items():
        for k in CHAVES_FICHA:
            _valor(cfg, f"fichas.{slug}.{k}")
        if f["execucao"] not in MODOS_EXECUCAO:
            raise ConfiguracaoInvalida(f"{CONFIG.name}: `fichas.{slug}.execucao` "
                                       f"{f['execucao']!r} não é {MODOS_EXECUCAO}")
    for nome, inst in cfg["instrumentos"].items():
        for k in CHAVES_INSTRUMENTO:
            if k not in inst:
                raise ConfiguracaoInvalida(f"{CONFIG.name}: falta a chave `{k}` do "
                                           f"instrumento {nome!r}")
        if inst["modo"] not in MODOS_INSTRUMENTO:
            raise ConfiguracaoInvalida(f"{CONFIG.name}: instrumento {nome!r} com modo "
                                       f"{inst['modo']!r}; admitidos: {MODOS_INSTRUMENTO}")
        fora = [i for i in inst["idiomas"] if i not in cfg["idiomas"]]
        if fora:
            raise ConfiguracaoInvalida(f"{CONFIG.name}: instrumento {nome!r} com idioma "
                                       f"fora de `idiomas`: {fora}")
    lo, hi = cfg["padroes"]["sensibilidade"]
    if not lo < hi:
        raise ConfiguracaoInvalida(f"{CONFIG.name}: `padroes.sensibilidade` com inferior "
                                   f"≥ superior: {[lo, hi]}")
    return cfg


def carrega_config(caminho=CONFIG):
    caminho = pathlib.Path(caminho)
    if not caminho.exists():
        raise ConfiguracaoInvalida(f"{caminho.name} ausente em {caminho.parent}")
    try:
        with caminho.open("rb") as fh:
            cfg = tomllib.load(fh)
    except tomllib.TOMLDecodeError as e:
        raise ConfiguracaoInvalida(f"{caminho.name} não é TOML válido: {e}") from None
    return valida_config(cfg)


try:
    CFG = carrega_config()
except ConfiguracaoInvalida as e:
    raise SystemExit(f"Configuração inválida — {e}") from None

DOC = RAIZ / CFG["protocolo"]
if not DOC.exists():
    raise SystemExit(f"Configuração inválida — {CONFIG.name}: a chave `protocolo` aponta "
                     f"{CFG['protocolo']!r}, que não existe")
DATA = RAIZ / "data"

# A forma de busca é de cada base e vive na ficha da base; o vocabulário é do protocolo.
FICHAS = {slug: dict(f) for slug, f in CFG["fichas"].items()}
BASES = tuple(f["sigla"] for f in FICHAS.values())
BDS = tuple(sorted(f["bd"] for f in FICHAS.values()))

# Arquivos alimentados: não são derivados de markdown e não se regeram.
SEMENTES = RAIZ / CFG["dados"]["sementes"]
REGISTRO = RAIZ / CFG["dados"]["registro"]
CSV_VALIDACAO = RAIZ / CFG["dados"]["validacao"]

IDIOMAS = tuple(CFG["idiomas"])
CAMADAS = ("nucleo", "proximos", "relacionados")

# Rótulos das linhas do quadro: gramática do leitor, não parâmetro do projeto.
ROTULO_CAMADA = {
    "Termos centrais": "nucleo",
    "Descritores potenciais": "proximos",
    "Termos relacionados": "relacionados",
}

CAMPOS_VALIDACAO = tuple(CFG["planilha"]["campos_validacao"])
CAMPOS_AUTORAIS = tuple(CFG["planilha"]["campos_autorais"])

STATUS_MANUAL = "pendente de validação manual"
OBS_MANUAL = "instrumento sem cliente automatizado: consultar e registrar à mão"

ORIGEM_PROTOCOLO = "protocolo"
ORIGEM_PADRAO = f"padrão ({CONFIG.name})"

LEIA = {
    "sementes": "AUTORAL. Metadados de conferência de cada semente. As referências, o ano, o "
                "DOI, as bases esperadas e a chave de citação vêm do protocolo "
                f"({CFG['protocolo']}). `ligacao` é a ligação com o "
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


# ------------------------------------------------------------------------ parâmetros
def _parametro(params, nome, valor_protocolo, chave_padrao):
    """Resolve um parâmetro: o do protocolo, se declarado (não None); senão, o padrão.

    `params` acumula valor e origem, que `--mostrar` exibe. Trecho do protocolo presente e
    ilegível não chega aqui: o leitor levanta ProtocoloInvalido antes.
    """
    if valor_protocolo is not None:
        valor, origem = valor_protocolo, ORIGEM_PROTOCOLO
    else:
        valor, origem = copy.deepcopy(_valor(CFG, chave_padrao)), ORIGEM_PADRAO
    params[nome] = {"valor": valor, "origem": origem}
    return valor


def _numeracao(ids, prefixo, onde):
    """Identificadores em sequência a partir de 1: `prefixo1`, `prefixo2`, ..."""
    esperado = [f"{prefixo}{k}" for k in range(1, len(ids) + 1)]
    if not ids:
        raise ProtocoloInvalido(f"{onde}: nenhum {prefixo}n encontrado")
    if ids != esperado:
        raise ProtocoloInvalido(f"{onde} fora da numeração {prefixo}1 a {prefixo}{len(ids)}: "
                                f"{ids}")


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
    _numeracao([e["id"] for e in especificas], "QER", "questões específicas")
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
            "ancora": bool(re.search(r"âncora obrigatória", corpo)),
        })
    _numeracao([f["id"] for f in saida], "FCT", "facetas")
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
    """As tabelas do controle terminológico, uma por faceta, com as camadas por idioma."""
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
                     "camadas": {i: {c: [] for c in CAMADAS} for i in IDIOMAS}}
            saida.append(atual)
            continue
        if atual is None or not linha.startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 1 + len(IDIOMAS):
            continue
        rotulo = cels[0].strip("* ").strip()
        camada = next((v for k, v in ROTULO_CAMADA.items() if rotulo.startswith(k)), None)
        if camada is None:
            continue
        for idioma, cel in zip(IDIOMAS, cels[1:1 + len(IDIOMAS)]):
            atual["camadas"][idioma][camada] = _termos_celula(cel)

    ids = [f["id"] for f in saida]
    if sorted(ids) != sorted(nomes):
        raise ProtocoloInvalido(f"esperava uma tabela por faceta ({sorted(nomes)}), "
                                f"achei {ids}")
    for f in saida:
        f["termos"] = {i: _sem_repeticao(
            [x for c in CAMADAS for x in f["camadas"][i][c]]) for i in IDIOMAS}
    return saida


# -------------------------------------------------------------------- instrumentos
def _resolve_instrumento(item, fid):
    """Chave do `config.toml` cujo nome está contido no item lido do protocolo."""
    alvo = f" {normaliza(item)} "
    achados = [nome for nome in CFG["instrumentos"] if f" {normaliza(nome)} " in alvo]
    if not achados:
        raise ProtocoloInvalido(f"instrumento de {fid}: {item!r} não consta de "
                                f"[instrumentos] do {CONFIG.name}")
    if len(achados) > 1:
        raise ProtocoloInvalido(f"instrumento de {fid}: {item!r} casa com mais de um "
                                f"instrumento do {CONFIG.name}: {achados}")
    return achados[0]


def instrumentos(t):
    """Instrumentos de cada faceta, da seção dedicada do protocolo. Sem padrão por faceta."""
    ids = [f["id"] for f in palavras(t)]
    bloco = secao(t, "Instrumentos para controle terminológico")
    saida = {}
    for m in re.finditer(r"^-\s*(FCT\d+)\s*:\s*(.*)$", bloco, re.M):
        fid = m.group(1)
        if fid not in ids:
            raise ProtocoloInvalido(f"instrumentos: {fid} não é faceta do protocolo")
        if fid in saida:
            raise ProtocoloInvalido(f"instrumentos: {fid} declarada mais de uma vez")
        itens = [x.strip() for x in desescapa(m.group(2)).split(",") if x.strip()]
        if not itens:
            raise ProtocoloInvalido(f"instrumentos: {fid} sem instrumento declarado")
        lista = []
        for item in itens:
            nome = _resolve_instrumento(item, fid)
            inst = CFG["instrumentos"][nome]
            lista.append({"nome": nome, "texto": item, "sigla": inst["sigla"],
                          "modo": inst["modo"], "idiomas": list(inst["idiomas"])})
        saida[fid] = lista
    faltam = [f for f in ids if f not in saida]
    if faltam:
        raise ProtocoloInvalido(f"instrumentos: faceta(s) sem linha na seção "
                                f"'Instrumentos para controle terminológico': {faltam}")
    return saida


def instrumentos_do_termo(d, fid, idioma):
    """Instrumentos em que se valida um termo da faceta `fid` no `idioma`."""
    return [i for i in d["instrumentos"][fid] if idioma in i["idiomas"]]


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
    if sorted(saida) != sorted(ids_faceta):
        raise ProtocoloInvalido(f"esperava uma string por faceta ({sorted(ids_faceta)}), "
                                f"achei {sorted(saida)}")
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


def _percentual(s):
    return float(s.replace(",", ".")) / 100


def expressoes(t, params):
    """Composição das expressões, a executada, a sonda e a faixa de sensibilidade.

    Devolve (composição, executada, sonda, sensibilidade), já resolvidos pela precedência.
    """
    try:
        bloco = secao(t, "Expressões de busca")
    except ProtocoloInvalido:
        bloco = None
    composicao, natureza, detalhe = {}, {}, {}
    if bloco is not None:
        for linha in bloco.splitlines():
            if not linha.lstrip().startswith("|"):
                continue
            cels = celulas(linha)
            if len(cels) < 4 or not re.match(r"^EB\d+$", cels[0]):
                continue
            ident = cels[0]
            comb = desescapa(cels[2]).replace("\\", " ").strip()
            if not re.search(r"STR\d+", comb):
                raise ProtocoloInvalido(f"expressão {ident} sem composição legível")
            composicao[ident] = _grupos_de_composicao(comb, ident)
            natureza[ident] = normaliza(cels[1])
            detalhe[ident] = desescapa(cels[3])
        _numeracao(list(composicao), "EB", "expressões")
    comp = _parametro(params, "composicao", composicao or None, "padroes.composicao")

    def papel(nome, chave_natureza):
        alvo = normaliza(CFG["expressoes"][chave_natureza])
        achados = sorted(k for k, v in natureza.items() if v == alvo)
        if len(achados) > 1:
            raise ProtocoloInvalido(f"mais de uma expressão com natureza "
                                    f"{CFG['expressoes'][chave_natureza]!r}: {achados}")
        valor = _parametro(params, nome, achados[0] if achados else None, f"padroes.{nome}")
        if valor not in comp:
            raise ProtocoloInvalido(f"a {nome} {valor!r} não é expressão da composição")
        return valor
    executada = papel("executada", "natureza_executada")
    sonda = papel("sonda", "natureza_sonda")

    # Faixa de sensibilidade: "< N%" e "> M%" no detalhamento da sonda.
    texto_sonda = detalhe.get(sonda, "")
    baixo = re.search(r"<\s*\**\s*(\d+(?:[.,]\d+)?)\s*%", texto_sonda)
    alto = re.search(r">\s*\**\s*(\d+(?:[.,]\d+)?)\s*%", texto_sonda)
    if bool(baixo) != bool(alto):
        raise ProtocoloInvalido(f"faixa de sensibilidade ilegível no detalhamento de {sonda}: "
                                f"falta o limite {'superior' if baixo else 'inferior'}")
    faixa = [_percentual(baixo.group(1)), _percentual(alto.group(1))] if baixo else None
    sens = _parametro(params, "sensibilidade", faixa, "padroes.sensibilidade")
    return comp, executada, sonda, sens


# ---------------------------------------------------------------------- critérios
DIMENSAO_RECORTE = "Intervalo temporal"


def criterios(t):
    bloco = secao(t, "Critérios de elegibilidade")
    saida, dimensao = [], ""
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
        saida.append({"id": f"CE{int(m.group(1))}", "dimensao": dimensao, "acao": acao,
                      "criterio": desescapa(cels[3]).strip(),
                      "justificativa": desescapa(cels[5]).strip()})
    _numeracao([c["id"] for c in saida], "CE", "critérios")
    return saida


def recorte(t, params):
    """Recorte temporal: ano inicial e teto, com o texto que o declara."""
    declarado = next((c for c in criterios(t)
                      if c["dimensao"] == DIMENSAO_RECORTE and c["acao"] == "Incluir"), None)
    ano = None
    if declarado:
        m = re.search(r"após o ano\s+(\d{4})", declarado["criterio"])
        if not m:
            raise ProtocoloInvalido("recorte temporal declarado sem ano legível "
                                    "('após o ano AAAA')")
        # "após o ano AAAA" inclui a partir de AAAA + 1. O teto é a data de execução.
        ano = int(m.group(1)) + 1
    ano = _parametro(params, "recorte_ano_min", ano, "padroes.recorte_ano_min")
    return {"ano_min": ano, "ano_max": None,
            "texto": declarado["criterio"] if declarado else ""}


def limiar(t, params):
    bloco = secao(t, "Acervos pessoais")
    valor = None
    if re.search(r"Regra de ajuste", bloco):
        m = re.search(r"recuperação inferior a\s+(\d+(?:[.,]\d+)?)\s*%", bloco)
        if not m:
            raise ProtocoloInvalido("regra de ajuste sem limiar legível "
                                    "('recuperação inferior a N%')")
        valor = _percentual(m.group(1))
    return _parametro(params, "limiar_aderencia", valor, "padroes.limiar_aderencia")


def ancoras(pal, params):
    marcadas = [f["id"] for f in pal if f["ancora"]] or None
    return _parametro(params, "ancoras", marcadas, "padroes.ancoras")


# ------------------------------------------------------------------------- fontes
def fontes(t):
    bloco = secao(t, "Fontes de informação")
    bases_bloco = secao(bloco, "Bases de dados")

    bases = []
    for linha in bases_bloco.splitlines():
        if not linha.lstrip().startswith("|"):
            continue
        cels = celulas(linha)
        if len(cels) < 3:
            continue
        m = re.match(r"^BD(\d+)$", cels[0])
        if not m:
            continue
        bases.append({"id": f"BD{int(m.group(1))}",
                      "nome": desescapa(cels[1]).strip(),
                      "papel": desescapa(cels[2]).strip()})
    _numeracao([b["id"] for b in bases], "BD", "bases")

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
    linha = linha[linha.index("Mapa por estudo"):] if linha else ""
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
    _numeracao([e["id"] for e in estudos], "SE", "referências")
    return estudos


def distribuicao(t, estudos):
    """Recalcula a distribuição do mapa e confere contra o parágrafo."""
    bloco = secao(t, "Acervos pessoais")
    por_base = {b: 0 for b in BASES}
    for e in estudos:
        for b in e["bases"]:
            if b not in por_base:
                raise ProtocoloInvalido(f"semente {e['id']}: base desconhecida {b!r}; "
                                        f"siglas de [fichas]: {list(BASES)}")
            por_base[b] += 1
    incidencias = sum(por_base.values())
    multi = sum(1 for e in estudos if len(e["bases"]) > 1)

    # A prosa declarada fica antes do mapa por estudo; o mapa não usa a forma "Sigla, n".
    prosa = bloco.split("Mapa por estudo")[0]
    siglas = "|".join(re.escape(b) for b in BASES)
    declarado = {b: int(v) for b, v in re.findall(r"\b(" + siglas + r"),\s*(\d+)", prosa)}
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

COR_FACETA = dict(CFG["cores"])
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


def execucao_base(slug, expressoes, curadas, executada):
    """O que se executa nesta base: uma, particionada em subconsultas ou curada.

    A expressão é a que o protocolo declara executada; a forma (única ou particionada)
    vem de `[fichas]` do config.toml, e a curada, da própria ficha.
    """
    expressao = executada
    if curadas:
        modo = "curada"
        itens = curadas
    else:
        modo = FICHAS[slug]["execucao"]
        if executada not in expressoes:
            raise ProtocoloInvalido(f"a ficha não traz a expressão executada {executada}")
        ex = expressoes[executada]
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
    execucao = execucao_base(slug, expressoes, curadas, d["executada"])
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


def _vocabulario(fid, d, decl):
    """Vocabulário de uma faceta para uma base.

    Devolve (vigentes, fora_da_string): `vigentes` são os termos da STR do protocolo nos
    idiomas e camadas que a ficha declara, classificados pelo quadro; `fora_da_string` são
    os termos do quadro da faceta, em qualquer idioma ou camada, que a STR não traz. O
    quadro é vocabulário de referência; o que vale para a busca é a STR.
    """
    f = next(x for x in d["tabelas"] if x["id"] == fid)
    idiomas = decl.get("idiomas", {}).get(fid) or list(IDIOMAS)
    camadas = CAMADAS if decl.get("camadas") == "todas" else ("nucleo",)
    na_str = {normaliza(x) for x in d["strings"][fid]["termos"]}
    tabela = _sem_repeticao([x for i in idiomas for c in camadas
                             for x in f["camadas"][i][c]])
    vigentes = [x for x in tabela if normaliza(x) in na_str]
    quadro = _sem_repeticao([x for i in IDIOMAS for c in CAMADAS for x in f["camadas"][i][c]])
    fora = [x for x in quadro if normaliza(x) not in na_str]
    return vigentes, fora


def _facetas_da_composicao(d, ident):
    """Facetas exigidas por uma expressão, pela composição lida do protocolo."""
    faceta_de = {s["id"]: fid for fid, s in d["strings"].items()}
    return sorted({faceta_de[x] for g in d["expressoes"][ident] for x in g})


def cobertura_base(slug, base, d):
    """Problemas de forma da base: vocabulário, âncoras, composição, execução."""
    problemas = []
    decl = base.get("declaracao") or {}
    modos = set(decl.get("derivacoes") or [])

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
            # inteira. É declaração da ficha, não omissão silenciosa: a cobertura literal
            # continua sendo reportada, e o que a regra não alcança tem de estar na tabela.
            if "radical" in modos and any(_radical_alcanca(termo, a) for a in achados):
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
            if so_quadro:
                problemas.append(f"{fid}: {termo!r} está na string desta base e não está na "
                                 f"string do protocolo (consta só do quadro: {so_quadro!r})")
                continue
            # Derivar por radical é ser raiz de um termo vigente: estar contido nele.
            if "radical" in modos and any(_radical_alcanca(p, termo) for p in esperados):
                continue
            problemas.append(f"{fid}: {termo!r} está na string desta base e não deriva do "
                             f"protocolo")
    for e, porque in _radical_sem_alcance(base):
        problemas.append(f"{e['faceta']}: {e['termo']!r} consta da redução como alcançado "
                         f"pela forma radical, e {porque}")

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

    execucao = base["execucao"]
    if execucao["expressao"] != d["executada"]:
        problemas.append(f"a base executa {execucao['expressao']}, e o protocolo declara "
                         f"executada {d['executada']}")
    if execucao["modo"] not in ("curada",) + MODOS_EXECUCAO:
        problemas.append(f"modo de execução desconhecido: {execucao['modo']!r}")
    if not execucao["itens"]:
        problemas.append("execução sem consulta legível")
    return problemas


def cobertura_por_faceta(slug, base, d):
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
    params = {}
    pal = palavras(t)
    tb = tabelas(t)
    st = strings(t)
    for n in st:
        # A string repete termo entre camadas; a lista executada é deduplicada. É ela
        # que a derivação local usa, e é ela que o relatório conta.
        st[n]["termos"] = _sem_repeticao(st[n]["termos"])
    comp, exec_, sonda, sens = expressoes(t, params)
    crit = criterios(t)
    est = sementes(t)
    d = {
        "questoes": questoes(t),
        "facetas": pal,
        "ancoras": ancoras(pal, params),
        "tabelas": tb,
        "instrumentos": instrumentos(t),
        "strings": st,
        "expressoes": comp,
        "executada": exec_,
        "sonda": sonda,
        "sensibilidade": sens,
        "criterios": crit,
        "recorte": recorte(t, params),
        "fontes": fontes(t),
        "limiar": limiar(t, params),
        "sementes": est,
        "distribuicao": distribuicao(t, est),
    }
    # O protocolo não declara estes; valem os do config.toml, com a origem registrada.
    d["divergencia"] = _parametro(params, "divergencia_fidelidade", None,
                                  "padroes.divergencia_fidelidade")
    d["calibracao_triagem"] = _parametro(params, "calibracao_triagem", None,
                                         "padroes.calibracao_triagem")
    _parametro(params, "minimo_termos_string", None, "conferencia.minimo_termos_string")
    _parametro(params, "dimensoes_criterio", None, "conferencia.dimensoes_criterio")
    d["parametros"] = params
    return d


# ---------------------------------------------------------------------- conferência
def _coerencia_expressoes(d):
    """Relações entre as expressões, sem valor esperado: âncoras, sonda e executada."""
    problemas = []
    comp, exec_, sonda = d["expressoes"], d["executada"], d["sonda"]
    str_de = {fid: s["id"] for fid, s in d["strings"].items()}
    existentes = set(str_de.values())
    ausentes = [a for a in d["ancoras"] if a not in str_de]
    if ausentes:
        return [f"âncoras {ausentes} não são facetas com string no protocolo"]
    ancora = [[str_de[a]] for a in d["ancoras"]]

    for ident, grupos in sorted(comp.items()):
        fora = sorted({x for g in grupos for x in g} - existentes)
        if fora:
            problemas.append(f"{ident}: composição cita string inexistente {fora}")
        for g in ancora:
            if g not in grupos:
                problemas.append(f"{ident}: falta a âncora obrigatória {g[0]}")
    if sorted(comp.get(sonda, [])) != sorted(ancora):
        problemas.append(f"a sonda {sonda} não é a conjunção das âncoras "
                         f"({' + '.join(g[0] for g in ancora)})")
    resto = [g for g in comp.get(exec_, []) if g not in ancora]
    especificas = {k: [g for g in v if g not in ancora] for k, v in comp.items()
                   if k not in (exec_, sonda)}
    especificas = {k: v[0][0] for k, v in especificas.items() if len(v) == 1 and len(v[0]) == 1}
    uniao = sorted(set(especificas.values()))
    if len(resto) != 1 or not uniao or sorted(resto[0]) != uniao:
        problemas.append(f"a executada {exec_} não é a união das específicas "
                         f"{sorted(especificas)}: além das âncoras tem {resto}, "
                         f"esperado [{uniao}]")
    return problemas


def conferir(t=None):
    """Problemas encontrados. Lista vazia = documento coerente."""
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
        # Repetição entre camadas é legítima (o mesmo termo em núcleo e em relacionados);
        # a lista final é deduplicada. Dentro da mesma camada, é defeito.
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

    # A string só pode usar termo que o quadro da própria faceta contém. É a remissão que
    # impede string e vocabulário de divergirem em silêncio.
    minimo = d["parametros"]["minimo_termos_string"]["valor"]
    quadro = {f["id"]: {normaliza(x) for i in IDIOMAS for x in f["termos"][i]}
              for f in d["tabelas"]}
    for n, s in d["strings"].items():
        if len(s["termos"]) < minimo:
            problemas.append(f"faceta {n}: string com {len(s['termos'])} termos "
                             f"(mínimo {minimo})")
        for termo in s["termos"]:
            if normaliza(termo) not in quadro[n]:
                problemas.append(f"faceta {n}: termo {termo!r} da string não consta do "
                                 f"quadro da faceta")

    problemas += _coerencia_expressoes(d)

    dimensoes = {c["dimensao"] for c in d["criterios"]}
    for esperada in d["parametros"]["dimensoes_criterio"]["valor"]:
        if esperada not in dimensoes:
            problemas.append(f"critério de {esperada!r} não declarado (dimensões do "
                             f"protocolo: {sorted(dimensoes)})")
    lo, hi = d["sensibilidade"]
    if not 0 <= lo < hi <= 1:
        problemas.append(f"faixa de sensibilidade incoerente: {lo:.0%} a {hi:.0%}")
    if not 0 < d["limiar"] <= 1:
        problemas.append(f"limiar de aderência incoerente: {d['limiar']:.0%}")

    if d["fontes"]["ordem_execucao"] != [b["nome"] for b in d["fontes"]["bases"]]:
        problemas.append(f"ordem de execução {d['fontes']['ordem_execucao']} difere da "
                         f"numeração das bases")
    bds = {b["id"] for b in d["fontes"]["bases"]}
    com_ficha = {f["bd"] for f in FICHAS.values()}
    for slug, f in FICHAS.items():
        if f["bd"] not in bds:
            problemas.append(f"ficha {slug} ({CONFIG.name}) aponta {f['bd']}, que não é base "
                             f"do protocolo")
    for bd in sorted(bds - com_ficha):
        problemas.append(f"base {bd} do protocolo sem ficha em [fichas] do {CONFIG.name}")

    if not d["questoes"]["questao_principal"]:
        problemas.append("questão geral vazia")

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
    return problemas


def _composicao_legivel(grupos):
    """`[["STR1"],["STR2"],["STR3","STR4"]]` como `1+2+(3|4)`."""
    partes = []
    for g in grupos:
        nomes = [x[3:] for x in g]
        partes.append(nomes[0] if len(nomes) == 1 else "(" + "|".join(nomes) + ")")
    return "+".join(partes)


def _legivel(valor):
    if isinstance(valor, float):
        return f"{valor:.0%}"
    if isinstance(valor, list) and valor and all(isinstance(x, float) for x in valor):
        return " a ".join(f"{x:.0%}" for x in valor)
    if isinstance(valor, dict):
        return ", ".join(f"{k}={_composicao_legivel(v)}" for k, v in sorted(valor.items()))
    if isinstance(valor, list):
        return ", ".join(str(x) for x in valor)
    return str(valor)


def relatorio(d):
    L = [f"  protocolo: {CFG['protocolo']}  (chave `protocolo` do {CONFIG.name})"]
    L.append(f"  questão: 1 geral, {len(d['questoes']['questoes_especificas'])} específicas")
    for f in d["tabelas"]:
        n_string = len(d["strings"][f["id"]]["termos"])
        n_bruto = sum(len(f["termos"][i]) for i in IDIOMAS)
        insts = ", ".join(f"{i['sigla']}({'/'.join(i['idiomas'])}"
                          f"{', manual' if i['modo'] == 'manual' else ''})"
                          for i in d["instrumentos"][f["id"]])
        L.append(f"  faceta {f['id']} — {f['nome'][:52]:<54} "
                 f"tabela {n_bruto:>3} formas / string {n_string:>3} termos   "
                 f"instrumentos: {insts}")
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
    L.append("  parâmetros em uso:")
    for nome, p in d["parametros"].items():
        L.append(f"    {nome:<24} {_legivel(p['valor'])[:70]:<72} [{p['origem']}]")
    return "\n".join(L)


def relatorio_bases(bases, d):
    """Uma linha por base. Cobertura é número, não aprovação: mede o preço de cada forma."""
    L = ["", "  Bases — forma lida da ficha; cobertura medida contra a string do protocolo:"]
    for slug, base in bases:
        cob = cobertura_por_faceta(slug, base, d)
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
    faltam = [b for b in BDS if b not in bases]
    if faltam:
        return [f"registro_execucao.json sem as bases {faltam}"]

    problemas = []
    for bd in BDS:
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
            problemas += [f"{slug}: {p}" for p in cobertura_base(slug, base, d)]
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
        for bd in BDS:
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
        manuais = sum(1 for r in linhas_validacao
                      if (r.get("status_proposto") or "").strip() == STATUS_MANUAL)
        if manuais:
            linhas.append(f"[validação] {manuais} linha(s) {STATUS_MANUAL} — consultar o "
                          f"instrumento e registrar na planilha")

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
# Os valores literais abaixo são os do documento corrente: o autoteste os altera para
# injetar defeito. Mutação que não se aplica é falha do autoteste, não aprovação.

def _troca_linha(linhas, prefixo, de, para):
    return [l.replace(de, para, 1) if l.startswith(prefixo) else l for l in linhas]


def _mutacoes(t):
    """Cópias defeituosas: (nome, texto, trecho esperado na reprovação)."""
    linhas = t.splitlines()
    i_rel = next(i for i, l in enumerate(linhas)
                 if l.startswith("| *Termos relacionados") and "modelo conceitual" in l)
    i_nuc = next(i for i, l in enumerate(linhas) if l.startswith("| *Termos centrais")
                 and "representação do conhecimento" in l)
    duplicada = list(linhas)
    duplicada[i_nuc] = duplicada[i_nuc].replace(
        "\\- representação do conhecimento \\- organização do conhecimento",
        "\\- representação do conhecimento \\- representação do conhecimento "
        "\\- organização do conhecimento", 1)

    casos = [
        ("linha de faceta removida", linhas[:i_rel] + linhas[i_rel + 1:],
         "camada relacionados vazia"),
        ("string fora do padrão OR",
         _troca_linha(linhas, "| STR2 |", " OR ", ", "), "fora do padrão"),
        ("semente ausente", [l for l in linhas if not l.startswith("- SE10:")], "prosa diz"),
        ("distribuição contradita", [l.replace("Scopus, 6;", "Scopus, 7;", 1) for l in linhas],
         "prosa diz"),
        ("termo duplicado na faceta", duplicada, "repetido na mesma camada"),
        ("questão geral removida",
         [l for l in linhas if l.strip() != "### Questão geral de revisão"], "Questão geral"),
        ("QER fora de numeração", [l for l in linhas if not l.startswith("- QER3:")],
         "numeração QER"),
        ("dimensão de critério ausente",
         _troca_linha(linhas, "| CE3 |", "| Idioma |", "| Língua |"), "critério de 'Idioma'"),
        ("base removida", [l for l in linhas if not l.startswith("| BD4 |")], "BRAPCI"),
        ("questão geral sem QGR", [l.replace("- QGR:", "", 1) for l in linhas], "QGR"),
        ("faceta com identificador trocado",
         [l.replace("Faceta 2 (FCT2)", "Faceta 2 (FCT3)", 1) for l in linhas],
         "não corresponde"),
        ("string apontando para outra faceta",
         [l.replace("| STR2 | FCT2", "| STR2 | FCT3", 1) for l in linhas], "não casam"),
        ("critério com identificador repetido",
         [l.replace("| CE3 |", "| CE2 |", 1) for l in linhas], "numeração CE"),
        ("base com identificador repetido",
         [l.replace("| BD3 |", "| BD2 |", 1) for l in linhas], "numeração BD"),
        ("semente fora de numeração",
         [l.replace("- SE10:", "- SE11:", 1) for l in linhas], "numeração SE"),
        # Coerência das expressões.
        ("âncora desmarcada",
         _troca_linha(linhas, "- Faceta 2 (FCT2)", " — âncora obrigatória 2", ""),
         "conjunção das âncoras"),
        ("executada que não é a união das específicas",
         _troca_linha(linhas, "| EB4 |", "(STR3 OR STR4)", "STR3"), "não é a união"),
        ("sonda que não é a conjunção das âncoras",
         _troca_linha(linhas, "| EB5 |", "STR1 \\+ STR2\\ |", "STR1 \\+ STR2 \\+ STR3\\ |"),
         "conjunção das âncoras"),
        ("expressão sem âncora",
         _troca_linha(linhas, "| EB2 |", "STR1 \\+ STR2 \\+ STR3", "STR1 \\+ STR3"),
         "falta a âncora"),
        ("duas expressões executadas",
         _troca_linha(linhas, "| EB2 |", "| Específica |", "| Cobertura restrita |"),
         "mais de uma expressão"),
        ("termo da string fora do quadro",
         _troca_linha(linhas, "| STR1 |", '("representação do conhecimento" OR ',
                      '("termo inventado" OR "representação do conhecimento" OR '),
         "não consta do quadro"),
        # Parâmetros lidos do protocolo: incoerente ou ilegível reprova, sem cair no padrão.
        ("faixa de sensibilidade incoerente",
         _troca_linha(linhas, "| EB5 |", "**< 5%**", "**< 25%**"), "incoerente"),
        ("faixa de sensibilidade ilegível",
         _troca_linha(linhas, "| EB5 |", "**> 15%**", "acima do teto"), "falta o limite"),
        ("limiar de aderência ilegível",
         _troca_linha(linhas, "- Regra de ajuste:", "inferior a 80%",
                      "inferior a oitenta por cento"), "limiar legível"),
        ("recorte temporal ilegível",
         _troca_linha(linhas, "| CE1 |", "após o ano 2016", "após o ano de dois mil"),
         "sem ano legível"),
        # Instrumentos.
        ("instrumento sem cadastro na configuração",
         _troca_linha(linhas, "- FCT1:", "UNESCO Thesaurus", "UNESCO Thesaurus, Tesauro X"),
         "não consta de [instrumentos]"),
        ("faceta sem linha de instrumentos", [l for l in linhas if not l.startswith("- FCT4:")],
         "sem linha"),
        ("instrumento ambíguo",
         _troca_linha(linhas, "- FCT2:", "ERIC Thesaurus,", "ERIC Thesaurus UNESCO Thesaurus,"),
         "mais de um instrumento"),
    ]
    return [(nome, "\n".join(ls), espera) for nome, ls, espera in casos]


def _autoteste_precedencia(t):
    """Parâmetro ausente do protocolo vale pelo padrão, com a origem registrada."""
    falhas, n = 0, 0
    casos = [
        ("limiar ausente do protocolo vale pelo padrão", "limiar_aderencia",
         [l for l in t.splitlines() if not l.startswith("- Regra de ajuste:")]),
        ("âncoras não marcadas valem pelo padrão", "ancoras",
         [re.sub(r" — âncora obrigatória \d", "", l) for l in t.splitlines()]),
    ]
    for nome, param, linhas in casos:
        n += 1
        mutante = "\n".join(linhas)
        if mutante == t:
            print(f"  [FALHA] mutação não aplicada: {nome}")
            falhas += 1
            continue
        try:
            p = analisa(mutante)["parametros"][param]
        except ProtocoloInvalido as e:
            print(f"  [FALHA] {nome}: leitura reprovou ({e})")
            falhas += 1
            continue
        if p["origem"] == ORIGEM_PADRAO and p["valor"] == _valor(CFG, f"padroes.{param}"):
            print(f"  [ok] {nome}")
        else:
            print(f"  [FALHA] {nome}: {p}")
            falhas += 1
    return falhas, n


def _autoteste_config():
    """Configuração ausente, inválida ou incompleta reprova com mensagem nomeada."""
    import tempfile
    falhas, n = 0, 0

    def testa(nome, func, espera):
        nonlocal falhas, n
        n += 1
        try:
            func()
        except ConfiguracaoInvalida as e:
            if espera in str(e):
                print(f"  [ok] reprovou: {nome} — {str(e)[:80]}")
                return
            print(f"  [FALHA] {nome}: reprovou por outro motivo — {e}")
        else:
            print(f"  [FALHA] aprovou indevidamente: {nome}")
        falhas += 1

    def sem(chave):
        c = copy.deepcopy(CFG)
        partes = chave.split(".")
        alvo = c
        for p in partes[:-1]:
            alvo = alvo[p]
        del alvo[partes[-1]]
        return lambda: valida_config(c)

    def com(chave, valor):
        c = copy.deepcopy(CFG)
        partes = chave.split(".")
        alvo = c
        for p in partes[:-1]:
            alvo = alvo[p]
        alvo[partes[-1]] = valor
        return lambda: valida_config(c)

    testa("chave exigida ausente", sem("padroes.limiar_aderencia"),
          "padroes.limiar_aderencia")
    testa("caminho do protocolo ausente", sem("protocolo"), "`protocolo`")
    testa("ficha sem arquivo", sem(f"fichas.{next(iter(FICHAS))}.arquivo"), "arquivo")
    primeiro = next(iter(CFG["instrumentos"]))
    c = copy.deepcopy(CFG)
    c["instrumentos"][primeiro]["modo"] = "outro"
    testa("instrumento com modo desconhecido", lambda: valida_config(c), "modo")
    testa("faixa padrão invertida", com("padroes.sensibilidade", [0.15, 0.05]), "inferior")
    with tempfile.TemporaryDirectory() as tmp:
        ruim = pathlib.Path(tmp) / "config.toml"
        ruim.write_text("protocolo = \n", encoding="utf-8")
        testa("arquivo que não é TOML", lambda: carrega_config(ruim), "não é TOML válido")
        testa("arquivo ausente", lambda: carrega_config(pathlib.Path(tmp) / "nada.toml"),
              "ausente")
    return falhas, n


def _autoteste_dados(d):
    """Prova que a conferência dos arquivos alimentados reprova cada defeito esperado."""
    sem, erro_s = _le_json(SEMENTES)
    reg, erro_r = _le_json(REGISTRO)
    if erro_s or erro_r:
        print("  [--] arquivos alimentados ausentes: o teste das conferências não foi "
              "executado")
        return 0, 0
    falhas, n = 0, 0

    def testa(nome, condicao):
        nonlocal falhas, n
        n += 1
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
    copia["estudos"][0].pop(CAMPOS_AUTORAIS[0], None)
    p, _ = _problemas_sementes(copia, d)
    testa("semente sem campo de conferência", bool(p))

    copia = copy.deepcopy(sem)
    copia["estudos"].append({"id": "SE99", "ligacao": "ti:semente inventada",
                             **{c: "" for c in CAMPOS_AUTORAIS}})
    _, a = _problemas_sementes(copia, d)
    testa("semente fora do protocolo com metadados preservados", bool(a))

    copia = copy.deepcopy(reg)
    del copia["bases"][BDS[0]]
    testa("registro sem uma das bases", bool(_problemas_registro(copia)))

    copia = copy.deepcopy(reg)
    copia["bases"][BDS[0]]["execucoes"].append({
        "id": "EX99", "expressao": d["executada"], "arquivo": "data/execucoes/ausente.ris",
        "registros_lidos": 1, "status": "valida"})
    testa("execução apontando arquivo de exportação ausente",
          bool(_problemas_registro(copia)))

    copia = copy.deepcopy(reg)
    copia["bases"][BDS[0]]["execucoes"].append({
        "id": "EX99", "expressao": d["executada"], "arquivo": str(REGISTRO.relative_to(RAIZ)),
        "registros_lidos": "um", "status": "valida"})
    testa("execução com `registros_lidos` que não é inteiro",
          bool(_problemas_registro(copia)))
    return falhas, n


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
            return cobertura_base(s, base, d)
        except ProtocoloInvalido as e:
            return [str(e)]

    def testa(nome, t_ficha, s=None, base_texto=None, espera=None):
        nonlocal falhas, n
        n += 1
        if t_ficha == (base_texto if base_texto is not None else original):
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
          original.replace('TS=("representação do conhecimento" OR ', 'TS=(', 1),
          espera="não consta da redução")
    testa("termo inventado acrescentado à string da base",
          original.replace('TS=("representação do conhecimento" OR ',
                           'TS=("invented search term" OR "representação do conhecimento" OR ',
                           1), espera="não deriva do protocolo")
    # O termo do quadro que a STR não traz continua no quadro; "deriva do quadro" não basta
    # para a base executá-lo.
    testa("termo só do quadro devolvido à string da base",
          original.replace('TS=("representação do conhecimento" OR ',
                           'TS=("modelo conceitual" OR "representação do conhecimento" OR ', 1),
          espera="não está na string do protocolo")
    brapci = ficha("brapci")
    testa("termo só do quadro, em flexão, na string da BRAPCI",
          brapci.replace('("educação" OR ', '("educação" OR "educativos" OR ', 1),
          "brapci", brapci, "não está na string do protocolo")
    testa("expressão com faceta trocada",
          original.replace("**Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧)",
                           "**Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥)", 1),
          espera="do protocolo")
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
    # não alcança `faceted taxonomy`.
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
    m2 = re.sub(r"^(\| FCT1 \|)", "| FCT1 | domain ontology | alcançado pela forma radical "
                "declarada |\n\\1", controle, count=1, flags=re.M)
    testa("motivo radical sem derivação radical declarada",
          m2.replace("| derivações | morfologia e radical |",
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
    for nome, mutante, espera in mut:
        if mutante == t:
            print(f"  [FALHA] mutação não aplicada: {nome}")
            falhas += 1
            continue
        problemas = [p for p in conferir(mutante) if espera in p]
        if problemas:
            print(f"  [ok] reprovou: {nome} — {problemas[0][:90]}")
        else:
            print(f"  [FALHA] não reprovou pelo motivo esperado ({espera!r}): {nome} — "
                  f"{conferir(mutante)[:1]}")
            falhas += 1
    d = analisa(t)
    f_p, n_p = _autoteste_precedencia(t)
    f_c, n_c = _autoteste_config()
    f_d, n_d = _autoteste_dados(d)
    f_b, n_b = _autoteste_bases(d)
    falhas += f_p + f_c + f_d + f_b
    if falhas:
        print(f"\n{falhas} caso(s) do autoteste falharam.")
        return 1
    print(f"\n{len(mut)} defeitos injetados no documento, {n_p} casos de precedência, "
          f"{n_c} de configuração, {n_d} nas conferências dos arquivos alimentados e {n_b} "
          f"nas fichas das bases, todos com o resultado esperado.")
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
