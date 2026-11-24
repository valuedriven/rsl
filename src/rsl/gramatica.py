"""Gramática do protocolo, da fonte do procedimento de busca de cada base, do arquivo de
sementes, do arquivo de exceções de flexão e do resultado de sondagem: a única fonte dos
literais de forma. Declara também o esqueleto e o texto fixo do procedimento gerado.

Cada elemento declara o que o leitor exige de um documento — seção, tabela, coluna, rótulo
de linha, marcador, forma de identificador, frase-padrão de onde se lê um parâmetro, domínio
de valores. Os leitores recebem o elemento, não o literal, e a reprovação nomeia o elemento
com o mesmo rótulo que `python3 -m rsl documentos gramatica` exibe.

A gramática descreve a FORMA. Valor do projeto — sigla de base, faceta existente, limiar,
idioma, composição — não entra aqui: vem do protocolo ou do `config.toml`.

Nível de exigência:
  exigido   ausente ou fora da forma, a leitura reprova com PROTOCOLO_ILEGIVEL;
  opcional  ausente, vale o padrão do config.toml ou a ausência é relatada pela conferência;
            presente e fora da forma, reprova com PROTOCOLO_ILEGIVEL.

O autoteste percorre os elementos exigidos e, para cada um, gera uma cópia sem ele ou com
ele deformado: elemento exigido sem gerador de defeito faz o autoteste falhar.
"""

import re

PROTOCOLO = "protocolo"
FONTE = "fonte do procedimento de busca"
SEMENTES = "arquivo de sementes"
FLEXOES = "arquivo de exceções de flexão"
SONDAGEM = "resultado de sondagem no registro de execução"
DOCUMENTOS = (PROTOCOLO, FONTE, SEMENTES, FLEXOES, SONDAGEM)
# O procedimento de busca de cada base é saída de geração: não tem grupo no contrato.
PROCEDIMENTO = "procedimento de busca"

EXIGIDO = "exigido"
OPCIONAL = "opcional"

ELEMENTOS = []


class Elemento:
    tipo = "elemento"

    def __init__(self, nome, documento, exigencia, descricao, secao=None):
        self.nome = nome
        self.documento = documento
        self.exigencia = exigencia
        self.descricao = descricao
        self.secao = secao
        ELEMENTOS.append(self)

    @property
    def rotulo(self):
        return f"{self.tipo} {self.nome}"

    @property
    def exigido(self):
        return self.exigencia == EXIGIDO

    def forma(self):
        return ""


class Secao(Elemento):
    """Cabeçalho Markdown `#…# titulo`, no nível declarado. O texto da seção vai até o
    próximo cabeçalho de nível igual ou maior."""

    tipo = "seção"

    def __init__(self, nome, documento, titulo, nivel, exigencia=EXIGIDO, pai=None,
                 descricao=""):
        self.titulo = titulo
        self.nivel = nivel
        self.pai = pai
        super().__init__(nome, documento, exigencia,
                         descricao or "cabeçalho ausente, ou em outro nível, reprova",
                         secao=pai)

    @property
    def rotulo(self):
        return f"seção '{self.titulo}'"

    def forma(self):
        caminho = f"{self.pai.titulo} › " if self.pai else ""
        return f"{'#' * self.nivel} {self.titulo}   ({caminho}{self.titulo}, nível {self.nivel})"


class Tabela(Elemento):
    """Tabela Markdown da seção. `por_nome`: colunas lidas pelo cabeçalho (coluna exigida
    ausente ou repetida reprova; coluna extra é ignorada). `exato`: cabeçalho exatamente
    igual, na ordem. `posicional`: colunas lidas pela posição; os nomes são descritivos."""

    tipo = "tabela"

    def __init__(self, nome, documento, secao, colunas, modo="por_nome",
                 exigencia=EXIGIDO, descricao="", linhas=""):
        self.colunas = tuple(colunas)
        self.modo = modo
        self.linhas = linhas
        super().__init__(nome, documento, exigencia, descricao, secao=secao)

    @property
    def rotulo(self):
        return f"tabela '{self.secao.titulo}'" if self.nome == self.secao.nome else \
            f"tabela '{self.secao.titulo}' ({self.nome})"

    def forma(self):
        modo = {"por_nome": "colunas exigidas, lidas pelo nome; extra é ignorada",
                "exato": "cabeçalho exatamente este, na ordem",
                "posicional": "colunas lidas pela posição"}[self.modo]
        cab = " | ".join(c or "(sem nome)" for c in self.colunas)
        extra = f"; linhas: {self.linhas}" if self.linhas else ""
        return f"| {cab} |   ({modo}{extra})"


class RotuloLinha(Elemento):
    """Rótulo da primeira célula de uma linha de tabela; casa pelo início do texto."""

    tipo = "rótulo de linha"

    def __init__(self, nome, documento, tabela, texto, interno, exigencia=EXIGIDO,
                 descricao=""):
        self.tabela = tabela
        self.texto = texto
        self.interno = interno
        super().__init__(nome, documento, exigencia, descricao, secao=tabela.secao)

    @property
    def rotulo(self):
        return f"rótulo de linha '{self.texto}' da {self.tabela.rotulo}"

    def forma(self):
        return f"| {self.texto}… | …   (lido como `{self.interno}`)"


class Marcador(Elemento):
    """Marcador de linha ou de parágrafo de onde se lê um valor."""

    tipo = "marcador"

    def __init__(self, nome, documento, secao, texto, padrao, exigencia=EXIGIDO,
                 descricao=""):
        self.texto = texto
        self.padrao = re.compile(padrao, re.M)
        super().__init__(nome, documento, exigencia, descricao, secao=secao)

    @property
    def rotulo(self):
        return f"marcador '{self.texto}'"

    def forma(self):
        return self.texto


class Identificador(Elemento):
    """Forma de identificador: prefixo seguido de número, em sequência a partir de 1."""

    tipo = "identificador"

    def __init__(self, nome, documento, secao, prefixo, exigencia=EXIGIDO, descricao="",
                 sequencia=True):
        self.prefixo = prefixo
        self.sequencia = sequencia
        self.padrao = re.compile(rf"{prefixo}(\d+)")
        super().__init__(nome, documento, exigencia, descricao, secao=secao)

    @property
    def rotulo(self):
        return f"identificador {self.prefixo}n"

    def forma(self):
        seq = ", numerado em sequência a partir de 1, sem lacuna" if self.sequencia else ""
        return f"{self.prefixo}n{seq}"

    def casa(self, texto):
        return re.fullmatch(self.padrao, texto)


class FrasePadrao(Elemento):
    """Frase de onde se lê um parâmetro ou uma estrutura; `padrao` é a expressão regular."""

    tipo = "frase-padrão"

    def __init__(self, nome, documento, secao, texto, padrao, exigencia=EXIGIDO,
                 descricao="", flags=re.M):
        self.texto = texto
        self.padrao = re.compile(padrao, flags)
        super().__init__(nome, documento, exigencia, descricao, secao=secao)

    @property
    def rotulo(self):
        return f"frase-padrão '{self.texto}'"

    def forma(self):
        return self.texto


