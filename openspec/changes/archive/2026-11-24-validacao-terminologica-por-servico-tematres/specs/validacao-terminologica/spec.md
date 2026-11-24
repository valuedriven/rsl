# Spec Delta

## ADDED Requirements

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
preferido ou não preferido. Termo sem casamento exato SHALL receber estatuto de termo livre
não localizado. A proposta MUST NOT preencher `decisao_ReT`.

#### Scenario: Termo preferido
- **WHEN** `ontology` casa com um descritor do instrumento
- **THEN** `status_proposto` é de descritor, e `rotulo_autorizado` traz o rótulo do instrumento

#### Scenario: Termo não preferido
- **WHEN** `learning environment` casa com um termo não preferido (UF) do instrumento
- **THEN** `status_proposto` é de descritor, e `decisao_ReT` fica vazia

#### Scenario: Sem casamento exato
- **WHEN** a busca devolve só `learning environments` para `learning environment`
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
- **THEN** a linha volta a aguardar consulta, e a evidência anterior permanece no diretório de evidência

#### Scenario: Endereço mudou com decisão
- **WHEN** a mesma linha tem `decisao_ReT = descritor`
- **THEN** a linha não é reconsultada nem alterada, e a saída a lista como decisão tomada sobre evidência de outro endereço

#### Scenario: Linha vigente
- **WHEN** a `url_consultada` da linha pertence ao endereço resolvido vigente
- **THEN** a linha não é reconsultada

### Requirement: Sonda por endereço resolvido
`termos sondar` SHALL consultar cada endereço resolvido de cada instrumento `Automático`,
um por idioma quando houver o marcador, com os metadados do vocabulário, termos de prova do
protocolo naquele idioma e um termo inexistente, sem gravar nada, e SHALL mostrar se a
resposta distingue termo preferido de não preferido.

#### Scenario: UNESCO em dois idiomas
- **WHEN** `unesco` declara `{idioma}` e os idiomas `en, es`
- **THEN** a sonda consulta os dois endereços, com termos de prova em inglês no primeiro e em espanhol no segundo

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

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: Modo automático exige cliente da sigla
**Reason**: `Caminho` passou a ser o endereço do serviço e os quatro instrumentos são
servidos por TemaTres; um cliente único, guiado pelo protocolo, substitui um cliente por
sigla, e o endereço deixa de pertencer ao código.
**Migration**: ver "Modo Automático é consulta ao serviço TemaTres do Caminho" e "Caminho é
o endereço do serviço consultado". O domínio de `Modo` continua `Manual` ou `Automático`, e
o cenário "Modo fora do domínio" passa ao primeiro desses requisitos.
