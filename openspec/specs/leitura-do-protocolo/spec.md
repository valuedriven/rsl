# leitura-do-protocolo Specification

## Purpose

Ler o protocolo de estratégia de pesquisa como fonte única de verdade, com valores padrão num
arquivo de configuração que o protocolo sobrescreve, e conferir a coerência interna do
documento sem fixar valores esperados no código.

## Requirements

### Requirement: Nenhum parâmetro fixado no código
O código MUST NOT conter valor de parâmetro do projeto: composição e papel das expressões,
âncoras, recorte, limiares, dimensões de critério, mapa de instrumentos, mapa base → ficha,
caminhos de dados, campos da planilha e o caminho do próprio protocolo. Todo parâmetro SHALL
vir do protocolo ou de `config.toml` na raiz.

#### Scenario: Busca por valor fixado
- **WHEN** se procura em `src/protocolo.py` por constante de parâmetro (ex.: `0.80`, `2017`,
  `"EB4"`, `"TBCI"`)
- **THEN** não há ocorrência fora de autoteste

### Requirement: Protocolo sobrescreve o padrão da configuração
`config.toml` SHALL conter valor padrão para todo parâmetro. Quando o protocolo declara o
parâmetro, o valor do protocolo SHALL prevalecer; quando não declara, vale o padrão.

#### Scenario: Protocolo declara o parâmetro
- **WHEN** a regra de ajuste do protocolo declara 80% e `config.toml` traz outro padrão
- **THEN** o leitor usa 80%

#### Scenario: Protocolo não declara o parâmetro
- **WHEN** o protocolo não declara o limiar de divergência da fidelidade
- **THEN** o leitor usa o padrão de `config.toml`

#### Scenario: Declaração ilegível não cai no padrão
- **WHEN** o protocolo tem o trecho do parâmetro mas o valor não é legível
- **THEN** a conferência reprova, nomeando o parâmetro, sem usar o padrão

#### Scenario: Configuração ausente ou incompleta
- **WHEN** `config.toml` não existe, não é TOML válido ou não tem um parâmetro
- **THEN** o script termina com erro que nomeia o arquivo e o parâmetro

### Requirement: Arquivo do protocolo é parametrizado
O caminho do documento do protocolo a ser lido SHALL vir de `config.toml`. Por ser o que
localiza o protocolo, esse parâmetro MUST NOT ser sobrescrito pelo protocolo. O caminho do
próprio `config.toml` é o único fixado: a raiz do projeto.

#### Scenario: Outro arquivo de protocolo
- **WHEN** `config.toml` aponta para outro arquivo de protocolo
- **THEN** todos os scripts leem esse arquivo, e `--mostrar` exibe o caminho em uso

#### Scenario: Protocolo inexistente
- **WHEN** o caminho configurado não existe
- **THEN** o script termina com erro que nomeia o caminho e a chave do `config.toml`

### Requirement: Origem de cada parâmetro é visível
`--mostrar` SHALL exibir, para cada parâmetro, o valor em uso e a sua origem (protocolo ou
padrão da configuração).

#### Scenario: Parâmetro vindo do padrão
- **WHEN** o limiar de divergência vem de `config.toml`
- **THEN** `--mostrar` o exibe com origem "padrão (config.toml)"

### Requirement: Conferência verifica coerência interna
`--conferir` SHALL reprovar contradições internas: termo de STR ausente do quadro da faceta;
expressão sem as âncoras; executada que não seja a união das específicas; sonda que não seja a
conjunção das âncoras; distribuição das sementes em prosa diferente da do mapa; dimensão de
critério em uso não declarada no protocolo; faixa de sensibilidade com inferior ≥ superior.

#### Scenario: Termo da string fora do quadro
- **WHEN** uma STR contém um termo que não consta do quadro da sua faceta
- **THEN** `--conferir` reprova, nomeando a faceta e o termo

#### Scenario: Dimensão de critério com grafia do protocolo
- **WHEN** a lista de dimensões em uso tem "Idioma" e o protocolo declara CE3 com "Idioma"
- **THEN** `--conferir` não reprova por dimensão de critério

### Requirement: Autoteste prova que cada conferência reprova
`--autoteste` SHALL injetar, numa cópia em memória, ao menos um defeito por conferência de
coerência e por regra de precedência, e exigir que cada um reprove. Defeito não detectado MUST
fazer o autoteste falhar.

#### Scenario: Conferência que não reprova
- **WHEN** um defeito injetado não é detectado pela conferência correspondente
- **THEN** `--autoteste` falha, nomeando o defeito

### Requirement: Somente biblioteca padrão
Os scripts SHALL executar só com a biblioteca padrão do Python 3.11 ou superior; a
configuração MUST ser lida sem pacote externo.

#### Scenario: Ambiente sem pacotes extras
- **WHEN** os scripts rodam num Python 3 limpo, sem pacotes instalados
- **THEN** a leitura de `config.toml` e todas as conferências funcionam

### Requirement: Scripts sem referência a versão do protocolo
Mensagens, comentários e nomes do código MUST NOT referir versão ou emenda específica do
protocolo; o histórico de versões vive em `data/historico.md`.

#### Scenario: Busca por referência de versão
- **WHEN** se procura por `v1`, `v2`, `_V2` ou "emenda v2" em `src/`
- **THEN** não há ocorrência

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
