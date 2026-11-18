# Strings de busca — ERIC

**Protocolo:** Representação do conhecimento sobre práticas educacionais e seus fatores situacionais — revisão sistemática conduzida pelo modelo RS Banyan.  
**Posição no modelo:** Módulo 3, Etapa 1, 3º e 4º passos (strings e expressões de busca) e Etapa 2, 1º passo (execução).  
**Fonte:** ERIC — interface pública `eric.ed.gov`.  
**Responsável técnico:** Junilson Pereira Souza. **Validação temática:** VT.  
**Vigente desde:** 18/11/2026 (alinhamento à v2 do protocolo). **Registro de execução:** `data/registro_execucao.json`, base `BD3`. **Histórico das decisões:** Anexo A.

---

## 1. Estado de verificação da sintaxe

**Nomes de campo verificados no painel *Advanced Search Tips* de `eric.ed.gov/?advanced`. O comportamento de cada um foi verificado por medição** — o registro das sondagens está em `data/registro_execucao.json`.

| Elemento | Situação |
| :--- | :--- |
| Nomes de campo (`title`, `abstract`, `descriptor`, `educationlevel`, `language`, `publicationtype`, `pubyear`, `author`, `source`, `institution`, `sponsor`, `audience`, `assessment`, `law`, `location`, `e_yearadded`, `iesgrantcontractnum`) e filtros (`pubyearmin`, `pubyearmax`) | **Verificados em fonte oficial** |
| Campos de casamento exato (`descriptorx`, `sourcex`, `locationx`, `lawx`, `assessmentx`) e prefixo `+` para termo obrigatório | **Verificados em fonte oficial**, comportamento **não medido**. Nenhuma expressão os usa; `descriptorx` está previsto para sondagem na Camada 3 |
| Prefixo de campo restringe de fato | **Verificado por medição** |
| Parênteses para agrupamento | **Suportados**, com uma condição: o grupo **não funciona sozinho** e precisa de condição externa |
| Condição externa a um grupo | **Verificada** em qualquer forma: campo, texto livre ou outro grupo, antes ou depois |
| Campos diferentes num mesmo grupo | **Não suportados**: devolvem zero, sem mensagem de erro |
| `pubyearmin`/`pubyearmax` junto a um grupo | **Não suportados**: zeram o retorno; funcionam em consulta sem parênteses |
| `pubyearmin`/`pubyearmax` ligados por `AND` em consulta sem parênteses | **Verificado por medição** na sondagem de 08/11, registrada no Anexo A, e é a forma das variantes desta ficha. O painel oficial afirma que os filtros *“cannot be used with AND/OR/+/-”*; prevalece a forma medida |
| Truncamento com `*` | **Não suportado**: `ontolog*` devolve zero |
| Lematização | **Verificada** para plural regular; **não** para irregular |
| Aspas como frase | **Verificadas** dentro e fora do campo; palavra solta não forma frase, e o operador implícito entre duas palavras é conjunção |
| Campo `descriptor` | **Medido**: é campo controlado, e casa apenas formas autorizadas |
| Comprimento máximo da consulta | **Teto entre 1.502 e 1.799 caracteres brutos**; regra de bolso: manter abaixo de **1.400** |
| Negação com prefixo `-` | **Verificada em fonte oficial**, não medida |
| Hífen como separador de palavras (`ontology-driven`, `e-learning`) | **Não medido**. Dele dependem cinco alcances declarados na redução e a âncora de artefato da SE8 |
| Teto de retorno exibido e de exportação por lote | **Não verificados** |
| Controles `Include Synonyms` e `Include Dead terms` | **Não localizados** na interface, na conferência do ReT de 08/11. O painel *Advanced Search Tips* os lista apenas como rótulos sob *Thesaurus*, sem descrever comportamento, e a menção não os torna controle disponível na busca. Nenhuma expressão depende deles |

---

