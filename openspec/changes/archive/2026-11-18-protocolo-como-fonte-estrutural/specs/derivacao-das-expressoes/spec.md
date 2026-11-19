# Spec Delta

## REMOVED Requirements

### Requirement: Bases vêm da configuração
**Reason**: `[fichas]` sai do `config.toml`; as bases passam a ser declaradas na tabela
"Bases de dados" do protocolo.
**Migration**: substituído por "Bases vêm do protocolo". A chave de linha de comando de cada
base passa a ser a sigla do protocolo (`wos`, `scopus`, `eric`, `brapci`), igual à chave
usada até aqui.

## ADDED Requirements

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

## MODIFIED Requirements

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
