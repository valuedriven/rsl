# Strings de busca — ERIC

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º passo, e Etapa 2, 1º passo.  
**Fonte:** ERIC — interface pública `eric.ed.gov`. **Elaborado em:** 05/11/2026.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** VT.  
**Revisão:** 08/11/2026 — recorte temporal 2017–2026 e saída da instanciação em estruturas computacionais do objeto da revisão. Quatro facetas, quatro expressões, quatro questões secundárias. Cronologia das decisões, com as reduções anteriores: Anexo A, seções 1 e 5.

> **A orientação de execução está concentrada na seção 4.** A evidência das 23 sondagens de sintaxe desta base, a cronologia das decisões e os retornos inválidos anteriores estão no **Anexo A, seção 7**.

---

## 1. Estado de verificação da sintaxe

**Nomes de campo verificados em fonte oficial — painel *Advanced Search Tips* de `eric.ed.gov/?advanced`, conferido em 08/11/2026. Comportamento de cada um verificado por medição**, em 23 consultas de sondagem registradas no Anexo A, seção 7.

| Elemento | Situação |
| :--- | :--- |
| Nomes de campo (`title`, `abstract`, `descriptor`, `educationlevel`, `language`, `publicationtype`, `pubyear`, `author`, `source`, `institution`, `sponsor`, `audience`, `assessment`, `law`, `location`, `e_yearadded`, `iesgrantcontractnum`) e filtros (`pubyearmin`, `pubyearmax`) | **Verificados em fonte oficial** |
| Prefixo de campo restringe de fato | **Verificado**: `title:ontology` devolveu 343 contra 1.500 de `ontology` em texto livre |
| Parênteses para agrupamento | **Suportados**, com uma condição: o grupo **não funciona sozinho** — precisa de condição externa |
| Condição externa a um grupo | **Verificada** em qualquer forma: campo, texto livre ou outro grupo, antes ou depois |
| Campos diferentes num mesmo grupo | **NÃO SUPORTADOS**: devolvem zero, sem mensagem de erro |
| `pubyearmin`/`pubyearmax` junto a um grupo | **NÃO SUPORTADOS**: zeram o retorno. Funcionam em consulta sem parênteses |
| Truncamento com `*` | **NÃO SUPORTADO**: `ontolog*` devolveu zero contra 1.500 de `ontology` |
| Lematização | **Verificada** para plural regular (`ontologies` = `ontology`); **não** para irregular (`thesaurus` 318, `thesauri` 41) |
| Aspas como frase | **Verificadas** dentro e fora do campo. Palavra solta **não** forma frase: o operador implícito entre duas palavras é conjunção |
| Campo `descriptor` | **Medido em 15 consultas**: 13 com retorno não vazio, 2 com zero. É campo controlado, e isso está provado — `descriptor:Ontology` devolveu zero enquanto `ontology` em texto livre devolve 1.500. Ver a seção 5.2 |
| Comprimento máximo da consulta | **Teto entre 1.502 e 1.799 caracteres brutos.** Regra de bolso: manter abaixo de **1.400** |
| Negação com prefixo `-` | **Verificada em fonte oficial**, não medida |
| Controles `Include Synonyms` e `Include Dead terms` | **Não localizados na interface**; nenhuma expressão depende deles |
| API `api.ies.ed.gov/eric/` | Conhecida por fonte **secundária**, não adotada |

---

## 2. Critérios de elegibilidade: onde cada um é aplicado

| Critério | Na consulta? | Como |
| :--- | :--- | :--- |
| Intervalo temporal 2017–2026 | **Não** | pelo **filtro de data da página de resultados**: os operadores de ano zeram o retorno quando a consulta tem grupos. Registrar o rótulo exato do filtro e os retornos antes e depois |
| Revisão por pares | **Não** | caixa `Peer reviewed only` **desmarcada**: o protocolo admite anais, capítulos e relatórios técnicos |
| Texto completo | **Não** | caixa `Full text available on ERIC` **desmarcada**: marcada, suprime os artigos de periódico EJ, cujo texto está no editor |
| Idiomas | **Não** | os registros da ERIC são descritos em inglês, e as expressões usam somente os termos em inglês das facetas. O campo `language` existe e não é usado: restringir idioma excluiria registros elegíveis |
| Tipo documental | **Não**, por decisão | o campo `publicationtype` existe, mas o protocolo admite artigo, anais, capítulo e relatório técnico |
| Domínio educacional | **Sim**, em forma radical | a faceta 🟨 entra como grupo de seis palavras-raiz. É também a condição externa exigida pela sintaxe — ver a seção 4 |

