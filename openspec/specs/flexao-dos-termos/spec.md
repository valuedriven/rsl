# flexao-dos-termos Specification

## Purpose

Dar a cada termo da STR as suas formas de número, por regra regular de pt, en e es e por
exceção declarada pelo pesquisador, sem adivinhar a flexão que a regra não decide, para que o
plural explícito de uma base seja completo por construção.

## Requirements

### Requirement: Plural por regra regular
Para cada termo de um idioma com plural explícito, a flexão SHALL produzir o plural pela
regra regular do idioma. Em en, flexiona-se a última palavra. Em pt e es, flexionam-se a
primeira palavra e as que a seguem até a primeira preposição, artigo ou contração. O
plural SHALL ter a grafia do idioma, inclusive o acento que a flexão retira ou acrescenta.

#### Scenario: Locução em inglês
- **WHEN** a STR3 tem `teaching strategy`
- **THEN** a flexão produz `teaching strategies`

#### Scenario: Locução em português com preposição
- **WHEN** a STR3 tem `estratégia de ensino`
- **THEN** a flexão produz `estratégias de ensino`

#### Scenario: Substantivo e adjetivo em português
- **WHEN** a STR3 tem `prática pedagógica`
- **THEN** a flexão produz `práticas pedagógicas`

#### Scenario: Acento retirado em espanhol
- **WHEN** a STR4 tem `situación de uso`
- **THEN** a flexão produz `situaciones de uso`

### Requirement: Flexão indecidível reprova
A palavra cuja terminação a regra não decide sem ambiguidade MUST reprovar a geração do
procedimento que a usa com plural explícito, nomeando o termo, o idioma e a terminação. São
exemplos o -ão do português, o -s final sem acento, o -f do inglês, a palavra de classe
adjetiva e o termo com conjunção. A reprovação vale até haver exceção declarada para o
termo. A flexão MUST NOT escolher uma das formas possíveis.

#### Scenario: Terminação em -ão
- **WHEN** a STR1 tem `classificação facetada` e não há exceção para o termo
- **THEN** `procedimentos gerar` reprova, nomeando `classificação facetada`, pt e `-ão`, e não
  grava

#### Scenario: Adjetivo isolado
- **WHEN** a STR2 tem `educational` e não há exceção para o termo
- **THEN** `procedimentos gerar` reprova, nomeando `educational`, en e a classe adjetiva

#### Scenario: Adjetivo isolado em português
- **WHEN** a STR2 tem `educacional` em pt e não há exceção para o termo
- **THEN** `procedimentos gerar` reprova, nomeando `educacional`, pt e a classe adjetiva; o
  adjetivo que segue o núcleo numa locução (`modelo conceitual`) não é recusado

### Requirement: Exceções declaradas pelo pesquisador
O arquivo de exceções, localizado por `[documentos] flexoes` do `config.toml`, SHALL
declarar, por termo e idioma, uma de três exceções: `irregular`, com as formas de plural;
`nao_contavel`, sem plural; ou `vetada`, com a forma que a regra produziria e que não se
usa. Toda exceção SHALL ter `origem`, que é a fonte ou a decisão que a sustenta. A exceção
prevalece sobre a regra.

#### Scenario: Plural irregular
- **WHEN** o arquivo declara `thesaurus`, en, `irregular`, com `thesauri` e `thesauruses`
- **THEN** a flexão de `thesaurus` produz essas duas formas, e nenhuma outra

#### Scenario: Não contável
- **WHEN** o arquivo declara `education`, en, `nao_contavel`
- **THEN** `education` entra no bloco sem plural, e a conferência não o aponta como termo só
  no singular

### Requirement: Exceção inválida reprova
Exceção sem `origem`, com tipo fora do domínio ou repetida para o mesmo termo e idioma MUST
reprovar com PROTOCOLO_ILEGIVEL, nomeando o termo e o campo. Exceção de termo que não está
em nenhuma STR nem em lista escrita à mão na fonte de alguma base (subconjunto ou forma
curada) SHALL ser relatada, sem reprovar.

#### Scenario: Exceção sem origem
- **WHEN** uma exceção do arquivo não tem `origem`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando o termo e o campo

#### Scenario: Exceção órfã
- **WHEN** o arquivo declara exceção para `practice`, que não está em nenhuma STR
- **THEN** a conferência relata a exceção órfã, e o código não muda por esse relato

#### Scenario: Exceção usada só num subconjunto
- **WHEN** o arquivo declara exceção para `ontology engineering`, en, que não está em nenhuma
  STR, e o subconjunto `STR1b` da fonte da ERIC traz o termo
- **THEN** a conferência não a relata como órfã

### Requirement: Forma gerada visível antes da gravação
Toda forma produzida pela regra ou pela exceção SHALL aparecer no ensaio de `procedimentos gerar`,
por base, faceta e idioma, com a indicação de origem (`regra` ou `exceção`). Assim, o
pesquisador revisa as formas antes de elas entrarem no procedimento.

#### Scenario: Ensaio lista a origem
- **WHEN** se executa `procedimentos gerar scopus` com STR1 contendo `thesaurus` e `ontology`
- **THEN** o ensaio lista `ontologies (regra)` e `thesauri (exceção)` em FCT1, en

### Requirement: Autoteste prova a flexão
O autoteste SHALL verificar a regra sobre os pares dos cenários. SHALL também provar que a
terminação indecidível reprova sem exceção e passa com ela, que a exceção sem `origem` dá
PROTOCOLO_ILEGIVEL e que a exceção `nao_contavel` cala a reprovação de termo só no
singular. Cada caso MUST falhar com a regra ou a conferência correspondente desligada.

#### Scenario: Indecidível sem a guarda
- **WHEN** a reprovação da flexão indecidível é desligada
- **THEN** o caso da terminação em -ão falha
