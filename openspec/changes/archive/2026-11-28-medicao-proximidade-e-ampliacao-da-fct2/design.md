# Design

## Contexto

O motivo e o escopo estão na proposta (Por quê; O que muda). O estado de partida:

- O protocolo tem os termos livres pt novos da FCT2 e da FCT3, editados pelo pesquisador. As
  linhas en e es e as de descritores são as anteriores. `strings gerar` reprova a STR3 (6
  termos a acrescentar e 5 a retirar), e a STR2 também diverge do quadro.
- A planilha de validação tem as linhas dos termos anteriores e nenhuma dos novos.
- `docs/flexoes.toml` declara exceções para termos que saem do quadro (`ensino e
  aprendizagem`, `teaching and learning`, `enseñanza y aprendizaje`, `intervenção
  educacional`), e não tem nenhuma para os termos novos.
- As transformações de sondagem são `sem_proximidade` e `metade`. A Scopus declara
  `[composicao] doi`, e a WoS não.
- A fonte da ERIC tem uma lista própria da STR2 no resumo (`education`, `educational`,
  `learning`, `teaching`, `learner`, `learners`), fora do quadro.

## Objetivos / Não objetivos

**Objetivos**
- Levar o quadro da FCT2 e da FCT3 até a STR e o procedimento de cada base, pelo caminho do
  projeto (README, Precedência), com a decisão do pesquisador em cada ponto em que o caminho
  a exige.
- Medir, sobre a FCT2 nova, o retorno da EB5 com a proximidade declarada, com distância 15 e
  sem proximidade, e a parcela de ruído.

**Não objetivos**
- Decidir a proximidade, emendar a EB4 ou mudar as notas N3 e N4.
- Medir a elegibilidade ou a recuperação das sementes em cada célula da grade.
- Tirar conclusão automática da grade: a leitura relata os retornos.

## Decisões

### D1. Equivalentes en e es: proposta do agente, revisão do pesquisador antes de gravar

Pela decisão de 2026-11-24, as linhas en e es de "Termo livre" têm só os equivalentes dos
termos pt. São tradução proposta pelo agente, não conferida em fonte de autoridade. Proposta:

| Faceta | pt | en | es |
| :--- | :--- | :--- | :--- |
| FCT2 | educacional | educational | educacional |
| FCT2 | ensino | teaching | enseñanza |
| FCT2 | aprendizagem | learning | aprendizaje |
| FCT2 | ensino-aprendizagem | teaching-learning | enseñanza-aprendizaje |
| FCT3 | prática de ensino | teaching practice | práctica de enseñanza |
| FCT3 | prática instrucional | instructional practice | práctica instruccional |
| FCT3 | prática docente | teacher practice | práctica docente |
| FCT3 | técnica de ensino | teaching technique | técnica de enseñanza |
| FCT3 | técnica instrucional | instructional technique | técnica instruccional |
| FCT3 | técnica docente | — (coberta por `teaching technique`) | técnica docente |

Consequências que o pesquisador revisa:
- **Saem das linhas en e es** os termos sem correspondente pt:
  - FCT2: `teaching and learning` e `enseñanza y aprendizaje`. Os dois seriam de todo modo
    subsumidos por `learning` e `aprendizaje`;
  - FCT3: `educational practice`, `teaching method`, `educational strategy`, `learning
    activity`, `educational intervention`, `práctica educativa`, `estrategia educativa`,
    `actividad de aprendizaje` e `intervención educativa`.
- **Colisão em inglês, decidida pelo pesquisador (2026-11-27):** vale a forma com maior
  potencial de busca efetiva, ainda que fuja da correspondência um a um. `prática docente`
  fica com `teacher practice`, forma usada na literatura. `técnica docente` fica sem
  equivalente próprio em inglês, porque `teacher technique` é forma pouco usual e
  `teaching technique` já cobre o conceito.
- **As linhas de descritores não mudam por esta decisão.** `métodos de ensino`, `educational
  practices`, `teaching methods` e `método de enseñanza` continuam até a decisão do ReT (D3).

### D2. Validação pelo comando, só dos termos sem estatuto

