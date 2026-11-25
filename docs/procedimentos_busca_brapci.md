# Strings de busca — BRAPCI

<!-- Gerado por `python3 -m rsl procedimentos gerar brapci --gravar` a partir de `docs/procedimentos/brapci`, do protocolo e do arquivo de sementes. Não editar: a edição à mão reprova em `documentos conferir`. -->

## 1. Estado de verificação da sintaxe

| Elemento | Categoria | Situação | Fonte | Sondagem |
| :--- | :--- | :--- | :--- | :--- |
| Aspas como frase | frase | **Não verificado** | — | SD2 |
| `AND`, `OR` e parênteses | operadores | **Não verificado** | — | SD1 |
| Truncamento `*` | truncamento | **Não verificado** | — | sem sondagem: não se usa |
| Lematização | lematizacao | **Não verificado**; flexões explícitas nas strings | — | SD3 |
| Comprimento máximo da consulta | limite_consulta | **Não verificado**; a maior consulta executável é medida por `python3 -m rsl documentos conferir`, no relato do teto de caracteres | — | SD4 |
| Proximidade | proximidade | **Não verificado** | — | sem sondagem: nenhuma consulta usa proximidade |
| Exportação — formatos e lote | exportacao | **Não verificado** | — | SD8 |
| Local de pesquisa | campos | **Não verificado** | — | SD5 |
| Campos diferentes na mesma consulta | campos | **Não verificado** | — | SD5 |
| Filtros | filtros | **Não verificado** | — | SD6 |
| Teto de exibição | limite_retorno | **Não verificado**; retorno de exatamente 1.000 será tratado como **corte** até medir | — | SD7 |
| Parênteses para agrupamento | agrupamento | **Não verificado** | — | SD1 |
| Teto de exportação por lote | limite_exportacao | **Não verificado** | — | SD8 |
| Vocabulário controlado de assunto | vocabulario_controlado | **Não verificado** | — | sem sondagem: verificação documental: a BRAPCI não foi conferida quanto a vocabulário de assunto; nenhuma consulta depende dele |
| Idioma do título, do resumo e das palavras-chave indexados | idioma_indexacao | **Não verificado** | — | SD9 |

Sintaxe não documentada em fonte alguma: **não verificada por medição** — sondar pelas sondagens abaixo e registrar cada uma.

**Regra de execução, para toda consulta deste procedimento de busca.**

1. Aplicar o filtro de ano **antes** de executar.
2. Manter **Local de pesquisa = Todos os campos**.
3. Usar o método de busca **ponderado**; registrar o método, o Local de pesquisa e o limite de resultados (1.000 a 5.000).
4. Não usar o filtro de tipo de publicação.
5. Anotar o retorno de cada consulta.
6. Retorno de 1.000: consulta truncada; partir conforme a variante "Partição".

**Outros campos do seletor**, só como instrumento: *Título*, para precisão e partição; *Resumo* e *Palavras-chave*, para medir onde a base indexa; *Autor*, para *backward search* e conferência de duplicatas.

### Sondagens a executar

Uma consulta por vez, sem nova tentativa automática; parar diante de captcha, aviso de atividade atípica ou bloqueio, e registrar.

#### SD1 — saber se `AND`, `OR` e os parênteses se comportam como booleanos

**Elementos verificados:** `AND`, `OR` e parênteses (Não verificado); Parênteses para agrupamento (Não verificado).

**Pré-requisitos.**

- busca da BRAPCI aberta no navegador do pesquisador, com Local de pesquisa = Todos os campos e método ponderado

**Consulta 1 — controle**, em caixa de busca.

```
ontologia
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: conjunção com `AND`.

```
ontologia AND educação
```

**Consulta 3 — teste**, em caixa de busca. Muda em relação ao controle: disjunção com `OR`.

```
ontologia OR taxonomia
```

**Consulta 4 — teste**, em caixa de busca. Muda em relação ao controle: grupo entre parênteses.

```
(ontologia OR taxonomia) AND educação
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno exibido
2. abrir três registros do primeiro teste e conferir se trazem as duas palavras

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < `AND` < controle ≤ `OR`, 0 < grupo ≤ `OR`, e os registros abertos trazem as duas palavras | os operadores e os parênteses se comportam como booleanos | Verificado por medição |
| 2 | qualquer outra relação, ou mensagem de erro | não se confirma o comportamento booleano; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD2 — saber se as aspas exigem a sequência exata das palavras

