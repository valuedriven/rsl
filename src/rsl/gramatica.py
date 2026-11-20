"""Gramática do protocolo e das fichas de busca: a única fonte dos literais de forma.

Cada elemento declara o que o leitor exige de um documento — seção, tabela, coluna, rótulo
de linha, marcador, forma de identificador, frase-padrão de onde se lê um parâmetro, domínio
de valores. Os leitores recebem o elemento, não o literal, e a reprovação nomeia o elemento
com o mesmo rótulo que `python3 -m rsl gramatica` exibe.

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
FICHA = "ficha de base"
SEMENTES = "arquivo de sementes"
DOCUMENTOS = (PROTOCOLO, FICHA, SEMENTES)

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
D_ACAO = Dominio("acao", P, S_CRITERIOS, "Ação", {"Incluir": "Incluir", "Excluir": "Excluir"})
ACAO_INCLUIR, ACAO_EXCLUIR = D_ACAO.valores
F_RECORTE = FrasePadrao(
    "recorte", P, S_CRITERIOS, "após o ano AAAA  (critério Incluir da dimensão do recorte)",
    r"após o ano\s+(\d{4})", exigencia=OPCIONAL,
    descricao="dimensão em `conferencia.dimensao_recorte`; sem o critério, vale "
              "`padroes.recorte_ano_min`; critério sem ano legível reprova")

S_FONTES = Secao("fontes", P, "Fontes de informação", 3)
S_BASES = Secao("bases", P, "Bases de dados", 4, pai=S_FONTES)
T_BASES = Tabela("bases", P, S_BASES, ("ID Base", "Sigla", "Nome da base"),
                 descricao="campo vazio, sigla repetida, sigla com caractere fora de "
                           "[A-Za-z0-9_-] e sigla sem ficha reprovam")
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

# ============================================================================ ficha
F = FICHA

SF_CRITERIOS = Secao("ficha.criterios", F, "2. Critérios de elegibilidade", 2)
TF_CRITERIOS = Tabela("ficha.criterios", F, SF_CRITERIOS, ("Critério", "ID"),
                      modo="posicional",
                      descricao="IDs CEn na segunda coluna (`CEn / CEm` conta os dois); "
                                "sem nenhum ID, reprova")
SF_STRINGS = Secao("ficha.strings", F, "3. Strings por faceta", 2)
SF_DECLARACAO = Secao("ficha.declaracao", F, "Declaração de cobertura", 3, pai=SF_STRINGS)
TF_DECLARACAO = Tabela(
    "ficha.declaracao", F, SF_DECLARACAO, ("Declaração", "Valor"), modo="posicional",
    linhas="rótulos idiomas, camadas, derivações; e a redução declarada, uma linha por "
           "termo: `| FCTn | termo | motivo |`")
RF_IDIOMAS = RotuloLinha("ficha.idiomas", F, TF_DECLARACAO, "idiomas", "idiomas",
                         descricao="`FCTn: <idioma>, <idioma>; FCTm: …`; ausente, ilegível ou com idioma "
                                   "fora do quadro reprova")
RF_CAMADAS = RotuloLinha("ficha.camadas", F, TF_DECLARACAO, "camadas", "camadas",
                         descricao="ausente reprova")
RF_DERIVACOES = RotuloLinha("ficha.derivacoes", F, TF_DECLARACAO, "derivações",
                            "derivacoes", exigencia=OPCIONAL,
                            descricao="ausente, nenhuma derivação declarada")
D_CAMADAS = Dominio("ficha.camadas", F, SF_DECLARACAO, "camadas",
                    {"todas": "todas", "nucleo": "nucleo"})
CAMADAS_TODAS, CAMADAS_NUCLEO = D_CAMADAS.valores
D_DERIVACOES = Dominio("ficha.derivacoes", F, SF_DECLARACAO, "derivações",
                       {"morfologia": "morfologia", "radical": "radical"},
                       exigencia=OPCIONAL,
                       descricao="separadas por vírgula, `;` ou ` e `; valor fora reprova")
DERIVACAO_RADICAL = "radical"
F_REDUCAO = FrasePadrao("ficha.reducao", F, SF_DECLARACAO, "| FCTn | termo | motivo |",
                        r"^FCT\d+$", exigencia=OPCIONAL,
                        descricao="motivo com `radical` afirma alcance pela forma radical "
                                  "(conferido); com `pendente`, lacuna em aberto")
MOTIVO_RADICAL = "radical"
MOTIVO_PENDENTE = "pendente"
F_STRING_BASE = FrasePadrao(
    "ficha.string", F, SF_STRINGS, "### `STRn` — … FCTn … conjunto `#n`, com um bloco ```",
    r"`(STR\d+[a-z]?)`",
    descricao="sem FCTn no cabeçalho, ou com número de blocos diferente de um, reprova; "
              "ficha sem nenhuma string legível reprova")
F_CONJUNTO = FrasePadrao("ficha.conjunto", F, SF_STRINGS, "conjunto `#n`",
                         r"conjunto\s+`(#\w+)`", exigencia=OPCIONAL)
SF_EXPRESSOES = Secao("ficha.expressoes", F, "4. Expressões de busca", 2)
MF_EXECUCAO = Marcador("ficha.execucao", F, SF_EXPRESSOES, "- Execução: <forma>",
                       r"^-\s*Execução:\s*(.*?)\s*$",
                       descricao="exatamente uma linha; ausente ou repetida reprova")
D_EXECUCAO = Dominio("ficha.execucao", F, SF_EXPRESSOES, "Execução",
                     {"única": "unica", "particionada": "particionada"})
F_EXPRESSAO_BASE = FrasePadrao(
    "ficha.expressao", F, SF_EXPRESSOES, "### EBn …", r"^(EB\d+)", exigencia=OPCIONAL,
    descricao="as expressões da ficha têm de ser as do protocolo (conferência)")
MARCA_FACETAS = "Facetas:"
MF_FACETAS = Marcador("ficha.facetas", F, SF_EXPRESSOES, f"**{MARCA_FACETAS}** FCTn AND …",
                      re.escape(MARCA_FACETAS) + r"\s*\**\s*(.+)", exigencia=OPCIONAL,
                      descricao="as facetas da expressão têm de ser as da composição "
                                "(conferência)")
# Subtítulos de `4. Expressões de busca` que não são expressão (início do título, em
# minúsculas) e os que têm leitura própria.
SUBTITULOS_IGNORADOS = ("como executar", "variantes", "como esta base")
SUBTITULO_PROXIMIDADE = "proximidade"
SUBTITULO_CURADAS = "curadas"
SUBTITULO_FORMA_LONGA = "forma longa"
M_SUBTITULOS = Marcador(
    "ficha.subtitulos", F, SF_EXPRESSOES,
    "### <subtítulo> com: " + ", ".join(SUBTITULOS_IGNORADOS + (
        SUBTITULO_PROXIMIDADE, SUBTITULO_CURADAS, SUBTITULO_FORMA_LONGA)),
    r"^###\s+", exigencia=OPCIONAL,
    descricao="como executar / variantes / como esta base: ignorados; proximidade: "
              "conjunto das âncoras; curadas: forma curada (`#### grupo` e `| n | "
              "`consulta` | FCTn |`); forma longa: `**EBn**` com bloco")
ROTULO_NAO_EXECUTADA = "nao e a forma executada"
# Estatuto da expressão, lido do texto que segue o subtítulo `### EBn` (normalizado). A
# ordem importa: a primeira frase encontrada decide.
ESTATUTOS = (
    ("sonda", ("sonda de sensibilidade", "controle de sensibilidade")),
    ("fidelidade", ("teste de fidelidade",)),
    ("derivada", ("nao se executa", "derivada localmente")),
    ("executada", ("executada e exportada", "esta que se executa")),
)
F_ESTATUTO = FrasePadrao(
    "ficha.estatuto", F, SF_EXPRESSOES,
    "; ".join(f"{e}: " + " / ".join(fr) for e, fr in ESTATUTOS),
    "|".join(re.escape(fr) for _, frs in ESTATUTOS for fr in frs), exigencia=OPCIONAL,
    descricao="sem nenhuma, o estatuto é `nao declarado`")
F_CITACAO = FrasePadrao(
    "ficha.citacao_execucao", F, None, "(BDn/<id>)  em toda menção ao registro de execução",
    r"\((BD\d+)/([^)\s]+)\)", exigencia=OPCIONAL,
    descricao="menção ao registro sem a citação, com BDn de outra base ou com execução "
              "inexistente reprova a base (conferir-dados)")


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
                               "(`pendencias`); presente fora da forma 10.x/…, reprova",
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
    linhas.append("Níveis: exigido — ausente ou fora da forma, PROTOCOLO_ILEGIVEL; opcional — "
                  "ausente, vale o padrão ou a conferência relata; presente e fora da forma, "
                  "PROTOCOLO_ILEGIVEL.")
    return "\n".join(linhas)
