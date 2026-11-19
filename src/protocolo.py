#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O protocolo como fonte: lê o documento, confere e sincroniza o que é alimentado.

O documento do protocolo (caminho na chave `protocolo` do `config.toml`) é a fonte única
da questão, das facetas, do vocabulário, das strings, das expressões, dos critérios, das
fontes, dos instrumentos de controle terminológico e do conjunto-semente. A forma de cada
base está na respectiva ficha, localizada pela sigla da tabela "Bases de dados" e pelo
padrão `[documentos] ficha` do `config.toml`. Este script lê as fontes em memória e NÃO
grava derivado algum.

Parâmetros estruturais — composição das expressões, instrumentos, bases, conjunto-semente
e idiomas do quadro — vêm só do protocolo, e a forma de execução, só da ficha: sem padrão,
a ausência ou o valor inválido reprova. As tabelas estruturais são lidas pelo nome da
coluna, não pela posição. Os demais parâmetros têm valor padrão no `config.toml`; o que o
protocolo declara prevalece, e trecho presente e ilegível reprova, sem cair no padrão.
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
import urllib.parse

if sys.version_info < (3, 11):
    raise SystemExit("src/protocolo.py exige Python 3.11 ou superior (tomllib, para ler "
                     "config.toml).")
import tomllib                                                      # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
# Único caminho fixado: o da configuração, na raiz. Todo o resto sai dela.
CONFIG = RAIZ / "config.toml"

# Chaves exigidas do config.toml. É o esquema do arquivo, não parâmetro do projeto.
CHAVES_CONFIG = (
    "protocolo",
    "padroes.recorte_ano_min", "padroes.limiar_aderencia", "padroes.sensibilidade",
    "padroes.ancoras", "padroes.executada", "padroes.sonda",
    "padroes.divergencia_fidelidade", "padroes.calibracao_triagem",
    "expressoes.natureza_executada", "expressoes.natureza_sonda", "expressoes.colunas",
    "conferencia.minimo_termos_string", "conferencia.dimensoes_criterio",
    "dados.sementes", "dados.registro", "dados.validacao",
    "documentos.ficha",
    "planilha.campos_validacao", "planilha.campos_autorais",
)
# Parâmetros estruturais: lidos só do protocolo (ou da ficha), sem padrão. A presença de
# qualquer um no config.toml reprova, para que não haja segunda fonte que divirja em
# silêncio.
CHAVES_RETIRADAS = ("padroes.composicao", "cores", "fichas", "instrumentos", "idiomas")
MARCA_SIGLA = "{sigla}"


class ConfiguracaoInvalida(Exception):
    """O config.toml não existe, não é TOML válido ou não tem uma chave exigida."""


def _valor(cfg, chave):
    atual = cfg
    for parte in chave.split("."):
        if not isinstance(atual, dict) or parte not in atual:
            raise ConfiguracaoInvalida(f"{CONFIG.name}: falta a chave `{chave}`")
        atual = atual[parte]
    return atual


def _tem(cfg, chave):
    try:
        _valor(cfg, chave)
        return True
    except ConfiguracaoInvalida:
        return False


def valida_config(cfg):
    """Confere o esquema da configuração; levanta ConfiguracaoInvalida no primeiro defeito."""
    for chave in CHAVES_RETIRADAS:
        if _tem(cfg, chave):
            raise ConfiguracaoInvalida(
                f"{CONFIG.name}: a chave `{chave}` não pertence mais à configuração — o "
                f"valor vem do protocolo (parâmetro estrutural, sem padrão); retirá-la")
    for chave in CHAVES_CONFIG:
        _valor(cfg, chave)
    padrao_ficha = cfg["documentos"]["ficha"]
    if not isinstance(padrao_ficha, str) or MARCA_SIGLA not in padrao_ficha:
        raise ConfiguracaoInvalida(f"{CONFIG.name}: `documentos.ficha` {padrao_ficha!r} não "
                                   f"contém {MARCA_SIGLA}: a ficha é localizada pela sigla")
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

# Arquivos alimentados: não são derivados de markdown e não se regeram.
SEMENTES = RAIZ / CFG["dados"]["sementes"]
REGISTRO = RAIZ / CFG["dados"]["registro"]
CSV_VALIDACAO = RAIZ / CFG["dados"]["validacao"]

CAMADAS = ("nucleo", "proximos", "relacionados")

# Rótulos das linhas do quadro: gramática do leitor, não parâmetro do projeto.
ROTULO_CAMADA = {
    "Termos centrais": "nucleo",
    "Descritores potenciais": "proximos",
    "Termos relacionados": "relacionados",
}

# Cabeçalhos exigidos das tabelas estruturais: contrato de formato do leitor, como
# ROTULO_CAMADA. Coluna extra (ex.: Justificativa) é ignorada.
COLUNAS_BASES = ("ID Base", "Sigla", "Nome da base")
COLUNAS_INSTRUMENTOS = ("Sigla", "Instrumento", "Modo", "Caminho", "Idiomas", "FCTs")
COLUNAS_SEMENTES = ("ID Semente", "Semente", "Bases")
MODO_MANUAL, MODO_AUTOMATICO = "Manual", "Automático"
MODOS_INSTRUMENTO = (MODO_MANUAL, MODO_AUTOMATICO)
# Forma de execução declarada na ficha (`- Execução: ...`) → valor interno.
FORMAS_EXECUCAO = {"única": "unica", "particionada": "particionada"}
MODOS_EXECUCAO = tuple(FORMAS_EXECUCAO.values())

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


# ------------------------------------------------------------------- tabelas
def blocos_de_tabela(bloco):
    """Tabelas Markdown de um trecho: cada uma, a lista das suas linhas consecutivas."""
    saida, atual = [], []
    for linha in bloco.splitlines():
        if linha.lstrip().startswith("|"):
            atual.append(linha)
        elif atual:
            saida.append(atual)
            atual = []
    if atual:
        saida.append(atual)
    return saida


def _separador(cels):
    return bool(cels) and all(re.fullmatch(r":?-+:?", c) for c in cels)


def le_tabela(linhas, exigidas, onde):
    """Linhas de uma tabela como dicionários indexados pelo nome da coluna.

    Devolve (cabeçalho, linhas). Coluna exigida ausente ou coluna repetida reprova; coluna
    extra é ignorada. Os valores são as células brutas: o escape do Markdown fica para
    quem lê cada coluna.
    """
    cab = [desescapa(c).strip() for c in celulas(linhas[0])]
    repetidas = sorted({c for c in cab if c and cab.count(c) > 1})
    if repetidas:
        raise ProtocoloInvalido(f"{onde}: coluna repetida {repetidas}")
    faltam = [c for c in exigidas if c not in cab]
    if faltam:
        raise ProtocoloInvalido(f"{onde}: falta a coluna {faltam}; cabeçalho lido {cab}")
    corpo = linhas[1:]
    if corpo and _separador(celulas(corpo[0])):
        corpo = corpo[1:]
    saida = []
    for linha in corpo:
        cels = celulas(linha)
        sobra = [c for c in cels[len(cab):] if c]
        if sobra:
            raise ProtocoloInvalido(f"{onde}: linha com mais células que o cabeçalho: "
                                    f"{linha.strip()[:60]!r}")
        saida.append({c: (cels[i] if i < len(cels) else "")
                      for i, c in enumerate(cab) if c})
    return cab, saida


def tabela_da_secao(t, titulo, exigidas):
    """A tabela de uma seção do protocolo, lida pelo cabeçalho."""
    tabelas_ = blocos_de_tabela(secao(t, titulo))
    if not tabelas_:
        raise ProtocoloInvalido(f"tabela '{titulo}' ausente")
    return le_tabela(tabelas_[0], exigidas, f"tabela '{titulo}'")[1]


def _lista(celula):
    """Itens de uma célula separados por vírgula."""
    return [x.strip() for x in desescapa(celula).split(",") if x.strip()]


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


