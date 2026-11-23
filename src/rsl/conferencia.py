"""Conferência da coerência interna do protocolo e dos procedimentos de busca.

A conferência verifica a coerência do documento, não valores esperados. Protocolo fora da
gramática não chega aqui como problema: a leitura levanta ProtocoloInvalido, que sobe até o
ponto de entrada com o código PROTOCOLO_ILEGIVEL. Procedimento de busca fora da gramática
reprova só a sua base, como problema de código PROTOCOLO_ILEGIVEL; as demais bases seguem
conferidas.
"""

from . import gramatica as G
from .cobertura import (cobertura_base, maior_consulta, numero_unico_na_base,
                        subsumidos_na_base)
from .erros import ProtocoloInvalido
from .fichas import base_derivada
from .geracao import problemas_atribuicao, problemas_str
from .leitura import CAMADAS
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


def problemas_bases(ctx, d):
    """Problemas de cada base, isolados: procedimento de busca ilegível reprova só a sua base."""
    problemas = []
    for b in d["bases"]:
        sigla = b["sigla"]
        try:
            base = base_derivada(ctx, d, sigla)
            problemas += [Problema(f"{sigla}: {p}") for p in cobertura_base(base, d)]
        except ProtocoloInvalido as e:
            problemas.append(Problema(f"{sigla}: {e}", e.codigo))
    return problemas


def conferir(ctx):
    """Problemas encontrados (Resultado). ProtocoloInvalido sobe: é outro código."""
    d = ctx.protocolo()
    problemas = []

    for f in d["tabelas"]:
        for i in d["idiomas"]:
            for c in CAMADAS:
                if not f["camadas"][i][c]:
                    problemas.append(f"faceta {f['id']}: camada {c} vazia em {i}")
        # Repetição entre camadas é legítima (o mesmo termo em núcleo e em relacionados);
        # a lista final é deduplicada. Dentro da mesma camada, é defeito.
        for i in d["idiomas"]:
            for c in CAMADAS:
                vistos = set()
                for termo in f["camadas"][i][c]:
                    k = normaliza(termo)
                    if k in vistos:
                        problemas.append(
                            f"faceta {f['id']} {i}/{c}: {termo!r} repetido na mesma camada")
                    vistos.add(k)

    # A string só pode usar termo que o quadro da própria faceta contém. É a remissão que
    # impede string e vocabulário de divergirem em silêncio.
    minimo = d["parametros"]["minimo_termos_string"]["valor"]
    quadro = {f["id"]: {normaliza(x) for i in d["idiomas"] for x in f["termos"][i]}
              for f in d["tabelas"]}
    for n, s in d["strings"].items():
        if len(s["termos"]) < minimo:
            problemas.append(f"faceta {n}: string com {len(s['termos'])} termos "
                             f"(mínimo {minimo})")
        for termo in s["termos"]:
            if normaliza(termo) not in quadro[n]:
                problemas.append(f"faceta {n}: termo {termo!r} da string não consta do "
                                 f"quadro da faceta")

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

    # Sem semente de validação a aderência decisória não tem denominador: o defeito é
    # impedido na leitura, não descoberto em M3/E2.
    if d["distribuicao"]["validacao_vazia"]:
        problemas.append("conjunto-semente sem semente de validação: a aderência que decide "
                         "a passagem não teria denominador")

    resultado = Resultado(Problema(p) for p in problemas)
    # A forma de cada base é parte da coerência do documento: procedimento de busca ilegível
    # ou fora do protocolo reprova só a sua base.
    resultado += problemas_bases(ctx, d)
    return resultado


def relatos(ctx, d):
    """Achados que não reprovam, por base: subsumidos usados na string da base, a maior
    consulta da base sem teto de caracteres e termos numa só forma de número em procedimento
    de busca de plural explícito."""
    saida = []
    for b in d["bases"]:
        sigla = b["sigla"]
        try:
            base = base_derivada(ctx, d, sigla)
        except ProtocoloInvalido:
            continue                      # já reprovada em problemas_bases
        for fid, sid, termo, por in subsumidos_na_base(base, d):
            saida.append(f"{sigla}: {sid} ({fid}): {termo!r} subsumido por {por!r} da STR")
        maior = maior_consulta(base)
        if base["declaracao"].get("teto") is None and maior:
            n, ident, rotulo = maior
            saida.append(f"{sigla}: teto de caracteres {G.TETO_NENHUM!r}; a maior consulta "
                         f"executável tem {n} caracteres ({ident}, {rotulo[:50]!r})")
        unicos = {}
        for fid, termo in numero_unico_na_base(base, d):
            unicos.setdefault(fid, []).append(termo)
        for fid, termos in sorted(unicos.items()):
            saida.append(f"{sigla}: {fid}: {len(termos)} termo(s) numa só forma de número, "
                         f"com plural explícito: {', '.join(map(repr, termos))}")
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