## 2. Critérios de elegibilidade

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — de 2017 até a data de execução, 2026 parcialmente coberto | CE1 / CE2 | **Não** | pelo **filtro de data da página de resultados**: os operadores de ano zeram o retorno quando a consulta tem grupos. Aplicar 2017 a 2026, com 2026 conforme a data de consulta, e registrar o rótulo do filtro e o retorno antes e depois |
| Idiomas — português, inglês e espanhol | CE3 | **Não** | os registros são descritos em inglês e as expressões usam só os termos em inglês. O campo `language` existe e não é usado: restringir idioma excluiria registro elegível |
| Tipo documental e revisão por pares | CE4 | **Não**, por decisão | caixa `Peer reviewed only` desmarcada e campo `publicationtype` não usado: o protocolo admite artigo, anais, capítulo, relatório técnico, e revisões sistemáticas e de escopo |
| Texto completo | CE5 | **Não** | caixa `Full text available on ERIC` desmarcada: marcada, suprime os artigos de periódico EJ, cujo texto está no editor |
| Adequação temática | CE6 | **Não** | filtragens do Módulo 3, Etapa 3 |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, em forma radical | a faceta 🟨 (FCT2) entra como grupo de quatro palavras-raiz, que é também a condição externa exigida pela sintaxe |
| Outros tipos documentais — editoriais, cartas, erratas, resenhas, apresentações de dossiê, resumos sem texto completo e versões preliminares | CE9 | **Não** | decisão de leitura, na 2ª filtragem |

---

## 3. Strings por faceta

Cada string corresponde a um quadro de controle terminológico do 2º passo. Sobre o vocabulário registrado incidem três operações, reversíveis e nenhuma delas supressão de termo: **desdobramento** da notação compacta, **compactação** do termo cuja recuperação já é implicada por outro da mesma faceta e **retirada do plural regular**, que a lematização torna redundante. As listas integrais das quatro facetas, nos três idiomas, estão no IO 1, Item 2.

`STRn` é o identificador do protocolo e `#n` a consulta correspondente. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

**Redução declarada em relação ao protocolo.** Esta base não usa a lista integral: `STR1` é reduzida aos termos que nomeiam artefato no título, e os cinco termos específicos que não têm acepção corrente fora da Organização do Conhecimento nem do domínio educacional vão ao resumo, na `STR1b`; `STR2` é reduzida a quatro palavras-raiz, que por casamento de palavra alcançam as expressões da faceta; `STR3` e `STR4` vão integralmente ao resumo. As formas plurais regulares são retiradas onde a lematização medida as torna redundantes. A lista do que fica de fora de `STR1` está na ressalva 7.

### Declaração de cobertura

O que esta busca alcança do vocabulário do protocolo. `src/protocolo.py` lê esta tabela
para conferir a string contra o protocolo; termo ausente e não declarado reprova a
conferência desta base.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: en; FCT2: en; FCT3: en; FCT4: en |
| camadas | todas |
| derivações | morfologia e radical |

**Redução declarada, termo a termo.** A emenda v2 retirou termos do vocabulário e esta
base mantém a restrição ao título na faceta 🟦. Tudo o que a string não contém literalmente
está abaixo: o que a emenda retirou permanece no protocolo e no estatuto de validação; o que
a forma radical alcança está declarado como tal; o resto é redução desta base.

