# Spec Delta

## ADDED Requirements

### Requirement: Registro da validação em dois arquivos
O registro da validação SHALL ser dividido em um arquivo de decisões e um resultado técnico,
com o caminho de cada um no `config.toml`. O arquivo de decisões SHALL guardar, por termo,
idioma e instrumento, a decisão do ReT; o resultado técnico SHALL guardar, para a mesma
chave, os dados da consulta e a resposta do instrumento. Um mesmo dado MUST NOT ser gravado
nos dois arquivos.

#### Scenario: Decisão só no arquivo de decisões
- **WHEN** o pesquisador registra uma decisão para um termo e instrumento
- **THEN** ela consta apenas do arquivo de decisões, e o resultado técnico não tem campo de
  decisão

#### Scenario: Consulta só no resultado técnico
- **WHEN** um termo é consultado em um instrumento
- **THEN** os dados da resposta constam apenas do resultado técnico, e o arquivo de decisões
  não repete rótulo, forma, sugestão, relações, URL ou evidência

#### Scenario: Decisão sem consulta registrada
- **WHEN** o arquivo de decisões traz uma decisão para uma chave que não tem linha no
  resultado técnico
- **THEN** a decisão é preservada e listada na saída da reconciliação, e não é descartada

#### Scenario: Consulta sem decisão
- **WHEN** o resultado técnico traz uma linha consultada cuja chave não tem decisão
- **THEN** a linha é preservada, e a ausência de decisão não é erro

#### Scenario: Registros ausentes
- **WHEN** nem o arquivo de decisões nem o resultado técnico existem
- **THEN** a linha esperada de todo termo no CT é "Termo livre"

### Requirement: Arquivo de decisões em TOML
O arquivo de decisões SHALL ser TOML, com uma tabela `[[decisoes]]` por termo, idioma e
instrumento decidido do protocolo, carregando `faceta`, `idioma`, `termo`, `instrumento` e,
quando houver, `decisao_ReT`, `justificativa_ReT` e `data_decisao`. Tabela sem nenhum campo de
decisão MUST NOT ser gravada. Identificação ausente, campo desconhecido, chave duplicada ou
data fora de `AAAA-MM-DD` MUST reprovar, nomeando a entrada.

#### Scenario: Justificativa multilinha
- **WHEN** a `justificativa_ReT` de uma tabela contém mais de uma linha
- **THEN** a leitura preserva o texto inteiro, e a regravação o mantém legível

#### Scenario: Tabela sem decisão
- **WHEN** a reconstrução encontra uma chave sem decisão, justificativa ou data
- **THEN** nenhuma tabela é gravada para ela

#### Scenario: Campo desconhecido
- **WHEN** uma tabela traz um campo que não é de identificação nem de decisão
- **THEN** `termos importar` e `documentos conferir` reprovam, nomeando a tabela e o campo

#### Scenario: Chave duplicada
- **WHEN** duas tabelas têm a mesma faceta, idioma, termo e instrumento
- **THEN** a leitura reprova, nomeando a chave repetida

#### Scenario: Data fora da forma
- **WHEN** uma tabela traz `data_decisao = "26/11/2026"`
- **THEN** a leitura reprova, nomeando o termo, o instrumento e a forma admitida
  `AAAA-MM-DD`

#### Scenario: Decisão de termo fora do protocolo
- **WHEN** uma tabela de decisão não corresponde a nenhuma chave do protocolo
- **THEN** ela é removida na reconstrução dos registros, sem ser gravada nem listada, e
  `documentos conferir` reprova enquanto ela existir

### Requirement: Resultado técnico em JSON
O resultado técnico SHALL ser JSON, com um vetor `linhas` e um objeto por termo, idioma e
instrumento consultado do protocolo. O objeto SHALL carregar os dados da consulta, a
resposta do instrumento e o caminho da evidência. Linha nunca consultada MUST NOT ser
gravada: a ausência significa "aguardando consulta". Linha de termo fora do protocolo MUST
NOT permanecer.

#### Scenario: Linha consultada
- **WHEN** um termo é consultado com sucesso
- **THEN** o objeto traz `consultado_em`, `versao_instrumento`, `url_consultada`,
  `status_proposto`, os campos da resposta e `arquivo_evidencia`

#### Scenario: Linha nunca consultada
- **WHEN** uma chave do protocolo ainda não foi consultada
- **THEN** ela não consta do resultado técnico, e a ausência é lida como "aguardando
  consulta"

#### Scenario: Consulta interrompida
- **WHEN** a consulta de um termo é interrompida por fonte externa
- **THEN** a linha consta do resultado técnico com a observação técnica e sem
  `status_proposto` nem `arquivo_evidencia`

