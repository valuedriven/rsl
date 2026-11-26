# Spec Delta

## Purpose

Atribuir a cada semente esperada numa base e não recuperada pela executada a causa da
perda — indexação, filtro, âncoras, proximidade ou faceta não âncora —, a partir de
consultas por nível montadas da composição da base e das exportações que o pesquisador
obtém no navegador.

## ADDED Requirements

### Requirement: Restrição por DOI declarada na fonte
A fonte de cada base SHALL poder declarar, em `[composicao]`, o campo opcional `doi`: o
modelo da restrição a um DOI, com o marcador `{doi}`. O código MUST NOT conter a forma da
restrição de nenhuma base. Modelo sem `{doi}` reprova a leitura da base com
PROTOCOLO_ILEGIVEL.

#### Scenario: Modelo declarado
- **WHEN** a fonte da Scopus declara `doi = "DOI({doi})"`
- **THEN** a restrição ao DOI `10.1111/exsy.12246` é `DOI(10.1111/exsy.12246)`

#### Scenario: Modelo sem marcador
- **WHEN** a fonte da WoS declara `doi = "DO="`
- **THEN** a leitura da WoS reprova com PROTOCOLO_ILEGIVEL, nomeando `composicao` e `doi`

#### Scenario: Campo na gramática
- **WHEN** se executa `documentos gramatica`
- **THEN** `[composicao]` traz o campo `doi`, opcional, com a exigência do marcador

### Requirement: Sementes diagnosticadas
`aderencia diagnosticar <base>` SHALL diagnosticar as sementes que o arquivo de sementes
espera na base, que têm DOI e que a aderência não conta como recuperadas na base (casamento
exato por título nos registros da executada). As esperadas sem DOI SHALL ser listadas como
não diagnosticáveis por DOI, com o identificador.

#### Scenario: Sementes perdidas na Scopus
- **WHEN** a executada da Scopus recuperou SE9 e não recuperou SE2, SE3, SE4, SE7 e SE8,
  todas com DOI
- **THEN** o diagnóstico cobre SE2, SE3, SE4, SE7 e SE8, e não SE9

#### Scenario: Semente sem DOI
- **WHEN** uma semente esperada na base não tem DOI no arquivo de sementes
- **THEN** ela aparece como não diagnosticável por DOI e não entra em nenhuma consulta

#### Scenario: Nada a diagnosticar
- **WHEN** a executada recuperou todas as sementes esperadas na base
- **THEN** o comando informa que não há perda a diagnosticar e sai com OK, sem gravar

### Requirement: Consultas por nível montadas da composição
O comando SHALL montar uma consulta por nível, com os DOIs das sementes diagnosticadas
unidos por `OR`. Os níveis SHALL ser cumulativos: (1) só os DOIs; (2) mais as cláusulas
de filtro da consulta; (3) mais a sonda sem proximidade; (4) mais a sonda; (5) mais a
executada. Sem proximidade na base, o nível 3 se funde ao 4.

#### Scenario: Níveis da Scopus
- **WHEN** a Scopus declara `doi = "DOI({doi})"` e proximidade `W/5` entre as âncoras
- **THEN** o nível 1 é `(DOI(a) OR DOI(b) …)`; o 2 acrescenta as cláusulas de filtro de
  EB5; o 3 é o nível 1 com `AND` e o texto de EB5 sem proximidade; o 4, com o texto de EB5;
  o 5, com o texto de EB4

#### Scenario: Filtros na interface
- **WHEN** um critério da base tem destino de interface
- **THEN** o nível 2 relata o filtro a aplicar na interface, com o rótulo do critério, além
  do texto da consulta

#### Scenario: Base sem proximidade
- **WHEN** a composição da base não declara proximidade
- **THEN** o diagnóstico tem os níveis 1, 2, âncoras (3 e 4 fundidos) e 5

#### Scenario: Base sem modelo de DOI
- **WHEN** a fonte da base não declara `[composicao] doi`
- **THEN** o comando sai com REPROVADO, nomeando a base e o campo a declarar, sem gravar

#### Scenario: Base particionada
- **WHEN** a sonda ou a executada da base tem mais de uma consulta
- **THEN** o comando sai com REPROVADO, nomeando a base e a expressão, sem gravar

### Requirement: Nível lido da execução registrada
O nível cuja expressão tem execução válida registrada na base SHALL ser lido da exportação
registrada, filtrada pelos DOIs, e não ser pedido ao pesquisador. O relato SHALL dizer, por
nível, se ele é submetido ou lido de execução registrada, com a execução.

#### Scenario: Sonda e executada registradas
- **WHEN** a Scopus tem EB4 e EB5 registradas
- **THEN** os níveis 4 e 5 são lidos de BD2/EX4 e BD2/EX1, e o pesquisador submete só os
  níveis 1 a 3