| Faceta | Termo fora da string | Motivo |
| :--- | :--- | :--- |
| FCT1 | knowledge organization system | alcançado pela forma radical declarada |
| FCT1 | domain ontology | alcançado pela forma radical declarada |
| FCT1 | application ontology | alcançado pela forma radical declarada |
| FCT1 | upper ontology | alcançado pela forma radical declarada |
| FCT1 | educational ontology | alcançado pela forma radical declarada |
| FCT1 | learning ontology | alcançado pela forma radical declarada |
| FCT1 | teaching ontology | alcançado pela forma radical declarada |
| FCT1 | educational ontological model | fora da string desta base — redução declarada: traz a forma adjetival `ontological`, que `title:ontology` não alcança, e não está literalmente em `STR1` |
| FCT1 | educational practice ontology | alcançado pela forma radical declarada |
| FCT1 | instructional design ontology | alcançado pela forma radical declarada |
| FCT1 | curriculum ontology | alcançado pela forma radical declarada |
| FCT1 | faceted ontology | alcançado pela forma radical declarada |
| FCT1 | ontological | retirado na emenda v2 |
| FCT1 | facet analysis | retirado na emenda v2 |
| FCT1 | conceptual model | retirado na emenda v2 |
| FCT1 | conceptual modeling | retirado na emenda v2 |
| FCT1 | conceptual modelling | retirado na emenda v2 |
| FCT1 | conceptual schema | retirado na emenda v2 |
| FCT1 | semantic model | retirado na emenda v2 |
| FCT1 | formal representation | retirado na emenda v2 |
| FCT1 | ontology development | alcançado pela forma radical declarada |
| FCT1 | ontology-based modeling | alcançado pela forma radical declarada se o hífen separar palavras — tokenização do hífen não medida, sondagem pendente |
| FCT1 | ontology-based modelling | alcançado pela forma radical declarada se o hífen separar palavras — tokenização do hífen não medida, sondagem pendente |
| FCT1 | ontology-based knowledge representation | alcançado pela forma radical declarada |
| FCT2 | teaching practice | alcançado pela forma radical declarada |
| FCT2 | teaching method | alcançado pela forma radical declarada |
| FCT2 | teaching strategy | alcançado pela forma radical declarada |
| FCT2 | classroom teaching | alcançado pela forma radical declarada |
| FCT2 | teaching-learning | alcançado pela forma radical declarada se o hífen separar palavras — tokenização do hífen não medida, sondagem pendente |
| FCT2 | teaching and learning | alcançado pela forma radical declarada |
| FCT2 | learning process | alcançado pela forma radical declarada |
| FCT2 | learning environment | alcançado pela forma radical declarada |
| FCT2 | learning design | alcançado pela forma radical declarada |
| FCT2 | learning object | alcançado pela forma radical declarada |
| FCT2 | learning analytics | alcançado pela forma radical declarada |
| FCT2 | learning outcome | alcançado pela forma radical declarada |
| FCT2 | learning path | alcançado pela forma radical declarada |
| FCT2 | student learning | alcançado pela forma radical declarada |
| FCT2 | blended learning | alcançado pela forma radical declarada |
| FCT2 | online learning | alcançado pela forma radical declarada |
| FCT2 | lifelong learning | alcançado pela forma radical declarada |
| FCT2 | learning management system | alcançado pela forma radical declarada |
| FCT2 | teaching-learning process | alcançado pela forma radical declarada se o hífen separar palavras — tokenização do hífen não medida, sondagem pendente |
| FCT2 | e-learning | alcançado pela forma radical declarada se o hífen separar palavras — tokenização do hífen não medida, sondagem pendente |
| FCT2 | basic education | alcançado pela forma radical declarada |
| FCT2 | primary education | alcançado pela forma radical declarada |
| FCT2 | secondary education | alcançado pela forma radical declarada |
| FCT2 | higher education | alcançado pela forma radical declarada |
| FCT2 | vocational and technical education | alcançado pela forma radical declarada |
| FCT2 | distance education | alcançado pela forma radical declarada |
| FCT2 | online education | alcançado pela forma radical declarada |
| FCT2 | digital education | alcançado pela forma radical declarada |
| FCT2 | formal education | alcançado pela forma radical declarada |
| FCT2 | non-formal education | alcançado pela forma radical declarada |
| FCT2 | curriculum | retirado na emenda v2 |
| FCT2 | educational technology | alcançado pela forma radical declarada |
| FCT2 | virtual learning environment | alcançado pela forma radical declarada |
| FCT2 | open educational resource | alcançado pela forma radical declarada |
| FCT2 | massive open online course | fora da string desta base — redução declarada |
| FCT2 | learner | retirado na emenda v2 |
| FCT2 | student | retirado na emenda v2 |
| FCT2 | teacher | retirado na emenda v2 |
| FCT2 | instructor | retirado na emenda v2 |
| FCT2 | educational institution | retirado na emenda v2 |
| FCT2 | educational level | retirado na emenda v2 |
| FCT2 | education modality | retirado na emenda v2 |
| FCT3 | educational practice | alcançado pela forma radical declarada |
| FCT3 | pedagogical practice | alcançado pela forma radical declarada |
| FCT3 | teaching practice | alcançado pela forma radical declarada |
| FCT3 | instructional practice | alcançado pela forma radical declarada |
| FCT4 | application context | retirado na emenda v2 |
| FCT4 | context of use | retirado na emenda v2 |
| FCT4 | learning environment | retirado na emenda v2 |

### `STR1` — conjunto `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

*Vai ao título; cinco termos específicos vão também ao resumo, em string própria.*

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering")
```

### `STR1b` — conjunto `#1b` — 🟦 FCT1 — Artefatos, subconjunto específico, no resumo

*Entram só os termos sem acepção corrente fora da Organização do Conhecimento nem no domínio
educacional. Os termos ambíguos na literatura em geral e os homônimos do domínio educacional
ficam no título, e fora desta string.*

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern")
```

### `STR2` — conjunto `#2` — 🟨 FCT2 — Domínio educacional — **âncora obrigatória**

