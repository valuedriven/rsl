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
- na aderência, o relato separado por papel da semente, com o intervalo de confiança, a
  coluna `papel` da planilha de aderência e o casamento por prefixo, que deixa de entrar no
  numerador e passa a ser relatado como indício;
- o **nome** dos arquivos de saída, que segue a convenção de nomes da interface de comando
  e vem do `config.toml` (`fidelidade_EB<n>.csv` passa a `fidelidade_eb<n>.csv`).

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

### Requirement: Aderência relatada por papel da semente

`--aderencia` SHALL relatar separadamente a recuperação das sementes de validação e a das
de desenvolvimento, com numerador e denominador de cada uma. Só a das sementes de validação
SHALL ser comparada ao limiar de aderência, e o relato MUST identificar qual das duas é a
que decide a passagem.

#### Scenario: Relato separado
- **WHEN** há 6 sementes de validação, das quais 5 recuperadas, e 4 de desenvolvimento,
  todas recuperadas
- **THEN** o relato mostra 5/6 para validação, comparado ao limiar, e 4/4 para
  desenvolvimento, marcado como não decisório

#### Scenario: Desenvolvimento não compensa validação
- **WHEN** a recuperação de validação fica abaixo do limiar e a total, somando
  desenvolvimento, fica acima
- **THEN** o relato declara a aderência abaixo do limiar

### Requirement: Casamento por prefixo é indício

`--aderencia` SHALL imprimir o casamento por prefixo de título como indício e MUST NOT
contá-lo no numerador da aderência. A confirmação do casamento por prefixo exige registro
humano na coluna `recuperada`.

#### Scenario: Prefixo não entra no numerador
- **WHEN** uma semente só casa com um registro por prefixo de título
- **THEN** o relato a marca como indício e não a conta como recuperada

### Requirement: Intervalo de confiança da aderência

O relato da aderência de validação SHALL trazer, junto com a proporção, o intervalo de
Wilson a 95%, calculado sobre o mesmo numerador e o mesmo denominador.

#### Scenario: Intervalo para 8 de 10
- **WHEN** 8 de 10 sementes de validação são recuperadas
- **THEN** o relato mostra 80% com intervalo de aproximadamente 49% a 94%

### Requirement: Planilha de aderência traz o papel

A planilha gerada pelo instrumento de aderência SHALL ter, em cada linha, o papel da
semente lido do arquivo de sementes. Os dados de conferência SHALL vir do mesmo arquivo,
e a planilha MUST NOT trazer a coluna `escopo`.

#### Scenario: Coluna de papel
- **WHEN** `aderencia planilhar` gera a planilha
- **THEN** cada linha traz a coluna `papel` com `desenvolvimento` ou `validação`, igual ao
  campo `papel` da semente no arquivo de sementes

#### Scenario: Sem coluna de escopo
- **WHEN** `aderencia planilhar` gera a planilha
- **THEN** o cabeçalho não traz `escopo`

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
sempre do arquivo de sementes e da tabela de bases.

#### Scenario: Preenchimento conservado
- **WHEN** a planilha traz `indexada = sim` e `observacao` preenchida na linha SE2 × wos,
  e `aderencia planilhar` é executado de novo, sem mudança no arquivo de sementes
- **THEN** a linha SE2 × wos sai com o mesmo `indexada` e a mesma `observacao`

#### Scenario: Coluna derivada atualizada
- **WHEN** o `tipo` de SE2 é preenchido no arquivo de sementes e a planilha já traz
  colunas manuais de SE2
- **THEN** a regravação traz o `tipo` novo e conserva as colunas manuais de SE2

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
