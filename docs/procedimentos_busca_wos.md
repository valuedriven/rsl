# Strings de busca — Web of Science (Core Collection)

<!-- Gerado por `python3 -m rsl procedimentos gerar wos --gravar` a partir de `docs/procedimentos/wos`, do protocolo e do arquivo de sementes. Não editar: a edição à mão reprova em `documentos conferir`. -->

## 1. Estado de verificação da sintaxe

| Elemento | Categoria | Situação | Fonte | Sondagem |
| :--- | :--- | :--- | :--- | :--- |
| `TS=` — tópico: título, resumo, palavras-chave de autor e *Keywords Plus* | campos | Verificado em fonte oficial | Clarivate, *Advanced Search Field Tags* | — |
| `TI=`, `AB=`, `AK=`, `SO=`, `KP=`, `WC=`, `SU=`, `DO=`, `ALL=` | campos | Verificado em fonte oficial | Clarivate, *Advanced Search Field Tags* | — |
| `PY=` — ano de publicação; exige combinação com outra *tag* | filtros | Verificado em fonte oficial | Clarivate, *Advanced Search Field Tags* | — |
| `DT=` — tipo de documento | filtros | Verificado em fonte oficial | Clarivate, *Advanced Search Field Tags*, e FECYT (2024) | — |
| `LA=` — idioma | filtros | Verificado em fonte secundária | FECYT, *De la consulta simple a la compleja en Web of Science* (2024) | — |
| Truncamento `*`, `?`, `$`; mínimo de 3 caracteres antes do curinga; curinga desativa a lematização | truncamento | Verificado em fonte oficial | Clarivate, *Advanced Search examples* | — |
| Limite de 200 conjuntos de busca por sessão | limite_consulta | Verificado em fonte oficial | Clarivate, *Advanced Search examples* | — |
| Aspas desligam a lematização e o localizador interno de sinônimos | frase | Verificado por medição (BD1/sd3-2026-11-25); afirmado sem fonte na skill `auditoria-das-strings` até 2026-11-23; conferir também na documentação oficial | — | SD3 |
| Busca em todos os campos (`ALL=`) limitada a 49 operadores booleanos; os demais campos sem limite | limite_consulta | **Não verificado** | — | sem sondagem: nenhuma expressão usa `ALL=`; conferir na documentação oficial (afirmado sem fonte na skill `auditoria-das-strings` até 2026-11-23) |
| Intervalos de `PY=` de até 5 anos (recomendação) | filtros | Verificado em fonte oficial | Clarivate, *Advanced Search examples* | — |
| Filtro de texto completo em sintaxe de consulta | filtros | **Não existe** | ausência na página de *field tags* | — |
| Valores exatos admitidos em `DT=` e `LA=` | filtros | Verificado por medição (BD1/sd4-2026-11-25) | — | SD4 |
| `NEAR/x` entre grupos entre parênteses | proximidade | Verificado por medição (BD1/sd2-2026-11-25) | — | SD2 |
| Distância padrão de `NEAR` sem número | proximidade | Verificado por medição (BD1/sd2-2026-11-25) | — | SD2 |
| Comprimento máximo da consulta | limite_consulta | Verificado por medição (BD1/sd5-2026-11-25); a maior consulta executável é medida por `python3 -m rsl documentos conferir`, no relato do teto de caracteres | — | SD5 |
| Tratamento de diacríticos | idioma_indexacao | Verificado por medição (BD1/sd6-2026-11-25); medido só com `educação` (til e cedilha); acento agudo e `ñ` sem sondagem | — | SD6 |
| Teto de retorno exibido | limite_retorno | Verificado por medição (BD1/sd7-2026-11-25); a navegação só chega ao registro 100000 | — | SD7 |
| Teto de exportação por lote | limite_exportacao | Verificado por medição (BD1/sd8-2026-11-25); 1000 registros por lote | — | SD8 |
| Operadores booleanos `AND` e `OR` | operadores | Verificado por medição (BD1/sd1-2026-11-25) | — | SD1 |
| Parênteses para agrupamento | agrupamento | Verificado por medição (BD1/sd1-2026-11-25) | — | SD1 |
| Lematização | lematizacao | Verificado por medição (BD1/sd3-2026-11-25); medida só em inglês, com `ontology`/`ontologies`; português e espanhol sem sondagem, sem efeito na busca: todo termo vai entre aspas, que desligam a lematização (SD3), e o plural é explícito | — | SD3 |
| Vocabulário controlado de assunto | vocabulario_controlado | **Não verificado** | — | sem sondagem: verificação documental: a Core Collection não foi conferida quanto a tesauro de assunto; nenhuma expressão depende dele |
| Exportação em RIS com todos os campos | exportacao | Verificado por medição (BD1/sd8-2026-11-25) | — | SD8 |