*Forma radical: quatro palavras-raiz que, por casamento de palavra, alcançam as expressões
registradas da faceta. A lista completa fica para o casamento local da derivação.*

```
(abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching)
```

### `STR3` — conjunto `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

*Vai ao resumo.*

```
(abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

### `STR4` — conjunto `#4` — 🟧 FCT4 — Fatores situacionais

*Vai ao resumo.*

```
(abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

---

## 4. Expressões de busca

### Como esta base exige que a expressão seja montada

Cinco regras, todas medidas. Quem alterar as expressões precisa respeitá-las, sob pena de
**retorno zero sem mensagem de erro**:

- grupo entre parênteses com `OR` **não funciona sozinho** — precisa de condição fora dele;
- a condição externa pode ser de campo, de texto livre ou outro grupo, antes ou depois;
- um grupo **não mistura campos**: `title:` e `abstract:` na mesma disjunção devolvem zero;
- `pubyearmin`/`pubyearmax` **não convivem com grupo** — o recorte temporal vem do filtro da página;
- **sem truncamento**, e expressão composta sempre entre aspas.

Daí a forma de toda expressão nesta base: **duas consultas de campo único**, unidas por
deduplicação — a faceta 🟦 no título (`STR1`) e o seu subconjunto específico no resumo
(`STR1b`) —, ambas com a faceta 🟨 como grupo externo. É a faceta 🟨 que satisfaz a primeira
regra, e por isso ela não é dispensada.

**Composição e contenção.** `EB1 = #1 + #2 + #3 + #4`; `EB2 = #1 + #2 + #3`;
`EB3 = #1 + #2 + #4`; `EB4 = #1 + #2 + (#3 OR #4)`; `EB5 = #1 + #2`. As facetas combinam-se
por `AND`, e acrescentar faceta **restringe**. Daí **EB1 ⊂ EB2 ⊂ EB4**, **EB1 ⊂ EB3 ⊂ EB4** e
**EB4 = EB2 ∪ EB3**: EB4 exige as duas âncoras e **ao menos uma** das facetas temáticas.
**EB5 ⊃ EB4**: retira a exigência temática e mede o que EB4 deixa de fora. *Geral* qualifica
a composição, não o alcance: EB1 é a mais restritiva, e serve de caracterização, nunca de
critério de exclusão.

Registro que não satisfaça EB1 **não é excluído**: permanece se satisfizer EB4. As facetas
temáticas são dimensões combináveis, não requisitos cumulativos de recuperação.

**Estatuto de cada expressão.**

| | Executar na base? | Como quê | O que se perde ao pular |
| :--- | :--- | :--- | :--- |
| **EB4** (cobertura restrita) | **sim, sempre** | é o portfólio: define o que a revisão recuperou nesta base | tudo — a base não participa da revisão |
| **EB5** (sonda) | **sim, uma única vez** | sonda de sensibilidade: mede o que EB4 perde | a medida do custo em recall da mudança de EB4 |
| **EB2** | sim | teste de fidelidade da derivação | a auditabilidade das contagens derivadas |
| **EB3** | sim | teste de fidelidade da derivação | idem |
| **EB1** (geral) | não | caracterização, por derivação local | nada, desde que a derivação rode |

**Execução única.** Executa-se **EB4**, com exportação única por consulta. **EB5** é
executada **uma única vez, na mesma base e data**, e **não compõe o corpus**. A pertinência a
EB1, EB2 e EB3 é calculada localmente por `derivar_expressoes.py`, e essas contagens são
**derivadas**, não reconsultadas.

**Fidelidade da derivação.** Antes de aceitar contagem derivada, executar **EB2 e EB3** e
comparar com o conjunto derivado: divergência acima de **10%** reprova o método.

**Leitura de retorno vazio.** Zero só é achado depois de provada a execução válida.
**EB4 = 0** é quase sempre defeito; **EB5 = 0** é defeito de execução, porque EB5 contém EB4;
**EB2 = 0** com EB4 > 0 é achado — há artefatos, nenhum representa práticas; **EB3 = 0** é
achado forte; **EB1 = 0** é o enunciado da lacuna. Contagem derivada próxima de zero obriga à
execução direta antes de ser relatada.

