# Histórico

Linha do tempo das decisões relevantes sobre a revisão, inclusive as emendas, com data, alcance e fundamento. Entradas mais recentes ao final. As ações por fazer ficam em `data/pendencias.json`; os resultados das consultas nas bases, em `data/registro_execucao.json`.

## 2026-11-17 — Emenda de busca (versão 2 do protocolo)

Nota de emenda transcrita integralmente do protocolo, de onde saiu em 2026-11-18 por decisão do pesquisador (o protocolo passa a conter só a forma vigente).

#### Nota de emenda ao protocolo (versão 2 — 2026-11-17)

A versão 1 executava EB4 = STR1 + STR2 como busca definitiva, com EB1, EB2 e EB3 calculadas localmente. A execução revelou volume incompatível com a triagem no prazo e baixo alinhamento às QER2 e QER3, que são constitutivas do escopo. A versão 2 adota:

1. **EB4 = STR1 + STR2 + (STR3 OR STR4)** como busca definitiva. Exige ao menos um termo de prática ou de fator situacional. Equivale a EB2 ∪ EB3. A justificativa é conceitual, não apenas operacional: sem prática ou fator situacional, o registro não responde a QER2 nem a QER3.
2. **STR1** — remoção de termos genéricos: `ontológico`, `ontológica`, `ontological`, `taxonomia` (isolada), `modelo conceitual`, `modelagem conceitual`, `esquema conceitual`, `modelo semântico`, `representação formal`, `análise facetada`, `facet analysis`, `análisis facetado`, `análisis de facetas`. Adição de termos compostos de alta precisão: `ontologia educacional`, `ontologia de aprendizagem`, `ontologia de ensino`, `modelo ontológico educacional`, `ontologia de prática educacional`, `ontologia de design instrucional`, `ontologia de currículo`, `ontologia facetada` (e equivalentes em EN/ES). **Manutenção de `modelo de domínio`** (necessário à recuperação de SE4).
3. **STR2** — remoção de termos de altíssima frequência: `estudante`, `aluno`, `professor`, `docente`, `currículo`, `instituição de ensino`, `nível de ensino`, `modalidade de ensino`, `educativo` (isolado), e equivalentes em EN/ES. Esses conceitos permanecem em STR4 quando qualificados (`característica do aluno`, `contexto institucional` etc.).
4. **STR4** — remoção de `contexto de aplicação`, `contexto de uso` e `ambiente de aprendizagem` (duplicado de STR2), e equivalentes em EN/ES. Os demais termos foram mantidos, inclusive os de FCT4 que já estavam qualificados (`situação de uso educacional`, `contexto educacional`).
5. **EB5** (controle de sensibilidade) = STR1 + STR2, executada uma única vez como sonda de sensibilidade, fora do corpus: a perda `EB5 \ EB4` é amostrada para classificação manual de elegibilidade.
6. **Triagem estratificada** — E1 (EB1) antes de E2 (EB2 ou EB3). A calibração dos critérios é feita no estrato E1 antes de se passar ao E2.
7. **Operadores de proximidade e restrição por campo** — onde a base suportar (WoS: `TS=` e `NEAR/n`; Scopus: `TITLE-ABS-KEY()` e `W/n`; ERIC: `TI,AB,KW`; BRAPCI: verificar sintaxe), aplicar para reduzir falsos positivos de registros em que os termos aparecem em seções distintas sem conexão temática.

## 2026-11-18 — Emenda de redação das strings (decisão do ReT)

As strings passaram a incluir os termos do controle terminológico que a emenda de 2026-11-17 não retirou e que nelas faltavam: `ontological engineering` (STR1), `teaching practice` e `aprendiz` (STR2). Alcance: busca — as strings mudam; reexecução e teste de aderência seguem o fluxo do protocolo. Registro transcrito da nota que constava antes da tabela de strings do protocolo.

## 2026-11-18 — Protocolo reduzido à forma vigente

Saíram do protocolo o aviso de versão, o resumo "em relação à versão 1" das strings e a Nota de emenda (transcrita acima). A regra de operadores de proximidade e restrição por campo (item 7 da Nota) permanece em vigor, em "Expressões de busca"; a triagem estratificada (item 6) permanece na seção da ferramenta de triagem. Explicações resumidas; colunas "Justificativa" de CE1–CE9 e BD1–BD4 preservadas sem alteração. Alcance: redação.

## 2026-11-18 — Instrumentos de controle terminológico por faceta (decisão do ReT)

