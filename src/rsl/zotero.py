"""Acesso ao Zotero e coleção de sementes: o cliente das duas vias, a cópia versionada, os
campos extraídos de cada item e o complemento da coleção.

Os dados bibliográficos, o resumo e as palavras-chave das sementes ficam no Zotero, na
coleção de `[zotero]` do `config.toml`; o arquivo de sementes guarda o controle e liga cada
semente ao item pelo DOI. Os comandos de análise não consultam o Zotero: leem a cópia em
`[dados] zotero`, gravada só por `sementes copiar` (e regravada por
`sementes completar --gravar`).

Acesso (AGENTS.md §9):
  - a via é a de `[zotero] acesso`, para ler e para escrever: `local` (o Zotero da máquina,
    `API_LOCAL`, aberto e com o acesso local habilitado nas preferências) ou `web` (a API
    web, `API`). Os caminhos de biblioteca e de coleção são os mesmos nas duas. O único
    construtor é `cliente(ctx)`; o cliente conhece uma só base de endereço, e por isso
    nenhum pedido recusado se repete pela outra via, nem automaticamente nem por escolha
    do código;
  - a chave da API web só se lê na via web. Vem da variável de ambiente `ZOTERO_API_KEY` ou,
    na falta, da linha `ZOTERO_API_KEY=` do `.env` da raiz, que tem de estar no `.gitignore`;
    é emitida pelo pesquisador e nunca se grava nem se imprime — em relato, só os quatro
    últimos caracteres; vai só no cabeçalho da requisição, nunca no endereço. Na via local,
    a leitura não lê variável nem `.env`; a escrita exige a chave da API local
    (`ZOTERO_LOCAL_API_KEY`) e o identificador do servidor (`ZOTERO_SERVER_ID`), lidos do
    mesmo modo e com as mesmas guardas só no primeiro pedido de escrita, e enviados só nele
    e nos seguintes;
  - nas duas vias, uma requisição por vez, sem nova tentativa: erro de rede, resposta fora
    do esperado, conflito de versão (412), limite de uso (429), pedido de espera (`Backoff`,
    `Retry-After`) ou falta de permissão interrompem o subcomando com FONTE_EXTERNA, cuja
    mensagem nomeia a via e o pedido. Na via local, o erro de conexão diz que o Zotero tem
    de estar aberto com o acesso local habilitado, e a escrita recusada indica conferir as
    credenciais locais ou escrever pela via web;
  - a escrita só acrescenta ou completa (resumo onde está vazio, etiquetas novas), exceto a
    retirada de item da coleção, que depende de `--retirar` e não apaga o item da biblioteca.
"""

import datetime
import json
import os
import pathlib
import shutil
import tempfile
import urllib.error
import urllib.parse
import urllib.request

from . import doi as _doi
from .config import RAIZ, linha_ignorada, relativo
from .erros import ConfiguracaoInvalida, DadosInvalidos, FonteExterna, Uso
from .markdown import normaliza
from .saida import Saida

VARIAVEL_CHAVE = "ZOTERO_API_KEY"
# Escrita pela API local: chave própria da API local e identificador do servidor, obtidos pelo
# pesquisador no Zotero da máquina (procedimento no README); lidos só quando há escrita.
VARIAVEL_CHAVE_LOCAL = "ZOTERO_LOCAL_API_KEY"
VARIAVEL_SERVIDOR = "ZOTERO_SERVER_ID"
# Arquivo de ambiente com a chave, na raiz; tem de estar no .gitignore.
ARQUIVO_CHAVE = RAIZ / ".env"
API = "https://api.zotero.org"
# API local do Zotero da máquina do pesquisador: mesmos caminhos da API web; a leitura dispensa
# chave, a escrita exige a chave local e o identificador do servidor. Só responde com o Zotero
# aberto e o acesso local habilitado nas preferências.
API_LOCAL = "http://localhost:23119/api"
BASES = {"local": API_LOCAL, "web": API}
METODOS_ESCRITA = ("POST", "PUT", "PATCH", "DELETE")
TIMEOUT = 45
POR_PAGINA = 100
UA = "rsl-sementes/1.0"
SUBPASTA_RESTAURACAO = "zotero"
CMD_COPIAR = "python3 -m rsl sementes copiar"
# Tipo da etiqueta automática no Zotero (a manual é 0).
ETIQUETA_AUTOMATICA = 1

# Campo do veículo por tipo de item; tipo fora da lista usa o primeiro preenchido.
VEICULO = {"journalArticle": "publicationTitle", "conferencePaper": "proceedingsTitle",
           "bookSection": "bookTitle"}
