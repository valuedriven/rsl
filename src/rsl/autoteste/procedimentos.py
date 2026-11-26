"""Autoteste da fonte, da geração, das sondagens e da flexão (alternativa B).

Cada defeito é injetado numa cópia em memória da fonte de uma base (`fontes.py`), do
arquivo de exceções ou num diretório temporário (registro de sondagem, gravação), nunca na
pasta corrente. A base de cada caso é escolhida pela estrutura da fonte.
"""

import contextlib
import copy
import io
import json
import pathlib
import re
import tempfile

from .. import gramatica as G
from ..config import Configuracao
from ..dados import problemas_registro, problemas_sondagens_registradas
from ..erros import ErroRSL
from ..flexao import Indecidivel, le_excecoes, orfas, plural_por_regra
from ..fonte import le_fonte
from ..procedimentos import gera, gera_base, inicia, problemas_igualdade, registro_de_execucao
from ..saida import Saida
from ..sondagens import registra
from .fontes import base_com, com_fonte, fonte_de, registro_com_sondagem

P, U, DADOS = Saida.PROTOCOLO_ILEGIVEL, Saida.USO, Saida.DADOS


def _codigo(funcao):
    """(código, texto) de uma chamada, com a saída padrão recolhida."""
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            r = funcao()
    except ErroRSL as e:
        return Saida(e.codigo), str(e)
    cod = r if isinstance(r, Saida) else Saida.OK
    return cod, out.getvalue()


def _com_config(ctx, **valores):
    cfg = ctx.config
    for chave, valor in valores.items():
        cfg = Configuracao(cfg.com(chave, valor), cfg.arquivo)
    return ctx.com_config(cfg)


