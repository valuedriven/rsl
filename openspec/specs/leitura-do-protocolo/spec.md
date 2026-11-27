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
`--conferir` SHALL reprovar contradições internas: termo de STR ausente das linhas "Termo
livre" e "Descritores correspondentes" do CT da faceta;
STR diferente da STR esperada calculada do quadro ("STR é a união do quadro da faceta", em
`geracao-das-strings`); termo do quadro em mais de uma faceta; expressão sem as âncoras;
executada que não seja a união das específicas; semente sem base ou com base fora da tabela
de bases; dimensão de critério em uso não declarada no protocolo; faixa de sensibilidade com
inferior ≥ superior. A sonda ser a conjunção das âncoras é garantida pela identificação
("Executada e sonda identificadas pela composição") e não é conferida de novo.

#### Scenario: Termo da string fora do quadro
- **WHEN** uma STR contém um termo que não consta das linhas "Termo livre" e "Descritores
  correspondentes" do CT da sua faceta
- **THEN** `--conferir` reprova, nomeando a faceta e o termo

#### Scenario: STR divergente da gerada
- **WHEN** o CT3 deixou de ter `practice` e a STR3 do protocolo ainda o contém, ou o CT3
  ganhou um termo que a STR não tem
- **THEN** `--conferir` reprova, nomeando a faceta, os termos a mais e a menos, e
  `strings gerar` como correção

#### Scenario: Subsumido presente na STR
- **WHEN** a STR1 contém `"ontology"` e `"domain ontology"`
- **THEN** `--conferir` reprova a STR1 como divergente da gerada, nomeando `domain ontology`
  como subsumido por `ontology`

#### Scenario: Termo em duas facetas do quadro
- **WHEN** `nível de ensino` consta do CT2 e do CT4
- **THEN** `--conferir` reprova, nomeando o termo e as duas facetas

#### Scenario: Mesma forma em idiomas da mesma faceta
- **WHEN** `contexto de uso` consta das colunas pt e es do CT4
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
falha, o código é REPROVADO, e a mensagem informa também os casos não executados. O número
de casos não executados SHALL vir de contagem feita pelo próprio autoteste (um caso trocado
pelo aviso, ou número calculado dos dados); o bloco que deixa de rodar por retorno
antecipado SHALL ser relatado como bloco inteiro, de tamanho não contado, e MUST NOT levar
número escrito à mão.

#### Scenario: Arquivos alimentados ausentes
- **WHEN** `projeto autoteste` termina sem falha e com casos não executados
- **THEN** a última mensagem diz que o autoteste é parcial, quantos casos não rodaram e por
  quê, e o código de saída é PARCIAL

#### Scenario: Falha com casos não executados
- **WHEN** um caso executado falha e há casos não executados
- **THEN** o código de saída é REPROVADO, e a mensagem informa os casos não executados

#### Scenario: Bloco não executado
- **WHEN** um grupo encerra antes dos seus casos por falta de dado de ensaio
- **THEN** o relato diz que o restante do bloco não foi executado e por quê, sem número de
  casos, e o código de saída é PARCIAL

#### Scenario: Contagem à mão recusada
- **WHEN** um grupo chama o aviso de casos não executados no formato antigo, com o número
  como primeiro argumento
- **THEN** a chamada é recusada no próprio autoteste, em vez de relatar um número que não
  foi contado

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
Cada tabela do controle terminológico SHALL ter cabeçalho `| Termo | idioma | idioma | ... |`.
A primeira célula é a coluna dos rótulos de linha e MUST ser `Termo`, sem ênfase nem espaços
nas pontas; outra primeira célula MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando o CT. O idioma de cada coluna é o
nome no cabeçalho, e não a posição. Os idiomas do projeto SHALL ser os do cabeçalho, e o
conjunto MUST ser o mesmo em todas as tabelas, sem repetição nem célula vazia.

#### Scenario: Colunas em outra ordem
- **WHEN** o cabeçalho do CT2 é `| | en | pt | es |`
- **THEN** os termos da coluna `pt` do CT2 são lidos como português

#### Scenario: Primeira célula fora da forma
- **WHEN** o cabeçalho do CT1 é `| Linha | pt | en | es |`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando CT1 e a forma
  `| Termo | idioma | … |`

#### Scenario: Idiomas diferentes entre tabelas
- **WHEN** o CT4 declara `pt | en` e os demais `pt | en | es`
- **THEN** a leitura reprova, nomeando a faceta e os idiomas divergentes

