"""Conferência da coerência interna do protocolo, da fonte de cada procedimento de busca e
do procedimento gravado.

A conferência verifica a coerência do documento, não valores esperados. Protocolo fora da
gramática não chega aqui como problema: a leitura levanta ProtocoloInvalido, que sobe até o
ponto de entrada com o código PROTOCOLO_ILEGIVEL. Fonte de procedimento fora da gramática
reprova só a sua base, como problema de código PROTOCOLO_ILEGIVEL; as demais bases seguem
conferidas. O procedimento gravado é saída: confere-se por igualdade com a geração.
"""

from . import gramatica as G
from .cobertura import listas_a_mao, cobertura_base, maior_consulta, subsumidos_na_base
from .erros import DadosInvalidos, ProtocoloInvalido
from .derivado import base_derivada
from .flexao import le_excecoes, orfas
from .geracao import candidatos, problemas_atribuicao, problemas_str
from .leitura import LINHAS, confere_referencia_curta, referencia_curta_sugerida
from .markdown import normaliza
from .saida import Saida, mais_grave


class Problema(str):
    """Texto do problema com o código de saída que ele impõe."""

    def __new__(cls, texto, codigo=Saida.REPROVADO):
        obj = super().__new__(cls, texto)
        obj.codigo = Saida(codigo)
        return obj


class Resultado(list):
    """Lista de problemas; vazia = documento coerente. `codigo`: o mais grave."""

    @property
    def codigo(self):
        return mais_grave(*(p.codigo for p in self)) if self else Saida.OK


def coerencia_expressoes(d):
    """Relações entre as expressões, sem valor esperado: âncoras e executada."""
    problemas = []
    p = d["papeis"]
    comp, exec_ = d["expressoes"], p["executada"]
    existentes = {s["id"] for s in d["strings"].values()}
    if p["ancoras_sem_string"]:
        return [f"âncoras {p['ancoras_sem_string']} não são facetas com string no protocolo"]
    ancora = p["ancoras"]

    for ident, grupos in sorted(comp.items()):
        fora = sorted({x for g in grupos for x in g} - existentes)
        if fora:
            problemas.append(f"{ident}: composição cita string inexistente {fora}")
        for g in ancora:
            if g not in grupos:
                problemas.append(f"{ident}: falta a âncora obrigatória {g[0]}")
    # A sonda ser a conjunção das âncoras é garantido pela identificação (leitura).
    resto = [g for g in comp.get(exec_, []) if g not in ancora]
    especificas = p["especificas"]
    uniao = sorted(set(especificas.values()))
    if len(resto) != 1 or not uniao or sorted(resto[0]) != uniao:
        problemas.append(f"a executada {exec_} não é a união das específicas "
                         f"{sorted(especificas)}: além das âncoras tem {resto}, "
                         f"esperado [{uniao}]")
    return problemas


def problemas_bases(ctx, d, igualdade=True):
    """Problemas de cada base, isolados: fonte ilegível reprova só a sua base. Com
    `igualdade`, o procedimento gravado que difere da geração também reprova a base."""
    from .procedimentos import problemas_igualdade                  # noqa: PLC0415
    try:
        excecoes = le_excecoes(ctx)
    except ProtocoloInvalido as e:
        return [Problema(str(e), e.codigo)]
    problemas = []
    for b in d["bases"]:
        sigla = b["sigla"]
        try:
            base = base_derivada(ctx, d, sigla)
            comp = base["comp"]
            if comp.indecidiveis:
                problemas.append(Problema(
                    f"{sigla}: flexão indecidível, sem exceção declarada — " + "; ".join(
                        f"{e.termo!r} ({e.idioma}): {e.motivo}" for e in comp.indecidiveis)))
            problemas += [Problema(f"{sigla}: {p}") for p in cobertura_base(base, d, excecoes)]
        except ProtocoloInvalido as e:
            problemas.append(Problema(f"{sigla}: {e}", e.codigo))
        except Exception as e:                                      # noqa: BLE001
            from .erros import Reprovado                            # noqa: PLC0415
            if not isinstance(e, Reprovado):
                raise
            problemas.append(Problema(str(e)))
    if igualdade:
        problemas += [Problema(f"{s}: {x}") for s, x in problemas_igualdade(ctx, d)]
    return problemas


