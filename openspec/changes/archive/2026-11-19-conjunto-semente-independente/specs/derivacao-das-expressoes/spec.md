# Spec Delta

## MODIFIED Requirements

### Requirement: Saídas preservadas
Para o protocolo e a configuração atuais, as saídas da derivação, da aderência, da
fidelidade e da sensibilidade MUST ser idênticas às anteriores à mudança, exceto a redação
da coluna `facetas_exigidas` de `contagens_busca.csv`, que passa à forma estrita
(`FCT1 AND FCT2 AND (FCT3 OR FCT4)`) por decisão do pesquisador, a grafia das siglas das
bases, que passa a ser a do protocolo (`wos`, `scopus`, `eric`, `brapci`), e, na aderência,
o relato separado por papel da semente, com o intervalo de confiança, a coluna `papel` da
planilha de aderência e o casamento por prefixo, que deixa de entrar no numerador e passa a
ser relatado como indício.

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

## ADDED Requirements

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
semente lido do protocolo.

#### Scenario: Coluna de papel
- **WHEN** `gen_semente.py` gera a planilha
- **THEN** cada linha traz a coluna `papel` com `desenvolvimento` ou `validação`, igual à
  da tabela do protocolo