---

## 3. Strings por faceta, em sintaxe nativa

Nesta base a sintaxe nativa combina **prefixo de campo** e **parênteses**. Cada string corresponde a um quadro de controle terminológico do 2º passo. Duas operações sobre o vocabulário registrado, ambas reversíveis e nenhuma delas supressão de termo: **desdobramento** da notação compacta de variante e **compactação**, que retira o termo cuja recuperação já é implicada por outro da mesma faceta. Nesta base acrescenta-se uma terceira: a **retirada do plural regular**, que a lematização torna redundante. As listas integrais das quatro facetas, nos três idiomas, estão no IO 1, Item 2.

> **Efeito do desdobramento morfológico de 08/11/2026 nesta base, que é o menor das quatro — e por um bom motivo.** A emenda acrescentou às facetas trinta formas adjetivais e plurais. Aqui, a retirada do plural regular desfaz quase todas: `ontologies`, `domain ontologies` e `pedagogies` saem por serem redundantes sob lematização medida, e `ontological engineering` sai por compactação, implicado por `ontological`. **Sobrou exatamente um termo novo na consulta: `title:ontological`** — e sobrou porque derivação adjetival não é flexão, e a lematização não a alcança. Isto é a confirmação de que o desdobramento foi bem dimensionado: nesta base ele custa 21 caracteres e traz o único ganho que a base não dava de graça. As formas em português e espanhol não entram aqui, porque esta ficha é só em inglês.

### `#1` — 🟦 Artefatos de representação e organização do conhecimento — **âncora obrigatória**

*33 termos em inglês → 19 após a compactação. Vai ao **título**; 5 termos específicos vão também ao resumo, em string própria. 528 caracteres.*

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation")
```

### `#1b` — 🟦 Artefatos, subconjunto específico, no resumo (158 caracteres)

*Entram só os termos sem acepção corrente fora da Organização do Conhecimento **nem no domínio educacional**. Ficam no título, e fora desta string, dez termos: seis ambíguos na literatura em geral — `ontology`, `ontologies`, `conceptual model`, `domain model`, `semantic model`, `formal representation` — e quatro homônimos próprios do domínio educacional, medidos no Anexo A, seção 7.4.*

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern")
```

### `#2` — 🟨 Domínio educacional — **âncora obrigatória** (129 caracteres)

*Forma radical: seis palavras-raiz que, por casamento de palavra, alcançam as 45 expressões registradas da faceta. A lista completa, de 26 termos, fica para o casamento local da derivação.*

```
(abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

### `#3` — 🟥 Práticas do processo de ensino-aprendizagem (765 caracteres)

*28 termos em inglês → 23 após a compactação. Vai ao resumo.*

```
(abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

### `#4` — 🟧 Fatores situacionais (1041 caracteres)

*32 termos em inglês → 31 após a compactação. Vai ao resumo.*

```
(abstract:"situational factor" OR abstract:"situation of use" OR abstract:"application context" OR abstract:"context of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"learning environment" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:context-aware OR abstract:contextualization OR abstract:contextualisation)
```

---

## 4. As quatro expressões de busca

### 4.1 Como esta base exige que a expressão seja montada

Cinco regras, todas medidas (Anexo A, seção 7). Quem alterar as expressões precisa respeitá-las, sob pena de **retorno zero sem mensagem de erro**:

- grupo entre parênteses com `OR` **não funciona sozinho** — precisa de condição fora dele;
- a condição externa pode ser de campo, de texto livre ou outro grupo, antes ou depois;
- um grupo **não mistura campos**: `title:` e `abstract:` na mesma disjunção devolvem zero;
- `pubyearmin`/`pubyearmax` **não convivem com grupo** — o recorte temporal vem do filtro da página (seção 2);
- **sem truncamento**, e expressão composta sempre entre aspas.

Daí a forma de toda expressão nesta base: **duas consultas de campo único**, unidas por deduplicação no Zotero — a faceta 🟦 no título e o seu subconjunto específico no resumo —, ambas com a faceta 🟨 como grupo externo. É a faceta 🟨 que satisfaz a primeira regra, e por isso ela não é dispensada nesta base.

