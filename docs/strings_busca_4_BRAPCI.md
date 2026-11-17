# Strings de busca — BRAPCI

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º passo (expressões de busca) e Etapa 2, 1º passo (execução).  
**Fonte:** BRAPCI — Base de Dados Referencial de Artigos de Periódicos em Ciência da Informação.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** VT.  
**Vigente desde:** 17/11/2026. **Registro de execução:** `data/registro_execucao.json`, base `BD4`. **Histórico das decisões:** Anexo A.

---

## 1. Estado de verificação da sintaxe

**A sintaxe desta base não está documentada em fonte alguma: foi apurada por medição**, em sondagens registradas em `data/registro_execucao.json`, com captura de tela.

| Elemento | Situação |
| :--- | :--- |
| Aspas como frase | **Funcionam**: a frase entre aspas restringe o retorno |
| `AND`, `OR` e parênteses | **Funcionam**, e o operador é insensível à caixa |
| Truncamento `*` | **Funciona**: o radical alcança as variantes morfológicas numa só consulta |
| Lematização | **Não medida**, e contornada pelo truncamento |
| Local de pesquisa | **Seletor único** — Título, Resumo, Palavras-chave, Autor, Todos os campos —, aplicado à consulta inteira |
| Campos diferentes na mesma consulta | **Não**, salvo se houver linhas de busca empilháveis, o que não foi verificado |
| Filtros | **Ano inicial e ano final**, tipo de publicação e limite de resultados |
| Teto de exibição | **1.000 registros**: retorno de exatamente 1.000 é **corte**, não contagem |

**Regra de execução, para toda consulta desta ficha.**

1. Aplicar o filtro de ano **antes** de executar.
2. Manter **Local de pesquisa = Todos os campos**.
3. Anotar o retorno de cada consulta.
4. Retorno de 1.000 significa consulta truncada: partir por idioma, por subconjunto de termos ou por subintervalo de anos, até que nenhuma parte encoste no teto, somando as partes e registrando a sobreposição.

**Por que *Todos os campos*.** EB4 é a expressão de cobertura, e restringir o campo contraria a sua função. As demais opções ficam como instrumentos, não como forma de execução:

- ***Título*** — instrumento de precisão e de partição: consulta que encoste no teto pode ser repetida em *Título* para devolver o núcleo mais pertinente e estimar quanto do excedente era ruído.
- ***Resumo*** e ***Palavras-chave*** — instrumentos de medição de cobertura: comparar o retorno de um mesmo termo nos três campos informa onde a base indexa.
- ***Autor*** — não se usa na busca; serve ao *backward search* e à conferência de duplicatas.

**Controles da interface.** O método de busca em uso é o **ponderado**; os métodos anterior (2024) e atual (2026) devolvem o mesmo volume, de modo que a escolha não altera o conjunto. O limite de resultados é configurável de 1.000 a 5.000 e é dado de reprodutibilidade: registrá-lo junto com o Local de pesquisa.

**Filtro de tipo de publicação: não se usa.** O protocolo admite artigo, anais, capítulo e relatório técnico, e restringir o tipo excluiria material elegível. Usa-se **apenas o filtro de ano**.

---

## 2. Critérios de elegibilidade

| Critério | Na consulta? | Como |
| :--- | :--- | :--- |
| Intervalo temporal — de 2017 até a data de execução, 2026 parcialmente coberto | **Sim, pelo filtro de ano** | aplicar ano inicial e final na interface, antes de exportar: 2017 e 2026, com o ano em curso conforme a data de consulta |
| Idiomas | **Dispensado** | a base é de produção brasileira em Ciência da Informação; as strings usam os termos em português, com os equivalentes em inglês apenas na faceta 🟦 |
| Tipo documental | **Dispensado** | a base é referencial de artigos de periódicos, o que corresponde a um dos tipos admitidos pelo protocolo |
| Texto completo | **Não** | verificação individual na 2ª filtragem |
| Domínio educacional | **Sim**, por âncora | faceta 🟨 nas consultas combinadas; ver a ressalva sobre o seu efeito nesta base |
| Adequação temática | **Não** | filtragens do Módulo 3, Etapa 3 |

---

## 3. Strings por faceta

Strings montadas sobre o **núcleo** de cada quadro terminológico, em português e, na faceta de artefatos, também em inglês. Elas alimentam a forma longa da seção 4 e **não são a forma executada** nesta base: a execução usa as consultas curadas.

