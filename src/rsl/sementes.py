"""Instrumento do teste de aderência: a planilha a preencher e o ensaio seco.

Tudo o que a planilha traz de cada semente — referência, bases, papel e os dados de
conferência (verificação, tipo, alinhamento…) — vem do arquivo de sementes
(`[documentos] sementes`), lido por `ctx.protocolo()`. Não há outro arquivo de semente. A
planilha é gravada em `[saidas] aderencia`.

A planilha é artefato misto: as colunas derivadas vêm sempre das sementes e da tabela de
bases; as colunas manuais (`manual` na declaração de `colunas()`) são preenchidas pelo
pesquisador no próprio arquivo e conservadas na regravação. A linha anterior casa com a nova
por `id` e `base`, confirmada pelo título normalizado. Se a regravação perderia conteúdo
manual não vazio — linha sem par, título divergente, coluna fora do esquema —, nada é
gravado e o subcomando sai com REPROVADO.

O ensaio seco — o que cada título entrega às facetas — é impresso no terminal, não
gravado: o instrumento é a planilha. O ensaio não é declaração de faceta: o campo
`facetas` é juízo do pesquisador e não se copia dele.
"""

import collections
import csv
import os
import tempfile

from . import gramatica as G
from .config import relativo
from .dados import campo_pendente
from .erros import DadosInvalidos, Reprovado
from .markdown import normaliza
from .saida import Saida

Coluna = collections.namedtuple("Coluna", "nome descricao manual")

# Colunas manuais citadas por nome fora deste módulo (texto de `aderencia medir`).
COL_INDEXADA = "indexada"
COL_RECUPERADA = "recuperada"

# Dialeto único da planilha: o da gravação é o da leitura da planilha anterior.
CODIFICACAO = "utf-8-sig"


def colunas(d):
    """As colunas da planilha, na ordem do arquivo. `manual` marca as que o pesquisador
    preenche: só essas são conservadas na regravação."""
    bases = [b["sigla"] for b in d["bases"]]
    executada = d["executada"]
    derivada = [
        ("id", "identificador da semente (SEn), conforme o conjunto-semente"),
        ("autores_ano", "autoria abreviada e ano"),
        ("titulo", "título, como consta na referência do conjunto-semente"),
        ("tipo", "primário ou secundário — preencher no arquivo de sementes"),
        ("verificacao", "estado de conferência da referência — preencher no arquivo de "
                        "sementes"),
        ("papel", "papel da semente no conjunto: desenvolvimento ou validação — do "
                  "conjunto-semente"),
        ("base", " ou ".join(filter(None, [", ".join(bases[:-1]), bases[-1]]))),
        ("esperada_na_base", "sim se o conjunto-semente cita esta base para a semente"),
    ]
    manual = [
        (COL_INDEXADA, "etapa 1: sim ou não, por busca de título. **obrigatório**"),
        ("data_etapa1", "data da busca de título"),
        (COL_RECUPERADA, f"etapa 2: sim ou não, por busca na exportação de {executada}"),
        ("como_localizada", "DOI, título ou não localizada"),
        ("data_etapa2", "data da conferência na exportação"),
        ("observacao", "o que explica o não: termo ausente, campo não indexado, recorte"),
    ]
    return ([Coluna(n, t, False) for n, t in derivada]
            + [Coluna(n, t, True) for n, t in manual])


def manuais(d):
    """Nomes das colunas manuais, na ordem da planilha."""
    return [c.nome for c in colunas(d) if c.manual]


def carrega(ctx, d):
    """Termos de cada faceta e as sementes lidas, com a marca de conferência preenchida."""
    facetas = {"facetas": [{"faceta": fid, "termos": v["termos"]}
                           for fid, v in d["strings"].items()]}
    conferencia = [c.chave for c in G.CONFERENCIA]
    estudos = []
    for ref in d["sementes"]:
        e = dict(ref)
        e["_meta"] = any(str(e.get(c) or "").strip() for c in conferencia)
        estudos.append(e)
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
    rotulo = {"verificacao": "verificação", "tipo": "tipo", "alinhamento": "alinhamento"}
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
                "autores_ano": f"{e['autores'][0].split(',')[0].strip()} et al. {e['ano']}",
                "titulo": e["titulo"],
                "tipo": e.get("tipo", ""),
                "verificacao": e.get("verificacao", ""),
                "papel": e["papel"],
                "base": b,
                "esperada_na_base": "sim" if b in e["bases"] else "nao",
                **{c: "" for c in manuais(d)},
            })
    return linhas


