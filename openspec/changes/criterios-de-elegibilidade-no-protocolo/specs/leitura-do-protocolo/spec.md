# Spec Delta

## ADDED Requirements

### Requirement: Critério de elegibilidade tem justificativa

Todo critério da tabela de critérios de elegibilidade SHALL ter a coluna "Justificativa"
preenchida. Célula vazia, ou só com espaço ou traço, MUST reprovar `--conferir`, nomeando o
ID do critério.

#### Scenario: Critério sem justificativa

- **WHEN** a linha do CE6 tem a coluna "Justificativa" vazia
- **THEN** `--conferir` reprova, nomeando CE6

#### Scenario: Todos os critérios justificados

- **WHEN** todas as linhas da tabela de critérios têm justificativa
- **THEN** essa dimensão não reprova

#### Scenario: Justificativa reduzida a traço

- **WHEN** a justificativa de um critério é `-`
- **THEN** `--conferir` reprova, nomeando o critério

### Requirement: Autoteste prova a reprovação do critério sem justificativa

O autoteste SHALL esvaziar, numa cópia em memória, a justificativa de um critério e exigir
que `--conferir` reprove pelo motivo esperado, nomeando o critério.

#### Scenario: Defeito injetado

- **WHEN** o autoteste esvazia a justificativa de um critério na cópia
- **THEN** a conferência reprova nomeando aquele critério, e o caso conta como resultado
  esperado
