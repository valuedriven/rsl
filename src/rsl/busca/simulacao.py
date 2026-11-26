"""Análise da sensibilidade: o que os elegíveis perdidos têm que a executada não alcança.

Lê a amostra classificada da sonda de sensibilidade e as exportações registradas da
executada e da sonda. A perda é a sonda menos a executada, chaveada como na sensibilidade.
O casamento local, com o vocabulário da base, diz quais facetas reconhece em cada registro
da amostra; as palavras-chave dos elegíveis, menos as que o vocabulário já reconhece, são os
candidatos, e com `--termo` se simula a executada ampliada sobre a perda. O alcance de um
candidato ou de um termo simulado se mede com as suas formas de número, pela mesma flexão
que dá as formas do vocabulário da base: a string emendada as traria.

O comando não altera string, protocolo nem fonte: informa a decisão do pesquisador.
"""

import csv

from ..config import relativo
from ..erros import DadosInvalidos, Uso
from ..flexao import Indecidivel, formas, le_excecoes
from ..markdown import normaliza
from ..saida import Saida
from . import Busca
from .aderencia import wilson
from .derivacao import carrega_facetas, facetas_atingidas, padrao, texto_do
from .registro import carrega_consultas, chave_dedup
from .sensibilidade import registros_da_expressao

SIM = ("sim", "s", "1", "true")
NAO = ("não", "nao", "n", "0", "false")


def elegivel(linha):
    """A classificação da amostra como booleano; valor fora de sim/não sai com DADOS."""
    v = (linha.get("elegivel") or "").strip().lower()
    if v in SIM:
        return True
    if v in NAO:
        return False
    raise DadosInvalidos(f"amostra, chave {linha.get('chave')!r}: `elegivel` = "
                         f"{linha.get('elegivel')!r} fora de sim/não")


def le_amostra(b, sigla):
    """Linhas da amostra (coluna `amostra = sim`), todas classificadas; DADOS se faltar."""
    rel = b.config.saida("sensibilidade", base=sigla)
    if not rel.exists():
        raise DadosInvalidos(f"{relativo(rel)} não existe: rode `python3 -m rsl conferencia "
                             f"sensibilidade {sigla}` e classifique a amostra")
    with rel.open(encoding="utf-8-sig", newline="") as fh:
        linhas = list(csv.DictReader(fh, delimiter=";"))
    amostra = [x for x in linhas if (x.get("amostra") or "").strip().lower() == "sim"]
    if not amostra:
        raise DadosInvalidos(f"{relativo(rel)}: nenhuma linha com `amostra = sim`; não há "
                             f"amostra a analisar")
    faltam = [x for x in amostra if not (x.get("elegivel") or "").strip()]
    if faltam:
        raise DadosInvalidos(
            f"{relativo(rel)}: {len(amostra) - len(faltam)} de {len(amostra)} linhas da "
            f"amostra classificadas — a análise exige a amostra inteira. Classifique a "
            f"coluna `elegivel` (primeira pendente: {faltam[0].get('chave')!r})")
    return amostra


def leitura_da_perda(b, sigla):
    """(registros da executada, registros da sonda, perda por chave)."""
    _, validas = carrega_consultas(b)
    executada = registros_da_expressao(sigla, b.executada, validas)
    sonda = registros_da_expressao(sigla, b.sonda, validas)
    if executada is None:
        raise DadosInvalidos(f"{sigla}: sem execução registrada de {b.executada} (a "
                             f"executada); a perda é {b.sonda} \\ {b.executada}")
    if sonda is None:
        raise DadosInvalidos(f"{sigla}: sem execução registrada de {b.sonda} (a sonda); a "
                             f"perda é {b.sonda} \\ {b.executada}")
    for r in sonda:
        r["base"] = sigla
    chaves_exec = {chave_dedup(r) for r in executada}
    perda = {}
    for r in sonda:
        k = chave_dedup(r)
        if k not in chaves_exec:
            perda[k] = r
    return executada, sonda, perda


