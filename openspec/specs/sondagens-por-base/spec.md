# sondagens-por-base Specification

## Purpose

Descrever, por base, cada teste que o pesquisador deve executar para verificar a sintaxe e
os demais recursos da base, como um roteiro executável. O roteiro fica ligado ao elemento
que o teste verifica e ao resultado registrado, de modo que nenhuma afirmação de medição
exista sem a sondagem que a sustenta.

## Requirements

### Requirement: Sondagem declarada como roteiro executável
Cada `[[sondagens]]` da fonte da base SHALL ter os campos que a gramática declara: `id`
(`SDn`, em sequência por base), `elementos` (elementos de `[[sintaxe]]` ou regras de
`[[regras_de_montagem]]` da mesma fonte), `objetivo`, `pre_requisitos`, `consultas`,
`passos`, `observar`, `leituras` e `evidencia`; `depende_de` é opcional. O campo ausente, ou o elemento que não existe, MUST reprovar a base
com PROTOCOLO_ILEGIVEL, nomeando a sondagem e o campo.

#### Scenario: Elemento inexistente
- **WHEN** a SD2 da WoS aponta o elemento "Proximidade entre frases", que não está em
  `[[sintaxe]]`
- **THEN** a leitura da WoS reprova, nomeando SD2 e o elemento

### Requirement: Consultas da sondagem
Cada sondagem SHALL ter ao menos uma consulta em `[[sondagens.consultas]]`, com `papel`
(`teste` ou `controle`), `onde` (o lugar de submissão) e, de modo exclusivo, `texto` literal
ou `expressao`, a referência de "Consulta por referência a uma expressão". Sondagem sem
consulta, ou com papel fora do domínio, MUST reprovar a base com PROTOCOLO_ILEGIVEL. Ciclo em
`depende_de` também MUST reprovar.

#### Scenario: Ciclo de dependência
- **WHEN** a SD1 depende da SD2, e a SD2 depende da SD1
- **THEN** a leitura reprova, nomeando as duas sondagens

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
aplicada na composição da expressão, e não no texto final:
- `sem_proximidade = true` une as âncoras por `AND` no lugar do operador de proximidade;
- `distancia = N`, com N inteiro positivo, mantém o operador de proximidade da base com a
  distância N no lugar da declarada;
- `metade = { faceta = "FCTn", parte = 1 | 2 }` mantém só uma das duas metades contíguas dos
  termos da faceta. A primeira metade fica com o termo excedente;
- `restricao = { termos = [...] }` acrescenta, unido por `AND` e antes das cláusulas de
  filtro, um grupo com os termos em forma literal, no campo das âncoras e com a regra de
  aspas da base.

As transformações se combinam, exceto `sem_proximidade` com `distancia`. No roteiro, a
origem da consulta SHALL nomear cada transformação, e os termos de `restricao` SHALL vir
listados com a marca "fora do protocolo".

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

#### Scenario: Outra distância de proximidade
- **WHEN** uma consulta da WoS declara `expressao = "EB5"` e `distancia = 15`, e a base
  declara `NEAR` com distância 5
- **THEN** o texto é o de EB5 com `NEAR/15` entre os grupos das âncoras, e difere do texto
  de EB5 só nesse operador

#### Scenario: Grupo de restrição
- **WHEN** uma consulta da WoS declara `expressao = "EB5"`, `sem_proximidade = true` e
  `restricao = { termos = ["machine learning", "deep learning"] }`
- **THEN** o texto é o de EB5 com `AND` entre as âncoras e com
  `AND TS=("machine learning" OR "deep learning")` antes das cláusulas de filtro, e o roteiro
  lista os dois termos como fora do protocolo

#### Scenario: Strings alteradas depois da declaração
- **WHEN** o quadro terminológico da FCT2 muda, e o procedimento da WoS é regenerado
- **THEN** as consultas com `distancia` e com `restricao` trazem a STR2 nova, sem edição da
  fonte

### Requirement: Referência inválida reprova
A leitura da fonte ou a composição da base MUST reprovar a base com PROTOCOLO_ILEGIVEL,
nomeando a sondagem e a consulta, quando a consulta:
- tem `texto` e `expressao` juntos ou nenhum dos dois;
- aponta expressão sem bloco na base, ou consulta, faceta ou parte inexistente;
- omite `consulta` numa expressão de várias consultas;
- declara `sem_proximidade` ou `distancia` numa base sem proximidade, ou as duas juntas;
- declara `distancia` igual à da base, ou que não é inteiro positivo;
- declara `restricao` com lista vazia.

#### Scenario: Expressão inexistente
- **WHEN** a SD5 da WoS declara `expressao = "EB9"`
- **THEN** a leitura da WoS reprova, nomeando SD5, a consulta 1 e EB9

#### Scenario: Sem proximidade na base que não a usa
- **WHEN** uma consulta da BRAPCI declara `sem_proximidade = true`, e a BRAPCI não declara
  proximidade
- **THEN** a leitura da BRAPCI reprova, nomeando a sondagem e a transformação

#### Scenario: Distância que não muda a consulta
- **WHEN** uma consulta da WoS declara `distancia = 5`, e a base declara `NEAR/5`
- **THEN** a leitura da WoS reprova, nomeando a sondagem, a consulta e a transformação, porque
  o controle seria cópia do teste

#### Scenario: Proximidade e distância juntas
- **WHEN** uma consulta declara `sem_proximidade = true` e `distancia = 15`
- **THEN** a leitura reprova, nomeando a sondagem, a consulta e as duas transformações