# ------------------------------------------------------------------------ fonte
def fonte(ctx, g):
    d = ctx.protocolo()
    alvo = base_com(ctx, d, lambda x: bool(x.get("sondagens"))
                    and any(s["situacao"] == G.SITUACAO_NAO_VERIFICADO and s.get("sondagem")
                            for s in x["sintaxe"]))
    if alvo is None:
        g.falha("mutação não aplicada: nenhuma base com sondagem declarada")
        return
    dado0, frag0, arqs0 = fonte_de(ctx, d, alvo)

    def caso(nome, mutar=None, frags=None, trechos=(), codigo=P):
        dado = copy.deepcopy(dado0)
        if mutar:
            mutar(dado)
        frag = frags(dict(frag0)) if frags else dict(frag0)
        if dado == dado0 and frag == frag0:
            g.falha(f"mutação não aplicada: {nome}")
            return
        cx = com_fonte(ctx, alvo, dado, frag)
        cod, texto = _codigo(lambda: le_fonte(cx, d, alvo))
        trechos = (trechos,) if isinstance(trechos, str) else trechos
        faltam = [x for x in trechos if x not in texto]
        g.testa(f"reprovou ({codigo.name}): {nome} [{alvo}]", cod == codigo and not faltam,
                f"{cod.name}, faltou {faltam} — {texto[-160:]}")

    # O corte por camada foi retirado: a fonte que ainda o declara reprova como campo
    # desconhecido, pela regra geral do esquema, e não é lida em silêncio.
    caso("campo `camadas` na [cobertura], retirado do esquema",
         lambda x: x["cobertura"].__setitem__("camadas", "todas"),
         trechos=("campo desconhecido", "'camadas'"))

    nao_verif = next(s for s in dado0["sintaxe"]
                     if s["situacao"] == G.SITUACAO_NAO_VERIFICADO and s.get("sondagem"))
    i_nv = dado0["sintaxe"].index(nao_verif)
    sd0 = dado0["sondagens"][0]
    k_inc = next(i for i, x in enumerate(sd0["leituras"])
                 if x["estado"] == G.SITUACAO_NAO_VERIFICADO)
    outra = next(b["id"] for b in d["bases"] if b["sigla"] != alvo)
    categoria = dado0["sintaxe"][0]["categoria"]
    criterio_sem = next((k for k, c in enumerate(dado0["criterios"])
                         if c["destino"] not in G.DESTINOS_COM_CLAUSULA), 0)

    caso("situação fora do domínio",
         lambda x: x["sintaxe"][0].update(situacao="medido"), trechos="fora do domínio")
    caso("campo desconhecido", lambda x: x["cobertura"].update(plurais="explícito"),
         trechos="campo desconhecido")
    caso("categoria esquecida",
         lambda x: x.update(sintaxe=[s for s in x["sintaxe"] if s["categoria"] != categoria]),
         trechos=categoria)
    caso("medição sem citação",
         lambda x: (x["sintaxe"][i_nv].update(situacao=G.SITUACAO_MEDICAO),
                    x["sintaxe"][i_nv].pop("sondagem")), trechos="sem `citacao`")
    caso("citação de outra base",
         lambda x: x["sintaxe"][0].update(situacao=G.SITUACAO_MEDICAO,
                                          citacao=f"{outra}/autoteste"),
         trechos="de outra base")
    caso("filtro na consulta sem cláusula",
         lambda x: (x["criterios"][criterio_sem].update(destino="consulta"),
                    x["criterios"][criterio_sem].pop("clausula", None)),
         trechos="`clausula`")
    # A cláusula vem de um critério que já a declara: a da base-alvo ou, se ela não tem
    # nenhum, a da primeira base da tabela que tenha. Sem nenhuma, o caso não executa.
    def tem_clausula(x):
        return any(c["destino"] in G.DESTINOS_COM_CLAUSULA for c in x.get("criterios", []))

    com_clausula = alvo if tem_clausula(dado0) else base_com(ctx, d, tem_clausula)
    if com_clausula is None:
        g.nao_executa(1, "cláusula com conector na borda: nenhuma base com critério de "
                         "destino " + " ou ".join(G.DESTINOS_COM_CLAUSULA))
    else:
        dado_c, frag_c, arqs_c = fonte_de(ctx, d, com_clausula)
        k = next(i for i, c in enumerate(dado_c["criterios"])
                 if c["destino"] in G.DESTINOS_COM_CLAUSULA)
        dado_c["criterios"][k]["clausula"] = "AND " + dado_c["criterios"][k]["clausula"]
        cx = com_fonte(ctx, com_clausula, dado_c, frag_c, arqs_c)
        cod, texto = _codigo(lambda: le_fonte(cx, d, com_clausula))
        g.testa(f"reprovou ({P.name}): cláusula com conector na borda [{com_clausula}]",
                cod == P and "conector na borda" in texto, f"{cod.name} — {texto[-160:]}")
    caso("fragmento de nome errado", frags=lambda f: dict(f, **{"variante.md": "x\n"}),
         trechos="variante.md")
    caso("falta como_executar.md",
         frags=lambda f: {k: v for k, v in f.items() if k != G.FRAGMENTO_OBRIGATORIO},
         trechos=G.FRAGMENTO_OBRIGATORIO)
    caso("título que quebra o esqueleto",
         frags=lambda f: dict(f, **{G.FRAGMENTO_OBRIGATORIO: "## Passos\n"}),
         trechos=f"{G.FRAGMENTO_OBRIGATORIO}:1")
    caso("`####` fora de variantes.md",
         frags=lambda f: dict(f, **{G.FRAGMENTO_OBRIGATORIO: "#### Passo\n"}),
         trechos=f"{G.FRAGMENTO_OBRIGATORIO}:1")
    caso("linha `- Execução:` em fragmento",
         frags=lambda f: dict(f, **{G.FRAGMENTO_OBRIGATORIO: f"{G.LINHA_EXECUCAO} única\n"}),
         trechos=G.LINHA_EXECUCAO)
    caso("marca PENDENTE lista todas as ocorrências",
         lambda x: (x["cobertura"].update(teto=G.PENDENTE),
                    x["composicao"].update(aspas=G.PENDENTE)),
         frags=lambda f: dict(f, **{G.FRAGMENTO_OBRIGATORIO: G.PENDENTE + "\n"}),
         trechos="3 marca(s)")
    caso("não verificado sem sondagem nem motivo",
         lambda x: x["sintaxe"][i_nv].pop("sondagem"),
         trechos="sem `sondagem` nem `sem_sondagem`")
    caso("sondagem que lista elemento inexistente",
         lambda x: x["sondagens"][0]["elementos"].append("Elemento inventado pelo autoteste"),
         trechos="Elemento inventado pelo autoteste")
    caso("sondagem sem leitura inconclusiva",
         lambda x: x["sondagens"][0]["leituras"][k_inc].update(
             estado="inexistente"), trechos="inconclusiva")
    caso("sondagem sem consulta", lambda x: x["sondagens"][0].update(consultas=[]),
         trechos="exige ao menos 1")

    def ciclo(x):
        a = x["sondagens"][0]
        b = copy.deepcopy(a)
        b["id"] = f"{G.I_SD.prefixo}{len(x['sondagens']) + 1}"
        b["depende_de"] = [a["id"]]
        b["elementos"] = []
        a["depende_de"] = [b["id"]]
        x["sondagens"].append(b)
    caso("ciclo em depende_de", ciclo, trechos="ciclo")

    # Início de base nova: recusado fora do protocolo e com pasta existente.
    cod, texto = _codigo(lambda: inicia(ctx, "base-inexistente-autoteste"))
    g.testa("`procedimentos iniciar` recusa base fora do protocolo", cod == U, texto[-120:])
    cod, texto = _codigo(lambda: inicia(ctx, alvo))
    g.testa(f"`procedimentos iniciar` recusa fonte já existente [{alvo}]", cod == U,
            texto[-120:])
    with tempfile.TemporaryDirectory() as tmp:
        cx = _com_config(ctx, **{"documentos.procedimento_fonte": f"{tmp}/{{sigla}}"})
        cod, texto = _codigo(lambda: inicia(cx, alvo))
        criado = pathlib.Path(tmp) / alvo / "procedimento.toml"
        cod2, texto2 = _codigo(lambda: le_fonte(cx, d, alvo))
        g.testa(f"fonte recém-iniciada existe e reprova pela marca PENDENTE [{alvo}]",
                cod == Saida.OK and criado.is_file() and cod2 == P
                and G.PENDENTE in texto2, f"{cod.name} {cod2.name} {texto2[-120:]}")


