"""Geração das strings de busca por faceta (STR) a partir do quadro terminológico.

A STR esperada de uma faceta é a união dos termos do quadro dessa faceta — três camadas,
idiomas do cabeçalho — menos os subsumidos por outro termo da mesma STR. O quadro é a fonte;
a tabela "Strings de busca por faceta" do protocolo é saída de geração, regravada por
`strings gerar --gravar` e conferida por `conferir`.

Subsunção (D2): `a` subsume `b` quando as palavras de `a` aparecem, contíguas e na mesma
ordem, em `b`, com a mesma grafia — acento e hífen inclusive, sem flexão. A regra é
conservadora porque o tratamento de diacrítico e de hífen pelas bases não está medido:
deixar de retirar custa comprimento; retirar demais custa recall.
"""

import os
import re
import tempfile

from . import gramatica as G
from .erros import ProtocoloInvalido
from .leitura import CAMADAS
from .markdown import celulas, linhas_de_tabela, normaliza, secao
from .saida import Saida


# ---------------------------------------------------------------------- subsunção
def _palavras(termo):
    """Palavras do termo, separadas só por espaço: o hífen pertence à palavra."""
    return termo.split()


def subsume(a, b):
    """`a` subsume `b`: as palavras de `a`, contíguas e na ordem, com a mesma grafia, em `b`."""
    pa, pb = _palavras(a), _palavras(b)
    if not pa or len(pa) >= len(pb):
        return False
    return any(pb[i:i + len(pa)] == pa for i in range(len(pb) - len(pa) + 1))


def subsumidos(termos):
    """{subsumido: termo que o subsume}, sobre uma lista de termos.

    O termo que subsume é o primeiro, na ordem da lista, que não é ele mesmo subsumido —
    é o que fica na STR. A contiguidade é transitiva, de modo que esse termo sempre existe.
    """
    sub = {b for b in termos if any(subsume(a, b) for a in termos)}
    saida = {}
    for b in termos:
        if b in sub:
            saida[b] = next(a for a in termos if a not in sub and subsume(a, b))
    return saida


# ------------------------------------------------------------------- STR esperada
def candidatos(f, idiomas):
    """Termos do quadro da faceta na ordem da STR: idioma do cabeçalho, camada, célula.

    A forma repetida — entre camadas ou entre idiomas — entra uma vez. A repetição se
    reconhece pela grafia exata, como a subsunção: `ontologia` e `ontología` são duas
    formas, porque o tratamento de diacrítico pelas bases não está medido.
    """
    return list(dict.fromkeys(x for i in idiomas for c in CAMADAS for x in f["camadas"][i][c]))


def esperada(f, idiomas):
    """(termos da STR esperada, {subsumido: termo que o subsume})."""
    todos = candidatos(f, idiomas)
    sub = subsumidos(todos)
    return [x for x in todos if x not in sub], sub


def texto_str(termos):
    """A célula de string: termos entre aspas ligados por OR, entre parênteses."""
    return "(" + " OR ".join(f'"{t}"' for t in termos) + ")"


def diferencas(d):
    """Diferença de cada faceta entre a STR do protocolo e a esperada.

    {fid: {"esperada", "subsumidos", "acrescentar", "retirar", "duplicados", "ordem"}}, só
    para as facetas que diferem. `duplicados` é {termo: ocorrências} dos termos que a STR do
    protocolo traz mais de uma vez; `ordem` é verdadeiro quando os termos coincidem, sem
    duplicidade, e só a ordem difere.
    """
    saida = {}
    for f in d["tabelas"]:
        fid = f["id"]
        termos, sub = esperada(f, d["idiomas"])
        atual = d["strings"][fid]["literais"]
        duplicados = d["strings"][fid].get("repetidos", {})
        if atual == termos and not duplicados:
            continue
        a_mais = [t for t in atual if t not in termos]
        a_menos = [t for t in termos if t not in atual]
        saida[fid] = {"esperada": termos, "subsumidos": sub,
                      "acrescentar": a_menos, "retirar": a_mais, "duplicados": duplicados,
                      "ordem": not a_mais and not a_menos and not duplicados}
    return saida


def duplicidade(termo, vezes):
    """A mensagem única da duplicidade, usada pela geração e por `conferir`."""
    return f"{termo!r} em DUPLICIDADE: {vezes} ocorrências na STR; a STR gerada o traz uma vez"


def descreve(fid, dif, d):
    """Linhas legíveis da diferença de uma faceta, com o motivo de cada retirada."""
    sid = d["strings"][fid]["id"]
    if dif["ordem"]:
        return [f"{sid} ({fid}): mesmos termos, ordem diferente da do quadro"]
    saida = [f"{sid} ({fid}): {len(dif['acrescentar'])} a acrescentar, "
             f"{len(dif['retirar'])} a retirar, {len(dif['duplicados'])} em duplicidade"]
    for t, n in dif["duplicados"].items():
        saida.append(f"    ! {duplicidade(t, n)}")
    for t in dif["acrescentar"]:
        saida.append(f"    + {t!r}")
    for t in dif["retirar"]:
        if t in dif["subsumidos"]:
            motivo = f"subsumido por {dif['subsumidos'][t]!r}"
        else:
            motivo = "não consta do quadro da faceta"
        saida.append(f"    - {t!r} ({motivo})")
    return saida


# ------------------------------------------------------------- atribuição única
def atribuicao_unica(d):
    """Formas normalizadas presentes no quadro de mais de uma faceta.

    Devolve [(forma do primeiro quadro, [facetas])]. A mesma forma em idiomas ou camadas
    da mesma faceta não conta: a regra incide entre facetas.
    """
    onde, grafia = {}, {}
    for f in d["tabelas"]:
        for x in candidatos(f, d["idiomas"]):
            k = normaliza(x)
            grafia.setdefault(k, x)
            onde.setdefault(k, [])
            if f["id"] not in onde[k]:
                onde[k].append(f["id"])
    return [(grafia[k], fs) for k, fs in onde.items() if len(fs) > 1]