> **Por que a expressão “geral” é a mais estreita, e não a mais ampla.** No gabarito do IO 1, *geral* qualifica a **composição** — E1 é a que reúne todas as strings montadas —, e não o alcance. Como as facetas se combinam por `AND`, acrescentar faceta **restringe**: E1 exige que o registro mencione as quatro, e por isso é a mais específica do conjunto. A mais ampla é a última, de cobertura, que exige apenas as duas âncoras. Daí a relação de continência — **E1 ⊂ E2 ⊂ E4** e **E1 ⊂ E3 ⊂ E4** —, e daí a execução única: a união das quatro é exatamente a de cobertura.

> **E a expressão geral não exclui ninguém.** Registro que não a satisfaça permanece no portfólio se satisfizer a de cobertura: as facetas temáticas são dimensões combináveis, e não requisitos cumulativos de recuperação — como o IO 1 declara no 1º passo do Item 2. O valor de E1 é **caracterizar**: quem reúne as quatro facetas tende a ser central à questão de revisão, e é por isso que a pertinência a E1 é a primeira chave da ordem de leitura produzida por `derivar_expressoes.py`.

**Obrigatoriedade de cada execução.** As quatro expressões não têm o mesmo estatuto no processo, e confundi-los custa caro nas duas direções — executar o que é redundante, ou pular o que é indispensável:

| | Executar na base? | Como quê | O que se perde ao pular |
| :--- | :--- | :--- | :--- |
| **E4** (cobertura) | **sim, sempre** | **é o portfólio**: define o que a revisão recuperou nesta base | tudo — a base não participa da revisão, não há exportação e a derivação não roda |
| **E2** | **sim** | teste de fidelidade da derivação | nenhum registro, e **a auditabilidade das contagens derivadas** |
| **E3** | **sim** | teste de fidelidade da derivação | idem |
| **E1** (geral) | não | caracterização, por derivação local | nada, desde que a derivação rode: a contagem de E1 é obrigatória, a sua execução não |

> **Leitura de um retorno vazio.** Antes de ler zero como achado, é preciso **provar que não é artefato de sintaxe** — nesta revisão houve três retornos zero por defeito de consulta, e um zero silencioso registrado como resultado apareceria no diagrama PRISMA como conclusão. Provada a execução válida: **E4 = 0 é quase sempre defeito**, pois significaria que a base não tem literatura alguma sobre artefatos de representação no domínio educacional; **E2 = 0** com E4 > 0 é achado — há artefatos, mas nenhum que represente práticas; **E3 = 0** é achado forte e plausível, já que a representação de fatores situacionais é a parte menos consolidada da questão; **E1 = 0** é o enunciado mais nítido da lacuna, e deixa a primeira chave da ordem de triagem uniforme.

> **Zero derivado e zero executado são afirmações diferentes.** O zero derivado pode vir da limitação do casamento local, que vê apenas título, resumo e palavras-chave como exportados. **Contagem derivada igual ou próxima de zero obriga à execução direta daquela expressão antes de ser relatada como achado.**

> **EXECUÇÃO ÚNICA (emenda de 06/11/2026).** Todas as expressões começam pelas strings 1 + 2 e apenas acrescentam facetas: **E1, E2 e E3 são subconjuntos estritos de E4**, a de cobertura, e a união das quatro é exatamente E4. Executa-se **apenas E4**; a pertinência de cada registro às demais é calculada localmente por `derivar_expressoes.py`, e as contagens de E1 a E3 no IO 2 são **derivadas**, não reconsultadas.

> **Exceção obrigatória — teste de fidelidade.** Antes de aceitar qualquer contagem derivada, executar **E2 e E3** e comparar com o conjunto derivado: divergência acima de 10% reprova a derivação e obriga a executar cada expressão separadamente.

**Limite de comprimento.** Manter cada consulta abaixo de **1.400 caracteres brutos**. Acima disso o risco é `404`, e a saída é partir a expressão: **manter o grupo da faceta 🟦 íntegro** e dividir ao meio o grupo da faceta temática. A união das partes é *exatamente* a expressão original, porque `A AND (B OR C)` equivale a `(A AND B) OR (A AND C)`; somar por deduplicação, nunca por adição de números.

### 4.2 E1 (geral) — todas as strings montadas. **“Geral” é a composição, não o alcance**: por exigir as quatro facetas simultaneamente, é a MAIS RESTRITIVA das quatro

**Não se executa.** Sonda de precisão máxima, nunca critério de exclusão, e a sua contagem é derivada de E4. **Facetas:** 🟦 AND 🟨 AND 🟥 AND 🟧

