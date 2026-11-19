# derivacao-das-expressoes Specification

## Purpose

Derivar localmente as expressões não executadas e montar o instrumento de aderência a
partir do que o protocolo e a configuração declaram, sem composição, papéis nem bases
fixados no código.

## Requirements

### Requirement: Prova da composição pelas relações do protocolo
A prova da composição da derivação SHALL verificar, sobre todas as combinações de facetas,
as relações lidas do protocolo: a executada é a união das específicas, a sonda contém toda
expressão, e a expressão geral está contida em cada específica. Os identificadores das
expressões MUST NOT ser fixados no código.

#### Scenario: Protocolo atual
- **WHEN** a derivação roda com a composição atual do protocolo
- **THEN** a prova não reporta problema e as expressões derivadas são as que não são
  executada nem sonda

#### Scenario: Executada que não é a união das específicas
- **WHEN** a composição lida tem a executada diferente da união das específicas
- **THEN** a prova reporta a combinação de facetas em que a relação falha

### Requirement: Expressões deriváveis vêm dos papéis
As expressões deriváveis SHALL ser todas as da composição exceto a executada e a sonda
declaradas pelo protocolo.

#### Scenario: Papéis lidos
- **WHEN** o protocolo declara EB4 executada e EB5 sonda
- **THEN** as deriváveis são as demais expressões da composição

### Requirement: Bases vêm do protocolo
As bases usadas na derivação e no instrumento de aderência — sigla e identificador `BDn` —
SHALL vir da tabela "Bases de dados" do protocolo, e a ficha, da sigla; o código MUST NOT
fixar lista nem mapa de bases. A base é escolhida na linha de comando pela sigla ou pelo
identificador.

#### Scenario: Sigla de uma base
- **WHEN** a tabela declara `BD3` com sigla `eric`
- **THEN** a derivação e o instrumento de aderência usam `eric` para a base, e
  `--base eric` e `--base BD3` selecionam a mesma base

#### Scenario: Base desconhecida na linha de comando
- **WHEN** se pede uma base que não é sigla nem identificador da tabela
- **THEN** o script termina com erro que lista as siglas e os identificadores lidos

### Requirement: Facetas do instrumento de aderência vêm do protocolo
As facetas usadas por `gen_semente.py` SHALL vir das facetas lidas do protocolo, na ordem
declarada; o código MUST NOT fixar a lista de facetas.

#### Scenario: Facetas lidas
- **WHEN** o protocolo declara FCT1 a FCT4
- **THEN** o instrumento usa FCT1 a FCT4, nessa ordem

### Requirement: Saídas preservadas
Para o protocolo e a configuração atuais, as saídas da derivação, da aderência, da
fidelidade e da sensibilidade MUST ser idênticas às anteriores à mudança, exceto a redação
da coluna `facetas_exigidas` de `contagens_busca.csv`, que passa à forma estrita
(`FCT1 AND FCT2 AND (FCT3 OR FCT4)`) por decisão do pesquisador, a grafia das siglas das
bases, que passa a ser a do protocolo (`wos`, `scopus`, `eric`, `brapci`), e, na aderência,
o relato separado por papel da semente, com o intervalo de confiança, a coluna `papel` da
planilha de aderência e o casamento por prefixo, que deixa de entrar no numerador e passa a
ser relatado como indício.

#### Scenario: Mesmo resultado
- **WHEN** a prova da composição, as deriváveis e o mapa de bases são calculados antes e
  depois da mudança
- **THEN** os valores coincidem, comparadas as siglas sem distinção de caixa

#### Scenario: Aderência preservada nos casamentos exatos
- **WHEN** a aderência é calculada antes e depois da separação por papel, com os mesmos
  registros
- **THEN** o total de sementes recuperadas por casamento exato coincide, e só a decomposição
  por papel, o intervalo e a coluna `papel` são novos; o casamento por prefixo deixa de ser
  contado e passa a indício

### Requirement: Aderência relatada por papel da semente

`--aderencia` SHALL relatar separadamente a recuperação das sementes de validação e a das
de desenvolvimento, com numerador e denominador de cada uma. Só a das sementes de validação
SHALL ser comparada ao limiar de aderência, e o relato MUST identificar qual das duas é a
que decide a passagem.

#### Scenario: Relato separado
- **WHEN** há 6 sementes de validação, das quais 5 recuperadas, e 4 de desenvolvimento,
  todas recuperadas
- **THEN** o relato mostra 5/6 para validação, comparado ao limiar, e 4/4 para
  desenvolvimento, marcado como não decisório

#### Scenario: Desenvolvimento não compensa validação
- **WHEN** a recuperação de validação fica abaixo do limiar e a total, somando
  desenvolvimento, fica acima
- **THEN** o relato declara a aderência abaixo do limiar

### Requirement: Casamento por prefixo é indício

`--aderencia` SHALL imprimir o casamento por prefixo de título como indício e MUST NOT
contá-lo no numerador da aderência. A confirmação do casamento por prefixo exige registro
humano na coluna `recuperada`.

#### Scenario: Prefixo não entra no numerador
- **WHEN** uma semente só casa com um registro por prefixo de título
- **THEN** o relato a marca como indício e não a conta como recuperada

### Requirement: Intervalo de confiança da aderência

O relato da aderência de validação SHALL trazer, junto com a proporção, o intervalo de
Wilson a 95%, calculado sobre o mesmo numerador e o mesmo denominador.

#### Scenario: Intervalo para 8 de 10
- **WHEN** 8 de 10 sementes de validação são recuperadas
- **THEN** o relato mostra 80% com intervalo de aproximadamente 49% a 94%

### Requirement: Planilha de aderência traz o papel

A planilha gerada pelo instrumento de aderência SHALL ter, em cada linha, o papel da
semente lido do protocolo.

#### Scenario: Coluna de papel
- **WHEN** `gen_semente.py` gera a planilha
- **THEN** cada linha traz a coluna `papel` com `desenvolvimento` ou `validação`, igual à
  da tabela do protocolo
