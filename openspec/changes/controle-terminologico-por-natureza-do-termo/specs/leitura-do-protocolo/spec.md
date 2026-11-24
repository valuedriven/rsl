## MODIFIED Requirements

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

## ADDED Requirements

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
