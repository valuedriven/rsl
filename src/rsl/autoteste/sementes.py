"""Autoteste do arquivo de sementes: cada defeito do arquivo, injetado numa cópia em memória
gerada das sementes lidas, reprova com PROTOCOLO_ILEGIVEL nomeando a semente e o campo; o
arquivo ausente termina com CONFIGURACAO. Os casos de campo ausente e de campo desconhecido
saem do esquema declarado na gramática, não de uma lista daqui.

A regravação da planilha de aderência, num diretório temporário, conserva as colunas
manuais, omite a linha vazia de semente ou de base que deixou de existir e recusa, com o
arquivo intacto, a que perderia preenchimento (semente renumerada, linha sem par, coluna
fora do esquema).

Dado não obtido ou juízo não feito (DOI ausente, facetas vazias, validação sem âncora) não
reprova: a cópia tem de ser aprovada e `projeto pendencias` tem de relatá-la. A evidência
bruta de semente inexistente reprova `dados conferir`."""

import contextlib
import csv
import hashlib
import io
import pathlib
import tempfile

from .. import gramatica as G
from ..config import Configuracao
from ..coerencia import conferir
from ..contexto import Contexto
from ..procedimentos import gera_base, registro_de_execucao
from ..dados import SUBPASTA_REFERENCIAS, pendencias_sementes, problemas_evidencia
from ..saida import Saida
from ..sementes import cmd_planilha, manuais
from . import resultado
from .textos import itens_toml, toml_de

P, R = Saida.PROTOCOLO_ILEGIVEL, Saida.REPROVADO
CHAVE = G.TT_SEMENTES.chave


def casos(ctx, g):
    texto, d = ctx.texto_sementes, ctx.protocolo()
    itens = itens_toml(texto, CHAVE)
    c_id, c_bases, c_papel = G.C_ID.chave, G.C_BASES.chave, G.C_PAPEL.chave
    c_ano, c_autores, c_doi = G.C_ANO.chave, G.C_AUTORES.chave, G.C_DOI.chave
    c_facetas = G.C_FACETAS.chave
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
        ("papel fora do domínio", com(-1, **{c_papel: "teste"}), P,
         (f"semente {ultimo}", "'teste' fora dos admitidos")),
        # Esquema estruturado: cada defeito, gerado das sementes lidas.
        ("ano como texto", com(-1, **{c_ano: str(itens[-1][c_ano])}), P,
         (f"semente {ultimo}", f"'{c_ano}' não é")),
        ("autores vazia", com(-1, **{c_autores: []}), P,
         (f"semente {ultimo}", f"'{c_autores}' vazio")),
        ("doi fora da forma", com(-1, **{c_doi: "DOI: " + (itens[-1].get(c_doi) or "x")}), P,
         (f"semente {ultimo}", f"'{c_doi}'", "fora da forma")),
        ("faceta fora da tabela", com(-1, **{c_facetas: [fora_da_tabela]}), P,
         (f"semente {ultimo}", fora_da_tabela)),
        ("faceta repetida", com(-1, **{c_facetas: [ids_facetas[0]] * 2}), P,
         (f"semente {ultimo}", f"{c_facetas} com repetição")),
        ("lacuna na numeração (semente do meio retirada)",
         toml_de(itens[:meio] + itens[meio + 1:], CHAVE), P,
         ("fora da numeração", f"{itens[meio + 1][c_id]} onde se esperava {itens[meio][c_id]}")),
        ("campo `semente` do esquema intermediário", com(-1, semente="Autor (2000). Título."), P,
         (f"semente {ultimo}", "campo desconhecido", "semente")),
        ("campo retirado `escopo`", com(-1, escopo=""), P,
         (f"semente {ultimo}", "campo desconhecido", "escopo")),
        ("conjunto-semente sem validação",
         toml_de([{**x, c_papel: G.PAPEL_DESENVOLVIMENTO} for x in itens], CHAVE), R,
         "sem semente de validação"),
    ]
    for nome, mutante, codigo, trecho in casos_:
        g.espera(nome, mutante, texto, executa, codigo, trecho)

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
    _planilha(ctx, g, itens, d)


