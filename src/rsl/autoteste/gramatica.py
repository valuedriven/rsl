"""Autoteste da gramática: cada elemento exigido, retirado ou deformado numa cópia do
documento, reprova com PROTOCOLO_ILEGIVEL e a mensagem nomeia o elemento.

O gerador de defeito é escolhido pelo tipo do elemento (seção, tabela, rótulo, marcador,
identificador, frase-padrão) ou, para domínio e casos sem gerador genérico, pelo nome. Elemento
exigido sem gerador faz o autoteste falhar, nomeando o elemento: a gramática não ganha
exigência que o autoteste não prove.
"""

import copy

from .. import gramatica as G
from ..coerencia import conferir
from ..dados import problemas_sondagens_registradas
from ..markdown import blocos_de_tabela, celulas, linha_do_cabecalho, normaliza, secao
from ..saida import Saida
from .fontes import com_fonte, fonte_de, registro_com_sondagem
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


def _quadro(e, t, d):
    """Quadro fora da forma: o defeito injetado é o CT sem tabela."""
    from .textos import remove_tabela                               # noqa: PLC0415
    primeiro = next(iter(d["locais"]["quadro"].values()))
    return remove_tabela(t, primeiro["cabecalho"]), e


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
    # Linha fora da forma deixa um buraco na numeração: quem reprova é o identificador.
    G.F_QER: _com_nomeado(_frase, G.I_QER),
    G.D_ANCORA: _celula_da_primeira("faceta", "cabecalho_facetas", G.D_ANCORA.campo),
    G.T_CRITERIOS: _com_nomeado(_tabela, G.I_CE),
    G.T_QUADRO: _quadro,
}


# ------------------------------------------- arquivos de esquema fechado (TOML)
_VAZIO = {"texto": "x", "lista de textos": ["x"], "inteiro": 1, "booleano": True,
          "tabela de listas": {"x": ["x"]}, "inteiro ou texto": 1, "texto ou tabela": "x",
          "tabela": {}, "lista de tabelas": []}


def _caminho(tabela):
    """Cadeia de tabelas da raiz até `tabela` (sem a raiz)."""
    cadeia = []
    while tabela is not None and tabela.chave:
        cadeia.insert(0, tabela)
        tabela = tabela.pai
    return cadeia


def _item(tabela):
    """Item mínimo da tabela, com todo campo exigido preenchido pelo tipo."""
    item = {c.chave: copy.deepcopy(c.dominio[0] if c.dominio and c.tipo_valor == "texto"
                                   else _VAZIO[c.tipo_valor])
            for c in tabela.campos if c.exigido}
    for s in tabela.subtabelas:
        if s.exigido:
            item[s.local] = [_item(s) for _ in range(s.minimo)] if s.multipla else _item(s)
    return item


def _contem(dado, tabela, cria):
    """(contêiner, chave) onde mora a tabela no dado; com `cria`, monta o que faltar."""
    atual = dado
    cadeia = _caminho(tabela)
    for k, t in enumerate(cadeia):
        nome = t.chave if t.pai is None else t.local
        if k == len(cadeia) - 1:
            return atual, nome
        if nome not in atual:
            if not cria:
                return None, None
            atual[nome] = [_item(t)] if t.multipla else _item(t)
        atual = atual[nome][0] if t.multipla else atual[nome]
    return dado, ""


def _primeiro(dado, tabela, cria):
    conteiner, nome = _contem(dado, tabela, cria)
    if conteiner is None:
        return None
    if nome not in conteiner:
        if not cria:
            return None
        conteiner[nome] = [_item(tabela)] if tabela.multipla else _item(tabela)
    v = conteiner[nome]
    return v[0] if tabela.multipla else v


def defeito_toml(e, dado):
    """Cópia do dado com o elemento `e` retirado ou deformado; None se não se aplica."""
    dado = copy.deepcopy(dado)
    if isinstance(e, G.TabelaFonte):
        if not e.chave:                         # raiz: chave fora do esquema
            dado["chave_fora_do_esquema"] = FORA_DA_FORMA
            return dado
        conteiner, nome = _contem(dado, e, cria=False)
        if conteiner is None or nome not in conteiner:
            return None
        del conteiner[nome]
        return dado
    if isinstance(e, G.CampoFonte):
        item = _primeiro(dado, e.tabela, cria=True)
        if e.tabela.chave == "":
            item = dado
        if item is None:
            return None
        item.pop(e.chave, None)
        return dado
    if e is G.I_SD:
        lista = dado.get("sondagens") or []
        if not lista:
            return None
        lista[0]["id"] = f"{G.I_SD.prefixo}99"
        return dado
    return None


