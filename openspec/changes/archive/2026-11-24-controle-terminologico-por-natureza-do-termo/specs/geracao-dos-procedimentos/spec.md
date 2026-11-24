## MODIFIED Requirements

### Requirement: Composição dos blocos a partir da STR
O bloco de string de cada faceta SHALL conter os termos da STR nos idiomas que
`[cobertura]` declara, menos a redução, sem filtro por linha do controle terminológico.
Somam-se a eles as formas de número da flexão (`flexao-dos-termos`), na ordem da STR, cada
uma logo depois do seu termo. Termo repetido entra uma vez. O campo, a forma do campo e as
aspas SHALL ser os de `[composicao]`.

#### Scenario: Termo novo na STR
- **WHEN** a STR2 ganha `plataforma educacional`, sem exceção, e a fonte da Scopus declara
  FCT2 em pt com plural explícito
- **THEN** o ensaio de `procedimentos gerar scopus` lista, em STR2 e em cada expressão com
  FCT2, `"plataforma educacional"` e `"plataformas educacionais"` a acrescentar

#### Scenario: Termo reduzido
- **WHEN** a fonte da ERIC declara `massive open online course` em `[[reducao]]` de FCT2
- **THEN** nenhum bloco da ERIC o contém

#### Scenario: Prefixo por termo e aspas só na locução
- **WHEN** a fonte da ERIC declara FCT3 com campo `abstract`, `forma = "prefixa"` e
  `aspas = "locucao"`
- **THEN** o bloco de STR3 traz `abstract:pedagogy` e `abstract:"teaching strategy"`

#### Scenario: Procedimento gerado sem camadas
- **WHEN** se executa `procedimentos gerar wos`
- **THEN** a tabela de cobertura do procedimento gerado não traz a linha `camadas`