_VEICULOS = ("publicationTitle", "proceedingsTitle", "bookTitle")
# Campos comparados entre duas cópias, na ordem do relato.
COMPARADOS = ("autores", "ano", "titulo", "veiculo", "volume", "numero", "paginas", "resumo",
              "palavras_chave")


# ------------------------------------------------------------------------- chave
def _do_arquivo(arquivo, variavel=VARIAVEL_CHAVE):
    """O valor de `<variavel>=` no arquivo de ambiente; "" se o arquivo ou a linha não
    existem. Arquivo que o `.gitignore` não lista é recusado: a chave iria ao controle de
    versão no próximo `git add`."""
    arquivo = pathlib.Path(arquivo)
    if not arquivo.exists():
        return ""
    if not linha_ignorada(arquivo.parent / ".gitignore", arquivo.name):
        raise ConfiguracaoInvalida(
            f"{arquivo.name} existe e o .gitignore não o lista: a chave iria ao controle de "
            f"versão. Acrescentar `{arquivo.name}` ao .gitignore antes de usá-lo")
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha.startswith("export "):
            linha = linha[len("export "):].strip()
        if linha.startswith(f"{variavel}="):
            return linha.split("=", 1)[1].strip().strip("'\"")
    return ""


def _do_ambiente(variavel, arquivo=None):
    """O valor da variável de ambiente ou, na falta, o da linha do arquivo de ambiente."""
    valor = os.environ.get(variavel, "").strip()
    return valor or _do_arquivo(ARQUIVO_CHAVE if arquivo is None else arquivo, variavel)


def chave_api(arquivo=None):
    """A chave: a da variável de ambiente ou, na falta, a do arquivo de ambiente da raiz
    (`.env`, fora do controle de versão). Ausente nos dois é CONFIGURACAO."""
    chave = _do_ambiente(VARIAVEL_CHAVE, arquivo)
    if not chave:
        raise ConfiguracaoInvalida(
            f"chave da API web do Zotero ausente: nem a variável de ambiente "
            f"{VARIAVEL_CHAVE} nem a linha `{VARIAVEL_CHAVE}=` em {ARQUIVO_CHAVE.name} (raiz do "
            f"projeto, listado no .gitignore). O pesquisador emite a chave (escrita só na "
            f"biblioteca de grupo) e a guarda fora do controle de versão; os subcomandos que "
            f"não acessam o Zotero não dependem dela")
    return chave


def credenciais_locais(arquivo=None):
    """(chave da API local, identificador do servidor), para a escrita pela via local; a
    falta de qualquer um é CONFIGURACAO, antes de qualquer pedido."""
    chave = _do_ambiente(VARIAVEL_CHAVE_LOCAL, arquivo)
    servidor = _do_ambiente(VARIAVEL_SERVIDOR, arquivo)
    faltam = [v for v, x in ((VARIAVEL_CHAVE_LOCAL, chave), (VARIAVEL_SERVIDOR, servidor))
              if not x]
    if faltam:
        raise ConfiguracaoInvalida(
            f"escrita pela via local do Zotero sem {' nem '.join(faltam)}: nem na variável de "
            f"ambiente nem em {ARQUIVO_CHAVE.name} (raiz, listado no .gitignore). O pesquisador "
            f"os obtém no Zotero da máquina (procedimento no README) e os guarda fora do "
            f"controle de versão; a leitura pela via local não depende deles. Nada foi pedido "
            f"ao Zotero")
    return chave, servidor


def mascara(chave):
    """O que se pode imprimir da chave: só os quatro últimos caracteres."""
    return f"…{chave[-4:]}" if len(chave) > 4 else "…"


# ----------------------------------------------------------------------- cliente
class Conflito(FonteExterna):
    """O item mudou no Zotero depois da cópia (HTTP 412)."""


