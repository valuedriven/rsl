# Spec Delta

## RENAMED Requirements

- FROM: `### Requirement: Termo só no singular relatado`
- TO: `### Requirement: Termo só no singular reprova`

## MODIFIED Requirements

### Requirement: Plural declarado por base
A declaração de cobertura de cada ficha SHALL ter a linha `plural`. A linha admite um valor
único, `explícito` ou `pela lematização`, que vale para todos os idiomas da ficha, ou um
valor por idioma, na forma `en: pela lematização; pt: explícito; es: explícito`, cobrindo
todos os idiomas que a declaração usa. A linha ausente, o valor fora do domínio ou o idioma
sem valor MUST reprovar com PROTOCOLO_ILEGIVEL. A reprovação nomeia a ficha e a linha.

#### Scenario: Linha ausente
- **WHEN** a declaração de cobertura da ficha da Scopus não tem a linha `plural`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a ficha e a linha

#### Scenario: Valor fora do domínio
- **WHEN** a linha `plural` da ficha da WoS diz `omitido`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, citando os dois valores admitidos

#### Scenario: Valor por idioma
- **WHEN** a ficha da WoS declara `plural | en: pela lematização; pt: explícito; es: explícito`
- **THEN** a flexão acrescenta plural só aos termos pt e es, e o en exige a lematização
  medida para en

#### Scenario: Idioma sem valor
- **WHEN** a declaração usa pt, en e es, e a linha `plural` diz só `en: explícito; pt: explícito`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando `es`

### Requirement: Plural pela lematização exige lematização medida
Para cada idioma com `pela lematização`, a ficha SHALL ter, na seção 1, a linha
"Lematização". A linha traz, para esse idioma, o estado verificado por medição e a citação
`(BDn/<id>)` de uma execução registrada daquela base. Um estado sem idioma vale para todos.
A conferência MUST reprovar só aquela base quando a linha falta, ou quando, para o idioma,
o estado não é verificado ou a citação falta.

#### Scenario: Lematização não verificada
- **WHEN** a ficha da ERIC declara `plural: pela lematização` e a seção 1 diz "Lematização —
  **Não verificado**"
- **THEN** `--conferir` reprova a ERIC, nomeando a declaração e a linha sem medição; as
  demais bases não são afetadas

#### Scenario: Lematização medida
- **WHEN** a ficha declara `plural: pela lematização` e a linha "Lematização" diz
  verificado por medição com `(BD3/sonda-plural)`, sem idioma
- **THEN** essa dimensão não reprova em `--conferir`, porque o estado vale para todos os
  idiomas, e a existência de `BD3/sonda-plural` é conferida por `--conferir-dados`, como em
  "Verificação por medição remete a execução registrada"

#### Scenario: Lematização medida num idioma só
- **WHEN** a ficha da WoS declara `en: pela lematização` e a linha "Lematização" diz `en:
  verificado por medição (BD1/sonda-plural-en); pt: não verificado`
- **THEN** essa dimensão não reprova em `--conferir`, porque o pt é `explícito`, e a
  existência de `BD1/sonda-plural-en` é conferida por `--conferir-dados`

#### Scenario: Plural explícito
- **WHEN** a ficha declara `plural: explícito`
- **THEN** o estado da linha "Lematização" não reprova

### Requirement: Termo só no singular reprova
Em idioma com plural explícito, a conferência MUST reprovar, por base, o termo da STR
presente na string da base numa só forma de número. A reprovação não vale quando o termo é
`nao_contavel` ou tem forma `vetada` no arquivo de exceções (`flexao-dos-termos`), nem
quando um truncamento declarado na ficha o alcança. A reprovação nomeia a faceta, o termo e
o idioma. A regra vale também para a forma curada.

#### Scenario: Plural esquecido
- **WHEN** a ficha da Scopus declara `plural: explícito` e traz `"teaching strategy"` sem
  `"teaching strategies"`, nem truncamento que o alcance, nem exceção
- **THEN** `--conferir` reprova a Scopus, nomeando `teaching strategy`, FCT3 e en; as
  demais bases passam

#### Scenario: Não contável
- **WHEN** a ficha traz `"education"` só no singular e o arquivo de exceções declara
  `education`, en, `nao_contavel`
- **THEN** essa dimensão não reprova
