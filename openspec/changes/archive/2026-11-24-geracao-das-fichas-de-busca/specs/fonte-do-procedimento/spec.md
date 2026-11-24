# Spec Delta

## Purpose

Guardar, por base, numa fonte que se edita, o conhecimento próprio da base que o
procedimento de busca expõe: os dados estruturados e a prosa livre. O procedimento passa a
ser saída de geração, e nenhum valor de base fica no código.

## ADDED Requirements

### Requirement: Fonte localizada pela sigla
A fonte do procedimento de cada base SHALL ser a pasta localizada pela sigla no padrão
`[documentos] procedimento_fonte` do `config.toml`, que MUST conter `{sigla}`. A pasta SHALL
conter `procedimento.toml` e, opcionalmente, fragmentos markdown de nome fixo. Pasta ou
`procedimento.toml` inexistente MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a base e o
caminho procurado.

#### Scenario: Fonte ausente
- **WHEN** a tabela de bases do protocolo traz `eric` e não existe
  `docs/procedimentos/eric/procedimento.toml`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando BD3, `eric` e o caminho

#### Scenario: Padrão sem a sigla
- **WHEN** `[documentos] procedimento_fonte` não contém `{sigla}`
- **THEN** o comando termina com CONFIGURACAO, nomeando a chave

### Requirement: Esquema do arquivo de dados
`procedimento.toml` SHALL seguir o esquema que a gramática declara, com as tabelas e os
campos de cada uma, e com o tipo, a exigência e o domínio de cada campo. Os casos abaixo
MUST reprovar a base com PROTOCOLO_ILEGIVEL, nomeando a base, a tabela e o campo:
- TOML inválido;
- campo obrigatório ausente;
- campo de tipo errado;
- valor fora do domínio;
- campo desconhecido.

#### Scenario: Situação fora do domínio
- **WHEN** um elemento de `[[sintaxe]]` da WoS tem `situacao = "medido"`
- **THEN** a leitura da WoS reprova com PROTOCOLO_ILEGIVEL, nomeando `sintaxe`, `situacao`
  e os valores admitidos; as demais bases não são afetadas

#### Scenario: Campo desconhecido
- **WHEN** `[cobertura]` da Scopus traz `plurais = "explícito"`
- **THEN** a leitura da Scopus reprova, nomeando o campo desconhecido

#### Scenario: Tabelas do esquema
- **WHEN** se executa `documentos gramatica`
- **THEN** o grupo da fonte traz as tabelas `[[sintaxe]]`, `[[criterios]]`, `[cobertura]`,
  `[[reducao]]`, `[composicao]`, `[[consultas_de_campo]]`, `[[subconjuntos]]`,
  `[[radical]]`, `[execucao]`, `[[regras_de_montagem]]`, `[[curadas]]`, `[[sementes]]`,
  `ressalvas` e `[[sondagens]]`

### Requirement: Elementos de sintaxe cobrem as categorias mínimas
Cada elemento de `[[sintaxe]]` SHALL ter `categoria`, com um valor do domínio de categorias
mínimas que a gramática declara. Cada categoria SHALL ter ao menos um elemento na fonte de cada base, ainda que com `situacao =
"inexistente"`. A categoria sem elemento MUST reprovar a base com PROTOCOLO_ILEGIVEL,
nomeando a categoria. O elemento de `lematizacao` admite `idioma`.

#### Scenario: Domínio das categorias
- **WHEN** se executa `documentos gramatica`
- **THEN** as categorias mínimas exibidas são `campos`, `operadores`, `frase`,
  `truncamento`, `lematizacao`, `proximidade`, `agrupamento`, `limite_consulta`,
  `limite_retorno`, `limite_exportacao`, `filtros`, `vocabulario_controlado`,
  `idioma_indexacao` e `exportacao`

#### Scenario: Categoria esquecida
- **WHEN** a fonte da Scopus não tem elemento de categoria `limite_exportacao`
- **THEN** a leitura da Scopus reprova, nomeando a categoria; as demais bases não são
  afetadas