### Requirement: Bases lidas da tabela do protocolo
As bases SHALL ser lidas da tabela "Bases de dados": identificador `BDn`, sigla e nome. Sigla
e identificador MUST ser únicos. A fonte do procedimento de busca de cada base SHALL ser
localizada pela sigla, no padrão `[documentos] procedimento_fonte` do `config.toml`. Fonte
inexistente MUST reprovar, nomeando a base e o caminho. O procedimento de busca gerado SHALL
ser gravado no padrão `[documentos] procedimento`. A ausência do procedimento gerado MUST
reprovar `documentos conferir` só naquela base, com `procedimentos gerar <sigla> --gravar`
como correção, e MUST NOT impedir a leitura da fonte.

#### Scenario: Procedimento de busca da sigla não existe
- **WHEN** o padrão é `docs/procedimentos/{sigla}` e não existe
  `docs/procedimentos/eric/procedimento.toml`
- **THEN** a leitura reprova, nomeando BD3, a sigla `eric` e o caminho procurado

#### Scenario: Procedimento ainda não gerado
- **WHEN** a fonte da ERIC existe e `docs/procedimentos_busca_eric.md` não existe
- **THEN** `documentos conferir` reprova só a ERIC, indicando `procedimentos gerar eric
  --gravar`

#### Scenario: Padrão sem a sigla
- **WHEN** `[documentos] procedimento` ou `[documentos] procedimento_fonte` não contém
  `{sigla}`
- **THEN** o script termina com erro de configuração que nomeia a chave

#### Scenario: Sigla repetida
- **WHEN** duas linhas da tabela têm a sigla `eric`
- **THEN** a leitura reprova, nomeando a sigla

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

### Requirement: Termos do quadro separados por vírgula
Cada célula de idioma do quadro terminológico SHALL ter os termos separados por vírgula.
Célula com o separador antigo (`\- ` no início ou depois de espaço) MUST reprovar com
PROTOCOLO_ILEGIVEL, nomeando a faceta, a linha e o idioma. Hífen dentro de palavra,
escapado ou não, pertence ao termo.

#### Scenario: Separador antigo
- **WHEN** a célula "Termo livre" em `pt` do CT1 traz `\- representação do conhecimento \- ontologia`
- **THEN** a leitura reprova, nomeando FCT1, a linha e `pt`, e dizendo que o separador é a
  vírgula

#### Scenario: Quadro atual
- **WHEN** as células trazem `termo, termo, termo`
- **THEN** cada termo é lido em separado, e o quadro de cada faceta tem mais formas que
  células

### Requirement: Referência exibida a partir dos campos
`configuracao mostrar` SHALL exibir cada semente como referência legível, montada dos campos na ordem
autores, ano, título, veículo, volume, número, páginas e DOI, omitindo o campo vazio. A
referência exibida MUST NOT ser gravada em arquivo nem no protocolo.

#### Scenario: Campo opcional vazio
- **WHEN** uma semente não tem `paginas`
- **THEN** a referência exibida não traz marcador de páginas

### Requirement: Tabela do controle terminológico identificada pelo título
Cada tabela da seção "Controle terminológico" SHALL ser precedida de um título de nível 3
na forma `CTn (FCTn)`, com uma única faceta e com o número do CT igual ao da faceta. Deve
haver uma tabela por faceta da tabela de facetas. Título fora da forma, número divergente,
mais de uma faceta, faceta inexistente, CT repetido ou tabela sem título MUST reprovar com
PROTOCOLO_ILEGIVEL.

#### Scenario: Forma vigente
- **WHEN** a seção traz `### CT1 (FCT1)` a `### CT4 (FCT4)`, cada um com a sua tabela
- **THEN** a leitura atribui cada tabela à faceta do parêntese

#### Scenario: Número divergente
- **WHEN** a seção traz `### CT2 (FCT3)`
- **THEN** a leitura reprova, nomeando CT2 e FCT3

#### Scenario: Duas facetas no mesmo CT
- **WHEN** a seção traz `### CT2 (FCT2, FCT4)`
- **THEN** a leitura reprova, dizendo que cada CT tem uma única faceta

#### Scenario: Forma antiga
- **WHEN** uma tabela da seção tem cabeçalho `| FCT1 | pt | en | es |` e nenhum título CT
- **THEN** a leitura reprova, nomeando a forma `### CTn (FCTn)`; a tabela não é ignorada