# ------------------------------------------------------------------------ geração
def geracao(ctx, g):
    d = ctx.protocolo()
    executada = d["executada"]
    part = base_com(ctx, d, lambda x: x["execucao"]["forma"] == "particionada"
                    and isinstance(x["cobertura"]["teto"], int))
    if part is None:
        g.falha("mutação não aplicada: nenhuma base particionada com teto")
    else:
        dado0, frag, arqs = fonte_de(ctx, d, part)

        def com(mutar):
            x = copy.deepcopy(dado0)
            mutar(x)
            return com_fonte(ctx, part, x, frag, arqs)

        # A partição se torna necessária por construção: o teto passa a ficar um caractere
        # abaixo da maior consulta gerada. Sem isso, o caso dependeria do comprimento
        # corrente das STRs, que pode caber no teto declarado.
        _, comp0, _ = gera_base(ctx, d, part)
        justo = max(len(c["texto"]) for e in comp0.expressoes.values()
                    for c in e["consultas"]) - 1

        def unica(x):
            x["execucao"].update(forma="unica")
            x["cobertura"]["teto"] = justo
        cod, texto = _codigo(lambda: gera_base(com(unica), d, part))
        g.testa(f"forma única com partição necessária reprova [{part}]",
                cod == Saida.REPROVADO and 'forma = "unica"' in texto, texto[-140:])
        cod, texto = _codigo(lambda: gera_base(com(
            lambda x: x["cobertura"].update(teto=50)), d, part))
        g.testa(f"âncoras acima do teto reprovam [{part}]",
                cod == Saida.REPROVADO and "âncoras" in texto, texto[-140:])
        _, comp, _ = gera_base(ctx, d, part)
        cons = comp.expressoes[executada]["consultas"]
        teto = dado0["cobertura"]["teto"]
        maior = max(len(c["texto"]) for e in comp.expressoes.values() for c in e["consultas"])
        g.testa(f"partição respeita o teto e conserva os termos [{part}]",
                maior <= teto and len(cons) > 1, f"maior {maior}, teto {teto}")

    # Linha condicionada ao estatuto e derivada sem bloco.
    alvo = d["bases"][0]["sigla"]
    dado, frag, arqs = fonte_de(ctx, d, alvo)
    fidel = [e for e in dado["execucao"]["expressoes"]
             if e["id"] not in (executada, d["sonda"])]
    for e in fidel:
        e["estatuto"] = "derivada"
    cx = com_fonte(ctx, alvo, dado, frag, arqs)
    _, comp, texto = gera_base(cx, d, alvo)
    g.testa(f"sem expressão de fidelidade, sem a linha de fidelidade [{alvo}]",
            "**Fidelidade:**" not in texto and "**Sensibilidade:**" in texto,
            "linha de fidelidade presente")
    g.testa(f"expressão derivada sem bloco [{alvo}]",
            all(not comp.expressoes[e["id"]]["consultas"] for e in fidel))
    sem_prox = "estrategia_de_proximidade.md" not in frag
    g.testa(f"subseção sem fonte não aparece [{alvo}]",
            not sem_prox or "### Estratégia de proximidade" not in texto)

    # Gravação: ensaio, gravação, igualdade, edição à mão, gravação interrompida.
    with tempfile.TemporaryDirectory() as tmp:
        cx = _com_config(ctx, **{"documentos.procedimento":
                                 f"{tmp}/procedimentos_busca_{{sigla}}.md"})
        dx = cx.protocolo()
        arq = pathlib.Path(tmp) / f"procedimentos_busca_{alvo}.md"
        cod, texto = _codigo(lambda: gera(cx, [alvo]))
        g.testa(f"ensaio não grava [{alvo}]", not arq.exists() and "Ensaio" in texto,
                texto[-120:])
        _codigo(lambda: gera(cx, [alvo], gravar=True))
        _, _, esperado = gera_base(cx, dx, alvo, registro=registro_de_execucao(cx))
        g.testa(f"gravado é o gerado [{alvo}]",
                arq.is_file() and arq.read_text(encoding="utf-8") == esperado)
        g.testa(f"procedimento em dia não reprova na igualdade [{alvo}]",
                not [x for s, x in problemas_igualdade(cx, dx) if s == alvo])
        bloco = re.search(r"```\n(.+?)\n```", esperado, re.S)
        editado = esperado.replace(bloco.group(1), bloco.group(1) + ' OR "autoteste"', 1)
        arq.write_text(editado, encoding="utf-8")
        pi = [x for s, x in problemas_igualdade(cx, dx) if s == alvo]
        g.testa(f"termo acrescentado à mão reprova na igualdade [{alvo}]",
                bool(pi) and f"procedimentos gerar {alvo} --gravar" in pi[0], f"{pi[:1]}")
        prosa = esperado.replace(G.ESQUELETO["s5"], G.ESQUELETO["s5"] + " (editada)", 1)
        arq.write_text(prosa, encoding="utf-8")
        g.testa(f"prosa editada no procedimento reprova [{alvo}]",
                bool([x for s, x in problemas_igualdade(cx, dx) if s == alvo]))
        from .. import geracao as GE
        original = GE.os.replace

        def falha(*a):
            raise OSError("falha simulada pelo autoteste")
        GE.os.replace = falha
        try:
            with contextlib.suppress(OSError):
                _codigo(lambda: gera(cx, [alvo], gravar=True))
        finally:
            GE.os.replace = original
        g.testa(f"gravação interrompida deixa o arquivo intacto [{alvo}]",
                arq.read_text(encoding="utf-8") == prosa)


