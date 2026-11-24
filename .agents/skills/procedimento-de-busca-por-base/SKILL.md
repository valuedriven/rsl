---
name: procedimento-de-busca-por-base
description: Cria ou atualiza o procedimento de busca de uma base — escreve a fonte do procedimento (pasta da base, `[documentos] procedimento_fonte`; sigla da tabela "Bases de dados" do protocolo) e gera o procedimento a partir dela e do protocolo — apura a sintaxe da base em fonte oficial e por medição, leva cada critério de elegibilidade ao lugar em que a base o permite aplicar, declara a forma da base (campo, aspas, proximidade, partição), o roteiro de sondagens, a forma de execução, as variantes, o conjunto-semente e as ressalvas, e confere o procedimento gerado contra o protocolo. Use ao montar o procedimento de busca de uma base nova, ao propagar emenda do protocolo aos procedimentos de busca, ao incorporar sintaxe recém-verificada, ao auditar se uma fonte está completa, ao decidir se um termo ausente da string é omissão ou redução declarada, e ao tratar de divergência entre o procedimento e o vocabulário do protocolo.
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
(`flexao-por-base`) e a forma declarada na fonte.

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

Esta skill cuida do **procedimento de busca inteiro**, pela fonte: o que pesquisar, o que registrar, em que ordem montar,
o que a forma da base pode mudar no vocabulário e como conferir. A lógica das cinco
expressões é de `expressoes-de-busca`; a execução e o registro dos retornos, de
`execucao-da-busca`. Ler a que couber antes do passo correspondente.

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

## Passo 1 — apurar a sintaxe da base: `[[sintaxe]]` e `[[sondagens]]`

Cada elemento de sintaxe é uma entrada de `[[sintaxe]]` com **categoria** (as categorias
mínimas estão no domínio da gramática; toda base tem ao menos um elemento de cada) e
**situação**, que é o que se registra:

| Situação | Evidência exigida |
| --- | --- |
| `oficial` | página de ajuda ou documentação do provedor; em `fonte`, o título da página |
| `secundaria` | material de terceiro — treinamento, guia de biblioteca |
| `medicao` | sondagem ou execução registrada, citada em `citacao = "BDn/<id>"` da própria base |
| `nao_verificado` | com `sondagem = "SDn"` do roteiro, ou `sem_sondagem` com o motivo |
| `inexistente` | a fonte da ausência; não localizar não é não existir |

**Toda menção ao registro de execução nomeia a execução ou a sondagem** `(BDn/<id>)`, com
`BDn` da própria base e o `id` existente no registro; a conferência dos dados reprova a fonte
sem esse lastro, e só aquela base. Instrução que apenas manda registrar diz "registro de
execução", sem o caminho.

**Roteiro de sondagens.** Todo elemento `nao_verificado` que se possa testar ganha uma
sondagem em `[[sondagens]]`: objetivo, pré-requisitos, consultas de controle e de teste,
passos, o que observar, leituras (uma delas inconclusiva) e evidência. O desenho segue a
skill `sondagens-de-sintaxe`. O resultado se registra pelo comando do projeto (sinopse em
`docs/procedimentos.md`), que imprime a mudança a aplicar na fonte; o elemento passa a
`medicao` com a citação, e a fonte se regenera. Regra de montagem que a composição
pressupõe vai a `[[regras_de_montagem]]`, com a mesma exigência de situação.

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
  **medida** por sondagem registrada (`flexao-por-base`), o elemento é `nao_verificado` e a
  fonte declara `plural = "explícito"`;
- **proximidade**: operador, distância padrão, se aceita grupos de cada lado;
- **agrupamento**: parênteses, mistura de campos num grupo, grupo isolado;
- **limites**: teto de caracteres da consulta — que alimenta `teto` em `[cobertura]` —, de conjuntos por sessão, de **retorno exibido** e
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

`[[criterios]]` cobre **todos** os critérios do protocolo, inclusive os que a base não
aplica (um ou mais IDs por entrada). Para cada um, um destino e o *como*; a razão, quando
houver, vai ao histórico, não à fonte:

| Destino | Quando | Exemplo de razão |
| --- | --- | --- |
| `consulta` | a sintaxe o expressa e convive com o resto; exige `clausula`, a única fonte do filtro nos blocos | cláusula de ano verificada |
| `ancora` | o critério se aplica pela faceta âncora | domínio de aplicação |
| `interface` | a base só o oferece na página, ou a cláusula quebra a consulta | operador de ano que zera consulta com grupo |
| `variante` | cláusula prevista numa variante; exige `clausula` | idioma, depois de sondado |
| `aproximado` | a busca o aproxima, e a triagem decide | inclusão temática |
| `dispensado` | a base, por constituição, já satisfaz o critério | base de um só idioma |
| `nao` | critério de leitura | adequação temática, texto completo, tipos excluídos na 2ª filtragem |

Três regras:

- **A busca não restringe além do protocolo.** Filtro que exclua tipo ou idioma admitido —
  "apenas revisado por pares", "apenas texto completo na base" — é restrição nova, não
  implementação do critério. Se parecer necessário, é recomendação ao pesquisador.
- **Critério de domínio vai por âncora**, não por filtro de categoria; categoria de assunto
  é camada de precisão, último recurso, declarada no relatório.
- **Dispensar um critério ou movê-lo para a interface é decisão registrada** no histórico,
  com o que se perde; na fonte fica só o destino e o *como*. Onde há filtro de ano na
  consulta e na página, o ano confere-se no **retorno**.

## Passo 3 — declaração de cobertura e composição

O vocabulário vem do protocolo; a forma da base decide o resto, e toda mudança se declara
na fonte, nunca na memória de quem executa. Os blocos se geram.

**O que a forma pode mudar**, sempre declarado: **campo** (tópico, título-resumo-palavras-
chave, título, resumo, descritor); **proximidade** e a distância medida; **truncamento** — há
base em que o curinga devolve zero; **teto de caracteres** e **teto de retorno**, que vira
partição ou lista curada; **filtro de ano**, na consulta ou na página; **idioma indexado**;
**alcance do vocabulário**, integral, com redução termo a termo ou por radicais; **morfologia**, sobre termo que já
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

**A declaração de cobertura** é `[cobertura]`: `idiomas` por faceta, `plural`, `teto` e
`derivacoes` (entram todos os termos da STR, que vem das linhas "Termo livre" e "Descritores correspondentes"; não há corte por linha) — e, só quando a base deixa fora da string um
termo vigente (da STR do protocolo), `[[reducao]]` termo a termo. Termo fora da STR e termo
alcançado pela forma radical não entram na redução.

**Parâmetros da geração.** É aqui, e não na skill nem no código, que a base difere das
outras. A base nova ou a sintaxe recém-medida muda o valor do parâmetro, nunca uma regra
escrita para uma base só.

- `plural` diz quem alcança o plural, com valor único ou por idioma: `explícito` — o gerador
  acrescenta a forma de número por regra e pelas exceções declaradas (`flexao-por-base`) —
  ou `pela lematização` — a base o alcança sozinha, e isso exige o elemento de
  `lematizacao` medido e citado para aquele idioma; sem isso, `documentos conferir` reprova
  a base. O termo que a regra não decide reprova a geração até ter exceção declarada.
- `teto` é o comprimento máximo de cada consulta, em caracteres do bloco tal como se cola na
  interface: um inteiro ou `"nenhum"`. Com número, o gerador parte a expressão sem retirar
  termo, mantendo as âncoras íntegras; com `execucao.forma = "unica"`, partição necessária
  reprova. Com `"nenhum"`, `documentos conferir` relata a maior consulta. A origem do número
  — medido, documentado ou regra de bolso — fica no elemento de `limite_consulta`.
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
  (`expressoes-de-busca`); o gerador as compõe, com proximidade e filtros iguais em todas.
  `[[execucao.expressoes]]` dá o título de cada uma e, só quando difere do papel lido do
  protocolo, o `estatuto` (executada, fidelidade, derivada, sonda). Expressão derivada não
  leva bloco.
- **Forma de execução** (`[execucao] forma`): `unica`, `particionada` (o gerador parte pelo
  teto, com as mesmas âncoras em todas as partes) ou `curada`, com as consultas escritas à
  mão em `[[curadas]]`, cada uma com as facetas que compõe. A forma curada é a única parte em
  que termos se escrevem à mão, e o termo só no singular nela reprova.
- **Regras de montagem** que a base impõe (grupo que exige condição externa, campo que não
  se mistura num grupo) vão a `[[regras_de_montagem]]`, com situação e sondagem.
- **Estratégia de proximidade**, quando a base tem operador de proximidade ou quando a
  expressão o usa: fragmento `estrategia_de_proximidade.md`, que o gerador põe na seção 4.
  É discussão, não forma executável: bloco cercado nele não entra no derivado, não se
  executa nem se confere.
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

- **Conjunto-semente**: o gerador lista as sementes que o arquivo de sementes atribui a esta
  base, com o DOI de lá; a fonte só acrescenta a observação por semente (`[[sementes]]`) e,
  quando preciso, `notas_sementes.md`. O **estado** da aderência não entra: está no registro
  de execução.
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

Lógica das expressões:
`expressoes-de-busca`. Desenho e leitura das sondagens: `sondagens-de-sintaxe`. Plural e
exceções de flexão: `flexao-por-base`. Sondagem, execução e registro sob as regras de acesso:
`execucao-da-busca`. Coerência e fidelidade: `conferencias-da-busca`. Recall:
`teste-de-aderencia`. Sementes: `conjunto-semente`. Critérios: `criterios-de-elegibilidade`.
Emenda: `registrar-decisao`. Nomes de arquivo deste projeto estão
no `README.md` (Mapa); comandos, em `docs/procedimentos.md`; bases, no protocolo; limiares em
uso, em `python3 -m rsl configuracao mostrar`. Não se repetem aqui.
