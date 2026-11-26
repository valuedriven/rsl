"""Leitores das exportações das bases: RIS, texto plano da Web of Science, CSV e TSV."""

import csv
import pathlib
import re

# Separador entre valores de um mesmo campo (várias palavras-chave, várias colunas de
# palavras-chave): o casamento local o usa para não casar termo através de dois valores.
SEPARADOR_VALORES = "; "

CAMPOS = ("titulo", "resumo", "palavras_chave", "ano", "doi", "id_base", "autores", "fonte")
# Campos lidos para a anatomia da perda (ano, idioma e tipo documental da semente
# filtrada). Não entram nas saídas da derivação, que usam `CAMPOS`.
EXTRAS = ("idioma", "tipo")


def vazio():
    return {k: "" for k in CAMPOS + EXTRAS}


def le_ris(texto):
    regs, atual = [], vazio()
    mapa = {"TI": "titulo", "T1": "titulo", "AB": "resumo", "N2": "resumo",
            "KW": "palavras_chave", "PY": "ano", "Y1": "ano", "DO": "doi",
            "AU": "autores", "JO": "fonte", "T2": "fonte", "ID": "id_base",
            "LA": "idioma", "TY": "tipo"}
    for linha in texto.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])\s+-\s?(.*)$", linha)
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "ER":
            if atual["titulo"]:
                regs.append(atual)
            atual = vazio()
        elif tag in mapa:
            campo = mapa[tag]
            atual[campo] = (atual[campo] + SEPARADOR_VALORES + val).strip(SEPARADOR_VALORES) \
                if atual[campo] else val
    if atual["titulo"]:
        regs.append(atual)
    return regs


def le_wos_txt(texto):
    """Exportação 'Plain text' da Web of Science: campos de duas letras."""
    regs, atual, tag = [], vazio(), None
    mapa = {"TI": "titulo", "AB": "resumo", "DE": "palavras_chave", "ID": "palavras_chave",
            "PY": "ano", "DI": "doi", "AF": "autores", "AU": "autores", "SO": "fonte",
            "UT": "id_base", "LA": "idioma", "DT": "tipo"}
    for linha in texto.splitlines():
        if linha.startswith("ER"):
            if atual["titulo"]:
                regs.append(atual)
            atual, tag = vazio(), None
            continue
        m = re.match(r"^([A-Z0-9]{2}) (.*)$", linha)
        if m:
            tag, val = m.group(1), m.group(2).strip()
        elif linha.startswith("   ") and tag:
            val = linha.strip()
        else:
            continue
        if tag in mapa:
            campo = mapa[tag]
            atual[campo] = (atual[campo] + " " + val).strip() if atual[campo] else val
    if atual["titulo"]:
        regs.append(atual)
    return regs


ALIAS = {
    "titulo": ("title", "article title", "titulo", "título", "ti"),
    "resumo": ("abstract", "resumo", "ab"),
    "palavras_chave": ("author keywords", "keywords", "palavras-chave", "index keywords",
                       "keywords plus", "de", "id"),
    "ano": ("publication year", "year", "ano", "py"),
    "doi": ("doi", "di"),
    "id_base": ("ut (unique wos id)", "ut", "eid", "accession number", "id"),
    "autores": ("authors", "author full names", "autores", "af", "au"),
    "fonte": ("source title", "journal", "fonte", "so"),
    "idioma": ("language", "idioma", "la"),
    "tipo": ("document type", "tipo documental", "tipo", "dt"),
}


def le_tabela(caminho, delim):
    regs = []
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        leitor = csv.DictReader(fh, delimiter=delim)
        cols = {(c or "").strip().lower(): c for c in (leitor.fieldnames or [])}
        casa = {}
        for campo, nomes in ALIAS.items():
            for n in nomes:
                if n in cols:
                    casa.setdefault(campo, []).append(cols[n])
        for linha in leitor:
            r = vazio()
            for campo, origens in casa.items():
                r[campo] = SEPARADOR_VALORES.join(str(linha.get(o) or "").strip()
                                     for o in origens if linha.get(o))
            if r["titulo"]:
                regs.append(r)
    return regs


def le_arquivo(caminho):
    caminho = pathlib.Path(caminho)
    ext = caminho.suffix.lower()
    if ext == ".ris":
        return le_ris(caminho.read_text(encoding="utf-8", errors="replace"))
    if ext == ".csv":
        return le_tabela(caminho, ",")
    if ext in (".tsv", ".tab"):
        return le_tabela(caminho, "\t")
    if ext == ".txt":
        texto = caminho.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^(PT|FN|VR) ", texto, re.M):
            return le_wos_txt(texto)
        if "\t" in texto.splitlines()[0]:
            return le_tabela(caminho, "\t")
        return le_ris(texto)
    return []
