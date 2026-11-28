# acesso-ao-zotero Specification

## Purpose

Dar ao projeto um acesso único ao Zotero, fonte das referências da revisão, por via local ou
web escolhida na configuração. Organizar nele as coleções da revisão, identificar cada
execução de busca de modo reprodutível e guardar fora do controle de versão o que se obtém
dele para leitura local.

## Requirements

### Requirement: Via de acesso ao Zotero configurável
Todo acesso ao Zotero SHALL usar a via de `[zotero] acesso`, `local` (o Zotero da máquina do
pesquisador) ou `web` (a API web), para ler e para escrever. Com as duas vias, os caminhos de
biblioteca e de coleção SHALL ser os mesmos de `[zotero]`. Valor fora de `local` e `web`
MUST reprovar a configuração com CONFIGURACAO, nomeando a chave.

#### Scenario: Via local
- **WHEN** `[zotero] acesso = "local"` e se executa `sementes copiar`
- **THEN** a coleção de `[zotero] colecao` é lida do Zotero da máquina, e nenhum pedido vai à
  API web

#### Scenario: Via web
- **WHEN** `[zotero] acesso = "web"` e se executa `sementes copiar`
- **THEN** a coleção é lida da API web, com a chave da API

#### Scenario: Valor fora do esquema
- **WHEN** `[zotero] acesso = "nuvem"`
- **THEN** a configuração reprova com CONFIGURACAO, nomeando `[zotero] acesso` e os valores
  aceitos

### Requirement: Chave da API só na via web
A chave da API web SHALL ser lida só quando a via é `web`. Com a via `local`, nenhum
subcomando SHALL ler a variável `ZOTERO_API_KEY`, a leitura MUST NOT ler variável nem o
`.env`, e a ausência da chave MUST NOT impedir a leitura.

#### Scenario: Via local sem chave
- **WHEN** `[zotero] acesso = "local"`, `ZOTERO_API_KEY` não está definida e não há `.env`
- **THEN** `sementes copiar` não sai com CONFIGURACAO por falta da chave

### Requirement: Credenciais da escrita pela via local
A escrita pela via `local` SHALL enviar a chave da API local (`ZOTERO_LOCAL_API_KEY`) e o
identificador do servidor (`ZOTERO_SERVER_ID`), lidos da variável de ambiente ou do `.env`,
com as guardas da chave web, só no primeiro pedido de escrita. A leitura MUST NOT enviá-los. A
falta de qualquer dos dois MUST fazer o subcomando sair com CONFIGURACAO, nomeando as
variáveis, antes de qualquer pedido de escrita. A chave local MUST NOT ser gravada nem
impressa.

#### Scenario: Escrita local com as credenciais
- **WHEN** `[zotero] acesso = "local"`, as duas variáveis estão no `.env` e se executa
  `sementes completar --gravar`
- **THEN** cada pedido de escrita leva `Zotero-API-Key` com a chave local e
  `Zotero-Server-ID`, e os pedidos de leitura não levam nenhum dos dois

#### Scenario: Escrita local sem as credenciais
- **WHEN** `[zotero] acesso = "local"`, falta `ZOTERO_LOCAL_API_KEY` e se executa
  `sementes completar --gravar`
- **THEN** o subcomando sai com CONFIGURACAO, nomeando as duas variáveis, e nenhum pedido de
  escrita é feito

### Requirement: Mesmas regras de acesso nas duas vias
Nas duas vias, o acesso SHALL fazer uma requisição por vez, sem nova tentativa. Erro de rede,
resposta fora do esperado, conflito de versão, limite de uso, pedido de espera ou falta de
permissão MUST interromper o subcomando com FONTE_EXTERNA, nomeando a via e o pedido.

#### Scenario: Zotero local fechado
- **WHEN** `[zotero] acesso = "local"` e o Zotero da máquina não responde
- **THEN** o subcomando sai com FONTE_EXTERNA, a mensagem nomeia a via local e diz que o
  Zotero tem de estar aberto com o acesso local habilitado, e nenhum pedido vai à API web

#### Scenario: Pedido de espera
- **WHEN** a resposta traz pedido de espera, em qualquer das vias
- **THEN** o subcomando para sem novo pedido e relata o que já foi feito

### Requirement: Mesma via em toda a sessão
A premissa SHALL ser manter a mesma via (`local` ou `web`) em toda a sessão de trabalho com o
Zotero. `sementes completar` MUST recusar com DADOS, antes de qualquer pedido ao Zotero, a
cópia lida por via diferente da de `[zotero] acesso`; a cópia sem a via registrada conta como
lida pela via `web`. `sementes copiar` SHALL avisar, no relato, quando a cópia anterior foi
lida por outra via.

