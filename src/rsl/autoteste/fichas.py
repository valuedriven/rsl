"""Autoteste da cobertura por base: as conferências leem o derivado da fonte e reprovam o
defeito só na base afetada.

Os defeitos entram de dois modos:
- na cópia em memória da fonte de uma base (`fontes.py`): campo retirado ou fora do domínio,
  critério renumerado, plural pela lematização sem medição, termo só no singular na forma
  curada;
- num compositor errado (`base_derivada(..., composicao=...)`): termo omitido, consulta acima
  do teto, flexão desligada. É o invariante contra gerador errado: as conferências recalculam
  o esperado sem o compositor.

A base de cada caso é escolhida pela estrutura da fonte ("a primeira base com teto
numérico", "a primeira base com proximidade"), e não pelo nome.
"""

import copy
import re

from .. import gramatica as G
from ..cobertura import cobertura_base
from ..erros import ProtocoloInvalido, Reprovado
from ..fichas import base_derivada
from ..flexao import Indecidivel, le_excecoes, plural_por_regra
from ..procedimentos import Composicao, gera_base
from ..saida import Saida
from .fontes import base_com, com_fonte, fonte_de

R, P, OK = Saida.REPROVADO, Saida.PROTOCOLO_ILEGIVEL, Saida.OK


def _problemas(ctx, d, sigla, composicao=None):
    """(código, mensagens) da conferência de cobertura de uma base."""
    try:
        base = base_derivada(ctx, d, sigla, composicao=composicao)
        p = cobertura_base(base, d, le_excecoes(ctx))
        if base["comp"].indecidiveis:
            p.append("flexão indecidível")
        return (R if p else OK), p
    except ProtocoloInvalido as e:
        return P, [str(e)]
    except Reprovado as e:
        return R, [str(e)]


def _omite(fid, ident):
    """Compositor que omite, em toda consulta de `ident`, o último termo de `fid`."""
    class Omite(Composicao):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            alvo = self.strings[fid]["termos"][-1]
            for c in self.expressoes[ident]["consultas"]:
                if c.get("termos") and alvo in c["termos"].get(fid, []):
                    c["termos"][fid] = [t for t in c["termos"][fid] if t != alvo]
            self.omitido = alvo
    return Omite


def _alonga(ident, tamanho):
    """Compositor que estica a primeira consulta de `ident` além de `tamanho`."""
    class Alonga(Composicao):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            c = self.expressoes[ident]["consultas"][0]
            c["texto"] = c["texto"] + " " * (tamanho + 1 - len(c["texto"]))
    return Alonga


def _sem_flexao(*a, **k):
    """Compositor que esquece a flexão (o gerador errado que perde o plural)."""
    k["flexao"] = False
    return Composicao(*a, **k)


def _termo_regular(d, fid, idioma):
    """Um termo da STR de `fid` em `idioma` com plural regular decidível."""
    tabela = next(f for f in d["tabelas"] if f["id"] == fid)
    for linha in tabela["linhas"][idioma].values():
        for t in linha:
            if t in d["strings"][fid]["literais"] and " " in t:
                try:
                    plural_por_regra(t, idioma)
                    return t
                except Indecidivel:
                    continue
    return None


