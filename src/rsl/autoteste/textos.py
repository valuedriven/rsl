"""Edição estrutural de cópias em memória: a partir da localização devolvida pelos leitores
(índice de linha em `texto.split("\\n")`), nunca de literais do documento vigente."""

import re

from ..markdown import celulas, desescapa, e_linha_de_tabela, monta_linha  # noqa: F401

FORA_DA_FORMA = "fora-da-forma"


def linhas(t):
    return t.split("\n")


def junta(ls):
    return "\n".join(ls)


def troca_linha(t, idx, nova):
    ls = linhas(t)
    ls[idx] = nova
    return junta(ls)


def remove_linhas(t, idxs):
    fora = set(idxs)
    return junta([l for k, l in enumerate(linhas(t)) if k not in fora])


def insere_depois(t, idx, nova):
    ls = linhas(t)
    ls.insert(idx + 1, nova)
    return junta(ls)


def cabecalho(t, idx):
    return [desescapa(c).strip() for c in celulas(linhas(t)[idx])]


def coluna(t, idx_cab, nome):
    return cabecalho(t, idx_cab).index(nome)


def celula(t, idx, k):
    return celulas(linhas(t)[idx])[k]


def troca_celula(t, idx, k, valor):
    ls = linhas(t)
    cels = celulas(ls[idx])
    while len(cels) <= k:
        cels.append("")
    cels[k] = valor
    ls[idx] = monta_linha(cels)
    return junta(ls)


def edita_celula(t, idx, k, funcao):
    return troca_celula(t, idx, k, funcao(celula(t, idx, k)))


def extensao_da_tabela(t, idx):
    """(primeira, última) linha da tabela que contém a linha `idx`."""
    ls = linhas(t)
    ini = fim = idx
    while ini > 0 and e_linha_de_tabela(ls[ini - 1]):
        ini -= 1
    while fim + 1 < len(ls) and e_linha_de_tabela(ls[fim + 1]):
        fim += 1
    return ini, fim


def remove_tabela(t, idx):
    ini, fim = extensao_da_tabela(t, idx)
    return remove_linhas(t, range(ini, fim + 1))


def remove_coluna(t, idx_cab, k):
    ini, fim = extensao_da_tabela(t, idx_cab)
    ls = linhas(t)
    for i in range(ini, fim + 1):
        cels = celulas(ls[i])
        ls[i] = monta_linha([c for j, c in enumerate(cels) if j != k])
    return junta(ls)


def troca_colunas(t, idx_cab, a, b):
    ini, fim = extensao_da_tabela(t, idx_cab)
    ls = linhas(t)
    for i in range(ini, fim + 1):
        cels = celulas(ls[i])
        cels[a], cels[b] = cels[b], cels[a]
        ls[i] = monta_linha(cels)
    return junta(ls)


def sub_na_linha(t, idx, padrao, novo, grupo=0):
    """Troca o primeiro casamento de `padrao` (ou o seu grupo) na linha `idx`."""
    ls = linhas(t)
    m = re.search(padrao, ls[idx])
    if not m:
        return t
    ls[idx] = ls[idx][:m.start(grupo)] + novo + ls[idx][m.end(grupo):]
    return junta(ls)


def primeira_linha(t, padrao, inicio=0, fim=None):
    """Índice da primeira linha (no intervalo) que casa `padrao`; None se nenhuma."""
    ls = linhas(t)
    fim = len(ls) if fim is None else fim
    return next((i for i in range(inicio, fim) if re.search(padrao, ls[i])), None)


def troca_termo_citado(bloco, termo, novo):
    """No texto de uma string ou bloco de base, troca a primeira ocorrência do termo
    entre aspas por `novo` (já com as aspas que quiser)."""
    alvo = f'"{termo}"'
    return bloco.replace(alvo, novo, 1) if alvo in bloco else bloco


def retira_termo_citado(bloco, termo):
    """Retira o termo entre aspas e o OR que o liga ao vizinho, com prefixo de campo."""
    padrao = r'(?:\b[A-Za-z]+:)?"' + re.escape(termo) + '"'
    m = re.search(padrao + r"\s+OR\s+", bloco) or re.search(r"\s+OR\s+" + padrao, bloco)
    return bloco[:m.start()] + bloco[m.end():] if m else bloco


def linhas_de_tabela_do_trecho(t, elemento):
    """(índice, linha) das linhas de tabela da seção `elemento` do documento `t`."""
    from ..markdown import linhas_de_tabela, secao
    return linhas_de_tabela(secao(t, elemento))


def linhas_do_trecho(t, elemento):
    """(índice, linha) das linhas da seção `elemento` (do documento inteiro, se None)."""
    from ..markdown import documento, linhas as linhas_md, secao
    return linhas_md(secao(t, elemento) if elemento is not None else documento(t))


# ------------------------------------------------------------- arquivo de sementes (TOML)
def itens_toml(texto, chave):
    """Os itens de `[[chave]]` do texto TOML, como cópia editável."""
    import tomllib
    return [dict(x) for x in tomllib.loads(texto)[chave]]


def _valor_toml(v):
    import json
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(_valor_toml(x) for x in v) + "]"
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def toml_de(itens, chave):
    """Texto TOML de uma lista de itens `[[chave]]` (textos, listas de textos, números,
    booleanos)."""
    blocos = []
    for item in itens:
        blocos.append(f"[[{chave}]]\n" +
                      "".join(f"{k} = {_valor_toml(v)}\n" for k, v in item.items()))
    return "\n".join(blocos)
