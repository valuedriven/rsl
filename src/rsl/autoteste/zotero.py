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
from ..saida import Saida
from . import resultado

CHAVE_SINTETICA = "autotesteCHAVEsintetica0000wxyz"


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
        cod, msgs, saida = _calado(lambda: Z.copia(cx, Z.Cliente(Z.chave_api(), srv),
                                                   Z.chave_api()))
        erro = Servidor(biblioteca, colecao, itens, falhas={1: (403, {})})
        cod_e, msgs_e, saida_e = _calado(
            lambda: Z.copia(cx, Z.Cliente(Z.chave_api(), erro), Z.chave_api()))
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
    cliente = Z.Cliente(CHAVE_SINTETICA, srv)
    cod, msgs, saida = _calado(lambda: Z.copia(cx, cliente, CHAVE_SINTETICA))
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
    cod, msgs, saida = _calado(lambda: Z.copia(cx, cliente, CHAVE_SINTETICA))
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
    cliente = Z.Cliente(CHAVE_SINTETICA, srv)
    _calado(lambda: Z.copia(cx, cliente, CHAVE_SINTETICA))
    versao = srv.versao
    n_pedidos = len(srv.pedidos)
    cod, msgs, saida = _calado(lambda: Z.completa(cx, cliente, CHAVE_SINTETICA))
    g.testa("sem --gravar, nada muda no Zotero e o item fora do arquivo é relatado",
            cod == Saida.OK and len(srv.pedidos) == n_pedidos and srv.versao == versao
            and "10.9999/autoteste.fora" in saida, f"{cod.name} {msgs[:1]}")
    acoes, _ = Z.plano(Z.le_copia(cx.config.caminho("dados.zotero")), set(dois),
                       OA.respostas_gravadas(cx, dois))
    primeira = next((x for x in acoes if x["campos"]["doi"] == dois[0]), None)
    g.testa("resumo já preenchido fica fora do plano",
            primeira is not None and primeira["resumo"] is None, f"{primeira}")

    cod, msgs, saida = _calado(lambda: Z.completa(cx, cliente, CHAVE_SINTETICA, gravar=True,
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
    cod, msgs, _ = _calado(lambda: Z.completa(cx, cliente, CHAVE_SINTETICA,
                                              retirar=["10.9999/autoteste.inexistente"]))
    g.testa("--retirar de DOI que nenhum item da cópia tem é recusado (USO)",
            cod == Saida.USO, f"{cod.name}")
    n_antes = len(srv.pedidos)
    cod, msgs, _ = _calado(lambda: Z.completa(cx, cliente, CHAVE_SINTETICA, gravar=True,
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
    cliente2 = Z.Cliente(CHAVE_SINTETICA, srv2)
    _calado(lambda: Z.copia(cx, cliente2, CHAVE_SINTETICA))
    srv2.altera(f"AUTO{1:04d}", title="mudou na interface")
    cod, msgs, _ = _calado(lambda: Z.completa(cx, cliente2, CHAVE_SINTETICA, gravar=True))
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
    cliente3 = Z.Cliente(CHAVE_SINTETICA, srv3)
    _calado(lambda: Z.copia(cx, cliente3, CHAVE_SINTETICA))
    srv3.falhas = {len(srv3.pedidos) + 1: (429, {"Retry-After": "30"})}
    cod, msgs, _ = _calado(lambda: Z.completa(cx, cliente3, CHAVE_SINTETICA, gravar=True))
    patches = [x for x in srv3.pedidos if x[0] == "PATCH"]
    g.testa("limite de uso (429) interrompe a gravação sem nova tentativa",
            cod == Saida.FONTE_EXTERNA and len(patches) == 1
            and any("429" in m for m in msgs), f"{cod.name} {len(patches)}")