**Suprimida nesta change** por decisão do pesquisador (2026-11-28). Vai para a change geral
de otimização das consultas terminológicas (PD41). O texto abaixo fica como registro do que
estava previsto.

A ordem é `termos importar`, que reconcilia a planilha com o protocolo preservando as
decisões, seguido de `termos validar <sigla>`, um instrumento por vez. Os instrumentos são
os que o protocolo atribui:
- `brased` para pt;
- `unesco` para en e es;
- `eric` para en.

São sempre os mesmos para a FCT2 e a FCT3. As linhas que deixaram de valer ficam na
planilha, que é o registro do estatuto: não se apagam.

Antes da primeira chamada, `termos sondar` confere cada endereço. Diante de erro, bloqueio
ou limite, a validação para e o fato se relata. A falha de acesso fica como pendência, e
não como "não localizado".

### D3. Descritores propostos pelo agente, decididos pelo ReT

**Suprimida nesta change** por decisão do pesquisador (2026-11-28). Vai para a change geral
de otimização das consultas terminológicas (PD41). O texto abaixo fica como registro do que
estava previsto.

O agente lê o estatuto proposto e a evidência de cada termo e propõe, por termo, a linha do
quadro, com a regra de 2026-11-24:
- descritor em algum dos instrumentos planejados vai para "Descritores correspondentes";
- sinônimo ou relacionado vai para "Termos sinônimos ou relacionados";
- o resto vai para "Termo livre".

A proposta vai, enxuta, para `openspec/changes/medicao-proximidade-e-ampliacao-da-fct2/revisao_descritores.md`
(termo livre → descritor proposto), a pedido do pesquisador, porque a planilha é extensa
demais para a revisão. O pesquisador preenche a
`decisao_ReT`, e só então se alteram as linhas do quadro. Termo sem decisão fica em
"Termo livre".

### D4. Flexão por exceção declarada

- Pela decisão de 2026-11-23, `ensino`, `aprendizagem`, `teaching`, `learning`,
  `enseñanza` e `aprendizaje` são substantivos de processo, não contáveis, e entram em
  `docs/flexoes.toml` com essa origem.
- `ensino-aprendizagem` e `enseñanza-aprendizaje` são formas compostas de processo, não
  contáveis como `teaching-learning`.
- Os descritores já no plural `métodos de ensino`, `educational practices` e
  `teaching methods` ganham o singular como forma complementar, como `fatores de rendimento
  escolar`, porque a regra não decide o número deles.
- Os termos da FCT3 são contáveis, e a forma plural sai da regra. O ensaio de
  `strings gerar` e de `procedimentos gerar` mostra as formas antes de gravar.
- As exceções cujo termo saiu do quadro se retiram, sem registro histórico no arquivo.

O agente propõe as exceções, e o pesquisador as revisa antes de gravar.

### D5. A lista própria da STR2 na ERIC

A fonte da ERIC compõe a STR2 do resumo com uma lista própria. Com `learning` e `teaching`
na STR2, a lista passa a ter só um termo fora do quadro: `learner`, e o plural `learners`.
Há duas saídas:
- retirar os dois e ficar com o subconjunto da STR2;
- mantê-los como forma da base, e nesse caso a diferença em relação ao protocolo fica
  declarada na fonte.

Decisão do pesquisador (2026-11-27): vale a abordagem com maior potencial de recuperar
estudos aderentes às questões. `learner` e `learners` ficam como forma da base, porque o
modelo de aprendiz (perfil, adaptação) é objeto central de QER3 e de várias sementes. A
diferença em relação ao protocolo fica declarada na fonte da ERIC.

### D6. Transformações `distancia` e `restricao`, de composição

As duas se aplicam na composição, como `sem_proximidade` e `metade`, e não por substituição
no texto. A transformação que não muda a consulta reprova (spec `sondagens-por-base`).

Alternativas consideradas:
- **Texto literal com as strings coladas.** Recusada: diverge na alteração seguinte do quadro.
- **Expressões novas em `[execucao]`.** Recusada: entrariam nas contagens e na derivação, e
  a grade fica fora do corpus.
