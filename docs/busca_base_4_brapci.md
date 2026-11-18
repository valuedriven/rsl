# Strings de busca — BRAPCI

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º e 4º passos (strings e expressões de busca) e Etapa 2, 1º passo (execução).  
**Fonte:** BRAPCI — Base de Dados Referencial de Artigos de Periódicos em Ciência da Informação.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** VT.  
**Vigente desde:** 18/11/2026 (EB4 da v2 por grupos, em lugar das consultas curadas). **Registro de execução:** `data/registro_execucao.json`, base `BD4`. **Histórico das decisões:** Anexo A.

---

## 1. Estado de verificação da sintaxe

**A sintaxe desta base não está documentada em fonte alguma: foi apurada por medição**, em sondagens registradas em `data/registro_execucao.json`, com captura de tela.

| Elemento | Situação |
| :--- | :--- |
| Aspas como frase | **Funcionam**: a frase entre aspas restringe o retorno |
| `AND`, `OR` e parênteses | **Funcionam**, e o operador é insensível à caixa |
| Truncamento `*` | **Funciona**: o radical alcança as variantes morfológicas numa só consulta. Não se usa: `ontolog*` alcança formas que a emenda v2 retirou |
| Lematização | **Não medida**, e contornada pelas flexões explícitas nas strings |
| Comprimento máximo da consulta | **Não verificado**; a EB4 expandida tem cerca de 4.100 caracteres — sondar antes da primeira execução |
| Combinação de conjuntos de busca | **Não verificada**; a execução usa a forma expandida |
| Proximidade | **Não verificada** |
| Exportação — formatos e lote | **Não verificada** |
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

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — de 2017 até a data de execução, 2026 parcialmente coberto | CE1 / CE2 | **No filtro da interface** | aplicar ano inicial e final antes de executar: 2017 e 2026, com o ano em curso conforme a data de consulta; conferir o ano no retorno |
| Idiomas — português, inglês e espanhol | CE3 | **Dispensado** | a base é de produção brasileira em Ciência da Informação; as strings usam os termos em português, com os equivalentes em inglês apenas na faceta 🟦. Nenhum filtro de idioma é aplicado |
| Tipo documental | CE4 | **Não**, por decisão | filtro de tipo de publicação não usado: restringir o tipo excluiria material elegível. Quais tipos a base indexa além de artigo de periódico **não foi verificado**; revisões sistemáticas e de escopo permanecem elegíveis |
| Texto completo | CE5 | **Não** | verificação individual na 2ª filtragem |
| Adequação temática | CE6 | **Não** | filtragens do Módulo 3, Etapa 3 |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, por âncora | a faceta 🟨 (FCT2) nas cinco expressões; ver a ressalva sobre o seu efeito nesta base |
| Outros tipos documentais — editoriais, cartas, erratas, resenhas, apresentações de dossiê, resumos sem texto completo e versões preliminares | CE9 | **Não** | decisão de leitura, na 2ª filtragem |

---

## 3. Strings por faceta

Strings montadas sobre `STR1`–`STR4` da versão 2 do protocolo, nos termos em português e, na faceta de artefatos, também em inglês. `STRn` é o identificador do protocolo e `#n` a string correspondente. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

**Fidelidade ao protocolo.** As strings desta ficha são os termos de `STR1`–`STR4` v2 nos idiomas declarados abaixo, literalmente, acrescidos apenas de flexões de número sobre termo que já consta deles. As flexões vão explícitas, e não por truncamento: o truncamento funciona nesta base, mas `ontolog*` alcança `ontológico` e `ontológica`, que a emenda v2 retirou.

### Declaração de cobertura

O que esta busca alcança do vocabulário do protocolo. `src/protocolo.py` lê esta tabela para conferir a string contra o protocolo; termo ausente e não declarado reprova a conferência desta base.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: pt, en; FCT2: pt; FCT3: pt; FCT4: pt |
| camadas | todas |
| derivações | morfologia |