class Dominio(Elemento):
    """Valores admitidos de um campo; `valores` leva o texto do documento ao valor interno."""

    tipo = "domínio"

    def __init__(self, nome, documento, secao, campo, valores, exigencia=EXIGIDO,
                 descricao=""):
        self.campo = campo
        self.valores = dict(valores)
        super().__init__(nome, documento, exigencia,
                         descricao or "valor fora do domínio, ou vazio, reprova", secao=secao)

    @property
    def rotulo(self):
        return f"domínio de '{self.campo}'"

    def forma(self):
        return " | ".join(self.valores)


class TabelaToml(Elemento):
    """Tabela de tabelas TOML (`[[nome]]`), uma por item; o esquema dos campos é fechado."""

    tipo = "tabela TOML"

    def __init__(self, nome, documento, chave, exigencia=EXIGIDO, descricao=""):
        self.chave = chave
        self.campos = []
        super().__init__(nome, documento, exigencia, descricao)

    @property
    def rotulo(self):
        return f"tabela TOML [[{self.chave}]]"

    def forma(self):
        return f"[[{self.chave}]]   (campos: {', '.join(c.chave for c in self.campos)}; " \
               f"campo fora do esquema reprova)"


class CampoToml(Elemento):
    """Campo de um item de uma tabela TOML: nome, tipo e exigência."""

    tipo = "campo"
    TIPOS = {"texto": str, "lista de textos": list, "inteiro": int}

    def __init__(self, nome, documento, tabela, chave, tipo_valor, exigencia=EXIGIDO,
                 descricao=""):
        self.tabela = tabela
        self.chave = chave
        self.tipo_valor = tipo_valor
        tabela.campos.append(self)
        super().__init__(nome, documento, exigencia, descricao)

    @property
    def rotulo(self):
        return f"campo '{self.chave}' de [[{self.tabela.chave}]]"

    def forma(self):
        return f"{self.chave} = <{self.tipo_valor}>"

    def aceita(self, valor):
        tipo = self.TIPOS[self.tipo_valor]
        # bool é subclasse de int no Python; no TOML, `true` não é número.
        if not isinstance(valor, tipo) or isinstance(valor, bool):
            return False
        return tipo is not list or all(isinstance(x, str) for x in valor)


# ======================================================================== protocolo
P = PROTOCOLO

S_QUESTAO = Secao("questao", P, "Questão de revisão", 2)
S_QGR = Secao("questao_geral", P, "Questão geral de revisão", 3, pai=S_QUESTAO)
S_QER = Secao("questoes_especificas", P, "Questões específicas de revisão", 3, pai=S_QUESTAO)
M_QGR = Marcador("qgr", P, S_QGR, "- QGR: <questão geral>", r"^-\s*QGR:\s*(.+)$",
                 descricao="primeiro parágrafo da seção; sem o marcador, reprova")
M_ESTRUTURA = Marcador(
    "estrutura", P, S_QGR, "[A] estrutura da questão…  (sem distinção de caixa)",
    r"(?i)^(?:a\s+)?estrutura da questão",
    descricao="parágrafo iniciado pelo marcador, que declara a estrutura (PICo); ausente, "
              "reprova")
I_QER = Identificador("qer", P, S_QER, "QER",
                      descricao="item `- QERn: <questão>`; fora da sequência, reprova")
F_QER = FrasePadrao("questao_especifica", P, S_QER, "- QERn: <questão>",
                    r"^-\s*(QER\d+):\s*(.+)$")

S_FACETAS = Secao("facetas", P, "Facetas da questão de revisão", 2)
T_FACETAS = Tabela(
    "facetas", P, S_FACETAS, ("Id faceta", "Faceta", "Âncora obrigatória"), modo="exato",
    linhas="uma por faceta: `| FCTn | <nome> | Sim/Não |`",
    descricao="cabeçalho diferente, nome vazio e tabela sem nenhuma âncora reprovam (sem "
              "âncora, a sonda não seria identificável)")
I_FCT = Identificador("fct", P, S_FACETAS, "FCT")
# Valor do documento, sem distinção de caixa → a faceta é âncora obrigatória.
D_ANCORA = Dominio("ancora", P, S_FACETAS, "Âncora obrigatória", {"Sim": True, "Não": False},
                   descricao="Sim ou Não, sem distinção de caixa; vazio ou outro valor "
                             "reprova")

S_INSTRUMENTOS = Secao("instrumentos", P, "Instrumentos para controle terminológico", 2)
T_INSTRUMENTOS = Tabela(
    "instrumentos", P, S_INSTRUMENTOS,
    ("Sigla", "Instrumento", "Modo", "Caminho", "Idiomas", "FCTs"),
    descricao="campo vazio, sigla repetida, Caminho que não é URL http(s), idioma fora do "
              "quadro, faceta inexistente e faceta sem instrumento reprovam")
D_MODO = Dominio("modo", P, S_INSTRUMENTOS, "Modo",
                 {"Manual": "Manual", "Automático": "Automático"},
                 descricao="Automático exige cliente com o nome da sigla; fora do domínio "
                           "reprova")
MODO_MANUAL, MODO_AUTOMATICO = D_MODO.valores

S_CONTROLE = Secao("controle", P, "Controle terminológico", 2)
T_QUADRO = Tabela(
    "quadro", P, S_CONTROLE, ("FCTn", "<idioma>", "…"), modo="por_nome",
    linhas="uma linha por camada; termos separados por vírgula",
    descricao="uma tabela por faceta, com o identificador na primeira célula do cabeçalho; "
              "as demais células nomeiam os idiomas, os mesmos em todas as tabelas, em "
              "qualquer ordem; célula com o separador antigo `\\- ` reprova")
SEPARADOR_TERMOS = r"\s*,\s*"
# Forma antiga da lista de termos (`\- termo \- termo`): reprova, em vez de virar um termo só.
SEPARADOR_ANTIGO = r"(?:^|\s)\\-\s"
R_NUCLEO = RotuloLinha("nucleo", P, T_QUADRO, "Termos centrais", "nucleo",
                       descricao="linha ausente reprova; célula vazia é reprovada pela "
                                 "conferência")
R_PROXIMOS = RotuloLinha("proximos", P, T_QUADRO, "Descritores potenciais", "proximos",
                         descricao=R_NUCLEO.descricao)
R_RELACIONADOS = RotuloLinha("relacionados", P, T_QUADRO, "Termos relacionados",
                             "relacionados", descricao=R_NUCLEO.descricao)
CAMADAS = (R_NUCLEO, R_PROXIMOS, R_RELACIONADOS)

