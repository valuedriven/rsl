## ADDED Requirements

### Requirement: Fidelidade por base
`conferencia fidelidade` SHALL receber a base e SHALL derivar o conjunto só das exportações
da executada dessa base, com o vocabulário dela. A execução direta SHALL ser o arquivo
dado ou, sem ele, as exportações registradas da expressão na base. Base sem a executada
registrada, ou sem execução direta registrada quando não se dá arquivo, MUST sair com
DADOS e nomear o registro que falta. A executada e a sonda MUST ser recusadas com USO.

#### Scenario: Corpus de outra base
- **WHEN** a WoS e a Scopus têm a EB4 registrada, e um registro só da EB4 da Scopus
  satisfaz a EB2
- **THEN** `conferencia fidelidade wos EB2` não o conta no conjunto derivado

#### Scenario: Execução direta registrada
- **WHEN** a EB2 da WoS está registrada e se executa `conferencia fidelidade wos EB2`
- **THEN** a execução direta são as exportações registradas da EB2 na WoS

#### Scenario: Sem execução direta
- **WHEN** a base não tem a EB2 registrada e não se dá arquivo
- **THEN** o subcomando sai com DADOS e mostra o `busca registrar` que falta

### Requirement: Casamento local respeita a fronteira entre trechos
O casamento local SHALL procurar cada termo no título, no resumo e em cada palavra-chave,
separadamente. Um termo MUST NOT casar juntando o fim de um trecho com o começo de outro.
O separador entre valores de um campo SHALL ser o mesmo que os leitores das exportações
usam ao unir esses valores.

#### Scenario: Duas palavras-chave
- **WHEN** um registro tem as palavras-chave `learning` e `context awareness`, e nenhum
  outro trecho traz `learning context`
- **THEN** o casamento local não reconhece o termo `learning context`

#### Scenario: Título e resumo
- **WHEN** o título termina com a primeira palavra de um termo e o resumo começa com a
  segunda
- **THEN** o casamento local não reconhece o termo

#### Scenario: Termo inteiro numa palavra-chave
- **WHEN** uma das palavras-chave é o termo inteiro
- **THEN** o casamento local reconhece a faceta

### Requirement: Autoteste prova a fidelidade por base e a fronteira
O autoteste SHALL provar, com registros sintéticos e termos lidos do vocabulário das bases,
que a fidelidade de uma base não conta o registro da executada de outra base, que sem
arquivo ela lê a execução direta registrada, e que um termo partido entre palavras-chave
ou entre título e resumo não é reconhecido.

#### Scenario: Mistura de bases reintroduzida
- **WHEN** o conjunto derivado volta a ler todas as bases
- **THEN** o caso de fidelidade por base falha

#### Scenario: Texto único reintroduzido
- **WHEN** o casamento volta a procurar os termos no texto unido
- **THEN** os casos de fronteira falham

## MODIFIED Requirements

### Requirement: Corpus da derivação é a executada
`busca derivar`, o conjunto derivado de `conferencia fidelidade` e `aderencia medir` SHALL
ler só as execuções registradas da expressão executada. As execuções da sonda e das
expressões de conferência MUST NOT entrar nos registros, nas contagens, na ordem de
triagem nem na aderência. `conferencia sensibilidade` SHALL continuar lendo a executada e
a sonda.

#### Scenario: Registro só da sonda
- **WHEN** a base tem EB4 e EB5 registradas, e um registro está só na exportação da EB5
- **THEN** esse registro não aparece em `registros.csv` nem em `ordem_triagem.csv`, e a
  contagem da executada em `contagens_busca.csv` é igual ao número de registros únicos da
  EB4

#### Scenario: Semente só na sonda
- **WHEN** uma semente aparece só na exportação da EB5
- **THEN** `aderencia medir` não a conta como recuperada

#### Scenario: Execução direta da expressão de conferência
- **WHEN** a EB2 está registrada com exportação própria
- **THEN** `busca derivar` não lê essa exportação, e as contagens brutas não a somam;
  `conferencia fidelidade <base> EB2 <arquivo>` lê o arquivo como execução direta e compara
  com o conjunto derivado da EB4 da mesma base

#### Scenario: Sensibilidade inalterada
- **WHEN** a base tem EB4 e EB5 registradas
- **THEN** `conferencia sensibilidade` mede a perda da EB5 para a EB4 como antes