O protocolo passou a declarar os instrumentos de cada faceta na seção "Instrumentos para controle terminológico": FCT1 — TBCI e UNESCO Thesaurus; FCT2 a FCT4 — ERIC Thesaurus, Brased/INEP e UNESCO Thesaurus. Revoga-se a dispensa de validação de FCT4: a faceta de fatores situacionais deixa de ser termo livre por decisão e passa a ser validada. ERIC Thesaurus e Brased/INEP não têm cliente automatizado e são validados à mão. Alcance: método de validação terminológica; as strings não mudam.

## 2026-11-18 — Consistência entre plano, protocolo, fichas e README (decisão do ReT)

- Limiares fora do protocolo passam a ser remissão ao `config.toml` (o valor em uso sai em `python3 src/protocolo.py --mostrar`). A divergência admitida no teste de fidelidade é de até 10% (`divergencia_fidelidade`), substituindo a "coincidência exata das contagens" do plano. A sensibilidade mínima da calibração da triagem assistida (95%) passa a `calibracao_triagem`. Alcance: método (fidelidade); redação (demais).
- Referências a critérios por número antigo atualizadas: "critério 4" → CE5 (localização de itens) e "critério 5" → CE6 (adequação temática), no protocolo (triagem) e no README. A correspondência "critério 5" → CE6 foi inferida pelo deslocamento da numeração e pelo conteúdo (regra de borda), não por registro anterior. O plano deixa de citar "critérios de exclusão (i) e (b)". Alcance: redação.
- O plano deixa de descrever as expressões de busca (2.1, 3.3 e 6.2) e o recorte temporal (2.1), por remissão ao protocolo. Alcance: redação.
- Remissões das questões secundárias corrigidas para o protocolo, `docs/03`, "Questão de revisão". Alcance: redação.

## 2026-11-19 — Forma de execução literal por base (decisão do ReT)

As expressões que se executam passam a ser **bloco literal único**, submetido como está. WoS e Scopus entregam EB2, EB3, EB4 e EB5 literais — as âncoras em proximidade inline —, sem `#n` e sem receita de montagem; a subseção `#5` deixa de existir como forma. A BRAPCI entrega EB4 e EB5 literais; EB1, EB2 e EB3 são derivadas localmente e não levam bloco. A ERIC não muda de consulta: a forma particionada em quatro consultas de campo único já é literal. Alcance: forma de execução das quatro bases; a composição das expressões, a derivação local e a execução das buscas não mudam.

`--conferir` ganha três dimensões: bloco de expressão executada, de fidelidade ou de sonda não referencia conjunto `#n`; o conjunto de termos do bloco confere com as strings das facetas que a expressão declara, ignorando operador, campo, proximidade (`NEAR/n`, `W/n`) e valor de filtro; e bloco na expressão derivada padrão reprova — a forma longa, quando a ficha a declara, é representação não executada e fica fora. A conferência compara termos, não topologia: termo posto no grupo errado ou operador trocado continua guardado pela coerência pós-execução (`EB4 = EB2 ∪ EB3`, `EB5 ⊃ EB4`).

**Não verificado:** o comprimento máximo da consulta aceito pela WoS, pela Scopus e pela BRAPCI. As consultas expandidas têm cerca de 9.900, 10.000 e 4.100 caracteres; a aceitação se mede na primeira execução, com a sonda de EB5 e depois a de EB4, registrada em `data/registro_execucao.json`. Recusa por extensão vira emenda de partição, com as mesmas âncoras em todas as partes e união por deduplicação; a emenda declara `- Execução: particionada` e escreve as partes literais. Nenhuma execução está registrada (`data/registro_execucao.json` ausente, PD02): nenhuma contagem fica vencida por esta decisão.

## 2026-11-19 — Citações de medição sem lastro rebaixadas (decisão do ReT)

As quatro fichas afirmavam verificação por medição e citavam `data/registro_execucao.json` como fonte, mas o registro não existe no repositório. Decisão: **rebaixar para Não verificado**, sem reconstituir as medições, porque não há dado que as sustente. Alcance: `docs/busca_base_wos.md` e `docs/busca_base_scopus.md`, seção 1; `docs/busca_base_eric.md` e `docs/busca_base_brapci.md`, cabeçalho e linhas de medição que dele dependem. A medição fica remetida à primeira execução e se registra então, com a execução nomeada. As strings e a composição das expressões não mudam; nenhuma contagem é afetada.

## 2026-11-19 — Fundamento quantitativo da emenda v2 não registrado

