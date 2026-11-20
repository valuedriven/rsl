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
DOCUMENTOS = (PROTOCOLO, FICHA)

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


# ======================================================================== protocolo
P = PROTOCOLO

S_QUESTAO = Secao("questao", P, "Questão de revisão", 2)
S_QGR = Secao("questao_geral", P, "Questão geral de revisão", 3, pai=S_QUESTAO)
S_QER = Secao("questoes_especificas", P, "Questões específicas de revisão", 3, pai=S_QUESTAO)
M_QGR = Marcador("qgr", P, S_QGR, "- QGR: <questão geral>", r"^-\s*QGR:\s*(.+)$",
                 descricao="primeiro parágrafo da seção; sem o marcador, reprova")
M_ESTRUTURA = Marcador(
    "estrutura", P, S_QGR, "Estrutura da questão…",
    r"^Estrutura da questão",
    descricao="parágrafo que declara a estrutura (PICo); ausente, reprova")
I_QER = Identificador("qer", P, S_QER, "QER",
                      descricao="item `- QERn: <questão>`; fora da sequência, reprova")
F_QER = FrasePadrao("questao_especifica", P, S_QER, "- QERn: <questão>",
                    r"^-\s*(QER\d+):\s*(.+)$")

S_PALAVRAS = Secao("palavras", P, "Palavras significativas da questão de revisão", 2)
F_FACETA = FrasePadrao(
    "faceta", P, S_PALAVRAS, "- Faceta n (FCTn): <nome> [(âncora obrigatória k)]",
    r"^-\s*Faceta\s+(\d+)\s*(?:\((FCT\d+)\))?\s*:\s*(.+)$",
    descricao="identificador diferente de FCTn, nome vazio ou travessão residual reprovam")
F_ANCORA = FrasePadrao(
    "ancora", P, S_PALAVRAS, "(âncora obrigatória k)",
    r"\s*\(\s*âncora obrigatória\s+(\d+)\s*\)\s*$", exigencia=OPCIONAL,
    descricao="no fim da linha da faceta; sem nenhuma, valem as âncoras padrão "
              "(`padroes.ancoras`); a palavra âncora fora dessa forma reprova")
PALAVRA_ANCORA = "âncora"
I_FCT = Identificador("fct", P, S_PALAVRAS, "FCT")

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
    linhas="uma linha por camada; termos separados por `\\- `",
    descricao="uma tabela por faceta, com o identificador na primeira célula do cabeçalho; "
              "as demais células nomeiam os idiomas, os mesmos em todas as tabelas, em "
              "qualquer ordem")
SEPARADOR_TERMOS = r"\\-\s*"
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
    "expressoes", P, S_EXPRESSOES,
    ("ID expressão", "Natureza", "Expressão de busca", "Detalhamento"), modo="exato",
    descricao="cabeçalho diferente reprova: as colunas são lidas pela posição; a Natureza "
              "identifica a executada e a sonda (`[expressoes]` do config.toml)")
I_EB = Identificador("eb", P, S_EXPRESSOES, "EB")
F_COMPOSICAO = FrasePadrao(
    "composicao", P, S_EXPRESSOES, "STRn AND STRn AND (STRn OR STRn)", r"STR\d+",
    descricao="AND em maiúsculas é a única conjunção; OR só entre parênteses, sem "
              "aninhamento; `+`, operador em minúscula ou OR fora de parênteses reprovam")
F_FAIXA = FrasePadrao(
    "faixa_sensibilidade", P, S_EXPRESSOES, "< N% … > M%  (no Detalhamento da sonda)",
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
T_SEMENTES = Tabela("sementes", P, S_SEMENTES, ("ID Semente", "Semente", "Bases", "Papel"),
                    descricao="semente sem base, base que não é sigla da tabela de bases "
                              "e base repetida reprovam")
I_SE = Identificador("se", P, S_SEMENTES, "SE")
D_PAPEL = Dominio("papel", P, S_SEMENTES, "Papel",
                  {"desenvolvimento": "desenvolvimento", "validação": "validação"},
                  descricao="só a validação decide a passagem; vazio ou fora do domínio "
                            "reprova")
PAPEL_DESENVOLVIMENTO, PAPEL_VALIDACAO = D_PAPEL.valores
F_REFERENCIA = FrasePadrao(
    "referencia", P, S_SEMENTES, "Autores (AAAA). Título. … DOI: 10.…",
    r"^(.*?)\s*\((\d{4})\)\.\s*(.*)$",
    descricao="sem autoria e ano entre parênteses, reprova; o título termina no primeiro "
              "ponto seguido de maiúscula ou dígito; o DOI é opcional")
F_DOI = FrasePadrao("doi", P, S_SEMENTES, "DOI: 10.…", r"DOI:\s*(10\.\S+?)\s*$",
                    exigencia=OPCIONAL)
M_REGRA = Marcador("regra_ajuste", P, S_SEMENTES, "Regra de ajuste", r"Regra de ajuste",
                   exigencia=OPCIONAL,
                   descricao="sem a regra, vale `padroes.limiar_aderencia`")
F_LIMIAR = FrasePadrao(
    "limiar_aderencia", P, S_SEMENTES, "recuperação inferior a N%  (na Regra de ajuste)",
    r"recuperação inferior a\s+(\d+(?:[.,]\d+)?)\s*%",
    descricao="exigida quando há Regra de ajuste: regra sem limiar legível reprova")
S_FERRAMENTA = Secao("ferramenta", P, "Ferramenta de gestão bibliográfica", 3)
F_FERRAMENTA = FrasePadrao("item_ferramenta", P, S_FERRAMENTA, "- <tema>: <texto>",
                           r"^-\s*(.+?):\s*(.+)$", exigencia=OPCIONAL)

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
