# Spec Delta

## ADDED Requirements

### Requirement: Verificação por medição remete a execução registrada

Toda citação do arquivo de registro de execução numa ficha, em tabela ou em prosa, SHALL
nomear a execução na forma `(BDn/<id>)`, com `BDn` da própria base. A conferência dos
arquivos alimentados MUST reprovar, só naquela base, quando falta o identificador, quando
`BDn` é de outra base ou quando `BDn/<id>` não existe no registro, nomeando ficha, linha e
referência.

#### Scenario: Citação sem identificador de execução

- **WHEN** a seção 1 da ficha da WoS declara "`NEAR/x` — Verificado por medição —
  `data/registro_execucao.json` (BD1)"
- **THEN** `--conferir-dados` reprova a WoS, nomeando a linha e a falta do identificador, e
  as demais bases não são afetadas

#### Scenario: Citação em prosa

- **WHEN** o cabeçalho da ficha da BRAPCI diz "apurada por medição, com as sondagens em
  `data/registro_execucao.json` (BD4)"
- **THEN** `--conferir-dados` reprova a BRAPCI pela falta do identificador de execução

#### Scenario: Base trocada na citação

- **WHEN** a ficha da ERIC cita `(BD1/sonda-near)`
- **THEN** `--conferir-dados` reprova a ERIC, nomeando a citação de outra base

#### Scenario: Execução citada inexistente

- **WHEN** a linha cita `(BD2/sonda-w5)` e o registro não tem a execução `sonda-w5` em BD2
- **THEN** `--conferir-dados` reprova a Scopus, nomeando a referência ausente

#### Scenario: Registro ausente

- **WHEN** a ficha cita uma execução e `data/registro_execucao.json` não existe
- **THEN** `--conferir-dados` reprova aquela base pela citação sem lastro, além de reportar
  o arquivo ausente

#### Scenario: Elemento não verificado

- **WHEN** a linha declara **Não verificado** e não cita o registro
- **THEN** essa dimensão não reprova

#### Scenario: Citação válida

- **WHEN** a linha cita `(BD1/sonda-near)` e o registro tem essa execução em BD1
- **THEN** essa dimensão não reprova

### Requirement: Autoteste prova a reprovação da verificação sem lastro

O autoteste SHALL injetar, numa cópia, citação de medição sem identificador e citação de
execução inexistente na ficha de uma única base, e exigir que só aquela base reprove. Sem
registro de execução, esses casos SHALL constar como não executados, com o motivo.

#### Scenario: Defeito injetado numa base

- **WHEN** o autoteste injeta `(BD1)` sem identificador na ficha da WoS, com registro
  presente
- **THEN** a conferência da WoS reprova e as das demais bases não reprovam

#### Scenario: Registro ausente no autoteste

- **WHEN** o autoteste roda sem `data/registro_execucao.json`
- **THEN** os casos desta exigência constam como não executados e não contam como
  resultado esperado
