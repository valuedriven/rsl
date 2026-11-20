# Spec Delta

## REMOVED Requirements

### Requirement: Linha de faceta sem cor
**Reason**: O pesquisador trocou a lista "Palavras significativas da questão de revisão"
pela tabela "Facetas da questão de revisão", com a coluna "Âncora obrigatória". A linha
`Faceta n (FCTn): nome (âncora obrigatória k)` não existe mais.

**Migration**: Ver "Facetas lidas da tabela".

### Requirement: Conjunto-semente lido de tabela
**Reason**: O pesquisador retirou a tabela de sementes do protocolo e a levou para um
arquivo TOML próprio, com o caminho no `config.toml` (2026-11-20).

**Migration**: Ver "Conjunto-semente lido do arquivo de sementes".

## MODIFIED Requirements

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

### Requirement: Conferência verifica coerência interna
`--conferir` SHALL reprovar contradições internas: termo de STR ausente do quadro da faceta;
expressão sem as âncoras; executada que não seja a união das específicas; semente sem base
ou com base fora da tabela de bases; dimensão de critério em uso não declarada no
protocolo; faixa de sensibilidade com inferior ≥ superior. A sonda ser a conjunção das
âncoras é garantida pela identificação ("Executada e sonda identificadas pela
composição") e não é conferida de novo.

#### Scenario: Termo da string fora do quadro
- **WHEN** uma STR contém um termo que não consta do quadro da sua faceta
- **THEN** `--conferir` reprova, nomeando a faceta e o termo

#### Scenario: Dimensão de critério com grafia do protocolo
- **WHEN** a lista de dimensões em uso tem "Idioma" e o protocolo declara CE3 com "Idioma"
- **THEN** `--conferir` não reprova por dimensão de critério

#### Scenario: Distribuição das sementes não é declarada em prosa
- **WHEN** o conjunto-semente está só no arquivo de sementes, sem parágrafo de incidências
  no protocolo
- **THEN** `--conferir` não reprova por distribuição; a distribuição por base é calculada do
  campo `bases` do arquivo e exibida

## ADDED Requirements

### Requirement: Facetas lidas da tabela
As facetas SHALL ser lidas da tabela "Facetas da questão de revisão", com cabeçalho exato
`Id faceta | Faceta | Âncora obrigatória`. O identificador SHALL ter a forma `FCTn`, em
sequência a partir de FCT1, e o nome MUST NOT ser vazio. A coluna "Âncora obrigatória"
SHALL admitir só `Sim` ou `Não`, sem distinção de caixa. As âncoras são as facetas
marcadas `Sim`, na ordem da tabela. O leitor MUST NOT extrair nem exigir cor, e hífen
dentro do nome pertence ao nome.

#### Scenario: Protocolo atual
- **WHEN** a tabela marca FCT1 e FCT2 com `Sim` e FCT3 e FCT4 com `Não`
- **THEN** as âncoras lidas são FCT1 e FCT2, e `mostrar` as exibe com origem no protocolo

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
de expressões e os candidatos. `mostrar` SHALL exibir a executada e a sonda com origem
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
- **THEN** vale `padroes.sensibilidade`, e `mostrar` exibe a origem "padrão (config.toml)"

### Requirement: Conjunto-semente lido do arquivo de sementes
O conjunto-semente SHALL ser lido do arquivo TOML localizado por `[documentos] sementes`,
uma tabela `[[sementes]]` por estudo, com esquema fechado:

- `id`: texto `SEn`, obrigatório, único e em sequência a partir de SE1;
- `semente`: a referência, texto obrigatório e não vazio;
- `bases`: lista obrigatória e não vazia de siglas da tabela de bases;
- `papel`: obrigatório, `desenvolvimento` ou `validação`.

Autoria, ano, título e DOI SHALL continuar extraídos do campo `semente`.

#### Scenario: Arquivo atual
- **WHEN** `docs/conjunto_semente.toml` tem as 10 sementes de SE1 a SE10
- **THEN** a leitura aprova, e a distribuição por base e por papel exibida por `mostrar` é
  a mesma calculada da tabela de bf6b9bf

#### Scenario: Distribuição calculada
- **WHEN** o arquivo é lido
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas do campo `bases`, e a distribuição por papel, do campo `papel`

### Requirement: Arquivo de sementes fora do esquema reprova
Arquivo de sementes ausente MUST terminar com CONFIGURACAO, nomeando a chave e o caminho.
TOML inválido, campo ausente, campo de tipo errado, campo desconhecido, `id` fora da forma,
repetido ou fora de sequência, base fora da tabela de bases ou com outra grafia, e `papel`
fora do domínio MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo.

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Papel fora do domínio
- **WHEN** a semente SE7 declara o papel `teste`
- **THEN** a leitura reprova, nomeando SE7 e os valores admitidos

#### Scenario: Campo desconhecido
- **WHEN** uma semente traz o campo `titulo`, que o esquema intermediário não declara
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
