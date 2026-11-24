"""Autoteste da geração das STRs: a STR editada à mão reprova, o termo em duas facetas
reprova e impede a gravação, a gravação regenera a STR sem tocar o resto do arquivo, a
gravação interrompida deixa o arquivo intacto, e a regra da subsunção (D2) e a unicidade
entre idiomas valem sobre os pares dos cenários da spec.

As cópias se geram da estrutura lida — "a primeira faceta", "a última faceta", "o primeiro
termo do núcleo", "um subsumido do quadro" —, e a gravação só acontece em arquivo
temporário, nunca no protocolo configurado.
"""

import os
import re
import tempfile

from .. import geracao
from .. import gramatica as G
from ..geracao import esperada, gera, subsume
from ..leitura import LINHAS
from ..saida import Saida
from . import conferir_texto
from .textos import coluna, edita_celula, sub_na_linha

R, OK = Saida.REPROVADO, Saida.OK
INVENTADO = "termo inventado na string"


def _grava_em_copia(ctx, texto):
    """Executa `strings gerar --gravar` sobre uma cópia temporária de `texto`.

    Devolve (código, texto do arquivo depois). O arquivo temporário é removido."""
    fd, caminho = tempfile.mkstemp(prefix="rsl_autoteste_", suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(texto)
        cod = gera(ctx.com_texto(texto), gravar=True, caminho=caminho, saida=lambda *_: None)
        with open(caminho, encoding="utf-8", newline="") as fh:
            return Saida(cod), fh.read()
    finally:
        if os.path.exists(caminho):
            os.unlink(caminho)


def casos(ctx, g):
    t, d = ctx.texto, ctx.protocolo()
    L = d["locais"]
    executa = conferir_texto(ctx)
    f1 = d["facetas"][0]["id"]
    fn = d["facetas"][-1]["id"]
    idx_str1 = L["string"][f1]

    # STR editada à mão: termo fora do quadro acrescentado, termo do quadro retirado e
    # subsumido reintroduzido. Os dois últimos só a igualdade com a STR gerada reprova.
    g.espera("STR com termo acrescentado à mão",
             sub_na_linha(t, idx_str1, r'\("', f'("{INVENTADO}" OR "'), t, executa, R,
             ("difere da STR gerada", INVENTADO))
    primeiro = d["strings"][f1]["literais"][0]
    g.espera("STR com termo do quadro retirado à mão",
             sub_na_linha(t, idx_str1, re.escape(f'"{primeiro}" OR '), ""), t, executa, R,
             ("difere da STR gerada", "a menos", repr(primeiro)))
    sub = None
    for f in d["tabelas"]:
        pares = esperada(f, d["idiomas"])[1]
        if pares:
            sub = (f["id"], *next(iter(pares.items())))
            break
    if sub is None:
        g.falha("mutação não aplicável: subsumido reintroduzido na STR — o quadro não tem "
                "termo subsumido")
    else:
        fs, termo, por = sub
        g.espera("STR com subsumido reintroduzido à mão",
                 sub_na_linha(t, L["string"][fs], r'\("', f'("{termo}" OR "'), t, executa,
                 R, ("difere da STR gerada", f"{termo!r} (subsumido por {por!r})"))

    # Termo em duplicidade na STR: a leitura deduplica a lista que se compara, e sem o
    # registro da repetição a STR repetida passaria em `documentos conferir` e não seria
    # regravada.
    repetida = sub_na_linha(t, idx_str1, r'\("', f'("{primeiro}" OR "')
    g.espera("STR com termo em duplicidade", repetida, t, executa, R,
             ("DUPLICIDADE", repr(primeiro), "2 ocorrências"))
    cod, depois = _grava_em_copia(ctx, repetida)
    g.testa("gravação desfaz a duplicidade e preserva o restante byte a byte",
            repetida != t and cod == OK and depois == t,
            f"código {cod.name}, {'igual' if depois == t else 'diferente'} do corrente")

    # Termo livre da primeira faceta acrescentado à linha "Termo livre" da última: atribuição
    # única violada, e a gravação recusada sem tocar no arquivo.
    q1, qn = L["quadro"][f1], L["quadro"][fn]
    livre = G.R_LIVRE.interno
    idioma = d["idiomas"][0]
    termo_f1 = next(f for f in d["tabelas"] if f["id"] == f1)["linhas"][idioma][livre][0]
    dup = edita_celula(t, qn[livre], coluna(t, qn["cabecalho"], idioma),
                       lambda c: f"{c}, {termo_f1}")
    g.espera("termo em duas facetas do quadro", dup, t, executa, R,
             ("atribuição única", repr(termo_f1), f1, fn))
    cod, depois = _grava_em_copia(ctx, dup)
    g.testa("gravação recusada com termo em duas facetas", cod == R and depois == dup,
            f"código {cod.name}, arquivo {'intacto' if depois == dup else 'ALTERADO'}")

    # Termo de "Termos sinônimos ou relacionados" na STR: a linha não entra na STR, e o termo
    # posto também na STR reprova pela remissão e pela igualdade com a STR gerada.
    rel = G.R_RELACIONADOS.interno
    so_rel = "termo relacionado do autoteste"
    com_rel = edita_celula(t, q1[rel], coluna(t, q1["cabecalho"], idioma),
                           lambda c: f"{c}, {so_rel}" if c.strip() else so_rel)
    com_rel = sub_na_linha(com_rel, idx_str1, r'\("', f'("{so_rel}" OR "')
    g.espera("termo de 'Termos sinônimos ou relacionados' posto na STR", com_rel, t, executa,
             R, ("difere da STR gerada", repr(so_rel), "que não entra na STR"))

    # Gravação: STR defasada regravada volta a ser, byte a byte, o documento corrente —
    # que o autoteste só roda sobre documento aprovado, com as STRs iguais às geradas.
    defasada = sub_na_linha(t, idx_str1, r'\("', f'("{INVENTADO}" OR "')
    cod, depois = _grava_em_copia(ctx, defasada)
    g.testa("gravação regenera a STR e preserva o restante byte a byte",
            defasada != t and cod == OK and depois == t,
            f"código {cod.name}, {'igual' if depois == t else 'diferente'} do corrente")

    # Gravação interrompida: a renomeação final falha, e o arquivo anterior fica intacto,
    # sem temporário deixado na pasta.
    intacto, restos, erro = _grava_interrompida(ctx, defasada)
    g.testa("gravação interrompida deixa o protocolo anterior intacto",
            erro and intacto and not restos,
            f"exceção {'propagada' if erro else 'AUSENTE'}, arquivo "
            f"{'intacto' if intacto else 'ALTERADO'}, temporários {restos}")

    # Regra da subsunção (D2), sobre os pares dos cenários da spec: o que deve subsumir e o
    # que não deve. Uma regra afrouxada (sem acento, hífen como separador, com flexão)
    # reprova os pares negativos; uma regra que deixa de subsumir reprova os positivos.
    for a, b, esperado, motivo in PARES_SUBSUNCAO:
        g.testa(f"subsunção: {a!r} {'subsume' if esperado else 'não subsume'} {b!r} "
                f"({motivo})", subsume(a, b) == esperado,
                f"subsume devolveu {subsume(a, b)}")
    # Mesma forma em dois idiomas da faceta: entra uma vez na STR esperada.
    idiomas = d["idiomas"]
    if len(idiomas) < 2:
        g.falha("mutação não aplicável: mesma forma em dois idiomas — o quadro tem um idioma")
    else:
        vazio = {c: [] for c in LINHAS}
        faceta = {"linhas": {i: dict(vazio) for i in idiomas}}
        faceta["linhas"][idiomas[0]] = {**vazio, LINHAS[0]: ["educacional"]}
        faceta["linhas"][idiomas[-1]] = {**vazio, LINHAS[0]: ["educacional"]}
        termos = esperada(faceta, idiomas)[0]
        g.testa("mesma forma em dois idiomas entra uma vez na STR esperada",
                termos == ["educacional"], f"STR esperada {termos}")

    # Linhas da STR: termo livre e descritores entram, nessa ordem; relacionados não.
    vazio = {c: [] for c in LINHAS}
    faceta = {"linhas": {i: dict(vazio) for i in idiomas}}
    faceta["linhas"][idiomas[0]] = {G.R_LIVRE.interno: ["livre do autoteste"],
                                    G.R_DESCRITORES.interno: ["descritor do autoteste"],
                                    G.R_RELACIONADOS.interno: ["relacionado do autoteste"]}
    termos = esperada(faceta, idiomas)[0]
    g.testa("STR esperada: termo livre e descritores, sem 'Termos sinônimos ou relacionados'",
            termos == ["livre do autoteste", "descritor do autoteste"],
            f"STR esperada {termos}")


PARES_SUBSUNCAO = (
    ("ontology", "domain ontology", True, "locução contida"),
    ("ontology", "ontology-based modeling", False, "hífen não é separador"),
    ("ontologia", "ontología de dominio", False, "acento distingue"),
    ("thesaurus", "thesauri", False, "flexão não subsume"),
    ("learning", "e-learning", False, "hífen não é separador"),
)


def _grava_interrompida(ctx, texto):
    """`strings gerar --gravar` numa cópia, com a renomeação final forçada a falhar.

    Devolve (arquivo intacto, temporários restantes na pasta, exceção propagada)."""
    pasta = tempfile.mkdtemp(prefix="rsl_autoteste_")
    caminho = os.path.join(pasta, "protocolo.md")
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        fh.write(texto)
    original, erro = geracao.os.replace, False

    def falha(*_):
        raise OSError("renomeação interrompida (autoteste)")

    geracao.os.replace = falha
    try:
        gera(ctx.com_texto(texto), gravar=True, caminho=caminho, saida=lambda *_: None)
    except OSError:
        erro = True
    finally:
        geracao.os.replace = original
    with open(caminho, encoding="utf-8", newline="") as fh:
        intacto = fh.read() == texto
    restos = sorted(n for n in os.listdir(pasta) if n != "protocolo.md")
    for n in os.listdir(pasta):
        os.unlink(os.path.join(pasta, n))
    os.rmdir(pasta)
    return intacto, restos, erro