**Redução declarada.** Idioma da produção nacional, acima — a faceta de artefatos entra também em inglês porque parte da produção nacional sobre o tema é publicada nessa língua —, e a redução da v2: os termos que a emenda retirou, termo a termo na tabela seguinte. Eles permanecem no quadro terminológico e no estatuto de validação; a string desta base não os executa.

| Faceta | Termo fora da string | Motivo |
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
| FCT2 | educativo | retirado na emenda v2 |
| FCT2 | currículo | retirado na emenda v2 |
| FCT2 | estudante | retirado na emenda v2 |
| FCT2 | aluno | retirado na emenda v2 |
| FCT2 | professor | retirado na emenda v2 |
| FCT2 | docente | retirado na emenda v2 |
| FCT2 | instituição de ensino | retirado na emenda v2 |
| FCT2 | nível de ensino | retirado na emenda v2 |
| FCT2 | modalidade de ensino | retirado na emenda v2 |
| FCT4 | contexto de aplicação | retirado na emenda v2 |
| FCT4 | contexto de uso | retirado na emenda v2 |
| FCT4 | ambiente de aprendizagem | retirado na emenda v2 |

### `STR1` — conjunto `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
("representação do conhecimento" OR "organização do conhecimento" OR "sistema de organização do conhecimento" OR "ontologia" OR "ontologias" OR "ontologia de domínio" OR "ontologias de domínio" OR "ontologia de aplicação" OR "ontologia de topo" OR "vocabulário controlado" OR "tesauro" OR "taxonomia facetada" OR "esquema de classificação" OR "esquema de metadados" OR "classificação facetada" OR "ontologia facetada" OR "ontologia educacional" OR "ontologia de aprendizagem" OR "ontologia de ensino" OR "modelo ontológico educacional" OR "ontologia de prática educacional" OR "ontologia de design instrucional" OR "ontologia de currículo" OR "modelo de domínio" OR "engenharia de ontologias" OR "desenvolvimento de ontologias" OR "padrão de projeto ontológico" OR "modelagem baseada em ontologias" OR "representação do conhecimento baseada em ontologias" OR "knowledge representation" OR "knowledge organization" OR "knowledge organization system" OR "knowledge organization systems" OR "ontology" OR "ontologies" OR "domain ontology" OR "domain ontologies" OR "application ontology" OR "upper ontology" OR "controlled vocabulary" OR "thesaurus" OR "thesauri" OR "faceted taxonomy" OR "classification scheme" OR "metadata schema" OR "faceted classification" OR "faceted ontology" OR "educational ontology" OR "learning ontology" OR "teaching ontology" OR "educational ontological model" OR "educational practice ontology" OR "instructional design ontology" OR "curriculum ontology" OR "domain model" OR "ontology engineering" OR "ontology development" OR "ontology design pattern" OR "ontology-based modeling" OR "ontology-based modelling" OR "ontology-based knowledge representation" OR "ontological engineering" OR "taxonomía facetada")
```

### `STR2` — conjunto `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

```
("educação" OR "educacional" OR "educacionais" OR "processo de ensino-aprendizagem" OR "método de ensino" OR "estratégia de ensino" OR "ensino superior" OR "ensino básico" OR "ambiente de aprendizagem" OR "objeto de aprendizagem" OR "trilha de aprendizagem" OR "situação de aprendizagem" OR "resultado de aprendizagem" OR "educação básica" OR "ensino fundamental" OR "ensino médio" OR "educação profissional e tecnológica" OR "educação a distância" OR "educação online" OR "educação digital" OR "educação formal" OR "educação não formal" OR "tecnologia educacional" OR "ambiente virtual de aprendizagem" OR "recurso educacional aberto" OR "aprendizagem eletrônica" OR "curso online aberto e massivo")
```

