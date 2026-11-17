---
name: expressoes-de-busca
description: Compõe as expressões de busca a partir das facetas e as especializa na sintaxe de cada base, com a lógica de execução de cada uma. Use ao montar, alterar ou conferir expressão de busca e string, ao decidir o que se executa e o que se calcula localmente, e ao tratar de operador de proximidade, truncamento, teto de caracteres ou filtro de ano.
---

# Expressões de busca

Duas partes do mesmo ato: a **lógica**, que é independente de base, e a **sintaxe**,
que é medida base a base. Separá-las convida a escrever string para uma base sem a
lógica que a governa.

## Parte 1 — a lógica

### Composição e contenção

Com duas facetas-âncora (1 e 2) e duas temáticas (3 e 4):

```
E1 = 1+2+3+4     E2 = 1+2+3     E3 = 1+2+4     E4 = 1+2
E1 ⊆ E2 ⊆ E4     E1 ⊆ E3 ⊆ E4     E1 = E2 ∩ E3
```

Logo `|E2| ≤ |E4|`, `|E3| ≤ |E4|` e `|E1| ≤ min(|E2|, |E3|)`. A contenção não é
observação: é **consequência da composição**, e é por isso que serve de conferência.

**"Geral" nomeia a composição, não o alcance.** E1 exige as quatro facetas e é a mais
restritiva — o menor dos quatro conjuntos. Serve de sonda de precisão máxima, nunca
de critério de exclusão.

### Os três estados de execução

Dizer que uma expressão "não se executa" é ambíguo, e o parecer externo apanhou isso.
São três estados, e o quadro do IO 1 os distingue:

1. **Busca definitiva nas bases** — a execução cujo retorno compõe o corpus. Só E4.
2. **Execução experimental de aferição** — execução direta na base só para medir a
   fidelidade da derivação; o retorno é descartado após a comparação. E2 e E3, no
   teste de fidelidade.
3. **Pertinência calculada localmente** — a expressão não vai à base; a contagem sai
   da aplicação dos seus termos aos registros já exportados, por
   `src/derivar_expressoes.py`.

### Por que só E4 vai à base

E4 é a expressão de **cobertura**: a mais larga, e a única cujo retorno é o corpus.
As demais derivam-se dela localmente, o que poupa execuções e torna a contagem
reprodutível. O preço é que a derivação precisa ser aferida — ver
`conferencias-da-busca`.

E o preço de E4 ser larga está medido: **56,0% dos registros únicos da Web of Science
e 57,5% da Scopus não trazem termo algum das facetas de práticas e de fatores
situacionais** em título, resumo ou palavras-chave. É por isso que o critério da 1ª
filtragem exige pelo menos uma das duas dimensões.

## Parte 2 — a sintaxe, por base

**Medida, não documentada.** A tabela completa está nas fichas por base, em
`docs/`; o que não se pode esquecer:

| Base | Medido |
| --- | --- |
| **ERIC** | **não trunca** — `ontolog*` devolve 0; lematiza plural regular; teto de caracteres medido entre 1.502 e 1.799, regra de bolso 1.400; campo `descriptor:` |
| **BRAPCI** | aspas, AND/OR, parênteses, truncamento; **teto de 1.000 registros no retorno**; consultas curadas à mão, não geradas das facetas |
| **Web of Science** | `TS=`, `NEAR/5`, `PY=(2017-2026)`, `DT=` |
| **Scopus** | `TITLE-ABS-KEY`, `W/5`, `PUBYEAR`, `LANGUAGE`, `DOCTYPE` |

Três regras que saíram de defeito real:

- **Filtro de ano confere-se no RETORNO, não na consulta.** Uma exportação da Scopus
  trouxe 8 registros de 2027 sob filtro que se supunha fechado — `PUBYEAR > 2016` sem
  o limite superior.
- **Simetria entre expressões.** Operador de proximidade e filtro de tipo de documento
  aplicados a E4 e não a E2 produziram `E2 > E4`, que é impossível. Era defeito da
  ficha, não do motor.
- **Partição por teto tem de ser exacta**: âncoras idênticas nas duas partes, termos
  temáticos disjuntos, união igual à expressão original. A exactidão verifica-se à
  mão, parte a parte.

## Depois de compor

As fichas, uma por base, ficam em `docs/` com a expressão executável e o
estado de verificação da sintaxe. O **registro de execução** fica em
`data/registro_execucao.json`, uma entrada por base. **Nunca ditar uma expressão
de memória nem reescrevê-la na conversa** — se a ficha estiver defasada, corrigi-la.

Alteração de expressão é emenda **de busca**: exige reexecução e novo teste de
aderência. `busca-nas-bases` para executar, `registrar-decisao` para o Anexo A.
