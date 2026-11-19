# Proposal

## Why

O teste de aderência é a condição de passagem de M3/E2, mas o conjunto-semente atual não
sustenta a conclusão que se pretende tirar dele. Há três razões:

- parte do vocabulário foi ajustada para recuperar sementes específicas, e essas mesmas
  sementes avaliam a busca;
- dez sementes não estimam o recall com precisão útil;
- a coluna "Bases" do protocolo determina em que bases cada semente é procurada, e ninguém
  a conferiu na fonte.

Nenhuma aderência foi registrada (PD02, PD17), então ainda dá para corrigir sem descartar
resultado.

Esta change **não decide** as questões abaixo. Ela apresenta as alternativas e as
consequências, porque limiar e procedimento de aferição cabem ao pesquisador (AGENTS.md §4).

## What Changes

### D1 — Circularidade entre vocabulário e sementes (verificado no histórico)

`data/historico.md` (2026-11-17) registra "Manutenção de `modelo de domínio` (necessário à
recuperação de SE4)". Outros termos compostos acrescentados na v2 (`ontologia facetada`,
`ontologia de currículo`) podem ter a mesma origem; isso é inferência e precisa de
conferência.

**Efeito.** A semente que orientou a escolha do termo é recuperada por construção, e o
recall medido sobre ela fica inflado.

Alternativas:
- **(a)** separar as sementes em **desenvolvimento**, usadas para ajustar o vocabulário,
  e **validação**, reservadas e nunca consultadas no ajuste. A aderência que conta para a
  passagem é a de validação. Exige ampliar o conjunto;
- **(b)** manter o conjunto único, identificando quais sementes influenciaram termos e
  relatando a aderência com e sem elas;
- **(c)** manter o conjunto único e declarar a limitação.

### D2 — Tamanho do conjunto e limiar (calculado)

São 10 sementes e 15 incidências. O limiar de 80% sobre a união das bases exige 8 de 10. O
intervalo de Wilson a 95% para 8/10 vai de cerca de 49% a 94%: o teste aprova sem estimar o
recall.

Alternativas:
- **(a)** ampliar o conjunto até um tamanho que o pesquisador fixe, conforme a precisão
  que quiser;
- **(b)** manter o tamanho e relatar o intervalo junto com a proporção, tratando o
  limiar como critério mínimo, não como estimativa;
- **(c)** combinar com D1 (a): as novas sementes entram como conjunto de validação.

### D3 — Incidência por base (não verificado)

O que segue é inferência de memória, não conferida:

- SE3 (*Expert Systems*), SE6 (*Education and Information Technologies*) e SE8
  (*Interactive Learning Environments*) podem estar indexadas na WoS;
- SE6 pode estar indexada também na Scopus.

O protocolo não as declara nessas bases.

**Retificação (2026-11-19).** A primeira versão desta proposta afirmava que
`gen_semente.py` gera linha só para a base declarada, e que a semente nunca seria
procurada numa base omitida. Isso está errado. O script já gera uma linha por semente **e
por base da tabela de bases**, marcando `esperada_na_base` como `sim` ou `nao`, e a etapa 1
(coluna `indexada`) decide o denominador.

O risco que resta é menor:
- a seção 5 de cada ficha lista só as sementes declaradas para aquela base;
- a coluna `esperada_na_base = nao` pode induzir quem preenche a pular a etapa 1 naquela
  linha;
- a incidência por base que `--conferir` calcula sai errada.

Ação, independente da decisão sobre D1 e D2:
- conferir na fonte a indexação de cada semente em cada uma das quatro bases;
- corrigir a coluna "Bases" e a seção 5 das fichas;
- registrar a conferência.

### D4 — Metadado das sementes

Os dados bibliográficos das 10 sementes estão pendentes de conferência (`--pendencias`). A
SE10 trazia o DOI do volume dos anais, não o do capítulo; a ficha da WoS já registrava isso.
Cada referência se confere na fonte (skill `conferir-referencia`), e nada se preenche de
memória. Na implementação, o DOI do capítulo foi conferido no Crossref e registrado.

### D5 — Casamento por prefixo

A skill `teste-de-aderencia` declara que prefixo é indício, nunca acerto; o código o
contava como recuperação. A correção alinha o código à skill: o prefixo é impresso como
`[? ]`, não entra no numerador, e a conferência humana fica registrada na coluna `recuperada`
do instrumento.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-do-protocolo`: **condicional a D1 (a)**. A tabela do conjunto-semente ganha a
  coluna que declara o papel de cada semente (desenvolvimento ou validação), e a ausência
  ou o valor inválido reprova a leitura.
- `derivacao-das-expressoes`: **condicional a D1 (a)**. `--aderencia` calcula e relata
  separadamente a aderência de validação e a de desenvolvimento, e a planilha de aderência
  traz o papel de cada semente.

Se D1 (a) não for adotada, a change fica restrita ao texto do protocolo, das fichas e do
metadado das sementes, e passa a `skip_specs: true`.

## Impact

- `docs/03_protocolo_estrategia_pesquisa.md` — tabela do conjunto-semente.
- `data/sementes.json` — metadado de conferência, editado pelo pesquisador e reconciliado
  por `--sincronizar`.
- `docs/busca_base_*.md`, seção 5 — sementes esperadas em cada base.
- `src/protocolo.py`, `src/gen_semente.py`, `src/derivar_expressoes.py` — só em D1 (a).
- `.agents/skills/conjunto-semente/` e `teste-de-aderencia/` — procedimento, se D1 (a).
- `data/historico.md` — emenda.
- Interage com `revisao-das-strings-por-faceta`: termo incluído para recuperar uma semente
  a desqualifica como semente de validação.
