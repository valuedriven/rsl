#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o instrumento do teste de aderência a partir do protocolo.

Entradas
  docs/03_protocolo_estrategia_pesquisa.md   referências, mapa por base e facetas
  data/sementes.json   metadados de conferência autorais, ligados por DOI ou título

As referências vêm do protocolo, lido por src/protocolo.py; `sementes.json` guarda só o
que é autoral — verificação, escopo, tipo, alinhamento, nota. A ligação é feita por DOI
ou título, de modo que o rótulo `id` pode mudar sem perder o metadado.

Saída
  data/semente_aderencia.csv   planilha a preencher durante a execução

O ensaio seco — o que cada título entrega às facetas — é impresso no terminal, não
gravado: o instrumento é a planilha.

Entrada de `sementes.json` sem correspondência no protocolo é reportada, para decisão.

Uso
  python3 src/gen_semente.py
"""
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import protocolo                                                    # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
PLANILHA = DATA / "semente_aderencia.csv"
SEMENTES = DATA / "sementes.json"

BASES = ["WoS", "Scopus", "ERIC", "BRAPCI"]
FACETAS = ["FCT1", "FCT2", "FCT3", "FCT4"]

COLS = [
    ("id", "identificador da semente (SEn), conforme o protocolo"),
    ("autores_ano", "autoria abreviada e ano"),
    ("titulo", "título, como consta na referência do protocolo"),
    ("tipo", "primário ou secundário — preencher em sementes.json"),
    ("escopo", "DENTRO, FRONTEIRA ou ÂNCORA AUSENTE — preencher em sementes.json"),
    ("verificacao", "estado de conferência da referência — preencher em sementes.json"),
    ("base", "WoS, Scopus, ERIC ou BRAPCI"),
    ("esperada_na_base", "sim se o mapa do protocolo indica esta base"),
    ("indexada", "etapa 1: sim ou não, por busca de título. **obrigatório**"),
    ("data_etapa1", "data da busca de título"),
    ("recuperada", "etapa 2: sim ou não, por busca na exportação de EB4"),
    ("como_localizada", "DOI, título ou não localizada"),
    ("data_etapa2", "data da conferência na exportação"),
    ("observacao", "o que explica o não: termo ausente, campo não indexado, recorte"),
]


def carrega():
    d = protocolo.analisa()
    facetas = {"facetas": [{"faceta": fid, "termos": v["termos"]}
                           for fid, v in d["strings"].items()]}
    meta = {}
    if SEMENTES.exists():
        for e in json.loads(SEMENTES.read_text(encoding="utf-8")).get("estudos", []):
            if e.get("ligacao"):
                meta[e["ligacao"]] = e
    else:
        raise SystemExit("data/sementes.json não encontrado: é onde vive o metadado autoral "
                         "das sementes")

    estudos = []
    for ref in d["sementes"]:
        e = dict(ref)
        # A ligação é por DOI ou título: o `id` é rótulo e pode mudar sem perder o metadado.
        m = meta.get(protocolo.ligacao_semente(ref), {})
        for c in protocolo.CAMPOS_AUTORAIS:
            e[c] = m.get(c, "")
        e["_meta"] = any(str(e.get(c) or "").strip() for c in protocolo.CAMPOS_AUTORAIS)
        estudos.append(e)

    atuais = {protocolo.ligacao_semente(s) for s in d["sementes"]}
    orfas = [k for k in meta if k not in atuais]
    if orfas:
        print(f"AVISO: {len(orfas)} entrada(s) de sementes.json sem semente no protocolo: "
              f"{len(orfas)} — decidir: remover com registro ou reincluir no protocolo")
    return facetas, estudos


# ------------------------------------------------------------------------ ensaio
def casa(titulo, termos):
    """Termos presentes no título, por frase inteira, sem distinguir acento ou caixa."""
    alvo = " " + protocolo.normaliza(titulo) + " "
    return [t for t in termos if " " + protocolo.normaliza(t) + " " in alvo]


def ensaio(estudos, facetas):
    por_faceta = {f["faceta"]: f["termos"] for f in facetas["facetas"]}
    linhas = []
    for e in estudos:
        linhas.append((e, {n: casa(e["titulo"], ts) for n, ts in por_faceta.items()}))
    return linhas


def relata_ensaio(estudos, facetas):
    """Imprime o ensaio seco: o que cada título entrega às facetas."""
    ens = ensaio(estudos, facetas)
    print("\nEnsaio seco — termos presentes no título, por faceta:")
    for e, pf in ens:
        achados = "  ".join(f"{f}: " + (", ".join(pf[f]) if pf[f] else "—")
                            for f in FACETAS)
        print(f"  {e['id']:>4} {e['chave']}: {achados}")
    n_e4 = sum(1 for _, pf in ens if pf.get("FCT1") and pf.get("FCT2")
               and (pf.get("FCT3") or pf.get("FCT4")))
    print(f"\n{n_e4} de {len(estudos)} satisfazem as duas âncoras e uma faceta temática pelo "
          "título. É ensaio, não execução: a busca alcança resumo e palavras-chave, de modo "
          "que a semente sem termo no título ainda pode ser recuperada.")


def _pendentes(estudos):
    """Sementes com campo de metadado ainda não conferido, e quais campos são."""
    ROTULO = {"verificacao": "verificação", "escopo": "escopo",
              "tipo": "tipo", "alinhamento": "alinhamento"}
    saida = []
    for e in estudos:
        campos = []
        for c in ("verificacao", "escopo", "tipo", "alinhamento"):
            v = str(e.get(c, "") or "")
            if not v or v.startswith(("A CONFERIR", "a conferir")) or "PENDÊNCIA" in v:
                campos.append(ROTULO[c])
        if campos:
            saida.append((e, campos))
    return saida


def csv_out(estudos):
    linhas = []
    for e in estudos:
        for b in BASES:
            linhas.append({
                "id": e["id"],
                "autores_ano": f"{e['autores'].split(',')[0].strip()} et al. {e['ano']}",
                "titulo": e["titulo"],
                "tipo": e.get("tipo", ""),
                "escopo": e.get("escopo", ""),
                "verificacao": e.get("verificacao", ""),
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


def main():
    facetas, estudos = carrega()

    linhas = csv_out(estudos)
    with PLANILHA.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[c for c, _ in COLS])
        w.writeheader()
        w.writerows(linhas)

    print(f"semente_aderencia.csv   {len(linhas)} linhas, {len(COLS)} colunas")
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
    relata_ensaio(estudos, facetas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