class Cliente:
    """Uma requisição por vez à base da via, sem nova tentativa. A via (`local` ou `web`)
    fixa a base de endereço: o cliente conhece uma só, e por isso nenhum pedido recusado se
    repete pela outra. Na via web, a chave vai em todo pedido. Na via local, a leitura vai sem
    chave, e a escrita leva a chave local e o identificador do servidor, obtidos de
    `credenciais` (por padrão, `credenciais_locais`) só no primeiro pedido de escrita. `abrir`
    substitui `urllib.request.urlopen` (autoteste, servidor simulado)."""

    def __init__(self, via, chave=None, abrir=None, credenciais=None):
        if via not in BASES:
            raise ConfiguracaoInvalida(f"via de acesso ao Zotero {via!r} fora dos valores "
                                       f"aceitos: {', '.join(BASES)}")
        if via == "web" and not chave:
            raise ConfiguracaoInvalida("a via web do Zotero exige a chave da API")
        self.via = via
        self.chave = chave if via == "web" else None
        self._servidor = None
        self._credenciais = credenciais or credenciais_locais
        self._abrir = abrir or urllib.request.urlopen
        self.base = BASES[via]

    def _cabecalhos_de_acesso(self, metodo):
        if self.via == "web":
            return {"Zotero-API-Key": self.chave}
        if metodo not in METODOS_ESCRITA:
            return {}
        if self._servidor is None:
            self.chave, self._servidor = self._credenciais()
        return {"Zotero-API-Key": self.chave, "Zotero-Server-ID": self._servidor}

    def rotulo(self, metodo, caminho):
        return f"{metodo} {caminho.split('?')[0]} (via {self.via})"

    def _recusa(self, metodo, condicao, rotulo, extra=""):
        """FonteExterna do pedido; na via local, a escrita recusada indica o que conferir."""
        dica = ""
        if self.via == "local" and metodo in METODOS_ESCRITA:
            dica = (f"; escrita recusada pela via local, e nada foi repetido pela via web: "
                    f"conferir {VARIAVEL_CHAVE_LOCAL} e {VARIAVEL_SERVIDOR} (procedimento no "
                    f"README) ou escrever com `[zotero] acesso = \"web\"` na configuração")
        return FonteExterna(f"{condicao} em {rotulo}{extra}{dica}")

    def pedido(self, metodo, caminho, corpo=None, cabecalhos=None):
        """(status, cabeçalhos em minúsculas, corpo em texto). Falha é FonteExterna, cuja
        mensagem nomeia o método e o caminho, nunca a chave."""
        url = f"{self.base}/{caminho.lstrip('/')}"
        dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8") if corpo is not None \
            else None
        cab = {"User-Agent": UA, "Zotero-API-Version": "3",
               **self._cabecalhos_de_acesso(metodo),
               **({"Content-Type": "application/json"} if dados is not None else {}),
               **(cabecalhos or {})}
        req = urllib.request.Request(url, data=dados, headers=cab, method=metodo)
        rotulo = self.rotulo(metodo, caminho)
        try:
            with self._abrir(req, timeout=TIMEOUT) as r:
                status = r.status
                h = {k.lower(): v for k, v in r.headers.items()}
                texto = r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            h = {k.lower(): v for k, v in (e.headers or {}).items()}
            espera = h.get("retry-after")
            if e.code == 412:
                raise Conflito(f"conflito de versão (HTTP 412) em {rotulo}") from None
            permissao = ("chave sem permissão (HTTP 403) — conferir em "
                         "zotero.org/settings/keys se a chave tem escrita na biblioteca de "
                         "grupo (permissão por grupo)" if self.via == "web"
                         else "acesso recusado pelo Zotero local (HTTP 403)")
            condicao = {403: permissao,
                        429: "limite de uso excedido (HTTP 429)",
                        503: "serviço indisponível (HTTP 503)"}.get(e.code,
                                                                    f"resposta HTTP {e.code}")
            extra = f"; pedido de espera de {espera} s" if espera else ""
            raise self._recusa(metodo, condicao, rotulo, extra) from None
        except Exception as e:                                      # noqa: BLE001
            local = ("; o Zotero tem de estar aberto nesta máquina, com o acesso local "
                     "habilitado nas preferências" if self.via == "local" else "")
            raise FonteExterna(f"erro de rede em {rotulo}: {type(e).__name__}{local}") \
                from None
        if metodo in METODOS_ESCRITA and not 200 <= status < 300:
            raise self._recusa(metodo, f"resposta HTTP {status}", rotulo)
        return status, h, texto


def cliente(ctx, abrir=None):
    """O cliente da via de `[zotero] acesso`: o único construtor de que todo acesso ao
    Zotero depende. A chave da API web só se lê na via web; as credenciais da via local, só
    no primeiro pedido de escrita."""
    via = ctx.config.valor("zotero.acesso")
    return Cliente(via, chave_api() if via == "web" else None, abrir)


def _sem_espera(h, rotulo):
    """Pedido de espera numa resposta bem-sucedida também interrompe."""
    for nome in ("backoff", "retry-after"):
        if h.get(nome):
            raise FonteExterna(f"pedido de espera do Zotero ({nome}: {h[nome]} s) em {rotulo}")


