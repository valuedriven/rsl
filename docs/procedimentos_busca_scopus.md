# Strings de busca — Scopus

<!-- Gerado por `python3 -m rsl procedimentos gerar scopus --gravar` a partir de `docs/procedimentos/scopus`, do protocolo e do arquivo de sementes. Não editar: a edição à mão reprova em `documentos conferir`. -->

## 1. Estado de verificação da sintaxe

| Elemento | Categoria | Situação | Fonte | Sondagem |
| :--- | :--- | :--- | :--- | :--- |
| `TITLE-ABS-KEY()` | campos | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `PUBYEAR >`, `<`, `=` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `LANGUAGE()` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `DOCTYPE()` com os códigos `ar`, `re`, `cp`, `ch`, `bk`, `ed`, `le`, `no`, `sh` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `SRCTYPE()` com `j`, `b`, `k`, `p`, `r`, `d` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `OPENACCESS(0` ou `1)` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `AND`, `OR`, `AND NOT`; precedência `OR` → `AND` → `AND NOT` | operadores | Verificado em fonte oficial; a precedência muda em 2026 | Elsevier, *Scopus Search API — search tips* | — |
| Truncamento `*` e `?`, mínimo de 3 caracteres antes do curinga | truncamento | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| Proximidade `W/n` e `PRE/n` | proximidade | Verificado em fonte oficial; `W/5` **não medido** | Elsevier, *Scopus Search API — search tips* | — |
| `W/5` entre os grupos inteiros das duas âncoras | proximidade | **Não verificado**; recusa leva à variante "Redução por recusa da interface" | — | SD2 |
| `{}` frase exata *versus* `""` frase aproximada | frase | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `""` aproximada já inclui plurais e admite truncamento dentro dela; `{}` exata não admite truncamento | frase | **Não verificado**; afirmado sem fonte na skill `auditoria-das-strings` até 2026-11-23; conferir também na documentação oficial | — | SD3 |
| Limite de operadores por consulta | limite_consulta | **Não verificado**; não documentado | — | SD4 |
| Comprimento máximo da consulta | limite_consulta | **Não verificado**; a maior consulta executável é medida por `python3 -m rsl documentos conferir`, no relato do teto de caracteres | — | SD4 |
| Lematização do plural | lematizacao | **Não verificado** | — | SD3 |
| Tratamento de diacríticos | idioma_indexacao | **Não verificado**; as strings trazem as duas grafias | — | SD5 |
| Teto de retorno exibido | limite_retorno | **Não verificado**; conferir na interface antes de exportar | — | SD6 |
| Teto de exportação por lote | limite_exportacao | **Não verificado**; conferir na interface antes de exportar | — | SD7 |
| Parênteses para agrupamento | agrupamento | **Não verificado** | — | SD1 |
| Vocabulário controlado de assunto | vocabulario_controlado | **Não verificado** | — | sem sondagem: verificação documental: os termos de indexação da Scopus não foram conferidos; nenhuma expressão depende deles |
| Exportação em RIS com todos os campos | exportacao | **Não verificado** | — | SD7 |

Todas as facetas vão entre parênteses explícitos; nenhuma expressão depende da ordem implícita de avaliação.

### Sondagens a executar

Uma consulta por vez, sem nova tentativa automática; parar diante de captcha, aviso de atividade atípica ou bloqueio, e registrar.

#### SD1 — saber se os parênteses agrupam dentro de `TITLE-ABS-KEY()` como booleanos

**Elementos verificados:** Parênteses para agrupamento (Não verificado).

**Pré-requisitos.**

- busca avançada da Scopus aberta no navegador do pesquisador, com o acesso institucional dele

**Consulta 1 — controle**, em busca avançada.

```
TITLE-ABS-KEY(ontology OR taxonomy)
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: grupo entre parênteses com condição.

```
TITLE-ABS-KEY((ontology OR taxonomy) AND education)
```

**Consulta 3 — teste**, em busca avançada. Muda em relação ao controle: sem parênteses, pela precedência.

```
TITLE-ABS-KEY(ontology OR taxonomy AND education)
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno exibido

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < primeiro teste ≤ controle, e o segundo teste = primeiro teste (precedência `OR` antes de `AND`) | os parênteses agrupam; a precedência documentada se confirma | Verificado por medição |
| 2 | primeiro teste = 0, primeiro teste > controle, ou mensagem de erro | o agrupamento não se confirma; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD2 — saber se a interface aceita `W/5` entre os grupos inteiros das duas âncoras