### `STR3` — conjunto `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
("prática" OR "prática educacional" OR "práticas educacionais" OR "prática pedagógica" OR "prática docente" OR "estratégia de ensino" OR "estratégia instrucional" OR "método de ensino" OR "método instrucional" OR "técnica de ensino" OR "atividade de aprendizagem" OR "tarefa de aprendizagem" OR "intervenção educacional" OR "intervenção pedagógica" OR "sequência didática" OR "sequência instrucional" OR "pedagogia" OR "pedagogias" OR "boa prática" OR "boas práticas" OR "prática recomendada" OR "práticas recomendadas" OR "abordagem pedagógica" OR "abordagem instrucional" OR "design instrucional" OR "desenho da aprendizagem" OR "desenho didático" OR "padrão pedagógico" OR "padrão de projeto pedagógico" OR "método ativo" OR "metodologia de ensino")
```

### `STR4` — conjunto `#4` — 🟧 FCT4 — Fatores situacionais

```
("fator situacional" OR "fatores situacionais" OR "situação de uso educacional" OR "contexto educacional" OR "contexto de aprendizagem" OR "fator contextual" OR "fatores contextuais" OR "fator de contexto" OR "fatores de contexto" OR "condição de aplicação" OR "condições de aplicação" OR "condição de implementação" OR "condições de implementação" OR "situação de aprendizagem" OR "cenário educacional" OR "contexto institucional" OR "contexto sociocultural" OR "população-alvo" OR "perfil da turma" OR "característica do aluno" OR "características dos alunos" OR "nível de ensino" OR "modalidade de ensino" OR "instituição de ensino" OR "instituição educacional" OR "infraestrutura educacional" OR "recurso disponível" OR "recursos disponíveis" OR "restrição contextual" OR "restrições contextuais" OR "modelagem de contexto" OR "representação de contexto" OR "contexto sensível" OR "contextualização")
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

Registro que não satisfaça EB1 **não é excluído**: permanece se satisfizer EB4. As facetas temáticas são dimensões combináveis, não requisitos cumulativos de recuperação.

**Estatuto de cada expressão.**

| | Executar na base? | Como quê | O que se perde ao pular |
| :--- | :--- | :--- | :--- |
| **EB4** (cobertura restrita) | **sim, sempre** | é o portfólio: define o que a revisão recuperou nesta base | tudo — a base não participa da revisão |
| **EB5** (sonda) | **sim, uma única vez** | sonda de sensibilidade: mede o que EB4 perde | a medida do custo em recall da restrição de EB4 |
| **EB2** e **EB3** | não | derivação local; o teste de fidelidade é exigido na WoS e na Scopus | nada, desde que a derivação rode |
| **EB1** (geral) | não | caracterização, por derivação local | nada, desde que a derivação rode |

**Execução única.** Executa-se **EB4**, com exportação única, e **EB5**, uma única vez, na mesma data, fora do corpus. A pertinência de cada registro a EB1, EB2 e EB3 é calculada localmente por `derivar_expressoes.py`.

**Forma de execução.** A interface não oferece combinação de conjuntos verificada: a consulta submetida é a **forma expandida**, montada por substituição de `#1` a `#4` pelos blocos da seção 3, num arquivo, e não por digitação. A forma expandida da EB4 tem cerca de 4.100 caracteres, e o comprimento máximo que a base aceita **não foi verificado**: sondá-lo antes da primeira execução (seção "Como executar").

**Leitura de retorno vazio.** Zero só é achado depois de provada a execução válida — e, nesta base, depois de provado que a consulta longa foi aceita inteira. **EB4 = 0** é quase sempre defeito; **EB5 = 0** é defeito de execução, porque EB5 contém EB4. Contagem derivada próxima de zero é, nesta base, plausível: a produção nacional sobre o tema é escassa, e o retorno nulo **é informação** — registra-se e constitui indício para a enunciação da lacuna. Não se deve, por causa dele, relaxar a âncora 🟦.

### EB1 (as quatro facetas)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧) · **conjuntos:** #1 AND #2 AND #3 AND #4

```
#1 AND #2 AND #3 AND #4
```

### EB2 (modelos e ontologias que representam práticas do processo de ensino-aprendizagem)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) · **conjuntos:** #1 AND #2 AND #3

```
#1 AND #2 AND #3
```

### EB3 (artefatos que formalizam os fatores situacionais do domínio educacional)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧) · **conjuntos:** #1 AND #2 AND #4

