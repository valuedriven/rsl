# validacao-terminologica Specification

## Purpose

Determinar contra que instrumentos de controle terminológico cada termo é validado a partir
da seção que o protocolo dedica aos instrumentos, e registrar como pendência o que não puder
ser consultado automaticamente.

## Requirements

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

### Requirement: Falha de fonte externa interrompe sem nova tentativa
A consulta automatizada a um instrumento SHALL fazer uma requisição por vez, sem
concorrência e sem nova tentativa automática. As condições abaixo MUST interromper a
validação na mesma hora, sem consultar o termo seguinte, sem outra rota e sem outro
endereço, e o subcomando termina com o código FONTE_EXTERNA:

- erro de rede;
- resposta HTTP 403 ou 429;
- resposta 5xx;
- página com captcha ou aviso de atividade atípica.

O que já foi consultado e registrado antes da interrupção SHALL ficar gravado na planilha
e na evidência. A mensagem MUST nomear o instrumento, o termo, a condição encontrada e
quantos termos ficaram sem consulta.

#### Scenario: Limite excedido
- **WHEN** o instrumento responde 429 na consulta do décimo termo
- **THEN** a validação para, os nove termos anteriores ficam registrados, nenhuma
  requisição nova é feita e a saída tem o código FONTE_EXTERNA

#### Scenario: Erro de rede
- **WHEN** a primeira requisição falha por erro de rede
- **THEN** nenhuma segunda requisição é feita, e a saída tem o código FONTE_EXTERNA

#### Scenario: Termo não localizado não é falha
- **WHEN** o instrumento responde normalmente sem o termo
- **THEN** o termo é registrado como termo livre, e a validação continua

### Requirement: Planilha de validação nomeada pela configuração
O caminho e o nome da planilha de validação SHALL vir do `config.toml`. O nome configurado
para o projeto é `validacao_terminologica.csv`.

#### Scenario: Grafia corrigida
- **WHEN** se procura `termologica` em `src/`, no `config.toml`, no README e nas skills
- **THEN** não há ocorrência

### Requirement: Domínio da decisão do ReT
A coluna `decisao_ReT` da planilha de validação SHALL admitir só `descritor`, `sinônimo ou
relacionado`, `termo livre` ou vazio, sem distinção de caixa. O vazio significa "sem
decisão". Valor fora do domínio MUST reprovar em `termos importar` e em `documentos
conferir`, nomeando o termo, a faceta, o idioma, o instrumento e o valor.

#### Scenario: Valor fora do domínio
- **WHEN** a planilha traz `decisao_ReT = autorizado` para `ontology` (FCT1, en, unesco)
- **THEN** `termos importar` reprova, nomeando o termo, o instrumento e os valores admitidos

#### Scenario: Caixa diferente
- **WHEN** a planilha traz `decisao_ReT = Descritor`
- **THEN** o valor é lido como `descritor`

### Requirement: Linha do termo resulta da decisão do ReT
A linha esperada de um termo no CT SHALL ser calculada sobre as decisões do ReT desse termo,
na faceta e no idioma dele, nos instrumentos planejados para ele: `descritores`, se alguma
decisão for `descritor`; senão `relacionados`, se alguma for `sinônimo ou relacionado`;
senão `livre`. `status_proposto` MUST NOT entrar no cálculo.

#### Scenario: Descritor em um instrumento
- **WHEN** `ontology` (FCT1, en) é `descritor` na UNESCO e `termo livre` no ERIC
- **THEN** a linha esperada é "Descritores correspondentes"

#### Scenario: Equivalente sem descritor
- **WHEN** `thesauri` (FCT1, en) é `sinônimo ou relacionado` na UNESCO e não tem outra decisão
- **THEN** a linha esperada é "Termos sinônimos ou relacionados"

#### Scenario: Instrumento manual pendente
- **WHEN** `learning context` (FCT4, en) está pendente de validação manual no ERIC e não tem
  decisão em outro instrumento
- **THEN** a linha esperada é "Termo livre"

#### Scenario: Proposta da máquina sem decisão
- **WHEN** `ontology` tem `status_proposto` de descritor autorizado na UNESCO e `decisao_ReT`
  vazia
- **THEN** a linha esperada é "Termo livre"

#### Scenario: Planilha ausente
- **WHEN** a planilha de validação não existe
- **THEN** a linha esperada de todo termo é "Termo livre"

### Requirement: Autoteste prova o domínio e a regra da linha
O autoteste SHALL verificar, sobre planilhas em memória, o domínio de `decisao_ReT` e a
regra da linha esperada: precedência de `descritor` sobre `sinônimo ou relacionado`,
pendência manual e proposta da máquina levando a `livre`, e valor fora do domínio
reprovado. Caso não verificado MUST fazer o autoteste falhar.

#### Scenario: Precedência invertida
- **WHEN** o autoteste dá a um termo `sinônimo ou relacionado` num instrumento e `descritor`
  noutro, e a linha calculada não é `descritores`
- **THEN** o autoteste falha, nomeando o caso
