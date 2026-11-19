# Spec Delta

## ADDED Requirements

### Requirement: Termo de string pertence a uma só faceta

Cada termo SHALL constar da string (STR) de uma única faceta. A comparação MUST ignorar
caixa e diacríticos. Termo presente em STR de duas ou mais facetas MUST reprovar
`--conferir`, nomeando o termo e as STR em que aparece. O quadro terminológico não está
sujeito a esta regra; só as strings.

#### Scenario: Termo repetido entre âncora e faceta de prática
- **WHEN** `teaching strategy` consta de STR2 e de STR3
- **THEN** `--conferir` reprova, nomeando `teaching strategy`, STR2 e STR3

#### Scenario: Repetição só por diacrítico
- **WHEN** `situacao de aprendizagem` consta de STR2 e `situação de aprendizagem` de STR4
- **THEN** `--conferir` reprova, tratando as duas grafias como o mesmo termo

#### Scenario: Repetição só no quadro
- **WHEN** `ambiente de aprendizagem` consta dos quadros de FCT2 e de FCT4 e só da STR2
- **THEN** essa dimensão não reprova

#### Scenario: Strings disjuntas
- **WHEN** nenhum termo consta de mais de uma STR
- **THEN** essa dimensão não reprova

### Requirement: Autoteste prova a reprovação do termo repetido

O autoteste SHALL copiar, numa cópia em memória, um termo de uma STR para outra e exigir
que `--conferir` reprove pelo motivo esperado.

#### Scenario: Defeito injetado
- **WHEN** o autoteste acrescenta à STR4 um termo da STR1
- **THEN** a conferência reprova, nomeando o termo e as duas strings
