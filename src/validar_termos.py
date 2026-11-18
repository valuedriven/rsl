#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validação terminológica assistida — RS Banyan, Módulo 3, Etapa 1, 2º passo.

Confronta os termos livres das quatro facetas com DOIS instrumentos legíveis por máquina:

  TBCI    Tesauro Brasileiro de Ciência da Informação (IBICT), servidor TemaTres 3.5.2
          API REST documentada em https://vocabularyserver.com/tbci/br/services.php
          sem chave de acesso. Termos em PORTUGUÊS.

  UNESCO  UNESCO Thesaurus, endpoint SPARQL https://vocabularies.unesco.org/sparql
          grafo nomeado <http://vocabularies.unesco.org/thesaurus/>, GET ou POST.
          Idiomas a confirmar pela sondagem (tarefa `idiomas`).

Estes dois são os ÚNICOS instrumentos de consulta sistemática do protocolo, e valem
para as quatro facetas. Os demais obras designadas — ERIC Thesaurus, Brased/INEP,
ACM CCS, LISTA, W3C, IEEE LOM — são REFERÊNCIA DOCUMENTAL pela regra única de
validação terminológica: não são percorridas termo a termo e não figuram como
instrumento de linha alguma da planilha. A faceta de fatores situacionais é
declarada de TERMO LIVRE por decisão de protocolo, e as suas linhas saem
pré-classificadas, com a decisão como procedência.

FRONTEIRA DE USO (protocolo): este script RECUPERA e REGISTRA. Não decide.
  - nenhum termo é excluído, reescrito ou incorporado automaticamente;
  - termo não localizado NÃO é erro: é termo livre, e assim é classificado;
  - TR e TE revelados pela consulta entram como CANDIDATOS, nunca nas strings;
  - a coluna `decisao_ReT` sai em branco: a decisão é do pesquisador, com o VT.

O REGISTRO é a própria planilha `data/validacao_termologica.csv`.
Não há JSON intermediário: a planilha guarda o estatuto de cada termo e instrumento,
e `--validar` e `--importar` a regravam. Toda resposta bruta é gravada em
`data/evidencia/<instrumento>/<arquivo>.json`. Linha sem evidência correspondente é
linha inválida — foi esse o defeito que originou a ressalva de procedência do protocolo.

Os termos NÃO são digitados aqui: vêm das tabelas do controle terminológico do
documento do protocolo, lidas por `src/protocolo.py`. Termo retirado do protocolo
permanece na planilha como linha fora do protocolo, preservada e reportada.

USO
  python3 src/validar_termos.py --sonda             # obrigatório antes de tudo
  python3 src/validar_termos.py --exportar          # reconstrói a planilha, sem rede
  python3 src/validar_termos.py --validar tbci      # executa a validação no TBCI
  python3 src/validar_termos.py --validar unesco
  python3 src/validar_termos.py --validar ambos --faceta 1
  python3 src/validar_termos.py --importar          # reconcilia a planilha com o protocolo

