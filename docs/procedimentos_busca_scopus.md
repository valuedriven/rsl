# Strings de busca — Scopus

<!-- Gerado por `python3 -m rsl procedimentos gerar scopus --gravar` a partir de `docs/procedimentos/scopus`, do protocolo e do arquivo de sementes. Não editar: a edição à mão reprova em `documentos conferir`. -->

## 1. Estado de verificação da sintaxe

| Elemento | Categoria | Situação | Fonte | Sondagem |
| :--- | :--- | :--- | :--- | :--- |
| `TITLE-ABS-KEY()` | campos | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| Restrição por DOI: `DOI(<DOI>)` | campos | Verificado em fonte oficial; código `DOI` na tabela de códigos de campo da busca avançada: `DOI(10.1007/s00202-004-0261-3)` devolve o documento com esse DOI (https://www.elsevier.support/scopus/answer/how-can-i-best-use-the-advanced-search, atualizada em 2026-08-24, consultada em 2026-11-26); é a forma da restrição por DOI do diagnóstico da perda. O agrupamento de vários `DOI()` por `OR` não está medido | Elsevier, *How can I best use the Advanced search?* (Scopus Support Center) | — |
| `PUBYEAR >`, `<`, `=` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `LANGUAGE()` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `DOCTYPE()` com os códigos `ar`, `re`, `cp`, `ch`, `bk`, `ed`, `le`, `no`, `sh` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `SRCTYPE()` com `j`, `b`, `k`, `p`, `r`, `d` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `OPENACCESS(0` ou `1)` | filtros | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| `AND`, `OR`, `AND NOT`; precedência `OR` → `AND` → `AND NOT` | operadores | Verificado em fonte oficial; a precedência muda em 2026 | Elsevier, *Scopus Search API — search tips* | — |
| Truncamento `*` e `?`, mínimo de 3 caracteres antes do curinga | truncamento | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| Proximidade `W/n` e `PRE/n` | proximidade | Verificado em fonte oficial; `W/5` medido só entre os grupos inteiros das âncoras (BD2/sd2-2026-11-25) | Elsevier, *Scopus Search API — search tips* | — |
| `W/5` entre os grupos inteiros das duas âncoras | proximidade | Verificado por medição (BD2/sd2-2026-11-25); recusa leva à variante "Redução por recusa da interface" | — | SD2 |
| `{}` frase exata *versus* `""` frase aproximada | frase | Verificado em fonte oficial | Elsevier, *Scopus Search API — search tips* | — |
| Curinga `*` dentro de `""` | truncamento | Verificado por medição (BD2/sd8-2026-11-25); afirmado sem fonte na skill `auditoria-das-strings` até 2026-11-23: a frase aproximada admite truncamento; conferir também na documentação oficial | — | SD8 |
| Curinga `*` dentro de `{}` | truncamento | Verificado por medição (BD2/sd9-2026-11-25); afirmado sem fonte na skill `auditoria-das-strings` até 2026-11-23: a frase exata não admite truncamento; conferir também na documentação oficial | — | SD9 |
| Limite de operadores por consulta | limite_consulta | Verificado por medição (BD2/sd4-2026-11-25); não documentado; a consulta de EB4, com 104 operadores, é aceita; o limite não foi medido | — | SD4 |
| Comprimento máximo da consulta | limite_consulta | Verificado por medição (BD2/sd4-2026-11-25); a consulta de EB4, com 2.655 caracteres, é aceita; o máximo não foi medido; a maior consulta executável é medida por `python3 -m rsl documentos conferir`, no relato do teto de caracteres | — | SD4 |
| Lematização do plural entre `""`, em inglês | lematizacao | Verificado por medição (BD2/sd3-2026-11-25-2); as aspas casam singular e plural; medido só em `"conceptual model"` | — | SD3 |
| Lematização do plural entre `""`, em português | lematizacao | Verificado por medição (BD2/sd3-2026-11-25-2); as aspas não casam o plural; plural explícito necessário; medido só em `"modelo conceitual"` | — | SD3 |
| Lematização do plural entre `""`, em espanhol | lematizacao | Verificado por medição (BD2/sd3-2026-11-25-2); as aspas não casam o plural; plural explícito necessário; medido só em `"modelo conceptual"` | — | SD3 |
| Tratamento de diacríticos | idioma_indexacao | Verificado por medição (BD2/sd5-2026-11-25); medido só em `"educação"`/`"educacao"`, entre aspas; as strings trazem só a grafia acentuada | — | SD5 |
| Teto de retorno exibido | limite_retorno | Verificado por medição (BD2/sd6-2026-11-25); a navegação chega só ao registro 2.000; a exportação não fica limitada a ele (BD2/sd7-2026-11-25) | — | SD6 |
| Teto de exportação por lote | limite_exportacao | Verificado por medição (BD2/sd7-2026-11-25); lote de 6.625 registros aceito, igual ao retorno; teto acima disso não medido; conferir na interface antes de exportar | — | SD7 |
| Parênteses para agrupamento | agrupamento | Verificado por medição (BD2/sd1-2026-11-25-2) | — | SD1 |
| Vocabulário controlado de assunto | vocabulario_controlado | **Não verificado** | — | sem sondagem: verificação documental: os termos de indexação da Scopus não foram conferidos; nenhuma expressão depende deles |
| Exportação em RIS com todos os campos | exportacao | Verificado por medição (BD2/sd7-2026-11-25) | — | SD7 |

Todas as facetas vão entre parênteses explícitos; nenhuma expressão depende da ordem implícita de avaliação.

### Sondagens a executar

Uma consulta por vez, sem nova tentativa automática; parar diante de captcha, aviso de atividade atípica ou bloqueio, e registrar.

#### SD1 — saber se os parênteses agrupam dentro de `TITLE-ABS-KEY()` como booleanos

**Elementos verificados:** Parênteses para agrupamento (Verificado por medição).

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

**Consulta 4 — teste**, em busca avançada. Muda em relação ao controle: parênteses contra a precedência: só agrupando o retorno difere do segundo teste.

```
TITLE-ABS-KEY(ontology OR (taxonomy AND education))
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno exibido

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < primeiro teste ≤ controle, segundo teste = primeiro teste, e primeiro teste < terceiro teste ≤ controle | os parênteses agrupam, também contra a precedência; a precedência documentada (`OR` antes de `AND`) se confirma | Verificado por medição |
| 2 | 0 < primeiro teste ≤ controle, e terceiro teste = segundo teste, sem mensagem | os parênteses são aceitos mas não alteram a precedência; levar ao pesquisador | Não verificado |
| 3 | algum teste = 0, primeiro teste > controle, terceiro teste > controle, ou mensagem de erro | inconclusiva: o agrupamento não se confirma; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

**Resultados registrados.**

- (BD2/sd1-2026-11-25) 2026-11-25T19:30: leitura 1
- (BD2/sd1-2026-11-25-2) 2026-11-25T19:37: leitura 1

#### SD2 — saber se a interface aceita `W/5` entre os grupos inteiros das duas âncoras

**Elementos verificados:** `W/5` entre os grupos inteiros das duas âncoras (Verificado por medição).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com os parênteses verificados

**Consulta 1 — controle**, em busca avançada. Texto de EB5, sem proximidade, 958 caracteres.

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") AND ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

**Consulta 2 — teste**, em busca avançada. Texto de EB5, 958 caracteres. Muda em relação ao controle: `W/5` entre os grupos inteiros.

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") W/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
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

**Resultados registrados.**

- (BD2/sd2-2026-11-25) 2026-11-25T19:47: leitura 1

#### SD3 — saber se a frase aproximada entre aspas casa o plural da locução sem que a consulta o traga, em inglês, português e espanhol

**Elementos verificados:** Lematização do plural entre `""`, em inglês (Verificado por medição); Lematização do plural entre `""`, em português (Verificado por medição); Lematização do plural entre `""`, em espanhol (Verificado por medição).

**Pré-requisitos.**

- busca avançada da Scopus aberta no navegador do pesquisador

**Consulta 1 — controle**, em busca avançada.

```
TITLE-ABS-KEY("conceptual model")
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: o plural inglês entre aspas.

```
TITLE-ABS-KEY("conceptual models")
```

**Consulta 3 — controle**, em busca avançada.

```
TITLE-ABS-KEY("modelo conceitual")
```

**Consulta 4 — teste**, em busca avançada. Muda em relação ao controle: o plural português entre aspas.

```
TITLE-ABS-KEY("modelos conceituais")
```

**Consulta 5 — controle**, em busca avançada.

```
TITLE-ABS-KEY("modelo conceptual")
```

**Consulta 6 — teste**, em busca avançada. Muda em relação ao controle: o plural espanhol entre aspas.

```
TITLE-ABS-KEY("modelos conceptuales")
```

**Passos.**

1. submeter cada consulta, uma por vez, na mesma sessão, e anotar o retorno e a mensagem, se houver
2. comparar cada teste com o controle do mesmo idioma, imediatamente acima dele

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | nos três idiomas, teste = controle > 0, sem mensagem | as aspas casam singular e plural da locução em inglês, português e espanhol | Verificado por medição |
| 2 | nos três idiomas, 0 < teste ≠ controle, sem mensagem | as aspas não casam o plural em nenhum dos três idiomas; o plural explícito é necessário | Verificado por medição |
| 3 | teste = controle num idioma e ≠ noutro, algum retorno = 0, ou mensagem de erro | inconclusiva para o elemento como um todo; levar ao pesquisador, que decide se o elemento se divide por idioma | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

**Resultados registrados.**

- (BD2/sd3-2026-11-25) 2026-11-25T19:47: leitura 2
- (BD2/sd3-2026-11-25-2) 2026-11-25T20:05: leitura 3

#### SD4 — saber se a interface aceita inteira a consulta de EB4

**Elementos verificados:** Comprimento máximo da consulta (Verificado por medição); Limite de operadores por consulta (Verificado por medição).
**Depende de:** SD2.

**Pré-requisitos.**

- SD2 registrada com `W/5` entre grupos verificado

**Consulta 1 — teste**, em busca avançada. Texto de EB4, 2.872 caracteres.

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") W/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND (TITLE-ABS-KEY("prática de ensino" OR "práticas de ensino" OR "prática instrucional" OR "práticas instrucionais" OR "prática docente" OR "práticas docentes" OR "técnica de ensino" OR "técnicas de ensino" OR "técnica instrucional" OR "técnicas instrucionais" OR "técnica docente" OR "técnicas docentes" OR "métodos de ensino" OR "método de ensino" OR "teaching practice" OR "teaching practices" OR "instructional practice" OR "instructional practices" OR "teacher practice" OR "teacher practices" OR "teaching technique" OR "teaching techniques" OR "instructional technique" OR "instructional techniques" OR "educational practices" OR "educational practice" OR "teaching methods" OR "teaching method" OR "práctica de enseñanza" OR "prácticas de enseñanza" OR "práctica instruccional" OR "prácticas instruccionales" OR "práctica docente" OR "prácticas docentes" OR "técnica de enseñanza" OR "técnicas de enseñanza" OR "técnica instruccional" OR "técnicas instruccionales" OR "método de enseñanza" OR "métodos de enseñanza") OR TITLE-ABS-KEY("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais" OR "ambientes educacionales" OR "fatores de rendimento escolar" OR "fator de rendimento escolar" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "situational factor" OR "situational factors" OR "educational environment" OR "educational environments" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor situacional" OR "factores situacionales" OR "entorno educativo" OR "entornos educativos")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

