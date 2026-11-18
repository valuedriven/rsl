---
name: strings-por-base
description: Compõe, confere e mantém a string de busca específica de cada base — o que a forma da base pode mudar em relação ao protocolo, o que não pode, e como declarar a redução. Use ao montar ou revisar a ficha de uma base, ao conferir a ficha contra o protocolo, ao decidir se um termo ausente é omissão ou redução declarada, e ao tratar de divergência entre a ficha e o vocabulário do protocolo.
---

# Strings por base

A string de uma base **não é a do protocolo com outro invólucro**. As bases divergem do
vocabulário canônico em conteúdo: uma acrescenta flexão morfológica, outra reduz a radicais,
outra usa só o núcleo e executa por consultas curadas. Tratá-las como cópias produziria a
sintaxe de uma com o vocabulário suposto de outra.

> **Duas fontes, com papéis distintos.** O **vocabulário** é do protocolo; a **forma** é da
> ficha da base. Mudar uma sem revisitar a outra é defeito que só aparece depois de a busca
> já ter sido executada.

## Onde cada coisa vive

| Peça | Lugar | Estatuto |
| --- | --- | --- |
| vocabulário por faceta, camadas e idiomas | IO 1 | fonte |
| forma: campo, operadores, filtros, variantes | ficha da base | fonte |
| declaração de cobertura | ficha, seção de strings | fonte, autoral |
| retorno de cada execução | registro de execução | autoral |

Não há derivado por base em `data/`: a forma é lida da ficha a cada execução. O que se
guarda é o que alguém alimenta — o retorno de cada execução e a declaração de cobertura.

## O que a forma pode mudar

Legítimo, e sempre declarado na ficha, nunca na memória de quem executa: **campo** (tópico,
título-resumo-palavras-chave, título, resumo, descriptor); **proximidade** e a distância
medida; **truncamento** — há base em que o curinga devolve zero; **teto de caracteres** e
**teto de retorno**, que vira partição ou lista curada, e a partição tem de ser exata;
**filtro de ano**, na consulta ou no filtro da página, e onde os dois existirem o ano
confere-se no retorno; **idioma indexado**; **camada do vocabulário**, integral, núcleo ou
radicais; **morfologia**, sobre termo que já consta; **forma de execução**, uma consulta,
duas por campo unidas por deduplicação, ou lista curada executada consulta a consulta.

## O que a forma não pode mudar

- **Termo do protocolo ausente sem declaração.** Ausência declarada é decisão com preço
  medido; silenciosa é omissão.
- **Âncora obrigatória.** Expressão sem âncora não é a mesma busca com menos facetas: é
  outra busca.
- **Composição e contenção.** As cinco expressões mantêm a composição de facetas do
  protocolo: `EB4 = EB2 ∪ EB3` e `EB5 ⊃ EB4`. A de cobertura continua igual à união das
  duas específicas, e a sonda continua contendo a de cobertura.
- **Simetria de filtros.** Proximidade e filtro de tipo valem para todas. Aplicá-los a uma
  só já produziu específica maior que a de cobertura — impossível, e era defeito da ficha,
  não do motor.
- **Termo que não derive do protocolo.** Palavra nova só com decisão registrada.

## A declaração de cobertura

É o que transforma "a string é menor" em "a string é menor **por isto**": tabela legível por
máquina, na ficha, com quatro parâmetros — **idiomas** por faceta, **camadas** (integral ou
núcleo), **derivações** (`morfologia` e/ou `radical`) e **exclusões** termo a termo.

`morfologia` reconhece flexão de número e gênero, não lematização. `radical` declara que uma
palavra-raiz presente alcança a expressão inteira — é regra declarada, não equivalência.

**Toda exclusão tem motivo**, e motivo que ainda não é decisão se escreve como lacuna
pendente: a diferença aparece em `--pendencias` e é o que permite reabrir o assunto.

## Gerar, conferir, provar

- `--conferir-dados` confere a ficha contra o protocolo — campo, redução declarada e
  cobertura — e reprova uma base sem congelar as outras: a forma de uma base não congela o
  resto.
- `--sincronizar` não toca na ficha; só reconcilia o que é alimentado em `data/`.
- `--autoteste` injeta defeitos — termo retirado, termo inventado, faceta trocada, declaração
  restringida. Conferência que nunca reprovou não protege nada.
- `--pendencias` relata a lacuna declarada e pendente, sem escrever.

## Cobertura é número, não aprovação

A cobertura mede quanto do vocabulário declarado está na string e se decompõe em literal,
alcançado por radical, declarado e descoberto. Não mede recall: recall é outra conta, com
outro denominador. Nunca apresentar cobertura alta como aderência, nem cobertura baixa como
falha — base que reduz vocabulário assume perda de recall, e o número declara a perda. Quem
decide se o preço é aceitável é o teste de aderência.

## Quando a ficha divergir do protocolo

1. **Identificar o que mudou**: vocabulário, forma, ou só declaração.
2. **Vocabulário ou forma mudaram** → revisar a ficha; termo novo entra ou entra na redução
   declarada, com motivo. Mudança que altere a recuperação exige nova execução e novo teste
   de aderência: é emenda de busca.
3. **Só a declaração mudou** → conferir; não há execução a repetir, mas há decisão a
   registrar.
4. **Registrar sempre** no Anexo A. Divergência fechada em silêncio volta na execução
   seguinte.

## Remissões

Lógica das expressões e leitura da sintaxe medida: `expressoes-de-busca`. Executar e
registrar, sob as regras de acesso institucional: `busca-nas-bases`. Coerência, fidelidade e
cobertura de campo: `conferencias-da-busca`. Recall contra o conjunto-semente:
`teste-de-aderencia`. Emenda e propagação: `registrar-decisao`. Bases, limiares, recorte e
nomes de arquivo deste projeto estão no `README.md`, e não se repetem aqui.
