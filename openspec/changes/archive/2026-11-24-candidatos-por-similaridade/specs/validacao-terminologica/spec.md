# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

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
