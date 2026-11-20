"""Busca: registro das execuções, derivação local das expressões não executadas, aderência
ao conjunto-semente, teste de fidelidade e sonda de sensibilidade.

Executa-se nas bases a expressão que o protocolo declara executada, uma vez por base; a
sonda, uma única vez, para medir o custo em recall da executada. As demais expressões que a
composição prova contidas na executada são calculadas aqui, sobre a exportação dela. A
composição, a executada, a sonda, o recorte e os limiares vêm do protocolo (`mostrar`
exibe os valores em uso).

O que este pacote NÃO faz: não exclui registro algum, não decide inclusão e não substitui
o teste de fidelidade. As contagens que produz são DERIVADAS e devem ser declaradas como tal
nas contagens da busca e no relatório.

Entradas (caminhos do config.toml): o protocolo; o registro de execuções (`[dados]
registro`), escrito por `busca registrar`; o arquivo de sementes (`[dados] sementes`); o
arquivo de cada execução registrada, intacto, onde estiver.

Saídas (`[saidas]` do config.toml): registros, contagens da busca, ordem de triagem,
fidelidade por expressão e sensibilidade por base.

Deduplicação: registro com o mesmo DOI — ou, na falta dele, o mesmo título normalizado — é
marcado em `duplicata_de` com o identificador da primeira ocorrência. Nada é apagado; as
contagens usam os registros únicos e o número bruto sai ao lado.
"""

import datetime

from .. import gramatica as G
from ..erros import Reprovado, Uso
from .composicao import derivaveis, grupos_em_facetas, prova_da_composicao


class Busca:
    """O que a busca usa do protocolo e da configuração, lido uma vez por subcomando."""

    def __init__(self, ctx):
        d = ctx.protocolo()
        self.ctx, self.config, self.d = ctx, ctx.config, d
        self.faceta_de = {v["id"]: fid for fid, v in d["strings"].items()}
        self.grupos = grupos_em_facetas(d["expressoes"], self.faceta_de)
        self.executada = d["executada"]
        self.sonda = d["sonda"]
        self.ancoras = {f["id"] for f in d["facetas"] if f.get("ancora")}
        # Recorte temporal do protocolo, aplicado como CONFERÊNCIA: o filtro de ano vai na
        # consulta ou no filtro da página de cada base, e esta etapa não deveria retirar
        # registro. Registro sem ano legível NÃO é descartado. Sem teto declarado, o limite
        # superior é o ano corrente.
        self.ano_min = int(d["recorte"]["ano_min"])
        self.ano_max = int(d["recorte"]["ano_max"] or datetime.date.today().year)
        self.limite_divergencia = float(d["divergencia"])
        self.limite_sensibilidade = tuple(d["sensibilidade"])
        # Sigla da tabela de bases: chave de linha de comando e nome nas saídas; BDn: chave
        # do registro de execuções.
        self.sigla_de_bd = {b["id"]: b["sigla"] for b in d["bases"]}
        self.bd_de = {b["sigla"]: b["id"] for b in d["bases"]}
        self.registro = self.config.caminho("dados.registro")
        problemas = prova_da_composicao(self.grupos, d["papeis"], self.faceta_de)
        if problemas:
            raise Reprovado("composição das expressões incoerente: " + "; ".join(problemas))
        self.derivaveis = derivaveis(self.grupos, self.executada, self.faceta_de.values())

    def bd(self, base):
        """(BDn, sigla) da base pedida pela sigla ou pelo identificador; (None, texto) se
        não for nenhum dos dois."""
        s = str(base or "").strip()
        if s in self.bd_de:
            return self.bd_de[s], s
        if s.upper() in self.sigla_de_bd:
            return s.upper(), self.sigla_de_bd[s.upper()]
        return None, s

    def exige_bd(self, base):
        bd, sigla = self.bd(base)
        if bd is None:
            raise Uso(f"Base inválida: {base!r}. Use {self.bases_validas()} (tabela de bases "
                      f"do protocolo).")
        return bd, sigla

    def bases_validas(self):
        return (f"siglas {', '.join(self.bd_de)} ou identificadores "
                f"{', '.join(self.sigla_de_bd)}")

    def expressoes_validas(self):
        """Primeira e última da composição lida, na ordem declarada."""
        ids = list(self.grupos)
        return f"{ids[0]} a {ids[-1]}" if len(ids) > 1 else ids[0]

    def id_expressao(self, expr):
        """Identificador da expressão a partir de `EBn`, da inicial seguida do número ou só
        do número; None se não existir."""
        s = str(expr).strip().upper()
        for prefixo in (G.I_EB.prefixo, G.I_EB.prefixo[0]):
            if s.startswith(prefixo):
                s = s[len(prefixo):]
                break
        if not s.isdigit():
            return None
        ident = f"{G.I_EB.prefixo}{int(s)}"
        return ident if ident in self.grupos else None

    def exige_expressao(self, expr):
        ident = self.id_expressao(expr)
        if ident is None:
            raise Uso(f"Expressão inválida: {expr!r}. Use {self.expressoes_validas()}.")
        return ident
