"""Autoteste do arquivo de sementes: cada defeito do arquivo, injetado numa cópia em memória
gerada das sementes lidas, reprova com PROTOCOLO_ILEGIVEL nomeando a semente e o campo; o
arquivo ausente termina com CONFIGURACAO. Os casos de campo ausente e de campo desconhecido
saem do esquema declarado na gramática, não de uma lista daqui.

Dado não obtido ou juízo não feito (DOI ausente, facetas vazias, semente sem âncora) não
reprova: a cópia tem de ser aprovada e `projeto pendencias` tem de relatá-la. A evidência
bruta de semente inexistente reprova `dados conferir`."""

import contextlib
import io
import pathlib
import tempfile

from .. import doi as _doi
from .. import gramatica as G
from ..config import Configuracao
from ..coerencia import conferir
from ..contexto import Contexto
from ..procedimentos import gera_base, registro_de_execucao
from ..dados import (SUBPASTA_CROSSREF, SUBPASTA_OPENALEX, SUBPASTA_REFERENCIAS, pendencias_sementes,
                     problemas_evidencia)
from ..saida import Saida
from . import resultado
from .textos import itens_toml, toml_de

P = Saida.PROTOCOLO_ILEGIVEL
CHAVE = G.TT_SEMENTES.chave


def casos(ctx, g):
    texto, d = ctx.texto_sementes, ctx.protocolo()
    itens = itens_toml(texto, CHAVE)
    c_id, c_bases = G.C_ID.chave, G.C_BASES.chave
    c_doi = G.C_DOI.chave
    primeiro, ultimo = itens[0][c_id], itens[-1][c_id]
    ids_facetas = [f["id"] for f in d["facetas"]]
    fora_da_tabela = f"{G.I_FCT.prefixo}{len(ids_facetas) + 1}"
    meio = len(itens) // 2 if len(itens) > 2 else 0

    def com(k, **mudancas):
        """Cópia com o item `k` alterado; valor None retira o campo."""
        novos = [dict(x) for x in itens]
        for campo, valor in mudancas.items():
            if valor is None:
                novos[k].pop(campo, None)
            else:
                novos[k][campo] = valor
        return toml_de(novos, CHAVE)

    def executa(m):
        return conferir(ctx.com_sementes(m))

    casos_ = [("TOML quebrado", texto + f"\n[[{CHAVE}]\n", P, "não é TOML válido")]
    for c in (x for x in G.TT_SEMENTES.campos if x.exigido):
        casos_.append((f"campo obrigatório '{c.chave}' retirado", com(-1, **{c.chave: None}),
                       P, (f"falta o campo '{c.chave}'", c.rotulo)))
    # Gerado do esquema: um nome que nenhum campo declarado tem, para que o caso continue
    # valendo quando o esquema ganhar campos.
    declarados = {c.chave for c in G.TT_SEMENTES.campos}
    desconhecido = next(n for n in (f"campo_fora_do_esquema_{k}" for k in range(1000))
                        if n not in declarados)
    casos_ += [
        ("campo desconhecido", com(-1, **{desconhecido: "x"}), P,
         (f"semente {ultimo}", "campo desconhecido", desconhecido)),
        ("campo de tipo errado (bases como texto)", com(-1, **{c_bases: itens[-1][c_bases][0]}),
         P, (f"semente {ultimo}", f"'{c_bases}' não é")),
        ("id repetido", com(-1, **{c_id: primeiro}), P,
         (f"semente {primeiro}", f"'{c_id}' repetido")),
        ("id fora da forma", com(-1, **{c_id: "S" + ultimo}), P,
         (f"semente S{ultimo}", "fora da forma")),
        ("id fora de sequência", com(-1, **{c_id: f"{G.I_SE.prefixo}{len(itens) + 1}"}), P,
         ("fora da numeração", f"{G.I_SE.prefixo}{len(itens) + 1}")),
        ("base fora da tabela de bases",
         com(-1, **{c_bases: [itens[-1][c_bases][0] + "x"]}), P,
         (f"semente {ultimo}", "não é sigla")),
        ("base com outra grafia",
         com(0, **{c_bases: [itens[0][c_bases][0].swapcase()]}), P,
         (f"semente {primeiro}", itens[0][c_bases][0].swapcase())),
        ("semente sem base", com(-1, **{c_bases: []}), P,
         (f"semente {ultimo}", "semente sem base")),
        ("base repetida", com(-1, **{c_bases: itens[-1][c_bases][:1] * 2}), P,
         (f"semente {ultimo}", f"{c_bases} com repetição")),
        # Esquema mínimo: cada defeito, gerado das sementes lidas.
        ("referência curta vazia", com(-1, **{G.C_REFERENCIA_CURTA.chave: ""}), P,
         (f"semente {ultimo}", f"'{G.C_REFERENCIA_CURTA.chave}' vazio")),
        ("doi fora da forma", com(-1, **{c_doi: "DOI: " + (itens[-1].get(c_doi) or "x")}), P,
         (f"semente {ultimo}", f"'{c_doi}'", "fora da forma")),
        ("doi vazio", com(-1, **{c_doi: ""}), P, (f"semente {ultimo}", f"'{c_doi}' vazio")),
        ("doi repetido (outra caixa)", com(-1, **{c_doi: itens[0][c_doi].upper()}), P,
         (f"semente {ultimo}", f"'{c_doi}' repetido", primeiro)),
        ("faceta do alinhamento fora da tabela",
         com(-1, **{G.C_ALINHAMENTO.chave: {fora_da_tabela: "ontologia"}}), P,
         (f"semente {ultimo}", fora_da_tabela)),
        ("frase de alinhamento vazia",
         com(-1, **{G.C_ALINHAMENTO.chave: {ids_facetas[0]: " "}}), P,
         (f"semente {ultimo}", "frase vazia", ids_facetas[0])),
        ("alinhamento como lista", com(-1, **{G.C_ALINHAMENTO.chave: ids_facetas[:2]}), P,
         (f"semente {ultimo}", f"'{G.C_ALINHAMENTO.chave}' não é")),
        ("lacuna na numeração (semente do meio retirada)",
         toml_de(itens[:meio] + itens[meio + 1:], CHAVE), P,
         ("fora da numeração", f"{itens[meio + 1][c_id]} onde se esperava {itens[meio][c_id]}")),
        ("campo `semente` do esquema intermediário", com(-1, semente="Autor (2000). Título."), P,
         (f"semente {ultimo}", "campo desconhecido", "semente")),
        ("campo retirado `escopo`", com(-1, escopo=""), P,
         (f"semente {ultimo}", "campo desconhecido", "escopo")),
        # Verificação binária: o texto livre antigo reprova, em vez de valer como estado.
        ("verificação como texto", com(-1, **{G.C_VERIFICACAO.chave: "CONFIRMADA"}), P,
         (f"semente {ultimo}", f"'{G.C_VERIFICACAO.chave}' não é booleano")),
    ]
    # Campos retirados do esquema (conjunto único de validação; conferência sem dado):
    # um arquivo antigo reprova alto, em vez de perder o campo em silêncio.
    # Os campos bibliográficos, `facetas` e `veiculo_conferido` saíram na fase 2: os dados
    # vêm do Zotero, e o campo de volta seria segunda fonte que diverge em silêncio.
    for retirado, valor in ([(c, "x") for c in G.BIBLIOGRAFICOS if c != "ano"]
                            + [("ano", 2000), ("facetas", ids_facetas[:1]),
                               ("veiculo_conferido", "sim"),
                               ("papel", "validação"), ("tipo", ""), ("alinhamento", ""),
                               ("eric", ""), ("observacoes", "")]):
        casos_.append((f"campo retirado `{retirado}`", com(-1, **{retirado: valor}), P,
                       (f"semente {ultimo}", "campo desconhecido", retirado)))
    for nome, mutante, codigo, trecho in casos_:
        g.espera(nome, mutante, texto, executa, codigo, trecho)

    # Título com ponto: o título é o campo inteiro do item do Zotero, sem corte.
    import copy as _copy                                            # noqa: PLC0415
    from .. import zotero as Z                                      # noqa: PLC0415
    alvo = _doi.normaliza(d["sementes"][-1]["doi"])
    doc = _copy.deepcopy(ctx.zotero)
    item = next(i for i in doc["itens"] if Z.campos(i)["doi"] == alvo)
    com_ponto = item["data"]["title"] + ". Segunda frase do título"
    item["data"]["title"] = com_ponto
    cod, msgs = resultado(lambda: ctx.com_zotero(doc).protocolo())
    lidos = ctx.com_zotero(doc).protocolo()["sementes"] if cod == Saida.OK else []
    g.testa("título com ponto seguido de maiúscula é lido inteiro do item do Zotero",
            bool(lidos) and lidos[-1]["titulo"] == com_ponto, f"{cod.name} {msgs[:1]}")

    # Campos em outra ordem: o esquema é por nome.
    invertido = toml_de([dict(reversed(list(x.items()))) for x in itens], CHAVE)
    cod, msgs = resultado(lambda: ctx.com_sementes(invertido).protocolo())
    g.testa("campos em outra ordem aprovam e dão as mesmas sementes",
            cod == Saida.OK and ctx.com_sementes(invertido).protocolo()["sementes"]
            == d["sementes"], f"{msgs[:1]}")

    # Arquivo ausente: CONFIGURACAO, com a chave e o caminho; nenhuma semente presumida.
    inexistente = ctx.config.valor("documentos.sementes") + ".inexistente"
    cfg = Configuracao(ctx.config.com("documentos.sementes", inexistente), ctx.config.arquivo)
    cod, msgs = resultado(lambda: Contexto(cfg).protocolo())
    g.testa("arquivo de sementes ausente termina com CONFIGURACAO, com a chave e o caminho",
            cod == Saida.CONFIGURACAO and any("documentos.sementes" in m and inexistente in m
                                              for m in msgs), f"{cod.name} {msgs[:1]}")

    _aprovam_com_pendencia(ctx, g, itens, com, d)
    _evidencia(ctx, g, itens)


