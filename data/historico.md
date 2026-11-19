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
