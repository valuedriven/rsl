"""Cliente do UNESCO Thesaurus: endpoint SPARQL, grafo nomeado do tesauro, POST.

Os rótulos de relação (TG, TE, TR) são colhidos nos idiomas que o protocolo declara para o
instrumento (coluna Idiomas da tabela de instrumentos).
"""

import json
import time

from ... import gramatica as G
from .. import http
from ..planejamento import (STATUS_AUTORIZADO, STATUS_EQUIVALENTE, STATUS_NAO_LOCALIZADO,
                            termos_de_prova)
from ...erros import FonteExterna

ENDERECO = "https://vocabularies.unesco.org/sparql"
GRAFO = "http://vocabularies.unesco.org/thesaurus/"
VERSAO = "UNESCO Thesaurus — grafo " + GRAFO
PAUSA = 1.0          # segundo entre requisições; serviço público de terceiro

PREFIXOS = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX isothes: <http://purl.org/iso25964/skos-thes#>
"""


def sparql(consulta, formato="application/sparql-results+json"):
    """POST, conforme a recomendação do próprio endpoint para consultas longas. Resposta
    sem `results.bindings` está fora do formato esperado: FonteExterna."""
    dados = (PREFIXOS + consulta).encode("utf-8")
    cab = {"Content-Type": "application/sparql-query", "Accept": formato}
    res = http.json_de(http.requisicao(ENDERECO, dados=dados, cabecalhos=cab), ENDERECO)
    if not (isinstance(res, dict) and isinstance(res.get("results"), dict)
            and isinstance(res["results"].get("bindings"), list)):
        raise FonteExterna(f"corpo fora do formato esperado (SPARQL JSON) em {ENDERECO}")
    return res


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def valida(termo, instrumento):
    q = f'''SELECT ?c ?tipo ?rotulo ?lang WHERE {{
  GRAPH <{GRAFO}> {{
    {{ ?c skos:prefLabel ?l . BIND("prefLabel" AS ?tipo) }}
    UNION
    {{ ?c skos:altLabel ?l . BIND("altLabel" AS ?tipo) }}
    FILTER(LCASE(STR(?l)) = "{esc(termo.lower())}")
    ?c skos:prefLabel ?rotulo .
    BIND(LANG(?rotulo) AS ?lang)
  }}
}} LIMIT 60'''
    res = sparql(q)
    reg = {"consulta": q, "status_http": 200, "resposta": res}
    linhas = res["results"]["bindings"]
    if not linhas:
        return reg, STATUS_NAO_LOCALIZADO, {}, "", ENDERECO, VERSAO

    uri = linhas[0]["c"]["value"]
    tipos = {b["tipo"]["value"] for b in linhas}
    status = STATUS_AUTORIZADO if "prefLabel" in tipos else STATUS_EQUIVALENTE
    autorizados = {b["rotulo"]["value"]: b.get("lang", {}).get("value", "")
                   for b in linhas if "rotulo" in b}

    idiomas = ",".join(f'"{esc(i)}"' for i in instrumento["idiomas"])
    q2 = f'''SELECT ?rel ?alvo ?rot WHERE {{
  GRAPH <{GRAFO}> {{
    VALUES ?rel {{ skos:broader skos:narrower skos:related skos:altLabel skos:scopeNote }}
    <{uri}> ?rel ?alvo .
    OPTIONAL {{ ?alvo skos:prefLabel ?rot . FILTER(LANG(?rot) IN ({idiomas})) }}
  }}
}} LIMIT 300'''
    time.sleep(PAUSA)
    rel = sparql(q2)
    reg["relacoes"] = {"consulta": q2, "status_http": 200, "resposta": rel}

    balde = {"broader": [], "narrower": [], "related": [], "altLabel": [], "scopeNote": []}
    for b in rel["results"]["bindings"]:
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
    return reg, status, dados, "", ENDERECO, VERSAO


def sonda(d, instrumento, emite):
    res = sparql("SELECT (COUNT(*) AS ?n) WHERE { GRAPH <%s> { ?s ?p ?o } }" % GRAFO)
    emite("  contagem de triplas -> HTTP 200")
    emite("  " + json.dumps(res, ensure_ascii=False)[:400])
    time.sleep(PAUSA)
    res = sparql("SELECT DISTINCT (LANG(?l) AS ?idioma) WHERE { GRAPH <%s> { "
                 "?c skos:prefLabel ?l } }" % GRAFO)
    emite("\n  idiomas dos prefLabel -> HTTP 200")
    emite("  " + json.dumps(res, ensure_ascii=False)[:800])
    emite(f"\n  >> Confira contra a coluna {G.T_INSTRUMENTOS.colunas[4]} de "
          f"`{instrumento['sigla']}` na {G.T_INSTRUMENTOS.rotulo} do")
    emite("     protocolo; divergência se registra no histórico e se corrige no protocolo.")
    for t in termos_de_prova(d, instrumento, inexistente=False):
        time.sleep(PAUSA)
        reg, status, dados, obs, _, _ = valida(t, instrumento)
        emite(f"\n  '{t}' -> {status}  {dados.get('uri_conceito', '')}")
        emite("   TG: " + dados.get("termos_genericos_TG", "")[:200])
        emite("   TR: " + dados.get("termos_relacionados_TR", "")[:200])