def casa_amostra(amostra, perda, sigla):
    """[(linha, registro da perda)] na ordem da amostra; linha sem par sai com DADOS."""
    pares, faltam = [], []
    for linha in amostra:
        reg = perda.get(linha.get("chave", ""))
        if reg is None:
            faltam.append(linha.get("chave", ""))
        else:
            pares.append((linha, reg))
    if faltam:
        raise DadosInvalidos(
            f"{len(faltam)} linha(s) da amostra sem par na perda (sonda \\ executada): "
            f"{', '.join(faltam[:5])}{' …' if len(faltam) > 5 else ''}. A amostra e as "
            f"exportações registradas não são do mesmo conjunto: refaça `conferencia "
            f"sensibilidade {sigla}` sobre as execuções correntes e reclassifique")
    return pares


def facetas_reconhecidas(b, sigla, pares):
    """({fid: {"elegivel": n, "nao": n}}, divergências). A divergência é o elegível em que o
    casamento local reconhece faceta não âncora: aproximação do casamento, não do vocabulário.
    """
    vocab = carrega_facetas(b, [sigla])
    contagem = {f["id"]: {"elegivel": 0, "nao": 0} for f in b.d["facetas"]}
    divergencias = []
    for linha, reg in pares:
        fac = facetas_atingidas(reg, vocab)
        e = elegivel(linha)
        for fid in fac:
            if fid in contagem:
                contagem[fid]["elegivel" if e else "nao"] += 1
        nao_ancora = sorted(fac - b.ancoras)
        if e and nao_ancora:
            divergencias.append((linha.get("chave", ""), nao_ancora, sorted(fac)))
    return contagem, divergencias


def relata_facetas(b, amostra, pares, contagem, divergencias):
    """Imprime o casamento local na amostra e as divergências."""
    elegiveis = sum(1 for x in amostra if elegivel(x))
    nao = len(amostra) - elegiveis
    print(f"\nCASAMENTO LOCAL NA AMOSTRA — {len(amostra)} registros ({elegiveis} elegíveis, "
          f"{nao} não elegíveis)")
    for f in b.d["facetas"]:
        c = contagem[f["id"]]
        papel = "âncora" if f["id"] in b.ancoras else "não âncora"
        print(f"  {f['id']} ({papel}): {c['elegivel']:>2} elegíveis, {c['nao']:>2} não "
              f"elegíveis")
    nao_ancora = [f["id"] for f in b.d["facetas"] if f["id"] not in b.ancoras]
    if divergencias:
        print(f"\n  DIVERGÊNCIA DO CASAMENTO LOCAL — {len(divergencias)} elegível(is) com "
              f"faceta não âncora reconhecida ({', '.join(nao_ancora)}):")
        for chave, reconhecidas, todas in divergencias:
            print(f"    {chave}: {', '.join(reconhecidas)} (todas: {', '.join(todas)})")
        print("  É aproximação do casamento local, não falha de vocabulário: conferir à mão.")
    else:
        print(f"\n  Nenhum elegível tem faceta não âncora reconhecida ({', '.join(nao_ancora)}) "
              f"pelo casamento local.")


def palavras_chave(reg):
    """Palavras-chave do registro, separadas como o leitor as une."""
    return [x.strip() for x in (reg.get("palavras_chave") or "").split(";") if x.strip()]


def motivo_de_exclusao(t, nao_ancora, ancora):
    """Por que a palavra-chave normalizada `t` não é candidata, ou None se é.

    Exclui-se a que um termo de faceta não âncora reconhece (`search`) e a que um termo de
    âncora casa inteira (`fullmatch`, com as formas de número da base). A que só CONTÉM
    termo de âncora continua candidata: todo registro da perda já passa pelas âncoras, e
    isso não diz que as facetas não âncora cobrem o conceito."""
    reconhece = sorted({fid for fid, p in nao_ancora if p.search(t)})
    if reconhece:
        return f"reconhecida por {', '.join(reconhece)} (não âncora)"
    igual = sorted({fid for fid, p in ancora if p.fullmatch(t)})
    if igual:
        return f"igual a termo de {', '.join(igual)} (âncora)"
    return None


