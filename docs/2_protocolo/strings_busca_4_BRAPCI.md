# Strings de busca — BRAPCI

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º passo, e Etapa 2, 1º passo.  
**Fonte:** BRAPCI — Base de Dados Referencial de Artigos de Periódicos em Ciência da Informação. **Elaborado em:** 05/11/2026.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** VT.  
**Revisão:** 08/11/2026 — recorte temporal 2017–2026 e saída da instanciação em estruturas computacionais do objeto da revisão. Quatro facetas, quatro expressões, quatro questões secundárias. Cronologia das decisões, com as reduções anteriores: Anexo A, seções 1 e 5.

---

## 1. Estado de verificação da sintaxe — ATENÇÃO

**Nada da sintaxe de consulta da BRAPCI foi verificado.** O ambiente desta sessão não alcançou o sítio da base, e nenhuma documentação de sua sintaxe foi localizada em fontes secundárias.

| Elemento | Situação | O que se apurou |
| :--- | :--- | :--- |
| Sítio da base | **Não alcançado** | o domínio não está acessível pelas ferramentas desta sessão |
| Documentação de sintaxe | **Não localizada** | a literatura consultada que utiliza a BRAPCI em revisões sistemáticas declara apenas que “as *strings* foram adaptadas, conforme a sintaxe utilizada em cada base de dados”, sem reproduzir a versão adaptada para a BRAPCI |
| Campos pesquisáveis | **Não verificados** | um estudo metodológico sobre recuperação na BRAPCI trabalha com os campos **título, palavras-chave e resumo**, o que sugere a sua existência, mas não documenta como invocá-los em consulta |
| Operadores booleanos, aspas, parênteses, truncamento | **Não verificados** | nenhuma fonte |
| Filtros de período, tipo documental e texto completo | **Não verificados** | nenhuma fonte |

> **Regra adotada em consequência.** Esta ficha **não** apresenta uma expressão longa como se fosse executável. Ela apresenta: (a) uma sondagem de sintaxe obrigatória; (b) um conjunto de consultas curtas, de uma e de duas facetas, que funciona sob a hipótese mais restritiva — base que aceite apenas palavras e frases; (c) a forma longa de contingência, a usar **somente** se a sondagem confirmar aspas, `AND`, `OR` e parênteses. Qualquer string que fosse aqui declarada “completa e executável” antes da sondagem seria invenção.

---

## 2. Sondagem de sintaxe — **EXECUTADA em 09/11/2026**

Nove sondagens, executadas pelo ReT. A base deixa de ser a única das quatro sem sintaxe medida. **Todas em *Local de pesquisa* = Todos os campos, sem filtro de ano** — ajuste identificado por medição em 10/11/2026, não anotado no momento da execução; ver a seção 2.2.

| # | Consulta | O que testava | Retorno | Veredito |
| :---: | :--- | :--- | ---: | :--- |
| 1 | `ontologia` | linha de base | 545 | referência das demais |
| 2 | `representação do conhecimento` | frase sem aspas | **1.000** | **não é frase** — e o número redondo levanta suspeita de teto |
| 3 | `"representação do conhecimento"` | aspas como frase | 659 | **aspas funcionam**: 659 < 1.000 |
| 4 | `ontologia AND educação` | conjunção em maiúsculas | 13 | **`AND` funciona**: 13 ≪ 545 |
| 5 | `ontologia and educação` | conjunção em minúsculas | 13 | **insensível à caixa**: idêntico a #4 |
| 6 | `ontologia OR tesauro` | disjunção | 840 | **`OR` funciona**: 840 > 545 |
| 7 | `(ontologia OR tesauro) AND educação` | agrupamento | 20 | **parênteses funcionam**: 20 ≥ 13, e o excedente é o que `tesauro` acrescenta |
| 8 | `ontolog*` | truncamento | 984 | **curinga funciona**: 984 > 545 |
| 9 | inspeção da interface | campos e filtros | — | **há filtros**: ano inicial e final, tipo de publicação e outros |

### 2.1 O que a sondagem decidiu

**Os parênteses funcionam, e isso dispensa a seção 5.** A forma de contingência existia porque a sintaxe era desconhecida e se temia que `AND`, `OR` e parênteses não operassem. Os três operam. Soma-se a isso o que a conferência do conjunto-semente já havia medido: a forma de contingência, por ler só o núcleo das facetas, **não recupera nenhuma das duas sementes desta base**. Não há razão para executá-la. **Executa-se a seção 4, e a 5 fica como registro.**

**O truncamento muda a economia das consultas nesta base.** `ontolog*` devolve 984 contra 545 de `ontologia` — alcança de uma vez `ontologias`, `ontológico`, `ontológica` e `ontológicos`, que o desdobramento de 08/11 acrescentara um a um. O desdobramento não foi em vão: ele serve à Web of Science, à Scopus e à ERIC, onde o curinga não existe ou não ajuda — na ERIC, `ontolog*` devolveu **zero**, medido em 08/11. Aqui, porém, o radical substitui a lista, e é a forma a preferir.

**Há filtros na interface, e o recorte temporal entra por eles.** Ano inicial e final, tipo de publicação e outros. O intervalo de 2017 a 2026 aplica-se na própria busca, como nas demais bases, e não por pós-filtragem.

> **Errata de 09/11/2026, em duas partes.** A primeira leitura da sondagem #9 registrou que a base não tinha campos nem filtros, e daí se concluiu que o recorte temporal sairia da consulta e que não haveria como restringir a busca por campo. **As duas conclusões ficam sem efeito**, por correções do ReT em 10/11: os filtros de ano e de tipo existem, e existe também um seletor de **Local de pesquisa**, com as opções *Título*, *Resumo*, *Palavras-chave*, *Autor* e *Todos os campos*. Registro das correções no Anexo A.

