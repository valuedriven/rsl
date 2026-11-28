# Proposal

## Why

A execução das expressões nas bases grava as exportações em `data/execucoes/`, fora do git,
e o registro dela, `data/registro_execucao.json`, mistura execuções com sondagens de sintaxe
e carrega prosa repetida. Com o Zotero como fonte única, cada execução vira uma coleção no
Zotero, o registro guarda só os metadados mínimos para rastreabilidade, e a deduplicação passa
ao Zotero.

## What Changes

- Cada exportação de uma execução vira uma coleção no Zotero, nomeada com o identificador da
  execução. A importação (manual no desktop, com o script conferindo e vinculando, ou
  automática) decide-se no design.
- **BREAKING**: o registro das execuções sai de `data/registro_execucao.json` para
  `data/execucoes.json`. Por base e por execução, ele guarda o identificador, a expressão,
  o texto completo da consulta, os filtros, a data e hora, o retorno, os registros lidos e a
  coleção do Zotero. Deixam de existir `forma`, `mede`, `origem`, o caminho de arquivo e as
  observações em prosa.
- O mínimo não fica abaixo do que o PRISMA-S exige para relatar a busca (base, plataforma,
  data, string completa, filtros, número de resultados).
- **BREAKING**: a deduplicação passa a ser feita no Zotero, pelo Zoplicate ou por outro
  recurso configurável na ferramenta. O script confere o resultado (por exemplo, DOI ainda
  duplicado) em vez de deduplicar. `registros_lidos` se grava antes da deduplicação, para
  que o número de duplicatas removidas se calcule.
- Migração das 8 exportações atuais (WoS e Scopus, EB2 a EB5) para o Zotero. Depois dela,
  remoção de `data/execucoes/`.
- Revisar as skills `executar-expressoes-de-busca` e `controlar-duplicatas`.

Sondagem antes do design: conferir, numa coleção de teste, como a mesclagem do Zoplicate
trata a pertença do item às coleções. Se o item mesclado mantém a união das coleções, a chave
do item no Zotero vira a identidade do registro nas análises. A sondagem só roda com
autorização do pesquisador.

Fora do escopo: o registro das sondagens (change 5) e as saídas das análises (change 6).
Esta change não gera entrada no `data/historico.md`.

Depende de: `zotero-como-fonte-unica`.

## Capabilities

### New Capabilities
- `registro-das-execucoes`: registro mínimo de cada execução, com o vínculo à coleção do
  Zotero e o identificador da execução.
- `controle-de-duplicatas`: deduplicação feita no Zotero e conferida pelo script, com o
  cálculo das duplicatas removidas.

### Modified Capabilities
- `cobertura-por-base`: a verificação por medição passa a remeter à execução registrada no
  arquivo novo.
- `derivacao-das-expressoes`: retorno declarado e registro de execução ausente passam a
  remeter a `data/execucoes.json`.
- `interface-de-comando`: subcomandos de registro da execução e de conferência da
  deduplicação.

## Impact

- Código: `src/rsl/busca/{execucao,registro,leitores}.py`, `src/rsl/dados.py`
  (`problemas_registro`), autotestes de busca e de dados.
- Dados: `data/registro_execucao.json` (parte das execuções), `data/execucoes/`.
- Configuração: `[dados] registro`, `[dados] execucoes`.
- Skills: `executar-expressoes-de-busca`, `controlar-duplicatas`.
- Sistema externo: coleções de execução no Zotero; plugin Zoplicate.
