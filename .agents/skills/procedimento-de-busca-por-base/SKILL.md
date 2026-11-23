---
name: procedimento-de-busca-por-base
description: Cria ou atualiza o procedimento de busca de uma base (docs/procedimentos_busca_<sigla>.md, sigla da tabela "Bases de dados" do protocolo) a partir do protocolo — apura a sintaxe da base em fonte oficial e por medição, leva cada critério de elegibilidade ao lugar em que a base o permite aplicar, compõe strings, expressões, forma de execução, variantes, conjunto-semente e ressalvas, declara o que a forma da base muda no vocabulário e confere o procedimento contra o protocolo. Use ao montar o procedimento de busca de uma base nova, ao propagar emenda do protocolo aos procedimentos de busca, ao incorporar sintaxe recém-verificada, ao auditar se um procedimento está completo e na forma que a conferência lê, ao decidir se um termo ausente da string é omissão ou redução declarada, e ao tratar de divergência entre o procedimento e o vocabulário do protocolo.
---

# Procedimento de busca por base

O procedimento de busca é o **protocolo de busca de uma base**: diz como o vocabulário, as expressões e os
critérios do protocolo se executam **naquela** base e com que evidência se sabe que ela
aceita o que se submete. Não é cópia do protocolo com outra sintaxe, nem manual da base.

A string de uma base **não é a do protocolo com outro invólucro**. As bases divergem do
vocabulário canônico em conteúdo: uma acrescenta flexão morfológica, outra reduz a radicais,
outra usa só o núcleo e executa por consultas curadas. Tratá-las como cópias produziria a
sintaxe de uma com o vocabulário suposto de outra.

> **Duas fontes, com papéis distintos.** O **vocabulário** é do protocolo; a **forma** é da
> procedimento de busca da base. Mudar uma sem revisitar a outra é defeito que só aparece depois de a busca
> já ter sido executada.

## O procedimento de busca é operacional

O procedimento de busca diz **como executar a busca naquela base, na forma vigente** — e nada além disso.
Quem o abre para executar não deve ter de separar a instrução do racional.

- **Só a decisão final.** Nada de histórico: sem datas de decisão, sem "vigente desde", sem
  "retirado em", sem forma anterior, sem retornos vencidos, sem numeração explicada por
  consulta removida. O histórico vai a `data/historico.md`; o estado da execução, ao
  registro de execução.
- **Sem cabeçalho.** O arquivo começa pelo título `# Strings de busca — <base>` e segue
  direto para a seção 1.
- **Sem informação de exclusão.** Termo retirado por emenda **não se lista** no procedimento: o
  leitor o desconta por construção, porque o vigente é a string (STR) do protocolo e o termo
  que só consta do quadro terminológico não é esperado na base. Termo
  alcançado pela forma radical também não se lista: o leitor calcula o alcance. A tabela de
  redução só existe quando a **própria base** deixa fora da string um termo vigente, uma
  linha por termo, motivo curto.
- **Sem justificativa.** Regra, disparo, forma e limiar — não o porquê. O racional de uma
  decisão está no protocolo ou no histórico; o procedimento não o repete. Uma frase de contexto só
  entra quando sem ela a instrução seria executada errado.
- **Número em prosa não entra** se o leitor o calcula (quantos termos, quantas consultas,
  comprimento de cada consulta): a cópia defasa.

Esta skill cuida da **procedimento de busca inteiro**: o que pesquisar, o que registrar, em que ordem montar,
o que a forma da base pode mudar no vocabulário e como conferir. A lógica das cinco
expressões é de `expressoes-de-busca`; a execução e o registro dos retornos, de
`execucao-da-busca`. Ler a que couber antes do passo correspondente.

## Antes de começar: qual é a operação

