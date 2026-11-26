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
        if cod == Saida.CONFIGURACAO and any(espera in m for m in msgs):
            g.ok(f"reprovou ({cod.name}): {nome} — {msgs[0][:80]}")
        elif cod == Saida.CONFIGURACAO:
            g.falha(f"{nome}: reprovou por outro motivo — {msgs[:1]}")
        else:
            g.falha(f"{nome}: código {cod.name}, esperado CONFIGURACAO — {msgs[:1]}")

    def valida(dado):
        return lambda: C.valida(dado, cfg.nome)

    testa("chave exigida ausente", valida(cfg.sem("padroes.limiar_aderencia")),
          "padroes.limiar_aderencia")
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
