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

### Requirement: Bases vêm da configuração
As siglas das bases usadas na derivação e no instrumento de aderência SHALL vir de
`[fichas]` do `config.toml`; o código MUST NOT fixar lista nem mapa de bases.

#### Scenario: Sigla de uma ficha
- **WHEN** `[fichas]` declara uma ficha com `sigla` e `bd`
- **THEN** a derivação e o instrumento de aderência usam essa sigla para a base

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
(`FCT1 AND FCT2 AND (FCT3 OR FCT4)`) por decisão do pesquisador.

#### Scenario: Mesmo resultado
- **WHEN** a prova da composição, as deriváveis e o mapa de bases são calculados antes e
  depois da mudança
- **THEN** os valores coincidem