**Decisão sobre o filtro de tipo de publicação: não se usa.** Pelo mesmo motivo registrado para o campo `publicationtype` da ERIC — o protocolo admite artigo, anais, capítulo e relatório técnico, e restringir o tipo excluiria material elegível. Usa-se **apenas o filtro de ano**.

### 2.2 Local de pesquisa — a base restringe por campo, por seletor

O seletor **Local de pesquisa** oferece *Título*, *Resumo*, *Palavras-chave*, *Autor* e *Todos os campos*. É a mesma capacidade que a ERIC exerce por prefixo de campo, exercida aqui por interface — com uma diferença que decide a estratégia.

| | ERIC | BRAPCI |
| :--- | :--- | :--- |
| Como se restringe | prefixo por termo: `title:ontology AND abstract:education` | seletor único, aplicado à consulta inteira |
| Campos diferentes na mesma consulta | **sim** — é a base da execução em camadas | **não**, salvo se a interface oferecer linhas de busca empilháveis, o que não foi verificado |
| Efeito sobre a estratégia | artefato no título, âncora de domínio no resumo | a consulta inteira num campo só; combinar campos exige consultas separadas e união no Zotero |

**Decisão de execução: *Todos os campos*, com o filtro de ano.** E4 é a expressão de cobertura, e restringir o campo contraria a sua função. As demais opções ficam como instrumentos, não como forma de execução:

- ***Título*** — instrumento de **precisão** e de **partição**. Se uma consulta encostar no teto de 1.000 mesmo com o recorte temporal, repeti-la em *Título* devolve o núcleo mais pertinente e permite estimar quanto do excedente era ruído.

- ***Resumo*** e ***Palavras-chave*** — instrumentos de **medição de cobertura**. Comparar o retorno de um mesmo termo nos três campos informa onde a base de fato indexa, que é o que nenhuma das quatro fichas sabe sobre esta base.

- ***Autor*** — não se usa na busca; serve ao *backward search* e à conferência de duplicatas, como o campo `author` da ERIC.

#### Linha de base e cobertura de campo — **MEDIDAS em 10/11/2026**

Sete consultas do mesmo termo, `ontologia`, executadas pelo ReT. São a primeira medição de **onde esta base indexa** — informação que nenhuma das quatro fichas tinha.

| # | Local de pesquisa | Filtro de ano | Retorno | Fração da linha de base |
| :---: | :--- | :--- | ---: | ---: |
| A1 | **Todos os campos** | nenhum | **545** | linha de base |
| A2 | Título | nenhum | 151 | 27,7% |
| A3 | Resumo | nenhum | 373 | 68,4% |
| A4 | Palavras-chave | nenhum | 358 | 65,7% |
| A5 | Autor | nenhum | 0 | 0% |
| B1 | **Todos os campos** | **2017-2026** | **280** | 51,4% |
| B2 | Título | **2017-2026** | 74 | 13,6% |

**A ressalva das nove sondagens está resolvida, e pelo melhor dos desfechos possíveis.** A1 devolveu **exatamente 545**, que é o retorno da sondagem #1 de 09/11, e **nenhuma das outras quatro opções devolveu esse número**. O ajuste em vigor naquele dia era, portanto, *Todos os campos*, sem filtro de ano. **Os nove retornos de 09/11 voltam a ser reprodutíveis**, com o ajuste declarado ao lado deles, e não há número a descartar. Era um dos três desfechos previstos; os outros dois obrigariam a declarar os nove números irreprodutíveis.

**O seletor restringe de fato.** 151, 373 e 358 contra 545 não são compatíveis com um seletor inoperante, que devolveria o mesmo número cinco vezes. *Resumo* e *Palavras-chave* restringem pouco; *Título* restringe muito; *Autor* devolve zero, o que é o esperado para um termo que não é nome de pessoa. **Ressalva, porque a diferença importa:** A5 = 0 é *coerente* com a opção *Autor* funcionar, mas não a **prova** — um seletor que não devolvesse nada para consulta alguma daria o mesmo zero. Uma consulta com sobrenome real resolve, e ela já é necessária por outro motivo — ver a seção 6.

**151 + 373 + 358 = 882, contra 545 no conjunto.** Pelo menos **337 registros trazem o termo em mais de um campo**, o que era de esperar: resumo e palavras-chave recobrem-se largamente. A leitura que interessa é a inversa: **394 dos 545 registros não trazem `ontologia` no título** e **172 não o trazem no resumo**. Nesta base, o título é um campo pobre.

**Consequência que confirma a decisão de execução e mede o que era estimativa.** Restringir a consulta ao título custaria, neste termo, **72,3% do que *Todos os campos* recupera**. Compare-se com a ERIC, onde a restrição ao título custou **zero** das três sementes esperadas. A assimetria entre as duas bases deixa de ser argumento e passa a ser número: **a ERIC suporta a execução por campo; a BRAPCI não**, e E4 executa-se aqui em *Todos os campos*. *Título* fica onde estava — instrumento de partição e de precisão, nunca forma de execução.

**Conferência interna que reforça a medida.** A fração do título é **27,7% sem filtro** e **26,4% dentro do recorte** (74 de 280). A estabilidade entre as duas passagens indica que a pobreza do campo título não é efeito do recorte temporal: é característica da indexação da base.

### 2.3 Teto de 1.000 registros — confirmado