*As duas consultas teriam 2478 e 2108 caracteres, acima do teto, e exigiriam partição em doze — para nada, já que a contagem é derivada.*

### 4.3 E2 (específica) — modelos e ontologias que representam práticas do processo de ensino-aprendizagem

**Conferência do teste de fidelidade.** **Facetas:** 🟦 AND 🟨 AND 🟥

**Consulta 2a — artefato no título.** A forma inteira tem 1432 caracteres, acima do teto de bolso, e por isso **vai partida em duas**: o grupo da faceta 🟦 fica íntegro e o grupo temático divide-se ao meio. Executar as duas e somar **por deduplicação**, nunca por adição de contagens — a interseção entre elas é vazia por construção, mas a de registros não é.

*2a-i* (1062 caracteres)

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

*2a-ii* (1035 caracteres)

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

**Consulta 2b — termo específico no resumo** (1062 caracteres)

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

### 4.4 E3 (específica) — artefatos que formalizam os fatores situacionais do domínio educacional

**Conferência do teste de fidelidade.** **Facetas:** 🟦 AND 🟨 AND 🟧

**Consulta 3a — artefato no título.** A forma inteira tem 1708 caracteres, acima do teto de bolso, e por isso **vai partida em duas**: o grupo da faceta 🟦 fica íntegro e o grupo temático divide-se ao meio. Executar as duas e somar **por deduplicação**, nunca por adição de contagens — a interseção entre elas é vazia por construção, mas a de registros não é.

*3a-i* (1203 caracteres)

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"application context" OR abstract:"context of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"learning environment" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

*3a-ii* (1170 caracteres)

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:context-aware OR abstract:contextualization OR abstract:contextualisation) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

**Consulta 3b — termo específico no resumo** (1338 caracteres)

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"application context" OR abstract:"context of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"learning environment" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:context-aware OR abstract:contextualization OR abstract:contextualisation) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

### 4.5 E4 (de cobertura) — artefatos de representação do conhecimento no domínio educacional, inclusive quando não mencionam as demais facetas nos metadados

**EXECUTADA nesta base** — é esta que se exporta. **Facetas:** 🟦 AND 🟨

**Consulta 4a — artefato no título** (662 caracteres)

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

**Consulta 4b — termo específico no resumo** (292 caracteres)

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

> **A execução de 08/11/2026 está vencida — reexecutar as duas.** A 4a devolveu **951 registros** naquela data, com 553 caracteres; o desdobramento do mesmo dia acrescentou `title:ontological` ao grupo da faceta 🟦, e a consulta passou a ter 574 caracteres. **É outra consulta**, e o 951 não lhe serve de retorno. A 4b nunca foi executada na forma vigente, com retorno esperado da ordem de 169. Exportar em arquivos separados, `eric_4a.ris` e `eric_4b.ris`, e depositar em `data/execucoes/eric/`. O ganho esperado da reexecução é pequeno em volume e não é desprezível em pertinência: `ontological` recupera o registro que diz *ontological principles*, *ontological engineering* ou *ontological model* no título sem dizer *ontology*, e duas sementes do conjunto-semente são exatamente desse tipo.*

### 4.6 O que fazer depois de executar

1. **Deduplicar 4a e 4b.** O retorno da base é a união deduplicada, **nunca a soma dos dois números**; anotar a sobreposição. O script de derivação também marca os repetidos, por DOI ou título normalizado, e conta os únicos; o número que vai ao IO 2 é o dos únicos, com o bruto ao lado.

2. **Aplicar o filtro de data da página** e anotar o retorno antes e depois, com o rótulo exato do filtro.

3. **Rodar, da raiz do repositório, `python3 src/protocolo.py --gerar`**; registrar cada execução — `python3 src/derivar_expressoes.py --registrar eric E4 data/execucoes/eric/eric_4a.ris --retorno <n>` e o mesmo para `eric_4b.ris` — e rodar `python3 src/derivar_expressoes.py --derivar`. O primeiro materializa o vocabulário, as strings e as expressões; os registros conferem o retorno declarado contra cada arquivo e recusam registrar quando divergem; o último confere o recorte, marca as duplicatas, calcula a pertinência de cada registro a E1, E2 e E3 e produz a fila de triagem. A derivação recusa rodar com derivado defasado.

