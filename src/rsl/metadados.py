"""Resumo e palavras-chave das sementes por fonte externa, consultada por DOI: a OpenAlex e,
como complemento só do resumo, o Crossref.

`sementes metadados` consulta a OpenAlex; `sementes metadados --fonte crossref` consulta o
Crossref só para as sementes ainda sem resumo em fonte nenhuma. Cada resposta 200 se grava
bruta em `[dados] evidencia`/<fonte>/<DOI normalizado>.json; o 404 deixa o marcador
`<DOI normalizado>.404`, com a data e hora, para que "sem registro" não se confunda com "não
consultada" nem com "consulta interrompida". O nome vem do DOI, não do `id`: retirar ou
renumerar semente não exige renomear evidência. Por padrão, só se consulta o DOI sem
resultado registrado na fonte; `--todas` refaz todas.

Acesso (AGENTS.md §9): sem e-mail nem identificação pessoal (agente de usuário genérico);
uma consulta por vez, com pausa; qualquer resposta que não 200 ou 404, corpo fora de JSON ou
erro de rede interrompe as consultas restantes, sem nova tentativa e sem outra rota. O
Crossref não é acionado automaticamente depois de erro da OpenAlex: é execução à parte,
pedida, e só para as sementes que a OpenAlex deixou sem resumo (404 ou 200 sem resumo).

As palavras-chave da OpenAlex são atribuídas por ela: não são as do autor nem as da base. O
Crossref só traz resumo quando a editora o deposita, e não traz palavras-chave. A semente sem
resumo em fonte nenhuma fica para o pesquisador, que o preenche no Zotero.
"""

import datetime
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from . import doi as _doi
from .config import relativo
from .dados import SUBPASTA_CROSSREF, SUBPASTA_OPENALEX
from .erros import FonteExterna
from .saida import Saida

UA = "rsl-sementes/1.0"
TIMEOUT = 45
PAUSA = 1.0
OPENALEX, CROSSREF = "openalex", "crossref"
FONTES = {
    OPENALEX: {"nome": "OpenAlex", "da": "da", "na": "na", "url": "https://api.openalex.org/works/doi:{doi}",
               "subpasta": SUBPASTA_OPENALEX},
    CROSSREF: {"nome": "Crossref", "da": "do", "na": "no", "url": "https://api.crossref.org/works/{doi}",
               "subpasta": SUBPASTA_CROSSREF},
}
CMD = "python3 -m rsl sementes metadados"


def pasta(ctx, fonte=OPENALEX):
    return ctx.config.caminho("dados.evidencia") / FONTES[fonte]["subpasta"]


def marcador(nome_json):
    """Nome do marcador de 404 correspondente ao nome da resposta."""
    return nome_json[:-len(".json")] + ".404"


def consulta(fonte, doi, abrir=None):
    """(status, corpo) da consulta de um DOI: 200 ou 404; o resto é FonteExterna."""
    f = FONTES[fonte]
    url = f["url"].format(doi=urllib.parse.quote(_doi.normaliza(doi), safe="/"))
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with (abrir or urllib.request.urlopen)(req, timeout=TIMEOUT) as r:
            status, corpo = r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 404, ""
        raise FonteExterna(f"resposta HTTP {e.code} {f['da']} {f['nome']} para o DOI {doi}") from None
    except Exception as e:                                          # noqa: BLE001
        motivo = getattr(e, "reason", None) or e
        raise FonteExterna(f"erro de rede {f['na']} {f['nome']} para o DOI {doi}: "
                           f"{type(e).__name__} ({motivo})") from None
    if status != 200:
        raise FonteExterna(f"resposta HTTP {status} {f['da']} {f['nome']} para o DOI {doi}")
    try:
        json.loads(corpo)
    except json.JSONDecodeError:
        raise FonteExterna(f"corpo fora do formato esperado (JSON) {f['da']} {f['nome']} para o DOI "
                           f"{doi}: {corpo[:80]!r}") from None
    return 200, corpo


# --------------------------------------------------------------------- extração
def resumo_openalex(resposta):
    """O resumo reconstruído de `abstract_inverted_index`; "" se ausente."""
    indice = (resposta or {}).get("abstract_inverted_index") or {}
    posicoes = [(p, palavra) for palavra, ps in indice.items() for p in ps]
    return " ".join(palavra for _, palavra in sorted(posicoes))


