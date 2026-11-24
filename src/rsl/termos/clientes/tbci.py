"""Cliente do Tesauro Brasileiro de Ciência da Informação (IBICT), servidor TemaTres 3.5.2.

API REST documentada em https://vocabularyserver.com/tbci/br/services.php, sem chave de
acesso. O endereço é do cliente, não da coluna Caminho do protocolo.
"""

import json
import time
import urllib.parse

from .. import http
from ..planejamento import STATUS_NAO_LOCALIZADO, STATUS_AUTORIZADO, norm, termos_de_prova

ENDERECO = "https://vocabularyserver.com/tbci/br/services.php"
VERSAO = "TemaTres 3.5.2 — conferir data na sonda"
PAUSA = 1.0          # segundo entre requisições; serviço público de terceiro


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


ROTULOS = {"term", "string", "value", "nombre", "term_name", "label"}
IDS = {"id", "key", "term_id", "tema"}


def item_exato(achado, termo):
    """(rótulo, identificador) do item da busca cujo rótulo casa exatamente com o termo.

    O identificador é colhido do mesmo item que casou, e não da resposta inteira: a busca
    devolve vários conceitos (`organização do conhecimento` traz também `sistemas de
    organização do conhecimento`), e o primeiro identificador da resposta pode ser de outro.
    Item sem identificador próprio devolve (rótulo, None). Nenhum casamento: (None, None)."""
    itens = achado.get("result") if isinstance(achado, dict) else None
    itens = list(itens.values()) if isinstance(itens, dict) else \
        (itens if isinstance(itens, list) else [])
    for item in itens:
        if not isinstance(item, dict):
            continue
        for r in achata(item, ROTULOS):
            if norm(r) == norm(termo):
                ids = achata(item, IDS)
                return r, (ids[0] if ids else None)
    return None, None


def chamada(task, arg):
    url = f"{ENDERECO}?{urllib.parse.urlencode({'task': task, 'arg': arg, 'output': 'json'})}"
    return url, http.json_de(http.requisicao(url), url)


def valida(termo, instrumento):
    """Procura o termo, identifica o conceito e colhe USE/UP, TG, TE, TR e nota."""
    url, achado = chamada("search", termo)
    reg = {"url_consultada": url, "status_http": 200, "busca": achado}
    exato, cid = item_exato(achado, termo)
    if not exato:
        return (reg, STATUS_NAO_LOCALIZADO, {}, "sem correspondência exata de rótulo", url,
                VERSAO)

    dados = {}
    if cid:
        for rotulo, task in (("equivalentes_USE_UP", "fetchAlt"),
                             ("termos_genericos_TG", "fetchUp"),
                             ("termos_especificos_TE", "fetchDown"),
                             ("termos_relacionados_TR", "fetchRelated"),
                             ("nota_de_escopo", "fetchNotes")):
            time.sleep(PAUSA)
            u, p = chamada(task, cid)
            reg[task] = {"url": u, "status_http": 200, "payload": p}
            vals = achata(p, {"term", "string", "value", "nombre", "label", "note", "scopenote"})
            dados[rotulo] = "; ".join(dict.fromkeys(v for v in vals if norm(v) != norm(termo)))

    status = STATUS_AUTORIZADO if cid else "localizado, identificador não extraído"
    dados["rotulo_autorizado"] = exato
    dados["uri_conceito"] = f"{ENDERECO}?task=fetchTerm&arg={cid}" if cid else ""
    obs = "" if cid else "identificador do conceito não extraído do JSON: conferir o payload"
    return reg, status, dados, obs, url, VERSAO


def sonda(d, instrumento, emite):
    u, p = chamada("fetchVocabularyData", "")
    emite(f"  fetchVocabularyData -> HTTP 200  {u}")
    emite("  " + json.dumps(p, ensure_ascii=False)[:600])
    for t in termos_de_prova(d, instrumento):
        time.sleep(PAUSA)
        u, p = chamada("search", t)
        emite(f"\n  search '{t}' -> HTTP 200")
        emite("  " + json.dumps(p, ensure_ascii=False)[:600])
    emite("\n  >> Confira: a estrutura do JSON traz rótulo e identificador? Se os nomes das")
    emite("     chaves diferirem dos previstos, ajuste o conjunto passado a achata().")
