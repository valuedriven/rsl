# cobertura-por-base Specification

## Purpose

Conferir a string de busca de cada procedimento de busca contra o vocabulário vigente do protocolo,
de modo que termo retirado não volte e termo vigente não falte sem redução declarada.

## Requirements

### Requirement: Vocabulário vigente é a string do protocolo
O termo vigente de uma faceta SHALL ser o que consta da STR correspondente no protocolo,
filtrado pelos idiomas que o procedimento de busca declara. O controle terminológico MUST
servir apenas para classificar o termo por idioma, e nenhuma lista de retirados SHALL ser
mantida no código ou no procedimento de busca. Nenhum filtro por linha do CT SHALL ser
aplicado.

#### Scenario: Termo vigente ausente da base
- **WHEN** um termo da STR, nos idiomas declarados, falta na string da base e não
  consta da redução declarada nem é alcançado por derivação declarada
- **THEN** a conferência daquela base reprova, nomeando faceta e termo

#### Scenario: Termo do quadro fora da STR
- **WHEN** um termo consta do quadro mas não da STR
- **THEN** ele não é esperado na string da base e a ausência não reprova

#### Scenario: Campo camadas declarado
- **WHEN** a `[cobertura]` de uma fonte de procedimento declara `camadas = "todas"`
- **THEN** a leitura da fonte reprova o campo como desconhecido, nomeando a base e o campo

### Requirement: Termo da base deriva da STR
Todo termo da string de uma base SHALL corresponder, em flexão ou pela derivação declarada, a
um termo da STR da mesma faceta, ou ser termo do quadro dessa faceta subsumido por um termo
da STR, na regra de `geracao-das-strings`. Termo que só exista no quadro sem estar subsumido,
ou que não exista em lugar nenhum, MUST reprovar. O subsumido aceito SHALL ser relatado por
base, sem reprovar.

#### Scenario: Termo retirado devolvido à base
- **WHEN** o procedimento de busca usa, mesmo em flexão, um termo que está no quadro, não está na STR e não
  é subsumido por termo da STR
- **THEN** a conferência daquela base reprova, dizendo que o termo não está na string do
  protocolo

#### Scenario: Termo inventado
- **WHEN** o procedimento de busca usa um termo que não deriva de nenhum termo do protocolo
- **THEN** a conferência daquela base reprova, nomeando o termo

#### Scenario: Subsumido em campo próprio
- **WHEN** o procedimento de busca da ERIC usa `"ontology engineering"` no resumo (`STR1b`), e a STR1 tem
  `ontology` e não tem `ontology engineering`, que está no quadro de FCT1
- **THEN** a conferência da ERIC não reprova por esse termo, e o relata como subsumido por
  `ontology`

### Requirement: Composição da base segue o protocolo
As facetas de cada expressão no procedimento de busca SHALL ser as que a composição lida do protocolo
determina, e a expressão executada pela base SHALL ser a que o protocolo declara executada.

#### Scenario: Base executa outra expressão
- **WHEN** o procedimento de busca executa uma expressão diferente da declarada executada no protocolo
- **THEN** a conferência daquela base reprova, nomeando as duas

### Requirement: Reprovação é por base
Defeito na forma de uma base MUST reprovar apenas a conferência daquela base.

#### Scenario: Um procedimento de busca divergente
- **WHEN** só o procedimento de busca da BRAPCI diverge do protocolo
- **THEN** só a conferência da BRAPCI reprova

### Requirement: Autoteste prova a reprovação por base
O autoteste SHALL injetar, um de cada vez, um defeito no procedimento de busca de uma única base — termo que
só consta do quadro, referência a conjunto `#n` no bloco executado e termo defasado em
relação à seção 3 —, exigindo que a conferência dessa base reprove e que a das demais não
reprove.

#### Scenario: Defeito só na BRAPCI
- **WHEN** o autoteste devolve ao procedimento de busca da BRAPCI um termo que só consta do quadro
- **THEN** a conferência da BRAPCI reprova e as das demais bases passam; outro resultado
  faz o autoteste falhar

#### Scenario: Conjunto devolvido ao bloco
- **WHEN** o autoteste troca o bloco da EB4 de uma base por um bloco que referencia `#n`
- **THEN** a conferência daquela base reprova e as das demais passam

#### Scenario: Bloco defasado em uma base
- **WHEN** o autoteste troca um termo do bloco executado de uma base por termo fora das
  facetas declaradas
- **THEN** a conferência daquela base reprova e as das demais passam

