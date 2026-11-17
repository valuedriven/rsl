# Strings de busca — ERIC

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º passo (expressões de busca) e Etapa 2, 1º passo (execução).  
**Fonte:** ERIC — interface pública `eric.ed.gov`.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** VT.  
**Vigente desde:** 17/11/2026. **Registro de execução:** `data/registro_execucao.json`, base `BD3`. **Histórico das decisões:** Anexo A.

---

## 1. Estado de verificação da sintaxe

**Nomes de campo verificados no painel *Advanced Search Tips* de `eric.ed.gov/?advanced`. O comportamento de cada um foi verificado por medição** — o registro das sondagens está em `data/registro_execucao.json`.

| Elemento | Situação |
| :--- | :--- |
| Nomes de campo (`title`, `abstract`, `descriptor`, `educationlevel`, `language`, `publicationtype`, `pubyear`, `author`, `source`, `institution`, `sponsor`, `audience`, `assessment`, `law`, `location`, `e_yearadded`, `iesgrantcontractnum`) e filtros (`pubyearmin`, `pubyearmax`) | **Verificados em fonte oficial** |
| Prefixo de campo restringe de fato | **Verificado por medição** |
| Parênteses para agrupamento | **Suportados**, com uma condição: o grupo **não funciona sozinho** e precisa de condição externa |
| Condição externa a um grupo | **Verificada** em qualquer forma: campo, texto livre ou outro grupo, antes ou depois |
| Campos diferentes num mesmo grupo | **Não suportados**: devolvem zero, sem mensagem de erro |
| `pubyearmin`/`pubyearmax` junto a um grupo | **Não suportados**: zeram o retorno; funcionam em consulta sem parênteses |
| Truncamento com `*` | **Não suportado**: `ontolog*` devolve zero |
| Lematização | **Verificada** para plural regular; **não** para irregular |
| Aspas como frase | **Verificadas** dentro e fora do campo; palavra solta não forma frase, e o operador implícito entre duas palavras é conjunção |
| Campo `descriptor` | **Medido**: é campo controlado, e casa apenas formas autorizadas |
| Comprimento máximo da consulta | **Teto entre 1.502 e 1.799 caracteres brutos**; regra de bolso: manter abaixo de **1.400** |
| Negação com prefixo `-` | **Verificada em fonte oficial**, não medida |
| Controles `Include Synonyms` e `Include Dead terms` | **Não localizados** na interface; nenhuma expressão depende deles |

---

## 2. Critérios de elegibilidade

| Critério | Na consulta? | Como |
| :--- | :--- | :--- |
| Intervalo temporal — de 2017 até a data de execução, 2026 parcialmente coberto | **Não** | pelo **filtro de data da página de resultados**: os operadores de ano zeram o retorno quando a consulta tem grupos. Aplicar 2017 a 2026, com 2026 conforme a data de consulta, e registrar o rótulo do filtro e o retorno antes e depois |
| Revisão por pares | **Não** | caixa `Peer reviewed only` desmarcada: o protocolo admite anais, capítulos e relatórios técnicos |
| Texto completo | **Não** | caixa `Full text available on ERIC` desmarcada: marcada, suprime os artigos de periódico EJ, cujo texto está no editor |
| Idiomas | **Não** | os registros são descritos em inglês e as expressões usam só os termos em inglês. O campo `language` existe e não é usado: restringir idioma excluiria registro elegível |
| Tipo documental | **Não**, por decisão | o campo `publicationtype` existe, mas o protocolo admite artigo, anais, capítulo e relatório técnico |
| Domínio educacional | **Sim**, em forma radical | a faceta 🟨 entra como grupo de seis palavras-raiz, que é também a condição externa exigida pela sintaxe |

---

## 3. Strings por faceta

Cada string corresponde a um quadro de controle terminológico do 2º passo. Sobre o vocabulário registrado incidem três operações, reversíveis e nenhuma delas supressão de termo: **desdobramento** da notação compacta, **compactação** do termo cuja recuperação já é implicada por outro da mesma faceta e **retirada do plural regular**, que a lematização torna redundante. As listas integrais das quatro facetas, nos três idiomas, estão no IO 1, Item 2.

