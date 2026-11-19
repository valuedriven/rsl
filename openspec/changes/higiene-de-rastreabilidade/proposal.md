# Proposal

## Why

A revisão geral de 2026-11-19 encontrou afirmações sem lastro e registros defasados. Duas
fichas dizem que algo foi **verificado por medição** e citam como fonte
`data/registro_execucao.json`, que não existe. Três pendências descrevem um estado que já
mudou. Nenhuma execução foi registrada ainda, então este é o momento em que corrigir custa
menos: nenhuma contagem depende dessas linhas.

## What Changes

- **Fichas com evidência inexistente.** As linhas abaixo citam um registro ausente:
  - `docs/busca_base_wos.md`, seção 1: "`NEAR/x` entre grupos entre parênteses —
    Verificado por medição — `data/registro_execucao.json` (BD1)";
  - `docs/busca_base_scopus.md`, seção 1: "Proximidade `W/n` e `PRE/n` — `W/5` medido —
    `data/registro_execucao.json` (BD2)";
  - `docs/busca_base_brapci.md`, linha 5: "apurada por medição, com as sondagens em
    `data/registro_execucao.json` (BD4)";
  - `docs/busca_base_eric.md`, linha 5: "comportamento verificado por medição, com as
    sondagens em `data/registro_execucao.json`".

  As quatro citações apareceram na varredura de 2026-11-19 (`grep registro_execucao
  docs/busca_base_*.md`).

  Há duas saídas, e a escolha é do pesquisador:
  - **(a)** reconstituir as medições em `data/registro_execucao.json` (PD02), se ele
    tiver o que a base exibiu;
  - **(b)** rebaixar as linhas para **não verificado**, com a medição remetida à primeira
    execução.

- **Pendências desatualizadas, em `data/pendencias.json`.** Cada uma muda de `estado` e
  ganha `resolucao`, sem ser apagada:
  - **PD01** diz que `data/sementes.json` está ausente, mas o arquivo existe. O que falta
    é o metadado de conferência das 10 sementes. Reescrever a descrição, ou resolver
    PD01 e abrir uma pendência para o metadado.
  - **PD13** aponta a change `parametros-scripts-e-autoteste` como pendente. Ela foi
    arquivada em `openspec/changes/archive/2026-11-18-parametros-scripts-e-autoteste/`.
    Resolver.
  - **PD14** diz que o arquivamento não foi commitado. Ele está commitado, conforme
    `git ls-files`. Resolver.

- **Fundamento da emenda v2 sem números.** `data/historico.md` (2026-11-17) diz que "a
  execução revelou volume incompatível", mas não traz contagem.
  - Se o pesquisador tiver as contagens da execução da versão 1, elas entram em
    `registro_execucao.json` e o histórico remete a elas.
  - Se não tiver, o histórico declara que o fundamento quantitativo não foi registrado.

- **Garantia contra recorrência.** Ao fechar um defeito, deve-se perguntar o que impede
  que ele volte; "reler" não é resposta. Proposta de garantia:
  - toda citação do registro numa ficha nomeia a execução (`BDn/<id>`);
  - `--conferir-dados` reprova a citação sem identificador ou que remeta a execução
    inexistente;
  - o autoteste demonstra que essa reprovação de fato ocorre.

- **Revisão geral sem procedimento.** A revisão de 2026-11-19 deu origem a esta change e
  às outras três, mas foi feita sem roteiro. Por isso não é reproduzível: outra pessoa, ou
  o agente noutra sessão, não sabe o que ela cobriu nem o que deixou de fora. Ela também
  cometeu um erro que um roteiro evitaria. Afirmou de memória que `gen_semente.py` só
  gera linha para a base declarada, e precisou retificar depois de ler o código.

  Proposta: criar a skill `revisao-geral-do-projeto` em `.agents/skills/`, que torna a
  revisão um procedimento. A skill fixa quatro coisas:
  - **o que se percorre:** estado do ciclo, conferências automáticas, lastro das
    afirmações, strings e facetas, conjunto-semente e critérios;
  - **como cada achado se classifica:** verificado, inferido ou hipótese, sempre com a
    evidência e a natureza do conserto;
  - **o que fica de fora:** escrita, acesso a fonte externa e decisão científica;
  - **a forma do produto.**

  A skill `parecer-sobre-protocolo` já cobre em parte a "autoavaliação crítica dos
  instrumentos". Cabe ao pesquisador escolher entre duas saídas:
  - **(a)** criar a skill nova e restringir a `parecer-sobre-protocolo` ao parecer
    externo;
  - **(b)** ampliar a `parecer-sobre-protocolo`, sem criar skill nova.

- **Change concluída e não arquivada.** `expressoes-literais-por-base` tem 15/15 tarefas
  e os arquivos dela estão sem commit. Revisar, commitar e arquivar a change é ação do
  pesquisador; a proposta apenas a lista.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `cobertura-por-base`: exigência nova. Toda citação do registro de execução numa ficha
  nomeia a execução (`BDn/<id>`), e a citação sem lastro reprova só aquela base. O autoteste
  injeta esse defeito. Se o pesquisador recusar a garantia, a change passa a
  `skip_specs: true`.

## Impact

- `docs/busca_base_wos.md`, `docs/busca_base_scopus.md` — seção 1; `docs/busca_base_brapci.md`,
  `docs/busca_base_eric.md` — cabeçalho.
- `data/pendencias.json` — PD01, PD13, PD14.
- `data/historico.md` — fundamento da emenda v2.
- `data/registro_execucao.json` — só na saída (a) e só com dados que o pesquisador fornecer.
- `src/protocolo.py` — conferência e autoteste, se a garantia for adotada.
- `.agents/skills/revisao-geral-do-projeto/SKILL.md` (nova, na saída a) ou
  `.agents/skills/parecer-sobre-protocolo/SKILL.md` (na saída b); README, seção
  "Atividades transversais". A skill não altera spec: é procedimento do agente, não
  comportamento de script.
- Fora do escopo: executar qualquer busca. Nenhum dado de execução é inventado ou
  transcrito de memória.