def _estrutural(params, nome, valor):
    """Parâmetro estrutural: só do protocolo. O leitor já reprovou a ausência."""
    params[nome] = {"valor": valor, "origem": ORIGEM_PROTOCOLO}
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
    """Nome e papel de cada faceta: `Faceta n (FCTn): nome [(âncora obrigatória k)]`.

    O nome é todo o resto da linha, hífens incluídos; o sufixo de âncora, entre parênteses,
    é opcional. Travessão residual (forma antiga, com cor) e parêntese de âncora mal formado
    reprovam: leitura tolerante faria a cor ou o sufixo entrarem no nome em silêncio.
    """
    bloco = secao(t, "Palavras significativas da questão de revisão")
    saida = []
    for m in re.finditer(r"^-\s*Faceta\s+(\d+)\s*(?:\((FCT\d+)\))?\s*:\s*(.+)$", bloco, re.M):
        n = int(m.group(1))
        codigo = m.group(2) or ""
        if codigo != f"FCT{n}":
            achado = codigo if codigo else "ausente"
            raise ProtocoloInvalido(
                f"faceta {n}: identificador {achado!r} não corresponde a FCT{n}")
        corpo = desescapa(m.group(3)).strip()
        if "—" in corpo:
            raise ProtocoloInvalido(f"faceta FCT{n}: travessão na linha ({corpo!r}); a forma é "
                                    f"`Faceta {n} (FCT{n}): nome (âncora obrigatória k)`")
        ma = re.search(r"\s*\(\s*âncora obrigatória\s+(\d+)\s*\)\s*$", corpo)
        nome = corpo[:ma.start()].strip() if ma else corpo
        if re.search(r"âncora", nome, re.I):
            raise ProtocoloInvalido(f"faceta FCT{n}: âncora fora da forma "
                                    f"`(âncora obrigatória k)` no fim da linha: {corpo!r}")
        if not nome:
            raise ProtocoloInvalido(f"faceta FCT{n}: sem nome")
        saida.append({"id": f"FCT{n}", "nome": nome, "ancora": bool(ma)})
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
    """As tabelas do controle terminológico, uma por faceta, com as camadas por idioma.

    O cabeçalho `| FCTn | pt | en | es |` dá a faceta e os idiomas: o idioma de cada coluna
    é o nome no cabeçalho, não a posição. O primeiro quadro fixa a ordem dos idiomas do
    projeto; os demais têm de ter o mesmo conjunto, em qualquer ordem.

    Devolve (tabelas, idiomas).
    """
    nomes = {f["id"]: f for f in palavras(t)}
    bloco = secao(t, "Controle terminológico")

    saida, idiomas = [], None
    for linhas in blocos_de_tabela(bloco):
        m = re.match(r"^FCT(\d+)$", celulas(linhas[0])[0])
        if not m:
            continue
        ident = f"FCT{int(m.group(1))}"
        if ident not in nomes:
            raise ProtocoloInvalido(f"tabela da faceta {ident} sem palavra significativa")
        cab, linhas_ = le_tabela(linhas, (), f"quadro de {ident}")
        proprios = cab[1:]
        if not proprios or any(not i for i in proprios):
            raise ProtocoloInvalido(f"quadro de {ident}: coluna de idioma sem nome no "
                                    f"cabeçalho {cab}")
        if idiomas is None:
            idiomas = tuple(proprios)
        elif set(proprios) != set(idiomas):
            raise ProtocoloInvalido(
                f"quadro de {ident}: idiomas {sorted(proprios)} diferem dos idiomas "
                f"{sorted(idiomas)} do quadro de {saida[0]['id']} — faltam "
                f"{sorted(set(idiomas) - set(proprios))}, sobram "
                f"{sorted(set(proprios) - set(idiomas))}")
        atual = {"id": ident, "nome": nomes[ident]["nome"], "ancora": nomes[ident]["ancora"],
                 "camadas": {i: {c: [] for c in CAMADAS} for i in idiomas}}
        saida.append(atual)
        for linha in linhas_:
            rotulo = linha[cab[0]].strip("* ").strip()
            camada = next((v for k, v in ROTULO_CAMADA.items() if rotulo.startswith(k)), None)
            if camada is None:
                continue
            for idioma in idiomas:
                atual["camadas"][idioma][camada] = _termos_celula(linha[idioma])

    ids = [f["id"] for f in saida]
    if sorted(ids) != sorted(nomes) or len(set(ids)) != len(ids):
        raise ProtocoloInvalido(f"esperava uma tabela por faceta ({sorted(nomes)}), "
                                f"achei {ids}")
    for f in saida:
        f["termos"] = {i: _sem_repeticao(
            [x for c in CAMADAS for x in f["camadas"][i][c]]) for i in idiomas}
    return saida, idiomas


# -------------------------------------------------------------------- instrumentos
SECAO_INSTRUMENTOS = "Instrumentos para controle terminológico"


def clientes_automaticos():
    """Siglas com cliente automatizado, do registro `CLIENTES` de validar_termos.py.

    Importação tardia: validar_termos importa este módulo na carga, e o registro de
    clientes é conhecimento da ferramenta, não parâmetro do projeto.
    """
    pasta = str(pathlib.Path(__file__).resolve().parent)
    if pasta not in sys.path:
        sys.path.insert(0, pasta)
    import validar_termos                                           # noqa: PLC0415
    return sorted(validar_termos.CLIENTES)


def instrumentos(t, ids_facetas, idiomas):
    """Instrumentos da tabela `Sigla | Instrumento | Modo | Caminho | Idiomas | FCTs`.

    Devolve (por sigla, por faceta). Sem padrão: toda faceta do quadro tem de constar da
    coluna FCTs de algum instrumento, e instrumento `Automático` tem de ter cliente com o
    nome da sua sigla.
    """
    onde = f"tabela '{SECAO_INSTRUMENTOS}'"
    por_sigla = {}
    for linha in tabela_da_secao(t, SECAO_INSTRUMENTOS, COLUNAS_INSTRUMENTOS):
        valores = {c: desescapa(linha[c]).strip() for c in COLUNAS_INSTRUMENTOS}
        sigla = valores["Sigla"] or "?"
        vazios = [c for c, v in valores.items() if not v]
        if vazios:
            raise ProtocoloInvalido(f"{onde}, linha {sigla}: campo vazio {vazios}")
        if sigla in por_sigla:
            raise ProtocoloInvalido(f"{onde}: sigla repetida {sigla!r}")
        if valores["Modo"] not in MODOS_INSTRUMENTO:
            raise ProtocoloInvalido(f"{onde}, linha {sigla}: Modo {valores['Modo']!r} fora "
                                    f"dos admitidos {list(MODOS_INSTRUMENTO)}")
        url = urllib.parse.urlparse(valores["Caminho"])
        if url.scheme not in ("http", "https") or not url.netloc:
            raise ProtocoloInvalido(f"{onde}, linha {sigla}: Caminho {valores['Caminho']!r} "
                                    f"não é URL http(s) bem formada")
        langs, fcts = _lista(linha["Idiomas"]), _lista(linha["FCTs"])
        for campo, itens in (("Idiomas", langs), ("FCTs", fcts)):
            repetidos = sorted({x for x in itens if itens.count(x) > 1})
            if repetidos:
                raise ProtocoloInvalido(f"{onde}, linha {sigla}: {campo} com valor repetido "
                                        f"{repetidos}")
        fora = [i for i in langs if i not in idiomas]
        if fora:
            raise ProtocoloInvalido(f"{onde}, linha {sigla}: idioma {fora} fora dos idiomas "
                                    f"do quadro terminológico {list(idiomas)}")
        fora = [f for f in fcts if f not in ids_facetas]
        if fora:
            raise ProtocoloInvalido(f"{onde}, linha {sigla}: FCTs {fora} não é faceta do "
                                    f"protocolo {list(ids_facetas)}")
        por_sigla[sigla] = {"sigla": sigla, "nome": valores["Instrumento"],
                            "modo": valores["Modo"], "caminho": valores["Caminho"],
                            "idiomas": langs, "facetas": fcts}
    if not por_sigla:
        raise ProtocoloInvalido(f"{onde} sem instrumento")
    automaticos = [s for s, i in por_sigla.items() if i["modo"] == MODO_AUTOMATICO]
    if automaticos:
        clientes = clientes_automaticos()
        sem = [s for s in automaticos if s not in clientes]
        if sem:
            raise ProtocoloInvalido(f"{onde}: instrumento {MODO_AUTOMATICO} sem cliente "
                                    f"automatizado: {sem}; clientes existentes: {clientes}")
    por_faceta = {fid: [i for i in por_sigla.values() if fid in i["facetas"]]
                  for fid in ids_facetas}
    faltam = [f for f, lista in por_faceta.items() if not lista]
    if faltam:
        raise ProtocoloInvalido(f"{onde}: faceta(s) sem instrumento na coluna FCTs: {faltam}")
    return por_sigla, por_faceta


def instrumentos_do_termo(d, fid, idioma):
    """Instrumentos em que se valida um termo da faceta `fid` no `idioma`."""
    return [i for i in d["instrumentos_por_faceta"][fid] if idioma in i["idiomas"]]


def estado_inicial(instrumento):
    """Campos com que nasce a linha de um termo ainda não registrado na planilha.

    Instrumento sem cliente automatizado (modo `Manual`) nasce pendente de validação
    manual; os demais, aguardando consulta.
    """
    if instrumento["modo"] == MODO_MANUAL:
        return {"status_proposto": STATUS_MANUAL, "observacao_tecnica": OBS_MANUAL}
    return {"observacao_tecnica": "aguardando consulta"}


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
FORMA_COMPOSICAO = "STRn AND STRn AND (STRn OR STRn)"


