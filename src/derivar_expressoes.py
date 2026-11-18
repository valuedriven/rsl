#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Derivação local das expressões não executadas (EB4 é a executada; EB5 é a sonda) — RS Banyan, Módulo 3, Etapa 2.

Protocolo v2. Cinco expressões, montadas como AND de grupos de facetas, em que um grupo
pode ser uma disjunção: EB1 = 1+2+3+4; EB2 = 1+2+3; EB3 = 1+2+4; EB4 = 1+2+(3 OR 4);
EB5 = 1+2. Daí EB4 = EB2 ∪ EB3, e EB5 ⊃ EB4. Executa-se EB4, a de cobertura, uma vez
por base; EB5 roda uma única vez como sonda de sensibilidade. A pertinência de cada
registro às demais é calculada aqui.

O que este script NÃO faz: não exclui registro algum, não decide inclusão e não
substitui o teste de fidelidade. As contagens que produz são DERIVADAS e devem ser
declaradas como tal no IO 2 e no relatório.

Entradas
  docs/03_protocolo_estrategia_pesquisa.md   vocabulário, composição e recorte (lido por src/protocolo.py)
  data/registro_execucao.json  registro documental e rastro técnico das execuções,
                               escrito por --registrar
  data/sementes.json       metadados autorais das sementes, ligados por DOI ou título
  <arquivo> de cada consulta registrada, intacto, onde estiver

O protocolo é lido diretamente: não há derivado intermediário a manter em dia.

Saídas na raiz de data/
  registros.csv        um registro por linha, com as facetas e expressões atingidas,
                       a chave de ordenação de leitura e a marca de duplicata
  io2_contagens.csv    base x expressão, para alimentar o IO 2
  ordem_triagem.csv    a fila da 1ª filtragem já ordenada (Medida 4)
  fidelidade_EB<n>.csv as divergências do teste, item a item
  sensibilidade_<base>.csv  a fração de EB5 fora de EB4, com a amostra a classificar

Deduplicação: dentro da mesma base, registro com o mesmo DOI — ou, na falta dele, o
mesmo título normalizado — é marcado em `duplicata_de` com o identificador da primeira
ocorrência. Nada é apagado; as contagens do IO 2 usam os registros únicos e o número
bruto sai ao lado. É o que faz a exportação da ERIC em vários arquivos não contar duas
vezes o mesmo registro.

Uso
  python3 src/derivar_expressoes.py --registrar wos EB4 data/execucoes/wos/e4.ris --retorno 18432
  python3 src/derivar_expressoes.py --registrar wos EB5 data/execucoes/wos/e5_sonda.ris --retorno 22014
  python3 src/derivar_expressoes.py --derivar
  python3 src/derivar_expressoes.py --aderencia
  python3 src/derivar_expressoes.py --fidelidade EB2 data/execucoes/wos/e2_conferencia.ris
  python3 src/derivar_expressoes.py --sensibilidade wos
