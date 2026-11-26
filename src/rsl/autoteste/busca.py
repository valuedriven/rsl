"""Autoteste da busca: a prova da composição reprova cada relação quebrada, a aderência é
relatada por papel, com o intervalo de Wilson, o casamento local usa os termos da base e o
corpus da derivação é só a executada."""

import contextlib
import copy
import csv
import io
import json
import pathlib
import re
import tempfile

from .. import gramatica as G
from ..busca import Busca
from ..busca.aderencia import (avalia_aderencia, casa_sementes, casa_titulo, chave_titulo,
                               registros_unicos, wilson)
from ..busca.composicao import grupos_em_facetas, prova_da_composicao
from ..busca.derivacao import carrega_facetas, derivar, facetas_atingidas, texto_do
from ..busca.fidelidade import fidelidade
from ..config import Configuracao
from ..erros import ErroRSL
from ..flexao import formas_de_numero
from ..leitura import papeis
from ..markdown import normaliza
from ..procedimentos import composicao_da_base, idiomas_do_termo
from .fontes import com_fonte, fonte_de


def composicao(ctx, g):
    """Cada defeito é injetado numa cópia da composição lida (em STRn, como no protocolo);
    os papéis são recalculados sobre a cópia, como a leitura faria, e a prova tem de
    reprovar pelo motivo esperado. Os identificadores vêm dos papéis do protocolo."""
    d = ctx.protocolo()
    p = d["papeis"]
    exec_, sonda, ancoras = p["executada"], p["sonda"], p["ancoras"]
    faceta_de = {v["id"]: fid for fid, v in d["strings"].items()}

    def prova(expressoes):
        dm = copy.deepcopy(d)
        dm["expressoes"] = expressoes
        return prova_da_composicao(grupos_em_facetas(expressoes, faceta_de), papeis(dm),
                                   faceta_de)

    def testa(nome, expressoes, espera):
        if expressoes == d["expressoes"]:
            g.falha(f"mutação não aplicada: {nome}")
            return
        achados = [x for x in prova(expressoes) if espera in x]
        if achados:
            g.ok(f"reprovou: {nome} — {achados[0][:88]}")
        else:
            g.falha(f"não reprovou pelo motivo esperado ({espera!r}): {nome}")

    controle = prova(copy.deepcopy(d["expressoes"]))
    g.testa("composição do protocolo aprovada pela prova", not controle,
            controle[0][:80] if controle else "")
    if not p["especificas"] or not p["gerais"]:
        g.falha(f"o protocolo não tem específica e geral para mutar: {p}")
        return
    uma = sorted(p["especificas"].values())[0]
    geral = sorted(p["gerais"])[0]

    m = copy.deepcopy(d["expressoes"])
    m[exec_] = ancoras + [[uma]]
    testa(f"executada {exec_} reduzida a uma só específica ({uma})", m, f"{exec_} ≠ ")
    # A falha nomeia a combinação de facetas em que a relação não vale.
    g.testa("a reprovação da executada nomeia a combinação de facetas",
            any(" em [" in x for x in prova(m) if f"{exec_} ≠ " in x))
    m = copy.deepcopy(d["expressoes"])
    m[sonda] = ancoras + [[uma]]
    testa(f"sonda {sonda} restrita por {uma}", m, f"{sonda} não contém")
    m = copy.deepcopy(d["expressoes"])
    m[geral] = [x for x in m[geral] if x != ancoras[-1]]
    testa(f"geral {geral} sem a âncora {ancoras[-1][0]}", m, "não está contida")
    m = copy.deepcopy(d["expressoes"])
    m["MUT1"] = copy.deepcopy(ancoras)
    testa("expressão a mais fora da executada", m, "deriváveis de")