A sondagem #2 devolveu exatamente 1.000, e o ReT confirmou em 10/11/2026 que **a base tem limite de 1.000 registros**. Não é contagem: é corte. **Retorno de 1.000 não vai ao IO 2 como número** — significa que a consulta devolveu *pelo menos* 1.000 e que o excedente não foi exibido nem exportado.

**A recomendação do ReT é o recorte temporal, e ela resolve o problema pela raiz.** Os retornos da sondagem foram medidos **sem** filtro de ano, sobre o acervo inteiro da base. Com 2017 a 2026 aplicado na interface, as consultas caem para uma fração disso. Duas delas são as que mereciam atenção:

| Consulta | Sem filtro | Com 2017-2026 | Situação |
| :--- | ---: | ---: | :--- |
| `ontolog*` | 984 | ~506 | **estimativa**, pela razão medida em `ontologia` |
| `"representação do conhecimento"` | 659 | ~339 | **estimativa**, idem |
| `ontologia` | 545 | **280** | **medido em 10/11/2026** |

**A razão medida é 51,4%**: de 545 registros com `ontologia` em todo o acervo, 280 estão entre 2017 e 2026 — pouco mais da metade da produção indexada com esse termo é anterior ao recorte. **As duas outras linhas são extrapolação dessa razão e estão assinaladas como tais**: a proporção de material recente varia de termo para termo, e `ontolog*` alcança formas adjetivais cuja distribuição no tempo não foi medida. Servem para dimensionar o risco, não para ir ao IO 2.

**O risco de teto cai, mas a regra não muda.** Sob a razão medida, a consulta mais próxima do limite — `ontolog*`, 984 sem filtro — ficaria em torno de 500 com o recorte, folgadamente abaixo de 1.000. Isso **não dispensa** anotar o retorno de cada consulta: é estimativa de um termo aplicada a outro, e o custo de errar é uma exportação truncada que não se anuncia.

**Regra de execução, que vale para toda consulta desta ficha.** Aplicar o filtro de ano **antes** de executar. Anotar o retorno. **Se ainda assim vier 1.000, a consulta está truncada** e precisa ser partida — por idioma, por subconjunto de termos ou por subintervalo de anos — até que nenhuma parte encoste no teto; somam-se então as partes e registra-se a sobreposição entre elas, como já se faz na ERIC.

> **Por que isso importa mais nesta base que nas outras.** A estratégia da faceta 🟦 isolada é a rede de segurança da BRAPCI: ela varre a produção nacional sobre representação do conhecimento sem exigir a âncora de domínio, justamente porque o domínio educacional nem sempre é nomeado em título e resumo na literatura brasileira de Ciência da Informação. É a consulta mais larga da ficha, e portanto a que mais arrisca o teto.

**Questão menor, que fica anotada e não exige sondagem.** Com o teto confirmado, o 1.000 da sondagem #2 está explicado, e já não se pode inferir dele o que a base faz com duas palavras **sem aspas** — se as une por `OR` ou se as conjuga. A pergunta fica sem resposta e **sem consequência prática**: todas as consultas da seção 4 ou trazem a frase entre aspas ou explicitam o `AND`, de modo que nenhuma depende do comportamento implícito.

Registrar as contagens e a inspeção no IO 2, com capturas de tela.

### 2.4 Execução das quatro expressões — **EXECUTADA, E PROVISÓRIA**

#### Estado da interface, lido nas capturas de tela

| Controle | Como estava |
| :--- | :--- |
| Ano inicial / Ano final | 2017 / 2026, nas quatro |
| Tipo de publicação | as quatro caixas marcadas — revistas brasileiras e estrangeiras, anais de eventos, livros e capítulos. Equivale a não filtrar por tipo |
| Local de pesquisa | Todos os campos, nas quatro |
| Método de busca | **Método ponderado**, nas quatro — e há outras duas opções |
| Limite de resultados | 1.000 em E1, E2 e E3; 5.000 em E4 |

**Dois controles que nenhum artefato do pacote conhecia.** A inspeção anterior desta base registrou o seletor de *Local de pesquisa* e os filtros de ano e de tipo. As capturas mostram mais dois: **Método de busca**, com três opções — *Método anterior (2024)*, *Método atual (2026)* e *Método ponderado* —, e **Limite de resultados**, de 1.000 a 5.000. **É a quarta vez que a inspeção desta interface se revela incompleta**, e a conclusão já registrada confirma-se: inspeção de interface é a classe de evidência mais frágil do pacote.

**O limite não cortou, e agora isso está medido.** Os retornos — o maior é 64 — ficam muito abaixo de 1.000, e a exportação traz 64 registros com 64 identificadores distintos. Nenhuma das quatro consultas encostou em teto algum.

**O recorte temporal estava aplicado, e a exportação confirma-o por dentro**: os 64 registros distribuem-se de 2017 a 2026, sem um único fora da janela.

#### Retornos

| Expressão | Composição | Retorno | Procedência |
| :--- | :--- | ---: | :--- |
| **E1** | 🟦 AND 🟨 AND 🟥 AND 🟧 | **0** | captura: “Nenhum resultado encontrado” |
| **E2** | 🟦 AND 🟨 AND 🟥 | 5 | captura: “Selecionar os 5 itens” |
| **E3** | 🟦 AND 🟨 AND 🟧 | 1 | captura: “Selecionar o 1 item” |
| **E4** | 🟦 AND 🟨 | **64** | **contagem da exportação** |

