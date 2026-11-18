---
name: rastreabilidade
description: Confere e garante a correspondência entre os componentes da revisão — questão, objetivos, facetas, quadro terminológico, strings, critérios e remissões entre instrumentos. Use ao verificar se dois componentes concordam, ao fechar divergência entre documentos, e ao decidir como impedir que ela volte.
---

# Rastreabilidade entre componentes

Esta skill tem um princípio e o princípio é a skill:

> **Garantia por construção, não por conferência.** Havendo escolha entre impedir o
> defeito e detectá-lo depois, impedir. Conferência só encontra o que já aconteceu.

## 1. As correspondências que têm de valer

| De | Para | Garantida por |
| --- | --- | --- |
| questão secundária | objetivo específico | objetivo nomeia o tema da questão, conferido contra o protocolo (`docs/03`) |
| objeto | questão principal | as mesmas operações nomeadas |
| regra de inclusão | elegibilidade e 1ª filtragem | a mesma regra escrita nos três lugares |
| quadro terminológico | strings executadas | o mesmo vocabulário qualificado |
| facetas | expressões de busca | composição, não escrita à mão |
| seção do plano (`docs/01`) | remissão de outro instrumento | citação por chave, conferida ao alterar a seção |
| contra-escopo | critérios de exclusão | cada revisão autônoma com o seu critério |

## 2. O método, em quatro passos

1. **Achar a fonte comum.** Duas coisas que precisam concordar ou saem da mesma
   fonte, ou vão divergir. Se não há fonte comum, criá-la é o conserto.
2. **Medir a divergência corrente**, com número. "Há divergência" não é achado;
   "84 termos nas strings ausentes do quadro, 47 por supressão de plural e 37 por
   introdução na qualificação" é.
3. **Perguntar: o que impede que volte?** Se a resposta for "reler", não está fechado.
4. **Escrever a regra que impede o retorno** — uma fonte única, uma conferência
   obrigatória, uma remissão por chave — e demonstrar que ela reprova o defeito que a
   motivou. **Regra que nunca reprova não protege nada.**

## 3. As quatro correspondências críticas

- **Regra de inclusão** — problema que seja objeto desta revisão e carregue critério de
  exclusão; numeração descontínua; exclusão sem critério; recorte invertido; regra de
  inclusão que deixe de ser disjuntiva ou de alcançar a 1ª filtragem.
- **Quadro × strings** — quadro do protocolo montado a partir de vocabulário diferente do
  das strings.
- **Remissão de seção** — numeração do plano descontínua ou repetida; qualquer documento
  remetendo a seção extinta.
- **Notação compacta** — termo em notação de variante, com barra ou parêntese, sem
  desdobramento.

Some-se a defasagem: **documento coerente e velho em relação à fonte**. Nada o
denuncia senão a conferência.

**Não há guarda automática neste repositório.** O que impede o retorno do defeito é a
fonte única documental e a conferência registrada. Onde a conferência for manual,
dizê-lo no registro — não apresentá-la como garantia de construção.

**Erro de conferência não é defeito do documento.** É a incoerência apontada antes de
virar resultado. Corrigir a fonte, nunca afrouxar a conferência.

## 4. Três divergências reais, e o que as causou

- **Quadro × strings, 84 termos.** Causa única: ordem das operações. O quadro saía da
  lista registrada e as strings da qualificada. Conserto: o quadro passa a usar o mesmo
  vocabulário que as strings, com a redução ao singular aplicada depois e só na
  exibição.
- **Remissão a seção errada, dois meses sem detecção.** O protocolo apontava as fronteiras
  de uso da IA para a seção das pessoas da equipe. Conserto: citação por chave e
  conferência das remissões ao alterar a seção.
- **Objeto × questão, duas operações perdidas.** Conserto: harmonização e, para o
  futuro, a conferência objetivo↔questão.

Todas tinham a mesma forma: **a mesma informação escrita em dois lugares**.

## 5. Conferir

1. Percorrer as correspondências da §1 e apontar, para cada uma, o documento que é
   fonte.
2. Medir a divergência corrente, com número.
3. Registrar no histórico (`data/historico.md`) a decisão que a conferência motivar.