def le_colecao(cliente, biblioteca, colecao):
    """A coleção lida pela via do cliente: {biblioteca, colecao, versao, via, lida_em,
    itens}, com os itens de topo como a API os devolve (formato json)."""
    itens, inicio, total, versao = [], 0, None, None
    while total is None or inicio < total:
        caminho = (f"{biblioteca}/collections/{colecao}/items/top?"
                   + urllib.parse.urlencode({"format": "json", "limit": POR_PAGINA,
                                             "start": inicio}))
        status, h, texto = cliente.pedido("GET", caminho)
        rotulo = cliente.rotulo("GET", caminho)
        if status != 200:
            raise FonteExterna(f"resposta HTTP {status} em {rotulo}")
        _sem_espera(h, rotulo)
        try:
            pagina = json.loads(texto)
            total = int(h.get("total-results", len(pagina)))
            versao = int(h["last-modified-version"])
        except (json.JSONDecodeError, KeyError, ValueError):
            raise FonteExterna(f"resposta fora do formato esperado em {rotulo}") from None
        if not isinstance(pagina, list):
            raise FonteExterna(f"resposta fora do formato esperado em {rotulo}")
        itens += pagina
        if not pagina:
            break
        inicio += len(pagina)
    lida = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    return {"biblioteca": biblioteca, "colecao": colecao, "versao": versao,
            "via": cliente.via, "lida_em": lida, "itens": itens}


# --------------------------------------------------------------------- coleções
def subcolecoes(cliente, biblioteca, mae):
    """[(chave, nome)] das coleções-filhas de `mae` (None: as da raiz da biblioteca), lidas
    pela via do cliente, paginadas."""
    filhas, inicio, total = [], 0, None
    lista = f"{biblioteca}/collections/top" if mae is None \
        else f"{biblioteca}/collections/{mae}/collections"
    while total is None or inicio < total:
        caminho = (f"{lista}?"
                   + urllib.parse.urlencode({"format": "json", "limit": POR_PAGINA,
                                             "start": inicio}))
        status, h, texto = cliente.pedido("GET", caminho)
        rotulo = cliente.rotulo("GET", caminho)
        if status != 200:
            raise FonteExterna(f"resposta HTTP {status} em {rotulo}")
        _sem_espera(h, rotulo)
        try:
            pagina = json.loads(texto)
            total = int(h.get("total-results", len(pagina)))
            filhas += [(c["key"], (c.get("data") or {})["name"]) for c in pagina]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            raise FonteExterna(f"resposta fora do formato esperado em {rotulo}") from None
        if not pagina:
            break
        inicio += len(pagina)
    return filhas


def localiza(filhas, nome, identificador=None):
    """A chave da única filha com o nome ou, com `identificador`, da única cujo nome começa
    por ele (coleção de execução). Nenhuma é None; duas ou mais é DADOS, nomeando as chaves,
    sem escolher uma."""
    if identificador:
        achadas = [(k, n) for k, n in filhas
                   if n == identificador or n.startswith(f"{identificador} ")]
        alvo = f"com o identificador {identificador!r} no início do nome"
    else:
        achadas = [(k, n) for k, n in filhas if n == nome]
        alvo = f"nomeadas {nome!r}"
    if len(achadas) > 1:
        raise DadosInvalidos(f"{len(achadas)} coleções-filhas {alvo}: "
                             + ", ".join(f"{k} ({n!r})" for k, n in achadas)
                             + " — o Zotero tem de ter uma só; nenhuma foi escolhida")
    return achadas[0][0] if achadas else None


def subcolecao(cliente, biblioteca, mae, nome, identificador=None):
    """A chave da filha, para quem só lê: ausente é DADOS, e nada se cria."""
    chave = localiza(subcolecoes(cliente, biblioteca, mae), nome, identificador)
    if chave is None:
        onde = "na raiz" if mae is None else f"dentro da coleção {mae}"
        raise DadosInvalidos(f"coleção {nome!r} ausente {onde} de {biblioteca}; nada foi "
                             f"criado: só um subcomando que escreve no Zotero a cria")
    return chave


def garante(cliente, biblioteca, mae, nome, identificador=None):
    """A chave da filha, criando-a quando ausente. Só para subcomandos que escrevem."""
    chave = localiza(subcolecoes(cliente, biblioteca, mae), nome, identificador)
    if chave is not None:
        return chave
    caminho = f"{biblioteca}/collections"
    status, h, texto = cliente.pedido("POST", caminho, [
        {"name": nome, **({"parentCollection": mae} if mae is not None else {})}])
    rotulo = cliente.rotulo("POST", caminho)
    try:
        resposta = json.loads(texto)
        criada = resposta["successful"]["0"]["key"]
    except (json.JSONDecodeError, KeyError, TypeError):
        falha = ""
        try:
            falha = f": {json.loads(texto)['failed']['0'].get('message', '')}"
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
            pass
        raise cliente._recusa("POST", f"coleção {nome!r} não criada{falha}", rotulo) from None
    for cab in ("backoff", "retry-after"):
        if h.get(cab):
            raise FonteExterna(f"coleção {nome!r} criada ({criada}), e o Zotero pediu espera "
                               f"({cab}: {h[cab]} s) em {rotulo}: nenhum pedido depois dele")
    return criada


