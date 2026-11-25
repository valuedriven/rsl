# Histórico

Linha do tempo das decisões arquiteturais da revisão (questão, escopo, critérios, método, estratégia de busca), inclusive as emendas, em entradas curtas com data, alcance e fundamento. Entradas mais recentes ao final. As ações por fazer ficam em `data/pendencias.json`; os resultados das consultas nas bases, em `data/registro_execucao.json`.

## 2026-11-17 — Emenda de busca (versão 2 do protocolo)

A versão 1 executava EB4 = STR1 + STR2. A execução revelou volume incompatível com a triagem no prazo e baixo alinhamento às QER2 e QER3, constitutivas do escopo. A versão 2 adota:

- **EB4 = STR1 + STR2 + (STR3 OR STR4)** como busca definitiva: sem prática ou fator situacional, o registro não responde a QER2 nem a QER3;
- retirada de termos genéricos da STR1 e de termos de altíssima frequência da STR2, e entrada de termos compostos de alta precisão na STR1;
- **EB5 = STR1 + STR2** como sonda de sensibilidade, fora do corpus, com amostragem da perda `EB5 \ EB4`;
- triagem estratificada, E1 (EB1) antes de E2 (EB2 ou EB3);
- proximidade e restrição por campo onde a base suportar.

As contagens da execução da versão 1 não foram registradas, e o fundamento quantitativo fica **não registrado**. A emenda se sustenta pela justificativa conceitual. Alcance: **busca**.

## 2026-11-18 — Termos acrescentados às strings

Entram nas strings os termos do controle terminológico que a emenda de 2026-11-17 não retirou e que nelas faltavam: `ontological engineering` (STR1), `teaching practice` e `aprendiz` (STR2). Alcance: **busca**.

## 2026-11-18 — Instrumentos de controle terminológico por faceta

FCT1 se valida no TBCI e no UNESCO Thesaurus; FCT2 a FCT4, no ERIC Thesaurus, no Brased/INEP e no UNESCO Thesaurus. A FCT4 deixa de ser termo livre por decisão e passa a ser validada. Alcance: **método** (validação terminológica).

## 2026-11-18 — Limiar do teste de fidelidade

A divergência admitida no teste de fidelidade passa a ser de até 10% (`divergencia_fidelidade`), em vez da coincidência exata das contagens. Alcance: **método**.

## 2026-11-19 — Expressões executadas como bloco literal

Cada expressão executada é um bloco literal único, submetido como está, sem montagem por `#n`. Recusa por extensão vira emenda de partição: as mesmas âncoras em todas as partes e união por deduplicação. Alcance: **busca** (forma de execução); a composição das expressões não muda.

## 2026-11-19 — Critérios de elegibilidade no protocolo

O protocolo passa a enunciar sozinho o que a triagem aplica. A regra única de inclusão (formalização, no domínio educacional, de práticas do processo de ensino-aprendizagem e/ou dos fatores situacionais que as condicionam) vira critério, com a regra de exceção e a regra de borda. As revisões sistemáticas e de escopo vão para um conjunto suplementar, fora do portfólio de evidência primária. Alcance: **elegibilidade**.

## 2026-11-19 — Aderência decidida pelas sementes de validação

- Semente que motivou a inclusão, a manutenção ou a retirada de um termo é de **desenvolvimento**, e as demais são de **validação**. SE4 é de desenvolvimento, porque `modelo de domínio` foi mantido para recuperá-la.
- Só a aderência de validação, sobre a união das bases, é comparada ao limiar de **80%**. A de desenvolvimento é relatada à parte e não compensa a de validação.
- O relato traz o intervalo de Wilson a 95%.
- O casamento por prefixo não conta como recuperação sem conferência humana.
- O conjunto atual fica, e a ampliação é pendência.
- A conferência de indexação das sementes é declaração do pesquisador, e não verificação independente.

Alcance: **método** (aferição da aderência).

## 2026-11-20 — Critérios CE1 a CE9, STR2 reduzida e faixa da sonda

- **Critérios renumerados de CE1 a CE9.** CE6 é a regra única de inclusão por adequação temática. Os critérios de exclusão temática nomeados e o de localização de itens saíram da tabela, e a não pertinência e o contra-escopo se fundem no CE6. O fundamento dessa mudança de conteúdo não foi registrado. Alcance: **elegibilidade**.
- **STR2 alinhada ao quadro de FCT2**, depois de o pesquisador retirar termos do quadro. Alcance: **busca**.
- **Faixa da sonda (N3).** Fração elegível de EB5 − EB4 abaixo do limite inferior favorece a executada. Acima do superior, exige reconsideração. Entre os dois, é inconclusiva e requer análise qualitativa. Alcance: **método**.
- **Texto completo não restringe a busca.** A falta de texto completo se trata na triagem (P4). Alcance: **busca**.

