"""Cliente do serviço TemaTres (`services.php`), único para todo instrumento `Automático`.

O endereço não pertence ao cliente: é o `Caminho` do instrumento no protocolo, resolvido
para o idioma do termo (`leitura.endereco`). O cliente sabe só o protocolo de consulta do
TemaTres — `search`, `suggestDetails`, `fetchAlt`, `fetchUp`, `fetchDown`, `fetchRelated`,
`fetchNotes` e `fetchVocabularyData`, com `output=json` — e a pausa entre requisições.

Termo sem casamento exato consulta `suggestDetails` com o termo inteiro (termos do
instrumento, preferidos ou entradas de não preferido, em que alguma palavra começa pelo
termo; com identificador). Um único item é
candidato por similaridade, com o conceito dele; vários itens vão todos para a sugestão, sem
escolha — a escolha é do ReT; nenhum item, termo livre não localizado. O código não mede
proximidade nem trunca o termo.

Interface:
  PAUSA                               segundos entre requisições ao serviço
  versao(endereco)                    (texto da versão, payload) de fetchVocabularyData
  consultor(endereco)                 consulta(task, arg) → (url, payload), com a pausa
  sugestoes(resposta)                 itens de suggestDetails: (entrada, rótulo, id, forma)
  descreve(sugestoes)                 o texto de `sugestao_similar`
  valida(termo, endereco, versao[, consulta])  → (registro bruto, status, campos,
                                        observação, url, versão); falha de fonte é FonteExterna
  sonda(d, instrumento, idioma, endereco, emite[, consulta])  consultas de prova, sem gravar
"""

import json
import time
import urllib.parse

from . import http
from .planejamento import (SEM_SUGESTAO, STATUS_AUTORIZADO, STATUS_CANDIDATO,
                           STATUS_NAO_LOCALIZADO, norm, termos_de_prova)

PAUSA = 1.0          # segundo entre requisições; serviço público de terceiro
ROTULOS = {"term", "string", "value", "nombre", "term_name", "label"}
IDS = {"id", "key", "term_id", "tema"}
RELACOES = (("equivalentes_USE_UP", "fetchAlt"),
            ("termos_genericos_TG", "fetchUp"),
            ("termos_especificos_TE", "fetchDown"),
            ("termos_relacionados_TR", "fetchRelated"),
            ("nota_de_escopo", "fetchNotes"))
# Forma do termo no instrumento, pela resposta de `search` (medida na sonda de 2026-11-24):
# item com `no_term_string` = false é termo preferido em `string`; item com `no_term_string`
# texto é a entrada do termo não preferido `no_term_string`, que remete ao preferido
# `string` (o `term_id` é o do preferido). Item sem o campo não informa a forma.
NAO_PREFERIDO = "no_term_string"
FORMA_PREFERIDO, FORMA_NAO_PREFERIDO = "preferido", "não preferido"
OBS_FORMA = "o serviço não informou a forma do termo (preferido ou não preferido)"


