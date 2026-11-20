"""Registro de uma execução no registro de execuções, com a conferência do retorno
declarado pela base contra o arquivo exportado."""

import datetime
import json
import pathlib

from ..config import RAIZ, relativo
from ..erros import DadosInvalidos, Uso
from ..markdown import normaliza
from ..saida import Saida
from . import Busca
from .leitores import le_arquivo
from .registro import ESTADOS_EXCLUIDOS, le_registro


def registrar(b, base, expressao, arquivo, retorno, data_hora=None, justificar=""):
    """Registra uma execução no registro por base e confere o retorno contra o arquivo.

    Retorno divergente sem justificativa é RECUSADO (REPROVADO): nada é gravado.
    """
    id_expr = b.exige_expressao(expressao)
    bd, nome = b.exige_bd(base)

    caminho = pathlib.Path(arquivo)
    if not caminho.is_absolute():
        caminho = pathlib.Path.cwd() / caminho
    if not caminho.exists():
        raise DadosInvalidos(f"Arquivo não encontrado: {arquivo}")
    regs = le_arquivo(caminho)
    if not regs:
        raise DadosInvalidos(f"Nenhum registro legível em {arquivo}. Nada foi registrado.")

    lidos = len(regs)
    status, just = "valida", ""
    if retorno is None:
        raise Uso("Informe --retorno com o número que a base exibiu. Nada foi registrado.")
    if int(retorno) != lidos:
        if not justificar:
            print(f"RECUSADO: a base declarou {retorno} registros e o arquivo traz {lidos}.\n"
                  "  Arquivo trocado, exportação parcial ou teto de retorno da base.\n"
                  "  Se a diferença for conhecida e aceitável, repita com --justificar "
                  "\"motivo\".")
            return Saida.REPROVADO
        status, just = "divergente_justificada", justificar.strip()

    try:
        rel = str(caminho.resolve().relative_to(RAIZ))
    except ValueError:
        rel = str(caminho.resolve())

    onde = relativo(b.registro)
    dado = le_registro(b)
    item = (dado.get("bases") or {}).get(bd)
    if not isinstance(item, dict):
        raise DadosInvalidos(f"{onde} sem a base {bd}. Nada foi registrado.")
    execucoes = item.setdefault("execucoes", [])
    agora = data_hora or datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    dia = agora[:10]

    achado = next((e for e in execucoes
                   if e.get("arquivo") == rel and e.get("expressao") == id_expr
                   and normaliza(e.get("estado")) not in ESTADOS_EXCLUIDOS), None)
    if achado is None:
        ids = {e.get("id") for e in execucoes}
        n = 1
        while f"EX{n}" in ids:
            n += 1
        achado = {
            "id": f"EX{n}",
            "expressao": id_expr,
            "forma": "registrada por busca registrar",
            "retorno": int(retorno),
            "data": dia,
            "data_hora": agora,
            "mede": f"{id_expr}, execução registrada",
            "estado": "registrada",
            "origem": "exportacao",
            "arquivo": rel,
            "registros_lidos": lidos,
            "status": status,
            "justificativa_divergencia": just,
        }
        execucoes.append(achado)
    else:
        achado.update({
            "retorno": int(retorno),
            "data": dia,
            "data_hora": agora,
            "arquivo": rel,
            "registros_lidos": lidos,
            "status": status,
            "justificativa_divergencia": just,
        })

    b.registro.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")

    print(f"Consulta registrada em {onde}:\n"
          f"  {bd} {achado['id']} — {nome} {id_expr} em {agora}\n"
          f"  retorno declarado {retorno}, registros lidos {lidos} — {status}")
    if status != "valida":
        print(f"  divergência justificada: {just}")
    print("  A data oficial de execução continua sendo a do cronograma.")
    return Saida.OK


def cmd_registrar(ctx, a):
    return registrar(Busca(ctx), a.base, a.expressao, a.arquivo, a.retorno, a.data_hora,
                     a.justificar)
