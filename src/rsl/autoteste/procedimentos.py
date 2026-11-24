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
from ..procedimentos import gera, gera_base, inicia, problemas_igualdade
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
        _, _, esperado = gera_base(cx, dx, alvo)
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
