"""Autoteste da busca: a prova da composição reprova cada relação quebrada, a aderência é
relatada sobre o conjunto, com o intervalo de Wilson, o casamento local usa os termos da base e o
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
from ..busca.aderencia import (VIA_AMBOS, VIA_DOI, avalia_aderencia, casa_sementes,
                               casa_titulo, chave_titulo, recupera_sementes,
                               registros_unicos, wilson)
from ..busca.anatomia import diagnosticar, monta_niveis, selecao
from ..busca.composicao import grupos_em_facetas, prova_da_composicao, satisfaz_em
from ..busca.derivacao import (carrega_facetas, derivar, facetas_atingidas, padrao,
                               texto_do, vocabulario_da_base)
from ..busca.fidelidade import fidelidade
from ..busca.leitores import SEPARADOR_VALORES, TIPOS_RIS, le_ris, le_wos_txt
from ..busca.registro import OBTER_DO_ZOTERO, chave_dedup, identificador_execucao
from ..busca.sensibilidade import sensibilidade
from ..busca.simulacao import analisa, valida_termos
from ..busca.simulacao import candidatos as candidatos_da_amostra
from ..config import Configuracao
from ..erros import ErroRSL
from ..flexao import formas_de_numero
from ..leitura import papeis
from ..markdown import normaliza
from ..saida import Saida
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
    """Relato único sobre o conjunto e intervalo de Wilson, com dados sintéticos."""
    lo, hi = wilson(8, 10)
    g.testa("Wilson 8/10 = 80% com intervalo 49,0%–94,3%",
            abs(lo - 0.490) < 0.001 and abs(hi - 0.943) < 0.001, f"{lo:.3%}–{hi:.3%}")
    g.testa("Wilson sem tentativa não tem intervalo", wilson(0, 0) is None)

    idx = {chave_titulo("Um título completo para o teste"): [{"base": "x"}]}
    exatas, prefixo = casa_titulo(idx, chave_titulo("Um título completo para o teste"))
    g.testa("título exato é recuperação", bool(exatas) and not prefixo)
    exatas, prefixo = casa_titulo(idx, chave_titulo("Um título completo"))
    g.testa("prefixo é indício, não recuperação", not exatas and bool(prefixo))

    sementes = [{"id": f"SE{k}"} for k in range(1, 11)]
    av = avalia_aderencia(sementes, {f"SE{k}" for k in range(1, 9)}, limiar=0.8)
    lo, hi = av["intervalo"]
    g.testa("relato único: 8/10 = 80%, com Wilson 49,0%–94,3% sobre o mesmo denominador, "
            "no limiar",
            av["recuperadas"] == 8 and av["total"] == 10 and av["proporcao"] == 0.8
            and abs(lo - 0.490) < 0.001 and abs(hi - 0.943) < 0.001 and av["aprovada"]
            and "por_papel" not in av,
            f"{av['recuperadas']}/{av['total']} {lo:.3%}–{hi:.3%} aprovada={av['aprovada']}")
    av = avalia_aderencia(sementes, {f"SE{k}" for k in range(1, 8)}, limiar=0.8)
    g.testa("7/10 fica abaixo do limiar de 80% e é declarada abaixo",
            av["recuperadas"] == 7 and not av["aprovada"], f"{av['proporcao']:.1%}")
    g.testa("ids recuperados na ordem das sementes",
            av["ids"] == [f"SE{k}" for k in range(1, 8)], f"{av['ids']}")

    # Recuperação também pelo DOI: título divergente com o mesmo DOI conta, pelo DOI; o
    # prefixo confirmado pelo DOI conta pelo DOI; o prefixo sem DOI segue indício.
    titulo = "Um título completo para o teste de recuperação pelo identificador"
    regs = [{"titulo": "Título que a base grafou de outra forma", "doi": "10.9999/AUTO.1",
             "base": "x"},
            {"titulo": titulo + " com subtítulo", "doi": "https://doi.org/10.9999/auto.2",
             "base": "x"},
            {"titulo": titulo + " e outro subtítulo", "doi": "10.9999/outro", "base": "x"},
            {"titulo": "Título exato da semente quatro do autoteste", "doi": "10.9999/auto.4",
             "base": "x"}]
    sementes = [{"id": "SX1", "titulo": "Título da semente no Zotero", "doi": "10.9999/auto.1"},
                {"id": "SX2", "titulo": titulo, "doi": "10.9999/auto.2"},
                {"id": "SX3", "titulo": titulo, "doi": "10.9999/auto.3"},
                {"id": "SX4", "titulo": "Título exato da semente quatro do autoteste",
                 "doi": "10.9999/auto.4"}]
    via = {e["id"]: (v, bool(p)) for e, v, _, p in recupera_sementes(sementes, regs)}
    g.testa("título divergente e mesmo DOI: recuperada, pelo DOI",
            via["SX1"] == (VIA_DOI, False), str(via["SX1"]))
    g.testa("prefixo de título confirmado pelo DOI: recuperada, pelo DOI",
            via["SX2"] == (VIA_DOI, False), str(via["SX2"]))
    g.testa("prefixo de título sem o DOI da semente: segue indício, não recuperada",
            via["SX3"] == ("", True), str(via["SX3"]))
    g.testa("título exato e DOI: recuperada pelos dois",
            via["SX4"] == (VIA_AMBOS, False), str(via["SX4"]))


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
        g.nao_executa("nenhuma base com composição legível — " + "; ".join(comp))
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
        g.nao_executa(f"{sigla}: nenhuma forma de número fora do alcance do sufixo s/es",
                      quantos=1)
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
        g.nao_executa(f"{sigla}: nenhum termo sem '*' para testar o sufixo", quantos=1)
    else:
        fid, t = alvo
        reg = {"titulo": t + "es", "resumo": "", "palavras_chave": "", "base": sigla}
        g.testa(f"sem sufixo aproximado: {t + 'es'!r} não é reconhecido em {fid} ({sigla})",
                fid not in facetas_atingidas(reg, vocab))

    _fronteira(g, sigla, vocab)
    _leitor_wos_txt(g)
    _lematizacao(ctx, g, b, sigla)
    _outra_base(ctx, g, b)


def _leitor_wos_txt(g):
    """O texto plano da WoS separa palavras-chave repetidas com o mesmo separador que os
    demais leitores: unidas por espaço, a fronteira entre valores se perderia no casamento."""
    reg = le_wos_txt("PT J\nTI Titulo do teste\nDE learning\nDE context awareness\nER\n")[0]
    esperado = f"learning{SEPARADOR_VALORES}context awareness"
    g.testa("leitor .txt da WoS separa palavras-chave repetidas com o separador de valores",
            reg["palavras_chave"] == esperado, repr(reg["palavras_chave"]))


def _fronteira(g, sigla, vocab):
    """Um termo de várias palavras, partido em dois pedaços que sozinhos não casam a
    faceta, não é reconhecido quando os pedaços estão em palavras-chave distintas nem
    quando um está no título e o outro no resumo; inteiro numa palavra-chave, é. O termo e
    o corte vêm do vocabulário da base, e a escolha usa os padrões, não a função sob teste."""
    achado = None
    for fid, f in vocab[sigla].items():
        for t in f["termos"]:
            palavras = t.split()
            if "*" in t or len(palavras) < 2:
                continue
            for k in range(1, len(palavras)):
                a, c = " ".join(palavras[:k]), " ".join(palavras[k:])
                if not any(p.search(normaliza(x)) for p in f["padroes"] for x in (a, c)):
                    achado = (fid, t, a, c)
                    break
            if achado:
                break
        if achado:
            break
    if achado is None:
        g.nao_executa(f"fronteira ({sigla}): nenhum termo de várias palavras partível")
        return
    fid, t, a, c = achado
    sep = SEPARADOR_VALORES
    inteiro = {"titulo": "", "resumo": "", "palavras_chave": f"outra{sep}{t}", "base": sigla}
    entre_chaves = dict(inteiro, palavras_chave=f"{a}{sep}{c}")
    entre_campos = dict(inteiro, titulo=a, resumo=c, palavras_chave="")
    g.testa(f"fronteira ({sigla}, {fid}): {t!r} inteiro numa palavra-chave é reconhecido",
            fid in facetas_atingidas(inteiro, vocab))
    g.testa(f"fronteira ({sigla}, {fid}): {a!r}{sep}{c!r} em palavras-chave distintas não "
            f"forma {t!r}", fid not in facetas_atingidas(entre_chaves, vocab))
    g.testa(f"fronteira ({sigla}, {fid}): {a!r} no título e {c!r} no resumo não formam "
            f"{t!r}", fid not in facetas_atingidas(entre_campos, vocab))
    # Controle: com o texto unido, o mesmo par casaria. É o que prova que os dois casos
    # acima reprovam se o casamento voltar a procurar no texto único.
    g.testa(f"controle da fronteira ({sigla}, {fid}): com o texto unido, {t!r} casaria",
            any(p.search(texto_do(entre_chaves)) for p in f["padroes"]),
            texto_do(entre_chaves))


def _lematizacao(ctx, g, b, sigla):
    """Na cópia da fonte com plural `pela lematização`, a string da base não traz a forma de
    número, e o casamento local a reconhece mesmo assim, pela forma de número do termo."""
    try:
        dado, frag, arqs = fonte_de(ctx, b.d, sigla)
    except LookupError as e:
        g.nao_executa(f"base que lematiza: {e}")
        return
    dado.setdefault("cobertura", {})["plural"] = G.PLURAL_LEMATIZACAO
    cx = com_fonte(ctx, sigla, dado, frag, arqs)
    bx = Busca(cx)
    try:
        comp = composicao_da_base(cx, bx.d, sigla)[1]
    except ErroRSL as e:
        g.nao_executa(f"base que lematiza ({sigla}): {str(e)[:80]}")
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
        g.nao_executa(f"base que lematiza ({sigla}): nenhuma forma de número fora da string")
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
    g.nao_executa("termos de outra base: nenhum par de bases com strings diferentes", quantos=1)


def _ris(registros):
    return "".join(f"TY  - JOUR\nTI  - {t}\nPY  - {ano}\nDO  - {doi}\nER  - \n\n"
                   for t, ano, doi in registros)


def _linhas_csv(caminho):
    with caminho.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def _registro_de_outra_base(b, sigla, conf):
    """(sigla, (título, ano, doi)) de uma base diferente de `sigla`, cujo título reúne um
    termo de cada grupo de `conf` pelo vocabulário dela e é reconhecido como pertencente a
    `conf`; (None, None) se nenhuma base compõe."""
    for base in b.d["bases"]:
        outra = base["sigla"]
        if outra == sigla:
            continue
        try:
            vocab = carrega_facetas(b, [outra])
        except ErroRSL:
            continue
        termos = []
        for grupo in b.grupos[conf]:
            fid = next((f for f in grupo if f in vocab[outra]), None)
            termo = fid and next((t for t in vocab[outra][fid]["termos"] if "*" not in t),
                                 None)
            if not termo:
                break
            termos.append(termo)
        else:
            titulo = " ".join(termos)
            reg = {"titulo": titulo, "resumo": "", "palavras_chave": "", "base": outra}
            if satisfaz_em(b.grupos, conf, facetas_atingidas(reg, vocab)):
                return outra, (titulo, b.ano_min, "10.0000/autoteste.outra.1")
    return None, None


def corpus(ctx, g):
    """Executada com N registros e sonda com N + 1, num registro de execução e numa pasta de
    saídas temporários, mais a execução direta de uma expressão de conferência: o excedente
    da sonda não entra nos registros, na ordem de triagem, na contagem da executada nem na
    aderência; a execução direta não entra nos registros e é lida pela fidelidade como
    arquivo; e `derivar` e `fidelidade` relatam as lidas e as deixadas de fora, com o motivo."""
    b, sigla, motivos = _base_que_compoe(ctx)
    if sigla is None:
        g.nao_executa("nenhuma base com composição legível — " + "; ".join(motivos))
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
        # Outra base, com a executada trazendo um registro que satisfaz a expressão de
        # conferência pelos termos DELA: a fidelidade da primeira base não pode contá-lo.
        outra, de_outra = _registro_de_outra_base(b, sigla, conf)
        if outra is not None:
            (pasta / "outra.ris").write_text(_ris([de_outra]), encoding="utf-8")
            registro["bases"][b.bd_de[outra]] = {"base": outra, "execucoes": [
                {"id": "EX1", "expressao": b.executada, "arquivo": str(pasta / "outra.ris"),
                 "registros_lidos": 1, "status": "valida"}]}
        (pasta / "registro.json").write_text(json.dumps(registro), encoding="utf-8")
        cfg = ctx.config
        cfg = Configuracao(cfg.com("dados.registro", str(pasta / "registro.json")), cfg.arquivo)
        cfg = Configuracao(cfg.com("saidas.pasta", str(pasta / "saidas")), cfg.arquivo)
        bx = Busca(ctx.com_config(cfg))
        relato, relato_fid = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(relato):
            derivar(bx)
            unicos = registros_unicos(bx)
        relato_reg = io.StringIO()
        with contextlib.redirect_stdout(relato_fid):
            fidelidade(bx, sigla, conf, str(pasta / "conferencia.ris"))
        with contextlib.redirect_stdout(relato_reg):
            fidelidade(bx, sigla, conf)

        def sem_execucao(ident):
            """Busca com o registro de execuções sem a execução `ident` da base testada."""
            d2 = copy.deepcopy(registro)
            d2["bases"][bd]["execucoes"] = [
                e for e in d2["bases"][bd]["execucoes"] if e["id"] != ident]
            arq = pasta / f"registro_sem_{ident}.json"
            arq.write_text(json.dumps(d2), encoding="utf-8")
            c2 = Configuracao(cfg.com("dados.registro", str(arq)), cfg.arquivo)
            return Busca(ctx.com_config(c2))

        # EX1 é a executada; EX3 é a execução direta da expressão de conferência.
        cod_sem_executada, _, erro_sem_executada = _roda_analise(
            lambda: fidelidade(sem_execucao("EX1"), sigla, conf))
        cod_sem_direta, _, erro_sem_direta = _roda_analise(
            lambda: fidelidade(sem_execucao("EX3"), sigla, conf))
        # Só os da base sob teste: a segunda base, quando há, entra nas saídas pela sua
        # própria executada.
        registros = [x for x in _linhas_csv(cfg.saida("registros")) if x["base"] == sigla]
        ordem = [x for x in _linhas_csv(cfg.saida("ordem_triagem")) if x["base"] == sigla]
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
    g.testa(f"`conferencia fidelidade {sigla} {conf}` sem arquivo lê a execução registrada "
            f"(2 registros)", re.search(r"execução direta na base\s*:\s*2\b",
                                        relato_reg.getvalue()) is not None,
            relato_reg.getvalue()[-300:])
    g.testa("fidelidade sem a executada registrada sai com DADOS e nomeia o registro",
            cod_sem_executada == Saida.DADOS and b.executada in erro_sem_executada
            and "busca registrar" in erro_sem_executada,
            f"{cod_sem_executada.name} {erro_sem_executada[:120]}")
    g.testa("fidelidade sem execução direta registrada sai com DADOS e nomeia o registro",
            cod_sem_direta == Saida.DADOS and conf in erro_sem_direta
            and "busca registrar" in erro_sem_direta,
            f"{cod_sem_direta.name} {erro_sem_direta[:120]}")
    if outra is None:
        g.nao_executa("fidelidade por base: nenhuma segunda base com registro que "
                      f"satisfaça {conf}", quantos=1)
    else:
        g.testa(f"fidelidade de {sigla} não conta o registro da executada de {outra} que "
                f"satisfaz {conf} (conjunto derivado 0)",
                re.search(r"conjunto derivado\s*:\s*0\b", relato_fid.getvalue()) is not None,
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


# ------------------------------------------------------------- anatomia da perda
def _ris_anat(linhas):
    """RIS de ensaio com idioma e tipo, que a causa `filtro` relata."""
    return "".join(
        f"TY  - {tipo}\nTI  - {titulo}\nPY  - {ano}\nLA  - {idioma}\nDO  - {doi}\nER  - \n\n"
        for titulo, ano, doi, idioma, tipo in linhas)


def _roda_anatomia(funcao):
    """(código, saída, mensagem) de uma chamada do diagnóstico, com a saída recolhida."""
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            r = funcao()
        return Saida(r), out.getvalue(), ""
    except ErroRSL as e:
        return Saida(e.codigo), out.getvalue(), str(e)


def _base_com_proximidade(ctx, b):
    """(sigla, fonte, fragmentos, arquivos) da primeira base com proximidade e sonda e
    executada de consulta única, legível."""
    for base in b.d["bases"]:
        sigla = base["sigla"]
        try:
            dado, frag, arqs = fonte_de(ctx, b.d, sigla)
            if not isinstance(dado.get("composicao", {}).get("proximidade"), dict):
                continue
            _, comp = composicao_da_base(ctx, b.d, sigla)
        except ErroRSL:
            continue
        if len(comp.expressoes[b.sonda]["consultas"]) == 1 and \
                len(comp.expressoes[b.executada]["consultas"]) == 1:
            return sigla, dado, frag, arqs
    return None


def anatomia(ctx, g):
    """Anatomia da perda com fonte de ensaio e exportações sintéticas: uma semente por
    causa, a recusa por exportação que não confere, nível faltando, incoerência entre
    níveis, DOI estranho e base sem `[composicao] doi`.

    A causa de cada semente é o PRIMEIRO nível em que o DOI some; usar o último faria as
    sementes ausentes desde o nível 1 saírem como `faceta não âncora`, e os casos de causa
    abaixo reprovariam. A conferência de subconjunto é provada pelo caso do DOI que
    reaparece: desligada, ele deixaria de reprovar.
    """
    b = Busca(ctx)
    achado = _base_com_proximidade(ctx, b)
    if achado is None:
        g.nao_executa("nenhuma base com proximidade e sonda/executada de consulta única")
        return
    sigla, dado0, frag0, arqs0 = achado
    dado = copy.deepcopy(dado0)
    dado.setdefault("composicao", {})[G.C_DOI_MODELO.chave] = f"DOI({G.MARCADOR_DOI})"

    # Dois títulos próprios: o da semente F difere do registro da executada, para que a
    # aderência não a conte como recuperada e o nível 5 revele a divergência de casamento.
    titulo_exec = "Registro sintetico da executada no autoteste da anatomia"
    definicao = {
        "SX1": ("10.0000/at.a", 2019, "eng", "JOUR"),   # não indexada
        "SX2": ("10.0000/at.b", 2020, "eng", "JOUR"),   # filtro
        "SX3": ("10.0000/at.c", 2021, "eng", "JOUR"),   # âncoras
        "SX4": ("10.0000/at.d", 2022, "eng", "JOUR"),   # proximidade
        "SX5": ("10.0000/at.e", 2023, "eng", "JOUR"),   # faceta não âncora
        "SX6": ("10.0000/at.f", 2024, "eng", "JOUR"),   # presente na executada
    }
    sementes = [{"id": k, "titulo": f"Semente sintetica {k} do autoteste da anatomia",
                 "doi": v[0], "bases": [sigla], "ano": v[1]} for k, v in definicao.items()]
    esperado = {"SX1": "não indexada", "SX2": "filtro", "SX3": "âncoras",
                "SX4": "proximidade", "SX5": "faceta não âncora",
                "SX6": "presente na executada"}

    def registros(ids, titulo_de=None):
        titulo_de = titulo_de or {}
        return _ris_anat([(titulo_de.get(k, f"Semente sintetica {k} do autoteste da anatomia"),
                           definicao[k][1], definicao[k][0], definicao[k][2],
                           definicao[k][3]) for k in ids])

    with tempfile.TemporaryDirectory() as tmp:
        pasta = pathlib.Path(tmp)
        l1, l2, l3 = pasta / "n1.ris", pasta / "n2.ris", pasta / "n3.ris"
        l1.write_text(registros(["SX2", "SX3", "SX4", "SX5", "SX6"]), encoding="utf-8")
        l2.write_text(registros(["SX3", "SX4", "SX5", "SX6"]), encoding="utf-8")
        l3.write_text(registros(["SX4", "SX5", "SX6"]), encoding="utf-8")
        (pasta / "sonda.ris").write_text(registros(["SX5", "SX6"]), encoding="utf-8")
        (pasta / "executada.ris").write_text(
            _ris_anat([(titulo_exec, 2024, "10.0000/at.f", "eng", "JOUR")]), encoding="utf-8")
        # A execução registrada só se lê com o texto vigente da expressão: o registro
        # sintético traz o texto composto agora, como `busca registrar` o gravaria.
        _, _, niveis0 = monta_niveis(Busca(com_fonte(ctx, sigla, dado, frag0, arqs0)), sigla,
                                     sementes)
        vigente = {n["expressao"]: n["texto_expressao"] for n in niveis0 if n["expressao"]}
        registro = {"bases": {b.bd_de[sigla]: {"base": sigla, "execucoes": [
            {"id": "EX1", "expressao": b.sonda, "arquivo": str(pasta / "sonda.ris"),
             "registros_lidos": 2, "status": "valida", "data_hora": "2026-11-25T10:00",
             "texto": vigente[b.sonda]},
            {"id": "EX2", "expressao": b.executada, "arquivo": str(pasta / "executada.ris"),
             "registros_lidos": 1, "status": "valida", "data_hora": "2026-11-25T10:00",
             "texto": vigente[b.executada]}]}}}
        # Outra base recupera SX7, esperada também nesta: a seleção é da executada desta
        # base, e SX7 tem de ser diagnosticada aqui mesmo recuperada lá.
        titulo_sx7 = "Semente sintetica SX7 recuperada so na outra base"
        outra = next((x["sigla"] for x in b.d["bases"] if x["sigla"] != sigla), None)
        if outra is not None:
            (pasta / "outra.ris").write_text(
                _ris_anat([(titulo_sx7, 2021, "10.0000/at.g", "eng", "JOUR")]),
                encoding="utf-8")
            registro["bases"][b.bd_de[outra]] = {"base": outra, "execucoes": [
                {"id": "EX1", "expressao": b.executada, "arquivo": str(pasta / "outra.ris"),
                 "registros_lidos": 1, "status": "valida",
                 "data_hora": "2026-11-25T10:00"}]}
        (pasta / "registro.json").write_text(json.dumps(registro), encoding="utf-8")
        cfg = ctx.config
        cfg = Configuracao(cfg.com("dados.registro", str(pasta / "registro.json")),
                           cfg.arquivo)
        cfg = Configuracao(cfg.com("saidas.pasta", str(pasta / "saidas")), cfg.arquivo)
        cx = com_fonte(ctx, sigla, dado, frag0, arqs0).com_config(cfg)
        bx = Busca(cx)

        fonte, comp, niveis = monta_niveis(bx, sigla, sementes)
        g.testa(f"níveis da base com proximidade: 1, 2, 3, 4, 5 [{sigla}]",
                [n["nivel"] for n in niveis] == [1, 2, 3, 4, 5]
                and niveis[3]["expressao"] == b.sonda
                and niveis[4]["expressao"] == b.executada,
                [(n["nivel"], n["expressao"]) for n in niveis])

        sem_prox = copy.deepcopy(dado)
        sem_prox["composicao"]["proximidade"] = "nenhum"
        # Sem proximidade, as transformações dela não se declaram (a leitura as recusa).
        for s_ in sem_prox.get("sondagens", []):
            for c_ in s_["consultas"]:
                c_.pop("sem_proximidade", None)
                c_.pop("distancia", None)
        cx_np = com_fonte(ctx, sigla, sem_prox, frag0, arqs0).com_config(cfg)
        _, _, niveis_np = monta_niveis(Busca(cx_np), sigla, sementes)
        g.testa("base sem proximidade funde os níveis 3 e 4 e mantém o 5",
                [n["nivel"] for n in niveis_np] == [1, 2, 3, 5]
                and niveis_np[2]["expressao"] == b.sonda,
                [(n["nivel"], n["expressao"]) for n in niveis_np])

        particionada = None
        for base in b.d["bases"]:
            try:
                dado_p, frag_p, arqs_p = fonte_de(ctx, b.d, base["sigla"])
            except LookupError:
                continue
            if dado_p["execucao"]["forma"] == "particionada":
                particionada = (base["sigla"], dado_p, frag_p, arqs_p)
                break
        if particionada is None:
            g.nao_executa("nenhuma base particionada para a recusa", quantos=1)
        else:
            sigla_p, dado_p, frag_p, arqs_p = particionada
            dado_p = copy.deepcopy(dado_p)
            dado_p.setdefault("composicao", {})[G.C_DOI_MODELO.chave] = f"DOI({G.MARCADOR_DOI})"
            cx_p = com_fonte(ctx, sigla_p, dado_p, frag_p, arqs_p).com_config(cfg)
            cod, _, erro = _roda_anatomia(
                lambda: (monta_niveis(Busca(cx_p), sigla_p, sementes), Saida.OK)[1])
            g.testa(f"base particionada reprova com REPROVADO [{sigla_p}]",
                    cod == Saida.REPROVADO and "consulta" in erro, f"{cod.name} {erro[:100]}")

        def resultado(retornos=None, exportacoes=None, data_hora="2026-11-25T10:00"):
            return _roda_anatomia(lambda: diagnosticar(
                bx, sigla, retornos or [], exportacoes or [], data_hora, sementes=sementes))

        cod, texto, erro = resultado(
            retornos=[(1, 5), (2, 4), (3, 3)],
            exportacoes=[(1, l1), (2, l2), (3, l3)])
        g.testa(f"diagnóstico aceito com os três níveis submetidos e os dois lidos [{sigla}]",
                cod == Saida.OK and not erro, f"{cod.name} {erro[:120]}")
        g.testa("o resumo por causa conta também a semente presente na executada",
                "presente na executada: 1" in texto, texto[-200:])
        g.testa("submissão no dia das execuções lidas não avisa de datas diferentes",
                "AVISO: execuções lidas" not in texto
                and "a conferir" not in texto, texto[-200:])
        rel = cfg.saida("anatomia", base=sigla)
        cons = cfg.saida("anatomia_consultas", base=sigla)
        linhas = {x["semente"]: x for x in _linhas_csv(rel)} if rel.exists() else {}
        causas = {k: x["causa"] for k, x in linhas.items()}
        g.testa("uma causa por semente, pelo primeiro nível vazio",
                causas == esperado, str(causas))
        g.testa("o filtro relata ano, idioma e tipo documental lidos do nível 1",
                "ano: 2020" in linhas.get("SX2", {}).get("observacao", "")
                and "idioma: eng" in linhas["SX2"]["observacao"]
                and "tipo: JOUR" in linhas["SX2"]["observacao"],
                linhas.get("SX2", {}).get("observacao", ""))
        g.testa("a semente presente na executada aponta a divergência do casamento por título",
                "casamento por título" in linhas.get("SX6", {}).get("observacao", ""),
                linhas.get("SX6", {}).get("observacao", ""))
        consultas = _linhas_csv(cons) if cons.exists() else []
        g.testa("anatomia_consultas: uma linha por nível, com a origem submetida ou lida",
                [x["nivel"] for x in consultas] == ["1", "2", "3", "4", "5"]
                and consultas[3]["origem"].startswith("execução")
                and consultas[4]["origem"].startswith("execução")
                and consultas[0]["origem"] == "submetido", str(consultas[-1:]))

        # Texto registrado diferente do vigente, ou ausente: o nível não se lê de execução,
        # e o roteiro o pede com o motivo. Com a conferência desligada, seria lido.
        from ..busca import anatomia as AN
        reg_mud = copy.deepcopy(registro)
        exs = reg_mud["bases"][b.bd_de[sigla]]["execucoes"]
        exs[0]["texto"] = exs[0]["texto"] + " OR zzz"
        exs[1].pop("texto")
        (pasta / "registro_mud.json").write_text(json.dumps(reg_mud), encoding="utf-8")
        cfg_m = Configuracao(cfg.com("dados.registro", str(pasta / "registro_mud.json")),
                             cfg.arquivo)
        bx_m = Busca(com_fonte(ctx, sigla, dado, frag0, arqs0).com_config(cfg_m))

        def roteiro_mud():
            return _roda_anatomia(lambda: diagnosticar(bx_m, sigla, [], [], "",
                                                       sementes=sementes))
        cod, texto_m, erro = roteiro_mud()
        g.testa("execução com texto diferente do vigente ou sem texto não se lê: o nível vai "
                "ao roteiro, com o motivo",
                cod == Saida.OK and "texto diferente do vigente" in texto_m
                and "sem texto registrado" in texto_m and "lido de" not in texto_m,
                f"{cod.name} {erro[:80]}")
        original = AN.motivo_sem_leitura
        AN.motivo_sem_leitura = lambda *a: None
        try:
            _, texto_sem, _ = roteiro_mud()
        finally:
            AN.motivo_sem_leitura = original
        g.testa("com a conferência do texto desligada, o nível seria lido (o caso falharia)",
                "lido de" in texto_sem, texto_sem[-120:])

        cod, texto_d, erro = resultado(retornos=[(1, 5), (2, 4), (3, 3)],
                                       exportacoes=[(1, l1), (2, l2), (3, l3)],
                                       data_hora="2026-11-27T10:00")
        obs_sx4 = {x["semente"]: x for x in _linhas_csv(rel)}.get("SX4", {}).get(
            "observacao", "") if rel.exists() else ""
        g.testa("submissão em outro dia avisa, e a causa proximidade sai a conferir",
                cod == Saida.OK and "AVISO: execuções lidas de 2026-11-25" in texto_d
                and "a conferir" in obs_sx4, f"{cod.name} {obs_sx4[:120]} {erro[:80]}")

        cod, _, erro = resultado(retornos=[(1, 6), (2, 4), (3, 3)],
                                 exportacoes=[(1, l1), (2, l2), (3, l3)])
        g.testa("exportação que não confere reprova com DADOS", cod == Saida.DADOS
                and "nível 1" in erro and "retorno 6" in erro, f"{cod.name} {erro[:100]}")
        cod, _, erro = resultado(retornos=[(1, 5), (3, 3)],
                                 exportacoes=[(1, l1), (3, l3)])
        g.testa("nível submetido sem resultado reprova com DADOS", cod == Saida.DADOS
                and "nível 2" in erro, f"{cod.name} {erro[:100]}")
        cod, _, erro = resultado(retornos=[(1, 5), (2, 4), (3, 0)],
                                 exportacoes=[(1, l1), (2, l2), (3, l3)])
        g.testa("exportação sobrando em nível de retorno 0 reprova com DADOS",
                cod == Saida.DADOS and "nível 3" in erro and "retorno 0" in erro,
                f"{cod.name} {erro[:100]}")
        cod, _, erro = resultado(retornos=[(1, 5), (2, 4), (3, 3), (4, 2)],
                                 exportacoes=[(1, l1), (2, l2), (3, l3)])
        g.testa("retorno sobrando em nível lido de execução reprova com DADOS",
                cod == Saida.DADOS and "nível 4" in erro, f"{cod.name} {erro[:100]}")
        cod, _, erro = resultado(retornos=[(1, 5), (2, 4), (3, 3)],
                                 exportacoes=[(1, l1), (2, l2), (3, l3)], data_hora="")
        g.testa("resultado sem --data-hora reprova com DADOS",
                cod == Saida.DADOS and "--data-hora" in erro, f"{cod.name} {erro[:100]}")

        sem_c = pasta / "sem_c.ris"
        sem_c.write_text(registros(["SX4", "SX5", "SX6"]), encoding="utf-8")
        com_c = pasta / "com_c.ris"
        com_c.write_text(registros(["SX3", "SX4", "SX5", "SX6"]), encoding="utf-8")
        cod, _, erro = resultado(retornos=[(1, 5), (2, 3), (3, 4)],
                                 exportacoes=[(1, l1), (2, sem_c), (3, com_c)])
        g.testa("DOI que reaparece num nível posterior reprova com REPROVADO",
                cod == Saida.REPROVADO and "nível 3" in erro and "10.0000/at.c" in erro,
                f"{cod.name} {erro[:100]}")

        estranho = pasta / "estranho.ris"
        estranho.write_text(_ris_anat([("Estranho", 2020, "10.9999/at.x", "eng", "JOUR")])
                            + registros(["SX2", "SX3", "SX4", "SX5"]), encoding="utf-8")
        cod, _, erro = resultado(retornos=[(1, 5), (2, 4), (3, 3)],
                                 exportacoes=[(1, estranho), (2, l2), (3, l3)])
        g.testa("DOI fora das sementes reprova com REPROVADO",
                cod == Saida.REPROVADO and "nível 1" in erro and "10.9999/at.x" in erro,
                f"{cod.name} {erro[:100]}")

        sem_doi = copy.deepcopy(dado0)
        sem_doi.get("composicao", {}).pop("doi", None)
        cx2 = com_fonte(ctx, sigla, sem_doi, frag0, arqs0).com_config(cfg)
        cod, _, erro = _roda_anatomia(lambda: diagnosticar(
            Busca(cx2), sigla, sementes=sementes))
        g.testa("base sem [composicao] doi reprova com REPROVADO, nomeando base e campo",
                cod == Saida.REPROVADO and sigla in erro and "doi" in erro
                and "composicao" in erro, f"{cod.name} {erro[:120]}")

        sem = copy.deepcopy(sementes)
        sem[0].pop("doi")
        with contextlib.redirect_stdout(io.StringIO()):
            sel = selecao(bx, sigla, sem)
        g.testa("semente sem DOI listada à parte e fora das consultas",
                [x["id"] for x in sel["sem_doi"]] == ["SX1"]
                and all(x["id"] != "SX1" for x in sel["diagnosticaveis"]),
                f"{[x['id'] for x in sel['sem_doi']]}")

        if outra is None:
            g.nao_executa("uma base só: sem outra base para a seleção por base", quantos=1)
        else:
            sx7 = {"id": "SX7", "titulo": titulo_sx7, "doi": "10.0000/at.g",
                   "bases": [sigla, outra], "ano": 2021}
            with contextlib.redirect_stdout(io.StringIO()):
                sel = selecao(bx, sigla, sementes + [sx7])
            g.testa(f"semente recuperada só em outra base ({outra}) é diagnosticada nesta",
                    any(x["id"] == "SX7" for x in sel["diagnosticaveis"]),
                    f"recuperadas: {sel['recuperadas']}")

        recuperada = {"id": "SX9", "titulo": titulo_exec, "doi": "10.0000/at.f",
                      "bases": [sigla], "ano": 2024}
        if rel.exists():
            rel.unlink()
        cod, texto, erro = _roda_anatomia(lambda: diagnosticar(
            bx, sigla, sementes=[recuperada]))
        g.testa("nada a diagnosticar informa e sai OK, sem gravar",
                cod == Saida.OK and "Nenhuma perda" in texto and not rel.exists(),
                f"{cod.name} {erro[:100]}")



# ------------------------------------------------------- análise da sensibilidade
def _ris_sim(linhas):
    """(título, ano, doi, palavras-chave, resumo) em RIS de ensaio."""
    return "".join(
        f"TY  - JOUR\nTI  - {titulo}\nAB  - {resumo}\nKW  - {kw}\nPY  - {ano}\n"
        f"DO  - {doi}\nER  - \n\n"
        for titulo, ano, doi, kw, resumo in linhas)


def _roda_analise(funcao):
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            r = funcao()
        return Saida(r), out.getvalue(), ""
    except ErroRSL as e:
        return Saida(e.codigo), out.getvalue(), str(e)


def sensibilidade_analise(ctx, g):
    """Análise da sensibilidade com executada e sonda sintéticas e amostra classificada: o
    casamento da amostra, a exclusão do candidato já no vocabulário, a contagem da simulação
    só sobre a perda e a recusa por amostra incompleta e por faceta âncora.

    O termo de ensaio aparece também num registro DA EXECUTADA: contar a executada na
    simulação somaria um registro a mais, e o caso da contagem reprovaria. O plural do termo
    é palavra-chave de um elegível e o único termo de um registro perdido fora da amostra:
    sem as formas de número, o plural seria candidato à parte e o acréscimo perderia um.
    """
    b, sigla, motivos = _base_que_compoe(ctx)
    if sigla is None:
        g.nao_executa("nenhuma base com composição legível — " + "; ".join(motivos))
        return
    _, comp = composicao_da_base(ctx, b.d, sigla)
    fct = next(f["id"] for f in b.d["facetas"] if f["id"] not in b.ancoras)
    termo = "special topic term"
    plural = "special topic terms"  # plural regular em inglês; pt e es não decidem
    # Três palavras-chave de prova, escolhidas pelos padrões da base:
    # - igual a termo de âncora: excluída;
    # - termo de âncora seguido de palavra sem sentido: só CONTÉM o termo, é candidata;
    # - termo de faceta não âncora: excluída, e num elegível é divergência do casamento.
    vocab = vocabulario_da_base(b, sigla)
    nao_ancora = [p for fid, f in vocab.items() if fid not in b.ancoras for p in f["padroes"]]
    simples = [(fid, t) for fid in comp.strings
               for t in comp.strings[fid]["termos"] if "*" not in t]
    termo_vocab = next(t for fid, t in simples if fid in b.ancoras
                       and not any(p.search(normaliza(f"{t} zzqx")) for p in nao_ancora))
    composto = normaliza(f"{termo_vocab} zzqx")
    termo_nao_ancora = next(t for fid, t in simples if fid == fct)
    executados = [("Registro da executada E1 do autoteste", 2020, "10.0000/sim.e1", "", ""),
                  ("Registro da executada E2 do autoteste", 2021, "10.0000/sim.e2", "", ""),
                  ("Registro da executada E3 do autoteste", 2022, "10.0000/sim.e3", "", ""),
                  (f"{termo} no registro da executada", 2023, "10.0000/sim.e4", "", "")]
    perdidos = [(f"Registro perdido L1 com {termo}", 2020, "10.0000/sim.l1",
                 f"{termo}; {termo_vocab}; {composto}; {termo_nao_ancora}", ""),
                (f"Registro perdido L2 com {termo}", 2021, "10.0000/sim.l2",
                 f"{termo}; {plural}", ""),
                (f"Registro perdido L3 com {termo}", 2022, "10.0000/sim.l3", termo, ""),
                (f"Registro perdido L4 com {plural}", 2023, "10.0000/sim.l4", "", "")]
    amostra = [("sim", "sim"), ("sim", "sim"), ("sim", "não")]
    with tempfile.TemporaryDirectory() as tmp:
        pasta = pathlib.Path(tmp)
        (pasta / "executada.ris").write_text(_ris_sim(executados), encoding="utf-8")
        (pasta / "sonda.ris").write_text(_ris_sim(executados + perdidos), encoding="utf-8")
        registro = {"bases": {b.bd_de[sigla]: {"base": sigla, "execucoes": [
            {"id": "EX1", "expressao": b.executada, "arquivo": str(pasta / "executada.ris"),
             "registros_lidos": len(executados), "status": "valida"},
            {"id": "EX2", "expressao": b.sonda, "arquivo": str(pasta / "sonda.ris"),
             "registros_lidos": len(executados) + len(perdidos), "status": "valida"}]}}}
        (pasta / "registro.json").write_text(json.dumps(registro), encoding="utf-8")
        cfg = ctx.config
        cfg = Configuracao(cfg.com("dados.registro", str(pasta / "registro.json")),
                           cfg.arquivo)
        cfg = Configuracao(cfg.com("saidas.pasta", str(pasta / "saidas")), cfg.arquivo)

        def escreve_amostra(classificacoes):
            rel = cfg.saida("sensibilidade", base=sigla)
            rel.parent.mkdir(parents=True, exist_ok=True)
            with rel.open("w", encoding="utf-8-sig", newline="") as fh:
                w = csv.writer(fh, delimiter=";")
                w.writerow(["chave", "ano", "titulo", "doi", "amostra", "elegivel"])
                for (titulo, ano, doi, _, _), (_, eleg) in zip(perdidos, classificacoes):
                    w.writerow([chave_dedup({"doi": doi, "titulo": titulo}), ano, titulo,
                                doi, "sim", eleg])
            return rel

        rel = escreve_amostra(amostra)
        bx = Busca(ctx.com_config(cfg))
        cod, texto, erro = _roda_analise(lambda: analisa(bx, sigla))
        g.testa("amostra inteira casada com a perda e analisada",
                cod == Saida.OK and "CASAMENTO LOCAL NA AMOSTRA — 3 registros" in texto,
                f"{cod.name} {erro[:100]}")
        candidatos = {x["termo"]: x for x in _linhas_csv(cfg.saida("candidatos", base=sigla))}
        g.testa("candidato já no vocabulário da base é excluído; o termo novo entra",
                normaliza(termo_vocab) not in candidatos
                and normaliza(termo_nao_ancora) not in candidatos and termo in candidatos,
                str(sorted(candidatos)[:5]))
        g.testa("o plural de outra candidata entra no grupo dela, e não é candidato à parte",
                plural not in candidatos
                and plural in candidatos.get(termo, {}).get("formas", "").split("; "),
                str({k: v.get("formas") for k, v in candidatos.items()}))
        g.testa(f"palavra-chave que só contém termo de âncora é candidata ({composto!r})",
                composto in candidatos, str(sorted(candidatos)[:5]))
        excl = texto.split("PALAVRAS-CHAVE EXCLUÍDAS", 1)[-1].split("LIMITES", 1)[0]
        g.testa("as excluídas saem listadas à parte, com o motivo",
                f"{normaliza(termo_vocab)} " in excl and "(âncora)" in excl
                and f"{normaliza(termo_nao_ancora)} " in excl and "(não âncora)" in excl,
                excl[:200])
        g.testa(f"elegível com termo de {fct} sai como divergência do casamento local",
                "DIVERGÊNCIA DO CASAMENTO LOCAL — 1 elegível" in texto
                and fct in texto.split("DIVERGÊNCIA DO CASAMENTO LOCAL", 1)[-1][:300],
                texto[:300])
        with contextlib.redirect_stdout(io.StringIO()):
            _, sem_kw, *_ = candidatos_da_amostra(bx, sigla, [
                ({"chave": "k1", "elegivel": "sim"},
                 {"titulo": "t1", "resumo": "", "palavras_chave": ""}),
                ({"chave": "k2", "elegivel": "sim"},
                 {"titulo": "t2", "resumo": "", "palavras_chave": "zzqx"}),
                ({"chave": "k3", "elegivel": "não"},
                 {"titulo": "t3", "resumo": "", "palavras_chave": ""})], {})
        g.testa("elegível sem palavras-chave é contado à parte (1 de 2 elegíveis)",
                sem_kw == 1, str(sem_kw))
        linha = candidatos.get(termo, {})
        g.testa("candidato: 2 elegíveis, 1 não elegível e acréscimo de 4 na perda, com o "
                "registro que só traz o plural",
                (linha.get("elegiveis"), linha.get("nao_elegiveis"),
                 linha.get("acrescimo")) == ("2", "1", "4"), str(linha))

        # Fronteira na análise: o termo inteiro numa palavra-chave é candidato; o mesmo par
        # partido em duas palavras-chave não alcança o registro da perda.
        fronteira = "zzqx zzqy"
        com_termo = {"titulo": "", "resumo": "", "palavras_chave": fronteira, "base": sigla}
        com_partes = {"titulo": "", "resumo": "",
                      "palavras_chave": f"zzqx{SEPARADOR_VALORES}zzqy", "base": sigla}
        with contextlib.redirect_stdout(io.StringIO()):
            linhas_f, *_ = candidatos_da_amostra(
                bx, sigla, [({"chave": "F1", "elegivel": "sim"}, com_termo)],
                {"F2": com_partes})
        cand = {x[0]: x for x in linhas_f}.get(fronteira)
        g.testa("fronteira na análise: termo de duas palavras não alcança o registro com as "
                "partes em palavras-chave distintas",
                cand is not None and cand[3] == 0, str(cand))
        g.testa("controle da fronteira na análise: com o texto unido, o termo alcançaria",
                any(p.search(texto_do(com_partes)) for p in [padrao(fronteira)]),
                texto_do(com_partes))

        cod, texto, erro = _roda_analise(lambda: analisa(bx, sigla, [(fct, termo)]))
        g.testa("simulação conta só a perda, com as formas de número do termo: 2/2 "
                "elegíveis, 1/1 não elegível, +4, total 8",
                cod == Saida.OK and "CONJUNTO: 2/2 elegíveis" in texto
                and f"(com {plural!r})" in texto
                and "1/1 não elegíveis, +4 registros (total 8)" in texto,
                f"{cod.name} {texto[-300:]}")

        escreve_amostra([("sim", "sim"), ("sim", ""), ("sim", "não")])
        cod, _, erro = _roda_analise(lambda: analisa(bx, sigla))
        g.testa("amostra incompleta reprova com DADOS, informando 2 de 3",
                cod == Saida.DADOS and "2 de 3" in erro, f"{cod.name} {erro[:120]}")

        escreve_amostra(amostra)
        cod, _, erro = _roda_analise(lambda: analisa(
            bx, sigla, [(sorted(b.ancoras)[0], termo)]))
        g.testa("faceta âncora recusada com USO", cod == Saida.USO and "âncora" in erro,
                f"{cod.name} {erro[:120]}")


@contextlib.contextmanager
def _sem_zotero(chamadas):
    """Todo pedido de rede e toda construção de cliente do Zotero são registrados e falham:
    o caso prova que as análises não consultam o Zotero."""
    import urllib.request                                           # noqa: PLC0415
    from .. import zotero as Z                                      # noqa: PLC0415
    antes_abrir, antes_cliente = urllib.request.urlopen, Z.cliente

    def abrir(req, *a, **k):
        chamadas.append(getattr(req, "full_url", str(req)))
        raise AssertionError("pedido de rede durante a análise")

    def cliente(*a, **k):
        chamadas.append("zotero.cliente")
        raise AssertionError("cliente do Zotero construído durante a análise")
    urllib.request.urlopen, Z.cliente = abrir, cliente
    try:
        yield
    finally:
        urllib.request.urlopen, Z.cliente = antes_abrir, antes_cliente


def exportacao_do_cache(ctx, g):
    """Execução registrada com `identificador`: a exportação é lida do cache em
    `[dados] execucoes`, pelo ponto único de resolução. Cache vazio é DADOS, nomeando a
    execução e a obtenção do Zotero, sem pedido ao Zotero; com o arquivo no cache, a mesma
    derivação passa (controle)."""
    from ..dados import problemas_registro                         # noqa: PLC0415
    b, sigla, motivos = _base_que_compoe(ctx)
    if sigla is None:
        g.nao_executa("nenhuma base com composição legível — " + "; ".join(motivos),
                      quantos=5)
        return
    bd = b.bd_de[sigla]
    executados = [(f"Registro sintetico {k} do cache no autoteste", b.ano_min,
                   f"10.0000/autoteste.cache.{k}") for k in (1, 2)]
    ids = {"EX1": "a1b2c3d4e5f6", "EX2": "f6e5d4c3b2a1"}
    with tempfile.TemporaryDirectory() as tmp:
        pasta = pathlib.Path(tmp)
        registro = {"bases": {x["id"]: {"base": x["sigla"], "execucoes": []}
                              for x in b.d["bases"]}}
        registro["bases"][bd]["execucoes"] = [
            {"id": "EX1", "expressao": b.executada, "identificador": ids["EX1"],
             "registros_lidos": len(executados), "status": "valida"},
            {"id": "EX2", "expressao": b.sonda, "identificador": ids["EX2"],
             "registros_lidos": len(executados), "status": "valida"}]
        (pasta / "registro.json").write_text(json.dumps(registro), encoding="utf-8")
        dado = copy.deepcopy(ctx.config.dado)
        dado["dados"].update(registro=str(pasta / "registro.json"),
                             temporarios=str(pasta / "tmp"),
                             execucoes=str(pasta / "tmp" / "execucoes"))
        dado["saidas"]["pasta"] = str(pasta / "saidas")
        cfg = Configuracao(dado, ctx.config.arquivo)
        cx = ctx.com_config(cfg)
        bx = Busca(cx)
        chamadas = []
        with _sem_zotero(chamadas):
            cod_d, _, erro_d = _roda_analise(lambda: derivar(bx))
            cod_s, _, erro_s = _roda_analise(lambda: sensibilidade(bx, sigla))
            problemas = problemas_registro(cx, registro, [x["id"] for x in b.d["bases"]])
        esperado = cfg.caminho("dados.execucoes") / sigla / f"{ids['EX1']}.ris"
        g.testa("cache vazio: `busca derivar` sai com DADOS, nomeia a execução e indica a "
                "obtenção do Zotero",
                cod_d == Saida.DADOS and f"{bd}/EX1" in erro_d and OBTER_DO_ZOTERO in erro_d
                and esperado.name in erro_d, f"{cod_d.name} {erro_d[:160]}")
        g.testa("cache vazio: `conferencia sensibilidade` sai com DADOS e indica a obtenção",
                cod_s == Saida.DADOS and OBTER_DO_ZOTERO in erro_s,
                f"{cod_s.name} {erro_s[:160]}")
        g.testa("cache vazio: `dados conferir` relata a execução e a obtenção do Zotero",
                any(f"{bd}/EX1" in x and OBTER_DO_ZOTERO in x for x in problemas),
                f"{problemas[:1]}")
        g.testa("cache vazio: nenhum pedido ao Zotero nem cliente construído",
                not chamadas, f"{chamadas[:2]}")
        prova = []
        with _sem_zotero(prova):
            from .. import zotero as Z                              # noqa: PLC0415
            try:
                Z.cliente(cx)
            except AssertionError:
                pass
        g.testa("o detector registra a construção de cliente do Zotero (sem isso, o caso acima "
                "nada provaria)", bool(prova), "nada registrado")
        esperado.parent.mkdir(parents=True)
        esperado.write_text(_ris(executados), encoding="utf-8")
        (esperado.parent / f"{ids['EX2']}.ris").write_text(_ris(executados),
                                                           encoding="utf-8")
        with _sem_zotero(chamadas):
            cod_c, saida_c, erro_c = _roda_analise(lambda: derivar(bx))
        g.testa("controle: com a exportação no cache (<execucoes>/<sigla>/<identificador>.ris)"
                ", a mesma derivação lê os registros, sem pedido ao Zotero",
                cod_c == Saida.OK and not chamadas
                and f"{len(executados)} registros" in saida_c, f"{cod_c.name} {erro_c[:160]}")


def leitor_ris(ctx, g):
    """Leitura RIS do original da base e da reexportação do Zotero: BOM inicial, autores em
    `A1`, título dos anais em `C3`, só o primeiro `DO` e o tipo na forma canônica. Cada caso
    tem o controle que mostra o que o defeito faria."""
    bom = "\ufeffTY  - JOUR\nTI  - Primeiro registro com BOM\nER  - \n"
    r = le_ris(bom)
    g.testa("BOM inicial: o TY do primeiro registro é lido",
            len(r) == 1 and r[0]["tipo"] == "JOUR", f"{r[:1]}")
    g.testa("controle do BOM: sem retirá-lo, a expressão das tags não casaria a primeira linha",
            re.match(r"^([A-Z][A-Z0-9])\s+-\s?(.*)$", bom.splitlines()[0]) is None
            and re.match(r"^([A-Z][A-Z0-9])\s+-\s?(.*)$",
                         bom.lstrip("\ufeff").splitlines()[0]) is not None,
            "a primeira linha casaria mesmo com o BOM")
    r = le_ris("TY  - CHAP\nAU  - Eybers, OO\nA1  - Muller, A\nTI  - Capítulo\n"
               "T2  - Livro\nDO  - 10.1/a.ch1\nDO  - 10.1/a\nER  - \n")[0]
    g.testa("`A1` entra nos autores, depois de `AU`",
            r["autores"] == f"Eybers, OO{SEPARADOR_VALORES}Muller, A", r["autores"])
    g.testa("só o primeiro `DO` vale, e a chave de deduplicação sai dele",
            r["doi"] == "10.1/a.ch1" and chave_dedup(r) == "doi:10.1/a.ch1", r["doi"])
    conf = le_ris("TY  - CONF\nTI  - Trabalho\nC3  - Anais do Autoteste\nER  - \n")[0]
    g.testa("`C3` (título dos anais na exportação do Zotero) é a fonte",
            conf["fonte"] == "Anais do Autoteste", conf["fonte"])
    tipos = {x: le_ris(f"TY  - {x}\nTI  - T\nER  - \n")[0]["tipo"]
             for x in ("CPAPER", "CONF", "CHAP", "label.ris.referenceType.BOOK_CHAPTER", "JOUR")}
    g.testa("tipo canônico: CONF = CPAPER, rótulo de capítulo da Scopus = CHAP, JOUR intacto",
            tipos == {"CPAPER": "CPAPER", "CONF": "CPAPER", "CHAP": "CHAP",
                      "label.ris.referenceType.BOOK_CHAPTER": "CHAP", "JOUR": "JOUR"}
            and set(TIPOS_RIS.values()) <= {"CPAPER", "CHAP"}, f"{tipos}")


def identificador(ctx, g):
    """Identificador da execução (D4): indiferente à ordem dos registros, diferente com um
    registro a mais e com outra data e hora; 12 hexadecimais."""
    regs = le_ris(_ris([(f"Registro sintetico {k}", 2020, f"10.0000/autoteste.id.{k}")
                        for k in range(5)]))
    base = identificador_execucao("wos", "EB4", "2026-11-25T20:54:46-03:00", regs)
    g.testa("identificador: 12 hexadecimais",
            len(base) == 12 and all(c in "0123456789abcdef" for c in base), base)
    g.testa("identificador indiferente à ordem dos registros",
            identificador_execucao("wos", "EB4", "2026-11-25T20:54:46-03:00",
                                   list(reversed(regs))) == base)
    g.testa("identificador muda com um registro a mais",
            identificador_execucao("wos", "EB4", "2026-11-25T20:54:46-03:00",
                                   regs + regs[:1]) != base)
    g.testa("identificador muda com a mesma lista em outra data e hora",
            identificador_execucao("wos", "EB4", "2026-11-26T20:54:46-03:00", regs) != base)
