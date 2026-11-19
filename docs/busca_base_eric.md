# Strings de busca — ERIC

## 1. Estado de verificação da sintaxe

Nomes de campo verificados no painel *Advanced Search Tips* de `eric.ed.gov/?advanced`; comportamento verificado por medição, com as sondagens em `data/registro_execucao.json` (BD3).

| Elemento | Situação |
| :--- | :--- |
| Nomes de campo (`title`, `abstract`, `descriptor`, `educationlevel`, `language`, `publicationtype`, `pubyear`, `author`, `source`, `institution`, `sponsor`, `audience`, `assessment`, `law`, `location`, `e_yearadded`, `iesgrantcontractnum`) e filtros (`pubyearmin`, `pubyearmax`) | **Verificados em fonte oficial** |
| Campos de casamento exato (`descriptorx`, `sourcex`, `locationx`, `lawx`, `assessmentx`) e prefixo `+` | **Verificados em fonte oficial**, comportamento **não medido** |
| Prefixo de campo restringe de fato | **Verificado por medição** |
| Parênteses para agrupamento | **Suportados**; o grupo **não funciona sozinho** e precisa de condição externa |
| Condição externa a um grupo | **Verificada** em qualquer forma: campo, texto livre ou outro grupo, antes ou depois |
| Campos diferentes num mesmo grupo | **Não suportados**: devolvem zero, sem mensagem de erro |
| `pubyearmin`/`pubyearmax` junto a um grupo | **Não suportados**: zeram o retorno |
| `pubyearmin`/`pubyearmax` ligados por `AND` em consulta sem parênteses | **Verificado por medição** |
| Truncamento com `*` | **Não suportado**: devolve zero |
| Lematização | **Verificada** para plural regular; **não** para irregular |
| Aspas como frase | **Verificadas** dentro e fora do campo; o operador implícito entre palavras é conjunção |
| Campo `descriptor` | **Medido**: campo controlado; casa apenas formas autorizadas |
| Comprimento máximo da consulta | **Teto entre 1.502 e 1.799 caracteres brutos**; manter abaixo de **1.400** |
| Negação com prefixo `-` | **Verificada em fonte oficial**, não medida |
| Hífen como separador de palavras (`ontology-driven`, `e-learning`) | **Não medido** |
| Teto de retorno exibido e de exportação por lote | **Não verificados** |
| Controles `Include Synonyms` e `Include Dead terms` | **Não localizados** na interface; nenhuma expressão depende deles |

---

## 2. Critérios de elegibilidade

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — 2017 até a data de execução | CE1 / CE2 | **Não** | filtro de data da página de resultados, 2017 a 2026; registrar o rótulo do filtro e o retorno antes e depois |
| Idiomas — português, inglês e espanhol | CE3 | **Não** | termos só em inglês; campo `language` não usado |
| Tipo documental e revisão por pares | CE4 | **Não** | `Peer reviewed only` desmarcada; campo `publicationtype` não usado |
| Texto completo | CE5 | **Não** | `Full text available on ERIC` desmarcada |
| Adequação temática | CE6 | **Não** | filtragens do Módulo 3, Etapa 3 |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, em forma radical | faceta 🟨 (FCT2) como grupo de quatro palavras-raiz |
| Outros tipos documentais | CE9 | **Não** | 2ª filtragem |

---

## 3. Strings por faceta

`STRn` é o identificador do protocolo e `#n` a consulta correspondente. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

Forma desta base: `STR1` no título; `STR1b`, subconjunto específico de `STR1`, no resumo; `STR2` em quatro palavras-raiz no resumo; `STR3` e `STR4` no resumo. Plural regular omitido onde a lematização o alcança.

### Declaração de cobertura

Lida por `src/protocolo.py`.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: en; FCT2: en; FCT3: en; FCT4: en |
| camadas | todas |
| derivações | morfologia e radical |

**Redução desta base.**

| Faceta | Termo fora da string | Motivo |
| :--- | :--- | :--- |
| FCT1 | educational ontological model | redução desta base |
| FCT2 | massive open online course | redução desta base |

### `STR1` — conjunto `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

