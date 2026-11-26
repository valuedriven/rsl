#### Refinamento por cruzamento título × resumo

Disparo: retorno da 4a acima do limite de triagem fixado pelo ReT e registrado nas contagens da busca. Forma: substituir a 4a pelas consultas abaixo, aplicando o filtro de data da página de 2017 a 2026 em cada uma; registrar o retorno antes e depois. O recorte de ano não vai na consulta: os campos `pubyearmin`/`pubyearmax` não recortam como o filtro da página.

| # | Consulta |
| :---: | :--- |
| X2 | `title:ontology AND abstract:"learning object"` |
| X3 | `title:ontology AND abstract:"instructional design"` |
| X4 | `title:ontology AND abstract:"learning design"` |
| X6 | `title:ontologies AND abstract:"learning object"` |
| X7 | `title:ontologies AND abstract:"instructional design"` |
| X8 | `title:ontologies AND abstract:"learning design"` |
| X14 | `title:"domain model" AND abstract:"learning object"` |
| X15 | `title:"domain model" AND abstract:"instructional design"` |
| X16 | `title:"domain model" AND abstract:"learning design"` |

#### Camada 3 — descritores de artefato

Disparo: estudo que trata do artefato sem o nomear no título nem no resumo. Forma: a consulta abaixo. Antes do uso, sondar cada descritor nas formas `descriptor:` e `descriptorx:` e registrar os retornos. Adoção exige emenda.

```
(descriptor:Thesauri OR descriptor:Indexing OR descriptor:Metadata OR descriptor:"Knowledge Representation") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners)
```

#### Contingência — consultas curtas, sem agrupamento

Disparo: aderência reprovada na busca por campo. Forma: executar todas as consultas abaixo, aplicar o filtro de data da página de 2017 a 2026 em cada uma, exportar e deduplicar em conjunto. O recorte de ano não vai na consulta: os campos `pubyearmin`/`pubyearmax` não recortam como o filtro da página. Não reproduzem EB4; a adoção exige emenda e a recomposição de FCT1 AND FCT2 AND (FCT3 OR FCT4) com `AND` entre um termo de cada faceta.

| # | Consulta | # | Consulta |
| :---: | :--- | :---: | :--- |
| 1 | `"knowledge representation"` | 2 | `"knowledge organization"` |
| 3 | `"knowledge organization system"` | 4 | `"knowledge organization systems"` |
| 5 | `"controlled vocabulary"` | 6 | `"controlled vocabularies"` |
| 7 | `thesaurus` | 8 | `thesauri` |
| 9 | `"classification scheme"` | 10 | `"classification schemes"` |
| 11 | `"metadata schema"` | 12 | `"metadata schemas"` |
| 13 | `"ontology engineering"` | 14 | `"ontology development"` |
| 15 | `"ontology design pattern"` | 16 | `"ontology-based knowledge representation"` |
| 18 | `ontology AND "learning object"` | 20 | `ontology AND "learning analytics"` |
| 21 | `ontology AND "learning design"` | 22 | `ontology AND "instructional design"` |
| 23 | `ontology AND "teaching methods"` | 24 | `ontology AND "situational factors"` |
| 25 | `ontology AND "educational context"` | 26 | `ontologies AND "learning object"` |
| 28 | `ontologies AND "learning analytics"` | 29 | `ontologies AND "learning design"` |
| 30 | `ontologies AND "instructional design"` | 35 | `"domain model" AND education` |
| 39 | `"ontological engineering"` | | |

#### Negação do ruído por descritor

Disparo: necessidade de levar ao resumo termos de `STR1` hoje restritos ao título. Forma: `-descriptor:"…"`, testando um a um, antes do uso: `Educational Research`, `Research Methodology`, `Epistemology`, `Qualitative Research`.
