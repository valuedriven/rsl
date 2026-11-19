# cobertura-por-base Specification

## Purpose

Conferir a string de busca de cada ficha de base contra o vocabulário vigente do protocolo,
de modo que termo retirado não volte e termo vigente não falte sem redução declarada.

## Requirements

### Requirement: Vocabulário vigente é a string do protocolo
O termo vigente de uma faceta SHALL ser o que consta da STR correspondente no protocolo,
filtrado pelos idiomas e camadas que a ficha declara. O quadro terminológico MUST servir
apenas para classificar o termo por idioma e camada, e nenhuma lista de retirados SHALL ser
mantida no código ou na ficha.

#### Scenario: Termo vigente ausente da base
- **WHEN** um termo da STR, nos idiomas e camadas declarados, falta na string da base e não
  consta da redução declarada nem é alcançado por derivação declarada
- **THEN** a conferência daquela base reprova, nomeando faceta e termo

#### Scenario: Termo do quadro fora da STR
- **WHEN** um termo consta do quadro mas não da STR
- **THEN** ele não é esperado na string da base e a ausência não reprova

### Requirement: Termo da base deriva da STR
Todo termo da string de uma base SHALL corresponder, em flexão ou pela derivação declarada, a
um termo da STR da mesma faceta. Termo que só exista no quadro, ou em lugar nenhum, MUST
reprovar.

#### Scenario: Termo retirado devolvido à base
- **WHEN** a ficha usa, mesmo em flexão, um termo que está no quadro e não está na STR
- **THEN** a conferência daquela base reprova, dizendo que o termo não está na string do
  protocolo

#### Scenario: Termo inventado
- **WHEN** a ficha usa um termo que não deriva de nenhum termo do protocolo
- **THEN** a conferência daquela base reprova, nomeando o termo

### Requirement: Composição da base segue o protocolo
As facetas de cada expressão na ficha SHALL ser as que a composição lida do protocolo
determina, e a expressão executada pela base SHALL ser a que o protocolo declara executada.

#### Scenario: Base executa outra expressão
- **WHEN** a ficha executa uma expressão diferente da declarada executada no protocolo
- **THEN** a conferência daquela base reprova, nomeando as duas

### Requirement: Reprovação é por base
Defeito na forma de uma base MUST reprovar apenas a conferência daquela base.

#### Scenario: Uma ficha divergente
- **WHEN** só a ficha da BRAPCI diverge do protocolo
- **THEN** só a conferência da BRAPCI reprova

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
### Requirement: Forma de execução declarada na ficha
Cada ficha SHALL declarar a sua forma de execução numa linha `- Execução: única` ou
`- Execução: particionada`. Linha ausente, repetida ou com outro valor MUST reprovar a
conferência daquela base, nomeando a ficha; nenhum valor padrão é presumido.

#### Scenario: Ficha sem declaração
- **WHEN** a ficha da ERIC não tem a linha de execução
- **THEN** a conferência da ERIC reprova, nomeando a ficha, e as demais bases não são afetadas

#### Scenario: Valor fora do domínio
- **WHEN** a ficha declara `- Execução: dividida`
- **THEN** a conferência daquela base reprova, nomeando o valor e os admitidos

### Requirement: Faceta da forma curada identificada pelo código
Na forma curada da ficha, a faceta de cada consulta SHALL ser identificada pelo código
`FCTn`. Símbolo gráfico (emoji, cor) MUST NOT identificar faceta.

#### Scenario: Consulta marcada só por emoji
- **WHEN** a célula de facetas de uma consulta curada traz `🟦` sem `FCT1`
- **THEN** a consulta é lida sem faceta atribuída

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

### Requirement: Critérios da ficha conferem com o protocolo

O conjunto de IDs de critério citados na seção 2 de cada ficha SHALL ser igual ao conjunto
de IDs da tabela de critérios do protocolo. ID citado que não existe no protocolo, ou
critério do protocolo ausente da ficha, MUST reprovar só a conferência daquela base,
nomeando ficha e ID.

#### Scenario: Ficha cita critério inexistente

- **WHEN** o protocolo é renumerado e a ficha de uma base ainda cita o ID antigo
- **THEN** a conferência daquela base reprova, nomeando a ficha e o ID citado como ausente
  do protocolo e o ID vigente como ausente da ficha, e as demais bases corrigidas não
  reprovam

#### Scenario: Critério agrupado numa linha

- **WHEN** a ficha cita `CE1 / CE2` numa mesma linha
- **THEN** os dois IDs contam como citados

#### Scenario: Fichas em dia

- **WHEN** as quatro fichas citam exatamente os IDs do protocolo
- **THEN** essa dimensão não reprova nenhuma base

### Requirement: Autoteste prova a reprovação do critério defasado

O autoteste SHALL injetar, numa cópia, um ID de critério inexistente na ficha de uma única
base e exigir que só aquela base reprove.

#### Scenario: Defeito injetado numa base

- **WHEN** o autoteste troca um ID existente por outro inexistente na ficha da Scopus
- **THEN** a conferência da Scopus reprova e as das demais bases não reprovam