4. **Conferir a aderência ao conjunto-semente.** Abaixo de 80%, a busca por campo está restritiva demais e passa-se à contingência da seção 5.3.

### 4.7 Quando o retorno não couber na triagem

As consultas da seção 5.1 são *subconjuntos* da 4a: executá-las por cima não acrescenta registro algum. Servem para **substituir** a 4a quando o seu retorno exceder o limite de triagem fixado pelo ReT — sugere-se **300 registros** como ponto de partida, e o número adotado tem de constar do IO 2. É restrição de recall, não ampliação: registrar o retorno antes e depois.

---

## 5. Variantes previstas

### 5.1 Refinamento por cruzamento título × resumo

Para substituir a 4a nos termos do item 4.7. Nestas o sufixo de ano é admissível, porque não há grupo entre parênteses.

| # | Consulta |
| :---: | :--- |
| X1 | `title:ontology AND abstract:curriculum AND pubyearmin:2017 AND pubyearmax:2026` |
| X2 | `title:ontology AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X3 | `title:ontology AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X4 | `title:ontology AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X5 | `title:ontologies AND abstract:curriculum AND pubyearmin:2017 AND pubyearmax:2026` |
| X6 | `title:ontologies AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X7 | `title:ontologies AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X8 | `title:ontologies AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X9 | `title:"conceptual model" AND abstract:curriculum AND pubyearmin:2017 AND pubyearmax:2026` |
| X10 | `title:"conceptual model" AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X11 | `title:"conceptual model" AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X12 | `title:"conceptual model" AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X13 | `title:"domain model" AND abstract:curriculum AND pubyearmin:2017 AND pubyearmax:2026` |
| X14 | `title:"domain model" AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X15 | `title:"domain model" AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X16 | `title:"domain model" AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X17 | `title:"semantic model" AND abstract:curriculum AND pubyearmin:2017 AND pubyearmax:2026` |
| X18 | `title:"semantic model" AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X19 | `title:"semantic model" AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X20 | `title:"semantic model" AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X21 | `title:"formal representation" AND abstract:curriculum AND pubyearmin:2017 AND pubyearmax:2026` |
| X22 | `title:"formal representation" AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X23 | `title:"formal representation" AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X24 | `title:"formal representation" AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |

### 5.2 Sondas de descritor — **EXECUTADAS**

As 15 consultas foram executadas pelo ReT, uma a uma, sem filtro de ano.

| # | Consulta | Faceta | Retorno |
| :---: | :--- | :---: | ---: |
| D1 | `descriptor:Thesauri` | 🟦 | 568 |
| D2 | `descriptor:Classification` | 🟦 | 21.241 |
| D3 | `descriptor:Indexing` | 🟦 | 1.966 |
| D4 | `descriptor:Metadata` | 🟦 | 1.001 |
| D5 | `descriptor:Semantics` | 🟦 | 13.577 |
| D6 | `descriptor:Vocabulary` | 🟦 | 28.729 |
| D7 | `descriptor:Taxonomy` | 🟦 | 1.628 |
| D8 | `descriptor:"Knowledge Representation"` | 🟦 | 869 |
| D9 | `descriptor:"Semantic Web"` | 🟦 | **zero** |
| D10 | `descriptor:Ontology` | 🟦 | **zero** |
| D11 | `descriptor:"Information Retrieval"` | 🟦 | 9.070 |
| D12 | `descriptor:"Educational Technology"` | 🟨 | 64.763 |
| D13 | `descriptor:"Instructional Design"` | 🟥 | 20.978 |
| D14 | `descriptor:"Learning Analytics"` | 🟨 | 2.035 |
| D15 | `descriptor:"Educational Objectives"` | 🟥 | 45.025 |

**O campo responde, e é de fato controlado — isto está provado, não suposto.** 13 das 15 sondas devolveram retorno não vazio. A prova de que o campo **não** cai em texto livre é o próprio zero de `descriptor:Ontology`: a palavra `ontology` em texto livre devolve **1.500** nesta base, e `title:ontology` devolve 343. Um campo que recaísse em texto livre não teria como devolver zero. **O controle interno não estava previsto na sondagem: emergiu dela.**

**O achado substantivo são os dois zeros, e eles dizem respeito ao centro desta revisão.** `descriptor:Ontology` e `descriptor:"Semantic Web"` devolveram **zero**. Nesta base — que é a base de educação — **o artefato central do recorte não tem descritor nesta forma**, enquanto `Educational Technology` tem 64.763 registros e `Educational Objectives`, 45.025. A assimetria é exatamente a fragmentação terminológica entre comunidades que esta revisão se propõe a evidenciar, e **passa a ser achado medido do próprio protocolo**, a relatar.