| Operação | Disparo | O que muda no procedimento |
| --- | --- | --- |
| **Procedimento novo** | base nova nas fontes do protocolo | tudo; exige a base já registrada no protocolo |
| **Propagação de emenda** | mudou vocabulário, expressão, critério ou recorte no protocolo | as seções afetadas; mudança que altere a recuperação é emenda de busca |
| **Sintaxe nova** | documentação consultada ou sondagem medida | seção 1 e o que dela depende |
| **Auditoria** | pedido de revisão ou divergência encontrada | nada, até o pesquisador decidir; relatar |

**Quando o procedimento divergir do protocolo**, identificar primeiro o que mudou:

- **vocabulário ou forma** → revisar o procedimento: termo novo entra na string ou na redução
  declarada, com motivo. Mudança que altere a recuperação exige nova execução e novo teste
  de aderência: é emenda de busca;
- **só a declaração** → conferir; não há execução a repetir, mas há decisão a registrar.

Nos dois casos, registrar no histórico (`data/historico.md`). Divergência fechada em silêncio volta na execução
seguinte.

**Base nova é decisão de escopo** — fontes de informação são do protocolo, e o pesquisador
decide. Sem a base registrada no protocolo (`BDn`, nome, justificativa), não há procedimento
a criar: apresentar a lacuna e pedir a decisão.

## Ler antes de escrever

Na ordem, e sempre a **versão corrente** — o procedimento pode ter sido editado pelo pesquisador
desde a última leitura, e essa edição é o ponto de partida:

1. `README.md` — mapa, nomes de arquivo e precedência; `docs/procedimentos.md` — comandos;
   `python3 -m rsl configuracao mostrar` — limiares em uso e a origem de cada um.
2. O protocolo de estratégia: questão, facetas e âncoras, quadro terminológico por camada e
   idioma, strings, expressões (a executada e a sonda, identificadas pela composição) e as
   suas notas, critérios de elegibilidade e fontes; o conjunto-semente vem do arquivo de
   sementes (`[documentos] sementes`). **É a fonte do vocabulário**; nada dele se reescreve
   de memória.
3. O protocolo de informações gerais: recorte e objeto, para os critérios de domínio.
4. O histórico: decisões já tomadas sobre esta base — reduções, variantes adotadas, defeitos
   que já ocorreram.
5. O registro de execução da base: sondagens medidas, estado da interface, retornos.
6. O procedimento de busca atual da base, se existir, e **o de outra base** como referência de
   estrutura — sem lhe copiar a sintaxe.

## Passo 1 — apurar a sintaxe da base

A seção 1 do procedimento é uma tabela **elemento · situação**. A fonte se diz uma vez, acima da
tabela, quando todo o documento se apoia numa só fonte; ganha coluna própria quando as fontes
diferem de elemento para elemento. Cada elemento tem um de quatro estados, e o estado é o
que se registra:

| Estado | Evidência exigida |
| --- | --- |
| **Verificado em fonte oficial** | página de ajuda ou documentação do provedor; no procedimento, o título da página; a data da consulta, no registro de execução |
| **Verificado em fonte secundária** | material de terceiro — treinamento, guia de biblioteca; declarar como secundário |
| **Verificado por medição** | sondagem registrada com consulta, retorno e captura, no registro de execução |
| **Não verificado** | escreve-se assim; nunca se presume pela documentação de outra base |

**Toda menção ao arquivo de registro de execução nomeia a execução.** Escrever o caminho do
registro — `data/registro_execucao.json` — em qualquer linha do procedimento, em tabela ou em prosa,
só é correto junto da citação `(BDn/<id>)`, com `BDn` da própria base e a execução existente
no registro; a conferência dos dados reprova o procedimento sem esse lastro, e só aquela base.
Instrução que apenas manda registrar diz "registro de execução", sem o caminho. O estado
**Verificado por medição** exige essa citação; sem ela, o estado é **Não verificado**.

**Documentação não é comportamento.** Bases já contradisseram a própria documentação —
curinga que devolve zero, operador que zera o retorno quando há grupo, teto de retorno não
anunciado. O que a expressão usa e só a documentação sustenta fica marcado como a medir, e a
sondagem é obrigatória antes da primeira execução (`execucao-da-busca`).

