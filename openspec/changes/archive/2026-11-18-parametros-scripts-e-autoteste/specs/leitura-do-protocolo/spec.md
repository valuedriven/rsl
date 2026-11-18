# Spec Delta

## ADDED Requirements

### Requirement: Papéis das expressões expostos uma única vez
O leitor SHALL expor os papéis das expressões — âncoras, específicas, gerais, executada e
sonda — calculados a partir da composição e das âncoras lidas, e a conferência de coerência
e a derivação MUST usar esse mesmo cálculo.

#### Scenario: Papéis do protocolo atual
- **WHEN** o protocolo atual é lido
- **THEN** as específicas são EB2 e EB3, a geral é EB1, a executada é EB4 e a sonda é EB5

### Requirement: Resumo do autoteste distingue caso não executado
O resumo do autoteste SHALL informar à parte os casos não executados e o motivo, e MUST NOT
contá-los como casos com o resultado esperado.

#### Scenario: Arquivos alimentados ausentes
- **WHEN** `--autoteste` roda sem os arquivos alimentados de `data/`
- **THEN** o resumo diz que os casos desses arquivos não foram executados e por quê, em vez
  de contá-los como zero casos aprovados

### Requirement: Composição das expressões na forma estrita
A coluna "Expressão de busca" da tabela de expressões SHALL ser lida na forma estrita
`STRn AND STRn AND (STRn OR STRn)`: `AND` em maiúsculas é a única conjunção e `OR`, em
maiúsculas, só aparece dentro de parênteses. Qualquer outra forma MUST reprovar a leitura
com mensagem que nomeie a expressão.

#### Scenario: Forma estrita
- **WHEN** a expressão é `STR1 AND STR2 AND (STR3 OR STR4)`
- **THEN** a composição lida tem os grupos `[STR1]`, `[STR2]` e `[STR3, STR4]`

#### Scenario: Conjunção fora da forma estrita
- **WHEN** a expressão usa `+` ou `and` como conjunção
- **THEN** a leitura reprova nomeando a expressão e a forma esperada

### Requirement: Cabeçalho da tabela de expressões conferido
O cabeçalho da tabela "Expressões de busca" SHALL coincidir exatamente, na ordem, com
`[expressoes] colunas` do `config.toml`; cabeçalho diferente MUST reprovar a leitura com
mensagem que mostre o cabeçalho lido e o esperado.

#### Scenario: Coluna renomeada
- **WHEN** a coluna "Expressão de busca" aparece como "Combinação de Strings"
- **THEN** a leitura reprova, mostrando o cabeçalho lido e o esperado

### Requirement: Resultado parcial do autoteste declarado
Quando houver caso não executado, o autoteste SHALL declarar que o resultado é parcial e que
o código de saída se refere apenas aos casos executados.

#### Scenario: Arquivos alimentados ausentes
- **WHEN** `--autoteste` termina sem falha e com casos não executados
- **THEN** a última mensagem diz que o autoteste é parcial, quantos casos não rodaram e por
  quê, e que o código de saída 0 vale só para os executados
