# Strings de busca — BRAPCI

## 1. Estado de verificação da sintaxe

Sintaxe não documentada em fonte alguma: **não verificada por medição** — sondar antes da primeira execução e registrar a execução.

| Elemento | Situação |
| :--- | :--- |
| Aspas como frase | **Não verificado**; sondar antes da primeira execução |
| `AND`, `OR` e parênteses | **Não verificado**; sondar antes da primeira execução |
| Truncamento `*` | **Não verificado**; não se usa |
| Lematização | **Não medida**; flexões explícitas nas strings |
| Comprimento máximo da consulta | **Não verificado**; a EB4 expandida tem cerca de 4.100 caracteres — sondar antes da primeira execução |
| Proximidade | **Não verificada** |
| Exportação — formatos e lote | **Não verificada** |
| Local de pesquisa | **Não verificado**; conferir na interface antes da primeira execução |
| Campos diferentes na mesma consulta | **Não verificado**; conferir na interface antes da primeira execução |
| Filtros | **Não verificado**; conferir na interface antes da primeira execução |
| Teto de exibição | **Não verificado**; retorno de exatamente 1.000 será tratado como **corte** até medir |

**Regra de execução, para toda consulta desta ficha.**

1. Aplicar o filtro de ano **antes** de executar.
2. Manter **Local de pesquisa = Todos os campos**.
3. Usar o método de busca **ponderado**; registrar o método, o Local de pesquisa e o limite de resultados (1.000 a 5.000).
4. Não usar o filtro de tipo de publicação.
5. Anotar o retorno de cada consulta.
6. Retorno de 1.000: consulta truncada; partir conforme a variante "Partição".

**Outros campos do seletor**, só como instrumento: *Título*, para precisão e partição; *Resumo* e *Palavras-chave*, para medir onde a base indexa; *Autor*, para *backward search* e conferência de duplicatas.

---

## 2. Critérios de elegibilidade

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — 2017 até a data de execução | CE1 / CE2 | **No filtro da interface** | ano inicial 2017 e final 2026, antes de executar; conferir o ano no retorno |
| Idiomas — português, inglês e espanhol | CE3 | **Dispensado** | strings em português, e em inglês na faceta 🟦; sem filtro de idioma |
| Tipo documental | CE4 / CE5 | **Não** | filtro de tipo não usado |
| Texto completo | CE6 | **Não** | 2ª filtragem |
| Adequação temática — regra de inclusão | CE7 | Aproximado | EB4 exige termo de prática (STR3) ou de fator situacional (STR4); a formalização se decide na triagem |
| Adequação temática — não pertinência | CE8 | **Não** | exclusões temáticas manifestas na 2ª filtragem; aplicação integral na 3ª |
| Adequação temática — contra-escopo | CE9 / CE10 / CE11 / CE12 | **Não** | exclusões temáticas manifestas na 2ª filtragem; aplicação integral na 3ª, com justificativa por ID |
| Domínio de aplicação educacional | CE13 / CE14 | **Sim**, por âncora | faceta 🟨 (FCT2) nas cinco expressões |
| Outros tipos documentais | CE15 | **Não** | 2ª filtragem |

---

## 3. Strings por faceta

`STRn` é o identificador do protocolo e `#n` a string correspondente. Flexões de número explícitas, sem truncamento. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

### Declaração de cobertura

Lida por `python3 -m rsl conferir` (leitor das fichas em `src/rsl/fichas.py`).

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: pt, en; FCT2: pt; FCT3: pt; FCT4: pt |
| camadas | todas |
| derivações | morfologia |