# ------------------------------------------------------------------------ sondagens
def sondagens(ctx, g):
    d = ctx.protocolo()
    alvo = base_com(ctx, d, lambda x: bool(x.get("sondagens")))
    if alvo is None:
        g.falha("mutação não aplicada: nenhuma base com sondagem")
        return
    dado, _, _ = fonte_de(ctx, d, alvo)
    sd = dado["sondagens"][0]
    n = len(sd["consultas"])
    with tempfile.TemporaryDirectory() as tmp:
        reg = pathlib.Path(tmp) / "registro.json"
        ev = pathlib.Path(tmp) / "evidencia.png"
        ev.write_bytes(b"autoteste")
        quando = "2026-01-01T10:00"

        def tenta(nome, codigo, **k):
            arg = dict(retornos=[1] * n, leitura=1, data_hora=quando, evidencias=[str(ev)])
            arg.update(k)
            cod, texto = _codigo(lambda: registra(
                ctx, alvo, sd["id"], arg["retornos"], arg["leitura"], arg["data_hora"],
                arg["evidencias"], caminho=reg))
            g.testa(f"registro recusado ({codigo.name}): {nome}", cod == codigo
                    and not reg.exists(), f"{cod.name} {texto[-120:]}")
            reg.unlink(missing_ok=True)

        tenta("sem evidência", U, evidencias=[])
        tenta("sem data e hora", U, data_hora=None)
        tenta("retornos em número diferente das consultas", U, retornos=[1] * (n + 1))
        tenta("leitura inexistente", U, leitura=len(sd["leituras"]) + 1)
        tenta("evidência que não existe", DADOS,
              evidencias=[str(pathlib.Path(tmp) / "nao-existe.png")])
        cod, texto = _codigo(lambda: registra(ctx, alvo, f"{G.I_SD.prefixo}999", [1], 1,
                                              quando, [str(ev)], caminho=reg))
        g.testa("registro recusado: sondagem inexistente na fonte",
                cod == P and not reg.exists(), f"{cod.name} {texto[-120:]}")
        for _ in range(2):
            _codigo(lambda: registra(ctx, alvo, sd["id"], [1] * n, 1, quando, [str(ev)],
                                     caminho=reg))
        ids = []
        if reg.exists():
            r = json.loads(reg.read_text(encoding="utf-8"))
            bd = next(b["id"] for b in d["bases"] if b["sigla"] == alvo)
            ids = [x["id"] for x in r["bases"][bd]["sondagens"]]
        raiz = f"{sd['id'].lower()}-2026-01-01"
        g.testa("registro grava o resultado e dá sufixo ao id repetido",
                ids == [raiz, f"{raiz}-2"], f"{ids}")
        # Registro criado pelo comando: aceito pela conferência do registro, com todas as
        # bases do protocolo (contraprova: o mesmo registro sem uma das outras bases reprova).
        bds = [b["id"] for b in d["bases"]]
        if reg.exists() and len(bds) > 1:
            r = json.loads(reg.read_text(encoding="utf-8"))
            outra = next(x for x in bds if x != bd)
            sem = copy.deepcopy(r)
            sem["bases"].pop(outra, None)
            g.testa("registro criado por `sondagens registrar` traz todas as bases e é aceito",
                    not problemas_registro(ctx, r, bds)
                    and any("sem as bases" in x for x in problemas_registro(ctx, sem, bds)),
                    f"{problemas_registro(ctx, r, bds)[:1]}")

    # Conferência do resultado registrado (`dados conferir`), sobre um registro válido.
    sigla, reg0 = registro_com_sondagem(ctx, d)
    if reg0 is None:
        g.falha("mutação não aplicada: nenhum registro de sondagem montável")
        return
    bd0 = next(b["id"] for b in d["bases"] if b["sigla"] == sigla)
    antes, rel0 = problemas_sondagens_registradas(ctx, d, reg0)
    g.testa(f"resultado registrado válido aprova, sem relato [{sigla}]",
            not antes and not rel0, f"{antes[:1]} {rel0[:1]}")

    def confere(nome, mutar, trecho, relato=False):
        mut = copy.deepcopy(reg0)
        mutar(mut["bases"][bd0]["sondagens"])
        probs, rels = problemas_sondagens_registradas(ctx, d, mut)
        alvo_lista, outra = (rels, probs) if relato else (probs, rels)
        g.testa(f"{'relatou' if relato else 'reprovou'}: {nome} [{sigla}]",
                any(trecho in x for x in alvo_lista) and (not relato or not probs),
                f"problemas {probs[:1]}, relatos {rels[:1]}")

    def inexistente(lista):
        lista[0]["sondagem"] = f"{G.I_SD.prefixo}999"
    confere("resultado de sondagem inexistente na fonte", inexistente, "não existe na fonte")
    confere("id de resultado repetido na base",
            lambda lista: lista.append(copy.deepcopy(lista[0])), "repetida")

    def leitura_fora(lista):
        lista[0]["leitura"]["numero"] = 99
    confere("leitura que não é nenhuma das declaradas", leitura_fora, "leitura 99")

    dado_r, _, _ = fonte_de(ctx, d, sigla)
    id_r = reg0["bases"][bd0]["sondagens"][0]["sondagem"]
    sd_r = next(x for x in dado_r["sondagens"] if x["id"] == id_r)
    k_med = next((i for i, x in enumerate(sd_r["leituras"], 1)
                  if x["estado"] == G.SITUACAO_MEDICAO), None)
    if k_med is None:
        g.falha(f"mutação não aplicada: {sd_r['id']} sem leitura de medição")
    else:
        def medicao(lista):
            lista[0]["leitura"].update(numero=k_med, estado=G.SITUACAO_MEDICAO)
        confere("resultado ainda não levado à fonte", medicao, "ainda não levado à fonte",
                relato=True)

    # Ordem do roteiro por dependência.
    _, _, texto = gera_base(ctx, d, alvo)
    ordem = re.findall(rf"^#### ({G.I_SD.prefixo}\d+)", texto, re.M)
    pos = {s: k for k, s in enumerate(ordem)}
    viola = [(s["id"], x) for s in dado["sondagens"] for x in s.get("depende_de", [])
             if pos.get(x, -1) > pos.get(s["id"], -1)]
    g.testa(f"roteiro em ordem de dependência [{alvo}]", ordem and not viola, f"{viola}")


