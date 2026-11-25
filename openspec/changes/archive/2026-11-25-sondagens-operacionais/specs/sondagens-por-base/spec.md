# Delta de especificação

## ADDED Requirements

### Requirement: Consulta por referência a uma expressão
Uma consulta de sondagem SHALL poder declarar `expressao = "EBn"` no lugar de `texto`. O
texto da consulta é então o da expressão na composição corrente da base, o mesmo da seção 4.
Quando a expressão tem mais de uma consulta, `consulta` SHALL dizer qual: o identificador
dela ou `mais_longa`. Com uma só, `consulta` é dispensável.

#### Scenario: Expressão de consulta única
- **WHEN** a SD5 da WoS declara `expressao = "EB4"`, e EB4 tem uma só consulta
- **THEN** o roteiro traz, no bloco da consulta, o mesmo texto do bloco de EB4 da seção 4

#### Scenario: Expressão particionada
- **WHEN** a SD12 da ERIC declara `expressao = "EB4"` e `consulta = "mais_longa"`, e EB4 tem
  várias consultas
- **THEN** o roteiro traz o texto da consulta de EB4 com mais caracteres e o identificador
  dela

### Requirement: Transformações declaradas da referência
Uma consulta por referência SHALL poder declarar uma transformação de conjunto fechado,
aplicada na composição da expressão: `sem_proximidade = true`, que une as âncoras por `AND`
no lugar do operador de proximidade, e `metade = { faceta = "FCTn", parte = 1 | 2 }`, que
mantém só uma das duas metades contíguas dos termos da faceta. A primeira metade fica com o
termo excedente.

#### Scenario: Controle sem proximidade
- **WHEN** a SD2 da Scopus declara, no controle, `expressao = "EB5"` e
  `sem_proximidade = true`
- **THEN** o controle é o texto de EB5 com `AND` entre os grupos das âncoras, e o teste
  com `expressao = "EB5"` é o texto de EB5 com `W/5`; os dois diferem só nesse operador

#### Scenario: Metades de uma faceta
- **WHEN** a SD4 da BRAPCI declara dois controles com `expressao = "EB5"` e `metade` da
  faceta 🟦, partes 1 e 2
- **THEN** cada controle traz EB5 com metade dos termos da faceta 🟦, e a união dos termos
  das duas metades, na ordem, é a string inteira da faceta

### Requirement: Referência inválida reprova
A leitura da fonte ou a composição da base MUST reprovar a base com PROTOCOLO_ILEGIVEL,
nomeando a sondagem e a consulta, quando a consulta tem `texto` e `expressao` juntos ou
nenhum dos dois, aponta expressão sem bloco na base, omite `consulta` numa expressão de
várias consultas, aponta consulta, faceta ou parte inexistente, ou declara `sem_proximidade`
numa base sem proximidade.

#### Scenario: Expressão inexistente
- **WHEN** a SD5 da WoS declara `expressao = "EB9"`
- **THEN** a leitura da WoS reprova, nomeando SD5, a consulta 1 e EB9

#### Scenario: Sem proximidade na base que não a usa
- **WHEN** uma consulta da BRAPCI declara `sem_proximidade = true`, e a BRAPCI não declara
  proximidade
- **THEN** a leitura da BRAPCI reprova, nomeando a sondagem e a transformação

### Requirement: Consulta literal sem marca de referência
O `texto` de uma consulta de sondagem MUST NOT conter marca de referência a outro trecho do
procedimento: identificador de expressão, string ou faceta (`EBn`, `STRn`, `FCTn`), a cor de
uma faceta ou "procedimento gerado". Isso reprova a base com PROTOCOLO_ILEGIVEL, nomeando a
sondagem, a consulta e a marca, e indicando o uso de `expressao`.

#### Scenario: Consulta em prosa
- **WHEN** a SD4 da Scopus declara `texto = "o bloco de EB4 no procedimento gerado"`
- **THEN** a leitura da Scopus reprova, nomeando SD4, a consulta 1 e a marca `EB4`, e
  indica `expressao`

#### Scenario: Consulta literal comum
- **WHEN** a SD1 da WoS declara `texto = "TS=(ontology AND education)"`
- **THEN** essa consulta não reprova

## MODIFIED Requirements

### Requirement: Consultas da sondagem
Cada sondagem SHALL ter ao menos uma consulta em `[[sondagens.consultas]]`, com `papel`
(`teste` ou `controle`), `onde` (o lugar de submissão) e, de modo exclusivo, `texto` literal
ou `expressao`, a referência de "Consulta por referência a uma expressão". Sondagem sem
consulta, ou com papel fora do domínio, MUST reprovar a base com PROTOCOLO_ILEGIVEL. Ciclo em
`depende_de` também MUST reprovar.

