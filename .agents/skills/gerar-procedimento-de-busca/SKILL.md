---
name: gerar-procedimento-de-busca
description: "Gera o procedimento de busca de cada base a partir da fonte (M3/E1): escreve a fonte do procedimento (pasta da base, `[documentos] procedimento_fonte`; sigla da tabela \"Bases de dados\" do protocolo) — declaração de cobertura, composição, forma de execução, variantes e ressalvas —, gera o procedimento e o confere contra o protocolo. Use ao montar o procedimento de busca de uma base nova, ao propagar emenda do protocolo aos procedimentos de busca, ao incorporar sintaxe recém-verificada, ao auditar se uma fonte está completa, ao decidir se um termo ausente da string é omissão ou redução declarada, e ao tratar de divergência entre o procedimento e o vocabulário do protocolo."
---

# Procedimento de busca por base

O procedimento de busca é o **protocolo de busca de uma base**: diz como o vocabulário, as expressões e os
critérios do protocolo se executam **naquela** base e com que evidência se sabe que ela
aceita o que se submete. Não é cópia do protocolo com outra sintaxe, nem manual da base.

A string de uma base **não é a do protocolo com outro invólucro**. As bases divergem do
vocabulário canônico em conteúdo: uma acrescenta flexão morfológica, outra reduz a radicais,
outra deixa termos fora da string, declarados um a um, e executa por consultas curadas. Tratá-las como cópias produziria a
sintaxe de uma com o vocabulário suposto de outra.

> **Duas fontes, com papéis distintos.** O **vocabulário** é do protocolo; a **forma** é da
> fonte do procedimento da base. Mudar uma sem revisitar a outra é defeito que só aparece
> depois de a busca já ter sido executada.

## Fonte e procedimento: escreve-se a fonte, gera-se o procedimento

O procedimento de busca (`docs/procedimentos_busca_<sigla>.md`) é **saída de geração** e
**nunca se edita**. Edita-se a **fonte** da base — a pasta que `[documentos]
procedimento_fonte` aponta —, com dois tipos de arquivo:

- `procedimento.toml`, de esquema fechado: sintaxe e roteiro de sondagens, critérios,
  declaração de cobertura, composição, execução, regras de montagem, sementes e ressalvas;
- fragmentos de prosa com nome fixo (`como_executar.md`, obrigatório; `variantes.md`,
  `estrategia_de_proximidade.md`, `notas_sintaxe.md`, `notas_execucao.md`,
  `notas_sementes.md`), que entram em lugar fixo do procedimento.

O esquema, os domínios, os fragmentos admitidos e o que reprova cada um estão em `python3 -m
rsl documentos gramatica`; não se repetem aqui. Os blocos de termos (strings e expressões)
**não se escrevem**: o gerador os compõe da STR do protocolo, com a flexão de número
(`declarar-flexao-por-base`) e a forma declarada na fonte.

A ordem é sempre: quadro terminológico → `strings gerar` → fonte → `procedimentos gerar`
(ensaio, revisado) → `procedimentos gerar --gravar` → `documentos conferir`. O procedimento
editado à mão reprova na conferência por igualdade; a correção é na fonte.

## O procedimento de busca é operacional

O procedimento de busca diz **como executar a busca naquela base, na forma vigente** — e nada além disso.
Quem o abre para executar não deve ter de separar a instrução do racional.

- **Só a decisão final.** Nada de histórico: sem datas de decisão, sem "vigente desde", sem
  "retirado em", sem forma anterior, sem retornos vencidos, sem numeração explicada por
  consulta removida. O histórico vai a `data/historico.md`; o estado da execução, ao
  registro de execução.
- **Sem informação de exclusão.** Termo retirado por emenda **não se lista** na fonte: o
  vigente é a string (STR) do protocolo, e o termo que só consta do quadro terminológico não
  é esperado na base. Termo alcançado pela forma radical também não se lista. `[[reducao]]`
  só existe quando a **própria base** deixa fora da string um termo vigente, uma linha por
  termo, motivo curto.
- **Sem justificativa.** Regra, disparo, forma e limiar — não o porquê. O racional de uma
  decisão está no protocolo ou no histórico; o procedimento não o repete. Uma frase de contexto só
  entra quando sem ela a instrução seria executada errado.
- **Número em prosa não entra** nos fragmentos se o gerador o calcula (quantos termos,
  quantas consultas, comprimento de cada consulta): a cópia defasa.