#### Scenario: Restrição vazia
- **WHEN** uma consulta da Scopus declara `restricao = { termos = [] }`
- **THEN** a leitura da Scopus reprova, nomeando a sondagem, a consulta e `restricao`

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

### Requirement: Leituras da sondagem
Cada sondagem SHALL ter ao menos duas leituras em `[[sondagens.leituras]]`, cada uma com
`resultado`, `conclusao` e `estado`, sendo uma delas a do resultado inconclusivo. `estado`
fora do domínio de `situacao`, ou a falta da leitura inconclusiva, MUST reprovar a base com
PROTOCOLO_ILEGIVEL.

#### Scenario: Sondagem sem leitura inconclusiva
- **WHEN** a SD3 da ERIC tem só as leituras "retorno > 0" e "retorno = 0"
- **THEN** a leitura da ERIC reprova, nomeando SD3 e a leitura inconclusiva ausente

### Requirement: Elemento não verificado aponta sondagem
Todo elemento de `[[sintaxe]]` e toda regra de `[[regras_de_montagem]]` com `situacao =
"nao_verificado"` SHALL ter um destes campos:
- `sondagem`, que aponta uma sondagem existente que o lista em `elementos`;
- `sem_sondagem`, com o motivo, por exemplo "não se usa".

A falta dos dois MUST reprovar a base com PROTOCOLO_ILEGIVEL. A sondagem que não lista
nenhum elemento SHALL ser relatada, sem reprovar.

#### Scenario: Elemento sem teste
- **WHEN** o elemento "Tratamento de diacríticos" da WoS é `nao_verificado`, sem `sondagem`
  nem `sem_sondagem`
- **THEN** a leitura da WoS reprova, nomeando o elemento

#### Scenario: Elemento dispensado com motivo
- **WHEN** o elemento "Truncamento `*`" da BRAPCI é `nao_verificado` com `sem_sondagem =
  "não se usa"`
- **THEN** essa dimensão não reprova, e a §1 mostra o motivo

### Requirement: Roteiro escrito no procedimento
O procedimento gerado SHALL trazer, na seção 1, a coluna "Sondagem" na tabela de sintaxe,
com o `SDn` ou o motivo de `sem_sondagem`. Quando houver sondagem, SHALL trazer também a
subseção `### Sondagens a executar`. A subseção SHALL abrir com a linha fixa de segurança:
uma consulta por vez, sem nova tentativa automática, parada diante de captcha, aviso de
atividade atípica ou bloqueio. As sondagens SHALL vir na ordem de `depende_de` e, dentro
dela, na ordem do `id`.

#### Scenario: Ordem por dependência
- **WHEN** a SD1 depende da SD4
- **THEN** a SD4 aparece antes da SD1 no roteiro

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

### Requirement: Registro do resultado por comando
`python3 -m rsl sondagens registrar <sigla> <SDn>` SHALL acrescentar, de forma atômica, o
resultado de uma sondagem a `bases.BDn.sondagens[]` do registro de execução, criando o
arquivo, com todas as bases do protocolo, quando não existe. Recebe `--retorno` uma vez por consulta declarada, na ordem,
`--leitura` (número da leitura observada), `--data-hora` ISO 8601 obrigatório, `--evidencia`
(um ou mais arquivos) e, opcionais, `--submetido <k> <texto>` e `--observacao`.

#### Scenario: Registro criado pelo comando
- **WHEN** `data/registro_execucao.json` não existe e se registra uma sondagem da ERIC
- **THEN** o arquivo criado traz BD1 a BD4, e `dados conferir` não o reprova por base ausente

#### Scenario: Ajuda do registro
- **WHEN** se executa `sondagens registrar -h`
- **THEN** a ajuda mostra os argumentos e diz que `--data-hora` é obrigatório porque o
  registro costuma ser posterior à sondagem

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

### Requirement: Registro recusado sem lastro
`sondagens registrar` MUST recusar a gravação, sem gravar, quando:
- a sigla não é base do protocolo, com o código USO;
- a fonte não declara a sondagem, com PROTOCOLO_ILEGIVEL;
- o número de `--retorno` difere do número de consultas declaradas, com USO;
- a leitura não existe, com USO;
- falta `--data-hora`, com USO;
- falta `--evidencia`, com USO;
- um arquivo de evidência não existe, com DADOS.

#### Scenario: Sem evidência
- **WHEN** se executa `sondagens registrar eric SD3 --retorno 0 --retorno 214 --leitura 2
  --data-hora 2026-11-12T15:40` sem `--evidencia`
- **THEN** nada é gravado, e a saída tem o código USO e diz que sondagem sem evidência não
  se registra

### Requirement: Resultado registrado conferido
`dados conferir` MUST reprovar só aquela base quando um resultado de `bases.BDn.sondagens`:
- não tem um campo obrigatório;
- repete o `id` na base;
- tem `sondagem` que não existe na fonte da base;
- tem `leitura` que não é nenhuma das leituras declaradas.

`dados conferir` SHALL relatar, sem reprovar, o resultado não incorporado: aquele cuja
leitura leva a uma situação diferente da que o elemento tem na fonte.

#### Scenario: Resultado de sondagem inexistente
- **WHEN** o registro tem, em BD3, um resultado com `sondagem = "SD9"`, e a fonte da ERIC não
  tem SD9
- **THEN** `dados conferir` reprova a ERIC, nomeando o resultado e SD9

#### Scenario: Resultado ainda não levado à fonte
- **WHEN** `sd3-2026-11-12` registra a leitura de estado `medicao`, e o elemento de SD3 ainda
  é `nao_verificado` na fonte da ERIC
- **THEN** `dados conferir` relata o elemento e a citação a aplicar, e o código não muda por
  esse relato

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