> **“Nesta forma” é a parte que ainda não se mediu.** Zero não autoriza concluir que o conceito não tenha descritor: autoriza concluir que **esta grafia** não é descritor. A resposta não se obtém adivinhando plurais e variantes, e sim abrindo `Browse Thesaurus` e procurando o conceito — a página mostra a forma preferida e as remissões `Use`. É o mesmo passo que a regra das duas evidências já exigia, agora com destino certo.

**O que falta para fechar, e não é a sondagem.** Retorno não vazio é evidência de **uso** do termo na indexação; a página do tesauro é evidência de **autoridade** da forma. As 13 não vazias têm a primeira e **não têm a segunda**: nenhuma passa a descritor autorizado antes de a página ser aberta e capturada. O IO 1 declara o *ERIC Thesaurus* instrumento **sem consulta sistemática**; com as duas evidências, ele passa a “consulta por campo”, o que é **emenda a decidir com a VT**.

#### 5.2.1 Camada 3, se a emenda for aprovada

A camada 3 existe para o caso que as camadas 1 e 2 não alcançam: **o estudo que trata do artefato sem o nomear no título nem no resumo**. Monta-se com os descritores de artefato de volume baixo — teto de 2.000 registros — porque acima disso o descritor é polissêmico numa base de educação: `Vocabulary`, com 28.729, é aprendizado de palavras; `Classification`, com 21.241, é categorização de alunos e de conteúdo. Ficam de fora por esse critério: `Classification` (21.241), `Semantics` (13.577), `Vocabulary` (28.729), `Information Retrieval` (9.070).

**Consulta 5a — descritor de artefato** (265 caracteres)

```
(descriptor:Thesauri OR descriptor:Indexing OR descriptor:Metadata OR descriptor:Taxonomy OR descriptor:"Knowledge Representation") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

Soma bruta dos 5 descritores, antes da âncora de domínio e da deduplicação: 6.032 registros. É o teto absoluto do que a camada pode trazer, não a sua expectativa.

> **Esta camada não se valida pelo conjunto-semente, e isso tem de estar escrito.** As três sementes esperadas nesta base já são recuperadas pelo título, de modo que a camada 3 não as melhora; e as sementes que a justificariam — a 5 e a 10, cujo artefato não está no título — **esta base não indexa**. A regra geral da ficha, de que nenhuma camada se adota sem medição contra o conjunto-semente, **não é aplicável aqui**, e a camada se justifica por outra via: a medição do campo, acima, e o exame qualitativo do que ela devolver. Adotar sem essa ressalva escrita seria aplicar a regra onde ela não alcança.

### 5.3 Contingência — consultas curtas, sem agrupamento

Para o caso de a aderência ao conjunto-semente reprovar a busca por campo. Uma linha por consulta, todas exportadas e deduplicadas em conjunto.

| # | Consulta | # | Consulta |
| :---: | :--- | :---: | :--- |
| 1 | `"knowledge representation" AND pubyearmin:2017 AND pubyearmax:2026` | 2 | `"knowledge organization" AND pubyearmin:2017 AND pubyearmax:2026` |
| 3 | `"knowledge organization system" AND pubyearmin:2017 AND pubyearmax:2026` | 4 | `"knowledge organization systems" AND pubyearmin:2017 AND pubyearmax:2026` |
| 5 | `"controlled vocabulary" AND pubyearmin:2017 AND pubyearmax:2026` | 6 | `"controlled vocabularies" AND pubyearmin:2017 AND pubyearmax:2026` |
| 7 | `thesaurus AND pubyearmin:2017 AND pubyearmax:2026` | 8 | `thesauri AND pubyearmin:2017 AND pubyearmax:2026` |
| 9 | `"classification scheme" AND pubyearmin:2017 AND pubyearmax:2026` | 10 | `"classification schemes" AND pubyearmin:2017 AND pubyearmax:2026` |
| 11 | `"metadata schema" AND pubyearmin:2017 AND pubyearmax:2026` | 12 | `"metadata schemas" AND pubyearmin:2017 AND pubyearmax:2026` |
| 13 | `"ontology engineering" AND pubyearmin:2017 AND pubyearmax:2026` | 14 | `"ontology development" AND pubyearmin:2017 AND pubyearmax:2026` |
| 15 | `"ontology design pattern" AND pubyearmin:2017 AND pubyearmax:2026` | 16 | `"ontology-based knowledge representation" AND pubyearmin:2017 AND pubyearmax:2026` |
| 17 | `"conceptual schema" AND pubyearmin:2017 AND pubyearmax:2026` | 18 | `ontology AND "learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| 19 | `ontology AND curriculum AND pubyearmin:2017 AND pubyearmax:2026` | 20 | `ontology AND "learning analytics" AND pubyearmin:2017 AND pubyearmax:2026` |
| 21 | `ontology AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` | 22 | `ontology AND "instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 23 | `ontology AND "teaching methods" AND pubyearmin:2017 AND pubyearmax:2026` | 24 | `ontology AND "situational factors" AND pubyearmin:2017 AND pubyearmax:2026` |
| 25 | `ontology AND "educational context" AND pubyearmin:2017 AND pubyearmax:2026` | 26 | `ontologies AND "learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| 27 | `ontologies AND curriculum AND pubyearmin:2017 AND pubyearmax:2026` | 28 | `ontologies AND "learning analytics" AND pubyearmin:2017 AND pubyearmax:2026` |
| 29 | `ontologies AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` | 30 | `ontologies AND "instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 31 | `"conceptual model" AND curriculum AND pubyearmin:2017 AND pubyearmax:2026` | 32 | `"conceptual model" AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 33 | `"conceptual model" AND "teaching methods" AND pubyearmin:2017 AND pubyearmax:2026` | 34 | `"conceptual model" AND "educational context" AND pubyearmin:2017 AND pubyearmax:2026` |
| 35 | `"domain model" AND education AND pubyearmin:2017 AND pubyearmax:2026` | 36 | `"semantic model" AND education AND pubyearmin:2017 AND pubyearmax:2026` |
| 37 | `"formal representation" AND education AND pubyearmin:2017 AND pubyearmax:2026` | 38 | `"conceptual models" AND curriculum AND pubyearmin:2017 AND pubyearmax:2026` |