Esta skill cuida do **procedimento de busca inteiro**, pela fonte: o que registrar, em que
ordem montar e como conferir. O que vai em cada parte da fonte é de outras skills, uma por
passo, e se lê a que couber antes do passo correspondente: a sintaxe e as sondagens, de
`executar-sondagens-de-sintaxe`; os critérios por base, de `definir-criterios-de-elegibilidade`;
a lógica das expressões e o que a forma da base pode mudar, de `elaborar-expressoes-de-busca`;
o plural, de `declarar-flexao-por-base`; as sementes, de `definir-conjunto-semente`; a execução e
o registro dos retornos, de `executar-expressoes-de-busca`.

## Antes de começar: qual é a operação

| Operação | Disparo | O que muda no procedimento |
| --- | --- | --- |
| **Procedimento novo** | base nova nas fontes do protocolo | tudo; exige a base já registrada no protocolo; começa por `python3 -m rsl procedimentos iniciar <sigla>`, e a lista de marcas `PENDENTE` da fonte criada é a lista de trabalho |
| **Propagação de emenda** | mudou vocabulário, expressão, critério ou recorte no protocolo | as seções afetadas; mudança que altere a recuperação é emenda de busca |
| **Sintaxe nova** | documentação consultada ou sondagem registrada | `[[sintaxe]]` e o que dela depende |
| **Auditoria** | pedido de revisão ou divergência encontrada | nada, até o pesquisador decidir; relatar |

**Quando o procedimento divergir do protocolo**, identificar primeiro o que mudou:

- **vocabulário ou forma** → revisar o procedimento: termo novo entra na string ou na redução
  declarada, com motivo. Mudança que altere a recuperação exige nova execução e novo teste
  de aderência: é emenda de busca;
- **só a declaração** → conferir; não há execução a repetir, mas há decisão a registrar.

No primeiro caso, registrar a emenda no histórico (`data/historico.md`). Divergência fechada em silêncio volta na execução
seguinte.

**Base nova é decisão de escopo** — fontes de informação são do protocolo, e o pesquisador
decide. Sem a base registrada no protocolo (`BDn`, nome, justificativa), não há procedimento
a criar: apresentar a lacuna e pedir a decisão.

## Ler antes de escrever

Na ordem, e sempre a **versão corrente** — o procedimento pode ter sido editado pelo pesquisador
desde a última leitura, e essa edição é o ponto de partida:

1. `README.md` — mapa, nomes de arquivo e precedência; `docs/procedimentos.md` — comandos;
   `python3 -m rsl configuracao mostrar` — limiares em uso e a origem de cada um.
2. O protocolo de estratégia: questão, facetas e âncoras, controle terminológico por linha e
   idioma, strings, expressões (a executada e a sonda, identificadas pela composição) e as
   suas notas, critérios de elegibilidade e fontes; o conjunto-semente vem do arquivo de
   sementes (`[documentos] sementes`). **É a fonte do vocabulário**; nada dele se reescreve
   de memória.
3. O protocolo de informações gerais: recorte e objeto, para os critérios de domínio.
4. O histórico: decisões já tomadas sobre esta base — reduções, variantes adotadas, defeitos
   que já ocorreram.
5. O registro de execução da base: sondagens medidas, estado da interface, retornos.
6. A fonte atual da base, se existir, e **a de outra base** como referência de estrutura —
   sem lhe copiar a sintaxe. O procedimento gerado mostra o resultado, não o que se edita.

## Passo 1 — a sintaxe da base: `[[sintaxe]]` e `[[sondagens]]`

O que apurar, onde pesquisar, a situação de cada elemento com a evidência exigida e o roteiro
de sondagens: `executar-sondagens-de-sintaxe`.

## Passo 2 — levar cada critério de elegibilidade à base: `[[criterios]]`

Destinos, o *como* de cada um e as regras de aplicação por base:
`definir-criterios-de-elegibilidade`, seção 8.

## Passo 3 — declaração de cobertura e composição

O vocabulário vem do protocolo; a forma da base decide o resto, e toda mudança se declara
na fonte, nunca na memória de quem executa. Os blocos se geram. O que a forma pode e não pode
mudar: `elaborar-expressoes-de-busca`, Parte 2.

**A declaração de cobertura** é `[cobertura]`: `idiomas` por faceta, `plural`, `teto` e
`derivacoes` (entram todos os termos da STR, que vem das linhas "Termo livre" e "Descritores correspondentes"; não há corte por linha) — e, só quando a base deixa fora da string um
termo vigente (da STR do protocolo), `[[reducao]]` termo a termo. Termo fora da STR e termo
alcançado pela forma radical não entram na redução.

