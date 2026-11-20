"""Instrumento do teste de aderência: a planilha a preencher e o ensaio seco.

As referências, as bases de cada semente e o papel vêm do protocolo; o arquivo de sementes
(`[dados] sementes`) guarda só o que é autoral — verificação, escopo, tipo, alinhamento,
nota —, ligado por DOI ou título, de modo que o rótulo `id` pode mudar sem perder o
metadado. A planilha é gravada em `[saidas] aderencia`.

O ensaio seco — o que cada título entrega às facetas — é impresso no terminal, não
gravado: o instrumento é a planilha. Entrada do arquivo de sementes sem correspondência no
protocolo é reportada, para decisão.
"""

import csv
import json

from .config import relativo
from .dados import campo_pendente, ligacao_semente
from .erros import DadosInvalidos
from .markdown import normaliza
from .saida import Saida


def colunas(d):
    bases = [b["sigla"] for b in d["bases"]]
    executada = d["executada"]
    return [
        ("id", "identificador da semente (SEn), conforme o protocolo"),
        ("autores_ano", "autoria abreviada e ano"),
        ("titulo", "título, como consta na referência do protocolo"),
        ("tipo", "primário ou secundário — preencher no arquivo de sementes"),
        ("escopo", "DENTRO, FRONTEIRA ou ÂNCORA AUSENTE — preencher no arquivo de sementes"),
        ("verificacao", "estado de conferência da referência — preencher no arquivo de "
                        "sementes"),
        ("papel", "papel da semente no conjunto: desenvolvimento ou validação — do protocolo"),
        ("base", " ou ".join(filter(None, [", ".join(bases[:-1]), bases[-1]]))),
        ("esperada_na_base", "sim se a tabela do conjunto-semente do protocolo cita esta base"),
        ("indexada", "etapa 1: sim ou não, por busca de título. **obrigatório**"),
        ("data_etapa1", "data da busca de título"),
        ("recuperada", f"etapa 2: sim ou não, por busca na exportação de {executada}"),
        ("como_localizada", "DOI, título ou não localizada"),
        ("data_etapa2", "data da conferência na exportação"),
        ("observacao", "o que explica o não: termo ausente, campo não indexado, recorte"),
    ]


def carrega(ctx, d):
    autorais = ctx.config.valor("planilha.campos_autorais")
    caminho = ctx.config.caminho("dados.sementes")
    facetas = {"facetas": [{"faceta": fid, "termos": v["termos"]}
                           for fid, v in d["strings"].items()]}
    if not caminho.exists():
        raise DadosInvalidos(f"{relativo(caminho)} não encontrado: é onde vive o metadado "
                             f"autoral das sementes")
    try:
        conteudo = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise DadosInvalidos(f"{relativo(caminho)} ilegível: {e}") from None
    meta = {e["ligacao"]: e for e in conteudo.get("estudos", []) if e.get("ligacao")}

    estudos = []
    for ref in d["sementes"]:
        e = dict(ref)
        # A ligação é por DOI ou título: o `id` é rótulo e pode mudar sem perder o metadado.
        m = meta.get(ligacao_semente(ref), {})
        for c in autorais:
            e[c] = m.get(c, "")
        e["_meta"] = any(str(e.get(c) or "").strip() for c in autorais)
        estudos.append(e)

    atuais = {ligacao_semente(s) for s in d["sementes"]}
    orfas = [k for k in meta if k not in atuais]
    if orfas:
        print(f"AVISO: {len(orfas)} entrada(s) de {caminho.name} sem semente no protocolo: "
              f"{len(orfas)} — decidir: remover com registro ou reincluir no protocolo")
    return facetas, estudos


# ------------------------------------------------------------------------ ensaio
def casa(titulo, termos):
    """Termos presentes no título, por frase inteira, sem distinguir acento ou caixa."""
    alvo = " " + normaliza(titulo) + " "
    return [t for t in termos if " " + normaliza(t) + " " in alvo]