### Requirement: Linhas do controle terminológico pela natureza do termo
Cada CT SHALL ter as linhas "Termo livre", "Descritores correspondentes" e "Termos sinônimos
ou relacionados", lidas como `livre`, `descritores` e `relacionados`. O rótulo é comparado
inteiro, sem ênfase nem espaços nas pontas. Linha ausente, repetida ou com rótulo
desconhecido MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando o CT e o rótulo.

#### Scenario: Rótulo antigo
- **WHEN** o CT1 traz a linha `*Termos centrais (núcleo)*`
- **THEN** a leitura reprova, nomeando CT1 e o rótulo desconhecido

#### Scenario: Rótulo com ênfase
- **WHEN** o CT1 traz `*Descritores correspondentes*`
- **THEN** a linha é lida como `descritores`

#### Scenario: Linha ausente
- **WHEN** o CT3 não tem a linha "Termos sinônimos ou relacionados"
- **THEN** a leitura reprova, nomeando CT3 e a linha que falta

### Requirement: Célula vazia admitida no controle terminológico
Uma célula de idioma de qualquer linha do CT MAY estar vazia. A conferência MUST NOT
reprovar a célula vazia: sem decisão de validação, as linhas de descritores e de sinônimos ou
relacionados ficam vazias, e essa é a classificação correta.

#### Scenario: Linha de descritores vazia
- **WHEN** nenhuma célula da linha "Descritores correspondentes" do CT2 tem termo
- **THEN** `--conferir` não reprova por célula vazia

### Requirement: Termo em uma única linha do CT
O mesmo termo, comparado na forma normalizada, MUST NOT constar de mais de uma linha do mesmo
CT no mesmo idioma. A repetição MUST reprovar em `--conferir`, nomeando a faceta, o idioma, o
termo e as linhas. A mesma forma em idiomas diferentes do mesmo CT é admitida.

#### Scenario: Termo livre e descritor ao mesmo tempo
- **WHEN** `ontology` consta das linhas "Termo livre" e "Descritores correspondentes" do CT1,
  em `en`
- **THEN** `--conferir` reprova, nomeando FCT1, `en`, `ontology` e as duas linhas

#### Scenario: Mesma forma em dois idiomas
- **WHEN** `educacional` consta da linha "Termo livre" do CT2 em `pt` e em `es`
- **THEN** `--conferir` não reprova por repetição entre linhas

### Requirement: Linha do termo confere com a validação terminológica
`--conferir` SHALL calcular a linha esperada de cada termo pela regra de
`validacao-terminologica` ("Linha do termo resulta da decisão do ReT") e MUST reprovar o termo
que estiver em outra linha, nomeando a faceta, o idioma, o termo, a linha atual e a esperada.
Planilha ausente MUST NOT reprovar o termo em "Termo livre".

#### Scenario: Descritor sem decisão
- **WHEN** a planilha de validação não existe e `ontology` está na linha "Descritores
  correspondentes" do CT1
- **THEN** `--conferir` reprova, dizendo que a linha esperada é "Termo livre"

#### Scenario: Planilha ausente com todos os termos livres
- **WHEN** a planilha de validação não existe e todo termo está em "Termo livre"
- **THEN** `--conferir` não reprova pela classificação, e `projeto pendencias` relata a
  validação pendente

#### Scenario: Descritor decidido e ainda em termo livre
- **WHEN** a planilha registra `decisao_ReT = descritor` para `ontology` (FCT1, en) na
  UNESCO, e o termo está em "Termo livre"
- **THEN** `--conferir` reprova, dizendo que a linha esperada é "Descritores correspondentes"

#### Scenario: Planilha ilegível
- **WHEN** a planilha de validação existe e não pode ser lida
- **THEN** `--conferir` termina com DADOS, e a planilha não é tratada como ausente

### Requirement: Autoteste prova as reprovações do controle terminológico
`projeto autoteste` SHALL injetar, numa cópia em memória, cada defeito de forma e de
coerência do controle terminológico: título fora da forma, número divergente, duas facetas,
forma antiga, primeira célula do cabeçalho fora da forma, rótulo desconhecido, termo em duas
linhas, termo fora da linha esperada com e sem planilha, termo de "Termos sinônimos ou
relacionados" posto na STR. Defeito não reprovado, ou reprovado com outro código, MUST fazer o autoteste
falhar.

#### Scenario: Conferência cruzada que não reprova
- **WHEN** o autoteste move, numa cópia, um termo sem decisão para "Descritores
  correspondentes" e `--conferir` não reprova
