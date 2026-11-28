"""Autoteste da cópia da coleção do Zotero, da consulta à OpenAlex e do complemento da
coleção, sem rede: um servidor simulado em memória faz o papel da API web do Zotero e da
OpenAlex. Os itens simulados são gerados das sementes lidas (DOI, título), não de literais.

Prova, cada caso exigindo a reprovação ou o comportamento esperado:
  - sem `ZOTERO_API_KEY`, `sementes copiar` sai com CONFIGURACAO;
  - a chave vai só no cabeçalho e não aparece inteira na saída nem nos arquivos gravados,
    nem com sucesso nem com erro — e o detector reprova quando a chave aparece;
  - a cópia traz biblioteca, coleção, versão e data e hora, e o relato entre duas cópias
    nomeia o acrescentado, o retirado e o campo alterado com os dois valores;
  - os campos extraídos do item (veículo de anais, DOI no campo extra);
  - a OpenAlex: 200 gravado pelo DOI, 404 sem gravação e a consulta segue, 429 interrompe
    as restantes sem nova tentativa; sem e-mail nem identificação;
  - o complemento: sem `--gravar` nada muda; resumo preenchido preservado; etiquetas
    preservadas; conflito de versão interrompe; `--retirar` tira só da coleção.
"""

import contextlib
import copy
import io
import json
import os
import pathlib
import tempfile
import types
import urllib.error
import urllib.parse

from .. import doi as _doi
from .. import metadados as OA
from .. import zotero as Z
from ..config import Configuracao
from ..erros import FonteExterna
from ..saida import Saida
from . import resultado

CHAVE_SINTETICA = "autotesteCHAVEsintetica0000wxyz"
CHAVE_LOCAL_SINTETICA = "autotesteLOCALsintetica000lmno"
SERVIDOR_SINTETICO = "autotesteSRV1"


def _credenciais_sinteticas():
    return CHAVE_LOCAL_SINTETICA, SERVIDOR_SINTETICO
LOCAL = urllib.parse.urlparse(Z.API_LOCAL).netloc
WEB = urllib.parse.urlparse(Z.API).netloc


# ------------------------------------------------------------------- servidor simulado
class _Resposta:
    def __init__(self, status, corpo=b"", cabecalhos=None):
        self.status = status
        self.headers = dict(cabecalhos or {})
        self._corpo = corpo

    def read(self):
        return self._corpo

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _erro(url, codigo, cabecalhos=None):
    return urllib.error.HTTPError(url, codigo, f"HTTP {codigo}", cabecalhos or {},
                                  io.BytesIO(b""))


class Servidor:
    """API web do Zotero e OpenAlex em memória. Registra cada pedido (método, URL,
    cabeçalhos, corpo). `falhas`: {nº do pedido (1, 2, …): (código, cabeçalhos)};
    `openalex`: {DOI normalizado: resposta (dict) ou código}."""

    def __init__(self, biblioteca, colecao, itens, openalex=None, falhas=None, crossref=None):
        self.biblioteca, self.colecao = biblioteca, colecao
        self.itens = {i["key"]: copy.deepcopy(i) for i in itens}
        self.versao = max([i["version"] for i in itens] or [1])
        self.openalex = openalex or {}
        self.crossref = crossref or {}
        self.falhas = dict(falhas or {})
        self.pedidos = []

    def __call__(self, req, timeout=None):
        url = req.full_url
        metodo = req.get_method()
        cab = {k.lower(): v for k, v in req.header_items()}
        corpo = json.loads(req.data.decode("utf-8")) if req.data else None
        self.pedidos.append((metodo, url, cab, corpo))
        n = len(self.pedidos)
        if n in self.falhas:
            codigo, h = self.falhas[n]
            raise _erro(url, codigo, h)
        partes = urllib.parse.urlparse(url)
        if partes.netloc == "api.openalex.org":
            doi = urllib.parse.unquote(partes.path.split("/works/doi:", 1)[1])
            r = self.openalex.get(_doi.normaliza(doi), 404)
            if isinstance(r, int):
                raise _erro(url, r)
            return _Resposta(200, json.dumps(r).encode("utf-8"))
        if partes.netloc == "api.crossref.org":
            doi = urllib.parse.unquote(partes.path.split("/works/", 1)[1])
            r = self.crossref.get(_doi.normaliza(doi), 404)
            if isinstance(r, int):
                raise _erro(url, r)
            return _Resposta(200, json.dumps(r).encode("utf-8"))
        caminho = partes.path.lstrip("/")
        if partes.netloc == LOCAL:
            if not caminho.startswith("api/"):
                raise _erro(url, 404)
            caminho = caminho[len("api/"):]
        if metodo == "GET" and caminho == (f"{self.biblioteca}/collections/{self.colecao}"
                                           f"/items/top"):
            q = urllib.parse.parse_qs(partes.query)
            inicio, limite = int(q["start"][0]), int(q["limit"][0])
            todos = [i for i in self.itens.values()
                     if self.colecao in i["data"].get("collections", [])]
            pagina = todos[inicio:inicio + limite]
            return _Resposta(200, json.dumps(pagina).encode("utf-8"),
                             {"Total-Results": str(len(todos)),
                              "Last-Modified-Version": str(self.versao)})
        if metodo == "PATCH" and caminho.startswith(f"{self.biblioteca}/items/"):
            chave = caminho.rsplit("/", 1)[1]
            item = self.itens[chave]
            if str(item["version"]) != cab.get("if-unmodified-since-version"):
                raise _erro(url, 412)
            self.versao += 1
            item["data"].update(corpo)
            item["version"] = item["data"]["version"] = self.versao
            return _Resposta(204)
        raise _erro(url, 400)

    def altera(self, chave, **campos):
        """Edição feita "na interface": muda o item e a versão."""
        self.versao += 1
        self.itens[chave]["data"].update(campos)
        self.itens[chave]["version"] = self.itens[chave]["data"]["version"] = self.versao


def item_sintetico(k, doi, titulo, colecao, tipo="journalArticle", **extra):
    chave = f"AUTO{k:04d}"
    dado = {"key": chave, "version": k + 1, "itemType": tipo, "title": titulo,
            "creators": [{"creatorType": "author", "lastName": f"Autor{k}",
                          "firstName": "A."}],
            "DOI": doi, "abstractNote": "", "tags": [], "collections": [colecao],
            "publicationTitle": f"Periódico {k}", "volume": "", "issue": "", "pages": "",
            "extra": ""}
    dado.update(extra)
    return {"key": chave, "version": k + 1, "meta": {"parsedDate": f"{2000 + k}"},
            "data": dado}


def vazou(chave, *textos):
    """A chave inteira aparece em algum dos textos."""
    return any(chave in t for t in textos)


