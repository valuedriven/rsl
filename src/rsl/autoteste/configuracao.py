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
    testa("padrão de caminho da ficha ausente", valida(cfg.sem("documentos.ficha")),
          "documentos.ficha")
    testa("padrão de caminho da ficha sem o marcador da sigla",
          valida(cfg.com("documentos.ficha", "docs/procedimentos_busca.md")),
          C.MARCADORES["documentos.ficha"])
    testa("saída de fidelidade sem o marcador da expressão",
          valida(cfg.com("saidas.fidelidade", "fidelidade.csv")),
          C.MARCADORES["saidas.fidelidade"])
    testa(f"[fichas.{sigla}] na configuração",
          valida(cfg.com("fichas", {sigla: {"execucao": "unica"}})), "`fichas`")
    # Toda chave retirada, de volta à configuração, é segunda fonte: reprova.
    for chave in (c for c in C.RETIRADAS if c != "fichas"):
        testa(f"chave retirada `{chave}` na configuração",
              valida(cfg.com(chave, ["valor do autoteste"])), f"`{chave}`")
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
