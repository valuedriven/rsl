---
name: expressoes-de-busca
description: Compõe as expressões de busca a partir das facetas e as especializa na sintaxe de cada base, com a lógica de execução de cada uma. Use ao montar, alterar ou conferir expressão de busca e string, ao decidir o que se executa e o que se calcula localmente, e ao tratar de operador de proximidade, truncamento, plural e lematização, teto de caracteres ou filtro de ano como parâmetros da base.
---

# Expressões de busca

Duas partes do mesmo ato: a **lógica**, que é independente de base, e a **sintaxe**,
que é medida base a base. Separá-las convida a escrever string para uma base sem a
lógica que a governa.

## Parte 1 — a lógica

### Composição e contenção

Com duas facetas-âncora (1 e 2) e duas temáticas (3 e 4):

```
EB1 = 1 AND 2 AND 3 AND 4     EB2 = 1 AND 2 AND 3     EB3 = 1 AND 2 AND 4
EB4 = 1 AND 2 AND (3 OR 4)                            EB5 = 1 AND 2
EB1 ⊆ EB2 ⊆ EB4     EB1 ⊆ EB3 ⊆ EB4     EB4 = EB2 ∪ EB3     EB5 ⊃ EB4
```

Logo `|EB1| ≤ min(|EB2|, |EB3|) ≤ |EB4| ≤ |EB5|`. A contenção não é observação: é
**consequência da composição**, e é por isso que serve de conferência. A união das
específicas é igual à de cobertura porque o grupo temático é uma disjunção — é a
álgebra que faz a derivação local valer a execução.

**"Geral" nomeia a composição, não o alcance.** EB1 exige as quatro facetas e é a mais
restritiva — o menor dos cinco conjuntos. Serve de sonda de precisão máxima, nunca
de critério de exclusão.

### Os três estados de execução

Dizer que uma expressão "não se executa" é ambíguo, e o parecer externo apanhou isso.
São três estados, e o quadro terminológico do protocolo (`docs/03`) os distingue:

1. **Busca definitiva nas bases** — a execução cujo retorno compõe o corpus. Só EB4.
2. **Execução experimental de aferição** — execução direta na base só para medir a
   fidelidade da derivação; o retorno é descartado após a comparação. EB2 e EB3, no
   teste de fidelidade.
3. **Sonda de sensibilidade** — EB5 vai à base uma vez, fora do corpus, para medir
   quanto a restrição de EB4 custa em alcance. A fração elegível da perda decide.
4. **Pertinência calculada localmente** — a expressão não vai à base; a contagem sai
   da aplicação dos seus termos aos registros já exportados, por
   `busca derivar` (`src/rsl/busca/`).

### Por que só EB4 vai à base

EB4 é a expressão de **cobertura**: a mais larga da busca definitiva, e a única cujo
retorno é o corpus. As demais derivam-se dela localmente, o que poupa execuções e
torna a contagem reprodutível. O preço é que a derivação precisa ser aferida — ver
`conferencias-da-busca` —, e a decisão de restringir EB5 a EB4 se mede pela sonda.

O preço de EB4 ser larga se mede, não se presume. A medida é a fração dos registros únicos da
executada sem termo algum das facetas temáticas em título, resumo ou palavras-chave. Uma
medida anterior deste projeto deu mais da metade, mas não tem execução registrada no
repositório: refazê-la na primeira execução e citar a execução. É essa fração que justifica
exigir, já na 1ª filtragem, pelo menos uma das duas dimensões.

## Parte 2 — a sintaxe é parâmetro da base

**Medida, não documentada, e declarada na ficha da base.** Esta skill não traz a sintaxe
de base alguma. O que difere de uma base para outra é parâmetro: apurado e registrado na
seção 1 da ficha (`ficha-de-busca-por-base`) e, quando governa a composição, declarado na
declaração de cobertura, onde `conferir` o lê.

| Parâmetro | Onde se declara | Como governa a composição |
| --- | --- | --- |
| **plural** | declaração de cobertura: `explícito` ou `pela lematização` | `explícito`: a string traz as duas formas de número, ou um truncamento que as alcance. `pela lematização`: só a forma do quadro, e só com a lematização medida e a execução citada na seção 1 |
| **teto de caracteres** | declaração de cobertura: número inteiro ou `nenhum` | com número, nenhuma consulta executável passa dele, e o que passa se particiona sem retirar termo. `conferir` mede cada bloco e reprova a base. Com `nenhum`, `conferir` relata a maior consulta |
| **truncamento** | seção 1 | curinga que a base não aceita, ou que devolve zero, não se usa: a forma vai por extenso |
| **proximidade** | seção 1; a discussão, na subseção "Estratégia de proximidade" da ficha | operador, distância e grupos de cada lado medidos antes de usar. Vale para todas as expressões ou para nenhuma |
| **campo** | seção 1 e cabeçalho de cada string | o campo da string é lido do texto; prefixos diferentes na mesma string são "misto" |
| **filtros** | seção 2 | na consulta ou na interface, conforme a base admite; o ano se confere no retorno |
| **teto de retorno** | seção 1 | retorno exatamente no teto é corte até prova em contrário: particionar |

**O teto não exige medição citada, ao contrário de `pela lematização`.** Um teto baixo
demais custa partição, não recall. Um teto alto demais aparece como recusa da interface. A
origem do número fica na linha "Comprimento máximo da consulta" da seção 1, com o seu estado
de verificação. Regra de bolso é declarada como regra de bolso.

Três regras que saíram de defeito real:

- **Filtro de ano confere-se no RETORNO, não na consulta.** Uma exportação trouxe
  registros do ano seguinte sob filtro que se supunha fechado: a cláusula tinha só o
  limite inferior.
- **Simetria entre expressões.** Operador de proximidade e filtro de tipo de documento
  aplicados a EB4 e não a EB2 produziram `EB2 > EB4`, que é impossível. Era defeito da
  ficha, não do motor.
- **Partição por teto tem de ser exata**: âncoras idênticas em todas as partes, termos
  temáticos disjuntos, união igual à expressão original. O comprimento de cada parte
  `conferir` mede. A exatidão da partição ainda se verifica à mão, parte a parte.

## Depois de compor

As fichas, uma por base, ficam em `docs/` com a expressão executável e o
estado de verificação da sintaxe. O **registro de execução** fica em
`data/registro_execucao.json`, uma entrada por base. **Nunca ditar uma expressão
de memória nem reescrevê-la na conversa** — se a ficha estiver defasada, corrigi-la.

Alteração de expressão é emenda **de busca**: exige reexecução e novo teste de
aderência. `busca-nas-bases` para executar, `registrar-decisao` para o histórico
(`data/historico.md`).