def achata(obj, chaves):
    """Colhe, em qualquer profundidade, os valores cujas chaves batam com `chaves`."""
    saida = []

    def anda(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.lower() in chaves and isinstance(v, (str, int, float)) \
                        and not isinstance(v, bool):
                    saida.append(str(v))
                anda(v)
        elif isinstance(o, list):
            for v in o:
                anda(v)
    anda(obj)
    return saida


def itens(resposta):
    """Os itens de `result` de uma resposta TemaTres, como lista."""
    r = resposta.get("result") if isinstance(resposta, dict) else None
    r = list(r.values()) if isinstance(r, dict) else (r if isinstance(r, list) else [])
    return [i for i in r if isinstance(i, dict)]


def item_exato(achado, termo):
    """(rótulo, identificador, forma) do item da busca cujo rótulo casa exatamente com o
    termo, sem distinção de caixa e de espaços.

    Primeiro o rótulo preferido (`string`); só sem ele, o não preferido (`no_term_string`),
    caso em que o rótulo devolvido é o preferido a que ele remete. A forma é a que o item
    informa, ou "" quando o item não traz o campo. O identificador é colhido do mesmo item
    que casou, e não da resposta inteira: a busca devolve vários conceitos (`organização do
    conhecimento` traz também `sistemas de organização do conhecimento`), e o primeiro
    identificador da resposta pode ser de outro. Item sem identificador próprio devolve
    (rótulo, None, forma). Nenhum casamento: (None, None, None)."""
    lista_ = itens(achado)
    for item in lista_:
        if isinstance(item.get(NAO_PREFERIDO), str):
            continue                    # entrada de não preferido: o `string` é remissão
        for r in achata(item, ROTULOS):
            if norm(r) == norm(termo):
                ids = achata(item, IDS)
                forma_ = FORMA_PREFERIDO if NAO_PREFERIDO in item else ""
                return r, (ids[0] if ids else None), forma_
    for item in lista_:
        np_ = item.get(NAO_PREFERIDO)
        if isinstance(np_, str) and norm(np_) == norm(termo):
            ids = achata(item, IDS)
            return (str(item.get("string") or np_), (ids[0] if ids else None),
                    FORMA_NAO_PREFERIDO)
    return None, None, None


def proposta(achado, termo):
    """(status, rótulo, identificador, forma) proposto para o termo sobre a resposta da
    busca.

    Casamento exato de rótulo, de termo preferido ou não preferido, propõe descritor
    (decisão do pesquisador); sem casamento exato, termo livre não localizado. A proposta
    nunca toca a decisão do ReT."""
    rotulo, cid, forma_ = item_exato(achado, termo)
    if rotulo is None:
        return STATUS_NAO_LOCALIZADO, None, None, None
    return STATUS_AUTORIZADO, rotulo, cid, forma_


def chamada(endereco, task, arg):
    url = f"{endereco}?{urllib.parse.urlencode({'task': task, 'arg': arg, 'output': 'json'})}"
    return url, http.json_de(http.requisicao(url), url)


def consultor(endereco):
    """`consulta(task, arg)` → (url, payload) no endereço, com a pausa antes de cada
    requisição depois da primeira. O autoteste passa no lugar dela respostas em memória."""
    feitas = []

    def consulta(task, arg):
        if feitas:
            time.sleep(PAUSA)
        feitas.append(task)
        return chamada(endereco, task, arg)
    return consulta


def texto_versao(payload):
    """Título e `lastMod` declarados em `fetchVocabularyData`; o que a instância não
    declarar fica dito como não declarado."""
    titulo = next(iter(achata(payload, {"title"})), "")
    data = next(iter(achata(payload, {"lastmod"})), "")
    return (f"{titulo or 'título não declarado'} — lastMod "
            f"{data or 'não declarado'} (fetchVocabularyData)")


def versao(endereco):
    """(versão, registro bruto) de `fetchVocabularyData`."""
    url, p = chamada(endereco, "fetchVocabularyData", "")
    return texto_versao(p), {"url": url, "status_http": 200, "payload": p}


def sugestoes(resposta):
    """Os itens de `suggestDetails`, na ordem do serviço, como (entrada, rótulo, id, forma).

    Forma medida na sondagem de 2026-11-24 (ERIC, UNESCO, TBCI, Brased): itens como os de
    `search`. Item com `no_term_string` texto casou pela entrada não preferida, que remete ao
    preferido `string`; `false`, pelo preferido; sem o campo, a forma não é informada. Sem
    item, a resposta não traz `result`."""
    lista_ = itens(resposta)
    lista_.sort(key=lambda i: int(i["order"]) if str(i.get("order", "")).isdigit() else 0)
    saida = []
    for item in lista_:
        np_, rotulo = item.get(NAO_PREFERIDO), str(item.get("string") or "")
        ids = achata(item, IDS)
        if isinstance(np_, str) and np_.strip():
            saida.append((np_, rotulo or np_, ids[0] if ids else None, FORMA_NAO_PREFERIDO))
        elif rotulo:
            saida.append((rotulo, rotulo, ids[0] if ids else None,
                          FORMA_PREFERIDO if NAO_PREFERIDO in item else ""))
    return saida


def descreve(sugestoes_):
    """`sugestao_similar`: cada item como `entrada [id]`, ou `entrada → preferido [id]`
    quando casou pela entrada não preferida; `SEM_SUGESTAO` sem item."""
    if not sugestoes_:
        return SEM_SUGESTAO
    return "; ".join((e if e == r else f"{e} → {r}") + (f" [{cid}]" if cid else "")
                     for e, r, cid, _ in sugestoes_)


def valida(termo, endereco, versao_, consulta=None):
    """Procura o termo, identifica o conceito e colhe USE/UP, TG, TE, TR e nota.

    Sem casamento exato, consulta a similaridade (docstring do módulo). `sugestao_similar`
    só vem nos campos quando não houve casamento exato: a sugestão, ou `SEM_SUGESTAO`."""
    consulta = consulta or consultor(endereco)
    url, achado = consulta("search", termo)
    reg = {"url_consultada": url, "status_http": 200, "busca": achado}
    status, exato, cid, forma_ = proposta(achado, termo)
    alvo, dados, obs_ = termo, {}, []
    if exato is None:
        u, p = consulta("suggestDetails", termo)
        reg["suggestDetails"] = {"url": u, "status_http": 200, "payload": p}
        sugs = sugestoes(p)
        dados["sugestao_similar"] = descreve(sugs)
        sem = "sem correspondência exata de rótulo"
        if not sugs:
            return reg, status, dados, f"{sem}; o serviço não sugeriu termo", url, versao_
        if len(sugs) > 1:
            cant = next(iter(achata(p.get("resume") if isinstance(p, dict) else None,
                                    {"cant_result"})), "não declarada")
            return (reg, status, dados, f"{sem}; o serviço devolveu {len(sugs)} itens "
                                        f"(contagem declarada pelo serviço: {cant}), sem "
                                        f"escolha pelo cliente: a escolha é do ReT", url,
                    versao_)
        alvo, exato, cid, forma_ = sugs[0]
        status = STATUS_CANDIDATO
        obs_.append(f"conceito do candidato sugerido {alvo!r}, e não do termo")

    if cid:
        for rotulo, task in RELACOES:
            u, p = consulta(task, cid)
            reg[task] = {"url": u, "status_http": 200, "payload": p}
            vals = achata(p, {"term", "string", "value", "nombre", "label", "note", "scopenote"})
            dados[rotulo] = "; ".join(dict.fromkeys(v for v in vals if norm(v) != norm(alvo)))
    dados["rotulo_autorizado"] = exato
    dados["uri_conceito"] = f"{endereco}?task=fetchTerm&arg={cid}" if cid else ""
    dados["forma_no_instrumento"] = forma_
    if not forma_:
        obs_.append(OBS_FORMA)
    if not cid:
        obs_.append("identificador do conceito não extraído do JSON: conferir o payload")
    return reg, status, dados, "; ".join(obs_), url, versao_


def sonda(d, instrumento, idioma, endereco, emite, consulta=None):
    """Metadados do vocabulário, termos de prova no idioma e um termo inexistente: a
    resposta bruta, o casamento exato e as chaves de cada item, para conferir se a
    resposta distingue termo preferido de não preferido; e, para cada termo, a resposta de
    `suggestDetails`, com os itens que o serviço devolve."""
    consulta = consulta or consultor(endereco)
    u, p = consulta("fetchVocabularyData", "")
    emite(f"  fetchVocabularyData -> HTTP 200  {u}")
    emite(f"  versão: {texto_versao(p)}")
    emite("  " + json.dumps(p, ensure_ascii=False)[:600])
    for t in termos_de_prova(d, instrumento, idioma):
        u, p = consulta("search", t)
        status, rotulo, cid, forma_ = proposta(p, t)
        emite(f"\n  search '{t}' -> HTTP 200  {u}")
        emite(f"  proposta: {status}  rótulo: {rotulo!r}  identificador: {cid!r}  "
              f"forma: {forma_!r}")
        for item in itens(p)[:5]:
            emite("   item: " + json.dumps(item, ensure_ascii=False)[:300])
        emite("  " + json.dumps(p, ensure_ascii=False)[:600])
        u, p = consulta("suggestDetails", t)
        sugs = sugestoes(p)
        emite(f"  suggestDetails '{t}' -> HTTP 200  {u}")
        emite(f"  {len(sugs)} item(ns): {descreve(sugs)}")
        emite("  " + json.dumps(p, ensure_ascii=False)[:600])
    emite(f"\n  >> Confira: o termo inexistente não casa? Os itens trazem `{NAO_PREFERIDO}` "
          f"(false: preferido; texto: entrada de não preferido)? Os itens de `suggestDetails` "
          f"trazem identificador?")
