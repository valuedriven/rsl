# Spec Delta

## MODIFIED Requirements

### Requirement: Nenhum parâmetro fixado no código
O código MUST NOT conter valor de parâmetro do projeto: composição e papel das expressões,
âncoras, recorte, limiares, dimensões de critério, instrumentos (sigla, modo, caminho,
idiomas, facetas), bases (sigla, ficha), idiomas do quadro, caminhos de dados, campos da
planilha e o caminho do próprio protocolo. Todo parâmetro SHALL vir do protocolo, da ficha
da base ou de `config.toml` na raiz.

#### Scenario: Busca por valor fixado
- **WHEN** se procura em `src/protocolo.py` por constante de parâmetro (ex.: `0.80`, `2017`,
  `"EB4"`, `"tbci"`, `"wos"`, `"pt"`)
- **THEN** não há ocorrência fora de autoteste

### Requirement: Protocolo sobrescreve o padrão da configuração
`config.toml` SHALL conter valor padrão para todo parâmetro **não estrutural**. Quando o
protocolo declara o parâmetro, o valor do protocolo SHALL prevalecer; quando não declara,
vale o padrão. Parâmetro estrutural não tem padrão (ver "Parâmetros estruturais só do
protocolo").

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
- **WHEN** `config.toml` não existe, não é TOML válido ou não tem um parâmetro não estrutural
- **THEN** o script termina com erro que nomeia o arquivo e o parâmetro

### Requirement: Origem de cada parâmetro é visível
`--mostrar` SHALL exibir, para cada parâmetro, o valor em uso e a sua origem (protocolo,
ficha da base ou padrão da configuração).

#### Scenario: Parâmetro vindo do padrão
- **WHEN** o limiar de divergência vem de `config.toml`
- **THEN** `--mostrar` o exibe com origem "padrão (config.toml)"

#### Scenario: Parâmetro estrutural
- **WHEN** `--mostrar` exibe a composição das expressões, os instrumentos, as bases ou os
  idiomas
- **THEN** a origem exibida é sempre o protocolo, e a forma de execução de cada base tem
  origem na ficha

### Requirement: Conferência verifica coerência interna
`--conferir` SHALL reprovar contradições internas: termo de STR ausente do quadro da faceta;
expressão sem as âncoras; executada que não seja a união das específicas; sonda que não seja a
conjunção das âncoras; semente sem base ou com base fora da tabela de bases; dimensão de
critério em uso não declarada no protocolo; faixa de sensibilidade com inferior ≥ superior.

#### Scenario: Termo da string fora do quadro
- **WHEN** uma STR contém um termo que não consta do quadro da sua faceta
- **THEN** `--conferir` reprova, nomeando a faceta e o termo

#### Scenario: Dimensão de critério com grafia do protocolo
- **WHEN** a lista de dimensões em uso tem "Idioma" e o protocolo declara CE3 com "Idioma"
- **THEN** `--conferir` não reprova por dimensão de critério

#### Scenario: Distribuição das sementes não é declarada em prosa
- **WHEN** o protocolo traz o conjunto-semente só na tabela, sem parágrafo de incidências
- **THEN** `--conferir` não reprova por distribuição; a distribuição por base é calculada da
  tabela e exibida

### Requirement: Autoteste prova que cada conferência reprova
`--autoteste` SHALL injetar, numa cópia em memória, ao menos um defeito por conferência de
coerência, por regra de precedência e por parâmetro estrutural (ausente e com valor inválido),
e exigir que cada um reprove. Defeito não detectado MUST fazer o autoteste falhar.

#### Scenario: Conferência que não reprova
- **WHEN** um defeito injetado não é detectado pela conferência correspondente
- **THEN** `--autoteste` falha, nomeando o defeito

#### Scenario: Parâmetro estrutural ausente
- **WHEN** o autoteste retira de uma cópia do protocolo a coluna `Sigla` da tabela de bases
- **THEN** a leitura reprova; leitura que caia em valor padrão faz o autoteste falhar

## ADDED Requirements

### Requirement: Parâmetros estruturais só do protocolo
Composição das expressões, instrumentos, bases, conjunto-semente e idiomas do quadro SHALL
ser lidos só do protocolo, sem padrão. Ausência ou valor inválido MUST reprovar a leitura,
nomeando tabela, linha e campo. `config.toml` que ainda traga `padroes.composicao`, `cores`,
`fichas`, `instrumentos` ou `idiomas` MUST reprovar, para que não haja segunda fonte.

#### Scenario: Tabela estrutural ausente
- **WHEN** o protocolo não tem a tabela "Bases de dados"
- **THEN** a leitura reprova nomeando a tabela, e nenhum valor da configuração é usado

#### Scenario: Chave retirada ainda presente na configuração
- **WHEN** `config.toml` traz a seção `[fichas.wos]`
- **THEN** o script termina com erro que nomeia a chave e diz que ela vem do protocolo

### Requirement: Linha de faceta sem cor
Cada faceta SHALL ser lida da linha `Faceta n (FCTn): nome`, seguida opcionalmente de
`(âncora obrigatória k)`. O leitor MUST NOT extrair nem exigir cor; hífen dentro do nome
pertence ao nome.

#### Scenario: Nome com hífen
- **WHEN** a linha é `Faceta 3 (FCT3): Práticas do processo de ensino-aprendizagem`
- **THEN** o nome lido é "Práticas do processo de ensino-aprendizagem" e FCT3 não é âncora

#### Scenario: Âncora entre parênteses
- **WHEN** a linha termina em `(âncora obrigatória 1)`
- **THEN** a faceta é lida como âncora e o parêntese não integra o nome

### Requirement: Idiomas lidos do cabeçalho do quadro
Cada tabela do quadro terminológico SHALL ter cabeçalho `| FCTn | idioma | idioma | ... |`; o
idioma de cada coluna é o nome no cabeçalho, não a posição. Os idiomas do projeto SHALL ser
os do cabeçalho, e o conjunto MUST ser o mesmo em todas as tabelas, sem repetição nem célula
vazia.

#### Scenario: Colunas em outra ordem
- **WHEN** o cabeçalho de FCT2 é `| FCT2 | en | pt | es |`
- **THEN** os termos da coluna `pt` de FCT2 são lidos como português

#### Scenario: Idiomas diferentes entre tabelas
- **WHEN** a tabela de FCT4 declara `pt | en` e as demais `pt | en | es`
- **THEN** a leitura reprova, nomeando a faceta e os idiomas divergentes

### Requirement: Bases lidas da tabela do protocolo
As bases SHALL ser lidas da tabela "Bases de dados": identificador `BDn`, sigla e nome. Sigla
e identificador MUST ser únicos. A ficha de cada base SHALL ser localizada pela sigla, no
padrão de caminho do `config.toml`; ficha inexistente MUST reprovar, nomeando base e caminho.

#### Scenario: Ficha da sigla não existe
- **WHEN** o padrão é `docs/busca_base_{sigla}.md` e não existe `docs/busca_base_eric.md`
- **THEN** a leitura reprova, nomeando BD3, a sigla `eric` e o caminho procurado

#### Scenario: Padrão sem a sigla
- **WHEN** o padrão de caminho do `config.toml` não contém `{sigla}`
- **THEN** o script termina com erro de configuração que nomeia a chave

#### Scenario: Sigla repetida
- **WHEN** duas linhas da tabela têm a sigla `eric`
- **THEN** a leitura reprova, nomeando a sigla

### Requirement: Conjunto-semente lido de tabela
O conjunto-semente SHALL ser lido da tabela `ID Semente | Semente | Bases`, com autoria, ano,
título e DOI extraídos da referência. Cada base citada MUST ser sigla da tabela de bases, na
grafia exata; semente sem base reprova.

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Distribuição calculada
- **WHEN** a tabela de sementes é lida
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas da tabela
