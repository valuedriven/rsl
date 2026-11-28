"""Consultas registradas: leitura do registro de execuções, coleta das exportações,
deduplicação e recorte temporal."""

import hashlib
import json
import pathlib
import re

from ..config import RAIZ, relativo
from ..dados import CMD_REGISTRAR
from ..erros import DadosInvalidos
from ..markdown import normaliza
from .leitores import le_arquivo

STATUS_VALIDOS = ("valida", "divergente_justificada")
ESTADOS_EXCLUIDOS = ("vencido", "nao executado")


# Indicação de quem obtém a exportação do cache. O comando de obtenção ainda não existe; a
# indicação passa a nomeá-lo quando existir.
OBTER_DO_ZOTERO = "obter a exportação do Zotero (coleção da execução)"


def exportacao(cfg, c):
    """O ponto único de resolução da exportação de uma execução, sem consultar o Zotero.

    `c` é a execução do registro, com a sigla da base em `base`. Com `identificador`, a
    exportação é a do cache: `<[dados] execucoes>/<sigla>/<identificador>.ris`. Sem ele, é o
    caminho declarado em `arquivo`, relativo à raiz (absoluto vale como está)."""
    ident = str(c.get("identificador") or "").strip()
    if ident:
        return cfg.caminho("dados.execucoes") / str(c.get("base") or "") / f"{ident}.ris"
    p = pathlib.Path(str(c.get("arquivo") or "").strip())
    return p if p.is_absolute() else RAIZ / p


def falta_exportacao(c, caminho, execucao):
    """A mensagem da exportação ausente no disco, nomeando a execução e o que a obtém."""
    if str(c.get("identificador") or "").strip():
        return (f"execução {execucao}: exportação {relativo(caminho)} ausente no cache — "
                f"{OBTER_DO_ZOTERO}")
    return f"execução {execucao}: arquivo ausente {c.get('arquivo')}"


def exige_exportacao(c):
    """O caminho resolvido da consulta, ou DADOS quando ausente no disco."""
    caminho = c["exportacao"]
    if not caminho.exists():
        raise DadosInvalidos(f"consulta {c.get('id')}: "
                             + falta_exportacao(c, caminho, c.get("execucao")))
    return caminho


def consultas_do_registro(b, dado):
    """Execuções com exportação declarada, lidas do registro documental por base."""
    consultas = []
    for bd, base in (dado.get("bases") or {}).items():
        if not isinstance(base, dict):
            continue
        nome = b.sigla_de_bd.get(bd, base.get("base") or bd)
        for e in base.get("execucoes") or []:
            arq = str(e.get("arquivo") or "").strip()
            ident = str(e.get("identificador") or "").strip()
            if not arq and not ident:
                continue
            if normaliza(e.get("estado")) in ESTADOS_EXCLUIDOS:
                continue
            status = e.get("status") or "valida"
            if status not in STATUS_VALIDOS:
                continue
            consultas.append({
                "id": f"{nome}-{e.get('expressao')}-{ident or pathlib.Path(arq).stem}",
                "execucao": f"{bd}/{e.get('id') or '?'}",
                "base": nome,
                "expressao": e.get("expressao"),
                "data_hora": e.get("data_hora") or e.get("data") or "",
                "retorno_declarado": e.get("retorno"),
                "registros_lidos": e.get("registros_lidos"),
                "arquivo": arq,
                "identificador": ident,
                "exportacao": exportacao(b.config, {**e, "base": nome}),
                "status": status,
                "justificativa_divergencia": e.get("justificativa_divergencia", ""),
                "texto": str(e.get("texto") or ""),
            })
    return consultas