# -------------------------------------------------------------------------- casos
def casos(ctx, g):
    sementes = [e for e in ctx.protocolo()["sementes"] if e.get("doi")]
    if len(sementes) < 5:
        g.nao_executa("menos de cinco sementes com DOI: sem como gerar os itens simulados")
        return
    biblioteca, colecao = ctx.config.valor("zotero.biblioteca"), ctx.config.valor(
        "zotero.colecao")
    itens = [item_sintetico(k, e["doi"], e["titulo"], colecao)
             for k, e in enumerate(sementes)]
    with tempfile.TemporaryDirectory() as tmp:
        dado = copy.deepcopy(ctx.config.dado)
        dado["dados"]["zotero"] = str(pathlib.Path(tmp) / "zotero.json")
        dado["dados"]["evidencia"] = str(pathlib.Path(tmp) / "evidencia")
        # Os casos da chave são da via web, qualquer que seja a via do config.toml.
        dado["zotero"]["acesso"] = "web"
        # A leitura do protocolo junta as sementes à cópia real, em memória; a cópia que os
        # comandos gravam e leem é a do diretório temporário.
        cx = ctx.com_config(Configuracao(dado, ctx.config.arquivo)).com_zotero(ctx.zotero)
        _chave(cx, g, tmp, biblioteca, colecao, itens)
        _copia(cx, g, biblioteca, colecao, itens)
        _campos(g, colecao)
        _openalex(cx, g, sementes)
    with tempfile.TemporaryDirectory() as tmp:
        dado = copy.deepcopy(ctx.config.dado)
        dado["dados"]["zotero"] = str(pathlib.Path(tmp) / "zotero.json")
        dado["dados"]["evidencia"] = str(pathlib.Path(tmp) / "evidencia")
        # A leitura do protocolo junta as sementes à cópia real, em memória; a cópia que os
        # comandos gravam e leem é a do diretório temporário.
        cx = ctx.com_config(Configuracao(dado, ctx.config.arquivo)).com_zotero(ctx.zotero)
        _completar(cx, g, biblioteca, colecao, sementes)
    with tempfile.TemporaryDirectory() as tmp:
        _vias(ctx, g, tmp, biblioteca, colecao, sementes)
    _copia_corrente(ctx, g)
    _colecoes(g, biblioteca)
    _colecao_das_buscas(ctx, g)
    with tempfile.TemporaryDirectory() as tmp:
        _obtencao(g, pathlib.Path(tmp))


class ServidorColecoes:
    """Coleções de uma biblioteca em memória: {chave: (nome, mãe)}. Lista as filhas
    paginadas (duas por página, para exercitar a paginação) e cria por POST."""

    def __init__(self, biblioteca, colecoes):
        self.biblioteca = biblioteca
        self.colecoes = dict(colecoes)
        self.pedidos = []

    def __call__(self, req, timeout=None):
        url, metodo = req.full_url, req.get_method()
        corpo = json.loads(req.data.decode("utf-8")) if req.data else None
        self.pedidos.append((metodo, url, {}, corpo))
        partes = urllib.parse.urlparse(url)
        caminho = partes.path.lstrip("/")
        if partes.netloc == LOCAL:
            caminho = caminho[len("api/"):]
        prefixo = f"{self.biblioteca}/collections"
        topo = caminho == f"{prefixo}/top"
        if metodo == "GET" and (topo or caminho.startswith(prefixo + "/")
                                and caminho.endswith("/collections")):
            mae = None if topo else caminho[len(prefixo) + 1:-len("/collections")]
            q = urllib.parse.parse_qs(partes.query)
            inicio = int(q["start"][0])
            filhas = [{"key": k, "data": {"key": k, "name": n, "parentCollection": m}}
                      for k, (n, m) in self.colecoes.items() if m == mae]
            return _Resposta(200, json.dumps(filhas[inicio:inicio + 2]).encode("utf-8"),
                             {"Total-Results": str(len(filhas))})
        if metodo == "POST" and caminho == prefixo:
            chave = f"NOVA{len(self.colecoes):04d}"
            self.colecoes[chave] = (corpo[0]["name"], corpo[0].get("parentCollection"))
            return _Resposta(200, json.dumps({"successful": {"0": {"key": chave}},
                                              "success": {"0": chave}, "unchanged": {},
                                              "failed": {}}).encode("utf-8"))
        raise _erro(url, 400)


def _colecoes(g, biblioteca):
    """Localização pelo nome, ausência na leitura sem criação, criação só por `garante`,
    homônimas e identificador repetido reprovando com DADOS."""
    mae = "BUSCAS00"
    base = {"WOS00001": ("wos", mae), "SCO00001": ("scopus", mae),
            "ERI00001": ("eric", mae), "EXE00001": ("3f9a0c1d2e7b wos EB4 2026-11-25",
                                                    "WOS00001"),
            "EXE00002": ("aaaaaaaaaaaa wos EB2 2026-11-25", "WOS00001")}
    srv = ServidorColecoes(biblioteca, base)
    cli = Z.Cliente("local", None, srv, _credenciais_sinteticas)
    cod, msgs = resultado(lambda: Z.subcolecao(cli, biblioteca, mae, "scopus"))
    g.testa("coleção da base localizada pelo nome, com a lista paginada",
            Z.subcolecao(cli, biblioteca, mae, "scopus") == "SCO00001"
            and Z.subcolecao(cli, biblioteca, mae, "eric") == "ERI00001", f"{msgs[:1]}")
    g.testa("coleção da execução localizada pelo identificador no início do nome",
            Z.subcolecao(cli, biblioteca, "WOS00001", "", "3f9a0c1d2e7b") == "EXE00001")
    n = len(srv.colecoes)
    cod, msgs = resultado(lambda: Z.subcolecao(cli, biblioteca, mae, "brapci"))
    g.testa("reprovou (DADOS): subcoleção ausente na leitura, nomeando a base e a mãe, e nada "
            "é criado",
            cod == Saida.DADOS and len(srv.colecoes) == n
            and not any(m == "POST" for m, _, _, _ in srv.pedidos)
            and any("brapci" in m and mae in m for m in msgs), f"{cod.name} {msgs[:1]}")
    criada = Z.garante(cli, biblioteca, mae, "brapci")
    g.testa("`garante` cria a ausente dentro da mãe e devolve a chave; na segunda chamada, "
            "localiza sem criar",
            srv.colecoes.get(criada) == ("brapci", mae)
            and Z.garante(cli, biblioteca, mae, "brapci") == criada
            and sum(1 for m, _, _, _ in srv.pedidos if m == "POST") == 1, f"{criada}")
    srv.colecoes["WOS00002"] = ("wos", mae)
    cod, msgs = resultado(lambda: Z.subcolecao(cli, biblioteca, mae, "wos"))
    g.testa("reprovou (DADOS): duas subcoleções `wos`, nomeando as duas chaves",
            cod == Saida.DADOS and any("WOS00001" in m and "WOS00002" in m for m in msgs),
            f"{cod.name} {msgs[:1]}")
    cod, msgs = resultado(lambda: Z.garante(cli, biblioteca, mae, "wos"))
    g.testa("reprovou (DADOS): homônimas também em `garante`, sem criar terceira",
            cod == Saida.DADOS and sum(1 for k, (nm, m) in srv.colecoes.items()
                                       if nm == "wos" and m == mae) == 2, f"{cod.name}")
    srv.colecoes["EXE00003"] = ("3f9a0c1d2e7b wos EB4 2026-11-26", "WOS00001")
    cod, msgs = resultado(lambda: Z.subcolecao(cli, biblioteca, "WOS00001", "",
                                               "3f9a0c1d2e7b"))
    g.testa("reprovou (DADOS): duas execuções com o mesmo identificador no início do nome",
            cod == Saida.DADOS and any("EXE00001" in m and "EXE00003" in m for m in msgs),
            f"{cod.name} {msgs[:1]}")
    g.testa("identificador que é só prefixo de outro não casa",
            Z.localiza([("K1", "3f9a0c1d2e7bX wos")], "", "3f9a0c1d2e7b") is None)