> **Retificação.** Os retornos informados primeiro foram E2 = 9 e E4 = 88. As capturas e a exportação medem **E2 = 5** e **E4 = 64**. Prevalece o que se pode contar: a exportação para E4, a captura para as demais. Os números anteriores não vão ao IO 2.

**Conferência de coerência, e passa.** A arquitetura obriga E1, E2 e E3 a caberem em E4, e E1 a caber em E2 e em E3: 0 ≤ 1 ≤ 64 e 0 ≤ 5 ≤ 64; a união de E2 e E3 fica entre 5 e 6, e cabe em 64. Contagem coerente não prova identidade de conjuntos, mas incoerência reprovaria na hora.

#### O achado que muda a leitura de todos estes números

**A expressão executada não é a expressão registrada.** As capturas mostram, grupo a grupo, uma fração do vocabulário do IO 1:

| Faceta | Termos executados | Termos registrados no IO 1 | Fração |
| :---: | ---: | ---: | ---: |
| 🟦 | 7 | 55 | 13% |
| 🟨 | 15 | 60 | 25% |
| 🟥 | 5 | 55 | 9% |
| 🟧 | 7 | 55 | 13% |

O grupo da faceta 🟦 executado traz **sete** termos — o núcleo em português e em inglês —, e **não traz `ontologia`, `tesauro`, `taxonomia`, `esquema de metadados`, `modelo conceitual` nem nenhum dos demais**. Os grupos 🟥 e 🟧 trazem o núcleo em português e nada mais; o 🟨 traz núcleo e próximos, também só em português. **É, na prática, a forma de contingência da seção 5 desta ficha**, não as expressões do Item 2 do IO 1.

**Consequência direta:** os 64 registros de E4 medem o alcance do NÚCLEO, não o do vocabulário registrado. Não são o retorno de E4 e **não podem ser lançados no IO 2 como tal**. Medem outra coisa — e medem-na bem, o que os torna úteis como piso.

#### Conferência do conjunto-semente

| Semente | Esperada aqui | Na exportação |
| :--- | :---: | :--- |
| 1 — Alvarenga & Cristovão | sim | **encontrada**, registro 338139 |
| 5 — Sousa & Duque | sim | **ausente** |

**A semente 1 foi recuperada, e o modo como o foi corrige esta ficha.** O casamento não é pelo título, que diz *objetos de aprendizagem* e *ontologia operacional de domínio*: é pela **palavra-chave `Representação do conhecimento`**. A seção 6 desta ficha previa que a forma reduzida falhasse a âncora de artefato nas duas sementes desta base — **essa previsão foi feita contra o título e está errada para a execução em *Todos os campos***, onde as palavras-chave do autor carregam o núcleo. Fica como errata, e com uma lição de alcance maior: **o ensaio seco contra títulos subestima o recall de uma base que indexa palavras-chave**.

**A semente 5 está ausente, e a sua ausência ainda não tem causa.** Procurei por autor, por título e por palavra do título: não está entre os registros. Duas explicações continuam abertas e exigem coisas diferentes — **a base não indexa o estudo**, caso em que a semente sai do denominador desta base; ou **indexa e a forma reduzida não a alcança**, caso em que conta contra a aderência. A consulta que separa as duas continua a ser a mesma: `Duque` em *Local de pesquisa* = **Autor**.

#### Conformidade dos registros com a expressão

Dos 64 registros exportados, **63 contêm termo executado das duas âncoras** no texto exportado — publicação, título, palavras-chave e resumo. **Um não contém**: o registro 381891, em espanhol, sobre acervo documental escolar, em que não ocorre nenhum dos sete termos da faceta 🟦, por palavra ou por radical, em idioma algum.

**Eram duas explicações possíveis, e a medição escolheu uma.** Ou o *Método ponderado* ordenava por peso em vez de filtrar — e aí nada do que se mediu teria a semântica que o protocolo presume —, ou *Todos os campos* alcançava campo que a exportação não traz.

| Teste | Resultado |
| :--- | :--- |
| E4 em *Método ponderado* | 64 |
| E4 em *Método atual (2026)* | 64 |
| Registros com `KEYWORDS` **vazia** na exportação | 4 de 64, e o 381891 é um deles |

**O método não é o culpado, e o registro discrepante está explicado.** A reexecução em *Método atual (2026)* devolveu **o mesmo número**, de modo que a escolha de método não altera o volume do conjunto. E o 381891 é um dos quatro registros cuja coluna `KEYWORDS` **vem vazia na exportação** — justamente o campo onde a semente 1 casa a sua âncora de artefato. A base indexa mais do que exporta, e a não conformidade é **artefato da exportação, não da recuperação**.

> **Duas ressalvas que ficam, e são pequenas.** Contagem igual não prova conjunto igual: a identidade só se confirmaria comparando as duas exportações, e o custo não se justifica. E **toda conferência feita contra esta exportação tem um ponto cego de 6%** — os registros sem palavras-chave —, o que importa ao teste de aderência tanto quanto importou aqui: ausência de casamento no arquivo exportado não é ausência de casamento na base.

#### O que falta para estes números irem ao IO 2

| | O que falta | Por quê |
| :---: | :--- | :--- |
| 1 | **Reexecutar com a expressão registrada**, não com o núcleo | é a diferença entre medir o protocolo e medir uma redução dele |
| 2 | ~~Fixar o método de busca~~ **FEITO**: os dois métodos devolvem 64. Registrar no IO 2 o método adotado | é dado de reprodutibilidade, como o Local de pesquisa |
| 3 | `Duque` em *Autor* | separa “base não indexa” de “busca não alcança”, e decide o denominador da aderência |
| 4 | Fechar **P6** | substituição de termo autorizado vence busca executada antes dela |

