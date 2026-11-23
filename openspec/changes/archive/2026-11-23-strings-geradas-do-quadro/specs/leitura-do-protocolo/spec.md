# Spec Delta

## MODIFIED Requirements

### Requirement: Conferência verifica coerência interna
`--conferir` SHALL reprovar contradições internas: termo de STR ausente do quadro da faceta;
STR diferente da STR esperada calculada do quadro ("STR é a união do quadro da faceta", em
`geracao-das-strings`); termo do quadro em mais de uma faceta; expressão sem as âncoras;
executada que não seja a união das específicas; semente sem base ou com base fora da tabela
de bases; dimensão de critério em uso não declarada no protocolo; faixa de sensibilidade com
inferior ≥ superior. A sonda ser a conjunção das âncoras é garantida pela identificação
("Executada e sonda identificadas pela composição") e não é conferida de novo.

#### Scenario: Termo da string fora do quadro
- **WHEN** uma STR contém um termo que não consta do quadro da sua faceta
- **THEN** `--conferir` reprova, nomeando a faceta e o termo

#### Scenario: STR divergente da gerada
- **WHEN** o quadro de FCT3 deixou de ter `practice` e a STR3 do protocolo ainda o contém, ou
  o quadro ganhou um termo que a STR não tem
- **THEN** `--conferir` reprova, nomeando a faceta, os termos a mais e a menos, e
  `strings gerar` como correção

#### Scenario: Subsumido presente na STR
- **WHEN** a STR1 contém `"ontology"` e `"domain ontology"`
- **THEN** `--conferir` reprova a STR1 como divergente da gerada, nomeando `domain ontology`
  como subsumido por `ontology`

#### Scenario: Termo em duas facetas do quadro
- **WHEN** `nível de ensino` consta dos quadros de FCT2 e FCT4
- **THEN** `--conferir` reprova, nomeando o termo e as duas facetas

#### Scenario: Mesma forma em idiomas da mesma faceta
- **WHEN** `contexto de uso` consta das colunas pt e es do quadro de FCT4
- **THEN** `--conferir` não reprova por atribuição única

#### Scenario: Dimensão de critério com grafia do protocolo
- **WHEN** a lista de dimensões em uso tem "Idioma" e o protocolo declara CE3 com "Idioma"
- **THEN** `--conferir` não reprova por dimensão de critério

#### Scenario: Distribuição das sementes não é declarada em prosa
- **WHEN** o conjunto-semente está só no arquivo de sementes, sem parágrafo de incidências
  no protocolo
- **THEN** `--conferir` não reprova por distribuição; a distribuição por base é calculada do
  campo `bases` do arquivo e exibida

### Requirement: Bases lidas da tabela do protocolo
As bases SHALL ser lidas da tabela "Bases de dados": identificador `BDn`, sigla e nome. Sigla
e identificador MUST ser únicos. A ficha de cada base SHALL ser localizada pela sigla, no
padrão de caminho do `config.toml`; ficha inexistente MUST reprovar, nomeando base e caminho.

#### Scenario: Ficha da sigla não existe
- **WHEN** o padrão é `docs/procedimentos_busca_{sigla}.md` e não existe
  `docs/procedimentos_busca_eric.md`
- **THEN** a leitura reprova, nomeando BD3, a sigla `eric` e o caminho procurado

#### Scenario: Padrão sem a sigla
- **WHEN** o padrão de caminho do `config.toml` não contém `{sigla}`
- **THEN** o script termina com erro de configuração que nomeia a chave

#### Scenario: Sigla repetida
- **WHEN** duas linhas da tabela têm a sigla `eric`
- **THEN** a leitura reprova, nomeando a sigla
