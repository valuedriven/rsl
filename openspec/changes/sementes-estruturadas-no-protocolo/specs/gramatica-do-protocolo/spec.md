# Spec Delta

## ADDED Requirements

### Requirement: Arquivo estruturado apontado pelo protocolo
A gramática SHALL admitir um elemento de apontamento de arquivo: uma linha com rótulo
declarado, seguida de um caminho relativo à raiz do projeto, e o esquema de campos
(nome, tipo e exigência) do arquivo apontado. A seção "Conjunto-semente" SHALL exigir
exatamente um apontamento, para um arquivo TOML. `rsl gramatica` SHALL exibir o rótulo e o
esquema do arquivo, com os campos, os tipos e a exigência de cada um.

#### Scenario: Esquema exibido
- **WHEN** se executa `rsl gramatica`
- **THEN** a seção "Conjunto-semente" aparece com o rótulo do apontamento e os campos
  `id`, `autores`, `ano`, `titulo`, `veiculo`, `volume`, `numero`, `paginas`, `doi`,
  `bases`, `facetas`, `papel`, `verificacao`, `tipo`, `alinhamento`, `nota`,
  `veiculo_conferido`, `eric` e `observacoes`, cada um com tipo e exigência

#### Scenario: Campo novo no esquema
- **WHEN** uma change acrescenta um campo ao esquema do arquivo
- **THEN** `rsl gramatica` o exibe, e o autoteste passa a gerar o caso de campo ausente,
  se ele for obrigatório

#### Scenario: Apontamento ausente
- **WHEN** a seção "Conjunto-semente" não traz a linha de apontamento
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a seção e o rótulo esperado
