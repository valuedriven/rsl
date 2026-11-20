# Spec Delta

## MODIFIED Requirements

### Requirement: Contrato exibido a partir do leitor
`python3 -m rsl gramatica` SHALL exibir o contrato completo a partir dessas declarações. O
contrato vem agrupado por documento (protocolo, ficha de base e arquivo de sementes) e,
para cada elemento, mostra o que é exigido, o que é opcional e o que reprova.

O contrato MUST NOT ser mantido à mão num segundo arquivo: documentação que o cite remete
ao subcomando.

#### Scenario: Elemento novo na gramática
- **WHEN** uma change acrescenta à gramática a exigência de uma coluna
- **THEN** `rsl gramatica` passa a exibi-la, sem edição de outro arquivo

#### Scenario: Conteúdo do contrato
- **WHEN** se executa `rsl gramatica`
- **THEN** a saída lista, entre outros, a seção "Conjunto-semente", as colunas exigidas da
  tabela de bases e as formas de identificador, cada uma com o seu nível de exigência

#### Scenario: Arquivo de sementes no contrato
- **WHEN** se executa `rsl gramatica`
- **THEN** a saída traz o grupo do arquivo de sementes, com a tabela `[[sementes]]` e os
  campos `id`, `semente`, `bases` e `papel`, cada um com tipo e exigência

## ADDED Requirements

### Requirement: Esquema do arquivo de sementes na gramática
A gramática SHALL declarar o esquema do arquivo de sementes: o nome da tabela e, para cada
campo, o nome, o tipo e a exigência. O leitor MUST usar essa declaração para aceitar ou
reprovar o arquivo, e o autoteste MUST gerar a partir dela os casos de campo ausente e de
campo desconhecido.

#### Scenario: Campo novo no esquema
- **WHEN** uma change acrescenta um campo obrigatório ao esquema
- **THEN** `rsl gramatica` o exibe, e o autoteste passa a gerar o caso de campo ausente

#### Scenario: Caminho fora da gramática
- **WHEN** se procura `docs/conjunto_semente.toml` nas declarações da gramática
- **THEN** não há ocorrência, porque o caminho vem do `config.toml`
