# Proposal

## Why

A ficha de base é o protocolo de execução de uma base, mas hoje três das quatro fichas
entregam uma **receita de montagem**, não uma consulta: WoS, Scopus e BRAPCI escrevem as
expressões como `#5 AND (#3 OR #4)` e delegam ao pesquisador substituir os conjuntos. Na
WoS e na Scopus os números `#n` são atribuídos pela sessão, então o texto colado não
reproduz a consulta fora dela; na BRAPCI não há conjunto a referenciar. O resultado é
montagem manual — exatamente o passo em que termo se perde sem aviso.

Nenhuma execução foi registrada ainda, então nenhuma contagem fica vencida: é o momento
mais barato de fechar a forma.

## What Changes

- **Forma de execução da expressão**: cada expressão executada passa a ser um **bloco
  literal único**, submetido como está, sem `#n` e sem substituição.
- **Fichas de WoS, Scopus e BRAPCI**: EB4 e EB5 literais; EB2 e EB3 literais na WoS e na
  Scopus, onde o teste de fidelidade as executa; EB1 sem bloco (nunca se executa) e EB2/EB3
  sem bloco na BRAPCI (derivadas localmente). O grupo das âncoras entra inline nos blocos e
  a subseção que o definia à parte deixa de existir como forma.
- **ERIC**: nenhuma consulta muda — a base não aceita campos diferentes no mesmo grupo, e
  a forma particionada em quatro consultas de campo único já é literal.
- **Instruções de montagem saem**: "submeter a forma expandida, montada em arquivo" e
  "definir `#5` e reusar" são substituídas por "submeter o bloco como está".
- **Seção 1 das fichas de WoS e Scopus**: ganha a linha de comprimento máximo da consulta,
  hoje ausente, mantida como **não verificada**; a consulta expandida passa a ser o que se
  sonda na primeira execução.
- **Conferência nova em `--conferir`** (BREAKING para ficha que use conjunto): bloco de
  expressão executada, de fidelidade ou de sonda não pode referenciar `#n`; o conjunto de
  termos de cada bloco tem de conferir com as facetas que ele declara, ignorando operadores,
  campos e valores de filtro; e bloco na expressão derivada padrão reprova — a forma longa
  declarada é representação não executada e fica fora.
- **Skill `ficha-de-busca-por-base`**: a regra "forma expandida em segunda cópia defasa" é
  invertida — o bloco literal é a forma de execução, e a conferência acima é o que impede a
  defasagem contra a seção 3.
- **Registro da decisão**: histórico e pendências. PD07, PD08 e PD10 passam a declarar só o
  que resta medir; a aceitação da consulta expandida continua **não verificada** até a sonda
  do pesquisador, que depende de `data/registro_execucao.json` (PD02).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `cobertura-por-base`: três exigências novas — o bloco da expressão executada é literal,
  sem referência a conjunto; os termos do bloco conferem com as facetas declaradas; e a
  expressão derivada padrão não leva bloco. A reprovação continua isolada por base e o
  autoteste passa a injetar também esses defeitos.

## Impact

- `docs/busca_base_wos.md`, `docs/busca_base_scopus.md`, `docs/busca_base_brapci.md` —
  expressões, "Como executar", "Variantes" e seção 1.
- `docs/busca_base_eric.md` — sem mudança de consulta; sujeita à conferência nova.
- `src/protocolo.py` — leitura do bloco executado e as duas conferências; autoteste.
- `.agents/skills/ficha-de-busca-por-base/SKILL.md` — regra e contrato de forma.
- `data/historico.md` e `data/pendencias.json` — decisão e pendências.
- Fora do escopo: a composição das expressões no protocolo, a lógica de derivação local e a
  execução das buscas, que é do pesquisador.
