# leitura-do-protocolo Specification

## Purpose

Ler o protocolo de estratégia de pesquisa como fonte única de verdade, com valores padrão num
arquivo de configuração que o protocolo sobrescreve, e conferir a coerência interna do
documento sem fixar valores esperados no código.

## Requirements

### Requirement: Nenhum parâmetro fixado no código
O código de `src/` MUST NOT conter valor de parâmetro do projeto. São parâmetros:

- composição e papel das expressões;
- âncoras, recorte e limiares;
- dimensões de critério;
- instrumentos (sigla, modo, caminho, idiomas, facetas);
- bases (sigla, procedimento de busca);
- idiomas do quadro;
- caminhos e nomes dos arquivos de dados, de entrada e de saída;
- campos da planilha;
- o caminho do próprio protocolo.

Todo parâmetro SHALL vir do protocolo, do procedimento de busca da base ou do `config.toml` na raiz. O
autoteste MUST NOT ser exceção. As cópias defeituosas que ele produz SHALL ser geradas a
partir da estrutura lida do protocolo corrente (por exemplo, "a última semente lida" ou "a
primeira base da tabela"), e não de literais do texto vigente.

Docstrings e mensagens MUST NOT descrever a composição, as siglas ou os valores vigentes
como se fossem do código.

#### Scenario: Busca por valor fixado
- **WHEN** se procura em `src/` por constante de parâmetro (ex.: `0.80`, `2017`, `"EB4"`,
  `"tbci"`, `"wos"`, `"pt"`, `"SE10"`, `"registro_execucao.json"`)
- **THEN** não há ocorrência, inclusive no autoteste

#### Scenario: Emenda legítima não quebra o autoteste
- **WHEN** o protocolo ganha uma semente nova, troca a sigla de uma base de forma coerente
  com os procedimentos de busca ou altera a faixa de sensibilidade dentro do válido
- **THEN** `documentos conferir` passa, e `projeto autoteste` executa os mesmos grupos de casos, sem caso
  "mutação não aplicada"

### Requirement: Protocolo sobrescreve o padrão da configuração
`config.toml` SHALL conter valor padrão para todo parâmetro **não estrutural**. Quando o
protocolo declara o parâmetro, o valor do protocolo SHALL prevalecer; quando não declara,
vale o padrão. Parâmetro estrutural não tem padrão (ver "Parâmetros estruturais só do
protocolo").

#### Scenario: Protocolo declara o parâmetro
- **WHEN** a regra de ajuste do protocolo declara 80% e `config.toml` traz outro padrão
- **THEN** o leitor usa 80%

#### Scenario: Protocolo não declara o parâmetro
- **WHEN** o protocolo não declara o limiar de divergência da fidelidade
- **THEN** o leitor usa o padrão de `config.toml`

#### Scenario: Declaração ilegível não cai no padrão
- **WHEN** o protocolo tem o trecho do parâmetro mas o valor não é legível
- **THEN** a conferência reprova, nomeando o parâmetro, sem usar o padrão

#### Scenario: Configuração ausente ou incompleta
- **WHEN** `config.toml` não existe, não é TOML válido ou não tem um parâmetro não estrutural
- **THEN** o script termina com erro que nomeia o arquivo e o parâmetro

### Requirement: Arquivo do protocolo é parametrizado
O caminho do documento do protocolo a ser lido SHALL vir de `config.toml`. Por ser o que
localiza o protocolo, esse parâmetro MUST NOT ser sobrescrito pelo protocolo. O caminho do
próprio `config.toml` é o único fixado: a raiz do projeto.

#### Scenario: Outro arquivo de protocolo
- **WHEN** `config.toml` aponta para outro arquivo de protocolo
- **THEN** todos os subcomandos leem esse arquivo, e `configuracao mostrar` exibe o caminho em uso

#### Scenario: Protocolo inexistente
- **WHEN** o caminho configurado não existe
- **THEN** o subcomando termina com o código CONFIGURACAO e com erro que nomeia o caminho
  e a chave do `config.toml`

### Requirement: Origem de cada parâmetro é visível
`--mostrar` SHALL exibir, para cada parâmetro, o valor em uso e a sua origem (protocolo,
procedimento de busca da base ou padrão da configuração).

#### Scenario: Parâmetro vindo do padrão
- **WHEN** o limiar de divergência vem de `config.toml`
- **THEN** `--mostrar` o exibe com origem "padrão (config.toml)"

#### Scenario: Parâmetro estrutural
- **WHEN** `--mostrar` exibe a composição das expressões, os instrumentos, as bases ou os
  idiomas
- **THEN** a origem exibida é sempre o protocolo, e a forma de execução de cada base tem
  origem no procedimento de busca

### Requirement: Conferência verifica coerência interna
`--conferir` SHALL reprovar contradições internas: termo de STR ausente do quadro da faceta;
STR diferente da STR esperada calculada do quadro ("STR é a união do quadro da faceta", em
`geracao-das-strings`); termo do quadro em mais de uma faceta; expressão sem as âncoras;
executada que não seja a união das específicas; semente sem base ou com base fora da tabela
de bases; dimensão de critério em uso não declarada no protocolo; faixa de sensibilidade com
inferior ≥ superior. A sonda ser a conjunção das âncoras é garantida pela identificação
("Executada e sonda identificadas pela composição") e não é conferida de novo.

#### Scenario: Termo da string fora do quadro
- **WHEN** uma STR contém um termo que não consta do quadro da sua faceta
- **THEN** `--conferir` reprova, nomeando a faceta e o termo

#### Scenario: STR divergente da gerada
- **WHEN** o quadro de FCT3 deixou de ter `practice` e a STR3 do protocolo ainda o contém, ou
  o quadro ganhou um termo que a STR não tem
- **THEN** `--conferir` reprova, nomeando a faceta, os termos a mais e a menos, e
  `strings gerar` como correção

#### Scenario: Subsumido presente na STR
- **WHEN** a STR1 contém `"ontology"` e `"domain ontology"`
- **THEN** `--conferir` reprova a STR1 como divergente da gerada, nomeando `domain ontology`
  como subsumido por `ontology`

#### Scenario: Termo em duas facetas do quadro
- **WHEN** `nível de ensino` consta dos quadros de FCT2 e FCT4
- **THEN** `--conferir` reprova, nomeando o termo e as duas facetas

#### Scenario: Mesma forma em idiomas da mesma faceta
- **WHEN** `contexto de uso` consta das colunas pt e es do quadro de FCT4
- **THEN** `--conferir` não reprova por atribuição única

#### Scenario: Dimensão de critério com grafia do protocolo
- **WHEN** a lista de dimensões em uso tem "Idioma" e o protocolo declara CE3 com "Idioma"
- **THEN** `--conferir` não reprova por dimensão de critério

#### Scenario: Distribuição das sementes não é declarada em prosa
- **WHEN** o conjunto-semente está só no arquivo de sementes, sem parágrafo de incidências
  no protocolo
- **THEN** `--conferir` não reprova por distribuição; a distribuição por base é calculada do
  campo `bases` do arquivo e exibida

### Requirement: Autoteste prova que cada conferência reprova
`projeto autoteste` SHALL injetar, numa cópia em memória, ao menos um defeito por:

- conferência de coerência;
- regra de precedência;
- parâmetro estrutural, ausente e com valor inválido;
- elemento exigido da gramática do protocolo.

Cada defeito SHALL ser reprovado com o código esperado: REPROVADO para coerência,
PROTOCOLO_ILEGIVEL para forma e CONFIGURACAO para configuração. Defeito não detectado, ou
detectado com outro código, MUST fazer o autoteste falhar.

#### Scenario: Conferência que não reprova
- **WHEN** um defeito injetado não é detectado pela conferência correspondente
- **THEN** `projeto autoteste` falha, nomeando o defeito

#### Scenario: Parâmetro estrutural ausente
- **WHEN** o autoteste retira de uma cópia do protocolo a coluna `Sigla` da tabela de bases
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL; leitura que caia em valor padrão faz o
  autoteste falhar

#### Scenario: Código trocado
- **WHEN** um defeito de forma é reprovado com REPROVADO em vez de PROTOCOLO_ILEGIVEL
- **THEN** `projeto autoteste` falha, nomeando o defeito e os dois códigos

### Requirement: Somente biblioteca padrão
Os scripts SHALL executar só com a biblioteca padrão do Python 3.11 ou superior; a
configuração MUST ser lida sem pacote externo.

#### Scenario: Ambiente sem pacotes extras
- **WHEN** os scripts rodam num Python 3 limpo, sem pacotes instalados
- **THEN** a leitura de `config.toml` e todas as conferências funcionam

### Requirement: Scripts sem referência a versão do protocolo
Mensagens, comentários e nomes do código MUST NOT referir versão ou emenda específica do
protocolo; o histórico de versões vive em `data/historico.md`.

#### Scenario: Busca por referência de versão
- **WHEN** se procura por `v1`, `v2`, `_V2` ou "emenda v2" em `src/`
- **THEN** não há ocorrência

### Requirement: Papéis das expressões expostos uma única vez
O leitor SHALL expor os papéis das expressões — âncoras, específicas, gerais, executada e
sonda — calculados a partir da composição e das âncoras lidas, e a conferência de coerência
e a derivação MUST usar esse mesmo cálculo.

#### Scenario: Papéis do protocolo atual
- **WHEN** o protocolo atual é lido
- **THEN** as específicas são EB2 e EB3, a geral é EB1, a executada é EB4 e a sonda é EB5

### Requirement: Resumo do autoteste distingue caso não executado
O resumo do autoteste SHALL informar à parte os casos não executados e o motivo, e MUST NOT
contá-los como casos com o resultado esperado.

#### Scenario: Arquivos alimentados ausentes
- **WHEN** `--autoteste` roda sem os arquivos alimentados de `data/`
- **THEN** o resumo diz que os casos desses arquivos não foram executados e por quê, em vez
  de contá-los como zero casos aprovados

### Requirement: Composição das expressões na forma estrita
A coluna "Expressão de busca" da tabela de expressões SHALL ser lida na forma estrita
`STRn AND STRn AND (STRn OR STRn)`: `AND` em maiúsculas é a única conjunção e `OR`, em
maiúsculas, só aparece dentro de parênteses. Qualquer outra forma MUST reprovar a leitura
com mensagem que nomeie a expressão.

#### Scenario: Forma estrita
- **WHEN** a expressão é `STR1 AND STR2 AND (STR3 OR STR4)`
- **THEN** a composição lida tem os grupos `[STR1]`, `[STR2]` e `[STR3, STR4]`

#### Scenario: Conjunção fora da forma estrita
- **WHEN** a expressão usa `+` ou `and` como conjunção
- **THEN** a leitura reprova nomeando a expressão e a forma esperada

### Requirement: Cabeçalho da tabela de expressões conferido
O cabeçalho da tabela "Expressões de busca" SHALL coincidir exatamente, na ordem, com as
colunas declaradas na gramática: `ID`, `Expressão de busca` e `Função protocolar`.
Cabeçalho diferente MUST reprovar a leitura com PROTOCOLO_ILEGIVEL e com mensagem que
mostre o cabeçalho lido e o esperado. A coluna "Função protocolar" é texto livre: o leitor
só extrai dela as referências `(Nn)` às notas explicativas.

#### Scenario: Coluna renomeada
- **WHEN** a coluna "Expressão de busca" aparece como "Combinação de Strings"
- **THEN** a leitura reprova, mostrando o cabeçalho lido e o esperado

#### Scenario: Cabeçalho antigo
- **WHEN** a tabela traz `ID expressão | Natureza | Expressão de busca | Detalhamento`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, mostrando o cabeçalho esperado

### Requirement: Resultado parcial do autoteste declarado
Quando houver caso não executado, o autoteste SHALL declarar que o resultado é parcial e
terminar com o código PARCIAL, desde que nenhum caso executado tenha falhado. Havendo
falha, o código é REPROVADO, e a mensagem informa também os casos não executados.

#### Scenario: Arquivos alimentados ausentes
- **WHEN** `projeto autoteste` termina sem falha e com casos não executados
- **THEN** a última mensagem diz que o autoteste é parcial, quantos casos não rodaram e por
  quê, e o código de saída é PARCIAL

#### Scenario: Falha com casos não executados
- **WHEN** um caso executado falha e há casos não executados
- **THEN** o código de saída é REPROVADO, e a mensagem informa os casos não executados

### Requirement: Parâmetros estruturais só do protocolo
Composição das expressões, facetas e âncoras, instrumentos, bases e idiomas do quadro SHALL
ser lidos só do protocolo, sem padrão. O conjunto-semente SHALL ser lido só do arquivo de
sementes, localizado por `[documentos] sementes` do `config.toml`, sem padrão. Ausência ou
valor inválido MUST reprovar a leitura, nomeando tabela ou arquivo, linha ou semente e
campo. `config.toml` que ainda traga `padroes.composicao`, `padroes.executada`,
`padroes.sonda`, `padroes.ancoras`, `[expressoes]`, `cores`, `fichas`, `instrumentos` ou
`idiomas` MUST reprovar, para que não haja segunda fonte.

#### Scenario: Tabela estrutural ausente
- **WHEN** o protocolo não tem a tabela "Bases de dados"
- **THEN** a leitura reprova nomeando a tabela, e nenhum valor da configuração é usado

#### Scenario: Chave retirada ainda presente na configuração
- **WHEN** `config.toml` traz a seção `[fichas.wos]`
- **THEN** o script termina com erro que nomeia a chave e diz que ela vem do protocolo

#### Scenario: Chave de natureza ainda presente
- **WHEN** `config.toml` traz `[expressoes] natureza_executada` ou `padroes.ancoras`
- **THEN** o script termina com erro de configuração que nomeia a chave

### Requirement: Idiomas lidos do cabeçalho do quadro
Cada tabela do quadro terminológico SHALL ter cabeçalho `| FCTn | idioma | idioma | ... |`; o
idioma de cada coluna é o nome no cabeçalho, não a posição. Os idiomas do projeto SHALL ser
os do cabeçalho, e o conjunto MUST ser o mesmo em todas as tabelas, sem repetição nem célula
vazia.

#### Scenario: Colunas em outra ordem
- **WHEN** o cabeçalho de FCT2 é `| FCT2 | en | pt | es |`
- **THEN** os termos da coluna `pt` de FCT2 são lidos como português

#### Scenario: Idiomas diferentes entre tabelas
- **WHEN** a tabela de FCT4 declara `pt | en` e as demais `pt | en | es`
- **THEN** a leitura reprova, nomeando a faceta e os idiomas divergentes

### Requirement: Bases lidas da tabela do protocolo
As bases SHALL ser lidas da tabela "Bases de dados": identificador `BDn`, sigla e nome. Sigla
e identificador MUST ser únicos. O procedimento de busca de cada base SHALL ser localizada pela sigla, no
padrão de caminho do `config.toml`; procedimento de busca inexistente MUST reprovar, nomeando base e caminho.

#### Scenario: Procedimento de busca da sigla não existe
- **WHEN** o padrão é `docs/procedimentos_busca_{sigla}.md` e não existe
  `docs/procedimentos_busca_eric.md`
- **THEN** a leitura reprova, nomeando BD3, a sigla `eric` e o caminho procurado

#### Scenario: Padrão sem a sigla
- **WHEN** o padrão de caminho do `config.toml` não contém `{sigla}`
- **THEN** o script termina com erro de configuração que nomeia a chave

#### Scenario: Sigla repetida
- **WHEN** duas linhas da tabela têm a sigla `eric`
- **THEN** a leitura reprova, nomeando a sigla

### Requirement: Conjunto de validação não vazio

O conjunto-semente SHALL ter ao menos uma semente de validação. Conjunto sem semente de
validação MUST reprovar `--conferir`, porque a aderência que decide a passagem não teria
denominador.

#### Scenario: Só sementes de desenvolvimento
- **WHEN** todas as sementes declaram `desenvolvimento`
- **THEN** `--conferir` reprova, nomeando a falta de semente de validação

#### Scenario: Autoteste do conjunto de validação vazio
- **WHEN** o autoteste troca, numa cópia, o papel de todas as sementes de validação para
  `desenvolvimento`
- **THEN** a conferência reprova pelo motivo esperado

### Requirement: Critério de elegibilidade tem justificativa

Todo critério da tabela de critérios de elegibilidade SHALL ter a coluna "Justificativa"
preenchida. Célula vazia, ou só com espaço ou traço, MUST reprovar `--conferir`, nomeando o
ID do critério.

#### Scenario: Critério sem justificativa

- **WHEN** a linha do CE6 tem a coluna "Justificativa" vazia
- **THEN** `--conferir` reprova, nomeando CE6

#### Scenario: Todos os critérios justificados

- **WHEN** todas as linhas da tabela de critérios têm justificativa
- **THEN** essa dimensão não reprova

#### Scenario: Justificativa reduzida a traço

- **WHEN** a justificativa de um critério é `-`
- **THEN** `--conferir` reprova, nomeando o critério

### Requirement: Autoteste prova a reprovação do critério sem justificativa

O autoteste SHALL esvaziar, numa cópia em memória, a justificativa de um critério e exigir
que `--conferir` reprove pelo motivo esperado, nomeando o critério.

#### Scenario: Defeito injetado

- **WHEN** o autoteste esvazia a justificativa de um critério na cópia
- **THEN** a conferência reprova nomeando aquele critério, e o caso conta como resultado
  esperado

### Requirement: Facetas lidas da tabela
As facetas SHALL ser lidas da tabela "Facetas da questão de revisão", com cabeçalho exato
`Id faceta | Faceta | Âncora obrigatória`. O identificador SHALL ter a forma `FCTn`, em
sequência a partir de FCT1, e o nome MUST NOT ser vazio. A coluna "Âncora obrigatória"
SHALL admitir só `Sim` ou `Não`, sem distinção de caixa. As âncoras são as facetas
marcadas `Sim`, na ordem da tabela. O leitor MUST NOT extrair nem exigir cor, e hífen
dentro do nome pertence ao nome.

#### Scenario: Protocolo atual
- **WHEN** a tabela marca FCT1 e FCT2 com `Sim` e FCT3 e FCT4 com `Não`
- **THEN** as âncoras lidas são FCT1 e FCT2, e `configuracao mostrar` as exibe com origem no protocolo

#### Scenario: Nome com hífen
- **WHEN** o nome de FCT3 é "Práticas do processo de ensino-aprendizagem"
- **THEN** o nome lido é o texto inteiro da célula

### Requirement: Tabela de facetas fora da forma reprova
Valor de âncora fora do domínio, nome vazio, identificador fora da forma ou fora de
sequência e tabela sem nenhuma âncora MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a
faceta ou a tabela.

#### Scenario: Âncora fora do domínio
- **WHEN** a célula "Âncora obrigatória" de FCT2 traz `Talvez`
- **THEN** a leitura reprova, nomeando FCT2 e os valores admitidos

#### Scenario: Nenhuma âncora
- **WHEN** todas as facetas estão marcadas `Não`
- **THEN** a leitura reprova, nomeando a tabela de facetas

### Requirement: Executada e sonda identificadas pela composição
O leitor SHALL identificar a executada e a sonda a partir da composição lida e das
âncoras, sem texto da tabela e sem padrão do `config.toml`:

- a executada é a única expressão com um grupo de mais de uma STR;
- a sonda é a única expressão cujos grupos são exatamente as STR das facetas-âncora.

Nenhum candidato, ou mais de um, MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a tabela
de expressões e os candidatos. `configuracao mostrar` SHALL exibir a executada e a sonda com origem
"protocolo (composição)".

#### Scenario: Protocolo atual
- **WHEN** a composição é EB1 a EB5, com EB4 = `STR1 AND STR2 AND (STR3 OR STR4)` e
  EB5 = `STR1 AND STR2`, e as âncoras são FCT1 e FCT2
- **THEN** a executada é EB4 e a sonda é EB5

#### Scenario: Duas expressões com OR
- **WHEN** EB1 passa a `STR1 AND (STR2 OR STR3)`
- **THEN** a leitura reprova, nomeando EB1 e EB4 como candidatas a executada

#### Scenario: Duas sondas
- **WHEN** uma cópia acrescenta EB6 = `STR1 AND STR2`
- **THEN** a leitura reprova, nomeando EB5 e EB6 como candidatas a sonda

### Requirement: Notas explicativas das expressões
A seção "Expressões de busca" SHALL admitir a subseção opcional `### Notas explicativas`,
com itens `- Nn — <texto>`. A referência `(Nn)` na coluna "Função protocolar" sem a nota
correspondente MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a expressão e a nota. Nota
não citada não reprova.

#### Scenario: Nota citada inexistente
- **WHEN** EB2 cita `(N7)` e não há nota N7
- **THEN** a leitura reprova, nomeando EB2 e N7

### Requirement: Faixa de sensibilidade lida da nota da executada
A faixa de sensibilidade SHALL ser lida das notas citadas na linha da executada, nos
padrões `< N%` e `> M%`. Sem nenhum dos dois limites, vale `padroes.sensibilidade`; com só
um deles, a leitura reprova, nomeando a nota e o limite que falta.

#### Scenario: Faixa da nota da executada
- **WHEN** EB4 cita `(N3)` e N3 traz "< 5%" e "> 15%"
- **THEN** a faixa lida é 5% a 15%, com origem no protocolo, e o trecho "5%–15%" não altera
  a leitura

#### Scenario: Limite só inferior
- **WHEN** a nota da executada traz "< 5%" e nenhum limite superior
- **THEN** a leitura reprova, nomeando a nota e o limite superior ausente

#### Scenario: Sem faixa declarada
- **WHEN** as notas citadas pela executada não trazem `<` nem `>` com percentual
- **THEN** vale `padroes.sensibilidade`, e `configuracao mostrar` exibe a origem "padrão (config.toml)"

### Requirement: Conjunto-semente lido do arquivo de sementes
O conjunto-semente SHALL ser lido do arquivo TOML localizado por `[documentos] sementes`,
uma tabela `[[sementes]]` por estudo, com os campos do esquema estruturado declarado na
gramática:

- bibliográficos: `id` (`SEn`, único e em sequência a partir de SE1), `autores` (lista não vazia), `ano` (inteiro),
  `titulo`, `veiculo`, e os opcionais `volume`, `numero`, `paginas` e `doi`;
- aferição: `bases` (siglas que indexam a semente), `facetas` (opcional, `FCTn` informadas
  pelo pesquisador) e `papel`;
- conferência, opcionais: `verificacao`, `tipo`, `alinhamento`, `nota`,
  `veiculo_conferido` e `eric`;
- `observacoes`, opcional: o que a referência traz e não cabe em outro campo.

Autoria, ano, título e DOI MUST ser lidos dos campos, sem extração por padrão de texto, e
nenhum outro arquivo SHALL guardar dado de semente.

#### Scenario: Arquivo atual
- **WHEN** o arquivo de sementes tem as 10 sementes de SE1 a SE10, com os campos do
  esquema estruturado
- **THEN** a leitura aprova, e a distribuição por base e por papel exibida por `configuracao mostrar` é
  a mesma exibida antes da troca do esquema intermediário pelo estruturado

#### Scenario: Título com ponto
- **WHEN** o `titulo` de uma semente contém um ponto seguido de maiúscula
- **THEN** o título lido é o campo inteiro

#### Scenario: Semente sem DOI
- **WHEN** uma semente não tem `doi`
- **THEN** a leitura aprova, e `projeto pendencias` relata o DOI ausente

#### Scenario: Distribuição calculada
- **WHEN** o arquivo é lido
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas do campo `bases`, e a distribuição por papel, do campo `papel`

### Requirement: Arquivo de sementes fora do esquema reprova
Arquivo de sementes ausente MUST terminar com CONFIGURACAO, nomeando a chave e o caminho.
MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo: TOML inválido; campo
obrigatório ausente ou de tipo errado; campo desconhecido; `id` fora da forma `SEn`,
repetido ou fora da sequência a partir de SE1; `doi` fora da forma `10.x/…`; base fora da tabela de bases, com outra grafia ou
repetida; faceta fora da tabela de facetas ou repetida; `papel` fora do domínio.

#### Scenario: Lacuna na numeração
- **WHEN** o arquivo tem SE1, SE2 e SE4, sem SE3
- **THEN** a leitura reprova, nomeando SE4 e o `id` esperado, SE3

#### Scenario: Papel fora do domínio
- **WHEN** uma semente traz `papel = "teste"`
- **THEN** a leitura reprova, nomeando a semente e os valores admitidos

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Faceta inexistente
- **WHEN** a semente SE7 traz `facetas = ["FCT9"]` e a tabela de facetas vai até FCT4
- **THEN** a leitura reprova, nomeando SE7 e a faceta

#### Scenario: Campo desconhecido
- **WHEN** uma semente traz o campo `titlo`, o campo retirado `escopo` ou o campo
  `semente` do esquema intermediário
- **THEN** a leitura reprova, nomeando a semente e o campo

#### Scenario: Arquivo ausente
- **WHEN** `[documentos] sementes` aponta um arquivo que não existe
- **THEN** o subcomando termina com CONFIGURACAO, nomeando a chave e o caminho, e nenhuma
  semente é presumida

### Requirement: Termos do quadro separados por vírgula
Cada célula de idioma do quadro terminológico SHALL ter os termos separados por vírgula.
Célula com o separador antigo (`\- ` no início ou depois de espaço) MUST reprovar com
PROTOCOLO_ILEGIVEL, nomeando a faceta, a camada e o idioma. Hífen dentro de palavra,
escapado ou não, pertence ao termo.

#### Scenario: Separador antigo
- **WHEN** a célula do núcleo em `pt` de FCT1 traz `\- representação do conhecimento \- ontologia`
- **THEN** a leitura reprova, nomeando FCT1, a camada e `pt`, e dizendo que o separador é a
  vírgula

#### Scenario: Quadro atual
- **WHEN** as células trazem `termo, termo, termo`
- **THEN** cada termo é lido em separado, e o quadro de cada faceta tem mais formas que
  células

### Requirement: Dado ou juízo pendente relatado, sem reprovar
`projeto pendencias` SHALL relatar, nomeando a semente, sem reprovar a leitura:

- `doi` ausente;
- `facetas` vazia ou ausente;
- semente de validação com `facetas` preenchida que não inclui nenhuma faceta marcada
  `Sim` na coluna "Âncora obrigatória" da tabela de facetas. O caso fica como pendência
  até o pesquisador decidir a regra. Com `facetas` vazia ou ausente, só se relata
  "facetas a informar": a falta de âncora decorre dela e não é relatada à parte;
- `tipo` ou `alinhamento` vazios.

#### Scenario: DOI a obter
- **WHEN** a semente SE6 não traz `doi`
- **THEN** a leitura aprova, e `projeto pendencias` relata SE6 com DOI ausente

#### Scenario: Facetas a informar
- **WHEN** a semente SE3 não traz `facetas`
- **THEN** a leitura aprova, e `projeto pendencias` relata SE3 com facetas a informar

#### Scenario: Validação sem âncora
- **WHEN** a semente de validação SE5 traz `facetas = ["FCT3"]`, e FCT1 e FCT2 são as
  âncoras
- **THEN** a leitura aprova, e `projeto pendencias` relata SE5 sem faceta âncora

#### Scenario: Validação sem facetas
- **WHEN** a semente de validação SE3 não traz `facetas`
- **THEN** `projeto pendencias` relata SE3 com facetas a informar, e não relata SE3 sem faceta
  âncora

### Requirement: Semente retirada não deixa resto
Semente retirada SHALL sair do arquivo, das saídas regeneradas e da evidência bruta.
`dados conferir` MUST reprovar arquivo da subpasta `referencias/` de `[dados] evidencia`
(hoje `data/evidencia/referencias/`) nomeado com um `SEn` que não está no arquivo de
sementes, nomeando o arquivo. As outras subpastas da evidência MUST NOT ser conferidas
por essa regra.

#### Scenario: Evidência de semente retirada
- **WHEN** SE10 é retirada do arquivo e `SE10_crossref.json` continua em
  `data/evidencia/referencias/`
- **THEN** `dados conferir` reprova, nomeando `SE10_crossref.json`

#### Scenario: Planilha regenerada
- **WHEN** SE10 é retirada e `aderencia planilhar` é executado
- **THEN** `semente_aderencia.csv` não traz linha de SE10

### Requirement: Referência exibida a partir dos campos
`configuracao mostrar` SHALL exibir cada semente como referência legível, montada dos campos na ordem
autores, ano, título, veículo, volume, número, páginas e DOI, omitindo o campo vazio. A
referência exibida MUST NOT ser gravada em arquivo nem no protocolo.

#### Scenario: Campo opcional vazio
- **WHEN** uma semente não tem `paginas`
- **THEN** a referência exibida não traz marcador de páginas

### Requirement: Autoteste prova a reprovação do esquema estruturado
O autoteste SHALL injetar numa cópia do arquivo de sementes, a partir das sementes lidas,
cada um destes defeitos e exigir PROTOCOLO_ILEGIVEL: `ano` como texto, `autores` vazia,
`doi` fora da forma, faceta fora da tabela, faceta repetida, lacuna na numeração dos `id` e
o campo `semente` do esquema intermediário. O autoteste SHALL também exigir que
`dados conferir` reprove a evidência de semente inexistente.

#### Scenario: DOI ausente não reprova
- **WHEN** o autoteste retira o `doi` de uma semente numa cópia
- **THEN** a cópia é aprovada e `projeto pendencias` relata a semente; se a cópia reprovar, o
  autoteste falha

#### Scenario: Defeito não detectado
- **WHEN** a cópia com o campo `semente` é aprovada
- **THEN** o autoteste falha, nomeando o defeito