### Requirement: Forma de execução declarada no procedimento de busca
A fonte do procedimento de cada base SHALL declarar a forma de execução em `[execucao]
forma`, com o valor `unica`, `particionada` ou `curada`. O campo ausente ou com outro valor
MUST reprovar a conferência daquela base, nomeando a fonte, e nenhum valor padrão é
presumido. O procedimento gerado SHALL trazer a linha `- Execução: <forma>` uma única vez.

#### Scenario: Procedimento de busca sem declaração
- **WHEN** `[execucao]` da fonte da ERIC não tem `forma`
- **THEN** a conferência da ERIC reprova, nomeando a fonte, e as demais bases não são
  afetadas

#### Scenario: Valor fora do domínio
- **WHEN** a fonte declara `forma = "dividida"`
- **THEN** a conferência daquela base reprova, nomeando o valor e os admitidos

### Requirement: Faceta da forma curada identificada pelo código
Na forma curada do procedimento de busca, a faceta de cada consulta SHALL ser identificada pelo código
`FCTn`. Símbolo gráfico (emoji, cor) MUST NOT identificar faceta.

#### Scenario: Consulta marcada só por emoji
- **WHEN** a célula de facetas de uma consulta curada traz `🟦` sem `FCT1`
- **THEN** a consulta é lida sem faceta atribuída

### Requirement: Expressão executada é bloco literal
Os blocos das expressões que se executam — a executada, as de fidelidade e a sonda — SHALL
ser submetidos como estão. Nenhum desses blocos SHALL referenciar conjunto de busca `#n`;
referência MUST reprovar a conferência daquela base, nomeando base e expressão.

#### Scenario: Bloco composto por conjuntos
- **WHEN** o bloco da EB4 da WoS é `#5 AND (#3 OR #4) AND PY=(2017-2026)`
- **THEN** a conferência da WoS reprova, nomeando a EB4 e a referência a conjunto, e as
  demais bases não são afetadas

#### Scenario: Bloco literal
- **WHEN** todos os blocos das expressões executadas, de fidelidade e de sonda se submetem
  como estão, sem `#n`
- **THEN** essa dimensão não reprova nenhuma base

#### Scenario: Expressão derivada sem bloco
- **WHEN** a EB1, derivada localmente, não tem bloco no procedimento de busca
- **THEN** a ausência não reprova, porque a expressão não se executa

### Requirement: Expressão derivada não leva bloco
Expressão derivada que não se executa MUST NOT ter bloco na forma padrão; bloco presente
MUST reprovar a conferência daquela base, nomeando a expressão derivada. A forma longa
declarada é representação não executada e não entra nessa conferência.

#### Scenario: Bloco em expressão derivada
- **WHEN** a EB1, derivada localmente, traz um bloco cercado na forma padrão
- **THEN** a conferência daquela base reprova, nomeando a expressão derivada, e as demais
  não são afetadas

### Requirement: Termos do bloco conferem com as facetas declaradas
O conjunto de termos de cada bloco executado, de fidelidade e de sonda SHALL ser o das
strings das facetas que a expressão declara. Operador, campo e valor de filtro MUST NOT
contar como termo. Termo ausente ou termo estranho MUST reprovar a conferência daquela
base, nomeando expressão e termo.

#### Scenario: Bloco defasado por emenda na seção 3
- **WHEN** um termo da STR3 é alterado e o bloco da EB4 mantém o termo anterior
- **THEN** a conferência daquela base reprova, nomeando o termo ausente e o termo que
  deixou de ser vigente

#### Scenario: Termo estranho no bloco
- **WHEN** um bloco traz termo que não consta de nenhuma faceta declarada nem de filtro
- **THEN** a conferência daquela base reprova, nomeando o termo

#### Scenario: Valor de filtro não é termo
- **WHEN** o bloco traz `DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")`
- **THEN** os valores do filtro não contam como termos estranhos

#### Scenario: Operador de proximidade não é termo
- **WHEN** o bloco traz `NEAR/5` ou `W/5` entre grupos de termos
- **THEN** o operador não conta como termo estranho

### Requirement: Verificação por medição remete a execução registrada
Toda citação de execução ou de sondagem na fonte do procedimento SHALL ter a forma `BDn/<id>`
(no texto, `(BDn/<id>)`), com o `BDn` da própria base. Isso vale para os campos `citacao` e
para o texto dos fragmentos e dos demais campos. Também SHALL estar nessa forma toda menção
ao arquivo de registro de execução.

A conferência dos arquivos alimentados MUST reprovar, só naquela base, nomeando a fonte, o
campo ou a linha e a referência, nestes casos:
- falta o identificador;
- o `BDn` é de outra base;
- o `id` não existe em `bases.BDn.execucoes` nem em `bases.BDn.sondagens` do registro.

