## ADDED Requirements

### Requirement: Casamento local pelos termos da base
O casamento local de cada faceta SHALL usar, por base, os termos da string composta para
a base: as formas de número geradas por regra e por exceção, e o radical truncado onde a
fonte o declara. A esses termos SHALL somar as formas de número de cada um, mesmo quando a
base declara plural `pela lematização`. O casamento MUST NOT acrescentar sufixo de plural
por aproximação. O `*` casa qualquer continuação da palavra.

#### Scenario: Plural irregular gerado para a base
- **WHEN** a STR da faceta traz `"learning activity"`, a string da base traz também
  `"learning activities"` e um registro da executada tem `learning activities` no resumo
- **THEN** o casamento local reconhece a faceta nesse registro

#### Scenario: Base que lematiza
- **WHEN** a base declara plural `pela lematização` em inglês, a string dela não traz
  `"learning activities"` e um registro tem `learning activities` no título
- **THEN** o casamento local reconhece a faceta nesse registro, pela forma de número de
  `learning activity`

#### Scenario: Sem sufixo aproximado
- **WHEN** o termo é `"conceptual model"`, nem a string da base nem as formas de número
  trazem `conceptual modeles`, e um registro traz só `conceptual modeles`
- **THEN** o casamento local não reconhece a faceta nesse registro

#### Scenario: Termos de outra base
- **WHEN** duas bases recebem strings diferentes da mesma faceta
- **THEN** os registros de cada base se casam com os termos da sua própria base

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
  `conferencia fidelidade EB2 <arquivo>` lê o arquivo como execução direta e compara com o
  conjunto derivado da EB4

#### Scenario: Sensibilidade inalterada
- **WHEN** a base tem EB4 e EB5 registradas
- **THEN** `conferencia sensibilidade` mede a perda da EB5 para a EB4 como antes

### Requirement: Relato das execuções lidas
`busca derivar`, `conferencia fidelidade` e `aderencia medir` SHALL relatar, antes do
resultado, as execuções lidas e as registradas que deixaram de fora, cada uma com a
expressão e o motivo.

#### Scenario: Execuções deixadas de fora
- **WHEN** a base tem EB2, EB3, EB4 e EB5 registradas e se executa `busca derivar`
- **THEN** o relato lista a EB4 como lida, e a EB2, a EB3 e a EB5 como deixadas de fora,
  a EB5 como sonda e as outras como execução direta de conferência

### Requirement: Autoteste prova o casamento e o corpus
O autoteste SHALL provar, com registros sintéticos e termos lidos da composição, que o
casamento local reconhece um plural que o sufixo `s`/`es` não alcança, e que um registro só
da sonda fica fora das contagens, da ordem de triagem e da aderência.

#### Scenario: Volta do sufixo aproximado
- **WHEN** o casamento local volta a usar os termos do protocolo com sufixo `s`/`es`
- **THEN** o autoteste falha no caso do plural irregular

#### Scenario: Sonda de volta ao corpus
- **WHEN** a derivação volta a ler todas as execuções registradas
- **THEN** o autoteste falha no caso do registro só da sonda

## MODIFIED Requirements

### Requirement: Saídas preservadas
Para o protocolo e a configuração atuais, o **conteúdo** das saídas da derivação, da
aderência, da fidelidade e da sensibilidade MUST ser idêntico ao anterior à mudança.
Ficam fora dessa exigência só estas exceções:

- a redação da coluna `facetas_exigidas` de `contagens_busca.csv`, que passa à forma
  estrita (`FCT1 AND FCT2 AND (FCT3 OR FCT4)`) por decisão do pesquisador;
- a grafia das siglas das bases, que passa a ser a do protocolo (`wos`, `scopus`, `eric`,
  `brapci`);
- na aderência, o relato separado por papel da semente, com o intervalo de confiança, a
  coluna `papel` da planilha de aderência e o casamento por prefixo, que deixa de entrar no
  numerador e passa a ser relatado como indício;
- o **nome** dos arquivos de saída, que segue a convenção de nomes da interface de comando
  e vem do `config.toml` (`fidelidade_EB<n>.csv` passa a `fidelidade_eb<n>.csv`);
- as facetas reconhecidas pelo casamento local, que passam a vir dos termos da base, e o
  que delas depende (colunas `facetas` e `expressoes` de `registros.csv`, contagens
  derivadas, ordem de triagem, conjunto derivado da fidelidade);
- os registros lidos pela derivação, pela fidelidade e pela aderência, que passam a ser só
  os da executada, e as contagens, a ordem de triagem e a aderência que deles dependem.

#### Scenario: Mesmo resultado
- **WHEN** a prova da composição, as deriváveis e o mapa de bases são calculados antes e
  depois da mudança
- **THEN** os valores coincidem, comparadas as siglas sem distinção de caixa

#### Scenario: Aderência preservada nos casamentos exatos
- **WHEN** a aderência é calculada antes e depois da separação por papel, com os mesmos
  registros
- **THEN** o total de sementes recuperadas por casamento exato coincide, e só a decomposição
  por papel, o intervalo e a coluna `papel` são novos; o casamento por prefixo deixa de ser
  contado e passa a indício

#### Scenario: Mesmo conteúdo com outro nome
- **WHEN** a derivação, a fidelidade e a sensibilidade rodam antes e depois da mudança sobre
  as mesmas exportações sintéticas
- **THEN** cada arquivo de saída tem conteúdo idêntico byte a byte ao correspondente
  anterior, que pode ter outro nome

#### Scenario: Sensibilidade preservada
- **WHEN** a sensibilidade roda antes e depois do casamento pelos termos da base e da
  restrição do corpus, sobre as mesmas exportações
- **THEN** `sensibilidade_<base>.csv` tem conteúdo idêntico byte a byte