def problemas_classificacao(ctx, d):
    """A linha de cada termo do CT confere com a decisão do ReT (`termos/decisao.py`).

    Cada termo tem uma única linha esperada por idioma: a repetição entre linhas do mesmo CT
    e idioma reprova. Termo fora da linha esperada reprova; sem planilha a linha esperada é
    "Termo livre", e o termo em outra linha reprova, porque o protocolo afirmaria uma
    classificação não verificada. Planilha ilegível não é planilha ausente: DADOS.
    """
    from .termos.decisao import ROTULO, esperada, fora_do_dominio, linhas_esperadas, planilha
    saida = []
    for f in d["tabelas"]:
        for i in d["idiomas"]:
            onde = {}
            for c in LINHAS:
                for termo in f["linhas"][i][c]:
                    onde.setdefault(normaliza(termo), (termo, []))
                    if c not in onde[normaliza(termo)][1]:
                        onde[normaliza(termo)][1].append(c)
            for termo, cs in onde.values():
                if len(cs) > 1:
                    saida.append(Problema(
                        f"faceta {f['id']} {i}: {termo!r} em mais de uma linha do "
                        f"{f['ct']} ({', '.join(repr(ROTULO[c]) for c in cs)}); cada termo "
                        f"tem uma única linha"))
    try:
        linhas = planilha(ctx)
    except DadosInvalidos as e:
        return saida + [Problema(str(e), Saida.DADOS)]
    origem = "pela decisão do ReT" if linhas is not None else \
        "sem planilha de validação, todo termo é termo livre"
    saida += [Problema(f"planilha de validação: {x}") for x in fora_do_dominio(linhas or [])]
    mapa = linhas_esperadas(d, linhas)
    for f in d["tabelas"]:
        for i in d["idiomas"]:
            for c in LINHAS:
                for termo in f["linhas"][i][c]:
                    e = esperada(mapa, f["id"], i, termo)
                    if e != c:
                        saida.append(Problema(
                            f"faceta {f['id']} {i}: {termo!r} na linha {ROTULO[c]!r} do "
                            f"{f['ct']}; a linha esperada é {ROTULO[e]!r} ({origem})"))
    return saida


def conferir(ctx):
    """Problemas encontrados (Resultado). ProtocoloInvalido sobe: é outro código."""
    d = ctx.protocolo()
    problemas = []

    # Célula vazia é admitida: sem decisão de validação, as linhas de descritores e de
    # sinônimos ou relacionados ficam vazias, e essa é a classificação correta.
    for f in d["tabelas"]:
        for i in d["idiomas"]:
            for c in LINHAS:
                vistos = set()
                for termo in f["linhas"][i][c]:
                    k = normaliza(termo)
                    if k in vistos:
                        problemas.append(
                            f"faceta {f['id']} {i}/{c}: {termo!r} repetido na mesma linha do CT")
                    vistos.add(k)

    # A string só pode usar termo das linhas do CT da própria faceta que compõem a STR
    # (termo livre e descritores). É a remissão que impede string e vocabulário de
    # divergirem em silêncio. Não há mínimo de termos por string (retirado em 2026-11-24).
    rotulos = " e ".join(repr(r.texto) for r in G.LINHAS_STR)
    quadro = {f["id"]: {normaliza(x) for x in candidatos(f, d["idiomas"])}
              for f in d["tabelas"]}
    for n, s in d["strings"].items():
        for termo in s["termos"]:
            if normaliza(termo) not in quadro[n]:
                problemas.append(f"faceta {n}: termo {termo!r} da string não consta das "
                                 f"linhas {rotulos} do CT da faceta")

    # A STR é saída de geração a partir do quadro: a editada à mão, ou a que ficou para trás
    # de uma alteração do quadro, reprova mesmo sem que ninguém rode o gerador. E o quadro
    # com termo em duas facetas faria as STRs geradas se implicarem.
    problemas += problemas_str(d)
    problemas += problemas_atribuicao(d)

    problemas += coerencia_expressoes(d)

    # Justificativa é afirmação de decisão: célula vazia, só com espaço ou com traço não a
    # contém. A conferência garante que existe; não avalia o conteúdo.
    coluna = G.T_CRITERIOS.colunas[G.COL_CRIT_JUST]
    for c in d["criterios"]:
        if not c["justificativa"].strip(" \t-–—"):
            problemas.append(f"critério {c['id']} sem justificativa (coluna "
                             f"'{coluna}' vazia)")

    dimensoes = {c["dimensao"] for c in d["criterios"]}
    for esperada in d["parametros"]["dimensoes_criterio"]["valor"]:
        if esperada not in dimensoes:
            problemas.append(f"critério de {esperada!r} não declarado (dimensões do "
                             f"protocolo: {sorted(dimensoes)})")
    lo, hi = d["sensibilidade"]
    if not 0 <= lo < hi <= 1:
        problemas.append(f"faixa de sensibilidade incoerente: {lo:.0%} a {hi:.0%}")
    if not 0 < d["limiar"] <= 1:
        problemas.append(f"limiar de aderência incoerente: {d['limiar']:.0%}")

    if d["fontes"]["ordem_execucao"] != [b["nome"] for b in d["fontes"]["bases"]]:
        problemas.append(f"ordem de execução {d['fontes']['ordem_execucao']} difere da "
                         f"numeração das bases")

    if not d["questoes"]["questao_principal"]:
        problemas.append("questão geral vazia")

    # Base e procedimento de busca de cada semente são lidas e conferidas pelo leitor (sigla
    # da tabela de bases, procedimento de busca existente); a distribuição é calculada da
    # tabela, sem prosa a conferir.
    for e in d["sementes"]:
        if not e["titulo"] or len(e["titulo"]) < 12:
            problemas.append(f"semente {e['id']}: título não legível ({e['titulo']!r})")
        motivo = confere_referencia_curta(e)
        if motivo:
            problemas.append(f"semente {e['id']}: referencia_curta "
                             f"{e['referencia_curta']!r} não confere com o item do Zotero — "
                             f"{motivo}; forma sugerida: "
                             f"{referencia_curta_sugerida(e['zotero'])!r}")

    resultado = Resultado(Problema(p) for p in problemas)
    resultado += problemas_classificacao(ctx, d)
    # A forma de cada base é parte da coerência do documento: procedimento de busca ilegível
    # ou fora do protocolo reprova só a sua base.
    resultado += problemas_bases(ctx, d)
    return resultado


