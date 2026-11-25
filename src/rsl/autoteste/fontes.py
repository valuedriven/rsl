"""Apoio do autoteste: cópias em memória da fonte do procedimento de busca de uma base.

A fonte vem da pasta corrente (`[documentos] procedimento_fonte`), lida como dado; o defeito
se injeta na cópia e se lê por `Contexto.com_fontes`, sem tocar a pasta.
"""

import copy
import tomllib

from .. import gramatica as G


def fonte_de(ctx, d, sigla):
    """(dado, fragmentos, arquivos) da fonte corrente de `sigla`, como cópia editável."""
    bruta = ctx.fonte_bruta(sigla, ctx.config.fonte(sigla))
    if bruta is None:
        raise LookupError(f"fonte de {sigla!r} inexistente")
    dado = bruta["toml"]
    dado = copy.deepcopy(dado) if isinstance(dado, dict) else tomllib.loads(dado)
    return dado, dict(bruta["fragmentos"]), list(bruta["arquivos"])


def com_fonte(ctx, sigla, dado, fragmentos, arquivos=None):
    """Contexto com a fonte de `sigla` trocada pela cópia."""
    if arquivos is None:
        arquivos = ["procedimento.toml"] + sorted(fragmentos)
    return ctx.com_fontes({sigla: {"toml": dado, "fragmentos": dict(fragmentos),
                                   "arquivos": list(arquivos)}})


def base_com(ctx, d, condicao):
    """Sigla da primeira base cuja fonte satisfaz `condicao(dado)`; None se nenhuma."""
    for b in d["bases"]:
        try:
            dado, _, _ = fonte_de(ctx, d, b["sigla"])
        except LookupError:
            continue
        if condicao(dado):
            return b["sigla"]
    return None


def _inconclusiva(dado):
    """A primeira sondagem cujos elementos a fonte ainda dá como não verificados: o
    resultado de leitura inconclusiva dela não tem nada a levar à fonte. Sondagem já medida
    não serve: o resultado inconclusivo contradiria a fonte e seria relatado."""
    situacao = {s["elemento"]: s["situacao"] for s in dado["sintaxe"]}
    situacao.update({r["texto"]: r["situacao"] for r in dado.get("regras_de_montagem", [])})
    return next((s for s in dado.get("sondagens", [])
                 if all(situacao.get(e) == G.SITUACAO_NAO_VERIFICADO for e in s["elementos"])),
                None)


def registro_com_sondagem(ctx, d):
    """(sigla, registro) com um resultado válido da primeira sondagem ainda não verificada
    da primeira base que a tenha: leitura inconclusiva, sem elemento a levar à fonte."""
    sigla = base_com(ctx, d, lambda x: _inconclusiva(x) is not None)
    if sigla is None:
        return None, None
    dado, _, _ = fonte_de(ctx, d, sigla)
    s = _inconclusiva(dado)
    k = next(i for i, x in enumerate(s["leituras"], 1)
             if x["estado"] == G.SITUACAO_NAO_VERIFICADO)
    bd = next(b for b in d["bases"] if b["sigla"] == sigla)
    resultado = {
        "id": f"{s['id'].lower()}-2026-01-01", "sondagem": s["id"],
        "data_hora": "2026-01-01T10:00",
        # `dados conferir` não compara o texto registrado com a fonte: o da consulta por
        # referência (sem `texto`) basta como marcador.
        "consultas": [{"texto": c.get("texto") or c["expressao"], "retorno": 1}
                      for c in s["consultas"]],
        "leitura": {"numero": k, "resultado": s["leituras"][k - 1]["resultado"],
                    "estado": s["leituras"][k - 1]["estado"]},
        "evidencia": ["autoteste.png"], "observacao": "",
    }
    return sigla, {"bases": {bd["id"]: {"base": bd["nome"], "execucoes": [],
                                        "sondagens": [resultado]}}}