As expressões usam `TS=`, `PY=`, `DT=` e `NEAR/5`. Valor de `DT=` recusado pela interface sai da consulta e vai ao refinamento, com a troca anotada no registro.

### Sondagens a executar

Uma consulta por vez, sem nova tentativa automática; parar diante de captcha, aviso de atividade atípica ou bloqueio, e registrar.

#### SD1 — saber se `AND`, `OR` e os parênteses dentro de `TS=` se comportam como booleanos

**Elementos verificados:** Operadores booleanos `AND` e `OR` (Verificado por medição); Parênteses para agrupamento (Verificado por medição).

**Pré-requisitos.**

- busca avançada da Web of Science Core Collection aberta no navegador do pesquisador, com o acesso institucional dele

**Consulta 1 — controle**, em busca avançada.

```
TS=(ontology)
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: conjunção com `AND`.

```
TS=(ontology AND education)
```

**Consulta 3 — teste**, em busca avançada. Muda em relação ao controle: disjunção com `OR`.

```
TS=(ontology OR taxonomy)
```

**Consulta 4 — teste**, em busca avançada. Muda em relação ao controle: grupo entre parênteses.

```
TS=((ontology OR taxonomy) AND education)
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno exibido

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < `AND` < controle ≤ `OR`, e 0 < grupo ≤ `OR` | os operadores e os parênteses se comportam como booleanos | Verificado por medição |
| 2 | qualquer outra relação, ou mensagem de erro | não se confirma o comportamento booleano; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela do histórico de busca, com as consultas e os retornos visíveis

**Resultados registrados.**

- (BD1/sd1-2026-11-25) 2026-11-25T16:50: leitura 1

#### SD2 — saber se `NEAR/5` é aceito entre grupos entre parênteses e qual é a distância de `NEAR` sem número

**Elementos verificados:** `NEAR/x` entre grupos entre parênteses (Verificado por medição); Distância padrão de `NEAR` sem número (Verificado por medição).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com operadores e parênteses verificados

**Consulta 1 — controle**, em busca avançada.

```
TS=((ontology OR taxonomy) AND (education OR learning))
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: `NEAR/5` no lugar de `AND`, entre grupos.

```
TS=((ontology OR taxonomy) NEAR/5 (education OR learning))
```

**Consulta 3 — teste**, em busca avançada. Muda em relação ao controle: `NEAR` sem número.

```
TS=(ontology NEAR education)
```

**Consulta 4 — teste**, em busca avançada. Muda em relação ao controle: `NEAR/15`, para comparar com `NEAR` sem número.

```
TS=(ontology NEAR/15 education)
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno exibido e a mensagem, se houver

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < primeiro teste ≤ controle, sem mensagem; `NEAR` sem número = `NEAR/15` | `NEAR/x` funciona entre grupos; a distância padrão é 15 | Verificado por medição |
| 2 | primeiro teste recusado ou = 0, ou `NEAR` sem número ≠ `NEAR/15` | a proximidade entre grupos ou a distância padrão não se confirma; levar ao pesquisador (variante de partição) | Não verificado |

**Evidência a registrar.**

- captura da tela do histórico de busca, com as consultas e os retornos visíveis

**Resultados registrados.**