def _casos_toml(ctx, g, d, e):
    """Elemento de arquivo TOML de esquema fechado: fonte, exceções ou resultado de
    sondagem."""
    if e.documento == G.F:
        alvo = next((b["sigla"] for b in d["bases"]
                     if _primeiro(fonte_de(ctx, d, b["sigla"])[0],
                                  getattr(e, "tabela", e) if not isinstance(e, G.Identificador)
                                  else G.T_SONDAGENS, cria=False) is not None),
                    d["bases"][0]["sigla"])
        dado, frag, arqs = fonte_de(ctx, d, alvo)
        mutante = defeito_toml(e, dado)
        def executa(m):
            return conferir(com_fonte(ctx, alvo, m, frag, arqs))
        g.espera(f"{e.rotulo} [{alvo}] retirado ou deformado", mutante, dado, executa,
                 Saida.PROTOCOLO_ILEGIVEL, (e.rotulo,))
        return
    if e.documento == G.X:
        import tomllib
        dado = tomllib.loads(ctx.texto_flexoes)
        mutante = defeito_toml(e, dado)
        def executa(m):
            return conferir(ctx.com_flexoes(toml_de(m.get("excecoes", []), "excecoes")
                                            if "excecoes" in m else
                                            "excecoes = 1\n"))
        g.espera(f"{e.rotulo} retirado ou deformado", mutante, dado, executa,
                 Saida.PROTOCOLO_ILEGIVEL, (e.rotulo,) if isinstance(e, G.CampoFonte)
                 else (G.T_EXCECOES.rotulo,))
        return
    # Resultado de sondagem no registro de execução: campo retirado de um resultado válido.
    sigla, reg = registro_com_sondagem(ctx, d)
    if reg is None:
        g.falha(f"mutação não aplicada: {e.rotulo} (nenhuma base declara sondagem)")
        return
    bd = next(b["id"] for b in d["bases"] if b["sigla"] == sigla)
    mut = copy.deepcopy(reg)
    if isinstance(e, G.CampoFonte):
        mut["bases"][bd]["sondagens"][0].pop(e.chave)
        trecho = e.chave
    else:
        mut["bases"][bd]["sondagens"] = {"nao": "lista"}
        trecho = "não é lista"
    antes, _ = problemas_sondagens_registradas(ctx, d, reg)
    depois, _ = problemas_sondagens_registradas(ctx, d, mut)
    g.testa(f"reprovou: {e.rotulo} [{sigla}] retirado ou deformado",
            not antes and any(trecho in x for x in depois),
            f"antes {antes[:1]}, depois {depois[:1]}")


def casos(ctx, g):
    d = ctx.protocolo()
    t = ctx.texto
    exigidos = G.exigidos()
    for e in exigidos:
        if e.documento in (G.F, G.X, G.R):
            _casos_toml(ctx, g, d, e)
            continue
        gerador = ESPECIFICOS.get(e) or GENERICOS.get(type(e))
        if gerador is None or (isinstance(e, G.Dominio) and e not in ESPECIFICOS):
            g.falha(f"elemento exigido sem gerador de defeito: {e.rotulo} ({e.documento})")
            continue
        if e.documento == G.PROTOCOLO:
            original = t
            def executa(m):
                return conferir(ctx.com_texto(m))
        else:
            original = ctx.texto_sementes
            def executa(m):
                return conferir(ctx.com_sementes(m))
        mutante, nomeado = gerador(e, original, d)
        g.espera(f"{e.rotulo} retirado ou deformado", mutante, original, executa,
                 Saida.PROTOCOLO_ILEGIVEL, (nomeado.rotulo,))
    por_doc = {doc: len([e for e in exigidos if e.documento == doc]) for doc in G.DOCUMENTOS}
    print("  (" + ", ".join(f"{n} de {doc}" for doc, n in por_doc.items())
          + " exigidos na gramática)")
