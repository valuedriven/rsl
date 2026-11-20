"""Autoteste do protocolo: defeitos injetados, precedência e leitura estrutural que aprova.

Toda cópia defeituosa é gerada da estrutura lida (`d["locais"]`): "a última semente",
"a primeira base", "a linha da expressão executada". Nada aqui depende de identificador,
sigla, termo ou valor do protocolo vigente.
"""

import re

from .. import gramatica as G
from ..fichas import _expressoes_em_negrito, consultas_curadas
from ..markdown import celulas, desescapa, linha_do_cabecalho, lista
from ..saida import Saida
from . import conferir_texto, resultado
from .textos import (cabecalho, celula, coluna, edita_celula, linhas, monta_linha,
                     remove_coluna, remove_linhas, remove_tabela, sub_na_linha, troca_celula,
                     troca_colunas, troca_linha)

R, P = Saida.REPROVADO, Saida.PROTOCOLO_ILEGIVEL
S_ = G.I_STR.prefixo
GRUPO_OR = rf"\(({S_}\d+(?:\s+OR\s+{S_}\d+)+)\)"


def _numero(ident, prefixo):
    return int(ident[len(prefixo):])


def mutacoes(ctx, g):
    t, d = ctx.texto, ctx.protocolo()
    L = d["locais"]
    executa = conferir_texto(ctx)
    casos = []

    def caso(nome, mutante, codigo, trecho):
        casos.append((nome, mutante, codigo, trecho))

    facetas = [f["id"] for f in d["facetas"]]
    f1, f2, fn = facetas[0], facetas[min(1, len(facetas) - 1)], facetas[-1]
    f3 = facetas[min(2, len(facetas) - 1)]
    idiomas = list(d["idiomas"])
    ancoradas = [f["id"] for f in d["facetas"] if f["ancora"]]
    livres = [f["id"] for f in d["facetas"] if not f["ancora"]]
    p = d["papeis"]
    especifica = sorted(p["especificas"])[0] if p["especificas"] else None
    idx_exec, idx_sonda = L["expressao"][d["executada"]], L["expressao"][d["sonda"]]
    idx_espec = L["expressao"].get(especifica)
    k_comp = G.T_EXPRESSOES.colunas.index(G.T_EXPRESSOES.colunas[2])
    k_nat = G.T_EXPRESSOES.colunas.index(G.T_EXPRESSOES.colunas[1])
    criterios = list(L["criterio"])
    bases = list(L["base"])
    sementes = list(L["semente"])
    c_bd_id, c_sigla, c_nome = G.T_BASES.colunas
    c_se_id, c_se_ref, c_se_bases, c_papel = G.T_SEMENTES.colunas
    c_i_sigla, _, c_modo, c_caminho, c_idiomas, c_fcts = G.T_INSTRUMENTOS.colunas
    cab_b, cab_s, cab_i = (L["cabecalho_bases"], L["cabecalho_sementes"],
                           L["cabecalho_instrumentos"])
    insts = list(L["instrumento"])

    def cel_inst(sigla, nome_col, valor):
        return troca_celula(t, L["instrumento"][sigla], coluna(t, cab_i, nome_col), valor)

    # --- quadro terminológico (coerência)
    q1 = L["quadro"][f1]
    rel = q1[G.R_RELACIONADOS.interno]
    mut = t
    for k in range(1, len(cabecalho(t, q1["cabecalho"]))):
        mut = troca_celula(mut, rel, k, "")
    caso("camada do quadro esvaziada", mut, R, f"camada {G.R_RELACIONADOS.interno} vazia")
    k_id0 = coluna(t, q1["cabecalho"], idiomas[0])
    nuc = q1[G.R_NUCLEO.interno]
    primeiro = re.split(G.SEPARADOR_TERMOS, celula(t, nuc, k_id0))
    primeiro = next((x.strip() for x in primeiro if x.strip()), "")
    caso("termo duplicado na mesma camada",
         edita_celula(t, nuc, k_id0, lambda c: f"\\- {primeiro} {c}"), R,
         "repetido na mesma camada")

    # --- questões
    caso("questão geral removida",
         remove_linhas(t, [linha_do_cabecalho(t, G.S_QGR)]), P, G.S_QGR.titulo)
    caso("questão específica fora de numeração",
         remove_linhas(t, [next(iter(L["qer"].values()))]), P, f"numeração {G.I_QER.prefixo}")
    caso("questão geral sem QGR", sub_na_linha(t, L["qgr"], r"^-\s*QGR:", ""), P, "QGR")

    # --- facetas
    n2 = _numero(f2, G.I_FCT.prefixo)
    caso("faceta com identificador trocado",
         sub_na_linha(t, L["faceta"][f2], rf"\(({G.I_FCT.prefixo}\d+)\)",
                      f"{G.I_FCT.prefixo}{n2 + 1}", 1),
         P, "não corresponde")
    if ancoradas:
        caso("âncora desmarcada",
             sub_na_linha(t, L["faceta"][ancoradas[-1]], G.F_ANCORA.padrao.pattern, ""),
             R, "conjunção das âncoras")
        caso("âncora com parêntese mal formado",
             sub_na_linha(t, L["faceta"][ancoradas[0]], r"\)\s*$", ""), P,
             "âncora fora da forma")
    alvo_livre = livres[0] if livres else f1
    caso("linha de faceta com travessão residual",
         troca_linha(t, L["faceta"][alvo_livre], linhas(t)[L["faceta"][alvo_livre]] +
                     " — vermelho"), P, "travessão")

    # --- strings
    caso("string fora do padrão OR", sub_na_linha(t, L["string"][f2], r" OR ", ", "), P,
         "fora do padrão")
    outra = f1 if f2 != f1 else fn
    caso("string apontando para outra faceta",
         troca_celula(t, L["string"][f2], 1, outra), P, "não casam")
    caso("termo da string fora do quadro",
         sub_na_linha(t, L["string"][f1], r'\("', '("termo inventado" OR "'), R,
         "não consta do quadro")

    # --- critérios
    dim_recorte = ctx.config.valor("conferencia.dimensao_recorte")
    dims = [x for x in d["parametros"]["dimensoes_criterio"]["valor"] if x != dim_recorte]
    if dims:
        mut = t
        for idx in L["criterio"].values():
            bruto = desescapa(celula(t, idx, G.COL_CRIT_DIMENSAO).strip("* ")).strip()
            if bruto == dims[0]:
                mut = troca_celula(mut, idx, G.COL_CRIT_DIMENSAO, dims[0] + " (renomeada)")
        caso("dimensão de critério ausente", mut, R, f"critério de {dims[0]!r}")
    ultimo_ce = L["criterio"][criterios[-1]]
    caso("critério sem justificativa", troca_celula(t, ultimo_ce, G.COL_CRIT_JUST, ""), R,
         "sem justificativa")
    caso("justificativa reduzida a traço",
         troca_celula(t, ultimo_ce, G.COL_CRIT_JUST, "—"), R, "sem justificativa")
    if len(criterios) > 1:
        caso("critério com identificador repetido",
             troca_celula(t, L["criterio"][criterios[1]], G.COL_CRIT_ID, criterios[0]), P,
             f"numeração {G.I_CE.prefixo}")
    caso("recorte temporal ilegível" if "recorte" in L else "recorte temporal (não declarado)",
         sub_na_linha(t, L["recorte"], G.F_RECORTE.padrao.pattern, "após o ano de dois mil")
         if "recorte" in L else None, P, "sem ano legível")

    # --- expressões
    if idx_espec is not None:
        anc_ult = p["ancoras"][-1][0] if p["ancoras"] else None
        caso("expressão sem âncora",
             edita_celula(t, idx_espec, k_comp,
                          lambda c: re.sub(rf"\b{anc_ult}\s+AND\s+", "", c, count=1))
             if anc_ult else None, R, "falta a âncora")
        caso("composição com `+` como conjunção",
             edita_celula(t, idx_espec, k_comp, lambda c: c.replace(" AND ", " + ")), P,
             "não é conjunção da forma estrita")
        caso("composição com operador em minúscula",
             edita_celula(t, idx_espec, k_comp, lambda c: c.replace(" AND ", " and ", 1)), P,
             "operador fora da forma estrita")
        caso("duas expressões executadas",
             troca_celula(t, idx_espec, k_nat,
                          ctx.config.valor("expressoes.natureza_executada")), P,
             "mais de uma expressão")
        str_espec = p["especificas"][especifica]
        caso("sonda que não é a conjunção das âncoras",
             edita_celula(t, idx_sonda, k_comp,
                          lambda c: c.rstrip("\\").rstrip() + f" AND {str_espec}" +
                          ("\\" if c.endswith("\\") else "")), R, "conjunção das âncoras")
    caso("executada que não é a união das específicas",
         edita_celula(t, idx_exec, k_comp,
                      lambda c: re.sub(GRUPO_OR, lambda m: m.group(1).split()[0], c, 1)),
         R, "não é a união")
    caso("composição com OR fora de parênteses",
         edita_celula(t, idx_exec, k_comp, lambda c: re.sub(GRUPO_OR, r"\1", c, 1)), P,
         "fora da forma estrita")
    caso("composição com parênteses aninhados",
         edita_celula(t, idx_exec, k_comp, lambda c: re.sub(GRUPO_OR, r"((\1))", c, 1)), P,
         "aninhados")
    cab_e = L["cabecalho_expressoes"]
    caso("cabeçalho da tabela de expressões renomeado",
         edita_celula(t, cab_e, k_comp, lambda c: c + " (renomeada)"), P, "difere do esperado")
    cels = celulas(linhas(t)[cab_e])
    cels[k_nat], cels[k_comp] = cels[k_comp], cels[k_nat]
    mut = troca_linha(t, cab_e, monta_linha(cels))
    caso("cabeçalho da tabela de expressões com colunas trocadas", mut, P,
         "difere do esperado")
    caso("composição ausente (seção de expressões removida)",
         remove_linhas(t, [linha_do_cabecalho(t, G.S_EXPRESSOES)]), P,
         G.S_EXPRESSOES.titulo)
    if "faixa" in L:
        lo, hi = d["sensibilidade"]
        caso("faixa de sensibilidade incoerente",
             sub_na_linha(t, L["faixa"], r"<\s*\**\s*(\d+(?:[.,]\d+)?)",
                          str(round(hi * 100) + 10), 1), R, "incoerente")
        caso("faixa de sensibilidade ilegível",
             sub_na_linha(t, L["faixa"], r">\s*\**\s*\d+(?:[.,]\d+)?\s*%", "acima do teto"), P,
             "falta o limite")
    caso("limiar de aderência ilegível",
         sub_na_linha(t, L["limiar"], G.F_LIMIAR.padrao.pattern,
                      "recuperação inferior a muitas") if "limiar" in L else None, P,
         "limiar legível")

    # --- bases
    caso("base removida", remove_linhas(t, [L["base"][bases[-1]]]), P, "ordem de execução")
    if len(bases) > 1:
        caso("base com identificador repetido",
             troca_celula(t, L["base"][bases[1]], coluna(t, cab_b, c_bd_id), bases[0]), P,
             f"numeração {G.I_BD.prefixo}")
        caso("sigla de base repetida",
             troca_celula(t, L["base"][bases[-1]], coluna(t, cab_b, c_sigla),
                          d["bases"][0]["sigla"]), P, "sigla repetida")
    sigla_ult = d["bases"][-1]["sigla"]
    caso("sigla de base sem ficha",
         troca_celula(t, L["base"][bases[-1]], coluna(t, cab_b, c_sigla), sigla_ult + "x"), P,
         f"ficha da sigla '{sigla_ult}x' não existe")
    caso(f"coluna {c_sigla} retirada da tabela de bases",
         remove_coluna(t, cab_b, coluna(t, cab_b, c_sigla)), P, f"falta a coluna ['{c_sigla}']")
    caso("tabela de bases ausente", remove_tabela(t, cab_b), P, "tabela ausente")

    # --- instrumentos
    caso("coluna repetida na tabela de instrumentos",
         troca_celula(t, cab_i, coluna(t, cab_i, c_caminho), c_modo), P,
         f"coluna repetida ['{c_modo}']")
    if len(insts) > 1:
        caso("instrumento com sigla repetida", cel_inst(insts[-1], c_i_sigla, insts[0]), P,
             "sigla repetida")
    caso("instrumento com campo vazio", cel_inst(insts[0], c_idiomas, ""), P, "campo vazio")
    caso("instrumento com Modo fora do domínio", cel_inst(insts[-1], c_modo, "Semiautomático"),
         P, "fora dos admitidos")
    caso("instrumento com idioma fora do quadro", cel_inst(insts[-1], c_idiomas, "xx"), P,
         "['xx'] fora")
    fcts0 = d["instrumentos"][insts[0]]["facetas"]
    caso("instrumento com faceta inexistente em FCTs",
         cel_inst(insts[0], c_fcts, ", ".join(fcts0[:-1] + [fcts0[-1] + "s"])), P,
         f"['{fcts0[-1]}s']")
    candidatas = [f for f in facetas
                  if all(len(i["facetas"]) > 1 for i in d["instrumentos"].values()
                         if f in i["facetas"])]
    mut = None
    if candidatas:
        alvo = candidatas[-1]
        mut = t
        for s, i in d["instrumentos"].items():
            if alvo in i["facetas"]:
                mut = troca_celula(mut, L["instrumento"][s], coluna(t, cab_i, c_fcts),
                                   ", ".join(x for x in i["facetas"] if x != alvo))
    caso("faceta do quadro sem instrumento", mut, P, "sem instrumento")
    automatico = next((s for s, i in d["instrumentos"].items()
                       if i["modo"] == G.MODO_AUTOMATICO), None)
    caso("instrumento Automático sem cliente",
         cel_inst(automatico, c_i_sigla, automatico + "-sem-cliente") if automatico else None,
         P, "sem cliente")
    caso("instrumento com Caminho que não é URL",
         cel_inst(insts[-1], c_caminho, "endereco sem esquema"), P, "não é URL")

    # --- quadro: idiomas pelo cabeçalho
    cab_q2 = L["quadro"][f2]["cabecalho"]
    caso("idioma repetido no cabeçalho do quadro",
         troca_celula(t, cab_q2, len(cabecalho(t, cab_q2)) - 1, idiomas[0])
         if len(idiomas) > 1 else None, P, "coluna repetida")
    cab_q3 = L["quadro"][f3]["cabecalho"]
    caso("coluna de idioma sem nome no quadro",
         troca_celula(t, cab_q3, min(2, len(cabecalho(t, cab_q3)) - 1), ""), P, "sem nome")
    cab_qn = L["quadro"][fn]["cabecalho"]
    caso("idiomas diferentes entre facetas",
         troca_celula(t, cab_qn, len(cabecalho(t, cab_qn)) - 1, "xx")
         if fn != f1 else None, P, "diferem dos idiomas")

    # --- sementes
    k_bases, k_papel = coluna(t, cab_s, c_se_bases), coluna(t, cab_s, c_papel)
    ult = sementes[-1]
    caso("semente sem base", troca_celula(t, L["semente"][ult], k_bases, ""), P,
         "semente sem base")
    s0 = d["sementes"][0]
    outra_grafia = s0["bases"][0].swapcase()
    caso("semente com sigla em outra grafia",
         edita_celula(t, L["semente"][s0["id"]], k_bases,
                      lambda c: c.replace(s0["bases"][0], outra_grafia, 1)), P,
         f"base ['{outra_grafia}']")
    caso("semente fora de numeração",
         troca_celula(t, L["semente"][ult], coluna(t, cab_s, c_se_id),
                      f"{G.I_SE.prefixo}{_numero(ult, G.I_SE.prefixo) + 1}"), P,
         f"numeração {G.I_SE.prefixo}")
    caso(f"coluna {c_papel} retirada da tabela de sementes", remove_coluna(t, cab_s, k_papel),
         P, f"falta a coluna ['{c_papel}']")
    por_papel = {e["papel"]: e["id"] for e in reversed(d["sementes"])}
    alvo_dev = por_papel.get(G.PAPEL_DESENVOLVIMENTO, sementes[0])
    caso("semente sem papel", troca_celula(t, L["semente"][alvo_dev], k_papel, ""), P,
         "papel da semente vazio")
    alvo_val = por_papel.get(G.PAPEL_VALIDACAO, sementes[0])
    caso("semente com papel fora do domínio",
         troca_celula(t, L["semente"][alvo_val], k_papel, "teste"), P, "papel 'teste' fora")
    mut = t
    for idx in L["semente"].values():
        mut = troca_celula(mut, idx, k_papel, G.PAPEL_DESENVOLVIMENTO)
    caso("conjunto-semente sem validação", mut, R, "sem semente de validação")

    for nome, mutante, codigo, trecho in casos:
        g.espera(nome, mutante, t, executa, codigo, trecho)


