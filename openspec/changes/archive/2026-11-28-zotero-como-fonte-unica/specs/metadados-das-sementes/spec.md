# Spec Delta

## MODIFIED Requirements

### Requirement: Cópia da coleção do Zotero
`sementes copiar` SHALL ler, pela via de acesso de `[zotero] acesso`, os itens de topo da
coleção configurada em `[zotero]` e gravar a resposta bruta no arquivo de `[dados] zotero`,
com a biblioteca, a coleção, a versão da biblioteca, a via usada e a data e hora da leitura.
Antes de gravar, o comando SHALL relatar os itens acrescentados, os retirados e os campos
alterados em relação à cópia anterior.

#### Scenario: Primeira cópia
- **WHEN** se executa `sementes copiar` sem cópia anterior
- **THEN** a resposta bruta da coleção fica gravada em `[dados] zotero`, com a data e hora da leitura, e o relato lista todos os itens como acrescentados

#### Scenario: Item alterado no Zotero
- **WHEN** o título de um item mudou no Zotero desde a cópia anterior
- **THEN** o relato nomeia o DOI do item, o campo `titulo` e os dois valores antes de gravar a nova cópia

#### Scenario: Cópia pela via local
- **WHEN** `[zotero] acesso = "local"` e se executa `sementes copiar`
- **THEN** a cópia gravada registra a via `local`, e a diferença para uma cópia anterior lida
  pela via `web` se relata pelos mesmos campos

### Requirement: Chave da API web fora do projeto
Quando a via de acesso é `web`, o acesso à API web do Zotero SHALL usar a chave da variável
de ambiente `ZOTERO_API_KEY` ou, na falta dela, a da linha `ZOTERO_API_KEY=` do `.env` da raiz
do projeto. O `.env` MUST ser recusado com CONFIGURACAO quando o `.gitignore` não o listar. A
chave MUST NOT ser gravada em arquivo versionado nem impressa; em relato, só os quatro
últimos caracteres podem aparecer.

#### Scenario: Chave no .env
- **WHEN** `ZOTERO_API_KEY` não está definida e o `.env` listado no `.gitignore` traz a linha
  da chave
- **THEN** `sementes copiar` usa a chave do `.env`

#### Scenario: .env fora do .gitignore
- **WHEN** o `.env` traz a chave e o `.gitignore` não o lista
- **THEN** `sementes copiar` sai com CONFIGURACAO, nomeando o `.gitignore`, sem imprimir a chave

#### Scenario: Variável ausente
- **WHEN** `[zotero] acesso = "web"` e se executa `sementes copiar` sem `ZOTERO_API_KEY`
  definida e sem `.env`
- **THEN** a saída tem o código CONFIGURACAO, e nenhum outro subcomando deixa de funcionar por isso

#### Scenario: Chave não impressa
- **WHEN** qualquer subcomando que acessa o Zotero termina, com sucesso ou com erro
- **THEN** a saída e os arquivos gravados não contêm a chave inteira
