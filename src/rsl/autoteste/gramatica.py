"""Autoteste da gramática: cada elemento exigido, retirado ou deformado numa cópia do
documento, reprova com PROTOCOLO_ILEGIVEL e a mensagem nomeia o elemento.

O gerador de defeito é escolhido pelo tipo do elemento (seção, tabela, rótulo, marcador,
identificador, frase-padrão) ou, para domínio e casos sem gerador genérico, pelo nome. Elemento
exigido sem gerador faz o autoteste falhar, nomeando o elemento: a gramática não ganha
exigência que o autoteste não prove.
"""

from .. import gramatica as G
from ..conferencia import conferir
from ..fichas import ficha
from ..markdown import blocos_de_tabela, celulas, linha_do_cabecalho, normaliza, secao
from ..saida import Saida
from .textos import (FORA_DA_FORMA, coluna, edita_celula, itens_toml,
                     linhas_de_tabela_do_trecho,
                     linhas_do_trecho, remove_linhas, sub_na_linha, toml_de, troca_celula)


# --------------------------------------------------------------- geradores por tipo
def _secao(e, t, d):
    return remove_linhas(t, [linha_do_cabecalho(t, e)]), e


def _tabela(e, t, d):
    blocos = [b for b in blocos_de_tabela(secao(t, e.secao))]
    if not blocos:
        return None, e
    if e.modo == "posicional":
        idxs = [b.primeira + k for b in blocos for k in range(len(b))]
        return remove_linhas(t, idxs), e
    cab = blocos[0].primeira
    return edita_celula(t, cab, 0, lambda c: c + "-renomeada"), e


def _rotulo(e, t, d):
    for idx, linha in linhas_de_tabela_do_trecho(t, e.secao):
        primeira = celulas(linha)[0].strip("* ").strip()
        if normaliza(primeira).startswith(normaliza(e.texto)):
            return troca_celula(t, idx, 0, "rótulo-desconhecido"), e
    return None, e


def _marcador(e, t, d):
    for idx, linha in linhas_do_trecho(t, e.secao):
        if e.padrao.search(linha):
            return remove_linhas(t, [idx]), e
    return None, e


def _identificador(e, t, d):
    for idx, linha in linhas_do_trecho(t, e.secao):
        if e.padrao.search(linha):
            return sub_na_linha(t, idx, e.padrao.pattern, "99", 1), e
    return None, e


def _frase(e, t, d):
    for idx, linha in linhas_do_trecho(t, e.secao):
        if e.padrao.search(linha):
            return sub_na_linha(t, idx, e.padrao.pattern, FORA_DA_FORMA), e
    return None, e


GENERICOS = {G.Secao: _secao, G.Tabela: _tabela, G.RotuloLinha: _rotulo,
             G.Marcador: _marcador, G.Identificador: _identificador, G.FrasePadrao: _frase}


# ---------------------------------------------------------- geradores por elemento
def _celula_da_primeira(locais_chave, cabecalho_chave, nome_coluna):
    def gera(e, t, d):
        L = d["locais"]
        idx = next(iter(L[locais_chave].values()))
        return troca_celula(t, idx, coluna(t, L[cabecalho_chave], nome_coluna),
                            FORA_DA_FORMA), e
    return gera


def _acao(e, t, d):
    idx = next(iter(d["locais"]["criterio"].values()))
    return troca_celula(t, idx, G.COL_CRIT_ACAO, FORA_DA_FORMA), e


def _no_primeiro_item(campo, funcao):
    """Arquivo de sementes: o campo do primeiro item editado por `funcao` (None o retira)."""
    def gera(e, t, d):
        itens = itens_toml(t, G.TT_SEMENTES.chave)
        valor = funcao(itens[0][campo])
        if valor is None:
            del itens[0][campo]
        else:
            itens[0][campo] = valor
        return toml_de(itens, G.TT_SEMENTES.chave), e
    return gera


def _tabela_toml(e, t, d):
    return t.replace(f"[[{e.chave}]]", f"[[{e.chave}-renomeada]]"), e


