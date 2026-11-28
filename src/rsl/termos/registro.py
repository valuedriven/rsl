"""Os dois registros da validação terminológica: decisões do ReT e resultado técnico.

O registro é dividido pelo critério de quem o edita:

- **decisões** (`[dados] validacao`, TOML): uma tabela `[[decisoes]]` por termo, idioma e
  instrumento decidido, com as quatro chaves de identificação (`faceta`, `idioma`, `termo`,
  `instrumento`) e, quando houver, os campos de decisão `decisao_ReT`, `justificativa_ReT`
  e `data_decisao`. É o arquivo que o pesquisador edita à mão; a regravação normaliza o
  texto e descarta comentários escritos à mão, reemitindo o cabeçalho.
- **resultado técnico** (`[dados] consulta_terminologica`, JSON): um objeto por chave
  consultada (ou interrompida), com os dados da consulta, a resposta do instrumento e o
  caminho da evidência. Ninguém o edita à mão: é escrito só pelo script.

A chave lógica dos dois é `(faceta, idioma, termo normalizado, instrumento)`. A ausência de
um objeto no resultado técnico significa "aguardando consulta"; linha de instrumento
`Manual` não é gravada, porque a pendência manual se deriva do protocolo.

A evidência gerenciada é `<instrumento>/<16 hex>.json` sob `[dados] evidencia`, com o nome
derivado de `instrumento|idioma|termo`. O expurgo calcula o caminho esperado de **todas** as
chaves do protocolo e remove os arquivos gerenciados que não pertencem a chave alguma,
preservando as pastas reservadas (`instrumentos`, `sondagens`, `openalex`, `crossref`,
`referencias`, `zotero`) e qualquer arquivo que não tenha o nome de 16 hex. O expurgo é
bloqueado quando uma linha consultada aponta evidência ausente.

Este módulo não decide: valida a forma, lê, escreve e expurga.
"""

import datetime
import hashlib
import json
import os
import pathlib
import re
import tomllib

from .. import gramatica as G
from ..config import relativo
from ..erros import DadosInvalidos
from ..leitura import instrumentos_do_termo
from ..markdown import normaliza
from .planejamento import OBS_AGUARDANDO

CAMPOS_ID = ("faceta", "idioma", "termo", "instrumento")
CAMPOS_DECISAO = ("decisao_ReT", "justificativa_ReT", "data_decisao")
CAMPOS_CONSULTA = ("consultado_em", "versao_instrumento", "url_consultada", "status_proposto")
CAMPOS_RESPOSTA = ("rotulo_autorizado", "forma_no_instrumento", "sugestao_similar",
                   "uri_conceito",
                   "equivalentes_USE_UP", "termos_genericos_TG", "termos_especificos_TE",
                   "termos_relacionados_TR", "nota_de_escopo")
CAMPOS_TECNICOS = CAMPOS_CONSULTA + CAMPOS_RESPOSTA + (
    "arquivo_evidencia", "observacao_tecnica")
# Ordem de gravação do objeto do resultado técnico (a mesma do arquivo versionado).
ORDEM_RESULTADO = CAMPOS_ID + ("consultado_em", "versao_instrumento", "url_consultada",
                               "status_proposto") + CAMPOS_RESPOSTA + (
                                   "arquivo_evidencia", "observacao_tecnica")

CABECALHO_DECISOES = (
    "# Decisões do ReT sobre o controle terminológico.\n"
    "# Editar só os campos decisao_ReT, justificativa_ReT e data_decisao.\n"
    "# A regravação normaliza o arquivo e descarta comentários escritos à mão.\n")

_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_EVIDENCIA = re.compile(r"^[0-9a-f]{16}\.json$")
RESERVADAS = frozenset({"instrumentos", "sondagens", "openalex", "crossref", "referencias",
                        "zotero"})


def chave(faceta, idioma, termo, instrumento):
    """Chave lógica dos dois registros: faceta, idioma, termo normalizado e instrumento."""
    return (str(faceta), idioma, normaliza(termo), instrumento)


