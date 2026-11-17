#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Derivação local das expressões não executadas (EB4, de cobertura, é a executada) — RS Banyan, Módulo 3, Etapa 2.

Emenda ao protocolo de 06/11/2026. Todas as quatro expressões começam por strings
1 + 2 e apenas acrescentam facetas: EB1, EB2 e EB3 são subconjuntos estritos de EB4, e a
união das quatro é exatamente EB4. Executa-se EB4, a de cobertura, uma vez por base,
exporta-se o resultado, e a pertinência de cada registro às demais é calculada aqui.

O que este script NÃO faz: não exclui registro algum, não decide inclusão e não
substitui o teste de fidelidade. As contagens que produz são DERIVADAS e devem ser
declaradas como tal no IO 2 e no relatório.

Entradas
  data/consultas.json      registro das execuções, escrito por --registrar
  data/strings.json        DERIVADO do protocolo: termos, strings e expressões
  data/criterios.json      DERIVADO do protocolo: recorte temporal
  data/sementes.json       DERIVADO do protocolo: conjunto-semente
  <arquivo> de cada consulta registrada, intacto, onde estiver

Nenhuma entrada é digitada à mão: o vocabulário e as expressões vêm do documento do
protocolo por src/protocolo.py --gerar, e o script recusa rodar com derivado defasado.

Saídas em data/saida/derivacao/
  registros.csv        um registro por linha, com as facetas e expressões atingidas,
                       a chave de ordenação de leitura e a marca de duplicata
  io2_contagens.csv    base x expressão, para alimentar o IO 2
  ordem_triagem.csv    a fila da 1ª filtragem já ordenada (Medida 4)
  fidelidade_EB<n>.csv as divergências do teste, item a item

Deduplicação: dentro da mesma base, registro com o mesmo DOI — ou, na falta dele, o
mesmo título normalizado — é marcado em `duplicata_de` com o identificador da primeira
ocorrência. Nada é apagado; as contagens do IO 2 usam os registros únicos e o número
bruto sai ao lado. É o que faz a exportação da ERIC em vários arquivos não contar duas
vezes o mesmo registro.

Uso
  python3 src/protocolo.py --gerar                    # antes de tudo, e após alterar o protocolo
  python3 src/derivar_expressoes.py --registrar wos EB4 data/execucoes/wos/e4.ris --retorno 18432
  python3 src/derivar_expressoes.py --derivar
  python3 src/derivar_expressoes.py --aderencia
  python3 src/derivar_expressoes.py --fidelidade EB2 data/execucoes/wos/e2_conferencia.ris
