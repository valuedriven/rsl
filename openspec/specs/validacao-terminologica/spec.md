# validacao-terminologica Specification

## Purpose

Determinar contra que instrumentos de controle terminológico cada termo é validado a partir
da seção que o protocolo dedica aos instrumentos, e registrar como pendência o que não puder
ser consultado automaticamente.

## Requirements

### Requirement: Instrumentos por faceta, lidos da seção do protocolo
Os instrumentos de validação de cada faceta SHALL ser lidos da seção "Instrumentos para
controle terminológico" do protocolo, uma linha por faceta com os nomes separados por vírgula.
O código MUST NOT fixar instrumento por idioma nem por faceta.

#### Scenario: Faceta com vários instrumentos
- **WHEN** o protocolo declara para FCT2 "ERIC Thesaurus, Brased/INEP, UNESCO Thesaurus"
- **THEN** os termos de FCT2 são planejados para esses três instrumentos

#### Scenario: Instrumento retirado do protocolo
- **WHEN** um instrumento deixa de constar da linha de uma faceta
- **THEN** nenhum termo dessa faceta é planejado para validação nele

#### Scenario: Seção ausente ou faceta sem linha
- **WHEN** a seção não existe ou uma faceta do quadro não tem linha nela
- **THEN** a conferência reprova, nomeando a faceta, e nenhum instrumento padrão é presumido

### Requirement: Nome do instrumento é resolvido pela configuração
Cada nome de instrumento lido do protocolo SHALL ser resolvido, pelo mapa da configuração,
para um modo de consulta (cliente automatizado ou manual) e para os idiomas que o instrumento
cobre. Nome sem entrada no mapa MUST reprovar a conferência, nomeando a faceta e o nome.

#### Scenario: Nome não mapeado
- **WHEN** o protocolo declara um instrumento cujo nome não consta do mapa
- **THEN** a conferência reprova, nomeando a faceta e o nome

#### Scenario: Termo fora dos idiomas do instrumento
- **WHEN** a configuração declara que o instrumento cobre só o português
- **THEN** só os termos em português da faceta são planejados para esse instrumento

### Requirement: Instrumento sem cliente automatizado é pendência
Instrumento mapeado como manual SHALL gerar linha na planilha com estatuto de pendência de
validação manual. Ela MUST NOT ser registrada como termo não encontrado.

#### Scenario: Instrumento manual
- **WHEN** a faceta declara um instrumento mapeado como manual
- **THEN** a planilha registra cada termo dessa faceta, nos idiomas do instrumento, como
  pendente de validação manual naquele instrumento

### Requirement: Autoteste do planejamento da validação
O autoteste SHALL verificar, sobre o protocolo e cópias alteradas em memória, o
planejamento dos termos por instrumento: todos os instrumentos da faceta, nenhum
instrumento retirado da linha, só os idiomas que o instrumento cobre e o modo manual.

#### Scenario: Instrumento retirado da linha
- **WHEN** o autoteste retira um instrumento da linha de uma faceta numa cópia do protocolo
- **THEN** nenhum termo dessa faceta é planejado para ele; o contrário faz o autoteste falhar

#### Scenario: Filtro por idioma
- **WHEN** o autoteste planeja um termo num idioma que um instrumento da faceta não cobre
- **THEN** esse instrumento não é planejado para o termo

#### Scenario: Instrumento manual
- **WHEN** a faceta declara instrumento de modo `manual`
- **THEN** o planejamento o marca como manual, e a linha nasce pendente de validação manual