#### Scenario: Recurso que a base não tem
- **WHEN** a BRAPCI não oferece vocabulário controlado, e a fonte o declara com `situacao =
  "inexistente"` e a fonte da ausência
- **THEN** a categoria está coberta

### Requirement: Medição exige citação
O elemento de `[[sintaxe]]` com `situacao = "medicao"` e a regra de `[[regras_de_montagem]]`
com `situacao = "medicao"` SHALL ter `citacao` na forma `BDn/<id>`, com o `BDn` da própria
base. A falta da citação MUST reprovar a base com PROTOCOLO_ILEGIVEL. A existência do `id`
no registro SHALL ser conferida por `dados conferir` (`cobertura-por-base`).

#### Scenario: Regra dita medida sem lastro
- **WHEN** a regra "um grupo não mistura campos" da ERIC tem `situacao = "medicao"` sem
  `citacao`
- **THEN** a leitura da ERIC reprova, nomeando a regra e o campo `citacao`

### Requirement: Critérios declarados com destino
Cada linha de `[[criterios]]` SHALL ter:
- `ids`, uma lista de `CEn`;
- `rotulo`;
- `destino`, que é `consulta`, `interface`, `variante`, `aproximado`, `dispensado` ou
  `nao`;
- `como`.

O destino `consulta` e o destino `variante` SHALL ter `clausula`, que é a sintaxe literal do
filtro. A `clausula` de destino `consulta` é a única fonte dos filtros dos blocos de
expressão.

#### Scenario: Filtro sem cláusula
- **WHEN** o critério CE1 da WoS tem `destino = "consulta"` sem `clausula`
- **THEN** a leitura da WoS reprova, nomeando CE1 e `clausula`

### Requirement: Fragmentos de prosa com nome fixo
A pasta da fonte SHALL admitir só os fragmentos que a gramática declara:
- `notas_sintaxe.md`;
- `estrategia_de_proximidade.md`;
- `como_executar.md`, obrigatório;
- `variantes.md`;
- `notas_execucao.md`;
- `notas_sementes.md`.

Fragmento de nome desconhecido, ou a falta de `como_executar.md`, MUST reprovar a base com
PROTOCOLO_ILEGIVEL, nomeando o arquivo e os nomes admitidos.

#### Scenario: Fragmento com nome errado
- **WHEN** a pasta da BRAPCI traz `variante.md`
- **THEN** a leitura da BRAPCI reprova, nomeando o arquivo e os nomes admitidos

### Requirement: Fragmento não quebra o esqueleto
Os casos abaixo MUST reprovar a base com PROTOCOLO_ILEGIVEL, nomeando o fragmento e a linha:
- título de nível 1 a 3 em qualquer fragmento;
- título `####` fora de `variantes.md`;
- a linha `- Execução:` em qualquer fragmento.

#### Scenario: Título que quebraria o esqueleto
- **WHEN** `como_executar.md` da Scopus traz `## Passos`
- **THEN** a leitura da Scopus reprova, nomeando o fragmento e a linha

### Requirement: Campo pendente impede a geração
O valor `PENDENTE` num campo de `procedimento.toml`, e a linha `PENDENTE` num fragmento,
SHALL marcar o que ainda não foi apurado. A fonte com marca pendente MUST reprovar a leitura
da base com PROTOCOLO_ILEGIVEL. A reprovação SHALL listar de uma vez todas as marcas, com
tabela e campo ou fragmento e linha. `procedimentos gerar` MUST NOT gravar o procedimento
dessa base.

#### Scenario: Fonte recém-iniciada
- **WHEN** a fonte da base `lisa` foi criada por `procedimentos iniciar lisa` e ainda não foi
  preenchida
- **THEN** `procedimentos gerar lisa` reprova, listando todos os campos `PENDENTE`, e não
  grava

