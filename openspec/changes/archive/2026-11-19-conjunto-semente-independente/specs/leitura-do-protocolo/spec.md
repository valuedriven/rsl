# Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

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