def _aprovam_com_pendencia(ctx, g, itens, com, d):
    """Dado ou juízo pendente: a cópia é aprovada e `projeto pendencias` a relata, nomeando a
    semente. Cópia reprovada, ou pendência não relatada, faz o autoteste falhar."""
    c_id, c_papel, c_facetas = G.C_ID.chave, G.C_PAPEL.chave, G.C_FACETAS.chave
    ancoras = d["ancoras"]
    nao_ancoras = [f["id"] for f in d["facetas"] if f["id"] not in ancoras]
    k_val = next((k for k, x in enumerate(itens) if x[c_papel] == G.PAPEL_VALIDACAO), None)

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
    aprova_e_relata("doi ausente", com(0, doi=None), ident, "DOI ausente")
    aprova_e_relata("facetas vazias", com(0, **{c_facetas: []}), ident, "facetas a informar")
    if k_val is None or not nao_ancoras:
        g.nao_executa(3, "sem semente de validação ou sem faceta que não seja âncora")
        return
    ident = itens[k_val][c_id]
    aprova_e_relata("semente de validação sem faceta âncora",
                    com(k_val, **{c_facetas: nao_ancoras[:1]}), ident, "sem faceta âncora")
    # Prova de que a pendência discrimina: com uma âncora, não se relata.
    aprova_e_relata("semente de validação com faceta âncora",
                    com(k_val, **{c_facetas: ancoras[:1]}), ident, "sem faceta âncora",
                    relata=False)
    # Com facetas vazias, só "facetas a informar": a falta de âncora não se relata à parte.
    aprova_e_relata("semente de validação sem facetas",
                    com(k_val, **{c_facetas: []}), ident, "sem faceta âncora",
                    relata=False)


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


