"""Anatomia da perda: por que a base não devolveu cada semente esperada.

A consulta de cada nível é montada da mesma composição que gerou as consultas executadas:
(1) só os DOIs das sementes diagnosticadas; (2) mais as cláusulas de filtro; (3) mais a
sonda sem proximidade; (4) mais a sonda; (5) mais a executada. O nível cuja expressão tem
execução registrada é lido da exportação, filtrado pelos DOIs, e não se submete. A causa de
cada semente é o primeiro nível em que o DOI dela desaparece.

A submissão é manual, no navegador do pesquisador (AGENTS.md §9). Este módulo só monta o
roteiro, lê as exportações que ele trouxer e atribui a causa.
"""

import csv
import datetime
import pathlib
import re

from .. import gramatica as G
from ..config import RAIZ, relativo
from ..erros import DadosInvalidos, Reprovado, Uso
from ..procedimentos import composicao_da_base
from ..saida import Saida
from . import Busca
from .aderencia import casa_sementes
from .leitores import le_arquivo
from .registro import carrega_consultas
from .sensibilidade import registros_da_expressao

CAUSA_NAO_INDEXADA = "não indexada"
CAUSA_FILTRO = "filtro"
CAUSA_ANCORAS = "âncoras"
CAUSA_PROXIMIDADE = "proximidade"
CAUSA_FACETA = "faceta não âncora"
CAUSA_PRESENTE = "presente na executada"
CAUSAS = (CAUSA_NAO_INDEXADA, CAUSA_FILTRO, CAUSA_ANCORAS, CAUSA_PROXIMIDADE, CAUSA_FACETA)


def normaliza_doi(valor):
    """DOI para comparação: caixa baixa, sem o prefixo de URL do DOI."""
    s = str(valor or "").strip().lower()
    return re.sub(r"^https?://(?:dx\.)?doi\.org/", "", s)


def selecao(b, sigla, sementes=None):
    """Sementes perdidas na base: as esperadas que a executada DESTA base não recupera por
    título exato, separadas entre as que têm DOI (diagnosticáveis) e as que não têm.

    O casamento é feito sobre todos os registros da executada na base, e não sobre os
    registros únicos do corpus: no corpus, a semente recuperada só em outra base contaria
    como recuperada aqui, e a cópia desta base, marcada como duplicata, sumiria.
    """
    sementes = b.d["sementes"] if sementes is None else sementes
    esperadas = [s for s in sementes if sigla in s["bases"]]
    _, validas = carrega_consultas(b)
    regs = registros_da_expressao(sigla, b.executada, validas)
    if regs is None:
        raise DadosInvalidos(f"{sigla}: sem execução registrada de {b.executada} (a "
                             f"executada); sem ela não se sabe que sementes a base perdeu")
    recuperadas = {e["id"] for e, exatas, _ in casa_sementes(esperadas, regs) if exatas}
    perdidas = [s for s in esperadas if s["id"] not in recuperadas]
    com_doi = [s for s in perdidas if normaliza_doi(s.get("doi"))]
    sem_doi = [s for s in perdidas if not normaliza_doi(s.get("doi"))]
    return {"esperadas": esperadas, "recuperadas": sorted(recuperadas),
            "diagnosticaveis": com_doi, "sem_doi": sem_doi}


def filtros_de_interface(fonte):
    """Critérios de destino `interface`: o filtro a aplicar na página, com o rótulo."""
    return [{"rotulo": c["rotulo"], "como": c.get("como", "")}
            for c in fonte["dado"]["criterios"] if c["destino"] == "interface"]