def _texto(valor, onde, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise DadosInvalidos(f"{onde}: `{campo}` vazio ou de outro tipo")
    return valor.strip()


def _data(valor, onde, item):
    """Data de decisão em `AAAA-MM-DD`; aceita a data nativa do TOML e grava texto.

    A mensagem nomeia o termo e o instrumento: a tabela é editada à mão e o índice sozinho
    não diz qual decisão corrigir."""
    quem = f"{item['termo']!r} ({item['faceta']}, {item['idioma']}, {item['instrumento']})"
    if isinstance(valor, datetime.datetime):
        raise DadosInvalidos(f"{onde}: `data_decisao` de {quem} com hora; a forma admitida é "
                             f"AAAA-MM-DD")
    if isinstance(valor, datetime.date):
        return valor.isoformat()
    if isinstance(valor, str):
        valor = valor.strip()
        if _DATA.fullmatch(valor):
            try:
                return datetime.date.fromisoformat(valor).isoformat()
            except ValueError:
                pass
    raise DadosInvalidos(f"{onde}: `data_decisao` de {quem} {valor!r} fora da forma admitida "
                         f"AAAA-MM-DD")


# ------------------------------------------------------------------------ leitura TOML
def le_decisoes(texto, caminho):
    """Tabelas de decisão do TOML, na ordem do arquivo. DadosInvalidos se ilegível."""
    if texto is None:
        return []
    try:
        dado = tomllib.loads(texto)
    except tomllib.TOMLDecodeError as e:
        raise DadosInvalidos(f"{caminho}: arquivo de decisões ilegível ({e})") from None
    desconhecidas = sorted(set(dado) - {"decisoes"})
    if desconhecidas:
        raise DadosInvalidos(f"{caminho}: chave desconhecida {desconhecidas}; o único vetor "
                             f"de topo é `decisoes`")
    tabelas = dado.get("decisoes", [])
    if not isinstance(tabelas, list):
        raise DadosInvalidos(f"{caminho}: `decisoes` não é lista de tabelas")
    permitidos = set(CAMPOS_ID) | set(CAMPOS_DECISAO)
    saida, vistas = [], {}
    for i, t in enumerate(tabelas, 1):
        onde = f"{caminho}: decisoes[{i}]"
        if not isinstance(t, dict):
            raise DadosInvalidos(f"{onde}: não é tabela")
        fora = sorted(set(t) - permitidos)
        if fora:
            raise DadosInvalidos(f"{onde}: campo desconhecido {fora} (admitidos: "
                                 f"{sorted(permitidos)})")
        item = {}
        for campo in CAMPOS_ID:
            if campo not in t:
                raise DadosInvalidos(f"{onde}: falta a chave de identificação `{campo}`")
            item[campo] = _texto(t[campo], onde, campo)
        k = chave(item["faceta"], item["idioma"], item["termo"], item["instrumento"])
        if k in vistas:
            raise DadosInvalidos(f"{onde}: chave repetida ({item['faceta']}, {item['idioma']}, "
                                 f"{item['termo']!r}, {item['instrumento']})")
        vistas[k] = onde
        for campo in CAMPOS_DECISAO:
            if campo not in t:
                continue
            if campo == "data_decisao":
                valor = _data(t[campo], onde, item)
            else:
                valor = t[campo]
                if not isinstance(valor, str):
                    raise DadosInvalidos(f"{onde}: `{campo}` não é texto")
                valor = valor.strip()
            if valor:
                item[campo] = valor
        saida.append(item)
    return saida


def escreve_decisoes(tabelas):
    """Texto TOML determinístico: as tabelas na ordem recebida, sem campo de decisão vazio."""
    partes = [CABECALHO_DECISOES.rstrip()]
    for t in tabelas:
        if not any((t.get(c) or "").strip() for c in CAMPOS_DECISAO):
            continue
        linhas = ["[[decisoes]]"]
        for campo in CAMPOS_ID:
            linhas.append(f"{campo} = {_string(t.get(campo, ''))}")
        for campo in CAMPOS_DECISAO:
            valor = (t.get(campo) or "").strip()
            if valor:
                linhas.append(f"{campo} = {_string(valor)}")
        partes.append("\n".join(linhas))
    return "\n\n".join(partes) + "\n"


def _string(valor):
    """String básica TOML: os escapes do JSON são válidos em TOML e evitam um escape próprio."""
    return json.dumps(str(valor), ensure_ascii=False)


# ------------------------------------------------------------------------ leitura JSON
def le_resultado(texto, caminho):
    """Objetos do resultado técnico, na ordem do arquivo. DadosInvalidos se ilegível."""
    if texto is None:
        return []
    try:
        dado = json.loads(texto)
    except json.JSONDecodeError as e:
        raise DadosInvalidos(f"{caminho}: resultado técnico ilegível ({e})") from None
    if not isinstance(dado, dict):
        raise DadosInvalidos(f"{caminho}: resultado técnico não é um objeto")
    desconhecidas = sorted(set(dado) - {"linhas"})
    if desconhecidas:
        raise DadosInvalidos(f"{caminho}: chave desconhecida {desconhecidas}; a única chave de "
                             f"topo é `linhas`")
    linhas = dado.get("linhas")
    if not isinstance(linhas, list):
        raise DadosInvalidos(f"{caminho}: falta o vetor `linhas`")
    permitidos = set(CAMPOS_ID) | set(CAMPOS_TECNICOS)
    saida, vistas = [], {}
    for i, t in enumerate(linhas, 1):
        onde = f"{caminho}: linhas[{i}]"
        if not isinstance(t, dict):
            raise DadosInvalidos(f"{onde}: não é objeto")
        fora = sorted(set(t) - permitidos)
        if fora:
            raise DadosInvalidos(f"{onde}: campo desconhecido {fora} (admitidos: "
                                 f"{sorted(permitidos)})")
        item = {}
        for campo in CAMPOS_ID:
            if campo not in t:
                raise DadosInvalidos(f"{onde}: falta a chave de identificação `{campo}`")
            item[campo] = _texto(t[campo], onde, campo)
        k = chave(item["faceta"], item["idioma"], item["termo"], item["instrumento"])
        if k in vistas:
            raise DadosInvalidos(f"{onde}: chave repetida ({item['faceta']}, {item['idioma']}, "
                                 f"{item['termo']!r}, {item['instrumento']})")
        vistas[k] = onde
        for campo in CAMPOS_TECNICOS:
            if campo not in t:
                continue
            valor = t[campo]
            if not isinstance(valor, str):
                raise DadosInvalidos(f"{onde}: `{campo}` não é texto")
            valor = valor.strip()
            if valor:
                item[campo] = valor
        saida.append(item)
    return saida


def escreve_resultado(linhas):
    """Texto JSON do resultado técnico, com campo vazio omitido."""
    objetos = []
    for linha in linhas:
        objeto = {}
        for campo in ORDEM_RESULTADO:
            valor = (linha.get(campo) or "").strip() if isinstance(linha.get(campo), str) \
                else linha.get(campo)
            if valor:
                objeto[campo] = valor
        objetos.append(objeto)
    return json.dumps({"linhas": objetos}, ensure_ascii=False, indent=2) + "\n"


# --------------------------------------------------------------------------- gravação
def _grava(caminho, texto):
    caminho = pathlib.Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_name(caminho.name + ".tmp")
    temporario.write_text(texto, encoding="utf-8")
    os.replace(temporario, caminho)


def grava_decisoes(caminho, tabelas):
    _grava(caminho, escreve_decisoes(tabelas))


def grava_resultado(caminho, linhas):
    _grava(caminho, escreve_resultado(linhas))


# --------------------------------------------------------------------------- evidência
def caminho_evidencia(pasta, instrumento, idioma, termo):
    """Caminho da evidência gerenciada de uma chave."""
    nome = hashlib.sha1(f"{instrumento}|{idioma}|{termo}".encode("utf-8")).hexdigest()[:16]
    return pathlib.Path(pasta) / instrumento.lower() / f"{nome}.json"


def chaves_do_protocolo(d):
    """(faceta, idioma, termo, instrumento) de todas as chaves planejadas, na ordem do
    protocolo, inclusive as nunca consultadas e as de instrumento `Manual`."""
    for f in d["tabelas"]:
        for idioma in d["idiomas"]:
            for termo in f["termos"][idioma]:
                for i in instrumentos_do_termo(d, f["id"], idioma):
                    yield f["id"], idioma, termo, i


def caminhos_esperados(pasta, d):
    """Conjunto de caminhos de evidência esperados para todas as chaves do protocolo."""
    return {caminho_evidencia(pasta, i["sigla"], idioma, termo).resolve()
            for _, idioma, termo, i in chaves_do_protocolo(d)}


def confere_evidencia(pasta, linhas):
    """Reprova quando uma linha com `status_proposto` aponta evidência ausente."""
    for linha in linhas:
        if not linha.get("status_proposto"):
            continue
        arquivo = (linha.get("arquivo_evidencia") or "").strip()
        if not arquivo:
            raise DadosInvalidos(
                f"linha consultada de {linha.get('termo')!r} ({linha.get('faceta')}, "
                f"{linha.get('idioma')}, {linha.get('instrumento')}) sem "
                f"`arquivo_evidencia`; nada foi expurgado")
        caminho = pathlib.Path(arquivo)
        if not caminho.is_absolute():
            caminho = pathlib.Path(pasta).parent / caminho
        if not caminho.is_file():
            raise DadosInvalidos(
                f"{relativo(caminho)}: evidência ausente para "
                f"{linha.get('termo')!r} ({linha.get('faceta')}, {linha.get('idioma')}, "
                f"{linha.get('instrumento')}); nada foi expurgado")


def expurga(pasta, esperados):
    """Remove a evidência gerenciada fora do conjunto esperado. Devolve os caminhos."""
    pasta = pathlib.Path(pasta)
    removidos = []
    if not pasta.is_dir():
        return removidos
    for sub in sorted(pasta.iterdir()):
        if not sub.is_dir() or sub.name in RESERVADAS:
            continue
        for arq in sorted(sub.iterdir()):
            if arq.is_file() and _EVIDENCIA.fullmatch(arq.name) \
                    and arq.resolve() not in esperados:
                arq.unlink()
                removidos.append(arq)
    return removidos


def tem_linha_tecnica(v, instrumento):
    """A linha vira objeto do resultado técnico? Só a chave consultada ou interrompida;
    nunca a pendente de consulta nem a de instrumento `Manual`."""
    if instrumento["modo"] == G.MODO_MANUAL:
        return False
    if v.get("status_proposto"):
        return True
    if any(v.get(c) for c in CAMPOS_CONSULTA if c != "status_proposto"):
        return True
    if any(v.get(c) for c in CAMPOS_RESPOSTA):
        return True
    obs = (v.get("observacao_tecnica") or "").strip()
    return bool(obs) and obs != OBS_AGUARDANDO
