# Design

## Context

A motivação e o critério de entrada estão em `proposal.md`. O critério foi conferido em
2026-11-23: `catalogo gerar`, sem `--gravar`, saiu 0 e sem problema `nome_antigo`, e o
`grep` em `config.toml` e `data/pendencias.json` não encontrou nome antigo.

Hoje, quatro mecanismos sustentam a transição:

- `__main__.ALIASES` e o laço que monta, para cada alias, um parser oculto que avisa e
  delega ao canônico. `_parser(aliases=…)` existe para o autoteste.
- `config.RENOMEADAS` e `_renomeia`, que aceitam `[documentos] ficha` com aviso. O
  parâmetro `avisa` de `valida` só serve a isso.
- No catálogo: `SKILLS_RENOMEADAS`, os campos `aliases`, `renomeadas`, `chaves` e `vivos`
  de `Entradas`, `_vivos`, `CODIGO_ISENTO`, `_padroes_antigos`, a regra `nome_antigo` e a
  seção "Correspondência de nomes". `vivos` só alimenta a regra `nome_antigo`.
- O grupo de autoteste "aliases de transição" e os casos de nome antigo dos grupos do
  catálogo e da configuração.

## Goals / Non-Goals

**Goals:**
- Tirar do código do produto qualquer tabela de nome antigo para nome canônico, conforme a
  decisão do pesquisador (opção 2: sai tudo junto com os aliases).
- Recusar o nome antigo de comando com USO e a chave antiga com CONFIGURACAO, com mensagem
  que nomeie a chave canônica.

**Non-Goals:**
- Não se substitui a varredura de nome antigo por outra conferência.
- A correspondência das specs com as flags antigas (requisito "Correspondência com os
  nomes das specs") não muda. Ela trata das flags anteriores à change de namespace e não é
  alias.

## Decisions

1. **Chave antiga vai para `RETIRADAS`.** `documentos.ficha` entra em `config.RETIRADAS`
   com o motivo "renomeada para `[documentos] procedimento`; renomeá-la, mantendo o valor".
   Cada motivo de `RETIRADAS` termina com a sua correção, e não com um "retirá-la" comum a
   todos, porque retirar esta chave faria faltar a canônica. `RENOMEADAS`, `_renomeia` e o
   parâmetro `avisa` saem. A alternativa era deixar a chave cair na regra de "chave
   desconhecida", mas a mensagem não nomearia a canônica. `RETIRADAS` já reprova com
   mensagem própria e já é percorrida pelo autoteste da configuração. A chave entra na
   prova sem caso novo, e a mensagem da canônica ganha um caso.
2. **Parser sem alias.** Saem `ALIASES`, `_com_aviso`, o laço de aliases e o parâmetro
   `aliases` de `_parser`. O grupo deixa de ter a forma oculta, porque só o alias a usava.
   Um nome antigo passa a cair no erro de argumento do `argparse`, que já sai com USO.
3. **Catálogo sem nome antigo.** Saem `SKILLS_RENOMEADAS`, `CODIGO_ISENTO`, `_vivos`,
   `_padroes_antigos`, `_chave_toml` se ficar sem uso, os campos `aliases`, `renomeadas`,
   `chaves` e `vivos` de `Entradas`, a regra `nome_antigo` de `REGRAS`, os filtros de
   alias em `comando_orfao` e em `visoes`, o campo `correspondencia` e a seção renderizada.
4. **Autoteste "nomes antigos recusados".** O grupo `aliases` é substituído por um que
   guarda a lista dos onze nomes antigos de comando como dado de teste, e não como dado do
   produto. Para cada nome, o grupo exige USO do parser real. Como contraprova, o mesmo
   detector aplicado ao nome canônico correspondente precisa *não* dar USO: assim o caso
   não passa trivialmente (por exemplo, com um parser que recusasse tudo). A prova de que
   o grupo reprova um alias reintroduzido é feita uma vez na implementação, com um alias
   reposto temporariamente, e fica registrada no relato da aplicação, em `tasks.md`; o
   histórico não guarda resultado de conferência.

## Risks / Trade-offs

- [Um documento volta a citar nome antigo, fora das citações de comando do guia] → nada
  automático acusa isso. É o custo aceito da opção 2. O usuário que executar o nome recebe
  USO, e o comando citado no guia continua conferido pela regra `comando_existe`.
- [Uma configuração local ainda tem `[documentos] ficha`] → reprova com CONFIGURACAO e
  nomeia `[documentos] procedimento`. A correção é renomear a chave.

## Migration Plan

Aplicar em um passo só: código, autoteste, catálogo regravado
(`python3 -m rsl catalogo gerar --gravar`) e entrada no histórico. Para reverter, basta
reverter o commit. Não há dado migrado.
