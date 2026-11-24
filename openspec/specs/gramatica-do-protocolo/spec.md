# gramatica-do-protocolo Specification

## Purpose

Tornar explícito, numa fonte única, o contrato de forma que o leitor exige do protocolo e
dos procedimentos de busca, para que quem edita esses documentos saiba o que pode mudar sem
quebrar a leitura e o que não pode.

## Requirements

### Requirement: Fonte única da gramática
Todo literal de forma que o leitor exige SHALL ser declarado num único lugar do código:

- título de seção e o seu nível;
- cabeçalho e colunas exigidas de cada tabela;
- rótulo de linha (por exemplo, as linhas do controle terminológico);
- marcador de lista (por exemplo, `- QGR:` e `- Execução:`);
- forma de identificador (`QERn`, `FCTn`, `CTn`, `STRn`, `EBn`, `CEn`, `BDn`, `SEn`);
- frase-padrão de onde se lê um parâmetro (por exemplo, "recuperação inferior a N%").

Os leitores MUST usar essas declarações e MUST NOT repetir o literal.

#### Scenario: Título repetido no leitor
- **WHEN** se procura, nos módulos de leitura, o título "Strings de busca por faceta" como
  literal
- **THEN** ele aparece só na declaração da gramática

#### Scenario: Título do controle terminológico no contrato
- **WHEN** se executa `rsl documentos gramatica`
- **THEN** a saída traz a forma `### CTn (FCTn)`, o cabeçalho `| Termo | <idioma> | … |` e
  os três rótulos de linha do controle terminológico, cada um com o nome interno, e não traz
  o campo `camadas` da cobertura

### Requirement: Contrato exibido a partir do leitor
`python3 -m rsl documentos gramatica` SHALL exibir o contrato completo a partir dessas
declarações. O contrato vem agrupado por documento:
- protocolo;
- fonte do procedimento de busca;
- arquivo de sementes;
- arquivo de exceções de flexão;
- resultado de sondagem no registro de execução.

Para cada elemento, o contrato mostra o que é exigido, o que é opcional e o que reprova. O
grupo da fonte do procedimento SHALL trazer as tabelas e campos de `procedimento.toml`, com
tipo, exigência e domínio, e os fragmentos admitidos, com a forma exigida de cada um. O
procedimento gerado MUST NOT ter grupo próprio, porque é saída.

O contrato MUST NOT ser mantido à mão num segundo arquivo: documentação que o cite remete
ao subcomando.

#### Scenario: Elemento novo na gramática
- **WHEN** uma change acrescenta à gramática a exigência de uma coluna
- **THEN** `rsl documentos gramatica` passa a exibi-la, sem edição de outro arquivo

#### Scenario: Conteúdo do contrato
- **WHEN** se executa `rsl documentos gramatica`
- **THEN** a saída lista, entre outros, a seção "Conjunto-semente", as colunas exigidas da
  tabela de bases e as formas de identificador, cada uma com o seu nível de exigência

#### Scenario: Arquivo de sementes no contrato
- **WHEN** se executa `rsl documentos gramatica`
- **THEN** a saída traz o grupo do arquivo de sementes, com a tabela `[[sementes]]` e os
  campos `id`, `bases` e `papel`, cada um com tipo e exigência

#### Scenario: Fonte do procedimento no contrato
- **WHEN** se executa `rsl documentos gramatica`
- **THEN** a saída traz o grupo da fonte do procedimento. Nele estão `[[sintaxe]]`, com
  `situacao` e os seus cinco valores, `[[sondagens]]`, com as leituras e a exigência da
  leitura inconclusiva, e a lista dos fragmentos admitidos

#### Scenario: Procedimento gerado fora do contrato
- **WHEN** se executa `rsl documentos gramatica`
- **THEN** não há grupo de forma do markdown do procedimento de busca, e a saída diz que ele
  é gerado por `procedimentos gerar`

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
que faltou ou veio fora da forma, com o mesmo nome que `rsl documentos gramatica` exibe.

#### Scenario: Coluna ausente
- **WHEN** a tabela de bases não tem a coluna `Sigla`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a tabela e a coluna como
  `rsl documentos gramatica` as exibe

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
- **THEN** `rsl documentos gramatica` o exibe, e o autoteste passa a gerar o caso de campo ausente

#### Scenario: Caminho fora da gramática
- **WHEN** se procura nas declarações da gramática o caminho configurado em `[documentos]
  sementes`
- **THEN** não há ocorrência, porque o caminho vem do `config.toml`

#### Scenario: Esquema estruturado exibido
- **WHEN** se executa `rsl documentos gramatica`
- **THEN** o grupo do arquivo de sementes traz os 19 campos do esquema estruturado, cada
  um com tipo e exigência, o `id` com a exigência de sequência a partir de SE1, e não
  traz `semente`

### Requirement: Esquema da fonte do procedimento na gramática
A gramática SHALL declarar a forma da fonte do procedimento (esquema de `procedimento.toml`,
fragmentos admitidos e categorias mínimas), o esqueleto e o texto fixo do procedimento
gerado, o esquema do arquivo de exceções de flexão e o do resultado de sondagem. O leitor e o
gerador MUST usar essas declarações, sem repetir o literal. O autoteste MUST gerar delas os
casos de campo ausente, campo desconhecido e valor fora do domínio.

#### Scenario: Campo novo na fonte
- **WHEN** uma change acrescenta um campo obrigatório a `[[sondagens]]`
- **THEN** `rsl documentos gramatica` o exibe, e o autoteste passa a gerar o caso de campo
  ausente