**Parâmetros da geração.** É aqui, e não na skill nem no código, que a base difere das
outras. A base nova ou a sintaxe recém-medida muda o valor do parâmetro, nunca uma regra
escrita para uma base só.

- `plural` diz quem alcança o plural, com valor único ou por idioma: `declarar-flexao-por-base`.
- `teto` é o comprimento máximo de cada consulta: `elaborar-expressoes-de-busca`, Parte 2.
- `morfologia` reconhece flexão de número e gênero, não lematização.
- `radical` declara que um termo da string alcança os termos do protocolo que o **contêm**
  por inteiro e na mesma ordem: `ontology` alcança `domain ontology`, mas
  `"ontology engineering"` não alcança `ontological engineering`. É regra declarada, não
  equivalência, e vale só onde o comportamento medido da base a sustenta. A forma radical
  que substitui a STR de uma faceta vai a `[[radical]]`.
- **Toda linha da redução tem motivo verdadeiro e curto** — "redução desta base" basta;
  motivo que ainda não é decisão se escreve com a palavra "pendente", que o relato de
  pendências lê. O argumento da redução vai ao histórico.

**Composição.** `[composicao]` declara as aspas (em todo termo ou só na locução), a
proximidade entre as âncoras e se a disjunção de grupos vai na mesma consulta ou em
consultas separadas; `[[composicao.facetas]]` dá, por faceta, o campo literal e se ele
envolve o grupo ou prefixa cada termo. Campo diferente por parte da faceta (título para a
STR inteira, resumo para um subconjunto específico) vai a `[[consultas_de_campo]]` e a
`[[subconjuntos]]`; o subconjunto só leva termos da STR da faceta.

**Decisões metodológicas desta seção são do pesquisador**: deixar termos fora da string,
restringir idiomas, reduzir a radicais, mover parte da faceta para outro campo. O agente propõe com a
razão medida — teto de caracteres, teto de retorno, idioma de indexação — e o custo
esperado em recall, e pede a decisão.

## Passo 4 — expressões, forma de execução e variantes

- As **cinco expressões** mantêm a composição e a contenção do protocolo
  (`elaborar-expressoes-de-busca`). `[[execucao.expressoes]]` dá o título de cada uma e, só quando difere do papel lido do
  protocolo, o `estatuto` (executada, fidelidade, derivada, sonda). Expressão derivada não
  leva bloco.
- **Forma de execução** (`[execucao] forma`): `unica`, `particionada` (o gerador parte pelo
  teto, com as mesmas âncoras em todas as partes) ou `curada`, com as consultas escritas à
  mão em `[[curadas]]`, cada uma com as facetas que compõe. A forma curada é a única parte em
  que termos se escrevem à mão (número de cada termo nela: `declarar-flexao-por-base`).
- **Regras de montagem** que a base impõe (grupo que exige condição externa, campo que não
  se mistura num grupo) vão a `[[regras_de_montagem]]`, com situação e sondagem.
- **Estratégia de proximidade**, quando a base tem operador de proximidade ou quando a
  expressão o usa: fragmento `estrategia_de_proximidade.md`, que o gerador põe na seção 4.
  É discussão, não forma executável: bloco cercado nele não entra no derivado, não se
  executa nem se confere. O que ele discute: `elaborar-expressoes-de-busca`, Parte 2.
- **Como executar** (`como_executar.md`): passos numerados, do controle da sessão ao
  registro, com o comando do projeto para registrar a execução. Sem contagem de consultas:
  o gerador a mostra.
- **Variantes previstas** (`variantes.md`, o único fragmento com subtítulos `####`): cada
  uma com o **disparo** (o que se observa para adotá-la), a
  **forma** e, quando houver, o limiar ou a exigência de emenda — em uma ou duas frases.
  Quando a variante muda a forma de execução, a emenda muda `[execucao] forma` na fonte. Nenhuma variante se adota por reduzir o número;
  mede-se contra o conjunto-semente.
  Consulta removida sai da tabela sem nota; os identificadores das demais não mudam.

## Passo 5 — conjunto-semente e ressalvas

- **Conjunto-semente**: o que o procedimento traz das sementes e o que a fonte acrescenta,
  `definir-conjunto-semente`, seção 9.
- **Ressalvas** (`ressalvas`, uma por item): só o que muda a execução ou o relato — estatuto dos termos, o que foi
  verificado só em fonte secundária, o que a base não cobre e quem cobre —, um item curto
  cada.

