# derivacao-das-expressoes Specification

## Purpose

Derivar localmente as expressões não executadas e montar o instrumento de aderência a
partir do que o protocolo e a configuração declaram, sem composição, papéis nem bases
fixados no código.

## Requirements

### Requirement: Prova da composição pelas relações do protocolo
A prova da composição da derivação SHALL verificar, sobre todas as combinações de facetas,
as relações lidas do protocolo: a executada é a união das específicas, a sonda contém toda
expressão, e a expressão geral está contida em cada específica. Os identificadores das
expressões MUST NOT ser fixados no código.

#### Scenario: Protocolo atual
- **WHEN** a derivação roda com a composição atual do protocolo
- **THEN** a prova não reporta problema e as expressões derivadas são as que não são
  executada nem sonda

#### Scenario: Executada que não é a união das específicas
- **WHEN** a composição lida tem a executada diferente da união das específicas
- **THEN** a prova reporta a combinação de facetas em que a relação falha

### Requirement: Expressões deriváveis vêm dos papéis
As expressões deriváveis SHALL ser todas as da composição exceto a executada e a sonda
identificadas pelo leitor a partir da composição e das âncoras.

#### Scenario: Papéis lidos
- **WHEN** a composição identifica EB4 como executada e EB5 como sonda
- **THEN** as deriváveis são as demais expressões da composição

### Requirement: Bases vêm do protocolo
As bases usadas na derivação e no instrumento de aderência — sigla e identificador `BDn` —
SHALL vir da tabela "Bases de dados" do protocolo, e o procedimento de busca, da sigla; o código MUST NOT
fixar lista nem mapa de bases. A base é escolhida na linha de comando pela sigla ou pelo
identificador.

#### Scenario: Sigla de uma base
- **WHEN** a tabela declara `BD3` com sigla `eric`
- **THEN** a derivação e o instrumento de aderência usam `eric` para a base, e
  `--base eric` e `--base BD3` selecionam a mesma base

#### Scenario: Base desconhecida na linha de comando
- **WHEN** se pede uma base que não é sigla nem identificador da tabela
- **THEN** o script termina com erro que lista as siglas e os identificadores lidos

### Requirement: Facetas do instrumento de aderência vêm do protocolo
As facetas usadas por `gen_semente.py` SHALL vir das facetas lidas do protocolo, na ordem
declarada; o código MUST NOT fixar a lista de facetas.

#### Scenario: Facetas lidas
- **WHEN** o protocolo declara FCT1 a FCT4
- **THEN** o instrumento usa FCT1 a FCT4, nessa ordem

### Requirement: Saídas preservadas
Para o protocolo e a configuração atuais, o **conteúdo** das saídas da derivação, da
aderência, da fidelidade e da sensibilidade MUST ser idêntico ao anterior à mudança.
Ficam fora dessa exigência só estas exceções:

- a redação da coluna `facetas_exigidas` de `contagens_busca.csv`, que passa à forma
  estrita (`FCT1 AND FCT2 AND (FCT3 OR FCT4)`) por decisão do pesquisador;
- a grafia das siglas das bases, que passa a ser a do protocolo (`wos`, `scopus`, `eric`,
  `brapci`);
- na aderência, o relato único com o intervalo de confiança e o casamento por prefixo, que
  deixa de entrar no numerador e passa a ser relatado como indício;
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
- **WHEN** a aderência é calculada antes e depois da mudança, com os mesmos registros
- **THEN** o total de sementes recuperadas por casamento exato coincide, e o relato único, o
  intervalo e o indício por prefixo são a forma atual

#### Scenario: Mesmo conteúdo com outro nome
- **WHEN** a derivação, a fidelidade e a sensibilidade rodam antes e depois da mudança sobre
  as mesmas exportações sintéticas
- **THEN** cada arquivo de saída tem conteúdo idêntico byte a byte ao correspondente
  anterior, que pode ter outro nome

#### Scenario: Sensibilidade preservada
- **WHEN** a sensibilidade roda antes e depois do casamento pelos termos da base e da
  restrição do corpus, sobre as mesmas exportações