def ensaio(estudos, facetas):
    por_faceta = {f["faceta"]: f["termos"] for f in facetas["facetas"]}
    return [(e, {n: casa(e["titulo"], ts) for n, ts in por_faceta.items()}) for e in estudos]


def relata_ensaio(d, estudos, facetas):
    """Imprime o ensaio seco: o que cada título entrega às facetas."""
    ids_facetas = [f["id"] for f in d["facetas"]]
    faceta_de = {v["id"]: fid for fid, v in d["strings"].items()}
    grupos = [[faceta_de[x] for x in g] for g in d["expressoes"][d["executada"]]]
    ens = ensaio(estudos, facetas)
    print("\nEnsaio seco — termos presentes no título, por faceta:")
    for e, pf in ens:
        achados = "  ".join(f"{f}: " + (", ".join(pf[f]) if pf[f] else "—")
                            for f in ids_facetas)
        print(f"  {e['id']:>4} {e['chave']}: {achados}")
    n_exec = sum(1 for _, pf in ens if all(any(pf.get(f) for f in g) for g in grupos))
    print(f"\n{n_exec} de {len(estudos)} satisfazem a composição de {d['executada']} pelo "
          "título. É ensaio, não execução: a busca alcança resumo e palavras-chave, de modo "
          "que a semente sem termo no título ainda pode ser recuperada.")


def _pendentes(estudos):
    """Sementes com campo de metadado ainda não conferido, e quais campos são."""
    rotulo = {"verificacao": "verificação", "escopo": "escopo",
              "tipo": "tipo", "alinhamento": "alinhamento"}
    saida = []
    for e in estudos:
        campos = [rotulo[c] for c in rotulo if campo_pendente(e.get(c, ""))]
        if campos:
            saida.append((e, campos))
    return saida


def linhas_planilha(d, estudos):
    linhas = []
    for e in estudos:
        for b in (x["sigla"] for x in d["bases"]):
            linhas.append({
                "id": e["id"],
                "autores_ano": f"{e['autores'].split(',')[0].strip()} et al. {e['ano']}",
                "titulo": e["titulo"],
                "tipo": e.get("tipo", ""),
                "escopo": e.get("escopo", ""),
                "verificacao": e.get("verificacao", ""),
                "papel": e["papel"],
                "base": b,
                "esperada_na_base": "sim" if b in e["bases"] else "nao",
                "indexada": "",
                "data_etapa1": "",
                "recuperada": "",
                "como_localizada": "",
                "data_etapa2": "",
                "observacao": "",
            })
    return linhas


def cmd_planilha(ctx, a=None):
    d = ctx.protocolo()
    facetas, estudos = carrega(ctx, d)
    cols = colunas(d)
    linhas = linhas_planilha(d, estudos)
    destino = ctx.config.saida("aderencia")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[c for c, _ in cols])
        w.writeheader()
        w.writerows(linhas)

    print(f"{destino.name}   {len(linhas)} linhas, {len(cols)} colunas")
    com_entrada = sum(1 for e in estudos if e["_meta"])
    confirmadas = sum(1 for e in estudos
                      if str(e.get("verificacao", "")).startswith("CONFIRMADA"))
    alinhadas = sum(1 for e in estudos
                    if e.get("alinhamento")
                    and not str(e["alinhamento"]).startswith(("A CONFERIR", "a conferir")))
    print(f"metadados: {com_entrada}/{len(estudos)} com campo autoral preenchido; "
          f"{confirmadas} com verificação confirmada; {alinhadas} com alinhamento conferido")
    pendentes = _pendentes(estudos)
    if pendentes:
        print("pendências de metadados:")
        for e, campos in pendentes:
            print(f"  {e['id']:>4}. {e['chave']}: {', '.join(campos)}")
    relata_ensaio(d, estudos, facetas)
    return Saida.OK