### 5.4 Negação do ruído por descritor

A negação `-descriptor:"…"` está documentada no painel oficial e **não foi medida**. Permitiria devolver ao resumo os quatro termos homônimos retirados, negando os descritores da literatura cognitiva e metodológica em lugar de evitá-los pelo campo. Candidatos a testar, um a um pela seção 5.2 antes de usar: `Educational Research`, `Research Methodology`, `Epistemology`, `Qualitative Research`. Negar descritor inexistente não faz nada; negar descritor largo retira estudo elegível.

---

## 6. Conjunto-semente — o que esta base deve recuperar

O conjunto-semente tem **10 estudos**, todos conferidos em fonte e todos dentro do escopo. Pela indicação do ReT, **3 são esperados nesta base**. Instrumento completo, procedimento e estado de conferência de cada referência: `data/saida/semente/Conjunto_Semente.md`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| 6 | Iatrellis et al. (2019) | `10.1007/s10639-019-09872-9` | ressalva de escopo — `data/saida/semente/Conjunto_Semente.md`, 3.1 |
| 7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| 8 | Cenka et al. (2023) | `10.1080/10494820.2022.2039947` | — |

**Procedimento, em duas etapas, e não confundir as duas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões da revisão, para saber se a base indexa a semente. Semente não indexada **sai do denominador desta base**, e isso se registra como cobertura da base, não como falha da busca. *Etapa 2:* procurar a semente na exportação de E4 já feita, por DOI e depois por título — **sem reexecutar a busca**, porque o teste se faz sobre o que a execução de fato devolveu.

**Limiar de 80%, e o que a reprovação obriga.** O IO 1 fixa o limiar e manda, abaixo dele, revisar o controle terminológico antes de prosseguir, com emenda registrada. O número que decide é o **global**, sobre a união das bases: perder uma semente aqui e achá-la em outra não é perda de portfólio. A aderência por base serve para diagnosticar **qual** base e **qual** faceta falharam.

