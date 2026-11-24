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
validação manual. Ela MUST NOT ser registrada como termo não encontrado. Instrumento
`Automático` MUST NOT gerar linha nesse estatuto.

#### Scenario: Instrumento manual
- **WHEN** a tabela declara um instrumento `Manual`
- **THEN** a planilha registra cada termo das facetas dele, nos idiomas do instrumento, como
  pendente de validação manual naquele instrumento

#### Scenario: Instrumento automático
- **WHEN** a tabela declara um instrumento `Automático`
- **THEN** nenhuma linha dele nasce nem permanece pendente de validação manual sem decisão

### Requirement: Autoteste do planejamento da validação
O autoteste SHALL verificar, sobre o protocolo e cópias alteradas em memória, o
planejamento dos termos por instrumento: todos os instrumentos da faceta, nenhum
instrumento retirado da linha, só os idiomas que o instrumento cobre e o modo manual. O
caso do modo manual MUST ser provado sobre cópia alterada, sem depender de o protocolo
vigente declarar instrumento `Manual`.

#### Scenario: Instrumento retirado da linha
- **WHEN** o autoteste retira um instrumento da linha de uma faceta numa cópia do protocolo
- **THEN** nenhum termo dessa faceta é planejado para ele; o contrário faz o autoteste falhar

#### Scenario: Filtro por idioma
- **WHEN** o autoteste planeja um termo num idioma que um instrumento da faceta não cobre
- **THEN** esse instrumento não é planejado para o termo

#### Scenario: Instrumento manual
- **WHEN** a faceta declara instrumento de modo `manual`
- **THEN** o planejamento o marca como manual, e a linha nasce pendente de validação manual

#### Scenario: Protocolo só com instrumentos automáticos
- **WHEN** o protocolo vigente declara todos os instrumentos `Automático`
- **THEN** o caso do modo manual é verificado sobre uma cópia em que um deles passa a `Manual`, e o autoteste não falha por falta de instrumento manual no protocolo

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
- **WHEN** `learning context` (FCT4, en) está pendente de validação manual num instrumento
  declarado `Manual` e não tem decisão em outro instrumento
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

### Requirement: Caminho é o endereço do serviço consultado
`Caminho` SHALL ser o endereço do serviço consultado na validação automatizada, lido do
protocolo; o código MUST NOT fixar endereço de instrumento. `Caminho` MAY conter o marcador
`{idioma}`, trocado por cada idioma da coluna `Idiomas`; sem o marcador, o mesmo endereço
vale para todos os idiomas do instrumento. Outro marcador entre chaves MUST reprovar a
leitura, nomeando o instrumento e o marcador.

#### Scenario: Endereço por idioma
- **WHEN** a linha de `unesco` declara `https://www.vocabularyserver.com/unesco/{idioma}/services.php` e os idiomas `en, es`
- **THEN** os termos em inglês são consultados em `.../unesco/en/services.php` e os em espanhol em `.../unesco/es/services.php`

#### Scenario: Endereço único
- **WHEN** a linha de `eric` declara `https://www.vocabularyserver.com/eric/services.php` sem marcador
- **THEN** todo termo planejado para `eric` é consultado nesse endereço

#### Scenario: Marcador desconhecido
- **WHEN** a linha de `unesco` declara `.../unesco/{lingua}/services.php`
- **THEN** a leitura reprova, nomeando `unesco` e `{lingua}`

#### Scenario: Endereço alterado no protocolo
- **WHEN** o pesquisador muda o `Caminho` de um instrumento
- **THEN** a consulta seguinte usa o endereço novo, sem alteração de código

### Requirement: Modo Automático é consulta ao serviço TemaTres do Caminho
Instrumento `Automático` SHALL ser consultado por um único cliente do serviço TemaTres, no
endereço resolvido do seu `Caminho`. A leitura MUST NOT exigir cliente com o nome da sigla:
qualquer sigla admite modo `Automático`.

#### Scenario: Instrumento novo automático
- **WHEN** o protocolo acrescenta a linha `xyz` em modo `Automático` com `Caminho` de serviço TemaTres
- **THEN** a leitura aceita a linha, e os termos das facetas de `xyz` são planejados para consulta automatizada nesse endereço

#### Scenario: Os quatro instrumentos do protocolo
- **WHEN** `tbci`, `unesco`, `eric` e `brased` são declarados `Automático`
- **THEN** o protocolo é legível, e `termos validar todos` consulta os quatro

#### Scenario: Modo fora do domínio
- **WHEN** a coluna `Modo` traz `Semiautomático`
- **THEN** a leitura reprova, nomeando o instrumento e os valores admitidos `Manual` e `Automático`

### Requirement: Rótulo encontrado é proposto como descritor
Termo cujo rótulo casa exatamente, sem distinção de caixa e de espaços, com um termo do
instrumento SHALL receber `status_proposto` de descritor, seja o termo do instrumento
preferido ou não preferido. Termo sem casamento exato SHALL seguir a consulta de
similaridade, e SHALL receber estatuto de termo livre não localizado quando ela não der
candidato. A proposta MUST NOT preencher `decisao_ReT`.