def colecao_das_buscas(ctx, cliente):
    """(biblioteca, chave) da coleção das buscas, localizada pelo nome de
    `[zotero] search_collection` na raiz da biblioteca das buscas (`[zotero] library`). Só
    leitura: ausente é DADOS, homônimas também; nada se cria."""
    biblioteca, nome = ctx.config.buscas()
    return biblioteca, subcolecao(cliente, biblioteca, None, nome)


# ------------------------------------------------------------------------ campos
def doi_do_item(dado):
    """DOI do campo DOI ou, na falta, da linha `DOI:` do campo extra; normalizado."""
    valor = (dado.get("DOI") or "").strip()
    if not valor:
        for linha in (dado.get("extra") or "").splitlines():
            if linha.strip().lower().startswith("doi:"):
                valor = linha.split(":", 1)[1].strip()
                break
    return _doi.normaliza(valor)


def campos(item):
    """Os campos de uma semente extraídos do item, sem transcrição."""
    dado = item.get("data") or {}
    autores = []
    for c in dado.get("creators") or []:
        if c.get("creatorType") != "author":
            continue
        if c.get("lastName"):
            autores.append(", ".join(x for x in (c["lastName"].strip(),
                                                 (c.get("firstName") or "").strip()) if x))
        elif (c.get("name") or "").strip():
            autores.append(c["name"].strip())
    data = str((item.get("meta") or {}).get("parsedDate") or "")
    tipo = dado.get("itemType") or ""
    veiculo = dado.get(VEICULO[tipo], "") if tipo in VEICULO else next(
        (dado[c] for c in _VEICULOS if dado.get(c)), "")
    return {
        "chave_item": item.get("key") or dado.get("key") or "",
        "versao_item": item.get("version", dado.get("version")),
        "tipo": tipo,
        "doi": doi_do_item(dado),
        "autores": autores,
        "ano": int(data[:4]) if data[:4].isdigit() else None,
        "titulo": (dado.get("title") or "").strip(),
        "veiculo": (veiculo or "").strip(),
        "volume": (dado.get("volume") or "").strip(),
        "numero": (dado.get("issue") or "").strip(),
        "paginas": (dado.get("pages") or "").strip(),
        "resumo": (dado.get("abstractNote") or "").strip(),
        "palavras_chave": [t["tag"] for t in dado.get("tags") or [] if t.get("tag")],
        "colecoes": list(dado.get("collections") or []),
    }


def por_doi(doc):
    """{DOI normalizado: [campos dos itens com esse DOI]}; item sem DOI fica sob ""."""
    saida = {}
    for item in doc.get("itens") or []:
        c = campos(item)
        saida.setdefault(c["doi"], []).append(c)
    return saida


# ------------------------------------------------------------------------- cópia
def le_copia(caminho):
    """A cópia gravada; ausente ou ilegível é DADOS, com a indicação de `sementes copiar`."""
    caminho = pathlib.Path(caminho)
    if not caminho.exists():
        raise DadosInvalidos(f"cópia da coleção do Zotero {relativo(caminho)} ausente — "
                             f"gravá-la com  {CMD_COPIAR}")
    try:
        doc = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise DadosInvalidos(f"cópia da coleção do Zotero {relativo(caminho)} ilegível "
                             f"({e}) — regravá-la com  {CMD_COPIAR}") from None
    faltam = [c for c in ("biblioteca", "colecao", "versao", "lida_em", "itens")
              if c not in doc] if isinstance(doc, dict) else ["(não é objeto JSON)"]
    if faltam or not isinstance(doc.get("itens"), list):
        raise DadosInvalidos(f"cópia da coleção do Zotero {relativo(caminho)} fora da forma "
                             f"(falta {', '.join(faltam) or 'a lista de itens'}) — regravá-la "
                             f"com  {CMD_COPIAR}")
    return doc


def _rotulo(doi, c):
    return doi or f"(sem DOI, item {c['chave_item']})"


def diferencas(anterior, nova):
    """Linhas do relato: itens acrescentados, retirados e campos alterados, por DOI."""
    def indice(doc):
        saida = {}
        for item in (doc or {}).get("itens") or []:
            c = campos(item)
            saida[c["doi"] or f"chave:{c['chave_item']}"] = c
        return saida
    antes, depois = indice(anterior), indice(nova)
    linhas = []
    for k in depois:
        if k not in antes:
            linhas.append(f"  + acrescentado: {_rotulo(depois[k]['doi'], depois[k])} — "
                          f"{depois[k]['titulo'][:70]}")
    for k in antes:
        if k not in depois:
            linhas.append(f"  - retirado: {_rotulo(antes[k]['doi'], antes[k])} — "
                          f"{antes[k]['titulo'][:70]}")
    for k in depois:
        if k in antes:
            for campo in COMPARADOS:
                a, b = antes[k][campo], depois[k][campo]
                if a != b:
                    linhas.append(f"  ~ alterado: {_rotulo(depois[k]['doi'], depois[k])} "
                                  f"{campo}: {_curto(a)!r} → {_curto(b)!r}")
    return linhas