def le_registro(b):
    """O registro de execuções, ou DadosInvalidos nomeando o arquivo."""
    onde = relativo(b.registro)
    if not b.registro.exists():
        raise DadosInvalidos(f"{onde} não encontrado: registre cada execução com  "
                             f"{CMD_REGISTRAR}  antes de derivar")
    try:
        return json.loads(b.registro.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise DadosInvalidos(f"{onde} ilegível: {e}") from None


def carrega_consultas(b, exigir=True):
    dado = le_registro(b)
    validas = [c for c in consultas_do_registro(b, dado) if c.get("status") in STATUS_VALIDOS]
    if exigir and not validas:
        raise DadosInvalidos(
            f"nenhuma execução com exportação registrada em {relativo(b.registro)}.\n"
            f"  Registre a execução primeiro:\n"
            f"  {CMD_REGISTRAR} <base> <expressao> <arquivo> --retorno <n>")
    return dado, validas


MOTIVO_SONDA = "sonda"
MOTIVO_CONFERENCIA = "execução direta de conferência"


def selecao_do_corpus(b, validas):
    """(lidas, deixadas de fora): o corpus é só a expressão executada.

    A sonda fica fora do corpus pelo protocolo, e as execuções diretas das expressões de
    conferência são subconjuntos da executada: lidas, inflariam as contagens brutas e a
    coluna `duplicata_de` sem acrescentar registro. Cada deixada de fora leva o motivo."""
    lidas, fora = [], []
    for c in validas:
        if c.get("expressao") == b.executada:
            lidas.append(c)
        else:
            motivo = MOTIVO_SONDA if c.get("expressao") == b.sonda else MOTIVO_CONFERENCIA
            fora.append((c, motivo))
    return lidas, fora


def consultas_do_corpus(b):
    """As consultas da executada, com o relato das lidas e das deixadas de fora; DADOS se
    nenhuma execução da executada está registrada."""
    _, validas = carrega_consultas(b)
    lidas, fora = selecao_do_corpus(b, validas)
    print(f"Execuções lidas (expressão executada, {b.executada}):")
    for c in lidas:
        print(f"  {c['execucao']}  {c['base']} {c['expressao']}")
    if fora:
        print("Execuções registradas deixadas de fora do corpus:")
        for c, motivo in fora:
            print(f"  {c['execucao']}  {c['base']} {c['expressao']} — {motivo}")
    if not lidas:
        raise DadosInvalidos(
            f"nenhuma execução de {b.executada} (a executada) registrada em "
            f"{relativo(b.registro)}: o corpus é só a executada.\n"
            f"  {CMD_REGISTRAR} <base> {b.executada} <arquivo> --retorno <n>")
    return lidas


def coleta(consultas):
    """Lê as exportações registradas e reconfere a contagem de cada uma."""
    tudo = []
    for c in consultas:
        caminho = exige_exportacao(c)
        regs = le_arquivo(caminho)
        if len(regs) != int(c.get("registros_lidos", -1)):
            raise DadosInvalidos(
                f"consulta {c.get('id')}: o arquivo tem {len(regs)} registros e o registro "
                f"diz {c.get('registros_lidos')}. Arquivo trocado ou reexportado: "
                f"reregistre antes de derivar.")
        for r in regs:
            r["base"] = c.get("base", "?")
            r["arquivo_origem"] = caminho.name
            r["consulta"] = c.get("id", "")
        print(f"  {c.get('id')}: {len(regs)} registros")
        tudo += regs
    return tudo


def chave_dedup(reg):
    d = (reg.get("doi") or "").strip().lower()
    return "doi:" + d if d else "ti:" + normaliza(reg.get("titulo"))[:120]


# Hexadecimais do SHA-256 que formam o identificador da execução (48 bits).
TAMANHO_IDENTIFICADOR = 12


def identificador_execucao(sigla, expressao, data_hora, registros):
    """O identificador de uma execução, calculado (D4): os primeiros hexadecimais do SHA-256
    da sigla da base, do identificador da expressão, da data e hora da execução e da lista
    ordenada das chaves de deduplicação dos registros, com as repetições. Indiferente à ordem
    dos registros; diferente com um registro a mais ou com outra data e hora."""
    objeto = json.dumps([sigla, expressao, data_hora, sorted(chave_dedup(r) for r in registros)],
                        ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(objeto.encode("utf-8")).hexdigest()[:TAMANHO_IDENTIFICADOR]


def identifica(regs):
    """Dá identificador a cada registro e marca a duplicata, sem apagar nada."""
    for i, r in enumerate(regs, 1):
        r["registro"] = f"R{i:05d}"
        r["duplicata_de"] = ""
    vistos = {}
    for r in regs:
        k = chave_dedup(r)
        if k in vistos:
            r["duplicata_de"] = vistos[k]
        else:
            vistos[k] = r["registro"]
    dup = sum(1 for r in regs if r["duplicata_de"])
    if dup:
        print(f"\nDeduplicação: {dup} registro(s) repetido(s) no mesmo DOI ou título, "
              f"marcados em `duplicata_de`. Nenhum foi apagado.")
    return regs


def exige_registros(regs):
    if not regs:
        raise DadosInvalidos("Nenhum registro lido.")
    return regs


def ano_de(reg):
    """Ano publicado como inteiro; 0 quando não há ano legível no registro."""
    m = re.search(r"(19|20)\d{2}", reg.get("ano") or "")
    return int(m.group(0)) if m else 0


def aplica_recorte(b, regs):
    """Aplica o recorte temporal e devolve (dentro, fora), com relatório."""
    dentro, fora, sem_ano = [], [], []
    for r in regs:
        a = ano_de(r)
        if a == 0:
            r["recorte"] = "ano ausente"
            sem_ano.append(r)
        elif b.ano_min <= a <= b.ano_max:
            r["recorte"] = "dentro"
            dentro.append(r)
        else:
            r["recorte"] = "fora"
            fora.append(r)
    print(f"\nRecorte temporal {b.ano_min}-{b.ano_max} (conferência):")
    print(f"  dentro ......... {len(dentro)}")
    print(f"  fora ........... {len(fora)}  (retirados)")
    print(f"  ano ausente .... {len(sem_ano)}  (MANTIDOS e marcados: decidir um a um "
          f"na 1ª filtragem)")
    if fora:
        bases = sorted({r.get("base", "?") for r in fora})
        print(f"  bases de origem dos retirados: {', '.join(bases)}")
        print("  O recorte é aplicado na busca em todas as bases — na consulta ou no filtro")
        print("  da página, como o procedimento de busca de cada base declara. Esta linha "
              "deveria ser zero:")
        print("  registro fora da janela")
        print("  indica divergência entre o declarado e o devolvido. Investigar antes de")
        print("  prosseguir, e não apenas registrar.")
    print("  Registrar os três números nas contagens da busca.")
    return dentro + sem_ano, fora