#### Scenario: Termo preferido
- **WHEN** `ontology` casa com um descritor do instrumento
- **THEN** `status_proposto` é de descritor, e `rotulo_autorizado` traz o rótulo do instrumento

#### Scenario: Termo não preferido
- **WHEN** `learning environment` casa com um termo não preferido (UF) do instrumento
- **THEN** `status_proposto` é de descritor, e `decisao_ReT` fica vazia

#### Scenario: Sem casamento exato
- **WHEN** a busca devolve só `learning environments` para `learning environment`, e a consulta por prefixo não dá item único
- **THEN** `status_proposto` é de termo livre não localizado

### Requirement: Forma do termo no instrumento registrada
A planilha SHALL ter a coluna `forma_no_instrumento`, com `preferido`, `não preferido` ou
vazio. Ela MUST ser preenchida só com o que a resposta do serviço informa; quando o serviço
não distingue a forma, fica vazia, e a forma MUST NOT ser inferida.

#### Scenario: Serviço informa a forma
- **WHEN** a resposta identifica o termo encontrado como não preferido
- **THEN** `forma_no_instrumento` é `não preferido`

#### Scenario: Serviço não informa
- **WHEN** a resposta não distingue termo preferido de não preferido
- **THEN** `forma_no_instrumento` fica vazia, e `observacao_tecnica` diz que o serviço não informou a forma

### Requirement: Linha de outro endereço volta a aguardar consulta
Linha sem `decisao_ReT` de instrumento `Automático` SHALL voltar a aguardar consulta quando
estiver pendente de validação manual ou quando a sua `url_consultada` não pertencer ao
endereço resolvido vigente para o seu idioma. Linha nessa situação com `decisao_ReT` MUST
ser preservada e listada na saída, nomeando termo, instrumento e endereço da evidência.

#### Scenario: Linha nascida manual
- **WHEN** `eric` passa de `Manual` a `Automático`, e a linha de `learning context` está pendente de validação manual sem decisão
- **THEN** a linha volta a aguardar consulta, e `termos validar eric` a consulta

#### Scenario: Endereço mudou
- **WHEN** a linha de `ontology` em `unesco` foi consultada em `https://vocabularies.unesco.org/sparql` e o `Caminho` vigente é outro
- **THEN** a linha volta a aguardar consulta, e a evidência anterior fica no diretório de evidência até a reconsulta, que a substitui no mesmo arquivo

#### Scenario: Endereço mudou com decisão
- **WHEN** a mesma linha tem `decisao_ReT = descritor`
- **THEN** a linha não é reconsultada nem alterada, e a saída a lista como decisão tomada sobre evidência de outro endereço

#### Scenario: Linha vigente
- **WHEN** a `url_consultada` da linha pertence ao endereço resolvido vigente
- **THEN** a linha não é reconsultada

### Requirement: Sonda por endereço resolvido
`termos sondar` SHALL consultar cada endereço resolvido de cada instrumento `Automático`,
um por idioma quando houver o marcador, com os metadados do vocabulário, termos de prova do
protocolo naquele idioma e um termo inexistente, sem gravar nada. SHALL mostrar se a
resposta distingue termo preferido de não preferido e os itens da consulta por prefixo para
cada termo de prova e para o termo inexistente.

#### Scenario: UNESCO em dois idiomas
- **WHEN** `unesco` declara `{idioma}` e os idiomas `en, es`
- **THEN** a sonda consulta os dois endereços, com termos de prova em inglês no primeiro e em espanhol no segundo

#### Scenario: Prefixo do termo inexistente
- **WHEN** a sonda consulta o prefixo do termo inexistente
- **THEN** a saída mostra os itens devolvidos, ou a ausência deles

#### Scenario: Interrupção na sonda
- **WHEN** um endereço responde 403 ou página de verificação anti-robô
- **THEN** a sonda para na hora, sem consultar o endereço seguinte, e termina com FONTE_EXTERNA

### Requirement: Autoteste prova endereço resolvido e reabertura
O autoteste SHALL verificar, sobre cópias alteradas em memória, a resolução de `{idioma}`,
a reprovação de marcador desconhecido, a reabertura da linha manual e da linha de outro
endereço sem decisão, e a preservação da linha com decisão. Caso não verificado MUST fazer o
autoteste falhar.

#### Scenario: Reabertura desligada
- **WHEN** a regra de reabertura deixa de valer e uma linha de outro endereço sem decisão não volta a aguardar consulta
- **THEN** o autoteste falha, nomeando o caso

#### Scenario: Marcador aceito sem resolução
- **WHEN** o endereço resolvido de um termo em espanhol ainda contém `{idioma}` ou `/en/`
- **THEN** o autoteste falha, nomeando o instrumento e o idioma