def _contexto(ctx, tmp, via):
    dado = copy.deepcopy(ctx.config.dado)
    dado["dados"]["zotero"] = str(pathlib.Path(tmp) / f"zotero_{via}.json")
    dado["dados"]["evidencia"] = str(pathlib.Path(tmp) / f"evidencia_{via}")
    dado["zotero"]["acesso"] = via
    return ctx.com_config(Configuracao(dado, ctx.config.arquivo)).com_zotero(ctx.zotero)


def _hosts(srv):
    return {urllib.parse.urlparse(u).netloc for _, u, _, _ in srv.pedidos}


def _vias(ctx, g, tmp, biblioteca, colecao, sementes):
    """As duas vias com o mesmo cliente: base de endereço, chave só na web, mensagens que
    nomeiam a via, Zotero local fechado e escrita recusada sem troca de via."""
    itens = [item_sintetico(k, e["doi"], e["titulo"], colecao)
             for k, e in enumerate(sementes)]
    web, local = _contexto(ctx, tmp, "web"), _contexto(ctx, tmp, "local")
    # Armadilha: um .env com a chave e fora do .gitignore. Lê-lo é CONFIGURACAO; a via local
    # não pode lê-lo.
    pasta = pathlib.Path(tmp) / "raiz_sem_gitignore"
    pasta.mkdir()
    env = pasta / ".env"
    env.write_text(f"{Z.VARIAVEL_CHAVE}={CHAVE_SINTETICA}\n", encoding="utf-8")
    srv = Servidor(biblioteca, colecao, itens)
    with _variavel(None), _arquivo_chave(env):
        cod, msgs, _ = _calado(lambda: Z.cliente(web, srv))
        g.testa("reprovou (CONFIGURACAO): via web lê a chave (aqui, do .env fora do "
                ".gitignore)", cod == Saida.CONFIGURACAO, f"{cod.name} {msgs[:1]}")
        cod, msgs, saida = _calado(lambda: Z.copia(local, Z.cliente(local, srv)))
    doc = json.loads(local.config.caminho("dados.zotero").read_text(encoding="utf-8")) \
        if local.config.caminho("dados.zotero").exists() else {}
    g.testa("via local sem chave: `sementes copiar` não sai com CONFIGURACAO e não lê o .env",
            cod == Saida.OK, f"{cod.name} {msgs[:1]}")
    g.testa("via local: todos os pedidos ao Zotero da máquina, sem chave no cabeçalho, nenhum "
            "à API web",
            srv.pedidos and _hosts(srv) == {LOCAL}
            and not any("zotero-api-key" in c for _, _, c, _ in srv.pedidos), f"{_hosts(srv)}")
    g.testa("via local: a cópia gravada registra a via `local`", doc.get("via") == "local",
            f"{doc.get('via')!r}")
    srv_w = Servidor(biblioteca, colecao, itens)
    with _variavel(CHAVE_SINTETICA):
        cod_w, msgs_w, _ = _calado(lambda: Z.copia(web, Z.cliente(web, srv_w)))
    g.testa("via web: pedidos à API web, com a chave, e a cópia registra a via `web`",
            cod_w == Saida.OK and _hosts(srv_w) == {WEB}
            and all(c.get("zotero-api-key") == CHAVE_SINTETICA for _, _, c, _ in srv_w.pedidos)
            and Z.le_copia(web.config.caminho("dados.zotero")).get("via") == "web",
            f"{cod_w.name} {_hosts(srv_w)}")
    # Diferença entre cópia web anterior e cópia local nova: os mesmos campos.
    destino = local.config.caminho("dados.zotero")
    destino.write_text(web.config.caminho("dados.zotero").read_text(encoding="utf-8"),
                       encoding="utf-8")
    alvo = itens[0]
    srv.altera(alvo["key"], title=alvo["data"]["title"] + " (via local)")
    cod, msgs, saida = _calado(lambda: Z.copia(local, Z.Cliente("local", None, srv, _credenciais_sinteticas)))
    g.testa("cópia local depois de cópia web: a diferença se relata pelos mesmos campos, com "
            "o aviso da troca de via",
            cod == Saida.OK and "via web" in saida and "AVISO" in saida
            and "mesma via" in saida
            and any(_doi.normaliza(alvo["data"]["DOI"]) in l and "titulo" in l
                    for l in saida.splitlines()), saida[-200:])

    # Zotero local fechado: erro de conexão, mensagem própria, nenhum pedido à web.
    tentados = []

    def fechado(req, timeout=None):
        tentados.append(req.full_url)
        raise urllib.error.URLError(ConnectionRefusedError(111, "Connection refused"))
    cod, msgs, _ = _calado(lambda: Z.copia(local, Z.Cliente("local", None, fechado, _credenciais_sinteticas)))
    g.testa("Zotero local fechado: FONTE_EXTERNA, nomeia a via local e diz que o Zotero tem "
            "de estar aberto com o acesso local habilitado; nenhum pedido à web",
            cod == Saida.FONTE_EXTERNA and len(tentados) == 1
            and urllib.parse.urlparse(tentados[0]).netloc == LOCAL
            and any("via local" in m and "aberto" in m and "acesso local" in m for m in msgs),
            f"{cod.name} {tentados} {msgs[:1]}")
    # Pedido de espera na via local também interrompe, sem novo pedido.
    srv_e = Servidor(biblioteca, colecao, itens)
    espera_srv = _ComEspera(srv_e)
    cod, msgs, _ = _calado(lambda: Z.copia(local, Z.Cliente("local", None, espera_srv, _credenciais_sinteticas)))
    g.testa("pedido de espera na via local: FONTE_EXTERNA sem novo pedido",
            cod == Saida.FONTE_EXTERNA and len(srv_e.pedidos) == 1
            and any("via local" in m for m in msgs), f"{cod.name} {len(srv_e.pedidos)}")
    _escrita_local(local, g, biblioteca, colecao, sementes)


