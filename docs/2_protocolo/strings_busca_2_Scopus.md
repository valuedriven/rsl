# Strings de busca — Scopus

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º passo, e Etapa 2, 1º passo.  
**Fonte:** Scopus — *Advanced search*. **Elaborado em:** 05/11/2026.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** VT.  
**Revisão:** 08/11/2026 — recorte temporal 2017–2026 e saída da instanciação em estruturas computacionais do objeto da revisão. Quatro facetas, quatro expressões, quatro questões secundárias. Cronologia das decisões, com as reduções anteriores: Anexo A, seções 1 e 5.

> **As duas consultas prontas para colar no navegador estão nas seções 3 e 4** — na 3 como strings por faceta `#1` e `#1b`, na 4 montadas na expressão de cobertura E4, com a preparação da interface. Antes de executar qualquer uma, a sondagem que fecha a seção 1.

---

## 1. Estado de verificação da sintaxe

| Elemento | Situação | Evidência |
| :--- | :--- | :--- |
| `TITLE-ABS-KEY()` | Verificado | Elsevier, *Scopus Search API — search tips* |
| `PUBYEAR >`, `<`, `=` | Verificado | idem |
| `LANGUAGE()` | Verificado | idem |
| `DOCTYPE()` com os códigos `ar` (artigo), `re` (revisão), `cp` (trabalho em anais), `ch` (capítulo), `bk`, `ed`, `le`, `no`, `sh` | Verificados | idem |
| `SRCTYPE()` com `j`, `b`, `k`, `p`, `r`, `d` | Verificado | idem |
| `OPENACCESS(0` ou `1)` | Verificado | idem |
| `AND`, `OR`, `AND NOT`; precedência OR → AND → AND NOT | Verificado | idem — com a advertência, na própria página, de que **“In 2026, the Boolean Operator Precedence will be updated”** |
| Truncamento `*` e `?`, mínimo de 3 caracteres antes do curinga | Verificado | idem |
| Proximidade `W/n` e `PRE/n` | Verificados | idem |
| `{}` frase exata *versus* `""` frase aproximada | Verificado | idem |
| Limite de número de operadores por consulta | **Não documentado** | se a interface recusar a expressão, aplicar a redução da seção 5.2 |

> **Precedência.** Porque a própria documentação anuncia alteração da precedência de operadores em 2026, **todas** as facetas abaixo vão entre parênteses explícitos e nenhuma expressão depende da ordem implícita de avaliação.

---

## 2. Critérios de elegibilidade: o que entra na string

| Critério | Expresso na string? | Como |
| :--- | :--- | :--- |
| Intervalo temporal 2017–2026 | **Sim** | `AND PUBYEAR > 2016 AND PUBYEAR < 2027`. A cota superior foi acrescentada depois de a exportação de E4 trazer 8 registros de 2027: `PUBYEAR > 2016` sozinho não fecha o recorte |
| Idiomas | **Sim** | `AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish))` |
| Tipo documental | **Sim** | `AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))`. Teses e dissertações não são tipo documental da Scopus |
| Disponibilidade de texto completo | **Não como tal** | `OPENACCESS(1)` restringe a acesso aberto, que **não** equivale a texto completo disponível pela via institucional. Usar apenas como variante de contingência (seção 5.3), nunca na busca principal, sob pena de viés de acesso |
| Domínio educacional | **Sim**, por âncora | facetas 🟦 e 🟨 em todas as quatro expressões |
| Adequação temática | **Não** | filtragens do Módulo 3, Etapa 3 |

---

## 3. Strings por faceta, em sintaxe nativa

### `#1` — 🟦 Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
TITLE-ABS-KEY("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías")
```

### `#2` — 🟨 Domínio educacional — **âncora obrigatória**

```
TITLE-ABS-KEY("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")
```

### `#3` — 🟥 Práticas do processo de ensino-aprendizagem

```
TITLE-ABS-KEY("practice" OR "educational practice" OR "pedagogical practice" OR "teaching practice" OR "instructional practice" OR "teaching strategy" OR "instructional strategy" OR "teaching method" OR "instructional method" OR "teaching technique" OR "learning activity" OR "learning task" OR "educational intervention" OR "instructional intervention" OR "teaching sequence" OR "instructional sequence" OR "pedagogy" OR "pedagogies" OR "best practices" OR "recommended practices" OR "pedagogical approach" OR "instructional approach" OR "instructional design" OR "learning design" OR "pedagogical pattern" OR "pedagogical design pattern" OR "active learning method" OR "teaching methodology" OR "prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boas práticas" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino" OR "práctica" OR "prácticas educativas" OR "práctica educativa" OR "práctica pedagógica" OR "práctica docente" OR "estrategia de enseñanza" OR "estrategia didáctica" OR "método de enseñanza" OR "método instruccional" OR "técnica de enseñanza" OR "actividad de aprendizaje" OR "tarea de aprendizaje" OR "intervención educativa" OR "intervención pedagógica" OR "secuencia didáctica" OR "secuencia instruccional" OR "pedagogía" OR "pedagogías" OR "buenas prácticas" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoque instruccional" OR "diseño instruccional" OR "diseño del aprendizaje" OR "diseño didáctico" OR "patrón pedagógico" OR "patrón de diseño pedagógico" OR "método de aprendizaje activo" OR "metodología de enseñanza")
```