def _aprovam_com_pendencia(ctx, g, itens, com, d):
    """Dado ou juízo pendente: a cópia é aprovada e `projeto pendencias` a relata, nomeando a
    semente. Cópia reprovada, ou pendência não relatada, faz o autoteste falhar."""
    c_id = G.C_ID.chave
    ancoras = d["ancoras"]
    nao_ancoras = [f["id"] for f in d["facetas"] if f["id"] not in ancoras]
    k_val = len(itens) // 2

    def regenerado(mutante):
        """Contexto com a cópia do arquivo de sementes e os procedimentos regenerados em
        memória: a seção 5 é gerada do arquivo de sementes, e a cópia só se aprova depois
        de `procedimentos gerar`."""
        cx = ctx.com_sementes(mutante)
        dx = cx.protocolo()
        # Com o registro de execução, como `procedimentos gerar`: o roteiro traz os
        # resultados de sondagem registrados.
        reg = registro_de_execucao(cx)
        return cx.com_procedimentos({b["sigla"]: gera_base(cx, dx, b["sigla"], registro=reg)[2]
                              for b in dx["bases"]})

    def aprova_e_relata(nome, mutante, ident, trecho, relata=True):
        cod, msgs = resultado(lambda: conferir(regenerado(mutante)))
        if cod != Saida.OK:
            g.falha(f"{nome}: a cópia devia ser aprovada — {cod.name} {msgs[:1]}")
            return
        linhas = pendencias_sementes(ctx.com_sementes(mutante).protocolo())
        achou = any(f"semente {ident} " in l and trecho in l for l in linhas)
        g.testa(f"aprova com pendência{'' if relata else ' (sem relato)'}: {nome}",
                achou == relata,
                f"`projeto pendencias` {'não relatou' if relata else 'relatou'} {ident} com "
                f"{trecho!r}")

    ident = itens[0][c_id]
    c_verif = G.C_VERIFICACAO.chave
    aprova_e_relata("verificação false", com(0, **{c_verif: False}), ident, "verificação")
    aprova_e_relata("verificação ausente", com(0, **{c_verif: None}), ident, "verificação")
    aprova_e_relata("verificação true", com(0, **{c_verif: True}), ident, "verificação",
                    relata=False)
    c_al = G.C_ALINHAMENTO.chave
    aprova_e_relata("alinhamento ausente", com(0, **{c_al: None}), ident,
                    "alinhamento a informar")
    if not nao_ancoras:
        g.nao_executa("sem faceta que não seja âncora")
        return
    ident = itens[k_val][c_id]
    aprova_e_relata("semente sem faceta âncora",
                    com(k_val, **{c_al: {nao_ancoras[0]: "frase do autoteste"}}), ident,
                    "sem faceta âncora")
    # Prova de que a pendência discrimina: com uma âncora, não se relata.
    aprova_e_relata("semente com faceta âncora",
                    com(k_val, **{c_al: {ancoras[0]: "frase do autoteste"}}), ident,
                    "sem faceta âncora", relata=False)
    # Com o alinhamento vazio, só "alinhamento a informar": a falta de âncora não se relata.
    aprova_e_relata("semente sem alinhamento",
                    com(k_val, **{c_al: {}}), ident, "sem faceta âncora", relata=False)
    _referencia_curta(ctx, g, itens, com, aprova_e_relata, regenerado)