A nota de emenda de 2026-11-17 afirma que "a execução revelou volume incompatível com a triagem no prazo", mas não traz contagem, e as contagens da execução da versão 1 não foram registradas nem estão com o pesquisador. Alcance: o fundamento quantitativo da emenda v2 fica declarado **não registrado**; nenhuma contagem é reconstituída de memória. A justificativa conceitual da emenda — QER2 e QER3 constitutivas do escopo — permanece, e é ela que sustenta a forma vigente.

## 2026-11-19 — Revisão geral do projeto como skill própria (decisão do ReT)

A revisão geral do projeto passa a ser procedimento reproduzível, na skill `revisao-geral-do-projeto`, separada da `parecer-sobre-protocolo`, que fica restrita à avaliação de parecer externo. A revisão geral **produz** achados percorrendo o estado do projeto; o parecer **confere** achados que chegam prontos. A skill nova remete ao README os comandos de conferência e à `parecer-sobre-protocolo` as classes de achado, sem os copiar. Alcance: procedimento do agente; os instrumentos da revisão não mudam.

## 2026-11-19 — Critérios de elegibilidade no protocolo (decisão do ReT)

O protocolo passa a enunciar sozinho o que a triagem aplica. A regra operacional de inclusão só existia no plano (`01_plano.md`, 2.4), embora o README declare o protocolo prevalente.

- A regra única de inclusão — o estudo formaliza, no domínio educacional, práticas do processo de ensino-aprendizagem **e/ou** os fatores situacionais que as condicionam — vira o critério de inclusão **CE7**, com a **regra de exceção** e a **regra de borda** em nota imediatamente após a tabela. O plano substitui a regra e a lista "Ficam fora do recorte" por remissão ao protocolo.
- O contra-escopo vira quatro critérios de exclusão nomeados, **CE9 a CE12**, um por item, para que a exclusão da 3ª filtragem cite o motivo por ID no fluxograma PRISMA. A não pertinência temática geral fica no **CE8**.
- As revisões sistemáticas e de escopo saem do CE4 e entram pelo **CE5**, com destino declarado: conjunto suplementar, com contagem própria, fora do portfólio de evidência primária.
- A localização de itens passa a **CE6** e declara a verificação na **segunda filtragem, de título e resumo**.
- A numeração passa de CE1–CE9 a **CE1–CE15**: os antigos CE7, CE8 e CE9 passam a CE13, CE14 e CE15.
- A coluna "Justificativa" passa a estar preenchida em todas as linhas; estavam vazias as de localização de itens e de adequação temática.

Alcance: **elegibilidade** — muda o que entra e por qual motivo; as strings e as expressões não mudam, e a busca não é reexecutada. As quatro fichas, o README e as skills são atualizados para os IDs vigentes. `--conferir` ganha duas dimensões: reprova critério de elegibilidade com justificativa vazia, e reprova, por base, a ficha cuja seção 2 não cite exatamente os IDs da tabela do protocolo. Cada uma tem caso de autoteste que injeta o defeito e prova a reprovação.

## 2026-11-19 — Conjunto-semente por papel: validação decide a aderência (decisão do ReT)

O conjunto-semente tinha 10 estudos e 15 incidências, sem distinguir os que orientaram o vocabulário dos que não orientaram. A emenda de 2026-11-17 registra que `modelo de domínio` foi mantido "necessário à recuperação de SE4": essa semente é recuperada por construção, e a aderência medida sobre ela fica inflada. Nenhuma aderência estava registrada (`data/registro_execucao.json` ausente), de modo que a correção não descarta resultado.

Decisões:

- **D1 (a) — separar desenvolvimento e validação.** Semente que motivou a inclusão, a manutenção ou a retirada de um termo é de **desenvolvimento**; as demais são de **validação**. Só a aderência de validação é comparada ao limiar e decide a passagem; a de desenvolvimento é relatada como não decisória e não compensa a validação.
- **Classificação atual:** SE4 é desenvolvimento, por registro explícito da manutenção de `modelo de domínio`; SE1, SE2, SE3, SE5, SE6, SE7, SE8, SE9 e SE10 são validação. A suspeita de que SE2 e SE9 tenham orientado `ontologia facetada` e `ontologia de currículo` é **não verificada** e não basta para reclassificá-las; fica registrada para conferência.
- **D2 — manter o conjunto atual e ampliar depois.** O conjunto de validação fica com 9 sementes por ora; a ampliação se registra como pendência, com tamanho-alvo a fixar pelo pesquisador. O limiar continua **80%**, agora aplicado só à validação: 80% exige **8 de 9 (88,9%)**, pois 7/9 = 77,8%.
- **Intervalo:** o relato da validação passa a trazer o intervalo de Wilson a 95%, junto da proporção.