**O que já NÃO falta**, e é ganho desta execução: o estado da interface está registrado; o recorte temporal está confirmado por dentro da exportação; o teto de 1.000 não cortou; a coerência entre as quatro expressões passa; a semente 1 está recuperada e o caminho pelo qual o foi está medido.

---

## 3. Critérios de elegibilidade: onde cada um é aplicado

| Critério | Na consulta? | Como |
| :--- | :--- | :--- |
| Intervalo temporal 2017–2026 | **Na consulta, pelo filtro de ano** | a inspeção de 09/11/2026 registrou por engano que a base não tinha filtros; as correções do ReT, de 10/11, restabelecem o filtro de ano inicial e final, o de tipo de publicação e o seletor de Local de pesquisa. Aplicar 2017 a 2026 na interface, antes de exportar. O filtro de **tipo de publicação não se usa**, porque restringir o tipo excluiria material elegível; o **Local de pesquisa fica em Todos os campos** na execução, e as demais opções servem de instrumento — seção 2.2 |
| Idiomas | **Dispensado** | a base é de produção brasileira em Ciência da Informação; as strings usam os termos em português, com os equivalentes em inglês apenas na faceta 🟦, onde a terminologia técnica circula em inglês na produção nacional |
| Tipo documental | **Dispensado** | a base é referencial de **artigos de periódicos**, o que já corresponde a um dos tipos admitidos pelo protocolo |
| Texto completo | **Não** | verificação individual na 2ª filtragem |
| Domínio educacional | **Sim**, por âncora | faceta 🟨 nas consultas combinadas; ver a ressalva 3 sobre o seu efeito nesta base |
| Adequação temática | **Não** | filtragens do Módulo 3, Etapa 3 |

---

## 4. Conjunto principal — consultas curtas (hipótese restritiva)

**Este é o conjunto a executar.** Todas as consultas abaixo, uma a uma, registrando o retorno de cada uma e deduplicando no Zotero. A sondagem de 09/11/2026 confirmou aspas, `AND`, `OR` e parênteses, de modo que a seção 5 não precisa ser executada.

> **Aplicar o filtro de ano 2017-2026 na interface ANTES de executar cada consulta.** O teto de 1.000 registros da base está confirmado, e os retornos da sondagem foram medidos sobre o acervo inteiro, sem recorte. **Retorno de exatamente 1.000 não é contagem, é corte**: anotá-lo como tal e partir a consulta — por idioma, por subconjunto de termos ou por subintervalo de anos — até que nenhuma parte encoste no teto, somando as partes e registrando a sobreposição. **Local de pesquisa: Todos os campos** — ver as seções 2.2 e 2.3.

> **Forma preferível nesta base: o truncamento.** Onde a lista traz variantes de um mesmo radical, `ontolog*` substitui `ontologia`, `ontologias` e as formas adjetivais numa só consulta — medido em 09/11: 984 contra 545. As consultas abaixo mantêm as formas explícitas porque são o registro do vocabulário; ao executar, pode-se usar o radical e anotar a substituição.

### 4.1 Faceta 🟦 isolada — varredura da representação do conhecimento na produção nacional

| # | Consulta |
| :---: | :--- |
| 1 | `"representação do conhecimento"` |
| 2 | `"organização do conhecimento"` |
| 3 | `"sistema de organização do conhecimento"` |
| 4 | `ontologia` |
| 5 | `ontologias` |
| 6 | `"ontologia de domínio"` |
| 7 | `"modelo conceitual"` |
| 8 | `"modelagem conceitual"` |
| 9 | `"engenharia de ontologias"` |
| 10 | `tesauro` |
| 11 | `taxonomia` |
| 12 | `"vocabulário controlado"` |
| 13 | `"esquema de metadados"` |
| 14 | `"classificação facetada"` |
| 15 | `"análise facetada"` |

> **Acréscimo de 09/11/2026, decisão D3.** As consultas de classificação e análise facetada entraram por ampliação conceitual do vocabulário, e nesta base valem mais que nas outras três: a tradição de Ranganathan tem presença forte na Ciência da Informação brasileira, e a produção nacional sobre análise facetada é substancial. As consultas da seção 4 são curadas uma a uma e **não se atualizam sozinhas** quando o vocabulário muda — ao contrário das expressões longas da seção 5, que leem as facetas. Todo acréscimo de termo exige revisitar esta lista.

A faceta 🟦 isolada é executada na íntegra porque, nesta base, o conjunto de artigos sobre representação do conhecimento é da ordem de grandeza que a leitura de títulos comporta, e porque o cruzamento com 🟨 pode falhar quando o vínculo educacional está no corpo do texto e não nos metadados. O resultado da faceta isolada é a **rede de segurança** desta base.

### 4.2 Pares 🟦 + 🟨 — representação no domínio educacional