Requer apenas a biblioteca padrão do Python 3.9+.
"""

import argparse
import csv
import datetime
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import protocolo                                                    # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
EVID = DATA / "evidencia"
CSV_SAIDA = DATA / "validacao_termologica.csv"

TBCI_SERV = "https://vocabularyserver.com/tbci/br/services.php"
UNESCO_SPARQL = "https://vocabularies.unesco.org/sparql"
UNESCO_GRAFO = "http://vocabularies.unesco.org/thesaurus/"

PAUSA = 1.0          # segundo entre requisições; serviço público de terceiro
TIMEOUT = 45
UA = "validacao-terminologica-RSL/1.0 (pesquisa academica; uso nao comercial)"

COLUNAS = ["faceta", "faceta_nome", "ancora", "idioma", "termo"] + \
          list(protocolo.CAMPOS_VALIDACAO)
CAMPOS_DECISAO = ("decisao_ReT", "justificativa_ReT", "data_decisao")

STATUS_NAO_LOCALIZADO = "termo livre (não localizado no instrumento)"


# --------------------------------------------------------------------- utilidades
def agora():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def _chave_linha(faceta, idioma, termo, instrumento):
    return (str(faceta), idioma, protocolo.normaliza(termo), instrumento)


def _planilha_existente():
    """Linhas já registradas, por faceta, idioma, termo normalizado e instrumento."""
    if not CSV_SAIDA.exists():
        return {}
    with CSV_SAIDA.open(encoding="utf-8-sig", newline="") as fh:
        return {_chave_linha(r.get("faceta", ""), r.get("idioma", ""), r.get("termo", ""),
                             r.get("instrumento", "")): r
                for r in csv.DictReader(fh, delimiter=";")}


def grava_evidencia(instrumento, chave, payload):
    d = EVID / instrumento
    d.mkdir(parents=True, exist_ok=True)
    nome = hashlib.sha1(chave.encode("utf-8")).hexdigest()[:16] + ".json"
    caminho = d / nome
    caminho.write_text(
        json.dumps({"chave": chave, "recuperado_em": agora(), "payload": payload},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")
    return str(caminho.relative_to(DATA))


def http(url, dados=None, cabecalhos=None):
    """Uma requisição, sem concorrência, com uma única repetição em erro de rede."""
    req = urllib.request.Request(url, data=dados, headers={"User-Agent": UA,
                                                           **(cabecalhos or {})})
    for tentativa in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")
        except Exception as e:                       # rede indisponível, DNS, TLS
            if tentativa == 2:
                return 0, f"ERRO DE REDE: {e!r}"
            time.sleep(3)


def achata(obj, chaves):
    """Colhe, em qualquer profundidade, os valores cujas chaves batam com `chaves`.
    Tolerante de propósito: a forma exata do JSON do TemaTres não foi confirmada."""
    saida = []
    def anda(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.lower() in chaves and isinstance(v, (str, int, float)):
                    saida.append(str(v))
                anda(v)
        elif isinstance(o, list):
            for v in o:
                anda(v)
    anda(obj)
    return saida


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


# --------------------------------------------------------------------------- TBCI
def tbci_chamada(task, arg):
    url = f"{TBCI_SERV}?{urllib.parse.urlencode({'task': task, 'arg': arg, 'output': 'json'})}"
    cod, corpo = http(url)
    try:
        return url, cod, json.loads(corpo)
    except Exception:
        return url, cod, {"_bruto": corpo[:20000]}


def tbci_valida(termo):
    """Procura o termo, identifica o conceito e colhe USE/UP, TG, TE, TR e nota."""
    url, cod, achado = tbci_chamada("search", termo)
    reg = {"url_consultada": url, "status_http": cod, "busca": achado}
    if cod != 200:
        return reg, None, {}, f"CONSULTA FALHOU (HTTP/rede: {cod}) — repetir"

    rotulos = achata(achado, {"term", "string", "value", "nombre", "term_name", "label"})
    ids = achata(achado, {"id", "key", "term_id", "tema"})
    exato = [r for r in rotulos if norm(r) == norm(termo)]
    if not exato:
        return reg, STATUS_NAO_LOCALIZADO, {}, "sem correspondência exata de rótulo"

    cid = ids[0] if ids else None
    dados = {}
    if cid:
        for rotulo, task in (("equivalentes_USE_UP", "fetchAlt"),
                             ("termos_genericos_TG", "fetchUp"),
                             ("termos_especificos_TE", "fetchDown"),
                             ("termos_relacionados_TR", "fetchRelated"),
                             ("nota_de_escopo", "fetchNotes")):
            time.sleep(PAUSA)
            u, c, p = tbci_chamada(task, cid)
            reg[task] = {"url": u, "status_http": c, "payload": p}
            vals = achata(p, {"term", "string", "value", "nombre", "label", "note", "scopenote"})
            dados[rotulo] = "; ".join(dict.fromkeys(v for v in vals if norm(v) != norm(termo)))

    status = ("descritor autorizado (a conferir pelo ReT)" if cid
              else "localizado, identificador não extraído")
    dados["rotulo_autorizado"] = exato[0]
    dados["uri_conceito"] = f"{TBCI_SERV}?task=fetchTerm&arg={cid}" if cid else ""
    obs = "" if cid else "identificador do conceito não extraído do JSON: conferir o payload"
    return reg, status, dados, obs


def tbci_versao():
    url, cod, p = tbci_chamada("fetchVocabularyData", "")
    return url, cod, p


# ------------------------------------------------------------------------- UNESCO
PREFIXOS = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX isothes: <http://purl.org/iso25964/skos-thes#>
"""


