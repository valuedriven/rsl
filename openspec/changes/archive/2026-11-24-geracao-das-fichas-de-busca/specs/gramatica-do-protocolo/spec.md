# Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

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