def _curto(valor, n=90):
    texto = "; ".join(valor) if isinstance(valor, list) else str(valor if valor is not None
                                                                  else "")
    return texto if len(texto) <= n else texto[:n - 1] + "…"


def grava_texto(destino, texto, chave=None):
    """Grava num temporário do mesmo diretório e só então substitui o anterior: interrupção
    no meio deixa o anterior intacto e nenhum arquivo parcial com o nome final. Se o texto
    contiver a chave da API, nada se grava (garantia, não conferência posterior)."""
    if chave and chave in texto:
        raise FonteExterna("o conteúdo a gravar contém a chave da API; nada foi gravado")
    destino = pathlib.Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=destino.parent, prefix=f".{destino.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(texto)
        os.replace(tmp, destino)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def grava_json(destino, doc, chave=None):
    """O documento em JSON, gravado por `grava_texto`."""
    grava_texto(destino, json.dumps(doc, ensure_ascii=False, indent=1) + "\n", chave)


def _registros_ris(texto):
    return sum(1 for l in texto.splitlines() if l.startswith("ER  -"))


def obtem_exportacao(cliente, biblioteca, colecao, destino):
    """A exportação de uma coleção de execução, em RIS, pela via do cliente, paginada
    (`limit`, `start`, `Total-Results`), gravada em `destino` só depois de lida por inteiro.
    Devolve o número de registros. Página fora do esperado, pedido de espera ou erro param
    sem novo pedido, e o arquivo anterior fica intacto."""
    paginas, inicio, total = [], 0, None
    while total is None or inicio < total:
        caminho = (f"{biblioteca}/collections/{colecao}/items/top?"
                   + urllib.parse.urlencode({"format": "ris", "limit": POR_PAGINA,
                                             "start": inicio}))
        status, h, texto = cliente.pedido("GET", caminho)
        rotulo = cliente.rotulo("GET", caminho)
        if status != 200:
            raise FonteExterna(f"resposta HTTP {status} em {rotulo}")
        _sem_espera(h, rotulo)
        try:
            total = int(h["total-results"])
        except (KeyError, ValueError):
            raise FonteExterna(f"resposta sem `Total-Results` em {rotulo}; nada foi "
                               f"gravado") from None
        n = _registros_ris(texto)
        if n == 0 and inicio < total:
            raise FonteExterna(f"página vazia em {rotulo} com {inicio} de {total} registros "
                               f"lidos; nada foi gravado")
        paginas.append(texto.strip("\n"))
        inicio += n
    if inicio != total:
        raise FonteExterna(f"{inicio} registros lidos de {total} anunciados em "
                           f"{biblioteca}/collections/{colecao}; nada foi gravado")
    if total == 0:
        # A via local responde 200, sem itens, também à coleção que não existe mais; e
        # execução sem registros não tem exportação. Nada se grava.
        raise DadosInvalidos(f"coleção {colecao} de {biblioteca} sem itens (vazia ou "
                             f"inexistente, via {cliente.via}); nada foi gravado")
    grava_texto(destino, "\n\n".join(paginas) + "\n", cliente.chave)
    return inicio


def _configurado(ctx):
    return ctx.config.biblioteca(), ctx.config.valor("zotero.colecao")


def _acesso(cliente):
    """O que se imprime da via: o nome e, na web, só os quatro últimos caracteres da chave."""
    return f"via {cliente.via}" + (f", chave {mascara(cliente.chave)}" if cliente.chave else "")


def via_da_copia(doc):
    """A via que leu a cópia; a cópia gravada antes do registro da via é da via web, a única
    que havia."""
    return doc.get("via") or "web"