**Elementos verificados:** `W/5` entre os grupos inteiros das duas âncoras (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com os parênteses verificados
- o procedimento gerado, para copiar as âncoras

**Consulta 1 — controle**, em busca avançada.

```
o bloco de EB5 no procedimento gerado, com `AND` no lugar de `W/5`
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: `W/5` entre os grupos inteiros.

```
o bloco de EB5 no procedimento gerado
```

**Passos.**

1. submeter o controle e anotar o retorno
2. submeter o teste e anotar o retorno e a mensagem, se houver

**Observar.**

- retorno exibido
- mensagem de erro ou de recusa, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste aceito, com 0 < teste ≤ controle | `W/5` entre os grupos inteiros funciona | Verificado por medição |
| 2 | teste recusado, = 0, ou > controle | `W/5` entre grupos não se confirma; levar ao pesquisador (variante "Forma ampla, sem proximidade") | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD3 — saber se a base casa singular e plural sem que a consulta os traga, entre aspas e entre chaves

**Elementos verificados:** Lematização do plural (Não verificado); `""` aproximada já inclui plurais e admite truncamento dentro dela; `{}` exata não admite truncamento (Não verificado).

**Pré-requisitos.**

- busca avançada da Scopus aberta no navegador do pesquisador

**Consulta 1 — controle**, em busca avançada.

```
TITLE-ABS-KEY("conceptual model")
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: o plural entre aspas.

```
TITLE-ABS-KEY("conceptual models")
```

**Consulta 3 — teste**, em busca avançada. Muda em relação ao controle: frase exata entre chaves.

```
TITLE-ABS-KEY({conceptual model})
```

**Consulta 4 — teste**, em busca avançada. Muda em relação ao controle: truncamento dentro das aspas.

```
TITLE-ABS-KEY("conceptual model*")
```

**Consulta 5 — teste**, em busca avançada. Muda em relação ao controle: truncamento dentro das chaves.

```
TITLE-ABS-KEY({conceptual model*})
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno e a mensagem, se houver
2. comparar também, com consultas análogas entre aspas, `ontologia`/`ontologias` e `ontología`/`ontologías`, e anotar os retornos

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | controle = plural entre aspas; chaves < controle; truncamento entre aspas ≥ controle; truncamento entre chaves recusado ou sem efeito | as aspas incluem plurais e admitem truncamento; as chaves são exatas e não o admitem | Verificado por medição |
| 2 | controle ≠ plural entre aspas, ou qualquer outra relação, ou pt e es diferentes do inglês | não se confirma o comportamento afirmado; levar ao pesquisador antes de declarar `pela lematização` | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD4 — saber se a interface aceita inteira a consulta de EB4

**Elementos verificados:** Comprimento máximo da consulta (Não verificado); Limite de operadores por consulta (Não verificado).
**Depende de:** SD2.

**Pré-requisitos.**

- SD2 registrada com `W/5` entre grupos verificado
- o procedimento gerado, para copiar a consulta

**Consulta 1 — teste**, em busca avançada.

```
o bloco de EB4 no procedimento gerado
```

**Passos.**

1. copiar o bloco de EB4 do procedimento e anotar o número de caracteres e de operadores
2. submetê-lo e anotar o retorno e a mensagem, se houver

**Observar.**

- retorno exibido
- mensagem de erro ou de recusa, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | aceita, com retorno > 0 | a interface aceita o comprimento e o número de operadores da consulta de EB4 | Verificado por medição |
| 2 | recusa por extensão ou por operadores, ou retorno = 0 | a consulta passa do limite; levar ao pesquisador (variante "Redução por recusa da interface") | Não verificado |

**Evidência a registrar.**

- captura da tela, com a consulta e o retorno visíveis

#### SD5 — saber se a base ignora diacríticos

**Elementos verificados:** Tratamento de diacríticos (Não verificado).

**Pré-requisitos.**

- busca avançada da Scopus aberta no navegador do pesquisador

**Consulta 1 — controle**, em busca avançada.

```
TITLE-ABS-KEY("educação")
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: sem diacrítico.

```
TITLE-ABS-KEY("educacao")
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno

**Observar.**

- retorno exibido de cada consulta

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste = controle > 0 | a base ignora diacríticos | Verificado por medição |
| 2 | teste ≠ controle, ambos > 0 | a base distingue diacríticos; as duas grafias são necessárias | Verificado por medição |
| 3 | controle = 0 | não se distingue o tratamento; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD6 — saber se a base exibe e deixa percorrer o retorno inteiro de uma busca larga

**Elementos verificados:** Teto de retorno exibido (Não verificado).

**Pré-requisitos.**

- busca avançada da Scopus aberta no navegador do pesquisador

**Consulta 1 — teste**, em busca avançada.

```
TITLE-ABS-KEY(education)
```

**Passos.**

1. submeter a consulta e anotar o retorno exibido
2. ir à última página de resultados pela navegação da interface, sem rastejar, e anotar a posição do último registro acessível

**Observar.**

- retorno exibido
- posição do último registro acessível
- aviso de limite, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | o último registro acessível tem a posição igual ao retorno exibido | não há teto de retorno exibido até esse tamanho | Verificado por medição |
| 2 | o último registro acessível tem posição menor que o retorno, ou há aviso de limite | há teto de retorno exibido, na posição anotada | Verificado por medição |
| 3 | a navegação não chega à última página | não se distingue o teto; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela do retorno e da última página acessível

#### SD7 — saber quantos registros a base exporta de uma vez em RIS com todos os campos

**Elementos verificados:** Teto de exportação por lote (Não verificado); Exportação em RIS com todos os campos (Não verificado).

**Pré-requisitos.**

- busca avançada da Scopus aberta no navegador do pesquisador

**Consulta 1 — teste**, em busca avançada.

```
TITLE-ABS-KEY(ontology AND education)
```

**Passos.**

1. submeter a consulta e anotar o retorno
2. abrir a exportação em RIS com todos os campos e anotar o número máximo de registros que ela aceita
3. exportar uma vez e contar os registros do arquivo

**Observar.**

- número máximo oferecido pela exportação
- número de registros no arquivo
- campos presentes no arquivo (resumo, palavras-chave)

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | o arquivo traz o número de registros pedido, com resumo e palavras-chave, e a exportação anuncia o máximo | a exportação em RIS com todos os campos funciona, com o teto anotado | Verificado por medição |
| 2 | a exportação falha, o arquivo vem sem resumo ou o número não corresponde ao pedido | não se confirma a exportação; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela da opção de exportação
- o arquivo exportado

---

## 2. Critérios de elegibilidade

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — 2017 até a data de execução | CE1 / CE2 | **Sim** | `AND PUBYEAR > 2016 AND PUBYEAR < 2027` |
| Idiomas — português, inglês e espanhol | CE3 | **Sim** | `AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish))` |
| Tipo documental | CE4 / CE5 | **Sim** | `AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))` |
| Adequação temática — regra de inclusão | CE6 | Aproximado | EB4 exige termo de prática (STR3) ou de fator situacional (STR4); a formalização se decide na triagem |
| Adequação temática — não pertinência e contra-escopo | CE6 | **Não** | exclusões temáticas manifestas na 2ª filtragem; aplicação integral na 3ª, com justificativa por ID |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, por âncora | faceta 🟨 (FCT2) nas cinco expressões |
| Outros tipos documentais | CE9 | **Não** | 2ª filtragem |
| Fator de impacto — não aplicável | CE10 | **Não** | não se aplica: critério só documental |

---

## 3. Strings por faceta

`STRn` é o identificador do protocolo e `#n` o número da string na composição. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

### Declaração de cobertura

Declarada em `docs/procedimentos/scopus/procedimento.toml`, `[cobertura]`; conferida por `python3 -m rsl documentos conferir`.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: pt, en, es; FCT2: pt, en, es; FCT3: pt, en, es; FCT4: pt, en, es |
| camadas | todas |
| plural | explícito |
| teto de caracteres | nenhum |
| derivações | morfologia |

### `STR1` — string `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
TITLE-ABS-KEY("representação do conhecimento" OR "organização do conhecimento" OR "ontologia" OR "ontologias" OR "modelo ontológico educacional" OR "modelos ontológicos educacionais" OR "vocabulário controlado" OR "vocabulários controlados" OR "tesauro" OR "tesauros" OR "taxonomia" OR "taxonomias" OR "esquema de classificação" OR "esquemas de classificação" OR "esquema de metadados" OR "esquemas de metadados" OR "classificação facetada" OR "classificações facetadas" OR "modelo conceitual" OR "modelos conceituais" OR "modelagem conceitual" OR "esquema conceitual" OR "esquemas conceituais" OR "modelo de domínio" OR "modelos de domínio" OR "modelo semântico" OR "modelos semânticos" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "padrões de projeto ontológicos" OR "modelagem baseada em ontologias" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "ontology" OR "ontologies" OR "educational ontological model" OR "educational ontological models" OR "controlled vocabulary" OR "controlled vocabularies" OR "thesaurus" OR "thesauri" OR "taxonomy" OR "taxonomies" OR "classification scheme" OR "classification schemes" OR "metadata schema" OR "metadata schemas" OR "faceted classification" OR "faceted classifications" OR "conceptual model" OR "conceptual models" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "conceptual schemas" OR "domain model" OR "domain models" OR "semantic model" OR "semantic models" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "ontología" OR "ontologías" OR "modelo ontológico educativo" OR "modelos ontológicos educativos" OR "vocabulario controlado" OR "vocabularios controlados" OR "taxonomía" OR "taxonomías" OR "esquema de clasificación" OR "esquemas de clasificación" OR "esquema de metadatos" OR "esquemas de metadatos" OR "clasificación facetada" OR "clasificaciones facetadas" OR "modelo conceptual" OR "modelos conceptuales" OR "modelado conceptual" OR "esquema conceptual" OR "esquemas conceptuales" OR "modelo de dominio" OR "modelos de dominio" OR "modelo semántico" OR "modelos semánticos" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "patrones de diseño ontológico" OR "modelado basado en ontologías")
```

### `STR2` — string `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