**Passos.**

1. anotar o número de caracteres, que está na linha que precede a consulta, e o de operadores
2. submeter a consulta e anotar o retorno e a mensagem, se houver

**Observar.**

- retorno exibido
- mensagem de erro ou de recusa, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | aceita, com retorno > 0 | a interface aceita o comprimento e o número de operadores da consulta de EB4 | Verificado por medição |
| 2 | recusa por extensão ou por operadores, ou retorno = 0 | a consulta passa do limite; levar ao pesquisador (variante "Redução por recusa da interface") | Não verificado |

**Evidência a registrar.**

- captura da tela, com a consulta e o retorno visíveis

**Resultados registrados.**

- (BD2/sd4-2026-11-25) 2026-11-25T20:26: leitura 1

#### SD5 — saber se a base ignora diacríticos

**Elementos verificados:** Tratamento de diacríticos (Verificado por medição).

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

**Resultados registrados.**

- (BD2/sd5-2026-11-25) 2026-11-25T20:05: leitura 1

#### SD6 — saber se a base exibe e deixa percorrer o retorno inteiro de uma busca larga

**Elementos verificados:** Teto de retorno exibido (Verificado por medição).

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

**Resultados registrados.**

- (BD2/sd6-2026-11-25) 2026-11-25T20:26: leitura 2