def formas_do_termo(termo, idiomas, excecoes):
    """O termo e as suas formas de número (regra regular ou exceção declarada) em cada
    idioma do protocolo, como `vocabulario_da_base` as gera para os termos da string. O
    idioma de uma palavra-chave não se conhece, e por isso se aplicam todos; o que a regra
    não decide (`curriculum`, terminação -s) não acrescenta forma."""
    saida = {termo}
    for i in idiomas:
        try:
            saida |= {f for f, _ in formas(termo, i, excecoes)}
        except Indecidivel:
            pass
    return saida


def agrupa_por_numero(termos, idiomas, excecoes):
    """{representante: formas} dos candidatos: a palavra-chave que é forma de número de
    outra candidata entra no grupo dela (`students` no de `student`). O representante é o
    membro que não é forma de outro; as formas do grupo, as de todos os membros."""
    termos = set(termos)
    formas_de = {t: {normaliza(f) for f in formas_do_termo(t, idiomas, excecoes)}
                 for t in termos}
    pai = {t: t for t in termos}

    def raiz(t):
        while pai[t] != t:
            t = pai[t]
        return t

    for t in sorted(termos):
        for f in formas_de[t] - {t}:
            if f in termos:
                a, c = raiz(t), raiz(f)
                if a != c:
                    pai[max(a, c)] = min(a, c)
    membros = {}
    for t in termos:
        membros.setdefault(raiz(t), set()).add(t)
    grupos = {}
    for grupo in membros.values():
        flexionados = {f for t in grupo for f in formas_de[t] - {t}}
        base = sorted(t for t in grupo if t not in flexionados) or sorted(grupo)
        grupos[base[0]] = set().union(*(formas_de[t] for t in grupo))
    return grupos


def presentes(formas_, textos):
    """As formas que casam em algum dos textos, em ordem: as que contribuíram para a
    contagem. A regra aplicada em idioma que não é o da palavra dá forma que não existe
    (`curriculuns`), que não casa em nada e não se relata."""
    return [f for f in sorted(formas_) if any(padrao(f).search(x) for x in textos)]


def candidatos(b, sigla, pares, perda):
    """([(termo, elegíveis, não elegíveis, acréscimo, formas)] na ordem do relato, número de
    elegíveis sem palavras-chave, {palavra-chave excluída: motivo}, número de palavras-chave
    candidatas antes do agrupamento). As palavras-chave que
    são forma de número uma da outra formam um candidato só, e o alcance se mede com
    `padrao` de cada forma sobre `texto_do`."""
    vocab = carrega_facetas(b, [sigla])[sigla]
    nao_ancora = [(fid, p) for fid, f in vocab.items() if fid not in b.ancoras
                  for p in f["padroes"]]
    ancora = [(fid, p) for fid, f in vocab.items() if fid in b.ancoras
              for p in f["padroes"]]
    elegiveis = [(linha, reg, texto_do(reg)) for linha, reg in pares if elegivel(linha)]
    nao_elegiveis = [(linha, reg, texto_do(reg)) for linha, reg in pares
                     if not elegivel(linha)]
    perdidos = [texto_do(reg) for reg in perda.values()]
    sem_palavras = sum(1 for _, reg, _ in elegiveis
                       if not (reg.get("palavras_chave") or "").strip())
    termos, excluidas = set(), {}
    for _, reg, _ in elegiveis:
        for kw in palavras_chave(reg):
            t = normaliza(kw)
            if not t or t in termos or t in excluidas:
                continue
            motivo = motivo_de_exclusao(t, nao_ancora, ancora)
            if motivo:
                excluidas[t] = motivo
            else:
                termos.add(t)
    grupos = agrupa_por_numero(termos, b.d["idiomas"], le_excecoes(b.ctx))
    linhas = []
    for t, todas in grupos.items():
        ps = [padrao(f) for f in sorted(todas)]
        el = sum(1 for _, _, texto in elegiveis if any(p.search(texto) for p in ps))
        ne = sum(1 for _, _, texto in nao_elegiveis if any(p.search(texto) for p in ps))
        acrescimo = sum(1 for texto in perdidos if any(p.search(texto) for p in ps))
        textos = [x for _, _, x in elegiveis + nao_elegiveis] + perdidos
        linhas.append((t, el, ne, acrescimo, presentes(todas - {t}, textos)))
    linhas.sort(key=lambda x: (-x[1], x[3], x[0]))
    return linhas, sem_palavras, excluidas, len(termos)