**Limite de comprimento.** Manter cada consulta abaixo de **1.400 caracteres brutos**; acima
disso o teto medido é de 1.502 a 1.799, e a saída é partir a expressão. A partição mantém o
grupo da faceta 🟦 íntegro e isola uma faceta temática de cada vez: a união das partes é
*exatamente* a expressão original, porque `A AND (B OR C)` equivale a `(A AND B) OR (A AND C)`.
Somar por deduplicação, nunca por adição de números.

### EB1 (geral) — as quatro facetas

**Não se executa; derivação local.** Sonda de precisão máxima, nunca critério de exclusão; a
contagem é derivada de EB4. **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧)

### EB2 (específica) — modelos e ontologias que representam práticas do processo de ensino-aprendizagem

**Conferência do teste de fidelidade.** **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥)

**Consulta 2a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

**Consulta 2b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

### EB3 (específica) — artefatos que formalizam os fatores situacionais do domínio educacional

**Conferência do teste de fidelidade.** **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧)

**Consulta 3a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

**Consulta 3b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

### EB4 (de cobertura restrita) — artefatos de representação no domínio educacional que mencionam prática ou fator situacional

**É esta que se executa e se exporta.** **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧))

A forma completa passa do teto de comprimento: **EB4 é exatamente a união de EB2 e EB3**, e
por isso se executa como as quatro consultas abaixo, somadas **por deduplicação**. A partição
não altera o conjunto.

**Consulta 4a — título × prática**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

**Consulta 4b — título × fator situacional**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

**Consulta 4c — termo específico × prática**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:practice OR abstract:"teaching strategy" OR abstract:"instructional strategy" OR abstract:"teaching method" OR abstract:"instructional method" OR abstract:"teaching technique" OR abstract:"learning activity" OR abstract:"learning task" OR abstract:"educational intervention" OR abstract:"instructional intervention" OR abstract:"teaching sequence" OR abstract:"instructional sequence" OR abstract:pedagogy OR abstract:"best practices" OR abstract:"recommended practices" OR abstract:"pedagogical approach" OR abstract:"instructional approach" OR abstract:"instructional design" OR abstract:"learning design" OR abstract:"pedagogical pattern" OR abstract:"pedagogical design pattern" OR abstract:"active learning method" OR abstract:"teaching methodology")
```

**Consulta 4d — termo específico × fator situacional**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching) AND (abstract:"situational factor" OR abstract:"situation of use" OR abstract:"educational context" OR abstract:"learning context" OR abstract:"contextual factors" OR abstract:"context factors" OR abstract:"application conditions" OR abstract:"implementation conditions" OR abstract:"learning situation" OR abstract:"educational setting" OR abstract:"institutional context" OR abstract:"sociocultural context" OR abstract:"target population" OR abstract:"class profile" OR abstract:"learner characteristics" OR abstract:"educational level" OR abstract:"education modality" OR abstract:"educational institution" OR abstract:"educational infrastructure" OR abstract:"learning infrastructure" OR abstract:"available resources" OR abstract:"contextual constraints" OR abstract:"context modeling" OR abstract:"context modelling" OR abstract:"context representation" OR abstract:"context-aware" OR abstract:contextualization OR abstract:contextualisation)
```

> **As quatro consultas ainda não foram executadas na forma vigente.** Exportar em arquivos
> separados, `eric_4a.ris` a `eric_4d.ris`, e depositar em `data/execucoes/eric/`.

### EB5 (sonda de sensibilidade) — as duas âncoras, sem exigir prática nem fator situacional

**Sonda de sensibilidade — executada uma única vez; não compõe o corpus.** A diferença
`EB5 \ EB4` mede o que a restrição temática deixa de fora. **Facetas:** FCT1 (🟦) AND FCT2 (🟨)

**Consulta 5a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge organization" OR title:ontology OR title:"controlled vocabulary" OR title:thesaurus OR title:thesauri OR title:"classification scheme" OR title:"metadata schema" OR title:"faceted classification" OR title:"faceted taxonomy" OR title:"domain model" OR title:"ontological engineering") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching)
```

**Consulta 5b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching)
```

### Como executar

