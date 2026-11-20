"""Autoteste do arquivo de sementes: cada defeito do arquivo, injetado numa cópia em memória
gerada das sementes lidas, reprova com PROTOCOLO_ILEGIVEL nomeando a semente e o campo; o
arquivo ausente termina com CONFIGURACAO. Os casos de campo ausente e de campo desconhecido
saem do esquema declarado na gramática, não de uma lista daqui.

Dado não obtido ou juízo não feito (DOI ausente, facetas vazias, validação sem âncora) não
reprova: a cópia tem de ser aprovada e `pendencias` tem de relatá-la. A evidência bruta de
semente inexistente reprova `conferir-dados`."""

import pathlib
import tempfile

from .. import gramatica as G
from ..config import Configuracao
from ..conferencia import conferir
from ..contexto import Contexto
from ..dados import SUBPASTA_REFERENCIAS, pendencias_sementes, problemas_evidencia
from ..saida import Saida
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


def _aprovam_com_pendencia(ctx, g, itens, com, d):
    """Dado ou juízo pendente: a cópia é aprovada e `pendencias` a relata, nomeando a
    semente. Cópia reprovada, ou pendência não relatada, faz o autoteste falhar."""
    c_id, c_papel, c_facetas = G.C_ID.chave, G.C_PAPEL.chave, G.C_FACETAS.chave
    ancoras = d["ancoras"]
    nao_ancoras = [f["id"] for f in d["facetas"] if f["id"] not in ancoras]
    k_val = next((k for k, x in enumerate(itens) if x[c_papel] == G.PAPEL_VALIDACAO), None)

    def aprova_e_relata(nome, mutante, ident, trecho, relata=True):
        cod, msgs = resultado(lambda: conferir(ctx.com_sementes(mutante)))
        if cod != Saida.OK:
            g.falha(f"{nome}: a cópia devia ser aprovada — {cod.name} {msgs[:1]}")
            return
        linhas = pendencias_sementes(ctx.com_sementes(mutante).protocolo())
        achou = any(f"semente {ident} " in l and trecho in l for l in linhas)
        g.testa(f"aprova com pendência{'' if relata else ' (sem relato)'}: {nome}",
                achou == relata,
                f"`pendencias` {'não relatou' if relata else 'relatou'} {ident} com "
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
    """Evidência `SEn_…` de semente que não está no arquivo reprova `conferir-dados`,
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