def sparql(consulta, formato="application/sparql-results+json"):
    """POST, conforme a recomendação do próprio endpoint para consultas longas."""
    dados = (PREFIXOS + consulta).encode("utf-8")
    cab = {"Content-Type": "application/sparql-query", "Accept": formato}
    cod, corpo = http(UNESCO_SPARQL, dados=dados, cabecalhos=cab)
    try:
        return cod, json.loads(corpo)
    except Exception:
        return cod, {"_bruto": corpo[:20000]}


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def unesco_valida(termo):
    q = f'''SELECT ?c ?tipo ?rotulo ?lang WHERE {{
  GRAPH <{UNESCO_GRAFO}> {{
    {{ ?c skos:prefLabel ?l . BIND("prefLabel" AS ?tipo) }}
    UNION
    {{ ?c skos:altLabel ?l . BIND("altLabel" AS ?tipo) }}
    FILTER(LCASE(STR(?l)) = "{esc(termo.lower())}")
    ?c skos:prefLabel ?rotulo .
    BIND(LANG(?rotulo) AS ?lang)
  }}
}} LIMIT 60'''
    cod, res = sparql(q)
    reg = {"consulta": q, "status_http": cod, "resposta": res}
    linhas = (res.get("results", {}) or {}).get("bindings", []) if isinstance(res, dict) else []
    if cod != 200:
        return reg, None, {}, f"CONSULTA FALHOU (HTTP/rede: {cod}) — repetir"
    if not linhas:
        return reg, STATUS_NAO_LOCALIZADO, {}, ""

    uri = linhas[0]["c"]["value"]
    tipos = {b["tipo"]["value"] for b in linhas}
    status = ("descritor autorizado (a conferir pelo ReT)" if "prefLabel" in tipos
              else "termo equivalente USE/UP (a conferir pelo ReT)")
    autorizados = {b["rotulo"]["value"]: b.get("lang", {}).get("value", "")
                   for b in linhas if "rotulo" in b}

    q2 = f'''SELECT ?rel ?alvo ?rot WHERE {{
  GRAPH <{UNESCO_GRAFO}> {{
    VALUES ?rel {{ skos:broader skos:narrower skos:related skos:altLabel skos:scopeNote }}
    <{uri}> ?rel ?alvo .
    OPTIONAL {{ ?alvo skos:prefLabel ?rot . FILTER(LANG(?rot) IN ("en","es","fr")) }}
  }}
}} LIMIT 300'''
    time.sleep(PAUSA)
    cod2, rel = sparql(q2)
    reg["relacoes"] = {"consulta": q2, "status_http": cod2, "resposta": rel}

    balde = {"broader": [], "narrower": [], "related": [], "altLabel": [], "scopeNote": []}
    for b in (rel.get("results", {}) or {}).get("bindings", []) if isinstance(rel, dict) else []:
        nome = b["rel"]["value"].rsplit("#", 1)[-1]
        valor = b.get("rot", {}).get("value") or b.get("alvo", {}).get("value", "")
        if nome in balde and valor:
            balde[nome].append(valor)

    dados = {
        "rotulo_autorizado": "; ".join(f"{k} [{v}]" for k, v in autorizados.items()),
        "uri_conceito": uri,
        "equivalentes_USE_UP": "; ".join(dict.fromkeys(balde["altLabel"])),
        "termos_genericos_TG": "; ".join(dict.fromkeys(balde["broader"])),
        "termos_especificos_TE": "; ".join(dict.fromkeys(balde["narrower"])),
        "termos_relacionados_TR": "; ".join(dict.fromkeys(balde["related"])),
        "nota_de_escopo": "; ".join(dict.fromkeys(balde["scopeNote"])),
    }
    return reg, status, dados, ""