## 2026-11-22 — Fator de impacto, ASReview, risco de viés e busca complementar

- **CE10 (fator de impacto), com ação "Não aplicável":** documentado e não aplicado na seleção. Alcance: **elegibilidade**.
- **ASReview fora do escopo**, com a calibração da triagem assistida. A classificação assistida por LLM na 1ª filtragem não muda. Alcance: **método** (triagem).
- **Avaliação de risco de viés incluída** no protocolo. O procedimento e o instrumento estão a definir (PD25). Alcance: **método**.
- **Busca complementar:** backward citation searching de uma geração, só sobre os estudos incluídos, sem forward (P11). Alcance: **método**.

## 2026-11-22 — Revisão das questões, das facetas e do controle terminológico

- **Escopo.** QER1 e OE1 passam a "propostos, especificados, aplicados ou avaliados". OE4, como a QER4, passa a "limitações, lacunas, incompatibilidades e insuficiências de integração entre práticas educacionais e fatores situacionais". O objetivo geral e o CE6 passam a "fatores situacionais associados à sua aplicação". Alcance: **escopo**.
- **"e" × "e/ou".** A QGR e o objetivo geral, com "e", tratam do recorte da revisão. O CE6 e a EB4, com "e/ou", tratam da inclusão de cada estudo.
- **STR gerada do quadro da faceta**, menos os termos subsumidos por outro da mesma STR. Cada termo fica numa só faceta. Alcance: **busca**.
- **Artefatos conceituais na FCT1** (`modelo conceitual`, `modelagem conceitual`, `esquema conceitual`, `modelo semântico`, `taxonomia` e equivalentes), revertendo parte da emenda v2. O risco aceito é a volta do ruído, como a taxonomia de Bloom. Alcance: **busca**.
- **Nível, modalidade, instituição, ambiente e infraestrutura de ensino passam da FCT4 à FCT2.** Amplia a âncora de domínio, e o efeito se mede na sonda. Alcance: **busca**.
- **População-alvo e recurso disponível saem do quadro** e passam a ser variáveis de extração (G4). Alcance: **busca**.
- **Formas por simetria entre idiomas**, propostas por IA e revisadas pelo pesquisador. Alcance: **busca**.

## 2026-11-23 — Plural explícito gerado por regra

Com plural explícito, a forma de número se gera por regra de pt, en e es, com exceções declaradas em `docs/flexoes.toml`. Os substantivos de processo ou de área são não contáveis em pt, es e en. `teaching-learning` entra no quadro da FCT2. Alcance: **busca**.

## 2026-11-24 — Controle terminológico pela natureza do termo

- **Critério.** A linha do termo resulta da `decisao_ReT` da planilha de validação, nos instrumentos planejados para a faceta e o idioma. Descritor em algum vai para "Descritores correspondentes". Senão, sinônimo ou relacionado em algum vai para "Termos sinônimos ou relacionados". Senão, vai para "Termo livre". A proposta da máquina não classifica.
- **Termo sem decisão do ReT vai para "Termo livre"**, pela regra do plano. As linhas de descritores e de sinônimos ou relacionados vazias significam "não validado", e não "inexistente".
- **A STR é composta só por "Termo livre" e "Descritores correspondentes".** "Termos sinônimos ou relacionados" não entra na STR.
- **En e es da linha "Termo livre" têm só os equivalentes dos termos pt.** Os equivalentes são tradução proposta pelo agente, não conferida em fonte de autoridade.
- **O teste de aderência será refeito**, porque as STRs mudaram de conteúdo.

Alcance: **método** e **busca**.

## 2026-11-25 — Descritores aceitos pelo ReT

- **Descritores correspondentes**, por correspondência exata nos instrumentos do protocolo: `representação do conhecimento`, `organização do conhecimento` e `ontologias` (TBCI); `ontology` e `ontología` (UNESCO); `educação` (Brased), `education` (UNESCO e ERIC) e `educación` (UNESCO); `métodos de ensino` (Brased), `educational practices` (ERIC), `teaching methods` (UNESCO e ERIC) e `método de enseñanza` (UNESCO); `educational environment` (UNESCO e ERIC) e `ambiente educacional`, em es (UNESCO).
- **A forma livre no singular permanece** ao lado do descritor no plural (`ontologia`, `método de ensino`, `educational practice`, `teaching method`).
- **`ambiente educacional` (pt) fica termo livre:** o Brased não tem o termo, e o candidato que sugere é outro conceito.
- **`contexto de aprendizaje` (es) fica termo livre:** na UNESCO é entrada não preferida de `Ambiente educacional`, e o descritor adotado é a forma preferida. O termo continua na STR4.
- **O teste de aderência será refeito.** Pela flexão, a única forma nova nas expressões é `ambientes educacionales`, na WoS e na Scopus. Na ERIC e na BRAPCI, só a ordem dos termos mudou.

Alcance: **busca**.
