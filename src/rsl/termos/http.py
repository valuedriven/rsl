"""Cliente HTTP da validação terminológica: uma requisição, sem nova tentativa.

Cada chamada faz uma requisição e classifica o resultado em três tipos: resposta útil
(devolvida), termo ausente (decidido pelo cliente do instrumento, sobre a resposta útil) ou
`FonteExterna`, que interrompe a validação na hora. São `FonteExterna`:

  - erro de rede (DNS, conexão, TLS, tempo esgotado);
  - resposta HTTP diferente de 200 (403 bloqueio, 429 limite, 5xx, e qualquer outra);
  - resposta 200 com marca de captcha ou de aviso de atividade atípica no corpo;
  - resposta 200 cujo corpo não está no formato esperado (JSON, SPARQL JSON).

A detecção de captcha é HEURÍSTICA, por marcadores no corpo: ela pode falhar. O caminho
conservador é o último item — corpo fora do formato esperado também interrompe —, de modo
que a falha de reconhecimento para a validação em vez de seguir adiante.

Não há concorrência, nem nova tentativa, nem outra rota ou endereço depois da falha
(AGENTS.md §9). A pausa entre requisições é do cliente de cada instrumento.
"""

import json
import urllib.error
import urllib.request

from ..erros import FonteExterna

TIMEOUT = 45
UA = "validacao-terminologica-RSL/1.0 (pesquisa academica; uso nao comercial)"
# Marcadores de captcha ou de aviso de atividade atípica, procurados no corpo em minúsculas.
MARCAS_BLOQUEIO = ("captcha", "unusual traffic", "atividade atípica", "atividade incomum",
                   "are you a robot", "are you human", "access denied", "too many requests",
                   "rate limit")


def requisicao(url, dados=None, cabecalhos=None):
    """Uma requisição. Devolve o corpo (texto) da resposta 200; senão, FonteExterna."""
    req = urllib.request.Request(url, data=dados, headers={"User-Agent": UA,
                                                           **(cabecalhos or {})})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            status, corpo = r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        condicao = {403: "bloqueio (HTTP 403)", 429: "limite excedido (HTTP 429)"}.get(
            e.code, f"erro do servidor (HTTP {e.code})" if e.code >= 500
            else f"resposta HTTP {e.code}")
        raise FonteExterna(f"{condicao} em {url}") from None
    except Exception as e:                                          # noqa: BLE001
        raise FonteExterna(f"erro de rede em {url}: {e!r}") from None
    if status != 200:
        raise FonteExterna(f"resposta HTTP {status} em {url}")
    baixo = corpo.lower()
    marca = next((m for m in MARCAS_BLOQUEIO if m in baixo), None)
    if marca:
        raise FonteExterna(f"página com marca de captcha ou de atividade atípica "
                           f"({marca!r}) em {url}")
    return corpo


def json_de(corpo, url):
    """O corpo como JSON; corpo fora do formato esperado é FonteExterna."""
    try:
        return json.loads(corpo)
    except json.JSONDecodeError:
        raise FonteExterna(f"corpo fora do formato esperado (JSON) em {url}: "
                           f"{corpo[:120]!r}") from None
