# Design

## Context

A motivação está em `proposal.md`. Estado observado em 2026-11-19:

- `criterios()` em `src/protocolo.py` lê a tabela "Critérios de elegibilidade" com seis
  colunas (ID, Dimensão, Ação, Critério, coluna vazia, Justificativa) e já guarda
  `justificativa`. Ninguém confere esse campo.
- `--conferir` já exige as dimensões de `[conferencia] dimensoes_criterio` do
  `config.toml`. A justificativa de CE5 e de CE6 está vazia, então a conferência nova
  reprova o protocolo atual até que o pesquisador as preencha.
- As quatro fichas citam os critérios na seção 2, em tabela com coluna de ID, às vezes
  agrupados (`CE1 / CE2`, `CE7 / CE8`). O README cita o CE6 em M3/E3.
- Regra de inclusão, regra de borda e contra-escopo estão em `docs/01_plano.md:82`.

## Goals / Non-Goals

**Goals:**
- O protocolo enuncia sozinho tudo o que os revisores aplicam na triagem.
- Renumerar critérios não deixa fichas defasadas sem aviso.

**Non-Goals:**
- Redigir os critérios. A redação é do pesquisador; o agente propõe texto quando pedido e
  marca a proposta como tal.
- Conferir o conteúdo da justificativa. A conferência garante só que ela existe.

## Decisions

**D-a. A forma da regra de inclusão (D1 da proposta) fica com o pesquisador.**
- Critério novo, com renumeração: torna a regra auditável por ID no fichamento e no
  PRISMA, mas mexe nas fichas, no README e nas skills.
- Conteúdo do CE6: sem renumeração, mas o CE6 acumula três coisas (inclusão, borda e
  contra-escopo) e fica longo.

Recomendação, para o pesquisador julgar: um critério de inclusão próprio para a regra
única e a de borda, e o contra-escopo como critérios de exclusão, um por linha. Isso dá ID
a cada motivo de exclusão, e a 3ª filtragem registra exclusões por ID.

**D-b. A conferência da justificativa é estrita (vazio, espaço ou traço reprovam).**
Alternativa: avisar sem reprovar. Foi rejeitada porque aviso não impede o defeito, e o
contrato prefere garantia por construção.

**D-c. A conferência das fichas compara conjuntos de IDs, não texto.** Os IDs saem por
`CE\d+` da coluna de ID da seção 2. Comparar a descrição de cada critério geraria falso
positivo a cada ajuste de redação; o ID é a chave, como em todo o projeto.

**D-d. A ordem das tarefas evita estado reprovado.** Primeiro o pesquisador preenche as
justificativas e redige as regras; depois se ativa a conferência. Assim `--conferir` não
fica reprovado entre uma etapa e outra.

## Risks / Trade-offs

- [Renumerar quebra referências fora das fichas: README, skills, plano] → a conferência
  cobre só as fichas. As demais referências se localizam por busca (`grep -rn "CE[0-9]"`)
  numa tarefa própria. Prosa fora do protocolo não é conferida automaticamente.
- [Contra-escopo como exclusão por ID muda a contagem do fluxograma PRISMA] → é o efeito
  pretendido: cada exclusão da 3ª filtragem passa a ter motivo citável.
- [A justificativa preenchida às pressas, só para passar] → a conferência não avalia
  conteúdo. A justificativa é decisão registrada do pesquisador, e a mudança entra no
  histórico.

## Migration Plan

Redação no protocolo → remissão no plano → fichas e README → conferências. Não há dado
derivado a regenerar. A planilha de validação e o registro de execução não dependem dos
critérios.