def _evidencia(ctx, g, itens):
    """Evidência `SEn_…` de semente que não está no arquivo reprova `dados conferir`,
    nomeando o arquivo; a de semente presente, não. Numa pasta temporária, gerada do
    último `id` lido. Só a subpasta de referências é conferida: o mesmo arquivo noutra
    subpasta da evidência não reprova."""
    ultimo = itens[-1][G.C_ID.chave]
    sem_ultimo = ctx.com_sementes(toml_de(itens[:-1], CHAVE)).protocolo()
    with tempfile.TemporaryDirectory() as tmp:
        arq = pathlib.Path(tmp) / SUBPASTA_REFERENCIAS / f"{ultimo}_autoteste.json"
        fora = pathlib.Path(tmp) / f"outra_{SUBPASTA_REFERENCIAS}" / arq.name
        for x in (arq, fora):
            x.parent.mkdir()
            x.write_text("{}", encoding="utf-8")
        presente = problemas_evidencia(ctx.protocolo(), tmp)
        retirada = problemas_evidencia(sem_ultimo, tmp)
    g.testa(f"evidência de semente presente ({ultimo}) não reprova", not presente,
            f"{presente[:1]}")
    g.testa(f"reprovou: evidência de semente retirada ({arq.name})",
            any(f"{SUBPASTA_REFERENCIAS}/{arq.name}" in p for p in retirada),
            "aprovou indevidamente")
    g.testa(f"evidência fora de {SUBPASTA_REFERENCIAS}/ não é conferida",
            not any(fora.parent.name in p for p in retirada), f"{retirada}")
    _evidencia_openalex(ctx, g, itens)