def relatos(ctx, d):
    """Achados que não reprovam: subsumidos usados nos blocos da base, a maior consulta da
    base sem teto de caracteres, exceções de flexão órfãs e sondagens sem elemento."""
    saida = []
    try:
        excecoes = le_excecoes(ctx)
    except ProtocoloInvalido:
        excecoes = {}
    derivadas = {}
    for b in d["bases"]:
        try:
            derivadas[b["sigla"]] = base_derivada(ctx, d, b["sigla"])
        except Exception:                                           # noqa: BLE001
            continue                      # já reprovada em problemas_bases
    a_mao = {t for base in derivadas.values() for _, _, termos in listas_a_mao(base)
             for t in termos}
    for termo, idioma in orfas(excecoes, d, a_mao):
        saida.append(f"exceção de flexão órfã: {termo!r} ({idioma}) não está em nenhuma STR "
                     f"nem em subconjunto ou forma curada de base alguma")
    for b in d["bases"]:
        sigla = b["sigla"]
        base = derivadas.get(sigla)
        if base is None:
            continue
        for fid, sid, termo, por in subsumidos_na_base(base, d):
            saida.append(f"{sigla}: {sid} ({fid}): {termo!r} subsumido por {por!r} da STR")
        maior = maior_consulta(base)
        if base["declaracao"].get("teto") is None and maior:
            n, ident, rotulo = maior
            saida.append(f"{sigla}: teto de caracteres {G.TETO_NENHUM!r}; a maior consulta "
                         f"executável tem {n} caracteres ({ident}, {rotulo[:50]!r})")
        listados = {e for s in base["fonte"]["sondagens"].values() for e in s["elementos"]}
        for sd, s in sorted(base["fonte"]["sondagens"].items()):
            if not s["elementos"]:
                saida.append(f"{sigla}: sondagem {sd} sem elemento")
        del listados
    return saida


def imprime_relatos(ctx):
    try:
        linhas_ = relatos(ctx, ctx.protocolo())
    except ProtocoloInvalido:
        return
    if linhas_:
        print("RELATOS (não reprovam):")
        for x in linhas_:
            print("  -", x)
        print()


def imprime_problemas(problemas):
    print("PROBLEMAS:")
    for p in problemas:
        print("  -", p)


def cmd_conferir(ctx, a=None):
    from .relatorio import relatorio                                # noqa: PLC0415
    resultado = conferir(ctx)
    imprime_relatos(ctx)
    if resultado:
        imprime_problemas(resultado)
        return resultado.codigo
    print("Documento na forma esperada.\n")
    print(relatorio(ctx, ctx.protocolo()))
    return Saida.OK