S_STRINGS = Secao("strings", P, "Strings de busca por faceta", 2)
T_STRINGS = Tabela("strings", P, S_STRINGS, ("ID String", "Faceta", "String"),
                   modo="posicional", linhas="uma por faceta: `| STRn | FCTn | (…) |`")
I_STR = Identificador("str", P, S_STRINGS, "STR", sequencia=False,
                      descricao="STRn tem de ser da faceta FCTn; uma string por faceta")
F_STRING = FrasePadrao("string", P, S_STRINGS, '("termo" OR "termo" OR …)',
                       r'"([^"]+)"',
                       descricao="termos entre aspas ligados por OR; resíduo fora desse "
                                 "padrão reprova")

S_EXPRESSOES = Secao("expressoes", P, "Expressões de busca", 2)
T_EXPRESSOES = Tabela(
    "expressoes", P, S_EXPRESSOES, ("ID", "Expressão de busca", "Função protocolar"),
    modo="exato",
    descricao="cabeçalho diferente reprova: as colunas são lidas pela posição. A Função "
              "protocolar é texto livre; dela só se extraem as referências (Nn). Executada e "
              "sonda são identificadas pela composição: nenhuma ou mais de uma candidata "
              "reprova")
I_EB = Identificador("eb", P, S_EXPRESSOES, "EB")
F_COMPOSICAO = FrasePadrao(
    "composicao", P, S_EXPRESSOES, "STRn AND STRn AND (STRn OR STRn)", r"STR\d+",
    descricao="AND em maiúsculas é a única conjunção; OR só entre parênteses, sem "
              "aninhamento; `+`, operador em minúscula ou OR fora de parênteses reprovam")
S_NOTAS = Secao("notas", P, "Notas explicativas", 3, exigencia=OPCIONAL, pai=S_EXPRESSOES,
                descricao="ausente, nenhuma nota; cabeçalho em outro nível reprova")
F_NOTA = FrasePadrao("nota", P, S_NOTAS, "- Nn — <texto>", r"^-\s*(N\d+)\s*—\s*(.+)$",
                     exigencia=OPCIONAL, descricao="nota repetida reprova")
F_REF_NOTA = FrasePadrao(
    "referencia_nota", P, S_EXPRESSOES, "(Nn)  na Função protocolar", r"\((N\d+)\)",
    exigencia=OPCIONAL,
    descricao="referência sem a nota correspondente reprova; nota não citada, não")
F_FAIXA = FrasePadrao(
    "faixa_sensibilidade", P, S_NOTAS, "< N% … > M%  (nas notas citadas pela executada)",
    r"(<|>)\s*\**\s*(\d+(?:[.,]\d+)?)\s*%", exigencia=OPCIONAL,
    descricao="sem os dois limites, vale `padroes.sensibilidade`; um sem o outro reprova")

S_CRITERIOS = Secao("criterios", P, "Critérios de elegibilidade", 3)
T_CRITERIOS = Tabela(
    "criterios", P, S_CRITERIOS,
    ("ID critério", "Dimensão", "Ação", "Critério", "", "Justificativa"), modo="posicional",
    linhas="Dimensão vazia herda a da linha anterior")
COL_CRIT_ID, COL_CRIT_DIMENSAO, COL_CRIT_ACAO, COL_CRIT_CRITERIO, _, COL_CRIT_JUST = \
    range(6)
I_CE = Identificador("ce", P, S_CRITERIOS, "CE")
# "Não aplicável": critério do modelo registrado só para documentação; não entra na seleção.
D_ACAO = Dominio("acao", P, S_CRITERIOS, "Ação",
                 {"Incluir": "Incluir", "Excluir": "Excluir", "Não aplicável": "Não aplicável"})
ACAO_INCLUIR, ACAO_EXCLUIR, ACAO_NAO_APLICAVEL = D_ACAO.valores
F_RECORTE = FrasePadrao(
    "recorte", P, S_CRITERIOS, "após o ano AAAA  (critério Incluir da dimensão do recorte)",
    r"após o ano\s+(\d{4})", exigencia=OPCIONAL,
    descricao="dimensão em `conferencia.dimensao_recorte`; sem o critério, vale "
              "`padroes.recorte_ano_min`; critério sem ano legível reprova")

S_FONTES = Secao("fontes", P, "Fontes de informação", 3)
S_BASES = Secao("bases", P, "Bases de dados", 4, pai=S_FONTES)
T_BASES = Tabela("bases", P, S_BASES, ("ID Base", "Sigla", "Nome da base"),
                 descricao="campo vazio, sigla repetida e sigla com caractere fora de "
                           "[A-Za-z0-9_-] reprovam; sigla sem fonte do procedimento de busca "
                           "reprova só aquela base")
I_BD = Identificador("bd", P, S_BASES, "BD")
F_ORDEM = FrasePadrao(
    "ordem_execucao", P, S_BASES, "Ordem de execução: <base>, <base> e <base>, nesta "
    "sequência.", r"Ordem de execução:\s*(.+?),?\s*nesta sequência\.?\s*",
    descricao="cada nome identifica uma só base pelo início do nome; ausente ou incompleta "
              "reprova")
MARCA_ORDEM = "Ordem de execução"
S_ACERVOS = Secao("acervos", P, "Acervos especiais", 4, pai=S_FONTES)
S_SEMENTES = Secao("sementes", P, "Conjunto-semente", 4, pai=S_FONTES)
M_REGRA = Marcador("regra_ajuste", P, S_SEMENTES, "Regra de ajuste", r"Regra de ajuste",
                   exigencia=OPCIONAL,
                   descricao="sem a regra, vale `padroes.limiar_aderencia`")
F_LIMIAR = FrasePadrao(
    "limiar_aderencia", P, S_SEMENTES, "recuperação inferior a N%  (na Regra de ajuste)",
    r"recuperação inferior a\s+(\d+(?:[.,]\d+)?)\s*%",
    descricao="exigida quando há Regra de ajuste: regra sem limiar legível reprova")

# ============================================================== arquivo de sementes
# O caminho do arquivo vem do config.toml (`[documentos] sementes`), não da gramática.
A = SEMENTES

TT_SEMENTES = TabelaToml(
    "sementes", A, "sementes",
    descricao="TOML inválido, tabela ausente ou vazia e campo desconhecido reprovam, "
              "nomeando a semente e o campo")


def _campo(chave, tipo_valor, descricao, exigencia=EXIGIDO):
    return CampoToml(f"sementes.{chave}", A, TT_SEMENTES, chave, tipo_valor,
                     exigencia=exigencia, descricao=descricao)


_OPC = "campo opcional: ausente equivale a vazio; presente e de outro tipo, reprova"
# Bibliográficos. A referência legível é montada destes campos; nada se extrai de texto.
C_ID = _campo("id", "texto", "ausente, de outro tipo, fora da forma SEn, repetido ou fora "
                             "da sequência a partir de SE1, sem lacuna, reprova")