def _evidencia_openalex(ctx, g, itens):
    """Resposta da OpenAlex de DOI que não está no arquivo reprova `dados conferir`,
    nomeando o arquivo; a de DOI presente, não, nem depois de renumerar as sementes."""
    d = ctx.protocolo()
    com_doi = [e for e in d["sementes"] if e.get("doi")]
    if len(com_doi) < 2:
        g.nao_executa("menos de duas sementes com DOI", quantos=3)
        return
    with tempfile.TemporaryDirectory() as tmp:
        pasta = pathlib.Path(tmp) / SUBPASTA_OPENALEX
        pasta.mkdir()
        for e in com_doi:
            (pasta / _doi.nome_arquivo(e["doi"])).write_text("{}", encoding="utf-8")
        presente = problemas_evidencia(d, tmp)
        inexistente = pasta / _doi.nome_arquivo("10.9999/autoteste.inexistente")
        inexistente.write_text("{}", encoding="utf-8")
        injetado = problemas_evidencia(d, tmp)
        inexistente.unlink()
        cruz = pathlib.Path(tmp) / SUBPASTA_CROSSREF
        cruz.mkdir()
        marca = cruz / "10.9999_autoteste.inexistente.404"
        marca.write_text("HTTP 404", encoding="utf-8")
        marcado = problemas_evidencia(d, tmp)
        marca.unlink()
        # Semente do meio retirada e as seguintes renumeradas: as outras respostas continuam
        # valendo sem renomear, e só a da retirada reprova.
        meio = len(itens) // 2
        renumeradas = [dict(x, **{G.C_ID.chave: f"{G.I_SE.prefixo}{k + 1}"})
                       for k, x in enumerate(itens[:meio] + itens[meio + 1:])]
        dr = ctx.com_sementes(toml_de(renumeradas, CHAVE)).protocolo()
        renum = problemas_evidencia(dr, tmp)
    g.testa("resposta da OpenAlex de DOI presente não reprova", not presente, f"{presente[:1]}")
    g.testa(f"reprovou: resposta da OpenAlex de DOI inexistente ({inexistente.name})",
            any(f"{SUBPASTA_OPENALEX}/{inexistente.name}" in p for p in injetado),
            "aprovou indevidamente")
    g.testa(f"reprovou: marcador de 404 do Crossref de DOI inexistente ({marca.name})",
            any(f"{SUBPASTA_CROSSREF}/{marca.name}" in p for p in marcado),
            "aprovou indevidamente")
    retirado = itens[meio].get(G.C_DOI.chave)
    esperado = [_doi.nome_arquivo(retirado)] if retirado else []
    g.testa("renumeração não exige renomear resposta da OpenAlex: só a da retirada reprova",
            sorted(p.split(f"{SUBPASTA_OPENALEX}/")[1].split(" ")[0] for p in renum)
            == esperado, f"{renum}")


