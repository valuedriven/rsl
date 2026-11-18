# Spec Delta

## Purpose

Ler o protocolo de estratégia de pesquisa como fonte única de verdade, com valores padrão num
arquivo de configuração que o protocolo sobrescreve, e conferir a coerência interna do
documento sem fixar valores esperados no código.

## ADDED Requirements

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