1. **Deduplicar 4a, 4b, 4c e 4d.** O retorno da base é a união deduplicada, **nunca a soma dos quatro números**; anotar a sobreposição. O script também marca os repetidos e conta os únicos; o número que vai ao IO 2 é o dos únicos, com o bruto ao lado.
2. **Aplicar o filtro de data da página** e anotar o retorno antes e depois, com o rótulo exato do filtro.
3. **Registrar as quatro execuções**, uma por arquivo, com `python3 src/derivar_expressoes.py --registrar eric EB4 <arquivo> --retorno <n>` e rodar `--derivar`. O registro confere o retorno declarado contra cada arquivo e recusa registrar quando divergem; a derivação confere o recorte, marca duplicatas e calcula a pertinência a EB1, EB2 e EB3.
4. **Conferir a aderência.** Abaixo de 80%, a busca por campo está restritiva demais, e passa-se à contingência das variantes.

**Quando o retorno não couber na triagem.** As consultas de refinamento das variantes **não são subconjuntos** da 4a nem reproduzem a composição da EB4: cruzam um termo de artefato no título com um único termo do resumo, sem a âncora 🟨 completa, e substituí-la por elas muda o conjunto recuperado. Servem para **substituir** a 4a quando o retorno exceder o limite de triagem fixado pelo ReT — sugere-se **300 registros** como ponto de partida, e o número adotado consta do IO 2. É restrição de recall, não ampliação: registrar o retorno antes e depois.

### Variantes previstas

#### Refinamento por cruzamento título × resumo

Para substituir a 4a quando o retorno exceder o limite de triagem. Nestas, o sufixo de ano é admissível, porque não há grupo entre parênteses.

Retiradas em 18/11, por usarem termo que a emenda v2 tirou do vocabulário (`conceptual model`, `semantic model`, `formal representation`, e `curriculum` da faceta 🟨): X1, X5, X9, X10, X11, X12, X13, X17, X18, X19, X20, X21, X22, X23, X24. A numeração das demais se mantém, para que o registro continue a remeter à mesma consulta.