# -------------------------------------------------------------------------- sonda
def sonda():
    print("SONDAGEM — nada é gravado. Confira cada resposta antes de validar.\n")

    print("== TBCI (TemaTres) ==")
    u, c, p = tbci_versao()
    print(f"  fetchVocabularyData -> HTTP {c}  {u}")
    print("  " + json.dumps(p, ensure_ascii=False)[:600])
    for t in ("ontologia", "representação do conhecimento", "palavra-que-nao-existe-xyz"):
        time.sleep(PAUSA)
        u, c, p = tbci_chamada("search", t)
        print(f"\n  search '{t}' -> HTTP {c}")
        print("  " + json.dumps(p, ensure_ascii=False)[:600])
    print("\n  >> Confira: a estrutura do JSON traz rótulo e identificador? Se os nomes das")
    print("     chaves diferirem dos previstos, ajuste o conjunto passado a achata().")

    print("\n== UNESCO (SPARQL) ==")
    cod, res = sparql("SELECT (COUNT(*) AS ?n) WHERE { GRAPH <%s> { ?s ?p ?o } }" % UNESCO_GRAFO)
    print(f"  contagem de triplas -> HTTP {cod}")
    print("  " + json.dumps(res, ensure_ascii=False)[:400])
    time.sleep(PAUSA)
    cod, res = sparql("SELECT DISTINCT (LANG(?l) AS ?idioma) WHERE { GRAPH <%s> { "
                      "?c skos:prefLabel ?l } }" % UNESCO_GRAFO)
    print(f"\n  idiomas dos prefLabel -> HTTP {cod}")
    print("  " + json.dumps(res, ensure_ascii=False)[:800])
    print("\n  >> Decisivo: se o português NÃO constar, os termos em pt não são consultáveis")
    print("     neste instrumento e permanecem termos livres — registre essa constatação.")
    for t in ("teaching methods", "educational technology"):
        time.sleep(PAUSA)
        reg, status, dados, obs = unesco_valida(t)
        rotulo = status if status else "CONSULTA FALHOU — " + obs
        print(f"\n  '{t}' -> {rotulo}  {dados.get('uri_conceito','')}")
        print("   TG:", dados.get("termos_genericos_TG", "")[:200])
        print("   TR:", dados.get("termos_relacionados_TR", "")[:200])


# ------------------------------------------------------------------- leitura/escrita
def carrega():
    """Reconstrói o registro a partir do protocolo e da planilha existente.

    A planilha é o registro: não há JSON intermediário. Termo novo nasce com o estatuto
    inicial que o protocolo declara; linha já registrada é preservada campo a campo,
    inclusive decisão do ReT e evidência.
    """
    d = protocolo.analisa()
    existente = _planilha_existente()
    dados = {"facetas": []}
    for f in d["tabelas"]:
        est = {}
        for idioma in protocolo.IDIOMAS:
            bloco = {}
            for termo in f["termos"][idioma]:
                validacoes = []
                for inst in protocolo.INSTRUMENTO_POR_IDIOMA[idioma]:
                    r = existente.get(_chave_linha(f["id"], idioma, termo, inst))
                    v = {c: ((r.get(c) or "").strip() if r else "")
                         for c in protocolo.CAMPOS_VALIDACAO}
                    v["instrumento"] = inst
                    if r is None:
                        if f["livre"]:
                            v["status_proposto"] = protocolo.STATUS_LIVRE_DECISAO
                            v["observacao_tecnica"] = "não consultado: decisão de protocolo"
                            v["justificativa_ReT"] = protocolo.JUSTIFICATIVA_LIVRE
                        else:
                            v["observacao_tecnica"] = "aguardando consulta"
                    validacoes.append(v)
                bloco[protocolo.normaliza(termo)] = {"termo": termo,
                                                     "validacoes": validacoes}
            est[idioma] = bloco
        dados["facetas"].append({"id": f["id"], "estatuto": est})
    return dados


