"""Decisão do ReT e linha do termo no controle terminológico.

A linha de um termo no CT resulta da `decisao_ReT` registrada no arquivo de decisões
(`[dados] validacao`, TOML), sobre os instrumentos planejados para a faceta e o idioma dele
(`planejamento.py`): descritor em algum instrumento → "Descritores correspondentes"; senão,
sinônimo ou relacionado em algum → "Termos sinônimos ou relacionados"; senão → "Termo livre".
Termo sem decisão, de instrumento manual ainda não consultado ou sem registro é termo livre
(plano, M3/E1: termo sem consulta registrada é termo livre). `status_proposto` é a proposta
da máquina e não classifica.

O domínio de `decisao_ReT` é fechado (gramatica.DECISAO_RET), sem distinção de caixa; o
vazio é "sem decisão". Valor fora dele é problema, não "sem decisão".
"""

from .. import gramatica as G
from ..config import relativo
from ..leitura import instrumentos_do_termo
from ..markdown import normaliza
from . import registro as R

COLUNA_DECISAO = "decisao_ReT"
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


def fora_do_dominio(tabelas):
    """[texto] de cada tabela com `decisao_ReT` fora do domínio, nomeando termo, faceta,
    idioma, instrumento e valor."""
    saida = []
    for r in tabelas or []:
        valor = (r.get(COLUNA_DECISAO) or "").strip()
        try:
            linha_da_decisao(valor)
        except KeyError:
            saida.append(f"{COLUNA_DECISAO} {valor!r} fora do domínio para {r.get('termo')!r} "
                         f"({r.get('faceta')}, {r.get('idioma')}, {r.get('instrumento')}); "
                         f"admitidos: {admitidos()}")
    return saida


def le_decisoes(texto, caminho):
    """Tabelas de decisão a partir do texto; DadosInvalidos se ilegível."""
    return R.le_decisoes(texto, caminho)


def decisoes(ctx):
    """Tabelas do arquivo de decisões do contexto; None se ele não existe."""
    texto = ctx.texto_decisoes
    if texto is None:
        return None
    return R.le_decisoes(texto, relativo(ctx.config.caminho("dados.validacao")))


def linhas_esperadas(d, tabelas):
    """{(faceta, idioma, termo normalizado): linha interna} dos termos com alguma decisão
    que não seja termo livre, só nos instrumentos planejados para a faceta e o idioma do
    termo. O termo ausente do mapa tem a linha `livre`. Valor fora do domínio é ignorado
    aqui e reprovado por `fora_do_dominio`."""
    planejados = {}
    decisoes_ = {}
    for r in tabelas or []:
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
            decisoes_.setdefault((fid, idioma, normaliza(r.get("termo"))), set()).add(linha)
    saida = {}
    for chave, achadas in decisoes_.items():
        linha = next(x for x in G.PRECEDENCIA_LINHA if x in achadas)
        if linha != G.R_LIVRE.interno:
            saida[chave] = linha
    return saida


def esperada(mapa, fid, idioma, termo):
    return mapa.get((fid, idioma, normaliza(termo)), G.R_LIVRE.interno)