### `#1` — 🟦 Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems")
```

### `#2` — 🟨 Domínio educacional — **âncora obrigatória**

```
("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos")
```

### `#3` — 🟥 Práticas do processo de ensino-aprendizagem

```
("prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente")
```

### `#4` — 🟧 Fatores situacionais

```
("fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem")
```

---

## 4. Expressões de busca

Esta base tem **duas formas**, e só uma se executa.

| Forma | Composição | Situação |
| :--- | :--- | :--- |
| **Curada** — consultas curtas, de uma e de duas facetas | termos escolhidos um a um | **é a forma de execução** |
| **Longa** — expressões EB1 a EB4 | strings da seção 3 | **não se executa**; fica como registro e como ponto de partida de uma forma intermediária |

As consultas curadas não leem as facetas: **acréscimo de termo ao vocabulário exige revisitar esta lista**, ao contrário das expressões longas.

### Forma de execução — consultas curadas

Todas as consultas abaixo devem ser executadas, uma a uma, com o filtro de ano e em *Todos os campos*, registrando o retorno de cada uma e deduplicando no Zotero.

> **Onde a lista traz variantes de um mesmo radical, preferir o truncamento.** `ontolog*` substitui `ontologia`, `ontologias` e as formas adjetivais numa só consulta. As consultas abaixo mantêm as formas explícitas porque são o registro do vocabulário; ao executar, pode-se usar o radical e anotar a substituição.

#### Faceta 🟦 isolada — varredura da representação do conhecimento na produção nacional

| # | Consulta |
| :---: | :--- |
| 1 | `"representação do conhecimento"` |
| 2 | `"organização do conhecimento"` |
| 3 | `"sistema de organização do conhecimento"` |
| 4 | `ontologia` |
| 5 | `ontologias` |
| 6 | `"ontologia de domínio"` |
| 7 | `"modelo conceitual"` |
| 8 | `"modelagem conceitual"` |
| 9 | `"engenharia de ontologias"` |
| 10 | `tesauro` |
| 11 | `taxonomia` |
| 12 | `"vocabulário controlado"` |
| 13 | `"esquema de metadados"` |
| 14 | `"classificação facetada"` |
| 15 | `"análise facetada"` |

A faceta 🟦 isolada é executada na íntegra porque, nesta base, o conjunto de artigos sobre representação do conhecimento é da ordem de grandeza que a leitura de títulos comporta, e porque o cruzamento com 🟨 pode falhar quando o vínculo educacional está no corpo do texto e não nos metadados. O resultado é a **rede de segurança** desta base.

#### Pares 🟦 + 🟨 — representação no domínio educacional

| # | Consulta |
| :---: | :--- |
| 1 | `"representação do conhecimento" AND educação` |
| 2 | `"representação do conhecimento" AND ensino` |
| 3 | `"representação do conhecimento" AND aprendizagem` |
| 4 | `"representação do conhecimento" AND educacional` |
| 5 | `"organização do conhecimento" AND educação` |
| 6 | `"organização do conhecimento" AND ensino` |
| 7 | `"organização do conhecimento" AND aprendizagem` |
| 8 | `"organização do conhecimento" AND educacional` |
| 9 | `ontologia AND educação` |
| 10 | `ontologia AND ensino` |
| 11 | `ontologia AND aprendizagem` |
| 12 | `ontologia AND educacional` |
| 13 | `"modelo conceitual" AND educação` |
| 14 | `"modelo conceitual" AND ensino` |
| 15 | `"modelo conceitual" AND aprendizagem` |
| 16 | `"modelo conceitual" AND educacional` |
| 17 | `tesauro AND educação` |
| 18 | `tesauro AND ensino` |
| 19 | `tesauro AND aprendizagem` |
| 20 | `tesauro AND educacional` |
| 21 | `taxonomia AND educação` |
| 22 | `taxonomia AND ensino` |
| 23 | `taxonomia AND aprendizagem` |
| 24 | `taxonomia AND educacional` |
| 25 | `"análise facetada" AND educação` |
| 26 | `"análise facetada" AND ensino` |
| 27 | `"análise facetada" AND aprendizagem` |
| 28 | `"análise facetada" AND educacional` |

#### Pares com as demais facetas

