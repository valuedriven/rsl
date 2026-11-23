# Proposal

## Why

As strings de cada base são escritas à mão a partir das STRs. A verificação de
`strings-geradas-do-quadro` mostrou o efeito: WoS, Scopus e BRAPCI declaram
`plural: explícito`, mas a maior parte dos termos está só no singular, e a conferência só
relata. Nada impede a divergência; ela só é detectada depois. A decisão `plural` também vale
para a base inteira, mas a lematização das bases costuma ser documentada por idioma. Esta
change faz das seções de strings e de expressões da ficha uma saída de geração e trata a
flexão de número por base e por idioma, de modo que o plural esquecido não seja possível.

## What Changes

- **Ficha mista: seções 3 e 4 geradas.** Um subcomando novo, `python3 -m rsl procedimentos gerar
  [<sigla>] [--gravar]`, compõe os blocos de string (`STRn`, e os subconjuntos por campo
  como `STR1b`) e os blocos das expressões de cada base. Os insumos são a STR do protocolo,
  a composição das expressões e os parâmetros de composição declarados na própria ficha.
  Sem `--gravar`, exibe a diferença e as formas geradas; com `--gravar`, substitui só os
  blocos cercados gerados, de forma atômica. A parte autoral não muda de lugar nem de
  autoria: sintaxe verificada (seção 1), critérios (seção 2), declaração de cobertura,
  prosa de execução e de variantes, estratégia de proximidade, conjunto-semente e
  ressalvas. A forma curada também fica autoral; hoje é a da BRAPCI.
  **BREAKING** para o fluxo de trabalho: os blocos gerados deixam de ser editados à mão.
- **Parâmetros de composição declarados na ficha.** A ficha ganha uma tabela com o que
  difere de base para base: o campo de cada faceta, a forma do termo no campo (envolvente
  do grupo ou prefixo por termo), a regra de aspas, o operador e a distância de
  proximidade entre as âncoras e os filtros de critério, tirados da seção 2. Os
  subconjuntos por campo e a forma radical continuam escolha autoral, declarada na ficha
  em tabela, e não em prosa.
- **Partição pelo teto, por construção.** Com teto numérico, o gerador parte o grupo OR da
  faceta não âncora até cada consulta caber no teto, sem retirar termo e com as âncoras
  íntegras. Se as âncoras sozinhas não couberem, a geração reprova em vez de partir uma
  âncora.
- **Flexão de número por regra e exceções.** Com plural explícito, o gerador acrescenta o
  plural de cada termo por regra regular de pt, en e es. As exceções ficam num arquivo do
  pesquisador (`[documentos] flexoes`): plural irregular, termo não contável e forma
  vetada. O termo cuja flexão a regra não decide sem ambiguidade reprova até ter exceção
  declarada; o gerador não adivinha. Toda forma gerada aparece no ensaio antes de gravar.
- **Plural por idioma.** A linha `plural` da declaração de cobertura passa a admitir um
  valor por idioma (`en: pela lematização; pt: explícito; es: explícito`). Um valor único
  continua valendo para todos os idiomas. `pela lematização` continua exigindo a
  lematização medida e citada, agora por idioma.
- **Conferência por construção.** `conferir` reprova o bloco gerado que difere do que o
  gerador produziria e o termo de base com plural explícito que está numa só forma de
  número sem exceção que o justifique. Antes, esse termo era só relatado.
- **Skill nova, `flexao-por-base`:** como decidir, por base e por idioma, entre plural
  explícito e lematização; como medir a lematização com sonda registrada; como julgar
  termo não contável e plural irregular; o que o ensaio do gerador deve mostrar ao
  pesquisador. A skill `ficha-de-busca-por-base` passa a descrever a ficha mista e a ordem
  de geração.
- **Migração das fichas.** As fichas atuais recebem a tabela de parâmetros e as exceções
  de flexão. A primeira gravação acrescenta os plurais que faltam; o ensaio é revisado
  antes.

Fora do escopo: gerar a seção 1, a seção 2 e a prosa; gerar a forma curada; truncamento
automático como alternativa à enumeração do plural; medir a lematização, que depende da
primeira execução de cada base.

Dependência: `strings-geradas-do-quadro` precisa estar arquivada antes. Esta change
modifica requisitos que aquela introduz (`Plural declarado por base`, `Termo só no
singular relatado`, `Ponto de entrada único` com `strings gerar`). A change
`namespace-de-comandos-e-skills` inclui `procedimentos gerar` na tabela canônica (tarefa 1.3a
dela). Pela decisão C1 do pesquisador (2026-11-23), o conceito passa a ser "procedimento de
busca": o comando nasce com o nome canônico, e a skill `ficha-de-busca-por-base` e a chave
`[documentos] ficha` são renomeadas por aquela change.

## Capabilities

### New Capabilities
- `geracao-das-fichas`: composição dos blocos de string e de expressão de cada base a
  partir da STR e dos parâmetros de composição da ficha, partição pelo teto, ensaio e
  gravação dos blocos gerados, e conferência de igualdade.
- `flexao-dos-termos`: flexão de número por regra de pt, en e es, arquivo de exceções
  (irregular, não contável, vetada), reprovação da flexão indecidível e plural por idioma.

### Modified Capabilities
- `cobertura-por-base`: `Plural declarado por base` passa a admitir valor por idioma, e
  `Termo só no singular relatado` passa a reprovar o termo sem exceção declarada.
- `interface-de-comando`: `Ponto de entrada único` passa a listar `procedimentos gerar`.

## Impact

- **Código** em `src/rsl/`:
  - novo módulo de geração das fichas e subcomando `procedimentos`;
  - novo módulo de flexão;
  - leitura da tabela de parâmetros de composição em `fichas.py`;
  - `gramatica.py`, para a tabela de parâmetros, a linha `plural` por idioma e o arquivo de
    exceções;
  - `cobertura.py`;
  - autoteste com casos que provam cada reprovação nova.
- **Configuração:** `[documentos] flexoes` no `config.toml`.
- **Documentos:**
  - as quatro fichas: tabela de parâmetros, blocos regravados e plurais acrescentados;
  - o arquivo de exceções de flexão, novo;
  - `README.md` (Mapa e Precedência);
  - `docs/procedimentos.md`;
  - `data/historico.md`, com entrada sem contagem;
  - `data/pendencias.json`: a pendência do plural de WoS, Scopus e BRAPCI se resolve na
    primeira gravação.
- **Skills:** `flexao-por-base` (nova), `ficha-de-busca-por-base` e
  `expressoes-de-busca`.
- **Busca:** as strings das bases mudam, com os plurais acrescentados e as partições
  recalculadas. Nenhuma execução está registrada, então nenhum resultado fica vencido. O
  teste de aderência mede o efeito na primeira execução.