| # | Consulta |
| :---: | :--- |
| X2 | `title:ontology AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X3 | `title:ontology AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X4 | `title:ontology AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X6 | `title:ontologies AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X7 | `title:ontologies AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X8 | `title:ontologies AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X14 | `title:"domain model" AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X15 | `title:"domain model" AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X16 | `title:"domain model" AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |

#### Camada 3 — descritores de artefato

Existe para o estudo que trata do artefato **sem o nomear no título nem no resumo**. Monta-se com os descritores de artefato de volume baixo — **teto de 2.000 registros** —, porque acima disso o descritor é polissêmico numa base de educação: `Vocabulary` é aprendizado de palavras e `Classification` é categorização de alunos e de conteúdo. Ficam de fora, por esse critério, `Classification`, `Semantics`, `Vocabulary` e `Information Retrieval`; e fica de fora `Taxonomy` (1.628), porque a emenda v2 retirou `taxonomy` isolada do vocabulário. Os descritores não são termos do protocolo: a camada só se adota por emenda.

```
(descriptor:Thesauri OR descriptor:Indexing OR descriptor:Metadata OR descriptor:"Knowledge Representation") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching)
```

**Sondagem prevista — `descriptorx`.** O painel oficial lista `descriptorx` como variante de casamento exato de `descriptor`; o comportamento **não foi medido**. Antes de qualquer uso, sondar cada um dos quatro descritores nas duas formas — `descriptor:Thesauri` e `descriptorx:Thesauri`, e assim por diante —, registrando os retornos no registro de execução. Até a sondagem, a camada usa `descriptor`, e nada se conclui sobre o que a diferença entre as duas formas significa.

> **Esta camada não se valida pelo conjunto-semente, e isso tem de estar escrito.** As três sementes esperadas nesta base trazem o termo de artefato no título — leitura dos títulos, não recuperação medida, e na SE8 dependente do hífen —, de modo que a camada não as melhora; e as sementes que a justificariam — cujo artefato não está no título — esta base não indexa. A camada justifica-se pela medição do campo e pelo exame qualitativo do que devolver, e a adoção depende de emenda aprovada com a VT.

#### Contingência — consultas curtas, sem agrupamento

Para o caso de a aderência reprovar a busca por campo. Uma linha por consulta, todas exportadas e deduplicadas em conjunto.

**Estas consultas não reproduzem a EB4.** As de 1 a 16 têm só a faceta 🟦, sem a âncora 🟨 e sem faceta temática; as demais cruzam 🟦 com um único termo de outra faceta. São outra busca, mais ampla que a EB5, e só se adotam por emenda, com a perda de precisão medida. Pela v2, a forma adotada no lugar da 4a–4d tem de recompor FCT1 AND FCT2 AND (FCT3 OR FCT4); em consulta sem parênteses, isso se faz com `AND` entre um termo de cada faceta, partindo pelos termos.

Retiradas em 18/11, pelo mesmo motivo do refinamento: 17, 19, 27, 31, 32, 33, 34, 36, 37, 38. A numeração das demais se mantém.

| # | Consulta | # | Consulta |
| :---: | :--- | :---: | :--- |
| 1 | `"knowledge representation" AND pubyearmin:2017 AND pubyearmax:2026` | 2 | `"knowledge organization" AND pubyearmin:2017 AND pubyearmax:2026` |
| 3 | `"knowledge organization system" AND pubyearmin:2017 AND pubyearmax:2026` | 4 | `"knowledge organization systems" AND pubyearmin:2017 AND pubyearmax:2026` |
| 5 | `"controlled vocabulary" AND pubyearmin:2017 AND pubyearmax:2026` | 6 | `"controlled vocabularies" AND pubyearmin:2017 AND pubyearmax:2026` |
| 7 | `thesaurus AND pubyearmin:2017 AND pubyearmax:2026` | 8 | `thesauri AND pubyearmin:2017 AND pubyearmax:2026` |
| 9 | `"classification scheme" AND pubyearmin:2017 AND pubyearmax:2026` | 10 | `"classification schemes" AND pubyearmin:2017 AND pubyearmax:2026` |
| 11 | `"metadata schema" AND pubyearmin:2017 AND pubyearmax:2026` | 12 | `"metadata schemas" AND pubyearmin:2017 AND pubyearmax:2026` |
| 13 | `"ontology engineering" AND pubyearmin:2017 AND pubyearmax:2026` | 14 | `"ontology development" AND pubyearmin:2017 AND pubyearmax:2026` |
| 15 | `"ontology design pattern" AND pubyearmin:2017 AND pubyearmax:2026` | 16 | `"ontology-based knowledge representation" AND pubyearmin:2017 AND pubyearmax:2026` |
| 18 | `ontology AND "learning object" AND pubyearmin:2017 AND pubyearmax:2026` | 20 | `ontology AND "learning analytics" AND pubyearmin:2017 AND pubyearmax:2026` |
| 21 | `ontology AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` | 22 | `ontology AND "instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 23 | `ontology AND "teaching methods" AND pubyearmin:2017 AND pubyearmax:2026` | 24 | `ontology AND "situational factors" AND pubyearmin:2017 AND pubyearmax:2026` |
| 25 | `ontology AND "educational context" AND pubyearmin:2017 AND pubyearmax:2026` | 26 | `ontologies AND "learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| 28 | `ontologies AND "learning analytics" AND pubyearmin:2017 AND pubyearmax:2026` | 29 | `ontologies AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 30 | `ontologies AND "instructional design" AND pubyearmin:2017 AND pubyearmax:2026` | 35 | `"domain model" AND education AND pubyearmin:2017 AND pubyearmax:2026` |
| 39 | `"ontological engineering" AND pubyearmin:2017 AND pubyearmax:2026` | | |

#### Negação do ruído por descritor

A negação `-descriptor:"…"` está documentada no painel oficial e **não foi medida**. Permitiria levar ao resumo os termos de `STR1` hoje restritos ao título por homonímia, negando os descritores da literatura cognitiva e metodológica em lugar de evitá-los pelo campo. Candidatos a testar, um a um, antes de usar: `Educational Research`, `Research Methodology`, `Epistemology`, `Qualitative Research`. Negar descritor inexistente não faz nada; negar descritor largo retira estudo elegível.

---

## 5. Conjunto-semente

