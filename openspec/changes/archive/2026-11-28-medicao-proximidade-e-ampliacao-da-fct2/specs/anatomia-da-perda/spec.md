## MODIFIED Requirements

### Requirement: Nível lido da execução registrada
O nível cuja expressão tem execução válida registrada na base, com o texto registrado igual
ao texto vigente da expressão, SHALL ser lido da exportação registrada, filtrada pelos DOIs,
e não ser pedido ao pesquisador. A execução sem texto registrado, ou com texto diferente do
vigente, MUST NOT ser lida: o nível vai ao roteiro, com o motivo. O relato SHALL dizer, por
nível, se ele é submetido ou lido de execução registrada, com a execução.

#### Scenario: Sonda e executada registradas
- **WHEN** a Scopus tem EB4 e EB5 registradas, com o texto vigente de cada uma
- **THEN** os níveis 4 e 5 são lidos de BD2/EX4 e BD2/EX1, e o pesquisador submete só os
  níveis 1 a 3

#### Scenario: Strings alteradas depois da execução
- **WHEN** a WoS tem EB5 registrada com o texto anterior à mudança da STR2
- **THEN** o nível 4 não é lido de BD1/EX4: o roteiro o pede, dizendo que a execução foi
  registrada com texto diferente do vigente

#### Scenario: Execução sem texto registrado
- **WHEN** a Scopus tem EB4 registrada sem o campo `texto`
- **THEN** o nível 5 não é lido de BD2/EX1: o roteiro o pede, dizendo que a igualdade ao
  texto vigente não se confere