*No título.*

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering")
```

### `STR1b` — conjunto `#1b` — 🟦 FCT1 — Artefatos, subconjunto específico, no resumo

*No resumo.*

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern")
```

### `STR2` — conjunto `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

*Forma radical, no resumo.*

```
(abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching)
```

### `STR3` — conjunto `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

*No resumo.*

```
(abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

### `STR4` — conjunto `#4` — 🟧 FCT4 — Fatores situacionais

*No resumo.*

```
(abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

---

## 4. Expressões de busca

### Como esta base exige que a expressão seja montada

Regras medidas; violá-las devolve **zero sem mensagem de erro**:

- grupo entre parênteses com `OR` precisa de condição fora dele;
- a condição externa pode ser de campo, de texto livre ou outro grupo, antes ou depois;
- um grupo não mistura campos: `title:` e `abstract:` na mesma disjunção devolvem zero;
- `pubyearmin`/`pubyearmax` não convivem com grupo: o recorte vem do filtro da página;
- sem truncamento; expressão composta sempre entre aspas;
- cada consulta abaixo de **1.400 caracteres brutos**; acima disso, partir a expressão mantendo o grupo 🟦 íntegro e unir por deduplicação.

Toda expressão é executada como duas consultas de campo único — `STR1` no título e `STR1b` no resumo —, ambas com a faceta 🟨 como grupo externo, unidas por deduplicação.

**Composição.** `EB1 = #1 AND #2 AND #3 AND #4`; `EB2 = #1 AND #2 AND #3`; `EB3 = #1 AND #2 AND #4`; `EB4 = #1 AND #2 AND (#3 OR #4)`; `EB5 = #1 AND #2`.

| Expressão | Execução |
| :--- | :--- |
| **EB4** | executar e exportar, em quatro consultas: é o corpus desta base |
| **EB5** | executar uma única vez, na mesma data; não compõe o corpus |
| **EB2**, **EB3** | executar só para o teste de fidelidade da derivação |
| **EB1** | não executar; derivação local |

- Execução: particionada
- **Fidelidade:** divergência acima de `divergencia_fidelidade` (`--mostrar`) entre EB2/EB3 executadas e derivadas reprova a derivação.
- **Retorno zero:** EB4 = 0 ou EB5 = 0 é defeito de execução até prova em contrário; contagem derivada próxima de zero exige execução direta antes do relato.

### EB1 (geral) — as quatro facetas

**Não se executa; derivação local.** **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧)

### EB2 (específica) — modelos e ontologias que representam práticas do processo de ensino-aprendizagem

**Conferência do teste de fidelidade.** **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥)

**Consulta 2a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

**Consulta 2b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

### EB3 (específica) — artefatos que formalizam os fatores situacionais do domínio educacional

**Conferência do teste de fidelidade.** **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧)

**Consulta 3a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

**Consulta 3b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

### EB4 (de cobertura restrita) — artefatos de representação no domínio educacional que mencionam prática ou fator situacional

**É esta que se executa e se exporta.** **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧))

Executar as quatro consultas abaixo e unir por deduplicação.

**Consulta 4a — título × prática**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

**Consulta 4b — título × fator situacional**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

**Consulta 4c — termo específico × prática**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

**Consulta 4d — termo específico × fator situacional**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

### EB5 (sonda de sensibilidade) — as duas âncoras, sem exigir prática nem fator situacional

**Sonda de sensibilidade — executada uma única vez; não compõe o corpus.** **Facetas:** FCT1 (🟦) AND FCT2 (🟨)

**Consulta 5a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching)
```

**Consulta 5b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching)
```

### Como executar

1. Executar 4a, 4b, 4c e 4d e exportar cada uma em arquivo próprio, `eric_4a.ris` a `eric_4d.ris`, em `data/execucoes/eric/`.
2. Aplicar o filtro de data da página e anotar o retorno antes e depois, com o rótulo exato do filtro.
3. Registrar as quatro execuções, uma por arquivo: `python3 src/derivar_expressoes.py --registrar eric EB4 <arquivo> --retorno <n>`; rodar `--derivar`. O retorno da base é a união deduplicada, nunca a soma: o número que vai às contagens da busca é o dos únicos, com o bruto ao lado.
4. Executar EB5 (5a e 5b) uma única vez e registrar com `EB5`.
5. Medir a aderência (seção 5). Abaixo do limiar de aderência (`limiar_aderencia`, `--mostrar`), passar à contingência das variantes.