C_AUTORES = _campo("autores", "lista de textos", "ausente, de outro tipo, vazia ou com "
                                                 "autor vazio reprova")
C_ANO = _campo("ano", "inteiro", "ausente ou de outro tipo (texto, por exemplo) reprova")
C_TITULO = _campo("titulo", "texto", "ausente, de outro tipo ou vazio reprova")
C_VEICULO = _campo("veiculo", "texto", "ausente, de outro tipo ou vazio reprova")
C_VOLUME = _campo("volume", "texto", _OPC, OPCIONAL)
C_NUMERO = _campo("numero", "texto", _OPC, OPCIONAL)
C_PAGINAS = _campo("paginas", "texto", _OPC, OPCIONAL)
C_DOI = _campo("doi", "texto", "campo opcional: ausente ou vazio vira pendência "
                               "(`projeto pendencias`); presente fora da forma 10.x/…, reprova",
               OPCIONAL)
# Aferição.
C_BASES = _campo("bases", "lista de textos",
                 "siglas das bases que indexam a semente (indexação, não recuperação); "
                 "lista vazia, base que não é sigla da tabela de bases do protocolo (grafia "
                 "exata) e base repetida reprovam")
C_FACETAS = _campo("facetas", "lista de textos",
                   "FCTn informadas pelo pesquisador (não do ensaio seco); faceta fora da "
                   "tabela de facetas ou repetida reprova; vazia vira pendência", OPCIONAL)
C_PAPEL = _campo("papel", "texto", "ausente ou de outro tipo reprova")
# Conferência: estado da referência e juízos do pesquisador.
C_VERIFICACAO = _campo("verificacao", "texto", _OPC, OPCIONAL)
C_TIPO = _campo("tipo", "texto", _OPC + "; vazio vira pendência", OPCIONAL)
C_ALINHAMENTO = _campo("alinhamento", "texto", _OPC + "; vazio vira pendência", OPCIONAL)
C_NOTA = _campo("nota", "texto", _OPC, OPCIONAL)
C_VEICULO_CONFERIDO = _campo("veiculo_conferido", "texto", _OPC, OPCIONAL)
C_ERIC = _campo("eric", "texto", _OPC, OPCIONAL)
# Sobra: o que a referência traz e não cabe em outro campo, transcrito como está.
C_OBSERVACOES = _campo("observacoes", "texto", _OPC, OPCIONAL)
CONFERENCIA = (C_VERIFICACAO, C_TIPO, C_ALINHAMENTO, C_NOTA, C_VEICULO_CONFERIDO, C_ERIC)

I_SE = Identificador("se", A, None, "SE", descricao="id fora da sequência reprova")
D_PAPEL = Dominio("papel", A, None, "papel",
                  {"desenvolvimento": "desenvolvimento", "validação": "validação"},
                  descricao="só a validação decide a passagem; vazio ou fora do domínio "
                            "reprova")
PAPEL_DESENVOLVIMENTO, PAPEL_VALIDACAO = D_PAPEL.valores
F_DOI = FrasePadrao("doi", A, None, "10.<prefixo>/<sufixo>  (no campo doi, sem `DOI:` nem "
                                    "URL)",
                    r"^10\.\d{4,9}/\S+$", exigencia=OPCIONAL,
                    descricao="doi presente fora da forma reprova")


# ======================================================== fonte do procedimento de busca
# O procedimento de busca de cada base (`[documentos] procedimento`) é SAÍDA de
# `procedimentos gerar` e não tem gramática de leitura. O que se lê e se edita é a fonte da
# base (`[documentos] procedimento_fonte`): `procedimento.toml`, de esquema fechado, e os
# fragmentos de prosa de nome fixo. Nenhum valor de base entra aqui: só a forma.
F = FONTE


class TabelaFonte(Elemento):
    """Tabela de um arquivo TOML de esquema fechado: `[chave]` (única) ou `[[chave]]`
    (lista de tabelas). `pai` é a tabela que a contém (`[[sondagens.consultas]]`). A raiz
    do arquivo é a tabela de chave vazia. Campo fora do esquema reprova."""

    tipo = "tabela"

    def __init__(self, nome, documento, chave, multipla=False, exigencia=EXIGIDO,
                 descricao="", pai=None, minimo=1):
        self.chave = chave
        self.multipla = multipla
        self.pai = pai
        self.minimo = minimo
        self.campos = []
        self.subtabelas = []
        if pai is not None:
            pai.subtabelas.append(self)
        super().__init__(nome, documento, exigencia, descricao)

    @property
    def local(self):
        """Nome da tabela dentro da que a contém (`consultas` em `sondagens.consultas`)."""
        return self.chave.rsplit(".", 1)[-1]

    @property
    def rotulo(self):
        if not self.chave:
            return "raiz do arquivo"
        return f"tabela [[{self.chave}]]" if self.multipla else f"tabela [{self.chave}]"

    def forma(self):
        campos = ", ".join(f"{c.chave}{'' if c.exigido else '?'}" for c in self.campos)
        subs = ", ".join(s.rotulo for s in self.subtabelas)
        minimo = f"; ao menos {self.minimo} item(ns)" if self.multipla and self.minimo else ""
        return (f"campos: {campos or '—'}{'; contém ' + subs if subs else ''}{minimo}; "
                f"`?` = opcional; campo fora do esquema reprova")


class CampoFonte(Elemento):
    """Campo de uma tabela de esquema fechado: tipo, exigência e, quando há, domínio."""

    tipo = "campo"
    TIPOS = ("texto", "lista de textos", "inteiro", "booleano", "tabela de listas",
             "inteiro ou texto", "texto ou tabela", "tabela", "lista de tabelas")

    def __init__(self, tabela, chave, tipo_valor, exigencia=EXIGIDO, dominio=None,
                 descricao=""):
        assert tipo_valor in self.TIPOS, tipo_valor
        self.tabela = tabela
        self.chave = chave
        self.tipo_valor = tipo_valor
        self.dominio = tuple(dominio) if dominio else None
        tabela.campos.append(self)
        nome = f"{tabela.chave or 'raiz'}.{chave}"
        super().__init__(nome, tabela.documento, exigencia, descricao)

    @property
    def rotulo(self):
        return f"campo '{self.chave}' da {self.tabela.rotulo}"

    def forma(self):
        dom = f" em {{{', '.join(self.dominio)}}}" if self.dominio else ""
        return f"{self.chave} = <{self.tipo_valor}>{dom}"

    def aceita(self, valor):
        """O valor tem o tipo declarado (o domínio se confere à parte)."""
        def texto(v):
            return isinstance(v, str)

        def lista(v):
            return isinstance(v, list) and all(isinstance(x, str) for x in v)

        def inteiro(v):
            return isinstance(v, int) and not isinstance(v, bool)
        t = self.tipo_valor
        if t == "texto":
            return texto(valor)
        if t == "lista de textos":
            return lista(valor)
        if t == "inteiro":
            return inteiro(valor)
        if t == "booleano":
            return isinstance(valor, bool)
        if t == "tabela de listas":
            return isinstance(valor, dict) and all(lista(v) for v in valor.values())
        if t == "inteiro ou texto":
            return inteiro(valor) or texto(valor)
        if t == "texto ou tabela":
            return texto(valor) or isinstance(valor, dict)
        if t == "tabela":
            return isinstance(valor, dict)
        if t == "lista de tabelas":
            return isinstance(valor, list) and all(isinstance(x, dict) for x in valor)
        return False