**Elementos verificados:** Aspas como frase (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com os operadores verificados

**Consulta 1 — controle**, em caixa de busca.

```
organização AND conhecimento
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: a locução entre aspas.

```
"organização do conhecimento"
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno
2. abrir três registros do controle que não estejam no teste e conferir se trazem as palavras separadas

**Observar.**

- retorno exibido de cada consulta

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < teste < controle, e os registros só do controle trazem as palavras separadas | as aspas exigem a sequência exata | Verificado por medição |
| 2 | teste = controle, ou teste = 0 | não se distingue o efeito das aspas; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD3 — saber se a base casa singular e plural sem que a consulta os traga

**Elementos verificados:** Lematização (Não verificado).
**Depende de:** SD2.

**Pré-requisitos.**

- SD2 registrada com as aspas verificadas

**Consulta 1 — controle**, em caixa de busca.

```
"ontologia"
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o plural no lugar do singular.

```
"ontologias"
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno
2. abrir três registros do teste e conferir se trazem só o plural

**Observar.**

- retorno exibido de cada consulta
- forma do termo nos registros abertos

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste ≠ controle, e os registros abertos trazem só o plural | a base não lematiza em português: as flexões explícitas são necessárias | Verificado por medição |
| 2 | teste = controle, ou registros com só o singular | pode haver lematização; levar ao pesquisador antes de declarar `pela lematização` | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD4 — saber se a base aceita inteira a consulta longa

**Elementos verificados:** Comprimento máximo da consulta (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com os operadores verificados
- o procedimento gerado, para copiar as consultas

**Consulta 1 — teste**, em caixa de busca.

```
o bloco de EB5 no procedimento gerado
```

**Consulta 2 — controle**, em caixa de busca.

```
a primeira metade da faceta 🟦 AND a faceta 🟨, copiadas do procedimento gerado
```

**Consulta 3 — controle**, em caixa de busca.

```
a segunda metade da faceta 🟦 AND a faceta 🟨, copiadas do procedimento gerado
```

**Passos.**

1. submeter o bloco de EB5 da seção 4 e anotar o retorno
2. partir a faceta 🟦 em duas metades, cada metade com a faceta 🟨, submeter as duas e anotar os retornos
3. comparar o retorno de EB5 com a união das metades

**Observar.**

- retorno exibido de cada consulta
- se o texto mostrado depois da submissão é a consulta inteira

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | EB5 ≥ cada metade, e o texto mostrado é a consulta inteira | a base aceita a consulta longa inteira | Verificado por medição |
| 2 | EB5 < alguma metade, texto cortado, ou mensagem de erro | a consulta longa não é aceita inteira; levar ao pesquisador (variante "Partição") | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com o fim da consulta e o retorno visíveis

#### SD5 — saber o que o seletor Local de pesquisa restringe e se uma consulta combina campos diferentes

**Elementos verificados:** Local de pesquisa (Não verificado); Campos diferentes na mesma consulta (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com os operadores verificados

**Consulta 1 — controle**, em caixa de busca, Local de pesquisa = Todos os campos.

```
"ontologia"
```

**Consulta 2 — teste**, em caixa de busca, Local de pesquisa = Título. Muda em relação ao controle: o Local de pesquisa.

```
"ontologia"
```

**Passos.**

1. submeter a mesma consulta com Local de pesquisa = Todos os campos e depois = Título, e anotar os retornos
2. abrir três registros da busca em Título e conferir o termo no título
3. conferir se a interface oferece mais de um campo na mesma consulta e anotar como

**Observar.**

- retorno exibido de cada consulta
- presença do termo no título
- opções do seletor

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < teste < controle, os registros abertos têm o termo no título, e a combinação de campos está anotada | o Local de pesquisa restringe; a combinação de campos fica descrita | Verificado por medição |
| 2 | teste = controle, teste = 0, ou registro sem o termo no título | não se distingue o efeito do seletor; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta e do seletor

#### SD6 — saber se o filtro de ano recorta o retorno

**Elementos verificados:** Filtros (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com os operadores verificados

**Consulta 1 — controle**, em caixa de busca, sem filtro de ano.

```
"ontologia"
```

**Consulta 2 — teste**, em caixa de busca, filtro de ano 2017 a 2026. Muda em relação ao controle: o filtro de ano.

```
"ontologia"
```

**Passos.**

1. submeter a consulta sem filtro e anotar o retorno
2. aplicar o filtro de ano 2017 a 2026 antes de executar, submeter de novo e anotar o retorno
3. conferir o ano de dez registros do teste

**Observar.**

- retorno exibido de cada consulta
- ano dos registros conferidos
- rótulo do filtro

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < teste < controle, e os registros conferidos estão entre 2017 e 2026 | o filtro de ano recorta o retorno | Verificado por medição |
| 2 | teste = controle, ou registro conferido fora do intervalo | o filtro de ano não se confirma; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com o filtro e o retorno visíveis

#### SD7 — saber se a base corta o retorno em 1.000 ou no limite de resultados escolhido

**Elementos verificados:** Teto de exibição (Não verificado).

**Pré-requisitos.**

- busca da BRAPCI aberta no navegador do pesquisador

**Consulta 1 — controle**, em caixa de busca, limite de resultados 1.000.

```
educação
```

**Consulta 2 — teste**, em caixa de busca, limite de resultados 5.000. Muda em relação ao controle: o limite de resultados.

```
educação
```

**Passos.**

1. submeter a consulta com o limite de resultados em 1.000 e anotar o retorno
2. repetir com o limite em 5.000 e anotar o retorno

**Observar.**

- retorno exibido de cada consulta
- aviso de limite, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | controle = 1.000 e teste > 1.000 | o retorno é cortado no limite de resultados escolhido | Verificado por medição |
| 2 | controle = teste < 1.000 | a consulta não alcança o teto; repetir com consulta mais larga | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com o limite e o retorno visíveis

#### SD8 — saber em que formatos e com quantos registros por vez a base exporta

**Elementos verificados:** Exportação — formatos e lote (Não verificado); Teto de exportação por lote (Não verificado).

**Pré-requisitos.**

- busca da BRAPCI aberta no navegador do pesquisador

**Consulta 1 — teste**, em caixa de busca.

```
"ontologia" AND "educação"
```

**Passos.**

1. submeter a consulta e anotar o retorno
2. abrir a exportação e anotar os formatos e o número máximo de registros
3. exportar uma vez em RIS ou BibTeX e contar os registros do arquivo

**Observar.**

- formatos oferecidos
- número máximo de registros
- número de registros no arquivo

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | o arquivo traz todos os registros do retorno, no formato escolhido | a exportação funciona no formato anotado, sem teto até esse tamanho | Verificado por medição |
| 2 | o arquivo traz menos registros que o retorno, no número que a exportação anuncia | há teto de exportação por lote, no número anotado | Verificado por medição |
| 3 | não há exportação, ou ela falha | sem exportação utilizável; registrar no Zotero e levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela da opção de exportação
- o arquivo exportado

#### SD9 — saber se os registros trazem título, resumo e palavras-chave também em inglês, buscáveis pela faceta 🟦 em inglês

**Elementos verificados:** Idioma do título, do resumo e das palavras-chave indexados (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com os operadores verificados

**Consulta 1 — controle**, em caixa de busca.

```
"ontologia"
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o termo em inglês.

```
"ontology"
```

**Passos.**

1. submeter cada consulta e anotar o retorno
2. abrir três registros do teste e anotar em que idioma estão título, resumo e palavras-chave

**Observar.**

- retorno exibido de cada consulta
- idiomas dos campos nos registros abertos

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste > 0, e os registros abertos trazem o resumo ou as palavras-chave em inglês | a base indexa campos em inglês; a faceta 🟦 em inglês alcança registros | Verificado por medição |
| 2 | teste = 0, ou registros só em português | não se confirma a indexação em inglês; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta e de cada registro aberto

---

## 2. Critérios de elegibilidade

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — 2017 até a data de execução | CE1 / CE2 | **No filtro da interface** | ano inicial 2017 e final 2026, antes de executar; conferir o ano no retorno |
| Idiomas — português, inglês e espanhol | CE3 | **Dispensado** | strings em português, e em inglês na faceta 🟦; sem filtro de idioma |
| Tipo documental | CE4 / CE5 | **Não** | filtro de tipo não usado |
| Adequação temática — regra de inclusão | CE6 | Aproximado | EB4 exige termo de prática (STR3) ou de fator situacional (STR4); a formalização se decide na triagem |
| Adequação temática — não pertinência e contra-escopo | CE6 | **Não** | exclusões temáticas manifestas na 2ª filtragem; aplicação integral na 3ª, com justificativa por ID |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, por âncora | faceta 🟨 (FCT2) nas cinco expressões |
| Outros tipos documentais | CE9 | **Não** | 2ª filtragem |
| Fator de impacto — não aplicável | CE10 | **Não** | não se aplica: critério só documental |

---

## 3. Strings por faceta

`STRn` é o identificador do protocolo e `#n` o número da string na composição. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

### Declaração de cobertura

Declarada em `docs/procedimentos/brapci/procedimento.toml`, `[cobertura]`; conferida por `python3 -m rsl documentos conferir`.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: pt, en; FCT2: pt; FCT3: pt; FCT4: pt |
| plural | explícito |
| teto de caracteres | nenhum |
| derivações | morfologia |

### `STR1` — string `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies")
```

### `STR2` — string `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

```
("educacional" OR "educacionais" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação")
```

### `STR3` — string `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
("prática educacional" OR "práticas educacionais" OR "método de ensino" OR "métodos de ensino" OR "estratégia educacional" OR "estratégias educacionais" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais")
```

### `STR4` — string `#4` — 🟧 FCT4 — Fatores situacionais

```
("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais")
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
| **EB1**, **EB2**, **EB3** | não executar; derivação local |

- Execução: única
- **Sensibilidade:** fração elegível de `EB5 \ EB4` abaixo do limite inferior da faixa `sensibilidade` (`python3 -m rsl configuracao mostrar`) mantém EB4; acima do superior, leva à reconsideração, com emenda.
- **Retorno zero:** EB4 = 0 ou EB5 = 0 é defeito de execução até prova em contrário; contagem derivada próxima de zero exige execução direta antes do relato.

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
("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies") AND ("educacional" OR "educacionais" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação") AND (("prática educacional" OR "práticas educacionais" OR "método de ensino" OR "métodos de ensino" OR "estratégia educacional" OR "estratégias educacionais" OR "atividade de aprendizagem" OR "atividades de aprendizagem" OR "intervenção educacional" OR "intervenções educacionais") OR ("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais"))
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨)

```
("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies") AND ("educacional" OR "educacionais" OR "ensino-aprendizagem" OR "ensino-aprendizagens" OR "ensino e aprendizagem" OR "educação")
```

### Como executar

1. Aplicar a regra de execução da seção 1.
2. **Sondar o comprimento.** Submeter o bloco de EB5 da seção 4 e conferir que foi aceito inteiro, comparando o retorno com o da faceta 🟦 partida em metades, cada metade com a faceta 🟨. Registrar a sondagem.
3. Executar o bloco de EB4 como está. Retorno de exatamente 1.000: partir, conforme as variantes.
4. Executar EB5 uma única vez, na mesma data.
5. Exportar em RIS ou BibTeX; sem exportação, registrar os metadados no Zotero e anotar a entrada manual como risco de transcrição.
6. Registrar: `python3 -m rsl busca registrar brapci EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`, com a justificativa do teto de 1.000 quando for o caso; rodar `busca derivar` e `conferencia sensibilidade`.
7. Medir a aderência (seção 5).

### Variantes previstas

#### Partição — por comprimento ou pelo teto de 1.000

Disparo: consulta recusada ou truncada pelo comprimento, ou retorno de exatamente 1.000. Forma, em ordem: (1) executar os blocos literais de EB2 e de EB3; (2) partir a faceta 🟦 em português e em inglês, com o resto idêntico; (3) subintervalos de anos. Unir por deduplicação, nunca por soma. Registrar a partição como adaptação. A emenda declara `- Execução: particionada` e escreve as partes literais.

#### Varredura da faceta 🟦 isolada — fora do corpus

Disparo: medir o custo da âncora 🟨 nesta base. Forma: a string da faceta 🟦 sozinha, com o filtro de ano, uma única vez. Amostrar e classificar à mão os registros da faceta 🟦 fora de EB5; fração elegível acima do limite superior da faixa `sensibilidade` (`python3 -m rsl configuracao mostrar`) leva a emenda.

#### Partição por *Título*

Disparo: consulta que encosta no teto de 1.000 mesmo com o recorte temporal. Forma: repetir em *Título* para estimar o ruído do excedente. Nunca é forma de execução.

---

## 5. Conjunto-semente

Esperadas nesta base, conforme o protocolo. Estado de conferência no arquivo de sementes (`[documentos] sementes`); aferição em `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE1 | Alvarenga & Cristovão (2023) | `10.26512/rici.v16.n1.2023.47618` | — |
| SE5 | Sousa & Duque (2018) | `10.5433/1981-8920.2018v23n1p271` | **caso-teste de cobertura de campo**: o artefato está fora do título |

**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões; semente não indexada sai do denominador e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação de EB4 por DOI e depois por título, sem reexecutar a busca.

**Limiar de aderência** (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`), sobre a união das bases. A aderência por base indica qual base e qual faceta falharam.

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