### `STR1` — string `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologias" OR "ontologia de domínio" OR "ontologias de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia facetada" OR "esquema de classificação" OR "esquema de metadados" OR "classificação facetada" OR "ontologia facetada" OR "ontologia educacional" OR "ontologia de aprendizagem" OR "ontologia de ensino" OR "modelo ontológico educacional" OR "ontologia de prática educacional" OR "ontologia de design instrucional" OR "ontologia de currículo" OR "modelo de domínio" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representação do conhecimento baseada em ontologias" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "ontologies" OR "domain ontology" OR "domain ontologies" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "faceted taxonomy" OR "classification scheme" OR "metadata schema" OR "faceted classification" OR "faceted ontology" OR "educational ontology" OR "learning ontology" OR "teaching ontology" OR "educational ontological model" OR "educational practice ontology" OR "instructional design ontology" OR "curriculum ontology" OR "domain model" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "taxonomía facetada")
```

### `STR2` — string `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

```
("educação" OR "educacional" OR "educacionais" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo")
```

### `STR3` — string `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
("prática" OR "prática educacional" OR "práticas educacionais" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boa prática" OR "boas práticas" OR "prática recomendada" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino")
```

### `STR4` — string `#4` — 🟧 FCT4 — Fatores situacionais

```
("fator situacional" OR "fatores situacionais" OR "situação de uso educacional" OR "contexto educacional" OR "contexto de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator de contexto" OR "fatores de contexto" OR "condição de aplicação" OR "condições de aplicação" OR "condição de implementação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "característica do aluno" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recurso disponível" OR "recursos disponíveis" OR "restrição contextual" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização")
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
| **EB2**, **EB3** | não executar; derivação local |
| **EB1** | não executar; derivação local |

- Execução: única
**Forma de execução.** Submeter o bloco de EB4 da seção 4 como está, sem definir conjunto.

**Retorno zero.** EB4 = 0 ou EB5 = 0 é defeito de execução até provado que a consulta longa foi aceita inteira. Contagem derivada nula, com execução válida, registra-se como achado; não relaxar a âncora 🟦 por causa dela.

### EB1 (as quatro facetas)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧)

### EB2 (modelos e ontologias que representam práticas do processo de ensino-aprendizagem)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥)

### EB3 (artefatos que formalizam os fatores situacionais do domínio educacional)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧)

### EB4 (de cobertura restrita — artefatos de representação no domínio educacional que mencionam prática ou fator situacional)

*Executada e exportada nesta base.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧))

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologias" OR "ontologia de domínio" OR "ontologias de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia facetada" OR "esquema de classificação" OR "esquema de metadados" OR "classificação facetada" OR "ontologia facetada" OR "ontologia educacional" OR "ontologia de aprendizagem" OR "ontologia de ensino" OR "modelo ontológico educacional" OR "ontologia de prática educacional" OR "ontologia de design instrucional" OR "ontologia de currículo" OR "modelo de domínio" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representação do conhecimento baseada em ontologias" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "ontologies" OR "domain ontology" OR "domain ontologies" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "faceted taxonomy" OR "classification scheme" OR "metadata schema" OR "faceted classification" OR "faceted ontology" OR "educational ontology" OR "learning ontology" OR "teaching ontology" OR "educational ontological model" OR "educational practice ontology" OR "instructional design ontology" OR "curriculum ontology" OR "domain model" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "taxonomía facetada") AND ("educação" OR "educacional" OR "educacionais" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo") AND (("prática" OR "prática educacional" OR "práticas educacionais" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boa prática" OR "boas práticas" OR "prática recomendada" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino") OR ("fator situacional" OR "fatores situacionais" OR "situação de uso educacional" OR "contexto educacional" OR "contexto de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator de contexto" OR "fatores de contexto" OR "condição de aplicação" OR "condições de aplicação" OR "condição de implementação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "característica do aluno" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recurso disponível" OR "recursos disponíveis" OR "restrição contextual" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização"))
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨)

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologias" OR "ontologia de domínio" OR "ontologias de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia facetada" OR "esquema de classificação" OR "esquema de metadados" OR "classificação facetada" OR "ontologia facetada" OR "ontologia educacional" OR "ontologia de aprendizagem" OR "ontologia de ensino" OR "modelo ontológico educacional" OR "ontologia de prática educacional" OR "ontologia de design instrucional" OR "ontologia de currículo" OR "modelo de domínio" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representação do conhecimento baseada em ontologias" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "ontologies" OR "domain ontology" OR "domain ontologies" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "faceted taxonomy" OR "classification scheme" OR "metadata schema" OR "faceted classification" OR "faceted ontology" OR "educational ontology" OR "learning ontology" OR "teaching ontology" OR "educational ontological model" OR "educational practice ontology" OR "instructional design ontology" OR "curriculum ontology" OR "domain model" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "taxonomía facetada") AND ("educação" OR "educacional" OR "educacionais" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo")
```