# Marca do que ainda não foi apurado: valor de campo ou linha de fragmento.
PENDENTE = "PENDENTE"

# Situação de um elemento de sintaxe, de uma regra de montagem e estado de uma leitura de
# sondagem. A leitura de estado `nao_verificado` é a leitura inconclusiva.
SITUACOES = ("oficial", "secundaria", "medicao", "nao_verificado", "inexistente")
SITUACAO_MEDICAO, SITUACAO_NAO_VERIFICADO = "medicao", "nao_verificado"
SITUACAO_TEXTO = {"oficial": "Verificado em fonte oficial",
                  "secundaria": "Verificado em fonte secundária",
                  "medicao": "Verificado por medição",
                  "nao_verificado": "**Não verificado**",
                  "inexistente": "**Não existe**"}
# Categorias mínimas: cada uma tem ao menos um elemento de sintaxe em toda base.
CATEGORIAS = ("campos", "operadores", "frase", "truncamento", "lematizacao", "proximidade",
              "agrupamento", "limite_consulta", "limite_retorno", "limite_exportacao",
              "filtros", "vocabulario_controlado", "idioma_indexacao", "exportacao")
CATEGORIA_LEMATIZACAO = "lematizacao"
CATEGORIA_TRUNCAMENTO = "truncamento"
DESTINOS = ("consulta", "ancora", "interface", "variante", "aproximado", "dispensado",
            "nao")
DESTINOS_COM_CLAUSULA = ("consulta", "variante")
DESTINO_CONSULTA = "consulta"
DESTINO_TEXTO = {"consulta": "**Sim**", "ancora": "**Sim**, por âncora",
                 "interface": "**No filtro da interface**", "variante": "Em variante",
                 "aproximado": "Aproximado", "dispensado": "**Dispensado**",
                 "nao": "**Não**"}
PAPEIS_CONSULTA = ("teste", "controle")
ESTATUTOS = ("executada", "sonda", "fidelidade", "derivada")
ESTATUTOS_COM_BLOCO = ("executada", "sonda", "fidelidade")

T_RAIZ = TabelaFonte("fonte", F, "", descricao="TOML inválido ou chave fora do esquema "
                                                "reprova a base")
C_RESSALVAS = CampoFonte(T_RAIZ, "ressalvas", "lista de textos", OPCIONAL,
                         descricao="§6, uma ressalva por item")

T_SINTAXE = TabelaFonte("fonte.sintaxe", F, "sintaxe", multipla=True,
                        descricao="§1, uma linha por elemento; toda categoria mínima tem "
                                  "ao menos um elemento")
CampoFonte(T_SINTAXE, "elemento", "texto", descricao="nome repetido reprova")
D_CATEGORIA = CampoFonte(T_SINTAXE, "categoria", "texto", dominio=CATEGORIAS,
                         descricao="categoria sem elemento na base reprova")
CampoFonte(T_SINTAXE, "idioma", "texto", OPCIONAL,
           descricao="só na categoria `lematizacao`; idioma fora do quadro reprova")
D_SITUACAO = CampoFonte(T_SINTAXE, "situacao", "texto", dominio=SITUACOES,
                        descricao="`medicao` exige `citacao`; `nao_verificado` exige "
                                  "`sondagem` ou `sem_sondagem`")
CampoFonte(T_SINTAXE, "fonte", "texto", OPCIONAL, descricao="fonte da verificação ou da "
                                                            "ausência")
C_CITACAO = CampoFonte(T_SINTAXE, "citacao", "texto", OPCIONAL,
                       descricao="`BDn/<id>` da própria base; exigida em `medicao`; a "
                                 "existência do id é conferida por `dados conferir`")
CampoFonte(T_SINTAXE, "sondagem", "texto", OPCIONAL,
           descricao="`SDn` existente que lista o elemento")
CampoFonte(T_SINTAXE, "sem_sondagem", "texto", OPCIONAL,
           descricao="motivo de não haver sondagem")
CampoFonte(T_SINTAXE, "nota", "texto", OPCIONAL)

T_CRITERIOS_F = TabelaFonte("fonte.criterios", F, "criterios", multipla=True,
                            descricao="§2; o conjunto dos IDs tem de ser o do protocolo "
                                      "(conferência)")
CampoFonte(T_CRITERIOS_F, "ids", "lista de textos", descricao="CEn")
CampoFonte(T_CRITERIOS_F, "rotulo", "texto")
D_DESTINO = CampoFonte(T_CRITERIOS_F, "destino", "texto", dominio=DESTINOS,
                       descricao="`consulta` e `variante` exigem `clausula`")
CampoFonte(T_CRITERIOS_F, "como", "texto")
CampoFonte(T_CRITERIOS_F, "clausula", "texto", OPCIONAL,
           descricao="sintaxe literal do filtro; a de `consulta` é a única fonte dos "
                     "filtros dos blocos")

T_COBERTURA = TabelaFonte("fonte.cobertura", F, "cobertura",
                          descricao="§3, declaração de cobertura")
CampoFonte(T_COBERTURA, "idiomas", "tabela de listas",
           descricao="FCTn = [idiomas]; faceta ou idioma desconhecido reprova")
D_CAMADAS_F = CampoFonte(T_COBERTURA, "camadas", "texto", dominio=("todas", "nucleo"))
CAMADAS_TODAS, CAMADAS_NUCLEO = D_CAMADAS_F.dominio
PLURAL_EXPLICITO, PLURAL_LEMATIZACAO = "explícito", "pela lematização"
D_PLURAL_F = CampoFonte(T_COBERTURA, "plural", "texto ou tabela",
                        dominio=(PLURAL_EXPLICITO, PLURAL_LEMATIZACAO),
                        descricao="valor único, ou tabela por idioma cobrindo todos os "
                                  "idiomas da base; `pela lematização` exige elemento de "
                                  "`lematizacao` medido, com citação (conferir)")
TETO_NENHUM = "nenhum"
D_TETO_F = CampoFonte(T_COBERTURA, "teto", "inteiro ou texto", dominio=(TETO_NENHUM,),
                      descricao="inteiro positivo de caracteres ou `nenhum`")