| # | Consulta |
| :---: | :--- |
| 1 | `"representação do conhecimento" AND educação` |
| 2 | `"representação do conhecimento" AND ensino` |
| 3 | `"representação do conhecimento" AND aprendizagem` |
| 4 | `"representação do conhecimento" AND educacional` |
| 5 | `"organização do conhecimento" AND educação` |
| 6 | `"organização do conhecimento" AND ensino` |
| 7 | `"organização do conhecimento" AND aprendizagem` |
| 8 | `"organização do conhecimento" AND educacional` |
| 9 | `ontologia AND educação` |
| 10 | `ontologia AND ensino` |
| 11 | `ontologia AND aprendizagem` |
| 12 | `ontologia AND educacional` |
| 13 | `"modelo conceitual" AND educação` |
| 14 | `"modelo conceitual" AND ensino` |
| 15 | `"modelo conceitual" AND aprendizagem` |
| 16 | `"modelo conceitual" AND educacional` |
| 17 | `tesauro AND educação` |
| 18 | `tesauro AND ensino` |
| 19 | `tesauro AND aprendizagem` |
| 20 | `tesauro AND educacional` |
| 21 | `taxonomia AND educação` |
| 22 | `taxonomia AND ensino` |
| 23 | `taxonomia AND aprendizagem` |
| 24 | `taxonomia AND educacional` |
| 25 | `"análise facetada" AND educação` |
| 26 | `"análise facetada" AND ensino` |
| 27 | `"análise facetada" AND aprendizagem` |
| 28 | `"análise facetada" AND educacional` |

### 4.3 Pares com as demais facetas

| # | Consulta | Facetas |
| :---: | :--- | :--- |
| 1 | `ontologia AND "prática pedagógica"` | 🟦 + 🟥 |
| 2 | `ontologia AND "prática educacional"` | 🟦 + 🟥 |
| 3 | `"representação do conhecimento" AND "prática pedagógica"` | 🟦 + 🟥 |
| 4 | `ontologia AND "sequência didática"` | 🟦 + 🟥 |
| 5 | `ontologia AND "contexto de aplicação"` | 🟦 + 🟧 |
| 6 | `ontologia AND contexto` | 🟦 + 🟧 |
| 7 | `ontologia AND "situação de aprendizagem"` | 🟦 + 🟧 |
| 8 | `"modelo conceitual" AND "contexto educacional"` | 🟦 + 🟧 |
| 9 | `"objeto de aprendizagem" AND metadados` | 🟨 + 🟦 |
| 10 | `"recursos educacionais abertos" AND metadados` | 🟨 + 🟦 |

---

## 5. Forma longa — **não se executa**, fica como registro

> **Decidido em 09/11/2026, por duas razões convergentes.** A primeira: esta seção existia como contingência, para o caso de a sondagem reprovar aspas, `AND`, `OR` ou parênteses — e a sondagem aprovou os quatro, de modo que a contingência perdeu o motivo. A segunda, e decisiva: as facetas abaixo usam o **núcleo** de cada quadro, e não a lista integral; confrontada com o conjunto-semente, essa redução **não recupera nenhuma das duas sementes que esta base deve indexar**, porque o núcleo da faceta 🟦 tem três expressões e nenhuma ocorre nos dois títulos, que dizem `ontologia` e `modelo de sistema da informação`.

Fica registrada por rastreabilidade e por um uso residual: se a execução da seção 4 mostrar que o teto de 1.000 atrapalha consulta a consulta, estas expressões longas são o ponto de partida para uma forma intermediária — **acrescentando ao núcleo os termos de *próximos* que as sementes exigem, `ontologia` à frente de todos**, com emenda registrada.

### `#1` — 🟦 Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems")
```

### `#2` — 🟨 Domínio educacional — **âncora obrigatória**

```
("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos")
```

### `#3` — 🟥 Práticas do processo de ensino-aprendizagem

```
("prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente")
```

### `#4` — 🟧 Fatores situacionais

```
("fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem")
```

### Expressões

**E1** (geral) — todas as strings montadas. **“Geral” é a composição, não o alcance**: por exigir as quatro facetas simultaneamente, é a MAIS RESTRITIVA das quatro &nbsp;·&nbsp; 🟦 AND 🟨 AND 🟥 AND 🟧 &nbsp;·&nbsp; **derivada**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems") AND ("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos") AND ("prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente") AND ("fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem")
```

**E2** (específica) — modelos e ontologias que representam práticas do processo de ensino-aprendizagem &nbsp;·&nbsp; 🟦 AND 🟨 AND 🟥 &nbsp;·&nbsp; **derivada** (executar só no teste de fidelidade)

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems") AND ("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos") AND ("prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente")
```

**E3** (específica) — artefatos que formalizam os fatores situacionais do domínio educacional &nbsp;·&nbsp; 🟦 AND 🟨 AND 🟧 &nbsp;·&nbsp; **derivada** (executar só no teste de fidelidade)

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems") AND ("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos") AND ("fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem")
```

**E4** (de cobertura) — artefatos de representação do conhecimento no domínio educacional, inclusive quando não mencionam as demais facetas nos metadados &nbsp;·&nbsp; 🟦 AND 🟨 &nbsp;·&nbsp; **EXECUTADA**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems") AND ("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos")
```

As expressões de três facetas ou mais tendem, nesta base, a retorno nulo ou próximo de zero. O retorno nulo **é informação**: registra-se no IO 2 e constitui indício para a enunciação da lacuna na produção nacional. Não se deve, por causa dele, relaxar a âncora 🟦.

---

## 6. Conjunto-semente — o que esta base deve recuperar

O conjunto-semente tem **10 estudos**, todos conferidos em fonte e todos dentro do escopo. Pela indicação do ReT, **2 são esperados nesta base**. Instrumento completo, procedimento e estado de conferência de cada referência: `data/saida/semente/Conjunto_Semente.md`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| 1 | Alvarenga & Cristovão (2023) | — | — |
| 5 | Sousa & Duque (2018) | `10.5433/1981-8920.2018v23n1p271` | **caso-teste de cobertura de campo** |