def _campo_toml(e, t, d):
    return _no_primeiro_item(e.chave, lambda v: None)(e, t, d)


GENERICOS.update({G.TabelaToml: _tabela_toml, G.CampoToml: _campo_toml})


def _string_base(e, t, d):
    for idx, linha in linhas_do_trecho(t, e.secao):
        if linha.startswith("###") and e.padrao.search(linha):
            return sub_na_linha(t, idx, G.I_FCT.padrao.pattern, ""), e
    return None, e


def _valor_do_rotulo(rotulo):
    def gera(e, t, d):
        for idx, linha in linhas_de_tabela_do_trecho(t, rotulo.secao):
            if normaliza(celulas(linha)[0]).startswith(normaliza(rotulo.texto)):
                return troca_celula(t, idx, 1, FORA_DA_FORMA), e
        return None, e
    return gera


def _execucao(e, t, d):
    m = G.MF_EXECUCAO.padrao.search(t)
    if not m:
        return None, e
    return t[:m.start(1)] + FORA_DA_FORMA + t[m.end(1):], e


def _com_nomeado(gerador, nomeado):
    """O defeito é detectado por outro elemento, que a mensagem nomeia."""
    def gera(e, t, d):
        mutante, _ = gerador(e, t, d)
        return mutante, nomeado
    return gera


ESPECIFICOS = {
    G.D_MODO: _celula_da_primeira("instrumento", "cabecalho_instrumentos",
                                       G.D_MODO.campo),
    G.D_ACAO: _acao,
    G.D_PAPEL: _no_primeiro_item(G.C_PAPEL.chave, lambda v: FORA_DA_FORMA),
    G.F_STRING_BASE: _string_base,
    G.D_CAMADAS: _valor_do_rotulo(G.RF_CAMADAS),
    G.D_PLURAL: _valor_do_rotulo(G.RF_PLURAL),
    G.D_TETO: _valor_do_rotulo(G.RF_TETO),
    G.D_EXECUCAO: _execucao,
    # Linha fora da forma deixa um buraco na numeração: quem reprova é o identificador.
    G.F_QER: _com_nomeado(_frase, G.I_QER),
    G.D_ANCORA: _celula_da_primeira("faceta", "cabecalho_facetas", G.D_ANCORA.campo),
    G.T_CRITERIOS: _com_nomeado(_tabela, G.I_CE),
    # Sem a tabela da declaração, a primeira exigência que falta é a dos idiomas.
    G.TF_DECLARACAO: _com_nomeado(_tabela, G.RF_IDIOMAS),
}


def casos(ctx, g):
    d = ctx.protocolo()
    t = ctx.texto
    sigla = d["bases"][0]["sigla"]
    t_ficha = ficha(ctx, d, sigla)
    exigidos = G.exigidos()
    for e in exigidos:
        gerador = ESPECIFICOS.get(e) or GENERICOS.get(type(e))
        if gerador is None or (isinstance(e, G.Dominio) and e not in ESPECIFICOS):
            g.falha(f"elemento exigido sem gerador de defeito: {e.rotulo} ({e.documento})")
            continue
        if e.documento == G.PROTOCOLO:
            original = t
            def executa(m):
                return conferir(ctx.com_texto(m))
        elif e.documento == G.SEMENTES:
            original = ctx.texto_sementes
            def executa(m):
                return conferir(ctx.com_sementes(m))
        else:
            original = t_ficha
            def executa(m):
                return conferir(ctx.com_fichas({sigla: m}))
        mutante, nomeado = gerador(e, original, d)
        onde = f" [{sigla}]" if e.documento == G.FICHA else ""
        g.espera(f"{e.rotulo}{onde} retirado ou deformado", mutante, original, executa,
                 Saida.PROTOCOLO_ILEGIVEL, (nomeado.rotulo,))
    print(f"  ({len(exigidos)} elementos exigidos na gramática, "
          f"{len([e for e in exigidos if e.documento == G.FICHA])} da ficha de base, "
          f"{len([e for e in exigidos if e.documento == G.SEMENTES])} do arquivo de sementes)")