"""

import argparse
import csv
import itertools
import datetime
import json
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import protocolo                                                    # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
REGISTRO = DATA / "registro_execucao.json"
SAIDA = DATA


def _mostra(caminho):
    """Caminho relativo ao repositório quando possível; absoluto quando não."""
    try:
        return str(pathlib.Path(caminho).relative_to(RAIZ))
    except ValueError:
        return str(caminho)

# O documento é a única fonte: vocabulário, composição e recorte vêm de lá.
_D = protocolo.analisa()
_STR = _D["strings"]
FACETA_DE = {v["id"]: fid for fid, v in _STR.items()}
# Composição em grupos: cada EB é um AND de grupos; cada grupo é uma disjunção de facetas.
GRUPOS = {eb: [[FACETA_DE[s] for s in grupo] for grupo in grupos]
          for eb, grupos in _D["expressoes"].items()}
SUPERCONJUNTO = _D["executada"]
SONDA = _D["sonda"]
ANCORAS = {f["id"] for f in _D["facetas"] if f.get("ancora")}

# Recorte temporal do protocolo, aplicado como CONFERÊNCIA em todas as bases. Na
# Web of Science, na Scopus e na BRAPCI o filtro de ano vai na própria consulta;
# na ERIC, onde os operadores de ano zeram o retorno em consulta com grupos, ele
# é aplicado pelos filtros da página de resultados. Em nenhuma delas esta etapa
# deveria retirar registro: se retirar, há divergência entre o que a consulta ou
# o filtro declararam e o que a base devolveu, e isso se investiga.
# Registro sem ano legível NÃO é descartado: fica com ano = 0 e sai marcado,
# porque descartar por ausência de metadado seria corte cego.
ANO_MIN = int(_D["recorte"]["ano_min"])
# O protocolo diz "de 2017 em diante", sem teto: o limite superior é o ano corrente.
ANO_MAX = int(_D["recorte"]["ano_max"] or datetime.date.today().year)
LIMITE_DIVERGENCIA = 0.10     # 10% — acima disso o método é reprovado
LIMITE_SENSIBILIDADE = (0.05, 0.15)   # faixa da fração ELEGÍVEL entre os perdidos

STATUS_VALIDOS = ("valida", "divergente_justificada")
BASE_CANONICA = {"wos": "WoS", "scopus": "Scopus", "eric": "ERIC", "brapci": "BRAPCI"}
BD_DE = {BASE_CANONICA[slug]: info["bd"] for slug, info in protocolo.FICHAS.items()}
SLUG_DE_BD = {info["bd"]: slug for slug, info in protocolo.FICHAS.items()}


def _base_canonica(base):
    s = str(base or "").strip()
    return BASE_CANONICA.get(s.lower(), s)


def _bd_de(base):
    s = str(base or "").strip()
    if s.upper() in SLUG_DE_BD:
        bd = s.upper()
        return bd, BASE_CANONICA[SLUG_DE_BD[bd]]
    nome = _base_canonica(s)
    return BD_DE.get(nome), nome


# ------------------------------------------------------------------ normalização
def normaliza(txt):
    t = unicodedata.normalize("NFD", (txt or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def padrao(termo):
    """Casamento por palavra inteira, com flexão simples de plural.

    O '*' do termo vira prefixo livre. Cada palavra admite sufixo de plural
    opcional (s/es), o que aproxima — sem reproduzir — a lematização que as bases
    aplicam em TS= e TITLE-ABS-KEY. É justamente essa aproximação que o teste de
    fidelidade mede: ela é a origem esperada da divergência."""
    t = normaliza(termo.replace("*", "\x00"))
    partes = []
    for palavra in t.split():
        if "\x00" in palavra:
            partes.append(re.escape(palavra).replace("\x00", r"\w*"))
        else:
            partes.append(re.escape(palavra) + r"(?:e?s)?")
    return re.compile(r"(?<!\w)" + r"\s+".join(partes) + r"(?!\w)")


def carrega_facetas():
    """Facetas e padrões de casamento, da lista executada de cada faceta no protocolo."""
    facetas = {}
    for fid, v in _STR.items():
        vistos, limpos = set(), []
        for t in v["termos"]:
            k = t.lower()
            if k not in vistos:
                vistos.add(k)
                limpos.append(t)
        nome = next((f["nome"] for f in _D["facetas"] if f["id"] == fid), "")
        facetas[fid] = {"nome": nome, "termos": limpos,
                        "padroes": [padrao(t) for t in limpos]}
    return facetas


# --------------------------------------------------------------------- leitores
CAMPOS = ("titulo", "resumo", "palavras_chave", "ano", "doi", "id_base", "autores", "fonte")


def vazio():
    return {k: "" for k in CAMPOS}


def le_ris(texto):
    regs, atual = [], vazio()
    mapa = {"TI": "titulo", "T1": "titulo", "AB": "resumo", "N2": "resumo",
            "KW": "palavras_chave", "PY": "ano", "Y1": "ano", "DO": "doi",
            "AU": "autores", "JO": "fonte", "T2": "fonte", "ID": "id_base"}
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
            atual[campo] = (atual[campo] + "; " + val).strip("; ") if atual[campo] else val
    if atual["titulo"]:
        regs.append(atual)
    return regs


def le_wos_txt(texto):
    """Exportação 'Plain text' da Web of Science: campos de duas letras."""
    regs, atual, tag = [], vazio(), None
    mapa = {"TI": "titulo", "AB": "resumo", "DE": "palavras_chave", "ID": "palavras_chave",
            "PY": "ano", "DI": "doi", "AF": "autores", "AU": "autores", "SO": "fonte",
            "UT": "id_base"}
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
                r[campo] = "; ".join(str(linha.get(o) or "").strip()
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


# ------------------------------------------------------------------- derivação
def texto_do(reg):
    return normaliza(" ".join((reg["titulo"], reg["resumo"], reg["palavras_chave"])))


def facetas_atingidas(reg, facetas):
    alvo = texto_do(reg)
    return {n for n, f in facetas.items() if any(p.search(alvo) for p in f["padroes"])}


def satisfaz(ident, fac):
    """Pertinência a uma expressão: todo grupo satisfeito, cada grupo por uma faceta."""
    return all(any(f in fac for f in grupo) for grupo in GRUPOS[ident])


def expressoes_de(fac):
    """Expressões do corpus a que o registro pertence — a sonda fica de fora.

    EB5 não compõe o corpus e só se mede contra a exportação própria; listá-la aqui diria
    que todo registro de EB4 pertence a EB5, o que é verdade e não informa nada.
    """
    return [n for n in GRUPOS if n != SONDA and satisfaz(n, fac)]


def _derivaveis():
    """Expressões cujo conjunto está contido na executada, provado sobre as 16 combinações.

    EB5 é superconjunto de EB4: a pertinência a ela NÃO se calcula sobre a exportação da
    de cobertura, porque os registros que só EB5 recupera não estão nesse arquivo. Ela
    entra pela sonda, com execução própria, e por isso fica fora desta lista.
    """
    todas = sorted(set(FACETA_DE.values()))
    conjuntos = {eb: set() for eb in GRUPOS}
    for r in range(len(todas) + 1):
        for combo in itertools.combinations(todas, r):
            fac = set(combo)
            for eb in GRUPOS:
                if satisfaz(eb, fac):
                    conjuntos[eb].add(frozenset(combo))
    alvo = conjuntos[SUPERCONJUNTO]
    return {eb for eb, s in conjuntos.items() if eb != SUPERCONJUNTO and s <= alvo}


DERIVAVEIS = _derivaveis()


def _prova_da_composicao():
    """Confere a álgebra das expressões sobre as 16 combinações de faceta.

    A prova existe porque o caso degenerado passa em silêncio: com a lista de facetas
    errada, as 16 combinações dão todas falsas, `EB4 = EB2 ∪ EB3` vale trivialmente e o
    erro só aparece quando a busca roda. Por isso toda expressão precisa ser satisfeita
    por ao menos uma combinação, além das contenções.
    """
    facetas = sorted(set(FACETA_DE.values()))
    combos = [set(c) for r in range(len(facetas) + 1)
              for c in itertools.combinations(facetas, r)]
    problemas = []
    if {"EB1", "EB2", "EB3", "EB4", "EB5"} - set(GRUPOS):
        return [f"expressões esperadas ausentes: {sorted(set(GRUPOS))}"]
    for eb in GRUPOS:
        if not any(satisfaz(eb, f) for f in combos):
            problemas.append(f"{eb} não é satisfeita por nenhuma combinação de facetas — "
                             f"mapeamento de faceta provavelmente errado")
    for f in combos:
        s = {eb: satisfaz(eb, f) for eb in GRUPOS}
        if s["EB4"] != (s["EB2"] or s["EB3"]):
            problemas.append(f"EB4 ≠ EB2 ∪ EB3 em {sorted(f)}")
        if s["EB4"] and not s["EB5"]:
            problemas.append(f"EB5 não contém EB4 em {sorted(f)}")
        if s["EB1"] and not (s["EB2"] and s["EB3"]):
            problemas.append(f"EB1 não está contida em EB2 e EB3 em {sorted(f)}")
    if DERIVAVEIS != {"EB1", "EB2", "EB3"}:
        problemas.append(f"deriváveis de EB4 deveriam ser EB1, EB2 e EB3, não "
                         f"{sorted(DERIVAVEIS)}")
    return problemas


_PROBLEMAS_DA_COMPOSICAO = _prova_da_composicao()
if _PROBLEMAS_DA_COMPOSICAO:
    raise AssertionError("composição das expressões incoerente: "
                         + "; ".join(_PROBLEMAS_DA_COMPOSICAO))


def chave_ordem(reg, exprs):
    """Medida 4: pertinência às expressões ricas primeiro, depois recência.

    Riqueza é o número de grupos de facetas exigidos — EB1 exige quatro, EB4 três.
    É a ordem de leitura, não critério de elegibilidade."""
    riqueza = max((len(GRUPOS[e]) for e in exprs), default=0)
    try:
        ano = int(re.search(r"(19|20)\d{2}", reg["ano"] or "").group(0))
    except Exception:
        ano = 0
    recente = 1 if ano >= 2022 else 0
    return (-riqueza, -recente, -ano)


# ------------------------------------------------------------------ consultas
def _caminho_do_arquivo(c):
    p = pathlib.Path(c.get("arquivo") or "")
    return p if p.is_absolute() else RAIZ / p


def _consultas_do_registro(dado):
    """Execuções com exportação declarada, lidas do registro documental por base."""
    consultas = []
    for bd, base in (dado.get("bases") or {}).items():
        if not isinstance(base, dict):
            continue
        slug = base.get("slug") or SLUG_DE_BD.get(bd, "")
        nome = BASE_CANONICA.get(slug, base.get("base") or bd)
        for e in base.get("execucoes") or []:
            arq = str(e.get("arquivo") or "").strip()
            if not arq:
                continue
            if normaliza(e.get("estado")) in ("vencido", "nao executado"):
                continue
            status = e.get("status") or "valida"
            if status not in STATUS_VALIDOS:
                continue
            consultas.append({
                "id": f"{nome}-{e.get('expressao')}-{pathlib.Path(arq).stem}",
                "base": nome,
                "expressao": e.get("expressao"),
                "data_hora": e.get("data_hora") or e.get("data") or "",
                "retorno_declarado": e.get("retorno"),
                "registros_lidos": e.get("registros_lidos"),
                "arquivo": arq,
                "status": status,
                "justificativa_divergencia": e.get("justificativa_divergencia", ""),
            })
    return consultas


def carrega_consultas(exigir=True):
    if not REGISTRO.exists():
        raise SystemExit("data/registro_execucao.json não encontrado: registre cada execução "
                         "com --registrar antes de derivar")
    try:
        dado = json.loads(REGISTRO.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"data/registro_execucao.json ilegível: {e}")
    validas = [c for c in _consultas_do_registro(dado)
               if c.get("status") in STATUS_VALIDOS]
    if exigir and not validas:
        raise SystemExit(
            "nenhuma execução com exportação registrada em data/registro_execucao.json.\n"
            "  Registre a execução primeiro:\n"
            "  python3 src/derivar_expressoes.py --registrar <base> <expressao> "
            "<arquivo> --retorno <n>")
    return dado, validas


def _id_expressao(expr):
    """Identificador da expressão a partir de `EB4`, `E4` ou `4`; None se não existir."""
    s = str(expr).strip().upper()
    for prefixo in ("EB", "E"):
        if s.startswith(prefixo):
            s = s[len(prefixo):]
            break
    if not s.isdigit():
        return None
    ident = f"EB{int(s)}"
    return ident if ident in GRUPOS else None


def registrar(base, expressao, arquivo, retorno, data_hora=None, justificar=""):
    """Registra uma execução no registro por base e confere o retorno contra o arquivo."""
    caminho = pathlib.Path(arquivo)
    if not caminho.is_absolute():
        caminho = (pathlib.Path.cwd() / caminho)
    if not caminho.exists():
        print(f"Arquivo não encontrado: {arquivo}")
        return 1
    regs = le_arquivo(caminho)
    if not regs:
        print(f"Nenhum registro legível em {arquivo}. Nada foi registrado.")
        return 1

    id_expr = _id_expressao(expressao)
    if id_expr is None:
        print(f"Expressão inválida: {expressao!r}. Use EB1 a EB5.")
        return 1

    bd, nome = _bd_de(base)
    if bd is None:
        print(f"Base inválida: {base!r}. Use wos, scopus, eric, brapci ou BD1 a BD4.")
        return 1

    lidos = len(regs)
    status, just = "valida", ""
    if retorno is None:
        print("Informe --retorno com o número que a base exibiu. Nada foi registrado.")
        return 1
    if int(retorno) != lidos:
        if not justificar:
            print(f"RECUSADO: a base declarou {retorno} registros e o arquivo traz {lidos}.\n"
                  "  Arquivo trocado, exportação parcial ou teto de retorno da base.\n"
                  "  Se a diferença for conhecida e aceitável, repita com --justificar \"motivo\".")
            return 1
        status, just = "divergente_justificada", justificar.strip()

    try:
        rel = str(caminho.resolve().relative_to(RAIZ))
    except ValueError:
        rel = str(caminho.resolve())

    if not REGISTRO.exists():
        print("data/registro_execucao.json não encontrado. Nada foi registrado.")
        return 1
    try:
        dado = json.loads(REGISTRO.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"data/registro_execucao.json ilegível: {e}")
        return 1
    item = (dado.get("bases") or {}).get(bd)
    if not isinstance(item, dict):
        print(f"data/registro_execucao.json sem a base {bd}.")
        return 1
    execucoes = item.setdefault("execucoes", [])
    agora = data_hora or datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    dia = agora[:10]

    achado = next((e for e in execucoes
                   if e.get("arquivo") == rel and e.get("expressao") == id_expr
                   and normaliza(e.get("estado")) not in ("vencido", "nao executado")), None)
    if achado is None:
        ids = {e.get("id") for e in execucoes}
        n = 1
        while f"EX{n}" in ids:
            n += 1
        achado = {
            "id": f"EX{n}",
            "expressao": id_expr,
            "forma": "registrada por --registrar",
            "retorno": int(retorno),
            "data": dia,
            "data_hora": agora,
            "mede": f"{id_expr}, execução registrada",
            "estado": "registrada",
            "origem": "exportacao",
            "arquivo": rel,
            "registros_lidos": lidos,
            "status": status,
            "justificativa_divergencia": just,
        }
        execucoes.append(achado)
    else:
        achado.update({
            "retorno": int(retorno),
            "data": dia,
            "data_hora": agora,
            "arquivo": rel,
            "registros_lidos": lidos,
            "status": status,
            "justificativa_divergencia": just,
        })

    REGISTRO.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")

    print(f"Consulta registrada em data/registro_execucao.json:\n"
          f"  {bd} {achado['id']} — {nome} {id_expr} em {agora}\n"
          f"  retorno declarado {retorno}, registros lidos {lidos} — {status}")
    if status != "valida":
        print(f"  divergência justificada: {just}")
    print("  A data oficial de execução continua sendo a do IO 7.")
    return 0


def coleta(consultas):
    """Lê as exportações registradas e reconfere a contagem de cada uma."""
    tudo = []
    for c in consultas:
        caminho = _caminho_do_arquivo(c)
        if not caminho.exists():
            raise SystemExit(f"consulta {c.get('id')}: arquivo ausente {c.get('arquivo')}")
        regs = le_arquivo(caminho)
        if len(regs) != int(c.get("registros_lidos", -1)):
            raise SystemExit(
                f"consulta {c.get('id')}: o arquivo tem {len(regs)} registros e o registro "
                f"diz {c.get('registros_lidos')}. Arquivo trocado ou reexportado: "
                f"reregistre antes de derivar.")
        for r in regs:
            r["base"] = c.get("base", "?")
            r["arquivo_origem"] = caminho.name
            r["consulta"] = c.get("id", "")
        print(f"  {c.get('id')}: {len(regs)} registros")
        tudo += regs
    return tudo


def chave_dedup(reg):
    d = (reg.get("doi") or "").strip().lower()
    return "doi:" + d if d else "ti:" + normaliza(reg.get("titulo"))[:120]


def identifica(regs):
    """Dá identificador a cada registro e marca a duplicata, sem apagar nada."""
    for i, r in enumerate(regs, 1):
        r["registro"] = f"R{i:05d}"
        r["duplicata_de"] = ""
    vistos = {}
    for r in regs:
        k = chave_dedup(r)
        if k in vistos:
            r["duplicata_de"] = vistos[k]
        else:
            vistos[k] = r["registro"]
    dup = sum(1 for r in regs if r["duplicata_de"])
    if dup:
        print(f"\nDeduplicação: {dup} registro(s) repetido(s) no mesmo DOI ou título, "
              f"marcados em `duplicata_de`. Nenhum foi apagado.")
    return regs


def ano_de(reg):
    """Ano publicado como inteiro; 0 quando não há ano legível no registro."""
    m = re.search(r"(19|20)\d{2}", reg.get("ano") or "")
    return int(m.group(0)) if m else 0


def aplica_recorte(regs):
    """Aplica o recorte temporal e devolve (dentro, fora), com relatório."""
    dentro, fora, sem_ano = [], [], []
    for r in regs:
        a = ano_de(r)
        if a == 0:
            r["recorte"] = "ano ausente"
            sem_ano.append(r)
        elif ANO_MIN <= a <= ANO_MAX:
            r["recorte"] = "dentro"
            dentro.append(r)
        else:
            r["recorte"] = "fora"
            fora.append(r)
    print(f"\nRecorte temporal {ANO_MIN}-{ANO_MAX} (conferência):")
    print(f"  dentro ......... {len(dentro)}")
    print(f"  fora ........... {len(fora)}  (retirados)")
    print(f"  ano ausente .... {len(sem_ano)}  (MANTIDOS e marcados: decidir um a um "
          f"na 1ª filtragem)")
    if fora:
        bases = sorted({r.get("base", "?") for r in fora})
        print(f"  bases de origem dos retirados: {', '.join(bases)}")
        print("  O recorte é aplicado na busca em todas as bases — na consulta ou, na ERIC,")
        print("  pelo filtro da página. Esta linha deveria ser zero: registro fora da janela")
        print("  indica divergência entre o declarado e o devolvido. Investigar antes de")
        print("  prosseguir, e não apenas registrar.")
    print("  Registrar os três números no IO 2.")
    return dentro + sem_ano, fora


def aderencia():
    """Teste de aderência ao conjunto-semente, sobre as consultas registradas.

    Mede recall: quantos dos estudos-semente que a base indexa aparecem na
    exportação. NÃO aplica o recorte temporal — o conjunto-semente valida o
    desenho da busca, não os critérios de elegibilidade.

    As referências vêm do protocolo, seção do conjunto-semente; a coluna
    `indexado` da planilha é o denominador e precisa ser preenchida à mão, base
    por base, buscando cada semente pelo título: ausência por falta de indexação
    não é falha da string.
    """
    sementes = _D["sementes"]
    _, validas = carrega_consultas()
    regs = [r for r in identifica(coleta(validas)) if not r["duplicata_de"]]
    if not regs:
        print("Nenhum registro lido.")
        sys.exit(1)

    def chave(t):
        t = unicodedata.normalize("NFKD", (t or "").lower())
        t = "".join(c for c in t if not unicodedata.combining(c))
        return re.sub(r"[^a-z0-9]+", " ", t).strip()

    idx = {}
    for r in regs:
        idx.setdefault(chave(r.get("titulo")), []).append(r)

    print(f"\nADERÊNCIA AO CONJUNTO-SEMENTE — {len(sementes)} estudos, "
          f"{len(regs)} registros únicos\n")
    achados = 0
    for e in sementes:
        k = chave(e["titulo"])
        casa = idx.get(k)
        if not casa:                      # tentativa por prefixo, para títulos truncados
            casa = [r for kk, v in idx.items() if kk.startswith(k[:60]) for r in v] or None
        if casa:
            achados += 1
            bases = ", ".join(sorted({r.get("base", "?") for r in casa}))
            print(f"  [OK ] {e['id']:>4}. {e['ano']}  {e['titulo'][:58]:<60} {bases}")
        else:
            print(f"  [   ] {e['id']:>4}. {e['ano']}  {e['titulo'][:58]:<60} "
                  f"esperado em: {', '.join(e['bases'])}")
    print(f"\n  recuperados: {achados} de {len(sementes)} sementes "
          f"({achados / len(sementes):.0%} do total informado)")
    print("\n  ATENÇÃO: esta razão NÃO é a aderência. O denominador correto são as sementes que")
    print("  cada base INDEXA, apurado à mão na coluna `indexado` da planilha. Semente ausente")
    print("  por não ser indexada não conta contra a string.")
    print("  Cada ausência acima exige diagnóstico: qual termo a teria alcançado?")


def derivar():
    facetas = carrega_facetas()
    _, validas = carrega_consultas()
    print("Lendo exportações registradas:")
    regs = identifica(coleta(validas))
    if not regs:
        print("Nenhum registro lido.")
        sys.exit(1)
    regs, fora = aplica_recorte(regs)
    unicos = [r for r in regs if not r["duplicata_de"]]

    SAIDA.mkdir(parents=True, exist_ok=True)
    por_registro = {}
    for r in regs:
        fac = facetas_atingidas(r, facetas)
        exprs = expressoes_de(fac)
        if SUPERCONJUNTO not in exprs:
            # registro veio da expressão de cobertura na base, mas o casamento local não
            # confirma as âncoras:
            # é divergência esperada (Keywords Plus, lematização), não motivo de descarte
            exprs = sorted(set(exprs) | {SUPERCONJUNTO})
        por_registro[r["registro"]] = (fac, exprs, chave_ordem(r, exprs))

    unicos.sort(key=lambda r: por_registro[r["registro"]][2])
    ordem = {}
    for i, r in enumerate(unicos, 1):
        ordem[r["registro"]] = i
    linhas = unicos + [r for r in regs if r["duplicata_de"]]

    contagens, brutas = {}, {}
    for r in unicos:
        for n in por_registro[r["registro"]][1]:
            contagens[(r["base"], n)] = contagens.get((r["base"], n), 0) + 1
    for r in regs:
        for n in por_registro[r["registro"]][1]:
            brutas[(r["base"], n)] = brutas.get((r["base"], n), 0) + 1

    cols = list(CAMPOS) + ["base", "arquivo_origem", "consulta", "registro", "duplicata_de",
                           "facetas", "expressoes", "ancoras_confirmadas", "recorte", "ordem"]
    with (SAIDA / "registros.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter=";")
        w.writeheader()
        for r in linhas:
            fac, exprs, _ = por_registro[r["registro"]]
            w.writerow({**{k: r[k] for k in CAMPOS},
                        "base": r["base"], "arquivo_origem": r["arquivo_origem"],
                        "consulta": r["consulta"], "registro": r["registro"],
                        "duplicata_de": r["duplicata_de"],
                        "facetas": " ".join(sorted(fac)),
                        "expressoes": " ".join(sorted(exprs)),
                        "ancoras_confirmadas": "sim" if ANCORAS <= fac else "não",
                        "recorte": r.get("recorte", ""),
                        "ordem": ordem.get(r["registro"], "")})

    bases = sorted({r["base"] for r in regs})
    with (SAIDA / "io2_contagens.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["base", "expressao", "facetas_exigidas", "registros",
                    "registros_com_duplicatas", "procedencia"])
        for b in bases:
            for n in sorted(GRUPOS):
                composicao = "+".join(
                    grupo[0] if len(grupo) == 1 else "(" + "|".join(grupo) + ")"
                    for grupo in GRUPOS[n])
                if n == SONDA:
                    w.writerow([b, n, composicao, "", "",
                                "SONDA — fora do corpus, executada à parte"])
                elif n == SUPERCONJUNTO:
                    w.writerow([b, n, composicao, contagens.get((b, n), 0),
                                brutas.get((b, n), 0), "EXECUTADA"])
                else:
                    w.writerow([b, n, composicao, contagens.get((b, n), 0),
                                brutas.get((b, n), 0), "DERIVADA"])

    with (SAIDA / "ordem_triagem.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["ordem", "base", "ano", "expressoes", "titulo", "doi"])
        for r in unicos:
            _, exprs, _ = por_registro[r["registro"]]
            w.writerow([ordem[r["registro"]], r["base"], r["ano"],
                        " ".join(sorted(exprs)), r["titulo"], r["doi"]])

    print(f"\n{len(linhas)} registros processados, {len(unicos)} únicos.")
    print(f"{_mostra(SAIDA)}/registros.csv, io2_contagens.csv e ordem_triagem.csv "
          f"gravados.")
    sem_ancora = sum(1 for r in unicos if not (ANCORAS <= por_registro[r["registro"]][0]))
    if sem_ancora:
        pct = 100 * sem_ancora / len(unicos)
        print(f"\nAVISO: em {sem_ancora} registros ({pct:.1f}%) o casamento local não confirmou "
              "as duas âncoras. É divergência esperada — a base casou por Keywords Plus ou por "
              "lematização. Nenhum registro foi descartado. Se esse percentual for alto, o teste "
              "de fidelidade tende a reprovar.")
    print("\nAs contagens das expressões não executadas são DERIVADAS. Declará-las como tal "
          "no IO 2 e no relatório, "
          "e só aceitá-las após o teste de fidelidade (--fidelidade).")


# ------------------------------------------------------------------ fidelidade
def chave(reg):
    d = (reg["doi"] or "").strip().lower()
    return "doi:" + d if d else "ti:" + normaliza(reg["titulo"])[:120]


def fidelidade(expr, caminho):
    ident = _id_expressao(expr)
    if ident is None:
        print(f"Expressão {expr!r} não existe. Use EB1 a EB5."); sys.exit(1)
    if ident == SONDA:
        print(f"{SONDA} é a sonda de sensibilidade, não expressão de conferência: o conjunto "
              f"dela é superconjunto de {SUPERCONJUNTO} e não se deriva da exportação da de "
              f"cobertura. Use  --sensibilidade <base>.")
        sys.exit(1)
    arq = pathlib.Path(caminho)
    if not arq.exists():
        print(f"Arquivo não encontrado: {arq}"); sys.exit(1)

    direto = {chave(r) for r in le_arquivo(arq)}
    if not direto:
        print("Nenhum registro lido do arquivo de conferência."); sys.exit(1)

    facetas = carrega_facetas()
    _, validas = carrega_consultas()
    derivado = set()
    for r in identifica(coleta(validas)):
        if r["duplicata_de"]:
            continue
        fac = facetas_atingidas(r, facetas)
        if satisfaz(ident, fac):
            derivado.add(chave(r))

    so_direto = direto - derivado
    so_derivado = derivado - direto
    uniao = direto | derivado
    div = (len(so_direto) + len(so_derivado)) / len(uniao) if uniao else 0

    print(f"\nTESTE DE FIDELIDADE — {ident}")
    print(f"  execução direta na base : {len(direto)}")
    print(f"  conjunto derivado       : {len(derivado)}")
    print(f"  só na execução direta   : {len(so_direto)}")
    print(f"  só no conjunto derivado : {len(so_derivado)}")
    print(f"  divergência simétrica   : {div:.1%}  (limite: {LIMITE_DIVERGENCIA:.0%})")
    SAIDA.mkdir(parents=True, exist_ok=True)
    rel = SAIDA / f"fidelidade_{ident}.csv"
    with rel.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["chave", "situacao"])
        for k in sorted(so_direto):
            w.writerow([k, "só na execução direta"])
        for k in sorted(so_derivado):
            w.writerow([k, "só no conjunto derivado"])
    print(f"  divergências listadas em {_mostra(rel)}")
    if div > LIMITE_DIVERGENCIA:
        print("\n  REPROVADO. A derivação não pode ser aceita: volte às execuções separadas "
              "por expressão e registre emenda ao protocolo.")
        return 1
    print("\n  APROVADO para esta expressão. Repita para a outra expressão de conferência "
          "antes de aceitar as contagens derivadas.")
    return 0


# ------------------------------------------------------------------ sensibilidade
def _registros_da_expressao(base, ident, validas):
    """Chaves de deduplicação dos registros de uma expressão, numa base."""
    consultas = [c for c in validas
                 if c.get("base") == base and c.get("expressao") == ident]
    if not consultas:
        return None
    chaves, registros = set(), []
    for c in consultas:
        caminho = _caminho_do_arquivo(c)
        if not caminho.exists():
            raise SystemExit(f"consulta {c.get('id')}: arquivo ausente {c.get('arquivo')}")
        for r in le_arquivo(caminho):
            k = chave_dedup(r)
            if k not in chaves:
                chaves.add(k)
                registros.append(r)
    return registros


def sensibilidade(base=None):
    """Fração de EB5 que EB4 não recupera — a sonda de sensibilidade do protocolo.

    A perda é a diferença de conjuntos, chaveada por DOI ou título. O arquivo gerado
    é a amostra a classificar à mão: a decisão do protocolo olha a fração ELEGÍVEL
    entre os perdidos, não o tamanho da perda. Sem essa classificação, o número
    impresso é limite superior do custo em recall, não estimativa dele.
    """
    _, validas = carrega_consultas()
    existentes = sorted({c.get("base") for c in validas})
    if base:
        canonica = BASE_CANONICA.get(base.strip().lower(), base.strip())
        if canonica not in existentes:
            raise SystemExit(f"base {base!r} sem consulta registrada; registradas: "
                             f"{', '.join(existentes) or 'nenhuma'}")
        alvos = [canonica]
    else:
        alvos = existentes

    SAIDA.mkdir(parents=True, exist_ok=True)
    saida = 0
    for b in alvos:
        e4 = _registros_da_expressao(b, SUPERCONJUNTO, validas)
        e5 = _registros_da_expressao(b, SONDA, validas)
        if e4 is None or e5 is None:
            falta = SUPERCONJUNTO if e4 is None else SONDA
            print(f"{b}: sem {falta} registrada — a sonda exige {SUPERCONJUNTO} e {SONDA} "
                  f"registradas na mesma base. Pulada.")
            saida = 1
            continue
        chaves4 = {chave_dedup(r) for r in e4}
        perdidos = [r for r in e5 if chave_dedup(r) not in chaves4]
        total5 = len({chave_dedup(r) for r in e5})
        fracao_perda = len(perdidos) / total5 if total5 else 0.0

        print(f"\nSONDA DE SENSIBILIDADE — {b}")
        print(f"  {SONDA} recupera .......... {total5}")
        print(f"  {SUPERCONJUNTO} recupera ...... {len(chaves4)}")
        print(f"  só em {SONDA} (perda) .... {len(perdidos)}  "
              f"({fracao_perda:.1%} de {SONDA})")
        print("  Este é o TAMANHO da perda, não a fração que decide: o protocolo decide pela "
              "fração ELEGÍVEL da amostra, classificada à mão.")

        rel = SAIDA / f"sensibilidade_{b.lower()}.csv"
        passo = max(1, len(perdidos) // 50)
        ordenados = sorted(perdidos, key=lambda x: normaliza(x["titulo"]))
        # Preserva o que o pesquisador já classificou: a amostra é dele, não do script.
        anterior = {}
        if rel.exists():
            with rel.open(encoding="utf-8-sig", newline="") as fh:
                for linha in csv.DictReader(fh, delimiter=";"):
                    anterior[linha.get("chave", "")] = linha.get("elegivel", "") or ""
        amostra = {chave_dedup(r) for i, r in enumerate(ordenados) if i % passo == 0}
        with rel.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(["chave", "ano", "titulo", "doi", "amostra", "elegivel"])
            for i, r in enumerate(ordenados):
                k = chave_dedup(r)
                w.writerow([k, r["ano"], r["titulo"], r["doi"],
                            "sim" if k in amostra else "", anterior.get(k, "")])
        onde = _mostra(rel)

        baixo, alto = LIMITE_SENSIBILIDADE
        if not amostra:
            print(f"  amostra em {onde}: nenhuma perda a classificar.")
        else:
            respondidos = [anterior.get(k, "").strip() for k in amostra
                           if anterior.get(k, "").strip()]
            if len(respondidos) < len(amostra):
                print(f"  amostra em {onde}: {len(respondidos)} de {len(amostra)} "
                      f"classificados — a decisão exige a amostra inteira.")
            else:
                sim = sum(1 for v in respondidos if v.lower() in ("sim", "s", "1", "true"))
                frac_eleg = sim / len(amostra)
                print(f"  fração ELEGÍVEL na amostra: {sim}/{len(amostra)} = {frac_eleg:.1%}")
                if frac_eleg < baixo:
                    print(f"  {frac_eleg:.1%} < {baixo:.0%}: a restrição está justificada.")
                elif frac_eleg > alto:
                    print(f"  {frac_eleg:.1%} > {alto:.0%}: reconsiderar, possivelmente "
                          f"retornar a {SONDA} como busca definitiva.")
                else:
                    print(f"  {frac_eleg:.1%} na faixa {baixo:.0%}–{alto:.0%}: decisão de "
                          f"mérito do pesquisador, a registrar como emenda.")
        print("  A decisão se registra como emenda ao protocolo.")
    return saida


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registrar", nargs=3, metavar=("BASE", "EXPRESSAO", "ARQUIVO"),
                    help="registra uma execução e confere o retorno declarado contra o arquivo")
    ap.add_argument("--retorno", type=int, help="retorno que a base exibiu, para --registrar")
    ap.add_argument("--data-hora", help="data e hora da consulta, ISO 8601 (padrão: agora)")
    ap.add_argument("--justificar", default="",
                    help="motivo aceito para retorno declarado divergente do arquivo")
    ap.add_argument("--aderencia", action="store_true",
                    help="teste de aderência ao conjunto-semente, sobre as consultas")
    ap.add_argument("--derivar", action="store_true",
                    help="lê as consultas, deriva as expressões não executadas, as contagens "
                         "e a ordem de triagem")
    ap.add_argument("--fidelidade", nargs=2, metavar=("EXPRESSAO", "ARQUIVO"),
                    help="compara o conjunto derivado com a execução direta (ex.: EB2 arq.ris)")
    ap.add_argument("--sensibilidade", nargs="?", const="", metavar="BASE",
                    help="mede a perda de EB5 para EB4 e escreve a amostra a classificar; "
                         "decide pela fração elegível (sem BASE, todas as bases com EB4 e "
                         "EB5 registradas)")
    a = ap.parse_args()
    if a.registrar:
        return registrar(*a.registrar, a.retorno, a.data_hora, a.justificar)
    if a.aderencia:
        aderencia(); return 0
    if a.derivar:
        derivar(); return 0
    if a.fidelidade:
        return fidelidade(*a.fidelidade)
    if a.sensibilidade is not None:
        return sensibilidade(a.sensibilidade or None)
    ap.print_help(); return 1


if __name__ == "__main__":
    sys.exit(main())