def aderencia(ctx, g):
    """Relato por papel e intervalo de Wilson, com dados sintéticos."""
    lo, hi = wilson(8, 10)
    g.testa("Wilson 8/10 = 80% com intervalo 49,0%–94,3%",
            abs(lo - 0.490) < 0.001 and abs(hi - 0.943) < 0.001, f"{lo:.3%}–{hi:.3%}")
    g.testa("Wilson sem tentativa não tem intervalo", wilson(0, 0) is None)

    idx = {chave_titulo("Um título completo para o teste"): [{"base": "x"}]}
    exatas, prefixo = casa_titulo(idx, chave_titulo("Um título completo para o teste"))
    g.testa("título exato é recuperação", bool(exatas) and not prefixo)
    exatas, prefixo = casa_titulo(idx, chave_titulo("Um título completo"))
    g.testa("prefixo é indício, não recuperação", not exatas and bool(prefixo))

    val, dev = G.PAPEL_VALIDACAO, G.PAPEL_DESENVOLVIMENTO
    sementes = ([{"id": f"V{k}", "papel": val} for k in range(1, 7)]
                + [{"id": f"D{k}", "papel": dev} for k in range(1, 5)])
    recuperadas = {f"V{k}" for k in range(1, 6)} | {f"D{k}" for k in range(1, 5)}
    av = avalia_aderencia(sementes, recuperadas, limiar=0.8)
    v, dv = av["decide"], av["por_papel"][dev]
    g.testa("5/6 de validação e 4/4 de desenvolvimento são relatados separados",
            v["recuperadas"] == 5 and v["total"] == 6
            and dv["recuperadas"] == 4 and dv["total"] == 4,
            f"validação {v['recuperadas']}/{v['total']}, "
            f"desenvolvimento {dv['recuperadas']}/{dv['total']}")
    g.testa("total recuperado independe do papel",
            sum(x["recuperadas"] for x in av["por_papel"].values()) == len(recuperadas))
    # 4/6 de validação = 66,7%; 4/4 de desenvolvimento leva o total a 80%, mas o
    # desenvolvimento não compensa: a validação continua abaixo do limiar.
    recuperadas = {f"V{k}" for k in range(1, 5)} | {f"D{k}" for k in range(1, 5)}
    av = avalia_aderencia(sementes, recuperadas, limiar=0.8)
    g.testa("desenvolvimento não compensa validação",
            av["decide"]["recuperadas"] == 4 and av["decide"]["total"] == 6
            and not av["decide"]["aprovada"] and av["por_papel"][dev]["proporcao"] == 1.0,
            f"validação {av['decide']['proporcao']:.1%}")


# ------------------------------------------------------------- casamento e corpus
def _padrao_com_sufixo(termo):
    """O casamento anterior a esta conferência: cada palavra com sufixo `s`/`es` opcional.
    Existe só para provar que o caso do plural irregular o reprova."""
    partes = [re.escape(x) + r"(?:e?s)?" for x in normaliza(termo).split()]
    return re.compile(r"(?<!\w)" + r"\s+".join(partes) + r"(?!\w)")


def _base_que_compoe(ctx):
    """(Busca, sigla, composição) da primeira base da tabela cuja composição se lê; (Busca,
    None, motivos) se nenhuma."""
    b = Busca(ctx)
    motivos = []
    for base in b.d["bases"]:
        try:
            return b, base["sigla"], composicao_da_base(ctx, b.d, base["sigla"])[1]
        except ErroRSL as e:
            motivos.append(f"{base['sigla']}: {str(e)[:60]}")
    return b, None, motivos


def _formas_da_composicao(d, comp, fid):
    """Termos da string que a base recebe e as formas de número deles: o que o casamento
    local tem de reconhecer, lido da composição e não do vocabulário sob teste."""
    termos = comp.strings[fid]["termos"]
    idioma_de = idiomas_do_termo(d, fid)
    numero = formas_de_numero([t for t in termos if "*" not in t],
                              lambda x: idioma_de.get(x, []), comp.excecoes)
    return list(termos) + sorted(numero - set(termos))


def casamento(ctx, g):
    """O plural que o sufixo `s`/`es` não alcança, tomado da composição de uma base, é
    reconhecido pelo vocabulário da base e não pelo casamento antigo sobre os termos do
    protocolo; nenhum sufixo aproximado volta; a base que lematiza casa a forma de número
    que a string dela não traz; e cada registro se casa com os termos da sua base."""
    b, sigla, comp = _base_que_compoe(ctx)
    if sigla is None:
        g.nao_executa(4, "nenhuma base com composição legível — " + "; ".join(comp))
        return
    vocab = carrega_facetas(b, [sigla])
    antigos = {fid: [_padrao_com_sufixo(t) for t in v["termos"]]
               for fid, v in b.d["strings"].items()}
    do_protocolo = {fid: {t.lower() for t in v["termos"]} for fid, v in b.d["strings"].items()}
    achado = None
    for fid in comp.strings:
        for forma in _formas_da_composicao(b.d, comp, fid):
            if "*" in forma or forma.lower() in do_protocolo.get(fid, ()):
                continue
            reg = {"titulo": forma, "resumo": "", "palavras_chave": "", "base": sigla}
            if not any(p.search(texto_do(reg)) for p in antigos.get(fid, [])):
                achado = (fid, forma, reg)
                break
        if achado:
            break
    if achado is None:
        g.nao_executa(1, f"{sigla}: nenhuma forma de número fora do alcance do sufixo s/es")
    else:
        fid, forma, reg = achado
        antigo = {n for n, ps in antigos.items() if any(p.search(texto_do(reg)) for p in ps)}
        novo = facetas_atingidas(reg, vocab)
        g.testa(f"plural irregular ({sigla}, {fid}, {forma!r}) reconhecido pelos termos da "
                f"base e não pelo sufixo s/es", fid in novo and fid not in antigo,
                f"termos da base: {sorted(novo)}; sufixo s/es: {sorted(antigo)}")

    # Sufixo aproximado: um termo da base acrescido de `es`, fora do vocabulário, não casa.
    todos = {t.lower() for f in vocab[sigla].values() for t in f["termos"]}
    alvo = next(((fid, t) for fid, f in vocab[sigla].items() for t in f["termos"]
                 if "*" not in t and (t + "es").lower() not in todos), None)
    if alvo is None:
        g.nao_executa(1, f"{sigla}: nenhum termo sem '*' para testar o sufixo")
    else:
        fid, t = alvo
        reg = {"titulo": t + "es", "resumo": "", "palavras_chave": "", "base": sigla}
        g.testa(f"sem sufixo aproximado: {t + 'es'!r} não é reconhecido em {fid} ({sigla})",
                fid not in facetas_atingidas(reg, vocab))

    _lematizacao(ctx, g, b, sigla)
    _outra_base(ctx, g, b)


