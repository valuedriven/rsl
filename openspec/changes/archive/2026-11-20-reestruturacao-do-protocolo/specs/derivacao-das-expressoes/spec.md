# Spec Delta

## MODIFIED Requirements

### Requirement: Expressões deriváveis vêm dos papéis
As expressões deriváveis SHALL ser todas as da composição exceto a executada e a sonda
identificadas pelo leitor a partir da composição e das âncoras.

#### Scenario: Papéis lidos
- **WHEN** a composição identifica EB4 como executada e EB5 como sonda
- **THEN** as deriváveis são as demais expressões da composição

### Requirement: Arquivos de entrada e de saída lidos da configuração
A derivação, a aderência, a fidelidade, a sensibilidade e o instrumento de aderência
SHALL obter do `config.toml` o caminho de cada arquivo que leem ou gravam. Isso inclui
`registro_execucao.json`, `sementes.json`, o arquivo de sementes (`[documentos] sementes`),
`semente_aderencia.csv` e as saídas na raiz de `data/`.

#### Scenario: Registro em outro caminho
- **WHEN** o `config.toml` aponta o registro de execução para outro caminho
- **THEN** `busca registrar`, `busca derivar` e `conferir-dados` leem e gravam esse
  caminho, e as mensagens o nomeiam

#### Scenario: Arquivo de sementes em outro caminho
- **WHEN** `[documentos] sementes` aponta outro arquivo
- **THEN** `sementes planilha` e `busca aderencia` leem as sementes desse arquivo

### Requirement: Planilha de aderência traz o papel

A planilha gerada pelo instrumento de aderência SHALL ter, em cada linha, o papel da
semente lido do arquivo de sementes.

#### Scenario: Coluna de papel
- **WHEN** `sementes planilha` gera a planilha
- **THEN** cada linha traz a coluna `papel` com `desenvolvimento` ou `validação`, igual ao
  campo `papel` da semente no arquivo de sementes