## Forma: o que a gramática exige

O esquema da fonte, os domínios, os fragmentos admitidos e o esqueleto do procedimento
gerado estão em `python3 -m rsl documentos gramatica`, e o leitor reprova o que sair deles.
Antes de escrever uma fonte, ler ali o que se exige; não copiar a forma de outra fonte como
se fosse o contrato.

**Base nova não exige mudança no código**: a sintaxe, o campo, a proximidade e a partição
são valores da fonte. Recurso que a fonte não exprima é alteração técnica a propor e a
provar com o autoteste, não algo a contornar no procedimento.

## Conferir e registrar

1. Gerar em ensaio e revisar a diferença: cada forma de número acrescentada, com a origem;
   cada mudança de texto. Gravar só depois. Rodar a conferência do documento, a dos dados e
   o autoteste do projeto (comandos em `docs/procedimentos.md`, seção Conferências
   transversais). Reprovação aponta incoerência: corrige-se a fonte ou se registra a
   redução com motivo — **nunca se afrouxa a conferência** para a fonte passar.
2. Relatar a **cobertura por faceta** como número, decomposta em literal, alcançado por
   radical, declarado e descoberto. **Cobertura não é recall**: mede quanto do vocabulário
   declarado está na string, com outro denominador. Cobertura alta não é aderência, nem
   cobertura baixa é falha — base que reduz vocabulário assume perda de recall, e o número
   declara a perda. Quem decide se o preço é aceitável é o teste de aderência.
3. Conferir o que o leitor **não** confere — e conferir calculando, não relendo:
   - **o motivo da redução é verdadeiro na base.** O leitor confere só o motivo que invoca
     a forma radical — e por contenção de palavras, não pelo comportamento da base. Os
     demais motivos ele não confere. Termo declarado alcançado tem de sê-lo **pelo
     comportamento medido da base**: frase entre aspas só alcança o termo que a contém
     inteira, lematização não alcança derivação adjetival, e o hífen como separador é
     suposição do leitor, a medir em cada base;
   - **as variantes, a contingência e as camadas** — os fragmentos são prosa, e a
     conferência não lê os termos deles. Usam só termos da STR do protocolo, sem termo que
     só conste do quadro? A relação que afirmam com a forma executada (subconjunto, partição exata)
     vale de fato, pela lógica da consulta?
   - **número escrito em prosa** — quantos termos, quantas palavras-raiz, quantas
     consultas — não deveria existir nos fragmentos; se for indispensável, recalcula-se a
     partir do procedimento gerado;
   - **propagação entre partes**: mudança na forma de execução (partição, nomes das
     consultas, arquivos de exportação) chega a `como_executar.md`, às ressalvas e ao
     registro de execução, e não só a `[execucao]`;
   - que cada critério tem destino, que cada elemento de sintaxe usado nas expressões tem
     estado e fonte, e que as variantes têm disparo.
4. Registrar no histórico o que mudou e por quê (`registrar-decisao`). Mudança que altere a
   recuperação torna vencidos os retornos anteriores daquela base: isso se registra no
   histórico e no registro de execução, **não na fonte**, que passa a declarar só a forma
   nova.
5. Reler a fonte, fragmentos inclusive, procurando o que não é operacional — data, "antes", "passou a", "retirado
   em", justificativa, estado — e levar ao histórico o que ainda não estiver lá.

## Ao entregar

Começar pelo que o procedimento gerado passou a dizer; depois, separadamente: o que se verificou e em que
fonte, o que ficou **não verificado** e as sondagens do roteiro a executar pelo pesquisador, as decisões
metodológicas propostas e ainda pendentes, e o resultado das conferências com a saída.

## Remissões

Lógica das expressões e o que a forma pode mudar: `elaborar-expressoes-de-busca`. Sintaxe,
roteiro, desenho e leitura das sondagens: `executar-sondagens-de-sintaxe`. Plural e exceções de
flexão: `declarar-flexao-por-base`. Execução e registro sob as regras de acesso:
`executar-expressoes-de-busca`. Coerência e fidelidade: `avaliar-resultados-da-busca`. Recall:
`testar-aderencia-das-expressoes`. Sementes: `definir-conjunto-semente`. Critérios por base:
`definir-criterios-de-elegibilidade`.
Emenda: `registrar-decisao`. Nomes de arquivo deste projeto estão
no `README.md` (Mapa); comandos, em `docs/procedimentos.md`; bases, no protocolo; limiares em
uso, em `python3 -m rsl configuracao mostrar`. Não se repetem aqui.