```
TITLE-ABS-KEY("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "ensino superior" OR "ensino básico" OR "ensino e aprendizagem" OR "trilha de aprendizagem" OR "trilhas de aprendizagem" OR "aprendizagem do estudante" OR "ensino híbrido" OR "aprendizagem online" OR "aprendizagem ao longo da vida" OR "sistema de gestão da aprendizagem" OR "sistemas de gestão da aprendizagem" OR "ensino fundamental" OR "ensino médio" OR "ambiente de aprendizagem" OR "ambientes de aprendizagem" OR "ambiente virtual de aprendizagem" OR "ambientes virtuais de aprendizagem" OR "objeto de aprendizagem" OR "objetos de aprendizagem" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "cursos online abertos e massivos" OR "instituição de ensino" OR "instituições de ensino" OR "nível de ensino" OR "níveis de ensino" OR "modalidade de ensino" OR "modalidades de ensino" OR "aprendiz" OR "aprendizes" OR "aprendices" OR "education" OR "educational" OR "teaching and learning" OR "teaching-learning" OR "learning path" OR "learning paths" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "learning management systems" OR "learning environment" OR "learning environments" OR "learning object" OR "learning objects" OR "e-learning" OR "massive open online course" OR "massive open online courses" OR "learning infrastructure" OR "learning infrastructures" OR "learner" OR "learners" OR "educación" OR "enseñanza superior" OR "enseñanza y aprendizaje" OR "itinerario de aprendizaje" OR "itinerarios de aprendizaje" OR "aprendizaje del estudiante" OR "aprendizaje combinado" OR "aprendizaje en línea" OR "aprendizaje a lo largo de la vida" OR "sistema de gestión del aprendizaje" OR "sistemas de gestión del aprendizaje" OR "tecnología educativa" OR "tecnologías educativas" OR "entorno de aprendizaje" OR "entornos de aprendizaje" OR "entorno virtual de aprendizaje" OR "entornos virtuales de aprendizaje" OR "objeto de aprendizaje" OR "objetos de aprendizaje" OR "recurso educativo abierto" OR "recursos educativos abiertos" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "cursos en línea masivos y abiertos" OR "institución educativa" OR "instituciones educativas" OR "infraestructura educativa" OR "infraestructuras educativas" OR "nivel educativo" OR "niveles educativos" OR "modalidad educativa" OR "modalidades educativas")
```

### `STR3` — string `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
TITLE-ABS-KEY("prática educacional" OR "práticas educacionais" OR "prática pedagógica" OR "práticas pedagógicas" OR "prática docente" OR "práticas docentes" OR "estratégia de ensino" OR "estratégias de ensino" OR "estratégia instrucional" OR "estratégias instrucionais" OR "método de ensino" OR "métodos de ensino" OR "método instrucional" OR "métodos instrucionais" OR "técnica de ensino" OR "técnicas de ensino" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "tarefa de aprendizagem" OR "tarefas de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais" OR "intervenção pedagógica" OR "intervenções pedagógicas" OR "sequência didática" OR "sequências didáticas" OR "sequência instrucional" OR "sequências instrucionais" OR "pedagogia" OR "pedagogias" OR "boa prática" OR "boas práticas" OR "prática recomendada" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagens pedagógicas" OR "abordagem instrucional" OR "abordagens instrucionais" OR "design instrucional" OR "desenho da aprendizagem" OR "desenhos da aprendizagem" OR "desenho didático" OR "desenhos didáticos" OR "padrão pedagógico" OR "padrões pedagógicos" OR "padrão de projeto pedagógico" OR "padrões de projeto pedagógicos" OR "método ativo" OR "métodos ativos" OR "metodologia de ensino" OR "metodologias de ensino" OR "educational practice" OR "educational practices" OR "pedagogical practice" OR "pedagogical practices" OR "teaching practice" OR "teaching practices" OR "instructional practice" OR "instructional practices" OR "teaching strategy" OR "teaching strategies" OR "instructional strategy" OR "instructional strategies" OR "teaching method" OR "teaching methods" OR "instructional method" OR "instructional methods" OR "teaching technique" OR "teaching techniques" OR "learning activity" OR "learning activities" OR "learning task" OR "learning tasks" OR "educational intervention" OR "educational interventions" OR "instructional intervention" OR "instructional interventions" OR "teaching sequence" OR "teaching sequences" OR "instructional sequence" OR "instructional sequences" OR "pedagogy" OR "pedagogies" OR "best practice" OR "best practices" OR "recommended practice" OR "recommended practices" OR "pedagogical approach" OR "pedagogical approaches" OR "instructional approach" OR "instructional approaches" OR "instructional design" OR "instructional designs" OR "learning design" OR "learning designs" OR "pedagogical pattern" OR "pedagogical patterns" OR "pedagogical design pattern" OR "pedagogical design patterns" OR "active learning method" OR "active learning methods" OR "teaching methodology" OR "teaching methodologies" OR "práctica educativa" OR "prácticas educativas" OR "práctica pedagógica" OR "prácticas pedagógicas" OR "práctica docente" OR "prácticas docentes" OR "estrategia de enseñanza" OR "estrategias de enseñanza" OR "estrategia didáctica" OR "estrategias didácticas" OR "método de enseñanza" OR "métodos de enseñanza" OR "método instruccional" OR "métodos instruccionales" OR "técnica de enseñanza" OR "técnicas de enseñanza" OR "actividad de aprendizaje" OR "actividades de aprendizaje" OR "tarea de aprendizaje" OR "tareas de aprendizaje" OR "intervención educativa" OR "intervenciones educativas" OR "intervención pedagógica" OR "intervenciones pedagógicas" OR "secuencia didáctica" OR "secuencias didácticas" OR "secuencia instruccional" OR "secuencias instruccionales" OR "pedagogía" OR "pedagogías" OR "buena práctica" OR "buenas prácticas" OR "práctica recomendada" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoques pedagógicos" OR "enfoque instruccional" OR "enfoques instruccionales" OR "diseño instruccional" OR "diseños instruccionales" OR "diseño del aprendizaje" OR "diseños del aprendizaje" OR "diseño didáctico" OR "diseños didácticos" OR "patrón pedagógico" OR "patrones pedagógicos" OR "patrón de diseño pedagógico" OR "patrones de diseño pedagógico" OR "método de aprendizaje activo" OR "métodos de aprendizaje activo" OR "metodología de enseñanza" OR "metodologías de enseñanza")
```

### `STR4` — string `#4` — 🟧 FCT4 — Fatores situacionais