- (BD1/sd2-2026-11-25) 2026-11-25T16:50: leitura 1

#### SD3 — saber se a base casa singular e plural sem que a consulta os traga, e se as aspas desligam isso

**Elementos verificados:** Lematização (Verificado por medição); Aspas desligam a lematização e o localizador interno de sinônimos (Verificado por medição).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com operadores e parênteses verificados

**Consulta 1 — controle**, em busca avançada.

```
TS=(ontology)
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: o plural no lugar do singular.

```
TS=(ontologies)
```

**Consulta 3 — teste**, em busca avançada. Muda em relação ao controle: o termo entre aspas.

```
TS=("ontology")
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno exibido

**Observar.**

- retorno exibido de cada consulta

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | controle = plural, e o termo entre aspas < controle | a base lematiza em inglês e as aspas desligam a lematização | Verificado por medição |
| 2 | controle ≠ plural, e o termo entre aspas = controle | a base não lematiza em inglês; as aspas não mudam o número | Verificado por medição |
| 3 | qualquer outra relação | não se distingue a lematização; levar ao pesquisador antes de declarar `pela lematização` | Não verificado |

**Evidência a registrar.**

- captura da tela do histórico de busca, com as consultas e os retornos visíveis

**Resultados registrados.**

- (BD1/sd3-2026-11-25) 2026-11-25T16:50: leitura 1

#### SD4 — saber se os valores de `DT=` e `LA=` usados no procedimento são aceitos

**Elementos verificados:** Valores exatos admitidos em `DT=` e `LA=` (Verificado por medição).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com operadores e parênteses verificados

**Consulta 1 — controle**, em busca avançada.

```
TS=(ontology)
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: o filtro de tipo de documento.

```
TS=(ontology) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

**Consulta 3 — teste**, em busca avançada. Muda em relação ao controle: a sondagem mínima de idioma.

```
TS=(ontology) AND LA=Portuguese
```

**Consulta 4 — teste**, em busca avançada. Muda em relação ao controle: o filtro de idioma da consulta.

```
TS=(ontology) AND LA=(English OR Portuguese OR Spanish)
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno e a mensagem, se houver
2. conferir cada valor na lista de refinamento da interface

**Observar.**

- retorno exibido de cada consulta
- valores na lista de refinamento de tipo de documento e de idioma

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | todos os testes aceitos, 0 < teste < controle, e cada valor presente na lista de refinamento | os valores de `DT=` e `LA=` são aceitos | Verificado por medição |
| 2 | algum teste recusado, = 0, ou valor ausente da lista | algum valor não é aceito; tirá-lo da consulta e levar ao refinamento, com a troca anotada | Não verificado |
| 3 | controle = 0, teste ≥ controle sem mensagem, ou listas de refinamento não conferidas | não se distingue se os valores são aceitos; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela do histórico de busca e das listas de refinamento

**Resultados registrados.**

- (BD1/sd4-2026-11-25) 2026-11-25T18:03: leitura 1

#### SD5 — saber se a interface aceita inteira a consulta de EB4

**Elementos verificados:** Comprimento máximo da consulta (Verificado por medição).
**Depende de:** SD2.

**Pré-requisitos.**

- SD2 registrada com a proximidade entre grupos verificada

**Consulta 1 — teste**, em busca avançada. Texto de EB4, 2.655 caracteres.

```
TS=(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") NEAR/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação" OR "educational" OR "teaching-learning" OR "teaching and learning" OR "education" OR "enseñanza-aprendizaje" OR "enseñanza-aprendizajes" OR "enseñanza y aprendizaje" OR "educación")) AND (TS=("prática educacional" OR "práticas educacionais" OR "método de ensino" OR "métodos de ensino" OR "estratégia educacional" OR "estratégias educacionais" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais" OR "educational practice" OR "educational practices" OR "teaching method" OR "teaching methods" OR "educational strategy" OR "educational strategies" OR "learning activity" OR "learning activities" OR "educational intervention" OR "educational interventions" OR "práctica educativa" OR "prácticas educativas" OR "estrategia educativa" OR "estrategias educativas" OR "actividad de aprendizaje" OR "actividades de aprendizaje" OR "intervención educativa" OR "intervenciones educativas" OR "método de enseñanza" OR "métodos de enseñanza") OR TS=("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais" OR "ambientes educacionales" OR "fatores de rendimento escolar" OR "fator de rendimento escolar" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "situational factor" OR "situational factors" OR "educational environment" OR "educational environments" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor situacional" OR "factores situacionales" OR "entorno educativo" OR "entornos educativos")) AND PY=(2017-2026) AND LA=(English OR Portuguese OR Spanish) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

