# Spec Delta

## MODIFIED Requirements

### Requirement: Esquema do arquivo de sementes na gramática
A gramática SHALL declarar o esquema do arquivo de sementes: o nome da tabela e, para cada
campo, o nome, o tipo e a exigência. O leitor MUST usar essa declaração para aceitar ou
reprovar o arquivo, e o autoteste MUST gerar a partir dela os casos de campo ausente e de
campo desconhecido. Os campos declarados SHALL ser os do esquema estruturado: `id`,
`autores`, `ano`, `titulo`, `veiculo`, `volume`, `numero`, `paginas`, `doi`, `bases`,
`facetas`, `papel`, `verificacao`, `tipo`, `alinhamento`, `nota`, `veiculo_conferido`,
`eric` e `observacoes`.

#### Scenario: Campo novo no esquema
- **WHEN** uma change acrescenta um campo obrigatório ao esquema
- **THEN** `rsl gramatica` o exibe, e o autoteste passa a gerar o caso de campo ausente

#### Scenario: Caminho fora da gramática
- **WHEN** se procura `docs/sementes.toml` nas declarações da gramática
- **THEN** não há ocorrência, porque o caminho vem do `config.toml`

#### Scenario: Esquema estruturado exibido
- **WHEN** se executa `rsl gramatica`
- **THEN** o grupo do arquivo de sementes traz os 19 campos do esquema estruturado, cada
  um com tipo e exigência, e não traz `semente`
