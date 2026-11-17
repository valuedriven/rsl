# Strings de busca — Web of Science (Core Collection)

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º passo (elaboração das expressões de busca) e Etapa 2, 1º passo (execução).  
**Fonte:** Web of Science Core Collection — *Advanced Search*. **Elaborado em:** 05/11/2026.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** bibliotecário(a) de referência (VT).  
**Revisão:** 08/11/2026 — recorte temporal 2017–2026 e saída da instanciação em estruturas computacionais do objeto da revisão. Quatro facetas, quatro expressões, quatro questões secundárias. Cronologia das decisões, com as reduções anteriores: Anexo A, seções 1 e 5.

---

## 1. Estado de verificação da sintaxe

Nenhum elemento de sintaxe abaixo foi presumido. A coluna *Evidência* indica a fonte em que cada recurso foi conferido nesta data.

| Elemento | Situação | Evidência |
| :--- | :--- | :--- |
| `TS=` (tópico: título, resumo, palavras-chave de autor e *Keywords Plus*) | Verificado | Clarivate, *Web of Science Core Collection Advanced Search Field Tags* |
| `TI=`, `AB=`, `AK=`, `SO=`, `KP=`, `WC=`, `SU=`, `DO=`, `ALL=` | Verificados | idem |
| `PY=` (ano de publicação) e exigência de combinação com outra *tag* | Verificado | idem |
| `DT=` (tipo de documento) | Verificado | idem (exemplo `SO=Liver Transplantation* AND DT=Book Chapter`) e FECYT (2024) |
| `LA=` (idioma) | Verificado em fonte **secundária** | FECYT, *De la consulta simple a la compleja en Web of Science* (out. 2024): “LA for Language”, exemplo `LA=Spanish`. **Não** localizado na página de *field tags* da Clarivate |
| Truncamento `*`, `?`, `$`; mínimo de 3 caracteres antes do curinga em Tópico/Título; curinga desativa lematização | Verificado | Clarivate, *Advanced Search examples* |
| Limite de 200 conjuntos de busca por sessão | Verificado | idem |
| Recomendação de intervalos de `PY=` de até 5 anos | Verificado | idem |
| Operador de **disponibilidade de texto completo** em sintaxe de consulta | **Não existe entre as *tags* verificadas** | ausência na página de *field tags*; aplicável apenas como refinamento de interface |
| Valores exatos admitidos em `DT=` e `LA=` | **Não verificados um a um** | conferir na lista suspensa da própria interface antes da execução |

> **Consequência prática.** As expressões da seção 4 usam apenas `TS=` e `PY=`, ambos verificados em documentação oficial. Idioma e tipo documental aparecem em linha separada (seção 5), porque dependem de valores a conferir na interface; e a disponibilidade de texto completo **não** é expressável em consulta, só em refinamento.

---

## 2. Critérios de elegibilidade: o que entra na string e o que não entra

| Critério (4º passo do Item 2) | Expresso na string? | Como |
| :--- | :--- | :--- |
| Intervalo temporal 2017–2026 | **Sim** | `AND PY=(2017-2026)`; variante em blocos de 5 anos na seção 5.1 |
| Idiomas português, inglês e espanhol | Em variante | `AND LA=(English OR Portuguese OR Spanish)` — seção 5.2, valores a conferir |
| Tipo documental | Em variante | `AND DT=(...)` — seção 5.2. Teses e dissertações **não** são cobertas pela Core Collection: ficam a cargo da BRAPCI e da BDTD, fora deste roteiro |
| Disponibilidade de texto completo | **Não** | refinamento de interface após a busca; a não localização em texto completo é critério da 2ª filtragem, não da busca |
| Domínio de aplicação educacional | **Sim**, por âncora | faceta 🟨 obrigatória em todas as quatro expressões |
| Adequação temática (exclusões (a) a (i)) | **Não** | decisão de leitura, nas filtragens do Módulo 3, Etapa 3 |

---

## 3. Strings por faceta, em sintaxe nativa

Cada string abaixo corresponde a um quadro de controle terminológico do 2º passo e é executada como um **conjunto de busca** próprio (`#1` a `#4`), para que as quatro expressões da seção 4 possam ser montadas por combinação de conjuntos sem reexecução dos termos.

### `#1` — 🟦 Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
TS=("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías")
```

### `#2` — 🟨 Domínio educacional — **âncora obrigatória**

```
TS=("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")
```

### `#3` — 🟥 Práticas do processo de ensino-aprendizagem

```
TS=("practice" OR "educational practice" OR "pedagogical practice" OR "teaching practice" OR "instructional practice" OR "teaching strategy" OR "instructional strategy" OR "teaching method" OR "instructional method" OR "teaching technique" OR "learning activity" OR "learning task" OR "educational intervention" OR "instructional intervention" OR "teaching sequence" OR "instructional sequence" OR "pedagogy" OR "pedagogies" OR "best practices" OR "recommended practices" OR "pedagogical approach" OR "instructional approach" OR "instructional design" OR "learning design" OR "pedagogical pattern" OR "pedagogical design pattern" OR "active learning method" OR "teaching methodology" OR "prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boas práticas" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino" OR "práctica" OR "prácticas educativas" OR "práctica educativa" OR "práctica pedagógica" OR "práctica docente" OR "estrategia de enseñanza" OR "estrategia didáctica" OR "método de enseñanza" OR "método instruccional" OR "técnica de enseñanza" OR "actividad de aprendizaje" OR "tarea de aprendizaje" OR "intervención educativa" OR "intervención pedagógica" OR "secuencia didáctica" OR "secuencia instruccional" OR "pedagogía" OR "pedagogías" OR "buenas prácticas" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoque instruccional" OR "diseño instruccional" OR "diseño del aprendizaje" OR "diseño didáctico" OR "patrón pedagógico" OR "patrón de diseño pedagógico" OR "método de aprendizaje activo" OR "metodología de enseñanza")
```

### `#4` — 🟧 Fatores situacionais

```
TS=("situational factors" OR "situational factor" OR "situation of use" OR "application context" OR "context of use" OR "educational context" OR "learning context" OR "contextual factors" OR "context factors" OR "application conditions" OR "implementation conditions" OR "learning situation" OR "educational setting" OR "learning environment" OR "institutional context" OR "sociocultural context" OR "target population" OR "class profile" OR "learner characteristics" OR "educational level" OR "education modality" OR "educational institution" OR "educational infrastructure" OR "learning infrastructure" OR "available resources" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context-aware" OR "contextualization" OR "contextualisation" OR "fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem" OR "fatores contextuais" OR "fatores de contexto" OR "condições de aplicação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "ambiente de aprendizagem" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recursos disponíveis" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização" OR "factores situacionales" OR "factor situacional" OR "situación de uso" OR "contexto de aplicación" OR "contexto educativo" OR "contexto de aprendizaje" OR "factores contextuales" OR "factores del contexto" OR "condiciones de aplicación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "escenario educativo" OR "entorno de aprendizaje" OR "población destinataria" OR "perfil del grupo" OR "características de los estudiantes" OR "nivel educativo" OR "modalidad educativa" OR "institución educativa" OR "infraestructura educativa" OR "recursos disponibles" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "sensible al contexto" OR "contextualización")
```

---

## 4. As quatro expressões de busca

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

> **EXECUÇÃO ÚNICA (emenda de 06/11/2026).** Todas as expressões começam por strings 1 + 2 e apenas acrescentam facetas: **E1, E2 e E3 são subconjuntos estritos de E4**, a de cobertura, e a união das quatro é exatamente E4. Executá-las separadamente não acrescenta um único registro ao portfólio. Nesta base executa-se **apenas E4**, com exportação única; a pertinência de cada registro a E1, E2 e E3 é calculada localmente pelo script `derivar_expressoes.py` sobre os arquivos exportados, e as contagens do IO 2 são **derivadas**, não reconsultadas. As formas expandidas de E1 a E3 permanecem registradas abaixo porque definem o que cada subconjunto significa — não para serem executadas.

> **Exceção obrigatória — teste de fidelidade.** Antes de aceitar qualquer contagem derivada, executar **E2 e E3 diretamente nesta base** e comparar com o conjunto derivado. Divergência superior a 10% reprova o método de derivação e obriga a voltar às execuções separadas, com registro de emenda. A divergência esperada é pequena e decorre de `Keywords Plus` e da lematização, que o casamento local reproduz por aproximação.

Duas formas são oferecidas para cada expressão: a **forma por conjuntos**, para uso no histórico de busca da interface, e a **forma expandida**, autocontida, para colar em uma única consulta e para registro no IO 2.

> **Advertência sobre a forma por conjuntos.** A combinação de referências de conjunto (`#5 AND #3`) com uma *tag* de campo (`AND PY=(...)`) na mesma linha **não** foi confirmada na documentação consultada. Na primeira execução, testar a forma por conjuntos na expressão de cobertura e comparar o número de retornos com o da forma expandida: se divergirem, ou se a interface recusar a linha, **usar exclusivamente a forma expandida** e registrar a decisão no IO 2.

### `#5` — as duas âncoras em proximidade

**Decisão D6, opção 1: `NEAR/5` e `DT=` aplicam-se às QUATRO expressões.** A forma anterior punha proximidade e filtro de tipo só em E4, e isso quebrava a continência — E2 devolveu 2.515 contra 1.596 de E4, o que a arquitetura não permite. Uniformizadas, as quatro voltam a satisfazer `E1 ⊂ E2 ⊂ E4` **por construção**: cada uma é `#5` com zero, uma ou duas facetas temáticas a mais, e acrescentar conjunção só reduz.

Definir este conjunto **uma vez** e reusá-lo nas quatro. É o par de âncoras com proximidade de cinco palavras, que exclui o registro em que artefato e domínio aparecem sem relação entre si.

```
TS=(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") NEAR/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa"))
```

> **Se a interface recusar a proximidade entre grupos entre parênteses** — a documentação da Clarivate exemplifica `NEAR/x` entre termos simples —, usar a redução a um termo de cada lado e somar as execuções por deduplicação:

```
TS=(ontolog* NEAR/5 educat*)
TS=("knowledge graph*" NEAR/5 educat*)
TS=("conceptual model*" NEAR/5 educat*)
TS=("knowledge organization*" NEAR/5 educat*)
```

### E1 (geral) — todas as strings montadas. **“Geral” é a composição, não o alcance**: por exigir as quatro facetas simultaneamente, é a MAIS RESTRITIVA das quatro

*DERIVADA localmente — não executar.*

**Facetas:** 🟦 AND 🟨 AND 🟥 AND 🟧 &nbsp;·&nbsp; **conjuntos:** #5 AND #3 AND #4

*Forma por conjuntos:*

```
#5 AND #3 AND #4 AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

*Forma expandida:*

```
TS=(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") NEAR/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")) AND TS=("practice" OR "educational practice" OR "pedagogical practice" OR "teaching practice" OR "instructional practice" OR "teaching strategy" OR "instructional strategy" OR "teaching method" OR "instructional method" OR "teaching technique" OR "learning activity" OR "learning task" OR "educational intervention" OR "instructional intervention" OR "teaching sequence" OR "instructional sequence" OR "pedagogy" OR "pedagogies" OR "best practices" OR "recommended practices" OR "pedagogical approach" OR "instructional approach" OR "instructional design" OR "learning design" OR "pedagogical pattern" OR "pedagogical design pattern" OR "active learning method" OR "teaching methodology" OR "prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boas práticas" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino" OR "práctica" OR "prácticas educativas" OR "práctica educativa" OR "práctica pedagógica" OR "práctica docente" OR "estrategia de enseñanza" OR "estrategia didáctica" OR "método de enseñanza" OR "método instruccional" OR "técnica de enseñanza" OR "actividad de aprendizaje" OR "tarea de aprendizaje" OR "intervención educativa" OR "intervención pedagógica" OR "secuencia didáctica" OR "secuencia instruccional" OR "pedagogía" OR "pedagogías" OR "buenas prácticas" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoque instruccional" OR "diseño instruccional" OR "diseño del aprendizaje" OR "diseño didáctico" OR "patrón pedagógico" OR "patrón de diseño pedagógico" OR "método de aprendizaje activo" OR "metodología de enseñanza") AND TS=("situational factors" OR "situational factor" OR "situation of use" OR "application context" OR "context of use" OR "educational context" OR "learning context" OR "contextual factors" OR "context factors" OR "application conditions" OR "implementation conditions" OR "learning situation" OR "educational setting" OR "learning environment" OR "institutional context" OR "sociocultural context" OR "target population" OR "class profile" OR "learner characteristics" OR "educational level" OR "education modality" OR "educational institution" OR "educational infrastructure" OR "learning infrastructure" OR "available resources" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context-aware" OR "contextualization" OR "contextualisation" OR "fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem" OR "fatores contextuais" OR "fatores de contexto" OR "condições de aplicação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "ambiente de aprendizagem" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recursos disponíveis" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização" OR "factores situacionales" OR "factor situacional" OR "situación de uso" OR "contexto de aplicación" OR "contexto educativo" OR "contexto de aprendizaje" OR "factores contextuales" OR "factores del contexto" OR "condiciones de aplicación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "escenario educativo" OR "entorno de aprendizaje" OR "población destinataria" OR "perfil del grupo" OR "características de los estudiantes" OR "nivel educativo" OR "modalidad educativa" OR "institución educativa" OR "infraestructura educativa" OR "recursos disponibles" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "sensible al contexto" OR "contextualización") AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### E2 (específica) — modelos e ontologias que representam práticas do processo de ensino-aprendizagem

*DERIVADA localmente — executar apenas no teste de fidelidade.*

**Facetas:** 🟦 AND 🟨 AND 🟥 &nbsp;·&nbsp; **conjuntos:** #5 AND #3

*Forma por conjuntos:*

```
#5 AND #3 AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

*Forma expandida:*

```
TS=(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") NEAR/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")) AND TS=("practice" OR "educational practice" OR "pedagogical practice" OR "teaching practice" OR "instructional practice" OR "teaching strategy" OR "instructional strategy" OR "teaching method" OR "instructional method" OR "teaching technique" OR "learning activity" OR "learning task" OR "educational intervention" OR "instructional intervention" OR "teaching sequence" OR "instructional sequence" OR "pedagogy" OR "pedagogies" OR "best practices" OR "recommended practices" OR "pedagogical approach" OR "instructional approach" OR "instructional design" OR "learning design" OR "pedagogical pattern" OR "pedagogical design pattern" OR "active learning method" OR "teaching methodology" OR "prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boas práticas" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino" OR "práctica" OR "prácticas educativas" OR "práctica educativa" OR "práctica pedagógica" OR "práctica docente" OR "estrategia de enseñanza" OR "estrategia didáctica" OR "método de enseñanza" OR "método instruccional" OR "técnica de enseñanza" OR "actividad de aprendizaje" OR "tarea de aprendizaje" OR "intervención educativa" OR "intervención pedagógica" OR "secuencia didáctica" OR "secuencia instruccional" OR "pedagogía" OR "pedagogías" OR "buenas prácticas" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoque instruccional" OR "diseño instruccional" OR "diseño del aprendizaje" OR "diseño didáctico" OR "patrón pedagógico" OR "patrón de diseño pedagógico" OR "método de aprendizaje activo" OR "metodología de enseñanza") AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### E3 (específica) — artefatos que formalizam os fatores situacionais do domínio educacional

*DERIVADA localmente — executar apenas no teste de fidelidade.*

**Facetas:** 🟦 AND 🟨 AND 🟧 &nbsp;·&nbsp; **conjuntos:** #5 AND #4

*Forma por conjuntos:*

```
#5 AND #4 AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

*Forma expandida:*

```
TS=(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") NEAR/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")) AND TS=("situational factors" OR "situational factor" OR "situation of use" OR "application context" OR "context of use" OR "educational context" OR "learning context" OR "contextual factors" OR "context factors" OR "application conditions" OR "implementation conditions" OR "learning situation" OR "educational setting" OR "learning environment" OR "institutional context" OR "sociocultural context" OR "target population" OR "class profile" OR "learner characteristics" OR "educational level" OR "education modality" OR "educational institution" OR "educational infrastructure" OR "learning infrastructure" OR "available resources" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context-aware" OR "contextualization" OR "contextualisation" OR "fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem" OR "fatores contextuais" OR "fatores de contexto" OR "condições de aplicação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "ambiente de aprendizagem" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recursos disponíveis" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização" OR "factores situacionales" OR "factor situacional" OR "situación de uso" OR "contexto de aplicación" OR "contexto educativo" OR "contexto de aprendizaje" OR "factores contextuales" OR "factores del contexto" OR "condiciones de aplicación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "escenario educativo" OR "entorno de aprendizaje" OR "población destinataria" OR "perfil del grupo" OR "características de los estudiantes" OR "nivel educativo" OR "modalidad educativa" OR "institución educativa" OR "infraestructura educativa" OR "recursos disponibles" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "sensible al contexto" OR "contextualización") AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### E4 (de cobertura) — artefatos de representação do conhecimento no domínio educacional, inclusive quando não mencionam as demais facetas nos metadados

*EXECUTADA e EXPORTADA nesta base.*

**Facetas:** 🟦 AND 🟨 &nbsp;·&nbsp; **conjuntos:** #5

*Forma por conjuntos:*

```
#5 AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

*Forma expandida:*

```
TS=(("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") NEAR/5 ("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa")) AND PY=(2017-2026) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

**Forma ampla, por conjunção — NÃO é a forma executada.** Fica registrada porque define o limite superior do recorte e porque o seu retorno é dado de calibração: **10.357 registros em 06/11/2026**, contra **1.839** da forma com proximidade. **Os dois números são anteriores ao desdobramento morfológico e à ampliação de D3**, e servem de ordem de grandeza, não de linha de base.

```
TS=("knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "domain ontology" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "classification scheme" OR "metadata schema" OR "ontologies" OR "ontological" OR "domain ontologies" OR "faceted classification" OR "facet analysis" OR "faceted taxonomy" OR "conceptual model" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "domain model" OR "semantic model" OR "formal representation" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologia de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia" OR "esquema de classificação" OR "esquema de metadados" OR "ontologias" OR "ontológico" OR "ontológica" OR "ontológicos" OR "ontológicas" OR "ontologias de domínio" OR "taxonomias" OR "classificação facetada" OR "análise facetada" OR "análise de facetas" OR "modelo conceitual" OR "modelagem conceitual" OR "esquema conceitual" OR "modelo de domínio" OR "modelo semântico" OR "representação formal" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "esquema de clasificación" OR "esquema de metadatos" OR "ontologías" OR "ontologías de dominio" OR "clasificación facetada" OR "análisis facetado" OR "análisis de facetas" OR "modelo conceptual" OR "modelado conceptual" OR "esquema conceptual" OR "modelo de dominio" OR "modelo semántico" OR "representación formal" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") AND TS=("education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "curriculum" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "learner" OR "student" OR "teacher" OR "instructor" OR "educational institution" OR "educational level" OR "education modality" OR "educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "currículo" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "estudante" OR "aluno" OR "professor" OR "docente" OR "instituição de ensino" OR "nível de ensino" OR "modalidade de ensino" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educacionales" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz" OR "estudiante" OR "alumno" OR "institución educativa" OR "nivel educativo" OR "modalidad educativa") AND PY=(2017-2026)
```

> **Condição de adoção, e ela continua de pé.** A proximidade é estreitamento real de recall, não ajuste gratuito. Antes de aceitá-la como forma da busca, executar o teste de aderência: recuperação do conjunto-semente igual ou superior a 80%. Abaixo disso, volta-se à forma ampla — **e, por D6, a forma ampla também se aplica às quatro**, para que a continência se preserve nos dois cenários. Registrar as duas contagens no IO 2.

---

## 4.5 Execução — **APROVADA NA CONFERÊNCIA DE COERÊNCIA**

| Expressão | Composição | 1ª execução | **2ª execução** |
| :--- | :--- | ---: | ---: |
| **E1** | `#5 AND #3 AND #4` | 140 | **27** |
| **E2** | `#5 AND #3` | 2515 | **386** |
| **E3** | `#5 AND #4` | 643 | **149** |
| **E4** | `#5` — a de cobertura | 1596 | **1596** |

| Relação obrigatória | Verificação |
| :--- | :--- |
| E1 ⊆ E2 | passa — 27 ≤ 386 |
| E1 ⊆ E3 | passa — 27 ≤ 149 |
| E2 ⊆ E4 | passa — 386 ≤ 1596 |
| E3 ⊆ E4 | passa — 149 ≤ 1596 |

**É a primeira execução conforme ao protocolo em todo o pacote.** As quatro relações passam, e passam porque a forma nova as garante por construção — não por coincidência aritmética.

**E4 repetiu-se exatamente: 1596 nas duas execuções.** A forma de E4 não mudou com D6, e o número também não. Executada em momentos diferentes, com o mesmo texto, devolveu o mesmo conjunto — o que é, de passagem, a confirmação mais barata de que a base está estável e de que a consulta foi submetida como está escrita.

#### O que a uniformização custou, medido

| | 1ª execução | 2ª execução | Variação |
| :--- | ---: | ---: | ---: |
| E1 | 140 | 27 | -81% |
| E2 | 2515 | 386 | -85% |
| E3 | 643 | 149 | -77% |

**A proximidade faz quase todo o trabalho, e é preciso dizê-lo com clareza: isto é perda de recall assumida**, não ganho de precisão gratuito. E2 caiu 85%, E3 caiu 77%. O que saiu foram os registros em que artefato e domínio apareciam a mais de cinco palavras de distância — e a hipótese de que esses registros são ruído **é hipótese, não medida**. Quem a testa é o teste de aderência.

#### A estrutura do conjunto, que a forma nova torna exata

Com E1 = `#5 AND #3 AND #4`, E2 = `#5 AND #3` e E3 = `#5 AND #4`, segue que **E1 é exatamente a interseção de E2 e E3** — não um subconjunto qualquer. A união deixa de ser um intervalo e passa a ser um número:

| Partição de E4 | Registros | |
| :--- | ---: | ---: |
| E1 — as quatro facetas | 27 | 1,7% |
| só práticas, sem fatores situacionais | 359 | 22,5% |
| só fatores situacionais, sem práticas | 122 | 7,6% |
| só as âncoras, nenhuma das duas | 1088 | 68,2% |
| **E4** | **1596** | **100%** |

**27 registros reúnem as quatro facetas** — 1,7% do que a expressão de cobertura recupera. É o núcleo da questão de revisão, e é pequeno. Na BRAPCI o mesmo número foi zero. **Os dois achados apontam na mesma direção** e, somados, passam a ser evidência da lacuna que a revisão investiga, não apenas um retorno de busca.

**359 registros tratam de prática sem fator situacional, contra 122 que tratam de fator situacional sem prática.** A literatura que representa a prática é cerca de **duas vezes e meia** maior que a que representa o seu condicionamento — e a BRAPCI mostrou a mesma assimetria, em escala menor. A leitura fica para a análise, mas o número é dado do protocolo.

#### O que vem agora, e é o teste que decide a forma da busca

A ficha condiciona a adoção da proximidade ao **teste de aderência: 80% do conjunto-semente**. Esta base espera **quatro sementes** — as de números 2, 7, 9 e 10 —, e a de número 10 é comunicação em anais da ISKO, que a *Core Collection* só indexa se a assinatura incluir o *Conference Proceedings Citation Index*. Não indexada, sai do denominador e a aderência mede-se sobre três.

| Resultado do teste | O que se faz |
| :--- | :--- |
| **4 de 4, ou 3 de 3** | a proximidade está validada e E4 é a expressão desta base. Exportar e seguir |
| **3 de 4** | 75%, abaixo do limiar. **Volta-se à forma ampla**, nas quatro, e o prazo resolve-se pela ordem de leitura e não pela expressão |
| **2 ou menos** | a perda não é de forma, é de vocabulário: a faceta a revisar aparece no exame de qual semente falhou e por qual âncora |

> **Até o teste correr, os 1596 não são portfólio: são candidatos.** O que já está firme é a conferência de coerência, e ela só diz que as quatro expressões são o que dizem ser. Se são as expressões certas, quem responde é o conjunto-semente.

---

## 4.6 Exportação de E4 e teste de aderência

#### A exportação

| | |
| :--- | ---: |
| Registros exportados, em dois arquivos RIS | 1596 |
| Distintos por identificador, DOI ou título | **1594** |
| Colisões de título a resolver à mão na deduplicação | 4 |
| Fora do recorte de 2017 a 2026 | **0** |

**A exportação confere com o retorno da interface**, e o recorte temporal confirma-se por dentro: nenhum registro fora da janela. **Quatro títulos aparecem duas vezes**, e a chave automática só resolve dois — nos outros dois, um registro traz DOI e o outro não, ou os dois trazem DOIs diferentes com páginas diferentes. **São casos para a deduplicação do 1º passo resolver à mão**, e ficam aqui nomeados para que não passem por descuido.

| Tipo | Registros | | Ano | Registros |
| :--- | ---: | :--- | :---: | ---: |
| JOUR | 1179 | | 2017 | 154 |
| CPAPER | 384 | | 2018 | 158 |
| CHAP | 16 | | 2019 | 174 |
| BOOK | 15 | | 2020 | 113 |
| | | | 2021 | 167 |
| | | | 2022 | 136 |
| | | | 2023 | 158 |
| | | | 2024 | 153 |
| | | | 2025 | 164 |
| | | | 2026 | 217 |

**384 trabalhos em anais na exportação — a assinatura cobre anais.** É medição que a ficha precisava e não tinha: a ressalva de cobertura desta base supunha que o *Conference Proceedings Citation Index* pudesse estar fora da assinatura, e agora se sabe que não está.

#### O teste

Esta base espera **quatro sementes**. Três foram recuperadas, **todas por DOI**, que é o casamento mais forte disponível:

| Semente | Resultado | Casamento |
| :---: | :--- | :--- |
| 2 — Das, Naskar & Roy | **encontrada** | DOI |
| 7 — Chimalakonda & Nori | **encontrada** | DOI |
| 9 — Piriyapongpipat, Goldin & Dit. | **encontrada** | DOI |
| 10 — Khoo & Kan | **ausente** | — |

> **O veredito depende de uma pergunta ainda sem resposta, e por isso fica SUSPENSO.** Se a semente 10 estiver indexada nesta base, a aderência é **3 de 4 = 75%**, abaixo do limiar de 80%, e **a proximidade cai**. Se não estiver indexada, sai do denominador, a aderência é **3 de 3 = 100%** e a proximidade está validada. **Uma consulta decide**: procurar o título `An ontology for conceptual analysis of signature pedagogies` nesta base, sem filtro algum.

**O que já se sabe, e aperta a hipótese.** O volume da semente 10 — *Knowledge Organization at the Interface*, anais do 16º Congresso da ISKO, 2020 — **tem um registro nesta exportação**, que é outro trabalho do mesmo volume. Logo a base indexa **ao menos parte** daquele volume. Isso não prova que indexe o trabalho de Khoo & Kan: a indexação de anais é seletiva por trabalho, não só por volume.

**E há uma razão para a falha que o título explica sozinho.** Confrontados os três títulos recuperados e o ausente com as facetas:

| Semente | Faceta 🟦 no título | Faceta 🟨 no título |
| :---: | :--- | :--- |
| 2 | `ontological` | `educational` |
| 9 | `ontology` | `curriculum` |
| 10 | `ontology` | **nenhuma** |

**A semente 10 não traz termo algum da faceta de domínio no título** — traz `pedagogies`, que é da faceta de práticas. Para passar em `#5`, precisaria de um termo de domínio a menos de cinco palavras de um termo de artefato no resumo ou nas palavras-chave. **É exatamente o caso que a proximidade exclui**, e é por isso que esta semente é a que decide a forma da busca nesta base: ela mede o que a restrição custa, em lugar de confirmar o que a restrição preserva.

| Se a consulta mostrar | Então | E se faz |
| :--- | :--- | :--- |
| a semente 10 **não está** na base | aderência 3 de 3 = 100% | a proximidade está validada; E4 é a expressão desta base e os 1.594 registros são o portfólio preliminar |
| a semente 10 **está** na base | aderência 3 de 4 = 75% | **volta-se à forma ampla**, nas quatro expressões, por D6; reexecutar e reexportar |

> **Não se contorna isto reduzindo o denominador por conveniência.** A ressalva de cobertura permite tirar do denominador a semente que a base **não indexa** — é cobertura, não falha da busca. Não permite tirar a que a base indexa e a busca não alcança: essa é falha da busca, e é o que o teste existe para medir.

---

## 5. Variantes previstas

### 5.1 Fracionamento do intervalo temporal

A documentação da Clarivate recomenda intervalos de `PY=` de até cinco anos. Se a execução de 2017–2026 em bloco falhar ou truncar o retorno, repetir cada expressão três vezes, substituindo o trecho final por:

```
AND PY=(2017-2020)
AND PY=(2017-2021)
AND PY=(2022-2026)
```

Somar os retornos no IO 2 e deduplicar no Zotero. Registrar o fracionamento como adaptação.

### 5.2 Acréscimo de idioma e tipo documental

Anexar ao final de qualquer expressão, **após conferir os valores na lista suspensa da interface**:

```
AND LA=(English OR Portuguese OR Spanish)
AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

Se um valor for recusado pela interface, suprimir a cláusula e aplicar o mesmo limite por refinamento, anotando a troca no IO 2.

### 5.3 Truncamento

O truncamento previsto no 3º passo (`ontolog*`, `taxonom*`, `educat*`, `learn*`, `teach*`, `personaliz*`, `prioriti*`, `weight*`, `contextualiz*`, `instantiat*`) **não** foi aplicado nas strings acima: na Web of Science o curinga desativa a lematização, de modo que `learn*` deixa de recuperar formas que `learning` recuperaria por lematização. A decisão é executar primeiro as strings sem curinga e, no teste de aderência, medir se o curinga aumenta o *recall* do conjunto-semente. Registrar o resultado do teste antes de alterar as strings.

### 5.4 Camada de precisão — resposta ao retorno de mais de 36.000 registros

A primeira execução da expressão de cobertura nesta base retornou mais de 36.000 registros. O diagnóstico apontou o cruzamento de `ontology` com `learning`, que recupera a subárea de *ontology learning* — tarefa de processamento de linguagem natural, sem relação com o domínio educacional — além de todo artigo de aprendizado de máquina que mencione uma ontologia. As strings da seção 3 já incorporam a qualificação desses termos. Se ainda assim o retorno for alto, aplicar as camadas abaixo **nesta ordem**, medindo a cada passo.

**Camada 1 — proximidade entre as âncoras.** JÁ INCORPORADA, e por D6 **nas quatro expressões**, pelo conjunto `#5` da seção 4 — antes estava só em E4, que é o que quebrava a continência. Mantida aqui a referência do operador: `NEAR/x`, que assume 15 palavras quando o número é omitido (documentação da Clarivate).

```
TS=((ontolog* OR "knowledge graph*" OR "knowledge organization*" OR "conceptual model*" OR thesaur* OR "controlled vocabular*" OR "metadata schema*" OR "classification scheme*") NEAR/5 (educat* OR teaching OR "teaching-learning" OR learner* OR student* OR curricul* OR pedagog*)) AND PY=(2017-2026)
```

A proximidade força as duas ideias à mesma vizinhança do texto, em vez de aceitá-las em pontos quaisquer do registro. **A confirmar na primeira execução:** a documentação exemplifica `NEAR/x` entre termos simples (`salmon NEAR/15 virus`), não entre grupos parentetizados. Se a interface recusar a forma acima, reduzir a um termo de cada lado (`TS=(ontolog* NEAR/5 educat*)`) e somar execuções.

**Camada 2 — restrição de campo.** `TS=` cobre título, resumo, palavras-chave de autor e *Keywords Plus*; este último é gerado automaticamente e é fonte relevante de ruído. Manter a faceta 🟦 em `TS=` e passar a faceta 🟨 para `AK=` (palavras-chave de autor) ou `TI=`:

```
TS=(<faceta 1>) AND AK=(<faceta 2>) AND PY=(2017-2026)
```

**Camada 3 — refinamento por categoria.** Último recurso, por ser o que mais arrisca perder trabalho interdisciplinar:

```
AND WC=("Education & Educational Research" OR "Education, Scientific Disciplines" OR "Information Science & Library Science" OR "Computer Science, Artificial Intelligence" OR "Computer Science, Information Systems" OR "Computer Science, Interdisciplinary Applications" OR "Computer Science, Theory & Methods")
```

Conferir os rótulos exatos das categorias na lista da própria interface antes de usar. Aplicada esta camada, declarar a restrição no relatório e compensá-la pelo backward search de uma geração.

**Regra de decisão.** Nenhuma camada é adotada por reduzir o número: cada uma é medida contra o conjunto-semente, e recuperação inferior a 80% a reprova e obriga a registrar emenda. Reduzir de 36.000 para 3.000 sem essa medida é adivinhação. Registrar no IO 2 a contagem de cada tentativa, inclusive a de 36.000, que é resultado de calibração e não erro. **Não** reduzir o retorno acrescentando facetas a E4: E4 é a expressão de cobertura, e é ela que garante recuperar ontologias educacionais silenciosas quanto a contexto, ponderação ou instanciação.

---

## 6. Conjunto-semente — o que esta base deve recuperar

O conjunto-semente tem **10 estudos**, todos conferidos em fonte e todos dentro do escopo. Pela indicação do ReT, **4 são esperados nesta base**. Instrumento completo, procedimento e estado de conferência de cada referência: `data/saida/semente/Conjunto_Semente.md`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| 2 | Das et al. (2022) | `10.5771/0943-7444-2022-1-6` | — |
| 7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| 9 | Piriyapongpipat et al. (2024) | `10.1186/s40561-024-00307-8` | — |
| 10 | Khoo & Kan (2020) | `10.5771/9783956507762` | **caso-teste de cobertura de campo** |

**Procedimento, em duas etapas, e não confundir as duas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões da revisão, para saber se a base indexa a semente. Semente não indexada **sai do denominador desta base**, e isso se registra como cobertura da base, não como falha da busca. *Etapa 2:* procurar a semente na exportação de E4 já feita, por DOI e depois por título — **sem reexecutar a busca**, porque o teste se faz sobre o que a execução de fato devolveu.

**Limiar de 80%, e o que a reprovação obriga.** O IO 1 fixa o limiar e manda, abaixo dele, revisar o controle terminológico antes de prosseguir, com emenda registrada. O número que decide é o **global**, sobre a união das bases: perder uma semente aqui e achá-la em outra não é perda de portfólio. A aderência por base serve para diagnosticar **qual** base e **qual** faceta falharam.

**Lematização nesta base:** **presumida para o inglês, não medida.** A Clarivate documenta lematização de plural regular em `TS=`; não há documentação equivalente para português e espanhol, e nada foi medido nesta revisão. Importa porque o desdobramento morfológico de 08/11/2026 acrescentou plurais e formas adjetivais às facetas: onde a base lematiza, o plural é redundante; onde não lematiza, era perda silenciosa. A **derivação adjetival** é outro caso: `ontological` não é flexão de `ontology`, e **base alguma a alcança** a partir do substantivo. Foi por isso que entrou no vocabulário — duas sementes do conjunto falhavam a âncora de artefato só por causa dela.

**Caso-teste de cobertura de campo nesta base.** Em semente 10, o **domínio** está fora do título — o que lá aparece é `pedagogies`, que é prática e não domínio, e E4 não lê a faceta de práticas. A recuperação depende, portanto, do resumo e das palavras-chave. **Se E4 recuperar, recuperou por campo que não é o título, e isso é evidência medida de que a cobertura de campo desta base basta; se não recuperar, a perda deixa de ser estimada e passa a ser medida.** Anotar o resultado por extenso no registro de execução.

**Ressalva de cobertura, a conferir na etapa 1.** A semente 10 (Khoo & Kan) é comunicação em anais da ISKO, publicada pela Ergon Verlag. A Web of Science só a indexa se a assinatura institucional incluir o *Conference Proceedings Citation Index*; a Core Collection sozinha não cobre anais. Retorno vazio na etapa 1 significa **não indexada nesta assinatura** e tira a semente do denominador desta base — não é falha da expressão. Registrar qual índice a assinatura cobre, porque isso condiciona o denominador e precisa constar no relato.

**Vantagem desta base no teste, e é por isso que ela o sustenta.** `TS=` alcança título, resumo, palavras-chave de autor e *Keywords Plus*. As duas falhas de cobertura de campo que o ensaio seco detectou — artefato ou domínio fora do título — **não deveriam custar semente alguma aqui**. Se custarem, o problema não é de campo e sim de vocabulário, e o diagnóstico passa a ser outro: faceta a revisar, não campo a ampliar.

---


## 7. Registro de execução (alimenta o IO 2)

| Execução | Data | Campos | Filtros aplicados na interface | Retornos | Observações |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **E4 — execução única (cobertura)** | | TS (tópico) | | | exportação completa |
| E2 — teste de fidelidade | | TS (tópico) | | | só para conferência |
| E3 — teste de fidelidade | | TS (tópico) | | | só para conferência |
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

3. **`LA=`.** A *tag* de idioma foi confirmada em material de treinamento da FECYT (out. 2024), não na página de *field tags* da Clarivate. Antes de usá-la, executar uma consulta mínima (`TS=ontology AND LA=Portuguese`) e verificar se a interface a aceita; se recusar, usar o refinamento por idioma.

4. **Texto completo.** A Core Collection é base referencial: a disponibilidade do texto completo depende do acesso institucional e não constitui filtro de busca. O critério de elegibilidade correspondente opera na 2ª filtragem.

5. **Teses e dissertações.** Não são cobertas por esta base. A lacuna é coberta pela BRAPCI e, se necessário, pela BDTD, registrada como ampliação do 5º passo.