### Requirement: Termo sem casamento exato consulta a similaridade
Termo sem casamento exato SHALL ser submetido à consulta por prefixo do serviço
(`suggestDetails`), com o termo inteiro, no mesmo endereço resolvido. Com um único item
devolvido, a linha SHALL receber `status_proposto` de candidato por similaridade, com
rótulo, identificador, forma no instrumento e relações do item, qualquer que seja a forma do
item e a posição do termo no rótulo. A proposta MUST NOT
preencher `decisao_ReT` nem propor descritor.

#### Scenario: Item único
- **WHEN** `teaching method` não casa exatamente no ERIC, e `suggestDetails` devolve só `Teaching Methods`
- **THEN** `status_proposto` é de candidato por similaridade, `sugestao_similar` traz `Teaching Methods`, e `rotulo_autorizado` e `uri_conceito` são os desse item

#### Scenario: Item único por entrada não preferida
- **WHEN** o único item devolvido casa pela entrada não preferida `Self teaching methods`, que remete a `Self instruction`
- **THEN** `status_proposto` é de candidato, `rotulo_autorizado` traz `Self instruction`, `forma_no_instrumento` é não preferido, e `sugestao_similar` traz a entrada e o preferido

#### Scenario: Item único com o termo no meio do rótulo
- **WHEN** o único item devolvido para `ambiente educacional` é o preferido `Organização do Ambiente Educacional`
- **THEN** `status_proposto` é de candidato, a conferir pelo ReT

#### Scenario: Sem sugestão
- **WHEN** `suggestDetails` não devolve item
- **THEN** `status_proposto` é de termo livre não localizado, e `sugestao_similar` registra que o serviço não sugeriu termo

#### Scenario: Candidato não classifica o termo
- **WHEN** a linha é candidata por similaridade e `decisao_ReT` está vazia
- **THEN** a linha esperada do termo no CT é "Termo livre"

### Requirement: Vários itens não são escolhidos pelo cliente
Com mais de um item devolvido pela consulta por prefixo, o cliente MUST NOT escolher entre
eles: a linha SHALL ficar termo livre não localizado, com todos os itens devolvidos em
`sugestao_similar`, e a escolha é do ReT. `observacao_tecnica` SHALL registrar quantos
itens vieram e a contagem declarada pelo serviço, pois a lista pode ter sido limitada por
ele.

#### Scenario: Vários itens
- **WHEN** `suggestDetails` devolve `Self instruction`, `Teaching method innovations` e `Teaching methods` para `teaching method` na UNESCO
- **THEN** `status_proposto` é de termo livre não localizado, os campos de conceito ficam vazios, `sugestao_similar` traz os três, com rótulo e identificador, na ordem do serviço, e `observacao_tecnica` registra 3 itens e a contagem do serviço

### Requirement: Sugestão de similaridade registrada
A planilha SHALL ter a coluna `sugestao_similar`. Em linha consultada sem casamento exato,
ela MUST trazer a sugestão do serviço ou a indicação de que não houve sugestão, e MUST NOT
ficar vazia. Em linha com casamento exato, fica vazia.

#### Scenario: Casamento exato
- **WHEN** `ontology` casa exatamente com um descritor do instrumento
- **THEN** a consulta por prefixo não é feita, e `sugestao_similar` fica vazia

### Requirement: Linha não localizada sem similaridade volta a aguardar consulta
Linha sem `decisao_ReT`, de instrumento `Automático`, com `status_proposto` de termo livre
não localizado e `sugestao_similar` vazia SHALL voltar a aguardar consulta. Linha nessa
situação com `decisao_ReT` MUST ser preservada sem reconsulta.

#### Scenario: Linha da validação anterior
- **WHEN** a linha de `teaching method` no ERIC é termo livre não localizado, sem `sugestao_similar` e sem decisão
- **THEN** a linha volta a aguardar consulta, e `termos validar eric` a consulta de novo

#### Scenario: Linha já consultada sem sugestão
- **WHEN** a linha é termo livre não localizado e `sugestao_similar` registra que não houve sugestão
- **THEN** a linha não é reconsultada

#### Scenario: Linha com decisão
- **WHEN** a linha é termo livre não localizado, sem `sugestao_similar`, com `decisao_ReT = termo livre`
- **THEN** a linha não é reconsultada nem alterada

### Requirement: Autoteste prova a similaridade e a reabertura correspondente
O autoteste SHALL verificar, sobre respostas e planilhas em memória, os desfechos da
consulta por prefixo (item único, item único por entrada não preferida, vários itens, sem
item) e a reabertura da linha não localizada sem `sugestao_similar`. Caso não
verificado MUST fazer o autoteste falhar.

#### Scenario: Reabertura desligada
- **WHEN** a regra deixa de reabrir a linha não localizada sem `sugestao_similar`
- **THEN** o autoteste falha, nomeando o caso