Elementos a apurar, todos — o que a base não tiver se registra como inexistente, com a
fonte da ausência:

- **campos**: rótulo ou *tag*, o que cada um cobre (título, resumo, palavras-chave de autor,
  palavras-chave atribuídas, descritor controlado), e se a restrição de campo funciona de
  fato;
- **operadores**: booleanos, precedência, caixa, operador implícito entre palavras;
- **frase**: aspas, e o que acontece com hífen, barra e parêntese dentro delas;
- **truncamento e curinga**: símbolo, mínimo de caracteres, e se o curinga desliga a
  lematização;
- **lematização**: plural regular, irregular, idiomas em que é documentada — e, até ser
  **medida na primeira execução da base** (sonda do singular contra o plural, registrada e
  citada `(BDn/<id>)` na linha "Lematização" da seção 1), o estado é **Não verificado** e o
  procedimento declara `plural: explícito`;
- **proximidade**: operador, distância padrão, se aceita grupos de cada lado;
- **agrupamento**: parênteses, mistura de campos num grupo, grupo isolado;
- **limites**: teto de caracteres da consulta — que alimenta o parâmetro `teto de
  caracteres` da declaração de cobertura —, de conjuntos por sessão, de **retorno exibido** e
  de **exportação**;
- **filtros**: ano, idioma, tipo documental, revisão por pares, texto completo — e para cada
  um **se vai na consulta ou só na interface**, e se convive com o resto da sintaxe;
- **vocabulário controlado** próprio da base e o campo em que opera;
- **idioma de indexação** dos registros;
- **exportação**: formatos, campos incluídos, tamanho do lote.

**Onde pesquisar.** Na documentação pública do provedor, que se lê sem autenticação. Ler
página pública de ajuda é consulta, não automação de interface — uma página por vez,
**sem nova tentativa após erro**, e isso se diz expressamente a quem for delegada a leitura; **executar consulta na base
não é desta etapa** e segue as regras de acesso do `AGENTS.md` §9 — autenticação feita pelo
pesquisador, sem paralelismo, sem nova tentativa, parada diante de qualquer bloqueio. Página
que não abriu é pendência registrada, nunca "a base não tem".

## Passo 2 — levar cada critério de elegibilidade à base

A seção 2 é uma tabela com **todos** os critérios do protocolo, inclusive os que a base não
aplica. Para cada um, um de quatro destinos e o *como*; a razão, quando houver, vai ao
histórico, não ao procedimento:

| Destino | Quando | Exemplo de razão |
| --- | --- | --- |
| **na consulta** | a sintaxe o expressa e convive com o resto | cláusula de ano verificada |
| **no filtro da interface** | a base só o oferece na página, ou a cláusula quebra a consulta | operador de ano que zera consulta com grupo |
| **dispensado pela cobertura da base** | a base, por constituição, já satisfaz o critério | base só de artigos de periódico; base de um só idioma |
| **não na busca** | critério de leitura | adequação temática, texto completo, tipos excluídos na 2ª filtragem |

Três regras:

- **A busca não restringe além do protocolo.** Filtro que exclua tipo ou idioma admitido —
  "apenas revisado por pares", "apenas texto completo na base" — é restrição nova, não
  implementação do critério. Se parecer necessário, é recomendação ao pesquisador.
- **Critério de domínio vai por âncora**, não por filtro de categoria; categoria de assunto
  é camada de precisão, último recurso, declarada no relatório.
- **Dispensar um critério ou movê-lo para a interface é decisão registrada** no histórico,
  com o que se perde; no procedimento fica só o destino e o *como*. Onde há filtro de ano na
  consulta e na página, o ano confere-se no **retorno**.

## Passo 3 — strings por faceta e declaração de cobertura

O vocabulário vem do protocolo; a forma da base decide o resto, e toda mudança se declara
no procedimento, nunca na memória de quem executa.

