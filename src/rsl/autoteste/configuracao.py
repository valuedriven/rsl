"""Autoteste da configuração: ausente, inválida, incompleta ou com chave fora do esquema
reprova com CONFIGURACAO e mensagem que nomeia a chave ou o arquivo."""

import pathlib
import tempfile

from .. import config as C
from ..saida import Saida
from . import resultado


def casos(ctx, g):
    cfg = ctx.config
    sigla = ctx.protocolo()["bases"][0]["sigla"]

    def testa(nome, funcao, espera):
        cod, msgs = resultado(funcao)
        textos = (espera,) if isinstance(espera, str) else tuple(espera)
        if cod == Saida.CONFIGURACAO and all(x in " ".join(msgs) for x in textos):
            g.ok(f"reprovou ({cod.name}): {nome} — {msgs[0][:80]}")
        elif cod == Saida.CONFIGURACAO:
            g.falha(f"{nome}: reprovou por outro motivo — {msgs[:1]}")
        else:
            g.falha(f"{nome}: código {cod.name}, esperado CONFIGURACAO — {msgs[:1]}")

    def valida(dado):
        return lambda: C.valida(dado, cfg.nome)

    testa("chave exigida ausente", valida(cfg.sem("padroes.limiar_aderencia")),
          "padroes.limiar_aderencia")
    testa("resultado técnico da validação ausente",
          valida(cfg.sem("dados.consulta_terminologica")), "dados.consulta_terminologica")
    # A chave e a seção retiradas nomeiam as duas chaves que as substituem: quem migra sabe
    # onde pôr a decisão e o resultado técnico. A chave vem primeiro, por ser o caso mais
    # provável no config.toml antigo.
    testa("chave `planilha.campos_validacao` retirada",
          valida(cfg.com("planilha", {"campos_validacao": ["status_proposto"]})),
          ("[dados] validacao", "[dados] consulta_terminologica"))
    testa("seção `[planilha]` retirada",
          valida(cfg.com("planilha", {"outra_chave": "x"})),
          ("[dados] validacao", "[dados] consulta_terminologica"))
    testa("caminho do protocolo ausente", valida(cfg.sem("protocolo")), "`protocolo`")
    testa("padrão de caminho do procedimento de busca ausente",
          valida(cfg.sem("documentos.procedimento")), "documentos.procedimento")
    testa("padrão de caminho do procedimento de busca sem o marcador da sigla",
          valida(cfg.com("documentos.procedimento", "docs/procedimentos_busca.md")),
          C.MARCADORES["documentos.procedimento"])
    # Chave antiga, renomeada: reprova no lugar da canônica e nomeia a canônica.
    antiga = cfg.sem("documentos.procedimento")
    antiga["documentos"]["ficha"] = cfg.valor("documentos.procedimento")
    testa("chave antiga `[documentos] ficha` no lugar da canônica", valida(antiga),
          "`[documentos] procedimento`")
    # A correção indicada é renomear, não retirar: retirada, a chave canônica faltaria.
    testa("chave antiga `[documentos] ficha` indica renomear, não retirar", valida(antiga),
          "renomeá-la")
    for marca in C.MARCADORES["saidas.fidelidade"]:
        sem_marca = cfg.valor("saidas.fidelidade").replace(marca, "")
        testa(f"saída de fidelidade sem o marcador {marca}",
              valida(cfg.com("saidas.fidelidade", sem_marca)), marca)
    testa(f"[fichas.{sigla}] na configuração",
          valida(cfg.com("fichas", {sigla: {"execucao": "unica"}})), "`fichas`")
    # Toda chave retirada, de volta à configuração, é segunda fonte: reprova.
    for chave in (c for c in C.RETIRADAS if c != "fichas"):
        testa(f"chave retirada `{chave}` na configuração",
              valida(cfg.com(chave, ["valor do autoteste"])), f"`{chave}`")
    # Caso nomeado, e não só o laço acima: o laço percorre RETIRADAS e deixaria de ver a chave
    # que voltasse ao esquema saindo de RETIRADAS.
    testa("mínimo de termos por string, retirado, na configuração",
          valida(cfg.com("conferencia.minimo_termos_string", 20)), "minimo_termos_string")
    testa("chave da planilha de aderência, retirada, na configuração",
          valida(cfg.com("saidas.aderencia", "semente_aderencia.csv")),
          "a planilha de aderência foi retirada")
    testa("biblioteca do Zotero fora da forma groups/<id> ou users/<id>",
          valida(cfg.com("zotero.biblioteca", "fatores")), "zotero.biblioteca")
    testa("chave fora do esquema", valida(cfg.com("padroes.chave_inventada", 1)),
          "chave desconhecida")
    testa("faixa padrão invertida",
          valida(cfg.com("padroes.sensibilidade",
                         list(reversed(cfg.valor("padroes.sensibilidade"))))), "inferior")
    with tempfile.TemporaryDirectory() as tmp:
        ruim = pathlib.Path(tmp) / C.NOME
        ruim.write_text("protocolo = \n", encoding="utf-8")
        testa("arquivo que não é TOML", lambda: C.carrega(ruim), "não é TOML válido")
        testa("arquivo ausente", lambda: C.carrega(pathlib.Path(tmp) / "nada.toml"),
              "ausente")
        sem_protocolo = pathlib.Path(tmp) / "sem_protocolo.toml"
        texto = cfg.arquivo.read_text(encoding="utf-8")
        texto = texto.replace(f'"{cfg.valor("protocolo")}"',
                              f'"{cfg.valor("protocolo")}.inexistente"', 1)
        sem_protocolo.write_text(texto, encoding="utf-8")
        testa("chave `protocolo` apontando arquivo inexistente",
              lambda: C.carrega(sem_protocolo), "que não existe")

    # Via de acesso, pasta de temporários e cache das exportações (acesso-ao-zotero). Cada
    # recusa tem o controle: a mesma configuração, sem a mutação, passa.
    def passa(nome, funcao):
        cod, msgs = resultado(funcao)
        g.testa(f"controle: {nome} passa", cod == Saida.OK, f"{cod.name} — {msgs[:1]}")

    testa("`[zotero] acesso` fora de local/web", valida(cfg.com("zotero.acesso", "nuvem")),
          "`[zotero] acesso`")
    for via in C.ACESSOS:
        passa(f"`[zotero] acesso = {via!r}`", valida(cfg.com("zotero.acesso", via)))
    testa("cache das exportações em data/",
          valida(cfg.com("dados.execucoes", "data/execucoes")), "`[dados] execucoes`")
    passa("cache das exportações dentro da pasta de temporários",
          valida(cfg.com("dados.execucoes",
                         f"{cfg.valor('dados.temporarios')}/execucoes")))
    pasta = cfg.valor("dados.temporarios").strip("/")
    with tempfile.TemporaryDirectory() as tmp:
        sem = pathlib.Path(tmp) / ".gitignore"
        sem.write_text("*.ris\n.env\n", encoding="utf-8")
        com = pathlib.Path(tmp) / "gitignore_com"
        com.write_text(f"*.ris\n.env\n{pasta}/\n", encoding="utf-8")
        testa("pasta de temporários fora do .gitignore",
              lambda: C.valida(cfg.dado, cfg.nome, sem), "não está listada")
        passa("pasta de temporários listada no .gitignore",
              lambda: C.valida(cfg.dado, cfg.nome, com))
        # Pasta fora da raiz dispensa o .gitignore; o caso acima, com o mesmo .gitignore e a
        # pasta dentro da raiz, é o controle que mostra que a dispensa não é geral.
        fora = cfg.com("dados.temporarios", str(pathlib.Path(tmp) / "tmp"))
        fora["dados"]["execucoes"] = str(pathlib.Path(tmp) / "tmp" / "execucoes")
        passa("pasta de temporários fora da raiz do projeto, sem linha no .gitignore",
              lambda: C.valida(fora, cfg.nome, sem))
        # `nome/` no .gitignore só casa com pasta: não protege o arquivo `.env`.
        so_pasta = pathlib.Path(tmp) / "gitignore_barra"
        so_pasta.write_text(".env/\n", encoding="utf-8")
        g.testa("`.env/` no .gitignore não conta como arquivo ignorado",
                not C.linha_ignorada(so_pasta, ".env")
                and C.linha_ignorada(com, ".env"), "a linha com barra final foi aceita")
    sem_buscas = C.Configuracao(cfg.sem("zotero.search_collection")
                                if "search_collection" in cfg.dado["zotero"] else cfg.dado,
                                cfg.arquivo)
    testa("coleção das buscas ausente, pedida por quem precisa dela",
          lambda: sem_buscas.exige("zotero.search_collection"), "search_collection")
    passa("coleção das buscas ausente não reprova a carga",
          valida(sem_buscas.dado))
    testa("coleção das buscas vazia", valida(cfg.com("zotero.search_collection", " ")),
          "zotero.search_collection")

    # Biblioteca e coleção das buscas: a biblioteca na forma da API ou pelo endereço do site;
    # sem `library`, a das sementes.
    url = "https://www.zotero.org/groups/6781444/modelagem-educacional"
    g.testa("endereço da biblioteca de grupo no site vale como groups/<id>",
            C.biblioteca_zotero(url) == "groups/6781444"
            and C.biblioteca_zotero("groups/6781444") == "groups/6781444"
            and C.biblioteca_zotero("https://www.zotero.org/usuario/library") is None,
            f"{C.biblioteca_zotero(url)!r}")
    testa("`[zotero] library` fora da forma",
          valida(cfg.com("zotero.library", "modelagem-educacional")), "zotero.library")
    passa("`[zotero] library` pelo endereço do site", valida(cfg.com("zotero.library", url)))
    com_buscas = C.Configuracao(cfg.com("zotero.search_collection", "buscas"), cfg.arquivo)
    com_url = C.Configuracao(C.Configuracao(com_buscas.com("zotero.library", url),
                                            cfg.arquivo).dado, cfg.arquivo)
    sem_lib = C.Configuracao(com_buscas.sem("zotero.library")
                             if "library" in com_buscas.dado["zotero"] else com_buscas.dado,
                             cfg.arquivo)
    g.testa("coleção das buscas: nome de `search_collection` e biblioteca de `library`",
            com_url.buscas() == ("groups/6781444", "buscas"), f"{com_url.buscas()}")
    g.testa("sem `library`, a coleção das buscas fica na biblioteca de `[zotero] biblioteca`",
            sem_lib.buscas() == (sem_lib.biblioteca(), "buscas"), f"{sem_lib.buscas()}")
