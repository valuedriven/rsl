# leitura-do-protocolo Specification

## Purpose

Ler o protocolo de estratégia de pesquisa como fonte única de verdade, com valores padrão num
arquivo de configuração que o protocolo sobrescreve, e conferir a coerência interna do
documento sem fixar valores esperados no código.

## Requirements

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
O conjunto-semente SHALL ser lido da tabela `ID Semente | Semente | Bases | Papel`, com
autoria, ano, título e DOI extraídos da referência. Cada base citada MUST ser sigla da tabela
de bases, na grafia exata; semente sem base reprova. `Papel` SHALL admitir só
`desenvolvimento` ou `validação`; papel ausente ou fora do domínio reprova, nomeando a
semente.

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Distribuição calculada
- **WHEN** a tabela de sementes é lida
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas da tabela

#### Scenario: Papel ausente
- **WHEN** a tabela de sementes não tem a coluna `Papel`, ou a célula de SE4 está vazia
- **THEN** a leitura reprova, nomeando a coluna ou a semente

#### Scenario: Papel fora do domínio
- **WHEN** a semente SE7 declara o papel `teste`
- **THEN** a leitura reprova, nomeando SE7 e os valores admitidos

#### Scenario: Distribuição por papel
- **WHEN** a tabela de sementes é lida
- **THEN** a contagem de sementes de validação e de desenvolvimento, total e por base, é
  calculada da tabela e exibida por `--mostrar`

### Requirement: Conjunto de validação não vazio

O conjunto-semente SHALL ter ao menos uma semente de validação. Conjunto sem semente de
validação MUST reprovar `--conferir`, porque a aderência que decide a passagem não teria
denominador.

#### Scenario: Só sementes de desenvolvimento
- **WHEN** todas as sementes declaram `desenvolvimento`
- **THEN** `--conferir` reprova, nomeando a falta de semente de validação

#### Scenario: Autoteste do conjunto de validação vazio
- **WHEN** o autoteste troca, numa cópia, o papel de todas as sementes de validação para
  `desenvolvimento`
- **THEN** a conferência reprova pelo motivo esperado

### Requirement: Critério de elegibilidade tem justificativa

Todo critério da tabela de critérios de elegibilidade SHALL ter a coluna "Justificativa"
preenchida. Célula vazia, ou só com espaço ou traço, MUST reprovar `--conferir`, nomeando o
ID do critério.

#### Scenario: Critério sem justificativa

- **WHEN** a linha do CE6 tem a coluna "Justificativa" vazia
- **THEN** `--conferir` reprova, nomeando CE6

#### Scenario: Todos os critérios justificados

- **WHEN** todas as linhas da tabela de critérios têm justificativa
- **THEN** essa dimensão não reprova

#### Scenario: Justificativa reduzida a traço

- **WHEN** a justificativa de um critério é `-`
- **THEN** `--conferir` reprova, nomeando o critério

### Requirement: Autoteste prova a reprovação do critério sem justificativa

O autoteste SHALL esvaziar, numa cópia em memória, a justificativa de um critério e exigir
que `--conferir` reprove pelo motivo esperado, nomeando o critério.

#### Scenario: Defeito injetado

- **WHEN** o autoteste esvazia a justificativa de um critério na cópia
- **THEN** a conferência reprova nomeando aquele critério, e o caso conta como resultado
  esperado
