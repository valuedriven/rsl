## MODIFIED Requirements

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
