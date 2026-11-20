"""Autoteste do arquivo de sementes: cada defeito do arquivo, injetado numa cópia em memória
gerada das sementes lidas, reprova com PROTOCOLO_ILEGIVEL nomeando a semente e o campo; o
arquivo ausente termina com CONFIGURACAO. Os casos de campo ausente e de campo desconhecido
saem do esquema declarado na gramática, não de uma lista daqui."""

from .. import gramatica as G
from ..config import Configuracao
from ..conferencia import conferir
from ..contexto import Contexto
from ..saida import Saida
from . import resultado
from .textos import itens_toml, toml_de

P, R = Saida.PROTOCOLO_ILEGIVEL, Saida.REPROVADO
CHAVE = G.TT_SEMENTES.chave


def casos(ctx, g):
    texto, d = ctx.texto_sementes, ctx.protocolo()
    itens = itens_toml(texto, CHAVE)
    c_id, c_bases, c_papel = G.C_ID.chave, G.C_BASES.chave, G.C_PAPEL.chave
    primeiro, ultimo = itens[0][c_id], itens[-1][c_id]

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
    for c in G.TT_SEMENTES.campos:
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
         (f"semente {ultimo}", "base repetida")),
        ("papel fora do domínio", com(-1, **{c_papel: "teste"}), P,
         (f"semente {ultimo}", "'teste' fora dos admitidos")),
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