**Passos.**

1. anotar o número de caracteres, que está na linha que precede a consulta
2. submeter a consulta e anotar o retorno e a mensagem, se houver

**Observar.**

- retorno exibido
- mensagem de erro ou de recusa, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | aceita, com retorno > 0 | a interface aceita a consulta de EB4 inteira; a execução única se mantém | Verificado por medição |
| 2 | recusa por extensão, ou retorno = 0 | a consulta passa do limite; levar ao pesquisador (variante de partição e teto) | Não verificado |

**Evidência a registrar.**

- captura da tela do histórico de busca, com a consulta e o retorno visíveis

**Resultados registrados.**

- (BD1/sd5-2026-11-25) 2026-11-25T18:58: leitura 1

#### SD6 — saber se a base ignora diacríticos

**Elementos verificados:** Tratamento de diacríticos (Verificado por medição).
**Depende de:** SD3.

**Pré-requisitos.**

- SD3 registrada, porque as aspas entram na consulta

**Consulta 1 — controle**, em busca avançada.

```
TS=("educação")
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: sem diacrítico.

```
TS=("educacao")
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

- captura da tela do histórico de busca, com as consultas e os retornos visíveis

**Resultados registrados.**

- (BD1/sd6-2026-11-25) 2026-11-25T18:58: leitura 1

#### SD7 — saber se a base exibe e deixa percorrer o retorno inteiro de uma busca larga

**Elementos verificados:** Teto de retorno exibido (Verificado por medição).

**Pré-requisitos.**

- busca avançada da Web of Science Core Collection aberta no navegador do pesquisador

**Consulta 1 — teste**, em busca avançada.

```
TS=(education)
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

**Resultados registrados.**

- (BD1/sd7-2026-11-25) 2026-11-25T18:58: leitura 2

#### SD8 — saber quantos registros a base exporta de uma vez em RIS com todos os campos

**Elementos verificados:** Teto de exportação por lote (Verificado por medição); Exportação em RIS com todos os campos (Verificado por medição).

**Pré-requisitos.**

- busca avançada da Web of Science Core Collection aberta no navegador do pesquisador

**Consulta 1 — teste**, em busca avançada.

```
TS=(ontology AND education)
```

**Passos.**

1. submeter a consulta e anotar o retorno
2. abrir a exportação em RIS com todos os campos e anotar o número máximo de registros por lote que ela aceita
3. exportar um lote e contar os registros do arquivo

**Observar.**

- número máximo por lote oferecido pela exportação
- número de registros no arquivo
- campos presentes no arquivo (resumo, palavras-chave)

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | o arquivo traz o número de registros pedido, com resumo e palavras-chave, e a exportação anuncia o máximo por lote | a exportação em RIS com todos os campos funciona, com o teto por lote anotado | Verificado por medição |
| 2 | a exportação falha, o arquivo vem sem resumo ou o número não corresponde ao pedido | não se confirma a exportação; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela da opção de exportação
- o arquivo exportado

**Resultados registrados.**

- (BD1/sd8-2026-11-25) 2026-11-25T19:12: leitura 1

---

## 2. Critérios de elegibilidade

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — 2017 até a data de execução | CE1 / CE2 | **Sim** | `AND PY=(2017-2026)` |
| Idiomas — português, inglês e espanhol | CE3 | **Sim** | `AND LA=(English OR Portuguese OR Spanish)` |
| Tipo documental | CE4 / CE5 | **Sim** | `AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")` |
| Adequação temática — regra de inclusão | CE6 | Aproximado | EB4 exige termo de prática (STR3) ou de fator situacional (STR4); a formalização se decide na triagem |
| Adequação temática — não pertinência e contra-escopo | CE6 | **Não** | exclusões temáticas manifestas na 2ª filtragem; aplicação integral na 3ª, com justificativa por ID |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, por âncora | faceta 🟨 (FCT2) nas cinco expressões |
| Outros tipos documentais | CE9 | **Não** | 2ª filtragem |
| Fator de impacto — não aplicável | CE10 | **Não** | não se aplica: critério só documental |