**Lematização nesta base:** **medida em 08/11/2026.** `title:ontologies` e `title:ontology` devolveram retornos iguais, e `thesaurus` devolveu 318 contra 41 de `thesauri` — de modo que a lematização alcança o plural regular e não o irregular. Importa porque o desdobramento morfológico de 08/11/2026 acrescentou plurais e formas adjetivais às facetas: onde a base lematiza, o plural é redundante; onde não lematiza, era perda silenciosa. A **derivação adjetival** é outro caso: `ontological` não é flexão de `ontology`, e **base alguma a alcança** a partir do substantivo. Foi por isso que entrou no vocabulário — duas sementes do conjunto falhavam a âncora de artefato só por causa dela.

**Resultado medido, e é favorável à forma de execução desta ficha.** A camada 1 restringe os termos da faceta 🟦 ao **título**, o que é perda de recall assumida em troca de precisão. A conferência do conjunto-semente permite medir essa perda sobre as três sementes esperadas aqui, e o resultado é **zero**: os títulos das sementes 6, 7 e 8 trazem, respectivamente, `ontology`, `ontology` e `conceptual model` com `ontology`. **Nenhuma das três perde a âncora de artefato pela restrição ao título.**

Isso não prova que a restrição seja inócua — três sementes não medem uma base —, mas inverte o ônus: a hipótese de que o título é restritivo demais passa a precisar de evidência, e a ficha deixa de depender só do argumento de precisão. Se a etapa 2 confirmar as três na exportação de E4, a assimetria de campo em relação à Web of Science e à Scopus, declarada na ressalva 4, está medida e não estimada.

**O que ainda não se mediu:** a semente que trate do artefato **sem o nomear no título** — o caso das sementes 5 e 10, que esta base não indexa. A camada 3, por `descriptor:`, existe para esse caso, e continua por sondar.

---


## 7. Registro de execução (alimenta o IO 2)

| Execução | Data | Filtro de data | Retornos | Arquivo |
| :--- | :---: | :--- | :---: | :--- |
| ~~Consulta 4a, forma de 553 caracteres~~ | 08/11/2026 | — | ~~951~~ | **vencida pelo desdobramento** |
| **E4 — Consulta 4a, artefato no título** | | | | `eric_4a.ris` |
| **E4 — Consulta 4b, termo no resumo** | | | | `eric_4b.ris` |
| **E4 — união deduplicada no Zotero** | | | | `eric_E4.ris` |
| Sobreposição entre 4a e 4b | | | diferença | — |
| **E4 — após o filtro de data** | | rótulo usado | | **é o que vai ao IO 2** |
| E2 — Consultas 2a e 2b | | | dois retornos + união | `eric_2a.ris`, `eric_2b.ris` |
| E3 — Consultas 3a e 3b, partidas | | | quatro retornos + união | `eric_3a-i.ris` … |
| E1 | — | — | derivada | — |
| X__ — refinamento, se usado | | | antes / depois | `eric_X__.ris` |
| D1…D15 — sondas de descritor | | | quantas retornaram | capturas de tela |
| Aderência ao conjunto-semente | | | % recuperado | — |

As sondagens de sintaxe e os retornos das execuções inválidas anteriores já constam do Anexo A, seção 7, e não se reanotam aqui.

---

## 8. Ressalvas

1. **Todos os termos têm estatuto de termo livre**: nenhum foi confrontado com instrumento de controle terminológico. São 365 registros de termo nas quatro facetas — 123 em português, 119 em inglês e 123 em espanhol. As expressões desta base **não devem ser apresentadas como compostas de descritores ERIC**. Procedimento e estado da validação: IO 1 e Anexo A, seções 2 e 3.

2. **A precisão vem do campo.** Dez termos da faceta 🟦 ficam restritos ao título. Perde-se o estudo que os mencione apenas no resumo, e é o teste de aderência ao conjunto-semente que mede essa perda — **reprova abaixo de 80%**.

3. **A faceta 🟨 entra em forma radical**, com seis palavras-raiz que alcançam as 45 expressões registradas por casamento de palavra. Redução declarada, e também a condição externa sem a qual a base devolve zero.

4. **Assimetria de campo em relação à Scopus**, a declarar no relato. Lá, `TITLE-ABS-KEY()` alcança título, resumo e palavras-chave de todos os termos. Aqui a parcela de palavras-chave corresponde ao campo `descriptor`, que casa apenas formas autorizadas, e dez termos ficam só no título. A seção 5.4 atacaria parte dessa assimetria.

5. **O retorno da base é a união deduplicada de 4a e 4b, depois do filtro de data.**

6. **A sintaxe desta base foi apurada por medição, não por documentação.** Alterar as expressões sem repetir as sondagens pertinentes arrisca retorno zero silencioso.