- **THEN** `projeto autoteste` falha, nomeando o defeito

#### Scenario: Forma antiga ignorada
- **WHEN** o autoteste troca, numa cópia, um título CT pelo cabeçalho antigo e a leitura não
  sai com PROTOCOLO_ILEGIVEL
- **THEN** `projeto autoteste` falha, nomeando o defeito e o código obtido

### Requirement: Sem mínimo de termos por STR
`--conferir` MUST NOT reprovar uma STR pelo número de termos: o tamanho da STR resulta do
controle terminológico. A chave `[conferencia] minimo_termos_string` MUST reprovar na
configuração como chave retirada, nomeando a chave e a correção.

#### Scenario: STR curta
- **WHEN** a STR1 tem menos termos do que o antigo mínimo de 20, e é igual à STR gerada
- **THEN** `--conferir` não reprova a STR1

#### Scenario: Chave do mínimo na configuração
- **WHEN** `config.toml` traz `[conferencia] minimo_termos_string = 20`
- **THEN** a configuração reprova com CONFIGURACAO, nomeando a chave como retirada

### Requirement: Conjunto-semente lido do arquivo mínimo de sementes
O conjunto-semente SHALL ser lido do arquivo TOML de `[documentos] sementes`, uma tabela
`[[sementes]]` por estudo, com o esquema mínimo da gramática: `id`, `doi`,
`referencia_curta` e `bases`, obrigatórios, e `alinhamento_facetas`, `verificacao` e `nota`,
opcionais. Os dados bibliográficos, o resumo e as palavras-chave MUST vir da cópia da coleção
do Zotero, e o arquivo de sementes MUST NOT guardá-los.

#### Scenario: Arquivo atual
- **WHEN** o arquivo de sementes tem as sementes de SE1 a SE19 com os campos do esquema
  mínimo, e a cópia da coleção tem um item para cada DOI
- **THEN** a leitura aprova, e a distribuição por base exibida por `configuracao mostrar` é
  calculada do campo `bases`

#### Scenario: Título vindo do Zotero
- **WHEN** o título do item do Zotero de uma semente contém um ponto seguido de maiúscula
- **THEN** o título lido é o campo inteiro do item

#### Scenario: Distribuição calculada
- **WHEN** o arquivo é lido
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas do campo `bases`

### Requirement: Verificação declarada pelo pesquisador
`verificacao = true` SHALL significar que o pesquisador declara conferidos os dados
bibliográficos do item no Zotero, e a declaração basta, sem registro de onde e como se
conferiu. `false` ou ausente é conferência pendente. Texto ou outro tipo MUST reprovar a
leitura.

#### Scenario: Verificação como texto
- **WHEN** uma semente traz `verificacao = "CONFIRMADA"`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo

#### Scenario: Verificação pendente
- **WHEN** uma semente traz `verificacao = false` ou não traz o campo
- **THEN** a leitura aprova, e `projeto pendencias` relata a verificação pendente

#### Scenario: Verificação conferida
- **WHEN** uma semente traz `verificacao = true` sem `nota`
- **THEN** `projeto pendencias` não relata verificação pendente para ela

### Requirement: Arquivo mínimo de sementes fora do esquema reprova
Arquivo de sementes ausente MUST terminar com CONFIGURACAO, nomeando a chave e o caminho.
MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo: TOML inválido; campo
obrigatório ausente ou de tipo errado; campo desconhecido; `id` fora da forma `SEn`,
repetido ou fora da sequência a partir de SE1; `doi` ausente, fora da forma `10.x/…` ou
repetido; base fora da tabela de bases, com outra grafia ou repetida; chave de
`alinhamento_facetas` fora da tabela de facetas, ou com frase vazia.

#### Scenario: Lacuna na numeração
- **WHEN** o arquivo tem SE1, SE2 e SE4, sem SE3
- **THEN** a leitura reprova, nomeando SE4 e o `id` esperado, SE3

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Faceta inexistente no alinhamento
- **WHEN** a semente SE7 traz `alinhamento_facetas = { FCT9 = "ontologia" }` e a tabela de
  facetas vai até FCT4
- **THEN** a leitura reprova, nomeando SE7 e a faceta

#### Scenario: Frase de alinhamento vazia
- **WHEN** a semente SE7 traz `alinhamento_facetas = { FCT1 = "" }`
- **THEN** a leitura reprova, nomeando SE7 e FCT1