def precedencia(ctx, g):
    """Parâmetro ausente do protocolo vale pelo padrão, com a origem registrada."""
    t, d = ctx.texto, ctx.protocolo()
    L = d["locais"]
    origem = f"padrão ({ctx.config.nome})"
    casos = [
        ("limiar ausente do protocolo vale pelo padrão", "limiar_aderencia",
         remove_linhas(t, [L["limiar"]]) if "limiar" in L else None),
        ("âncoras não marcadas valem pelo padrão", "ancoras",
         remove_ancoras(t, d)),
    ]
    for nome, param, mutante in casos:
        if mutante is None or mutante == t:
            g.falha(f"mutação não aplicada: {nome}")
            continue
        cod, msgs = resultado(lambda: ctx.com_texto(mutante).protocolo())
        if cod != Saida.OK:
            g.falha(f"{nome}: leitura reprovou ({msgs[:1]})")
            continue
        p_ = ctx.com_texto(mutante).protocolo()["parametros"][param]
        g.testa(nome, p_["origem"] == origem
                and p_["valor"] == ctx.config.valor(f"padroes.{param}"), repr(p_))


def remove_ancoras(t, d):
    mut = t
    for idx in d["locais"]["faceta"].values():
        mut = sub_na_linha(mut, idx, G.F_ANCORA.padrao.pattern, "")
    return mut


