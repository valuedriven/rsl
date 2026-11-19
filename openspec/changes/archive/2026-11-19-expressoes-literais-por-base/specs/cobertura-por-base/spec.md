# Spec Delta

## ADDED Requirements

### Requirement: Expressão executada é bloco literal

Os blocos das expressões que se executam — a executada, as de fidelidade e a sonda — SHALL
ser submetidos como estão. Nenhum desses blocos SHALL referenciar conjunto de busca `#n`;
referência MUST reprovar a conferência daquela base, nomeando base e expressão.

#### Scenario: Bloco composto por conjuntos

- **WHEN** o bloco da EB4 da WoS é `#5 AND (#3 OR #4) AND PY=(2017-2026)`
- **THEN** a conferência da WoS reprova, nomeando a EB4 e a referência a conjunto, e as
  demais bases não são afetadas

#### Scenario: Bloco literal

- **WHEN** todos os blocos das expressões executadas, de fidelidade e de sonda se submetem
  como estão, sem `#n`
- **THEN** essa dimensão não reprova nenhuma base

#### Scenario: Expressão derivada sem bloco

- **WHEN** a EB1, derivada localmente, não tem bloco na ficha
- **THEN** a ausência não reprova, porque a expressão não se executa

### Requirement: Expressão derivada não leva bloco

Expressão derivada que não se executa MUST NOT ter bloco na forma padrão; bloco presente
MUST reprovar a conferência daquela base, nomeando a expressão derivada. A forma longa
declarada é representação não executada e não entra nessa conferência.

#### Scenario: Bloco em expressão derivada

- **WHEN** a EB1, derivada localmente, traz um bloco cercado na forma padrão
- **THEN** a conferência daquela base reprova, nomeando a expressão derivada, e as demais
  não são afetadas

### Requirement: Termos do bloco conferem com as facetas declaradas

O conjunto de termos de cada bloco executado, de fidelidade e de sonda SHALL ser o das
strings das facetas que a expressão declara. Operador, campo e valor de filtro MUST NOT
contar como termo. Termo ausente ou termo estranho MUST reprovar a conferência daquela
base, nomeando expressão e termo.

#### Scenario: Bloco defasado por emenda na seção 3

- **WHEN** um termo da STR3 é alterado e o bloco da EB4 mantém o termo anterior
- **THEN** a conferência daquela base reprova, nomeando o termo ausente e o termo que
  deixou de ser vigente

#### Scenario: Termo estranho no bloco

- **WHEN** um bloco traz termo que não consta de nenhuma faceta declarada nem de filtro
- **THEN** a conferência daquela base reprova, nomeando o termo

#### Scenario: Valor de filtro não é termo

- **WHEN** o bloco traz `DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")`
- **THEN** os valores do filtro não contam como termos estranhos

#### Scenario: Operador de proximidade não é termo

- **WHEN** o bloco traz `NEAR/5` ou `W/5` entre grupos de termos
- **THEN** o operador não conta como termo estranho

## MODIFIED Requirements

### Requirement: Autoteste prova a reprovação por base

O autoteste SHALL injetar, um de cada vez, um defeito na ficha de uma única base — termo que
só consta do quadro, referência a conjunto `#n` no bloco executado e termo defasado em
relação à seção 3 —, exigindo que a conferência dessa base reprove e que a das demais não
reprove.

#### Scenario: Defeito só na BRAPCI

- **WHEN** o autoteste devolve à ficha da BRAPCI um termo que só consta do quadro
- **THEN** a conferência da BRAPCI reprova e as das demais bases passam; outro resultado
  faz o autoteste falhar

#### Scenario: Conjunto devolvido ao bloco

- **WHEN** o autoteste troca o bloco da EB4 de uma base por um bloco que referencia `#n`
- **THEN** a conferência daquela base reprova e as das demais passam

#### Scenario: Bloco defasado em uma base

- **WHEN** o autoteste troca um termo do bloco executado de uma base por termo fora das
  facetas declaradas
- **THEN** a conferência daquela base reprova e as das demais passam