### `#4` — 🟧 Fatores situacionais

```
TITLE-ABS-KEY("situational factors" OR "situational factor" OR "situation of use" OR "application context" OR "context of use" OR "educational context" OR "learning context" OR "contextual factors" OR "context factors" OR "application conditions" OR "implementation conditions" OR "learning situation" OR "educational setting" OR "learning environment" OR "institutional context" OR "sociocultural context" OR "target population" OR "class profile" OR "learner characteristics" OR "educational level" OR "education modality" OR "educational institution" OR "educational infrastructure" OR "learning infrastructure" OR "available resources" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context-aware" OR "contextualization" OR "contextualisation" OR "fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem" OR "fatores contextuais" OR "fatores de contexto" OR "condições de aplicação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "ambiente de aprendizagem" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recursos disponíveis" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização" OR "factores situacionales" OR "factor situacional" OR "situación de uso" OR "contexto de aplicación" OR "contexto educativo" OR "contexto de aprendizaje" OR "factores contextuales" OR "factores del contexto" OR "condiciones de aplicación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "escenario educativo" OR "entorno de aprendizaje" OR "población destinataria" OR "perfil del grupo" OR "características de los estudiantes" OR "nivel educativo" OR "modalidad educativa" OR "institución educativa" OR "infraestructura educativa" OR "recursos disponibles" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "sensible al contexto" OR "contextualización")
```

---

## 4. As quatro expressões de busca

Cada expressão já incorpora período, idioma e tipo documental. Colar integralmente no campo de *Advanced search*.

> **Por que a expressão “geral” é a mais estreita, e não a mais ampla.** No gabarito do IO 1, *geral* qualifica a **composição** — E1 reúne todas as strings montadas —, e não o alcance. Como as facetas se combinam por `AND`, acrescentar faceta **restringe**: E1 exige que o registro mencione as quatro, e por isso é a mais específica do conjunto; a mais ampla é a de cobertura, que exige apenas as duas âncoras. Daí **E1 ⊂ E2 ⊂ E4** e **E1 ⊂ E3 ⊂ E4**. Registro que não satisfaça E1 **não é excluído**: permanece se satisfizer a de cobertura, porque as facetas temáticas são dimensões combináveis, e não requisitos cumulativos de recuperação. O valor de E1 é caracterizar — quem reúne as quatro facetas tende a ser central à questão de revisão, e é a primeira chave da ordem de leitura.

**Obrigatoriedade de cada execução.** As quatro expressões não têm o mesmo estatuto no processo, e confundi-los custa caro nas duas direções — executar o que é redundante, ou pular o que é indispensável:

| | Executar na base? | Como quê | O que se perde ao pular |
| :--- | :--- | :--- | :--- |
| **E4** (cobertura) | **sim, sempre** | **é o portfólio**: define o que a revisão recuperou nesta base | tudo — a base não participa da revisão, não há exportação e a derivação não roda |
| **E2** | **sim** | teste de fidelidade da derivação | nenhum registro, e **a auditabilidade das contagens derivadas** |
| **E3** | **sim** | teste de fidelidade da derivação | idem |
| **E1** (geral) | não | caracterização, por derivação local | nada, desde que a derivação rode: a contagem de E1 é obrigatória, a sua execução não |

> **Leitura de um retorno vazio.** Antes de ler zero como achado, é preciso **provar que não é artefato de sintaxe** — nesta revisão houve três retornos zero por defeito de consulta, e um zero silencioso registrado como resultado apareceria no diagrama PRISMA como conclusão. Provada a execução válida: **E4 = 0 é quase sempre defeito**, pois significaria que a base não tem literatura alguma sobre artefatos de representação no domínio educacional; **E2 = 0** com E4 > 0 é achado — há artefatos, mas nenhum que represente práticas; **E3 = 0** é achado forte e plausível, já que a representação de fatores situacionais é a parte menos consolidada da questão; **E1 = 0** é o enunciado mais nítido da lacuna, e deixa a primeira chave da ordem de triagem uniforme.

> **Zero derivado e zero executado são afirmações diferentes.** O zero derivado pode vir da limitação do casamento local, que vê apenas título, resumo e palavras-chave como exportados. **Contagem derivada igual ou próxima de zero obriga à execução direta daquela expressão antes de ser relatada como achado.**

> **D6 vale aqui também, e por força do mesmo argumento.** A redação anterior desta ficha punha `W/5` só em E4, e E1, E2 e E3 em conjunção simples — **a mesma assimetria que, na Web of Science, fez E2 devolver mais registros que E4**. Aqui ela não produziu incoerência visível, porque E4 é grande o bastante para acomodar E2 mesmo medindo coisa diferente: **a conferência passou em silêncio**, o que é pior do que reprovar. As quatro passam a levar `W/5` entre as âncoras, e a continência volta a valer por construção. O filtro de ano e o de tipo documental já eram uniformes nesta ficha.

### E1 (geral) — todas as strings montadas. **“Geral” é a composição, não o alcance**: por exigir as quatro facetas simultaneamente, é a MAIS RESTRITIVA das quatro

