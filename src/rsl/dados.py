"""Arquivos alimentados: conferência contra o protocolo e relato de pendências.

Nada aqui é derivado de Markdown. São arquivos que se alimentam (`[dados]` do
config.toml): o registro documental das execuções e a evidência bruta. O que o protocolo
ou o arquivo de sementes (`[documentos] sementes`) já dizem não se copia para JSON —
lê-se do documento, por `ctx.protocolo()`.

Arquivo ausente ou ilegível sai com o código DADOS; conteúdo incoerente com o protocolo,
com REPROVADO; procedimento de busca fora da gramática, com PROTOCOLO_ILEGIVEL, só na sua base.
"""

import csv
import json
import pathlib
import re

from . import gramatica as G
from .config import RAIZ, relativo
from .coerencia import Problema, Resultado, imprime_problemas, problemas_bases
from .erros import DadosInvalidos, ProtocoloInvalido
from .derivado import base_derivada
from .fonte import le_fonte
from .markdown import normaliza
from .saida import Saida

CMD_PENDENCIAS = "python3 -m rsl projeto pendencias"
CMD_REGISTRAR = "python3 -m rsl busca registrar"
CMD_EXPORTAR = "python3 -m rsl termos exportar"
CMD_VALIDAR = "python3 -m rsl termos validar"
STATUS_EXECUCAO = ("valida", "divergente_justificada")
# Subpasta de `[dados] evidencia` com a evidência bruta das referências das sementes,
# nomeada `SEn_…`; só ela é conferida contra o arquivo de sementes (D6).
SUBPASTA_REFERENCIAS = "referencias"