```
#1 AND #2 AND #4
```

### EB4 (de cobertura restrita — artefatos de representação no domínio educacional que mencionam prática ou fator situacional)

*Executada e exportada nesta base.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧)) · **conjuntos:** #1 AND #2 AND (#3 OR #4)

```
#1 AND #2 AND (#3 OR #4)
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) · **conjuntos:** #1 AND #2

```
#1 AND #2
```

A forma expandida não é mantida em duplicidade aqui: cópia em segundo lugar defasa na primeira alteração da string.

### Como executar

1. Aplicar o filtro de ano e manter *Todos os campos*; registrar o método de busca e o limite de resultados.
2. **Sondar o comprimento.** Submeter a forma expandida de EB5 e conferir que a interface a aceitou inteira — comparar o retorno com o de `#1 AND #2` partido em metades da faceta 🟦 (variante "Partição"). Registrar a sondagem.
3. Executar **EB4** na forma expandida. Retorno de exatamente 1.000 é corte: partir, conforme as variantes, até que nenhuma parte encoste no teto.
4. Executar **EB5** uma única vez, na mesma data, fora do corpus.
5. Exportar em RIS ou BibTeX; se a base não exportar, registrar os metadados no Zotero e anotar a entrada manual como risco de transcrição.
6. Registrar com `python3 src/derivar_expressoes.py --registrar brapci EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`, com a justificativa do teto de 1.000 quando for o caso; rodar `--derivar` e `--sensibilidade`.
7. Medir a aderência ao conjunto-semente. Se uma semente esperada não aparecer, seguir o procedimento da seção 5.

### Variantes previstas

#### Partição — por comprimento ou pelo teto de 1.000

Disparo: a consulta recusada ou truncada pelo comprimento, ou retorno de exatamente 1.000. Forma, em ordem: (1) `EB4 = EB2 ∪ EB3` — executar `#1 AND #2 AND #3` e `#1 AND #2 AND #4`; (2) partir a faceta 🟦 em português e em inglês, com o resto da expressão idêntico — `(A1 OR A2) AND B` equivale a `(A1 AND B) OR (A2 AND B)`; (3) subintervalos de anos. Toda partição é exata: as mesmas âncoras em todas as partes, união por deduplicação, nunca por soma. Registrar a partição como adaptação.

#### Varredura da faceta 🟦 isolada — fora do corpus

Disparo: a ressalva 4 — o vínculo educacional pode não comparecer nos metadados desta base. Forma: `#1` sozinho, com o filtro de ano, uma única vez. **Não compõe o corpus**: os registros de `#1` fora de EB5 são amostrados e classificados à mão, como na sonda de sensibilidade. Se a fração elegível passar de 15%, a âncora 🟨 está custando recall nesta base, e a correção é emenda, não inclusão avulsa.

#### Partição por *Título*

Consulta que encoste no teto de 1.000 mesmo com o recorte temporal pode ser repetida em *Título*: devolve o núcleo mais pertinente e permite estimar quanto do excedente era ruído. É instrumento de precisão e de diagnóstico, nunca forma de execução.

---

## 5. Conjunto-semente

