# gramatica-do-protocolo Specification

## Purpose

Tornar explícito, numa fonte única, o contrato de forma que o leitor exige do protocolo e
das fichas de busca, para que quem edita esses documentos saiba o que pode mudar sem
quebrar a leitura e o que não pode.

## Requirements

### Requirement: Fonte única da gramática
Todo literal de forma que o leitor exige SHALL ser declarado num único lugar do código:

- título de seção e o seu nível;
- cabeçalho e colunas exigidas de cada tabela;
- rótulo de linha (por exemplo, as camadas do quadro terminológico);
- marcador de lista (por exemplo, `- QGR:` e `- Execução:`);
- forma de identificador (`QERn`, `FCTn`, `STRn`, `EBn`, `CEn`, `BDn`, `SEn`);
- frase-padrão de onde se lê um parâmetro (por exemplo, "recuperação inferior a N%").

Os leitores MUST usar essas declarações e MUST NOT repetir o literal.

#### Scenario: Título repetido no leitor
- **WHEN** se procura, nos módulos de leitura, o título "Strings de busca por faceta" como
  literal
- **THEN** ele aparece só na declaração da gramática

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

### Requirement: Gramática descreve a forma, não o conteúdo
A gramática SHALL declarar só a forma: nomes de seção, colunas, rótulos, marcadores e
formas de identificador. Valores do projeto MUST NOT fazer parte dela; eles vêm do
protocolo ou do `config.toml`. São exemplos de valor: siglas de base, facetas existentes,
limiares, idiomas e composição.

#### Scenario: Sigla de base
- **WHEN** se procura `wos` ou `FCT1` nas declarações da gramática
- **THEN** não há ocorrência

### Requirement: Violação da gramática nomeia o elemento
A leitura que encontra o documento fora da gramática SHALL reprovar com o código
PROTOCOLO_ILEGIVEL. A mensagem MUST nomear o documento, a seção e o elemento do contrato
que faltou ou veio fora da forma, com o mesmo nome que `rsl gramatica` exibe.

#### Scenario: Coluna ausente
- **WHEN** a tabela de bases não tem a coluna `Sigla`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a tabela e a coluna como
  `rsl gramatica` as exibe

### Requirement: Autoteste cobre a gramática
O autoteste SHALL, para cada elemento exigido da gramática, retirar ou deformar esse
elemento numa cópia do documento e exigir a reprovação com PROTOCOLO_ILEGIVEL. Elemento
exigido sem caso de autoteste MUST fazer o autoteste falhar.

#### Scenario: Elemento sem caso
- **WHEN** a gramática ganha um elemento exigido e o autoteste não tem caso para ele
- **THEN** o autoteste falha, nomeando o elemento

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
- **WHEN** se procura nas declarações da gramática o caminho configurado em `[documentos]
  sementes`
- **THEN** não há ocorrência, porque o caminho vem do `config.toml`

#### Scenario: Esquema estruturado exibido
- **WHEN** se executa `rsl gramatica`
- **THEN** o grupo do arquivo de sementes traz os 19 campos do esquema estruturado, cada
  um com tipo e exigência, o `id` com a exigência de sequência a partir de SE1, e não
  traz `semente`