#### Scenario: Termo retirado do protocolo
- **WHEN** a reconstrução encontra uma linha técnica cuja chave não está no protocolo
- **THEN** a linha é retirada do resultado técnico

#### Scenario: JSON ilegível
- **WHEN** o resultado técnico não é JSON válido ou não traz o vetor `linhas`
- **THEN** os comandos que o leem terminam com DADOS, nomeando o arquivo

#### Scenario: Chave duplicada no resultado técnico
- **WHEN** dois objetos têm a mesma faceta, idioma, termo e instrumento
- **THEN** a leitura termina com DADOS, nomeando a chave repetida

### Requirement: Evidência vigente versionada e expurgo
Só a resposta bruta da consulta vigente de cada termo do protocolo SHALL ser versionada. A
evidência gerenciada é o arquivo `<instrumento>/<16 hex>.json` sob `[dados] evidencia`.
`termos exportar` e `termos importar` SHALL remover a evidência gerenciada cuja chave não
pertence mais ao protocolo, e MUST NOT remover evidência de outro tipo. Linha técnica com
`status_proposto` cuja evidência esteja ausente MUST reprovar antes de qualquer expurgo.

#### Scenario: Termo retirado do protocolo
- **WHEN** um termo deixa de constar do protocolo e os registros são reconstruídos
- **THEN** a decisão eventual, a linha técnica e a evidência gerenciada dele são removidas

#### Scenario: Reconsulta
- **WHEN** um termo do protocolo é consultado de novo
- **THEN** a resposta nova substitui a anterior no mesmo arquivo de evidência, e a anterior
  não permanece

#### Scenario: Linha reaberta
- **WHEN** uma linha sem decisão volta a aguardar consulta
- **THEN** a evidência anterior continua no diretório até a reconsulta, que a substitui

#### Scenario: Evidência de outro tipo
- **WHEN** a pasta de evidência contém sondagens, respostas da OpenAlex ou do Crossref,
  referências, cópias do Zotero ou a sonda de instrumentos
- **THEN** o expurgo não toca nesses arquivos

#### Scenario: Evidência ausente
- **WHEN** uma linha técnica consultada aponta evidência que não existe
- **THEN** `termos exportar` e `termos importar` reprovam, nomeando o termo e o arquivo, e
  nada é expurgado

### Requirement: Reconciliação sincroniza a partir do protocolo
`termos exportar` e `termos importar` SHALL reconstruir os dois arquivos a partir das chaves
do protocolo, preservando as decisões dessas chaves e removendo a decisão, a linha técnica e
a evidência de chave fora do protocolo. Não se mantém histórico de termos, e os dois comandos
MUST terminar com OK.

#### Scenario: Exportação com decisão fora do protocolo
- **WHEN** `termos exportar` reconstrói os registros e encontra uma decisão sem chave no
  protocolo
- **THEN** a decisão é removida, a saída informa quantas foram removidas e o comando termina
  com OK

#### Scenario: Importação com decisão fora do protocolo
- **WHEN** `termos importar` encontra uma decisão sem chave no protocolo
- **THEN** a decisão é removida, a saída informa quantas foram removidas e o comando termina
  com OK

#### Scenario: Importação sem decisão fora do protocolo
- **WHEN** todas as decisões correspondem a chaves do protocolo
- **THEN** `termos importar` termina com OK, sem informar remoção

#### Scenario: Linha técnica fora do protocolo
- **WHEN** o resultado técnico traz uma chave que saiu do protocolo
- **THEN** a linha é retirada e a evidência dela é expurgada

## MODIFIED Requirements

### Requirement: Instrumento sem cliente automatizado é pendência
Instrumento declarado `Manual` SHALL ter a pendência de validação manual derivada do
protocolo, e não gravada no resultado técnico. Ela MUST NOT ser registrada como termo não
encontrado. Instrumento `Automático` MUST NOT gerar linha nesse estatuto.

#### Scenario: Instrumento manual
- **WHEN** a tabela declara um instrumento `Manual`
- **THEN** a pendência de validação manual é derivada do protocolo para cada termo das
  facetas dele, nos idiomas do instrumento, e nenhuma linha manual é gravada no resultado
  técnico

#### Scenario: Instrumento automático
- **WHEN** a tabela declara um instrumento `Automático`
- **THEN** nenhuma linha dele nasce nem permanece pendente de validação manual sem decisão

### Requirement: Propriedades do instrumento lidas do protocolo
Sigla, modo, caminho e idiomas de cada instrumento SHALL ser lidos da sua linha na tabela. A
sigla MUST ser única e é o valor gravado no campo `instrumento` dos dois registros. Os
idiomas MUST estar entre os idiomas do quadro terminológico. Campo vazio reprova.

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

