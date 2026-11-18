# Strings de busca — Web of Science (Core Collection)

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º e 4º passos (strings e expressões de busca) e Etapa 2, 1º passo (execução).  
**Fonte:** Web of Science Core Collection — *Advanced Search*.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** bibliotecário(a) de referência (VT).  
**Vigente desde:** 18/11/2026 (alinhamento à v2 do protocolo). **Registro de execução:** `data/registro_execucao.json`, base `BD1`. **Histórico das decisões:** Anexo A.

---

## 1. Estado de verificação da sintaxe

| Elemento | Situação | Fonte |
| :--- | :--- | :--- |
| `TS=` — tópico: título, resumo, palavras-chave de autor e *Keywords Plus* | Verificado | Clarivate, *Advanced Search Field Tags* |
| `TI=`, `AB=`, `AK=`, `SO=`, `KP=`, `WC=`, `SU=`, `DO=`, `ALL=` | Verificados | idem |
| `PY=` — ano de publicação, e exigência de combinação com outra *tag* | Verificado | idem |
| `DT=` — tipo de documento | Verificado | idem e FECYT (2024) |
| `LA=` — idioma | Verificado em fonte **secundária** | FECYT, *De la consulta simple a la compleja en Web of Science* (2024). Não localizado na página de *field tags* |
| Truncamento `*`, `?`, `$`; mínimo de 3 caracteres antes do curinga; curinga desativa a lematização | Verificado | Clarivate, *Advanced Search examples* |
| Limite de 200 conjuntos de busca por sessão | Verificado | idem |
| Recomendação de intervalos de `PY=` de até 5 anos | Verificado | idem |
| Operador de disponibilidade de texto completo em sintaxe de consulta | **Não existe** entre as *tags* verificadas | ausência na página de *field tags* |
| Valores exatos admitidos em `DT=` e `LA=` | **Não verificados um a um** | conferir na lista suspensa da interface |
| Proximidade `NEAR/x` entre grupos entre parênteses | **Verificado por medição** (aceita pela interface; ordem de grandeza) | calibração de 06/11 e execuções EX4–EX6, `data/registro_execucao.json` (BD1) |
| Distância padrão de `NEAR` sem número | **Não verificada** | — |
| `NEAR` entre referências de conjunto (`#1 NEAR/5 #2`) e conjunto combinado com `PY=`/`DT=` na mesma linha | **Não verificados** | medir na primeira execução; ver "Como executar" |
| Tratamento de diacríticos (`ontología` × `ontologia`) | **Não verificado** | as strings trazem as duas grafias, de modo que nada depende dele |
| Teto de retorno exibido e de exportação por lote | **Não verificados** | conferir na interface antes de exportar |

> As expressões da seção 4 usam `TS=`, `PY=` e `DT=`, verificados em documentação oficial, e `NEAR/5`, verificado por medição. Os valores de `DT=` ainda não foram conferidos um a um na lista da interface: valor recusado sai da consulta e vai ao refinamento, com a troca anotada no registro. Idioma vai em variante, porque `LA=` só tem fonte secundária; disponibilidade de texto completo **não** é expressável em consulta, só em refinamento.

---

## 2. Critérios de elegibilidade

| Critério | ID | Expresso na string? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — de 2017 até a data de execução, 2026 parcialmente coberto | CE1 / CE2 | **Sim** | `AND PY=(2017-2026)`: o filtro fecha o ano da execução; 2026 entra parcialmente, conforme a data de consulta e a atualização da base, e 2027 fica fora. Fracionamento em intervalos menores: seção 4, variantes |
| Idiomas — português, inglês e espanhol | CE3 | Em variante | `AND LA=(English OR Portuguese OR Spanish)`, valores a conferir |
| Tipo documental | CE4 | **Sim** | `AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")`, nas cinco expressões; valores a conferir na interface (seção 1). Teses e dissertações **não** são cobertas pela Core Collection: ficam a cargo da BRAPCI e da BDTD. Revisões sistemáticas e de escopo permanecem elegíveis |
| Disponibilidade de texto completo | CE5 | **Não** | refinamento de interface após a busca; a não localização é critério da 2ª filtragem |
| Adequação temática | CE6 | **Não** | decisão de leitura, nas filtragens do Módulo 3, Etapa 3 |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, por âncora | faceta 🟨 (FCT2) obrigatória nas cinco expressões |
| Outros tipos documentais — editoriais, cartas, erratas, resenhas, apresentações de dossiê, resumos sem texto completo e versões preliminares | CE9 | **Não** | decisão de leitura, na 2ª filtragem |