def monta_niveis(b, sigla, sementes):
    """(fonte, composição, níveis) do diagnóstico, na ordem cumulativa.

    Cada nível é {nivel, texto, expressao, rotulo}: `expressao` é o identificador da
    expressão cuja execução registrada pode ser lida, ou None quando o nível se submete.
    Base sem `[composicao] doi` ou com a sonda/executada particionada reprova.
    """
    fonte, comp = composicao_da_base(b.ctx, b.d, sigla)
    modelo = fonte.get("doi")
    if not modelo:
        raise Reprovado(f"{sigla}: a fonte não declara `[composicao] doi`; sem o modelo da "
                        f"restrição a um DOI a perda não se diagnostica "
                        f"(`{fonte['pasta']}/procedimento.toml`)")
    dois = "(" + " OR ".join(modelo.replace(G.MARCADOR_DOI, str(s["doi"]).strip())
                             for s in sementes) + ")"
    niveis = [{"nivel": 1, "texto": dois, "expressao": None, "rotulo": "só os DOIs"}]

    filtros = list(comp.clausulas)
    texto2 = dois + ("" if not filtros else " AND " + " AND ".join(filtros))
    niveis.append({"nivel": 2, "texto": texto2, "expressao": None,
                   "rotulo": "mais as cláusulas de filtro"})

    sonda = comp.texto_da_expressao(b.sonda)
    executada = comp.texto_da_expressao(b.executada)
    if fonte["proximidade"] is not None:
        sem = comp.texto_da_expressao(b.sonda, sem_proximidade=True)
        niveis.append({"nivel": 3, "texto": f"{dois} AND {sem}", "expressao": None,
                       "rotulo": "mais as âncoras, sem proximidade"})
        niveis.append({"nivel": 4, "texto": f"{dois} AND {sonda}", "expressao": b.sonda,
                       "rotulo": "mais a proximidade"})
    else:
        # Sem proximidade, os níveis 3 e 4 coincidem: um só nível de âncoras.
        niveis.append({"nivel": 3, "texto": f"{dois} AND {sonda}", "expressao": b.sonda,
                       "rotulo": "mais as âncoras (a base não declara proximidade)"})
    niveis.append({"nivel": 5, "texto": f"{dois} AND {executada}", "expressao": b.executada,
                   "rotulo": "mais a executada"})
    return fonte, comp, niveis


def execucoes_da_expressao(b, sigla, ident, validas):
    """Consultas registradas e válidas de `ident` na base."""
    return [c for c in validas if c.get("base") == sigla and c.get("expressao") == ident]


def leitura_registrada(b, sigla, nivel, validas):
    """{origem, registros, arquivos, datas} da execução registrada do nível, ou None.

    Só o nível cuja expressão tem execução válida registrada se lê; os demais se submetem.
    """
    if nivel["expressao"] is None:
        return None
    regs = registros_da_expressao(sigla, nivel["expressao"], validas)
    if regs is None:
        return None
    consultas = execucoes_da_expressao(b, sigla, nivel["expressao"], validas)
    return {"origem": ", ".join(c["execucao"] for c in consultas),
            "registros": regs,
            "arquivos": [c.get("arquivo", "") for c in consultas],
            "datas": [c.get("data_hora", "") for c in consultas if c.get("data_hora")]}


def dois_dos_registros(regs):
    """Conjunto de DOIs normalizados dos registros."""
    return {normaliza_doi(r.get("doi")) for r in regs if normaliza_doi(r.get("doi"))}


def _milhar(n):
    return f"{n:,}".replace(",", ".")


