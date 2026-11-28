# Spec Delta

## ADDED Requirements

### Requirement: Configuração dos registros da validação
`[dados] validacao` e `[dados] consulta_terminologica` SHALL constar do `config.toml` e
apontar, respectivamente, o arquivo de decisões e o resultado técnico da validação. A seção
`[planilha]` MUST reprovar com mensagem que nomeia as duas chaves novas.

#### Scenario: Chaves presentes
- **WHEN** a configuração do projeto é lida
- **THEN** `[dados] validacao` resolve o arquivo de decisões e
  `[dados] consulta_terminologica` resolve o resultado técnico

#### Scenario: Chave ausente
- **WHEN** o `config.toml` não traz `[dados] consulta_terminologica`
- **THEN** qualquer subcomando que lê a configuração termina com CONFIGURACAO, nomeando a
  chave

#### Scenario: Seção retirada
- **WHEN** o `config.toml` traz a seção `[planilha]`
- **THEN** qualquer subcomando que lê a configuração termina com CONFIGURACAO, e a mensagem
  nomeia `[dados] validacao` e `[dados] consulta_terminologica`

#### Scenario: Caminho alterado
- **WHEN** o pesquisador muda `[dados] validacao`
- **THEN** `termos exportar` grava no caminho novo, e o caminho antigo não é lido

## MODIFIED Requirements

### Requirement: Convenção de nomes
Os subcomandos SHALL ser `grupo ação` quando houver grupo natural, com a ação no infinitivo,
em português e sem acento; o topo pode ser verbo quando não houver grupo. O grupo SHALL
nomear o artefato ou domínio (`documentos`, `dados`, `projeto`, `configuracao`, `termos`,
`strings`, `catalogo`, `aderencia`, `busca`, `conferencia`). Os arquivos que os subcomandos
gravam SHALL seguir estas regras:

- `snake_case`, em português e sem acento;
- o nome é o substantivo do conteúdo;
- quando há um arquivo por chave (expressão, base), o sufixo é a chave em minúsculas, e
  com duas chaves, a base antes da expressão (`fidelidade_wos_eb2.csv`,
  `sensibilidade_wos.csv`).

O nome de cada arquivo de entrada e de saída SHALL vir do `config.toml`.

#### Scenario: Saída por expressão
- **WHEN** `conferencia fidelidade wos EB2` confere a EB2 na WoS
- **THEN** a saída gravada se chama `fidelidade_wos_eb2.csv`

#### Scenario: Planilha de validação
- **WHEN** a configuração é a do projeto
- **THEN** o arquivo de decisões se chama `validacao_terminologica.toml` e o resultado
  técnico se chama `consulta_terminologica.json`

#### Scenario: Ação nominal recusada
- **WHEN** se tenta registrar um comando cuja ação é substantivo, como a sonda do grupo
  `termos`
- **THEN** o nome canônico é `termos sondar`, e o substantivo não é aceito como comando