def casos(ctx, g):
    d = ctx.protocolo()
    siglas = [b["sigla"] for b in d["bases"]]
    executada = d["executada"]
    correntes = {s: _problemas(ctx, d, s) for s in siglas}
    reprovadas = [s for s, (c, _) in correntes.items() if c != OK]
    if reprovadas:
        g.falha(f"bases correntes já reprovadas: {reprovadas} — "
                f"{correntes[reprovadas[0]][1][:1]}")
        return

    def so_a_base(nome, alvo, mutar, codigo, trechos, composicao=None, frags=None):
        """Mutação na fonte de `alvo` (ou compositor errado): reprova `alvo` com o código e
        os trechos esperados, e nenhuma outra base."""
        if alvo is None:
            g.falha(f"mutação não aplicada: {nome} (nenhuma base com a condição)")
            return
        dado, frag, arqs = fonte_de(ctx, d, alvo)
        original = copy.deepcopy(dado)
        if mutar:
            mutar(dado)
            if dado == original and frags is None:
                g.falha(f"mutação não aplicada: {nome}")
                return
        if frags is not None:
            frag = frags(frag)
            arqs = ["procedimento.toml"] + sorted(frag)
        cx = com_fonte(ctx, alvo, dado, frag, arqs)
        cod, msgs = _problemas(cx, d, alvo, composicao)
        outras = {s: _problemas(cx, d, s)[0] for s in siglas if s != alvo}
        trechos = (trechos,) if isinstance(trechos, str) else tuple(trechos)
        faltam = [x for x in trechos if not any(x in m for m in msgs)]
        afetadas = [s for s, c in outras.items() if c != OK]
        if cod != codigo:
            g.falha(f"{nome} [{alvo}]: código {cod.name}, esperado {codigo.name} — "
                    f"{msgs[:1]}")
        elif faltam:
            g.falha(f"{nome} [{alvo}]: faltou {faltam} — {msgs[:1]}")
        elif afetadas:
            g.falha(f"{nome} [{alvo}]: reprovou também {afetadas}")
        else:
            achado = next(m for m in msgs if any(x in m for x in trechos))
            g.ok(f"reprovou só a base ({cod.name}): {nome} [{alvo}] — {achado[:80]}")

    primeira = siglas[0]
    ultima = siglas[-1]

    # Critérios: renumerar o protocolo sem atualizar a fonte.
    ce = sorted({c["id"] for c in d["criterios"]}, key=lambda x: int(x[2:]))
    novo = f"{G.I_CE.prefixo}{int(ce[-1][2:]) + 90}"
    def renumera(x):
        for c in x["criterios"]:
            c["ids"] = [novo if i == ce[0] else i for i in c["ids"]]
    so_a_base("fonte cita critério inexistente e omite o vigente", primeira, renumera, R,
              (novo, ce[0]))

    # Forma de execução: ausente e fora do domínio.
    so_a_base("forma de execução ausente", ultima,
              lambda x: x["execucao"].pop("forma"), P, ("`forma`",))
    so_a_base("forma de execução fora do domínio", ultima,
              lambda x: x["execucao"].update(forma="dividida"), P, ("dividida",))

    # Teto: ausente e ilegível.
    so_a_base("teto ausente", primeira, lambda x: x["cobertura"].pop("teto"), P, ("`teto`",))
    so_a_base("teto ilegível", primeira, lambda x: x["cobertura"].update(teto="curto"), P,
              ("curto",))

    # Plural: ausente, fora do domínio, idioma sem valor.
    so_a_base("plural ausente", primeira, lambda x: x["cobertura"].pop("plural"), P,
              ("`plural`",))
    so_a_base("plural fora do domínio", primeira,
              lambda x: x["cobertura"].update(plural="omitido"), P,
              (G.PLURAL_EXPLICITO, G.PLURAL_LEMATIZACAO))
    multi = base_com(ctx, d, lambda x: len({i for v in x["cobertura"]["idiomas"].values()
                                           for i in v}) > 1)
    if multi:
        dado_m, _, _ = fonte_de(ctx, d, multi)
        idiomas_m = sorted({i for v in dado_m["cobertura"]["idiomas"].values() for i in v})
        so_a_base("plural por idioma sem um dos idiomas", multi,
                  lambda x: x["cobertura"].update(
                      plural={i: G.PLURAL_EXPLICITO for i in idiomas_m[:-1]}), P,
                  (idiomas_m[-1],))
    else:
        g.falha("mutação não aplicada: plural por idioma (nenhuma base com mais de um idioma)")

    # Plural pela lematização sem lematização medida; e com ela medida (não reprova).
    def lematizacao_nao_medida(x):
        x["cobertura"]["plural"] = G.PLURAL_LEMATIZACAO
        for s in x["sintaxe"]:
            if s["categoria"] == G.CATEGORIA_LEMATIZACAO:
                s.pop("citacao", None)
                s["situacao"] = G.SITUACAO_NAO_VERIFICADO
                if not s.get("sondagem"):
                    s["sem_sondagem"] = "autoteste"
    so_a_base("plural pela lematização sem lematização medida", primeira,
              lematizacao_nao_medida, R, (G.PLURAL_LEMATIZACAO,))
    bd1 = d["bases"][0]["id"]
    dado, frag, arqs = fonte_de(ctx, d, primeira)
    dado["cobertura"]["plural"] = G.PLURAL_LEMATIZACAO
    for s in dado["sintaxe"]:
        if s["categoria"] == G.CATEGORIA_LEMATIZACAO:
            s.update(situacao=G.SITUACAO_MEDICAO, citacao=f"{bd1}/autoteste-lematizacao")
            s.pop("sondagem", None)
            s.pop("sem_sondagem", None)
            s.pop("idioma", None)
    for sd in dado.get("sondagens", []):
        lem = {s["elemento"] for s in dado["sintaxe"]
               if s["categoria"] == G.CATEGORIA_LEMATIZACAO}
        sd["elementos"] = [e for e in sd["elementos"] if e not in lem] or sd["elementos"]
    cod, msgs = _problemas(com_fonte(ctx, primeira, dado, frag, arqs), d, primeira)
    g.testa(f"plural pela lematização com lematização medida e citada não reprova "
            f"essa dimensão [{primeira}]",
            not any(G.PLURAL_LEMATIZACAO in m for m in msgs), f"{cod.name} {msgs[:1]}")

    # Termo só no singular na forma curada, e o mesmo termo declarado não contável.
    alvo_c = base_com(ctx, d, lambda x: any("en" in v for v in
                                            x["cobertura"]["idiomas"].values())
                      and x["cobertura"]["plural"] == G.PLURAL_EXPLICITO)
    fid_c = next((f for f in sorted(d["strings"]) if _termo_regular(d, f, "en")), None)
    if alvo_c and fid_c:
        termo = _termo_regular(d, fid_c, "en")
        dado_c, _, _ = fonte_de(ctx, d, alvo_c)
        if "en" not in dado_c["cobertura"]["idiomas"].get(fid_c, []):
            alvo_c = None
    if alvo_c and fid_c:
        ancoras = list(d["ancoras"])
        def curada(x):
            x["execucao"]["forma"] = "curada"
            x["curadas"] = [{"grupo": "autoteste", "consulta": f'"{termo}"',
                             "facetas": sorted(set(ancoras + [fid_c]))}]
        so_a_base("termo só no singular na forma curada", alvo_c, curada, R,
                  (repr(termo), fid_c, "en"))
        dado, frag, arqs = fonte_de(ctx, d, alvo_c)
        curada(dado)
        exc = (ctx.texto_flexoes.rstrip("\n") + "\n\n[[excecoes]]\n"
               f'termo = "{termo}"\nidioma = "en"\ntipo = "nao_contavel"\n'
               'origem = "autoteste"\n')
        cx = com_fonte(ctx, alvo_c, dado, frag, arqs).com_flexoes(exc)
        _, msgs = _problemas(cx, d, alvo_c)
        g.testa(f"termo só no singular declarado não contável não reprova [{alvo_c}]",
                not any("só no singular" in m and repr(termo) in m for m in msgs),
                f"{msgs[:1]}")
    else:
        g.falha("mutação não aplicada: termo só no singular na forma curada")

    # Invariante contra gerador errado.
    fid_omite = sorted(d["strings"])[-1]
    so_a_base(f"compositor omite um termo de {fid_omite} no bloco de {executada}", primeira,
              None, R, ("não está no bloco",), composicao=_omite(fid_omite, executada))
    com_teto = base_com(ctx, d, lambda x: isinstance(x["cobertura"]["teto"], int))
    if com_teto:
        teto = fonte_de(ctx, d, com_teto)[0]["cobertura"]["teto"]
        so_a_base("compositor deixa consulta acima do teto", com_teto, None, R,
                  (f"acima do teto de caracteres declarado ({teto})",),
                  composicao=_alonga(executada, teto))
    else:
        g.falha("mutação não aplicada: consulta acima do teto (nenhuma base com teto)")
    com_explicito = base_com(ctx, d, lambda x: x["cobertura"]["plural"] ==
                             G.PLURAL_EXPLICITO and not x.get("radical"))
    so_a_base("compositor esquece a flexão", com_explicito, None, R, ("não está no bloco",),
              composicao=_sem_flexao)

    # Estratégia de proximidade: bloco cercado no fragmento não entra no derivado.
    prox = base_com(ctx, d, lambda x: isinstance(x["composicao"]["proximidade"], dict))
    if prox:
        dado, frag, arqs = fonte_de(ctx, d, prox)
        antes = base_derivada(ctx, d, prox)
        frag2 = dict(frag, **{"estrategia_de_proximidade.md":
                              "Discussão.\n\n```\nTS=(a NEAR/2 b)\n```\n"})
        cx = com_fonte(ctx, prox, dado, frag2, ["procedimento.toml"] + sorted(frag2))
        depois = base_derivada(cx, d, prox)
        _, _, texto = gera_base(cx, d, prox)
        g.testa(f"bloco cercado na estratégia de proximidade não entra no derivado [{prox}]",
                antes["expressoes"] == depois["expressoes"]
                and re.search(r"^### Estratégia de proximidade$", texto, re.M) is not None,
                "derivado mudou ou subseção ausente")
    else:
        g.falha("mutação não aplicada: estratégia de proximidade (nenhuma base com "
                "proximidade)")