#### SD7 — saber quantos registros a base exporta de uma vez em RIS com todos os campos

**Elementos verificados:** Teto de exportação por lote (Verificado por medição); Exportação em RIS com todos os campos (Verificado por medição).

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

**Resultados registrados.**

- (BD2/sd7-2026-11-25) 2026-11-25T20:26: leitura 1

#### SD8 — saber se o curinga trunca dentro da frase aproximada entre aspas

**Elementos verificados:** Curinga `*` dentro de `""` (Verificado por medição).

**Pré-requisitos.**

- busca avançada da Scopus aberta no navegador do pesquisador

**Consulta 1 — controle**, em busca avançada.

```
TITLE-ABS-KEY("conceptual model")
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: curinga no fim da locução entre aspas.

```
TITLE-ABS-KEY("conceptual model*")
```

**Passos.**

1. submeter cada consulta, uma por vez, na mesma sessão, e anotar o retorno e a mensagem, se houver

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro ou de recusa, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste > controle, sem mensagem | o curinga trunca dentro das aspas, na forma testada | Verificado por medição |
| 2 | 0 < teste ≤ controle, sem mensagem, ou consulta recusada com mensagem | o curinga não trunca dentro das aspas | Verificado por medição |
| 3 | teste = 0 sem mensagem, ou controle = 0 | inconclusiva: o zero não distingue recusa silenciosa de ausência do termo | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

**Resultados registrados.**

- (BD2/sd8-2026-11-25) 2026-11-25T20:05: leitura 1

#### SD9 — saber se o curinga trunca dentro da frase exata entre chaves

**Elementos verificados:** Curinga `*` dentro de `{}` (Verificado por medição).

**Pré-requisitos.**

- busca avançada da Scopus aberta no navegador do pesquisador

**Consulta 1 — controle**, em busca avançada.

```
TITLE-ABS-KEY({conceptual model})
```

**Consulta 2 — teste**, em busca avançada. Muda em relação ao controle: curinga no fim da locução entre chaves.

```
TITLE-ABS-KEY({conceptual model*})
```

**Passos.**

1. submeter cada consulta, uma por vez, na mesma sessão, e anotar o retorno e a mensagem, se houver

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro ou de recusa, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste > controle, sem mensagem | o curinga trunca dentro das chaves, na forma testada | Verificado por medição |
| 2 | 0 < teste ≤ controle, sem mensagem, ou consulta recusada com mensagem | o curinga não trunca dentro das chaves | Verificado por medição |
| 3 | teste = 0 sem mensagem, ou controle = 0 | inconclusiva: o zero não distingue recusa silenciosa de ausência do termo | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

**Resultados registrados.**

- (BD2/sd9-2026-11-25) 2026-11-25T20:05: leitura 2

#### SD10 — medir o retorno de EB5 com a proximidade declarada, com distância 15 e sem proximidade entre as âncoras, e a parcela de ruído da forma sem proximidade

**Elementos verificados:** .

**Pré-requisitos.**

- busca avançada aberta no navegador do pesquisador, com o acesso institucional dele
- procedimento regenerado com as strings vigentes

**Consulta 1 — controle**, em busca avançada. Texto de EB5, 958 caracteres.

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") W/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

**Consulta 2 — teste**, em busca avançada. Texto de EB5, proximidade com distância 15, 959 caracteres. Muda em relação ao controle: `W/15` entre as âncoras.

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") W/15 ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

**Consulta 3 — teste**, em busca avançada. Texto de EB5, sem proximidade, 958 caracteres. Muda em relação ao controle: `AND` entre as âncoras.

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") AND ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

**Consulta 4 — teste**, em busca avançada. Texto de EB5, sem proximidade, restrição AND com termos fora do protocolo: `ontology learning`, `machine learning`, `deep learning`, `aprendizaje automático`, 1.066 caracteres. Muda em relação ao controle: `AND` entre as âncoras e só os registros com uma forma de ruído conhecida (limite inferior do ruído).

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") AND ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND TITLE-ABS-KEY("ontology learning" OR "machine learning" OR "deep learning" OR "aprendizaje automático") AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

**Passos.**

1. submeter as quatro consultas na mesma sessão, uma por vez, na ordem, e anotar o retorno exibido de cada uma
2. não exportar: a sondagem mede volume

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro ou de recusa, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | todas aceitas, com controle ≤ consulta 2 ≤ consulta 3 e consulta 4 ≤ consulta 3 | retornos medidos; a decisão sobre a proximidade é do pesquisador | Verificado por medição |
| 2 | alguma consulta recusada ou com mensagem | a forma recusada não se mede; levar ao pesquisador | Não verificado |
| 3 | retornos fora das relações da primeira leitura, ou controle = 0 | inconclusiva: levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela do histórico de busca, com as quatro consultas e os retornos visíveis

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
| plural | explícito |
| teto de caracteres | nenhum |
| derivações | morfologia |

### `STR1` — string `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
TITLE-ABS-KEY("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías")
```

### `STR2` — string `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