def roteiro(b, sigla, fonte, niveis, lidos, teto, sementes, sem_doi):
    """Imprime o roteiro sem gravar: sementes, texto de cada nível, origem e chamada."""
    dois = {normaliza_doi(s.get("doi")) for s in sementes}
    print(f"\nANATOMIA DA PERDA — {sigla} ({b.bd_de.get(sigla, '?')})")
    print(f"  Sementes diagnosticadas: {', '.join(s['id'] for s in sementes)}")
    for s in sementes:
        print(f"    {s['id']}: {s['doi']}")
    if sem_doi:
        print(f"  Não diagnosticáveis por DOI (sem DOI no arquivo de sementes): "
              f"{', '.join(s['id'] for s in sem_doi)}")
    interface = filtros_de_interface(fonte)
    for n in niveis:
        lido = lidos.get(n["nivel"])
        if lido:
            quantos = len(dois_dos_registros(lido["registros"]) & dois)
            origem = (f"lido de {lido['origem']}"
                      f"{' em ' + ', '.join(sorted(set(lido['datas']))) if lido['datas'] else ''}"
                      f" ({quantos} de {len(dois)} DOIs encontrados)")
        else:
            origem = "a submeter"
        print(f"\n  Nível {n['nivel']} — {n['rotulo']} — {origem} — "
              f"{_milhar(len(n['texto']))} caracteres")
        print(n["texto"])
        if teto is not None and len(n["texto"]) > teto:
            print(f"  AVISO: {_milhar(len(n['texto']))} caracteres, acima do teto de "
                  f"{_milhar(teto)} declarado na fonte; a base pode recusar.")
        if n["nivel"] == 2 and interface:
            print("  Filtros a aplicar na interface (além do texto):")
            for f in interface:
                print(f"    - {f['rotulo']}: {f['como']}")
    submetidos = [n for n in niveis if not lidos.get(n["nivel"])]
    if submetidos:
        print("\n  Para registrar o resultado:")
        partes = ["python3 -m rsl aderencia diagnosticar " + sigla]
        for n in submetidos:
            partes.append(f"    --retorno {n['nivel']} <K{n['nivel']}> --exportacao "
                          f"{n['nivel']} <arquivo do nível {n['nivel']}>")
        partes.append("    --data-hora <AAAA-MM-DDTHH:MM>")
        print(" \\\n".join(partes))
        print("  (`--exportacao` só quando o retorno for maior que zero.)")
    else:
        print("\n  Todos os níveis vêm de execução registrada: nada a submeter.")
    print("\n  A submissão é manual, no navegador, com o acesso institucional; uma consulta "
          "por vez, e parada imediata diante de captcha, aviso de atividade atípica ou "
          "bloqueio.")


MAPA_CAUSA = {1: CAUSA_NAO_INDEXADA, 2: CAUSA_FILTRO, 3: CAUSA_ANCORAS,
              4: CAUSA_PROXIMIDADE, 5: CAUSA_FACETA}


def _data(texto):
    try:
        return datetime.datetime.fromisoformat(texto)
    except (TypeError, ValueError):
        raise Uso(f"--data-hora {texto!r} não é ISO 8601 (AAAA-MM-DDTHH:MM)") from None


def _pares(lista, nome, niveis):
    """{nível: valor} de `--retorno`/`--exportacao N VALOR`; nível repetido ou inexistente
    sai com USO."""
    saida = {}
    for n, valor in lista:
        try:
            n = int(n)
        except (TypeError, ValueError):
            raise Uso(f"--{nome} {n}: o nível é um número inteiro") from None
        if n not in niveis:
            raise Uso(f"--{nome} {n}: só existem os níveis {niveis}")
        if n in saida:
            raise Uso(f"--{nome} {n}: nível repetido")
        saida[n] = valor
    return saida


def _resultados(sigla, niveis, lidos, retornos, exportacoes, data_hora, sementes):
    """Resultados conferidos dos níveis: {nível: {origem, retorno, arquivo, data_hora,
    registros, dois}}. Falta, sobra ou divergência sai com DADOS; incoerência, REPROVADO."""
    quando = _data(data_hora)
    numeros = [n["nivel"] for n in niveis]
    diagnosticados = {normaliza_doi(s.get("doi")) for s in sementes}
    retornos = _pares(retornos, "retorno", numeros)
    exportacoes = _pares(exportacoes, "exportacao", numeros)
    for n in numeros:
        if n in lidos and (n in retornos or n in exportacoes):
            raise DadosInvalidos(f"nível {n} é lido de {lidos[n]['origem']} e não se "
                                 f"submete; retire `--retorno {n}` e `--exportacao {n}`")
        if n not in lidos and n not in retornos:
            raise DadosInvalidos(f"nível {n} sem --retorno: todo nível submetido exige o "
                                 f"retorno exibido")
    resultados = {}
    for n in niveis:
        numero = n["nivel"]
        if numero in lidos:
            lido = lidos[numero]
            todos = dois_dos_registros(lido["registros"])
            dois = todos & diagnosticados
            resultados[numero] = {
                "nivel": numero, "origem": f"execução {lido['origem']}",
                "retorno": len(dois), "arquivo": "; ".join(lido["arquivos"]),
                "data_hora": "; ".join(lido["datas"]), "registros": lido["registros"],
                "dois": dois}
            continue
        k = retornos[numero]
        if k < 0:
            raise Uso(f"--retorno {numero} {k}: retorno negativo não existe")
        if k == 0 and numero in exportacoes:
            raise DadosInvalidos(f"nível {numero} com retorno 0 e --exportacao "
                                 f"{exportacoes[numero]!r}: retorno zero não tem exportação; "
                                 f"confira o retorno exibido")
        if k > 0 and numero not in exportacoes:
            raise DadosInvalidos(f"nível {numero} com retorno {k} e sem --exportacao: toda "
                                 f"exportação que devolve registro se lê")
        if k > 0:
            arq = pathlib.Path(exportacoes[numero])
            arq = arq if arq.is_absolute() else RAIZ / arq
            if not arq.exists():
                raise DadosInvalidos(f"nível {numero}: exportação {exportacoes[numero]!r} "
                                     f"não existe")
            regs = le_arquivo(arq)
            if len(regs) != k:
                raise DadosInvalidos(f"nível {numero}: retorno {k} e {len(regs)} registro(s) "
                                     f"lido(s) de {relativo(arq)}")
            nome_arq = relativo(arq)
        else:
            regs, nome_arq = [], ""
        resultados[numero] = {"nivel": numero, "origem": "submetido", "retorno": k,
                              "arquivo": nome_arq, "data_hora": data_hora,
                              "registros": regs, "dois": dois_dos_registros(regs)}
    return resultados, quando