def ensaio(ctx, g):
    """Ensaio seco por campo, sobre sementes sintéticas geradas dos termos lidos das STR: o
    termo só no resumo sai marcado R; o campo que falta é "ausente", não "sem termo"; a
    faceta alinhada sem termo é listada; e `aderencia ensaiar` não grava arquivo."""
    from .. import sementes as S                                    # noqa: PLC0415
    d = dict(ctx.protocolo())
    ids = [f["id"] for f in d["facetas"]]
    termos = {fid: v["termos"] for fid, v in d["strings"].items()}
    if len(ids) < 3 or not all(termos.get(f) for f in ids[:3]):
        g.nao_executa("menos de três facetas com string", quantos=4)
        return
    t1, t2 = termos[ids[0]][0], termos[ids[1]][0]
    neutro = "zzautoteste semente"
    sementes = [
        {"id": "SX1", "chave": "Autoteste 1", "titulo": neutro, "resumo": f"um {t1} aqui",
         "palavras_chave": [t2], "alinhamento_facetas": {ids[0]: "a", ids[2]: "b"}},
        {"id": "SX2", "chave": "Autoteste 2", "titulo": f"{t1} e {t2}", "resumo": "",
         "palavras_chave": [], "alinhamento_facetas": {}},
    ]
    d["sementes"] = sementes
    por = {e["id"]: r for e, r in S.ensaio(d)}
    g.testa(f"termo só no resumo ({t1}) marcado R na {ids[0]}",
            por["SX1"][ids[0]].get(t1) == ["R"], f"{por['SX1'][ids[0]]}")
    g.testa(f"termo nas palavras-chave ({t2}) marcado P na {ids[1]}",
            por["SX1"][ids[1]].get(t2) == ["P"], f"{por['SX1'][ids[1]]}")
    linhas = S.relata(d)
    texto = "\n".join(linhas)
    g.testa("campo ausente marcado como ausente, separado de sem termo",
            any("SX2" in l and "resumo ausente" in l and "palavras-chave ausente" in l
                for l in linhas) and not any("SX1" in l and "ausente" in l for l in linhas),
            texto[:200])
    g.testa(f"faceta alinhada sem termo listada ({ids[2]} da SX1)",
            any("alinhada sem termo" in l and ids[2] in l and ids[0] not in l.split(":")[-1]
                for l in linhas), texto[-400:])
    d["sementes"] = [dict(sementes[1], alinhamento_facetas={ids[2]: "c"})]
    so_titulo = S.relata(d)
    g.testa("faceta alinhada sem termo, com campo ausente, não é dada como indício de lacuna",
            any("campos presentes" in l and ids[2] in l for l in so_titulo)
            and not any("indício de lacuna de vocabulário" in l for l in so_titulo), "\n".join(so_titulo)[:300])
    d["sementes"] = sementes
    g.testa("relato traz as duas contagens e a ressalva sobre as palavras-chave",
            "só pelo título" in texto and "pelos três campos juntos" in texto
            and "OpenAlex" in texto, texto[-300:])

    def retrato():
        raiz = pathlib.Path(ctx.config.caminho("dados.registro")).parent.parent
        return {(str(p), p.stat().st_mtime_ns, p.stat().st_size)
                for p in raiz.rglob("*") if p.is_file() and ".git" not in p.parts}
    antes = retrato()
    with contextlib.redirect_stdout(io.StringIO()):
        cod, msgs = resultado(lambda: S.cmd_ensaiar(ctx))
    g.testa("`aderencia ensaiar` não cria nem altera arquivo do projeto",
            cod == Saida.OK and retrato() == antes, f"{cod.name} {msgs[:1]}")