### `#1` — 🟦 Artefatos de representação e organização do conhecimento — **âncora obrigatória**

*Vai ao título; cinco termos específicos vão também ao resumo, em string própria.*

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation")
```

### `#1b` — 🟦 Artefatos, subconjunto específico, no resumo

*Entram só os termos sem acepção corrente fora da Organização do Conhecimento nem no domínio educacional. Ficam no título, e fora desta string, dez termos: seis ambíguos na literatura em geral e quatro homônimos próprios do domínio educacional.*

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern")
```

### `#2` — 🟨 Domínio educacional — **âncora obrigatória**

*Forma radical: seis palavras-raiz que, por casamento de palavra, alcançam as expressões registradas da faceta. A lista completa fica para o casamento local da derivação.*

```
(abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

### `#3` — 🟥 Práticas do processo de ensino-aprendizagem

*Vai ao resumo.*

```
(abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

### `#4` — 🟧 Fatores situacionais

*Vai ao resumo.*

```
(abstract:"situational factor" OR abstract:"situation of use" OR abstract:"application context" OR abstract:"context of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"learning environment" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:context-aware OR abstract:contextualization OR abstract:contextualisation)
```

---

## 4. Expressões de busca

### Como esta base exige que a expressão seja montada

Cinco regras, todas medidas. Quem alterar as expressões precisa respeitá-las, sob pena de **retorno zero sem mensagem de erro**:

- grupo entre parênteses com `OR` **não funciona sozinho** — precisa de condição fora dele;
- a condição externa pode ser de campo, de texto livre ou outro grupo, antes ou depois;
- um grupo **não mistura campos**: `title:` e `abstract:` na mesma disjunção devolvem zero;
- `pubyearmin`/`pubyearmax` **não convivem com grupo** — o recorte temporal vem do filtro da página;
- **sem truncamento**, e expressão composta sempre entre aspas.

Daí a forma de toda expressão nesta base: **duas consultas de campo único**, unidas por deduplicação — a faceta 🟦 no título e o seu subconjunto específico no resumo —, ambas com a faceta 🟨 como grupo externo. É a faceta 🟨 que satisfaz a primeira regra, e por isso ela não é dispensada.

**Composição e contenção.** `EB1 = #1 + #2 + #3 + #4`; `EB2 = #1 + #2 + #3`; `EB3 = #1 + #2 + #4`; `EB4 = #1 + #2`. As facetas combinam-se por `AND`, e acrescentar faceta restringe: **EB1 ⊂ EB2 ⊂ EB4**, **EB1 ⊂ EB3 ⊂ EB4**, e **EB1 é exatamente a interseção de EB2 e EB3**. *Geral* qualifica a composição, não o alcance: EB1 é a mais restritiva, e serve de sonda de precisão máxima, nunca de critério de exclusão.

**Execução única.** Executa-se **EB4**; a pertinência a EB1, EB2 e EB3 é calculada localmente por `derivar_expressoes.py`, e essas contagens são **derivadas**.

**Fidelidade da derivação.** Antes de aceitar contagem derivada, executar **EB2 e EB3** e comparar: divergência acima de **10%** reprova o método.

**Leitura de retorno vazio.** Zero só é achado depois de provada a execução válida. **EB4 = 0** é quase sempre defeito; **EB2 = 0** com EB4 > 0 é achado; **EB3 = 0** é achado forte; **EB1 = 0** é o enunciado da lacuna. Contagem derivada próxima de zero obriga à execução direta antes de ser relatada.

**Limite de comprimento.** Manter cada consulta abaixo de **1.400 caracteres brutos**; acima disso o teto medido é de 1.502 a 1.799, e a saída é partir a expressão. A partição mantém o grupo da faceta 🟦 íntegro e divide ao meio o grupo temático: a união das partes é *exatamente* a expressão original, porque `A AND (B OR C)` equivale a `(A AND B) OR (A AND C)`. Somar por deduplicação, nunca por adição de números.

### EB1 (geral) — as quatro facetas

**Não se executa.** Sonda de precisão máxima, nunca critério de exclusão; a contagem é derivada de EB4. **Facetas:** 🟦 AND 🟨 AND 🟥 AND 🟧