"""

import argparse
import csv
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
STRINGS_JSON = DATA / "strings.json"
CRITERIOS_JSON = DATA / "criterios.json"
SEMENTES_JSON = DATA / "sementes.json"
CONSULTAS_JSON = DATA / "consultas.json"
SAIDA = DATA / "saida" / "derivacao"

_STRINGS = protocolo.carrega(STRINGS_JSON)
_CRITERIOS = protocolo.carrega(CRITERIOS_JSON)
_FACETAS = protocolo.carrega(protocolo.ARQ["facetas"])
# A composição do protocolo vem em strings (STRn); a derivação casa facetas (FCTn).
EXPRESSOES = {e: [f"FCT{s[3:]}" for s in comps]
              for e, comps in _STRINGS["expressoes"].items()}
SUPERCONJUNTO = _STRINGS["executada"]
ANCORAS = {f["id"] for f in _FACETAS["facetas"] if f.get("ancora")}

# Recorte temporal do protocolo, aplicado como CONFERÊNCIA em todas as bases. Na
# Web of Science, na Scopus e na BRAPCI o filtro de ano vai na própria consulta;
# na ERIC, onde os operadores de ano zeram o retorno em consulta com grupos, ele
# é aplicado pelos filtros da página de resultados. Em nenhuma delas esta etapa
# deveria retirar registro: se retirar, há divergência entre o que a consulta ou
# o filtro declararam e o que a base devolveu, e isso se investiga.
# Registro sem ano legível NÃO é descartado: fica com ano = 0 e sai marcado,
# porque descartar por ausência de metadado seria corte cego.
ANO_MIN = int(_CRITERIOS["recorte"]["ano_min"])
# O protocolo diz "de 2017 em diante", sem teto: o limite superior é o ano corrente.
ANO_MAX = int(_CRITERIOS["recorte"]["ano_max"] or datetime.date.today().year)
LIMITE_DIVERGENCIA = 0.10     # 10% — acima disso o método é reprovado

STATUS_VALIDOS = ("valida", "divergente_justificada")
BASE_CANONICA = {"wos": "WoS", "scopus": "Scopus", "eric": "ERIC", "brapci": "BRAPCI"}


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
    """Facetas e padrões de casamento, da lista EXECUTADA em strings.json."""
    facetas = {}
    for f in _STRINGS["facetas"]:
        vistos, limpos = set(), []
        for t in f["termos"]:
            k = t.lower()
            if k not in vistos:
                vistos.add(k)
                limpos.append(t)
        facetas[f["faceta"]] = {"nome": "", "termos": limpos,
                                "padroes": [padrao(t) for t in limpos]}
    for f in _FACETAS["facetas"]:
        if f["id"] in facetas:
            facetas[f["id"]]["nome"] = f["nome"]
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


def expressoes_de(fac):
    return [n for n, exig in EXPRESSOES.items() if set(exig) <= fac]


def chave_ordem(reg, exprs):
    """Medida 4: pertinência às expressões ricas primeiro, depois recência."""
    riqueza = max((len(EXPRESSOES[e]) for e in exprs), default=0)
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


def carrega_consultas(exigir=True):
    if not CONSULTAS_JSON.exists():
        raise SystemExit("data/consultas.json não encontrado: registre cada execução com "
                         "--registrar antes de derivar")
    try:
        dado = json.loads(CONSULTAS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"data/consultas.json ilegível: {e}")
    validas = [c for c in dado.get("consultas", []) if c.get("status") in STATUS_VALIDOS]
    if exigir and not validas:
        raise SystemExit(
            "nenhuma consulta válida em data/consultas.json.\n"
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
    return ident if ident in EXPRESSOES else None


def registrar(base, expressao, arquivo, retorno, data_hora=None, justificar=""):
    """Registra uma execução e confere o retorno declarado contra o arquivo."""
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
        print(f"Expressão inválida: {expressao!r}. Use EB1 a EB4.")
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

    base = BASE_CANONICA.get(base.strip().lower(), base.strip())
    try:
        rel = str(caminho.resolve().relative_to(RAIZ))
    except ValueError:
        rel = str(caminho.resolve())

    _, validas = carrega_consultas(exigir=False)
    dado = json.loads(CONSULTAS_JSON.read_text(encoding="utf-8"))
    consultas = dado.setdefault("consultas", [])
    ident = f"{base}-{id_expr}-{pathlib.Path(arquivo).stem}"
    entrada = {
        "id": ident,
        "base": base,
        "expressao": id_expr,
        "data_hora": data_hora or datetime.datetime.now().astimezone().isoformat(
            timespec="seconds"),
        "retorno_declarado": int(retorno),
        "registros_lidos": lidos,
        "arquivo": rel,
        "status": status,
        "justificativa_divergencia": just,
    }
    for i, c in enumerate(consultas):
        if (c.get("base"), c.get("expressao"), c.get("arquivo")) == \
                (entrada["base"], entrada["expressao"], entrada["arquivo"]):
            consultas[i] = entrada
            break
    else:
        consultas.append(entrada)
    CONSULTAS_JSON.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")

    print(f"Consulta registrada em data/consultas.json:\n"
          f"  {ident}\n"
          f"  {entrada['base']} {entrada['expressao']} em {entrada['data_hora']}\n"
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

    As referências vêm do protocolo, por `src/protocolo.py --gerar`; a coluna
    `indexado` da planilha é o denominador e precisa ser preenchida à mão, base
    por base, buscando cada semente pelo título: ausência por falta de indexação
    não é falha da string.
    """
    if not SEMENTES_JSON.exists():
        raise SystemExit("data/sementes.json não encontrado: rode  python3 src/protocolo.py --gerar")
    dados = protocolo.carrega(SEMENTES_JSON)
    sementes = [e for e in dados["estudos"] if e.get("no_protocolo") is not False]
    orfas = [e for e in dados["estudos"] if e.get("no_protocolo") is False]
    if orfas:
        print(f"AVISO: {len(orfas)} semente(s) fora do protocolo em sementes.json, "
              f"ignorada(s) no teste.")
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
            for n in sorted(EXPRESSOES):
                w.writerow([b, n, "+".join(EXPRESSOES[n]),
                            contagens.get((b, n), 0), brutas.get((b, n), 0),
                            "EXECUTADA" if n == SUPERCONJUNTO else "DERIVADA"])

    with (SAIDA / "ordem_triagem.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["ordem", "base", "ano", "expressoes", "titulo", "doi"])
        for r in unicos:
            _, exprs, _ = por_registro[r["registro"]]
            w.writerow([ordem[r["registro"]], r["base"], r["ano"],
                        " ".join(sorted(exprs)), r["titulo"], r["doi"]])

    print(f"\n{len(linhas)} registros processados, {len(unicos)} únicos.")
    print(f"{SAIDA.relative_to(RAIZ)}/registros.csv, io2_contagens.csv e ordem_triagem.csv "
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
        print(f"Expressão {expr!r} não existe. Use EB1 a EB4."); sys.exit(1)
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
        if set(EXPRESSOES[ident]) <= fac:
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
    print(f"  divergências listadas em {rel.relative_to(RAIZ)}")
    if div > LIMITE_DIVERGENCIA:
        print("\n  REPROVADO. A derivação não pode ser aceita: volte às execuções separadas "
              "por expressão e registre emenda ao protocolo.")
        return 1
    print("\n  APROVADO para esta expressão. Repita para a outra expressão de conferência "
          "antes de aceitar as contagens derivadas.")
    return 0


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
    a = ap.parse_args()
    if a.registrar:
        return registrar(*a.registrar, a.retorno, a.data_hora, a.justificar)
    if a.aderencia:
        aderencia(); return 0
    if a.derivar:
        derivar(); return 0
    if a.fidelidade:
        return fidelidade(*a.fidelidade)
    ap.print_help(); return 1


if __name__ == "__main__":
    sys.exit(main())
