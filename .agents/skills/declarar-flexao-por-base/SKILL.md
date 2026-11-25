---
name: declarar-flexao-por-base
description: "Complementa a geração do procedimento de busca (`gerar-procedimento-de-busca`): declara, por base e por idioma, como o plural dos termos da string chega à busca, pela forma explícita ou pela lematização medida, e julga os termos que a regra regular não flexiona (plural irregular, não contável, forma vetada). Use ao declarar o plural de uma base, ao revisar as formas de número que a geração acrescenta, ao propor exceções de flexão e quando um termo aparece numa só forma de número."
---

# Flexão de número por base

O plural é recall. Um termo buscado só no singular, numa base que não lematiza, perde os
estudos que só usam o plural, e a perda não aparece em lugar nenhum: o retorno é menor e
parece correto. Esta skill decide como cada base alcança o plural e julga os termos que a
regra não resolve.

## 1. Plural explícito ou lematização

Para cada base e **para cada idioma** em que a base é buscada, há duas formas de alcançar o
plural:

- **explícito:** a string traz as duas formas de número;
- **pela lematização:** a base casa singular e plural por conta própria.

A declaração é `[cobertura] plural` da fonte do procedimento da base, com valor único ou por
idioma: `explícito` — o gerador acrescenta a forma de número por regra e pelas exceções
declaradas — ou `pela lematização`, que exige o elemento de `lematizacao` medido e citado para
aquele idioma; sem isso, `documentos conferir` reprova a base.

O padrão é o **explícito**. A lematização só se declara quando foi **medida** naquela base,
naquele idioma, por sondagem registrada (ver `executar-sondagens-de-sintaxe`): o controle no
singular, o teste no plural, e a leitura que os distingue. A afirmação da documentação da
base, ou a lematização medida em outro idioma, não bastam.

Lematização medida não é garantia de tudo: ela pode não alcançar plural irregular, termo
entre aspas ou locução. Quando a sondagem mediu só o termo simples, a declaração vale para o
que se mediu, e o resto continua explícito ou vira nova sondagem.

O custo do explícito é o comprimento da consulta. Numa base com teto de caracteres, mais
formas significam mais partes; isso é aceitável, e não justifica declarar uma lematização
não medida.

## 2. Termos que a regra não decide

A geração aplica a regra regular de cada idioma. Quando a terminação admite mais de um
plural, quando a palavra é de classe adjetiva, quando o termo tem conjunção ou preposição
que muda o núcleo, a regra **não escolhe**: o termo fica indecidível, e reprova a geração,
até haver exceção declarada. A decisão é do pesquisador; o agente propõe, com a origem.

Três tipos de exceção:

- **irregular:** o plural não segue a regra (`thesaurus` → `thesauri`; locução em que o
  modificador concorda, `padrão de projeto pedagógico` → `padrões de projeto
  pedagógicos`). A forma vem de dicionário, do uso nos estudos do domínio ou do
  vocabulário controlado da área;
- **não contável:** o termo nomeia processo, área ou disciplina e não se usa no plural
  (`educação`, `ensino superior`, `conceptual modeling`). Adjetivo isolado também não tem
  número;
- **vetada:** a regra produziria uma forma que não se usa, ou que muda o sentido; ela é
  retirada sem pôr outra no lugar.

**A origem é obrigatória.** "Proposta do agente" é origem válida, desde que o pesquisador
a revise antes da gravação; dicionário, vocabulário controlado ou o uso medido num conjunto
de estudos são origens melhores. Origem vaga ("comum") não é origem.

**Coerência entre idiomas.** O mesmo conceito tende a ter o mesmo tratamento nos três
idiomas: se `conceptual modeling` é não contável, `modelagem conceitual` e `modelado
conceptual` também tendem a ser. Divergência deliberada se justifica na origem.

**Plural de loanword.** Palavra estrangeira dentro de termo em outro idioma (`online` em
`aprendizagem online`) não recebe a flexão do idioma do termo; a regra a flexionaria e
erraria, e a exceção corrige.

## 3. Termo numa só forma de número

Em idioma de plural explícito, termo da string que aparece numa só forma de número é
defeito, salvo quando:

- é não contável ou tem forma vetada, declarados nas exceções;
- um truncamento declarado e medido o alcança.

Onde o termo se escreve à mão (subconjuntos, forma curada), a falta do plural é o erro mais
provável; o termo só no singular na forma curada reprova. Corrige-se acrescentando a forma ou declarando a exceção; nunca afrouxando a
conferência.

## 4. O que conferir no ensaio da geração

Antes de gravar, o ensaio lista, por faceta e idioma, cada forma de número acrescentada e a
sua origem (regra ou exceção). Conferir:

- formas erradas pela regra (concordância, acento, loanword);
- formas corretas mas sem uso, que só alongam a consulta: candidatas a não contável;
- termos cuja forma de número já é outro termo da string (`thesauri` de `thesaurus`):
  não se flexionam de novo;
- termos que deixaram de aparecer: a geração não pode perder termo da string.

As formas acrescentadas mudam a busca. Elas entram no registro de decisões, para que o
efeito delas apareça no teste de aderência da execução seguinte.