```
TITLE-ABS-KEY("fator situacional" OR "fatores situacionais" OR "situação de uso" OR "situações de uso" OR "contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator de contexto" OR "fatores de contexto" OR "condição de aplicação" OR "condições de aplicação" OR "condição de implementação" OR "condições de implementação" OR "situação de aprendizagem" OR "situações de aprendizagem" OR "cenário educacional" OR "cenários educacionais" OR "contexto institucional" OR "contextos institucionais" OR "contextos institucionales" OR "contexto sociocultural" OR "contextos socioculturais" OR "contextos socioculturales" OR "perfil da turma" OR "perfis da turma" OR "característica do aluno" OR "características dos alunos" OR "restrição contextual" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "representações de contexto" OR "contexto sensível" OR "contextos sensíveis" OR "sensível ao contexto" OR "sensíveis ao contexto" OR "contextualização" OR "situational factor" OR "situational factors" OR "situation of use" OR "situations of use" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "context factor" OR "context factors" OR "application condition" OR "application conditions" OR "implementation condition" OR "implementation conditions" OR "learning situation" OR "learning situations" OR "educational setting" OR "educational settings" OR "institutional context" OR "institutional contexts" OR "sociocultural context" OR "sociocultural contexts" OR "class profile" OR "class profiles" OR "learner characteristic" OR "learner characteristics" OR "contextual constraint" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context representations" OR "context-aware" OR "contextualization" OR "contextualizations" OR "contextualisation" OR "contextualisations" OR "factor situacional" OR "factores situacionales" OR "situación de uso" OR "situaciones de uso" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor del contexto" OR "factores del contexto" OR "condición de aplicación" OR "condiciones de aplicación" OR "condición de implementación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "situaciones de aprendizaje" OR "escenario educativo" OR "escenarios educativos" OR "perfil del grupo" OR "perfiles del grupo" OR "característica del estudiante" OR "características de los estudiantes" OR "restricción contextual" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "representaciones del contexto" OR "sensible al contexto" OR "sensibles al contexto" OR "contextualización")
```

---

## 4. Expressões de busca

```
EB1 = #1 AND #2 AND #3 AND #4
EB2 = #1 AND #2 AND #3
EB3 = #1 AND #2 AND #4
EB4 = #1 AND #2 AND (#3 OR #4)     (executada)
EB5 = #1 AND #2                    (sonda de sensibilidade)
```

| Expressão | Execução |
| :--- | :--- |
| **EB4** | executar e exportar: é o corpus desta base |
| **EB5** | executar uma única vez, na mesma data; não compõe o corpus |
| **EB2**, **EB3** | executar só para o teste de fidelidade da derivação |
| **EB1** | não executar; derivação local |

- Execução: única
- **Fidelidade:** divergência acima de `divergencia_fidelidade` (`python3 -m rsl configuracao mostrar`) entre EB2/EB3 executadas e derivadas reprova a derivação.
- **Sensibilidade:** fração elegível de `EB5 \ EB4` abaixo do limite inferior da faixa `sensibilidade` (`python3 -m rsl configuracao mostrar`) mantém EB4; acima do superior, leva à reconsideração, com emenda.
- **Retorno zero:** EB4 = 0 ou EB5 = 0 é defeito de execução até prova em contrário; contagem derivada próxima de zero exige execução direta antes do relato.

### EB1 (as quatro facetas)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧)

### EB2 (modelos e ontologias que representam práticas do processo de ensino-aprendizagem)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥)