def le_anterior(destino):
    """(cabeçalho, linhas) da planilha anterior, lida no dialeto da gravação; None se não
    existe. Arquivo que não se lê como a planilha levanta DadosInvalidos."""
    if not destino.exists():
        return None
    nome = relativo(destino)
    try:
        with destino.open(encoding=CODIFICACAO, newline="") as f:
            leitor = csv.DictReader(f)
            linhas = list(leitor)
            cab = leitor.fieldnames or []
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        raise DadosInvalidos(f"{nome}: planilha anterior ilegível ({e}). Nada foi gravado.")
    faltam = [c for c in ("id", "base", "titulo") if c not in cab]
    if faltam:
        raise DadosInvalidos(f"{nome}: planilha anterior ilegível — o cabeçalho não traz "
                             f"{', '.join(faltam)}. Nada foi gravado.")
    for n, linha in enumerate(linhas, start=2):
        if None in linha:
            raise DadosInvalidos(f"{nome}: planilha anterior ilegível — a linha {n} tem mais "
                                 f"campos que o cabeçalho. Nada foi gravado.")
    return cab, linhas


def preserva(d, linhas, anterior):
    """Copia para `linhas` as colunas manuais da planilha anterior. Devolve o conteúdo
    manual não vazio que ficaria sem destino, como texto por linha anterior; lista vazia
    quando nada se perde."""
    if anterior is None:
        return []
    cab, antigas = anterior
    nomes = {c.nome for c in colunas(d)}
    cols_manuais = manuais(d)
    fora = [c for c in cab if c not in nomes]
    novas = {(l["id"], l["base"]): l for l in linhas}
    usadas, perdas = set(), []
    for a in antigas:
        chave = ((a.get("id") or "").strip(), (a.get("base") or "").strip())
        rotulo = f"{chave[0] or '(sem id)'} × {chave[1] or '(sem base)'}"
        com_valor = [c for c in fora if (a.get(c) or "").strip()]
        if com_valor:
            perdas.append(f"{rotulo}: {', '.join(com_valor)} — coluna fora do esquema")
        preenchidas = [c for c in cols_manuais if (a.get(c) or "").strip()]
        nova = novas.get(chave)
        if nova is not None and chave not in usadas \
                and normaliza(nova["titulo"]) == normaliza(a.get("titulo") or ""):
            usadas.add(chave)
            for c in cols_manuais:
                nova[c] = a.get(c) or ""
            continue
        if not preenchidas:
            continue
        if nova is None:
            motivo = "linha sem par no arquivo de sementes e na tabela de bases"
        elif chave in usadas:
            motivo = "linha repetida na planilha anterior"
        else:
            motivo = (f"título divergente — na planilha: «{a.get('titulo') or ''}»; "
                      f"no arquivo de sementes: «{nova['titulo']}»")
        perdas.append(f"{rotulo}: {', '.join(preenchidas)} — {motivo}")
    return perdas


def _modo(destino):
    """Permissão do arquivo anterior; sem ele, a de um arquivo novo sob a umask."""
    if destino.exists():
        return destino.stat().st_mode & 0o777
    umask = os.umask(0)
    os.umask(umask)
    return 0o666 & ~umask


def grava(destino, cols, linhas):
    """Grava num temporário do mesmo diretório e só então substitui o anterior."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=destino.parent, prefix=f".{destino.name}.",
                               suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=CODIFICACAO, newline="") as f:
            w = csv.DictWriter(f, fieldnames=[c.nome for c in cols])
            w.writeheader()
            w.writerows(linhas)
        os.chmod(tmp, _modo(destino))
        os.replace(tmp, destino)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def cmd_planilha(ctx, a=None):
    d = ctx.protocolo()
    facetas, estudos = carrega(ctx, d)
    cols = colunas(d)
    linhas = linhas_planilha(d, estudos)
    destino = ctx.config.saida("aderencia")
    perdas = preserva(d, linhas, le_anterior(destino))
    if perdas:
        raise Reprovado(
            f"{relativo(destino)}: a regravação perderia preenchimento manual — nada foi "
            f"gravado, e o arquivo anterior está intacto.\n"
            + "\n".join(f"  {p}" for p in perdas)
            + "\nTransferir à mão o preenchimento para a linha certa (semente renumerada) ou "
              "esvaziá-lo (semente ou base retirada, coluna acrescentada), e regravar.")
    grava(destino, cols, linhas)

    print(f"{destino.name}   {len(linhas)} linhas, {len(cols)} colunas")
    com_entrada = sum(1 for e in estudos if e["_meta"])
    confirmadas = sum(1 for e in estudos
                      if str(e.get("verificacao", "")).startswith("CONFIRMADA"))
    alinhadas = sum(1 for e in estudos
                    if e.get("alinhamento")
                    and not str(e["alinhamento"]).startswith(("A CONFERIR", "a conferir")))
    print(f"conferência: {com_entrada}/{len(estudos)} com campo de conferência preenchido; "
          f"{confirmadas} com verificação confirmada; {alinhadas} com alinhamento conferido")
    pendentes = _pendentes(estudos)
    if pendentes:
        print("pendências de conferência:")
        for e, campos in pendentes:
            print(f"  {e['id']:>4}. {e['chave']}: {', '.join(campos)}")
    relata_ensaio(d, estudos, facetas)
    return Saida.OK
