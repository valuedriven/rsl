# Spec Delta

## MODIFIED Requirements

### Requirement: Facetas do instrumento de aderência vêm do protocolo
As facetas usadas por `aderencia ensaiar` SHALL vir das facetas lidas do protocolo, na ordem
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
  os da executada, e as contagens, a ordem de triagem e a aderência que deles dependem;
- na aderência, a semente cujo DOI aparece na exportação, que passa a contar como
  recuperada mesmo sem casamento exato de título.

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
contá-lo no numerador da aderência. A semente só conta como recuperada por casamento exato
de título ou pelo DOI.

#### Scenario: Prefixo não entra no numerador
- **WHEN** uma semente só casa com um registro por prefixo de título
- **THEN** o relato a marca como indício e não a conta como recuperada

#### Scenario: Prefixo confirmado pelo DOI
- **WHEN** uma semente casa com um registro por prefixo de título e o DOI do registro é o da
  semente
- **THEN** a semente conta como recuperada, pelo DOI

### Requirement: Arquivos de entrada e de saída lidos da configuração
A derivação, a aderência, a fidelidade, a sensibilidade e o instrumento de aderência
SHALL obter do `config.toml` o caminho de cada arquivo que leem ou gravam. Isso inclui
`registro_execucao.json`, o arquivo de sementes (`[documentos] sementes`), a cópia da
coleção do Zotero (`[dados] zotero`) e as saídas na raiz de `data/`.

#### Scenario: Registro em outro caminho
- **WHEN** o `config.toml` aponta o registro de execução para outro caminho
- **THEN** `busca registrar`, `busca derivar` e `dados conferir` leem e gravam esse
  caminho, e as mensagens o nomeiam

#### Scenario: Arquivo de sementes em outro caminho
- **WHEN** `[documentos] sementes` aponta outro arquivo
- **THEN** `aderencia ensaiar` e `aderencia medir` leem as sementes desse arquivo

#### Scenario: Chave antiga do arquivo de conferência
- **WHEN** o `config.toml` traz a chave `[dados] sementes`
- **THEN** a configuração reprova, nomeando a chave, como as demais chaves fora do esquema

#### Scenario: Cópia da coleção em outro caminho
- **WHEN** `[dados] zotero` aponta outro arquivo
- **THEN** `aderencia ensaiar`, `aderencia medir` e `sementes copiar` leem e gravam esse
  arquivo

## ADDED Requirements

### Requirement: Recuperação da semente pelo DOI
`aderencia medir` SHALL contar como recuperada a semente cujo DOI, comparado em caixa baixa
e sem prefixo de URL, aparece num registro da exportação da executada, e SHALL relatar se a
semente foi recuperada pelo título, pelo DOI ou pelos dois.

#### Scenario: Título divergente, mesmo DOI
- **WHEN** o título do registro exportado difere do título do item do Zotero e o DOI é o
  mesmo
- **THEN** a semente conta como recuperada, e o relato diz que foi pelo DOI

## REMOVED Requirements

### Requirement: Regravação da planilha de aderência preserva o preenchimento manual
**Reason**: a planilha de aderência foi retirada: a indexação é o campo `bases` do arquivo de sementes e a recuperação é calculada por `aderencia medir`.
**Migration**: nenhum dado se perde, porque nenhuma coluna manual da planilha está preenchida; a explicação de cada perda vem de `aderencia diagnosticar`.

### Requirement: Regravação recusada quando perderia preenchimento manual
**Reason**: a planilha de aderência foi retirada; não há preenchimento manual a perder.
**Migration**: nenhum dado se perde, porque nenhuma coluna manual da planilha está preenchida; a explicação de cada perda vem de `aderencia diagnosticar`.

### Requirement: Autoteste prova a preservação da planilha de aderência
**Reason**: a planilha de aderência foi retirada.
**Migration**: nenhum dado se perde, porque nenhuma coluna manual da planilha está preenchida; a explicação de cada perda vem de `aderencia diagnosticar`.