### Requirement: Roteiro sem resultados
Sem `--retorno`, o comando SHALL imprimir o roteiro: as sementes diagnosticadas com o DOI,
o texto de cada nível a submeter, os níveis lidos de execução registrada e os argumentos
para registrar o resultado. Nesse modo, MUST NOT gravar.

#### Scenario: Roteiro da Scopus
- **WHEN** se executa `aderencia diagnosticar scopus`
- **THEN** o terminal traz o texto dos níveis 1 a 3, a indicação de que os níveis 4 e 5 vêm
  de BD2/EX4 e BD2/EX1, e o exemplo da chamada com `--retorno`, `--exportacao` e
  `--data-hora`; nenhum arquivo é gravado

### Requirement: Resultado de cada nível submetido
Com resultado, o comando SHALL exigir, para cada nível submetido, `--retorno N K` e, com
K maior que zero, `--exportacao N ARQUIVO`, além de `--data-hora` ISO 8601. Os registros
lidos de cada exportação SHALL ser iguais a K. Falta, sobra ou divergência sai com DADOS,
sem gravar.

#### Scenario: Nível sem resultado
- **WHEN** o nível 3 devolve zero e se passa `--retorno 3 0` sem exportação
- **THEN** o nível 3 conta como vazio

#### Scenario: Exportação que não confere
- **WHEN** se passa `--retorno 1 5` e a exportação do nível 1 tem 4 registros
- **THEN** o comando sai com DADOS, nomeando o nível, o retorno e os registros lidos

#### Scenario: Nível faltando
- **WHEN** falta `--retorno` de um nível submetido
- **THEN** o comando sai com DADOS, nomeando o nível

### Requirement: Coerência entre os níveis
Cada nível SHALL ser subconjunto do anterior, nos DOIs das sementes diagnosticadas, e nenhum
nível pode trazer DOI fora delas. A violação sai com REPROVADO, nomeando o nível e os DOIs,
sem gravar: é sinal de consulta submetida diferente da montada.

#### Scenario: DOI que reaparece
- **WHEN** o DOI de SE3 falta no nível 2 e aparece no nível 3
- **THEN** o comando sai com REPROVADO, nomeando o nível 3 e o DOI

#### Scenario: DOI estranho
- **WHEN** a exportação do nível 1 traz um DOI que não é de semente diagnosticada
- **THEN** o comando sai com REPROVADO, nomeando o nível 1 e o DOI

### Requirement: Causa atribuída pelo primeiro nível vazio
A causa de cada semente SHALL ser o primeiro nível em que o DOI dela não aparece. As
causas, em ordem, são: `não indexada`, `filtro`, `âncoras`, `proximidade`, `faceta não
âncora`. Presente em todos os níveis, SHALL relatar `presente na executada`, indício de
falha do casamento por título.

#### Scenario: Semente não indexada
- **WHEN** o DOI de SE4 não aparece no nível 1
- **THEN** a causa de SE4 é `não indexada`, e o relato sugere `indexada = não` na planilha
  de aderência, sem preenchê-la

#### Scenario: Semente filtrada
- **WHEN** o DOI de SE2 aparece no nível 1 e não no 2
- **THEN** a causa de SE2 é `filtro`, com o ano, o idioma e o tipo documental lidos da
  exportação do nível 1

#### Scenario: Semente perdida pela proximidade
- **WHEN** o DOI de SE7 aparece até o nível 3 e não no 4
- **THEN** a causa de SE7 é `proximidade`

#### Scenario: Semente presente na executada
- **WHEN** o DOI de uma semente aparece no nível 5
- **THEN** a causa relatada é `presente na executada`, e o relato aponta a divergência com
  o casamento por título da aderência

### Requirement: Resultado gravado
Com resultado aceito, o comando SHALL gravar `[saidas] anatomia` (`anatomia_<base>.csv`),
com uma linha por semente diagnosticada (identificador, DOI, presença em cada nível e causa),
e `[saidas] anatomia_consultas` (`anatomia_consultas_<base>.csv`), com cada nível: texto,
origem (submetido ou execução), retorno, arquivo e data e hora.

#### Scenario: Arquivos gravados
- **WHEN** o diagnóstico da Scopus é aceito
- **THEN** `data/anatomia_scopus.csv` tem uma linha por semente diagnosticada, e
  `data/anatomia_consultas_scopus.csv` tem uma linha por nível, com o texto submetido

### Requirement: Autoteste prova a anatomia
O autoteste SHALL provar, com exportações sintéticas e uma fonte de ensaio, cada causa, a
recusa por exportação que não confere, a recusa por incoerência entre níveis e a recusa por
modelo de DOI ausente.

#### Scenario: Volta da causa a olho
- **WHEN** a atribuição deixa de usar o primeiro nível vazio
- **THEN** o autoteste falha em ao menos um caso de causa

#### Scenario: Volta da tolerância à incoerência
- **WHEN** a conferência de subconjunto entre níveis é desligada
- **THEN** o autoteste falha no caso do DOI que reaparece