- **`acrescimo`, para comparar a FCT2 antiga com a nova na mesma sessão.** Retirada: os
  termos novos já estão no protocolo, e a FCT2 antiga não volta por transformação, porque
  `ensino e aprendizagem` saiu do quadro. A comparação com a FCT2 antiga usa a EB5
  registrada em 2026-11-25. Na WoS ela é a BD1/EX4, cujo texto coincide com o do procedimento
  daquela data. Na Scopus é a BD2/EX4, sem texto registrado. Essa comparação mistura o efeito
  da FCT2 com o da data e se relata assim.

### D7. A grade: uma sondagem por base, com `elementos` vazio

É uma sondagem nova, a seguinte da sequência na WoS e na Scopus, sem elemento de sintaxe:
ela mede volume, não sintaxe. A spec manda relatar, sem reprovar, a sondagem sem elemento.

| # | Papel | Proximidade | Transformação |
| :---: | :--- | :--- | :--- |
| 1 | controle | a declarada (5) | nenhuma |
| 2 | teste | 15 | `distancia = 15` |
| 3 | teste | `AND` | `sem_proximidade` |
| 4 | teste | `AND`, só o ruído | `sem_proximidade`, `restricao` |

A `restricao` é `ontology learning`, `machine learning`, `deep learning` e
`aprendizaje automático`. A consulta 4 dá um **limite inferior** da parcela de ruído: conta
só essas formas, e um registro que as contém pode ser elegível.

As leituras:
1. todas aceitas, com 1 ≤ 2 ≤ 3 e 4 ≤ 3: retornos medidos (`medicao`);
2. alguma recusada ou com mensagem: levar ao pesquisador (`nao_verificado`);
3. qualquer outra relação: inconclusiva (`nao_verificado`).

### D8. Restrição por DOI na WoS: `DO=({doi})`

A tag `DO=` está verificada em fonte oficial (§1 da WoS). O agrupamento por `OR` não está
medido, como o de `DOI()` na Scopus (PD40), e o roteiro leva a mesma cautela.

### D9. Nível do diagnóstico lido só com o texto vigente

O diagnóstico lia os níveis 4 e 5 das execuções registradas sem conferir o texto. Com as
STRs regeneradas, os níveis 1 a 3 sairiam com o vocabulário novo, e os 4 e 5 com o da
execução. A causa atribuída misturaria os dois. O registro de execução já guarda o texto
submetido (`texto`, gravado por `busca registrar`). Por isso a leitura passa a exigir que ele
seja igual ao texto vigente da expressão, com os espaços normalizados. Sem texto registrado,
como nas execuções da Scopus de 2026-11-25, a igualdade não se confere, e o nível também se
submete.

Alternativa considerada: avisar e ler mesmo assim. Recusada, porque o aviso não impede a
causa errada, e a garantia vem por construção.

Fica fora: a seleção das sementes diagnosticadas continua lida da exportação da executada
registrada. Ela é a medida da aderência daquela execução, e não um nível do diagnóstico.

## Riscos / Compromissos

- [`learning` e `teaching` como âncora ampliam muito a EB5, e a EB4 também, enquanto ela
  não é emendada] → a grade mede o volume antes da decisão. A execução definitiva só acontece
  depois da emenda.
- [Equivalente proposto pelo agente lido como autorizado] → a revisão do D1 vem antes de
  gravar. A ressalva "termos livres" continua nos procedimentos, e a validação do D2 é quem
  dá estatuto.
- [Falha de acesso a um instrumento no meio da validação] → parada imediata e pendência,
  sem nova tentativa (D2).
- [Uma consulta da grade passa do teto de caracteres da base] → o roteiro mostra o
  comprimento; a variante de partição prevista trata o caso, e a string não se encurta.
- [O retorno muda entre a data das execuções e a sessão da grade] → o controle vai na mesma
  sessão, e a grade se compara a ele.

## Plano de migração

Não há migração de dados. Os campos novos da sondagem são opcionais, e a fonte sem eles gera
o mesmo texto de antes. O protocolo, a planilha, as exceções e as fontes ficam no controle de
versão, e reverter é voltar ao commit anterior e regenerar.

## Questões em aberto

- O tratamento do hífen pela WoS e pela Scopus pode tornar redundante `teaching-learning`
  diante de `teaching` e `learning`. Isso não muda a grade e se observa na emenda.