### EB2 (específica) — modelos e ontologias que representam práticas do processo de ensino-aprendizagem

**Conferência do teste de fidelidade.** **Facetas:** 🟦 AND 🟨 AND 🟥

**Consulta 2a — artefato no título.** A forma inteira passa do teto de bolso e vai **partida em duas**: o grupo da faceta 🟦 fica íntegro e o grupo temático divide-se ao meio. Executar as duas e somar **por deduplicação**, nunca por adição de contagens.

*2a-i*

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

*2a-ii*

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

**Consulta 2b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

### EB3 (específica) — artefatos que formalizam os fatores situacionais do domínio educacional

**Conferência do teste de fidelidade.** **Facetas:** 🟦 AND 🟨 AND 🟧

**Consulta 3a — artefato no título.** Mesma regra de partição da 2a: grupo da faceta 🟦 íntegro, grupo temático dividido ao meio, soma por deduplicação.

*3a-i*

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"application context" OR abstract:"context of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"learning environment" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

*3a-ii*

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:context-aware OR abstract:contextualization OR abstract:contextualisation) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

**Consulta 3b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"application context" OR abstract:"context of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"learning environment" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:context-aware OR abstract:contextualization OR abstract:contextualisation) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

### EB4 (de cobertura) — artefatos de representação do conhecimento no domínio educacional

**É esta que se executa e se exporta.** **Facetas:** 🟦 AND 🟨

**Consulta 4a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:ontological OR title:"faceted classification" OR title:"facet analysis" OR title:"faceted taxonomy" OR title:"conceptual model" OR title:"conceptual modeling" OR title:"conceptual modelling" OR title:"conceptual schema" OR title:"domain model" OR title:"semantic model" OR title:"formal representation") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

**Consulta 4b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

> **As duas consultas ainda não foram executadas na forma vigente.** Exportar em arquivos separados, `eric_4a.ris` e `eric_4b.ris`, e depositar em `data/execucoes/eric/`. O termo `title:ontological` recupera o registro que diz *ontological principles*, *ontological engineering* ou *ontological model* no título sem dizer *ontology*, e há sementes do conjunto-semente desse tipo.

### Como executar

1. **Deduplicar 4a e 4b.** O retorno da base é a união deduplicada, **nunca a soma dos dois números**; anotar a sobreposição. O script também marca os repetidos e conta os únicos; o número que vai ao IO 2 é o dos únicos, com o bruto ao lado.
2. **Aplicar o filtro de data da página** e anotar o retorno antes e depois, com o rótulo exato do filtro.
3. **Registrar as duas execuções** com `python3 src/derivar_expressoes.py --registrar eric EB4 <arquivo> --retorno <n>` e rodar `--derivar`. O registro confere o retorno declarado contra cada arquivo e recusa registrar quando divergem; a derivação confere o recorte, marca duplicatas e calcula a pertinência a EB1, EB2 e EB3.
4. **Conferir a aderência.** Abaixo de 80%, a busca por campo está restritiva demais, e passa-se à contingência das variantes.

**Quando o retorno não couber na triagem.** As consultas de refinamento das variantes são *subconjuntos* da 4a: executá-las por cima não acrescenta registro algum. Servem para **substituir** a 4a quando o retorno exceder o limite de triagem fixado pelo ReT — sugere-se **300 registros** como ponto de partida, e o número adotado consta do IO 2. É restrição de recall, não ampliação: registrar o retorno antes e depois.

### Variantes previstas

#### Refinamento por cruzamento título × resumo

Para substituir a 4a quando o retorno exceder o limite de triagem. Nestas, o sufixo de ano é admissível, porque não há grupo entre parênteses.

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

#### Camada 3 — descritores de artefato

Existe para o estudo que trata do artefato **sem o nomear no título nem no resumo**. Monta-se com os descritores de artefato de volume baixo — **teto de 2.000 registros** —, porque acima disso o descritor é polissêmico numa base de educação: `Vocabulary` é aprendizado de palavras e `Classification` é categorização de alunos e de conteúdo. Ficam de fora, por esse critério, `Classification`, `Semantics`, `Vocabulary` e `Information Retrieval`.

```
(descriptor:Thesauri OR descriptor:Indexing OR descriptor:Metadata OR descriptor:Taxonomy OR descriptor:"Knowledge Representation") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:student OR abstract:curriculum)
```