---

## 3. Strings por faceta

`STRn` é o identificador do protocolo e `#n` o número da string na composição. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

### Declaração de cobertura

Declarada em `docs/procedimentos/wos/procedimento.toml`, `[cobertura]`; conferida por `python3 -m rsl documentos conferir`.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: pt, en, es; FCT2: pt, en, es; FCT3: pt, en, es; FCT4: pt, en, es |
| plural | explícito |
| teto de caracteres | nenhum |
| derivações | morfologia |

### `STR1` — string `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
TS=("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías")
```

### `STR2` — string `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

```
TS=("educacional" OR "educacionais" OR "educacionales" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação" OR "educational" OR "teaching-learning" OR "teaching and learning" OR "education" OR "enseñanza-aprendizaje" OR "enseñanza-aprendizajes" OR "enseñanza y aprendizaje" OR "educación")
```

### `STR3` — string `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
TS=("prática educacional" OR "práticas educacionais" OR "método de ensino" OR "métodos de ensino" OR "estratégia educacional" OR "estratégias educacionais" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais" OR "educational practice" OR "educational practices" OR "teaching method" OR "teaching methods" OR "educational strategy" OR "educational strategies" OR "learning activity" OR "learning activities" OR "educational intervention" OR "educational interventions" OR "práctica educativa" OR "prácticas educativas" OR "estrategia educativa" OR "estrategias educativas" OR "actividad de aprendizaje" OR "actividades de aprendizaje" OR "intervención educativa" OR "intervenciones educativas" OR "método de enseñanza" OR "métodos de enseñanza")
```

### `STR4` — string `#4` — 🟧 FCT4 — Fatores situacionais

```
TS=("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais" OR "ambientes educacionales" OR "fatores de rendimento escolar" OR "fator de rendimento escolar" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "situational factor" OR "situational factors" OR "educational environment" OR "educational environments" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor situacional" OR "factores situacionales" OR "entorno educativo" OR "entornos educativos")
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
TS=(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") NEAR/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação" OR "educational" OR "teaching-learning" OR "teaching and learning" OR "education" OR "enseñanza-aprendizaje" OR "enseñanza-aprendizajes" OR "enseñanza y aprendizaje" OR "educación")) AND TS=("prática educacional" OR "práticas educacionais" OR "método de ensino" OR "métodos de ensino" OR "estratégia educacional" OR "estratégias educacionais" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais" OR "educational practice" OR "educational practices" OR "teaching method" OR "teaching methods" OR "educational strategy" OR "educational strategies" OR "learning activity" OR "learning activities" OR "educational intervention" OR "educational interventions" OR "práctica educativa" OR "prácticas educativas" OR "estrategia educativa" OR "estrategias educativas" OR "actividad de aprendizaje" OR "actividades de aprendizaje" OR "intervención educativa" OR "intervenciones educativas" OR "método de enseñanza" OR "métodos de enseñanza") AND PY=(2017-2026) AND LA=(English OR Portuguese OR Spanish) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### EB3 (artefatos que formalizam os fatores situacionais do domínio educacional)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧)

```
TS=(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") NEAR/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação" OR "educational" OR "teaching-learning" OR "teaching and learning" OR "education" OR "enseñanza-aprendizaje" OR "enseñanza-aprendizajes" OR "enseñanza y aprendizaje" OR "educación")) AND TS=("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais" OR "ambientes educacionales" OR "fatores de rendimento escolar" OR "fator de rendimento escolar" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "situational factor" OR "situational factors" OR "educational environment" OR "educational environments" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor situacional" OR "factores situacionales" OR "entorno educativo" OR "entornos educativos") AND PY=(2017-2026) AND LA=(English OR Portuguese OR Spanish) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### EB4 (de cobertura restrita — artefatos de representação no domínio educacional que mencionam prática ou fator situacional)

*Executada e exportada nesta base.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧))