def _lematizacao(ctx, g, b, sigla):
    """Na cópia da fonte com plural `pela lematização`, a string da base não traz a forma de
    número, e o casamento local a reconhece mesmo assim, pela forma de número do termo."""
    try:
        dado, frag, arqs = fonte_de(ctx, b.d, sigla)
    except LookupError as e:
        g.nao_executa(1, f"base que lematiza: {e}")
        return
    dado.setdefault("cobertura", {})["plural"] = G.PLURAL_LEMATIZACAO
    cx = com_fonte(ctx, sigla, dado, frag, arqs)
    bx = Busca(cx)
    try:
        comp = composicao_da_base(cx, bx.d, sigla)[1]
    except ErroRSL as e:
        g.nao_executa(1, f"base que lematiza ({sigla}): {str(e)[:80]}")
        return
    vocab = carrega_facetas(bx, [sigla])
    achado = None
    for fid, s in comp.strings.items():
        na_string = {t.lower() for t in s["termos"]}
        forma = next((x for x in _formas_da_composicao(bx.d, comp, fid)
                      if "*" not in x and x.lower() not in na_string), None)
        if forma:
            achado = (fid, forma)
            break
    if achado is None:
        g.nao_executa(1, f"base que lematiza ({sigla}): nenhuma forma de número fora da string")
        return
    fid, forma = achado
    reg = {"titulo": forma, "resumo": "", "palavras_chave": "", "base": sigla}
    g.testa(f"base que lematiza ({sigla}, {fid}): {forma!r}, ausente da string, reconhecido "
            f"pela forma de número", fid in facetas_atingidas(reg, vocab),
            f"reconhecidas: {sorted(facetas_atingidas(reg, vocab))}")


def _outra_base(ctx, g, b):
    """Um termo que só a string de uma base traz reconhece a faceta no registro dessa base e
    não no mesmo registro atribuído a outra: cada registro se casa com os termos da sua base."""
    vocab = {}
    for base in b.d["bases"]:
        try:
            vocab.update(carrega_facetas(b, [base["sigla"]]))
        except ErroRSL:
            continue
    for a in vocab:
        for c in vocab:
            if a == c:
                continue
            for fid, f in vocab[a].items():
                for t in f["termos"]:
                    if "*" in t or fid not in vocab[c]:
                        continue
                    # O par se escolhe pelos padrões de cada base, não pela função sob teste.
                    if any(p.search(normaliza(t)) for p in vocab[c][fid]["padroes"]):
                        continue
                    em_a = {"titulo": t, "resumo": "", "palavras_chave": "", "base": a}
                    em_c = dict(em_a, base=c)
                    g.testa(f"termos de outra base: {t!r} reconhece {fid} em {a} e não em {c}",
                            fid in facetas_atingidas(em_a, vocab)
                            and fid not in facetas_atingidas(em_c, vocab))
                    return
    g.nao_executa(1, "termos de outra base: nenhum par de bases com strings diferentes")


def _ris(registros):
    return "".join(f"TY  - JOUR\nTI  - {t}\nPY  - {ano}\nDO  - {doi}\nER  - \n\n"
                   for t, ano, doi in registros)