**O que a forma pode mudar**, sempre declarado: **campo** (tópico, título-resumo-palavras-
chave, título, resumo, descritor); **proximidade** e a distância medida; **truncamento** — há
base em que o curinga devolve zero; **teto de caracteres** e **teto de retorno**, que vira
partição ou lista curada; **filtro de ano**, na consulta ou na página; **idioma indexado**;
**camada do vocabulário**, integral, núcleo ou radicais; **morfologia**, sobre termo que já
consta; **forma de execução**, uma consulta, várias de campo único unidas por deduplicação,
ou lista curada executada consulta a consulta.

**O que a forma não pode mudar:**

- **termo do protocolo ausente sem declaração** — ausência declarada é decisão com preço
  medido; silenciosa é omissão;
- **âncora obrigatória** — expressão sem âncora não é a mesma busca com menos facetas: é
  outra busca;
- **composição, contenção e simetria de filtros** das cinco expressões
  (`expressoes-de-busca`);
- **termo que não derive do protocolo** — palavra nova só com decisão registrada, e isso vale
  também para variantes, contingências e camadas.

**A declaração de cobertura** é tabela legível por máquina, com cinco parâmetros —
**idiomas** por faceta, **camadas** (integral ou núcleo), **plural**, **teto de caracteres** e
**derivações** — e, só quando a base deixa fora da string um termo vigente (da STR do
protocolo), a **redução** termo a termo. Termo fora da STR e termo alcançado pela forma
radical não entram na redução: o leitor os trata.

**Parâmetros da geração da busca.** É aqui, e não na skill, que a base difere das outras.
`plural` e `teto de caracteres` governam a composição: a string e as consultas se montam a
partir da STR aplicando o valor declarado, e `documentos conferir` confere o resultado contra ele. Base
nova ou sintaxe recém-medida muda o valor do parâmetro, nunca uma regra escrita para uma
base só.

- `plural` diz quem alcança o plural: `explícito` — a string traz as duas formas de número,
  ou um truncamento que as alcance — ou `pela lematização` — a base o alcança sozinha. `pela
  lematização` só vale com a linha "Lematização" da seção 1 **verificada por medição** e
  com a execução citada `(BDn/<id>)`; sem isso, `documentos conferir` reprova a base. Em `explícito`,
  `documentos conferir` relata, sem reprovar, os termos numa só forma de número: substantivo não
  contável não tem plural de uso; o agente propõe o plural termo a termo e o pesquisador decide.
- `teto de caracteres` é o comprimento máximo de cada consulta executável, em caracteres
  do bloco tal como se cola na interface: um número inteiro (`1400` ou `1.400`) ou
  `nenhum`. Com número, a consulta que passa dele se particiona sem retirar termo
  (`expressoes-de-busca`), e `documentos conferir` reprova a base em que alguma passe. Com `nenhum`,
  `documentos conferir` relata a maior consulta. A origem do número — medido, documentado ou regra de
  bolso — fica na linha "Comprimento máximo da consulta" da seção 1. Sem medição, o teto é
  escolha conservadora proposta ao pesquisador. Valor alto demais aparece como recusa da
  interface; valor baixo demais custa partição, não recall.
- `morfologia` reconhece flexão de número e gênero, não lematização.
- `radical` declara que um termo da string alcança os termos do protocolo que o **contêm**
  por inteiro e na mesma ordem: `ontology` alcança `domain ontology`, mas
  `"ontology engineering"` não alcança `ontological engineering`. É regra declarada, não
  equivalência, e vale só onde o comportamento medido da base a sustenta.
- **Toda linha da redução tem motivo verdadeiro e curto** — "redução desta base" basta;
  motivo que ainda não é decisão se escreve com a palavra "pendente", que o relato de
  pendências lê. O argumento da redução vai ao histórico.