### Variantes previstas

#### Refinamento por cruzamento título × resumo

Disparo: retorno da 4a acima do limite de triagem fixado pelo ReT e registrado nas contagens da busca. Forma: substituir a 4a pelas consultas abaixo, com o sufixo de ano; registrar o retorno antes e depois.

| # | Consulta |
| :---: | :--- |
| X2 | `title:ontology AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X3 | `title:ontology AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X4 | `title:ontology AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X6 | `title:ontologies AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X7 | `title:ontologies AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X8 | `title:ontologies AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X14 | `title:"domain model" AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X15 | `title:"domain model" AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X16 | `title:"domain model" AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |

#### Camada 3 — descritores de artefato

Disparo: estudo que trata do artefato sem o nomear no título nem no resumo. Forma: a consulta abaixo. Antes do uso, sondar cada descritor nas formas `descriptor:` e `descriptorx:` e registrar os retornos. Adoção exige emenda.

```
(descriptor:Thesauri OR descriptor:Indexing OR descriptor:Metadata OR descriptor:"Knowledge Representation") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching)
```

#### Contingência — consultas curtas, sem agrupamento

Disparo: aderência reprovada na busca por campo. Forma: executar todas as consultas abaixo, exportar e deduplicar em conjunto. Não reproduzem EB4; a adoção exige emenda e a recomposição de FCT1 AND FCT2 AND (FCT3 OR FCT4) com `AND` entre um termo de cada faceta.

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
| 18 | `ontology AND "learning object" AND pubyearmin:2017 AND pubyearmax:2026` | 20 | `ontology AND "learning analytics" AND pubyearmin:2017 AND pubyearmax:2026` |
| 21 | `ontology AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` | 22 | `ontology AND "instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 23 | `ontology AND "teaching methods" AND pubyearmin:2017 AND pubyearmax:2026` | 24 | `ontology AND "situational factors" AND pubyearmin:2017 AND pubyearmax:2026` |
| 25 | `ontology AND "educational context" AND pubyearmin:2017 AND pubyearmax:2026` | 26 | `ontologies AND "learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| 28 | `ontologies AND "learning analytics" AND pubyearmin:2017 AND pubyearmax:2026` | 29 | `ontologies AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 30 | `ontologies AND "instructional design" AND pubyearmin:2017 AND pubyearmax:2026` | 35 | `"domain model" AND education AND pubyearmin:2017 AND pubyearmax:2026` |
| 39 | `"ontological engineering" AND pubyearmin:2017 AND pubyearmax:2026` | | |

#### Negação do ruído por descritor

Disparo: necessidade de levar ao resumo termos de `STR1` hoje restritos ao título. Forma: `-descriptor:"…"`, testando um a um, antes do uso: `Educational Research`, `Research Methodology`, `Epistemology`, `Qualitative Research`.

---

## 5. Conjunto-semente

Esperadas nesta base, conforme o protocolo. Estado de conferência em `data/sementes.json`; aferição em `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE6 | Iatrellis et al. (2019) | `10.1007/s10639-019-09872-9` | — |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE8 | Cenka et al. (2023) | `10.1080/10494820.2022.2039947` | alcance depende do hífen (`ontology-driven`) |

**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões; semente não indexada sai do denominador e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação de EB4 por DOI e depois por título, sem reexecutar a busca.

**Limiar de aderência** (`limiar_aderencia`, `--mostrar`), sobre a união das bases. A aderência por base indica qual base e qual faceta falharam.

---

## 6. Ressalvas

1. Todos os termos são **termos livres**; não apresentar as expressões como compostas de descritores ERIC.
2. Alterar as expressões exige repetir as sondagens pertinentes da seção 1.
3. No relato, declarar a assimetria de campo em relação à Scopus: aqui a faceta 🟦 vai ao título, e as palavras-chave correspondem ao campo controlado `descriptor`.