*DERIVADA localmente — não executar.*

**Facetas:** 🟦 AND 🟨 AND 🟥 AND 🟧

```
TITLE-ABS-KEY(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") W/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")) AND TITLE-ABS-KEY("practice" OR "educational practice" OR "pedagogical practice" OR "teaching practice" OR "instructional practice" OR "teaching strategy" OR "instructional strategy" OR "teaching method" OR "instructional method" OR "teaching technique" OR "learning activity" OR "learning task" OR "educational intervention" OR "instructional intervention" OR "teaching sequence" OR "instructional sequence" OR "pedagogy" OR "pedagogies" OR "best practices" OR "recommended practices" OR "pedagogical approach" OR "instructional approach" OR "instructional design" OR "learning design" OR "pedagogical pattern" OR "pedagogical design pattern" OR "active learning method" OR "teaching methodology" OR "prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boas práticas" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino" OR "práctica" OR "prácticas educativas" OR "práctica educativa" OR "práctica pedagógica" OR "práctica docente" OR "estrategia de enseñanza" OR "estrategia didáctica" OR "método de enseñanza" OR "método instruccional" OR "técnica de enseñanza" OR "actividad de aprendizaje" OR "tarea de aprendizaje" OR "intervención educativa" OR "intervención pedagógica" OR "secuencia didáctica" OR "secuencia instruccional" OR "pedagogía" OR "pedagogías" OR "buenas prácticas" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoque instruccional" OR "diseño instruccional" OR "diseño del aprendizaje" OR "diseño didáctico" OR "patrón pedagógico" OR "patrón de diseño pedagógico" OR "método de aprendizaje activo" OR "metodología de enseñanza") AND TITLE-ABS-KEY("situational factors" OR "situational factor" OR "situation of use" OR "application context" OR "context of use" OR "educational context" OR "learning context" OR "contextual factors" OR "context factors" OR "application conditions" OR "implementation conditions" OR "learning situation" OR "educational setting" OR "learning environment" OR "institutional context" OR "sociocultural context" OR "target population" OR "class profile" OR "learner characteristics" OR "educational level" OR "education modality" OR "educational institution" OR "educational infrastructure" OR "learning infrastructure" OR "available resources" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context-aware" OR "contextualization" OR "contextualisation" OR "fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem" OR "fatores contextuais" OR "fatores de contexto" OR "condições de aplicação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "ambiente de aprendizagem" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recursos disponíveis" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização" OR "factores situacionales" OR "factor situacional" OR "situación de uso" OR "contexto de aplicación" OR "contexto educativo" OR "contexto de aprendizaje" OR "factores contextuales" OR "factores del contexto" OR "condiciones de aplicación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "escenario educativo" OR "entorno de aprendizaje" OR "población destinataria" OR "perfil del grupo" OR "características de los estudiantes" OR "nivel educativo" OR "modalidad educativa" OR "institución educativa" OR "infraestructura educativa" OR "recursos disponibles" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "sensible al contexto" OR "contextualización") AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### E2 (específica) — modelos e ontologias que representam práticas do processo de ensino-aprendizagem

*DERIVADA localmente — executar apenas no teste de fidelidade.*

**Facetas:** 🟦 AND 🟨 AND 🟥

```
TITLE-ABS-KEY(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") W/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")) AND TITLE-ABS-KEY("practice" OR "educational practice" OR "pedagogical practice" OR "teaching practice" OR "instructional practice" OR "teaching strategy" OR "instructional strategy" OR "teaching method" OR "instructional method" OR "teaching technique" OR "learning activity" OR "learning task" OR "educational intervention" OR "instructional intervention" OR "teaching sequence" OR "instructional sequence" OR "pedagogy" OR "pedagogies" OR "best practices" OR "recommended practices" OR "pedagogical approach" OR "instructional approach" OR "instructional design" OR "learning design" OR "pedagogical pattern" OR "pedagogical design pattern" OR "active learning method" OR "teaching methodology" OR "prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boas práticas" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino" OR "práctica" OR "prácticas educativas" OR "práctica educativa" OR "práctica pedagógica" OR "práctica docente" OR "estrategia de enseñanza" OR "estrategia didáctica" OR "método de enseñanza" OR "método instruccional" OR "técnica de enseñanza" OR "actividad de aprendizaje" OR "tarea de aprendizaje" OR "intervención educativa" OR "intervención pedagógica" OR "secuencia didáctica" OR "secuencia instruccional" OR "pedagogía" OR "pedagogías" OR "buenas prácticas" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoque instruccional" OR "diseño instruccional" OR "diseño del aprendizaje" OR "diseño didáctico" OR "patrón pedagógico" OR "patrón de diseño pedagógico" OR "método de aprendizaje activo" OR "metodología de enseñanza") AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### E3 (específica) — artefatos que formalizam os fatores situacionais do domínio educacional

*DERIVADA localmente — executar apenas no teste de fidelidade.*

**Facetas:** 🟦 AND 🟨 AND 🟧

```
TITLE-ABS-KEY(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") W/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")) AND TITLE-ABS-KEY("situational factors" OR "situational factor" OR "situation of use" OR "application context" OR "context of use" OR "educational context" OR "learning context" OR "contextual factors" OR "context factors" OR "application conditions" OR "implementation conditions" OR "learning situation" OR "educational setting" OR "learning environment" OR "institutional context" OR "sociocultural context" OR "target population" OR "class profile" OR "learner characteristics" OR "educational level" OR "education modality" OR "educational institution" OR "educational infrastructure" OR "learning infrastructure" OR "available resources" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context-aware" OR "contextualization" OR "contextualisation" OR "fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem" OR "fatores contextuais" OR "fatores de contexto" OR "condições de aplicação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "ambiente de aprendizagem" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recursos disponíveis" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização" OR "factores situacionales" OR "factor situacional" OR "situación de uso" OR "contexto de aplicación" OR "contexto educativo" OR "contexto de aprendizaje" OR "factores contextuales" OR "factores del contexto" OR "condiciones de aplicación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "escenario educativo" OR "entorno de aprendizaje" OR "población destinataria" OR "perfil del grupo" OR "características de los estudiantes" OR "nivel educativo" OR "modalidad educativa" OR "institución educativa" OR "infraestructura educativa" OR "recursos disponibles" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "sensible al contexto" OR "contextualización") AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### E4 (de cobertura) — artefatos de representação do conhecimento no domínio educacional, inclusive quando não mencionam as demais facetas nos metadados

*EXECUTADA e EXPORTADA nesta base.*

**Facetas:** 🟦 AND 🟨

```
TITLE-ABS-KEY(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") W/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

**Forma ampla, por conjunção — NÃO é a forma executada.** Registrada como limite superior do recorte; o seu retorno entra no IO 2 como dado de calibração, ao lado do retorno da forma executada. **Por D6, se a aderência reprovar a proximidade, esta forma também se aplica às quatro**, e não só a E4.

```
TITLE-ABS-KEY("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") AND TITLE-ABS-KEY("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa") AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

> **Condição de adoção:** igual à da Web of Science — recuperação do conjunto-semente igual ou superior a 80%, medida antes de aceitar a proximidade como forma da busca. Esta base espera **seis sementes** — as de números 2, 3, 4, 7, 8 e 9 —, mais que qualquer outra, e é por isso o teste mais informativo do conjunto.

---

## 4.5 Execução — **A FAMÍLIA AMPLA, MEDIDA E COERENTE**

**A consulta de E4 submetida foi conferida contra as duas formas desta ficha e é IDÊNTICA, caractere a caractere, à forma ampla por conjunção** — 5.269 caracteres, sem `W/5`. Não há ambiguidade a resolver: sabe-se exatamente o que foi executado.

| Expressão | Retorno | Fração de E4 |
| :--- | ---: | ---: |
| **E1** | 608 | 3,4% |
| **E2** | 5.365 | 30,4% |
| **E3** | 1.943 | 11,0% |
| **E4** | 17.677 | 100% |

| Relação obrigatória | Verificação |
| :--- | :--- |
| E1 ⊆ E2 | passa — 608 ≤ 5.365 |
| E1 ⊆ E3 | passa — 608 ≤ 1.943 |
| E2 ⊆ E4 | passa — 5.365 ≤ 17.677 |
| E3 ⊆ E4 | passa — 1.943 ≤ 17.677 |

**As quatro medem a MESMA forma, e por isso a coerência delas significa alguma coisa.** A redação anterior desta ficha punha `W/5` só em E4; a execução, porém, usou a forma ampla em E4, e as demais já eram conjunção simples. **O resultado é uma família internamente consistente** — quatro expressões da mesma forma, com os mesmos filtros de ano, idioma e tipo documental. A assimetria que D6 corrigiu existia na ficha e **não chegou a contaminar esta execução**.

**17.677 registros são o LIMITE SUPERIOR do recorte nesta base**, que é exatamente o dado de calibração que esta ficha pedia e não tinha. Deixa de ser estimativa.

#### A estrutura, comparada com a da Web of Science

| | Scopus, forma ampla | Web of Science, forma com proximidade |
| :--- | ---: | ---: |
| E1 / E4 | 3,4% | 1,7% |
| E2 / E4 | 30,4% | 24,2% |
| E3 / E4 | 11,0% | 9,3% |
| E4 | 17.677 | 1.596 |

**As proporções são próximas, apesar de medirem bases diferentes em formas diferentes.** A fração que reúne as quatro facetas fica entre 1,7% e 3,4%; a de práticas, entre 24% e 30%; a de fatores situacionais, entre 9% e 11%. **A assimetria entre práticas e fatores situacionais repete-se nas três bases executadas até aqui** — a literatura que representa a prática é duas a três vezes maior que a que representa o seu condicionamento. Três bases, duas línguas, duas formas de expressão: é regularidade e não acidente de uma consulta.

#### Segunda execução — a família com proximidade, **menos E4**

| Expressão | Forma ampla | **Com `W/5`** | Retenção |
| :--- | ---: | ---: | ---: |
| E1 | 608 | **178** | 29,3% |
| E2 | 5.365 | **1.013** | 18,9% |
| E3 | 1.943 | **543** | 27,9% |
| E4 | 17.677 | *17.677* | *100%* |

#### O caminho até o número certo

A primeira execução com `W/5` devolveu em E4 o mesmo da forma ampla, e esta ficha concluiu que a consulta não teria sido reexecutada. **A conclusão estava errada e fica retificada**: o ReT confirmou a reexecução. O argumento que a sustentava — proximidade é estritamente mais estreita que conjunção — vale **sob o pressuposto de que o motor aplique o operador como o documenta**, e era o pressuposto que faltava medir. Mediu-se.

#### Sonda do operador — **EXECUTADA, e conclusiva**

| # | Consulta | Retorno | Retenção |
| :---: | :--- | ---: | ---: |
| 1 | `TITLE-ABS-KEY(ontology AND education)` | 3.729 | — |
| 2 | `TITLE-ABS-KEY(ontology W/5 education)` | **380** | 10,2% |
| 3 | `TITLE-ABS-KEY(("ontology" OR "thesaurus") AND ("education" OR "curriculum"))` | 4.230 | — |
| 4 | `TITLE-ABS-KEY(("ontology" OR "thesaurus") W/5 ("education" OR "curriculum"))` | **465** | 11,0% |

Todas com `AND PUBYEAR > 2016` e nada mais.

**O operador `W/5` funciona, e funciona nos dois casos que importavam.** Corta 89,8% entre termos simples e 89,0% entre grupos de frases entre aspas. **E as duas consultas com proximidade são a expressão de proximidade SOZINHA**, sem segunda cláusula — que era exatamente a diferença estrutural sob suspeita. **As hipóteses 1 e 3 estão refutadas por medição.**

> **Resta a hipótese 2, e a conclusão é desconfortável mas é a que sobra:** o texto submetido em E4 não foi o da forma com proximidade. A forma ampla e a forma com proximidade diferem em onze caracteres — 5.269 contra 5.258 — e são visualmente quase idênticas ao longo de cinco mil caracteres de termos; recuperar a errada do histórico ou da área de transferência é o acidente mais fácil desta execução inteira. **Não é erro de método: é o que acontece quando a consulta é longa demais para se conferir a olho.**

**Com o operador comprovado, a consulta correta foi submetida a partir de arquivo** — para que não dependesse de recuperar texto da interface — e o resultado fecha o caso:

| Texto submetido | Retorno |
| :--- | ---: |
| Forma com `W/5`, do arquivo | **3.194** |
| Forma com `W/5`, do primeiro bloco desta seção | **3.194** |
| Forma ampla, do segundo bloco desta seção | 17.677 |

**As duas vias da forma com proximidade devolveram o mesmo número, e a forma ampla devolveu o anterior.** Fica provado que o arquivo e a ficha carregam a mesma consulta, e que o retorno de 17.677 era mesmo da forma ampla. A hipótese 2 está confirmada por construção, e não por eliminação.

#### A previsão que esta ficha fez, e errou

A ficha previu, pela retenção da sonda, que E4 com proximidade devolveria **entre 1.800 e 1.950** registros. Devolveu **3.194** — cerca de 1,7 vez mais. **A previsão estava errada, e a razão é instrutiva:**

| Medição | Retenção da proximidade |
| :--- | ---: |
| Sonda, dois termos de cada lado | 11,0% |
| Web of Science, facetas inteiras | 15,4% |
| Scopus, facetas inteiras | **18,1%** |

**A retenção da proximidade CRESCE com a riqueza dos operandos.** Com dois termos de cada lado, é preciso que aquele par específico caia a cinco palavras; com noventa de um lado e cento e dez do outro, basta que **algum** par caia. A sonda mediu o operador corretamente e **subestimou o seu efeito sobre as facetas inteiras** — e as duas bases concordam nisso, com 15,4% e 18,1% contra os 11,0% da sonda.

> **Fica como regra, porque vale para a próxima base:** retenção de proximidade medida em par mínimo é **cota inferior** do que as facetas inteiras retêm, não estimativa. A cota deduzida da união de E2 e E3 — 1.378 — essa não errou, porque não era extrapolação e sim dedução das medições desta mesma base.

#### A família completa, e a conferência final

| Expressão | Forma ampla | **Com `W/5`** | Retenção | Fração de E4 |
| :--- | ---: | ---: | ---: | ---: |
| **E1** | 608 | **178** | 29,3% | 5,6% |
| **E2** | 5.365 | **1.013** | 18,9% | 31,7% |
| **E3** | 1.943 | **543** | 27,9% | 17,0% |
| **E4** | 17.677 | **3.194** | 18,1% | 100% |

| Relação obrigatória | Verificação |
| :--- | :--- |
| E1 ⊆ E2 | passa — 178 ≤ 1.013 |
| E1 ⊆ E3 | passa — 178 ≤ 543 |
| E2 ⊆ E4 | passa — 1.013 ≤ 3.194 |
| E3 ⊆ E4 | passa — 543 ≤ 3.194 |
| Cota deduzida da união de E2 e E3 | passa — 1.378 ≤ 3.194 ≤ 17.677 |

**A família está completa e coerente, e a quinta verificação é a que vale mais**, porque não é tautológica: a cota de 1.378 foi deduzida das medições de E2 e E3 **antes** de E4 ser executada, e o retorno medido a respeita. Previsão independente que se confirma é a forma mais barata de confiança que este protocolo tem.

#### A estrutura de E4 nesta base

| Partição de E4 | Registros | |
| :--- | ---: | ---: |
| E1 — as quatro facetas | 178 | 5,6% |
| só práticas | 835 | 26,1% |
| só fatores situacionais | 365 | 11,4% |
| só as âncoras | 1.816 | 56,9% |
| **E4** | **3.194** | **100%** |

**Comparada com a Web of Science, esta base é mais densa no núcleo**: 5,6% dos registros reúnem as quatro facetas, contra 1,7% lá. A assimetria entre práticas e fatores situacionais mantém-se — 26,1% contra 11,4%, pouco mais de duas vezes —, e é a quarta vez que ela aparece.

#### Exportação de E4

| | |
| :--- | ---: |
| Registros exportados | 3.194 |
| Distintos por identificador, DOI ou título | **3.190** |
| **Fora do recorte de 2017 a 2026** | **8**, todos de 2027 |

**Defeito da ficha, apanhado pela exportação: o filtro de ano não tinha cota superior.** `AND PUBYEAR > 2016` deixa entrar tudo o que vier depois, e entraram 8 registros de 2027 — pré-publicações e números antecipados. A Web of Science usava `PY=(2017-2026)`, com as duas cotas, desde o início; **só esta ficha estava aberta de um lado**. Corrigido para `AND PUBYEAR > 2016 AND PUBYEAR < 2027`, e a consulta em arquivo foi regravada. Os 8 registros podem sair na deduplicação, mas o recorte tem de fechar na consulta, não na limpeza.

> **A exportação traz ainda `label.ris.referenceType.BOOK_CHAPTER` como tipo em 291 registros**, em lugar do rótulo traduzido. É defeito do exportador da base, não dos dados; anotar para que a contagem por tipo no IO 2 não o reproduza.

#### Teste de aderência — **REPROVADO**

| Semente | Resultado |
| :---: | :--- |
| 2 — Das, Naskar & Roy | encontrada, por DOI |
| 3 — Chi, Chen & Hung | **ausente** |
| 4 — Shvets e outros | **ausente** |
| 7 — Chimalakonda & Nori | encontrada, por DOI |
| 8 — Cenka, Santoso & Junus | encontrada, por DOI |
| 9 — Piriyapongpipat, Goldin & Dit. | encontrada, por DOI |

**4 de 6 = 67%, contra o limiar de 80%.** É reprovação, e não por margem estreita.

**E a causa NÃO é a proximidade — isto está medido, não suposto.** Os títulos das duas ausentes trazem as duas âncoras, e trazem-nas perto:

| Semente | Título | 🟦 | 🟨 | Distância no título |
| :---: | :--- | :--- | :--- | :--- |
| 3 | *Learning adaptivity in support of flipped learning: an ontological…* | `ontological` | `learning` | **2 palavras** |
| 4 | *Towards a Domain Model for Learning and Teaching* | `domain model` | `learning`, `teaching` | **2 palavras** |

**Ambas satisfariam `W/5` só pelo título.** Logo a perda ocorre antes da proximidade — e as hipóteses que restam são outras: o registro não está indexado nesta base; está indexado e não sobrevive aos filtros de idioma ou de tipo documental; ou o motor não está aplicando o operando inteiro.

#### Anatomia da perda — quatro consultas por semente

Cada passo isola uma causa, e o primeiro que falhar é a causa. Substituir `<DOI>` pelo DOI da semente: `10.1111/exsy.12246` para a 3, `10.5220/0012471400003645` para a 4.

| # | Consulta | Se devolver zero |
| :---: | :--- | :--- |
| 1 | `DOI(<DOI>)` | **a base não indexa o estudo** — sai do denominador, e a aderência recalcula-se sobre as que restam |
| 2 | `DOI(<DOI>) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))` | **um filtro a exclui** — e o quadro de critérios do IO 1 tem de dizer qual, porque é exclusão deliberada e não falha |
| 3 | `DOI(<DOI>) AND TITLE-ABS-KEY(🟦) AND TITLE-ABS-KEY(🟨)` | **o vocabulário não a alcança** — é falha de faceta, e a emenda é de termo |
| 4 | `DOI(<DOI>) AND TITLE-ABS-KEY((🟦) W/5 (🟨))` | **a proximidade a exclui** — e então sim a forma da busca está em causa |

> **Oito consultas ao todo, e elas decidem mais do que esta base.** Se a causa for a proximidade, a condição de adoção manda voltar à forma ampla **nas quatro expressões e nas duas bases**, por D6. Se for cobertura ou filtro, a proximidade sobrevive e o denominador muda. **Não se escolhe entre as duas por conveniência: escolhe-se pelo passo em que a consulta devolver zero.**

#### O que falta nesta base

| | O que fazer |
| :---: | :--- |
| 1 | ~~Executar E4 com `W/5`~~ **FEITO** — 3.194, dentro da faixa prevista pela cota |
| 2 | **Exportar E4** na forma adotada |
| 3 | ~~Medir a aderência~~ **FEITO, e REPROVOU**: 4 de 6. Rodar a anatomia da perda das sementes 3 e 4 |

> **Dimensão do que vem pela frente.** Se a proximidade aqui reduzir na mesma proporção que reduziu na Web of Science — onde a forma com proximidade reteve cerca de 15% da ampla —, E4 ficaria na casa dos 2.700 registros. **É extrapolação de uma base para outra e não entra no IO 2**; serve para dimensionar a triagem antes de a consulta correr. Se a proximidade for reprovada pela aderência, o volume de triagem é o de 17.677, e o prazo resolve-se pela ordem de leitura.

---

## 5. Variantes previstas

### 5.1 Sem limite de tipo documental

Para medir o peso da restrição documental, executar a expressão de cobertura suprimindo a cláusula `DOCTYPE` e comparar os retornos. A diferença é reportada no IO 2 como efeito do critério.

### 5.2 Redução por recusa da interface

Se a expressão for recusada por extensão, dividir a faceta 🟨 em duas execuções complementares — a primeira com os termos de educação formal, a segunda com os termos de tecnologia educacional e aprendizagem digital — mantendo as demais facetas idênticas, e somar os retornos com deduplicação. Registrar a divisão como adaptação.

### 5.3 Acesso aberto (contingência)

```
AND OPENACCESS(1)
```

Usar **apenas** se a obtenção de textos completos se mostrar inviável na 2ª filtragem, e declarar o viés de acesso resultante como limitação da revisão.

### 5.5 Camada de precisão

Pelos mesmos motivos registrados na ficha da Web of Science — retorno de mais de 36.000 registros na expressão de cobertura, concentrado no cruzamento de `ontology` com `learning` —, as strings da seção 3 já usam os termos qualificados. Se o retorno permanecer alto, aplicar a proximidade entre as âncoras, com o operador `W/n`, que a documentação da Elsevier registra:

```
TITLE-ABS-KEY((ontolog* OR "knowledge graph*" OR "knowledge organization*" OR "conceptual model*" OR thesaur*) W/5 (educat* OR teaching OR learner* OR student* OR curricul* OR pedagog*)) AND PUBYEAR > 2016
```

Como camada seguinte, restringir a área temática com `SUBJAREA`, conferindo os códigos na documentação antes do uso. Vale aqui a mesma regra de decisão: toda camada é medida contra o conjunto-semente, e recuperação inferior a 80% a reprova.

### 5.4 Truncamento e proximidade

A Scopus admite `*` e `?` e os operadores `W/n` e `PRE/n`. Nenhum foi aplicado nas strings acima, para manter a equivalência com a execução na Web of Science e permitir a comparação dos retornos. Variante a testar no conjunto-semente, se o *recall* ficar abaixo do limiar:

```
TITLE-ABS-KEY(ontolog* W/5 educat*)
```

---

## 6. Conjunto-semente — o que esta base deve recuperar

O conjunto-semente tem **10 estudos**, todos conferidos em fonte e todos dentro do escopo. Pela indicação do ReT, **6 são esperados nesta base**. Instrumento completo, procedimento e estado de conferência de cada referência: `data/saida/semente/Conjunto_Semente.md`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| 2 | Das et al. (2022) | `10.5771/0943-7444-2022-1-6` | — |
| 3 | Chi et al. (2018) | `10.1111/exsy.12246` | — |
| 4 | Shvets et al. (2024) | `10.5220/0012471400003645` | — |
| 7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| 8 | Cenka et al. (2023) | `10.1080/10494820.2022.2039947` | — |
| 9 | Piriyapongpipat et al. (2024) | `10.1186/s40561-024-00307-8` | — |

**Procedimento, em duas etapas, e não confundir as duas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões da revisão, para saber se a base indexa a semente. Semente não indexada **sai do denominador desta base**, e isso se registra como cobertura da base, não como falha da busca. *Etapa 2:* procurar a semente na exportação de E4 já feita, por DOI e depois por título — **sem reexecutar a busca**, porque o teste se faz sobre o que a execução de fato devolveu.

**Limiar de 80%, e o que a reprovação obriga.** O IO 1 fixa o limiar e manda, abaixo dele, revisar o controle terminológico antes de prosseguir, com emenda registrada. O número que decide é o **global**, sobre a união das bases: perder uma semente aqui e achá-la em outra não é perda de portfólio. A aderência por base serve para diagnosticar **qual** base e **qual** faceta falharam.

**Lematização nesta base:** **presumida para o inglês, não medida.** A Elsevier documenta radicalização em `TITLE-ABS-KEY`; o alcance sobre português e espanhol não foi medido. Importa porque o desdobramento morfológico de 08/11/2026 acrescentou plurais e formas adjetivais às facetas: onde a base lematiza, o plural é redundante; onde não lematiza, era perda silenciosa. A **derivação adjetival** é outro caso: `ontological` não é flexão de `ontology`, e **base alguma a alcança** a partir do substantivo. Foi por isso que entrou no vocabulário — duas sementes do conjunto falhavam a âncora de artefato só por causa dela.

**Ressalva de cobertura, a conferir na etapa 1.** Duas sementes desta base não são artigo de periódico: a 4 (Shvets e outros) é comunicação em anais da MODELSWARD, publicada pela SciTePress, e a 10 não é esperada aqui. A cobertura de anais da Scopus é ampla mas seletiva por conferência; retorno vazio na etapa 1 significa **não indexada**, tira a semente do denominador desta base e se registra como cobertura, não como falha da busca.

**Conferência cruzada com a Web of Science.** As duas bases têm cobertura de campo equivalente — `TITLE-ABS-KEY` e `TS=` —, e quatro sementes são esperadas em ambas. **Aderência discrepante entre as duas, sobre as mesmas sementes, indica problema de agrupamento ou de sintaxe, não de cobertura**, e é o diagnóstico mais barato disponível: a mesma semente, a mesma faceta, dois resultados diferentes.

---


## 7. Registro de execução (alimenta o IO 2)

| Execução | Data | Campos | Filtros embutidos | Retornos | Observações |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **E4 — execução única (cobertura)** | | TITLE-ABS-KEY | PUBYEAR, LANGUAGE, DOCTYPE | | exportação completa |
| E2 — teste de fidelidade | | TITLE-ABS-KEY | idem | | só para conferência |
| E3 — teste de fidelidade | | TITLE-ABS-KEY | idem | | só para conferência |
| Contagens E1 a E3 | — | — | — | derivadas | `src/derivar_expressoes.py --derivar`; declarar como derivadas no IO 2 |

> **Derivação.** As contagens derivadas pressupõem o protocolo corrente: rodar
> `python3 src/protocolo.py --gerar`; registrar a execução com
> `python3 src/derivar_expressoes.py --registrar <base> E4 <arquivo> --retorno <n>`; e rodar
> `python3 src/derivar_expressoes.py --derivar`, todos da raiz do repositório. O registro
> confere o retorno declarado contra o arquivo e **recusa registrar quando divergem**; a
> derivação reconfere a contagem e recusa cópia defasada do protocolo. Cada derivado guarda
> o `sha256` do documento de origem.

---

## 8. Ressalvas

1. **Estatuto dos termos — decisão de 06/11/2026.** Todos os termos desta ficha são **termos livres**: nesta data nenhum deles foi confrontado com instrumento algum. São 365 registros de termo nas quatro facetas — 123 em português, 119 em inglês e 123 em espanhol. A validação terminológica do 2º passo é feita em duas vias. *Via automatizada:* Tesauro Brasileiro de Ciência da Informação (IBICT), por interface de serviços TemaTres, para os termos em português; e UNESCO Thesaurus, por endpoint SPARQL, para os termos em inglês e em espanhol. *Sem consulta:* ERIC Thesaurus, Brased/INEP, ACM CCS, LISTA, W3C e IEEE LOM — os termos que deles dependeriam permanecem termos livres até o encerramento da revisão, e assim devem ser declarados no relatório. A ausência de validação não retira o termo das expressões de busca; retira-lhe apenas a qualidade de descritor autorizado. Concluída a validação, só os termos confirmados no TBCI ou no UNESCO podem ser apresentados como descritores autorizados, e a incorporação de termos relacionados ou específicos revelados pela consulta obriga a regerar esta ficha. Registro da validação: `data/saida/validacao/validacao_terminologica.csv`, com a resposta bruta de cada consulta em `data/evidencia/`.

2. **Termos qualificados para busca. Duas operações sobre o vocabulário registrado, nenhuma delas supressão de termo. SUBSTITUIÇÃO: palavra isolada de uso geral — learning, teaching, aprendizagem, ensino, taxonomy, classification, ranking, adaptation, inference e equivalentes — entra na expressão pelas formas compostas correspondentes, ou dela sai permanecendo no quadro. DESDOBRAMENTO: os nove termos em notação compacta de variante — “thesaurus/thesauri”, “knowledge organization system(s)” e congêneres — vão à expressão como alternativas explícitas ligadas por OR, porque a barra e o parêntese, dentro de aspas, são caracteres literais. A camada de qualificação recusa, com erro de execução, termo novo em notação compacta não desdobrada. DESDOBRAMENTO MORFOLÓGICO, acrescentado em 08/11/2026 por emenda autorizada: formas adjetivais e plurais — “ontological”, “ontológicos”, “ontologias”, “educacionais” — e o substantivo isolado de pedagogia entraram nas quatro facetas, por falha medida no ensaio seco do conjunto-semente; a derivação adjetival importa porque base alguma a alcança a partir do substantivo, ao contrário do plural regular. A SUBSTITUIÇÃO E A RETIRADA CASAM A FORMA, NÃO O LEMA: variante nova de termo retirado tem de ser retirada também, uma a uma — foi o que se fez com “taxonomies” e “taxonomías”, que de outro modo reintroduziriam nas strings o termo que a decisão havia excluído. Todos os termos permanecem nos quadros de controle terminológico e na validação do 2º passo. Razão de cada operação e os retornos que a motivaram: Anexo A, seções 3 e 4.**

3. A alteração anunciada na precedência de operadores em 2026 obriga a conferir, na primeira execução, se o número de retornos da expressão de cobertura é compatível com o da mesma expressão na Web of Science. Discrepância de ordem de grandeza indica problema de agrupamento, não de cobertura.

4. `OPENACCESS(1)` **não** é filtro de texto completo institucional; a confusão entre as duas coisas introduziria viés de acesso no portfólio.