def _linhas_csv(caminho):
    with caminho.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def corpus(ctx, g):
    """Executada com N registros e sonda com N + 1, num registro de execução e numa pasta de
    saídas temporários, mais a execução direta de uma expressão de conferência: o excedente
    da sonda não entra nos registros, na ordem de triagem, na contagem da executada nem na
    aderência; a execução direta não entra nos registros e é lida pela fidelidade como
    arquivo; e `derivar` e `fidelidade` relatam as lidas e as deixadas de fora, com o motivo."""
    b, sigla, motivos = _base_que_compoe(ctx)
    if sigla is None:
        g.nao_executa(8, "nenhuma base com composição legível — " + "; ".join(motivos))
        return
    bd = b.bd_de[sigla]
    executados = [(f"Registro sintetico {k} da executada no autoteste", b.ano_min,
                   f"10.0000/autoteste.executada.{k}") for k in (1, 2)]
    excedente = ("Registro sintetico excedente presente so na sonda", b.ano_min,
                 "10.0000/autoteste.sonda.1")
    so_conferencia = ("Registro sintetico presente so na execucao direta de conferencia",
                      b.ano_min, "10.0000/autoteste.conferencia.1")
    conf = sorted(b.d["papeis"]["especificas"])[0]
    n = len(executados)
    with tempfile.TemporaryDirectory() as tmp:
        pasta = pathlib.Path(tmp)
        (pasta / "executada.ris").write_text(_ris(executados), encoding="utf-8")
        (pasta / "sonda.ris").write_text(_ris(executados + [excedente]), encoding="utf-8")
        (pasta / "conferencia.ris").write_text(_ris(executados[:1] + [so_conferencia]),
                                               encoding="utf-8")
        registro = {"bases": {bd: {"base": sigla, "execucoes": [
            {"id": "EX1", "expressao": b.executada, "arquivo": str(pasta / "executada.ris"),
             "registros_lidos": n, "status": "valida"},
            {"id": "EX2", "expressao": b.sonda, "arquivo": str(pasta / "sonda.ris"),
             "registros_lidos": n + 1, "status": "valida"},
            {"id": "EX3", "expressao": conf, "arquivo": str(pasta / "conferencia.ris"),
             "registros_lidos": 2, "status": "valida"}]}}}
        (pasta / "registro.json").write_text(json.dumps(registro), encoding="utf-8")
        cfg = ctx.config
        cfg = Configuracao(cfg.com("dados.registro", str(pasta / "registro.json")), cfg.arquivo)
        cfg = Configuracao(cfg.com("saidas.pasta", str(pasta / "saidas")), cfg.arquivo)
        bx = Busca(ctx.com_config(cfg))
        relato, relato_fid = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(relato):
            derivar(bx)
            unicos = registros_unicos(bx)
        with contextlib.redirect_stdout(relato_fid):
            fidelidade(bx, conf, str(pasta / "conferencia.ris"))
        registros = _linhas_csv(cfg.saida("registros"))
        ordem = _linhas_csv(cfg.saida("ordem_triagem"))
        contagem = next((x for x in _linhas_csv(cfg.saida("contagens"))
                         if x["base"] == sigla and x["expressao"] == b.executada), {})
    chave = normaliza(excedente[0])
    g.testa(f"registro só da sonda fora de `registros.csv` ({len(registros)} de {n})",
            len(registros) == n and all(normaliza(x["titulo"]) != chave for x in registros))
    g.testa(f"execução direta de {conf} fora de `registros.csv`",
            all(normaliza(x["titulo"]) != normaliza(so_conferencia[0]) for x in registros))
    esperado = [f"{bd}/EX1  {sigla} {b.executada}\n",
                f"{bd}/EX2  {sigla} {b.sonda} — sonda\n",
                f"{bd}/EX3  {sigla} {conf} — execução direta de conferência\n"]
    for nome, texto in (("derivar", relato.getvalue()), ("fidelidade", relato_fid.getvalue())):
        lidas, _, fora = texto.partition("deixadas de fora")
        g.testa(f"relato de `{nome}`: {b.executada} lida; {b.sonda} e {conf} deixadas de "
                f"fora, com o motivo", esperado[0] in lidas
                and all(x in fora and x not in lidas for x in esperado[1:]), texto[:300])
    g.testa(f"`conferencia fidelidade {conf}` lê o arquivo como execução direta (2 registros)",
            re.search(r"execução direta na base\s*:\s*2\b", relato_fid.getvalue()) is not None,
            relato_fid.getvalue()[-300:])
    g.testa(f"registro só da sonda fora de `ordem_triagem.csv` ({len(ordem)} de {n})",
            len(ordem) == n and all(normaliza(x["titulo"]) != chave for x in ordem))
    g.testa(f"contagem de {b.executada} igual aos registros da executada ({n})",
            contagem.get("registros") == str(n)
            and contagem.get("registros_com_duplicatas") == str(n), str(contagem))
    sementes = [{"id": "SX1", "titulo": excedente[0]}, {"id": "SX2", "titulo": executados[0][0]}]
    casados = {e["id"]: bool(exatas) for e, exatas, _ in casa_sementes(sementes, unicos)}
    g.testa("semente só na sonda não conta na aderência; a da executada conta",
            casados == {"SX1": False, "SX2": True}, str(casados))