---

## 3. Strings por faceta

Uma string por faceta, executada como conjunto de busca próprio (`#1` a `#4`), para que as expressões da seção 4 se montem por combinação sem reexecutar termos. `STRn` é o identificador do protocolo e `#n` o conjunto correspondente na interface. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

**Fidelidade ao protocolo.** As strings desta ficha são `STR1`–`STR4` da versão 2 do protocolo, literalmente e nos três idiomas, acrescidas apenas de flexões de número sobre termo que já consta delas, nos termos da ressalva 2. O que o quadro terminológico registra e a STR v2 não executa está declarado termo a termo abaixo.

### Declaração de cobertura

O que esta busca alcança do vocabulário do protocolo. `src/protocolo.py` lê esta tabela para conferir a string contra o protocolo; termo ausente e não declarado reprova a conferência desta base.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: pt, en, es; FCT2: pt, en, es; FCT3: pt, en, es; FCT4: pt, en, es |
| camadas | todas |
| derivações | morfologia |

**Redução declarada.** A única redução é a da v2: os termos que a emenda retirou, termo a termo na tabela seguinte. Os acréscimos em relação à STR v2 são flexão de número sobre termo que já consta dela.

**Redução declarada, termo a termo.** Os termos abaixo permanecem no quadro terminológico e no estatuto de validação; a string desta base não os executa. As razões estão na Nota de emenda e o efeito é medido no teste de aderência e na sonda de sensibilidade.

| Faceta | Termo retirado da string | Motivo |
| :--- | :--- | :--- |
| FCT1 | taxonomia | retirado na emenda v2 |
| FCT1 | ontológico | retirado na emenda v2 |
| FCT1 | ontológica | retirado na emenda v2 |
| FCT1 | análise facetada | retirado na emenda v2 |
| FCT1 | análise de facetas | retirado na emenda v2 |
| FCT1 | modelo conceitual | retirado na emenda v2 |
| FCT1 | modelagem conceitual | retirado na emenda v2 |
| FCT1 | esquema conceitual | retirado na emenda v2 |
| FCT1 | modelo semântico | retirado na emenda v2 |
| FCT1 | representação formal | retirado na emenda v2 |
| FCT1 | ontological | retirado na emenda v2 |
| FCT1 | facet analysis | retirado na emenda v2 |
| FCT1 | conceptual model | retirado na emenda v2 |
| FCT1 | conceptual modeling | retirado na emenda v2 |
| FCT1 | conceptual modelling | retirado na emenda v2 |
| FCT1 | conceptual schema | retirado na emenda v2 |
| FCT1 | semantic model | retirado na emenda v2 |
| FCT1 | formal representation | retirado na emenda v2 |
| FCT1 | análisis facetado | retirado na emenda v2 |
| FCT1 | análisis de facetas | retirado na emenda v2 |
| FCT1 | modelo conceptual | retirado na emenda v2 |
| FCT1 | modelado conceptual | retirado na emenda v2 |
| FCT1 | esquema conceptual | retirado na emenda v2 |
| FCT1 | modelo semántico | retirado na emenda v2 |
| FCT1 | representación formal | retirado na emenda v2 |
| FCT2 | educativo | retirado na emenda v2 |
| FCT2 | currículo | retirado na emenda v2 |
| FCT2 | estudante | retirado na emenda v2 |
| FCT2 | aluno | retirado na emenda v2 |
| FCT2 | professor | retirado na emenda v2 |
| FCT2 | docente | retirado na emenda v2 |
| FCT2 | instituição de ensino | retirado na emenda v2 |
| FCT2 | nível de ensino | retirado na emenda v2 |
| FCT2 | modalidade de ensino | retirado na emenda v2 |
| FCT2 | curriculum | retirado na emenda v2 |
| FCT2 | learner | retirado na emenda v2 |
| FCT2 | student | retirado na emenda v2 |
| FCT2 | teacher | retirado na emenda v2 |
| FCT2 | instructor | retirado na emenda v2 |
| FCT2 | educational institution | retirado na emenda v2 |
| FCT2 | educational level | retirado na emenda v2 |
| FCT2 | education modality | retirado na emenda v2 |
| FCT2 | estudiante | retirado na emenda v2 |
| FCT2 | alumno | retirado na emenda v2 |
| FCT2 | institución educativa | retirado na emenda v2 |
| FCT2 | nivel educativo | retirado na emenda v2 |
| FCT2 | modalidad educativa | retirado na emenda v2 |
| FCT4 | contexto de aplicação | retirado na emenda v2 |
| FCT4 | contexto de uso | retirado na emenda v2 |
| FCT4 | ambiente de aprendizagem | retirado na emenda v2 |
| FCT4 | application context | retirado na emenda v2 |
| FCT4 | context of use | retirado na emenda v2 |
| FCT4 | learning environment | retirado na emenda v2 |
| FCT4 | contexto de aplicación | retirado na emenda v2 |
| FCT4 | entorno de aprendizaje | retirado na emenda v2 |