| # | Consulta | Facetas |
| :---: | :--- | :--- |
| 1 | `ontologia AND "prática pedagógica"` | 🟦 + 🟥 |
| 2 | `ontologia AND "prática educacional"` | 🟦 + 🟥 |
| 3 | `"representação do conhecimento" AND "prática pedagógica"` | 🟦 + 🟥 |
| 4 | `ontologia AND "sequência didática"` | 🟦 + 🟥 |
| 5 | `ontologia AND "contexto de aplicação"` | 🟦 + 🟧 |
| 6 | `ontologia AND contexto` | 🟦 + 🟧 |
| 7 | `ontologia AND "situação de aprendizagem"` | 🟦 + 🟧 |
| 8 | `"modelo conceitual" AND "contexto educacional"` | 🟦 + 🟧 |
| 9 | `"objeto de aprendizagem" AND metadados` | 🟨 + 🟦 |
| 10 | `"recursos educacionais abertos" AND metadados` | 🟨 + 🟦 |

### Forma longa — não se executa

As expressões abaixo usam o núcleo das facetas, e não a lista integral. Confrontadas com o conjunto-semente, **não recuperam nenhuma das duas sementes desta base**: o núcleo da faceta 🟦 não ocorre nos dois títulos, que dizem `ontologia` e `modelo de sistema da informação`. Ficam registradas por rastreabilidade e para um uso residual: se o teto de 1.000 atrapalhar consulta a consulta, são o ponto de partida de uma forma intermediária, acrescentando ao núcleo os termos de *próximos* que as sementes exigem — `ontologia` à frente de todos —, com emenda registrada.

**EB1** (geral) — as quatro facetas · 🟦 AND 🟨 AND 🟥 AND 🟧 · **derivada**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems") AND ("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos") AND ("prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente") AND ("fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem")
```

**EB2** (específica) — modelos e ontologias que representam práticas · 🟦 AND 🟨 AND 🟥 · **derivada**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems") AND ("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos") AND ("prática" OR "práticas educacionais" OR "prática educacional" OR "prática pedagógica" OR "prática docente")
```

**EB3** (específica) — artefatos que formalizam fatores situacionais · 🟦 AND 🟨 AND 🟧 · **derivada**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems") AND ("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos") AND ("fatores situacionais" OR "fator situacional" OR "situação de uso educacional" OR "contexto de aplicação" OR "contexto de uso" OR "contexto educacional" OR "contexto de aprendizagem")
```

**EB4** (de cobertura) — artefatos de representação no domínio educacional · 🟦 AND 🟨

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems") AND ("educação" OR "educacional" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educacionais" OR "educativo" OR "educativos")
```

Expressões de três facetas ou mais tendem, nesta base, a retorno nulo ou próximo de zero. O retorno nulo **é informação**: registra-se e constitui indício para a enunciação da lacuna na produção nacional. Não se deve, por causa dele, relaxar a âncora 🟦.

### Como executar

1. Aplicar o filtro de ano e manter *Todos os campos*.
2. Executar as consultas curadas, uma a uma, anotando o retorno de cada uma; preferir o truncamento onde a lista traz variantes do mesmo radical.
3. Exportar cada consulta em RIS ou BibTeX; se a base não exportar, registrar os metadados no Zotero e anotar a entrada manual como risco de transcrição.
4. Deduplicar o conjunto no Zotero.
5. Anotar em `data/registro_execucao.json` (base `BD4`); registrar com `python3 src/derivar_expressoes.py --registrar brapci EB4 <arquivo> --retorno <n>`; rodar `--derivar`.
6. Medir a aderência ao conjunto-semente. Se uma semente esperada não aparecer, seguir o procedimento da seção 5.

### Variantes previstas

#### Truncamento em lugar da lista

Onde a consulta traz variantes de um mesmo radical, usar o radical: `ontolog*` alcança `ontologia`, `ontologias` e as formas adjetivais numa só consulta. Anotar a substituição no registro.

#### Partição por *Título*

Consulta que encoste no teto de 1.000 mesmo com o recorte temporal pode ser repetida em *Título*: devolve o núcleo mais pertinente e permite estimar quanto do excedente era ruído. É instrumento de precisão e de partição, nunca forma de execução.

#### Forma intermediária

Se o teto atrapalhar consulta a consulta, montar a forma intermediária a partir das expressões longas, acrescentando ao núcleo os termos de *próximos* que as sementes exigem — `ontologia` à frente de todos —, com emenda registrada.

---

## 5. Conjunto-semente

