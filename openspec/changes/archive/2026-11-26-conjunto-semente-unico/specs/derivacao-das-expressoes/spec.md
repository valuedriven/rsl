# Spec Delta

## MODIFIED Requirements

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

### Requirement: Intervalo de confiança da aderência

O relato da aderência SHALL trazer, junto com a proporção, o intervalo de Wilson a 95%,
calculado sobre o mesmo numerador e o mesmo denominador.

#### Scenario: Intervalo para 8 de 10
- **WHEN** 8 de 10 sementes são recuperadas
- **THEN** o relato mostra 80% com intervalo de aproximadamente 49% a 94%

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

## ADDED Requirements

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

## REMOVED Requirements

### Requirement: Aderência relatada por papel da semente
**Reason**: A divisão entre sementes de validação e de desenvolvimento foi removida; todo o
conjunto é de validação e não há mais duas aderências a relatar.

**Migration**: O relato passa a ter um único numerador e denominador, coberto pelo
requisito "Aderência relatada sobre o conjunto". Nenhuma ação sobre o arquivo de sementes
além da remoção do campo `papel`.

### Requirement: Planilha de aderência traz o papel
**Reason**: O campo `papel` foi removido do arquivo de sementes, e a planilha não tem mais
de onde lê-lo.

**Migration**: `aderencia planilhar` regenera a planilha sem a coluna `papel`; as colunas
manuais continuam preservadas na regravação.