### `STR1` — conjunto `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
TS=("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologias" OR "ontologia de domínio" OR "ontologias de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia facetada" OR "esquema de classificação" OR "esquema de metadados" OR "classificação facetada" OR "ontologia facetada" OR "ontologia educacional" OR "ontologia de aprendizagem" OR "ontologia de ensino" OR "modelo ontológico educacional" OR "ontologia de prática educacional" OR "ontologia de design instrucional" OR "ontologia de currículo" OR "modelo de domínio" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representação do conhecimento baseada em ontologias" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "ontologies" OR "domain ontology" OR "domain ontologies" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "faceted taxonomy" OR "classification scheme" OR "metadata schema" OR "faceted classification" OR "faceted ontology" OR "educational ontology" OR "learning ontology" OR "teaching ontology" OR "educational ontological model" OR "educational practice ontology" OR "instructional design ontology" OR "curriculum ontology" OR "domain model" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "taxonomía facetada" OR "esquema de clasificación" OR "esquema de metadatos" OR "clasificación facetada" OR "ontología facetada" OR "ontología educativa" OR "ontología de aprendizaje" OR "ontología de enseñanza" OR "modelo ontológico educativo" OR "ontología de práctica educativa" OR "ontología de diseño instruccional" OR "ontología de currículo" OR "modelo de dominio" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías")
```

### `STR2` — conjunto `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

```
TS=("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz")
```

