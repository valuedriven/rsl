# Proposal

## Why

A revisão geral de 2026-11-19 encontrou nas strings do protocolo
(`docs/03_protocolo_estrategia_pesquisa.md`, "Strings de busca por faceta") quatro
problemas que afetam o que a expressão executada EB4 recupera e o que a sonda EB5 consegue
medir. Nenhuma execução foi registrada: mudar as strings agora não invalida nenhuma
contagem, e depois da primeira execução definitiva qualquer mudança vira emenda com
reexecução.

Esta change **não decide** as questões abaixo. Ela as apresenta com as alternativas e as
suas consequências, porque decidir sobre a busca cabe ao pesquisador (AGENTS.md §4).

## What Changes

### D1 — Termos repetidos em mais de uma faceta (verificado no texto)

> **Atualização de 2026-11-20 (change `reestruturacao-do-protocolo`).** O pesquisador
> retirou 23 termos do quadro de FCT2, e STR2 e as strings de FCT2 das fichas foram
> alinhadas a ele. Saíram de STR2 todos os termos repetidos listados abaixo, além de treze
> sem par em outra faceta (registro em `data/historico.md`, 2026-11-20). Para STR2, a
> alternativa adotada na prática foi a (a). Falta decidir se a conferência deve reprovar
> a repetição entre facetas, e o efeito sobre EB2/EB3 e sobre a aderência ainda não foi
> medido.

O mesmo termo aparece em strings de facetas diferentes:

- STR2, que é a âncora do domínio educacional, contém `teaching practice`, `teaching method`,
  `teaching strategy`, `learning design`, `método de ensino`, `estratégia de ensino`,
  `método de enseñanza` e `estrategia de enseñanza`, que também estão em STR3;
- `situação de aprendizagem` e `situación de aprendizaje` estão em STR2 e em STR4.

**Efeito.** Um único termo satisfaz duas facetas. Um registro com "ontology" e "teaching
strategy" passa em EB2, embora ninguém tenha mencionado o domínio por um termo próprio. A
âncora FCT2 fica mais fraca, e o estrato E1/E2 da triagem fica menos discriminante.

Alternativas:
- **(a)** cada termo pertence a uma só faceta. O termo sai da faceta em que é menos
  característico, e uma conferência reprova a repetição;
- **(b)** manter a sobreposição como intencional e declará-la no protocolo e no relato,
  com o efeito sobre EB2/EB3;
- **(c)** decidir caso a caso, registrando cada termo mantido em duas facetas.

### D2 — `practice`, `prática` e `práctica` isolados em STR3

A emenda v2 tirou termos genéricos de STR1 e STR2 pelo critério de frequência, mas manteve
em STR3 a forma isolada desses termos, que é de altíssima frequência e polissêmica ("in
practice").

**Hipótese, ainda não medida.** STR3 é satisfeita por quase todo registro que já satisfaz
STR1 e STR2. Nesse caso EB4 ≈ EB5, a restrição da v2 rende pouco, e `EB5 \ EB4` sai pequena
por um motivo trivial.

**Medição que decide.** Comparar as contagens de EB4 e de EB5 na primeira sondagem, e as de
EB4 com e sem a forma isolada.

Alternativas:
- **(a)** retirar a forma isolada, mantendo as compostas;
- **(b)** manter e registrar a justificativa;
- **(c)** decidir depois da medição.

### D3 — "Modelo conceitual" fora de STR1

A questão geral nomeia "modelos conceituais" em primeiro lugar. A v2 retirou
`modelo conceitual`, `conceptual model`, `conceptual modeling` e equivalentes; a decisão
está registrada. Com isso, a faceta P cobre, na prática, ontologias e sistemas de
organização do conhecimento, mais `domain model`.

Alternativas:
- **(a)** declarar a cobertura reduzida como limitação no protocolo e no relato;
- **(b)** reintroduzir os termos sob proximidade mais estreita, ou só em título e
  palavras-chave, medindo o ganho contra o volume;
- **(c)** medir antes a perda: contar quanto a forma com `conceptual model` acrescenta à
  sonda.

### D4 — A sonda EB5 não mede a perda por proximidade

Na WoS e na Scopus, as âncoras se combinam por `NEAR/5` / `W/5`, e EB5 usa a mesma
proximidade. Por isso `EB5 \ EB4` não mede o que a proximidade exclui; só as 10 sementes
detectam essa perda. Na ERIC e na BRAPCI não há proximidade, de modo que a mesma expressão
do protocolo tem definição operacional diferente conforme a base.

Alternativas:
- **(a)** acrescentar uma sonda sem proximidade (`STR1 AND STR2`, executada uma vez, fora
  do corpus) na WoS e na Scopus;
- **(b)** declarar a heterogeneidade entre bases e confiar na aderência;
- **(c)** retirar a proximidade.

### Hipótese a conferir — SE4

O título é "Domain Model for **Learning and Teaching**", e STR2 tem só `teaching and
learning`. A recuperação depende então do resumo. Conferir na fonte antes de decidir se
entra a ordem inversa.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-do-protocolo`: **condicional a D1 (a)**. `--conferir` reprova termo que conste
  de STR de mais de uma faceta, nomeando o termo e as facetas, e o autoteste injeta o
  defeito.
- `cobertura-por-base`: **condicional a D4 (a)**. Ficha que combina as âncoras por
  proximidade SHALL trazer também o bloco literal da sonda sem proximidade. A composição do
  protocolo não muda: é a mesma `STR1 AND STR2`, em outra forma operacional.
- `derivacao-das-expressoes`: **condicional a D4 (a)**. `--sensibilidade` relata
  separadamente a perda por restrição (`EB5 \ EB4`) e a perda por proximidade (sonda sem
  proximidade menos sonda com proximidade).

Se nenhuma dessas alternativas for adotada, a mudança fica restrita ao texto do protocolo
e das fichas, e a change passa a `skip_specs: true`.

## Impact

- `docs/03_protocolo_estrategia_pesquisa.md` — quadro terminológico e strings.
- `docs/busca_base_*.md` — strings e blocos literais das quatro fichas, regenerados a partir
  do protocolo.
- `data/historico.md` — emenda com data, alcance e fundamento.
- `data/validacao_termologica.csv` — reconciliada por `--importar`, quando existir.
- `src/protocolo.py`, `src/derivar_expressoes.py` — só nas alternativas condicionais.
- Depende de: `higiene-de-rastreabilidade` (registro de execução) para as medições de D2 e
  D3. Interage com `conjunto-semente-independente`: termo incluído para recuperar uma
  semente compromete o uso dessa semente na validação.
