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
(`FCT1 AND FCT2 AND (FCT3 OR FCT4)`) por decisão do pesquisador, e a grafia das siglas das
bases, que passa a ser a do protocolo (`wos`, `scopus`, `eric`, `brapci`).

#### Scenario: Mesmo resultado
- **WHEN** a prova da composição, as deriváveis e o mapa de bases são calculados antes e
  depois da mudança
- **THEN** os valores coincidem, comparadas as siglas sem distinção de caixa
