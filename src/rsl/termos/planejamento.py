"""Planejamento da validação terminológica: que termo se valida em que instrumento, e com que
estatuto nasce a linha da planilha.

Um termo do quadro de uma faceta é planejado para cada instrumento cuja coluna FCTs traz a
faceta e cuja coluna Idiomas traz o idioma do termo. Instrumento `Manual` não tem cliente:
a linha nasce pendente de validação manual — nunca como termo não encontrado.
"""

import re

from .. import gramatica as G

STATUS_MANUAL = "pendente de validação manual"
OBS_MANUAL = "instrumento sem cliente automatizado: consultar e registrar à mão"
OBS_AGUARDANDO = "aguardando consulta"
STATUS_NAO_LOCALIZADO = "termo livre (não localizado no instrumento)"
STATUS_AUTORIZADO = "descritor autorizado (a conferir pelo ReT)"
STATUS_EQUIVALENTE = "termo equivalente USE/UP (a conferir pelo ReT)"
# Termo de prova que nenhum instrumento tem: a sonda confere a resposta de termo ausente.
TERMO_INEXISTENTE = "palavra-que-nao-existe-xyz"


def estado_inicial(instrumento):
    """Campos com que nasce a linha de um termo ainda não registrado na planilha."""
    if instrumento["modo"] == G.MODO_MANUAL:
        return {"status_proposto": STATUS_MANUAL, "observacao_tecnica": OBS_MANUAL}
    return {"observacao_tecnica": OBS_AGUARDANDO}


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


def termos_de_prova(d, instrumento, inexistente=True, quantos=2):
    """Termos para a sonda: os primeiros da primeira faceta e do primeiro idioma que o
    instrumento cobre, lidos do protocolo, e um termo que não existe."""
    fid, idioma = instrumento["facetas"][0], instrumento["idiomas"][0]
    f = next(x for x in d["tabelas"] if x["id"] == fid)
    saida = list(f["termos"][idioma][:quantos])
    return saida + ([TERMO_INEXISTENTE] if inexistente else [])