**Compor por construção, não por digitação.** Strings de dezenas de termos copiadas à mão
perdem termo sem aviso. Montá-las a partir do quadro terminológico lido do protocolo — com o
leitor do projeto, num roteiro descartável no diretório temporário, ou com conferência termo
a termo — e só depois aplicar a forma da base. O que se retira por decisão da
base fica na redução declarada; o resto se confere pelo leitor, não pela prosa.

**Decisões metodológicas desta seção são do pesquisador**: usar só o núcleo, restringir
idiomas, reduzir a radicais, mover parte da faceta para outro campo. O agente propõe com a
razão medida — teto de caracteres, teto de retorno, idioma de indexação — e o custo
esperado em recall, e pede a decisão.

## Passo 4 — expressões, forma de execução e variantes

- As **cinco expressões** mantêm a composição e a contenção do protocolo
  (`expressoes-de-busca`). Proximidade e filtros, se usados, valem **para todas**.
- Cada expressão que se executa — a executada, as de fidelidade e a sonda — é **bloco
  literal único**, com as âncoras em proximidade inline. Não se definem conjuntos `#n`: a
  numeração é atribuída pela sessão e não se reproduz a partir do procedimento. O bloco é o que se
  submete; não há receita de montagem.
- A **segunda cópia** — o bloco contra a seção 3 — não é tolerada por convenção: é conferida.
  O conjunto de termos do bloco tem de ser o das strings das facetas declaradas; termo
  defasado ou estranho reprova a conferência daquela base.
- Cada expressão declara o seu **estatuto** (executada e exportada, teste de fidelidade,
  derivada localmente, sonda de sensibilidade) e as **facetas** que compõe. Expressão
  derivada que não se executa não leva bloco; bloco presente na derivada padrão reprova a
  conferência, e a forma longa é exceção declarada.
- **Forma de execução**: única, particionada em consultas de campo único unidas por
  deduplicação, ou lista curada executada consulta a consulta. Partição tem de ser exata:
  as mesmas âncoras em todas as partes. Lista curada não lê as facetas, e o procedimento diz isso.
- **Estratégia de proximidade**, quando a base tem operador de proximidade ou quando a
  expressão o usa: subseção `### Estratégia de proximidade` na seção 4. É discussão, não
  forma executável: o leitor a ignora, e bloco cercado nela não se executa nem se confere.
  Discute, com o estado de verificação de cada afirmação:
  - **o que a proximidade restringe**: entre que grupos se aplica (as âncoras, uma âncora e
    uma temática) e que ruído pretende cortar. Proximidade sem ruído identificado é
    restrição sem motivo;
  - **operador e distância**: ordenado ou não, distância padrão, unidade (palavra), e a
    distância escolhida contra as alternativas. Distância menor ganha precisão e perde os
    registros em que os conceitos aparecem em frases diferentes do resumo;
  - **comportamento medido** com grupos grandes de cada lado, com frase entre aspas,
    truncamento e restrição de campo. Há base que recusa ou zera a consulta sem aviso, e
    documentação não substitui sondagem;
  - **o preço em recall**: sementes que a proximidade exclui e a anatomia da perda da sonda.
    Esse é o disparo da forma sem proximidade, que fica nas variantes;
  - **simetria e derivação**: a mesma cláusula em todas as expressões, ou em nenhuma. O teste
    de fidelidade diz se a derivação local reproduz a expressão executada com proximidade;
  - **o que fica para o pesquisador**: usar ou não a proximidade, e com que distância. O
    agente propõe com a medida e o custo esperado.
- **Como executar**: passos numerados, do controle da sessão ao registro, com o comando do
  projeto para registrar a execução.
- **Variantes previstas**: cada uma com o **disparo** (o que se observa para adotá-la), a
  **forma** e, quando houver, o limiar ou a exigência de emenda — em uma ou duas frases.
  Quando a variante muda a forma de execução, a emenda declara `- Execução:` com o novo
  valor e escreve as partes literais. Nenhuma variante se adota por reduzir o número;
  mede-se contra o conjunto-semente.
  Consulta removida sai da tabela sem nota; os identificadores das demais não mudam.

