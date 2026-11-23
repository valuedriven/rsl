# Proposal

## Why

`docs/procedimentos.md` é a única fonte do mapeamento passo → fonte, skill e script, mas
nada o lê. Uma skill nova pode ficar órfã, um comando renomeado pode deixar citação morta,
a contagem de passos pode divergir — hoje o guia declara 63 e lista 64 — e 29 passos não têm
apoio declarado, sem que nenhuma conferência reprove. O guia já corrigiu o conteúdo; falta
tornar a sua forma verificável.

## What Changes

- **Novo comando `python3 -m rsl catalogo gerar [--gravar] [--json]`.** Sem `--gravar`,
  imprime o catálogo, confere e sai com `REPROVADO` se houver inconsistência; com
  `--gravar`, grava `docs/catalogo_de_apoio.md` de forma atômica. A fonte continua sendo
  `docs/procedimentos.md`; o catálogo é saída de geração e não se edita à mão.
- **Conferência do catálogo**, com oito regras: skill citada existe; toda skill existente foi
  citada ou declarada transversal; caminho e opção de comando citados existem; todo comando
  do parser foi citado ou declarado transversal; todo passo tem skill, script,
  `Apoio: manual` ou `Apoio: lacuna`; a contagem é `modelo 63 + adaptação N = total`; o
  catálogo gravado está atualizado; nenhum documento ou skill viva cita nome antigo de
  comando ou de skill.
- **Passo de adaptação declarado.** O guia passa a dizer “sessenta e três passos, mais um
  passo de adaptação do projeto — a geração das strings de busca —, totalizando sessenta e
  quatro”. O passo novo recebe a marca `(adaptação do projeto)`; o plano continua dizendo
  que o modelo tem 63 passos.
- **Cobertura declarada.** Os 29 passos sem skill nem script recebem `Apoio: manual — razão`
  ou `Apoio: lacuna — razão`. Citações que faltam são acrescentadas: `questao-e-objetivos`
  em M2/E2, `relato-prisma` na tabela de composição e na normalização, `busca-nas-bases`
  na exportação e nos alertas. As skills passam a declarar o papel: procedimento,
  instrumento, artefato ou transversal.
- **Autoteste do catálogo**, com injeções que devem reprovar: skill inexistente, skill
  órfã, comando inexistente, opção inexistente, contagem errada, passo sem marcador,
  catálogo defasado e citação de nome antigo.
- **Documentação**: o README ganha o caminho de `docs/catalogo_de_apoio.md` e o comando de
  geração; o guia ganha a seção que explica o catálogo; o histórico registra a decisão.

Não há renomeação de comando ou de skill nesta change. A renomeação das fichas para
`docs/procedimentos_busca_<sigla>.md` já está feita e é apenas consumida pelo catálogo.

## Capabilities

### New Capabilities

- `catalogo-de-apoio`: derivação do catálogo de skills e scripts a partir do guia de
  procedimentos, cobertura por passo e conferência de integridade.

### Modified Capabilities

- `interface-de-comando`: o ponto de entrada único passa a listar `catalogo gerar`.

## Impact

- Código: `src/rsl/__main__.py`, novo `src/rsl/catalogo.py`, `src/rsl/autoteste/` (grupo
  “catálogo”).
- Documentos: `docs/procedimentos.md` (contagem, marca de adaptação, marcadores de apoio e
  citações), `docs/01_plano.md` (nota sobre o passo de adaptação), `README.md` (mapa e
  comando) e `docs/catalogo_de_apoio.md` (novo, gerado).
- Specs: nova `catalogo-de-apoio`; delta em `interface-de-comando`.
- Histórico: `data/historico.md`, com a decisão e o alcance.
- Não mudam: protocolo, fichas, conjunto-semente, strings, expressões, critérios, bases,
  contagens de busca, `config.toml` e os artefatos já arquivados.
