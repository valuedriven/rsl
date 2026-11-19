# Design

## Context

A motivação e as decisões D1–D4 estão em `proposal.md`. Estado observado em 2026-11-19:

- `strings()` em `src/protocolo.py` lê cada STR como lista de termos entre aspas, por
  faceta. `--conferir` já verifica que todo termo de STR consta do quadro da sua faceta,
  mas não verifica se o mesmo termo aparece em outra STR.
- Sobreposição verificada no texto do protocolo: oito termos em STR2 e STR3 (en/pt/es) e
  `situação/situación de aprendizagem/aprendizaje` em STR2 e STR4.
- `expressoes_base()` lê cada `### EBn` da ficha e os blocos cercados dela, com rótulo
  (`_cercados`). Um segundo cabeçalho `### EB5 ...` sobrescreveria o primeiro, então a
  variante tem de ser um segundo bloco dentro da mesma seção, distinguido pelo rótulo.
- A exigência "Termos do bloco conferem com as facetas declaradas" vem da change
  `expressoes-literais-por-base`, ainda não arquivada. Esta change depende do arquivamento
  dela.
- `sensibilidade()` compara EB5 com EB4 por base, a partir das execuções registradas.
  `registrar()` identifica a expressão por `EBn` e não tem noção de variante.
- A exigência principal "Saídas preservadas" também é modificada pela change
  `conjunto-semente-independente`. Para não colidir, esta change não altera saída
  existente: só acrescenta uma saída quando a variante está registrada.

## Goals / Non-Goals

**Goals:**
- Facetas que não se satisfazem umas às outras, se o pesquisador escolher D1 (a).
- Uma medida da perda por proximidade, se o pesquisador escolher D4 (a).
- Decisões de D2 e D3 tomadas com números da primeira sondagem, não por suposição.

**Non-Goals:**
- Escolher termos. O agente propõe, mede e aponta consequências; a emenda é do
  pesquisador.
- Mudar a composição das expressões no protocolo. `EB4 = STR1 AND STR2 AND (STR3 OR STR4)`
  continua; D4 (a) é forma operacional da mesma `STR1 AND STR2`.
- Executar buscas. As medições dependem do registro de execução (PD02) e são feitas pelo
  pesquisador, conforme as fichas.

## Decisions

**D-a. Ordem: medir antes de emendar D2 e D3.** As duas hipóteses (EB4 ≈ EB5 por causa de
`practice`; perda por `conceptual model`) se resolvem com contagens de sondagem baratas,
feitas na primeira sessão em cada base. Emendar antes seria decidir no escuro.
Alternativa: emendar já pela regra da v2 (retirar termo genérico). Fica disponível ao
pesquisador como D2 (a), mas o design recomenda medir.

**D-b. Sondagens propostas para a primeira sessão (WoS e Scopus).** Cada uma é registrada
como execução fora do corpus:
1. contagem de EB4 e de EB5 como estão;
2. contagem de EB4 com STR3 sem `practice`, `prática` e `práctica`;
3. contagem de EB5 com STR1 acrescida de `conceptual model*`, menos EB5.

Os números entram no registro, e as decisões D2 e D3 citam a execução (`BDn/<id>`), o que
amarra a decisão ao lastro, como exige a change `higiene-de-rastreabilidade`.

**D-c. Disjunção das strings conferida em `--conferir` (D1 a).** A comparação normaliza
caixa e diacríticos, com a mesma normalização já usada pelo leitor. Alternativa: conferir
também os quadros. Foi rejeitada porque o quadro registra o vocabulário do conceito e pode
legitimamente listar o mesmo termo em duas facetas. O que define a busca é a STR.

**D-d. Critério para escolher a faceta que fica com o termo repetido.** Proposta ao
pesquisador: o termo fica na faceta cuja definição ele nomeia. `teaching strategy` nomeia
uma prática, então fica em FCT3, não no domínio; `situação de aprendizagem` nomeia um
fator, então fica em FCT4. Consequência a medir: STR2 perde termos e a âncora de domínio
fica mais estrita. A sondagem 1 de D-b, refeita após a emenda, mostra o efeito.

**D-e. Variante "sem proximidade" como segundo bloco da EB5 (D4 a).** O bloco fica na
mesma seção `### EB5`, com rótulo contendo "sem proximidade", e é registrado como EB5 com
variante declarada. Alternativas:
- expressão nova (EB6) na composição: foi rejeitada porque mudaria a composição do
  protocolo e a prova da composição por uma diferença que é só operacional;
- cabeçalho próprio: o leitor sobrescreveria a EB5.

**D-f. Ficha sem proximidade não leva a variante.** Bloco idêntico ao da sonda é
redundante e induz a registro duplicado. Reprovar a presença dele mantém a forma única.

## Risks / Trade-offs

- [D1 (a) retira de STR2 termos que hoje garantem o domínio a registros de prática] →
  esses registros continuam satisfazendo FCT3. Só os que dependiam do termo para
  satisfazer FCT2 saem de EB2, e a sondagem refeita mede quantos são.
- [A sonda sem proximidade multiplica o retorno a classificar] → a amostra segue o
  procedimento da sensibilidade (amostra, não universo), e a classificação é à mão,
  fora do corpus.
- [Emendar strings exige regenerar os blocos literais das quatro fichas] → a conferência
  "Termos do bloco conferem com as facetas declaradas" reprova o bloco defasado. A
  regeneração é guardada por construção.
- [Termo novo motivado por semente compromete a validação] → toda inclusão de termo cita,
  no histórico, se alguma semente a motivou, e `conjunto-semente-independente`
  reclassifica essa semente.
- [Dependência de change não arquivada] → a tarefa 1.1 verifica o arquivamento de
  `expressoes-literais-por-base` antes de começar.

## Migration Plan

1. Pré-requisitos: `expressoes-literais-por-base` arquivada; registro de execução criado
   (`higiene-de-rastreabilidade`, PD02).
2. Sondagens de D-b registradas pelo pesquisador.
3. Decisões D1–D4 registradas no histórico, citando as execuções.
4. Emenda do protocolo, conferências e regeneração das fichas, no mesmo passo para
   `--conferir` não ficar reprovado.
5. Validação terminológica reconciliada (`--importar`) se a planilha existir.

Nenhuma execução definitiva existe, então nenhuma contagem fica vencida.
