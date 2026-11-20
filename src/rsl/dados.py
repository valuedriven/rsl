"""Arquivos alimentados: conferência contra o protocolo, sincronização das sementes e
relato de pendências.

Nada aqui é derivado de Markdown. São arquivos que se alimentam (`[dados]` do
config.toml): os metadados autorais de cada semente e o registro documental das
execuções. O que o protocolo já diz não se copia para JSON — lê-se do documento.

Arquivo ausente ou ilegível sai com o código DADOS; conteúdo incoerente com o protocolo,
com REPROVADO; ficha fora da gramática, com PROTOCOLO_ILEGIVEL, só na sua base.
"""

import csv
import json
import pathlib

from . import gramatica as G
from .config import RAIZ, relativo
from .conferencia import Problema, Resultado, imprime_problemas, problemas_bases
from .erros import DadosInvalidos, ProtocoloInvalido
from .fichas import base_derivada, ficha
from .markdown import normaliza
from .saida import Saida

CMD_SINCRONIZAR = "python3 -m rsl sementes sincronizar"
CMD_PENDENCIAS = "python3 -m rsl pendencias"
CMD_REGISTRAR = "python3 -m rsl busca registrar"
CMD_EXPORTAR = "python3 -m rsl termos exportar"
CMD_VALIDAR = "python3 -m rsl termos validar"
STATUS_EXECUCAO = ("valida", "divergente_justificada")
VERSAO_SEMENTES = 2


def leia_sementes(ctx):
    return ("AUTORAL. Metadados de conferência de cada semente. As referências, o ano, o "
            "DOI, as bases esperadas e a chave de citação vêm do protocolo "
            f"({ctx.caminho_protocolo}). `ligacao` é a ligação com o "
            "protocolo, por DOI ou título — não é conteúdo bibliográfico e não se edita; "
            "`id` é rótulo e pode mudar sem perder o metadado. "
            f"`{CMD_SINCRONIZAR}` casa por DOI ou título e preserva o que foi conferido. "
            f"Semente retirada do protocolo permanece, e `{CMD_PENDENCIAS}` a reporta.")


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


def ligacao_semente(e):
    """Ligação de uma semente com o protocolo: DOI quando houver; senão, título normalizado.

    É a chave que a sincronização usa e que os consumidores devem usar: o `id` é rótulo,
    não identidade, e pode mudar sem que o metadado autoral se perca.
    """
    doi = (e.get("doi") or "").strip().lower()
    return ("doi:" + doi) if doi else ("ti:" + normaliza(e.get("titulo", ""))[:120])


def _indice_sementes(dado):
    return {e.get("id"): e for e in (dado or {}).get("estudos", []) if e.get("id")}


def problemas_sementes(ctx, dado, d):
    problemas, avisos = [], []
    nome = ctx.config.caminho("dados.sementes").name
    if not isinstance(dado, dict) or "estudos" not in dado:
        return [f"{nome} sem a chave `estudos`"], []
    autorais = ctx.config.valor("planilha.campos_autorais")
    idx = _indice_sementes(dado)
    protocolo = {e["id"]: e for e in d["sementes"]}
    for ident, e in protocolo.items():
        meta = idx.get(ident)
        if meta is None:
            problemas.append(f"sementes: {ident} ({ligacao_semente(e)}) sem metadados")
            continue
        if meta.get("ligacao") and meta["ligacao"] != ligacao_semente(e):
            avisos.append(f"sementes: {ident} tem ligação {meta['ligacao']!r} e o protocolo "
                          f"{ligacao_semente(e)!r} — conferir")
        for campo in autorais:
            if campo not in meta:
                problemas.append(f"sementes: {ident} sem o campo {campo!r}")
    for ident in idx:
        if ident not in protocolo:
            avisos.append(f"sementes: {ident} fora do protocolo, metadados preservados — "
                          f"decidir")
    return problemas, avisos


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
        execucoes = base.get("execucoes")
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


