"""Autoteste dos procedimentos de busca: a cobertura da base reprova procedimento de busca
divergente do protocolo, e só na base afetada.

As bases e os termos de cada caso são escolhidos pela estrutura lida: "a primeira base sem
derivação radical", "a primeira base que declara a forma radical", "um termo vigente da
string que nenhum outro cobre", "um termo do quadro que a STR não traz". Caso cuja
condição o documento corrente não oferece falha como mutação não aplicável.
"""

import re

from .. import gramatica as G
from ..cobertura import (_mesmo_termo, _par_irregular, _radical_alcanca, _radical_sem_alcance,
                         _vocabulario, cobertura_base, maior_consulta, subsumidos_na_base)
from ..geracao import esperada
from ..erros import ProtocoloInvalido
from ..fichas import base_derivada, ficha, termos_bloco
from ..markdown import normaliza, secao
from ..saida import Saida
from .textos import coluna, edita_celula, linhas_de_tabela_do_trecho, retira_termo_citado

R, P, OK = Saida.REPROVADO, Saida.PROTOCOLO_ILEGIVEL, Saida.OK
INVENTADO = "invented search term"
RETIRADO = "retired quadro term"
MOTIVO_RADICAL = f"alcançado pela forma {G.DERIVACAO_RADICAL} declarada"


def _insere_antes_do_primeiro(bloco, novo):
    """`"novo" OR ` antes do primeiro termo entre aspas do bloco."""
    return re.sub(r'"([^"]+)"', lambda m: f'"{novo}" OR "{m.group(1)}"', bloco, count=1)


