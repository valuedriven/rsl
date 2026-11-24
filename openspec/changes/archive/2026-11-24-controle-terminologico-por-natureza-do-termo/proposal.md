# Proposal

## Why

O pesquisador reestruturou a seção "Controle terminológico" do protocolo. Cada tabela passa a
ser identificada por `### CTn (FCTn)`, e as linhas passam a classificar o termo pela
**natureza** dele: termo livre, descritor de vocabulário controlado, sinônimo ou relacionado.
Antes, o critério era a **distância conceitual** ao conceito central (núcleo, próximos,
relacionados). A edição já está no protocolo, e desde então o leitor o recusa:
`documentos conferir` sai com PROTOCOLO_ILEGIVEL ("esperava uma tabela por faceta, achei []").

Trocar só os rótulos faria o protocolo afirmar como "descritor correspondente" termos que
nenhum instrumento validou. O plano proíbe isso (`docs/01_plano.md`, riscos e M3/E1: "termo
sem consulta registrada é termo livre"). Por isso a change adota o critério novo junto com a
forma nova e impõe por conferência que a linha de cada termo corresponda à decisão registrada
na validação terminológica.

## What Changes

- **BREAKING. Identificação das tabelas pelo título.** Cada tabela do controle terminológico
  é precedida de `### CTn (FCTn)`. O número de CT é o mesmo da faceta, e cada CT tem uma
  única faceta. A primeira célula do cabeçalho deixa de identificar a faceta. A tabela sem
  título, com título fora da forma, com número divergente ou com mais de uma faceta reprova.
- **BREAKING. Linhas renomeadas, com nomes internos novos:**

  | Linha | Nome interno | Antes |
  | --- | --- | --- |
  | Termo livre | `livre` | Termos centrais (núcleo), `nucleo` |
  | Descritores correspondentes | `descritores` | Descritores potenciais e termos próximos, `proximos` |
  | Termos sinônimos ou relacionados | `relacionados` | Termos relacionados e variantes, `relacionados` |

- **Critério de classificação novo (decisão do pesquisador):**
  - A linha de um termo resulta da `decisao_ReT` da planilha de validação, considerando os
    instrumentos da faceta e do idioma do termo.
  - Descritor autorizado em pelo menos um instrumento vai para "Descritores correspondentes".
  - O termo que não é descritor em nenhum instrumento, mas é USE/UP ou TR de um descritor em
    pelo menos um, vai para "Termos sinônimos ou relacionados".
  - Os demais termos vão para "Termo livre", inclusive os sem decisão e os de instrumento
    manual ainda não consultado.
- **`decisao_ReT` ganha domínio fechado.** Os valores admitidos correspondem às três linhas,
  e o vazio significa "sem decisão". Valor fora do domínio reprova.
- **Conferência cruzada entre o CT e a planilha.** Termo fora da linha que a regra determina
  reprova. Planilha ausente não reprova termo em "Termo livre": vira pendência de validação.
  Termo em "Descritores" ou em "Sinônimos ou relacionados" sem a decisão correspondente
  reprova mesmo sem planilha, porque o protocolo estaria afirmando uma classificação não
  verificada.
- **Repetição entre linhas reprova.** O mesmo termo, no mesmo idioma, em duas linhas do
  mesmo CT passa a reprovar. Até aqui era legítima.
- **Célula vazia admitida.** Sem descritor validado, as linhas de descritores e de
  sinônimos/relacionados ficam vazias, e isso é a classificação correta.
- **BREAKING. Corte `camadas` retirado.** O campo `camadas` da `[cobertura]` das fontes de
  procedimento sai da gramática e das quatro fontes, que hoje declaram `"todas"`. A cobertura
  e a composição dos blocos sempre usam todas as linhas. Se um corte por teto de caracteres
  voltar a ser necessário, será decidido sob o critério novo.
- **Acrescentado na verificação (decisões 9 a 13 do design):** a STR é composta só pelas
  linhas "Termo livre" e "Descritores correspondentes"; o mínimo de termos por STR sai da
  configuração; a primeira célula do cabeçalho do CT é `Termo`; en/es da linha "Termo livre"
  passam a conter os equivalentes dos termos pt. A decisão 13 (executar a validação
  automática) foi retificada: a validação fica fora do escopo (ver abaixo e o design).
- **Conteúdo do protocolo.** Não existe planilha de validação. Pela regra, todo termo vai
  hoje para "Termo livre", e as outras duas linhas ficam vazias. O conjunto de termos de cada
  faceta não muda. As STRs mudam só de ordem e são regeneradas, assim como os procedimentos
  de busca.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-do-protocolo`: identificação das tabelas pelo título `### CTn (FCTn)`; idiomas do
  cabeçalho sem o identificador; linhas novas; célula vazia admitida; repetição entre linhas
  reprovada; conferência de coerência com o cruzamento CT × planilha.
- `gramatica-do-protocolo`: forma de identificador `CTn` acrescentada à fonte única.
- `geracao-das-strings`: ordem da STR pelas linhas novas (livre, descritores, relacionados).
- `validacao-terminologica`: domínio de `decisao_ReT` e regra que leva das decisões à linha
  do CT.
- `cobertura-por-base`: vocabulário vigente sem filtro por camada.
- `fonte-do-procedimento`: `procedimentos iniciar` deixa de gerar `camadas`.
- `geracao-dos-procedimentos`: composição dos blocos sem filtro por camada.

## Impact

- **Código:** `gramatica.py` (seção, identificador CT, rótulos de linha, campo `camadas`),
  `leitura.py` (`tabelas()`), `conferencia.py` (célula vazia, repetição, cruzamento com a
  planilha), `geracao.py`, `cobertura.py`, `procedimentos.py`, `fichas.py`, `termos/`
  (domínio de `decisao_ReT`) e os autotestes de protocolo, geração e procedimentos.
- **Documentos:**
  - protocolo: termos movidos para "Termo livre" e STRs regeneradas;
  - as quatro fontes `procedimento.toml`, sem `camadas`;
  - os quatro `docs/procedimentos_busca_*.md`, regenerados;
  - `data/historico.md`, com as decisões;
  - `data/pendencias.json`, onde PD03 passa a citar a regra nova.
- **Skills:** `facetacao-e-termos-livres` §2, que define a camada como distância conceitual, e
  `procedimento-de-busca-por-base`, que menciona usar só o núcleo.
- **Busca:** retificado na verificação (2026-11-24). As STRs mudam de conteúdo: o
  pesquisador editou o quadro depois da implementação, a linha "Termos sinônimos ou
  relacionados" deixa de entrar na STR, e en/es da linha "Termo livre" passam a ser os
  equivalentes dos termos pt. O teste de aderência será refeito (PD31). Termo novo revelado depois pela validação é ampliação e segue o
  registro próprio.
- **Fora do escopo:** executar a validação terminológica (TBCI e UNESCO por cliente; ERIC e
  Brased à mão pelo pesquisador) e reclassificar a partir dela. Isso é trabalho posterior,
  feito sob a regra que esta change impõe.