def problemas_citacoes_registro(ctx, d, registro):
    """Citação do registro de execução sem lastro, por base.

    Toda menção ao caminho do registro — em tabela ou em prosa — nomeia a execução na forma
    da gramática, com `BDn` da própria base e o id presente no registro. Menção sem
    identificador, identificador de outra base ou execução inexistente reprova só a base da
    ficha. Sem o registro, a menção já é citação sem lastro. As fichas vêm do contexto,
    que pode trazer cópias alteradas (autoteste).
    """
    caminho = str(ctx.config.valor("dados.registro"))
    execucoes = {}
    if isinstance(registro, dict) and isinstance(registro.get("bases"), dict):
        for bd, base in registro["bases"].items():
            if isinstance(base, dict) and isinstance(base.get("execucoes"), list):
                execucoes[bd] = {e.get("id") for e in base["execucoes"]
                                 if isinstance(e, dict)}
    problemas = []
    for b in d["bases"]:
        sigla, bd = b["sigla"], b["id"]
        try:
            t = ficha(ctx, d, sigla)
        except ProtocoloInvalido as e:
            problemas.append(Problema(f"{sigla}: {e}", e.codigo))
            continue
        for n, linha in enumerate(t.splitlines(), 1):
            if caminho not in linha:
                continue
            citacoes = G.F_CITACAO.padrao.findall(linha)
            where = f"{sigla}: ficha {b['ficha']}:{n}"
            if not citacoes:
                problemas.append(f"{where}: menção ao registro sem identificador de execução "
                                 f"`{G.F_CITACAO.texto.split()[0]}`")
                continue
            for cit_bd, ident in citacoes:
                ref = f"{cit_bd}/{ident}"
                if cit_bd != bd:
                    problemas.append(f"{where}: cita a execução {ref}, de outra base; a "
                                     f"execução tem de ser de {bd}")
                elif ident not in execucoes.get(bd, set()):
                    if registro is None:
                        problemas.append(f"{where}: cita a execução {ref} sem lastro — "
                                         f"registro de execução ausente")
                    else:
                        problemas.append(f"{where}: cita a execução {ref}, inexistente no "
                                         f"registro")
    return [p if isinstance(p, Problema) else Problema(p) for p in problemas]


def conferir_dados(ctx):
    """Confere os arquivos alimentados contra o documento. Devolve (Resultado, avisos)."""
    d = ctx.protocolo()
    problemas, avisos = Resultado(), []

    dado, erro = le_json(ctx.config.caminho("dados.sementes"))
    if erro:
        problemas.append(Problema(f"{erro} — rode  {CMD_SINCRONIZAR}", Saida.DADOS))
    else:
        p, a = problemas_sementes(ctx, dado, d)
        problemas += [Problema(x) for x in p]
        avisos += a

    registro, erro = le_json(ctx.config.caminho("dados.registro"))
    if erro:
        problemas.append(Problema(erro, Saida.DADOS))
    else:
        problemas += [Problema(x) for x in problemas_registro(
            ctx, registro, [b["id"] for b in d["bases"]])]

    problemas += problemas_bases(ctx, d)
    problemas += problemas_citacoes_registro(ctx, d, registro)
    return problemas, avisos


def cmd_conferir_dados(ctx, a=None):
    problemas, avisos = conferir_dados(ctx)
    for v in avisos:
        print("AVISO:", v)
    if problemas:
        imprime_problemas(problemas)
        return problemas.codigo
    pasta = relativo(ctx.config.caminho("dados.sementes").parent)
    print(f"Arquivos alimentados de {pasta}/ na forma esperada.")
    return Saida.OK


# ------------------------------------------------------------------- sincronização
def sincroniza_sementes(ctx, d, existente):
    """Casa por DOI ou título, com o id como último recurso; preserva o conferido."""
    autorais = ctx.config.valor("planilha.campos_autorais")
    antigos = (existente or {}).get("estudos", [])
    por_ligacao = {}
    for e in antigos:
        por_ligacao.setdefault(e.get("ligacao"), []).append(e)
    usados, estudos, novos, religados = set(), [], [], []
    for e in d["sementes"]:
        ligacao = ligacao_semente(e)
        escolhido = None
        for cand in por_ligacao.get(ligacao, []):
            if id(cand) not in usados:
                escolhido = cand
                break
        if escolhido is None:
            for cand in antigos:
                if id(cand) in usados or cand.get("id") != e["id"]:
                    continue
                escolhido = cand
                religados.append(f"{e['id']}: ligação atualizada de "
                                 f"{cand.get('ligacao')!r} para {ligacao!r}")
                break
        if escolhido is None:
            meta = {"id": e["id"], "ligacao": ligacao}
            meta.update({campo: "" for campo in autorais})
            novos.append(e["id"])
            estudos.append(meta)
            continue
        usados.add(id(escolhido))
        meta = {"id": e["id"], "ligacao": ligacao}
        for campo in autorais:
            meta[campo] = escolhido.get(campo, "")
        estudos.append(meta)
    orfaos = [x for x in antigos if id(x) not in usados]
    return ({"_leia": leia_sementes(ctx), "versao": VERSAO_SEMENTES, "estudos": estudos},
            novos, religados, orfaos)


def _escreve(caminho, dado):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")


