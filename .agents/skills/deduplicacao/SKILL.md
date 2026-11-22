---
name: deduplicacao
description: Deduplica os registros exportados das bases em duas passagens, por identificador e por semelhança, com regra explícita para o par duvidoso. Use ao consolidar exportações de mais de uma base, ao contar registros únicos, e ao decidir se dois registros são o mesmo estudo.
---

# Deduplicação

Quatro bases trazem o mesmo estudo com metadados diferentes. A deduplicação decide
quantos estudos **distintos** existem — número que depois entra no fluxograma PRISMA
e em toda contagem do relato.

## 1. Duas passagens, nesta ordem

**Primeira, por identificador.** Chave em cascata: `UT` (Web of Science) → `DOI` →
título normalizado. É a ordem de confiabilidade: o `UT` é único por base, o DOI é
único por documento, o título colide.

**Segunda, por semelhança**, sobre o que restou. É assistida, e é a passagem onde o
julgamento entra.

## 2. A regra que decide os casos difíceis

> **Par duvidoso NÃO é fundido.**

O par permanece como dois registros e a decisão é registrada. O custo de não fundir é
um registro a mais na triagem, que a filtragem resolve; o custo de fundir errado é um
estudo que desaparece do portfólio sem ninguém notar. Os dois custos não são
simétricos.

Casos que parecem duplicata e não são: pré-print e versão publicada; artigo de
conferência e sua extensão em periódico; erratum e artigo original; capítulo e artigo
homónimos do mesmo autor.

## 3. Conferência obrigatória

Os pares marcados como duplicata pela passagem assistida são **conferidos um a um**.
Nenhum par se funde por classificação automática sozinha. O registro de cada fusão
guarda as duas chaves originais, para que a contagem seja refazível.

## 4. O que a deduplicação não é

Não é **limpeza de metadados**. Registro com campo ausente continua ausente depois de
deduplicado — e essa ausência tem consequência própria: ver a cobertura de campo em
`conferencias-da-busca`. Medido aqui: 4 dos 64 registros da BRAPCI sem
palavras-chave, 6% de ponto cego.

Também não decide elegibilidade. Duplicata é identidade do documento, não pertinência.

## 5. Onde entra na cadeia

Depois da exportação, **antes** do teste de aderência — porque ele se mede sobre o
corpus deduplicado.

A aderência mede-se sobre a **união** das bases, que só existe depois de deduplicar.

## 6. Registrar

Por base: registros exportados. Após a 1ª passagem: duplicatas por `UT`, por `DOI`,
por título. Após a 2ª: pares marcados, fundidos e mantidos como distintos, com o
motivo. E o total de registros únicos, que é o número que segue para a 1ª filtragem.

Tudo isso vai para as contagens da busca e alimenta o fluxograma PRISMA.