- **THEN** `sensibilidade_<base>.csv` tem conteúdo idêntico byte a byte

### Requirement: Casamento por prefixo é indício

`--aderencia` SHALL imprimir o casamento por prefixo de título como indício e MUST NOT
contá-lo no numerador da aderência. A confirmação do casamento por prefixo exige registro
humano na coluna `recuperada`.

#### Scenario: Prefixo não entra no numerador
- **WHEN** uma semente só casa com um registro por prefixo de título
- **THEN** o relato a marca como indício e não a conta como recuperada

### Requirement: Intervalo de confiança da aderência

O relato da aderência SHALL trazer, junto com a proporção, o intervalo de Wilson a 95%,
calculado sobre o mesmo numerador e o mesmo denominador.

#### Scenario: Intervalo para 8 de 10
- **WHEN** 8 de 10 sementes são recuperadas
- **THEN** o relato mostra 80% com intervalo de aproximadamente 49% a 94%

### Requirement: Aderência relatada sobre o conjunto
A aderência SHALL relatar a recuperação do conjunto-semente com um único numerador e
denominador e SHALL compará-la ao limiar de aderência, identificando-a como a que decide a
passagem.

#### Scenario: Relato único
- **WHEN** há 10 sementes, das quais 8 recuperadas
- **THEN** o relato mostra 8/10, comparado ao limiar, como a aderência que decide a
  passagem

#### Scenario: Abaixo do limiar
- **WHEN** a recuperação do conjunto fica abaixo do limiar
- **THEN** o relato declara a aderência abaixo do limiar

### Requirement: Arquivos de entrada e de saída lidos da configuração
A derivação, a aderência, a fidelidade, a sensibilidade e o instrumento de aderência
SHALL obter do `config.toml` o caminho de cada arquivo que leem ou gravam. Isso inclui
`registro_execucao.json`, o arquivo de sementes (`[documentos] sementes`),
`semente_aderencia.csv` e as saídas na raiz de `data/`.

#### Scenario: Registro em outro caminho
- **WHEN** o `config.toml` aponta o registro de execução para outro caminho
- **THEN** `busca registrar`, `busca derivar` e `dados conferir` leem e gravam esse
  caminho, e as mensagens o nomeiam

#### Scenario: Arquivo de sementes em outro caminho
- **WHEN** `[documentos] sementes` aponta outro arquivo
- **THEN** `aderencia planilhar` e `aderencia medir` leem as sementes desse arquivo

#### Scenario: Chave antiga do arquivo de conferência
- **WHEN** o `config.toml` traz a chave `[dados] sementes`
- **THEN** a configuração reprova, nomeando a chave, como as demais chaves fora do esquema

### Requirement: Regravação da planilha de aderência preserva o preenchimento manual
`aderencia planilhar` SHALL regravar `semente_aderencia.csv` conservando, em cada linha, as
colunas preenchidas à mão (`indexada`, `data_etapa1`, `recuperada`, `como_localizada`,
`data_etapa2` e `observacao`). A linha anterior casa com a nova por `id` e `base`, e só
casa se o título for o mesmo, sem distinguir acento nem caixa. As demais colunas MUST vir
sempre do arquivo de sementes e da tabela de bases, e a planilha MUST NOT trazer a coluna
`escopo`.

#### Scenario: Preenchimento conservado
- **WHEN** a planilha traz `indexada = sim` e `observacao` preenchida na linha SE2 × wos,
  e `aderencia planilhar` é executado de novo, sem mudança no arquivo de sementes
- **THEN** a linha SE2 × wos sai com o mesmo `indexada` e a mesma `observacao`

#### Scenario: Coluna derivada atualizada
- **WHEN** a `verificacao` de SE2 é alterada no arquivo de sementes e a planilha já traz
  colunas manuais de SE2
- **THEN** a regravação traz a `verificacao` nova e conserva as colunas manuais de SE2

#### Scenario: Sem coluna de escopo
- **WHEN** `aderencia planilhar` gera a planilha
- **THEN** o cabeçalho não traz `escopo`

