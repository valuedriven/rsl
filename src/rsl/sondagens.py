"""Registro do resultado de uma sondagem do roteiro de uma base.

`sondagens registrar <sigla> <SDn>` acrescenta o resultado a `bases.BDn.sondagens[]` do
registro de execução, de forma atômica, e exibe a citação `BDn/<id>` e, por elemento da
sondagem, a situação e a citação a aplicar na fonte. NÃO altera a fonte: a fonte se edita
pelo agente ou pelo pesquisador (a biblioteca padrão não escreve TOML preservando
comentários).

A data e a hora são obrigatórias, sem padrão "agora": a sondagem costuma ser registrada
depois de feita, e a data presumida seria falsa. A evidência é obrigatória e tem de existir:
sondagem sem evidência não é sondagem.
"""

import datetime
import json
import pathlib

from . import gramatica as G
from .config import RAIZ, relativo
from .erros import DadosInvalidos, ProtocoloInvalido, Uso
from .fonte import le_fonte
from .geracao import grava_atomico
from .saida import Saida


def _data(texto):
    try:
        return datetime.datetime.fromisoformat(texto)
    except (TypeError, ValueError):
        raise Uso(f"--data-hora {texto!r} não é ISO 8601 (AAAA-MM-DDTHH:MM)") from None


def registra(ctx, sigla, sd, retornos, leitura, data_hora, evidencias, submetidos=(),
             observacao="", caminho=None, saida=print):
    d = ctx.protocolo()
    b = next((x for x in d["bases"] if x["sigla"] == sigla), None)
    if b is None:
        raise Uso(f"base {sigla!r} não consta da tabela de bases do protocolo "
                  f"({[x['sigla'] for x in d['bases']]})")
    if not data_hora:
        raise Uso("falta --data-hora: obrigatório, sem padrão, porque o registro costuma ser "
                  "posterior à sondagem")
    if not evidencias:
        raise Uso("falta --evidencia: sondagem sem evidência não se registra")
    quando = _data(data_hora)
    fonte = le_fonte(ctx, d, sigla)
    s = fonte["sondagens"].get(sd)
    if s is None:
        raise ProtocoloInvalido(G.T_SONDAGENS, f"a fonte de {sigla} não declara a sondagem "
                                               f"{sd!r} ({sorted(fonte['sondagens'])})",
                                fonte["doc"])
    if len(retornos) != len(s["consultas"]):
        raise Uso(f"{sd} declara {len(s['consultas'])} consulta(s); vieram {len(retornos)} "
                  f"--retorno")
    if leitura is None or not 1 <= leitura <= len(s["leituras"]):
        raise Uso(f"--leitura {leitura!r}: {sd} declara as leituras 1 a {len(s['leituras'])}")
    caminhos = []
    for ev in evidencias:
        arq = pathlib.Path(ev)
        arq = arq if arq.is_absolute() else RAIZ / arq
        if not arq.is_file():
            raise DadosInvalidos(f"evidência {ev!r} não existe")
        caminhos.append(relativo(arq))
    textos = [c["texto"] for c in s["consultas"]]
    for k, texto in submetidos:
        try:
            idx = int(k)
        except ValueError:
            raise Uso(f"--submetido {k!r}: K é o número da consulta") from None
        if not 1 <= idx <= len(textos):
            raise Uso(f"--submetido {k}: {sd} tem as consultas 1 a {len(textos)}")
        textos[idx - 1] = texto

    caminho = pathlib.Path(caminho) if caminho else ctx.config.caminho("dados.registro")
    if caminho.exists():
        try:
            registro = json.loads(caminho.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise DadosInvalidos(f"{relativo(caminho)} ilegível: {e}") from None
    else:
        # Registro novo: com todas as bases do protocolo, para que `dados conferir` e
        # `busca registrar` o aceitem nas demais bases.
        registro = {"bases": {x["id"]: {"base": x["nome"], "execucoes": []}
                              for x in d["bases"]}}
    base = registro.setdefault("bases", {}).setdefault(b["id"], {"base": b["nome"],
                                                                 "execucoes": []})
    lista = base.setdefault("sondagens", [])
    raiz = f"{sd.lower()}-{quando.date().isoformat()}"
    existentes = {r.get("id") for r in lista if isinstance(r, dict)}
    rid, n = raiz, 2
    while rid in existentes:
        rid, n = f"{raiz}-{n}", n + 1
    escolhida = s["leituras"][leitura - 1]
    lista.append({
        "id": rid, "sondagem": sd, "data_hora": quando.isoformat(timespec="minutes"),
        "consultas": [{"texto": t, "retorno": r} for t, r in zip(textos, retornos)],
        "leitura": {"numero": leitura, "resultado": escolhida["resultado"],
                    "estado": escolhida["estado"]},
        "evidencia": caminhos, "observacao": observacao,
    })
    os_texto = json.dumps(registro, ensure_ascii=False, indent=2) + "\n"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    grava_atomico(caminho, os_texto)
    citacao = f"{b['id']}/{rid}"
    saida(f"Registrado em {relativo(caminho)}: {citacao}.")
    saida(f"Mudança a aplicar na fonte {fonte['pasta']}/procedimento.toml (o comando não a "
          f"altera):")
    for el in s["elementos"]:
        extra = f', citacao = "{citacao}"' if escolhida["estado"] == G.SITUACAO_MEDICAO else ""
        saida(f"  - {el!r}: situacao = \"{escolhida['estado']}\"{extra}")
    saida(f"O roteiro do procedimento traz os resultados registrados: depois de aplicar a "
          f"mudança, gerar com `python3 -m rsl procedimentos gerar {sigla} --gravar`.")
    return Saida.OK


def cmd_registrar(ctx, a):
    return registra(ctx, a.sigla, a.sondagem, a.retorno, a.leitura, a.data_hora,
                    a.evidencia, a.submetido, a.observacao)
