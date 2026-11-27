"""Coleção de sementes do Zotero: a cópia versionada, os campos extraídos de cada item e o
complemento da coleção pela API web.

Os dados bibliográficos, o resumo e as palavras-chave das sementes ficam no Zotero, na
coleção de `[zotero]` do `config.toml`; o arquivo de sementes guarda o controle e liga cada
semente ao item pelo DOI. Os comandos de análise não consultam o Zotero: leem a cópia em
`[dados] zotero`, gravada só por `sementes copiar` (e regravada por
`sementes completar --gravar`).

Acesso (AGENTS.md §9):
  - a chave da API web vem da variável de ambiente `ZOTERO_API_KEY` ou, na falta, da linha
    `ZOTERO_API_KEY=` do `.env` da raiz, que tem de estar no `.gitignore`; é emitida pelo
    pesquisador e nunca se grava nem se imprime — em relato, só os quatro últimos caracteres;
    vai só no cabeçalho da requisição, nunca no endereço;
  - uma requisição por vez, sem nova tentativa: erro de rede, resposta fora do esperado,
    conflito de versão (412), limite de uso (429), pedido de espera (`Backoff`,
    `Retry-After`) ou falta de permissão interrompem o subcomando;
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
from .config import RAIZ, relativo
from .erros import ConfiguracaoInvalida, DadosInvalidos, FonteExterna, Uso
from .markdown import normaliza
from .saida import Saida

VARIAVEL_CHAVE = "ZOTERO_API_KEY"
# Arquivo de ambiente com a chave, na raiz; tem de estar no .gitignore.
ARQUIVO_CHAVE = RAIZ / ".env"
API = "https://api.zotero.org"
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
def _linha_ignorada(gitignore, nome):
    if not gitignore.exists():
        return False
    return any(l.strip() in (nome, f"/{nome}")
               for l in gitignore.read_text(encoding="utf-8").splitlines())


def _do_arquivo(arquivo):
    """O valor de `ZOTERO_API_KEY=` no arquivo de ambiente; "" se o arquivo ou a linha não
    existem. Arquivo que o `.gitignore` não lista é recusado: a chave iria ao controle de
    versão no próximo `git add`."""
    arquivo = pathlib.Path(arquivo)
    if not arquivo.exists():
        return ""
    if not _linha_ignorada(arquivo.parent / ".gitignore", arquivo.name):
        raise ConfiguracaoInvalida(
            f"{arquivo.name} existe e o .gitignore não o lista: a chave iria ao controle de "
            f"versão. Acrescentar `{arquivo.name}` ao .gitignore antes de usá-lo")
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha.startswith("export "):
            linha = linha[len("export "):].strip()
        if linha.startswith(f"{VARIAVEL_CHAVE}="):
            return linha.split("=", 1)[1].strip().strip("'\"")
    return ""


def chave_api(arquivo=None):
    """A chave: a da variável de ambiente ou, na falta, a do arquivo de ambiente da raiz
    (`.env`, fora do controle de versão). Ausente nos dois é CONFIGURACAO."""
    chave = os.environ.get(VARIAVEL_CHAVE, "").strip()
    if not chave:
        chave = _do_arquivo(ARQUIVO_CHAVE if arquivo is None else arquivo)
    if not chave:
        raise ConfiguracaoInvalida(
            f"chave da API web do Zotero ausente: nem a variável de ambiente "
            f"{VARIAVEL_CHAVE} nem a linha `{VARIAVEL_CHAVE}=` em {ARQUIVO_CHAVE.name} (raiz do "
            f"projeto, listado no .gitignore). O pesquisador emite a chave (escrita só na "
            f"biblioteca de grupo) e a guarda fora do controle de versão; os subcomandos que "
            f"não acessam o Zotero não dependem dela")
    return chave


def mascara(chave):
    """O que se pode imprimir da chave: só os quatro últimos caracteres."""
    return f"…{chave[-4:]}" if len(chave) > 4 else "…"


# ----------------------------------------------------------------------- cliente
class Conflito(FonteExterna):
    """O item mudou no Zotero depois da cópia (HTTP 412)."""


class Cliente:
    """Uma requisição por vez à API web, sem nova tentativa. `abrir` substitui
    `urllib.request.urlopen` (autoteste, servidor simulado)."""

    def __init__(self, chave, abrir=None, base=API):
        self._chave = chave
        self._abrir = abrir or urllib.request.urlopen
        self.base = base

    def pedido(self, metodo, caminho, corpo=None, cabecalhos=None):
        """(status, cabeçalhos em minúsculas, corpo em texto). Falha é FonteExterna, cuja
        mensagem nomeia o método e o caminho, nunca a chave."""
        url = f"{self.base}/{caminho.lstrip('/')}"
        dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8") if corpo is not None \
            else None
        cab = {"User-Agent": UA, "Zotero-API-Version": "3", "Zotero-API-Key": self._chave,
               **({"Content-Type": "application/json"} if dados is not None else {}),
               **(cabecalhos or {})}
        req = urllib.request.Request(url, data=dados, headers=cab, method=metodo)
        rotulo = f"{metodo} {caminho.split('?')[0]}"
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
            condicao = {403: "chave sem permissão (HTTP 403) — conferir em "
                             "zotero.org/settings/keys se a chave tem escrita na biblioteca "
                             "de grupo (permissão por grupo)",
                        429: "limite de uso excedido (HTTP 429)",
                        503: "serviço indisponível (HTTP 503)"}.get(e.code,
                                                                    f"resposta HTTP {e.code}")
            extra = f"; pedido de espera de {espera} s" if espera else ""
            raise FonteExterna(f"{condicao} em {rotulo}{extra}") from None
        except Exception as e:                                      # noqa: BLE001
            raise FonteExterna(f"erro de rede em {rotulo}: {type(e).__name__}") from None
        return status, h, texto


def _sem_espera(h, rotulo):
    """Pedido de espera numa resposta bem-sucedida também interrompe."""
    for nome in ("backoff", "retry-after"):
        if h.get(nome):
            raise FonteExterna(f"pedido de espera do Zotero ({nome}: {h[nome]} s) em {rotulo}")


def le_colecao(cliente, biblioteca, colecao):
    """A coleção lida da API web: {biblioteca, colecao, versao, lida_em, itens}, com os
    itens de topo como a API os devolve (formato json)."""
    itens, inicio, total, versao = [], 0, None, None
    while total is None or inicio < total:
        caminho = (f"{biblioteca}/collections/{colecao}/items/top?"
                   + urllib.parse.urlencode({"format": "json", "limit": POR_PAGINA,
                                             "start": inicio}))
        status, h, texto = cliente.pedido("GET", caminho)
        if status != 200:
            raise FonteExterna(f"resposta HTTP {status} em GET {caminho.split('?')[0]}")
        _sem_espera(h, f"GET {caminho.split('?')[0]}")
        try:
            pagina = json.loads(texto)
            total = int(h.get("total-results", len(pagina)))
            versao = int(h["last-modified-version"])
        except (json.JSONDecodeError, KeyError, ValueError):
            raise FonteExterna(f"resposta fora do formato esperado em GET "
                               f"{caminho.split('?')[0]}") from None
        if not isinstance(pagina, list):
            raise FonteExterna(f"resposta fora do formato esperado em GET "
                               f"{caminho.split('?')[0]}")
        itens += pagina
        if not pagina:
            break
        inicio += len(pagina)
    lida = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    return {"biblioteca": biblioteca, "colecao": colecao, "versao": versao, "lida_em": lida,
            "itens": itens}


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


def grava_json(destino, doc, chave=None):
    """Grava num temporário do mesmo diretório e só então substitui o anterior. Se o texto
    contiver a chave da API, nada se grava (garantia, não conferência posterior)."""
    texto = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
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


def _configurado(ctx):
    return ctx.config.valor("zotero.biblioteca"), ctx.config.valor("zotero.colecao")


def copia(ctx, cliente, chave):
    """Lê a coleção, relata a diferença para a cópia anterior e grava a nova cópia."""
    biblioteca, colecao = _configurado(ctx)
    destino = ctx.config.caminho("dados.zotero")
    anterior = le_copia(destino) if destino.exists() else None
    nova = le_colecao(cliente, biblioteca, colecao)
    linhas = diferencas(anterior, nova)
    print(f"Coleção {colecao} de {biblioteca}: {len(nova['itens'])} itens, versão "
          f"{nova['versao']} da biblioteca, lida em {nova['lida_em']} (chave {mascara(chave)})")
    if anterior is None:
        print("Sem cópia anterior: todos os itens entram como acrescentados.")
    else:
        print(f"Diferença para a cópia anterior (versão {anterior['versao']}, lida em "
              f"{anterior['lida_em']}): {len(linhas) or 'nenhuma'}")
    for l in linhas:
        print(l)
    grava_json(destino, nova, chave)
    print(f"Cópia gravada em {relativo(destino)}.")
    return nova


def cmd_copiar(ctx, a=None):
    chave = chave_api()
    copia(ctx, Cliente(chave), chave)
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


def completa(ctx, cliente, chave, retirar=(), gravar=False):
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
    print(f"Ponto de restauração: {relativo(alvo)}  (chave {mascara(chave)})")
    aplica(cliente, biblioteca, colecao, acoes)
    copia(ctx, cliente, chave)


def cmd_completar(ctx, a):
    confere_retirar(ctx, a.retirar or ())
    chave = chave_api()
    completa(ctx, Cliente(chave), chave, retirar=a.retirar or (), gravar=a.gravar)
    return Saida.OK