### Como executar

1. Aplicar a regra de execução da seção 1.
2. **Sondar o comprimento.** Submeter o bloco de EB5 da seção 4 e conferir que foi aceito inteiro, comparando o retorno com o da faceta 🟦 partida em metades, cada metade com a faceta 🟨. Registrar a sondagem.
3. Executar o bloco de EB4 como está. Retorno de exatamente 1.000: partir, conforme as variantes.
4. Executar EB5 uma única vez, na mesma data.
5. Exportar em RIS ou BibTeX; sem exportação, registrar os metadados no Zotero e anotar a entrada manual como risco de transcrição.
6. Registrar: `python3 -m rsl busca registrar brapci EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`, com a justificativa do teto de 1.000 quando for o caso; rodar `busca derivar` e `busca sensibilidade`.
7. Medir a aderência (seção 5).

### Variantes previstas

#### Partição — por comprimento ou pelo teto de 1.000

Disparo: consulta recusada ou truncada pelo comprimento, ou retorno de exatamente 1.000. Forma, em ordem: (1) executar os blocos literais de EB2 e de EB3; (2) partir a faceta 🟦 em português e em inglês, com o resto idêntico; (3) subintervalos de anos. Unir por deduplicação, nunca por soma. Registrar a partição como adaptação. A emenda declara `- Execução: particionada` e escreve as partes literais.

#### Varredura da faceta 🟦 isolada — fora do corpus

Disparo: medir o custo da âncora 🟨 nesta base. Forma: a string da faceta 🟦 sozinha, com o filtro de ano, uma única vez. Amostrar e classificar à mão os registros da faceta 🟦 fora de EB5; fração elegível acima do limite superior da faixa `sensibilidade` (`python3 -m rsl mostrar`) leva a emenda.

#### Partição por *Título*

Disparo: consulta que encosta no teto de 1.000 mesmo com o recorte temporal. Forma: repetir em *Título* para estimar o ruído do excedente. Nunca é forma de execução.

---

## 5. Conjunto-semente

Esperadas nesta base, conforme o protocolo. Estado de conferência em `data/sementes.json`; aferição em `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE1 | Alvarenga & Cristovão (2023) | — | — |
| SE5 | Sousa & Duque (2018) | `10.5433/1981-8920.2018v23n1p271` | **caso-teste de cobertura de campo**: o artefato está fora do título |

**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões; semente não indexada sai do denominador e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação por DOI e depois por título, sem reexecutar a busca.

**Limiar de aderência** (`limiar_aderencia`, `python3 -m rsl mostrar`), sobre a união das bases. A aderência por base indica qual base e qual faceta falharam.

**Se a SE5 não aparecer.** Consultar `Duque` em *Local de pesquisa* = **Autor**, abrir o registro e ler resumo e palavras-chave.

| Achado | Leitura |
| :--- | :--- |
| o resumo ou as palavras-chave trazem `ontologia` | falha de campo, não de vocabulário |
| nem o resumo nem as palavras-chave trazem o termo | falha de vocabulário da faceta 🟦 |
| a consulta por `Duque` devolve zero | opção *Autor* inoperante ou registro não indexado: registrar antes de usar o campo no *backward search* |

---

## 6. Ressalvas

1. Alterar as consultas exige repetir as sondagens pertinentes da seção 1.
2. Todos os termos são **termos livres**; não apresentá-los como descritores autorizados.
3. No relato, declarar que o corpus desta base é a EB4, com o custo da âncora 🟨 medido pela sonda EB5 e pela varredura da faceta 🟦 isolada.