def linhas_de(dados):
    """Uma linha por termo e instrumento, ligada ao bloco de estatuto que a origina.

    Os termos vêm do protocolo — a lista que se valida é a dele. O estatuto vem da
    planilha; termo do protocolo sem bloco no estado interno é defeito de construção."""
    d = protocolo.analisa()
    info = {f["id"]: f for f in d["facetas"]}
    est = {f["id"]: f.get("estatuto", {}) for f in dados.get("facetas", [])}
    for f in d["tabelas"]:
        meta = info.get(f["id"], {})
        for idioma in protocolo.IDIOMAS:
            for termo in f["termos"][idioma]:
                e = est.get(f["id"], {}).get(idioma, {}).get(protocolo.normaliza(termo))
                if e is None:
                    raise SystemExit(
                        f"estado interno sem bloco para {termo!r} da faceta {f['id']}; "
                        f"rode  python3 src/validar_termos.py --exportar")
                for v in e.get("validacoes", []):
                    yield {"faceta": f["id"], "faceta_nome": meta.get("nome", ""),
                           "ancora": "sim" if meta.get("ancora") else "não",
                           "idioma": idioma, "termo": termo, "_v": v}


def _linha_csv(ln):
    v = ln["_v"]
    row = {"faceta": ln["faceta"], "faceta_nome": ln["faceta_nome"],
           "ancora": ln["ancora"], "idioma": ln["idioma"], "termo": ln["termo"]}
    for c in protocolo.CAMPOS_VALIDACAO:
        row[c] = v.get(c, "")
    return row


def grava_planilha(dados):
    """Grava o registro na planilha, preservando as linhas fora do protocolo."""
    CSV_SAIDA.parent.mkdir(parents=True, exist_ok=True)
    linhas = [_linha_csv(ln) for ln in linhas_de(dados)]
    chaves = {_chave_linha(l["faceta"], l["idioma"], l["termo"], l["instrumento"])
              for l in linhas}
    orfaos = [r for k, r in _planilha_existente().items() if k not in chaves]
    with CSV_SAIDA.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUNAS, delimiter=";")
        w.writeheader()
        w.writerows(linhas)
        for r in orfaos:
            w.writerow({c: r.get(c, "") for c in COLUNAS})
    livres = sum(1 for l in linhas
                 if l["status_proposto"] == protocolo.STATUS_LIVRE_DECISAO)
    a_validar = sum(1 for l in linhas if not l["status_proposto"])
    print(f"{CSV_SAIDA.relative_to(RAIZ)}: {len(linhas)} linhas — {a_validar} a validar, "
          f"{livres} já classificadas como termo livre por decisão de protocolo.")
    if orfaos:
        print(f"  {len(orfaos)} linha(s) fora do protocolo preservada(s) na planilha — "
              f"decidir: manter com registro ou retirar à mão.")


def exporta_csv(dados=None):
    grava_planilha(carrega() if dados is None else dados)
    return 0


def importar():
    """Reconcilia a planilha com o protocolo, preservando decisões e linhas órfãs."""
    if not CSV_SAIDA.exists():
        print(f"{CSV_SAIDA.name} não existe. Rode --exportar antes.")
        return 1
    dados = carrega()
    idx = {_chave_linha(ln["faceta"], ln["idioma"], ln["termo"],
                        ln["_v"].get("instrumento")): ln["_v"]
           for ln in linhas_de(dados)}
    with CSV_SAIDA.open(encoding="utf-8-sig", newline="") as fh:
        linhas = list(csv.DictReader(fh, delimiter=";"))
    casadas, sem_casa, com_decisao = 0, [], 0
    for r in linhas:
        k = _chave_linha(r.get("faceta", ""), r.get("idioma", ""), r.get("termo", ""),
                         r.get("instrumento", ""))
        v = idx.get(k)
        if v is None:
            sem_casa.append(k)
            continue
        casadas += 1
        for c in CAMPOS_DECISAO:
            valor = (r.get(c) or "").strip()
            if valor:
                v[c] = valor
                if c == "decisao_ReT":
                    com_decisao += 1
    grava_planilha(dados)
    print(f"{casadas} linha(s) casada(s), {com_decisao} decisão(ões) preservada(s), "
          f"{len(sem_casa)} fora do protocolo (preservadas).")
    import collections
    duplas = [k for k, n in collections.Counter(
        (r.get("faceta"), r.get("idioma"), protocolo.normaliza(r.get("termo")))
        for r in linhas).items() if n > 1]
    if duplas:
        print(f"AVISO: {len(duplas)} termo(s) aparecem mais de uma vez na planilha; a última "
              "linha lida prevalece.")
    for k in sem_casa[:10]:
        print(f"  fora do protocolo: {k}")
    return 0 if not sem_casa else 1


