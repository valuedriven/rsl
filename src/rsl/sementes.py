"""Ensaio seco do teste de aderência (`aderencia ensaiar`): o que o título, as
palavras-chave e o resumo de cada semente entregam às facetas.

O ensaio só imprime: não grava arquivo. Para cada semente e faceta, imprime os termos da STR
da faceta encontrados, cada um marcado com o campo onde apareceu (T título, P
palavras-chave, R resumo), por frase inteira e sem distinguir acento nem caixa. Relata
quantas sementes satisfazem a composição da executada só pelo título e quantas pelos três
campos juntos, e lista a faceta alinhada à semente (`alinhamento_facetas`) sem termo em campo
nenhum, como indício de lacuna de vocabulário. Campo que a cópia da coleção não traz é
"campo ausente", e não "sem termo".

É ensaio, não execução: as palavras-chave são as atribuídas pela OpenAlex, e não as do autor
nem as da base, e a base pode indexar outros campos. Quem mede é `aderencia medir`; quem
explica uma perda é `aderencia diagnosticar`. O ensaio não é declaração de faceta: o
alinhamento é juízo do pesquisador e não se copia do ensaio.
"""

from .markdown import normaliza
from .saida import Saida

# Campos do ensaio, na ordem do relato: (chave no dicionário da semente, marca, nome).
CAMPOS = (("titulo", "T", "título"), ("palavras_chave", "P", "palavras-chave"),
          ("resumo", "R", "resumo"))


def casa(texto, termos):
    """Termos presentes no texto, por frase inteira, sem distinguir acento ou caixa."""
    alvo = " " + normaliza(texto) + " "
    return [t for t in termos if " " + normaliza(t) + " " in alvo]


def _textos(e, campo):
    """Os textos de um campo da semente: as palavras-chave, uma a uma (o termo não casa
    através de duas); os demais, um texto. Lista vazia é campo ausente."""
    valor = e.get(campo)
    if isinstance(valor, list):
        return [x for x in valor if str(x).strip()]
    return [valor] if str(valor or "").strip() else []


def achados(e, termos):
    """{termo: [marcas dos campos onde apareceu]}, só dos termos encontrados."""
    saida = {}
    for campo, marca, _ in CAMPOS:
        for texto in _textos(e, campo):
            for t in casa(texto, termos):
                if marca not in saida.setdefault(t, []):
                    saida[t].append(marca)
    return saida


def ausentes(e):
    """Nomes dos campos que a cópia não traz para a semente."""
    return [nome for campo, _, nome in CAMPOS if not _textos(e, campo)]


def alinhadas(e):
    """Facetas alinhadas à semente."""
    return list(e.get("alinhamento_facetas") or {})


def ensaio(d):
    """[(semente, {faceta: {termo: [marcas]}})], na ordem das sementes."""
    por_faceta = {fid: v["termos"] for fid, v in d["strings"].items()}
    return [(e, {f: achados(e, ts) for f, ts in por_faceta.items()}) for e in d["sementes"]]


def satisfaz(pf, grupos, so_titulo):
    """A semente satisfaz a composição: cada grupo tem faceta com termo (no título, ou em
    qualquer dos três campos)."""
    def tem(f):
        return any(("T" in m) if so_titulo else bool(m) for m in pf.get(f, {}).values())
    return all(any(tem(f) for f in g) for g in grupos)


def relata(d):
    """Linhas do ensaio seco."""
    ids_facetas = [f["id"] for f in d["facetas"]]
    faceta_de = {v["id"]: fid for fid, v in d["strings"].items()}
    grupos = [[faceta_de[x] for x in g] for g in d["expressoes"][d["executada"]]]
    ens = ensaio(d)
    L = ["Ensaio seco — termos de cada faceta, com o campo onde apareceram (T título, "
         "P palavras-chave, R resumo):"]
    for e, pf in ens:
        falta = ausentes(e)
        marca = f"  [{', '.join(f'{x} ausente' for x in falta)}]" if falta else ""
        L.append(f"  {e['id']:>4} {e['chave']}{marca}")
        for f in ids_facetas:
            termos = pf.get(f, {})
            texto = ", ".join(f"{t} ({','.join(m)})" for t, m in termos.items()) or "—"
            L.append(f"         {f}: {texto}")
        lacuna = [f for f in alinhadas(e) if not pf.get(f)]
        if lacuna and falta:
            L.append(f"         alinhada sem termo nos campos presentes ({', '.join(falta)} "
                     f"ausente: não é indício de lacuna): {', '.join(lacuna)}")
        elif lacuna:
            L.append(f"         alinhada sem termo em campo nenhum (indício de lacuna de "
                     f"vocabulário): {', '.join(lacuna)}")
    n = len(ens)
    so_titulo = sum(1 for _, pf in ens if satisfaz(pf, grupos, True))
    tres = sum(1 for _, pf in ens if satisfaz(pf, grupos, False))
    sem_resumo = sum(1 for e, _ in ens if "resumo" in ausentes(e))
    sem_palavras = sum(1 for e, _ in ens if "palavras-chave" in ausentes(e))
    L += ["",
          f"Composição de {d['executada']}: {so_titulo} de {n} sementes a satisfazem só pelo "
          f"título; {tres} de {n}, pelos três campos juntos.",
          f"Campo ausente na cópia: resumo em {sem_resumo} de {n}; palavras-chave em "
          f"{sem_palavras} de {n} — a falta de termo nesses campos não é resultado.",
          "É ensaio, não execução: as palavras-chave vêm da OpenAlex (atribuídas por ela), e "
          "não do autor nem da base, e a base pode indexar outros campos. Quem mede a "
          "recuperação é `aderencia medir`; quem explica a perda é `aderencia diagnosticar`."]
    return L


def cmd_ensaiar(ctx, a=None):
    d = ctx.protocolo()
    copia = d.get("zotero")
    if copia:
        print(f"Cópia da coleção do Zotero: versão {copia['versao']}, lida em "
              f"{copia['lida_em']}.")
    print("\n".join(relata(d)))
    return Saida.OK