#### Scenario: Semente sem DOI
- **WHEN** uma semente não traz `doi`
- **THEN** a leitura reprova, nomeando a semente e o campo `doi`

#### Scenario: Campo desconhecido
- **WHEN** uma semente traz o campo `titlo`, os campos retirados `autores`, `ano`, `titulo`,
  `veiculo`, `volume`, `numero`, `paginas`, `facetas` ou `veiculo_conferido`, os campos
  retirados antes `escopo`, `papel`, `tipo`, `alinhamento`, `eric` e `observacoes`, ou o
  campo `semente` do esquema intermediário
- **THEN** a leitura reprova, nomeando a semente e o campo

#### Scenario: Arquivo ausente
- **WHEN** `[documentos] sementes` aponta um arquivo que não existe
- **THEN** o subcomando termina com CONFIGURACAO, nomeando a chave e o caminho, e nenhuma
  semente é presumida

### Requirement: Pendência de semente relatada, sem reprovar
`projeto pendencias` SHALL relatar, nomeando a semente, sem reprovar a leitura:

- `alinhamento_facetas` vazio ou ausente;
- alinhamento sem nenhuma faceta marcada `Sim` em "Âncora obrigatória", enquanto o
  pesquisador não decide a regra; com o alinhamento vazio, só "alinhamento a informar";
- item do Zotero sem resumo ou sem palavras-chave na cópia da coleção;
- semente sem registro na OpenAlex.

#### Scenario: Alinhamento a informar
- **WHEN** a semente SE3 não traz `alinhamento_facetas`
- **THEN** a leitura aprova, e `projeto pendencias` relata SE3 com alinhamento a informar

#### Scenario: Validação sem âncora
- **WHEN** a semente SE5 traz `alinhamento_facetas = { FCT3 = "metodologia da problematização" }`,
  e FCT1 e FCT2 são as âncoras
- **THEN** a leitura aprova, e `projeto pendencias` relata SE5 sem faceta âncora

#### Scenario: Validação sem alinhamento
- **WHEN** a semente SE3 não traz `alinhamento_facetas`
- **THEN** `projeto pendencias` relata SE3 com alinhamento a informar, e não relata SE3 sem
  faceta âncora

#### Scenario: Resumo ausente
- **WHEN** o item do Zotero da semente SE5 não tem resumo na cópia da coleção
- **THEN** a leitura aprova, e `projeto pendencias` relata SE5 com resumo ausente

### Requirement: Semente retirada não deixa resto na evidência
Semente retirada SHALL sair do arquivo de sementes e das saídas regeneradas. `dados
conferir` MUST reprovar arquivo da subpasta `referencias/` de `[dados] evidencia` nomeado
com um `SEn` que não está no arquivo de sementes, e arquivo das subpastas `openalex/` e
`crossref/` — resposta ou marcador de 404 — cujo DOI não está no arquivo de sementes,
nomeando o arquivo. As outras subpastas da evidência MUST
NOT ser conferidas por essa regra.

#### Scenario: Evidência de semente retirada
- **WHEN** SE10 é retirada do arquivo e `SE10_crossref.json` continua em
  `data/evidencia/referencias/`
- **THEN** `dados conferir` reprova, nomeando `SE10_crossref.json`

#### Scenario: Resposta da OpenAlex de semente retirada
- **WHEN** a semente de DOI `10.5753/wetie.2023.236130` é retirada e a resposta da OpenAlex
  desse DOI continua em `data/evidencia/openalex/`
- **THEN** `dados conferir` reprova, nomeando o arquivo

#### Scenario: Renumeração sem renomear evidência
- **WHEN** SE15 é retirada e as seguintes são renumeradas
- **THEN** nenhum arquivo de `data/evidencia/openalex/` precisa ser renomeado, e `dados
  conferir` aprova

### Requirement: Autoteste prova a reprovação do esquema mínimo
O autoteste SHALL injetar numa cópia do arquivo de sementes, a partir das sementes lidas,
cada um destes defeitos e exigir PROTOCOLO_ILEGIVEL: `doi` ausente, `doi` fora da forma,
`doi` repetido, faceta do alinhamento fora da tabela, frase de alinhamento vazia, lacuna na
numeração dos `id`, campo bibliográfico retirado (`titulo`) e o campo `semente` do esquema
intermediário.

#### Scenario: DOI ausente reprova
- **WHEN** o autoteste retira o `doi` de uma semente numa cópia
- **THEN** a cópia reprova com PROTOCOLO_ILEGIVEL; se for aprovada, o autoteste falha