def grava_candidatos(b, sigla, linhas):
    rel = b.config.saida("candidatos", base=sigla)
    rel.parent.mkdir(parents=True, exist_ok=True)
    with rel.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["termo", "elegiveis", "nao_elegiveis", "acrescimo", "formas"])
        for t, el, ne, acrescimo, outras in linhas:
            w.writerow([t, el, ne, acrescimo, "; ".join(outras)])
    return rel


def valida_termos(b, termos):
    """[(FCTn, termo)] conferidos: a faceta existe e não é âncora; o termo não é vazio."""
    nao_ancora = [f["id"] for f in b.d["facetas"] if f["id"] not in b.ancoras]
    facetas = [f["id"] for f in b.d["facetas"]]
    saida = []
    for fct, termo in termos:
        if fct not in facetas:
            raise Uso(f"faceta {fct!r} não existe; as facetas não âncora do protocolo são "
                      f"{', '.join(nao_ancora)}")
        if fct in b.ancoras:
            raise Uso(f"{fct} é âncora obrigatória: a perda está dentro das âncoras da "
                      f"sonda, e ampliar âncora não se simula sobre ela. As facetas não "
                      f"âncora são {', '.join(nao_ancora)}")
        t = (termo or "").strip()
        if not t:
            raise Uso(f"--termo {fct}: termo vazio")
        saida.append((fct, t))
    return saida


def simula(b, termos, pares, perda, executada):
    """Relato da executada ampliada: para cada termo e para o conjunto, os elegíveis e não
    elegíveis da amostra recuperados, o acréscimo à executada e o total ampliado."""
    elegiveis = [texto_do(reg) for linha, reg in pares if elegivel(linha)]
    nao_elegiveis = [texto_do(reg) for linha, reg in pares if not elegivel(linha)]
    perdidos = [texto_do(reg) for reg in perda.values()]
    total_exec = len({chave_dedup(r) for r in executada})
    idiomas, excecoes = b.d["idiomas"], le_excecoes(b.ctx)
    itens = []
    for fct, t in termos:
        todas = formas_do_termo(t, idiomas, excecoes)
        itens.append((fct, t, presentes(todas - {t}, elegiveis + nao_elegiveis + perdidos),
                      [padrao(f) for f in sorted(todas)]))

    def conta(padroes):
        el = sum(1 for texto in elegiveis if any(p.search(texto) for p in padroes))
        ne = sum(1 for texto in nao_elegiveis if any(p.search(texto) for p in padroes))
        acrescimo = sum(1 for texto in perdidos if any(p.search(texto) for p in padroes))
        return el, ne, acrescimo

    print(f"\nSIMULAÇÃO DA EXECUTADA AMPLIADA — {b.executada} com os termos acrescentados")
    print(f"  executada atual: {total_exec} registros; amostra: {len(elegiveis)} elegíveis, "
          f"{len(nao_elegiveis)} não elegíveis")
    for fct, t, outras, ps in itens:
        el, ne, acrescimo = conta(ps)
        lo, hi = wilson(el, len(elegiveis)) if elegiveis else (0.0, 0.0)
        com = f" (com {', '.join(repr(x) for x in outras)})" if outras else ""
        print(f"  {fct} + {t!r}{com}: {el}/{len(elegiveis)} elegíveis ({lo:.1%}–{hi:.1%}), "
              f"{ne}/{len(nao_elegiveis)} não elegíveis, +{acrescimo} registros "
              f"(total {total_exec + acrescimo})")
    el, ne, acrescimo = conta([p for *_, ps in itens for p in ps])
    lo, hi = wilson(el, len(elegiveis)) if elegiveis else (0.0, 0.0)
    print(f"  CONJUNTO: {el}/{len(elegiveis)} elegíveis ({lo:.1%}–{hi:.1%}), "
          f"{ne}/{len(nao_elegiveis)} não elegíveis, +{acrescimo} registros "
          f"(total {total_exec + acrescimo})")
    return el, acrescimo


def relata_limites(amostra):
    """Os limites do cálculo: casamento local, amostra e remissão à fidelidade."""
    print("\nLIMITES DO RELATO")
    print("  Os números vêm do casamento local, que aproxima a base: não reproduz "
          "proximidade, campo nem lematização além do vocabulário da base.")
    print(f"  A fração de elegíveis é medida na amostra de {len(amostra)} registros, não no "
          f"conjunto da perda; o acréscimo é contado no conjunto inteiro da perda.")
    print("  O alcance de cada candidato e de cada termo simulado inclui as formas de número "
          "da regra regular dos idiomas do protocolo e das exceções declaradas, e o relato "
          "mostra as que casaram em algum registro. A forma que a regra não decide (ex.: "
          "-um, -s) fica de fora até haver exceção, e as duas palavras-chave continuam "
          "candidatas separadas (`curriculum` e `curricula`).")
    print("  A medida da aproximação é `python3 -m rsl conferencia fidelidade`.")


def analisa(b, base, termos=()):
    """Relato completo da análise da sensibilidade de uma base; `termos` simula a ampliação."""
    _, sigla = b.exige_bd(base)
    termos = valida_termos(b, termos) if termos else ()
    amostra = le_amostra(b, sigla)
    executada, _, perda = leitura_da_perda(b, sigla)
    pares = casa_amostra(amostra, perda, sigla)
    contagem, divergencias = facetas_reconhecidas(b, sigla, pares)
    relata_facetas(b, amostra, pares, contagem, divergencias)
    linhas, sem_palavras, excluidas, n_palavras = candidatos(b, sigla, pares, perda)
    print(f"\nTERMOS CANDIDATOS — {len(linhas)} candidato(s), de {n_palavras} palavras-chave "
          f"de elegíveis novas para as facetas não âncora (as formas de número de uma mesma "
          f"palavra formam um candidato só)")
    if sem_palavras:
        print(f"  {sem_palavras} elegível(is) sem palavras-chave na exportação: não "
              f"contribuem candidatos.")
    for t, el, ne, acrescimo, outras in linhas[:40]:
        com = f"  (com {', '.join(outras)})" if outras else ""
        print(f"  {t:<40} {el:>2} elegíveis  {ne:>2} não elegíveis  +{acrescimo} "
              f"registros{com}")
    if len(linhas) > 40:
        print(f"  … e mais {len(linhas) - 40}; o arquivo traz todos.")
    rel = grava_candidatos(b, sigla, linhas)
    print(f"  Candidatos em {relativo(rel)}.")
    print(f"\nPALAVRAS-CHAVE EXCLUÍDAS — {len(excluidas)} (reconhecidas por faceta não "
          f"âncora, ou iguais a termo de âncora; a que só contém termo de âncora é candidata)")
    for t in sorted(excluidas):
        print(f"  {t:<40} {excluidas[t]}")
    if termos:
        simula(b, termos, pares, perda, executada)
    relata_limites(amostra)
    print("\n  A escolha dos termos, a validação terminológica e a emenda são decisão do "
          "pesquisador; este comando não altera string, protocolo nem fonte.")
    return Saida.OK


def cmd_simular(ctx, a):
    return analisa(Busca(ctx), a.base, a.termo or [])