#### Scenario: Citação sem identificador de execução
- **WHEN** o elemento "`NEAR/x` entre grupos" da WoS tem `situacao = "medicao"` e
  `citacao = "BD1"`
- **THEN** `dados conferir` reprova a WoS, nomeando o elemento e a falta do identificador, e
  as demais bases não são afetadas

#### Scenario: Citação em prosa
- **WHEN** `notas_sintaxe.md` da BRAPCI diz "apurada por medição, com as sondagens em
  `data/registro_execucao.json` (BD4)"
- **THEN** `dados conferir` reprova a BRAPCI pela falta do identificador, e as demais bases
  não são afetadas

#### Scenario: Base trocada na citação
- **WHEN** um elemento de `[[sintaxe]]` da ERIC tem `citacao = "BD1/sonda-near"`
- **THEN** `dados conferir` reprova a ERIC, nomeando a citação de outra base

#### Scenario: Citação de sondagem registrada
- **WHEN** um elemento da WoS cita `BD1/sd1-2026-12-02` e o registro tem esse `id` em
  `bases.BD1.sondagens`
- **THEN** essa dimensão não reprova

#### Scenario: Execução citada inexistente
- **WHEN** a fonte da Scopus cita `BD2/sonda-w5` e o registro não tem esse `id` em BD2
- **THEN** `dados conferir` reprova a Scopus, nomeando a referência ausente

#### Scenario: Registro ausente
- **WHEN** a fonte cita uma execução e `data/registro_execucao.json` não existe
- **THEN** `dados conferir` reprova aquela base pela citação sem lastro, além de relatar o
  arquivo ausente

#### Scenario: Elemento não verificado
- **WHEN** o elemento tem `situacao = "nao_verificado"` e não cita o registro
- **THEN** essa dimensão não reprova

#### Scenario: Citação válida
- **WHEN** a fonte da WoS cita `BD1/sonda-near` e o registro tem esse `id` em
  `bases.BD1.execucoes`
- **THEN** essa dimensão não reprova

### Requirement: Autoteste prova a reprovação da verificação sem lastro
O autoteste SHALL injetar, numa cópia, citação de medição sem identificador e citação de
execução inexistente no procedimento de busca de uma única base, e exigir que só aquela base reprove. Sem
registro de execução, esses casos SHALL constar como não executados, com o motivo.

#### Scenario: Defeito injetado numa base
- **WHEN** o autoteste injeta `(BD1)` sem identificador no procedimento de busca da WoS, com registro
  presente
- **THEN** a conferência da WoS reprova e as das demais bases não reprovam

#### Scenario: Registro ausente no autoteste
- **WHEN** o autoteste roda sem `data/registro_execucao.json`
- **THEN** os casos desta exigência constam como não executados e não contam como
  resultado esperado

### Requirement: Critérios do procedimento de busca conferem com o protocolo
O conjunto dos IDs de `[[criterios]]` da fonte de cada base SHALL ser igual ao conjunto de
IDs da tabela de critérios do protocolo. Um ID que não existe no protocolo, ou um critério
do protocolo ausente da fonte, MUST reprovar só a conferência daquela base, nomeando a fonte
e o ID.

#### Scenario: Procedimento de busca cita critério inexistente
- **WHEN** o protocolo é renumerado e a fonte de uma base ainda cita o ID antigo
- **THEN** a conferência daquela base reprova, nomeando o ID citado como ausente do
  protocolo e o vigente como ausente da fonte; as demais bases, já corrigidas, não reprovam

#### Scenario: Critério agrupado numa linha
- **WHEN** uma linha de `[[criterios]]` tem `ids = ["CE1", "CE2"]`
- **THEN** os dois IDs contam como citados

#### Scenario: Procedimentos de busca em dia
- **WHEN** as quatro fontes citam exatamente os IDs do protocolo
- **THEN** essa dimensão não reprova nenhuma base

### Requirement: Autoteste prova a reprovação do critério defasado

O autoteste SHALL injetar, numa cópia, um ID de critério inexistente no procedimento de busca de uma única
base e exigir que só aquela base reprove.

#### Scenario: Defeito injetado numa base

- **WHEN** o autoteste troca um ID existente por outro inexistente no procedimento de busca da Scopus
- **THEN** a conferência da Scopus reprova e as das demais bases não reprovam

### Requirement: Plural declarado por base
`[cobertura] plural` da fonte de cada base SHALL ter uma destas formas:
- um valor único, `explícito` ou `pela lematização`, que vale para todos os idiomas da base;
- uma tabela por idioma, como `{ en = "pela lematização", pt = "explícito", es = "explícito" }`,
  cobrindo todos os idiomas que `[cobertura] idiomas` usa.