Alcance: **método de aferição da aderência** — muda o denominador que decide a passagem e a forma do relato; as strings, as expressões, o recorte e o limiar de 80% não mudam, e a busca não é reexecutada. O denominador definitivo continua sendo a coluna `indexado` da planilha, conferida à mão; o relato por papel é sobre as sementes informadas.

A coluna `Papel` entra na tabela do conjunto-semente e é exigida pela leitura: papel ausente, fora do domínio (`desenvolvimento` ou `validação`) ou conjunto de validação vazio reprova `--conferir`. `gen_semente.py` passa a gravar a coluna `papel`, e `--aderencia` relata validação e desenvolvimento separadamente, com o intervalo de Wilson. A classificação foi registrada antes de qualquer execução; `data/registro_execucao.json` continua ausente.

## 2026-11-19 — Conferência do conjunto-semente declarada pelo pesquisador

O pesquisador declarou ter conferido a indexação das 10 sementes nas quatro bases e os dados bibliográficos (autoria, título, veículo, ano e DOI). A coluna `Bases` e as referências do protocolo foram mantidas; a seção 5 das quatro fichas confere com a coluna, e `--conferir` exibe a mesma distribuição por base (wos 4, scopus 6, eric 3, brapci 2). A conferência não detalhou data e fonte por base; a declaração foi registrada em 2026-11-19.

A verificação bibliográfica foi registrada em `data/sementes.json`; `escopo`, `tipo` e `alinhamento` continuam pendentes (PD01), porque não constam do protocolo e são juízos autorais. O DOI da SE10 registrado é o do volume dos anais; o DOI do capítulo não foi registrado, e a ficha da WoS já remete à busca por título na etapa 2.

Alcance: **dados do conjunto-semente** — as strings, as expressões, a composição e o limiar não mudam; a busca não é reexecutada. Nenhuma célula foi preenchida de memória: os dados são os do protocolo, confirmados pelo pesquisador.

## 2026-11-19 — Correções da verificação do conjunto-semente (decisão do ReT)

A verificação da change `conjunto-semente-independente` apontou quatro avisos e duas sugestões. As correções aplicadas:

- **DOI do capítulo da SE10 — retificação.** A entrada anterior registrava o DOI do volume dos anais (`10.5771/9783956507762`) e dizia que o DOI do capítulo não fora registrado. O capítulo tem DOI próprio, `10.5771/9783956507762-484`, conferido no Crossref em 2026-11-19; a resposta bruta está em `data/evidencia/referencias/SE10_crossref.json`, e o registro extraído, em `SE10_crossref.md`. O protocolo, `data/sementes.json` e a ficha da WoS foram corrigidos.
- **Regra de ajuste do protocolo.** A prosa passou a dizer que o limiar de 80% se aplica às **sementes de validação**, sobre a união das bases; as de desenvolvimento são relatadas à parte e não compensam a validação. O valor do limiar, as strings, as expressões e o recorte não mudaram.
- **Conferência do conjunto-semente.** O lastro ficou declarado como limitação: a conferência de indexação é declaração do pesquisador e não detalhou data e fonte por base; não se apresenta como verificação independente (PD19). A classificação por papel foi registrada antes de qualquer execução registrada; PD17, se confirmada como aderência das strings vigentes, exige reavaliar essa ordem.
- **Casamento por prefixo.** `--aderencia` deixou de contar o casamento por prefixo como recuperação: ele é impresso como `[? ]`, fica fora do numerador e exige conferência humana e registro na coluna `recuperada`. A mudança alinha o código à skill `teste-de-aderencia`; não havia aderência registrada, de modo que nenhum resultado é afetado.
- **Testes.** O autoteste de `derivar_expressoes.py` ganhou casos para título exato, prefixo como indício e preservação do total recuperado; o de `protocolo.py` continua cobrindo papel ausente, papel fora do domínio e conjunto de validação vazio e executou 113 casos, com 10 ainda não executados por falta de `data/registro_execucao.json` (PD02). A preservação "Mesmo resultado" foi conferida por inspeção do diff — as funções de derivação, fidelidade e sensibilidade não foram tocadas, e a prova da composição e as deriváveis seguem no autoteste existente.

Alcance: **método de aferição da aderência e dados do conjunto-semente** — o numerador deixa de aceitar prefixo sem conferência, e o DOI e a prosa do limiar são corrigidos. As strings, as expressões, o recorte e o valor do limiar não mudam; a busca não é reexecutada.