def copia(ctx, cliente):
    """Lê a coleção, relata a diferença para a cópia anterior e grava a nova cópia."""
    biblioteca, colecao = _configurado(ctx)
    destino = ctx.config.caminho("dados.zotero")
    anterior = le_copia(destino) if destino.exists() else None
    nova = le_colecao(cliente, biblioteca, colecao)
    linhas = diferencas(anterior, nova)
    print(f"Coleção {colecao} de {biblioteca}: {len(nova['itens'])} itens, versão "
          f"{nova['versao']} da biblioteca, lida em {nova['lida_em']} ({_acesso(cliente)})")
    if anterior is None:
        print("Sem cópia anterior: todos os itens entram como acrescentados.")
    else:
        print(f"Diferença para a cópia anterior (versão {anterior['versao']}, lida em "
              f"{anterior['lida_em']}"
              + (f", via {anterior['via']}" if anterior.get("via") else "")
              + f"): {len(linhas) or 'nenhuma'}")
        if via_da_copia(anterior) != cliente.via:
            print(f"AVISO: a cópia anterior foi lida pela via {via_da_copia(anterior)} e esta, "
                  f"pela via {cliente.via}. A versão não se compara entre vias, e a ordem das "
                  f"etiquetas pode diferir sem mudança de conteúdo. A premissa é manter a mesma "
                  f"via em toda a sessão.")
    for l in linhas:
        print(l)
    grava_json(destino, nova, cliente.chave)
    print(f"Cópia gravada em {relativo(destino)}.")
    return nova


def cmd_copiar(ctx, a=None):
    copia(ctx, cliente(ctx))
    return Saida.OK


# -------------------------------------------------------------------- complemento
def plano(doc, dois_sementes, respostas, retirar=()):
    """O que `sementes completar` gravaria, por item.

    `dois_sementes`: DOIs normalizados do arquivo de sementes; `respostas`: {DOI: (resumo,
    [palavras-chave])} gravados (resumo da OpenAlex ou, na falta, do Crossref); `retirar`: DOIs normalizados a tirar da coleção.
    Devolve (ações, fora): ações [{"item", "resumo", "etiquetas", "retirar"}] só dos itens
    com algo a gravar; fora, os itens que não estão no arquivo de sementes e não se retiram.
    """
    acoes, fora = [], []
    for item in doc.get("itens") or []:
        c = campos(item)
        if c["doi"] and c["doi"] in retirar:
            acoes.append({"item": item, "campos": c, "resumo": None, "etiquetas": [],
                          "retirar": True})
            continue
        if c["doi"] not in dois_sementes:
            fora.append(c)
            continue
        resumo, palavras = respostas.get(c["doi"], ("", []))
        novo_resumo = resumo if resumo and not c["resumo"] else None
        existentes = {normaliza(t) for t in c["palavras_chave"]}
        novas = []
        for p in palavras:
            if p and normaliza(p) not in existentes:
                existentes.add(normaliza(p))
                novas.append(p)
        if novo_resumo or novas:
            acoes.append({"item": item, "campos": c, "resumo": novo_resumo,
                          "etiquetas": novas, "retirar": False})
    return acoes, fora


def corpo_da_acao(acao, colecao):
    """O PATCH de uma ação: só os campos que mudam; etiquetas existentes preservadas."""
    dado = acao["item"].get("data") or {}
    corpo = {}
    if acao["resumo"]:
        corpo["abstractNote"] = acao["resumo"]
    if acao["etiquetas"]:
        corpo["tags"] = list(dado.get("tags") or []) + [
            {"tag": t, "type": ETIQUETA_AUTOMATICA} for t in acao["etiquetas"]]
    if acao["retirar"]:
        corpo["collections"] = [c for c in dado.get("collections") or [] if c != colecao]
    return corpo


def imprime_plano(acoes, fora, retirar):
    print(f"Plano: {len(acoes)} item(ns) com algo a gravar.")
    for x in acoes:
        c = x["campos"]
        if x["retirar"]:
            print(f"  {c['doi']}: retirar da coleção (o item continua na biblioteca)")
            continue
        partes = []
        if x["resumo"]:
            partes.append(f"resumo ({len(x['resumo'].split())} palavras)")
        if x["etiquetas"]:
            partes.append(f"{len(x['etiquetas'])} etiqueta(s) automática(s): "
                          + "; ".join(x["etiquetas"]))
        print(f"  {c['doi']}: " + " + ".join(partes))
    if fora:
        print(f"Itens da coleção fora do arquivo de sementes ({len(fora)}), só relatados"
              f"{'' if retirar else '; retirá-los com --retirar <DOI>'}:")
        for c in fora:
            print(f"  {_rotulo(c['doi'], c)} — {c['titulo'][:70]}")


def aplica(cliente, biblioteca, colecao, acoes):
    """Grava as ações item a item, com o controle de versão do item. Para no primeiro
    conflito, limite ou pedido de espera, sem nova tentativa. Devolve as ações gravadas."""
    feitas = []
    for x in acoes:
        c = x["campos"]
        caminho = f"{biblioteca}/items/{c['chave_item']}"
        try:
            status, h, _ = cliente.pedido(
                "PATCH", caminho, corpo_da_acao(x, colecao),
                {"If-Unmodified-Since-Version": str(c["versao_item"])})
        except Conflito:
            _interrompe(feitas, f"conflito de versão no item {c['doi']}: o item mudou no "
                                f"Zotero depois da cópia. Rodar  {CMD_COPIAR}  e refazer o "
                                f"plano")
        except FonteExterna as e:
            _interrompe(feitas, f"no item {c['doi']}: {e}")
        if status != 204:
            _interrompe(feitas, f"resposta HTTP {status} no item {c['doi']}")
        feitas.append(x)
        print(f"  gravado: {c['doi']}")
        if h.get("backoff") or h.get("retry-after"):
            _interrompe(feitas, f"pedido de espera do Zotero depois do item {c['doi']}")
    return feitas


