"""Decisão do ReT e linha do termo no controle terminológico.

A linha de um termo no CT resulta da `decisao_ReT` registrada na planilha de validação,
sobre os instrumentos planejados para a faceta e o idioma dele (`planejamento.py`):
descritor em algum instrumento → "Descritores correspondentes"; senão, sinônimo ou
relacionado em algum → "Termos sinônimos ou relacionados"; senão → "Termo livre". Termo sem
decisão, de instrumento manual ainda não consultado ou sem planilha é termo livre (plano,
M3/E1: termo sem consulta registrada é termo livre). `status_proposto` é a proposta da
máquina e não classifica.

O domínio de `decisao_ReT` é fechado (gramatica.DECISAO_RET), sem distinção de caixa; o
vazio é "sem decisão". Valor fora dele é problema, não "sem decisão".
"""

import csv
import io

from .. import gramatica as G
from ..config import relativo
from ..erros import DadosInvalidos
from ..leitura import instrumentos_do_termo
from ..markdown import normaliza

COLUNA_DECISAO = "decisao_ReT"
# Colunas sem as quais a planilha não diz de que termo, em que instrumento, é a decisão.
COLUNAS_EXIGIDAS = ("faceta", "idioma", "termo", "instrumento", COLUNA_DECISAO)
_DOMINIO = {k.casefold(): v for k, v in G.DECISAO_RET.items()}
ROTULO = {r.interno: r.texto for r in G.LINHAS_CT}


def admitidos():
    return list(G.DECISAO_RET) + ["(vazio)"]


def linha_da_decisao(valor):
    """Linha do CT de uma decisão: o nome interno, None para o vazio; KeyError fora do
    domínio."""
    v = (valor or "").strip().casefold()
    if not v:
        return None
    return _DOMINIO[v]


def fora_do_dominio(linhas):
    """[texto] de cada linha da planilha com `decisao_ReT` fora do domínio, nomeando termo,
    faceta, idioma, instrumento e valor."""
    saida = []
    for r in linhas:
        valor = (r.get(COLUNA_DECISAO) or "").strip()
        try:
            linha_da_decisao(valor)
        except KeyError:
            saida.append(f"{COLUNA_DECISAO} {valor!r} fora do domínio para {r.get('termo')!r} "
                         f"({r.get('faceta')}, {r.get('idioma')}, {r.get('instrumento')}); "
                         f"admitidos: {admitidos()}")
    return saida


def le_planilha(texto, caminho):
    """Linhas da planilha de validação a partir do texto; DadosInvalidos se ilegível (CSV
    inválido ou sem as colunas exigidas). Planilha ilegível não é planilha ausente."""
    try:
        leitor = csv.DictReader(io.StringIO(texto), delimiter=";")
        linhas = list(leitor)
    except csv.Error as e:
        raise DadosInvalidos(f"{caminho}: planilha de validação ilegível ({e})") from None
    faltam = [c for c in COLUNAS_EXIGIDAS if c not in (leitor.fieldnames or [])]
    if faltam:
        raise DadosInvalidos(f"{caminho}: planilha de validação ilegível — faltam as "
                             f"colunas {faltam}")
    return linhas


def planilha(ctx):
    """Linhas da planilha de validação do contexto; None se ela não existe."""
    texto = ctx.texto_validacao
    if texto is None:
        return None
    return le_planilha(texto, relativo(ctx.config.caminho("dados.validacao")))


def linhas_esperadas(d, linhas):
    """{(faceta, idioma, termo normalizado): linha interna} dos termos com alguma decisão
    que não seja termo livre, só nos instrumentos planejados para a faceta e o idioma do
    termo. O termo ausente do mapa tem a linha `livre`. Valor fora do domínio é ignorado
    aqui e reprovado por `fora_do_dominio`."""
    planejados = {}
    decisoes = {}
    for r in linhas or []:
        fid, idioma = (r.get("faceta") or "").strip(), (r.get("idioma") or "").strip()
        if (fid, idioma) not in planejados:
            # Linha órfã (faceta fora do protocolo) não classifica termo algum.
            planejados[fid, idioma] = {i["sigla"] for i in
                                       instrumentos_do_termo(d, fid, idioma)} \
                if fid in d["instrumentos_por_faceta"] else set()
        if (r.get("instrumento") or "").strip() not in planejados[fid, idioma]:
            continue
        try:
            linha = linha_da_decisao(r.get(COLUNA_DECISAO))
        except KeyError:
            continue
        if linha is not None:
            decisoes.setdefault((fid, idioma, normaliza(r.get("termo"))), set()).add(linha)
    saida = {}
    for chave, achadas in decisoes.items():
        linha = next(x for x in G.PRECEDENCIA_LINHA if x in achadas)
        if linha != G.R_LIVRE.interno:
            saida[chave] = linha
    return saida


def esperada(mapa, fid, idioma, termo):
    return mapa.get((fid, idioma, normaliza(termo)), G.R_LIVRE.interno)