O conjunto-semente tem **10 estudos**, todos conferidos em fonte e dentro do escopo. Pela indicação do ReT, **2 são esperados nesta base**. Instrumento completo: `data/saida/semente/Conjunto_Semente.md`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE1 | Alvarenga & Cristovão (2023) | — | — |
| SE5 | Sousa & Duque (2018) | `10.5433/1981-8920.2018v23n1p271` | **caso-teste de cobertura de campo** |

**Procedimento, em duas etapas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões, para saber se a base indexa a semente. Semente não indexada **sai do denominador** e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação por DOI e depois por título, **sem reexecutar a busca**.

**Limiar de 80%.** Decide o número **global**, sobre a união das bases. A aderência por base diagnostica **qual** base e **qual** faceta falharam.

**Lematização.** **Não medida, mas contornada**: o truncamento funciona e alcança as variantes morfológicas de uma vez, de modo que a lematização deixa de ser crítica nesta base.

**Caso-teste de cobertura de campo — SE5.** O **artefato** está fora do título: a ontologia das salas de aula é o resultado pretendido, descrito no resumo, enquanto o título anuncia um *modelo de sistema da informação*. A recuperação depende do resumo e das palavras-chave. Se EB4 recuperar, recuperou por campo que não é o título; se não recuperar, a perda deixa de ser estimada e passa a ser medida.

**Se a semente não aparecer.** Consultar `Duque` em *Local de pesquisa* = **Autor**, abrir o registro de Sousa & Duque (2018) e ler resumo e palavras-chave. O resultado separa duas causas:

| Achado | Leitura |
| :--- | :--- |
| o resumo ou as palavras-chave trazem `ontologia` | a semente é recuperável em *Todos os campos*, e a falha era de campo, não de vocabulário |
| nem o resumo nem as palavras-chave trazem o termo | a faceta 🟦 não alcança o registro: o problema é de vocabulário, e a semente deixa de medir campo |
| a consulta por `Duque` devolve zero | a opção *Autor* não funciona, ou o registro não está indexado: achado a registrar antes de usar o campo no *backward search* |

**Estado atual.** A execução realizada mediu o **núcleo** do vocabulário, e não as expressões registradas: os retornos **não podem ser lançados no IO 2 como retorno de EB4**. A reexecução com a expressão registrada e a consulta por `Duque` estão pendentes. Estado e números em `data/registro_execucao.json`.

---

## 6. Ressalvas

1. **A sintaxe desta base foi medida, não documentada.** A primeira tarefa na base é a sondagem, e a forma final das strings decorre dela. Alterar as consultas sem repetir as sondagens pertinentes arrisca retorno zero silencioso.

2. **Estatuto dos termos.** Todos os termos desta ficha são **termos livres**: nenhum foi confrontado com instrumento de controle terminológico. A validação do 2º passo corre no TBCI, para o português, e no UNESCO Thesaurus, para inglês e espanhol; ERIC Thesaurus, Brased/INEP, ACM CCS, LISTA, W3C e IEEE LOM ficam sem consulta. A ausência de validação não retira o termo da expressão; retira-lhe a qualidade de descritor autorizado.

3. **Termos qualificados para busca.** **Substituição** de palavra isolada de uso geral pelas formas compostas correspondentes, ou sua retirada da expressão permanecendo no quadro. **Desdobramento** de termo em notação compacta em alternativas explícitas ligadas por `OR`. **Desdobramento morfológico** de formas adjetivais e plurais, porque a derivação adjetival não é alcançada por lematização alguma. Substituição e retirada casam a **forma, não o lema**. Os termos em português desta ficha são os únicos do conjunto que passam pela via automatizada do TBCI, tesauro da própria área da base: confirmado um descritor autorizado, ele é o candidato mais forte a entrar nas consultas, e a incorporação obriga a regerar esta ficha.

4. **Efeito da âncora 🟨 nesta base.** A BRAPCI indexa Ciência da Informação, não educação: o vínculo educacional pode não comparecer no título, no resumo ou nas palavras-chave. É por isso que a faceta 🟦 é executada também isolada, com leitura de todos os títulos retornados. A decisão amplia o esforço de triagem nesta base e deve ser declarada no relato.

5. **Exportação.** Se a base dispuser de exportação em RIS ou BibTeX, exportar; se não, registrar os metadados manualmente no Zotero e anotar a entrada manual como fonte de risco de erro de transcrição.
