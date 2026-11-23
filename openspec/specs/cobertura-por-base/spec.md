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
um termo da STR da mesma faceta, ou ser termo do quadro dessa faceta subsumido por um termo
da STR, na regra de `geracao-das-strings`. Termo que só exista no quadro sem estar subsumido,
ou que não exista em lugar nenhum, MUST reprovar. O subsumido aceito SHALL ser relatado por
base, sem reprovar.

#### Scenario: Termo retirado devolvido à base
- **WHEN** a ficha usa, mesmo em flexão, um termo que está no quadro, não está na STR e não
  é subsumido por termo da STR
- **THEN** a conferência daquela base reprova, dizendo que o termo não está na string do
  protocolo

#### Scenario: Termo inventado
- **WHEN** a ficha usa um termo que não deriva de nenhum termo do protocolo
- **THEN** a conferência daquela base reprova, nomeando o termo

#### Scenario: Subsumido em campo próprio
- **WHEN** a ficha da ERIC usa `"ontology engineering"` no resumo (`STR1b`), e a STR1 tem
  `ontology` e não tem `ontology engineering`, que está no quadro de FCT1
- **THEN** a conferência da ERIC não reprova por esse termo, e o relata como subsumido por
  `ontology`

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

### Requirement: Plural declarado por base
A declaração de cobertura de cada ficha SHALL ter a linha `plural`, com o valor `explícito`
ou `pela lematização`. A linha ausente, ou com outro valor, MUST reprovar com
PROTOCOLO_ILEGIVEL.

#### Scenario: Linha ausente
- **WHEN** a declaração de cobertura da ficha da Scopus não tem a linha `plural`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a ficha e a linha

#### Scenario: Valor fora do domínio
- **WHEN** a linha `plural` da ficha da WoS diz `omitido`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, citando os dois valores admitidos

### Requirement: Plural pela lematização exige lematização medida
Ficha que declara `plural: pela lematização` SHALL ter, na seção 1, a linha "Lematização"
com o estado verificado por medição e a citação `(BDn/<id>)` de uma execução registrada
daquela base. A conferência MUST reprovar só aquela base quando a linha falta, quando o
estado não é verificado ou quando a citação falta.

#### Scenario: Lematização não verificada
- **WHEN** a ficha da ERIC declara `plural: pela lematização` e a seção 1 diz "Lematização —
  **Não verificado**"
- **THEN** `--conferir` reprova a ERIC, nomeando a declaração e a linha sem medição; as
  demais bases não são afetadas

#### Scenario: Lematização medida
- **WHEN** a ficha declara `plural: pela lematização` e a linha "Lematização" diz
  verificado por medição com `(BD3/sonda-plural)`
- **THEN** essa dimensão não reprova em `--conferir`, e a existência de `BD3/sonda-plural`
  é conferida por `--conferir-dados`, como em "Verificação por medição remete a execução
  registrada"

#### Scenario: Plural explícito
- **WHEN** a ficha declara `plural: explícito`
- **THEN** o estado da linha "Lematização" não reprova

### Requirement: Termo só no singular relatado
Em ficha com `plural: explícito`, a conferência SHALL relatar, por faceta e sem reprovar, os
termos da STR presentes na string da base em uma só forma de número e não alcançados por
truncamento.

#### Scenario: Plural esquecido
- **WHEN** a ficha da Scopus declara `plural: explícito` e traz `"teaching strategy"` sem
  `"teaching strategies"` nem truncamento que o alcance
- **THEN** `--conferir` relata `teaching strategy` em FCT3 da Scopus, e o código não muda
  por esse relato

### Requirement: Autoteste prova a reprovação do plural sem lastro
O autoteste SHALL injetar, na cópia da ficha de uma só base, a declaração `plural: pela
lematização` com a linha "Lematização" não verificada, e exigir que só aquela base reprove;
e SHALL retirar a linha `plural` e exigir PROTOCOLO_ILEGIVEL.

#### Scenario: Defeito injetado numa base
- **WHEN** o autoteste injeta `plural: pela lematização` na ficha da WoS, com a lematização
  não verificada
- **THEN** a conferência da WoS reprova, as demais não reprovam, e o autoteste falha se
  isso não ocorrer

### Requirement: Teto de caracteres declarado por base
A declaração de cobertura de cada ficha SHALL ter a linha `teto de caracteres`, com um
número inteiro positivo de caracteres (`1400` ou `1.400`) ou `nenhum`. A linha ausente, ou
com outro valor, MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a ficha e a linha.

#### Scenario: Linha ausente
- **WHEN** a declaração de cobertura da ficha da WoS não tem a linha `teto de caracteres`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a ficha e a linha

#### Scenario: Valor ilegível
- **WHEN** a linha `teto de caracteres` da ficha diz `curto`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando o domínio do teto

### Requirement: Consulta acima do teto reprova a base
Com teto numérico, a conferência SHALL medir o comprimento, em caracteres, de cada consulta
executável da base e MUST reprovar só aquela base quando alguma passar do teto, nomeando a
expressão, a consulta, o comprimento e o teto. Consulta executável é cada bloco das
expressões da seção 4, salvo a forma longa e o bloco rotulado como não executado, e cada
consulta da forma curada. Com `nenhum`, a conferência SHALL relatar, sem reprovar, a maior
consulta executável da base.

#### Scenario: Consulta acima do teto
- **WHEN** a ficha da ERIC declara `teto de caracteres | 1400` e a consulta 4a2 tem 1.450
  caracteres
- **THEN** `conferir` reprova a ERIC, nomeando EB4, a consulta 4a2, 1450 e 1400; as demais
  bases não são afetadas

#### Scenario: Consulta no limite
- **WHEN** a maior consulta da base tem exatamente o comprimento do teto declarado
- **THEN** essa dimensão não reprova

#### Scenario: Sem teto
- **WHEN** a ficha da Scopus declara `teto de caracteres | nenhum`
- **THEN** `conferir` relata a maior consulta da Scopus com o comprimento, e o código não
  muda por esse relato

### Requirement: Estratégia de proximidade não é forma executável
A subseção `### Estratégia de proximidade` da seção 4 da ficha SHALL ser ignorada pela
leitura: bloco cercado nela não entra no derivado da base, não se executa e não se confere.
A subseção não é exigida.

#### Scenario: Bloco cercado na estratégia de proximidade
- **WHEN** a ficha da WoS ganha uma subseção "Estratégia de proximidade" com um bloco
  cercado
- **THEN** o derivado da WoS é igual ao de antes e `conferir` não muda o código

### Requirement: Autoteste prova o teto e a estratégia de proximidade
O autoteste SHALL:
- declarar, na cópia da ficha de uma só base, um teto uma unidade abaixo da maior consulta
  e exigir que só aquela base reprove;
- declarar o teto igual à maior consulta, com separador de milhar, e exigir que passe;
- retirar a linha `teto de caracteres` e exigir PROTOCOLO_ILEGIVEL;
- deformar o valor do teto e exigir PROTOCOLO_ILEGIVEL;
- inserir a subseção de estratégia de proximidade com bloco cercado e exigir o derivado
  inalterado.

#### Scenario: Conferência desligada
- **WHEN** a conferência do comprimento contra o teto é desligada
- **THEN** o caso do teto abaixo da maior consulta falha
