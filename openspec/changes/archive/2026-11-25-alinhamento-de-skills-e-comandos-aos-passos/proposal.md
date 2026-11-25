# Proposal

## Why

Skills e comandos ligam-se aos passos do RS Banyan de forma frouxa, e nada o denuncia. Há skill
que cobre oito passos de três módulos (`relato-prisma`) e skill sem passo próprio
(`conjunto-semente`, `flexao-por-base`). O nome não revela o passo: só `conferir-referencia` e
`registrar-decisao` seguem a forma verbo + objeto. `procedimento-de-busca-por-base` repete o que
outras quatro skills já dizem, e a função de revisão está repartida entre `revisao-geral-do-projeto`,
`rastreabilidade` e a metade de auditoria de `auditoria-das-strings`. Do lado dos comandos,
`busca derivar` deduplica, recorta, ordena a triagem e conta, mas o guia o cita num só passo; e
`documentos conferir`, `dados conferir` e `projeto autoteste` estão ancorados em "Montar o protocolo"
por encaixe, quando são transversais. A conferência do catálogo aprova tudo isso.

## What Changes

- **Passo-âncora.** Cada skill passa a ter um de três papéis: **principal** (principal em exatamente
  um passo, podendo servir de apoio a outros), **subordinada** (complementa a principal de um passo)
  ou **transversal** (sem passo). Os papéis atuais — procedimento, instrumento, artefato, transversal
  — são substituídos. **BREAKING** para a tabela "Papel das skills" do guia.
- **Marca de principal no guia.** O passo declara a sua skill principal e os seus comandos principais
  de forma que o catálogo leia; as demais citações são apoio. Cada passo tem no máximo uma skill
  principal; um passo pode ter mais de um comando principal.
- **Nome das skills na forma verbo no infinitivo + objeto**, tirado do verbo do passo-âncora. Pasta e
  `name` mudam juntos. **BREAKING**: corte seco, sem alias nem tabela de correspondência, como
  decidido na remoção dos aliases de 2026-11-23.
- **Escopo das skills revisto** para que cada uma não exceda o seu passo. `procedimento-de-busca-por-base`
  é enxugada e devolve sintaxe, sondagem, flexão e critério às skills donas; `execucao-da-busca` deixa
  o registro de sondagem; os 11 critérios de `auditoria-das-strings` ficam na skill do passo "Gerar as
  strings de busca".
- **Skills sem passo**: `flexao-por-base` passa a subordinada, com nome no infinitivo, ancorada no
  passo da principal que complementa; `conjunto-semente` ganha passo de adaptação próprio
  ("Definir conjunto semente", M3/E1) e passa a principal, como `definir-conjunto-semente`.
- **Revisão e rastreabilidade agrupadas**: `revisao-geral-do-projeto` e `rastreabilidade` fundem-se
  numa skill transversal de revisão do projeto, que absorve a auditoria geral de strings e orienta
  `documentos conferir`, `dados conferir` e `projeto autoteste`. `parecer-sobre-protocolo` e
  `conferencias-da-busca` ficam separadas, porque cada uma tem passo próprio.
- **Comandos ancorados, sem renomeação.** Cada comando é principal em um passo ou transversal
  declarado; `busca derivar` passa a ser citado como apoio nos passos que alimenta. A gramática
  `grupo ação` não muda. Reorganização mínima de módulos: `src/rsl/fichas.py` (resíduo do nome
  anterior ao C1) e `src/rsl/conferencia.py`.
- **Conferência por construção no catálogo**: skill principal sem exatamente um passo, passo com mais
  de uma skill principal, subordinada sem passo ou sem principal, comando sem âncora nem declaração
  transversal — cada um reprova, com caso de autoteste que demonstra a reprovação.

Fora do escopo: renomear comandos; organizar `src/rsl/` por etapa; criar passos de adaptação novos;
alterar questão, critérios, protocolo ou método. A reestruturação é de instrumento, não arquitetural:
não entra em `data/historico.md`.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `catalogo-de-apoio`: os papéis de skill passam a ser principal, subordinada e transversal; o guia
  marca a skill principal e os comandos principais de cada passo; a conferência ganha as regras de
  âncora de skill e de comando, com os casos de autoteste correspondentes.

## Impact

- `.agents/skills/`: 21 das 23 pastas renomeadas, duas fundidas; remissões entre skills.
- `docs/procedimentos.md` (citações, marca de principal, tabela de papéis) e `docs/catalogo_de_apoio.md`
  (regenerado).
- `src/rsl/catalogo.py` e `src/rsl/autoteste/catalogo.py`; `src/rsl/fichas.py` e `src/rsl/conferencia.py`
  com os seus importadores.
- `data/pendencias.json` (ações sugeridas que citam skill), `README.md` onde citar skill, e a spec
  `catalogo-de-apoio`, cujos cenários citam nomes de skill.
- Sem efeito sobre dados, protocolo, procedimentos de busca gerados nem parâmetros.