# ------------------------------------------------------------------------ flexão
def flexao(ctx, g):
    d = ctx.protocolo()
    regulares = [("situational factor", "en", "situational factors"),
                 ("prática pedagógica", "pt", "práticas pedagógicas"),
                 ("método de ensino", "pt", "métodos de ensino"),
                 ("situación de aprendizaje", "es", "situaciones de aprendizaje"),
                 # o adjetivo que segue o núcleo concorda com ele e não é recusado
                 ("modelo conceitual", "pt", "modelos conceituais")]
    for termo, idioma, esperado in regulares:
        try:
            obtido = plural_por_regra(termo, idioma)
        except Indecidivel as e:
            obtido = f"indecidível: {e.motivo}"
        g.testa(f"plural por regra: {termo!r} ({idioma}) → {esperado!r}",
                obtido == esperado, obtido)
    for termo, idioma in [("situação de uso", "pt"), ("educational", "en"),
                          ("educacional", "pt"), ("educativo", "es"),
                          ("teaching and learning", "en")]:
        try:
            plural_por_regra(termo, idioma)
            g.falha(f"indecidível aceito pela regra: {termo!r} ({idioma})")
        except Indecidivel as e:
            g.ok(f"indecidível recusado: {termo!r} ({idioma}) — {e.motivo}")

    # Termo indecidível sem exceção reprova a geração.
    alvo = d["bases"][0]["sigla"]
    cod, texto = _codigo(lambda: gera_base(ctx.com_flexoes(""), d, alvo))
    g.testa(f"flexão indecidível sem exceção reprova a geração [{alvo}]",
            cod == Saida.REPROVADO and "indecidível" in texto, f"{cod.name} {texto[-120:]}")

    def excecao(nome, texto, trecho):
        cod, msg = _codigo(lambda: le_excecoes(ctx.com_flexoes(texto)))
        g.testa(f"exceção inválida reprova: {nome}", cod == P and trecho in msg,
                f"{cod.name} {msg[-120:]}")
    um = '[[excecoes]]\ntermo = "education"\nidioma = "en"\n'
    excecao("sem origem", um + 'tipo = "nao_contavel"\n', "origem")
    excecao("tipo fora do domínio", um + 'tipo = "raro"\norigem = "x"\n', "fora do domínio")
    excecao("repetida", (um + 'tipo = "nao_contavel"\norigem = "x"\n') * 2, "repetida")
    excecao("irregular sem formas", um + 'tipo = "irregular"\norigem = "x"\n', "formas")
    e = le_excecoes(ctx.com_flexoes('[[excecoes]]\ntermo = "termo-orfao-autoteste"\n'
                                    'idioma = "en"\ntipo = "nao_contavel"\norigem = "x"\n'))
    g.testa("exceção órfã é relatada", orfas(e, d) == [("termo-orfao-autoteste", "en")])
    g.testa("exceção de termo escrito à mão na fonte (subconjunto, curada) não é órfã",
            orfas(e, d, {"termo-orfao-autoteste"}) == [])


# ------------------------------------------------------- consulta de sondagem por referência
def _consultas(dado):
    """[(índice da sondagem, índice da consulta, consulta)] de todas as sondagens."""
    return [(i, k, c) for i, s in enumerate(dado.get("sondagens", []))
            for k, c in enumerate(s["consultas"])]


def _onde(dado, i, k):
    return (dado["sondagens"][i]["id"], f"consulta {k + 1}")


def _tokens(texto):
    return re.findall(r'"[^"]+"|[^\s()]+', texto)