O conjunto-semente tem **10 estudos**. O estado de conferência de cada um está em `data/sementes.json` — hoje, as dez com verificação, escopo, tipo e alinhamento pendentes (`python3 src/protocolo.py --pendencias`). Pela indicação do ReT, **3 são esperados nesta base**. Planilha de aferição, uma linha por semente e por base: `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE6 | Iatrellis et al. (2019) | `10.1007/s10639-019-09872-9` | — |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE8 | Cenka et al. (2023) | `10.1080/10494820.2022.2039947` | — |

**Procedimento, em duas etapas.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões, para saber se a base indexa a semente. Semente não indexada **sai do denominador** e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação de EB4 por DOI e depois por título, **sem reexecutar a busca**.

**Limiar de 80%.** Decide o número **global**, sobre a união das bases. A aderência por base diagnostica **qual** base e **qual** faceta falharam.

**Lematização.** **Medida nesta base**: alcança o plural regular e não o irregular. É o que permite retirar `ontologies`, `domain ontologies` e `pedagogies` da consulta, e é por isso que o efeito do desdobramento morfológico aqui é o menor das quatro bases. A **derivação adjetival** não é alcançada por lematização alguma, e `ontological`, retirado na emenda v2, não está na consulta: os termos que só o contêm ficam fora, como redução declarada — ressalva 7.

**Restrição ao título — perda medida.** A camada 1 restringe os termos da faceta 🟦 ao título, o que é perda de recall assumida em troca de precisão. Pela leitura dos títulos, **nenhuma das três sementes esperadas perde a âncora de artefato** por essa restrição: SE6 e SE7 trazem `ontology`; a SE8 traz `ontology-driven`, e o alcance depende de o hífen separar palavras, o que não foi medido. É inferência, não recuperação medida — o registro marca a aderência como não medida. Três sementes não medem uma base, mas invertem o ônus: a hipótese de que o título é restritivo demais passa a precisar de evidência.

**Cobertura.** As sementes cujo artefato não está no título não são indexadas por esta base. A camada 3 existe para esse caso e depende de emenda aprovada.

---

## 6. Ressalvas

1. **Todos os termos têm estatuto de termo livre**: nenhum foi confrontado com instrumento de controle terminológico. As expressões desta base **não devem ser apresentadas como compostas de descritores ERIC**. Procedimento e estado da validação: IO 1 e Anexo A.

2. **A precisão vem do campo.** Nove dos doze termos de `STR1` ficam restritos ao título; os outros três — `controlled vocabulary`, `metadata schema` e `thesauri` — vão também ao resumo, em `STR1b`. Perde-se o estudo que os mencione apenas no resumo, e é o teste de aderência que mede essa perda — reprova abaixo de 80%.

3. **A faceta 🟨 entra em forma radical**, com quatro palavras-raiz que alcançam as expressões registradas por casamento de palavra. Redução declarada, e também a condição externa sem a qual a base devolve zero.

4. **Assimetria de campo em relação à Scopus**, a declarar no relato. Lá, `TITLE-ABS-KEY()` alcança título, resumo e palavras-chave de todos os termos. Aqui, a parcela de palavras-chave corresponde ao campo `descriptor`, que casa apenas formas autorizadas, e oito termos ficam só no título.

5. **O retorno da base é a união deduplicada de 4a, 4b, 4c e 4d, depois do filtro de data.**

6. **A sintaxe desta base foi apurada por medição, não por documentação.** Alterar as expressões sem repetir as sondagens pertinentes arrisca retorno zero silencioso.

7. **Redução de `STR1` — o que fica de fora e por quê.** A faceta tem 30 termos ingleses vigentes — os 38 do quadro terminológico menos os 8 que a emenda v2 retirou. A consulta de título traz 12 deles literalmente — `ontological engineering` entrou em 18/11, por decisão do ReT —; `STR1b` traz, no resumo, mais 2 — `ontology engineering` e `ontology design pattern`. Dos 16 que não estão literalmente em consulta alguma, **15 são alcançados por casamento de palavra** no título — comportamento medido na sondagem 8, em que `education` alcança `"higher education"` —: `title:ontology` alcança os onze compostos com `ontology` (`domain ontology`, `application ontology`, `upper ontology`, `educational ontology`, `learning ontology`, `teaching ontology`, `educational practice ontology`, `instructional design ontology`, `curriculum ontology`, `faceted ontology` e `ontology development`) e, se o hífen separar palavras, as duas formas hifenizadas; `title:"knowledge organization"`, `knowledge organization system`; `title:"knowledge representation"`, `ontology-based knowledge representation`. Desses 15, **2 — `ontology-based modeling` e `ontology-based modelling` — dependem da tokenização do hífen**, que não foi medida, e assim estão declarados na redução. **O 1 restante não é alcançado**: `educational ontological model` traz a forma adjetival `ontological`, que lematização alguma alcança a partir de `ontology`, e não está literalmente em `STR1`. É redução declarada desta base, e o teste de aderência é o que mede o seu custo.