def _interrompe(feitas, motivo):
    raise FonteExterna(f"gravação interrompida, sem nova tentativa — {motivo}. "
                       f"{len(feitas)} item(ns) gravado(s) antes da interrupção"
                       + (": " + ", ".join(x["campos"]["doi"] for x in feitas) if feitas
                          else ""))


def ponto_de_restauracao(ctx, destino):
    """Guarda a cópia corrente em `[dados] evidencia`/zotero/, antes da primeira gravação."""
    agora = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    pasta = ctx.config.caminho("dados.evidencia") / SUBPASTA_RESTAURACAO
    pasta.mkdir(parents=True, exist_ok=True)
    alvo = pasta / f"{pathlib.Path(destino).stem}_antes_{agora}.json"
    shutil.copyfile(destino, alvo)
    return alvo


def confere_retirar(ctx, retirar, doc=None):
    """Recusa com USO o `--retirar` de DOI de semente do arquivo ou sem item na cópia, antes
    de ler a chave e de qualquer pedido ao Zotero. Devolve (DOIs das sementes, DOIs a retirar),
    normalizados."""
    if doc is None:
        doc = le_copia(ctx.config.caminho("dados.zotero"))
    dois = {_doi.normaliza(e["doi"]) for e in ctx.protocolo()["sementes"] if e.get("doi")}
    retirar = {_doi.normaliza(x) for x in retirar}
    na_colecao = {c["doi"] for c in map(campos, doc["itens"])}
    for x in sorted(retirar):
        if x in dois:
            raise Uso(f"--retirar {x}: o DOI é de uma semente do arquivo de sementes; tirar "
                      f"o item da coleção quebraria a leitura de todos os comandos. Retirar a "
                      f"semente do arquivo antes de tirá-la da coleção")
        if x not in na_colecao:
            raise Uso(f"--retirar {x}: nenhum item da cópia da coleção tem esse DOI")
    return dois, retirar


def completa(ctx, cliente, retirar=(), gravar=False):
    """Imprime o plano e, com `gravar`, aplica-o e regrava a cópia. Não devolve nada: o
    plano, para inspeção, é `plano()`."""
    from .metadados import respostas_gravadas                       # noqa: PLC0415
    biblioteca, colecao = _configurado(ctx)
    destino = ctx.config.caminho("dados.zotero")
    doc = le_copia(destino)
    if (doc["biblioteca"], doc["colecao"]) != (biblioteca, colecao):
        raise DadosInvalidos(f"a cópia {relativo(destino)} é de {doc['colecao']} em "
                             f"{doc['biblioteca']}, e [zotero] aponta {colecao} em "
                             f"{biblioteca} — rodar  {CMD_COPIAR}")
    if via_da_copia(doc) != cliente.via:
        raise DadosInvalidos(f"a cópia {relativo(destino)} foi lida pela via "
                             f"{via_da_copia(doc)}, e [zotero] acesso é {cliente.via}: as "
                             f"versões de item só valem na via que as leu, e o plano daria "
                             f"conflito em todo item. Manter a mesma via em toda a sessão, ou "
                             f"rodar  {CMD_COPIAR}  pela via {cliente.via}. Nada foi pedido ao "
                             f"Zotero")
    dois, retirar = confere_retirar(ctx, retirar, doc)
    respostas = respostas_gravadas(ctx, dois)
    acoes, fora = plano(doc, dois, respostas, retirar)
    print(f"Cópia lida: versão {doc['versao']}, lida em {doc['lida_em']}.")
    imprime_plano(acoes, fora, retirar)
    if not gravar:
        print("Sem --gravar: nada foi gravado no Zotero.")
        return
    if not acoes:
        print("Nada a gravar.")
        return
    alvo = ponto_de_restauracao(ctx, destino)
    print(f"Ponto de restauração: {relativo(alvo)}  ({_acesso(cliente)})")
    aplica(cliente, biblioteca, colecao, acoes)
    copia(ctx, cliente)


def cmd_completar(ctx, a):
    confere_retirar(ctx, a.retirar or ())
    completa(ctx, cliente(ctx), retirar=a.retirar or (), gravar=a.gravar)
    return Saida.OK