def _grupos_de_composicao(comb, ident):
    """Composição na forma estrita `STR1 AND STR2 AND (STR3 OR STR4)`.

    A forma devolvida é uma lista de grupos; todo grupo tem de ser satisfeito e, dentro do
    grupo, basta um dos STRn. `AND`, em maiúsculas, é a única conjunção; `OR`, em
    maiúsculas, só aparece dentro de parênteses, sem aninhamento. Qualquer outra forma —
    `+`, operador em minúscula, `OR` fora de parênteses — reprova: a expressão do protocolo
    é a que se executa, e leitura tolerante esconderia a divergência.
    """
    comb = " ".join(comb.split())
    if "+" in comb:
        raise ProtocoloInvalido(f"expressão {ident}: `+` não é conjunção da forma estrita "
                                f"{FORMA_COMPOSICAO}; use AND: {comb!r}")
    minusculas = sorted({m.group(0) for m in re.finditer(r"\b(?:and|or|not)\b", comb,
                                                          re.I)} - {"AND", "OR"})
    if minusculas:
        raise ProtocoloInvalido(f"expressão {ident}: operador fora da forma estrita "
                                f"{FORMA_COMPOSICAO} {minusculas}: {comb!r}")
    partes, profundidade, atual = [], 0, ""
    for tok in re.split(r"(\(|\)|\bAND\b)", comb):
        if tok == "(":
            profundidade += 1
            if profundidade > 1:
                raise ProtocoloInvalido(f"expressão {ident}: parênteses aninhados fora da "
                                        f"forma estrita {FORMA_COMPOSICAO}: {comb!r}")
        elif tok == ")":
            profundidade -= 1
            if profundidade < 0:
                raise ProtocoloInvalido(f"expressão {ident}: parêntese fechado sem abrir")
        if tok == "AND" and profundidade == 0:
            partes.append(atual)
            atual = ""
        else:
            atual += tok
    partes.append(atual)
    if profundidade:
        raise ProtocoloInvalido(f"expressão {ident}: parêntese aberto sem fechar")

    grupos = []
    for parte in partes:
        p = parte.strip()
        if not p:
            raise ProtocoloInvalido(f"expressão {ident}: operador AND sem operando")
        m = re.fullmatch(r"\(\s*(STR\d+(?:\s+OR\s+STR\d+)+)\s*\)", p)
        if m:
            membros = [x.strip() for x in m.group(1).split("OR")]
        elif re.fullmatch(r"STR\d+", p):
            membros = [p]
        else:
            raise ProtocoloInvalido(
                f"expressão {ident}: composição fora da forma estrita "
                f"{FORMA_COMPOSICAO}: {comb!r}")
        grupos.append(membros)
    return grupos


def _percentual(s):
    return float(s.replace(",", ".")) / 100


def expressoes(t, params):
    """Composição das expressões, a executada, a sonda e a faixa de sensibilidade.

    Devolve (composição, executada, sonda, sensibilidade). A composição é estrutural: sem a
    tabela, a leitura reprova; executada, sonda e faixa seguem a precedência.
    """
    bloco = secao(t, "Expressões de busca")
    composicao, natureza, detalhe = {}, {}, {}
    linhas_tabela = [l for l in bloco.splitlines() if l.lstrip().startswith("|")]
    if not linhas_tabela:
        raise ProtocoloInvalido("tabela 'Expressões de busca' ausente")
    # O cabeçalho diz o que cada coluna é: lido por posição, um cabeçalho trocado
    # faria a natureza ou a expressão vir de outra coluna, em silêncio.
    esperado = list(CFG["expressoes"]["colunas"])
    lido = [desescapa(c).strip() for c in celulas(linhas_tabela[0])]
    if lido != esperado:
        raise ProtocoloInvalido(
            f"tabela 'Expressões de busca': cabeçalho {lido} difere do esperado "
            f"{esperado} ([expressoes] colunas do {CONFIG.name})")
    for linha in linhas_tabela:
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
    comp = _estrutural(params, "composicao", composicao)

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


SECAO_SEMENTES = "Conjunto-semente"


def limiar(t, params):
    bloco = secao(t, SECAO_SEMENTES)
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
def caminho_ficha(sigla):
    """Caminho da ficha de uma base, relativo à raiz, pelo padrão `[documentos] ficha`."""
    return CFG["documentos"]["ficha"].replace(MARCA_SIGLA, sigla)


def bases_de_dados(bloco_fontes):
    """Bases da tabela "Bases de dados": identificador, sigla, nome e ficha."""
    onde = "tabela 'Bases de dados'"
    tabelas_ = blocos_de_tabela(secao(bloco_fontes, "Bases de dados"))
    if not tabelas_:
        raise ProtocoloInvalido(f"{onde} ausente")
    bases = []
    for linha in le_tabela(tabelas_[0], COLUNAS_BASES, onde)[1]:
        valores = {c: desescapa(linha[c]).strip() for c in COLUNAS_BASES}
        ident = valores["ID Base"] or "?"
        vazios = [c for c, v in valores.items() if not v]
        if vazios:
            raise ProtocoloInvalido(f"{onde}, linha {ident}: campo vazio {vazios}")
        m = re.fullmatch(r"BD(\d+)", ident)
        if not m:
            raise ProtocoloInvalido(f"{onde}: ID Base {ident!r} fora da forma BDn")
        sigla = valores["Sigla"]
        if not re.fullmatch(r"[\w-]+", sigla):
            raise ProtocoloInvalido(f"{onde}, linha {ident}: Sigla {sigla!r} não serve de "
                                    f"chave (letras, dígitos, `_` ou `-`)")
        if any(b["sigla"] == sigla for b in bases):
            raise ProtocoloInvalido(f"{onde}: sigla repetida {sigla!r}")
        ficha_ = caminho_ficha(sigla)
        if not (RAIZ / ficha_).exists():
            raise ProtocoloInvalido(f"{onde}, linha {ident}: ficha da sigla {sigla!r} não "
                                    f"existe — procurada em {ficha_} (`documentos.ficha` "
                                    f"do {CONFIG.name})")
        bases.append({"id": f"BD{int(m.group(1))}", "sigla": sigla,
                      "nome": valores["Nome da base"], "ficha": ficha_})
    _numeracao([b["id"] for b in bases], "BD", "bases")
    return bases


def fontes(t):
    bloco = secao(t, "Fontes de informação")
    bases_bloco = secao(bloco, "Bases de dados")
    bases = bases_de_dados(bloco)

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


def sementes(t, siglas):
    """Referências e bases esperadas, da tabela `ID Semente | Semente | Bases`.

    Cada base citada tem de ser sigla da tabela de bases, na grafia exata; semente sem base
    reprova.
    """
    onde = f"tabela '{SECAO_SEMENTES}'"
    estudos = []
    for linha in tabela_da_secao(t, SECAO_SEMENTES, COLUNAS_SEMENTES):
        ident = desescapa(linha["ID Semente"]).strip()
        if not re.fullmatch(r"SE\d+", ident):
            raise ProtocoloInvalido(f"{onde}: ID Semente {ident!r} fora da forma SEn")
        ref = desescapa(linha["Semente"]).strip()
        m = re.match(r"^(.*?)\s*\((\d{4})\)\.\s*(.*)$", ref)
        if not m:
            raise ProtocoloInvalido(f"{onde}, linha {ident}: referência sem autoria e ano no "
                                    f"padrão esperado")
        autores, ano, resto = m.groups()
        bases = _lista(linha["Bases"])
        if not bases:
            raise ProtocoloInvalido(f"{onde}, linha {ident}: semente sem base")
        fora = [b for b in bases if b not in siglas]
        if fora:
            raise ProtocoloInvalido(f"{onde}, linha {ident}: base {fora} não é sigla da "
                                    f"tabela 'Bases de dados' {list(siglas)}")
        if len(set(bases)) != len(bases):
            raise ProtocoloInvalido(f"{onde}, linha {ident}: base repetida {bases}")
        primeiro = autores.split(",")[0].strip()
        estudos.append({
            "id": ident, "autores": autores.strip(), "ano": int(ano),
            "titulo": _titulo(resto), "doi": _doi(ref),
            "bases": bases, "chave": f"{primeiro} {ano}",
        })
    _numeracao([e["id"] for e in estudos], "SE", "referências")
    return estudos


def distribuicao(estudos, siglas):
    """Distribuição das sementes pelas bases, calculada da tabela. Não confere prosa."""
    por_base = {b: 0 for b in siglas}
    for e in estudos:
        for b in e["bases"]:
            por_base[b] += 1
    multi = sum(1 for e in estudos if len(e["bases"]) > 1)
    return {
        "por_base": por_base, "incidencias": sum(por_base.values()),
        "registros": len(estudos), "em_mais_de_uma_base": multi,
        "em_uma_so": len(estudos) - multi,
    }


# ------------------------------------------------------------------- fichas por base
# A ficha da base é a fonte da FORMA; o protocolo é a fonte do VOCABULÁRIO. O script não
# conhece sintaxe de base: campo, tag e operador são lidos do texto da ficha. O que ele
# conhece é o contrato de extração — onde a string está e como o termo se separa.

OPERADORES = {"OR", "AND", "NOT"}
CAMPOS_STRING = ("title", "abstract", "descriptor", "TS", "TI", "AB", "AK")
SECOES_FICHA = ("3. Strings por faceta", "4. Expressões de busca",
                "Declaração de cobertura")
MODOS_DERIVACAO = ("morfologia", "radical")