def confere_coerencia(resultados, sementes):
    """Cada nível só com DOIs diagnosticados e contido no anterior; a violação reprova,
    porque a consulta submetida não foi a montada."""
    diagnosticados = {normaliza_doi(s.get("doi")) for s in sementes}
    anterior = None
    for numero in sorted(resultados):
        dois = resultados[numero]["dois"]
        estranhos = sorted(dois - diagnosticados)
        if estranhos:
            raise Reprovado(f"nível {numero}: DOI(s) fora das sementes diagnosticadas — "
                            f"{', '.join(estranhos)}; a consulta submetida não é a montada")
        if anterior is not None:
            reaparecem = sorted((dois - anterior) & diagnosticados)
            if reaparecem:
                raise Reprovado(f"nível {numero}: DOI(s) ausentes do nível anterior e "
                                f"presentes neste — {', '.join(reaparecem)}; a base mudou "
                                f"entre as submissões ou a consulta não é a montada")
        anterior = dois


def _registro_do_doi(resultados, doi):
    """O registro do nível 1 com o DOI, para ler ano, idioma e tipo documental."""
    for r in resultados[min(resultados)]["registros"]:
        if normaliza_doi(r.get("doi")) == doi:
            return r
    return {}


def atribui(resultados, sementes, quando, datas_lidas):
    """Uma linha por semente: presença em cada nível, causa e observação.

    A causa é o primeiro nível em que o DOI da semente desaparece; presente em todos, a
    semente já está na executada e o casamento por título da aderência falhou.
    """
    numeros = sorted(resultados)
    linhas = []
    for s in sementes:
        doi = normaliza_doi(s.get("doi"))
        presenca = {n: doi in resultados[n]["dois"] for n in numeros}
        if all(presenca.values()):
            causa = CAUSA_PRESENTE
            obs = "divergência com o casamento por título da aderência: o DOI está na executada"
        else:
            primeiro = next(n for n in numeros if not presenca[n])
            causa = MAPA_CAUSA[primeiro]
            if causa == CAUSA_NAO_INDEXADA:
                obs = "sugere `indexada = não` na planilha de aderência (o comando não preenche)"
            elif causa == CAUSA_FILTRO:
                reg = _registro_do_doi(resultados, doi)
                partes = [f"{k}: {reg.get(k)}" for k in ("ano", "idioma", "tipo")
                          if reg.get(k)]
                obs = ("identificar o critério que a exclui — "
                       + (", ".join(partes) if partes else "exportação sem ano, idioma ou tipo"))
            elif causa == CAUSA_PROXIMIDADE:
                obs = ""
            elif causa == CAUSA_FACETA:
                obs = ""
            else:
                obs = ""
        datas = {d[:10] for d in datas_lidas if d}
        if causa == CAUSA_PROXIMIDADE and datas and quando.date().isoformat() not in datas:
            obs = (obs + "; " if obs else "") + (
                f"a conferir: a execução lida é de {', '.join(sorted(datas))} e a submissão "
                f"de {quando.date().isoformat()}; a base pode ter indexado o estudo depois")
        linhas.append({"semente": s["id"], "doi": s.get("doi", ""), "presenca": presenca,
                       "causa": causa, "observacao": obs})
    return linhas