# ------------------------------------------------------------------- execução
def instrumentos_do(idioma):
    return list(protocolo.INSTRUMENTO_POR_IDIOMA[idioma])


def validar(quais, faceta=None):
    dados = carrega()
    feitos = 0
    falhas = 0
    for ln in linhas_de(dados):
        v = ln["_v"]
        if v.get("status_proposto"):
            continue
        if faceta and str(ln["faceta"]) != str(faceta):
            continue
        inst = v.get("instrumento")
        if inst not in quais:
            continue

        termo = ln["termo"]
        if inst == "TBCI":
            reg, status, dados_inst, obs = tbci_valida(termo)
            v["url_consultada"] = reg.get("url_consultada", "")
            v["versao_instrumento"] = "TemaTres 3.5.2 — conferir data na sonda"
        else:
            reg, status, dados_inst, obs = unesco_valida(termo)
            v["url_consultada"] = UNESCO_SPARQL
            v["versao_instrumento"] = "UNESCO Thesaurus — grafo " + UNESCO_GRAFO

        if status is None:                       # serviço fora do ar ou recusando
            v["observacao_tecnica"] = obs
            v["arquivo_evidencia"] = grava_evidencia(inst.lower(), f"{inst}|{termo}|falha", reg)
            falhas += 1
            grava_planilha(dados)
            print(f"[   ] {inst:<7} {termo[:48]:<50} {obs}")
            if falhas >= 5:
                print("\n5 falhas consecutivas: execução interrompida para não insistir "
                      "contra um serviço indisponível. Nenhum termo foi classificado por "
                      "falta de resposta. Rode --sonda e tente mais tarde.")
                return
            time.sleep(PAUSA * 3)
            continue
        falhas = 0
        v["consultado_em"] = agora()
        v["status_proposto"] = status
        v["observacao_tecnica"] = obs
        for k in ("rotulo_autorizado", "uri_conceito", "equivalentes_USE_UP",
                  "termos_genericos_TG", "termos_especificos_TE",
                  "termos_relacionados_TR", "nota_de_escopo"):
            v[k] = dados_inst.get(k, "")
        v["arquivo_evidencia"] = grava_evidencia(inst.lower(), f"{inst}|{termo}", reg)

        feitos += 1
        print(f"[{feitos:>3}] {inst:<7} {termo[:48]:<50} {status}")
        time.sleep(PAUSA)

        if feitos % 20 == 0:
            grava_planilha(dados)

    grava_planilha(dados)
    print(f"\n{feitos} termos consultados. Evidência bruta em {EVID.relative_to(RAIZ)}/.")
    print("As colunas decisao_ReT, justificativa_ReT e data_decisao ficam em branco: "
          "a classificação final e a incorporação de TR/TE são do pesquisador, com o VT.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sonda", action="store_true",
                    help="testa os dois serviços e imprime as respostas; não grava nada")
    ap.add_argument("--exportar", action="store_true",
                    help="reconstrói a planilha a partir do protocolo, sem rede")
    ap.add_argument("--importar", action="store_true",
                    help="reconcilia a planilha com o protocolo, preservando as decisões")
    ap.add_argument("--validar", choices=["tbci", "unesco", "ambos"],
                    help="executa a validação no instrumento indicado")
    ap.add_argument("--faceta", type=int, help="restringe a uma faceta")
    a = ap.parse_args()

    if a.sonda:
        sonda()
    elif a.exportar:
        return exporta_csv()
    elif a.importar:
        return importar()
    elif a.validar:
        quais = {"tbci": ["TBCI"], "unesco": ["UNESCO"],
                 "ambos": ["TBCI", "UNESCO"]}[a.validar]
        validar(quais, a.faceta)
    else:
        ap.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