def referencias(ctx, g):
    """Consulta por referência (`expressao`): a recusa na leitura da fonte, a resolução na
    composição e o texto resolvido no registro. As bases vêm da estrutura das fontes."""
    from .. import fonte as FO
    from .. import procedimentos as PR
    from .. import sondagens as SO
    d = ctx.protocolo()

    def acha(cond):
        """(sigla, dado, frag, arqs, i, k) da primeira consulta que satisfaz `cond`."""
        for b in d["bases"]:
            dado, frag, arqs = fonte_de(ctx, d, b["sigla"])
            for i, k, c in _consultas(dado):
                if cond(dado, c):
                    return b["sigla"], dado, frag, arqs, i, k
        return None

    def simples(dado, c):
        return "expressao" in c and not any(x in c for x in ("consulta",) + G.TRANSFORMACOES)

    def le(sigla, dado, frag, arqs):
        cx = com_fonte(ctx, sigla, dado, frag, arqs)
        return lambda: le_fonte(cx, d, sigla)

    def compoe(sigla, dado, frag, arqs, classe=None):
        cx = com_fonte(ctx, sigla, dado, frag, arqs)
        return lambda: (classe or PR.Composicao)(cx, d, le_fonte(cx, d, sigla))

    def reprova(nome, funcao, trechos, sigla):
        cod, texto = _codigo(funcao)
        faltam = [x for x in trechos if x not in texto]
        g.testa(f"reprovou (PROTOCOLO_ILEGIVEL): {nome} [{sigla}]", cod == P and not faltam,
                f"{cod.name}, faltou {faltam} — {texto[-160:]}")

    ref = acha(simples)
    if ref is None:
        g.falha("mutação não aplicada: nenhuma consulta por referência sem transformação")
        return
    sigla, dado0, frag, arqs, i, k = ref
    sd, cons = _onde(dado0, i, k)
    lit = acha(lambda x, c: "texto" in c)

    def muda(base, mutar):
        sig, dado, fr, ar = base
        x = copy.deepcopy(dado)
        mutar(x)
        if x == dado:
            g.falha("mutação não aplicada")
        return sig, x, fr, ar

    base_ref = (sigla, dado0, frag, arqs)

    # -- camada da fonte (leitura)
    def na_ref(**mud):
        def mutar(x):
            c = x["sondagens"][i]["consultas"][k]
            for chave, valor in mud.items():
                if valor is None:
                    c.pop(chave, None)
                else:
                    c[chave] = valor
        return muda(base_ref, mutar)
    reprova("`texto` e `expressao` juntos", le(*na_ref(texto="TS=(x)")),
            (sd, cons, "juntos"), sigla)
    reprova("nem `texto` nem `expressao`", le(*na_ref(expressao=None)),
            (sd, cons, "nem `texto` nem `expressao`"), sigla)
    fora = f"{G.I_EB.prefixo}{len(d['expressoes']) + 1}"
    reprova("expressão inexistente", le(*na_ref(expressao=fora)), (sd, cons, fora), sigla)
    reprova("`metade` com parte fora de {1, 2}",
            le(*na_ref(metade={"faceta": d["facetas"][0]["id"], "parte": 3})),
            (sd, cons, "parte 3"), sigla)
    reprova("`metade` de faceta inexistente",
            le(*na_ref(metade={"faceta": "FCT99", "parte": 1})), (sd, cons, "FCT99"), sigla)
    reprova("`metade` fora da forma", le(*na_ref(metade={"faceta": d["facetas"][0]["id"]})),
            (sd, cons, "exige `faceta`"), sigla)
    sem = acha(lambda x, c: isinstance(x["composicao"]["proximidade"], str))
    if sem is None:
        g.falha("mutação não aplicada: nenhuma base sem proximidade com sondagem")
    else:
        s2, dado2, fr2, ar2, i2, k2 = sem

        def sem_prox(x):
            c = x["sondagens"][i2]["consultas"][k2]
            c.pop("texto", None)
            c.update(expressao=d["executada"], sem_proximidade=True)
        reprova("`sem_proximidade` na base sem proximidade",
                le(*muda((s2, dado2, fr2, ar2), sem_prox)),
                (_onde(dado2, i2, k2)[0], "sem_proximidade"), s2)
    if lit is None:
        g.falha("mutação não aplicada: nenhuma consulta literal")
    else:
        s3, dado3, fr3, ar3, i3, k3 = lit
        b3 = (s3, dado3, fr3, ar3)
        sd3, cons3 = _onde(dado3, i3, k3)
        cor = next((f["cor"] for f in dado3["composicao"]["facetas"] if f.get("cor")), None)

        def prosa(texto):
            return muda(b3, lambda x: x["sondagens"][i3]["consultas"][k3].update(texto=texto))
        reprova("consulta em prosa com identificador de expressão",
                le(*prosa(f"o bloco de {d['executada']} no {G.LOCUCAO_REFERENCIA}")),
                (sd3, cons3, repr(d["executada"]), "expressao"), s3)
        reprova("consulta em prosa com a locução", le(*prosa(f"copiar do "
                                                             f"{G.LOCUCAO_REFERENCIA}")),
                (sd3, cons3, G.LOCUCAO_REFERENCIA), s3)
        if cor:
            reprova("consulta em prosa com a cor de uma faceta",
                    le(*prosa(f"a faceta {cor} inteira")), (sd3, cons3, cor), s3)
        reprova("`consulta` declarada com `texto`",
                le(*muda(b3, lambda x: x["sondagens"][i3]["consultas"][k3].update(
                    consulta=G.CONSULTA_MAIS_LONGA))), (sd3, cons3, "só se declaram"), s3)
        cod, texto = _codigo(le(*b3))
        g.testa(f"consulta literal comum não reprova [{s3}]", cod == Saida.OK, texto[-120:])
        # Conferência de marcas desligada: a consulta em prosa passaria (o caso falharia).
        original = FO.marcas_de_referencia
        FO.marcas_de_referencia = lambda *a: []
        try:
            cod, _ = _codigo(le(*prosa(f"o bloco de {d['executada']} no "
                                       f"{G.LOCUCAO_REFERENCIA}")))
        finally:
            FO.marcas_de_referencia = original
        g.testa(f"com a conferência de marcas desligada, a consulta em prosa passa (o caso "
                f"falharia) [{s3}]", cod == Saida.OK, cod.name)

    # -- camada da composição (resolução)
    _, comp0, texto0 = gera_base(com_fonte(ctx, *base_ref), d, sigla)
    alvo = dado0["sondagens"][i]["consultas"][k]["expressao"]
    bloco = comp0.expressoes[alvo]["consultas"][0]["texto"]
    resolvido = comp0.sondagens[sd][k]["texto"]
    g.testa(f"consulta por referência igual ao bloco de {alvo} na §4 [{sigla}]",
            resolvido == bloco and f"```\n{bloco}\n```" in texto0.split(
                G.ESQUELETO["s4"])[1] and f"```\n{resolvido}\n```" in texto0.split(
                G.ESQUELETO["s2"])[0], f"{len(resolvido)} × {len(bloco)}")

    # Strings alteradas: o bloco da sondagem acompanha a composição, sem edição da fonte.
    marca = "zzstringalterada"

    class Alterada(PR.Composicao):
        def _parte(self, fid, campo_q):
            p = super()._parte(fid, campo_q)
            return dict(p, termos=list(p["termos"]) + [marca])

    def acompanha(classe):
        comp = compoe(*base_ref, classe=classe)()
        novo = comp.expressoes[alvo]["consultas"][0]["texto"]
        r = comp.sondagens[sd][k]["texto"]
        return marca in novo and novo != bloco and r == novo
    g.testa(f"com as strings alteradas, a consulta por referência acompanha {alvo} [{sigla}]",
            acompanha(Alterada))

    class Congelada(Alterada):
        def resolve(self, sd_, k_, c):
            r = super().resolve(sd_, k_, c)
            return dict(r, texto=resolvido) if sd_ == sd and k_ == k + 1 else r
    g.testa(f"com a consulta congelada no texto anterior, o caso falharia [{sigla}]",
            not acompanha(Congelada))
    sem_bloco =next((e for e, x in comp0.expressoes.items() if not x["consultas"]), None)

    def derivada(x):
        x["sondagens"][i]["consultas"][k]["expressao"] = alvo
        next(e for e in x["execucao"]["expressoes"] if e["id"] == alvo)["estatuto"] = "derivada"
    if sem_bloco is None:
        reprova("expressão sem bloco na base", compoe(*muda(base_ref, derivada)),
                (sd, cons, "não tem bloco"), sigla)
    else:
        reprova("expressão sem bloco na base", compoe(*na_ref(expressao=sem_bloco)),
                (sd, cons, "não tem bloco"), sigla)

    longa = acha(lambda x, c: c.get("consulta") == G.CONSULTA_MAIS_LONGA)
    if longa is None:
        g.falha("mutação não aplicada: nenhuma consulta `mais_longa`")
    else:
        s4, dado4, fr4, ar4, i4, k4 = longa
        b4 = (s4, dado4, fr4, ar4)
        sd4, cons4 = _onde(dado4, i4, k4)
        comp4 = compoe(*b4)()
        e4 = dado4["sondagens"][i4]["consultas"][k4]["expressao"]
        cs = comp4.expressoes[e4]["consultas"]
        maior = max(len(c["texto"]) for c in cs)
        primeira = next(c for c in cs if len(c["texto"]) == maior)
        r4 = comp4.sondagens[sd4][k4]
        g.testa(f"`mais_longa` é a primeira consulta de maior comprimento de {e4} [{s4}]",
                len(cs) > 1 and r4["texto"] == primeira["texto"]
                and f"consulta {primeira['id']}" in r4["origem"], r4["origem"])

        def na4(**mud):
            return muda(b4, lambda x: x["sondagens"][i4]["consultas"][k4].update(mud))
        reprova("expressão de várias consultas sem `consulta`",
                compoe(*muda(b4, lambda x: x["sondagens"][i4]["consultas"][k4].pop(
                    "consulta"))), (sd4, cons4, "declarar `consulta`"), s4)
        reprova("consulta inexistente na expressão", compoe(*na4(consulta="999z")),
                (sd4, cons4, "'999z' não existe"), s4)
        reprova("transformação em expressão de várias consultas",
                compoe(*na4(metade={"faceta": d["facetas"][0]["id"], "parte": 1})),
                (sd4, cons4, "consulta única"), s4)

    prox = acha(lambda x, c: c.get("sem_proximidade"))
    if prox is None:
        g.falha("mutação não aplicada: nenhuma consulta com `sem_proximidade`")
    else:
        s5, dado5, fr5, ar5, i5, k5 = prox
        b5 = (s5, dado5, fr5, ar5)
        sd5, cons5 = _onde(dado5, i5, k5)
        comp5 = compoe(*b5)()
        c5 = dado5["sondagens"][i5]["consultas"][k5]
        teste = comp5.expressoes[c5["expressao"]]["consultas"][0]["texto"]
        controle = comp5.sondagens[sd5][k5]["texto"]
        p = comp5.fonte["proximidade"]
        op = f" {p['operador']}/{p['distancia']} "
        g.testa(f"`sem_proximidade` difere do teste só no operador [{s5}]",
                controle != teste and teste.count(op) == 1
                and teste.replace(op, " AND ") == controle, f"{controle[:80]}")

        class SemEfeito(PR.Composicao):
            def _ancoras(self, partes, sem_proximidade=False):
                return super()._ancoras(partes, False)
        reprova("com a composição que ignora `sem_proximidade`, a transformação sem efeito",
                compoe(*b5, classe=SemEfeito), (sd5, cons5, "não muda a consulta"), s5)

        # Teto: a resolução reprova o texto acima do teto (composição que o alonga).
        def teto_justo(x):
            x["cobertura"]["teto"] = max(len(c["texto"]) for e in comp5.expressoes.values()
                                         for c in e["consultas"])

        class Alonga(PR.Composicao):
            def _transformada(self, *a):
                return super()._transformada(*a) + " " * (self.fonte["teto"] or 0)
        reprova("consulta resolvida acima do teto",
                compoe(*muda(b5, teto_justo), classe=Alonga), (sd5, cons5, "passa do teto"),
                s5)

    met = acha(lambda x, c: c.get("metade"))
    if met is None:
        g.falha("mutação não aplicada: nenhuma consulta com `metade`")
    else:
        s6, dado6, fr6, ar6, i6, _ = met
        b6 = (s6, dado6, fr6, ar6)
        sd6 = dado6["sondagens"][i6]["id"]
        cs6 = dado6["sondagens"][i6]["consultas"]
        partes = {c["metade"]["parte"]: k for k, c in enumerate(cs6) if c.get("metade")}
        fid = next(c["metade"]["faceta"] for c in cs6 if c.get("metade"))
        e6 = next(c["expressao"] for c in cs6 if c.get("metade"))

        def confere_metades(classe=None):
            comp6 = compoe(*b6, classe=classe)()
            termos = [PR.literal(t, comp6.aspas) for t in comp6.strings[fid]["termos"]]
            inteira = comp6.expressoes[e6]["consultas"][0]["texto"]
            da = [[t for t in _tokens(comp6.sondagens[sd6][partes[n]]["texto"]) if t in termos]
                  for n in sorted(partes)]
            return (sorted(partes) == list(G.METADE_PARTES) and all(da)
                    and da[0] + da[1] == termos
                    and [t for t in _tokens(inteira) if t in termos] == termos)
        g.testa(f"`metade`: a união das partes é a string da faceta {fid}, em ordem [{s6}]",
                confere_metades())

        class SemMetade(PR.Composicao):
            def _transformada(self, ident, onde, sem_prox, metade):
                return super()._transformada(ident, onde, sem_prox, None)
        g.testa(f"com a `metade` desligada, a conferência das partes falha [{s6}]",
                not confere_metades(SemMetade))

    # -- registro: o texto resolvido, não a referência
    with tempfile.TemporaryDirectory() as tmp:
        reg = pathlib.Path(tmp) / "registro.json"
        ev = pathlib.Path(tmp) / "evidencia.png"
        ev.write_bytes(b"autoteste")
        n = len(dado0["sondagens"][i]["consultas"])
        cx = com_fonte(ctx, *base_ref)

        def gravado():
            reg.unlink(missing_ok=True)
            _codigo(lambda: registra(cx, sigla, sd, [1] * n, 1, "2026-01-01T10:00",
                                     [str(ev)], caminho=reg))
            if not reg.exists():
                return None
            r = json.loads(reg.read_text(encoding="utf-8"))
            bd = next(b["id"] for b in d["bases"] if b["sigla"] == sigla)
            return r["bases"][bd]["sondagens"][0]["consultas"][k]["texto"]
        texto_reg = gravado()
        g.testa(f"registro grava o texto resolvido de {alvo}, não a referência [{sigla}]",
                texto_reg == bloco, f"{(texto_reg or '')[:80]!r}")

        class Referencia(PR.Composicao):
            def resolve(self, sd_, k_, c):
                r = super().resolve(sd_, k_, c)
                return dict(r, texto=c.get("expressao") or r["texto"])
        original = SO.Composicao
        SO.Composicao = Referencia
        try:
            texto_ref = gravado()
        finally:
            SO.Composicao = original
        g.testa(f"com o registro gravando a referência, o caso falharia [{sigla}]",
                texto_ref is not None and texto_ref != bloco, f"{texto_ref!r}")