def _planilha(ctx, g, itens, d):
    """Regravação da planilha de aderência num diretório temporário: o preenchimento
    manual é conservado; a regravação que o perderia é recusada com o arquivo intacto.
    `id`, bases e títulos vêm das sementes lidas."""
    if len(itens) < 3:
        g.nao_executa(10,"menos de três sementes: sem semente do meio a retirar")
        return
    c_id = G.C_ID.chave
    bases = [b["sigla"] for b in d["bases"]]
    cols_m = manuais(d)
    primeiro, ultimo = itens[0][c_id], itens[-1][c_id]
    meio = len(itens) // 2

    with tempfile.TemporaryDirectory() as tmp:
        cfg = Configuracao(ctx.config.com("saidas.pasta", tmp), ctx.config.arquivo)
        cx = ctx.com_config(cfg)
        arq = cfg.saida("aderencia")

        def roda(c=cx):
            with contextlib.redirect_stdout(io.StringIO()):
                return resultado(lambda: cmd_planilha(c))

        def le():
            with arq.open(encoding="utf-8-sig", newline="") as f:
                r = csv.DictReader(f)
                return list(r.fieldnames), list(r)

        def grava(cab, linhas):
            with arq.open("w", encoding="utf-8-sig", newline="") as f:
                w = csv.DictWriter(f, fieldnames=cab)
                w.writeheader()
                w.writerows(linhas)

        def preenche(ident, base, valores):
            cab, linhas = le()
            for x in linhas:
                if x["id"] == ident and x["base"] == base:
                    x.update(valores)
            grava(cab, linhas)

        def linha(ident, base):
            return next((x for x in le()[1] if x["id"] == ident and x["base"] == base), {})

        def sha():
            return hashlib.sha256(arq.read_bytes()).hexdigest()

        def recusa(nome, c, trechos, codigo=R):
            antes = sha()
            cod, msgs = roda(c)
            faltam = [t for t in trechos if not any(t in m for m in msgs)]
            intacto = sha() == antes
            g.testa(f"regravação recusada ({codigo.name}), arquivo intacto: {nome}",
                    cod == codigo and not faltam and intacto,
                    f"{cod.name}, faltam {faltam}, intacto={intacto} {msgs[:1]}")

        # Primeira geração: colunas manuais vazias.
        cod, msgs = roda()
        linhas = le()[1] if arq.exists() else []
        g.testa("planilha de aderência gerada sem anterior, com as colunas manuais vazias",
                cod == Saida.OK and len(linhas) == len(itens) * len(bases)
                and not any(x[c] for x in linhas for c in cols_m), f"{cod.name} {msgs[:1]}")
        if not arq.exists():
            return

        # Preservação: todas as colunas manuais de primeiro × primeira base.
        valores = {c: f"{c} {primeiro} autoteste" for c in cols_m}
        preenche(primeiro, bases[0], valores)
        cod, msgs = roda()
        conservado = {c: linha(primeiro, bases[0]).get(c) for c in cols_m}
        g.testa(f"regravação conserva as colunas manuais ({primeiro} × {bases[0]})",
                cod == Saida.OK and conservado == valores, f"{cod.name} {conservado}")

        # Coluna derivada atualizada, manuais conservadas.
        c_tipo = G.C_TIPO.chave
        novo_tipo = f"{itens[0].get(c_tipo) or ''} autoteste".strip()
        mudado = [dict(x) for x in itens]
        mudado[0][c_tipo] = novo_tipo
        cod, msgs = roda(cx.com_sementes(toml_de(mudado, CHAVE)))
        x = linha(primeiro, bases[0])
        g.testa(f"regravação traz o tipo novo de {primeiro} e conserva as manuais",
                cod == Saida.OK and x.get("tipo") == novo_tipo
                and {c: x.get(c) for c in cols_m} == valores, f"{cod.name} {msgs[:1]}")
        roda()

        # Semente do meio retirada, as seguintes renumeradas: o id da retirada passa a
        # outro estudo, e o preenchimento não pode migrar para ele.
        alvo_id, alvo_base = itens[meio][c_id], bases[-1]
        preenche(alvo_id, alvo_base, {cols_m[0]: f"{cols_m[0]} {alvo_id} autoteste"})
        renumeradas = [dict(x, **{c_id: f"{G.I_SE.prefixo}{k + 1}"})
                       for k, x in enumerate(itens[:meio] + itens[meio + 1:])]
        recusa(f"semente renumerada ({alvo_id} × {alvo_base})",
               cx.com_sementes(toml_de(renumeradas, CHAVE)),
               (f"{alvo_id} × {alvo_base}", cols_m[0], itens[meio][G.C_TITULO.chave],
                "título divergente"))
        preenche(alvo_id, alvo_base, {cols_m[0]: ""})

        # Última semente retirada: linha sem par com preenchimento é recusada; vazia, omitida.
        sem_ultimo = cx.com_sementes(toml_de(itens[:-1], CHAVE))
        preenche(ultimo, bases[0], {cols_m[-1]: f"{cols_m[-1]} {ultimo} autoteste"})
        recusa(f"linha sem par com preenchimento ({ultimo} × {bases[0]})", sem_ultimo,
               (f"{ultimo} × {bases[0]}", cols_m[-1], "sem par"))
        preenche(ultimo, bases[0], {cols_m[-1]: ""})
        cod, msgs = roda(sem_ultimo)
        g.testa(f"linha sem par e vazia omitida ({ultimo})",
                cod == Saida.OK and not any(x["id"] == ultimo for x in le()[1]),
                f"{cod.name} {msgs[:1]}")
        roda()

        # Base que deixou de existir: a linha vazia dela é omitida, sem recusa.
        cab, linhas = le()
        retirada = next(n for n in (f"base_autoteste_{k}" for k in range(1000))
                        if n not in bases)
        grava(cab, linhas + [dict(linhas[0], base=retirada, **{c: "" for c in cols_m})])
        cod, msgs = roda()
        g.testa(f"linha vazia de base que deixou de existir omitida ({primeiro} × {retirada})",
                cod == Saida.OK and not any(x["base"] == retirada for x in le()[1]),
                f"{cod.name} {msgs[:1]}")
        grava(cab, linhas)

        # Coluna fora do esquema: vazia, é descartada; com valor, recusa.
        cab, linhas = le()
        extra = next(n for n in (f"coluna_autoteste_{k}" for k in range(1000)) if n not in cab)
        grava(cab + [extra], [dict(x, **{extra: ""}) for x in linhas])
        cod, msgs = roda()
        g.testa("coluna fora do esquema vazia é descartada",
                cod == Saida.OK and extra not in le()[0], f"{cod.name} {msgs[:1]}")
        cab, linhas = le()
        grava(cab + [extra], [dict(x, **{extra: f"{x['id']} autoteste" if k == 0 else ""})
                              for k, x in enumerate(linhas)])
        recusa(f"coluna fora do esquema com valor ({extra})", cx,
               (f"{linhas[0]['id']} × {linhas[0]['base']}", extra, "fora do esquema"))

        # Planilha anterior ilegível: DADOS, sem regravar.
        arq.write_bytes(b"\xff\xfe\x00" + bytes(range(128, 256)))
        recusa("planilha anterior ilegível", cx, (arq.name, "ilegível"), Saida.DADOS)