def cmd_sincronizar(ctx, a=None):
    """Reconcilia o arquivo de sementes com o protocolo. Não cria nem grava derivado."""
    from .conferencia import conferir                               # noqa: PLC0415
    problemas = conferir(ctx)
    if problemas:
        print("Documento fora da forma esperada; nada foi sincronizado:")
        for p in problemas:
            print("  -", p)
        return problemas.codigo
    d = ctx.protocolo()
    caminho = ctx.config.caminho("dados.sementes")
    nome = caminho.name

    sem, erro = le_json(caminho)
    if erro and caminho.exists():
        raise DadosInvalidos(erro)
    dados_s, novos_s, religados, orfaos = sincroniza_sementes(ctx, d, sem or {})

    if sem == dados_s:
        print(f"  {nome}: sem mudança")
        mudou = False
    else:
        _escreve(caminho, dados_s)
        print(f"  {nome}: gravado")
        mudou = True

    if novos_s:
        print(f"\n  semente(s) acrescentada(s): {', '.join(novos_s)}")
    if religados:
        print("\n  ligação de semente refeita:")
        for x in religados:
            print("    ~", x)
    if orfaos:
        print(f"\n  semente(s) fora do protocolo, metadados preservados: "
              f"{', '.join(x.get('id', '?') for x in orfaos)}")
    if not mudou:
        print("\nNada a gravar: o metadado das sementes já reflete o protocolo.")
    return Saida.OK


# ---------------------------------------------------------------------- pendências
CAMPOS_PENDENTES = (("verificacao", "verificação"), ("escopo", "escopo"),
                    ("tipo", "tipo"), ("alinhamento", "alinhamento"))


def campo_pendente(valor):
    v = str(valor or "")
    return not v or v.startswith(("A CONFERIR", "a conferir")) or "PENDÊNCIA" in v


def cmd_pendencias(ctx, a=None):
    """Relata o que está aberto, sem escrever arquivo algum."""
    from .termos.planejamento import STATUS_MANUAL                  # noqa: PLC0415
    d = ctx.protocolo()
    linhas = []
    sementes_ = ctx.config.caminho("dados.sementes")
    registro_ = ctx.config.caminho("dados.registro")
    validacao = ctx.config.caminho("dados.validacao")

    for caminho, acao in ((sementes_, f"rode  {CMD_SINCRONIZAR}"),
                          (registro_, "reconstitua o registro a partir das fichas e do que "
                                      "a base exibiu")):
        if not caminho.exists():
            linhas.append(f"[ausente] {relativo(caminho)} — {acao}")

    s, erro = le_json(sementes_)
    if erro is None:
        protocolo = {e["id"]: e for e in d["sementes"]}
        for ident, meta in _indice_sementes(s).items():
            if ident not in protocolo:
                linhas.append(f"[semente fora do protocolo] {ident} — decidir: remover com "
                              f"registro ou reincluir no protocolo")
                continue
            vazios = [rotulo for campo, rotulo in CAMPOS_PENDENTES
                      if campo_pendente(meta.get(campo))]
            if vazios:
                chave = protocolo[ident]["chave"]
                linhas.append(f"[semente {ident} {chave}] pendente: {', '.join(vazios)}")
        faltam = [e["id"] for e in d["sementes"] if e["id"] not in _indice_sementes(s)]
        if faltam:
            linhas.append(f"[sementes] {len(faltam)} sem metadados: {', '.join(faltam)} — "
                          f"rode  {CMD_SINCRONIZAR}")

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
        linhas.append(f"[validação] {relativo(validacao)} ausente — rode  {CMD_EXPORTAR}")
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

    # Lacuna que a própria ficha declara e deixa em aberto. A decisão é do pesquisador:
    # acrescentar o termo à string, com nova execução e novo teste de aderência, ou manter
    # a perda e declará-la no relatório.
    for base in d["bases"]:
        try:
            b = base_derivada(ctx, d, base["sigla"])
        except ProtocoloInvalido as e:
            linhas.append(f"[{base['sigla']}] ficha ilegível: {e}")
            continue
        pendentes = [e for e in b["declaracao"]["exclusoes"]
                     if G.MOTIVO_PENDENTE in normaliza(e["motivo"])]
        if pendentes:
            linhas.append(
                f"[{b['base']['nome']}] {len(pendentes)} termo(s) declarado(s) como lacuna, "
                f"com decisão pendente: " +
                ", ".join(f"{e['termo']} ({e['faceta']})" for e in pendentes[:6]))
    pasta = relativo(sementes_.parent)
    if not linhas:
        print(f"Nenhuma pendência detectada nos artefatos de {pasta}/.")
    else:
        print(f"{len(linhas)} pendência(s) detectada(s) — relato, nada foi escrito:\n")
        for l in linhas:
            print("  " + l)
    return Saida.OK