#### Scenario: Defeito não detectado
- **WHEN** a cópia com o campo `semente` é aprovada
- **THEN** o autoteste falha, nomeando o defeito

### Requirement: Autoteste prova a reprovação da junção com o Zotero
O autoteste SHALL injetar numa cópia da coleção o item de uma semente sem título, e retirar
dela o item de outra semente, e exigir a reprovação em cada caso. SHALL também exigir que
`dados conferir` reprove a evidência de semente inexistente.

#### Scenario: Item sem título
- **WHEN** o autoteste esvazia o título do item de uma semente numa cópia da coleção
- **THEN** a leitura reprova; se for aprovada, o autoteste falha

#### Scenario: Item retirado da cópia
- **WHEN** o autoteste retira da cópia da coleção o item de uma semente
- **THEN** a leitura reprova com DADOS; se for aprovada, o autoteste falha

### Requirement: Semente casada com o item do Zotero pelo DOI
A leitura SHALL casar cada semente com o item da cópia da coleção que tem o mesmo DOI,
comparado em caixa baixa e sem prefixo de URL. DOI do arquivo de sementes sem item na cópia,
ou com mais de um item, MUST reprovar com DADOS, nomeando a semente e o DOI. Item da cópia
cujo DOI não está no arquivo de sementes SHALL ser relatado, sem reprovar.

#### Scenario: DOI sem item
- **WHEN** a semente SE19 tem um DOI que nenhum item da cópia traz
- **THEN** a leitura reprova com DADOS, nomeando SE19, o DOI e `sementes copiar`

#### Scenario: Item a mais na coleção
- **WHEN** a cópia traz o item de DOI `10.5220/0012471400003645`, que nenhuma semente cita
- **THEN** a leitura aprova, e `projeto pendencias` relata o item como fora do arquivo de
  sementes

#### Scenario: DOI com caixa ou prefixo diferente
- **WHEN** o arquivo traz `10.1111/EXSY.12246` e o item traz `https://doi.org/10.1111/exsy.12246`
- **THEN** a semente casa com o item

### Requirement: Referência curta conferida contra o Zotero
`referencia_curta` SHALL ter a forma `<sobrenome> <ano>: <início do título>`, conferida
contra o item da cópia: o ano igual ao do item, o resto sem acento, caixa nem pontuação. `documentos conferir` MUST reprovar a que não
confere, nomeando a semente e a forma sugerida; a leitura MUST NOT reprovar por isso.

#### Scenario: Sobrenome trocado
- **WHEN** o sobrenome da referência curta não é o do primeiro autor do item
- **THEN** `documentos conferir` reprova, nomeando a semente e a forma sugerida

#### Scenario: Ano trocado
- **WHEN** o ano da referência curta não é o do item
- **THEN** `documentos conferir` reprova, nomeando a semente e a forma sugerida

#### Scenario: Reticências finais
- **WHEN** a referência curta termina em `…` depois das primeiras palavras do título do item
- **THEN** `documentos conferir` aprova

#### Scenario: Referência curta conferida
- **WHEN** a semente traz `referencia_curta = "Alvarenga 2023: Objetos de aprendizagem organizados…"` e o item do Zotero tem Alvarenga como primeiro autor, ano 2023 e título que começa por essas palavras
- **THEN** `documentos conferir` aprova

#### Scenario: Título corrigido no Zotero
- **WHEN** o título do item mudou no Zotero e a referência curta não começa mais pelas mesmas palavras
- **THEN** `documentos conferir` reprova, nomeando a semente e a forma sugerida, e `aderencia medir` continua funcionando

#### Scenario: Referência curta ausente
- **WHEN** a semente não traz `referencia_curta`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo

### Requirement: Alinhamento das facetas por frase
`alinhamento_facetas` SHALL ser uma tabela TOML cujas chaves são `FCTn` da tabela de facetas
do protocolo e cujos valores são frases curtas, não vazias, que explicam por que a semente
se alinha à faceta. Faceta ausente da tabela significa semente não alinhada a ela.

#### Scenario: Alinhamento lido
- **WHEN** a semente traz
  `alinhamento_facetas = { FCT1 = "ontologia de domínio", FCT2 = "ensino de matemática na educação básica" }`
- **THEN** a leitura aprova, e a semente fica alinhada à FCT1 e à FCT2, com as duas frases

#### Scenario: Forma de lista recusada
- **WHEN** a semente traz `alinhamento_facetas = ["FCT1", "FCT2"]`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo
