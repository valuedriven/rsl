# Strings de busca — Scopus

## 1. Estado de verificação da sintaxe

| Elemento | Situação | Fonte |
| :--- | :--- | :--- |
| `TITLE-ABS-KEY()` | Verificado | Elsevier, *Scopus Search API — search tips* |
| `PUBYEAR >`, `<`, `=` | Verificado | idem |
| `LANGUAGE()` | Verificado | idem |
| `DOCTYPE()` com os códigos `ar`, `re`, `cp`, `ch`, `bk`, `ed`, `le`, `no`, `sh` | Verificados | idem |
| `SRCTYPE()` com `j`, `b`, `k`, `p`, `r`, `d` | Verificado | idem |
| `OPENACCESS(0` ou `1)` | Verificado | idem |
| `AND`, `OR`, `AND NOT`; precedência `OR` → `AND` → `AND NOT` | Verificado; a precedência muda em 2026 | idem |
| Truncamento `*` e `?`, mínimo de 3 caracteres antes do curinga | Verificado | idem |
| Proximidade `W/n` e `PRE/n` | Verificados; `W/5` **medido** entre termos simples e entre grupos pequenos de frases | idem e `data/registro_execucao.json` (BD2) |
| `W/5` entre os grupos inteiros de `#5` | **Não medido** | medir na primeira execução; recusa leva à variante "Redução por recusa da interface" |
| `{}` frase exata *versus* `""` frase aproximada | Verificado | idem |
| Limite de operadores por consulta | **Não documentado** | — |
| Combinação de consultas do histórico (`#n`) com filtros na mesma linha | **Não verificada** | ver "Como executar" |
| Lematização do plural | **Não verificada** | — |
| Tratamento de diacríticos | **Não verificado** | as strings trazem as duas grafias |
| Teto de retorno exibido e de exportação por lote | **Não verificados** | conferir na interface antes de exportar |

Todas as facetas vão entre parênteses explícitos; nenhuma expressão depende da ordem implícita de avaliação.

---

## 2. Critérios de elegibilidade

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — 2017 até a data de execução | CE1 / CE2 | **Sim** | `AND PUBYEAR > 2016 AND PUBYEAR < 2027` |
| Idiomas — português, inglês e espanhol | CE3 | **Sim** | `AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish))` |
| Tipo documental | CE4 | **Sim** | `AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))` |
| Disponibilidade de texto completo | CE5 | **Não** | 2ª filtragem; `OPENACCESS(1)` só como contingência |
| Adequação temática | CE6 | **Não** | filtragens do Módulo 3, Etapa 3 |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, por âncora | faceta 🟨 (FCT2) nas cinco expressões |
| Outros tipos documentais | CE9 | **Não** | 2ª filtragem |

---

## 3. Strings por faceta

`STRn` é o identificador do protocolo e `#n` o conjunto correspondente. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

### Declaração de cobertura

Lida por `src/protocolo.py`.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: pt, en, es; FCT2: pt, en, es; FCT3: pt, en, es; FCT4: pt, en, es |
| camadas | todas |
| derivações | morfologia |

### `STR1` — conjunto `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
TITLE-ABS-KEY("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologias" OR "ontologia de domínio" OR "ontologias de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia facetada" OR "esquema de classificação" OR "esquema de metadados" OR "classificação facetada" OR "ontologia facetada" OR "ontologia educacional" OR "ontologia de aprendizagem" OR "ontologia de ensino" OR "modelo ontológico educacional" OR "ontologia de prática educacional" OR "ontologia de design instrucional" OR "ontologia de currículo" OR "modelo de domínio" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representação do conhecimento baseada em ontologias" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "ontologies" OR "domain ontology" OR "domain ontologies" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "faceted taxonomy" OR "classification scheme" OR "metadata schema" OR "faceted classification" OR "faceted ontology" OR "educational ontology" OR "learning ontology" OR "teaching ontology" OR "educational ontological model" OR "educational practice ontology" OR "instructional design ontology" OR "curriculum ontology" OR "domain model" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "taxonomía facetada" OR "esquema de clasificación" OR "esquema de metadatos" OR "clasificación facetada" OR "ontología facetada" OR "ontología educativa" OR "ontología de aprendizaje" OR "ontología de enseñanza" OR "modelo ontológico educativo" OR "ontología de práctica educativa" OR "ontología de diseño instruccional" OR "ontología de currículo" OR "modelo de dominio" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías")
```

### `STR2` — conjunto `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

```
TITLE-ABS-KEY("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz")
```

### `STR3` — conjunto `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
TITLE-ABS-KEY("prática" OR "prática educacional" OR "práticas educacionais" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boa prática" OR "boas práticas" OR "prática recomendada" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino" OR "practice" OR "educational practice" OR "pedagogical practice" OR "teaching practice" OR "instructional practice" OR "teaching strategy" OR "instructional strategy" OR "teaching method" OR "instructional method" OR "teaching technique" OR "learning activity" OR "learning task" OR "educational intervention" OR "instructional intervention" OR "teaching sequence" OR "instructional sequence" OR "pedagogy" OR "pedagogies" OR "best practice" OR "best practices" OR "recommended practice" OR "recommended practices" OR "pedagogical approach" OR "instructional approach" OR "instructional design" OR "learning design" OR "pedagogical pattern" OR "pedagogical design pattern" OR "active learning method" OR "teaching methodology" OR "práctica" OR "práctica educativa" OR "prácticas educativas" OR "práctica pedagógica" OR "práctica docente" OR "estrategia de enseñanza" OR "estrategia didáctica" OR "método de enseñanza" OR "método instruccional" OR "técnica de enseñanza" OR "actividad de aprendizaje" OR "tarea de aprendizaje" OR "intervención educativa" OR "intervención pedagógica" OR "secuencia didáctica" OR "secuencia instruccional" OR "pedagogía" OR "buena práctica" OR "buenas prácticas" OR "práctica recomendada" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoque instruccional" OR "diseño instruccional" OR "diseño del aprendizaje" OR "diseño didáctico" OR "patrón pedagógico" OR "patrón de diseño pedagógico" OR "método de aprendizaje activo" OR "metodología de enseñanza")
```

### `STR4` — conjunto `#4` — 🟧 FCT4 — Fatores situacionais

```
TITLE-ABS-KEY("fator situacional" OR "fatores situacionais" OR "situação de uso educacional" OR "contexto educacional" OR "contexto de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator de contexto" OR "fatores de contexto" OR "condição de aplicação" OR "condições de aplicação" OR "condição de implementação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "característica do aluno" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recurso disponível" OR "recursos disponíveis" OR "restrição contextual" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização" OR "situational factor" OR "situational factors" OR "situation of use" OR "educational context" OR "learning context" OR "contextual factor" OR "contextual factors" OR "context factor" OR "context factors" OR "application condition" OR "application conditions" OR "implementation condition" OR "implementation conditions" OR "learning situation" OR "educational setting" OR "institutional context" OR "sociocultural context" OR "target population" OR "class profile" OR "learner characteristic" OR "learner characteristics" OR "educational level" OR "education modality" OR "educational institution" OR "educational infrastructure" OR "learning infrastructure" OR "available resource" OR "available resources" OR "contextual constraint" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context-aware" OR "contextualization" OR "contextualisation" OR "factor situacional" OR "factores situacionales" OR "situación de uso" OR "contexto educativo" OR "contexto de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor del contexto" OR "factores del contexto" OR "condición de aplicación" OR "condiciones de aplicación" OR "condición de implementación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "escenario educativo" OR "población destinataria" OR "perfil del grupo" OR "característica del estudiante" OR "características de los estudiantes" OR "nivel educativo" OR "modalidad educativa" OR "institución educativa" OR "infraestructura educativa" OR "recurso disponible" OR "recursos disponibles" OR "restricción contextual" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "sensible al contexto" OR "contextualización")
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

| Expressão | Execução |
| :--- | :--- |
| **EB4** | executar e exportar: é o corpus desta base |
| **EB5** | executar uma única vez, na mesma data; não compõe o corpus |
| **EB2**, **EB3** | executar só para o teste de fidelidade da derivação |
| **EB1** | não executar; derivação local |

- **Fidelidade:** divergência acima de **10%** entre EB2/EB3 executadas e derivadas reprova a derivação.
- **Sensibilidade:** fração elegível de `EB5 \ EB4` **< 5%** mantém EB4; **> 15%** leva à reconsideração, com emenda.
- **Retorno zero:** EB4 = 0 ou EB5 = 0 é defeito de execução até prova em contrário; contagem derivada próxima de zero exige execução direta antes do relato.

### `#5` — as duas âncoras em proximidade

Definir uma vez e reusar nas cinco expressões.

```
TITLE-ABS-KEY(("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologias" OR "ontologia de domínio" OR "ontologias de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia facetada" OR "esquema de classificação" OR "esquema de metadados" OR "classificação facetada" OR "ontologia facetada" OR "ontologia educacional" OR "ontologia de aprendizagem" OR "ontologia de ensino" OR "modelo ontológico educacional" OR "ontologia de prática educacional" OR "ontologia de design instrucional" OR "ontologia de currículo" OR "modelo de domínio" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representação do conhecimento baseada em ontologias" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "ontologies" OR "domain ontology" OR "domain ontologies" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "faceted taxonomy" OR "classification scheme" OR "metadata schema" OR "faceted classification" OR "faceted ontology" OR "educational ontology" OR "learning ontology" OR "teaching ontology" OR "educational ontological model" OR "educational practice ontology" OR "instructional design ontology" OR "curriculum ontology" OR "domain model" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "sistema de organización del conocimiento" OR "sistemas de organización del conocimiento" OR "ontología" OR "ontología de dominio" OR "ontología de aplicación" OR "ontología de alto nivel" OR "vocabulario controlado" OR "taxonomía facetada" OR "esquema de clasificación" OR "esquema de metadatos" OR "clasificación facetada" OR "ontología facetada" OR "ontología educativa" OR "ontología de aprendizaje" OR "ontología de enseñanza" OR "modelo ontológico educativo" OR "ontología de práctica educativa" OR "ontología de diseño instruccional" OR "ontología de currículo" OR "modelo de dominio" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "modelado basado en ontologías" OR "representación del conocimiento basada en ontologías") W/5 ("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "education" OR "educational" OR "teaching practice" OR "teaching method" OR "teaching strategy" OR "classroom teaching" OR "teaching-learning" OR "teaching and learning" OR "learning process" OR "learning environment" OR "learning design" OR "learning object" OR "learning analytics" OR "learning outcome" OR "learning path" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "teaching-learning process" OR "basic education" OR "primary education" OR "secondary education" OR "higher education" OR "vocational and technical education" OR "distance education" OR "online education" OR "digital education" OR "formal education" OR "non-formal education" OR "educational technology" OR "virtual learning environment" OR "open educational resource" OR "e-learning" OR "massive open online course" OR "educación" OR "proceso de enseñanza-aprendizaje" OR "método de enseñanza" OR "estrategia de enseñanza" OR "enseñanza superior" OR "entorno de aprendizaje" OR "objeto de aprendizaje" OR "situación de aprendizaje" OR "resultado de aprendizaje" OR "educación básica" OR "educación primaria" OR "educación secundaria" OR "educación superior" OR "educación profesional y técnica" OR "educación a distancia" OR "educación en línea" OR "educación digital" OR "educación formal" OR "educación no formal" OR "tecnología educativa" OR "entorno virtual de aprendizaje" OR "recurso educativo abierto" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "aprendiz"))
```

### EB1 (as quatro facetas)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧) · **conjuntos:** #5 AND #3 AND #4

```
#5 AND #3 AND #4 AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB2 (modelos e ontologias que representam práticas do processo de ensino-aprendizagem)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) · **conjuntos:** #5 AND #3

```
#5 AND #3 AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB3 (artefatos que formalizam os fatores situacionais do domínio educacional)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧) · **conjuntos:** #5 AND #4

```
#5 AND #4 AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB4 (de cobertura restrita — artefatos de representação no domínio educacional que mencionam prática ou fator situacional)

*Executada e exportada nesta base.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧)) · **conjuntos:** #5 AND (#3 OR #4)

```
#5 AND (#3 OR #4) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) · **conjuntos:** #5

```
#5 AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

Forma expandida: substituir `#5`, `#3` e `#4` pelos blocos desta ficha, num arquivo.

### Como executar

1. Conferir a sessão contra a seção 1, na primeira execução do dia.
2. Definir `#3`, `#4` e `#5` com os blocos desta ficha e submeter a forma por conjuntos de EB4. Se a interface recusar consulta do histórico combinada com filtros, submeter a forma expandida, montada em arquivo. Anotar no registro a forma aceita.
3. Submeter sempre a partir de arquivo, nunca recuperando o texto da interface.
4. Exportar em RIS, com todos os campos.
5. Conferir o retorno da exportação contra o da tela e o recorte temporal dentro do arquivo.
6. Registrar EB4 e EB5: `python3 src/derivar_expressoes.py --registrar scopus EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`; rodar `--derivar` e `--sensibilidade`.
7. Medir a aderência (seção 5). Semente esperada não recuperada: aplicar a anatomia da perda.
8. Na primeira execução, conferir se o retorno de EB4 tem a mesma ordem de grandeza do da Web of Science; discrepância indica problema de agrupamento.

### Variantes previstas

#### Forma ampla, sem proximidade

Disparo: a anatomia da perda atribui a perda à proximidade, ou a interface recusa `W/5` entre grupos deste tamanho. Forma: `#1 AND #2` no lugar de `#5`, nas cinco expressões. Adoção exige emenda.

#### Sem limite de tipo documental

Disparo: medir o efeito do critério CE4. Forma: EB4 sem a cláusula `DOCTYPE`; reportar a diferença de retorno.

#### Redução por recusa da interface

Disparo: expressão recusada por extensão. Forma: partir o grupo 🟨 de `#5` em duas metades — educação formal; tecnologia educacional e aprendizagem digital —, mantendo o resto idêntico, e unir por deduplicação. Registrar a partição como adaptação.

#### Acesso aberto — contingência

Disparo: obtenção de textos completos inviável na 2ª filtragem. Forma: anexar a cláusula abaixo e declarar o viés de acesso como limitação.

```
AND OPENACCESS(1)
```

#### Truncamento

Não usar curinga. Disparo: aderência abaixo de 80%. Forma: testar a consulta abaixo; a adoção exige emenda.

```
TITLE-ABS-KEY(ontolog* W/5 educat*)
```

#### Camada de precisão

Disparo: retorno alto demais para a triagem. Forma: restringir por `SUBJAREA`, com os códigos conferidos na documentação. Camada com aderência abaixo de 80% é reprovada.

---

## 5. Conjunto-semente

Esperadas nesta base, conforme o protocolo. Estado de conferência em `data/sementes.json`; aferição em `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE2 | Das et al. (2022) | `10.5771/0943-7444-2022-1-6` | — |
| SE3 | Chi et al. (2018) | `10.1111/exsy.12246` | — |
| SE4 | Shvets et al. (2024) | `10.5220/0012471400003645` | comunicação em anais |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE8 | Cenka et al. (2023) | `10.1080/10494820.2022.2039947` | — |
| SE9 | Piriyapongpipat et al. (2024) | `10.1186/s40561-024-00307-8` | — |

**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões; semente não indexada sai do denominador e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação de EB4 por DOI e depois por título, sem reexecutar a busca.

**Limiar de 80%**, sobre a união das bases. A aderência por base indica qual base e qual faceta falharam.

**Anatomia da perda.** Executar em ordem, com o DOI da semente; a primeira que devolver zero é a causa.

| # | Consulta | Se devolver zero |
| :---: | :--- | :--- |
| 1 | `DOI(<DOI>)` | a base não indexa o estudo: sai do denominador |
| 2 | `DOI(<DOI>) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))` | um filtro a exclui: identificar qual critério |
| 3 | `DOI(<DOI>) AND TITLE-ABS-KEY(🟦) AND TITLE-ABS-KEY(🟨)` | o vocabulário não a alcança: emenda de termo |
| 4 | `DOI(<DOI>) AND TITLE-ABS-KEY((🟦) W/5 (🟨))` | a proximidade a exclui: variante "Forma ampla" |

---

## 6. Ressalvas

1. Todos os termos são **termos livres**; não apresentá-los como descritores autorizados.
2. **`OPENACCESS(1)`** não é filtro de texto completo institucional.