DERIVACAO_MORFOLOGIA, DERIVACAO_RADICAL = "morfologia", "radical"
D_DERIVACOES_F = CampoFonte(T_COBERTURA, "derivacoes", "lista de textos", OPCIONAL,
                            dominio=(DERIVACAO_MORFOLOGIA, DERIVACAO_RADICAL))

T_REDUCAO = TabelaFonte("fonte.reducao", F, "reducao", multipla=True, exigencia=OPCIONAL,
                        minimo=0, descricao="§3, termo vigente fora dos blocos")
CampoFonte(T_REDUCAO, "faceta", "texto")
CampoFonte(T_REDUCAO, "termo", "texto")
CampoFonte(T_REDUCAO, "motivo", "texto",
           descricao="com `radical`, afirma alcance pela forma radical (conferido); com "
                     "`pendente`, lacuna em aberto")
MOTIVO_RADICAL = "radical"
MOTIVO_PENDENTE = "pendente"

T_COMPOSICAO = TabelaFonte("fonte.composicao", F, "composicao",
                           descricao="parâmetros de composição dos blocos")
D_ASPAS = CampoFonte(T_COMPOSICAO, "aspas", "texto", dominio=("todo_termo", "locucao"),
                     descricao="`locucao`: aspas só no termo com espaço ou hífen")
ASPAS_TODO_TERMO, ASPAS_LOCUCAO = D_ASPAS.dominio
D_PROXIMIDADE = CampoFonte(T_COMPOSICAO, "proximidade", "texto ou tabela",
                           dominio=("nenhum",),
                           descricao="`nenhum` ou {operador = \"NEAR\", distancia = 5}; "
                                     "com proximidade, as âncoras ficam no mesmo campo")
D_DISJUNCAO = CampoFonte(T_COMPOSICAO, "disjuncao", "texto",
                         dominio=("em_linha", "consultas_separadas"),
                         descricao="`consultas_separadas`: cada alternativa de um grupo "
                                   "com OR vira consulta própria")
DISJUNCAO_EM_LINHA, DISJUNCAO_SEPARADA = D_DISJUNCAO.dominio
T_COMP_FACETAS = TabelaFonte("fonte.composicao.facetas", F, "composicao.facetas",
                             multipla=True, pai=T_COMPOSICAO,
                             descricao="uma por faceta do protocolo")
CampoFonte(T_COMP_FACETAS, "faceta", "texto")
CampoFonte(T_COMP_FACETAS, "campo", "texto",
           descricao="texto literal do campo, como a base o escreve; vazio = sem campo")
D_FORMA_CAMPO = CampoFonte(T_COMP_FACETAS, "forma", "texto", dominio=("envolve", "prefixa"),
                           descricao="`envolve`: campo(grupo); `prefixa`: campo em cada termo")
FORMA_ENVOLVE, FORMA_PREFIXA = D_FORMA_CAMPO.dominio
CampoFonte(T_COMP_FACETAS, "rotulo", "texto", OPCIONAL,
           descricao="nome curto da faceta no rótulo das consultas separadas")
CampoFonte(T_COMP_FACETAS, "cor", "texto", OPCIONAL, descricao="marca da faceta no texto")

T_CONSULTAS_CAMPO = TabelaFonte("fonte.consultas_de_campo", F, "consultas_de_campo",
                                multipla=True, exigencia=OPCIONAL, minimo=0,
                                descricao="cada expressão executada vira uma consulta por "
                                          "entrada, rotulada `<n><letra>`")
CampoFonte(T_CONSULTAS_CAMPO, "letra", "texto")
CampoFonte(T_CONSULTAS_CAMPO, "faceta", "texto")
CampoFonte(T_CONSULTAS_CAMPO, "string", "texto", descricao="STRn ou id de subconjunto")
CampoFonte(T_CONSULTAS_CAMPO, "campo", "texto")
CampoFonte(T_CONSULTAS_CAMPO, "rotulo", "texto")

T_SUBCONJUNTOS = TabelaFonte("fonte.subconjuntos", F, "subconjuntos", multipla=True,
                             exigencia=OPCIONAL, minimo=0,
                             descricao="termo fora da STR da faceta, e não subsumido por "
                                       "ela, reprova")
T_RADICAL = TabelaFonte("fonte.radical", F, "radical", multipla=True, exigencia=OPCIONAL,
                        minimo=0, descricao="forma radical que substitui a STR da faceta")
for _t in (T_SUBCONJUNTOS, T_RADICAL):
    CampoFonte(_t, "id", "texto", descricao="`STRn` ou `STRn<letra>`")
    CampoFonte(_t, "faceta", "texto")
    CampoFonte(_t, "campo", "texto")
    CampoFonte(_t, "termos", "lista de textos")
    CampoFonte(_t, "rotulo", "texto")

T_EXECUCAO = TabelaFonte("fonte.execucao", F, "execucao", descricao="§4")
FORMAS_EXECUCAO = ("unica", "particionada", "curada")
FORMA_EXECUCAO_TEXTO = {"unica": "única", "particionada": "particionada",
                        "curada": "curada"}
D_EXECUCAO_F = CampoFonte(T_EXECUCAO, "forma", "texto", dominio=FORMAS_EXECUCAO,
                          descricao="sem padrão; `unica` com partição necessária reprova")
T_EXPRESSOES_F = TabelaFonte("fonte.execucao.expressoes", F, "execucao.expressoes",
                             multipla=True, pai=T_EXECUCAO,
                             descricao="uma por expressão do protocolo")
CampoFonte(T_EXPRESSOES_F, "id", "texto", descricao="EBn do protocolo")
CampoFonte(T_EXPRESSOES_F, "titulo", "texto", descricao="vai a `### EBn (<titulo>)`")
CampoFonte(T_EXPRESSOES_F, "estatuto", "texto", OPCIONAL, dominio=ESTATUTOS,
           descricao="só quando difere do papel lido do protocolo")

T_REGRAS = TabelaFonte("fonte.regras_de_montagem", F, "regras_de_montagem", multipla=True,
                       exigencia=OPCIONAL, minimo=0,
                       descricao="§4, \"Como esta base exige a montagem\"")
CampoFonte(T_REGRAS, "texto", "texto")
CampoFonte(T_REGRAS, "situacao", "texto", dominio=SITUACOES,
           descricao="as mesmas exigências da situação de [[sintaxe]]")
CampoFonte(T_REGRAS, "citacao", "texto", OPCIONAL)
CampoFonte(T_REGRAS, "sondagem", "texto", OPCIONAL)
CampoFonte(T_REGRAS, "sem_sondagem", "texto", OPCIONAL)

T_CURADAS = TabelaFonte("fonte.curadas", F, "curadas", multipla=True, exigencia=OPCIONAL,
                        minimo=0, descricao="exigida com `forma = \"curada\"`")