```
TS=(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") NEAR/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação" OR "educational" OR "teaching-learning" OR "teaching and learning" OR "education" OR "enseñanza-aprendizaje" OR "enseñanza-aprendizajes" OR "enseñanza y aprendizaje" OR "educación")) AND (TS=("prática educacional" OR "práticas educacionais" OR "método de ensino" OR "métodos de ensino" OR "estratégia educacional" OR "estratégias educacionais" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais" OR "educational practice" OR "educational practices" OR "teaching method" OR "teaching methods" OR "educational strategy" OR "educational strategies" OR "learning activity" OR "learning activities" OR "educational intervention" OR "educational interventions" OR "práctica educativa" OR "prácticas educativas" OR "estrategia educativa" OR "estrategias educativas" OR "actividad de aprendizaje" OR "actividades de aprendizaje" OR "intervención educativa" OR "intervenciones educativas" OR "método de enseñanza" OR "métodos de enseñanza") OR TS=("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais" OR "ambientes educacionales" OR "fatores de rendimento escolar" OR "fator de rendimento escolar" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "situational factor" OR "situational factors" OR "educational environment" OR "educational environments" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor situacional" OR "factores situacionales" OR "entorno educativo" OR "entornos educativos")) AND PY=(2017-2026) AND LA=(English OR Portuguese OR Spanish) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨)

```
TS=(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") NEAR/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação" OR "educational" OR "teaching-learning" OR "teaching and learning" OR "education" OR "enseñanza-aprendizaje" OR "enseñanza-aprendizajes" OR "enseñanza y aprendizaje" OR "educación")) AND PY=(2017-2026) AND LA=(English OR Portuguese OR Spanish) AND DT=(Article OR Review OR "Proceedings Paper" OR "Book Chapter")
```

### Como executar

1. Conferir a sessão contra a seção 1, na primeira execução do dia.
2. Submeter o bloco de EB4 da seção 4 como está, sem definir conjunto e sem montar arquivo. Na primeira execução, conferir se a interface aceita a consulta inteira; recusa por extensão leva à variante "Partição por recusa da proximidade ou do comprimento", registrada como adaptação.
3. Exportar em RIS, com todos os campos, em lotes dentro do limite da base.
4. Conferir o retorno da exportação contra o da tela.
5. Registrar EB4 e EB5: `python3 -m rsl busca registrar wos EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`; rodar `busca derivar` e `conferencia sensibilidade`.
6. Medir a aderência ao conjunto-semente (seção 5). Semente não recuperada: `python3 -m rsl aderencia diagnosticar wos`, que exige `[composicao] doi` na fonte.

### Variantes previstas

#### Partição por recusa da proximidade ou do comprimento

Disparo: a interface recusa o bloco executado por proximidade entre grupos deste tamanho ou por extensão. Forma: partir o grupo 🟦 em subconjuntos, cada um com o grupo 🟨 inteiro, repetindo os filtros em cada parte, e unir por deduplicação. Registrar a partição como adaptação. A emenda declara `- Execução: particionada` e escreve as partes literais.

#### Fracionamento do intervalo temporal

Disparo: execução em bloco falha ou trunca o retorno. Forma: repetir a expressão com cada faixa, unir por deduplicação e registrar o retorno de cada faixa.

```
AND PY=(2017-2021)
AND PY=(2022-2026)
```

#### Idioma recusado

Disparo: a interface recusa algum valor de `LA=` da consulta, ou o valor some da lista de refinamento. Forma: tirar o valor da cláusula, aplicar o limite por refinamento de idioma, anotar a troca no registro e repetir a SD4.

#### Truncamento

Não usar curinga. Disparo: aderência abaixo do limiar de aderência (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`). Forma: testar `ontolog*`, `educat*`, `contextualiz*`; a adoção exige emenda.

