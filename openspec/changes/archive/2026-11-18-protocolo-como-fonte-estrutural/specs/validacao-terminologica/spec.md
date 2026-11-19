# Spec Delta

## MODIFIED Requirements

### Requirement: Instrumentos por faceta, lidos da seção do protocolo
Os instrumentos de validação SHALL ser lidos da tabela da seção "Instrumentos para controle
terminológico" do protocolo, com as colunas `Sigla | Instrumento | Modo | Caminho | Idiomas
| FCTs`, uma linha por instrumento. As facetas de cada instrumento são as da coluna `FCTs`,
separadas por vírgula. O código MUST NOT fixar instrumento por idioma nem por faceta.

#### Scenario: Faceta com vários instrumentos
- **WHEN** a tabela declara FCT2 nas linhas de `unesco`, `eric` e `brased`
- **THEN** os termos de FCT2 são planejados para esses três instrumentos

#### Scenario: Instrumento retirado do protocolo
- **WHEN** uma faceta deixa de constar da coluna `FCTs` de um instrumento
- **THEN** nenhum termo dessa faceta é planejado para validação nele

#### Scenario: Seção ausente ou faceta sem linha
- **WHEN** a seção não existe ou uma faceta do quadro não consta da coluna `FCTs` de nenhum
  instrumento
- **THEN** a conferência reprova, nomeando a faceta, e nenhum instrumento padrão é presumido

#### Scenario: Faceta inexistente na coluna FCTs
- **WHEN** a coluna `FCTs` traz `FCT4s` ou outra grafia que não é faceta do protocolo
- **THEN** a leitura reprova, nomeando o instrumento e o valor

### Requirement: Instrumento sem cliente automatizado é pendência
Instrumento declarado `Manual` SHALL gerar linha na planilha com estatuto de pendência de
validação manual. Ela MUST NOT ser registrada como termo não encontrado.

#### Scenario: Instrumento manual
- **WHEN** a tabela declara um instrumento `Manual`
- **THEN** a planilha registra cada termo das facetas dele, nos idiomas do instrumento, como
  pendente de validação manual naquele instrumento

## REMOVED Requirements

### Requirement: Nome do instrumento é resolvido pela configuração
**Reason**: sigla, modo e idiomas do instrumento passam a ser declarados na tabela do
protocolo; não há mais mapa de instrumentos em `config.toml`.
**Migration**: declarar cada instrumento numa linha da tabela "Instrumentos para controle
terminológico"; os requisitos "Propriedades do instrumento lidas do protocolo" e "Modo
automático exige cliente da sigla" substituem este.

## ADDED Requirements

### Requirement: Propriedades do instrumento lidas do protocolo
Sigla, modo, caminho e idiomas de cada instrumento SHALL ser lidos da sua linha na tabela. A
sigla MUST ser única e é o valor gravado na coluna `instrumento` da planilha. Os idiomas
MUST estar entre os idiomas do quadro terminológico. Campo vazio reprova.

#### Scenario: Termo fora dos idiomas do instrumento
- **WHEN** a linha de `tbci` declara só `pt`
- **THEN** só os termos em português das facetas de `tbci` são planejados para ele

#### Scenario: Idioma fora do quadro
- **WHEN** um instrumento declara o idioma `fr` e o quadro não tem coluna `fr`
- **THEN** a leitura reprova, nomeando o instrumento e o idioma

### Requirement: Modo automático exige cliente da sigla
`Modo` SHALL admitir só `Manual` ou `Automático`. Instrumento `Automático` SHALL ser
consultado pelo cliente cujo nome é a sua sigla; sem cliente com esse nome, a leitura MUST
reprovar. `Caminho` é a referência do instrumento para relato e consulta manual; o
endereço de consulta automática pertence ao cliente.

#### Scenario: Automático sem cliente
- **WHEN** a linha de `eric` declara `Automático` e não há cliente `eric`
- **THEN** a leitura reprova, nomeando a sigla e os clientes existentes

#### Scenario: Modo fora do domínio
- **WHEN** a coluna `Modo` traz `Semiautomático`
- **THEN** a leitura reprova, nomeando o instrumento e os valores admitidos