O que já foi consultado e registrado antes da interrupção SHALL ficar gravado no resultado
técnico e na evidência. A mensagem MUST nomear o instrumento, o termo, a condição encontrada
e quantos termos ficaram sem consulta.

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
Os caminhos e nomes dos dois registros da validação SHALL vir do `config.toml`:
`[dados] validacao`, para as decisões, e `[dados] consulta_terminologica`, para o resultado
técnico. No projeto, eles são `data/validacao_terminologica.toml` e
`data/consulta_terminologica.json`.

#### Scenario: Arquivo de decisões
- **WHEN** a configuração é a do projeto
- **THEN** o arquivo de decisões se chama `validacao_terminologica.toml`

#### Scenario: Resultado técnico
- **WHEN** a configuração é a do projeto
- **THEN** o resultado técnico se chama `consulta_terminologica.json`

#### Scenario: Grafia corrigida
- **WHEN** se procura `termologica` em `src/`, no `config.toml`, no README e nas skills
- **THEN** não há ocorrência

#### Scenario: Caminho alterado
- **WHEN** o pesquisador muda `[dados] validacao` ou `[dados] consulta_terminologica`
- **THEN** o comando seguinte usa o caminho novo, sem alteração de código, e o caminho
  antigo não é lido

### Requirement: Domínio da decisão do ReT
O campo `decisao_ReT` do arquivo de decisões SHALL admitir só `descritor`, `sinônimo ou
relacionado`, `termo livre` ou vazio, sem distinção de caixa. O vazio significa "sem
decisão". Valor fora do domínio MUST reprovar em `termos importar` e em `documentos
conferir`, nomeando o termo, a faceta, o idioma, o instrumento e o valor.

#### Scenario: Valor fora do domínio
- **WHEN** o arquivo de decisões traz `decisao_ReT = autorizado` para `ontology` (FCT1, en,
  unesco)
- **THEN** `termos importar` reprova, nomeando o termo, o instrumento e os valores admitidos

#### Scenario: Caixa diferente
- **WHEN** o arquivo de decisões traz `decisao_ReT = Descritor`
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
- **WHEN** o arquivo de decisões não existe
- **THEN** a linha esperada de todo termo é "Termo livre"

### Requirement: Autoteste prova o domínio e a regra da linha
O autoteste SHALL verificar, sobre arquivos de decisão em memória, o domínio de `decisao_ReT`
e a regra da linha esperada: precedência de `descritor` sobre `sinônimo ou relacionado`,
pendência manual e proposta da máquina levando a `livre`, e valor fora do domínio reprovado.
Caso não verificado MUST fazer o autoteste falhar.

#### Scenario: Precedência invertida
- **WHEN** o autoteste dá a um termo `sinônimo ou relacionado` num instrumento e `descritor`
  noutro, e a linha calculada não é `descritores`
- **THEN** o autoteste falha, nomeando o caso

### Requirement: Forma do termo no instrumento registrada
O resultado técnico SHALL ter o campo `forma_no_instrumento`, com `preferido`, `não
preferido` ou vazio. Ele MUST ser preenchido só com o que a resposta do serviço informa;
quando o serviço não distingue a forma, fica vazio, e a forma MUST NOT ser inferida.

#### Scenario: Serviço informa a forma
- **WHEN** a resposta identifica o termo encontrado como não preferido
- **THEN** `forma_no_instrumento` é `não preferido`

#### Scenario: Serviço não informa
- **WHEN** a resposta não distingue termo preferido de não preferido
- **THEN** `forma_no_instrumento` fica vazia, e `observacao_tecnica` diz que o serviço não
  informou a forma

### Requirement: Sugestão de similaridade registrada
O resultado técnico SHALL ter o campo `sugestao_similar`. Em linha consultada sem casamento
exato, ele MUST trazer a sugestão do serviço ou a indicação de que não houve sugestão, e
MUST NOT ficar vazio. Em linha com casamento exato, fica vazio.

#### Scenario: Casamento exato
- **WHEN** `ontology` casa exatamente com um descritor do instrumento
- **THEN** a consulta por prefixo não é feita, e `sugestao_similar` fica vazia

### Requirement: Autoteste prova a similaridade e a reabertura correspondente
O autoteste SHALL verificar, sobre respostas e registros em memória, os desfechos da
consulta por prefixo (item único, item único por entrada não preferida, vários itens, sem
item) e a reabertura da linha não localizada sem `sugestao_similar`. Caso não
verificado MUST fazer o autoteste falhar.

#### Scenario: Reabertura desligada
- **WHEN** a regra deixa de reabrir a linha não localizada sem `sugestao_similar`
- **THEN** o autoteste falha, nomeando o caso