def base_de(d, sigla):
    """A base de sigla `sigla`, da tabela "Bases de dados" lida em `d`."""
    achada = next((b for b in d["bases"] if b["sigla"] == sigla), None)
    if achada is None:
        raise ProtocoloInvalido(f"base {sigla!r} não consta da tabela 'Bases de dados' "
                                f"({[b['sigla'] for b in d['bases']]})")
    return achada


def ficha(d, sigla):
    return (RAIZ / base_de(d, sigla)["ficha"]).read_text(encoding="utf-8")


def forma_execucao(t_ficha, caminho):
    """Forma de execução declarada na ficha: exatamente uma linha `- Execução: <forma>`.

    Sem padrão: linha ausente, repetida ou com valor fora de `FORMAS_EXECUCAO` reprova,
    nomeando a ficha. Devolve o valor interno (`unica` ou `particionada`).
    """
    achados = re.findall(r"^-\s*Execução:\s*(.*?)\s*$", t_ficha, re.M)
    admitidos = list(FORMAS_EXECUCAO)
    if not achados:
        raise ProtocoloInvalido(f"ficha {caminho}: falta a linha `- Execução: <forma>` "
                                f"(formas admitidas: {admitidos})")
    if len(achados) > 1:
        raise ProtocoloInvalido(f"ficha {caminho}: linha `- Execução:` repetida {achados}")
    valor = desescapa(achados[0]).strip()
    if valor not in FORMAS_EXECUCAO:
        raise ProtocoloInvalido(f"ficha {caminho}: forma de execução {valor!r} fora das "
                                f"admitidas {admitidos}")
    return FORMAS_EXECUCAO[valor]


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


def _termos_bloco(texto):
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
    # A fidelidade vem antes da derivação: a expressão derivada que se executa no teste
    # de fidelidade é bloco que se submete, e o estatuto tem de dizer isso.
    if "teste de fidelidade" in baixo:
        return "fidelidade"
    if "nao se executa" in baixo or "derivada localmente" in baixo:
        return "derivada"
    if "executada e exportada" in baixo or "esta que se executa" in baixo:
        return "executada"
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
                        "blocos": _cercados(corpo), "forma_longa": True}
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
            # A faceta é identificada só pelo código FCTn; símbolo gráfico não conta.
            facetas = {f"FCT{n}" for n in re.findall(r"FCT(\d)", cels[2] if len(cels) > 2 else "")}
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


def execucao_base(forma, expressoes, curadas, executada):
    """O que se executa nesta base: uma, particionada em subconsultas ou curada.

    A expressão é a que o protocolo declara executada; a forma (única ou particionada)
    é a declarada na ficha (`forma_execucao`), e a curada, a da própria ficha.
    """
    expressao = executada
    if curadas:
        modo = "curada"
        itens = curadas
    else:
        modo = forma
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


def declaracao_base(t, idiomas_quadro):
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
            if i not in idiomas_quadro:
                raise ProtocoloInvalido(f"declaração de {fid}: idioma {i!r} desconhecido")
    modos = [m.strip() for m in re.split(r"\s*(?:,|;| e )\s*", derivacoes) if m.strip()]
    for m in modos:
        if m not in MODOS_DERIVACAO:
            raise ProtocoloInvalido(f"derivação declarada desconhecida: {m!r}; "
                                    f"admitidas: {MODOS_DERIVACAO}")
    return {"idiomas": idiomas, "camadas": camadas, "derivacoes": modos,
            "exclusoes": exclusoes}