### `STR3` — conjunto `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
TS=("prática" OR "prática educacional" OR "práticas educacionais" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boa prática" OR "boas práticas" OR "prática recomendada" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino" OR "practice" OR "educational practice" OR "pedagogical practice" OR "teaching practice" OR "instructional practice" OR "teaching strategy" OR "instructional strategy" OR "teaching method" OR "instructional method" OR "teaching technique" OR "learning activity" OR "learning task" OR "educational intervention" OR "instructional intervention" OR "teaching sequence" OR "instructional sequence" OR "pedagogy" OR "pedagogies" OR "best practice" OR "best practices" OR "recommended practice" OR "recommended practices" OR "pedagogical approach" OR "instructional approach" OR "instructional design" OR "learning design" OR "pedagogical pattern" OR "pedagogical design pattern" OR "active learning method" OR "teaching methodology" OR "práctica" OR "práctica educativa" OR "prácticas educativas" OR "práctica pedagógica" OR "práctica docente" OR "estrategia de enseñanza" OR "estrategia didáctica" OR "método de enseñanza" OR "método instruccional" OR "técnica de enseñanza" OR "actividad de aprendizaje" OR "tarea de aprendizaje" OR "intervención educativa" OR "intervención pedagógica" OR "secuencia didáctica" OR "secuencia instruccional" OR "pedagogía" OR "buena práctica" OR "buenas prácticas" OR "práctica recomendada" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoque instruccional" OR "diseño instruccional" OR "diseño del aprendizaje" OR "diseño didáctico" OR "patrón pedagógico" OR "patrón de diseño pedagógico" OR "método de aprendizaje activo" OR "metodología de enseñanza")
```

### `STR4` — conjunto `#4` — 🟧 FCT4 — Fatores situacionais

```
TS=("fator situacional" OR "fatores situacionais" OR "situação de uso educacional" OR "contexto educacional" OR "contexto de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator de contexto" OR "fatores de contexto" OR "condição de aplicação" OR "condições de aplicação" OR "condição de implementação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "característica do aluno" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recurso disponível" OR "recursos disponíveis" OR "restrição contextual" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização" OR "situational factor" OR "situational factors" OR "situation of use" OR "educational context" OR "learning context" OR "contextual factor" OR "contextual factors" OR "context factor" OR "context factors" OR "application condition" OR "application conditions" OR "implementation condition" OR "implementation conditions" OR "learning situation" OR "educational setting" OR "institutional context" OR "sociocultural context" OR "target population" OR "class profile" OR "learner characteristic" OR "learner characteristics" OR "educational level" OR "education modality" OR "educational institution" OR "educational infrastructure" OR "learning infrastructure" OR "available resource" OR "available resources" OR "contextual constraint" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context-aware" OR "contextualization" OR "contextualisation" OR "factor situacional" OR "factores situacionales" OR "situación de uso" OR "contexto educativo" OR "contexto de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor del contexto" OR "factores del contexto" OR "condición de aplicación" OR "condiciones de aplicación" OR "condición de implementación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "escenario educativo" OR "población destinataria" OR "perfil del grupo" OR "característica del estudiante" OR "características de los estudiantes" OR "nivel educativo" OR "modalidad educativa" OR "institución educativa" OR "infraestructura educativa" OR "recurso disponible" OR "recursos disponibles" OR "restricción contextual" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "sensible al contexto" OR "contextualización")
```

---

## 4. Expressões de busca


```
EB1 = #1 + #2 + #3 + #4
EB2 = #1 + #2 + #3
EB3 = #1 + #2 + #4
EB4 = #1 + #2 + (#3 OR #4)     (executada)
EB5 = #1 + #2                  (sonda de sensibilidade)
```

As facetas combinam-se por `AND`, e acrescentar faceta **restringe**. Daí **EB1 ⊂ EB2 ⊂ EB4**, **EB1 ⊂ EB3 ⊂ EB4** e **EB4 = EB2 ∪ EB3**: EB4 exige as duas âncoras e **ao menos uma** das facetas temáticas. **EB5 ⊃ EB4**: retira a exigência temática e mede o que EB4 deixa de fora. *Geral* qualifica a composição, não o alcance: EB1 é a mais restritiva das expressões.

Registro que não satisfaça EB1 **não é excluído**: permanece se satisfizer EB4. As facetas temáticas são dimensões combináveis, não requisitos cumulativos de recuperação. EB1 **caracteriza** — quem reúne as quatro facetas tende a ser central à questão —, e é a primeira chave da ordem de leitura.

**Estatuto de cada expressão.**

| | Executar na base? | Como quê | O que se perde ao pular |
| :--- | :--- | :--- | :--- |
| **EB4** (cobertura restrita) | **sim, sempre** | é o portfólio: define o que a revisão recuperou nesta base | tudo — a base não participa da revisão |
| **EB5** (sonda) | **sim, uma única vez** | sonda de sensibilidade: mede o que EB4 perde | a medida do custo em recall da mudança de EB4 |
| **EB2** | sim | teste de fidelidade da derivação | a auditabilidade das contagens derivadas |
| **EB3** | sim | teste de fidelidade da derivação | idem |
| **EB1** (geral) | não | caracterização, por derivação local | nada, desde que a derivação rode |

**Execução única.** Executa-se **EB4**, com exportação única. **EB5** é executada **uma única vez, na mesma base e data**, e **não compõe o corpus**: o retorno é a sonda de sensibilidade. A pertinência de cada registro a EB1, EB2 e EB3 é calculada localmente por `derivar_expressoes.py`, e essas contagens são **derivadas**, não reconsultadas.

**Fidelidade da derivação.** Antes de aceitar contagem derivada, executar **EB2 e EB3** e comparar com o conjunto derivado: divergência acima de **10%** reprova o método e obriga a voltar às execuções separadas, com emenda registrada.

**Sensibilidade.** Mede-se a fração de registros recuperados por EB5 que **não** são recuperados por EB4, e amostra-se essa fração para classificação manual de elegibilidade. Se a fração elegível for **< 5%**, a mudança está justificada; se **> 15%**, reconsiderar — possivelmente retornar a EB5 como busca definitiva. O resultado é registrado como emenda ao protocolo.

**Leitura de retorno vazio.** Zero só é achado depois de provada a execução válida. **EB4 = 0** é quase sempre defeito; **EB5 = 0** é defeito de execução, porque EB5 contém EB4; **EB2 = 0** com EB4 > 0 é achado — há artefatos, nenhum representa práticas; **EB3 = 0** é achado forte, porque a representação de fatores situacionais é a parte menos consolidada; **EB1 = 0** é o enunciado mais nítido da lacuna. Contagem derivada próxima de zero obriga à execução direta antes de ser relatada.


### `#5` — as duas âncoras em proximidade

Definir **uma vez** e reusar em todas as expressões. A proximidade de cinco palavras exclui o registro em que artefato e domínio aparecem sem relação entre si. **A proximidade e o filtro aplicam-se às cinco**, e é isso que faz a contenção valer por construção: cada expressão é `#5` com zero, uma ou duas facetas a mais.

```
TS=(("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologias" OR "ontologia de domínio" OR "ontologias de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia facetada" OR "esquema de classificação" OR "esquema de metadados" OR "classificação facetada" OR "ontologia facetada" OR "ontologia educacional" OR "ontologia de aprendizagem" OR "ontologia de ensino" OR "modelo ontológico educacional" OR "ontologia de prática educacional" OR "ontologia de design instrucional" OR "ontologia de currículo" OR "modelo de domínio" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representação do conhecimento baseada em ontologias" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "ontologies" OR "domain ontology" OR "domain ontologies" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "faceted taxonomy" OR "classification scheme" OR "metadata schema" OR "faceted classification" OR "faceted ontology" OR "educational ontology" OR "learning ontology" OR "teaching ontology" OR "educational ontological model" OR "educational practice ontology" OR "instructional design ontology" OR "curriculum ontology" OR "domain model" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "taxonomía facetada" OR "esquema de clasificación" OR "esquema de metadatos" OR "clasificación facetada" OR "ontología facetada" OR "ontología educativa" OR "ontología de aprendizaje" OR "ontología de enseñanza" OR "modelo ontológico educativo" OR "ontología de práctica educativa" OR "ontología de diseño instruccional" OR "ontología de currículo" OR "modelo de dominio" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") NEAR/5 ("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz"))
```

Se a interface recusar a proximidade entre grupos deste tamanho, **não há forma reduzida equivalente**: consultas de um termo de cada lado não somam `#5`. Parar, registrar a recusa e partir o grupo 🟦 em subconjuntos, cada um com o grupo 🟨 inteiro do outro lado — `(A1 OR A2) NEAR/5 B` equivale a `(A1 NEAR/5 B) OR (A2 NEAR/5 B)`, de modo que a união deduplicada das partes é exatamente `#5`. Registrar a partição como adaptação.

### EB1 (as quatro facetas)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧) · **conjuntos:** #5 AND #3 AND #4

```
#5 AND #3 AND #4 AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### EB2 (modelos e ontologias que representam práticas do processo de ensino-aprendizagem)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) · **conjuntos:** #5 AND #3

```
#5 AND #3 AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### EB3 (artefatos que formalizam os fatores situacionais do domínio educacional)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧) · **conjuntos:** #5 AND #4

```
#5 AND #4 AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### EB4 (de cobertura restrita — artefatos de representação no domínio educacional que mencionam prática ou fator situacional)

*Executada e exportada nesta base.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧)) · **conjuntos:** #5 AND (#3 OR #4)

```
#5 AND (#3 OR #4) AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) · **conjuntos:** #5

```
#5 AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

A **forma expandida** de qualquer expressão obtém-se substituindo `#5`, `#3` e `#4` pelos blocos da seção 3. Ela não é mantida em duplicidade aqui: cópia em segundo lugar defasa na primeira alteração da string.

### Como executar

1. Conferir a sessão contra a seção 1, se for a primeira execução do dia.
2. Definir `#3` e `#4` na sessão com os blocos da seção 3 e `#5` com o bloco da seção 4 — `#1 NEAR/5 #2` entre referências de conjunto **não está verificado** e não substitui o bloco —, e submeter a **forma por conjuntos de EB4**. Se a interface recusar combinar conjunto com `PY=` e `DT=`, montar a forma expandida por substituição a partir dos blocos desta ficha, num arquivo, e não por digitação; anotar no registro qual das duas formas foi aceita.
3. Manter na consulta `AND PY=(2017-2026)` e `DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")`; idioma por `LA=` ou por refinamento.
4. Exportar em RIS, com todos os campos, em arquivos dentro do limite da base.
5. Conferir o retorno da exportação contra o da tela: divergência indica exportação parcial ou teto de retorno.
6. Registrar **EB4** e **EB5** (`python3 src/derivar_expressoes.py --registrar wos EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`); rodar `--derivar` e `--sensibilidade`.
7. Medir a aderência ao conjunto-semente. Abaixo de 80%, revisar forma ou vocabulário, com emenda registrada no Anexo A. A sonda EB5 não entra no denominador nem no corpus: o que ela mede é a sensibilidade.

### Variantes previstas

#### Fracionamento do intervalo temporal

A documentação recomenda intervalos de `PY=` de até cinco anos. Se a execução em bloco falhar ou truncar o retorno, repetir cada expressão substituindo o trecho final por:

```
AND PY=(2017-2021)
AND PY=(2022-2026)
```

As duas faixas são disjuntas e cobrem o recorte. Deduplicar no Zotero e registrar o retorno de cada faixa. Registrar o fracionamento como adaptação.

#### Idioma

Anexar ao final de qualquer expressão, **após a sondagem S1 de `LA=` e a conferência dos valores na lista suspensa da interface**:

```
AND LA=(English OR Portuguese OR Spanish)
```

Se um valor for recusado, suprimir a cláusula e aplicar o mesmo limite por refinamento, anotando a troca no registro. O tipo documental já está nas cinco expressões.

#### Truncamento

O truncamento (`ontolog*`, `educat*`, `contextualiz*`) **não** se aplica aqui: na Web of Science o curinga desativa a lematização, e `ontolog*` alcança `ontological`, que a emenda v2 retirou. Executar sem curinga; se a aderência ficar abaixo de 80%, testar o curinga e registrar o resultado — a adoção é emenda, porque reintroduz forma retirada.

#### Camada de precisão

As strings da seção 3 já qualificam os termos que cruzavam `ontology` com `learning` — a subárea de *ontology learning* e o aprendizado de máquina que menciona ontologia. Se o retorno ainda for alto, aplicar as camadas abaixo **nesta ordem**, medindo a cada passo.

**Camada 1 — proximidade entre as âncoras.** Já incorporada, nas cinco expressões, pelo conjunto `#5`, com distância 5. Reduzir a distância é a única variação desta camada, medida contra o conjunto-semente.

**Camada 2 — restrição de campo.** Manter a faceta 🟦 em `TS=` e passar a faceta 🟨 para `AK=` (palavras-chave de autor) ou `TI=`, porque *Keywords Plus* é gerado automaticamente e é fonte de ruído:

```
TS=(<faceta 1>) AND AK=(<faceta 2>) AND PY=(2017-2026)
```

**Camada 3 — refinamento por categoria.** Último recurso, por arriscar perder trabalho interdisciplinar:

```
AND WC=("Education & Educational Research" OR "Education, Scientific Disciplines" OR "Information Science & Library Science" OR "Computer Science, Artificial Intelligence" OR "Computer Science, Information Systems" OR "Computer Science, Interdisciplinary Applications" OR "Computer Science, Theory & Methods")
```

Conferir os rótulos das categorias na lista da interface antes de usar. Aplicada esta camada, declarar a restrição no relatório e compensá-la pelo *backward search* de uma geração.

> **Regra de decisão.** Nenhuma camada se adota por reduzir o número: cada uma é medida contra o conjunto-semente, e recuperação inferior a 80% a reprova e obriga a emenda. **Não** reduzir o retorno acrescentando facetas a EB4 — é a expressão de cobertura, e é ela que recupera a ontologia educacional silenciosa quanto a fatores situacionais.

---

## 5. Conjunto-semente

O conjunto-semente tem **10 estudos**. O estado de conferência de cada um está em `data/sementes.json` — hoje, as dez com verificação, escopo, tipo e alinhamento pendentes (`python3 src/protocolo.py --pendencias`). Pela indicação do ReT, **4 são esperados nesta base**. Planilha de aferição, uma linha por semente e por base: `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE2 | Das et al. (2022) | `10.5771/0943-7444-2022-1-6` | — |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE9 | Piriyapongpipat et al. (2024) | `10.1186/s40561-024-00307-8` | — |
| SE10 | Khoo & Kan (2020) | `10.5771/9783956507762` | **caso-teste de cobertura de campo**. O DOI é o do volume dos anais, não o do trabalho: na etapa 2, procurar por título |

**Procedimento, em duas etapas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões da revisão, para saber se a base indexa a semente. Semente não indexada **sai do denominador desta base** e registra-se como cobertura da base, não como falha da busca. *Etapa 2:* procurar a semente na exportação de EB4 por DOI e depois por título, **sem reexecutar a busca**.

**Limiar de 80%.** O número que decide é o **global**, sobre a união das bases: perder uma semente aqui e achá-la em outra não é perda de portfólio. A aderência por base diagnostica **qual** base e **qual** faceta falharam.

**Lematização.** Presumida para o inglês, **não medida**. A Clarivate documenta lematização de plural regular em `TS=`; não há documentação equivalente para português e espanhol. A **derivação adjetival** não é alcançada por lematização alguma — `ontological` não é flexão de `ontology` —, e é por isso que as formas adjetivais estão no vocabulário.

**Cobertura de anais.** A assinatura institucional cobre o *Conference Proceedings Citation Index*, de modo que não há semente a excluir do denominador por cobertura de anais. Isso não decide a SE10: a indexação de anais é seletiva por trabalho, e é a consulta da etapa 1 que separa cobertura de falha da busca.

**Caso-teste de cobertura de campo — SE10.** O domínio está fora do título: o que aparece é `pedagogies`, que é prática, não domínio. A recuperação depende do resumo e das palavras-chave. Se EB4 recuperar, recuperou por campo que não é o título; se não recuperar, a perda deixa de ser estimada e passa a ser medida. Anotar o resultado no registro.

**Estado atual.** A aderência está **suspensa** até a consulta que decide se a SE10 está indexada. Enquanto isso, o retorno de EB4 são **candidatos**, não portfólio. O estado, as sementes recuperadas e a consulta pendente estão em `data/registro_execucao.json`. Todos os retornos anteriores a 18/11/2026 são **vencidos**: os de 17/11 por precederem a v2, e qualquer outro porque em 18/11 as strings passaram a ser a STR v2 literal — sete formas em espanhol da `STR1` e `pedagogía` acrescentadas, e `ontological engineering`, `teaching practice` e `aprendiz` incluídos na STR v2 por decisão do ReT; três repetições eliminadas. Não servem ao IO 2 até a reexecução.

---

## 6. Ressalvas

1. **Estatuto dos termos.** Todos os termos desta ficha são **termos livres**: nenhum foi confrontado com instrumento de controle terminológico. A validação do 2º passo corre em duas vias — Tesauro Brasileiro de Ciência da Informação (IBICT), para o português, e UNESCO Thesaurus, para inglês e espanhol. ERIC Thesaurus, Brased/INEP, ACM CCS, LISTA, W3C e IEEE LOM ficam **sem consulta**, e os termos que deles dependeriam permanecem livres até o encerramento da revisão. A ausência de validação não retira o termo da expressão; retira-lhe a qualidade de descritor autorizado.

2. **Termos qualificados para busca.** Três operações sobre o vocabulário, nenhuma delas supressão de termo. **Substituição:** palavra isolada de uso geral — *learning*, *teaching*, *aprendizagem*, *ensino*, *taxonomy*, *classification*, *ranking*, *adaptation*, *inference* — entra pelas formas compostas correspondentes, ou sai da expressão permanecendo no quadro. **Desdobramento:** termo em notação compacta de variante — “thesaurus/thesauri”, “knowledge organization system(s)” — vai à expressão como alternativas explícitas ligadas por `OR`, porque a barra e o parêntese, dentro de aspas, são caracteres literais. **Desdobramento morfológico:** formas adjetivais e plurais entram na expressão; a derivação adjetival importa porque base alguma a alcança a partir do substantivo, ao contrário do plural regular. Substituição e retirada casam a **forma, não o lema**: variante nova de termo retirado tem de ser retirada também.

3. **`LA=`.** A *tag* foi confirmada em material de treinamento da FECYT, não na página de *field tags* da Clarivate. Antes de usá-la, executar uma consulta mínima (`TS=ontology AND LA=Portuguese`); se a interface recusar, usar o refinamento por idioma.

4. **Texto completo.** A Core Collection é base referencial: a disponibilidade do texto completo depende do acesso institucional e não constitui filtro de busca. O critério correspondente opera na 2ª filtragem.

5. **Teses e dissertações.** Não são cobertas por esta base. A lacuna é coberta pela BRAPCI e, se necessário, pela BDTD, registrada como ampliação do 6º passo (fontes).