**Procedimento, em duas etapas, e não confundir as duas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões da revisão, para saber se a base indexa a semente. Semente não indexada **sai do denominador desta base**, e isso se registra como cobertura da base, não como falha da busca. *Etapa 2:* procurar a semente na exportação de E4 já feita, por DOI e depois por título — **sem reexecutar a busca**, porque o teste se faz sobre o que a execução de fato devolveu.

**Limiar de 80%, e o que a reprovação obriga.** O IO 1 fixa o limiar e manda, abaixo dele, revisar o controle terminológico antes de prosseguir, com emenda registrada. O número que decide é o **global**, sobre a união das bases: perder uma semente aqui e achá-la em outra não é perda de portfólio. A aderência por base serve para diagnosticar **qual** base e **qual** faceta falharam.

**Lematização nesta base:** **não medida, mas contornada.** A sondagem de 09/11/2026 não testou lematização, e por isso ela permanece desconhecida — mas mediu o **truncamento**, que funciona: `ontolog*` devolveu 984 contra 545 de `ontologia`. O radical alcança as variantes morfológicas de uma vez, de modo que, nesta base, a questão da lematização deixa de ser crítica. Importa porque o desdobramento morfológico de 08/11/2026 acrescentou plurais e formas adjetivais às facetas: onde a base lematiza, o plural é redundante; onde não lematiza, era perda silenciosa. A **derivação adjetival** é outro caso: `ontological` não é flexão de `ontology`, e **base alguma a alcança** a partir do substantivo. Foi por isso que entrou no vocabulário — duas sementes do conjunto falhavam a âncora de artefato só por causa dela.

**Caso-teste de cobertura de campo nesta base.** Em semente 5, o **artefato** está fora do título — a ontologia das salas de aula é o resultado pretendido, descrito no resumo, enquanto o título anuncia um *modelo de sistema da informação*. A recuperação depende, portanto, do resumo e das palavras-chave. **Se E4 recuperar, recuperou por campo que não é o título, e isso é evidência medida de que a cobertura de campo desta base basta; se não recuperar, a perda deixa de ser estimada e passa a ser medida.** Anotar o resultado por extenso no registro de execução.

**Achado que muda o peso das duas formas desta ficha.** O conjunto-semente foi confrontado com o vocabulário das duas formas, e o resultado separa-as:

| Forma | Semente 1 (Alvarenga & Cristovão) | Semente 5 (Sousa & Duque) |
| :--- | :--- | :--- |
| **Principal** (seção 4, consultas curtas) | recuperada — `ontologia` casa nas consultas 4.1 nº 4 e 4.2 nº 11 | **não recuperada pelo título** — nenhuma consulta da seção 4 casa |
| **Contingência** (seção 5, só o núcleo) | **não recuperada** — o título não traz termo algum do núcleo da faceta 🟦 | **não recuperada** — idem |

**A forma de contingência falha a âncora de artefato nas duas sementes desta base.** O núcleo da faceta 🟦 tem três expressões — *representação do conhecimento*, *organização do conhecimento*, *sistema de organização do conhecimento* — e nenhuma ocorre nos dois títulos, que dizem `ontologia` e `modelo de sistema da informação`. `ontologia` é termo de **próximos**, e a contingência não o lê.

Consequências, e nenhuma delas é pequena. Primeira: **a forma principal é a forma desta base**, e a contingência é o que ela diz ser — contingência, a usar só se a sondagem reprovar aspas, `AND`, `OR` e parênteses. Segunda: **se a contingência for usada, a reprovação no teste de aderência é esperada e não diagnostica a busca**; nesse caso o limiar de 80% não se aplica à contingência sem ressalva escrita, porque mediria a redução ao núcleo e não o controle terminológico. Terceira: se a sondagem reprovar parênteses, o caminho não é a contingência como está, e sim **acrescentar ao seu núcleo os termos de próximos que as sementes exigem** — `ontologia` à frente de todos —, com emenda registrada.

**Semente 5 é o caso-teste de cobertura de campo desta base, e a medição de 10/11/2026 o levou até a última pergunta.** O título — *modelo de sistema da informação* — não nomeia artefato algum do núcleo da faceta 🟦: a ontologia das salas de aula é o resultado pretendido, descrito no resumo. As sete consultas da seção 2.2 mediram onde a base indexa, e o quadro é favorável à semente:

| Local de pesquisa | `ontologia` | O que isso diz sobre a semente 5 |
| :--- | ---: | :--- |
| Todos os campos | 545 | é a forma de execução, e a mais larga das cinco |
| Resumo | 373 | **a base indexa resumo com folga** — 68,4% da linha de base. É por aqui que a semente é alcançável, se o resumo trouxer o termo |
| Palavras-chave | 358 | segunda via, 65,7% |
| Título | 151 | 27,7%. **394 dos 545 registros não trazem o termo no título**, e a semente 5 é quase certamente um deles |

**O que falta é uma única consulta, e ela resolve duas coisas.** Os números acima dizem que a base indexa resumo e palavras-chave; não dizem se **este** registro traz `ontologia` em algum deles. Consultar `Duque` em *Local de pesquisa* = **Autor**, abrir o registro de Sousa & Duque (2018) e ler resumo e palavras-chave responde diretamente — e, de quebra, é o controle que falta à opção *Autor*, cujo zero em `ontologia` é coerente com funcionar mas não o prova.

| Achado | Leitura |
| :--- | :--- |
| o resumo ou as palavras-chave trazem `ontologia` | **a semente é recuperável por E4 em *Todos os campos***, e a falha medida era de campo, não de vocabulário. Encerra o caso-teste |
| nem o resumo nem as palavras-chave trazem o termo | a faceta 🟦 não alcança este registro nesta base por via alguma. O problema passa a ser de **vocabulário**, e a semente deixa de medir campo para medir faceta — emenda a discutir com a VT |
| a consulta por `Duque` devolve zero | a opção *Autor* não funciona, ou o registro não está indexado. Nos dois casos é achado a registrar antes de qualquer uso do campo no *backward search* |