def base_derivada(sigla, d, t_ficha=None):
    """O derivado de uma base. A forma vem da ficha; o vocabulário, do protocolo."""
    b = base_de(d, sigla)
    t = ficha(d, sigla) if t_ficha is None else t_ficha
    forma = forma_execucao(t, b["ficha"])
    expressoes, curadas, ancoras = expressoes_base(t, sigla)
    execucao = execucao_base(forma, expressoes, curadas, d["executada"])
    return {
        "base": {"id": b["id"], "sigla": sigla, "nome": b["nome"], "ficha": b["ficha"],
                 "execucao_declarada": forma},
        "facetas": facetas_base(t),
        "ancoras": ancoras,
        "expressoes": {k: expressoes[k] for k in sorted(expressoes)},
        "execucao": execucao,
        "filtros": filtros_base(execucao),
        "declaracao": declaracao_base(t, d["idiomas"]),
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
    idiomas = decl.get("idiomas", {}).get(fid) or list(d["idiomas"])
    camadas = CAMADAS if decl.get("camadas") == "todas" else ("nucleo",)
    na_str = {normaliza(x) for x in d["strings"][fid]["termos"]}
    tabela = _sem_repeticao([x for i in idiomas for c in camadas
                             for x in f["camadas"][i][c]])
    vigentes = [x for x in tabela if normaliza(x) in na_str]
    quadro = _sem_repeticao([x for i in d["idiomas"] for c in CAMADAS
                             for x in f["camadas"][i][c]])
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
        # Bloco só onde há execução: a derivada padrão não é forma que se submete. A
        # forma longa é representação não executada e fica fora desta regra.
        if expr["estatuto"] == "derivada" and not expr.get("forma_longa"):
            if expr["blocos"]:
                problemas.append(f"{ident}: expressão derivada não se executa e não leva bloco")
            continue
        if not precisa_forma or not expr["blocos"]:
            continue
        # Bloco que se submete é literal: referência a conjunto depende da numeração da
        # sessão e não se reproduz a partir da ficha.
        referencias = sorted({r for b in expr["blocos"]
                              for r in re.findall(r"#\d+", b["texto"])})
        if referencias:
            problemas.append(f"{ident}: referência a conjunto {', '.join(referencias)} no "
                             f"bloco — a expressão que se executa é bloco literal")
            continue
        # O conjunto de termos do bloco tem de ser o das strings que a expressão declara:
        # é o que impede a segunda cópia de defasar da seção 3.
        esperados = _sem_repeticao([t for s in base["facetas"]
                                    if s["faceta"] in expr["facetas"] for t in s["termos"]])
        achados = _sem_repeticao([t for b in expr["blocos"]
                                  for t in _termos_bloco(b["texto"])])
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
    tb, idiomas = tabelas(t)
    _estrutural(params, "idiomas", list(idiomas))
    ids_facetas = [f["id"] for f in pal]
    insts, insts_faceta = instrumentos(t, ids_facetas, idiomas)
    _estrutural(params, "instrumentos", [
        f"{s} ({i['modo']}; {'/'.join(i['idiomas'])}; {','.join(i['facetas'])})"
        for s, i in insts.items()])
    st = strings(t)
    for n in st:
        # A string repete termo entre camadas; a lista executada é deduplicada. É ela
        # que a derivação local usa, e é ela que o relatório conta.
        st[n]["termos"] = _sem_repeticao(st[n]["termos"])
    comp, exec_, sonda, sens = expressoes(t, params)
    crit = criterios(t)
    fts = fontes(t)
    siglas = [b["sigla"] for b in fts["bases"]]
    _estrutural(params, "bases", [f"{b['id']} {b['sigla']} → {b['ficha']}"
                                  for b in fts["bases"]])
    est = sementes(t, siglas)
    _estrutural(params, "sementes", [f"{e['id']}: {', '.join(e['bases'])}" for e in est])
    d = {
        "questoes": questoes(t),
        "facetas": pal,
        "ancoras": ancoras(pal, params),
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
        "recorte": recorte(t, params),
        "fontes": fts,
        "bases": fts["bases"],
        "limiar": limiar(t, params),
        "sementes": est,
        "distribuicao": distribuicao(est, siglas),
    }
    # O protocolo não declara estes; valem os do config.toml, com a origem registrada.
    d["divergencia"] = _parametro(params, "divergencia_fidelidade", None,
                                  "padroes.divergencia_fidelidade")
    d["calibracao_triagem"] = _parametro(params, "calibracao_triagem", None,
                                         "padroes.calibracao_triagem")
    _parametro(params, "minimo_termos_string", None, "conferencia.minimo_termos_string")
    _parametro(params, "dimensoes_criterio", None, "conferencia.dimensoes_criterio")
    d["parametros"] = params
    d["papeis"] = papeis(d)
    return d


_CACHE = {}


def dados():
    """O protocolo lido uma vez por execução, para os scripts consumidores.

    Leitura reprovada termina o script com a mensagem do leitor: nenhum consumidor segue
    com estrutura incompleta.
    """
    if "d" not in _CACHE:
        try:
            _CACHE["d"] = analisa()
        except ProtocoloInvalido as e:
            raise SystemExit(f"Protocolo ilegível ({CFG['protocolo']}) — {e}\n"
                             f"  Rode  python3 src/protocolo.py --conferir") from None
    return _CACHE["d"]


# ---------------------------------------------------------------------- conferência
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


def _coerencia_expressoes(d):
    """Relações entre as expressões, sem valor esperado: âncoras, sonda e executada."""
    problemas = []
    p = d.get("papeis") or papeis(d)
    comp, exec_, sonda = d["expressoes"], p["executada"], p["sonda"]
    existentes = {s["id"] for s in d["strings"].values()}
    if p["ancoras_sem_string"]:
        return [f"âncoras {p['ancoras_sem_string']} não são facetas com string no protocolo"]
    ancora = p["ancoras"]

    for ident, grupos in sorted(comp.items()):
        fora = sorted({x for g in grupos for x in g} - existentes)
        if fora:
            problemas.append(f"{ident}: composição cita string inexistente {fora}")
        for g in ancora:
            if g not in grupos:
                problemas.append(f"{ident}: falta a âncora obrigatória {g[0]}")
    if sorted(comp.get(sonda, [])) != sorted(ancora):
        problemas.append(f"a sonda {sonda} não é a conjunção das âncoras "
                         f"({' AND '.join(g[0] for g in ancora)})")
    resto = [g for g in comp.get(exec_, []) if g not in ancora]
    especificas = p["especificas"]
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
        for i in d["idiomas"]:
            for c in CAMADAS:
                if not f["camadas"][i][c]:
                    problemas.append(f"faceta {f['id']}: camada {c} vazia em {i}")
        # Repetição entre camadas é legítima (o mesmo termo em núcleo e em relacionados);
        # a lista final é deduplicada. Dentro da mesma camada, é defeito.
        for i in d["idiomas"]:
            for c in CAMADAS:
                vistos = set()
                for termo in f["camadas"][i][c]:
                    k = normaliza(termo)
                    if k in vistos:
                        problemas.append(
                            f"faceta {f['id']} {i}/{c}: {termo!r} repetido na mesma camada")
                    vistos.add(k)

    # A string só pode usar termo que o quadro da própria faceta contém. É a remissão que
    # impede string e vocabulário de divergirem em silêncio.
    minimo = d["parametros"]["minimo_termos_string"]["valor"]
    quadro = {f["id"]: {normaliza(x) for i in d["idiomas"] for x in f["termos"][i]}
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

    if not d["questoes"]["questao_principal"]:
        problemas.append("questão geral vazia")

    # Base e ficha de cada semente são lidas e conferidas pelo leitor (sigla da tabela de
    # bases, ficha existente); a distribuição é calculada da tabela, sem prosa a conferir.
    for e in d["sementes"]:
        if not e["titulo"] or len(e["titulo"]) < 12:
            problemas.append(f"semente {e['id']}: título não legível ({e['titulo']!r})")

    # A forma de cada base é parte da coerência do documento: ficha ilegível ou fora do
    # protocolo reprova só a sua base.
    problemas += _problemas_bases(d)
    return problemas


def _composicao_legivel(grupos):
    """`[["STR1"],["STR2"],["STR3","STR4"]]` como `1 AND 2 AND (3 OR 4)`: a forma estrita
    do protocolo, com o número da STR."""
    partes = []
    for g in grupos:
        nomes = [x[3:] for x in g]
        partes.append(nomes[0] if len(nomes) == 1 else "(" + " OR ".join(nomes) + ")")
    return " AND ".join(partes)


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
        n_bruto = sum(len(f["termos"][i]) for i in d["idiomas"])
        insts = ", ".join(f"{i['sigla']}({'/'.join(i['idiomas'])}"
                          f"{', manual' if i['modo'] == MODO_MANUAL else ''})"
                          for i in d["instrumentos_por_faceta"][f["id"]])
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
    for nome, valor, origem in execucao_das_fichas(d):
        L.append(f"    {nome:<24} {valor[:70]:<72} [{origem}]")
    return "\n".join(L)


def execucao_das_fichas(d):
    """Forma de execução de cada base, com origem na ficha: (nome, valor, origem).

    Ficha ilegível nesse ponto aparece como tal, sem derrubar a exibição das demais.
    """
    saida = []
    for b in d["bases"]:
        try:
            valor = forma_execucao(ficha(d, b["sigla"]), b["ficha"])
        except (ProtocoloInvalido, OSError) as e:
            valor = f"ILEGÍVEL — {e}"
        saida.append((f"execucao.{b['sigla']}", valor, f"ficha {b['ficha']}"))
    return saida


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


def _problemas_registro(dado, bds):
    """Confere o registro documental e as execuções que declaram arquivo exportado.

    `bds` são os identificadores da tabela "Bases de dados" do protocolo.
    """
    if not isinstance(dado, dict):
        return ["registro_execucao.json não é um objeto"]
    bases = dado.get("bases")
    if not isinstance(bases, dict):
        return ["registro_execucao.json sem a chave `bases`"]
    faltam = [b for b in bds if b not in bases]
    if faltam:
        return [f"registro_execucao.json sem as bases {faltam}"]

    problemas = []
    for bd in bds:
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
    """Problemas de cada base, isolados: ficha ilegível reprova só a sua base."""
    problemas = []
    for b in d["bases"]:
        sigla = b["sigla"]
        try:
            base = base_derivada(sigla, d)
            problemas += [f"{sigla}: {p}" for p in cobertura_base(sigla, base, d)]
        except ProtocoloInvalido as e:
            problemas.append(f"{sigla}: {e}")
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
        problemas += _problemas_registro(dado, [b["id"] for b in d["bases"]])

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
        for bd in [b["id"] for b in d["bases"]]:
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
    for base in d["bases"]:
        try:
            b = base_derivada(base["sigla"], d)
        except ProtocoloInvalido as e:
            linhas.append(f"[{base['sigla']}] ficha ilegível: {e}")
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


def _tabela_sem_coluna(linhas, cabecalho, coluna):
    """Retira a coluna `coluna` (posição) da tabela cujo cabeçalho começa por `cabecalho`."""
    i = next(k for k, l in enumerate(linhas) if l.startswith(cabecalho))
    saida = list(linhas)
    while i < len(saida) and saida[i].lstrip().startswith("|"):
        cels = celulas(saida[i])
        saida[i] = "| " + " | ".join(c for k, c in enumerate(cels) if k != coluna) + " |"
        i += 1
    return saida


def _sem_tabela(linhas, cabecalho):
    i = next(k for k, l in enumerate(linhas) if l.startswith(cabecalho))
    j = i
    while j < len(linhas) and linhas[j].lstrip().startswith("|"):
        j += 1
    return linhas[:i] + linhas[j:]


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
        # Coerência das expressões.
        ("âncora desmarcada",
         _troca_linha(linhas, "- Faceta 2 (FCT2)", " (âncora obrigatória 2)", ""),
         "conjunção das âncoras"),
        ("executada que não é a união das específicas",
         _troca_linha(linhas, "| EB4 |", "(STR3 OR STR4)", "STR3"), "não é a união"),
        ("sonda que não é a conjunção das âncoras",
         _troca_linha(linhas, "| EB5 |", "STR1 AND STR2\\ |", "STR1 AND STR2 AND STR3\\ |"),
         "conjunção das âncoras"),
        ("expressão sem âncora",
         _troca_linha(linhas, "| EB2 |", "STR1 AND STR2 AND STR3", "STR1 AND STR3"),
         "falta a âncora"),
        # Forma estrita da composição: só AND como conjunção, OR só entre parênteses.
        ("cabeçalho da tabela de expressões renomeado",
         _troca_linha(linhas, "| ID expressão |", "| Expressão de busca |",
                      "| Combinação de Strings |"), "difere do esperado"),
        ("cabeçalho da tabela de expressões com colunas trocadas",
         _troca_linha(linhas, "| ID expressão |", "| Natureza | Expressão de busca |",
                      "| Expressão de busca | Natureza |"), "difere do esperado"),
        ("composição com `+` como conjunção",
         _troca_linha(linhas, "| EB2 |", "STR1 AND STR2 AND STR3", "STR1 + STR2 + STR3"),
         "não é conjunção da forma estrita"),
        ("composição com operador em minúscula",
         _troca_linha(linhas, "| EB2 |", "STR1 AND STR2 AND STR3", "STR1 and STR2 AND STR3"),
         "operador fora da forma estrita"),
        ("composição com OR fora de parênteses",
         _troca_linha(linhas, "| EB4 |", "(STR3 OR STR4)", "STR3 OR STR4"),
         "fora da forma estrita"),
        ("composição com parênteses aninhados",
         _troca_linha(linhas, "| EB4 |", "(STR3 OR STR4)", "((STR3 OR STR4))"),
         "aninhados"),
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
        # Parâmetros estruturais: ausência e valor inválido reprovam, sem padrão.
        ("composição ausente (seção de expressões removida)",
         [l for l in linhas if l.strip() != "## Expressões de busca"], "Expressões de busca"),
        # Leitor de tabela pelo cabeçalho.
        ("coluna Sigla retirada da tabela de bases",
         _tabela_sem_coluna(linhas, "| ID Base |", 1), "falta a coluna ['Sigla']"),
        ("coluna repetida na tabela de instrumentos",
         _troca_linha(linhas, "| Sigla | Instrumento", "| Caminho |", "| Modo |"),
         "coluna repetida ['Modo']"),
        ("tabela de bases ausente", _sem_tabela(linhas, "| ID Base |"),
         "tabela 'Bases de dados' ausente"),
        # Facetas.
        ("âncora com parêntese mal formado",
         _troca_linha(linhas, "- Faceta 1 (FCT1)", "(âncora obrigatória 1)",
                      "(âncora obrigatória 1"), "âncora fora da forma"),
        ("linha de faceta com travessão residual",
         _troca_linha(linhas, "- Faceta 3 (FCT3)", "ensino-aprendizagem",
                      "ensino-aprendizagem — vermelho"), "travessão"),
        # Quadro terminológico: idioma pelo cabeçalho.
        ("idioma repetido no cabeçalho do quadro",
         _troca_linha(linhas, "| FCT2 | pt |", "| FCT2 | pt | en | es |",
                      "| FCT2 | pt | en | en |"), "coluna repetida ['en']"),
        ("coluna de idioma sem nome no quadro",
         _troca_linha(linhas, "| FCT3 | pt |", "| FCT3 | pt | en | es |",
                      "| FCT3 | pt |  | es |"), "sem nome"),
        ("idiomas diferentes entre facetas",
         _troca_linha(linhas, "| FCT4 | pt |", "| FCT4 | pt | en | es |",
                      "| FCT4 | pt | en | fr |"), "diferem dos idiomas"),
        # Instrumentos.
        ("instrumento com sigla repetida",
         _troca_linha(linhas, "| eric |", "| eric |", "| brased |"), "sigla repetida"),
        ("instrumento com campo vazio",
         _troca_linha(linhas, "| tbci |", "| pt | FCT1 |", "|  | FCT1 |"), "campo vazio"),
        ("instrumento com Modo fora do domínio",
         _troca_linha(linhas, "| eric |", "| Manual |", "| Semiautomático |"),
         "fora dos admitidos"),
        ("instrumento com idioma fora do quadro",
         _troca_linha(linhas, "| brased |", "| pt | FCT2", "| fr | FCT2"), "['fr'] fora"),
        ("instrumento com faceta inexistente em FCTs",
         _troca_linha(linhas, "| unesco |", "FCT4 |", "FCT4s |"), "['FCT4s']"),
        ("faceta do quadro sem instrumento",
         _troca_linha(_troca_linha(_troca_linha(linhas, "| unesco |", ", FCT4 |", " |"),
                                   "| eric |", ", FCT4 |", " |"),
                      "| brased |", ", FCT4 |", " |"), "sem instrumento"),
        ("instrumento Automático sem cliente",
         _troca_linha(linhas, "| eric |", "| Manual |", "| Automático |"), "sem cliente"),
        ("instrumento com Caminho que não é URL",
         _troca_linha(linhas, "| eric |", "https://vocabularyserver.com/eric/",
                      "vocabularyserver eric"), "não é URL"),
        # Bases e sementes.
        ("sigla de base repetida",
         _troca_linha(linhas, "| BD3 |", "| eric |", "| scopus |"), "sigla repetida"),
        ("sigla de base sem ficha",
         _troca_linha(linhas, "| BD3 |", "| eric |", "| ericx |"),
         "ficha da sigla 'ericx' não existe"),
        ("semente sem base",
         _troca_linha(linhas, "| SE10 |", "| wos |", "|  |"), "semente sem base"),
        ("semente com sigla em outra grafia",
         _troca_linha(linhas, "| SE2 |", "| wos, scopus |", "| WoS, scopus |"),
         "linha SE2: base ['WoS']"),
        ("semente fora de numeração",
         [l.replace("| SE10 |", "| SE11 |", 1) for l in linhas], "numeração SE"),
    ]
    return [(nome, "\n".join(ls), espera) for nome, ls, espera in casos]


def _autoteste_precedencia(t):
    """Parâmetro ausente do protocolo vale pelo padrão, com a origem registrada."""
    falhas, n = 0, 0
    casos = [
        ("limiar ausente do protocolo vale pelo padrão", "limiar_aderencia",
         [l for l in t.splitlines() if not l.startswith("- Regra de ajuste:")]),
        ("âncoras não marcadas valem pelo padrão", "ancoras",
         [re.sub(r" \(âncora obrigatória \d\)", "", l) for l in t.splitlines()]),
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
    testa("padrão de caminho da ficha ausente", sem("documentos.ficha"), "documentos.ficha")
    testa("padrão de caminho da ficha sem {sigla}",
          com("documentos.ficha", "docs/busca_base.md"), MARCA_SIGLA)
    # Chave retirada (parâmetro estrutural) de volta à configuração: segunda fonte.
    testa("[fichas.wos] na configuração",
          com("fichas", {"wos": {"bd": "BD1", "sigla": "WoS", "execucao": "unica"}}),
          "`fichas`")
    for chave, valor in (("padroes.composicao", {"EB1": [["STR1"]]}), ("cores", {"x": "FCT1"}),
                         ("instrumentos", {"X": {"sigla": "x"}}), ("idiomas", ["pt"])):
        testa(f"chave retirada `{chave}` na configuração", com(chave, valor), f"`{chave}`")
    testa("faixa padrão invertida", com("padroes.sensibilidade", [0.15, 0.05]), "inferior")
    with tempfile.TemporaryDirectory() as tmp:
        ruim = pathlib.Path(tmp) / "config.toml"
        ruim.write_text("protocolo = \n", encoding="utf-8")
        testa("arquivo que não é TOML", lambda: carrega_config(ruim), "não é TOML válido")
        testa("arquivo ausente", lambda: carrega_config(pathlib.Path(tmp) / "nada.toml"),
              "ausente")
    return falhas, n


def _autoteste_validacao(t, d):
    """Prova o planejamento da validação terminológica por instrumento.

    Sobre o protocolo e cópias alteradas em memória: todos os instrumentos da faceta são
    planejados, instrumento cuja coluna FCTs perde a faceta não é, só nos idiomas que o
    instrumento cobre, e o modo `Manual` faz a linha nascer pendente de validação manual.
    """
    falhas, n = 0, 0

    def testa(nome, condicao, detalhe=""):
        nonlocal falhas, n
        n += 1
        if condicao:
            print(f"  [ok] {nome}")
        else:
            print(f"  [FALHA] {nome}{' — ' + detalhe if detalhe else ''}")
            falhas += 1

    def planejados(dd, fid):
        return {i["sigla"] for idioma in dd["idiomas"]
                for i in instrumentos_do_termo(dd, fid, idioma)}

    # Vários instrumentos: a faceta com mais instrumentos tem todos planejados. Sem faceta
    # com mais de um, o caso não prova nada e falha.
    por_faceta = d["instrumentos_por_faceta"]
    fid = max(por_faceta, key=lambda f: len(por_faceta[f]))
    declarados = {i["sigla"] for i in por_faceta[fid] if set(i["idiomas"]) & set(d["idiomas"])}
    testa(f"faceta com vários instrumentos ({fid}) planeja todos",
          len(declarados) > 1 and planejados(d, fid) == declarados,
          f"declarados {sorted(declarados)}, planejados {sorted(planejados(d, fid))}")

    # Instrumento retirado: a faceta sai da coluna FCTs da linha dele, na cópia do texto.
    if len(por_faceta[fid]) < 2:
        testa(f"instrumento retirado de {fid}", False,
              "a faceta não tem dois instrumentos para retirar um")
    else:
        sigla = por_faceta[fid][-1]["sigla"]
        linha = next(l for l in t.splitlines()
                     if l.lstrip().startswith("|") and celulas(l)[0] == sigla)
        cels = celulas(linha)
        cab = celulas(blocos_de_tabela(secao(t, SECAO_INSTRUMENTOS))[0][0])
        k = cab.index("FCTs")
        cels[k] = ", ".join(f for f in _lista(cels[k]) if f != fid)
        mutante = t.replace(linha, "| " + " | ".join(cels) + " |", 1)
        dm = analisa(mutante)
        testa(f"faceta {fid} retirada da coluna FCTs de {sigla}: {sigla} não é planejado",
              mutante != t and sigla not in planejados(dm, fid)
              and planejados(dm, fid) == planejados(d, fid) - {sigla},
              f"planejados {sorted(planejados(dm, fid))}")

    # Filtro por idioma: um instrumento passa a cobrir só um dos idiomas.
    dm = copy.deepcopy(d)
    inst = dm["instrumentos_por_faceta"][fid][0]
    so = inst["idiomas"][0]
    inst["idiomas"] = [so]
    fora = [i for i in dm["idiomas"] if i != so]
    testa(f"{inst['sigla']} restrito a {so} só é planejado em {so}",
          bool(fora)
          and inst["sigla"] in {i["sigla"] for i in instrumentos_do_termo(dm, fid, so)}
          and all(inst["sigla"] not in {i["sigla"] for i in instrumentos_do_termo(dm, fid, x)}
                  for x in fora))

    # Modo manual: um instrumento automático declarado Manual nasce pendente.
    dm = copy.deepcopy(d)
    autos = [i for i in dm["instrumentos_por_faceta"][fid] if i["modo"] != MODO_MANUAL]
    if not autos:
        testa(f"instrumento manual em {fid}", False, "nenhum instrumento automático")
    else:
        autos[0]["modo"] = MODO_MANUAL
        plano = [i for idioma in dm["idiomas"] for i in instrumentos_do_termo(dm, fid, idioma)
                 if i["sigla"] == autos[0]["sigla"]]
        testa(f"{autos[0]['sigla']} declarado {MODO_MANUAL} nasce pendente de validação "
              f"manual", bool(plano) and all(i["modo"] == MODO_MANUAL and
                                            estado_inicial(i).get("status_proposto")
                                            == STATUS_MANUAL for i in plano))
    manuais = [i for i in d["instrumentos"].values() if i["modo"] == MODO_MANUAL]
    testa("instrumento manual do protocolo nasce pendente e o automático não",
          bool(manuais)
          and all(estado_inicial(i).get("status_proposto") == STATUS_MANUAL for i in manuais)
          and all(estado_inicial(i).get("status_proposto") != STATUS_MANUAL
                  for i in d["instrumentos"].values() if i["modo"] != MODO_MANUAL))
    return falhas, n


def _autoteste_estrutural(t, d):
    """Leituras estruturais que têm de APROVAR: o leitor não pode reprovar o que é válido.

    Complementa as mutações, que provam a reprovação: aqui se prova que a gramática nova
    lê o caso legítimo com o valor certo.
    """
    falhas, n = 0, 0

    def testa(nome, condicao, detalhe=""):
        nonlocal falhas, n
        n += 1
        if condicao:
            print(f"  [ok] {nome}")
        else:
            print(f"  [FALHA] {nome}{' — ' + detalhe if detalhe else ''}")
            falhas += 1

    # Hífen dentro do nome pertence ao nome; âncora entre parênteses não.
    fct3 = next(f for f in d["facetas"] if f["id"] == "FCT3")
    testa("FCT3 lida com o hífen no nome e sem âncora",
          fct3["nome"] == "Práticas do processo de ensino-aprendizagem" and not fct3["ancora"],
          repr(fct3))
    fct1 = next(f for f in d["facetas"] if f["id"] == "FCT1")
    testa("FCT1 lida como âncora, sem o parêntese no nome",
          fct1["ancora"] and "(" not in fct1["nome"] and "âncora" not in fct1["nome"],
          repr(fct1))
    # Nome da base pela coluna, não pela posição.
    bd1 = next(b for b in d["bases"] if b["id"] == "BD1")
    testa("BD1 lida com o nome da coluna 'Nome da base'",
          bd1["nome"] == "Web of Science (Core Collection)", repr(bd1))

    # Colunas do quadro em outra ordem: os termos de `pt` continuam lidos como português.
    linhas = t.splitlines()
    i = next(k for k, l in enumerate(linhas) if l.startswith("| FCT2 |"))
    cab = celulas(linhas[i])
    a, b = cab.index("pt"), cab.index("en")
    j = i
    while j < len(linhas) and linhas[j].lstrip().startswith("|"):
        cels = celulas(linhas[j])
        cels[a], cels[b] = cels[b], cels[a]
        linhas[j] = "| " + " | ".join(cels) + " |"
        j += 1
    mutante = "\n".join(linhas)
    problemas = conferir(mutante)
    try:
        dm = analisa(mutante)
        f2 = next(f for f in dm["tabelas"] if f["id"] == "FCT2")
        orig = next(f for f in d["tabelas"] if f["id"] == "FCT2")
        mesmos = all(f2["termos"][x] == orig["termos"][x] for x in d["idiomas"])
    except ProtocoloInvalido as e:
        mesmos, problemas = False, [str(e)]
    testa("quadro de FCT2 com colunas `en | pt` aprova e lê `pt` como português",
          mutante != t and not problemas and mesmos, f"{problemas[:1]}")

    # Forma curada: emoji sem FCTn não atribui faceta.
    curadas = consultas_curadas("#### Grupo\n| n | Consulta | Facetas |\n| - | - | - |\n"
                                "| 1 | `ontology` | 🟦 |\n| 2 | `ontology` | FCT1 |\n")
    testa("consulta curada marcada só por emoji fica sem faceta; FCTn atribui",
          "facetas" not in curadas[0] and curadas[1].get("facetas") == ["FCT1"],
          repr(curadas))

    # Forma longa: representação não executada, marcada para ficar fora da conferência
    # de bloco que recusa a derivada padrão.
    longa = _expressoes_em_negrito("**EB1** geral\n\n```\nconsulta\n```\n")
    testa("forma longa é derivada marcada e não entra na conferência de bloco",
          longa["EB1"]["estatuto"] == "derivada"
          and longa["EB1"].get("forma_longa") is True,
          repr(longa))
    return falhas, n


# Casos de `_autoteste_dados`, para relatar quantos deixaram de rodar quando os arquivos
# alimentados faltam. Teste novo em `_autoteste_dados` atualiza este número; o autoteste
# reprova se divergirem.
CASOS_DADOS = 6


def _autoteste_dados(d):
    """Prova que a conferência dos arquivos alimentados reprova cada defeito esperado.

    Devolve (falhas, executados, não executados, motivo). Sem os arquivos, nenhum caso
    roda: eles são contados como não executados, nunca como aprovados.
    """
    sem, erro_s = _le_json(SEMENTES)
    reg, erro_r = _le_json(REGISTRO)
    if erro_s or erro_r:
        motivo = "; ".join(e for e in (erro_s, erro_r) if e)
        print(f"  [--] {CASOS_DADOS} caso(s) das conferências dos arquivos alimentados NÃO "
              f"executados: {motivo}")
        return 0, 0, CASOS_DADOS, motivo
    falhas, n = 0, 0

    def testa(nome, condicao):
        nonlocal falhas, n
        n += 1
        if condicao:
            print(f"  [ok] reprovou: {nome}")
        else:
            print(f"  [FALHA] aprovou indevidamente: {nome}")
            falhas += 1

    bds = [b["id"] for b in d["bases"]]
    base_ps, _ = _problemas_sementes(sem, d)
    base_pr = _problemas_registro(reg, bds)
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
    del copia["bases"][bds[0]]
    testa("registro sem uma das bases", bool(_problemas_registro(copia, bds)))

    copia = copy.deepcopy(reg)
    copia["bases"][bds[0]]["execucoes"].append({
        "id": "EX99", "expressao": d["executada"], "arquivo": "data/execucoes/ausente.ris",
        "registros_lidos": 1, "status": "valida"})
    testa("execução apontando arquivo de exportação ausente",
          bool(_problemas_registro(copia, bds)))

    copia = copy.deepcopy(reg)
    copia["bases"][bds[0]]["execucoes"].append({
        "id": "EX99", "expressao": d["executada"], "arquivo": str(REGISTRO.relative_to(RAIZ)),
        "registros_lidos": "um", "status": "valida"})
    testa("execução com `registros_lidos` que não é inteiro",
          bool(_problemas_registro(copia, bds)))
    if n != CASOS_DADOS:
        print(f"  [FALHA] {n} casos executados, CASOS_DADOS declara {CASOS_DADOS}")
        falhas += 1
    return falhas, n, 0, ""


def _autoteste_bases(d):
    """Prova que a cobertura da base reprova ficha divergente do protocolo.

    Cada defeito é injetado numa cópia do texto da ficha e a conferência tem de recusá-lo.
    Defeito que a conferência não pega é defeito que passa em silêncio na fonte.
    """
    falhas, n = 0, 0
    # As mutações abaixo reescrevem trechos do texto de fichas específicas; as siglas são
    # as dessas fichas. Base renomeada ou retirada da tabela "Bases de dados" falha aqui,
    # nomeada, em vez de derrubar o autoteste com KeyError.
    siglas = [b["sigla"] for b in d["bases"]]
    usados = ("wos", "brapci", "eric")
    ausentes = [s for s in usados if s not in siglas]
    if ausentes:
        print(f"  [FALHA] bases usadas pelo autoteste das fichas ausentes da tabela 'Bases de "
              f"dados': {ausentes}; atualizar as mutações de _autoteste_bases")
        return 1, 1
    slug = "wos"
    original = ficha(d, slug)

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
    brapci = ficha(d, "brapci")
    testa("termo só do quadro, em flexão, na string da BRAPCI",
          brapci.replace('("educação" OR ', '("educação" OR "educativos" OR ', 1),
          "brapci", brapci, "não está na string do protocolo")
    # Reprovação por base: o mesmo defeito, só na ficha da BRAPCI, reprova a BRAPCI e
    # nenhuma outra base.
    n += 1
    mutante = brapci.replace('("educação" OR ', '("educação" OR "educativos" OR ', 1)
    por_base = {s: problemas_de(s, mutante if s == "brapci" else ficha(d, s)) for s in siglas}
    outras = {s: p for s, p in por_base.items() if s != "brapci" and p}
    if mutante != brapci and por_base["brapci"] and not outras:
        print(f"  [ok] defeito só na BRAPCI reprova só a BRAPCI — "
              f"{', '.join(s for s in siglas if s != 'brapci')} passam")
    else:
        print(f"  [FALHA] defeito só na BRAPCI: BRAPCI "
              f"{'reprovou' if por_base['brapci'] else 'passou'}, outras reprovadas "
              f"{sorted(outras)}")
        falhas += 1
    testa("expressão com faceta trocada",
          original.replace("**Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧)",
                           "**Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥)", 1),
          espera="do protocolo")
    testa("declaração de cobertura restringindo as camadas",
          original.replace("| camadas | todas |", "| camadas | nucleo |", 1))

    # Forma radical, na ficha que a declara. O controle é a ficha corrente com toda linha
    # falsamente declarada como radical reetiquetada como redução: tem de passar, ou os
    # defeitos injetados sobre ele não provam nada.
    eric = ficha(d, "eric")

    # Forma de execução declarada na ficha: sem padrão, e o defeito fica na base afetada.
    linha_exec = "- Execução: particionada\n"
    testa("ficha da ERIC sem a linha de execução", eric.replace(linha_exec, "", 1), "eric",
          eric, "falta a linha `- Execução")
    testa("ficha da ERIC com a linha de execução repetida",
          eric.replace(linha_exec, linha_exec * 2, 1), "eric", eric, "repetida")
    testa("ficha da ERIC com forma de execução fora do domínio",
          eric.replace(linha_exec, "- Execução: dividida\n", 1), "eric", eric, "'dividida'")
    n += 1
    sem_linha = eric.replace(linha_exec, "", 1)
    por_base = {s: problemas_de(s, sem_linha if s == "eric" else ficha(d, s)) for s in siglas}
    outras = {s: p for s, p in por_base.items() if s != "eric" and p}
    if sem_linha != eric and any("busca_base_eric" in p for p in por_base["eric"]) \
            and not outras:
        print(f"  [ok] ficha da ERIC sem execução reprova só a ERIC, nomeando a ficha — "
              f"{', '.join(s for s in siglas if s != 'eric')} passam")
    else:
        print(f"  [FALHA] ficha da ERIC sem execução: ERIC {por_base['eric'][:1]}, outras "
              f"reprovadas {sorted(outras)}")
        falhas += 1

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

    # Bloco literal: referência a conjunto e termo defasado da seção 3. Cada defeito é
    # injetado num bloco de uma base e tem de reprovar só aquela base.
    def com_bloco(texto_ficha, ident, transforma):
        """Transforma o primeiro bloco cercado da expressão `ident` da ficha."""
        i = texto_ficha.index(f"### {ident}")
        cab, corpo = texto_ficha[:i], texto_ficha[i:]
        a = corpo.index("```") + 3
        b = corpo.index("```", a)
        return cab + corpo[:a] + transforma(corpo[a:b]) + corpo[b:]

    def com_bloco_novo(texto_ficha, ident, bloco):
        """Acrescenta um bloco cercado à expressão `ident`, que não tinha forma."""
        i = texto_ficha.find(f"### {ident}")
        if i < 0:
            return texto_ficha
        j = texto_ficha.find("**Facetas:**", i)
        if j < 0:
            return texto_ficha
        fim = texto_ficha.find("\n", j)
        if fim < 0:
            return texto_ficha
        return texto_ficha[:fim + 1] + "\n```\n" + bloco + "\n```\n" + texto_ficha[fim + 1:]

    casos = [
        ("conjunto #n devolvido ao bloco executado", "wos",
         com_bloco(original, "EB4", lambda b: b.replace("\nTS=", "\n#5 AND TS=", 1)),
         ("referência a conjunto",)),
        ("termo do bloco executado defasado da seção 3", "wos",
         com_bloco(original, "EB4", lambda b: b.replace('"prática"', '"praxis"', 1)),
         ("do bloco não consta das facetas declaradas",
          "das facetas declaradas não está no bloco")),
        ("termo alterado só na seção 3", "wos",
         original.replace('"prática" OR', '"praxis" OR', 1),
         ("do bloco não consta das facetas declaradas",
          "das facetas declaradas não está no bloco")),
        ("termo do bloco executado particionado defasado da seção 3", "eric",
         com_bloco(controle, "EB4", lambda b: b.replace("abstract:practice",
                                                       "abstract:praxis", 1)),
         ("do bloco não consta das facetas declaradas",)),
        ("conjunto #n devolvido ao bloco de fidelidade", "wos",
         com_bloco(original, "EB2", lambda b: b.replace("\nTS=", "\n#5 AND TS=", 1)),
         ("referência a conjunto",)),
        ("termo do bloco de sonda defasado da seção 3", "wos",
         com_bloco(original, "EB5",
                   lambda b: b.replace('"knowledge representation"',
                                       '"knowledge representation X"', 1)),
         ("do bloco não consta das facetas declaradas",
          "das facetas declaradas não está no bloco")),
        ("bloco devolvido à expressão derivada padrão", "wos",
         com_bloco_novo(original, "EB1", 'TS=("ontologia")'),
         ("expressão derivada não se executa e não leva bloco",)),
    ]
    for nome, base_mut, mutante, esperas in casos:
        n += 1
        referencia = original if base_mut == "wos" else controle
        if mutante == referencia:
            print(f"  [FALHA] mutação não aplicada: {nome}")
            falhas += 1
            continue
        por_base = {s: problemas_de(s, mutante if s == base_mut else ficha(d, s))
                    for s in siglas}
        outras = {s: p for s, p in por_base.items() if s != base_mut and p}
        achados = [p for p in por_base[base_mut] if any(e in p for e in esperas)]
        faltam = [e for e in esperas if not any(e in p for p in por_base[base_mut])]
        if not faltam and not outras:
            print(f"  [ok] reprovou: {nome} — só a {base_mut.upper()} — "
                  f"{achados[0][:80]}")
        else:
            print(f"  [FALHA] {nome}: {base_mut.upper()} "
                  f"{'faltou ' + str(faltam) if faltam else 'reprovou'}, outras reprovadas "
                  f"{sorted(outras)}")
            falhas += 1

    # A forma longa é representação não executada: o bloco nela não é recusado pela regra
    # que fecha a derivada padrão.
    n += 1
    base_longa = base_derivada("wos", d, original)
    base_longa["expressoes"]["EB1"]["blocos"] = [{"rotulo": "", "texto": 'TS=("ontologia")'}]
    base_longa["expressoes"]["EB1"]["forma_longa"] = True
    problemas_longa = cobertura_base("wos", base_longa, d)
    if not any("expressão derivada" in p for p in problemas_longa):
        print("  [ok] forma longa com bloco não é recusada pela regra da derivada")
    else:
        print(f"  [FALHA] forma longa recusada: {problemas_longa[:1]}")
        falhas += 1
    return falhas, n


def _autoteste_composicao():
    """Prova da composição da derivação, que vive em `derivar_expressoes.py`.

    Importada aqui para que o autoteste do projeto seja um só comando. Falha de importação
    é falha do caso, não caso não executado: o script é parte do projeto.
    """
    import importlib.util
    caminho = pathlib.Path(__file__).resolve().parent / "derivar_expressoes.py"
    try:
        spec = importlib.util.spec_from_file_location("derivar_expressoes", caminho)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:                                          # noqa: BLE001
        print(f"  [FALHA] {caminho.name} não carregou: {e}")
        return 1, 1
    return mod._autoteste_composicao()


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
    f_s, n_s = _autoteste_estrutural(t, d)
    f_v, n_v = _autoteste_validacao(t, d)
    f_d, n_d, x_d, motivo_d = _autoteste_dados(d)
    f_b, n_b = _autoteste_bases(d)
    f_e, n_e = _autoteste_composicao()
    falhas += f_p + f_c + f_s + f_v + f_d + f_b + f_e
    executados = len(mut) + n_p + n_c + n_s + n_v + n_d + n_b + n_e
    parcial = ""
    if x_d:
        parcial = (
            f"\n\nAUTOTESTE PARCIAL: {x_d} de {executados + x_d} casos NÃO foram "
            f"executados — os das conferências dos arquivos alimentados ({motivo_d}).\n"
            f"Esses casos não foram aprovados nem reprovados: não se sabe se a conferência "
            f"dos arquivos alimentados reprova os defeitos que deveria.\n"
            f"O código de saída {1 if falhas else 0} se refere apenas aos {executados} casos "
            f"executados.\n"
            f"Para executá-los: gerar {SEMENTES.relative_to(RAIZ)} (src/protocolo.py "
            f"--sincronizar) e {REGISTRO.relative_to(RAIZ)} (src/derivar_expressoes.py "
            f"--registrar) e rodar de novo.")
    if falhas:
        print(f"\n{falhas} caso(s) do autoteste falharam.{parcial}")
        return 1
    dados = f"{n_d} nas conferências dos arquivos alimentados, " if n_d else ""
    print(f"\n{'Todos os' if not x_d else 'Os'} {executados} casos executados tiveram o "
          f"resultado esperado: {len(mut)} defeitos injetados no documento, {n_p} casos de "
          f"precedência, {n_c} de configuração, {n_s} de leitura estrutural que aprova, "
          f"{n_v} de planejamento da validação, "
          f"{dados}{n_b} nas fichas das bases, {n_e} da prova da composição da "
          f"derivação.{parcial}")
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