CampoFonte(T_CURADAS, "grupo", "texto")
CampoFonte(T_CURADAS, "consulta", "texto")
CampoFonte(T_CURADAS, "facetas", "lista de textos")

T_SEMENTES_F = TabelaFonte("fonte.sementes", F, "sementes", multipla=True,
                           exigencia=OPCIONAL, minimo=0,
                           descricao="observação por semente; semente que não é da base "
                                     "reprova")
CampoFonte(T_SEMENTES_F, "id", "texto")
CampoFonte(T_SEMENTES_F, "observacao", "texto")

T_SONDAGENS = TabelaFonte("fonte.sondagens", F, "sondagens", multipla=True,
                          exigencia=OPCIONAL, minimo=0,
                          descricao="roteiro executável; ciclo em `depende_de` reprova")
I_SD = Identificador("sd", F, None, "SD", descricao="SDn em sequência por base")
CampoFonte(T_SONDAGENS, "id", "texto", descricao="SDn")
CampoFonte(T_SONDAGENS, "elementos", "lista de textos",
           descricao="elementos de [[sintaxe]] ou textos de [[regras_de_montagem]]")
CampoFonte(T_SONDAGENS, "objetivo", "texto")
CampoFonte(T_SONDAGENS, "pre_requisitos", "lista de textos")
CampoFonte(T_SONDAGENS, "passos", "lista de textos")
CampoFonte(T_SONDAGENS, "observar", "lista de textos")
CampoFonte(T_SONDAGENS, "evidencia", "lista de textos")
CampoFonte(T_SONDAGENS, "depende_de", "lista de textos", OPCIONAL)
T_SOND_CONSULTAS = TabelaFonte("fonte.sondagens.consultas", F, "sondagens.consultas",
                               multipla=True, pai=T_SONDAGENS,
                               descricao="ao menos uma por sondagem")
D_PAPEL_CONSULTA = CampoFonte(T_SOND_CONSULTAS, "papel", "texto", dominio=PAPEIS_CONSULTA)
CampoFonte(T_SOND_CONSULTAS, "texto", "texto", descricao="consulta literal")
CampoFonte(T_SOND_CONSULTAS, "onde", "texto", descricao="caixa, campo ou filtro")
CampoFonte(T_SOND_CONSULTAS, "muda", "texto", OPCIONAL,
           descricao="o que muda em relação ao controle")
T_SOND_LEITURAS = TabelaFonte("fonte.sondagens.leituras", F, "sondagens.leituras",
                              multipla=True, pai=T_SONDAGENS, minimo=2,
                              descricao="ao menos duas; uma delas, a inconclusiva, com "
                                        "`estado = \"nao_verificado\"`")
CampoFonte(T_SOND_LEITURAS, "resultado", "texto", descricao="condição observável")
CampoFonte(T_SOND_LEITURAS, "conclusao", "texto")
CampoFonte(T_SOND_LEITURAS, "estado", "texto", dominio=SITUACOES,
           descricao="a situação que o elemento passa a ter")

# Fragmentos de prosa: nome → (posição no procedimento, admite `####`).
FRAGMENTOS = {
    "notas_sintaxe.md": ("§1, depois da tabela", False),
    "estrategia_de_proximidade.md": ("§4, subseção \"Estratégia de proximidade\"", False),
    "como_executar.md": ("§4, subseção \"Como executar\" (obrigatório)", False),
    "variantes.md": ("§4, subseção \"Variantes previstas\"", True),
    "notas_execucao.md": ("§4, depois das linhas fixas de execução", False),
    "notas_sementes.md": ("§5, depois do limiar", False),
}
FRAGMENTO_OBRIGATORIO = "como_executar.md"
LINHA_EXECUCAO = "- Execução:"
FR_FRAGMENTOS = FrasePadrao(
    "fonte.fragmentos", F, None,
    "; ".join(f"{n} ({p})" for n, (p, _) in FRAGMENTOS.items()),
    r"^(#{1,4})\s", exigencia=OPCIONAL,
    descricao="nome desconhecido, falta de como_executar.md, título de nível 1 a 3, "
              "`####` fora de variantes.md e a linha `- Execução:` reprovam a base")
F_CITACAO = FrasePadrao(
    "fonte.citacao_execucao", F, None,
    "BDn/<id>  (no texto, `(BDn/<id>)`) em toda menção ao registro de execução",
    r"\b(BD\d+)/([A-Za-z0-9][\w.-]*)", exigencia=OPCIONAL,
    descricao="menção ao registro sem a citação, ou citação com BDn de outra base ou com "
              "id ausente de `execucoes` e de `sondagens`, reprova a base "
              "(python3 -m rsl dados conferir)")

# Esqueleto e texto fixo do procedimento gerado (saída; não tem leitura).
ESQUELETO = {
    "titulo": "# Strings de busca — {nome}",
    "s1": "## 1. Estado de verificação da sintaxe",
    "s1_colunas": ("Elemento", "Categoria", "Situação", "Fonte", "Sondagem"),
    "s1_sondagens": "### Sondagens a executar",
    "s2": "## 2. Critérios de elegibilidade",
    "s2_colunas": ("Critério", "ID", "Na consulta?", "Como"),
    "s3": "## 3. Strings por faceta",
    "s3_declaracao": "### Declaração de cobertura",
    "s4": "## 4. Expressões de busca",
    "s4_montagem": "### Como esta base exige a montagem",
    "s4_proximidade": "### Estratégia de proximidade",
    "s4_curadas": "### Forma curada",
    "s4_como": "### Como executar",
    "s4_variantes": "### Variantes previstas",
    "s5": "## 5. Conjunto-semente",
    "s6": "## 6. Ressalvas",
    "separador": "---",
}
TEXTO_FIXO = {
    "aviso": "<!-- Gerado por `python3 -m rsl procedimentos gerar {sigla} --gravar` a partir "
             "de `{fonte}`, do protocolo e do arquivo de sementes. Não editar: a edição à mão "
             "reprova em `documentos conferir`. -->",
    "s3_intro": "`STRn` é o identificador do protocolo e `#n` o número da string na "
                "composição. Mapa das facetas: {mapa}.",
    "s3_declaracao": "Declarada em `{fonte}`, `[cobertura]`; conferida por `python3 -m rsl "
                     "documentos conferir`.",
    "s3_reducao": "**Redução desta base.**",
    "s1_seguranca": "Uma consulta por vez, sem nova tentativa automática; parar diante de "
                    "captcha, aviso de atividade atípica ou bloqueio, e registrar.",
    "fidelidade": "- **Fidelidade:** divergência acima de `divergencia_fidelidade` "
                  "(`python3 -m rsl configuracao mostrar`) entre {expressoes} executadas e "
                  "derivadas reprova a derivação.",
    "sensibilidade": "- **Sensibilidade:** fração elegível de `{sonda} \\ {executada}` abaixo "
                     "do limite inferior da faixa `sensibilidade` (`python3 -m rsl "
                     "configuracao mostrar`) mantém {executada}; acima do superior, leva à "
                     "reconsideração, com emenda.",
    "retorno_zero": "- **Retorno zero:** {executada} = 0 ou {sonda} = 0 é defeito de "
                    "execução até prova em contrário; contagem derivada próxima de zero "
                    "exige execução direta antes do relato.",
    "s5_intro": "Esperadas nesta base, conforme o protocolo. Estado de conferência no "
                "arquivo de sementes (`[documentos] sementes`); aferição em "
                "`data/semente_aderencia.csv`.",
    "s5_procedimento": "**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem "
                       "recorte temporal e sem as expressões; semente não indexada sai do "
                       "denominador e registra-se como cobertura. *Etapa 2:* procurar a "
                       "semente na exportação de {executada} por DOI e depois por título, "
                       "sem reexecutar a busca.",
    "s5_limiar": "**Limiar de aderência** (`limiar_aderencia`, `python3 -m rsl configuracao "
                 "mostrar`), sobre a união das bases. A aderência por base indica qual base "
                 "e qual faceta falharam.",
}
EXECUCAO_TEXTO = {"executada": "executar e exportar: é o corpus desta base",
                  "sonda": "executar uma única vez, na mesma data; não compõe o corpus",
                  "fidelidade": "executar só para o teste de fidelidade da derivação",
                  "derivada": "não executar; derivação local"}
