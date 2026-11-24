# Spec Delta

## Purpose

Descrever, por base, cada teste que o pesquisador deve executar para verificar a sintaxe e
os demais recursos da base, como um roteiro executável. O roteiro fica ligado ao elemento
que o teste verifica e ao resultado registrado, de modo que nenhuma afirmação de medição
exista sem a sondagem que a sustenta.

## ADDED Requirements

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
(`teste` ou `controle`), `texto` literal e `onde`, o lugar de submissão. Sondagem sem
consulta, ou com papel fora do domínio, MUST reprovar a base com PROTOCOLO_ILEGIVEL. Ciclo em
`depende_de` também MUST reprovar.

#### Scenario: Ciclo de dependência
- **WHEN** a SD1 depende da SD2, e a SD2 depende da SD1
- **THEN** a leitura reprova, nomeando as duas sondagens

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
3. cada consulta em bloco cercado, precedida do papel e do lugar de submissão;
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
Ao terminar, o comando SHALL exibir a citação `BDn/<id>` e, por elemento da sondagem, a
`situacao` e a `citacao` a aplicar na fonte. O comando MUST NOT alterar a fonte.

#### Scenario: Sondagem já feita registrada depois
- **WHEN** se executa `sondagens registrar eric SD3 --retorno 0 --retorno 214 --leitura 2
  --data-hora 2026-11-12T15:40 --evidencia data/evidencia/sondagens/eric_sd3.png`
- **THEN** o registro ganha, em BD3, o resultado `sd3-2026-11-12`, com as duas consultas
  declaradas e os seus retornos. A saída mostra `BD3/sd3-2026-11-12` e os elementos de SD3
  com a situação da leitura 2

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
  declarada e resultado ainda não levado à fonte

#### Scenario: Exigência de evidência desligada
- **WHEN** a recusa por falta de evidência é desligada
- **THEN** o caso do registro sem evidência falha