def _referencia_curta(ctx, g, itens, com, aprova_e_relata, regenerado):
    """`referencia_curta`: a sugerida do item aprova `documentos conferir`; sobrenome, ano ou
    título que não conferem com o item reprovam, sem reprovar a leitura. A ausente reprova a
    leitura, no caso de campo obrigatório retirado."""
    from ..leitura import referencia_curta_sugerida                 # noqa: PLC0415
    d = ctx.protocolo()
    z = d["sementes"][0]["zotero"]
    ident = itens[0][G.C_ID.chave]
    c_rc = G.C_REFERENCIA_CURTA.chave
    sugerida = referencia_curta_sugerida(z)
    autoria, titulo = sugerida.split(":", 1)
    sobrenome, ano = autoria.rsplit(" ", 1)
    casos_ = [
        ("referência curta sugerida", sugerida, True),
        ("referência curta sem reticências e com outra caixa", sugerida.rstrip("…").upper(),
         True),
        ("sobrenome trocado", f"{sobrenome}x {ano}:{titulo}", False),
        ("ano trocado", f"{sobrenome} {int(ano) + 1}:{titulo}", False),
        ("sem o ano", f"{sobrenome}:{titulo}", False),
        ("título que não é o começo do item", f"{sobrenome} {ano}: zzautoteste {titulo}",
         False),
        ("sem dois-pontos", sugerida.replace(":", ""), False),
    ]
    for nome, valor, aprova in casos_:
        cod, msgs = resultado(lambda v=valor: conferir(regenerado(com(0, **{c_rc: v}))))
        leitura, _ = resultado(lambda v=valor: ctx.com_sementes(com(0, **{c_rc: v})).protocolo())
        if aprova:
            g.testa(f"{nome}: `documentos conferir` aprova", cod == Saida.OK,
                    f"{cod.name} {msgs[:1]}")
        else:
            g.testa(f"reprovou: {nome} — conferência reprova com a forma sugerida e a leitura "
                    f"aprova", cod != Saida.OK and leitura == Saida.OK
                    and any(f"semente {ident}" in m and sugerida in m for m in msgs),
                    f"{cod.name}/{leitura.name} {msgs[:1]}")