#### Camada de precisão

Disparo: retorno alto demais para a triagem. Aplicar nesta ordem, medindo cada passo contra o conjunto-semente:

1. reduzir a distância de `NEAR/5` entre as âncoras;
2. passar a faceta 🟨 para `AK=` ou `TI=`, mantendo a 🟦 em `TS=`:

```
TS=(<faceta 1>) AND AK=(<faceta 2>) AND PY=(2017-2026)
```

3. refinar por categoria, conferindo os rótulos na interface; declarar a restrição no relatório e compensá-la por *backward search* de uma geração:

```
AND WC=("Education & Educational Research" OR "Education, Scientific Disciplines" OR "Information Science & Library Science" OR "Computer Science, Artificial Intelligence" OR "Computer Science, Information Systems" OR "Computer Science, Interdisciplinary Applications" OR "Computer Science, Theory & Methods")
```

Regra: camada com aderência abaixo do limiar de aderência (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`) é reprovada. Não acrescentar facetas a EB4 para reduzir o retorno.

---

## 5. Conjunto-semente

Esperadas nesta base, conforme o protocolo. Estado de conferência e indexação declarada (`bases`) no arquivo de sementes (`[documentos] sementes`); recuperação medida por `python3 -m rsl aderencia medir`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE2 | Das, Naskar & Roy (2022) | `10.5771/0943-7444-2022-1-6` | — |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE9 | Piriyapongpipat, Goldin & Ditcharoen (2024) | `10.1186/s40561-024-00307-8` | — |
| SE10 | Khoo & Kan (2020) | `10.5771/9783956507762-484` | caso-teste de cobertura de campo; DOI do capítulo |
| SE13 | Hernández-Carrasco et al. (2022) | `10.3390/math10091355` | — |
| SE14 | Nunes Passos et al. (2024) | `10.15628/holos.2023.10328` | — |
| SE15 | Griful-Freixenet, Struyven & Vantieghem (2021) | `10.1177/0022487120965525` | — |
| SE17 | Hickey & Riddle (2024) | `10.1080/13603116.2023.2259906` | — |

**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões; semente não indexada sai do denominador e se registra no campo `bases` do arquivo de sementes. *Etapa 2:* `aderencia medir` procura a semente na exportação de EB4 pelo DOI e pelo título, sem reexecutar a busca.

**Limiar de aderência** (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`), sobre a união das bases. A aderência por base indica qual base e qual faceta falharam.

**SE10.** O domínio está fora do título; anotar no registro se EB4 a recupera.

**Anatomia da perda.** A causa da perda não se atribui a olho:
`python3 -m rsl aderencia diagnosticar <sigla>` monta, da composição desta base, as
consultas por nível com os DOIs das sementes não recuperadas, lê da execução registrada os
níveis que já a têm e atribui a causa pelo primeiro nível em que o DOI desaparece — não
indexada, filtro, âncoras, proximidade ou faceta não âncora. O comando exige que a fonte
declare `[composicao] doi`; sem a declaração, recusa e nomeia o campo.

---

## 6. Ressalvas

1. Todos os termos são **termos livres**; não apresentá-los como descritores autorizados.
2. **`LA=`** vai na consulta, porque os valores English, Portuguese e Spanish foram aceitos (BD1/sd4-2026-11-25); valor recusado leva à variante "Idioma recusado".
3. **Texto completo** não é filtro de busca nesta base: o critério opera na 2ª filtragem.
4. **Teses e dissertações** não são cobertas pela Core Collection: ficam a cargo da BRAPCI e, se necessário, da BDTD.