def palavras_chave_openalex(resposta):
    """As palavras-chave atribuídas pela OpenAlex (`keywords[].display_name`)."""
    return [k["display_name"] for k in (resposta or {}).get("keywords") or []
            if isinstance(k, dict) and k.get("display_name")]


def resumo_crossref(resposta):
    """O resumo do Crossref (`message.abstract`, em JATS) sem a marcação nem o título
    "Abstract"; "" se ausente."""
    texto = ((resposta or {}).get("message") or {}).get("abstract") or ""
    texto = re.sub(r"<(?:jats:)?title>.*?</(?:jats:)?title>", " ", texto, flags=re.S)
    texto = html.unescape(re.sub(r"<[^>]+>", " ", texto))
    return re.sub(r"\s+", " ", texto).strip()


RESUMO = {OPENALEX: resumo_openalex, CROSSREF: resumo_crossref}


# ----------------------------------------------------------------- estado gravado
def estado(ctx, fonte, doi):
    """O que está gravado para o DOI na fonte: ("resposta", dict), ("sem registro", None) ou
    ("não consultada", None) — esta cobre a consulta interrompida."""
    nome = _doi.nome_arquivo(doi)
    arq = pasta(ctx, fonte) / nome
    if arq.exists():
        return "resposta", json.loads(arq.read_text(encoding="utf-8"))
    if (pasta(ctx, fonte) / marcador(nome)).exists():
        return "sem registro", None
    return "não consultada", None


def resumos_do_zotero(ctx):
    """{DOI: resumo do item} da cópia da coleção; vazio se a cópia não existe."""
    from .zotero import le_copia, por_doi                           # noqa: PLC0415
    caminho = ctx.config.caminho("dados.zotero")
    if not caminho.exists():
        return {}
    return {d: cs[0]["resumo"] for d, cs in por_doi(le_copia(caminho)).items() if d and cs}


def respostas_gravadas(ctx, dois):
    """{DOI: (resumo, [palavras-chave])}: o resumo da OpenAlex ou, na falta dele, o do
    Crossref; as palavras-chave, só da OpenAlex. Só os DOIs com alguma resposta."""
    saida = {}
    for d in dois:
        k_oa, r_oa = estado(ctx, OPENALEX, d)
        k_cr, r_cr = estado(ctx, CROSSREF, d)
        if k_oa != "resposta" and k_cr != "resposta":
            continue
        resumo = resumo_openalex(r_oa) or resumo_crossref(r_cr)
        saida[_doi.normaliza(d)] = (resumo, palavras_chave_openalex(r_oa))
    return saida


def elegiveis_crossref(ctx, sementes):
    """Sementes sem resumo em fonte nenhuma, com resultado da OpenAlex registrado (resposta
    sem resumo ou 404). A não consultada na OpenAlex não é elegível: falta a primeira fonte,
    e o Crossref não substitui consulta interrompida."""
    no_zotero = resumos_do_zotero(ctx)
    saida = []
    for e in sementes:
        k, r = estado(ctx, OPENALEX, e["doi"])
        if k == "não consultada" or resumo_openalex(r):
            continue
        if no_zotero.get(_doi.normaliza(e["doi"])):
            continue
        saida.append(e)
    return saida