def problemas_atribuicao(d):
    return [f"{x!r} consta do quadro de {' e '.join(fs)}: cada termo pertence a uma faceta "
            f"só (atribuição única)" for x, fs in atribuicao_unica(d)]


def problemas_str(d):
    """Problemas de STR divergente da esperada, para `conferir`."""
    saida = []
    for fid, dif in sorted(diferencas(d).items()):
        sid = d["strings"][fid]["id"]
        if dif["ordem"]:
            saida.append(f"{sid}: mesmos termos da STR gerada, em ordem diferente da do "
                         f"quadro; corrigir com `strings gerar --gravar`")
            continue
        partes = [duplicidade(t, n) for t, n in dif["duplicados"].items()]
        if dif["retirar"]:
            itens = [f"{t!r} (subsumido por {dif['subsumidos'][t]!r})"
                     if t in dif["subsumidos"] else repr(t) for t in dif["retirar"]]
            partes.append(f"a mais: {', '.join(itens)}")
        if dif["acrescentar"]:
            partes.append(f"a menos: {', '.join(repr(t) for t in dif['acrescentar'])}")
        saida.append(f"{sid}: difere da STR gerada do quadro de {fid} — "
                     f"{'; '.join(partes)}; corrigir com `strings gerar --gravar`")
    return saida


# ------------------------------------------------------------------------ gravação
_CELULA_STR = re.compile(r"^(\s*\|[^|]*\|[^|]*\|)[^|]*(\|.*)$")


def regrava(texto, d):
    """Texto do protocolo com as células de string substituídas pelas STRs esperadas.

    Só a terceira célula das linhas `STRn` da seção de strings muda; o resto do texto,
    inclusive as quebras de linha, fica igual byte a byte.
    """
    linhas_ = texto.split("\n")
    por_linha = {}
    for idx, linha in linhas_de_tabela(secao(texto, G.S_STRINGS)):
        cels = celulas(linha)
        if len(cels) < 3:
            continue
        mi = G.I_STR.casa(cels[0])
        if mi:
            por_linha[idx] = f"{G.I_FCT.prefixo}{int(mi.group(1))}"
    novas = {f["id"]: texto_str(esperada(f, d["idiomas"])[0]) for f in d["tabelas"]}
    for idx, fid in por_linha.items():
        m = _CELULA_STR.match(linhas_[idx])
        if m is None:
            # A leitura aceitou a linha, mas a célula não se isola para a troca: recusar a
            # gravação nomeando a linha, em vez de gravar uma linha deformada.
            raise ProtocoloInvalido(G.T_STRINGS, f"linha {idx + 1}: célula de string de "
                                                 f"{fid} não isolável para a gravação")
        linhas_[idx] = f"{m.group(1)} {novas[fid]} {m.group(2)}"
    return "\n".join(linhas_)


def grava_atomico(caminho, texto):
    """Grava num temporário do mesmo diretório e renomeia: falha no meio não toca o arquivo."""
    pasta = os.path.dirname(os.path.abspath(caminho))
    fd, tmp = tempfile.mkstemp(dir=pasta, prefix=".tmp_", suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(texto)
        try:
            os.chmod(tmp, os.stat(caminho).st_mode & 0o7777)
        except FileNotFoundError:
            pass
        os.replace(tmp, caminho)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ------------------------------------------------------------------------ comando
def gera(ctx, gravar=False, caminho=None, saida=print):
    """Compara as STRs do protocolo com as geradas e, com `gravar`, regrava `caminho`.

    `caminho` é o arquivo do protocolo (padrão: o da configuração); o autoteste passa uma
    cópia temporária. Devolve o código de saída.
    """
    d = ctx.protocolo()
    duplicados = problemas_atribuicao(d)
    difs = diferencas(d)

    for fid in sorted(difs):
        for linha in descreve(fid, difs[fid], d):
            saida(linha)
    if not difs:
        saida("Nenhuma diferença: as STRs do protocolo são as geradas do quadro.")
    if duplicados:
        saida("ATRIBUIÇÃO ÚNICA VIOLADA:")
        for p in duplicados:
            saida(f"  - {p}")

    if not gravar:
        if difs or duplicados:
            saida("\nEnsaio: nada foi gravado.")
            return Saida.REPROVADO
        return Saida.OK
    if duplicados:
        saida("\nGravação recusada: o quadro tem termo em mais de uma faceta, e as STRs "
              "geradas se implicariam. Nada foi gravado.")
        return Saida.REPROVADO
    if not difs:
        return Saida.OK
    caminho = caminho or ctx.config.protocolo()
    # O arquivo corrente é relido imediatamente antes de gravar, sem tradução de quebra de
    # linha: o restante fica igual byte a byte, e a edição feita depois da leitura não se
    # perde — a gravação é recusada.
    with open(caminho, encoding="utf-8", newline="") as fh:
        bruto = fh.read()
    if bruto.replace("\r\n", "\n") != ctx.texto:
        saida("\nGravação recusada: o protocolo mudou durante a execução. Nada foi gravado.")
        return Saida.REPROVADO
    grava_atomico(caminho, regrava(bruto, d))
    saida(f"\nGravado: {len(difs)} STR(s) em {caminho}.")
    return Saida.OK


def cmd_gerar(ctx, a):
    return gera(ctx, gravar=getattr(a, "gravar", False))