> **Esta camada não se valida pelo conjunto-semente, e isso tem de estar escrito.** As três sementes esperadas nesta base já são recuperadas pelo título, de modo que a camada não as melhora; e as sementes que a justificariam — cujo artefato não está no título — esta base não indexa. A camada justifica-se pela medição do campo e pelo exame qualitativo do que devolver, e a adoção depende de emenda aprovada com a VT.

#### Contingência — consultas curtas, sem agrupamento

Para o caso de a aderência reprovar a busca por campo. Uma linha por consulta, todas exportadas e deduplicadas em conjunto.

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

#### Negação do ruído por descritor

A negação `-descriptor:"…"` está documentada no painel oficial e **não foi medida**. Permitiria devolver ao resumo os quatro termos homônimos retirados, negando os descritores da literatura cognitiva e metodológica em lugar de evitá-los pelo campo. Candidatos a testar, um a um, antes de usar: `Educational Research`, `Research Methodology`, `Epistemology`, `Qualitative Research`. Negar descritor inexistente não faz nada; negar descritor largo retira estudo elegível.

---

## 5. Conjunto-semente

O conjunto-semente tem **10 estudos**, todos conferidos em fonte e dentro do escopo. Pela indicação do ReT, **3 são esperados nesta base**. Instrumento completo: `data/saida/semente/Conjunto_Semente.md`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE6 | Iatrellis et al. (2019) | `10.1007/s10639-019-09872-9` | ressalva de escopo — `Conjunto_Semente.md`, 3.1 |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE8 | Cenka et al. (2023) | `10.1080/10494820.2022.2039947` | — |

**Procedimento, em duas etapas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões, para saber se a base indexa a semente. Semente não indexada **sai do denominador** e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação de EB4 por DOI e depois por título, **sem reexecutar a busca**.

**Limiar de 80%.** Decide o número **global**, sobre a união das bases. A aderência por base diagnostica **qual** base e **qual** faceta falharam.

**Lematização.** **Medida nesta base**: alcança o plural regular e não o irregular. É o que permite retirar `ontologies`, `domain ontologies` e `pedagogies` da consulta, e é por isso que o efeito do desdobramento morfológico aqui é o menor das quatro bases. A **derivação adjetival** não é alcançada por lematização alguma, e `title:ontological` permanece.

**Restrição ao título — perda medida.** A camada 1 restringe os termos da faceta 🟦 ao título, o que é perda de recall assumida em troca de precisão. Nas três sementes esperadas, **nenhuma perde a âncora de artefato** por essa restrição. Três sementes não medem uma base, mas invertem o ônus: a hipótese de que o título é restritivo demais passa a precisar de evidência.

**Cobertura.** As sementes cujo artefato não está no título não são indexadas por esta base. A camada 3 existe para esse caso e depende de emenda aprovada.

---

## 6. Ressalvas

1. **Todos os termos têm estatuto de termo livre**: nenhum foi confrontado com instrumento de controle terminológico. As expressões desta base **não devem ser apresentadas como compostas de descritores ERIC**. Procedimento e estado da validação: IO 1 e Anexo A.

2. **A precisão vem do campo.** Dez termos da faceta 🟦 ficam restritos ao título. Perde-se o estudo que os mencione apenas no resumo, e é o teste de aderência que mede essa perda — reprova abaixo de 80%.

3. **A faceta 🟨 entra em forma radical**, com seis palavras-raiz que alcançam as expressões registradas por casamento de palavra. Redução declarada, e também a condição externa sem a qual a base devolve zero.

4. **Assimetria de campo em relação à Scopus**, a declarar no relato. Lá, `TITLE-ABS-KEY()` alcança título, resumo e palavras-chave de todos os termos. Aqui, a parcela de palavras-chave corresponde ao campo `descriptor`, que casa apenas formas autorizadas, e dez termos ficam só no título.

5. **O retorno da base é a união deduplicada de 4a e 4b, depois do filtro de data.**

6. **A sintaxe desta base foi apurada por medição, não por documentação.** Alterar as expressões sem repetir as sondagens pertinentes arrisca retorno zero silencioso.