O conjunto-semente tem **10 estudos**. O estado de conferência de cada um está em `data/sementes.json` — hoje, as dez com verificação, escopo, tipo e alinhamento pendentes (`python3 src/protocolo.py --pendencias`). Pela indicação do ReT, **2 são esperados nesta base**. Planilha de aferição, uma linha por semente e por base: `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE1 | Alvarenga & Cristovão (2023) | — | — |
| SE5 | Sousa & Duque (2018) | `10.5433/1981-8920.2018v23n1p271` | **caso-teste de cobertura de campo** |

**Procedimento, em duas etapas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões, para saber se a base indexa a semente. Semente não indexada **sai do denominador** e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação por DOI e depois por título, **sem reexecutar a busca**.

**Limiar de 80%.** Decide o número **global**, sobre a união das bases. A aderência por base diagnostica **qual** base e **qual** faceta falharam.

**Lematização.** **Não medida, mas contornada**: as flexões de número vão explícitas nas strings. O truncamento, que funciona nesta base, não se usa, porque alcança formas que a emenda v2 retirou.

**Caso-teste de cobertura de campo — SE5.** O **artefato** está fora do título: a ontologia das salas de aula é o resultado pretendido, descrito no resumo, enquanto o título anuncia um *modelo de sistema da informação*. A recuperação depende do resumo e das palavras-chave. Se EB4 recuperar, recuperou por campo que não é o título; se não recuperar, a perda deixa de ser estimada e passa a ser medida.

**Se a semente não aparecer.** Consultar `Duque` em *Local de pesquisa* = **Autor**, abrir o registro de Sousa & Duque (2018) e ler resumo e palavras-chave. O resultado separa duas causas:

| Achado | Leitura |
| :--- | :--- |
| o resumo ou as palavras-chave trazem `ontologia` | a semente é recuperável em *Todos os campos*, e a falha era de campo, não de vocabulário |
| nem o resumo nem as palavras-chave trazem o termo | a faceta 🟦 não alcança o registro: o problema é de vocabulário, e a semente deixa de medir campo |
| a consulta por `Duque` devolve zero | a opção *Autor* não funciona, ou o registro não está indexado: achado a registrar antes de usar o campo no *backward search* |

**Estado atual.** A execução realizada mediu o **núcleo** do vocabulário da v1, e não a EB4 da v2: os retornos **não podem ser lançados no IO 2 como retorno de EB4** e estão vencidos. A partir de 18/11/2026 a forma de execução é a EB4 da v2 por grupos, com as strings integrais da STR v2 — a `STR1` passa a conter `ontologia`, que as duas sementes exigem e que o núcleo não tinha. A sondagem de comprimento, a execução e a consulta por `Duque` estão pendentes. Estado e números em `data/registro_execucao.json`.

---

## 6. Ressalvas

1. **A sintaxe desta base foi medida, não documentada.** A primeira tarefa na base é a sondagem, e a forma final das strings decorre dela. Alterar as consultas sem repetir as sondagens pertinentes arrisca retorno zero silencioso.

2. **Estatuto dos termos.** Todos os termos desta ficha são **termos livres**: nenhum foi confrontado com instrumento de controle terminológico. A validação do 2º passo corre no TBCI, para o português, e no UNESCO Thesaurus, para inglês e espanhol; ERIC Thesaurus, Brased/INEP, ACM CCS, LISTA, W3C e IEEE LOM ficam sem consulta. A ausência de validação não retira o termo da expressão; retira-lhe a qualidade de descritor autorizado.

3. **Termos qualificados para busca.** **Substituição** de palavra isolada de uso geral pelas formas compostas correspondentes, ou sua retirada da expressão permanecendo no quadro. **Desdobramento** de termo em notação compacta em alternativas explícitas ligadas por `OR`. **Desdobramento morfológico** de formas adjetivais e plurais, porque a derivação adjetival não é alcançada por lematização alguma. Substituição e retirada casam a **forma, não o lema**. Os termos em português desta ficha são os únicos do conjunto que passam pela via automatizada do TBCI, tesauro da própria área da base: confirmado um descritor autorizado, ele é o candidato mais forte a entrar nas strings, e a incorporação é emenda ao protocolo, propagada a esta ficha.

4. **Efeito da âncora 🟨 nesta base.** A BRAPCI indexa Ciência da Informação, não educação: o vínculo educacional pode não comparecer no título, no resumo ou nas palavras-chave. Pela v2, o corpus desta base é a EB4, como nas demais; o custo da âncora mede-se pela sonda EB5 e pela varredura da faceta 🟦 isolada, ambas fora do corpus (seção 4, variantes). Até 17/11 a faceta 🟦 isolada compunha o corpus como rede de segurança; deixou de compor em 18/11, e isso deve ser declarado no relato.

5. **Exportação.** Se a base dispuser de exportação em RIS ou BibTeX, exportar; se não, registrar os metadados manualmente no Zotero e anotar a entrada manual como fonte de risco de erro de transcrição.