## Passo 5 — conjunto-semente e ressalvas

- **Conjunto-semente**: as sementes que o protocolo atribui a esta base, com identificador,
  DOI ou outro identificador **conferido na fonte**, e o procedimento em duas etapas —
  indexação primeiro, recuperação depois. Contagens **não se transcrevem**: leem-se do
  protocolo. O **estado** da aderência não entra no procedimento: está no registro de execução.
- **Ressalvas**: só o que muda a execução ou o relato — estatuto dos termos, o que foi
  verificado só em fonte secundária, o que a base não cobre e quem cobre —, um item curto
  cada.

## Contrato de forma — o que a conferência lê

O procedimento de busca é fonte autoral e é **lido pelo leitor do protocolo** do projeto. O que está abaixo
não é estilo: fora disso a conferência daquela base reprova ou, pior, lê errado. Antes de
alterar, conferir no leitor se o contrato ainda é este.

| Elemento | Forma exigida |
| --- | --- |
| seções lidas | cabeçalhos exatos `## 3. Strings por faceta`, `## 4. Expressões de busca` e `### Declaração de cobertura` |
| declaração | tabela com as linhas `idiomas` (`FCTn: pt, en, es;` …), `camadas` (`todas` ou `nucleo`), `plural` (`explícito` ou `pela lematização`), `teto de caracteres` (número inteiro ou `nenhum`) e `derivações` (`morfologia` e/ou `radical`); sem `idiomas`, `camadas`, `plural` ou `teto de caracteres`, ou com valor fora do domínio, a leitura daquela base reprova |
| redução termo a termo | só para termo vigente que a base deixa fora; linhas `\| FCTn \| termo \| motivo \|` dentro da seção da declaração. Termo retirado por emenda e termo alcançado pela forma radical não se declaram |
| string por faceta | `### \`STRn\` — string \`#n\` — <cor> FCTn — <nome>`, com **um único** bloco cercado |
| campo da string | lido do texto: início `TS=` ou `TITLE-ABS-KEY`, ou prefixo `title:`, `abstract:`, `descriptor:`; campo de outra forma é lido como "todos os campos", e prefixos diferentes na mesma string, como "misto" |
| termo da string | entre aspas, separado por `OR`; sem proximidade nem aspas aninhadas dentro da string da faceta |
| expressão | `### EBn ...` com uma linha `**Facetas:** FCT1 (…) AND …` e o estatuto por extenso nas primeiras linhas |
| bloco da expressão | literal para executada, fidelidade e sonda: sem referência a conjunto `#n`; o conjunto de termos confere com as strings das facetas declaradas, e operador, campo, proximidade (`NEAR/n`, `W/n`) e valor de filtro não contam como termo. Ausência de bloco só passa na expressão derivada que não se executa; bloco presente na derivada padrão reprova. A forma longa, quando declarada, é representação não executada e fica fora da conferência de bloco |
| forma de execução | exatamente uma linha `- Execução: única` ou `- Execução: particionada`; ausente, repetida ou com outro valor reprova a conferência desta base — não há padrão |
| âncoras | inline no bloco de cada expressão; a subseção de proximidade não é exigida e não é forma executável |
| forma curada | subseção com "curadas" no título; consultas em `####` grupos, linhas `\| n \| \`consulta\` \| facetas \|`; a faceta se reconhece só pelo código `FCTn` — emoji ou cor não identifica faceta |
| forma longa não executada | subseção "forma longa", expressões em `**EBn**`; não executada e fora da conferência de bloco |
| ignoradas pela leitura | subseções iniciadas por "Como executar", "Variantes", "Como esta base" e "Estratégia de proximidade" |
| filtros reconhecidos | `PY=(…)`, `PUBYEAR`, `LA=`/`LANGUAGE`, `DT=`/`DOCTYPE`; filtro fora disso é lido como "na interface" |