```
TITLE-ABS-KEY("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")
```

### `STR3` — string `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
TITLE-ABS-KEY("prática de ensino" OR "práticas de ensino" OR "prática instrucional" OR "práticas instrucionais" OR "prática docente" OR "práticas docentes" OR "técnica de ensino" OR "técnicas de ensino" OR "técnica instrucional" OR "técnicas instrucionais" OR "técnica docente" OR "técnicas docentes" OR "métodos de ensino" OR "método de ensino" OR "teaching practice" OR "teaching practices" OR "instructional practice" OR "instructional practices" OR "teacher practice" OR "teacher practices" OR "teaching technique" OR "teaching techniques" OR "instructional technique" OR "instructional techniques" OR "educational practices" OR "educational practice" OR "teaching methods" OR "teaching method" OR "práctica de enseñanza" OR "prácticas de enseñanza" OR "práctica instruccional" OR "prácticas instruccionales" OR "práctica docente" OR "prácticas docentes" OR "técnica de enseñanza" OR "técnicas de enseñanza" OR "técnica instruccional" OR "técnicas instruccionales" OR "método de enseñanza" OR "métodos de enseñanza")
```

### `STR4` — string `#4` — 🟧 FCT4 — Fatores situacionais

```
TITLE-ABS-KEY("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais" OR "ambientes educacionales" OR "fatores de rendimento escolar" OR "fator de rendimento escolar" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "situational factor" OR "situational factors" OR "educational environment" OR "educational environments" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor situacional" OR "factores situacionales" OR "entorno educativo" OR "entornos educativos")
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
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") W/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND TITLE-ABS-KEY("prática de ensino" OR "práticas de ensino" OR "prática instrucional" OR "práticas instrucionais" OR "prática docente" OR "práticas docentes" OR "técnica de ensino" OR "técnicas de ensino" OR "técnica instrucional" OR "técnicas instrucionais" OR "técnica docente" OR "técnicas docentes" OR "métodos de ensino" OR "método de ensino" OR "teaching practice" OR "teaching practices" OR "instructional practice" OR "instructional practices" OR "teacher practice" OR "teacher practices" OR "teaching technique" OR "teaching techniques" OR "instructional technique" OR "instructional techniques" OR "educational practices" OR "educational practice" OR "teaching methods" OR "teaching method" OR "práctica de enseñanza" OR "prácticas de enseñanza" OR "práctica instruccional" OR "prácticas instruccionales" OR "práctica docente" OR "prácticas docentes" OR "técnica de enseñanza" OR "técnicas de enseñanza" OR "técnica instruccional" OR "técnicas instruccionales" OR "método de enseñanza" OR "métodos de enseñanza") AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB3 (artefatos que formalizam os fatores situacionais do domínio educacional)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧)

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") W/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND TITLE-ABS-KEY("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais" OR "ambientes educacionales" OR "fatores de rendimento escolar" OR "fator de rendimento escolar" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "situational factor" OR "situational factors" OR "educational environment" OR "educational environments" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor situacional" OR "factores situacionales" OR "entorno educativo" OR "entornos educativos") AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB4 (de cobertura restrita — artefatos de representação no domínio educacional que mencionam prática ou fator situacional)

*Executada e exportada nesta base.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧))

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") W/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND (TITLE-ABS-KEY("prática de ensino" OR "práticas de ensino" OR "prática instrucional" OR "práticas instrucionais" OR "prática docente" OR "práticas docentes" OR "técnica de ensino" OR "técnicas de ensino" OR "técnica instrucional" OR "técnicas instrucionais" OR "técnica docente" OR "técnicas docentes" OR "métodos de ensino" OR "método de ensino" OR "teaching practice" OR "teaching practices" OR "instructional practice" OR "instructional practices" OR "teacher practice" OR "teacher practices" OR "teaching technique" OR "teaching techniques" OR "instructional technique" OR "instructional techniques" OR "educational practices" OR "educational practice" OR "teaching methods" OR "teaching method" OR "práctica de enseñanza" OR "prácticas de enseñanza" OR "práctica instruccional" OR "prácticas instruccionales" OR "práctica docente" OR "prácticas docentes" OR "técnica de enseñanza" OR "técnicas de enseñanza" OR "técnica instruccional" OR "técnicas instruccionales" OR "método de enseñanza" OR "métodos de enseñanza") OR TITLE-ABS-KEY("contexto educacional" OR "contextos educacionais" OR "contexto de aprendizagem" OR "contextos de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator situacional" OR "fatores situacionais" OR "ambiente educacional" OR "ambientes educacionais" OR "ambientes educacionales" OR "fatores de rendimento escolar" OR "fator de rendimento escolar" OR "educational context" OR "educational contexts" OR "learning context" OR "learning contexts" OR "contextual factor" OR "contextual factors" OR "situational factor" OR "situational factors" OR "educational environment" OR "educational environments" OR "contexto educativo" OR "contextos educativos" OR "contexto de aprendizaje" OR "contextos de aprendizaje" OR "factor contextual" OR "factores contextuales" OR "factor situacional" OR "factores situacionales" OR "entorno educativo" OR "entornos educativos")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨)

```
TITLE-ABS-KEY(("ontologia" OR "ontologias" OR "modelo conceitual" OR "modelos conceituais" OR "representação do conhecimento" OR "organização do conhecimento" OR "knowledge representation" OR "knowledge representations" OR "knowledge organization" OR "knowledge organizations" OR "conceptual model" OR "conceptual models" OR "ontology" OR "ontologies" OR "representación del conocimiento" OR "organización del conocimiento" OR "modelo conceptual" OR "modelos conceptuales" OR "ontología" OR "ontologías") W/5 ("educacional" OR "educacionais" OR "educacionales" OR "ensino" OR "aprendizagem" OR "ensino-aprendizagem" OR "educação" OR "educational" OR "teaching" OR "learning" OR "teaching-learning" OR "education" OR "enseñanza" OR "aprendizaje" OR "enseñanza-aprendizaje" OR "educación")) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))
```

### Como executar

1. Conferir a sessão contra a seção 1, na primeira execução do dia.
2. Submeter o bloco de EB4 da seção 4 como está, sem definir conjunto. Na primeira execução, conferir se a interface aceita a consulta inteira; recusa por extensão leva à variante "Redução por recusa da interface", registrada como adaptação.
3. Submeter sempre a partir de arquivo, nunca recuperando o texto da interface.
4. Exportar em RIS, com todos os campos.
5. Conferir o retorno da exportação contra o da tela e o recorte temporal dentro do arquivo.
6. Registrar EB4 e EB5: `python3 -m rsl busca registrar scopus EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`; rodar `busca derivar` e `conferencia sensibilidade`.
7. Medir a aderência (seção 5). Semente esperada não recuperada: diagnosticar a causa com `python3 -m rsl aderencia diagnosticar scopus`.
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

Esperadas nesta base, conforme o protocolo. Estado de conferência e indexação declarada (`bases`) no arquivo de sementes (`[documentos] sementes`); recuperação medida por `python3 -m rsl aderencia medir`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE2 | Das, Naskar & Roy (2022) | `10.5771/0943-7444-2022-1-6` | — |
| SE3 | Chi, Chen & Hung (2018) | `10.1111/exsy.12246` | — |
| SE4 | Palomino et al. (2023) | `10.58459/rptel.2023.18018` | — |
| SE6 | Iatrellis, Kameas & Fitsilis (2019) | `10.1007/s10639-019-09877-4` | — |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE8 | Cenka, Santoso & Junus (2023) | `10.1080/10494820.2022.2039947` | — |
| SE9 | Piriyapongpipat, Goldin & Ditcharoen (2024) | `10.1186/s40561-024-00307-8` | — |
| SE13 | Hernández-Carrasco et al. (2022) | `10.3390/math10091355` | — |
| SE15 | Griful-Freixenet, Struyven & Vantieghem (2021) | `10.1177/0022487120965525` | — |
| SE17 | Hickey & Riddle (2024) | `10.1080/13603116.2023.2259906` | — |
| SE18 | Tondeur et al. (2024) | `10.1007/s10758-024-09784-9` | — |

**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões; semente não indexada sai do denominador e se registra no campo `bases` do arquivo de sementes. *Etapa 2:* `aderencia medir` procura a semente na exportação de EB4 pelo DOI e pelo título, sem reexecutar a busca.

**Limiar de aderência** (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`), sobre a união das bases. A aderência por base indica qual base e qual faceta falharam.

**Anatomia da perda.** A causa da perda não se atribui a olho:
`python3 -m rsl aderencia diagnosticar <sigla>` monta, da composição desta base, as
consultas por nível com os DOIs das sementes não recuperadas, lê da execução registrada os
níveis que já a têm e atribui a causa pelo primeiro nível em que o DOI desaparece — não
indexada, filtro, âncoras, proximidade ou faceta não âncora. O comando exige que a fonte
declare `[composicao] doi`; sem a declaração, recusa e nomeia o campo. O roteiro é submetido
no navegador do pesquisador, uma consulta por vez, e o resultado se registra com `--retorno`,
`--exportacao` e `--data-hora`.

---

## 6. Ressalvas

1. Todos os termos são **termos livres**; não apresentá-los como descritores autorizados.