Os casos abaixo MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a fonte e o campo:
- o campo ausente;
- o valor fora do domínio;
- o idioma sem valor.

#### Scenario: Linha ausente
- **WHEN** `[cobertura]` da fonte da Scopus não tem `plural`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a fonte e o campo

#### Scenario: Valor fora do domínio
- **WHEN** `plural = "omitido"` na fonte da WoS
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, citando os dois valores admitidos

#### Scenario: Valor por idioma
- **WHEN** a fonte da WoS declara `plural = { en = "pela lematização", pt = "explícito", es = "explícito" }`
- **THEN** a flexão acrescenta plural só aos termos pt e es, e o en exige a lematização
  medida para en

#### Scenario: Idioma sem valor
- **WHEN** a base usa pt, en e es, e `plural` traz só en e pt
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando `es`

### Requirement: Plural pela lematização exige lematização medida
Para cada idioma com `pela lematização`, a fonte SHALL ter um elemento de `[[sintaxe]]` de
`categoria = "lematizacao"` com `situacao = "medicao"` e `citacao` de execução ou sondagem
registrada daquela base. O elemento com `idioma` vale para esse idioma; o elemento sem
`idioma` vale para todos. A conferência MUST reprovar só aquela base quando, para o idioma,
não há elemento medido com citação.

#### Scenario: Lematização não verificada
- **WHEN** a fonte da ERIC declara `plural = "pela lematização"` e o único elemento de
  `lematizacao` é `nao_verificado`
- **THEN** `documentos conferir` reprova a ERIC, nomeando a declaração e o elemento sem
  medição; as demais bases não são afetadas

#### Scenario: Lematização medida
- **WHEN** a fonte declara `plural = "pela lematização"` e o elemento de `lematizacao`, sem
  `idioma`, é `medicao` com `citacao = "BD3/sonda-plural"`
- **THEN** essa dimensão não reprova em `documentos conferir`, porque a medição vale para
  todos os idiomas, e a existência de `BD3/sonda-plural` é conferida por `dados conferir`

#### Scenario: Lematização medida num idioma só
- **WHEN** a fonte da WoS declara en `pela lematização`, e o elemento de `lematizacao` com
  `idioma = "en"` é `medicao` com `citacao = "BD1/sd5-2026-12-02"`
- **THEN** essa dimensão não reprova em `documentos conferir`, e a existência da citação é
  conferida por `dados conferir`

#### Scenario: Plural explícito
- **WHEN** a fonte declara `plural = "explícito"`
- **THEN** a situação dos elementos de `lematizacao` não reprova

### Requirement: Termo só no singular reprova
Em idioma com plural explícito, a conferência MUST reprovar, por base, o termo da STR
presente nos blocos da base numa só forma de número. A reprovação nomeia a faceta, o termo e
o idioma, e não vale quando:
- o termo é `nao_contavel` no arquivo de exceções (`flexao-dos-termos`);
- o termo tem forma `vetada` no arquivo de exceções;
- um truncamento declarado na fonte alcança o termo.

A regra vale também para a forma curada e para os subconjuntos, que são as partes da fonte
onde se escrevem termos à mão.

#### Scenario: Plural esquecido
- **WHEN** a ERIC declara plural explícito em en, e o subconjunto `STR1b` da fonte traz
  `metadata schema` sem `metadata schemas` e sem exceção
- **THEN** `documentos conferir` reprova a ERIC, nomeando `metadata schema`, FCT1 e en; as
  demais bases passam

#### Scenario: Plural esquecido na forma curada
- **WHEN** uma consulta de `[[curadas]]` da fonte traz `"teaching strategy"` sem `"teaching
  strategies"` e sem exceção, e a base declara plural explícito em en
- **THEN** `documentos conferir` reprova a base, nomeando `teaching strategy`, FCT3 e en;
  as demais bases passam

#### Scenario: Não contável
- **WHEN** o bloco traz `"education"` só no singular e o arquivo de exceções declara
  `education`, en, `nao_contavel`
- **THEN** essa dimensão não reprova

### Requirement: Autoteste prova a reprovação do plural sem lastro
O autoteste SHALL injetar, na cópia do procedimento de busca de uma só base, a declaração `plural: pela
lematização` com a linha "Lematização" não verificada, e exigir que só aquela base reprove;
e SHALL retirar a linha `plural` e exigir PROTOCOLO_ILEGIVEL.

#### Scenario: Defeito injetado numa base
- **WHEN** o autoteste injeta `plural: pela lematização` no procedimento de busca da WoS, com a lematização
  não verificada
