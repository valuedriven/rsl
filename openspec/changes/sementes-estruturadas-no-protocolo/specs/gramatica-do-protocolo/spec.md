# Spec Delta

## ADDED Requirements

### Requirement: Bloco estruturado como elemento da gramática
A gramática SHALL admitir um elemento de bloco cercado com linguagem declarada (`toml`) e
com esquema de campos (nome, tipo e exigência). `rsl gramatica` SHALL exibir o esquema do
bloco da seção "Conjunto-semente" com os campos, os tipos e a exigência de cada um.

#### Scenario: Esquema exibido
- **WHEN** se executa `rsl gramatica`
- **THEN** a seção "Conjunto-semente" aparece com o bloco `toml` e os campos `id`,
  `autores`, `ano`, `titulo`, `veiculo`, `volume`, `numero`, `paginas`, `doi`, `bases` e
  `papel`,
  cada um com tipo e exigência

#### Scenario: Campo novo no esquema
- **WHEN** uma change acrescenta um campo ao esquema do bloco
- **THEN** `rsl gramatica` o exibe, e o autoteste passa a gerar o caso de campo ausente,
  se ele for obrigatório