def casos(ctx, g):
    d = ctx.protocolo()
    siglas = [b["sigla"] for b in d["bases"]]
    textos = {s: ficha(ctx, d, s) for s in siglas}
    lidas = {s: base_derivada(ctx, d, s) for s in siglas}

    def radical(s):
        return G.DERIVACAO_RADICAL in lidas[s]["declaracao"]["derivacoes"]

    sem_radical = [s for s in siglas if not radical(s)] or siglas
    com_radical = [s for s in siglas if radical(s)]
    A = sem_radical[0]
    D = sem_radical[-1]
    F = next((s for s in siglas if s not in (A,)), A)
    RAD = com_radical[0] if com_radical else None
    E = RAD or A
    executada = d["executada"]

    def problemas_de(s, texto, dd=None):
        dd = d if dd is None else dd
        try:
            p = cobertura_base(base_derivada(ctx, dd, s, texto), dd)
            return (R if p else OK), p
        except ProtocoloInvalido as e:
            return P, [str(e)]

    def por_base(alvo, texto, dd=None):
        return {s: problemas_de(s, texto if s == alvo else textos[s], dd) for s in siglas}

    def testa(nome, s, mutante, original, codigo, espera=(), dd=None):
        if mutante is None or mutante == original:
            g.falha(f"mutação não aplicada: {nome}")
            return
        cod, msgs = problemas_de(s, mutante, dd)
        esperas = (espera,) if isinstance(espera, str) else tuple(espera)
        faltam = [x for x in esperas if not any(x in m for m in msgs)]
        if cod != codigo:
            g.falha(f"{nome}: código {cod.name}, esperado {codigo.name} — {msgs[:1]}")
        elif faltam or not msgs:
            g.falha(f"{nome}: faltou {faltam or 'reprovação'} — {msgs[:1]}")
        else:
            achado = next((m for m in msgs if any(x in m for x in esperas)), msgs[0])
            g.ok(f"reprovou ({cod.name}): {nome} [{s}] — {achado[:84]}")

    def so_a_base(nome, s, mutante, original, codigo, esperas, dd=None):
        if mutante is None or mutante == original:
            g.falha(f"mutação não aplicada: {nome}")
            return
        pb = por_base(s, mutante, dd)
        outras = sorted(x for x, (c, _) in pb.items() if x != s and c != OK)
        cod, msgs = pb[s]
        faltam = [x for x in esperas if not any(x in m for m in msgs)]
        if cod == codigo and not faltam and not outras:
            g.ok(f"reprovou ({cod.name}): {nome} — só {s}; "
                 f"{', '.join(x for x in siglas if x != s) or 'nenhuma outra'} passam")
        else:
            g.falha(f"{nome}: {s} {cod.name} faltou {faltam}, outras reprovadas {outras}")

    def string_de(s, fid):
        return next((x for x in lidas[s]["facetas"] if x["faceta"] == fid), None)

    def muda_string(s, fid, transforma, texto=None):
        texto = textos[s] if texto is None else texto
        st = string_de(s, fid)
        if st is None:
            return None
        novo = transforma(st["texto"])
        return texto.replace(st["texto"], novo, 1) if novo != st["texto"] else None

    fid = d["facetas"][0]["id"]
    decl_a = lidas[A]["declaracao"]
    vigentes, _ = _vocabulario(fid, d, decl_a)
    st_a = string_de(A, fid)

    # (1) termo vigente retirado da string, sem outro que o cubra.
    alvo = None
    if st_a:
        excl = [e["termo"] for e in decl_a["exclusoes"] if e["faceta"] == fid]
        for termo in st_a["termos"]:
            outros = [o for o in st_a["termos"] if o != termo]
            if (any(_mesmo_termo(termo, v) for v in vigentes)
                    and not any(_mesmo_termo(termo, o) for o in outros)
                    and not any(_mesmo_termo(termo, e) for e in excl)
                    and retira_termo_citado(st_a["texto"], termo) != st_a["texto"]):
                alvo = termo
                break
    testa("termo do protocolo retirado da string da base", A,
          muda_string(A, fid, lambda b: retira_termo_citado(b, alvo)) if alvo else None,
          textos[A], R, "não consta da redução")
    testa("termo inventado acrescentado à string da base", A,
          muda_string(A, fid, lambda b: _insere_antes_do_primeiro(b, INVENTADO)), textos[A],
          R, "não deriva do protocolo")
    # Com a STR gerada do quadro, todo termo do quadro fora da STR é subsumido, e o
    # subsumido é aceito. O termo retirado da STR e mantido no quadro só existe com a STR
    # defasada: o caso o cria, acrescentando ao quadro de uma cópia um termo que nenhum
    # termo da STR subsume, sem regerar a STR.
    def com_termo_no_quadro(f_id):
        q = L_["quadro"][f_id]
        k = coluna(t_p, q["cabecalho"], d["idiomas"][0])
        mut = edita_celula(t_p, q[G.R_RELACIONADOS.interno], k,
                           lambda c: f"{c}, {RETIRADO}")
        return ctx.com_texto(mut).protocolo()

    t_p, L_ = ctx.texto, d["locais"]
    d_q = com_termo_no_quadro(fid)
    testa("termo só do quadro devolvido à string da base", A,
          muda_string(A, fid, lambda b: _insere_antes_do_primeiro(b, RETIRADO)),
          textos[A], R, "não está na string do protocolo", dd=d_q)

    # (2) a mesma família de defeito, em flexão, noutra base: reprova só ela.
    f_d = next((f["id"] for f in d["facetas"] if string_de(D, f["id"])), None)
    d_qd = com_termo_no_quadro(f_d) if f_d else None
    mut_d = (muda_string(D, f_d, lambda b: _insere_antes_do_primeiro(b, RETIRADO + "s"))
             if f_d else None)
    testa("termo só do quadro, em flexão, na string da base", D, mut_d, textos[D], R,
          "não está na string do protocolo", dd=d_qd)
    so_a_base("defeito só numa base reprova só essa base", D, mut_d, textos[D], R, (),
              dd=d_qd)

    # (2b) subsumido por termo da STR, na string da base: aceito e relatado, não reprovado.
    sub_ficha = None
    for f in d["facetas"]:
        if not string_de(A, f["id"]):
            continue
        tab = next(x for x in d["tabelas"] if x["id"] == f["id"])
        pares = esperada(tab, d["idiomas"])[1]
        if pares:
            sub_ficha = (f["id"], *next(iter(pares.items())))
            break
    if sub_ficha is None:
        g.falha("mutação não aplicável: subsumido aceito na string da base — nenhuma "
                "faceta do procedimento de busca tem termo subsumido no quadro")
    else:
        f_s, termo_s, por_s = sub_ficha
        # O termo entra na string da faceta e em todo bloco que a repete: só assim a
        # coerência entre seção 3 e seção 4 não reprova por outro motivo.
        texto_s = string_de(A, f_s)["texto"]
        miolo = texto_s[texto_s.index('"'):texto_s.rindex('"') + 1]
        mut_s = textos[A].replace(miolo, f'"{termo_s}" OR {miolo}')
        cod_s, msgs_s = problemas_de(A, mut_s)
        relato = subsumidos_na_base(base_derivada(ctx, d, A, mut_s), d)
        citado = [m for m in msgs_s if repr(termo_s) in m]
        if cod_s == OK and any(x[2] == termo_s and x[3] == por_s for x in relato):
            g.ok(f"aceitou e relatou: subsumido {termo_s!r} (por {por_s!r}) na string de {A}")
        else:
            g.falha(f"subsumido {termo_s!r} na string de {A}: código {cod_s.name}, "
                    f"reprovações {citado[:1]}, relato {relato[:1]}")

    # Par de plural irregular no relato de número único: o par cala o relato; a regra
    # afrouxada (qualquer troca de final) calaria os pares negativos.
    for x, y, esperado in PARES_IRREGULARES:
        g.testa(f"plural irregular: {x!r} × {y!r} {'é' if esperado else 'não é'} par de "
                f"número", _par_irregular(x, y) == esperado,
                f"devolveu {_par_irregular(x, y)}")

    # (3) seção de critérios do procedimento de busca: ID inexistente numa base reprova só ela.
    t_f = textos[F]
    trecho = secao(t_f, G.SF_CRITERIOS)
    inicio = t_f.index(trecho)
    achado = G.I_CE.padrao.search(trecho)
    mut_f, esperas_f = None, ()
    if achado:
        retirado = achado.group(0)
        novo = f"{G.I_CE.prefixo}{max(int(c['id'][len(G.I_CE.prefixo):]) for c in d['criterios']) + 1}"
        mut_f = t_f[:inicio + achado.start()] + novo + t_f[inicio + achado.end():]
        esperas_f = (novo, f"não cita {retirado}")
    so_a_base("ID de critério inexistente na seção de critérios do procedimento de busca", F,
              mut_f, t_f, R, esperas_f)

    # (4) facetas da expressão executada e camadas declaradas.
    t_a = textos[A]
    mut = None
    i = t_a.find(f"### {executada}")
    j = t_a.find(G.MARCA_FACETAS, i) if i >= 0 else -1
    if j >= 0:
        fim = t_a.find("\n", j)
        linha = t_a[j:fim]
        corte = linha.rfind(" AND ")
        if corte > 0:
            mut = t_a[:j] + linha[:corte] + t_a[fim:]
    testa("expressão com faceta trocada", A, mut, t_a, R, "do protocolo")
    outro_valor = next(v for v in G.D_CAMADAS.valores if v != decl_a["camadas"])
    mut = _troca_rotulo(t_a, G.RF_CAMADAS, outro_valor)
    testa("declaração de cobertura restringindo as camadas", A, mut, t_a, R)

    # (4b) plural declarado: `pela lematização` sem lastro numa só base reprova só ela; a
    # linha retirada é procedimento de busca ilegível.
    texto_lem = next(k for k, v in G.D_PLURAL.valores.items() if v == G.PLURAL_LEMATIZACAO)
    sem_lastro = next((s for s in siglas
                       if lidas[s]["declaracao"]["plural"] != G.PLURAL_LEMATIZACAO
                       and not (lidas[s]["lematizacao"][1] and lidas[s]["lematizacao"][2])),
                      None)
    if sem_lastro is None:
        g.falha("mutação não aplicável: plural pela lematização sem lastro — todo procedimento "
                "de busca já declara a lematização ou a tem medida")
    else:
        t_w = textos[sem_lastro]
        so_a_base("plural pela lematização sem a lematização medida", sem_lastro,
                  _troca_rotulo(t_w, G.RF_PLURAL, texto_lem), t_w, R,
                  (f"declara plural {texto_lem!r}", G.RF_LEMATIZACAO.texto))
    linha_plural = next((linha for _, linha in linhas_de_tabela_do_trecho(t_a, G.SF_DECLARACAO)
                         if normaliza(linha.strip("| ").split("|")[0])
                         == normaliza(G.RF_PLURAL.texto)), None)
    testa("declaração de cobertura sem a linha plural", A,
          t_a.replace(linha_plural + "\n", "", 1) if linha_plural else None, t_a, P,
          ("linha de plural", G.RF_PLURAL.rotulo))

    # (4c) teto de caracteres declarado: abaixo da maior consulta de uma base, só ela
    # reprova; igual à maior, passa; a linha retirada é procedimento de busca ilegível.
    maior = maior_consulta(lidas[A])
    if maior is None:
        g.falha(f"mutação não aplicável: teto de caracteres — {A} sem consulta executável")
    else:
        n, ident_maior, _ = maior
        so_a_base("teto de caracteres abaixo da maior consulta", A,
                  _troca_rotulo(t_a, G.RF_TETO, str(n - 1)), t_a, R,
                  (f"{n} caracteres, acima do teto de caracteres declarado ({n - 1})",
                   ident_maior))
        cod, msgs = problemas_de(A, _troca_rotulo(t_a, G.RF_TETO, f"{n:,}".replace(",", ".")))
        g.testa(f"teto de caracteres igual à maior consulta, com separador de milhar [{A}]",
                cod == OK, f"código {cod.name} — {msgs[:1]}")
    linha_teto = next((linha for _, linha in linhas_de_tabela_do_trecho(t_a, G.SF_DECLARACAO)
                       if normaliza(linha.strip("| ").split("|")[0])
                       == normaliza(G.RF_TETO.texto)), None)
    testa("declaração de cobertura sem a linha de teto de caracteres", A,
          t_a.replace(linha_teto + "\n", "", 1) if linha_teto else None, t_a, P,
          ("linha de teto de caracteres", G.RF_TETO.rotulo))

    # (4d) a subseção de estratégia de proximidade é prosa: bloco cercado nela não muda o
    # derivado da base nem a conferência.
    i_exec = t_a.find("\n### Como executar")
    if i_exec < 0:
        g.falha(f"mutação não aplicável: estratégia de proximidade — {A} sem 'Como executar'")
    else:
        com_prox = (t_a[:i_exec] + "\n### Estratégia de proximidade\n\nDiscussão da "
                    "distância entre as âncoras.\n\n```\n\"termo a\" NEAR/3 \"termo b\"\n"
                    "```\n" + t_a[i_exec:])
        try:
            igual, erro = base_derivada(ctx, d, A, com_prox) == lidas[A], ""
        except ProtocoloInvalido as e:
            igual, erro = False, f" — {e}"
        cod = problemas_de(A, com_prox)[0]
        g.testa(f"estratégia de proximidade com bloco cercado não muda o derivado [{A}]",
                igual and cod == OK, f"derivado {'igual' if igual else 'DIFERENTE'}, "
                                     f"código {cod.name}{erro}")

    # (5) forma de execução declarada no procedimento de busca: sem padrão, e o defeito fica
    # na base.
    t_e = textos[E]
    m_exec = G.MF_EXECUCAO.padrao.search(t_e)
    linha_exec = m_exec.group(0) + "\n" if m_exec else None
    testa("procedimento de busca sem a linha de execução", E,
          t_e.replace(linha_exec, "", 1) if linha_exec else None, t_e, P, "falta a linha")
    testa("procedimento de busca com a linha de execução repetida", E,
          t_e.replace(linha_exec, linha_exec * 2, 1) if linha_exec else None, t_e, P,
          "repetida")
    testa("procedimento de busca com forma de execução fora do domínio", E,
          t_e.replace(m_exec.group(0), m_exec.group(0).replace(m_exec.group(1), "dividida"),
                      1) if m_exec else None, t_e, P, "'dividida'")
    so_a_base("procedimento de busca sem execução reprova só a sua base, nomeando o "
              "procedimento de busca", E,
              t_e.replace(linha_exec, "", 1) if linha_exec else None, t_e, P,
              (lidas[E]["base"]["ficha"],))

    # (6) forma radical, no procedimento de busca que a declara. O controle é o procedimento
    # de busca corrente com toda linha falsamente declarada como radical reetiquetada como
    # redução: tem de passar, ou os defeitos injetados sobre ele não provam nada.
    if RAD is None:
        for nome in ("controle da forma radical aprovado",
                     "redução declarada como radical sem termo da string que a alcance",
                     "termo inventado que partilha uma palavra com o protocolo",
                     "motivo radical sem derivação radical declarada"):
            g.falha(f"mutação não aplicável: {nome} — nenhum procedimento de busca declara a "
                    f"forma radical")
        controle = None
    else:
        controle = textos[RAD]
        for e, _ in _radical_sem_alcance(lidas[RAD]):
            controle = re.sub(r"^(\|\s*" + re.escape(e["faceta"]) + r"\s*\|\s*"
                              + re.escape(e["termo"]) + r"\s*\|)[^\n]*$",
                              r"\1 redução desta base (controle do autoteste) |",
                              controle, count=1, flags=re.M)
        cod, msgs = problemas_de(RAD, controle)
        g.testa(f"controle da forma radical aprovado [{RAD}]", cod == OK, f"{msgs[:1]}")
        lida_c = base_derivada(ctx, d, RAD, controle)
        st_r = next((x for x in lida_c["facetas"] if x["faceta"] == fid), None)
        sem_alcance = None
        if st_r:
            for termo in st_r["termos"]:
                outros = [o for o in st_r["termos"] if o != termo]
                if (len(termo.split()) > 1
                        and not any(_radical_alcanca(termo, o) or _mesmo_termo(termo, o)
                                    for o in outros)
                        and retira_termo_citado(st_r["texto"], termo) != st_r["texto"]):
                    sem_alcance = termo
                    break
        mut = None
        if sem_alcance:
            mut = controle.replace(st_r["texto"],
                                   retira_termo_citado(st_r["texto"], sem_alcance), 1)
            mut = _acrescenta_reducao(mut, fid, sem_alcance, MOTIVO_RADICAL)
        testa("redução declarada como radical sem termo da string que a alcance", RAD, mut,
              controle, R, "consta da redução como alcançado")
        vig_r, _ = _vocabulario(fid, d, lida_c["declaracao"])
        palavra = normaliza(vig_r[0]).split()[0] if vig_r else "termo"
        inventado = f"{palavra} zzinventado"
        mut = (controle.replace(st_r["texto"], _insere_antes_do_primeiro(st_r["texto"],
                                                                         inventado), 1)
               if st_r else None)
        testa("termo inventado que partilha uma palavra com o protocolo", RAD, mut, controle,
              R, f"{inventado!r} está na string")
        modos = [m for m in lida_c["declaracao"]["derivacoes"] if m != G.DERIVACAO_RADICAL]
        mut = _acrescenta_reducao(controle, fid, vig_r[0] if vig_r else palavra,
                                  MOTIVO_RADICAL)
        mut = _troca_rotulo(mut, G.RF_DERIVACOES, " e ".join(modos))
        testa("motivo radical sem derivação radical declarada", RAD, mut, controle, R,
              "não declara a derivação radical")

    # (7) bloco literal: referência a conjunto e termo defasado da seção 3.
    expr_a = lidas[A]["expressoes"]
    por_estatuto = {}
    for ident, ex in expr_a.items():
        por_estatuto.setdefault(ex["estatuto"], []).append(ident)
    termos_str = {normaliza(x) for s in lidas[A]["facetas"] for x in s["termos"]}

    def bloco_unico(ident):
        """(bloco, termo) com um termo entre aspas que aparece uma só vez nos blocos da
        expressão e uma só vez na seção de strings."""
        blocos = [b["texto"] for b in expr_a.get(ident, {}).get("blocos", [])]
        juntos = "\n".join(blocos)
        cordas = "\n".join(s["texto"] for s in lidas[A]["facetas"])
        for b in blocos:
            for termo in termos_bloco(b):
                if (normaliza(termo) in termos_str and juntos.count(f'"{termo}"') == 1
                        and cordas.count(f'"{termo}"') == 1):
                    return b, termo
        return None, None

    def no_bloco(ident, transforma, texto=None):
        texto = t_a if texto is None else texto
        blocos = expr_a.get(ident, {}).get("blocos", [])
        if not blocos:
            return None
        return texto.replace(blocos[0]["texto"], transforma(blocos[0]["texto"]), 1)

    defasado = ("do bloco não consta das facetas declaradas",
                "das facetas declaradas não está no bloco")

    def caso_bloco(nome, s, mutante, original, esperas):
        so_a_base(nome, s, mutante, original, R, esperas)

    caso_bloco("conjunto #n devolvido ao bloco executado", A,
               no_bloco(executada, lambda b: "#1 AND " + b), t_a, ("referência a conjunto",))
    bloco, termo = bloco_unico(executada)
    caso_bloco("termo do bloco executado defasado da seção de strings", A,
               t_a.replace(bloco, bloco.replace(f'"{termo}"', f'"{termo}zz"', 1), 1)
               if bloco else None, t_a, defasado)
    caso_bloco("termo alterado só na seção de strings", A,
               (lambda st: t_a.replace(st["texto"], st["texto"].replace(
                   f'"{termo}"', f'"{termo}zz"', 1), 1))(
                   next(s for s in lidas[A]["facetas"] if f'"{termo}"' in s["texto"]))
               if termo else None, t_a, defasado)
    if RAD is not None:
        exp_r = base_derivada(ctx, d, RAD, controle)["expressoes"].get(executada, {})
        blocos_r = exp_r.get("blocos", [])
        mut = (controle.replace(blocos_r[0]["texto"],
                                blocos_r[0]["texto"] + ' OR "termo-defasado-zz"', 1)
               if blocos_r else None)
        so_a_base(f"termo acrescentado ao bloco executado ({lidas[RAD]['execucao']['modo']})",
                  RAD, mut, controle, R, (defasado[0],))
    else:
        g.falha("mutação não aplicável: bloco executado do procedimento de busca com forma radical")
    fidel = (por_estatuto.get("fidelidade") or [None])[0]
    caso_bloco("conjunto #n devolvido ao bloco de fidelidade", A,
               no_bloco(fidel, lambda b: "#1 AND " + b) if fidel else None, t_a,
               ("referência a conjunto",))
    sonda = (por_estatuto.get("sonda") or [None])[0]
    bloco, termo = bloco_unico(sonda) if sonda else (None, None)
    caso_bloco("termo do bloco de sonda defasado da seção de strings", A,
               t_a.replace(bloco, bloco.replace(f'"{termo}"', f'"{termo}zz"', 1), 1)
               if bloco else None, t_a, defasado)
    derivada = next((k for k in por_estatuto.get("derivada", [])
                     if not expr_a[k]["blocos"] and not expr_a[k].get("forma_longa")), None)
    caso_bloco("bloco devolvido à expressão derivada padrão", A,
               _bloco_novo(t_a, derivada, '"bloco do autoteste"') if derivada else None, t_a,
               ("expressão derivada não se executa e não leva bloco",))

    # (8) a forma longa é representação não executada: o bloco nela não é recusado pela
    # regra que fecha a derivada padrão.
    if derivada:
        longa = base_derivada(ctx, d, A, t_a)
        longa["expressoes"][derivada]["blocos"] = [{"rotulo": "", "texto": '"x"'}]
        longa["expressoes"][derivada]["forma_longa"] = True
        recusada = [p for p in cobertura_base(longa, d) if "expressão derivada" in p]
        g.testa("forma longa com bloco não é recusada pela regra da derivada", not recusada,
                f"{recusada[:1]}")
    else:
        g.falha("mutação não aplicável: forma longa — nenhuma expressão derivada sem bloco")


