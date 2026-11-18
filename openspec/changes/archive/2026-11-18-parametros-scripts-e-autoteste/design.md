# Design

## Context

Motivação em `proposal.md`. Estado atual relevante:

- `src/protocolo.py`, `_coerencia_expressoes(d)`, já calcula âncoras e específicas a partir
  da composição lida, mas só para reprovar; não expõe o resultado.
- `src/derivar_expressoes.py:80-83` já obtém `GRUPOS`, executada (`SUPERCONJUNTO`) e sonda do
  protocolo, mas `_prova_da_composicao` (l. 320-346) fixa `EB1` a `EB5` e as relações
  `EB4 = EB2 ∪ EB3`, `EB5 ⊃ EB4`, `EB1 ⊆ EB2 ∩ EB3` e `DERIVAVEIS == {EB1, EB2, EB3}`.
- `src/derivar_expressoes.py:104` fixa `BASE_CANONICA`; `src/gen_semente.py:37` fixa `BASES`.
  `[fichas]` do `config.toml` já tem `sigla` por slug, e `protocolo.FICHAS`/`protocolo.BASES`
  já a expõem.
- O autoteste de `protocolo.py` não exercita `instrumentos_do_termo` nem a reprovação
  isolada por base, e `_autoteste_dados` devolve zero casos quando os arquivos de `data/`
  faltam.

## Goals / Non-Goals

**Goals:**
- Um único cálculo dos papéis das expressões, usado pela conferência e pela derivação.
- Nenhum identificador de expressão nem sigla de base fixado em `src/`.
- Saídas idênticas às atuais para o protocolo e a configuração atuais.

**Non-Goals:**
- Alterar a lógica de derivação, aderência, fidelidade ou sensibilidade.
- Reescrever `derivar_expressoes.py` além da prova da composição e do mapa de bases.

## Decisions

### D1. `protocolo.papeis(d)`
Função pura sobre o resultado de `analisa()`: devolve âncoras (grupos unitários das STR das
facetas-âncora), específicas (expressões, exceto executada e sonda, com exatamente um grupo
unitário além das âncoras), gerais (exceto executada e sonda, com mais de um grupo além das
âncoras), executada e sonda. `_coerencia_expressoes` passa a usá-la; `analisa()` grava o
resultado em `d["papeis"]`.
*Alternativa:* recalcular em `derivar_expressoes.py`. Rejeitada: dois cálculos dos mesmos
papéis podem divergir em silêncio.

### D2. Prova da composição genérica
Sobre todas as combinações de facetas, para os papéis de D1:
- `executada(f) == any(específica(f))`;
- `sonda(f)` vale sempre que qualquer outra expressão vale;
- cada geral está contida em cada específica cuja string distintiva ela exige;
- deriváveis = composição − {executada, sonda}, e a prova exige que coincidam com o que
  `_derivaveis()` calcula.
Mantém-se a exigência de que toda expressão seja satisfeita por ao menos uma combinação.

### D3. Bases pela configuração
`BASE_CANONICA = {slug: f["sigla"] for slug, f in protocolo.FICHAS.items()}` e
`BASES = list(protocolo.BASES)` em `gen_semente.py`, na ordem de `[fichas]`.

### D4. Autoteste
- `_autoteste_validacao(t)`: sobre cópias em memória, confere `instrumentos_do_termo` para
  faceta com vários instrumentos, instrumento retirado da linha, termo fora dos idiomas e
  instrumento manual.
- Caso novo em `_autoteste_bases`: altera só a ficha da BRAPCI e exige reprovação nela e
  aprovação nas demais.
- `_autoteste_dados` devolve também o número de casos não executados e o motivo; o resumo
  os lista à parte.

## Risks / Trade-offs

- **[Prova genérica mais fraca que a fixa]** Uma relação esquecida deixaria de ser provada →
  as quatro relações atuais viram as quatro relações genéricas de D2, uma a uma, e um
  autoteste com composição alterada exige que a prova reprove.
- **[Ordem das bases]** `gen_semente.py` escreve colunas por base; mudar a ordem muda a
  planilha → `[fichas]` tem hoje a mesma ordem da lista fixada (WoS, Scopus, ERIC, BRAPCI);
  a tarefa confere.