#### Scenario: Ciclo de dependência
- **WHEN** a SD1 depende da SD2, e a SD2 depende da SD1
- **THEN** a leitura reprova, nomeando as duas sondagens

### Requirement: Forma de cada sondagem no roteiro
Cada sondagem SHALL vir em `#### SDn — <objetivo>`, nesta ordem:
1. os elementos verificados, com a situação atual;
2. os pré-requisitos;
3. cada consulta em bloco cercado que contém só a consulta, pronta para colar, precedida do
   papel e do lugar de submissão; na consulta por referência, também da origem (expressão,
   consulta e transformação) e do número de caracteres;
4. os passos numerados;
5. o que observar;
6. a tabela de leitura, com resultado, conclusão e estado;
7. a evidência a registrar;
8. os resultados registrados, com a citação `(BDn/<id>)`, quando houver.

#### Scenario: Sondagem de proximidade
- **WHEN** a fonte da WoS declara a SD1, com o teste `TS=(ontology NEAR/5 education)`, o
  controle `TS=(ontology AND education)` e três leituras
- **THEN** o procedimento da WoS traz `#### SD1 — …` com os dois blocos rotulados "teste"
  e "controle", a tabela com as três leituras e a linha "NEAR/x entre grupos" com SD1 na
  coluna "Sondagem"

#### Scenario: Consulta por referência no roteiro
- **WHEN** a SD5 da WoS declara `expressao = "EB4"`
- **THEN** a linha que precede o bloco diz que a consulta é EB4 e o seu número de
  caracteres, e o bloco contém só o texto de EB4

#### Scenario: Strings alteradas
- **WHEN** o quadro terminológico muda, as strings e o procedimento da WoS são regenerados
- **THEN** o bloco da SD5 acompanha o novo texto de EB4 sem edição da fonte, e o
  procedimento não gerado de novo reprova em `documentos conferir`

### Requirement: Forma do resultado registrado
O resultado gravado SHALL ter `id` (`sd<n>-<data>`, com sufixo quando se repete),
`sondagem`, `data_hora`, `consultas` (texto submetido e retorno de cada uma), `leitura`
(resultado e estado da leitura escolhida), `evidencia` (caminhos relativos) e `observacao`.
O texto submetido de uma consulta por referência SHALL ser o literal resolvido no momento do
registro, salvo `--submetido`. Ao terminar, o comando SHALL exibir a citação `BDn/<id>` e,
por elemento da sondagem, a `situacao` e a `citacao` a aplicar na fonte. O comando MUST NOT
alterar a fonte.

#### Scenario: Sondagem já feita registrada depois
- **WHEN** se executa `sondagens registrar eric SD3 --retorno 0 --retorno 214 --leitura 2
  --data-hora 2026-11-12T15:40 --evidencia data/evidencia/sondagens/eric_sd3.png`
- **THEN** o registro ganha, em BD3, o resultado `sd3-2026-11-12`, com as duas consultas
  declaradas e os seus retornos. A saída mostra `BD3/sd3-2026-11-12` e os elementos de SD3
  com a situação da leitura 2

#### Scenario: Registro de consulta por referência
- **WHEN** se registra a SD5 da WoS, cuja consulta declara `expressao = "EB4"`
- **THEN** o texto gravado da consulta é o literal de EB4 naquele momento, não a referência

### Requirement: Autoteste prova o roteiro e o registro
O autoteste SHALL provar, numa cópia, cada validação, recusa e conferência desta
capacidade, e cada caso MUST falhar com a validação ou a recusa correspondente desligada.

#### Scenario: Casos cobertos
- **WHEN** se executa `projeto autoteste`
- **THEN** há caso para elemento não verificado sem sondagem, leitura inconclusiva ausente,
  ciclo em `depende_de`, ordem do roteiro, gravação de `sondagens registrar`, recusa sem
  evidência e com número de retornos errado, registro criado com todas as bases e, em
  `dados conferir`, resultado com sondagem inexistente, com `id` repetido, com leitura não
  declarada e resultado ainda não levado à fonte. Há caso também para consulta por
  referência igual ao bloco da seção 4, `mais_longa`, `sem_proximidade`, `metade`, cada
  referência inválida, consulta em prosa, consulta por referência que acompanha as strings
  alteradas, e texto resolvido no registro

#### Scenario: Exigência de evidência desligada
- **WHEN** a recusa por falta de evidência é desligada
- **THEN** o caso do registro sem evidência falha

#### Scenario: Conferência de consulta literal desligada
- **WHEN** a recusa de marca de referência em `texto` é desligada
- **THEN** o caso da consulta em prosa falha
