## MODIFIED Requirements

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