#### Scenario: Completar com cópia de outra via
- **WHEN** `[zotero] acesso = "local"`, a cópia foi lida pela via `web` e se executa
  `sementes completar --gravar`
- **THEN** o subcomando sai com DADOS, nomeia as duas vias e indica manter a mesma via ou
  refazer a cópia, e nenhum pedido vai ao Zotero

#### Scenario: Troca de via na cópia
- **WHEN** a cópia anterior foi lida pela via `web` e se executa `sementes copiar` pela via
  `local`
- **THEN** o relato avisa que a versão não se compara entre vias e que a ordem das etiquetas
  pode diferir sem mudança de conteúdo

### Requirement: Escrita sem troca de via
A escrita no Zotero SHALL usar só a via configurada. Quando a via recusa a escrita, o
subcomando MUST sair com FONTE_EXTERNA, nomeando a via e a recusa, e MUST NOT repetir a escrita
pela outra via.

#### Scenario: Via local recusa escrita
- **WHEN** `[zotero] acesso = "local"`, se executa `sementes completar --gravar` e o Zotero da
  máquina recusa o pedido de escrita
- **THEN** o subcomando sai com FONTE_EXTERNA, nada é gravado pela API web, e a mensagem
  indica conferir as credenciais locais ou escrever com a via `web` na configuração

### Requirement: Coleções da revisão no Zotero
As referências da revisão SHALL ficar em duas coleções: a das sementes (`[zotero] colecao`)
e a das buscas. Dentro da das buscas, há uma subcoleção por base, nomeada pela sigla da base
no protocolo. Dentro de cada base, há uma coleção por execução, cujo nome começa pelo
identificador da execução.

#### Scenario: Coleção de uma execução
- **WHEN** uma execução da base com sigla `wos` tem o identificador `3f9a0c1d2e7b`
- **THEN** a coleção dela fica dentro da subcoleção `wos` da coleção das buscas, e o nome
  começa por `3f9a0c1d2e7b`

### Requirement: Biblioteca e coleção das buscas na configuração
A coleção das buscas SHALL ser a de nome `[zotero] search_collection`, na raiz da biblioteca
de `[zotero] library` ou, sem essa chave, na de `[zotero] biblioteca`. Toda biblioteca SHALL
valer na forma `groups/<id>`, `users/<id>` ou pelo endereço da biblioteca de grupo no site do
Zotero; outra forma MUST reprovar a configuração com CONFIGURACAO, nomeando a chave.

#### Scenario: Biblioteca das buscas pelo endereço do site
- **WHEN** `[zotero] library = "https://www.zotero.org/groups/6781444/modelagem-educacional"` e
  `[zotero] search_collection = "buscas"`
- **THEN** a coleção das buscas é a coleção `buscas` da raiz de `groups/6781444`

#### Scenario: Biblioteca das buscas omitida
- **WHEN** `[zotero] search_collection` está na configuração e `[zotero] library` não
- **THEN** a coleção das buscas é procurada na raiz da biblioteca de `[zotero] biblioteca`

#### Scenario: Nome da coleção das buscas ausente
- **WHEN** um subcomando precisa das coleções das buscas e `[zotero] search_collection` não está
  na configuração
- **THEN** o subcomando sai com CONFIGURACAO, nomeando a chave

#### Scenario: Biblioteca fora da forma
- **WHEN** `[zotero] library = "modelagem-educacional"`
- **THEN** a configuração reprova com CONFIGURACAO, nomeando `[zotero] library`

### Requirement: Coleção localizada pelo nome, sem escolha entre homônimas
A coleção de uma base ou de uma execução SHALL ser localizada pelo nome dentro da coleção-mãe.
Só um subcomando que escreve no Zotero SHALL criá-la quando não existe. Duas coleções-filhas
com o mesmo nome, ou com o mesmo identificador no início do nome, MUST fazer o subcomando sair
com DADOS, nomeando as duas, sem escolher uma.

#### Scenario: Subcoleção da base inexistente na leitura
- **WHEN** um subcomando só de leitura procura a subcoleção de uma base e ela não existe
- **THEN** o subcomando sai com DADOS, nomeando a base e a coleção das buscas, e nada é criado

#### Scenario: Homônimas
- **WHEN** a coleção das buscas tem duas subcoleções nomeadas `wos`, ou a raiz da biblioteca
  das buscas tem duas coleções com o nome de `[zotero] search_collection`