def _troca_rotulo(texto, rotulo, valor):
    """Troca o valor da linha de rótulo `rotulo` na declaração de cobertura."""
    for _, linha in linhas_de_tabela_do_trecho(texto, G.SF_DECLARACAO):
        cels = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(cels) >= 2 and normaliza(cels[0]).startswith(normaliza(rotulo.texto)):
            nova = f"| {cels[0]} | {valor} |" + "".join(f" {c} |" for c in cels[2:])
            return texto.replace(linha, nova, 1)
    return texto


def _acrescenta_reducao(texto, fid, termo, motivo):
    """Acrescenta `| fid | termo | motivo |` ao fim da tabela da declaração de cobertura."""
    ultima = linhas_de_tabela_do_trecho(texto, G.SF_DECLARACAO)[-1][1]
    return texto.replace(ultima, ultima + f"\n| {fid} | {termo} | {motivo} |", 1)


def _bloco_novo(texto, ident, bloco):
    """Acrescenta um bloco cercado à expressão `ident`, logo após a linha de facetas."""
    i = texto.find(f"### {ident}")
    j = texto.find(G.MARCA_FACETAS, i) if i >= 0 else -1
    if j < 0:
        return None
    fim = texto.find("\n", j)
    return texto[:fim + 1] + "\n```\n" + bloco + "\n```\n" + texto[fim + 1:]


PARES_IRREGULARES = (
    ("thesaurus", "thesauri", True),
    ("analysis", "analyses", True),
    ("curriculum", "curricula", True),
    ("thesaurus", "thesaurus", False),
    ("thesaurus", "taxonomy", False),
    ("domain thesaurus", "thesauri", False),
    ("bus", "bi", False),
)