def _grava(b, sigla, niveis, resultados, linhas):
    """Grava `[saidas] anatomia` e `[saidas] anatomia_consultas`."""
    numeros = sorted(resultados)
    rel = b.config.saida("anatomia", base=sigla)
    rel.parent.mkdir(parents=True, exist_ok=True)
    with rel.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["semente", "doi"] + [f"nivel_{n}" for n in numeros]
                   + ["causa", "observacao"])
        for linha in linhas:
            w.writerow([linha["semente"], linha["doi"]]
                       + ["sim" if linha["presenca"][n] else "" for n in numeros]
                       + [linha["causa"], linha["observacao"]])
    cons = b.config.saida("anatomia_consultas", base=sigla)
    with cons.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["nivel", "texto", "origem", "retorno", "arquivo", "data_hora"])
        for n in numeros:
            r = resultados[n]
            w.writerow([n, next(x["texto"] for x in niveis if x["nivel"] == n),
                        r["origem"], r["retorno"], r["arquivo"], r["data_hora"]])
    return rel, cons


def diagnosticar(b, base, retornos=(), exportacoes=(), data_hora=None, sementes=None):
    """Roteiro (sem resultado) ou resultado do diagnóstico da perda numa base."""
    bd, sigla = b.exige_bd(base)
    sel = selecao(b, sigla, sementes)
    if not sel["diagnosticaveis"]:
        if sel["sem_doi"]:
            print(f"Não diagnosticáveis por DOI (sem DOI no arquivo de sementes): "
                  f"{', '.join(s['id'] for s in sel['sem_doi'])}")
        print(f"Nenhuma perda a diagnosticar em {sigla} ({bd}): todas as sementes esperadas "
              f"nesta base foram recuperadas por título exato.")
        return Saida.OK
    fonte, comp, niveis = monta_niveis(b, sigla, sel["diagnosticaveis"])
    _, validas = carrega_consultas(b)
    lidos = {}
    for n in niveis:
        lido = leitura_registrada(b, sigla, n, validas)
        if lido:
            lidos[n["nivel"]] = lido
    if not retornos and not exportacoes and not data_hora:
        roteiro(b, sigla, fonte, niveis, lidos, fonte["teto"], sel["diagnosticaveis"],
                sel["sem_doi"])
        return Saida.OK
    if not data_hora:
        raise DadosInvalidos("falta --data-hora: com resultado, a data e a hora da "
                             "submissão são obrigatórias, ISO 8601")
    resultados, quando = _resultados(sigla, niveis, lidos, retornos, exportacoes,
                                     data_hora, sel["diagnosticaveis"])
    confere_coerencia(resultados, sel["diagnosticaveis"])
    datas = sorted({d for r in resultados.values() if r["origem"].startswith("execução")
                    for d in r["data_hora"].split("; ") if d})
    linhas = atribui(resultados, sel["diagnosticaveis"], quando, datas)
    rel, cons = _grava(b, sigla, niveis, resultados, linhas)
    print(f"\nANATOMIA DA PERDA — {sigla} ({bd})")
    for linha in linhas:
        print(f"  {linha['semente']:>4}  {linha['causa']:<22} {linha['observacao']}")
    if datas and quando.date().isoformat() not in {d[:10] for d in datas}:
        print(f"\n  AVISO: execuções lidas de {', '.join(sorted({d[:10] for d in datas}))}; "
              f"submissão de {quando.date().isoformat()}. A base pode ter mudado entre elas.")
    print(f"\n  Sementes por causa: "
          + "; ".join(f"{c}: {sum(1 for x in linhas if x['causa'] == c)}"
                      for c in CAUSAS + (CAUSA_PRESENTE,)
                      if any(x["causa"] == c for x in linhas)))
    print(f"  Resultado em {relativo(rel)}; consultas em {relativo(cons)}.")
    return Saida.OK


def cmd_diagnosticar(ctx, a):
    return diagnosticar(Busca(ctx), a.base, a.retorno or (), a.exportacao or (),
                        a.data_hora)