### Requirement: Início da fonte de uma base nova
`python3 -m rsl procedimentos iniciar <sigla>` SHALL criar, de forma atômica, a pasta da
fonte da base, com `procedimento.toml` e `como_executar.md`. O que é derivável do protocolo,
do quadro e do arquivo de sementes vem preenchido; o que exige apuração na base ou decisão do
pesquisador vem com a marca `PENDENTE`. `plural` vem `explícito`, que vale até a lematização
ser medida.

#### Scenario: O que vem preenchido
- **WHEN** se executa `procedimentos iniciar lisa` para base registrada no protocolo
- **THEN** a fonte traz preenchidos uma linha de `[[criterios]]` por critério do protocolo
  (`ids` e `rotulo`), os idiomas do quadro por faceta, `camadas = "todas"`, `plural =
  "explícito"`, uma linha de `[[sementes]]` por semente com `lisa` em `bases` e um elemento
  de `[[sintaxe]]` por categoria mínima, `nao_verificado`

#### Scenario: O que vem pendente
- **WHEN** se executa `procedimentos iniciar lisa`
- **THEN** vêm com `PENDENTE` o destino e o *como* de cada critério, o teto, as derivações,
  a composição, a forma de execução, a sondagem de cada elemento e `como_executar.md`

### Requirement: Início recusado
`procedimentos iniciar` MUST recusar-se, sem gravar e nomeando o motivo, quando a sigla não
está na tabela de bases do protocolo, porque base nova é decisão de escopo, com o código USO,
e quando a pasta da fonte já existe, para não sobrescrever trabalho, com o código USO.

#### Scenario: Base fora do protocolo
- **WHEN** se executa `procedimentos iniciar lisa` e o protocolo não tem a sigla `lisa`
- **THEN** o comando nada grava e diz que a base precisa primeiro ser registrada no
  protocolo

#### Scenario: Fonte já existente
- **WHEN** se executa `procedimentos iniciar wos`
- **THEN** o comando nada grava e nomeia a pasta existente

#### Scenario: Esqueleto preenchido do que é derivável
- **WHEN** o protocolo registra a base `lisa` e se executa `procedimentos iniciar lisa`
- **THEN** a fonte traz todos os IDs de critério do protocolo, as sementes com `lisa` em
  `bases` e um elemento de sintaxe por categoria mínima, e `documentos conferir` reprova a
  base por campos pendentes, listando-os

### Requirement: Nenhum valor de base no código
O código MUST NOT conter sigla de base, nome de campo de base, operador de proximidade de
base, cláusula de filtro nem texto específico de uma base. Tudo o que difere de base para
base SHALL vir da fonte. O esqueleto, o texto fixo e as categorias mínimas são forma e SHALL
ser declarados uma única vez na gramática.

#### Scenario: Campo de base no código
- **WHEN** se procura `TS=`, `TITLE-ABS-KEY` ou `abstract:` nos módulos de `src/rsl/`, fora
  do autoteste
- **THEN** não há ocorrência

### Requirement: Autoteste prova a fonte
O autoteste SHALL injetar, numa cópia da fonte de uma única base, um defeito de cada vez
para cada validação desta capacidade, e exigir PROTOCOLO_ILEGIVEL só naquela base. SHALL
também iniciar, numa cópia do protocolo com uma base fictícia, a fonte por `procedimentos
iniciar` e exigir as recusas e os campos pendentes. Cada caso MUST falhar com a validação
correspondente desligada.

#### Scenario: Defeitos cobertos
- **WHEN** se executa `projeto autoteste`
- **THEN** há caso para campo obrigatório ausente, campo desconhecido, valor fora do domínio,
  categoria mínima sem elemento, medição sem citação, filtro sem cláusula, fragmento de nome
  desconhecido, título proibido em fragmento e marca `PENDENTE`

#### Scenario: Validação desligada
- **WHEN** a exigência de citação na medição é desligada
- **THEN** o caso da medição sem citação falha