- **THEN** o subcomando sai com DADOS e nomeia as chaves das duas coleções

### Requirement: Identificador da execução calculado
O identificador de uma execução SHALL ser calculado, e não atribuído: são os 12 primeiros
caracteres hexadecimais do SHA-256 da sigla da base, do identificador da expressão, da data e
hora da execução e da lista ordenada das chaves dos registros exportados, com as repetições.
A chave de um registro é a da deduplicação: o DOI normalizado ou, sem DOI, o título
normalizado.

#### Scenario: Ordem dos registros indiferente
- **WHEN** a mesma exportação é lida com os registros em outra ordem
- **THEN** o identificador é o mesmo

#### Scenario: Um registro a mais
- **WHEN** duas exportações da mesma base, expressão e data e hora diferem em um registro
- **THEN** os identificadores diferem

#### Scenario: Mesma consulta em outro dia
- **WHEN** a mesma expressão é executada na mesma base em dois dias e devolve os mesmos
  registros
- **THEN** as duas execuções têm identificadores diferentes

### Requirement: Pasta de temporários fora do controle de versão
O que se obtém do Zotero para leitura local e as saídas regeneráveis SHALL ficar na pasta de
`[dados] temporarios`. A configuração MUST reprovar com CONFIGURACAO quando essa pasta, dentro
da raiz do projeto, não está listada no `.gitignore` da raiz, ou quando `[dados] execucoes`
aponta caminho fora dela. Pasta fora da raiz do projeto SHALL dispensar o `.gitignore`, porque
não entra no controle de versão.

#### Scenario: Pasta fora do projeto
- **WHEN** `[dados] temporarios` aponta uma pasta fora da raiz do projeto, `[dados] execucoes`
  fica dentro dela e o `.gitignore` não a lista
- **THEN** a configuração não reprova

#### Scenario: Pasta fora do .gitignore
- **WHEN** `[dados] temporarios = "tmp"` e o `.gitignore` não lista `tmp/`
- **THEN** a configuração reprova com CONFIGURACAO, nomeando a pasta e o `.gitignore`

#### Scenario: Cache das exportações em data/
- **WHEN** `[dados] execucoes = "data/execucoes"` e `[dados] temporarios = "tmp"`
- **THEN** a configuração reprova com CONFIGURACAO, nomeando `[dados] execucoes`

### Requirement: Exportação de uma execução obtida do Zotero
A exportação de uma execução que tem coleção no Zotero SHALL ser obtida dessa coleção, em RIS,
pela via configurada, e gravada no cache, em `[dados] execucoes`, por base, com o
identificador da execução no nome. O arquivo SHALL ser substituído só depois de gravado por
inteiro. Conteúdo que contenha a chave da API MUST NOT ser gravado.

#### Scenario: Exportação obtida
- **WHEN** se obtém a exportação da execução `3f9a0c1d2e7b` da base `wos`
- **THEN** o arquivo fica no cache, na pasta da base `wos`, com `3f9a0c1d2e7b` no nome, e é
  legível pelo leitor de RIS das análises

#### Scenario: Coleção sem itens
- **WHEN** a coleção da execução não tem itens, por estar vazia ou não existir mais
- **THEN** a obtenção sai com DADOS, e nada é gravado no cache

#### Scenario: Interrupção no meio
- **WHEN** a obtenção é interrompida antes do fim
- **THEN** o arquivo anterior do cache continua intacto, e não fica arquivo parcial com o nome
  final

### Requirement: Análises leem a exportação só do disco
Todo subcomando que lê exportações de execução SHALL obtê-las por um ponto único: o cache, para
a execução que tem coleção no Zotero, ou o arquivo registrado, para a que não tem. Os
subcomandos de análise e de conferência MUST NOT consultar o Zotero. Exportação ausente no
disco MUST fazer o subcomando sair com DADOS, nomeando a execução e o que a obtém.

#### Scenario: Cache ausente
- **WHEN** uma execução registrada tem coleção no Zotero e a exportação dela não está no cache
- **THEN** `busca derivar` sai com DADOS, nomeia a execução e indica a obtenção do Zotero, e
  nenhum pedido vai ao Zotero

#### Scenario: Execução registrada só com arquivo
- **WHEN** uma execução registrada não tem coleção no Zotero e declara o arquivo exportado
- **THEN** `busca derivar`, `conferencia sensibilidade` e `dados conferir` leem esse arquivo,
  como antes
