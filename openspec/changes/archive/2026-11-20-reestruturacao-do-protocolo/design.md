# Design

## Context

A motivação está em `proposal.md`, e os requisitos, nas specs desta change.

Estado verificado em 2026-11-20, no arquivo de trabalho:

- `rsl conferir` sai com 4: `seção 'Palavras significativas da questão de revisão': seção
  não encontrada`. Como a leitura para no primeiro erro, as divergências seguintes foram
  levantadas comparando os títulos e as tabelas do protocolo de 73cf68a com os do arquivo
  atual, e não pelo leitor.
- `docs/conjunto_semente.toml` existe, não versionado, com 10 `[[sementes]]` e os campos `id`,
  `semente`, `bases` e `papel`. `id`, `bases` e `papel` coincidem com a tabela retirada.
  O texto de `semente` não foi confrontado célula a célula com a tabela antiga; perdeu ao
  menos o escape `\.` do Markdown.
- O leitor identifica a executada e a sonda pela coluna Natureza, comparada com
  `[expressoes] natureza_executada` e `natureza_sonda`, e lê a faixa no Detalhamento da
  sonda (`leitura.py`, `expressoes()`).
- As âncoras vêm do sufixo `(âncora obrigatória k)` na linha da faceta, com padrão
  `padroes.ancoras`.
- A proximidade é tratada nas fichas (`fichas.py`, `SUBTITULO_PROXIMIDADE`). O parágrafo
  retirado do protocolo não era lido.

## Goals / Non-Goals

**Goals:**
- `rsl conferir` = 0 sobre o protocolo que o pesquisador escreveu, sem pedir mudança de
  forma no documento.
- Toda forma nova declarada na gramática, exibida por `rsl gramatica` e coberta pelo
  autoteste.

**Non-Goals:**
- Estruturar os campos das sementes, fundir `data/sementes.json` ou mudar o nome e a
  tabela de `docs/conjunto_semente.toml`. Isso cabe a `sementes-estruturadas-no-protocolo`.
- Interpretar "Função protocolar", Procedimentos, Instrumentos ou Ferramentas. São texto
  para o leitor humano.
- Mudar a regra de decisão da sonda. A zona de 5% a 15% descrita em N3 é do método.
  Aqui só se confere se o relato a trata como inconclusiva (tarefa 2.5).

## Decisions

### D1. Executada e sonda pela composição

- A **executada** é a única expressão com um grupo de mais de uma STR, ou seja, com `OR`.
- A **sonda** é a única expressão cujos grupos são exatamente as STR das facetas-âncora.

Zero ou mais de um candidato reprova com PROTOCOLO_ILEGIVEL, nomeando a tabela de
expressões e os candidatos.

Os padrões `padroes.executada` e `padroes.sonda` saem: a identificação sempre resolve ou
reprova, e um padrão seria segunda fonte. A conferência "sonda que não seja a conjunção
das âncoras" fica garantida por construção e sai da lista de `conferir`. O caso de
autoteste correspondente passa a ser a ambiguidade, com duas expressões só de âncoras.
A conferência "executada que não seja a união das específicas" continua, porque não é
garantida pela identificação.

Alternativas descartadas:
- texto da "Função protocolar" casado com o `config.toml`: depende de redação livre e
  quebra em silêncio de sentido quando a célula é reescrita;
- marcador na nota: mais uma convenção de redação a manter.

### D2. Notas explicativas e faixa de sensibilidade

- `### Notas explicativas` é subseção opcional de "Expressões de busca", com itens
  `- Nn — <texto>`.
- Uma referência `(Nn)` na coluna "Função protocolar" sem a nota correspondente reprova
  com PROTOCOLO_ILEGIVEL. Uma nota não citada não reprova.
- A faixa é lida das notas citadas na linha da **executada**, onde hoje está N3, com o
  mesmo padrão `< N%` e `> M%`. Os dois limites ausentes fazem valer
  `padroes.sensibilidade`, e um sem o outro reprova, como hoje. O trecho "5%–15%" não
  casa com o padrão, por não ter `<` nem `>`.

A faixa sai da linha da sonda porque o pesquisador a escreveu como regra de decisão sobre
a executada. Ler da sonda faria o leitor cair no padrão sem aviso, mesmo com a faixa
declarada.

### D3. Facetas em tabela

- A tabela de facetas tem cabeçalho exato `Id faceta | Faceta | Âncora obrigatória`.
- O identificador é `FCTn`, em sequência, e o nome não pode ser vazio.
- A âncora admite só `Sim` ou `Não`, sem distinção de caixa. Qualquer outro valor
  reprova.
- Sem nenhuma âncora, a leitura reprova, porque a sonda não seria identificável.