def pendencias(ctx, d):
    """Linhas de `projeto pendencias`, calculadas das respostas, dos marcadores e da cópia."""
    no_zotero = resumos_do_zotero(ctx)
    linhas = []
    for e in d["sementes"]:
        if not e.get("doi"):
            continue
        abertos = []
        k_oa, r_oa = estado(ctx, OPENALEX, e["doi"])
        k_cr, r_cr = estado(ctx, CROSSREF, e["doi"])
        if k_oa == "não consultada":
            abertos.append(f"sem resposta da OpenAlex (não consultada ou interrompida) — "
                           f"{CMD}")
        else:
            if k_oa == "sem registro":
                abertos.append("sem registro na OpenAlex")
            tem_resumo = (resumo_openalex(r_oa) or resumo_crossref(r_cr)
                          or no_zotero.get(_doi.normaliza(e["doi"])))
            de_fonte = resumo_openalex(r_oa) or resumo_crossref(r_cr)
            if de_fonte and not no_zotero.get(_doi.normaliza(e["doi"])):
                abertos.append("resumo ausente no item do Zotero, disponível na fonte — "
                               "`sementes completar --gravar`")
            if not tem_resumo and k_cr == "não consultada":
                abertos.append(f"resumo ausente na OpenAlex — {CMD} --fonte crossref")
            elif not tem_resumo:
                abertos.append("resumo ausente em todas as fontes (OpenAlex, Crossref, "
                               "Zotero) — o pesquisador preenche o resumo no Zotero")
        if abertos:
            linhas.append(f"[semente {e['id']} {e['chave']}] dados: {'; '.join(abertos)}")
    return linhas


# -------------------------------------------------------------------- consulta
def metadados(ctx, fonte=OPENALEX, todas=False, abrir=None, pausa=PAUSA):
    """Consulta a fonte para as sementes devidas, em ordem; grava as respostas 200 e os
    marcadores de 404. Devolve (linhas do relato, ids sem registro). FonteExterna interrompe
    as restantes, depois de imprimir o já feito."""
    f = FONTES[fonte]
    destino = pasta(ctx, fonte)
    destino.mkdir(parents=True, exist_ok=True)
    sementes = [e for e in ctx.protocolo()["sementes"] if e.get("doi")]
    if fonte == CROSSREF:
        sementes = elegiveis_crossref(ctx, sementes)
    if not todas:
        sementes = [e for e in sementes if estado(ctx, fonte, e["doi"])[0] == "não consultada"]
    linhas, sem_registro = [], []
    for k, e in enumerate(sementes):
        if k and pausa:
            time.sleep(pausa)
        try:
            status, corpo = consulta(fonte, e["doi"], abrir)
        except FonteExterna as erro:
            for l in linhas:
                print(l)
            raise FonteExterna(f"{e['id']}: {erro}. Consultas restantes não feitas: "
                               f"{len(sementes) - k - 1}; já registradas nesta execução: "
                               f"{len(linhas)}. Nenhuma nova tentativa nem outra fonte foi "
                               f"acionada") from None
        nome = _doi.nome_arquivo(e["doi"])
        if status == 404:
            agora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
            (destino / marcador(nome)).write_text(f"HTTP 404 em {agora}\n", encoding="utf-8")
            sem_registro.append(e["id"])
            linhas.append(f"  {e['id']:>4} {e['doi']}: sem registro {f['na']} {f['nome']}")
            continue
        arq = destino / nome
        arq.write_text(corpo, encoding="utf-8")
        (destino / marcador(nome)).unlink(missing_ok=True)
        resposta = json.loads(corpo)
        resumo = RESUMO[fonte](resposta)
        texto = f"sim ({len(resumo.split())} palavras)" if resumo else "não"
        extra = (f", {len(palavras_chave_openalex(resposta))} palavra(s)-chave"
                 if fonte == OPENALEX else "")
        linhas.append(f"  {e['id']:>4} {e['doi']}: resumo {texto}{extra} → {relativo(arq)}")
    return linhas, sem_registro


def cmd_metadados(ctx, a=None):
    fonte = getattr(a, "fonte", None) or OPENALEX
    linhas, sem_registro = metadados(ctx, fonte, todas=getattr(a, "todas", False))
    f = FONTES[fonte]
    nome = f["nome"]
    if not linhas:
        print(f"{nome}: nenhuma semente a consultar"
              + ("" if getattr(a, "todas", False) else " (só as sem resultado registrado; "
                                                       "--todas refaz)") + ".")
    else:
        nota = (" (palavras-chave atribuídas pela OpenAlex, não pelo autor nem pela base)"
                if fonte == OPENALEX else " (só o resumo; o Crossref não traz palavras-chave)")
        print(f"Respostas {f['da']} {nome} por semente{nota}:")
        for l in linhas:
            print(l)
    if sem_registro:
        print(f"Sem registro {f['na']} {nome}: {', '.join(sem_registro)}")
    return Saida.OK
