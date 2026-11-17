#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o instrumento do teste de aderência a partir do protocolo.

Entradas
  data/strings.json    DERIVADO do protocolo (termos executados das quatro facetas)
  data/sementes.json   MISTO — referências e mapa por base derivados do protocolo, com
                       os metadados de conferência autorais preservados por --gerar

Saídas em data/saida/semente/
  Conjunto_Semente.md     guia de execução do teste
  semente_aderencia.csv   planilha a preencher durante a execução

Semente marcada com no_protocolo=false — retirada do documento sem ser apagada — fica
fora do instrumento e é reportada, para decisão.

Uso
  python3 src/protocolo.py --gerar
  python3 src/gen_semente.py
"""
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import protocolo                                                    # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
SAIDA = DATA / "saida" / "semente"
SEMENTES = DATA / "sementes.json"
STRINGS = DATA / "strings.json"

BASES = ["WoS", "Scopus", "ERIC", "BRAPCI"]
CORES = {1: "\U0001F7E6", 2: "\U0001F7E8", 3: "\U0001F7E5", 4: "\U0001F7E7"}

COLS = [
    ("n", "número da semente, conforme o protocolo"),
    ("autores_ano", "autoria abreviada e ano"),
    ("titulo", "título, como consta na referência do protocolo"),
    ("tipo", "primário ou secundário — preencher em sementes.json"),
    ("escopo", "DENTRO, FRONTEIRA ou ÂNCORA AUSENTE — preencher em sementes.json"),
    ("verificacao", "estado de conferência da referência — preencher em sementes.json"),
    ("base", "WoS, Scopus, ERIC ou BRAPCI"),
    ("esperada_na_base", "sim se o mapa do protocolo indica esta base"),
    ("indexada", "etapa 1: sim ou não, por busca de título. **obrigatório**"),
    ("data_etapa1", "data da busca de título"),
    ("recuperada", "etapa 2: sim ou não, por busca na exportação de E4"),
    ("como_localizada", "DOI, título ou não localizada"),
    ("data_etapa2", "data da conferência na exportação"),
    ("observacao", "o que explica o não: termo ausente, campo não indexado, recorte"),
]


def carrega():
    if not SEMENTES.exists():
        raise SystemExit("sementes.json não encontrado: rode  python3 src/protocolo.py --gerar")
    facetas = protocolo.carrega(STRINGS)
    dados = protocolo.carrega(SEMENTES)

    estudos = []
    for ref in dados["estudos"]:
        if ref.get("no_protocolo") is False:
            continue
        e = dict(ref)
        e["_meta"] = any(str(ref.get(c) or "").strip() for c in protocolo.CAMPOS_AUTORAIS)
        estudos.append(e)

    orfas = [e for e in dados["estudos"] if e.get("no_protocolo") is False]
    if orfas:
        print(f"AVISO: {len(orfas)} semente(s) fora do protocolo em sementes.json, "
              f"fora do instrumento:")
        for e in orfas:
            print(f"  {e.get('n')}. {e.get('chave', '')} — decidir: remover com registro "
                  f"ou reincluir no protocolo")
    return facetas, dados, estudos


# ------------------------------------------------------------------------ ensaio
def casa(titulo, termos):
    """Termos presentes no título, por frase inteira, sem distinguir acento ou caixa."""
    alvo = " " + protocolo.normaliza(titulo) + " "
    return [t for t in termos if " " + protocolo.normaliza(t) + " " in alvo]


def ensaio(estudos, facetas):
    por_faceta = {f["n"]: f["termos"] for f in facetas["facetas"]}
    linhas = []
    for e in estudos:
        linhas.append((e, {n: casa(e["titulo"], ts) for n, ts in por_faceta.items()}))
    return linhas


# ---------------------------------------------------------------------- markdown
def md(facetas, sementes, estudos):
    L = []
    A = L.append
    dist = sementes["distribuicao"]
    limiar = f"{sementes['limiar']:.0%}"
    ens = ensaio(estudos, facetas)

    A("# Conjunto-semente — instrumento do teste de aderência\n")
    A(f"**{len(estudos)} estudos**, todos primários e dentro do recorte temporal, conforme a "
      "seção *Acervos pessoais* do protocolo. As referências e o mapa por base são lidos "
      "daquele documento; este instrumento é derivado dele e não o substitui.\n")

    A("## 1. Para que serve\n")
    A("O conjunto-semente é o controlo externo da busca: estudos que o pesquisador **já "
      "sabe** serem pertinentes, reunidos antes da execução e por caminho independente "
      "dela. A expressão é executada e se pergunta quantos deles ela recupera.\n")
    A("A pergunta que o teste responde não é se a busca achou coisa boa, e sim **se ela "
      "deixou de achar coisa que se sabia existir**. Perder uma semente conhecida indica "
      "que a busca perde também o que não se conhece.\n")
    A(f"**Limiar do protocolo: {limiar}.** Abaixo dele, revisa-se o controlo "
      "terminológico antes de prosseguir, com emenda registrada no Anexo A. O limiar é "
      "decisão do projeto, não norma da literatura, e consta como tal no relato.\n")

    A("## 2. Composição por base — conferida contra o mapa do protocolo\n")
    A("São **incidências por base**, não estudos distintos: um mesmo estudo pode estar "
      "indexado em mais de uma base.\n")
    A("| Base | Incidências |")
    A("| :--- | :---: |")
    for b in BASES:
        A(f"| {b} | {dist['por_base'].get(b, 0)} |")
    A(f"| **Total** | **{dist['incidencias']}** |")
    A("")
    A(f"{dist['registros']} registros únicos: {dist['em_mais_de_uma_base']} estudos em mais "
      f"de uma base e {dist['em_uma_so']} em uma só.\n")

    faltando = [e for e in estudos if not e["_meta"]]
    if faltando:
        A(f"> **{len(faltando)} sementes sem metadados em `data/sementes.json`.** As colunas "
          "de conferência, escopo e tipo saem em branco para elas. O instrumento pode ser "
          "executado; o que falta é registro, não dado de busca.\n")

    pendentes = _pendentes(estudos)
    if pendentes:
        A(f"> **{len(pendentes)} sementes com metadados pendentes.** O campo marcado "
          "`A CONFERIR` ou `PENDÊNCIA` não foi verificado nesta rodada; o instrumento "
          "registra a pendência em vez de a esconder.\n")
        for e, campos in pendentes:
            A(f"> - **{e['n']}. {e['chave']}** — {', '.join(campos)}")
        A("")

    A("## 3. Referências\n")
    for e in estudos:
        A(f"**{e['n']}. {e['autores']} ({e['ano']}).** {e['titulo']}")
        if e.get("doi"):
            A(f"- DOI: `{e['doi']}`")
        A(f"- Bases esperadas: {', '.join(e['bases']) or '—'}")
        if e.get("verificacao"):
            A(f"- Conferência: {e['verificacao']}")
        if e.get("escopo"):
            A(f"- Escopo: {e['escopo']}")
        if e.get("tipo"):
            A(f"- Tipo: {e['tipo']}")
        if e.get("veiculo_conferido"):
            A(f"- Veículo conferido: {e['veiculo_conferido']}")
        if e.get("alinhamento"):
            A(f"- Alinhamento P–Co–I–O: {e['alinhamento']}")
        if e.get("nota"):
            A(f"- Nota: {e['nota']}")
        A("")

    A("## 4. Ensaio seco — o que o título entrega às facetas\n")
    A("Casamento por frase inteira entre cada título e os termos das quatro facetas, nos "
      "três idiomas. **É ensaio, não execução**: a busca procura em título, resumo e "
      "palavras-chave, de modo que a semente sem termo no título ainda pode ser "
      "recuperada pelo resumo.\n")
    A("| # | " + " | ".join(f"{CORES[n]} F{n}" for n in sorted(CORES)) +
      " | E4 (F1+F2) pelo título |")
    A("| :---: | " + " | ".join(":---" for _ in CORES) + " | :--- |")
    for e, pf in ens:
        cels = ["`" + "`, `".join(pf[n]) + "`" if pf[n] else "—" for n in sorted(CORES)]
        e4 = "**sim**" if pf.get(1) and pf.get(2) else "**não**"
        A(f"| {e['n']} | " + " | ".join(cels) + f" | {e4} |")
    A("")
    n_e4 = sum(1 for _, pf in ens if pf.get(1) and pf.get(2))
    A(f"**{n_e4} de {len(estudos)} satisfazem as duas âncoras pelo título.** Nas demais, a "
      "recuperação depende do resumo — e é nelas que a etapa 2 do procedimento exige "
      "cuidado: ausência na exportação pode ser falha da busca ou ausência do termo em "
      "todos os campos indexados.\n")

    A("## 5. Planilha a preencher\n")
    A(f"`semente_aderencia.csv`, uma linha por semente e por base — {len(estudos)} × "
      f"{len(BASES)} = {len(estudos) * len(BASES)} linhas. Preencher durante a execução, "
      "não depois: as colunas de registro são a evidência do teste.\n")
    A("| Coluna | O que registrar |")
    A("| :--- | :--- |")
    for c, d in COLS:
        A(f"| `{c}` | {d} |")
    A("")
    A("> `indexada` em branco impede o cálculo: sem ela não há denominador. "
      "`recuperada` só se preenche onde `indexada` = sim.\n")
    return "\n".join(L) + "\n"


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
                "n": e["n"],
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
    facetas, sementes, estudos = carrega()
    SAIDA.mkdir(parents=True, exist_ok=True)

    (SAIDA / "Conjunto_Semente.md").write_text(md(facetas, sementes, estudos),
                                              encoding="utf-8")

    linhas = csv_out(estudos)
    with (SAIDA / "semente_aderencia.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[c for c, _ in COLS])
        w.writeheader()
        w.writerows(linhas)

    print(f"Conjunto_Semente.md     {len(estudos)} sementes")
    print(f"semente_aderencia.csv   {len(linhas)} linhas, {len(COLS)} colunas")
    com_entrada = sum(1 for e in estudos if e["_meta"])
    confirmadas = sum(1 for e in estudos
                      if str(e.get("verificacao", "")).startswith("CONFIRMADA"))
    alinhadas = sum(1 for e in estudos
                    if e.get("alinhamento")
                    and not str(e["alinhamento"]).startswith(("A CONFERIR", "a conferir")))
    print(f"metadados: {com_entrada}/{len(estudos)} com entrada em sementes.json; "
          f"{confirmadas} com verificação confirmada; {alinhadas} com alinhamento conferido")
    pendentes = _pendentes(estudos)
    if pendentes:
        print("pendências de metadados:")
        for e, campos in pendentes:
            print(f"  {e['n']:>2}. {e['chave']}: {', '.join(campos)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