`padroes.ancoras` sai: com a coluna exigida, o padrão nunca seria usado. A ordem das
âncoras é a da tabela. A numeração `(âncora obrigatória k)` deixa de existir, e nada no
código depende de k além da ordem.

### D4. Arquivo de sementes, formato intermediário

- O caminho do arquivo está em `[documentos] sementes = "docs/conjunto_semente.toml"`. Arquivo
  ausente termina com CONFIGURACAO, nomeando a chave e o caminho, como o protocolo
  inexistente.
- O esquema é fechado: tabela `[[sementes]]` com `id` (`SEn`, único, em sequência), `semente` (texto
  não vazio), `bases` (lista não vazia de siglas da tabela de bases, sem repetição) e
  `papel` (`desenvolvimento` ou `validação`). Campo desconhecido, ausente ou de tipo
  errado reprova com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo.
- Autoria, ano, título e DOI continuam extraídos de `semente` por `_titulo()` e `_doi()`,
  com o defeito conhecido. Essa é a limitação aceita do passo intermediário, e a
  correção é o objeto de `sementes-estruturadas-no-protocolo`.

O caminho não vai para o protocolo por decisão do pesquisador. Por isso o cabeçalho do
`config.toml` é reescrito: o conjunto-semente deixa de vir "só do protocolo" e passa a
vir só do arquivo de sementes.

Sobre a chave: `[dados] sementes` já aponta `data/sementes.json`, e a chave nova fica em
`[documentos]`, ao lado da ficha, porque o arquivo é documento editado pelo pesquisador.

### D5. Elementos retirados

Saem da gramática e do leitor:

- "Palavras significativas", com `F_FACETA` e `F_ANCORA`;
- `T_SEMENTES`;
- "Ferramenta de gestão bibliográfica", com `ferramenta_gestao` em `fontes()` e na
  exibição de `mostrar`.

`config.toml` com `[expressoes]`, `padroes.executada`, `padroes.sonda` ou
`padroes.ancoras` reprova, como as demais chaves fora do esquema.

### D6. Marcador da estrutura

O marcador passa a casar parágrafo iniciado por "A estrutura da questão", com o artigo
opcional e sem distinção de caixa. A exigência de existir o parágrafo continua.

### D7. Achados da implementação, decididos pelo pesquisador (2026-11-20)

Com a leitura de volta, a conferência mostrou divergências que o levantamento de títulos
e tabelas não previa:

- **Arquivo de sementes.** O arquivo criado pelo pesquisador chama-se
  `docs/conjunto_semente.toml`. A chave `[documentos] sementes` aponta esse arquivo, e os
  artefatos desta change foram corrigidos.
- **Separador do quadro terminológico.** As células passaram a separar os termos por
  vírgula. O leitor lia cada célula como um termo só, sem reprovar. A gramática declara a
  vírgula como separador, e o separador antigo (`\- ` no início ou depois de espaço)
  reprova com PROTOCOLO_ILEGIVEL. Nenhum termo de 73cf68a tinha vírgula interna.
- **Dimensão "Localização de itens"** retirada de `conferencia.dimensoes_criterio`.
- **STR2 e as strings de FCT2 das fichas** perderam os 23 termos que o pesquisador
  retirou do quadro de FCT2. Isso antecipa parte do D1 de `revisao-das-strings-por-faceta`
  e muda a busca, não só a forma.
- **Critérios das fichas** renumerados pelo mapa aprovado (registro em
  `data/historico.md`, 2026-11-20).

## Risks / Trade-offs

- **[A ordem de correção esconde o defeito seguinte]** → a leitura para no primeiro erro.
  A tarefa 1.1 lista as divergências do levantamento de títulos, e cada tarefa de leitura
  roda `conferir` para ver o próximo erro.
- **[A identificação estrutural falha numa reestruturação futura]**, por exemplo uma
  segunda expressão com `OR` → reprova com os candidatos nomeados, e não escolhe em
  silêncio.
- **[Texto de `semente` diferente da tabela retirada]** → a tarefa 3.1 compara título,
  autoria, ano e DOI extraídos antes (de bf6b9bf) e depois (do arquivo), e diferença vai
  ao pesquisador antes de seguir.
- **[Extração por expressão regular ainda ativa]** → limitação declarada (D4), com
  correção em change própria.

## Migration Plan

1. Gramática e leitor, seção por seção, até `conferir` = 0.
2. `config.toml` e `config.py`, no mesmo passo da leitura que deixa de usar as chaves.
3. P5, histórico, README e skills.

Rollback: reverter o commit. O protocolo e o arquivo de sementes não são alterados por
esta change, salvo P5.