class _ComEspera:
    """Responde como o servidor, com `Backoff` na resposta."""

    def __init__(self, srv):
        self.srv = srv

    def __call__(self, req, timeout=None):
        r = self.srv(req, timeout)
        r.headers["Backoff"] = "30"
        return r


class _Silenciador(Z.Cliente):
    """Mutação: o cliente que engole a recusa de escrita. Existe só para provar que o caso
    da recusa reprova quando ela é silenciada."""

    def pedido(self, metodo, caminho, corpo=None, cabecalhos=None):
        try:
            return super().pedido(metodo, caminho, corpo, cabecalhos)
        except FonteExterna:
            if metodo in Z.METODOS_ESCRITA:
                return 204, {}, ""
            raise


def _escrita_local(local, g, biblioteca, colecao, sementes):
    """A via local recusa a escrita: FONTE_EXTERNA, indicação da via web, um só PATCH e
    zero pedidos à API web. O mesmo cenário com a recusa silenciada reprova o caso."""
    dois = [_doi.normaliza(e["doi"]) for e in sementes]
    resp = {"abstract_inverted_index": {"resumo": [0]}, "keywords": [{"display_name": "X"}]}
    pasta = OA.pasta(local)
    pasta.mkdir(parents=True, exist_ok=True)
    for d in dois[:2]:
        (pasta / _doi.nome_arquivo(d)).write_text(json.dumps(resp), encoding="utf-8")

    def cenario(classe, credenciais=_credenciais_sinteticas):
        srv = Servidor(biblioteca, colecao, [item_sintetico(k, e["doi"], e["titulo"], colecao)
                                            for k, e in enumerate(sementes)])
        cli = classe("local", None, srv, credenciais)
        _calado(lambda: Z.copia(local, cli))
        srv.falhas = {len(srv.pedidos) + 1: (501, {})}
        cod, msgs, _ = _calado(lambda: Z.completa(local, cli, gravar=True))
        return cod, msgs, srv

    def recusa_relatada(cod, msgs, srv):
        escritas = [x for x in srv.pedidos if x[0] in Z.METODOS_ESCRITA]
        return (cod == Saida.FONTE_EXTERNA and len(escritas) == 1
                and _hosts(srv) == {LOCAL}
                and any('acesso = "web"' in m and "via local" in m
                        and Z.VARIAVEL_CHAVE_LOCAL in m for m in msgs))

    cod, msgs, srv = cenario(Z.Cliente)
    g.testa("via local recusa a escrita: FONTE_EXTERNA, indica `acesso = \"web\"`, um só "
            "pedido de escrita e zero pedidos à API web",
            recusa_relatada(cod, msgs, srv), f"{cod.name} {_hosts(srv)} {msgs[:1]}")
    leitura = [c for m, _, c, _ in srv.pedidos if m == "GET"]
    escrita = [c for m, _, c, _ in srv.pedidos if m in Z.METODOS_ESCRITA]
    g.testa("via local: a leitura vai sem chave nem identificador do servidor; a escrita leva "
            "a chave local e o `Zotero-Server-ID`",
            leitura and all("zotero-api-key" not in c and "zotero-server-id" not in c
                            for c in leitura)
            and escrita and all(c.get("zotero-api-key") == CHAVE_LOCAL_SINTETICA
                                and c.get("zotero-server-id") == SERVIDOR_SINTETICO
                                for c in escrita), f"{len(leitura)} GET, {len(escrita)} escrita")
    g.testa("via local: a chave local não aparece nas mensagens",
            not vazou(CHAVE_LOCAL_SINTETICA, *msgs), "a chave local vazou")
    cod, msgs, srv = cenario(_Silenciador)
    g.testa("o caso da recusa local reprova quando a recusa é silenciada",
            not recusa_relatada(cod, msgs, srv), f"{cod.name}")
    # Mesma via em toda a sessão: cópia lida por outra via é recusada antes de qualquer
    # pedido; a cópia sem `via` conta como web.
    destino = local.config.caminho("dados.zotero")
    doc = json.loads(destino.read_text(encoding="utf-8"))
    for rotulo, via in (("lida pela via web", "web"), ("sem o campo `via`", None)):
        outra = dict(doc)
        outra.pop("via", None)
        if via:
            outra["via"] = via
        destino.write_text(json.dumps(outra), encoding="utf-8")
        srv = Servidor(biblioteca, colecao, [])
        cod, msgs, _ = _calado(lambda: Z.completa(
            local, Z.Cliente("local", None, srv, _credenciais_sinteticas), gravar=True))
        g.testa(f"reprovou (DADOS): `completar` pela via local com a cópia {rotulo}, sem "
                f"pedido ao Zotero",
                cod == Saida.DADOS and not srv.pedidos
                and any("via web" in m and "mesma via" in m for m in msgs),
                f"{cod.name} {msgs[:1]}")
    outra = dict(doc, via="local")
    destino.write_text(json.dumps(outra), encoding="utf-8")
    cod, msgs, _ = _calado(lambda: Z.completa(
        local, Z.Cliente("local", None, Servidor(biblioteca, colecao, []),
                         _credenciais_sinteticas)))
    g.testa("controle: `completar` pela via local com a cópia lida pela via local passa a "
            "conferência da via", not any("mesma via" in m for m in msgs),
            f"{cod.name} {msgs[:1]}")
    # Sem credenciais locais: CONFIGURACAO antes de qualquer pedido de escrita, nomeando as
    # duas variáveis. As credenciais vêm de um .env vazio e listado, não do .env da raiz.
    pasta = local.config.caminho("dados.evidencia") / "sem_credenciais_locais"
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / ".gitignore").write_text(".env\n", encoding="utf-8")
    vazio = pasta / ".env"
    vazio.write_text("# sem credenciais\n", encoding="utf-8")
    antes = {v: os.environ.pop(v, None) for v in (Z.VARIAVEL_CHAVE_LOCAL, Z.VARIAVEL_SERVIDOR)}
    try:
        cod, msgs, srv = cenario(Z.Cliente, lambda: Z.credenciais_locais(vazio))
    finally:
        for v, x in antes.items():
            if x is not None:
                os.environ[v] = x
    g.testa("reprovou (CONFIGURACAO): escrita local sem chave local nem identificador do "
            "servidor, nomeando os dois, sem pedido de escrita",
            cod == Saida.CONFIGURACAO
            and not any(m in Z.METODOS_ESCRITA for m, _, _, _ in srv.pedidos)
            and any(Z.VARIAVEL_CHAVE_LOCAL in m and Z.VARIAVEL_SERVIDOR in m for m in msgs),
            f"{cod.name} {msgs[:1]}")


def _copia_corrente(ctx, g):
    """A cópia corrente, gravada antes do registro da via, continua legível."""
    caminho = ctx.config.caminho("dados.zotero")
    if not caminho.exists():
        g.nao_executa(f"cópia {caminho.name} ausente: sem como conferir a leitura da cópia "
                      f"gravada antes do registro da via", quantos=1)
        return
    cod, msgs = resultado(lambda: Z.le_copia(caminho))
    g.testa("a cópia corrente (com ou sem o campo `via`) continua legível por `le_copia`",
            cod == Saida.OK, f"{cod.name} {msgs[:1]}")