---


## 7. Registro de execução (alimenta o IO 2)

| Bloco | Consulta | Data | Campo(s) | Filtros | Retornos | Observações |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| Sondagem | 1 a 9 | | | | | |
| 4.1 | 1 a 13 | | | | | |
| 4.2 | 1 a 24 | | | | | |
| 4.3 | 1 a 17 | | | | | |
| 5 | E1 a E4 | | | | | |

> **Derivação.** As contagens derivadas pressupõem o protocolo corrente: rodar
> `python3 src/protocolo.py --gerar`; registrar a execução com
> `python3 src/derivar_expressoes.py --registrar <base> E4 <arquivo> --retorno <n>`; e rodar
> `python3 src/derivar_expressoes.py --derivar`, todos da raiz do repositório. O registro
> confere o retorno declarado contra o arquivo e **recusa registrar quando divergem**; a
> derivação reconfere a contagem e recusa cópia defasada do protocolo. Cada derivado guarda
> o `sha256` do documento de origem.

---

## 8. Ressalvas

1. **Esta ficha é um roteiro de execução condicionado, não um conjunto de strings verificadas.** A sintaxe da BRAPCI não foi confirmada em nenhuma fonte. A primeira tarefa na base é a sondagem da seção 2; a forma final das strings decorre dela e esta ficha deve ser atualizada com o que a sondagem revelar, com data e capturas de tela.

2. **Estatuto dos termos — decisão de 06/11/2026.** Todos os termos desta ficha são **termos livres**: nesta data nenhum deles foi confrontado com instrumento algum. São 365 registros de termo nas quatro facetas — 123 em português, 119 em inglês e 123 em espanhol. A validação terminológica do 2º passo é feita em duas vias. *Via automatizada:* Tesauro Brasileiro de Ciência da Informação (IBICT), por interface de serviços TemaTres, para os termos em português; e UNESCO Thesaurus, por endpoint SPARQL, para os termos em inglês e em espanhol. *Sem consulta:* ERIC Thesaurus, Brased/INEP, ACM CCS, LISTA, W3C e IEEE LOM — os termos que deles dependeriam permanecem termos livres até o encerramento da revisão, e assim devem ser declarados no relatório. A ausência de validação não retira o termo das expressões de busca; retira-lhe apenas a qualidade de descritor autorizado. Concluída a validação, só os termos confirmados no TBCI ou no UNESCO podem ser apresentados como descritores autorizados, e a incorporação de termos relacionados ou específicos revelados pela consulta obriga a regerar esta ficha. Registro da validação: `data/saida/validacao/validacao_terminologica.csv`, com a resposta bruta de cada consulta em `data/evidencia/`.

3. **Termos qualificados para busca. Duas operações sobre o vocabulário registrado, nenhuma delas supressão de termo. SUBSTITUIÇÃO: palavra isolada de uso geral — learning, teaching, aprendizagem, ensino, taxonomy, classification, ranking, adaptation, inference e equivalentes — entra na expressão pelas formas compostas correspondentes, ou dela sai permanecendo no quadro. DESDOBRAMENTO: os nove termos em notação compacta de variante — “thesaurus/thesauri”, “knowledge organization system(s)” e congêneres — vão à expressão como alternativas explícitas ligadas por OR, porque a barra e o parêntese, dentro de aspas, são caracteres literais. A camada de qualificação recusa, com erro de execução, termo novo em notação compacta não desdobrada. DESDOBRAMENTO MORFOLÓGICO, acrescentado em 08/11/2026 por emenda autorizada: formas adjetivais e plurais — “ontological”, “ontológicos”, “ontologias”, “educacionais” — e o substantivo isolado de pedagogia entraram nas quatro facetas, por falha medida no ensaio seco do conjunto-semente; a derivação adjetival importa porque base alguma a alcança a partir do substantivo, ao contrário do plural regular. A SUBSTITUIÇÃO E A RETIRADA CASAM A FORMA, NÃO O LEMA: variante nova de termo retirado tem de ser retirada também, uma a uma — foi o que se fez com “taxonomies” e “taxonomías”, que de outro modo reintroduziriam nas strings o termo que a decisão havia excluído. Todos os termos permanecem nos quadros de controle terminológico e na validação do 2º passo. Razão de cada operação e os retornos que a motivaram: Anexo A, seções 3 e 4.**

   **Consequência específica para esta base.** Os termos em português desta ficha são os únicos do conjunto que passam pela via automatizada do TBCI, tesauro brasileiro da própria área da base. Confirmado um descritor autorizado no TBCI, ele é o candidato mais forte a entrar nas consultas da BRAPCI — mas a incorporação depende da decisão registrada no 2º passo e obriga a regerar esta ficha.

4. **Efeito da âncora 🟨 nesta base.** A BRAPCI indexa Ciência da Informação, não educação: o vínculo educacional de um artigo pode não comparecer no título, no resumo ou nas palavras-chave. É por isso que a faceta 🟦 é executada também isolada (seção 4.1), com leitura de todos os títulos retornados. A decisão amplia o esforço de triagem nesta base e deve ser declarada no relato.

5. Se a base dispuser de exportação em RIS ou BibTeX, exportar; se não, registrar os metadados manualmente no Zotero e anotar a entrada manual como fonte de risco de erro de transcrição.