```
TITLE-ABS-KEY(("representação do conhecimento" OR "organização do conhecimento" OR "ontologia" OR "ontologias" OR "modelo ontológico educacional" OR "modelos ontológicos educacionais" OR "vocabulário controlado" OR "vocabulários controlados" OR "tesauro" OR "tesauros" OR "taxonomia" OR "taxonomias" OR "esquema de classificação" OR "esquemas de classificação" OR "esquema de metadados" OR "esquemas de metadados" OR "classificação facetada" OR "classificações facetadas" OR "modelo conceitual" OR "modelos conceituais" OR "modelagem conceitual" OR "esquema conceitual" OR "esquemas conceituais" OR "modelo de domínio" OR "modelos de domínio" OR "modelo semântico" OR "modelos semânticos" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "padrões de projeto ontológicos" OR "modelagem baseada em ontologias" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "ontology" OR "ontologies" OR "educational ontological model" OR "educational ontological models" OR "controlled vocabulary" OR "controlled vocabularies" OR "thesaurus" OR "thesauri" OR "taxonomy" OR "taxonomies" OR "classification scheme" OR "classification schemes" OR "metadata schema" OR "metadata schemas" OR "faceted classification" OR "faceted classifications" OR "conceptual model" OR "conceptual models" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "conceptual schemas" OR "domain model" OR "domain models" OR "semantic model" OR "semantic models" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "ontología" OR "ontologías" OR "modelo ontológico educativo" OR "modelos ontológicos educativos" OR "vocabulario controlado" OR "vocabularios controlados" OR "taxonomía" OR "taxonomías" OR "esquema de clasificación" OR "esquemas de clasificación" OR "esquema de metadatos" OR "esquemas de metadatos" OR "clasificación facetada" OR "clasificaciones facetadas" OR "modelo conceptual" OR "modelos conceptuales" OR "modelado conceptual" OR "esquema conceptual" OR "esquemas conceptuales" OR "modelo de dominio" OR "modelos de dominio" OR "modelo semántico" OR "modelos semánticos" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "patrones de diseño ontológico" OR "modelado basado en ontologías") W/5 ("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "ensino superior" OR "ensino básico" OR "ensino e aprendizagem" OR "trilha de aprendizagem" OR "trilhas de aprendizagem" OR "aprendizagem do estudante" OR "ensino híbrido" OR "aprendizagem online" OR "aprendizagem ao longo da vida" OR "sistema de gestão da aprendizagem" OR "sistemas de gestão da aprendizagem" OR "ensino fundamental" OR "ensino médio" OR "ambiente de aprendizagem" OR "ambientes de aprendizagem" OR "ambiente virtual de aprendizagem" OR "ambientes virtuais de aprendizagem" OR "objeto de aprendizagem" OR "objetos de aprendizagem" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "cursos online abertos e massivos" OR "instituição de ensino" OR "instituições de ensino" OR "nível de ensino" OR "níveis de ensino" OR "modalidade de ensino" OR "modalidades de ensino" OR "aprendiz" OR "aprendizes" OR "aprendices" OR "education" OR "educational" OR "teaching and learning" OR "teaching-learning" OR "learning path" OR "learning paths" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "learning management systems" OR "learning environment" OR "learning environments" OR "learning object" OR "learning objects" OR "e-learning" OR "massive open online course" OR "massive open online courses" OR "learning infrastructure" OR "learning infrastructures" OR "learner" OR "learners" OR "educación" OR "enseñanza superior" OR "enseñanza y aprendizaje" OR "itinerario de aprendizaje" OR "itinerarios de aprendizaje" OR "aprendizaje del estudiante" OR "aprendizaje combinado" OR "aprendizaje en línea" OR "aprendizaje a lo largo de la vida" OR "sistema de gestión del aprendizaje" OR "sistemas de gestión del aprendizaje" OR "tecnología educativa" OR "tecnologías educativas" OR "entorno de aprendizaje" OR "entornos de aprendizaje" OR "entorno virtual de aprendizaje" OR "entornos virtuales de aprendizaje" OR "objeto de aprendizaje" OR "objetos de aprendizaje" OR "recurso educativo abierto" OR "recursos educativos abiertos" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "cursos en línea masivos y abiertos" OR "institución educativa" OR "instituciones educativas" OR "infraestructura educativa" OR "infraestructuras educativas" OR "nivel educativo" OR "niveles educativos" OR "modalidad educativa" OR "modalidades educativas")) AND TITLE-ABS-KEY("prática educacional" OR "práticas educacionais" OR "prática pedagógica" OR "práticas pedagógicas" OR "prática docente" OR "práticas docentes" OR "estratégia de ensino" OR "estratégias de ensino" OR "estratégia instrucional" OR "estratégias instrucionais" OR "método de ensino" OR "métodos de ensino" OR "método instrucional" OR "métodos instrucionais" OR "técnica de ensino" OR "técnicas de ensino" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "tarefa de aprendizagem" OR "tarefas de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais" OR "intervenção pedagógica" OR "intervenções pedagógicas" OR "sequência didática" OR "sequências didáticas" OR "sequência instrucional" OR "sequências instrucionais" OR "pedagogia" OR "pedagogias" OR "boa prática" OR "boas práticas" OR "prática recomendada" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagens pedagógicas" OR "abordagem instrucional" OR "abordagens instrucionais" OR "design instrucional" OR "desenho da aprendizagem" OR "desenhos da aprendizagem" OR "desenho didático" OR "desenhos didáticos" OR "padrão pedagógico" OR "padrões pedagógicos" OR "padrão de projeto pedagógico" OR "padrões de projeto pedagógicos" OR "método ativo" OR "métodos ativos" OR "metodologia de ensino" OR "metodologias de ensino" OR "educational practice" OR "educational practices" OR "pedagogical practice" OR "pedagogical practices" OR "teaching practice" OR "teaching practices" OR "instructional practice" OR "instructional practices" OR "teaching strategy" OR "teaching strategies" OR "instructional strategy" OR "instructional strategies" OR "teaching method" OR "teaching methods" OR "instructional method" OR "instructional methods" OR "teaching technique" OR "teaching techniques" OR "learning activity" OR "learning activities" OR "learning task" OR "learning tasks" OR "educational intervention" OR "educational interventions" OR "instructional intervention" OR "instructional interventions" OR "teaching sequence" OR "teaching sequences" OR "instructional sequence" OR "instructional sequences" OR "pedagogy" OR "pedagogies" OR "best practice" OR "best practices" OR "recommended practice" OR "recommended practices" OR "pedagogical approach" OR "pedagogical approaches" OR "instructional approach" OR "instructional approaches" OR "instructional design" OR "instructional designs" OR "learning design" OR "learning designs" OR "pedagogical pattern" OR "pedagogical patterns" OR "pedagogical design pattern" OR "pedagogical design patterns" OR "active learning method" OR "active learning methods" OR "teaching methodology" OR "teaching methodologies" OR "práctica educativa" OR "prácticas educativas" OR "práctica pedagógica" OR "prácticas pedagógicas" OR "práctica docente" OR "prácticas docentes" OR "estrategia de enseñanza" OR "estrategias de enseñanza" OR "estrategia didáctica" OR "estrategias didácticas" OR "método de enseñanza" OR "métodos de enseñanza" OR "método instruccional" OR "métodos instruccionales" OR "técnica de enseñanza" OR "técnicas de enseñanza" OR "actividad de aprendizaje" OR "actividades de aprendizaje" OR "tarea de aprendizaje" OR "tareas de aprendizaje" OR "intervención educativa" OR "intervenciones educativas" OR "intervención pedagógica" OR "intervenciones pedagógicas" OR "secuencia didáctica" OR "secuencias didácticas" OR "secuencia instruccional" OR "secuencias instruccionales" OR "pedagogía" OR "pedagogías" OR "buena práctica" OR "buenas prácticas" OR "práctica recomendada" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoques pedagógicos" OR "enfoque instruccional" OR "enfoques instruccionales" OR "diseño instruccional" OR "diseños instruccionales" OR "diseño del aprendizaje" OR "diseños del aprendizaje" OR "diseño didáctico" OR "diseños didácticos" OR "patrón pedagógico" OR "patrones pedagógicos" OR "patrón de diseño pedagógico" OR "patrones de diseño pedagógico" OR "método de aprendizaje activo" OR "métodos de aprendizaje activo" OR "metodología de enseñanza" OR "metodologías de enseñanza") PUBYEAR > 2016 AND PUBYEAR < 2027 (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB3 (artefatos que formalizam os fatores situacionais do domínio educacional)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧)

```
TITLE-ABS-KEY(("representação do conhecimento" OR "organização do conhecimento" OR "ontologia" OR "ontologias" OR "modelo ontológico educacional" OR "modelos ontológicos educacionais" OR "vocabulário controlado" OR "vocabulários controlados" OR "tesauro" OR "tesauros" OR "taxonomia" OR "taxonomias" OR "esquema de classificação" OR "esquemas de classificação" OR "esquema de metadados" OR "esquemas de metadados" OR "classificação facetada" OR "classificações facetadas" OR "modelo conceitual" OR "modelos conceituais" OR "modelagem conceitual" OR "esquema conceitual" OR "esquemas conceituais" OR "modelo de domínio" OR "modelos de domínio" OR "modelo semântico" OR "modelos semânticos" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "padrões de projeto ontológicos" OR "modelagem baseada em ontologias" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "ontology" OR "ontologies" OR "educational ontological model" OR "educational ontological models" OR "controlled vocabulary" OR "controlled vocabularies" OR "thesaurus" OR "thesauri" OR "taxonomy" OR "taxonomies" OR "classification scheme" OR "classification schemes" OR "metadata schema" OR "metadata schemas" OR "faceted classification" OR "faceted classifications" OR "conceptual model" OR "conceptual models" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "conceptual schemas" OR "domain model" OR "domain models" OR "semantic model" OR "semantic models" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "ontología" OR "ontologías" OR "modelo ontológico educativo" OR "modelos ontológicos educativos" OR "vocabulario controlado" OR "vocabularios controlados" OR "taxonomía" OR "taxonomías" OR "esquema de clasificación" OR "esquemas de clasificación" OR "esquema de metadatos" OR "esquemas de metadatos" OR "clasificación facetada" OR "clasificaciones facetadas" OR "modelo conceptual" OR "modelos conceptuales" OR "modelado conceptual" OR "esquema conceptual" OR "esquemas conceptuales" OR "modelo de dominio" OR "modelos de dominio" OR "modelo semántico" OR "modelos semánticos" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "patrones de diseño ontológico" OR "modelado basado en ontologías") W/5 ("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "ensino superior" OR "ensino básico" OR "ensino e aprendizagem" OR "trilha de aprendizagem" OR "trilhas de aprendizagem" OR "aprendizagem do estudante" OR "ensino híbrido" OR "aprendizagem online" OR "aprendizagem ao longo da vida" OR "sistema de gestão da aprendizagem" OR "sistemas de gestão da aprendizagem" OR "ensino fundamental" OR "ensino médio" OR "ambiente de aprendizagem" OR "ambientes de aprendizagem" OR "ambiente virtual de aprendizagem" OR "ambientes virtuais de aprendizagem" OR "objeto de aprendizagem" OR "objetos de aprendizagem" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "cursos online abertos e massivos" OR "instituição de ensino" OR "instituições de ensino" OR "nível de ensino" OR "níveis de ensino" OR "modalidade de ensino" OR "modalidades de ensino" OR "aprendiz" OR "aprendizes" OR "aprendices" OR "education" OR "educational" OR "teaching and learning" OR "teaching-learning" OR "learning path" OR "learning paths" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "learning management systems" OR "learning environment" OR "learning environments" OR "learning object" OR "learning objects" OR "e-learning" OR "massive open online course" OR "massive open online courses" OR "learning infrastructure" OR "learning infrastructures" OR "learner" OR "learners" OR "educación" OR "enseñanza superior" OR "enseñanza y aprendizaje" OR "itinerario de aprendizaje" OR "itinerarios de aprendizaje" OR "aprendizaje del estudiante" OR "aprendizaje combinado" OR "aprendizaje en línea" OR "aprendizaje a lo largo de la vida" OR "sistema de gestión del aprendizaje" OR "sistemas de gestión del aprendizaje" OR "tecnología educativa" OR "tecnologías educativas" OR "entorno de aprendizaje" OR "entornos de aprendizaje" OR "entorno virtual de aprendizaje" OR "entornos virtuales de aprendizaje" OR "objeto de aprendizaje" OR "objetos de aprendizaje" OR "recurso educativo abierto" OR "recursos educativos abiertos" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "cursos en línea masivos y abiertos" OR "institución educativa" OR "instituciones educativas" OR "infraestructura educativa" OR "infraestructuras educativas" OR "nivel educativo" OR "niveles educativos" OR "modalidad educativa" OR "modalidades educativas")) AND TITLE-ABS-KEY("fator situacional" OR "fatores situacionais" OR "situação de uso" OR "situações de uso" OR "contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator de contexto" OR "fatores de contexto" OR "condição de aplicação" OR "condições de aplicação" OR "condição de implementação" OR "condições de implementação" OR "situação de aprendizagem" OR "situações de aprendizagem" OR "cenário educacional" OR "cenários educacionais" OR "contexto institucional" OR "contextos institucionais" OR "contextos institucionales" OR "contexto sociocultural" OR "contextos socioculturais" OR "contextos socioculturales" OR "perfil da turma" OR "perfis da turma" OR "característica do aluno" OR "características dos alunos" OR "restrição contextual" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "representações de contexto" OR "contexto sensível" OR "contextos sensíveis" OR "sensível ao contexto" OR "sensíveis ao contexto" OR "contextualização" OR "situational factor" OR "situational factors" OR "situation of use" OR "situations of use" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "context factor" OR "context factors" OR "application condition" OR "application conditions" OR "implementation condition" OR "implementation conditions" OR "learning situation" OR "learning situations" OR "educational setting" OR "educational settings" OR "institutional context" OR "institutional contexts" OR "sociocultural context" OR "sociocultural contexts" OR "class profile" OR "class profiles" OR "learner characteristic" OR "learner characteristics" OR "contextual constraint" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context representations" OR "context-aware" OR "contextualization" OR "contextualizations" OR "contextualisation" OR "contextualisations" OR "factor situacional" OR "factores situacionales" OR "situación de uso" OR "situaciones de uso" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor del contexto" OR "factores del contexto" OR "condición de aplicación" OR "condiciones de aplicación" OR "condición de implementación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "situaciones de aprendizaje" OR "escenario educativo" OR "escenarios educativos" OR "perfil del grupo" OR "perfiles del grupo" OR "característica del estudiante" OR "características de los estudiantes" OR "restricción contextual" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "representaciones del contexto" OR "sensible al contexto" OR "sensibles al contexto" OR "contextualización") PUBYEAR > 2016 AND PUBYEAR < 2027 (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB4 (de cobertura restrita — artefatos de representação no domínio educacional que mencionam prática ou fator situacional)

*Executada e exportada nesta base.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧))