- **THEN** a conferência da WoS reprova, as demais não reprovam, e o autoteste falha se
  isso não ocorrer

### Requirement: Teto de caracteres declarado por base
`[cobertura]` da fonte de cada base SHALL ter `teto`, com um número inteiro positivo de
caracteres ou `"nenhum"`. O campo ausente, ou com outro valor, MUST reprovar com
PROTOCOLO_ILEGIVEL, nomeando a fonte e o campo.

#### Scenario: Linha ausente
- **WHEN** `[cobertura]` da fonte da WoS não tem `teto`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a fonte e o campo

#### Scenario: Valor ilegível
- **WHEN** `teto = "curto"`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando o domínio do teto

### Requirement: Consulta acima do teto reprova a base
Com teto numérico, a conferência SHALL medir o comprimento, em caracteres, de cada consulta
executável da base e MUST reprovar só aquela base quando alguma passar do teto, nomeando a
expressão, a consulta, o comprimento e o teto. Consulta executável é cada bloco das
expressões da seção 4, salvo a forma longa e o bloco rotulado como não executado, e cada
consulta da forma curada. Com `nenhum`, a conferência SHALL relatar, sem reprovar, a maior
consulta executável da base.

#### Scenario: Consulta acima do teto
- **WHEN** o procedimento de busca da ERIC declara `teto de caracteres | 1400` e a consulta 4a2 tem 1.450
  caracteres
- **THEN** `documentos conferir` reprova a ERIC, nomeando EB4, a consulta 4a2, 1450 e 1400; as demais
  bases não são afetadas

#### Scenario: Consulta no limite
- **WHEN** a maior consulta da base tem exatamente o comprimento do teto declarado
- **THEN** essa dimensão não reprova

#### Scenario: Sem teto
- **WHEN** o procedimento de busca da Scopus declara `teto de caracteres | nenhum`
- **THEN** `documentos conferir` relata a maior consulta da Scopus com o comprimento, e o código não
  muda por esse relato

### Requirement: Estratégia de proximidade não é forma executável
O fragmento `estrategia_de_proximidade.md` da fonte SHALL ser texto de discussão. Bloco
cercado nele não entra no derivado da base, não se executa e não se confere. O fragmento não
é exigido. O gerador o escreve na subseção `### Estratégia de proximidade` da seção 4.

#### Scenario: Bloco cercado na estratégia de proximidade
- **WHEN** a fonte da WoS ganha `estrategia_de_proximidade.md` com um bloco cercado
- **THEN** o derivado da WoS é igual ao de antes, e o procedimento ganha só a subseção

### Requirement: Autoteste prova o teto e a estratégia de proximidade
O autoteste SHALL:
- declarar, na cópia do procedimento de busca de uma só base, um teto uma unidade abaixo da maior consulta
  e exigir que só aquela base reprove;
- declarar o teto igual à maior consulta, com separador de milhar, e exigir que passe;
- retirar a linha `teto de caracteres` e exigir PROTOCOLO_ILEGIVEL;
- deformar o valor do teto e exigir PROTOCOLO_ILEGIVEL;
- inserir a subseção de estratégia de proximidade com bloco cercado e exigir o derivado
  inalterado.

#### Scenario: Conferência desligada
- **WHEN** a conferência do comprimento contra o teto é desligada
- **THEN** o caso do teto abaixo da maior consulta falha

### Requirement: Conferências leem a fonte
As conferências desta capacidade SHALL ler a estrutura derivada da fonte do procedimento da
base (`fonte-do-procedimento`), e não o markdown gerado, que se confere só por igualdade
(`geracao-dos-procedimentos`). O campo e o filtro de cada bloco SHALL vir de `[composicao]`
e de `[[criterios]]`, e MUST NOT ser reconhecidos pelo texto do bloco.

#### Scenario: Correspondência com a fonte
- **WHEN** a conferência examina o que antes lia nas seções 1, 2 e 3, nos blocos e na forma
  curada
- **THEN** lê, respectivamente, `[[sintaxe]]`, `[[criterios]]`, `[cobertura]` e
  `[[reducao]]`, os blocos compostos pelo gerador e `[[curadas]]`

#### Scenario: Campo declarado, não inferido
- **WHEN** a fonte da ERIC declara FCT1 no campo `title`
- **THEN** a conferência trata FCT1 da ERIC como campo `title`, sem ler o prefixo do bloco

#### Scenario: Invariante protege contra gerador errado
- **WHEN** o autoteste faz o compositor omitir um termo da STR3 no bloco de EB4 de uma base
- **THEN** a conferência "Termos do bloco conferem com as facetas declaradas" reprova só
  aquela base