**Base nova exige mudança no leitor**, além do procedimento: o mapa de procedimentos por base e, se a
sintaxe trouxer campo ou filtro novo, o reconhecimento correspondente. Isso é alteração
técnica a propor e a provar com o autoteste, não algo que o procedimento resolva sozinho.

## Estrutura do procedimento de busca

```
# Strings de busca — <base>                sem cabeçalho: direto para a seção 1
## 1. Estado de verificação da sintaxe     elemento · situação; fonte
## 2. Critérios de elegibilidade           todos os CE · na consulta? · como
## 3. Strings por faceta                   mapa das facetas; forma da base em uma frase
### Declaração de cobertura                tabela; redução própria da base, se houver
### `STRn` — string `#n` — …                uma por faceta, um bloco cada
## 4. Expressões de busca                  composição, execução de cada EB, limiares, leitura de zero
### (forma curada | como esta base exige a montagem)
### EB1 … EB5                              facetas, estatuto, bloco literal quando se executa
### Estratégia de proximidade              opcional; discussão, não lida como forma
### Como executar
### Variantes previstas                    disparo · forma · regra de medida
## 5. Conjunto-semente                     sementes da base; procedimento; limiar
## 6. Ressalvas                            itens curtos, só o que muda execução ou relato
```

O texto que se repete entre procedimentos — composição, execução de cada expressão, leitura de
zero — pode ser o mesmo, e é curto; o que **não** se repete é qualquer afirmação sobre
sintaxe, que é sempre desta base e com a sua fonte.

## Conferir e registrar

1. Rodar a conferência do documento, a dos dados e o autoteste do projeto (comandos em
   `docs/procedimentos.md`, seção Conferências transversais). Reprovação aponta incoerência: corrige-se o procedimento ou se registra a redução
   com motivo — **nunca se afrouxa a conferência** para o procedimento passar.
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
   - **as variantes, a contingência e as camadas** — o leitor salta as subseções
     "Variantes", "Como executar" e "Estratégia de proximidade". Usam só termos da STR do protocolo, sem termo que
     só conste do quadro? A relação que afirmam com a forma executada (subconjunto, partição exata)
     vale de fato, pela lógica da consulta?
   - **número escrito em prosa** — quantos termos, quantas palavras-raiz, quantas
     consultas — não deveria existir; se for indispensável, recalcula-se a partir das
     strings do próprio procedimento;
   - **propagação entre seções**: mudança na forma de execução (partição, nomes das
     consultas, arquivos de exportação) chega a "Como executar", às ressalvas e ao registro
     de execução, e não só à seção 4;
   - que cada critério tem destino, que cada elemento de sintaxe usado nas expressões tem
     estado e fonte, e que as variantes têm disparo.
4. Registrar no histórico o que mudou e por quê (`registrar-decisao`). Mudança que altere a
   recuperação torna vencidos os retornos anteriores daquela base: isso se registra no
   histórico e no registro de execução, **não no procedimento**, que passa a mostrar só a forma
   nova.
5. Reler o procedimento procurando o que não é operacional — data, "antes", "passou a", "retirado
   em", justificativa, estado — e levar ao histórico o que ainda não estiver lá.

## Ao entregar

Começar pelo que o procedimento passou a dizer; depois, separadamente: o que se verificou e em que
fonte, o que ficou **não verificado** e precisa de sondagem pelo pesquisador, as decisões
metodológicas propostas e ainda pendentes, e o resultado das conferências com a saída.

## Remissões

Lógica das expressões:
`expressoes-de-busca`. Sondagem, execução e registro sob as regras de acesso:
`execucao-da-busca`. Coerência e fidelidade: `conferencias-da-busca`. Recall:
`teste-de-aderencia`. Sementes: `conjunto-semente`. Critérios: `criterios-de-elegibilidade`.
Emenda: `registrar-decisao`. Nomes de arquivo deste projeto estão
no `README.md` (Mapa); comandos, em `docs/procedimentos.md`; bases, no protocolo; limiares em
uso, em `python3 -m rsl configuracao mostrar`. Não se repetem aqui.