```
TITLE-ABS-KEY(("representação do conhecimento" OR "organização do conhecimento" OR "ontologia" OR "ontologias" OR "modelo ontológico educacional" OR "modelos ontológicos educacionais" OR "vocabulário controlado" OR "vocabulários controlados" OR "tesauro" OR "tesauros" OR "taxonomia" OR "taxonomias" OR "esquema de classificação" OR "esquemas de classificação" OR "esquema de metadados" OR "esquemas de metadados" OR "classificação facetada" OR "classificações facetadas" OR "modelo conceitual" OR "modelos conceituais" OR "modelagem conceitual" OR "esquema conceitual" OR "esquemas conceituais" OR "modelo de domínio" OR "modelos de domínio" OR "modelo semântico" OR "modelos semânticos" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "padrões de projeto ontológicos" OR "modelagem baseada em ontologias" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "ontology" OR "ontologies" OR "educational ontological model" OR "educational ontological models" OR "controlled vocabulary" OR "controlled vocabularies" OR "thesaurus" OR "thesauri" OR "taxonomy" OR "taxonomies" OR "classification scheme" OR "classification schemes" OR "metadata schema" OR "metadata schemas" OR "faceted classification" OR "faceted classifications" OR "conceptual model" OR "conceptual models" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "conceptual schemas" OR "domain model" OR "domain models" OR "semantic model" OR "semantic models" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "ontología" OR "ontologías" OR "modelo ontológico educativo" OR "modelos ontológicos educativos" OR "vocabulario controlado" OR "vocabularios controlados" OR "taxonomía" OR "taxonomías" OR "esquema de clasificación" OR "esquemas de clasificación" OR "esquema de metadatos" OR "esquemas de metadatos" OR "clasificación facetada" OR "clasificaciones facetadas" OR "modelo conceptual" OR "modelos conceptuales" OR "modelado conceptual" OR "esquema conceptual" OR "esquemas conceptuales" OR "modelo de dominio" OR "modelos de dominio" OR "modelo semántico" OR "modelos semánticos" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "patrones de diseño ontológico" OR "modelado basado en ontologías") W/5 ("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "ensino superior" OR "ensino básico" OR "ensino e aprendizagem" OR "trilha de aprendizagem" OR "trilhas de aprendizagem" OR "aprendizagem do estudante" OR "ensino híbrido" OR "aprendizagem online" OR "aprendizagem ao longo da vida" OR "sistema de gestão da aprendizagem" OR "sistemas de gestão da aprendizagem" OR "ensino fundamental" OR "ensino médio" OR "ambiente de aprendizagem" OR "ambientes de aprendizagem" OR "ambiente virtual de aprendizagem" OR "ambientes virtuais de aprendizagem" OR "objeto de aprendizagem" OR "objetos de aprendizagem" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "cursos online abertos e massivos" OR "instituição de ensino" OR "instituições de ensino" OR "nível de ensino" OR "níveis de ensino" OR "modalidade de ensino" OR "modalidades de ensino" OR "aprendiz" OR "aprendizes" OR "aprendices" OR "education" OR "educational" OR "teaching and learning" OR "teaching-learning" OR "learning path" OR "learning paths" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "learning management systems" OR "learning environment" OR "learning environments" OR "learning object" OR "learning objects" OR "e-learning" OR "massive open online course" OR "massive open online courses" OR "learning infrastructure" OR "learning infrastructures" OR "learner" OR "learners" OR "educación" OR "enseñanza superior" OR "enseñanza y aprendizaje" OR "itinerario de aprendizaje" OR "itinerarios de aprendizaje" OR "aprendizaje del estudiante" OR "aprendizaje combinado" OR "aprendizaje en línea" OR "aprendizaje a lo largo de la vida" OR "sistema de gestión del aprendizaje" OR "sistemas de gestión del aprendizaje" OR "tecnología educativa" OR "tecnologías educativas" OR "entorno de aprendizaje" OR "entornos de aprendizaje" OR "entorno virtual de aprendizaje" OR "entornos virtuales de aprendizaje" OR "objeto de aprendizaje" OR "objetos de aprendizaje" OR "recurso educativo abierto" OR "recursos educativos abiertos" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "cursos en línea masivos y abiertos" OR "institución educativa" OR "instituciones educativas" OR "infraestructura educativa" OR "infraestructuras educativas" OR "nivel educativo" OR "niveles educativos" OR "modalidad educativa" OR "modalidades educativas")) AND (TITLE-ABS-KEY("prática educacional" OR "práticas educacionais" OR "prática pedagógica" OR "práticas pedagógicas" OR "prática docente" OR "práticas docentes" OR "estratégia de ensino" OR "estratégias de ensino" OR "estratégia instrucional" OR "estratégias instrucionais" OR "método de ensino" OR "métodos de ensino" OR "método instrucional" OR "métodos instrucionais" OR "técnica de ensino" OR "técnicas de ensino" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "tarefa de aprendizagem" OR "tarefas de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais" OR "intervenção pedagógica" OR "intervenções pedagógicas" OR "sequência didática" OR "sequências didáticas" OR "sequência instrucional" OR "sequências instrucionais" OR "pedagogia" OR "pedagogias" OR "boa prática" OR "boas práticas" OR "prática recomendada" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagens pedagógicas" OR "abordagem instrucional" OR "abordagens instrucionais" OR "design instrucional" OR "desenho da aprendizagem" OR "desenhos da aprendizagem" OR "desenho didático" OR "desenhos didáticos" OR "padrão pedagógico" OR "padrões pedagógicos" OR "padrão de projeto pedagógico" OR "padrões de projeto pedagógicos" OR "método ativo" OR "métodos ativos" OR "metodologia de ensino" OR "metodologias de ensino" OR "educational practice" OR "educational practices" OR "pedagogical practice" OR "pedagogical practices" OR "teaching practice" OR "teaching practices" OR "instructional practice" OR "instructional practices" OR "teaching strategy" OR "teaching strategies" OR "instructional strategy" OR "instructional strategies" OR "teaching method" OR "teaching methods" OR "instructional method" OR "instructional methods" OR "teaching technique" OR "teaching techniques" OR "learning activity" OR "learning activities" OR "learning task" OR "learning tasks" OR "educational intervention" OR "educational interventions" OR "instructional intervention" OR "instructional interventions" OR "teaching sequence" OR "teaching sequences" OR "instructional sequence" OR "instructional sequences" OR "pedagogy" OR "pedagogies" OR "best practice" OR "best practices" OR "recommended practice" OR "recommended practices" OR "pedagogical approach" OR "pedagogical approaches" OR "instructional approach" OR "instructional approaches" OR "instructional design" OR "instructional designs" OR "learning design" OR "learning designs" OR "pedagogical pattern" OR "pedagogical patterns" OR "pedagogical design pattern" OR "pedagogical design patterns" OR "active learning method" OR "active learning methods" OR "teaching methodology" OR "teaching methodologies" OR "práctica educativa" OR "prácticas educativas" OR "práctica pedagógica" OR "prácticas pedagógicas" OR "práctica docente" OR "prácticas docentes" OR "estrategia de enseñanza" OR "estrategias de enseñanza" OR "estrategia didáctica" OR "estrategias didácticas" OR "método de enseñanza" OR "métodos de enseñanza" OR "método instruccional" OR "métodos instruccionales" OR "técnica de enseñanza" OR "técnicas de enseñanza" OR "actividad de aprendizaje" OR "actividades de aprendizaje" OR "tarea de aprendizaje" OR "tareas de aprendizaje" OR "intervención educativa" OR "intervenciones educativas" OR "intervención pedagógica" OR "intervenciones pedagógicas" OR "secuencia didáctica" OR "secuencias didácticas" OR "secuencia instruccional" OR "secuencias instruccionales" OR "pedagogía" OR "pedagogías" OR "buena práctica" OR "buenas prácticas" OR "práctica recomendada" OR "prácticas recomendadas" OR "enfoque pedagógico" OR "enfoques pedagógicos" OR "enfoque instruccional" OR "enfoques instruccionales" OR "diseño instruccional" OR "diseños instruccionales" OR "diseño del aprendizaje" OR "diseños del aprendizaje" OR "diseño didáctico" OR "diseños didácticos" OR "patrón pedagógico" OR "patrones pedagógicos" OR "patrón de diseño pedagógico" OR "patrones de diseño pedagógico" OR "método de aprendizaje activo" OR "métodos de aprendizaje activo" OR "metodología de enseñanza" OR "metodologías de enseñanza") OR TITLE-ABS-KEY("fator situacional" OR "fatores situacionais" OR "situação de uso" OR "situações de uso" OR "contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator de contexto" OR "fatores de contexto" OR "condição de aplicação" OR "condições de aplicação" OR "condição de implementação" OR "condições de implementação" OR "situação de aprendizagem" OR "situações de aprendizagem" OR "cenário educacional" OR "cenários educacionais" OR "contexto institucional" OR "contextos institucionais" OR "contextos institucionales" OR "contexto sociocultural" OR "contextos socioculturais" OR "contextos socioculturales" OR "perfil da turma" OR "perfis da turma" OR "característica do aluno" OR "características dos alunos" OR "restrição contextual" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "representações de contexto" OR "contexto sensível" OR "contextos sensíveis" OR "sensível ao contexto" OR "sensíveis ao contexto" OR "contextualização" OR "situational factor" OR "situational factors" OR "situation of use" OR "situations of use" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "context factor" OR "context factors" OR "application condition" OR "application conditions" OR "implementation condition" OR "implementation conditions" OR "learning situation" OR "learning situations" OR "educational setting" OR "educational settings" OR "institutional context" OR "institutional contexts" OR "sociocultural context" OR "sociocultural contexts" OR "class profile" OR "class profiles" OR "learner characteristic" OR "learner characteristics" OR "contextual constraint" OR "contextual constraints" OR "context modeling" OR "context modelling" OR "context representation" OR "context representations" OR "context-aware" OR "contextualization" OR "contextualizations" OR "contextualisation" OR "contextualisations" OR "factor situacional" OR "factores situacionales" OR "situación de uso" OR "situaciones de uso" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor del contexto" OR "factores del contexto" OR "condición de aplicación" OR "condiciones de aplicación" OR "condición de implementación" OR "condiciones de implementación" OR "situación de aprendizaje" OR "situaciones de aprendizaje" OR "escenario educativo" OR "escenarios educativos" OR "perfil del grupo" OR "perfiles del grupo" OR "característica del estudiante" OR "características de los estudiantes" OR "restricción contextual" OR "restricciones contextuales" OR "modelado del contexto" OR "representación del contexto" OR "representaciones del contexto" OR "sensible al contexto" OR "sensibles al contexto" OR "contextualización")) PUBYEAR > 2016 AND PUBYEAR < 2027 (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨)

```
TITLE-ABS-KEY(("representação do conhecimento" OR "organização do conhecimento" OR "ontologia" OR "ontologias" OR "modelo ontológico educacional" OR "modelos ontológicos educacionais" OR "vocabulário controlado" OR "vocabulários controlados" OR "tesauro" OR "tesauros" OR "taxonomia" OR "taxonomias" OR "esquema de classificação" OR "esquemas de classificação" OR "esquema de metadados" OR "esquemas de metadados" OR "classificação facetada" OR "classificações facetadas" OR "modelo conceitual" OR "modelos conceituais" OR "modelagem conceitual" OR "esquema conceitual" OR "esquemas conceituais" OR "modelo de domínio" OR "modelos de domínio" OR "modelo semântico" OR "modelos semânticos" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "padrões de projeto ontológicos" OR "modelagem baseada em ontologias" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "ontology" OR "ontologies" OR "educational ontological model" OR "educational ontological models" OR "controlled vocabulary" OR "controlled vocabularies" OR "thesaurus" OR "thesauri" OR "taxonomy" OR "taxonomies" OR "classification scheme" OR "classification schemes" OR "metadata schema" OR "metadata schemas" OR "faceted classification" OR "faceted classifications" OR "conceptual model" OR "conceptual models" OR "conceptual modeling" OR "conceptual modelling" OR "conceptual schema" OR "conceptual schemas" OR "domain model" OR "domain models" OR "semantic model" OR "semantic models" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontological engineering" OR "representación del conocimiento" OR "organización del conocimiento" OR "ontología" OR "ontologías" OR "modelo ontológico educativo" OR "modelos ontológicos educativos" OR "vocabulario controlado" OR "vocabularios controlados" OR "taxonomía" OR "taxonomías" OR "esquema de clasificación" OR "esquemas de clasificación" OR "esquema de metadatos" OR "esquemas de metadatos" OR "clasificación facetada" OR "clasificaciones facetadas" OR "modelo conceptual" OR "modelos conceptuales" OR "modelado conceptual" OR "esquema conceptual" OR "esquemas conceptuales" OR "modelo de dominio" OR "modelos de dominio" OR "modelo semántico" OR "modelos semánticos" OR "ingeniería de ontologías" OR "desarrollo de ontologías" OR "patrón de diseño ontológico" OR "patrones de diseño ontológico" OR "modelado basado en ontologías") W/5 ("educação" OR "educacional" OR "educacionais" OR "educacionales" OR "ensino superior" OR "ensino básico" OR "ensino e aprendizagem" OR "trilha de aprendizagem" OR "trilhas de aprendizagem" OR "aprendizagem do estudante" OR "ensino híbrido" OR "aprendizagem online" OR "aprendizagem ao longo da vida" OR "sistema de gestão da aprendizagem" OR "sistemas de gestão da aprendizagem" OR "ensino fundamental" OR "ensino médio" OR "ambiente de aprendizagem" OR "ambientes de aprendizagem" OR "ambiente virtual de aprendizagem" OR "ambientes virtuais de aprendizagem" OR "objeto de aprendizagem" OR "objetos de aprendizagem" OR "aprendizagem eletrônica" OR "curso online aberto e massivo" OR "cursos online abertos e massivos" OR "instituição de ensino" OR "instituições de ensino" OR "nível de ensino" OR "níveis de ensino" OR "modalidade de ensino" OR "modalidades de ensino" OR "aprendiz" OR "aprendizes" OR "aprendices" OR "education" OR "educational" OR "teaching and learning" OR "teaching-learning" OR "learning path" OR "learning paths" OR "student learning" OR "blended learning" OR "online learning" OR "lifelong learning" OR "learning management system" OR "learning management systems" OR "learning environment" OR "learning environments" OR "learning object" OR "learning objects" OR "e-learning" OR "massive open online course" OR "massive open online courses" OR "learning infrastructure" OR "learning infrastructures" OR "learner" OR "learners" OR "educación" OR "enseñanza superior" OR "enseñanza y aprendizaje" OR "itinerario de aprendizaje" OR "itinerarios de aprendizaje" OR "aprendizaje del estudiante" OR "aprendizaje combinado" OR "aprendizaje en línea" OR "aprendizaje a lo largo de la vida" OR "sistema de gestión del aprendizaje" OR "sistemas de gestión del aprendizaje" OR "tecnología educativa" OR "tecnologías educativas" OR "entorno de aprendizaje" OR "entornos de aprendizaje" OR "entorno virtual de aprendizaje" OR "entornos virtuales de aprendizaje" OR "objeto de aprendizaje" OR "objetos de aprendizaje" OR "recurso educativo abierto" OR "recursos educativos abiertos" OR "aprendizaje electrónico" OR "curso en línea masivo y abierto" OR "cursos en línea masivos y abiertos" OR "institución educativa" OR "instituciones educativas" OR "infraestructura educativa" OR "infraestructuras educativas" OR "nivel educativo" OR "niveles educativos" OR "modalidad educativa" OR "modalidades educativas")) PUBYEAR > 2016 AND PUBYEAR < 2027 (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### Como executar

1. Conferir a sessão contra a seção 1, na primeira execução do dia.
2. Submeter o bloco de EB4 da seção 4 como está, sem definir conjunto. Na primeira execução, conferir se a interface aceita a consulta inteira; recusa por extensão leva à variante "Redução por recusa da interface", registrada como adaptação.
3. Submeter sempre a partir de arquivo, nunca recuperando o texto da interface.
4. Exportar em RIS, com todos os campos.
5. Conferir o retorno da exportação contra o da tela e o recorte temporal dentro do arquivo.
6. Registrar EB4 e EB5: `python3 -m rsl busca registrar scopus EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`; rodar `busca derivar` e `conferencia sensibilidade`.
7. Medir a aderência (seção 5). Semente esperada não recuperada: aplicar a anatomia da perda.
8. Na primeira execução, conferir se o retorno de EB4 tem a mesma ordem de grandeza do da Web of Science; discrepância indica problema de agrupamento.

### Variantes previstas

#### Forma ampla, sem proximidade

Disparo: a anatomia da perda atribui a perda à proximidade, ou a interface recusa `W/5` entre grupos deste tamanho. Forma: trocar a proximidade entre as duas âncoras por `AND` entre os grupos, nas cinco expressões. Adoção exige emenda.

#### Sem limite de tipo documental

Disparo: medir o efeito dos critérios CE4 e CE5. Forma: EB4 sem a cláusula `DOCTYPE`; reportar a diferença de retorno.

#### Redução por recusa da interface

Disparo: bloco executado recusado por extensão. Forma: partir o grupo 🟨 das âncoras em duas metades — educação formal; tecnologia educacional e aprendizagem digital —, mantendo o resto idêntico, e unir por deduplicação. Registrar a partição como adaptação. A emenda declara `- Execução: particionada` e escreve as partes literais.

#### Truncamento

Não usar curinga. Disparo: aderência abaixo do limiar de aderência (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`). Forma: testar a consulta abaixo; a adoção exige emenda.

```
TITLE-ABS-KEY(ontolog* W/5 educat*)
```

#### Camada de precisão

Disparo: retorno alto demais para a triagem. Forma: restringir por `SUBJAREA`, com os códigos conferidos na documentação. Camada com aderência abaixo do limiar de aderência (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`) é reprovada.

---

## 5. Conjunto-semente

Esperadas nesta base, conforme o protocolo. Estado de conferência no arquivo de sementes (`[documentos] sementes`); aferição em `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE2 | Das et al. (2022) | `10.5771/0943-7444-2022-1-6` | — |
| SE3 | Chi et al. (2018) | `10.1111/exsy.12246` | — |
| SE4 | Shvets et al. (2024) | `10.5220/0012471400003645` | comunicação em anais |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE8 | Cenka et al. (2023) | `10.1080/10494820.2022.2039947` | — |
| SE9 | Piriyapongpipat et al. (2024) | `10.1186/s40561-024-00307-8` | — |

**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões; semente não indexada sai do denominador e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação de EB4 por DOI e depois por título, sem reexecutar a busca.

**Limiar de aderência** (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`), sobre a união das bases. A aderência por base indica qual base e qual faceta falharam.

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