def estrutural(ctx, g):
    """Leituras que têm de APROVAR: o leitor não pode reprovar o que é válido, e lê o valor
    pela coluna e pelo rótulo, não pela posição."""
    t, d = ctx.texto, ctx.protocolo()
    L = d["locais"]
    ls = linhas(t)

    # Nome da faceta: todo o resto da linha, hífen incluído; a âncora fica fora do nome.
    errados = []
    for f in d["facetas"]:
        bruto = desescapa(ls[L["faceta"][f["id"]]].split(":", 1)[1]).strip()
        esperado = bruto[:bruto.rfind("(")].strip() if f["ancora"] else bruto
        if f["nome"] != esperado:
            errados.append((f["id"], f["nome"], esperado))
    g.testa("nome de cada faceta lido inteiro, com hífen, sem o sufixo de âncora",
            not errados, repr(errados))
    ancoras = [f for f in d["facetas"] if f["ancora"]]
    g.testa("faceta marcada lida como âncora, sem o parêntese no nome",
            bool(ancoras) and all("(" not in f["nome"]
                                  and G.PALAVRA_ANCORA not in f["nome"] for f in ancoras),
            repr(ancoras))

    def mesmo_com(mutante, chave):
        cod, msgs = resultado(lambda: ctx.com_texto(mutante).protocolo())
        if cod != Saida.OK:
            return False, msgs[:1]
        return ctx.com_texto(mutante).protocolo()[chave] == d[chave], ""

    cab_b = L["cabecalho_bases"]
    _, c_sigla, c_nome = G.T_BASES.colunas
    mut = troca_colunas(t, cab_b, coluna(t, cab_b, c_sigla), coluna(t, cab_b, c_nome))
    igual, msg = mesmo_com(mut, "bases")
    g.testa("bases lidas pelo nome da coluna, com as colunas em outra ordem",
            mut != t and igual, f"{msg}")
    cab_s = L["cabecalho_sementes"]
    _, _, c_bases, c_papel = G.T_SEMENTES.colunas
    mut = troca_colunas(t, cab_s, coluna(t, cab_s, c_bases), coluna(t, cab_s, c_papel))
    igual, msg = mesmo_com(mut, "sementes")
    g.testa("sementes e papel lidos pelo nome da coluna, com as colunas em outra ordem",
            mut != t and igual, f"{msg}")

    dist = d["distribuicao"]
    g.testa("distribuição por papel soma estudos e incidências e tem validação",
            sum(dist["por_papel"].values()) == len(d["sementes"])
            and sum(sum(v.values()) for v in dist["por_base_papel"].values())
            == dist["incidencias"] and not dist["validacao_vazia"], repr(dist))

    # Colunas do quadro em outra ordem: cada idioma continua lido pelo nome.
    fid = d["facetas"][min(1, len(d["facetas"]) - 1)]["id"]
    cab = L["quadro"][fid]["cabecalho"]
    idiomas = list(d["idiomas"])
    if len(idiomas) > 1:
        mut = troca_colunas(t, cab, coluna(t, cab, idiomas[0]), coluna(t, cab, idiomas[1]))
        cod, msgs = resultado(lambda: conferir_texto(ctx)(mut))
        mesmos = False
        if cod == Saida.OK:
            fm = next(f for f in ctx.com_texto(mut).protocolo()["tabelas"] if f["id"] == fid)
            fo = next(f for f in d["tabelas"] if f["id"] == fid)
            mesmos = all(fm["termos"][x] == fo["termos"][x] for x in idiomas)
        g.testa(f"quadro de {fid} com as colunas `{idiomas[1]} | {idiomas[0]}` aprova e lê "
                f"cada idioma pelo nome", mut != t and cod == Saida.OK and mesmos, f"{msgs[:1]}")
    else:
        g.falha("quadro com colunas de idioma em outra ordem: o protocolo tem um só idioma")

    # Forma curada: símbolo gráfico sem FCTn não atribui faceta.
    f1 = d["facetas"][0]["id"]
    curadas = consultas_curadas("#### Grupo\n| n | Consulta | Facetas |\n| - | - | - |\n"
                                f"| 1 | `consulta` | 🟦 |\n| 2 | `consulta` | {f1} |\n")
    g.testa("consulta curada marcada só por símbolo fica sem faceta; FCTn atribui",
            "facetas" not in curadas[0] and curadas[1].get("facetas") == [f1], repr(curadas))

    # Forma longa: representação não executada, marcada para ficar fora da conferência
    # de bloco que recusa a derivada padrão.
    eb = sorted(d["expressoes"])[0]
    longa = _expressoes_em_negrito(f"**{eb}** geral\n\n```\nconsulta\n```\n")
    g.testa("forma longa é derivada marcada e não entra na conferência de bloco",
            eb in longa and longa[eb]["estatuto"] == "derivada"
            and longa[eb].get("forma_longa") is True, repr(longa))