def le_json(caminho):
    """Carrega um JSON alimentado. Devolve (dado, erro); erro None quando legível."""
    caminho = pathlib.Path(caminho)
    if not caminho.exists():
        return None, f"{relativo(caminho)} ausente"
    try:
        return json.loads(caminho.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"{relativo(caminho)} ilegível: {e}"


def exige_json(caminho):
    """O JSON alimentado, ou DadosInvalidos nomeando o arquivo."""
    dado, erro = le_json(caminho)
    if erro:
        raise DadosInvalidos(erro)
    return dado


def problemas_registro(ctx, dado, bds):
    """Confere o registro documental e as execuções que declaram arquivo exportado.

    `bds` são os identificadores da tabela de bases do protocolo.
    """
    nome = ctx.config.caminho("dados.registro").name
    if not isinstance(dado, dict):
        return [f"{nome} não é um objeto"]
    bases = dado.get("bases")
    if not isinstance(bases, dict):
        return [f"{nome} sem a chave `bases`"]
    faltam = [b for b in bds if b not in bases]
    if faltam:
        return [f"{nome} sem as bases {faltam}"]

    problemas = []
    for bd in bds:
        base = bases[bd]
        execucoes = base.get("execucoes", [] if "sondagens" in base else None)
        if not isinstance(execucoes, list):
            problemas.append(f"{nome}: {bd} sem a lista `execucoes`")
            continue
        ids = [e.get("id") for e in execucoes if isinstance(e, dict)]
        repetidos = sorted({x for x in ids if ids.count(x) > 1})
        if repetidos:
            problemas.append(f"{nome}: {bd} com execuções repetidas {repetidos}")
        for e in execucoes:
            if not isinstance(e, dict):
                problemas.append(f"{nome}: {bd} com execução que não é objeto")
                continue
            arq = str(e.get("arquivo") or "").strip()
            if not arq:
                continue
            caminho = pathlib.Path(arq)
            if not caminho.is_absolute():
                caminho = RAIZ / caminho
            if not caminho.exists():
                problemas.append(f"{nome}: {bd}/{e.get('id')} aponta arquivo ausente "
                                 f"{arq!r}")
            if not isinstance(e.get("registros_lidos"), int):
                problemas.append(f"{nome}: {bd}/{e.get('id')} declara arquivo sem "
                                 f"`registros_lidos` inteiro")
            status = e.get("status")
            if status and status not in STATUS_EXECUCAO:
                problemas.append(f"{nome}: {bd}/{e.get('id')} com status {status!r} "
                                 f"desconhecido")
    return problemas


def _ids_do_registro(registro):
    """{BDn: ids de `execucoes` e de `sondagens`} do registro de execução."""
    ids = {}
    if isinstance(registro, dict) and isinstance(registro.get("bases"), dict):
        for bd, base in registro["bases"].items():
            if not isinstance(base, dict):
                continue
            for chave in ("execucoes", "sondagens"):
                if isinstance(base.get(chave), list):
                    ids.setdefault(bd, set()).update(
                        e.get("id") for e in base[chave] if isinstance(e, dict))
    return ids


def _textos_da_fonte(ctx, d, sigla):
    """[(onde, texto)] de toda a fonte da base: cada campo de texto de `procedimento.toml`
    e cada linha dos fragmentos."""
    fonte = le_fonte(ctx, d, sigla)
    saida = []

    def percorre(valor, caminho):
        if isinstance(valor, str):
            saida.append((caminho, valor))
        elif isinstance(valor, list):
            for i, x in enumerate(valor, 1):
                percorre(x, f"{caminho}[{i}]")
        elif isinstance(valor, dict):
            for k, v in valor.items():
                percorre(v, f"{caminho}.{k}" if caminho else k)
    percorre(fonte["dado"], "")
    for nome, texto in sorted(fonte["fragmentos"].items()):
        for n, linha in enumerate(texto.splitlines(), 1):
            saida.append((f"{nome}:{n}", linha))
    return fonte, saida


def problemas_citacoes_registro(ctx, d, registro):
    """Citação do registro de execução sem lastro, por base, em toda a fonte.

    Toda menção ao caminho do registro nomeia a execução ou a sondagem na forma
    `BDn/<id>`, com `BDn` da própria base e o id presente em `execucoes` ou em `sondagens`;
    toda citação tem esse lastro. Sem o registro, a citação já é sem lastro. As fontes vêm
    do contexto, que pode trazer cópias alteradas (autoteste).
    """
    caminho = str(ctx.config.valor("dados.registro"))
    ids = _ids_do_registro(registro)
    problemas = []
    for b in d["bases"]:
        sigla, bd = b["sigla"], b["id"]
        try:
            fonte, textos = _textos_da_fonte(ctx, d, sigla)
        except ProtocoloInvalido as e:
            problemas.append(Problema(f"{sigla}: {e}", e.codigo))
            continue
        for onde, texto in textos:
            citacoes = G.F_CITACAO.padrao.findall(texto)
            if caminho not in texto and not citacoes:
                continue
            where = f"{sigla}: fonte {fonte['pasta']} ({onde})"
            if not citacoes:
                problemas.append(f"{where}: menção ao registro sem identificador "
                                 f"`BDn/<id>`")
                continue
            for cit_bd, ident in citacoes:
                ref = f"{cit_bd}/{ident}"
                if cit_bd != bd:
                    problemas.append(f"{where}: cita {ref}, de outra base; a citação tem de "
                                     f"ser de {bd}")
                elif ident not in ids.get(bd, set()):
                    if registro is None:
                        problemas.append(f"{where}: cita {ref} sem lastro — registro de "
                                         f"execução ausente")
                    else:
                        problemas.append(f"{where}: cita {ref}, inexistente em `execucoes` e "
                                         f"em `sondagens` do registro")
    return [p if isinstance(p, Problema) else Problema(p) for p in problemas]


def problemas_sondagens_registradas(ctx, d, registro):
    """(problemas, relatos) dos resultados de `bases.BDn.sondagens`: campos, id único,
    sondagem existente na fonte, leitura declarada; e o resultado ainda não levado à
    fonte (relato)."""
    problemas, relatos = [], []
    if not isinstance(registro, dict) or not isinstance(registro.get("bases"), dict):
        return problemas, relatos
    exigidos = [c.chave for c in G.T_RES_SONDAGEM.campos if c.exigido]
    for b in d["bases"]:
        sigla, bd = b["sigla"], b["id"]
        lista = (registro["bases"].get(bd) or {}).get("sondagens")
        if lista is None:
            continue
        if not isinstance(lista, list):
            problemas.append(f"{sigla}: `bases.{bd}.sondagens` não é lista")
            continue
        try:
            fonte = le_fonte(ctx, d, sigla)
        except ProtocoloInvalido:
            continue                      # a base já reprova pela leitura
        situacao = {s["elemento"]: s for s in fonte["dado"]["sintaxe"]}
        situacao.update({r["texto"]: r for r in fonte["dado"].get("regras_de_montagem", [])})
        vistos = set()
        for r in lista:
            if not isinstance(r, dict):
                problemas.append(f"{sigla}: resultado de sondagem que não é objeto")
                continue
            rid = r.get("id")
            faltam = [c for c in exigidos if c not in r]
            if faltam:
                problemas.append(f"{sigla}: sondagem registrada {rid!r} sem {faltam}")
                continue
            if rid in vistos:
                problemas.append(f"{sigla}: sondagem registrada {rid!r} repetida em {bd}")
            vistos.add(rid)
            sd = fonte["sondagens"].get(r["sondagem"])
            if sd is None:
                problemas.append(f"{sigla}: resultado {rid!r} da sondagem {r['sondagem']!r}, "
                                 f"que não existe na fonte")
                continue
            leitura = r["leitura"] if isinstance(r["leitura"], dict) else {}
            k = leitura.get("numero")
            if not isinstance(k, int) or not 1 <= k <= len(sd["leituras"]):
                problemas.append(f"{sigla}: resultado {rid!r}: leitura {k!r} não é nenhuma "
                                 f"das {len(sd['leituras'])} declaradas em {r['sondagem']}")
                continue
            estado = sd["leituras"][k - 1]["estado"]
            for el in sd["elementos"]:
                item = situacao.get(el)
                cit = f"{bd}/{rid}"
                if item and (item["situacao"] != estado or (
                        estado == G.SITUACAO_MEDICAO and item.get("citacao") != cit)):
                    relatos.append(f"{sigla}: resultado {cit} ({r['sondagem']}, leitura {k}) "
                                   f"ainda não levado à fonte — {el!r}: situacao = "
                                   f"{estado!r}" + (f", citacao = {cit!r}"
                                                    if estado == G.SITUACAO_MEDICAO else ""))
    return problemas, relatos


def problemas_evidencia(d, pasta):
    """Evidência bruta de semente que não está no arquivo de sementes (D6).

    Todo arquivo sob `pasta/referencias/` (`pasta` é `[dados] evidencia`) cujo nome comece
    por `SEn_` pertence à semente `SEn`. Se o `id` não está no arquivo de sementes, a
    semente foi retirada (ou renumerada) e a evidência ficou: reprova, nomeando o arquivo.
    As outras subpastas da evidência não são conferidas. Não confere se a evidência de um
    `id` existente é mesmo daquela semente.
    """
    pasta = pathlib.Path(pasta) / SUBPASTA_REFERENCIAS
    if not pasta.is_dir():
        return []
    ids = {e["id"] for e in d["sementes"]}
    padrao = re.compile(rf"({G.I_SE.padrao.pattern})_")
    problemas = []
    for arq in sorted(x for x in pasta.rglob("*") if x.is_file()):
        m = padrao.match(arq.name)
        if m and m.group(1) not in ids:
            problemas.append(f"evidência {relativo(arq)} é da semente {m.group(1)}, que não "
                             f"está no arquivo de sementes — remover a evidência da semente "
                             f"retirada, ou renomeá-la para o id novo (renumeração)")
    return problemas


def conferir_dados(ctx):
    """Confere os arquivos alimentados contra o documento. Devolve (Resultado, avisos)."""
    d = ctx.protocolo()
    problemas, avisos = Resultado(), []

    registro, erro = le_json(ctx.config.caminho("dados.registro"))
    if erro:
        problemas.append(Problema(erro, Saida.DADOS))
    else:
        problemas += [Problema(x) for x in problemas_registro(
            ctx, registro, [b["id"] for b in d["bases"]])]

    problemas += [Problema(x) for x in problemas_evidencia(
        d, ctx.config.caminho("dados.evidencia"))]
    problemas += problemas_bases(ctx, d, igualdade=False)
    problemas += problemas_citacoes_registro(ctx, d, registro)
    sond, relatos = problemas_sondagens_registradas(ctx, d, registro)
    problemas += [Problema(x) for x in sond]
    avisos += relatos
    return problemas, avisos


def cmd_conferir_dados(ctx, a=None):
    problemas, avisos = conferir_dados(ctx)
    for v in avisos:
        print("AVISO:", v)
    if problemas:
        imprime_problemas(problemas)
        return problemas.codigo
    pasta = relativo(ctx.config.caminho("dados.registro").parent)
    print(f"Arquivos alimentados de {pasta}/ na forma esperada.")
    return Saida.OK


# ---------------------------------------------------------------------- pendências
# Campos de conferência cujo valor vazio é juízo ou conferência ainda não feitos.
CAMPOS_PENDENTES = ((G.C_VERIFICACAO.chave, "verificação"), (G.C_TIPO.chave, "tipo"),
                    (G.C_ALINHAMENTO.chave, "alinhamento"))


def campo_pendente(valor):
    v = str(valor or "")
    return not v or v.startswith(("A CONFERIR", "a conferir")) or "PENDÊNCIA" in v


def pendencias_sementes(d):
    """Dado ainda não obtido e juízo ainda não feito, por semente, sem reprovar (D4).

    DOI ausente; facetas a informar; semente de validação cujas facetas não incluem
    nenhuma âncora (a regra está em aberto: só se relata); campo de conferência vazio.
    Com `facetas` vazia, relata-se só "facetas a informar": a falta de âncora é
    consequência dela, não segundo juízo pendente.
    """
    ancoras_ = set(d["ancoras"])
    linhas = []
    for e in d["sementes"]:
        abertos = []
        if not e[G.C_DOI.chave]:
            abertos.append("DOI ausente")
        if not e[G.C_FACETAS.chave]:
            abertos.append("facetas a informar")
        elif e["papel"] == G.PAPEL_VALIDACAO and not ancoras_ & set(e[G.C_FACETAS.chave]):
            abertos.append(f"validação sem faceta âncora ({', '.join(d['ancoras'])}) — "
                           f"regra a decidir")
        abertos += [rotulo for campo, rotulo in CAMPOS_PENDENTES
                    if campo_pendente(e.get(campo))]
        if abertos:
            linhas.append(f"[semente {e['id']} {e['chave']}] pendente: {', '.join(abertos)}")
    return linhas


def cmd_pendencias(ctx, a=None):
    """Relata o que está aberto, sem escrever arquivo algum."""
    from .termos.planejamento import STATUS_MANUAL                  # noqa: PLC0415
    d = ctx.protocolo()
    linhas = []
    registro_ = ctx.config.caminho("dados.registro")
    validacao = ctx.config.caminho("dados.validacao")

    if not registro_.exists():
        linhas.append(f"[ausente] {relativo(registro_)} — registre a primeira execução com  "
                      f"{CMD_REGISTRAR}")

    linhas += pendencias_sementes(d)

    registro, erro = le_json(registro_)
    if erro is not None:
        linhas.append(erro)
    else:
        bases = registro.get("bases") or {}
        com_arquivo = 0
        for bd in [b["id"] for b in d["bases"]]:
            base = bases.get(bd) or {}
            nome = base.get("base") or bd
            for p in base.get("pendencias") or []:
                linhas.append(f"[{bd} {nome}] {p}")
            for e in base.get("execucoes") or []:
                if not isinstance(e, dict):
                    continue
                if e.get("arquivo"):
                    com_arquivo += 1
                    if e.get("status") not in STATUS_EXECUCAO:
                        linhas.append(
                            f"[{bd} {e.get('id')}] execução registrada com status "
                            f"{e.get('status')!r} — reconferir ou reregistrar")
        if not com_arquivo:
            linhas.append(f"[registro] nenhuma execução com exportação registrada — use  "
                          f"{CMD_REGISTRAR}")

    if not validacao.exists():
        linhas.append(f"[validação] {relativo(validacao)} ausente: nenhum termo tem decisão do "
                      f"ReT, e todo termo do controle terminológico fica em 'Termo livre' "
                      f"até a validação — rode  {CMD_EXPORTAR}")
    else:
        with validacao.open(encoding="utf-8-sig", newline="") as fh:
            linhas_validacao = list(csv.DictReader(fh, delimiter=";"))
        sem_status = sum(1 for r in linhas_validacao
                         if not (r.get("status_proposto") or "").strip())
        if sem_status:
            linhas.append(f"[validação] {sem_status} linha(s) sem `status_proposto` — rode  "
                          f"{CMD_VALIDAR} <sigla>")
        manuais = sum(1 for r in linhas_validacao
                      if (r.get("status_proposto") or "").strip() == STATUS_MANUAL)
        if manuais:
            linhas.append(f"[validação] {manuais} linha(s) {STATUS_MANUAL} — consultar o "
                          f"instrumento e registrar na planilha")

    # Lacuna que o próprio procedimento de busca declara e deixa em aberto. A decisão é do
    # pesquisador: acrescentar o termo à string, com nova execução e novo teste de
    # aderência, ou manter a perda e declará-la no relatório.
    for base in d["bases"]:
        try:
            b = base_derivada(ctx, d, base["sigla"])
        except ProtocoloInvalido as e:
            linhas.append(f"[{base['sigla']}] procedimento de busca ilegível: {e}")
            continue
        pendentes = [e for e in b["declaracao"]["exclusoes"]
                     if G.MOTIVO_PENDENTE in normaliza(e["motivo"])]
        if pendentes:
            linhas.append(
                f"[{b['base']['nome']}] {len(pendentes)} termo(s) declarado(s) como lacuna, "
                f"com decisão pendente: " +
                ", ".join(f"{e['termo']} ({e['faceta']})" for e in pendentes[:6]))
    pasta = relativo(registro_.parent)
    if not linhas:
        print(f"Nenhuma pendência detectada nos artefatos de {pasta}/.")
    else:
        print(f"{len(linhas)} pendência(s) detectada(s) — relato, nada foi escrito:\n")
        for l in linhas:
            print("  " + l)
    return Saida.OK
