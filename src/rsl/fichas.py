"""O derivado de cada base: a estrutura que as conferências e a busca leem.

O derivado vem da fonte do procedimento de busca (`fonte.py`) e da composição dos blocos
(`procedimentos.py`), e nunca do markdown gerado, que se confere só por igualdade. O campo e
o filtro de cada bloco vêm de `[composicao]` e de `[[criterios]]`: nada aqui reconhece campo
nem filtro pelo texto.
"""

from . import gramatica as G
from .erros import ProtocoloInvalido
from .fonte import le_fonte

MODOS_EXECUCAO = G.FORMAS_EXECUCAO
MODO_CURADA = "curada"


def base_de(d, sigla):
    """A base de sigla `sigla`, da tabela de bases lida em `d`."""
    achada = next((b for b in d["bases"] if b["sigla"] == sigla), None)
    if achada is None:
        raise ProtocoloInvalido(G.T_BASES, f"base {sigla!r} não consta da tabela "
                                           f"({[b['sigla'] for b in d['bases']]})")
    return achada


def forma_execucao(ctx, d, sigla):
    """A forma de execução declarada na fonte (`[execucao] forma`)."""
    return le_fonte(ctx, d, sigla)["dado"]["execucao"]["forma"]


def base_derivada(ctx, d, sigla, flexao=True, composicao=None):
    """O derivado de uma base: facetas, critérios, expressões, execução e declaração.
    `composicao` substitui a classe compositora (o autoteste injeta defeito por aqui)."""
    from .procedimentos import Composicao                           # noqa: PLC0415
    b = base_de(d, sigla)
    fonte = le_fonte(ctx, d, sigla)
    comp = (composicao or Composicao)(ctx, d, fonte, flexao=flexao)
    dado = fonte["dado"]
    facetas = []
    for fid, s in comp.strings.items():
        facetas.append({"id": s["id"], "faceta": fid, "termos": list(s["termos"]),
                        "radical": bool(s.get("radical"))})
    for s in comp.subconjuntos.values():
        facetas.append({"id": s["id"], "faceta": s["faceta"], "termos": list(s["termos"]),
                        "radical": False})
    faceta_de = comp.faceta_de
    expressoes = {}
    for ident, e in comp.expressoes.items():
        fids = sorted({faceta_de[x] for g in d["expressoes"][ident] for x in g})
        expressoes[ident] = {"id": ident, "estatuto": e["estatuto"], "facetas": fids,
                             "consultas": e["consultas"]}
    executada = d["executada"]
    itens = [{"rotulo": c["rotulo"] or c["id"], "consulta": c["texto"], "id": c["id"]}
             for c in comp.expressoes[executada]["consultas"]]
    cob = dado["cobertura"]
    declaracao = {"idiomas": cob["idiomas"],
                  "derivacoes": cob.get("derivacoes") or [], "plural": fonte["plural"],
                  "teto": fonte["teto"], "exclusoes": dado.get("reducao", [])}
    criterios = sorted({i for c in dado["criterios"] for i in c["ids"]},
                       key=lambda x: int(x[len(G.I_CE.prefixo):]))
    return {
        "base": {"id": b["id"], "sigla": sigla, "nome": b["nome"], "ficha": b["ficha"],
                 "fonte": fonte["pasta"], "execucao_declarada": dado["execucao"]["forma"]},
        "facetas": facetas,
        "criterios": criterios,
        "expressoes": expressoes,
        "execucao": {"modo": dado["execucao"]["forma"], "expressao": executada,
                     "itens": itens},
        "declaracao": declaracao,
        "sintaxe": dado["sintaxe"],
        "curadas": dado.get("curadas", []),
        "fonte": fonte,
        "comp": comp,
    }