@contextlib.contextmanager
def _variavel(valor):
    antes = os.environ.get(Z.VARIAVEL_CHAVE)
    if valor is None:
        os.environ.pop(Z.VARIAVEL_CHAVE, None)
    else:
        os.environ[Z.VARIAVEL_CHAVE] = valor
    try:
        yield
    finally:
        if antes is None:
            os.environ.pop(Z.VARIAVEL_CHAVE, None)
        else:
            os.environ[Z.VARIAVEL_CHAVE] = antes


def _calado(funcao):
    """(código, mensagens, saída impressa)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cod, msgs = resultado(funcao)
    return cod, msgs, buf.getvalue()


@contextlib.contextmanager
def _arquivo_chave(caminho):
    antes = Z.ARQUIVO_CHAVE
    Z.ARQUIVO_CHAVE = pathlib.Path(caminho)
    try:
        yield
    finally:
        Z.ARQUIVO_CHAVE = antes


def _chave(cx, g, tmp, biblioteca, colecao, itens):
    pasta = pathlib.Path(tmp) / "raiz_simulada"
    pasta.mkdir()
    env = pasta / ".env"
    with _variavel(None), _arquivo_chave(env):
        cod, msgs, _ = _calado(lambda: Z.cmd_copiar(cx))
        g.testa("sem ZOTERO_API_KEY nem .env, `sementes copiar` sai com CONFIGURACAO",
                cod == Saida.CONFIGURACAO and any(Z.VARIAVEL_CHAVE in m for m in msgs),
                f"{cod.name} {msgs[:1]}")
        env.write_text(f"# comentário\n{Z.VARIAVEL_CHAVE}={CHAVE_SINTETICA}\n",
                       encoding="utf-8")
        cod, msgs = resultado(Z.chave_api)
        g.testa(".env fora do .gitignore é recusado (CONFIGURACAO)",
                cod == Saida.CONFIGURACAO and any(".gitignore" in m for m in msgs)
                and not vazou(CHAVE_SINTETICA, *msgs), f"{cod.name} {msgs[:1]}")
        (pasta / ".gitignore").write_text("*.pyc\n.env\n", encoding="utf-8")
        lida = Z.chave_api()
        g.testa("sem a variável, a chave vem do .env listado no .gitignore",
                lida == CHAVE_SINTETICA, "chave não lida")
        env.unlink()

    srv = Servidor(biblioteca, colecao, itens)
    with _variavel(CHAVE_SINTETICA):
        cod, msgs, saida = _calado(lambda: Z.copia(cx, Z.Cliente("web", Z.chave_api(), srv)))
        erro = Servidor(biblioteca, colecao, itens, falhas={1: (403, {})})
        cod_e, msgs_e, saida_e = _calado(
            lambda: Z.copia(cx, Z.Cliente("web", Z.chave_api(), erro)))
    gravados = [p.read_text(encoding="utf-8", errors="replace")
                for p in pathlib.Path(tmp).rglob("*") if p.is_file()]
    g.testa("chave da API só no cabeçalho, nunca no endereço",
            srv.pedidos and all(c.get("zotero-api-key") == CHAVE_SINTETICA
                                and CHAVE_SINTETICA not in u for _, u, c, _ in srv.pedidos),
            f"{[u for _, u, _, _ in srv.pedidos][:1]}")
    g.testa("chave não impressa nem gravada (sucesso e erro), com os quatro últimos "
            "caracteres no relato",
            cod == Saida.OK and cod_e == Saida.FONTE_EXTERNA and gravados
            and not vazou(CHAVE_SINTETICA, saida, saida_e, *msgs, *msgs_e, *gravados)
            and Z.mascara(CHAVE_SINTETICA) in saida,
            f"{cod.name}/{cod_e.name}")
    # O detector reprova quando a chave aparece: sem isso, o caso acima nada provaria.
    g.testa("o detector de vazamento reprova saída que contém a chave",
            vazou(CHAVE_SINTETICA, saida + CHAVE_SINTETICA), "detector não achou a chave")
    cod, msgs = resultado(lambda: Z.grava_json(pathlib.Path(tmp) / "vaza.json",
                                               {"x": CHAVE_SINTETICA}, CHAVE_SINTETICA))
    g.testa("gravação com a chave no conteúdo é recusada, sem arquivo",
            cod == Saida.FONTE_EXTERNA and not (pathlib.Path(tmp) / "vaza.json").exists(),
            f"{cod.name}")


def _copia(cx, g, biblioteca, colecao, itens):
    destino = cx.config.caminho("dados.zotero")
    if destino.exists():
        destino.unlink()
    srv = Servidor(biblioteca, colecao, itens)
    cliente = Z.Cliente("web", CHAVE_SINTETICA, srv)
    cod, msgs, saida = _calado(lambda: Z.copia(cx, cliente))
    doc = json.loads(destino.read_text(encoding="utf-8")) if destino.exists() else {}
    g.testa("primeira cópia: biblioteca, coleção, versão, data e hora e todos os itens "
            "como acrescentados",
            cod == Saida.OK and doc.get("biblioteca") == biblioteca
            and doc.get("colecao") == colecao and doc.get("versao") == srv.versao
            and doc.get("lida_em") and len(doc.get("itens", [])) == len(itens)
            and saida.count("+ acrescentado") == len(itens), f"{cod.name} {msgs[:1]}")
    alvo, retirado = itens[0], itens[1]
    novo_titulo = alvo["data"]["title"] + " (alterado no autoteste)"
    srv.altera(alvo["key"], title=novo_titulo)
    srv.altera(retirado["key"], collections=[])
    srv.itens["AUTONOVO"] = item_sintetico(900, "10.9999/autoteste.novo", "Item novo",
                                           colecao)
    srv.itens["AUTONOVO"]["key"] = "AUTONOVO"
    cod, msgs, saida = _calado(lambda: Z.copia(cx, cliente))
    doi_alvo = _doi.normaliza(alvo["data"]["DOI"])
    g.testa("relato entre cópias nomeia o DOI, o campo `titulo` e os dois valores",
            cod == Saida.OK and any(doi_alvo in l and "titulo" in l and novo_titulo[:40] in l
                                    and alvo["data"]["title"][:40] in l
                                    for l in saida.splitlines()), f"{cod.name}")
    g.testa("relato entre cópias nomeia o item retirado e o acrescentado",
            "- retirado: " + _doi.normaliza(retirado["data"]["DOI"]) in saida
            and "+ acrescentado: 10.9999/autoteste.novo" in saida, saida[-200:])


def _campos(g, colecao):
    anais = Z.campos(item_sintetico(1, "", "Trabalho", colecao, tipo="conferencePaper",
                                    proceedingsTitle="Anais do Autoteste",
                                    extra="DOI: 10.5771/9783956507762-484"))
    g.testa("trabalho em anais: veículo é o título dos anais", anais["veiculo"] ==
            "Anais do Autoteste", f"{anais['veiculo']!r}")
    g.testa("DOI no campo extra é lido", anais["doi"] == "10.5771/9783956507762-484",
            f"{anais['doi']!r}")
    g.testa("DOI com caixa e prefixo de URL normalizado",
            _doi.normaliza("https://doi.org/10.1111/EXSY.12246") == "10.1111/exsy.12246")


def _openalex(cx, g, sementes):
    resp = {"abstract_inverted_index": {"ontologia": [1], "uma": [0]},
            "keywords": [{"display_name": "Ontologia"}, {"display_name": "Ensino"}]}
    sem_resumo = {"abstract_inverted_index": None, "keywords": []}
    dois = [_doi.normaliza(e["doi"]) for e in sementes]
    oa = {dois[0]: resp, dois[2]: resp, dois[3]: resp, dois[4]: 429}
    if len(dois) > 5:
        oa[dois[5]] = resp
    srv = Servidor("", "", [], openalex=oa)
    cod, msgs, _ = _calado(lambda: OA.metadados(cx, abrir=srv, pausa=0))
    pasta = OA.pasta(cx)
    nomes = {p.name for p in pasta.glob("*.json")} if pasta.exists() else set()
    esperados = {_doi.nome_arquivo(d) for d in (dois[0], dois[2], dois[3])}
    g.testa("OpenAlex: 429 na quinta consulta interrompe as restantes, sem nova tentativa",
            cod == Saida.FONTE_EXTERNA and len(srv.pedidos) == 5
            and any("429" in m and sementes[4]["id"] in m for m in msgs),
            f"{cod.name} {len(srv.pedidos)} pedidos {msgs[:1]}")
    g.testa("OpenAlex: erro não aciona o Crossref (nenhuma consulta a outra fonte)",
            not any("crossref" in u for _, u, _, _ in srv.pedidos))
    g.testa("OpenAlex: respostas 200 gravadas pelo DOI, sem resposta para o 404",
            nomes == esperados, f"{sorted(nomes)}")
    g.testa("OpenAlex: 404 deixa o marcador `.404` com a data e hora",
            (pasta / OA.marcador(_doi.nome_arquivo(dois[1]))).exists())
    gravada = json.loads((pasta / _doi.nome_arquivo(dois[0])).read_text()) \
        if (pasta / _doi.nome_arquivo(dois[0])).exists() else {}
    g.testa("OpenAlex: resumo reconstruído e palavras-chave lidas",
            OA.resumo_openalex(gravada) == "uma ontologia"
            and OA.palavras_chave_openalex(gravada) == ["Ontologia", "Ensino"])
    g.testa("OpenAlex: sem e-mail nem identificação no pedido",
            all("mailto" not in u and "@" not in u and "from" not in c
                and "@" not in c.get("user-agent", "") for _, u, c, _ in srv.pedidos))
    d = cx.protocolo()
    linhas = OA.pendencias(cx, d)
    alvo = sementes[4]["id"]
    g.testa(f"pendência: consulta interrompida ({alvo}) é \"não consultada ou "
            f"interrompida\", não \"sem registro\" nem \"sem resumo\"",
            any(f"semente {alvo} " in l and "interrompida" in l and "sem registro" not in l
                and "resumo ausente" not in l for l in linhas), f"{linhas[:2]}")
    g.testa(f"pendência: 404 ({sementes[1]['id']}) é \"sem registro na OpenAlex\"",
            any(f"semente {sementes[1]['id']} " in l and "sem registro na OpenAlex" in l
                for l in linhas), f"{linhas[:2]}")

    # Segunda execução: só os DOIs sem resultado registrado.
    srv2 = Servidor("", "", [], openalex={x: sem_resumo for x in dois})
    cod, msgs, _ = _calado(lambda: OA.metadados(cx, abrir=srv2, pausa=0))
    g.testa(f"segunda execução consulta só as pendentes ({len(dois) - 4} de {len(dois)})",
            cod == Saida.OK and len(srv2.pedidos) == len(dois) - 4
            and all(dois[k] not in urllib.parse.unquote(u) for k in range(4)
                    for _, u, _, _ in srv2.pedidos), f"{cod.name} {len(srv2.pedidos)}")

    # Crossref: só as sem resumo em fonte nenhuma (404 ou resposta sem resumo).
    jats = {"message": {"abstract": "<jats:title>Abstract</jats:title><jats:p>Texto do "
                                    "resumo &amp; mais.</jats:p>"}}
    srv3 = Servidor("", "", [], crossref={dois[1]: jats})
    cod, msgs, _ = _calado(lambda: OA.metadados(cx, OA.CROSSREF, abrir=srv3, pausa=0))
    consultados = {_doi.normaliza(urllib.parse.unquote(u.split("/works/", 1)[1]))
                   for _, u, _, _ in srv3.pedidos}
    elegiveis = {dois[1]} | set(dois[4:])
    g.testa("Crossref: consulta só as sementes sem resumo na OpenAlex nem no Zotero",
            cod == Saida.OK and consultados == elegiveis
            and all("api.crossref.org" in u for _, u, _, _ in srv3.pedidos),
            f"{cod.name} {sorted(consultados)}")
    cr = json.loads((OA.pasta(cx, OA.CROSSREF) / _doi.nome_arquivo(dois[1])).read_text())
    g.testa("Crossref: resumo JATS reconstruído sem marcação nem título",
            OA.resumo_crossref(cr) == "Texto do resumo & mais.", OA.resumo_crossref(cr))
    linhas = OA.pendencias(cx, d)
    da_semente = [l for l in linhas if f"semente {sementes[1]['id']} " in l]
    g.testa("pendência: com o resumo do Crossref, a semente não fica sem resumo e o resumo "
            "vai ao Zotero pelo `completar`",
            not any("todas as fontes" in l or "ausente na OpenAlex" in l for l in da_semente)
            and any("disponível na fonte" in l for l in da_semente), f"{da_semente}")
    g.testa("pendência: sem resumo em todas as fontes, fica para o pesquisador no Zotero",
            any(f"semente {alvo} " in l and "resumo ausente em todas as fontes" in l
                and "pesquisador" in l for l in linhas), f"{linhas[:2]}")
    g.testa("completar usa o resumo do Crossref na falta do da OpenAlex",
            OA.respostas_gravadas(cx, [dois[1]]).get(dois[1], ("",))[0]
            == "Texto do resumo & mais.")


def _completar(cx, g, biblioteca, colecao, sementes):
    dois = [_doi.normaliza(e["doi"]) for e in sementes]
    tags15 = [{"tag": f"etiqueta {k}"} for k in range(13)] + [{"tag": "Ontologia"},
                                                              {"tag": "Ensino"}]
    itens = [item_sintetico(k, e["doi"], e["titulo"], colecao)
             for k, e in enumerate(sementes)]
    itens[0]["data"]["abstractNote"] = "Resumo preenchido à mão."
    itens[1]["data"]["tags"] = tags15
    fora = item_sintetico(800, "10.9999/autoteste.fora", "Fora do arquivo", colecao)
    itens.append(fora)
    resp = {"abstract_inverted_index": {"resumo": [1], "outro": [0]},
            "keywords": [{"display_name": x} for x in
                         ("Ontologia", "Ensino", "Currículo", "Didática", "Avaliação")]}
    pasta = OA.pasta(cx)
    pasta.mkdir(parents=True, exist_ok=True)
    for d in dois[:3]:
        (pasta / _doi.nome_arquivo(d)).write_text(json.dumps(resp), encoding="utf-8")

    srv = Servidor(biblioteca, colecao, itens)
    cliente = Z.Cliente("web", CHAVE_SINTETICA, srv)
    _calado(lambda: Z.copia(cx, cliente))
    versao = srv.versao
    n_pedidos = len(srv.pedidos)
    cod, msgs, saida = _calado(lambda: Z.completa(cx, cliente))
    g.testa("sem --gravar, nada muda no Zotero e o item fora do arquivo é relatado",
            cod == Saida.OK and len(srv.pedidos) == n_pedidos and srv.versao == versao
            and "10.9999/autoteste.fora" in saida, f"{cod.name} {msgs[:1]}")
    acoes, _ = Z.plano(Z.le_copia(cx.config.caminho("dados.zotero")), set(dois),
                       OA.respostas_gravadas(cx, dois))
    primeira = next((x for x in acoes if x["campos"]["doi"] == dois[0]), None)
    g.testa("resumo já preenchido fica fora do plano",
            primeira is not None and primeira["resumo"] is None, f"{primeira}")

    cod, msgs, saida = _calado(lambda: Z.completa(cx, cliente, gravar=True,
                                                  retirar=["10.9999/autoteste.fora"]))
    it0, it1 = srv.itens[itens[0]["key"]]["data"], srv.itens[itens[1]["key"]]["data"]
    g.testa("com --gravar: resumo preenchido preservado",
            cod == Saida.OK and it0["abstractNote"] == "Resumo preenchido à mão.",
            f"{cod.name} {msgs[:1]}")
    g.testa("com --gravar: 15 etiquetas + 5 palavras-chave (2 existentes) = 18 etiquetas, "
            "as novas automáticas",
            len(it1["tags"]) == 18 and all(t.get("type") == Z.ETIQUETA_AUTOMATICA
                                           for t in it1["tags"][15:]),
            f"{len(it1['tags'])}")
    sai = srv.itens[fora["key"]]["data"]
    g.testa("--retirar tira o item só da coleção; ele continua na biblioteca",
            colecao not in sai["collections"] and fora["key"] in srv.itens
            and not any(colecao in x.get("collections", [])
                        for x in Z.le_copia(cx.config.caminho("dados.zotero"))["itens"]
                        if x["key"] == fora["key"]), f"{sai['collections']}")
    restauracao = list((cx.config.caminho("dados.evidencia") / Z.SUBPASTA_RESTAURACAO)
                       .glob("*_antes_*.json"))
    g.testa("ponto de restauração guardado antes da primeira gravação", bool(restauracao))
    cod, msgs, _ = _calado(lambda: Z.completa(cx, cliente,
                                              retirar=["10.9999/autoteste.inexistente"]))
    g.testa("--retirar de DOI que nenhum item da cópia tem é recusado (USO)",
            cod == Saida.USO, f"{cod.name}")
    n_antes = len(srv.pedidos)
    cod, msgs, _ = _calado(lambda: Z.completa(cx, cliente, gravar=True,
                                              retirar=[dois[0]]))
    g.testa("reprovou (USO): --retirar de DOI de semente do arquivo, sem pedido ao Zotero",
            cod == Saida.USO and len(srv.pedidos) == n_antes
            and any("semente do arquivo" in m for m in msgs), f"{cod.name} {msgs[:1]}")
    # Sem chave, a recusa continua sendo USO: o `--retirar` se confere antes da chave.
    sem_env = cx.config.caminho("dados.evidencia") / "sem_chave" / ".env"
    with _variavel(None), _arquivo_chave(sem_env):
        cod, msgs, _ = _calado(lambda: Z.cmd_completar(
            cx, types.SimpleNamespace(retirar=[dois[0]], gravar=True)))
    g.testa("reprovou (USO): --retirar de DOI de semente do arquivo, mesmo sem a chave",
            cod == Saida.USO and any("semente do arquivo" in m for m in msgs),
            f"{cod.name} {msgs[:1]}")

    # Conflito: o item muda "na interface" depois da cópia; a gravação para nele.
    srv2 = Servidor(biblioteca, colecao, [item_sintetico(k, e["doi"], e["titulo"], colecao)
                                         for k, e in enumerate(sementes)])
    cliente2 = Z.Cliente("web", CHAVE_SINTETICA, srv2)
    _calado(lambda: Z.copia(cx, cliente2))
    srv2.altera(f"AUTO{1:04d}", title="mudou na interface")
    cod, msgs, _ = _calado(lambda: Z.completa(cx, cliente2, gravar=True))
    gravou_primeiro = bool(srv2.itens["AUTO0000"]["data"]["abstractNote"])
    pararam = [m for _, _, _, m in srv2.pedidos if m is not None]
    g.testa("conflito de versão interrompe: anteriores gravados, saída nomeia o DOI e pede "
            "`sementes copiar`",
            cod == Saida.FONTE_EXTERNA and gravou_primeiro and len(pararam) == 2
            and any(dois[1] in m and "sementes copiar" in m for m in msgs),
            f"{cod.name} {len(pararam)} {msgs[:1]}")
    # Limite de uso: 429 no primeiro PATCH interrompe sem nova tentativa.
    srv3 = Servidor(biblioteca, colecao, [item_sintetico(k, e["doi"], e["titulo"], colecao)
                                         for k, e in enumerate(sementes)])
    cliente3 = Z.Cliente("web", CHAVE_SINTETICA, srv3)
    _calado(lambda: Z.copia(cx, cliente3))
    srv3.falhas = {len(srv3.pedidos) + 1: (429, {"Retry-After": "30"})}
    cod, msgs, _ = _calado(lambda: Z.completa(cx, cliente3, gravar=True))
    patches = [x for x in srv3.pedidos if x[0] == "PATCH"]
    g.testa("limite de uso (429) interrompe a gravação sem nova tentativa",
            cod == Saida.FONTE_EXTERNA and len(patches) == 1
            and any("429" in m for m in msgs), f"{cod.name} {len(patches)}")


def _colecao_das_buscas(ctx, g):
    """A coleção das buscas é localizada pelo nome de `[zotero] search_collection` na raiz
    da biblioteca de `[zotero] library`, sem criar nada; homônimas na raiz reprovam."""
    biblioteca = "groups/6781444"
    dado = copy.deepcopy(ctx.config.dado)
    dado["zotero"].update(library=f"https://www.zotero.org/{biblioteca}/modelagem-educacional",
                          search_collection="buscas")
    cx = ctx.com_config(Configuracao(dado, ctx.config.arquivo))
    srv = ServidorColecoes(biblioteca, {"RAIZ0001": ("sementes", None),
                                        "RAIZ0002": ("buscas", None),
                                        "FILHA001": ("buscas", "RAIZ0001")})
    cli = Z.Cliente("local", None, srv, _credenciais_sinteticas)
    cod, msgs = resultado(lambda: Z.colecao_das_buscas(cx, cli))
    g.testa("coleção das buscas localizada pelo nome na raiz da biblioteca de `library` (a "
            "homônima dentro de outra coleção não conta)",
            cod == Saida.OK and Z.colecao_das_buscas(cx, cli) == (biblioteca, "RAIZ0002")
            and all(f"/{biblioteca}/collections/top" in u for _, u, _, _ in srv.pedidos),
            f"{cod.name} {msgs[:1]}")
    srv.colecoes.pop("RAIZ0002")
    cod, msgs = resultado(lambda: Z.colecao_das_buscas(cx, cli))
    g.testa("reprovou (DADOS): coleção das buscas ausente na raiz, nomeando o nome e a "
            "biblioteca, sem criar",
            cod == Saida.DADOS and any("'buscas'" in m and biblioteca in m for m in msgs)
            and not any(m == "POST" for m, _, _, _ in srv.pedidos), f"{cod.name} {msgs[:1]}")
    srv.colecoes.update({"RAIZ0003": ("buscas", None), "RAIZ0004": ("buscas", None)})
    cod, msgs = resultado(lambda: Z.colecao_das_buscas(cx, cli))
    g.testa("reprovou (DADOS): duas coleções `buscas` na raiz, nomeando as duas chaves",
            cod == Saida.DADOS and any("RAIZ0003" in m and "RAIZ0004" in m for m in msgs),
            f"{cod.name} {msgs[:1]}")
    criada = Z.garante(cli, biblioteca, None, "outra")
    g.testa("`garante` na raiz cria sem coleção-mãe",
            srv.colecoes.get(criada) == ("outra", None), f"{criada}")


class ServidorRIS:
    """Coleção de execução em memória, exportada em RIS por página (`limit`, `start`), com
    `Total-Results`. `falhas`: {nº do pedido: código}."""

    def __init__(self, biblioteca, colecao, registros, falhas=None):
        self.biblioteca, self.colecao, self.registros = biblioteca, colecao, registros
        self.falhas = dict(falhas or {})
        self.pedidos = []

    def __call__(self, req, timeout=None):
        url = req.full_url
        self.pedidos.append(("GET", url, {}, None))
        if len(self.pedidos) in self.falhas:
            raise _erro(url, self.falhas[len(self.pedidos)])
        partes = urllib.parse.urlparse(url)
        q = urllib.parse.parse_qs(partes.query)
        assert q["format"] == ["ris"]
        ini, lim = int(q["start"][0]), int(q["limit"][0])
        corpo = "".join(self.registros[ini:ini + lim])
        return _Resposta(200, corpo.encode("utf-8"),
                         {"Total-Results": str(len(self.registros))})


def _sem_numero(funcao, *a):
    """Chama `funcao` e descarta o número devolvido (resultado() o leria como código)."""
    funcao(*a)


def _obtencao(g, pasta):
    """`obtem_exportacao`: RIS paginado e legível pelo leitor das análises, com o número de
    registros servido; interrupção no meio deixa o anterior intacto, sem arquivo parcial;
    conteúdo com a chave não é gravado."""
    from ..busca.leitores import le_arquivo                       # noqa: PLC0415
    n = Z.POR_PAGINA + Z.POR_PAGINA // 2
    regs = [f"TY  - JOUR\nTI  - Registro sintetico {k}\nPY  - 2020\n"
            f"DO  - 10.0000/autoteste.obtencao.{k}\nER  - \n\n" for k in range(n)]
    destino = pasta / "wos" / "3f9a0c1d2e7b.ris"
    srv = ServidorRIS("groups/1", "EXEC0001", regs)
    cod, msgs = resultado(lambda: _sem_numero(Z.obtem_exportacao,
        Z.Cliente("local", None, srv, _credenciais_sinteticas), "groups/1", "EXEC0001", destino))
    lidos = le_arquivo(destino) if destino.exists() else []
    g.testa(f"obtenção: {n} registros em duas páginas, gravados e legíveis pelo leitor",
            cod == Saida.OK and len(srv.pedidos) == 2 and len(lidos) == n
            and lidos[-1]["doi"] == f"10.0000/autoteste.obtencao.{n - 1}",
            f"{cod.name} {len(srv.pedidos)} pedidos, {len(lidos)} lidos {msgs[:1]}")
    anterior = destino.read_text(encoding="utf-8")
    falha = ServidorRIS("groups/1", "EXEC0001", regs[:-1], falhas={2: 503})
    cod, msgs = resultado(lambda: _sem_numero(Z.obtem_exportacao,
        Z.Cliente("local", None, falha, _credenciais_sinteticas), "groups/1", "EXEC0001",
        destino))
    sobras = [x.name for x in destino.parent.iterdir() if x.name != destino.name]
    g.testa("obtenção interrompida na segunda página: FONTE_EXTERNA, anterior intacto, sem "
            "arquivo parcial nem temporário",
            cod == Saida.FONTE_EXTERNA and destino.read_text(encoding="utf-8") == anterior
            and not sobras and len(falha.pedidos) == 2, f"{cod.name} {sobras}")
    vazia = ServidorRIS("groups/1", "APAGADA1", [])
    nada = pasta / "wos" / "apagada.ris"
    cod, msgs = resultado(lambda: _sem_numero(Z.obtem_exportacao,
        Z.Cliente("local", None, vazia, _credenciais_sinteticas), "groups/1", "APAGADA1", nada))
    g.testa("reprovou (DADOS): coleção sem itens (vazia ou apagada, a via local responde 200), "
            "nada gravado", cod == Saida.DADOS and not nada.exists(), f"{cod.name}")
    vaza = ServidorRIS("groups/1", "EXEC0001",
                       [f"TY  - JOUR\nTI  - {CHAVE_SINTETICA}\nER  - \n\n"])
    outro = pasta / "web" / "vaza.ris"
    cod, msgs = resultado(lambda: _sem_numero(Z.obtem_exportacao,
        Z.Cliente("web", CHAVE_SINTETICA, vaza), "groups/1", "EXEC0001", outro))
    g.testa("obtenção com a chave no conteúdo: nada gravado",
            cod == Saida.FONTE_EXTERNA and not outro.exists(), f"{cod.name}")