def juncao(ctx, g):
    """Junção pelo DOI com a cópia da coleção do Zotero, sobre cópias em memória geradas da
    cópia lida: item retirado da cópia reprova com DADOS, nomeando a semente, o DOI e
    `sementes copiar`; DOI com outra caixa e prefixo de URL casa; item a mais é relatado;
    cópia ausente sai com DADOS."""
    import copy as _copy                                            # noqa: PLC0415
    from .. import zotero as Z                                      # noqa: PLC0415
    doc, d = ctx.zotero, ctx.protocolo()
    alvo = d["sementes"][-1]
    chave = _doi.normaliza(alvo["doi"])

    def sem_alvo():
        x = _copy.deepcopy(doc)
        x["itens"] = [i for i in x["itens"] if Z.campos(i)["doi"] != chave]
        return x
    cod, msgs = resultado(lambda: ctx.com_zotero(sem_alvo()).protocolo())
    g.testa(f"reprovou (DADOS): item de {alvo['id']} retirado da cópia",
            cod == Saida.DADOS and any(alvo["id"] in m and alvo["doi"] in m
                                       and "sementes copiar" in m for m in msgs),
            f"{cod.name} {msgs[:1]}")

    duplicado = _copy.deepcopy(doc)
    extra = next(i for i in duplicado["itens"] if Z.campos(i)["doi"] == chave)
    duplicado["itens"].append(_copy.deepcopy(extra))
    cod, msgs = resultado(lambda: ctx.com_zotero(duplicado).protocolo())
    g.testa(f"reprovou (DADOS): dois itens com o DOI de {alvo['id']}",
            cod == Saida.DADOS and any(alvo["id"] in m for m in msgs), f"{cod.name}")

    caixa = _copy.deepcopy(doc)
    for i in caixa["itens"]:
        if Z.campos(i)["doi"] == chave:
            i["data"]["DOI"] = "https://doi.org/" + i["data"]["DOI"].upper()
    cod, msgs = resultado(lambda: ctx.com_zotero(caixa).protocolo())
    g.testa("DOI do item com outra caixa e prefixo de URL casa com a semente",
            cod == Saida.OK, f"{cod.name} {msgs[:1]}")

    a_mais = _copy.deepcopy(doc)
    novo = _copy.deepcopy(a_mais["itens"][0])
    novo["key"] = novo["data"]["key"] = "AUTOTESTE"
    novo["data"]["DOI"] = "10.9999/autoteste.fora"
    a_mais["itens"].append(novo)
    linhas = pendencias_sementes(ctx.com_zotero(a_mais).protocolo())
    g.testa("item da cópia fora do arquivo de sementes é relatado em `projeto pendencias`",
            any("10.9999/autoteste.fora" in l and "fora do arquivo" in l for l in linhas))

    sem_resumo = _copy.deepcopy(doc)
    for i in sem_resumo["itens"]:
        if Z.campos(i)["doi"] == chave:
            i["data"]["tags"] = []
    linhas = pendencias_sementes(ctx.com_zotero(sem_resumo).protocolo())
    g.testa(f"palavras-chave ausentes no item de {alvo['id']} viram pendência",
            any(f"semente {alvo['id']} " in l and "palavras-chave ausentes" in l
                for l in linhas))

    for nome, campo, vazio in (("título", "title", ""), ("autor", "creators", []),
                               ("ano", None, None)):
        x = _copy.deepcopy(doc)
        for i in x["itens"]:
            if Z.campos(i)["doi"] == chave:
                if campo:
                    i["data"][campo] = vazio
                else:
                    i["meta"]["parsedDate"] = ""
        cod, msgs = resultado(lambda x=x: ctx.com_zotero(x).protocolo())
        g.testa(f"reprovou (DADOS): item de {alvo['id']} sem {nome}",
                cod == Saida.DADOS and any(alvo["id"] in m and f"sem {nome}" in m
                                           and "sementes copiar" in m for m in msgs),
                f"{cod.name} {msgs[:1]}")

    dado = _copy.deepcopy(ctx.config.dado)
    dado["dados"]["zotero"] = ctx.config.valor("dados.zotero") + ".inexistente"
    cod, msgs = resultado(lambda: Contexto(Configuracao(dado, ctx.config.arquivo)).protocolo())
    g.testa("cópia da coleção ausente sai com DADOS e indica `sementes copiar`",
            cod == Saida.DADOS and any("sementes copiar" in m for m in msgs),
            f"{cod.name} {msgs[:1]}")


def et_al(ctx, g):
    """Regra do et al.: até três autores, todos; quatro ou mais, o primeiro e "et al."."""
    from ..leitura import autoria_exibida                           # noqa: PLC0415
    g.testa("três autores aparecem todos",
            autoria_exibida(["A, x", "B, y", "C, z"]) == "A, B & C")
    g.testa("quatro autores abreviam ao primeiro e et al.",
            autoria_exibida(["A, x", "B, y", "C, z", "D, w"]) == "A et al.")
    g.testa("lista já abreviada no arquivo aparece com et al.",
            autoria_exibida(["Tondeur, J. et al."]) == "Tondeur et al.")
