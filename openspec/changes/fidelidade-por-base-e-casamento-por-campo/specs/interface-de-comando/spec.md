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
- **THEN** a planilha de validação se chama `validacao_terminologica.csv`

#### Scenario: Ação nominal recusada
- **WHEN** se tenta registrar um comando cuja ação é substantivo, como a sonda do grupo
  `termos`
- **THEN** o nome canônico é `termos sondar`, e o substantivo não é aceito como comando