ESTATUTO_FRASE = {"executada": "Executada e exportada nesta base.",
                  "sonda": "Sonda de sensibilidade — executada uma única vez; não compõe o "
                           "corpus.",
                  "fidelidade": "Derivada localmente — executar apenas no teste de "
                                "fidelidade.",
                  "derivada": "Derivada localmente — não executar."}
ESTATUTO_PAPEL = {"executada": "(executada)", "sonda": "(sonda de sensibilidade)"}

# Modelo textual de `procedimentos iniciar`: a biblioteca padrão lê TOML e não o escreve.
# `{...}` é preenchido com o derivável; o resto vem com a marca PENDENTE.
MODELO_INICIO = '''# Fonte do procedimento de busca de {nome} ({bd}), criada por
# `python3 -m rsl procedimentos iniciar {sigla}`. Esquema: `python3 -m rsl documentos gramatica`.
# Toda marca "{pendente}" é trabalho a fazer: a base fica reprovada até não restar nenhuma.

ressalvas = []

{sintaxe}
{criterios}
[cobertura]
camadas = "todas"
plural = "explícito"
teto = "{pendente}"
derivacoes = ["{pendente}"]

[cobertura.idiomas]
{idiomas}

[composicao]
aspas = "{pendente}"
proximidade = "{pendente}"
disjuncao = "{pendente}"
{composicao}
[execucao]
forma = "{pendente}"
{expressoes}
{sementes}'''


# ============================================================ arquivo de exceções de flexão
X = FLEXOES
T_RAIZ_FLEXOES = TabelaFonte("flexoes", X, "", exigencia=OPCIONAL,
                             descricao="arquivo ausente: nenhuma exceção; TOML inválido ou "
                                       "chave fora do esquema reprova")
T_EXCECOES = TabelaFonte("flexoes.excecoes", X, "excecoes", multipla=True, minimo=0,
                         descricao="exceção repetida para o mesmo termo e idioma reprova; "
                                   "exceção de termo fora de toda STR é relatada")
CampoFonte(T_EXCECOES, "termo", "texto")
CampoFonte(T_EXCECOES, "idioma", "texto", descricao="idioma do quadro")
D_TIPO_EXCECAO = CampoFonte(T_EXCECOES, "tipo", "texto",
                            dominio=("irregular", "nao_contavel", "vetada"),
                            descricao="`irregular` e `vetada` exigem `formas`")
EXC_IRREGULAR, EXC_NAO_CONTAVEL, EXC_VETADA = D_TIPO_EXCECAO.dominio
CampoFonte(T_EXCECOES, "formas", "lista de textos", OPCIONAL,
           descricao="irregular: as formas de plural; vetada: a forma que não se usa")
CampoFonte(T_EXCECOES, "origem", "texto", descricao="fonte ou decisão que sustenta a "
                                                    "exceção")


# ======================================================= resultado de sondagem registrado
R = SONDAGEM
T_RES_SONDAGEM = TabelaFonte("registro.sondagens", R, "bases.BDn.sondagens", multipla=True,
                             minimo=0, descricao="gravado por `sondagens registrar`; id "
                                                 "repetido na base reprova")
CampoFonte(T_RES_SONDAGEM, "id", "texto", descricao="`sd<n>-<data>`, com sufixo quando "
                                                    "se repete")
CampoFonte(T_RES_SONDAGEM, "sondagem", "texto", descricao="SDn existente na fonte da base")
CampoFonte(T_RES_SONDAGEM, "data_hora", "texto", descricao="ISO 8601")
CampoFonte(T_RES_SONDAGEM, "consultas", "lista de tabelas",
           descricao="lista de {texto, retorno}, na ordem das consultas declaradas")
CampoFonte(T_RES_SONDAGEM, "leitura", "tabela",
           descricao="{numero, resultado, estado}: uma das leituras declaradas")
CampoFonte(T_RES_SONDAGEM, "evidencia", "lista de textos", descricao="caminhos relativos")
CampoFonte(T_RES_SONDAGEM, "observacao", "texto", OPCIONAL)


def exigidos(documento=None):
    return [e for e in ELEMENTOS if e.exigido and (documento is None or
                                                    e.documento == documento)]


def contrato():
    """O contrato legível, a partir das declarações, agrupado por documento."""
    linhas = []
    for doc in DOCUMENTOS:
        linhas.append(f"{'=' * 8} {doc}")
        for e in (x for x in ELEMENTOS if x.documento == doc):
            linhas.append(f"  [{e.exigencia:<8}] {e.rotulo}")
            if e.forma():
                linhas.append(f"      forma: {e.forma()}")
            if e.descricao:
                linhas.append(f"      reprova: {e.descricao}")
        linhas.append("")
    linhas.append(f"O {PROCEDIMENTO} de cada base não tem grupo: é saída de `python3 -m rsl "
                  f"procedimentos gerar`, gerado da fonte, do protocolo e do arquivo de "
                  f"sementes; edita-se a fonte. Categorias mínimas de [[sintaxe]]: "
                  f"{', '.join(CATEGORIAS)}.")
    linhas.append("Níveis: exigido — ausente ou fora da forma, PROTOCOLO_ILEGIVEL; opcional — "
                  "ausente, vale o padrão ou a conferência relata; presente e fora da forma, "
                  "PROTOCOLO_ILEGIVEL.")
    return "\n".join(linhas)