#### Scenario: Primeira geração
- **WHEN** `semente_aderencia.csv` não existe
- **THEN** `aderencia planilhar` grava a planilha com as colunas manuais vazias

#### Scenario: Linha anterior sem preenchimento
- **WHEN** a planilha traz uma linha de semente ou de base que deixou de existir, com as
  colunas manuais vazias
- **THEN** a regravação omite essa linha e sai OK

### Requirement: Regravação recusada quando perderia preenchimento manual
`aderencia planilhar` MUST NOT gravar a planilha quando a regravação perderia conteúdo não
vazio da planilha anterior: coluna manual de linha sem par, de linha cujo título mudou, ou
de coluna fora do esquema. O subcomando SHALL sair com REPROVADO, nomeando cada `id`,
`base` e coluna afetados, e deixar o arquivo anterior intacto.

#### Scenario: Semente renumerada
- **WHEN** SE3 é retirada, SE4 passa a SE3, e a planilha traz `indexada` preenchida na
  linha SE3 × scopus com o título da semente retirada
- **THEN** `aderencia planilhar` sai com REPROVADO, nomeando SE3 × scopus e o título
  divergente, e `semente_aderencia.csv` não muda

#### Scenario: Semente retirada com preenchimento
- **WHEN** SE10 sai do arquivo de sementes e a planilha traz `recuperada` preenchida em
  SE10 × wos
- **THEN** `aderencia planilhar` sai com REPROVADO, nomeando SE10 × wos e a coluna
  `recuperada`, e `semente_aderencia.csv` não muda

#### Scenario: Coluna acrescentada à mão
- **WHEN** a planilha traz uma coluna fora do esquema com algum valor preenchido
- **THEN** `aderencia planilhar` sai com REPROVADO, nomeando a coluna, e
  `semente_aderencia.csv` não muda

#### Scenario: Planilha anterior ilegível
- **WHEN** `semente_aderencia.csv` existe e não é CSV legível
- **THEN** `aderencia planilhar` sai com DADOS, nomeando o arquivo, e não o regrava

### Requirement: Autoteste prova a preservação da planilha de aderência
O autoteste SHALL gerar a planilha num diretório temporário, preencher colunas manuais,
regravá-la e exigir que o preenchimento seja conservado. SHALL também exigir a recusa,
com o arquivo intacto, para semente renumerada e para linha sem par com preenchimento.
Os valores e os `id` usados MUST vir das sementes lidas, e não de literais.

#### Scenario: Regravação que apaga
- **WHEN** a regravação grava a planilha sem ler a anterior
- **THEN** o autoteste falha no caso de preservação

#### Scenario: Recusa ausente
- **WHEN** a regravação descarta a linha sem par com preenchimento
- **THEN** o autoteste falha no caso de recusa

### Requirement: Retorno declarado obrigatório no registro de execução
`busca registrar` SHALL exigir `--retorno` na validação de argumentos. Sem ele, o
subcomando MUST sair com USO antes de ler qualquer arquivo, e nada é registrado. A ajuda
(`-h`) SHALL apresentar `--retorno` como obrigatório.

#### Scenario: Sem retorno
- **WHEN** `busca registrar wos EB4 exportacao.txt` é executado sem `--retorno`
- **THEN** o subcomando sai com USO, nomeia `--retorno` como argumento exigido, e o
  registro de execução não muda

#### Scenario: Ajuda
- **WHEN** `busca registrar -h` é executado
- **THEN** a sinopse mostra `--retorno RETORNO` fora de colchetes

### Requirement: Registro de execução ausente remete à primeira execução registrada
Quando `[dados] registro` não existe, `projeto pendencias` SHALL relatar a ausência e orientar o
registro da primeira execução com `busca registrar`. A orientação MUST NOT mandar
reconstituir o registro a partir dos procedimentos de busca ou da memória.

#### Scenario: Registro ausente
- **WHEN** `projeto pendencias` é executado sem `registro_execucao.json`
- **THEN** a linha da ausência nomeia `busca registrar` e não contém "reconstitua"

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
