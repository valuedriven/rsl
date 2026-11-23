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

As expressões que se executam passam a ser **bloco literal único**, submetido como está. WoS e Scopus entregam EB2, EB3, EB4 e EB5 literais — as âncoras em proximidade inline —, sem `#n` e sem receita de montagem; a subseção `#5` deixa de existir como forma. A BRAPCI entrega EB4 e EB5 literais; EB1, EB2 e EB3 são derivadas localmente e não levam bloco. A ERIC não muda de consulta: a forma particionada em consultas de campo único já é literal. Alcance: forma de execução das bases; a composição das expressões, a derivação local e a execução das buscas não mudam.

`--conferir` ganha as dimensões seguintes: bloco de expressão executada, de fidelidade ou de sonda não referencia conjunto `#n`; o conjunto de termos do bloco confere com as strings das facetas que a expressão declara, ignorando operador, campo, proximidade (`NEAR/n`, `W/n`) e valor de filtro; e bloco na expressão derivada padrão reprova — a forma longa, quando a ficha a declara, é representação não executada e fica fora. A conferência compara termos, não topologia: termo posto no grupo errado ou operador trocado continua guardado pela coerência pós-execução (`EB4 = EB2 ∪ EB3`, `EB5 ⊃ EB4`).

**Não verificado:** o comprimento máximo da consulta aceito pela WoS, pela Scopus e pela BRAPCI. A aceitação se mede na primeira execução, com a sonda de EB5 e depois a de EB4, registrada em `data/registro_execucao.json`. Recusa por extensão vira emenda de partição, com as mesmas âncoras em todas as partes e união por deduplicação; a emenda declara `- Execução: particionada` e escreve as partes literais. Nenhuma execução está registrada (`data/registro_execucao.json` ausente, PD02): nenhuma contagem fica vencida por esta decisão.

## 2026-11-19 — Citações de medição sem lastro rebaixadas (decisão do ReT)

As fichas afirmavam verificação por medição e citavam `data/registro_execucao.json` como fonte, mas o registro não existe no repositório. Decisão: **rebaixar para Não verificado**, sem reconstituir as medições, porque não há dado que as sustente. Alcance: `docs/busca_base_wos.md` e `docs/busca_base_scopus.md`, seção 1; `docs/busca_base_eric.md` e `docs/busca_base_brapci.md`, cabeçalho e linhas de medição que dele dependem. A medição fica remetida à primeira execução e se registra então, com a execução nomeada. As strings e a composição das expressões não mudam; nenhuma contagem é afetada.

## 2026-11-19 — Fundamento quantitativo da emenda v2 não registrado

A nota de emenda de 2026-11-17 afirma que "a execução revelou volume incompatível com a triagem no prazo", mas não traz contagem, e as contagens da execução da versão 1 não foram registradas nem estão com o pesquisador. Alcance: o fundamento quantitativo da emenda v2 fica declarado **não registrado**; nenhuma contagem é reconstituída de memória. A justificativa conceitual da emenda — QER2 e QER3 constitutivas do escopo — permanece, e é ela que sustenta a forma vigente.

## 2026-11-19 — Revisão geral do projeto como skill própria (decisão do ReT)

A revisão geral do projeto passa a ser procedimento reproduzível, na skill `revisao-geral-do-projeto`, separada da `parecer-sobre-protocolo`, que fica restrita à avaliação de parecer externo. A revisão geral **produz** achados percorrendo o estado do projeto; o parecer **confere** achados que chegam prontos. A skill nova remete ao README os comandos de conferência e à `parecer-sobre-protocolo` as classes de achado, sem os copiar. Alcance: procedimento do agente; os instrumentos da revisão não mudam.

## 2026-11-19 — Critérios de elegibilidade no protocolo (decisão do ReT)

O protocolo passa a enunciar sozinho o que a triagem aplica. A regra operacional de inclusão só existia no plano (`01_plano.md`, 2.4), embora o README declare o protocolo prevalente.

- A regra única de inclusão — o estudo formaliza, no domínio educacional, práticas do processo de ensino-aprendizagem **e/ou** os fatores situacionais que as condicionam — vira o critério de inclusão **CE7**, com a **regra de exceção** e a **regra de borda** em nota imediatamente após a tabela. O plano substitui a regra e a lista "Ficam fora do recorte" por remissão ao protocolo.
- O contra-escopo vira critérios de exclusão nomeados, **CE9 a CE12**, um por item, para que a exclusão da 3ª filtragem cite o motivo por ID no fluxograma PRISMA. A não pertinência temática geral fica no **CE8**.
- As revisões sistemáticas e de escopo saem do CE4 e entram pelo **CE5**, com destino declarado: conjunto suplementar, com contagem própria, fora do portfólio de evidência primária.
- A localização de itens passa a **CE6** e declara a verificação na **segunda filtragem, de título e resumo**.
- A numeração passa de CE1–CE9 a **CE1–CE15**: os antigos CE7, CE8 e CE9 passam a CE13, CE14 e CE15.
- A coluna "Justificativa" passa a estar preenchida em todas as linhas; estavam vazias as de localização de itens e de adequação temática.

Alcance: **elegibilidade** — muda o que entra e por qual motivo; as strings e as expressões não mudam, e a busca não é reexecutada. As fichas, o README e as skills são atualizados para os IDs vigentes. `--conferir` ganha as dimensões seguintes: reprova critério de elegibilidade com justificativa vazia, e reprova, por base, a ficha cuja seção 2 não cite exatamente os IDs da tabela do protocolo. Cada uma tem caso de autoteste que injeta o defeito e prova a reprovação.

## 2026-11-19 — Conjunto-semente por papel: validação decide a aderência (decisão do ReT)

O conjunto-semente não distinguia os que orientaram o vocabulário dos que não orientaram. A emenda de 2026-11-17 registra que `modelo de domínio` foi mantido "necessário à recuperação de SE4": essa semente é recuperada por construção, e a aderência medida sobre ela fica inflada. Nenhuma aderência estava registrada (`data/registro_execucao.json` ausente), de modo que a correção não descarta resultado.

Decisões:

- **D1 (a) — separar desenvolvimento e validação.** Semente que motivou a inclusão, a manutenção ou a retirada de um termo é de **desenvolvimento**; as demais são de **validação**. Só a aderência de validação é comparada ao limiar e decide a passagem; a de desenvolvimento é relatada como não decisória e não compensa a validação.
- **Classificação atual:** SE4 é desenvolvimento, por registro explícito da manutenção de `modelo de domínio`; SE1, SE2, SE3, SE5, SE6, SE7, SE8, SE9 e SE10 são validação. A suspeita de que SE2 e SE9 tenham orientado `ontologia facetada` e `ontologia de currículo` é **não verificada** e não basta para reclassificá-las; fica registrada para conferência.
- **D2 — manter o conjunto atual e ampliar depois.** O conjunto de validação fica como está por ora; a ampliação se registra como pendência, com tamanho-alvo a fixar pelo pesquisador. O limiar continua **80%**, agora aplicado só à validação.
- **Intervalo:** o relato da validação passa a trazer o intervalo de Wilson a 95%, junto da proporção.

Alcance: **método de aferição da aderência** — muda o denominador que decide a passagem e a forma do relato; as strings, as expressões, o recorte e o limiar de 80% não mudam, e a busca não é reexecutada. O denominador definitivo continua sendo a coluna `indexado` da planilha, conferida à mão; o relato por papel é sobre as sementes informadas.

A coluna `Papel` entra na tabela do conjunto-semente e é exigida pela leitura: papel ausente, fora do domínio (`desenvolvimento` ou `validação`) ou conjunto de validação vazio reprova `--conferir`. `gen_semente.py` passa a gravar a coluna `papel`, e `--aderencia` relata validação e desenvolvimento separadamente, com o intervalo de Wilson. A classificação foi registrada antes de qualquer execução; `data/registro_execucao.json` continua ausente.

## 2026-11-19 — Conferência do conjunto-semente declarada pelo pesquisador

O pesquisador declarou ter conferido a indexação das sementes nas bases e os dados bibliográficos (autoria, título, veículo, ano e DOI). A coluna `Bases` e as referências do protocolo foram mantidas; a seção 5 das fichas confere com a coluna, e `--conferir` exibe a mesma distribuição por base. A conferência não detalhou data e fonte por base; a declaração foi registrada em 2026-11-19.

A verificação bibliográfica foi registrada em `data/sementes.json`; `escopo`, `tipo` e `alinhamento` continuam pendentes (PD01), porque não constam do protocolo e são juízos autorais. O DOI da SE10 registrado é o do volume dos anais; o DOI do capítulo não foi registrado, e a ficha da WoS já remete à busca por título na etapa 2.

Alcance: **dados do conjunto-semente** — as strings, as expressões, a composição e o limiar não mudam; a busca não é reexecutada. Nenhuma célula foi preenchida de memória: os dados são os do protocolo, confirmados pelo pesquisador.

## 2026-11-19 — Correções da verificação do conjunto-semente (decisão do ReT)

A verificação da change `conjunto-semente-independente` apontou avisos e sugestões. As correções aplicadas:

- **DOI do capítulo da SE10 — retificação.** A entrada anterior registrava o DOI do volume dos anais (`10.5771/9783956507762`) e dizia que o DOI do capítulo não fora registrado. O capítulo tem DOI próprio, `10.5771/9783956507762-484`, conferido no Crossref em 2026-11-19; a resposta bruta está em `data/evidencia/referencias/SE10_crossref.json`, e o registro extraído, em `SE10_crossref.md`. O protocolo, `data/sementes.json` e a ficha da WoS foram corrigidos.
- **Regra de ajuste do protocolo.** A prosa passou a dizer que o limiar de 80% se aplica às **sementes de validação**, sobre a união das bases; as de desenvolvimento são relatadas à parte e não compensam a validação. O valor do limiar, as strings, as expressões e o recorte não mudaram.
- **Conferência do conjunto-semente.** O lastro ficou declarado como limitação: a conferência de indexação é declaração do pesquisador e não detalhou data e fonte por base; não se apresenta como verificação independente (PD19). A classificação por papel foi registrada antes de qualquer execução registrada; PD17, se confirmada como aderência das strings vigentes, exige reavaliar essa ordem.
- **Casamento por prefixo.** `--aderencia` deixou de contar o casamento por prefixo como recuperação: ele é impresso como `[? ]`, fica fora do numerador e exige conferência humana e registro na coluna `recuperada`. A mudança alinha o código à skill `teste-de-aderencia`; não havia aderência registrada, de modo que nenhum resultado é afetado.
- **Testes.** O autoteste de `derivar_expressoes.py` ganhou casos para título exato, prefixo como indício e preservação do total recuperado; o de `protocolo.py` continua cobrindo papel ausente, papel fora do domínio e conjunto de validação vazio. A preservação "Mesmo resultado" foi conferida por inspeção do diff — as funções de derivação, fidelidade e sensibilidade não foram tocadas, e a prova da composição e as deriváveis seguem no autoteste existente.

Alcance: **método de aferição da aderência e dados do conjunto-semente** — o numerador deixa de aceitar prefixo sem conferência, e o DOI e a prosa do limiar são corrigidos. As strings, as expressões, o recorte e o valor do limiar não mudam; a busca não é reexecutada.

## 2026-11-19 — Scripts reunidos no pacote `src/rsl` (decisão de instrumento)

Os scripts (`src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e `src/gen_semente.py`) deram lugar ao pacote `src/rsl/`, com um ponto de entrada único, `python3 -m rsl <subcomando>`, a partir da raiz e com `src/` no caminho de importação (`PYTHONPATH=src`). Change `refatoracao-dos-scripts`.

- **Comandos.** As opções viraram subcomandos por atividade: `conferir`, `conferir-dados`, `autoteste` (agora um só, com a prova da composição e a aderência por papel), `mostrar`, `pendencias`, `gramatica`; `sementes sincronizar|planilha`; `termos sonda|exportar|validar|importar`; `busca registrar|derivar|aderencia|fidelidade|sensibilidade`. A correspondência com os nomes antigos está na spec `interface-de-comando`. README, skills, fichas e plano citam os subcomandos.
- **Códigos de saída.** Passam a distinguir a reprovação do conteúdo da falha em ler: 0 OK, 1 REPROVADO, 2 USO, 3 CONFIGURACAO, 4 PROTOCOLO_ILEGIVEL, 5 DADOS, 6 PARCIAL, 7 FONTE_EXTERNA. Antes, conferência reprovada, protocolo ilegível, configuração inválida e arquivo ausente saíam todos com 1, e o autoteste parcial saía com 0.
- **Nomes de arquivo.** A planilha de validação passa a `data/validacao_terminologica.csv` (a grafia anterior, "termológica", remete a calor); a saída de fidelidade, a `fidelidade_eb<n>.csv`. Todos os caminhos de entrada e de saída vêm do `config.toml` (`[dados]`, `[saidas]`).
- **Gramática do protocolo.** A forma que o leitor exige do protocolo e das fichas está declarada num só lugar do código e é exibida por `python3 -m rsl gramatica`. O leitor ficou mais estrito em pontos: o cabeçalho de seção tem de estar no nível declarado, e a linha de cada camada do quadro terminológico (núcleo, próximos, relacionados) passa a ser exigida, com PROTOCOLO_ILEGIVEL. Antes, a linha ausente era lida como camada vazia e reprovada como incoerência.
- **Fonte externa.** A validação terminológica deixou de repetir a requisição depois de erro de rede e de seguir para o termo seguinte depois de falha. Agora interrompe na hora, sem nova tentativa, conforme o AGENTS.md §9.

Fundamento: a exploração de 2026-11-19 verificou códigos de saída ambíguos, conteúdo fixado no código (caminhos, nomes de saída, literais do protocolo vigente nas mutações do autoteste), normalizações Unicode diferentes, código morto e a nova tentativa automática em `validar_termos.py` (proposta da change).

Alcance: **instrumento, não método**. Composição, critérios, limiares, strings e recorte não mudam. Antes da migração, gravou-se uma referência com o código antigo sobre exportações e um registro de execução sintéticos. Com o código novo, `mostrar` e `conferir` saíram idênticos byte a byte, e `registros.csv`, `contagens_busca.csv`, `ordem_triagem.csv`, a fidelidade e as sensibilidades também, com o nome novo. A comparação das normalizações (NFKD e NFD) sobre os termos do protocolo e das fichas e sobre os textos sintéticos não achou diferença, e ficou a NFKD. Valores que estavam fixos no código passaram ao `config.toml` sem mudança de valor: ano de recência da ordem de triagem (`busca.ano_recencia = 2022`), tamanho-alvo da amostra da sonda (`busca.amostra_sensibilidade = 50`) e dimensão do recorte (`conferencia.dimensao_recorte`). Nenhuma execução está registrada (PD02): nenhuma contagem fica vencida.

Mudanças de comportamento fora da forma, registradas para conferência:

- `termos validar --faceta n` passou a filtrar a faceta. Antes, comparava `FCTn` com `n` e não consultava nenhum termo.
- O cliente da UNESCO colhe os rótulos de TG, TE e TR nos idiomas que o protocolo declara para o instrumento (hoje `en, es`), e não mais em `en, es, fr`, que estavam fixos no código.
- A sonda dos clientes usa termos do próprio protocolo, e não termos fixos.
- O campo `forma` das execuções registradas passa a dizer `registrada por busca registrar`.

## 2026-11-20 — Emenda de forma do protocolo e leitor ajustado (change `reestruturacao-do-protocolo`)

O pesquisador reestruturou o protocolo depois de bf6b9bf, e o leitor deixou de lê-lo (`rsl conferir` saía com PROTOCOLO_ILEGIVEL). A change `reestruturacao-do-protocolo` ajustou a gramática e o leitor ao documento escrito, sem pedir mudança de forma ao protocolo. Mudanças de forma, todas feitas pelo pesquisador e agora aceitas pelo leitor:

- **Facetas em tabela.** A lista "Palavras significativas da questão de revisão" deu lugar à tabela "Facetas da questão de revisão" (`Id faceta | Faceta | Âncora obrigatória`, com `Sim`/`Não`). As âncoras são lidas da coluna, sem padrão no `config.toml` (`padroes.ancoras` saiu); tabela sem âncora reprova.
- **Nova tabela de expressões, com notas.** A tabela passou a `ID | Expressão de busca | Função protocolar`, sem as colunas Natureza e Detalhamento, e ganhou a subseção "Notas explicativas" (N1–N4). A executada e a sonda passaram a ser identificadas pela composição (a executada é a única com grupo OR; a sonda, a única formada só pelas âncoras), por decisão do pesquisador de 2026-11-20; saíram `[expressoes]`, `padroes.executada` e `padroes.sonda`. A faixa de sensibilidade (5% a 15%) é lida da nota citada pela executada (N3). O parágrafo de operadores de proximidade saiu do protocolo; a proximidade continua nas fichas.
- **Conjunto-semente em arquivo próprio.** A tabela de sementes saiu do protocolo para `docs/conjunto_semente.toml` (`[[sementes]]` com `id`, `semente`, `bases`, `papel`), localizado por `[documentos] sementes` do `config.toml`; o protocolo não cita o caminho, por decisão do pesquisador de 2026-11-20. A seção "Conjunto-semente" do protocolo mantém a regra de ajuste e a fórmula. O formato é intermediário: a decomposição do campo `semente` fica com a change `sementes-estruturadas-no-protocolo`. As sementes lidas do arquivo dão autoria, ano, título, DOI, bases e papel idênticos aos lidos da tabela de bf6b9bf, e a mesma distribuição por base e por papel.
- **"Ferramenta de gestão bibliográfica" substituída** pelas tabelas "Procedimentos", "Instrumentos" e "Ferramentas", que o leitor não interpreta.
- **Critérios renumerados de CE1 a CE9.** CE6 é a regra única de inclusão por adequação temática; os critérios de exclusão temática nomeados (antigos CE8 a CE12) e o de localização de itens (antigo CE6) não estão mais na tabela. O fundamento dessa mudança de conteúdo não foi registrado nesta change.
- **P5 corrigido.** Citava "CE7, regras de exceção e borda e CE8–CE15"; passou a "CE6 (adequação temática) e CE7–CE9".
- **Marcador da estrutura da questão** reescrito como "A estrutura da questão…".

Divergências que o levantamento da change não previa, encontradas quando a leitura voltou a passar, e decididas pelo pesquisador em 2026-11-20:

- **Separador do quadro terminológico.** O quadro passou a separar os termos por vírgula, e não mais por `\- `. Sem ajuste, o leitor lia cada célula como um termo só, sem reprovar. A gramática passou a declarar a vírgula como separador, e o separador antigo reprova. Nenhum termo do quadro de 73cf68a tinha vírgula interna.
- **Dimensão "Localização de itens"** retirada de `conferencia.dimensoes_criterio`, acompanhando a tabela de critérios.
- **STR2 alinhada ao quadro de FCT2.** O pesquisador retirou termos do quadro de FCT2. Continuam no quadro de FCT3 ou FCT4 (`método de ensino`, `estratégia de ensino`, `teaching practice`, `teaching method`, `teaching strategy`, `learning design`, `método de enseñanza`, `estrategia de enseñanza`, `situação de aprendizagem`, `situación de aprendizaje` — parte do D1 da change `revisao-das-strings-por-faceta`), e não estão em faceta nenhuma (`processo de ensino-aprendizagem`, `objeto de aprendizagem`, `trilha de aprendizagem`, `resultado de aprendizagem`, `classroom teaching`, `teaching-learning`, `learning process`, `learning object`, `learning analytics`, `learning outcome`, `teaching-learning process`, `proceso de enseñanza-aprendizaje`, `resultado de aprendizaje`). Os termos retirados saíram de STR2 e das strings de FCT2 das fichas (a ERIC não usa esses termos).
- **Critérios nas fichas** renumerados pelo mapa aprovado: CE1–CE5 iguais; a linha de texto completo (antigo CE6) saiu; antigo CE7 → CE6; não pertinência (CE8) e contra-escopo (CE9–CE12) fundidos numa linha, CE6; CE13/CE14 → CE7/CE8; CE15 → CE9.

Alcance: **forma** para os itens da emenda do pesquisador; **busca** para STR2 e as strings de FCT2 das fichas, que perderam termos e mudam o que EB4 e a sonda EB5 recuperam; **elegibilidade** para a renumeração dos critérios. Nenhuma execução está registrada (`data/registro_execucao.json` ausente), de modo que nenhuma contagem fica vencida; o teste de aderência ainda não foi feito com as strings novas.

Pendência de método, levada ao pesquisador: N3 diz que a fração elegível de 5% a 15% em EB5 − EB4 "é inconclusiva e requer análise qualitativa"; `rsl busca sensibilidade` relata essa faixa como "decisão de mérito do pesquisador, a registrar como emenda". O código não foi alterado.

## 2026-11-20 — Decisões sobre as pendências da change `reestruturacao-do-protocolo` (decisão do ReT)

- **Faixa inconclusiva da sonda.** Vale a regra de N3: uma fração elegível de EB5 − EB4 abaixo do limite inferior favorece a manutenção da executada; acima do superior exige reconsideração e, se necessário, emenda; entre os dois é inconclusiva e requer análise qualitativa. `rsl busca sensibilidade` passou a relatar as faixas nesses termos; antes chamava a faixa intermediária de "decisão de mérito".
- **Texto completo não restringe a busca.** A linha "texto completo" saiu das fichas, e a variante de contingência `AND OPENACCESS(1)` saiu da ficha da Scopus, com a ressalva que a acompanhava. A falta de texto completo é tratada na triagem (P4), e não na busca.
- **Skill `criterios-de-elegibilidade` genérica.** A skill deixou de citar critérios e regras deste protocolo (CE7, CE12, regra de borda e de exceção vigentes) e remete ao README e ao protocolo. Fica a pergunta de método que ela ensina: que critério passa a excluir o que um critério retirado alcançava.
- **Efeito das strings novas.** O efeito da retirada dos termos de STR2 sobre EB4 e EB5 será avaliado na busca (teste de aderência e sonda de sensibilidade), e não antes.

Alcance: **instrumento** (relato da sensibilidade e skill) e **busca** (sem restrição por acesso aberto na Scopus). Limiares, strings e critérios não mudam por estas decisões.

## 2026-11-20 — Conjunto-semente estruturado campo a campo (change `sementes-estruturadas-no-protocolo`)

O arquivo de sementes (`[documentos] sementes` do `config.toml`) passou do esquema intermediário (`id`, `semente` em texto livre, `bases`, `papel`) ao esquema estruturado, e é agora o único lugar de dado de semente. Decisões do pesquisador de 2026-11-19 e 2026-11-20, registradas na proposta da change.

- **Campos estruturados.** Os dados bibliográficos são campos (`autores` em lista, `ano` inteiro, `titulo`, `veiculo`, `volume`, `numero`, `paginas`, `doi`), e não se extraem mais da referência por padrão de texto: `_titulo()` e `_doi()` saíram do leitor. Entraram `facetas` (FCTn informadas pelo pesquisador) e `observacoes` (o que a referência traz e não cabe em outro campo, transcrito como está: SE4 "SciTePress"; SE5 "(UEL)"; SE6 "(Springer)"; SE10 os editores, "Aalborg, Dinamarca" e "Ergon Verlag"). `bases` passa a significar indexação, e não recuperação. A transcrição foi feita campo a campo, sem os leitores de padrão e sem completar dado de memória. A reconstituição a partir do campo `semente` não deixou sobra em nenhuma semente. O texto de `semente` diferia da célula da tabela de bf6b9bf só pelo escape `\.` em SE2, SE3, SE7 e SE8, e a diferença foi apresentada ao pesquisador antes da gravação.
- **Fusão dos dados de conferência, com o mesmo conteúdo.** `verificacao`, `tipo`, `alinhamento`, `nota`, `veiculo_conferido` e `eric` passaram de `data/sementes.json` ao arquivo de sementes, casados por DOI. A conferência campo a campo não deu diferença em nenhuma semente. `data/sementes.json` foi removido, e com ele `sementes sincronizar`, a ligação por DOI ou título, o aviso de entrada órfã e as chaves `[dados] sementes` e `[planilha] campos_autorais` do `config.toml`.
- **`escopo` retirado.** Estava vazio em todas as sementes, o que foi verificado antes da retirada. A planilha de aderência perdeu a coluna. Campo `escopo` no arquivo reprova como campo desconhecido.
- **Sequência de `id` mantida, com renumeração na retirada.** O `id` continua em sequência a partir de SE1, sem lacuna. Retirar uma semente renumera as seguintes. A retirada renomeia a evidência bruta, atualiza `data/pendencias.json` e registra neste histórico a correspondência entre `id` antigo e novo (skill `conjunto-semente`, §4). Evidência `SEn_…` de `id` que não está no arquivo reprova `conferir-dados`. A conferência percorre só a subpasta `referencias/` de `[dados] evidencia` (decisão do pesquisador de 2026-11-20).
- **DOI ausente é pendência, não reprovação.** `pendencias` relata o DOI ausente, as facetas vazias, a semente de validação sem faceta âncora e `tipo` ou `alinhamento` vazios. Nenhuma semente atual está sem DOI. Todas aparecem com facetas a informar (PD20). A regra para semente de validação sem âncora fica em branco por decisão do pesquisador (PD21). Com `facetas` vazia, só se relata "facetas a informar", e a falta de âncora não é relatada à parte (decisão do pesquisador de 2026-11-20).

Fundamento: o leitor de padrão lia sem reprovar, e errado, referência com ponto no título, com subtítulo ou com DOI fora do fim. Os metadados de conferência viviam noutro arquivo, ligados por um elo frágil (proposta da change).

Alcance: **instrumento**. Composição, critérios, limiares, strings, recorte e o próprio conjunto de sementes não mudam. A distribuição exibida por `mostrar` é a de antes; `semente_aderencia.csv` perde a coluna `escopo`, e a coluna `titulo` passa a vir sem o ponto final, que `_titulo()` incluía e o campo `titulo` não traz.

O que não se alterou e por quê:

- as entradas anteriores deste histórico citam o caminho e o esquema vigentes na data, e não se reescrevem;
- a mudança de forma do protocolo já foi registrada pela entrada de `reestruturacao-do-protocolo`;
- `conferir-dados` não confere se a evidência de um `id` existente é mesmo daquela semente. Depois de uma renumeração, arquivo não renomeado passa em silêncio. Comparar o DOI da evidência com o `doi` da semente fica em aberto, para decisão do pesquisador (design da change, Open Questions).

## 2026-11-22 — Fator de impacto como critério não aplicável e retirada do ASReview (decisão do ReT)

- **CE10 — Fator de impacto, ação "Não aplicável".** O critério que o RS Banyan prevê em M3/E1 entra na tabela de critérios do protocolo só para documentação: não é aplicado na seleção. As fichas ganharam a linha CE10 na seção 2, como `conferir` exige. A gramática do protocolo passou a admitir "Não aplicável" no domínio de 'Ação' (`src/rsl/gramatica.py`); `mostrar` conta os critérios por ação. Alcance: **critérios** (documental) e **instrumento** (gramática). Resolve PD24.
- **ASReview fora do escopo, com a calibração da triagem assistida.** A priorização da fila por aprendizado ativo saiu do plano (decisão 5b da §3.3, que deixa de ter subdivisão; §4.1, §6.1, §6.2, §7, §8.1 e §8.2) e, com ela, a calibração que só a ela servia: o parâmetro `padroes.calibracao_triagem` saiu do `config.toml` e do código (`config.py`, `leitura.py`) e, se voltar, reprova a configuração como chave desconhecida; a skill `calibracao-da-triagem` foi apagada; o guia de procedimentos perdeu o índice correspondente. A classificação assistida por LLM na 1ª filtragem (decisão 5) não muda. As pendências PD15 e PD30 foram apagadas por decisão do pesquisador, e a PD11 deixou de citar a calibração. Alcance: **método** (triagem) e **instrumento**.

Fundamento: decisão do pesquisador de 2026-11-22, na tarefa 4.1 da change `guia-de-procedimentos`.

O que não se alterou: as entradas anteriores deste histórico que citam o ASReview ou `calibracao_triagem` registram o estado da data e não se reescrevem.

## 2026-11-22 — Revisão das pendências, risco de viés, busca complementar e remissões a passo (decisão do ReT)

- **Pendência concluída sai do arquivo.** Até aqui, `data/pendencias.json` guardava as pendências resolvidas e descartadas com `estado` e `resolucao`. Passa a conter só ações não concluídas: a pendência resolvida ou descartada é excluída, e o que a encerrou fica neste histórico, que cita o `id`; o `id` não se reutiliza. O README (Três registros) foi ajustado. Saíram nesta data PD13 e PD14 (commits 726280a e 7249dac), PD19 (lastro limitado registrado em 2026-11-19, "Conferência do conjunto-semente"), PD24 (CE10, entrada anterior desta data), e as abaixo. Alcance: **instrumento** (forma do registro).
- **PD02 descartada.** Pedia reconstituir `data/registro_execucao.json` a partir das fichas. A decisão de 2026-11-19 ("Citações de medição sem lastro rebaixadas") já tinha recusado a reconstituição por falta de dado; o registro passa a existir na primeira execução, por `busca registrar`, coberta pelas PD07 a PD10 e PD16. A mensagem de `pendencias` que ainda manda reconstituir (`src/rsl/dados.py`) é corrigida pela change `correcoes-de-registro-e-aderencia`.
- **PD17 descartada.** Apontava um resultado de aderência sem registro (Scopus abaixo do limiar, WoS suspensa) que a skill `teste-de-aderencia` citava até 2026-11-18. Não há dado que o sustente e, mesmo que existisse, não valeria para as strings vigentes, alteradas em 2026-11-17 (emenda v2) e em 2026-11-20 (retirada de termos da STR2). A aderência se mede na primeira execução das strings vigentes. Com ela cai a ressalva sobre a ordem classificação × aderência.
- **Avaliação de risco de viés incluída (PD25).** O plano declara não aplicáveis os itens de risco de viés por instrumentos de ensaio clínico (§6.3). Decisão: incluir a avaliação de risco de viés no protocolo e retirar do plano a formulação de não aplicabilidade. Procedimento e instrumento ainda não definidos: a PD25 permanece aberta para isso, e o plano não muda até a emenda, para não ficar sem nenhuma das duas formulações. Alcance: **método** (seleção e relato).
- **Busca complementar: backward de uma geração, sem forward (PD26).** O plano previa backward de uma geração (§3.3, decisão 7); o P11 do protocolo previa backward e forward, sem fixar geração. Decisão: o protocolo declara, no P11, backward citation searching limitado a uma geração, apenas sobre os estudos incluídos, sem forward; a justificativa da BD1 deixou de citar o forward. O plano perdeu a decisão 7 da §3.3 (a compressão passa a vir das decisões restantes, §7) e remete ao P11 no cronograma de marcos e na mitigação de risco. Alcance: **método** (busca complementar). As expressões de busca, os critérios e o CE2 e CE5, que já falavam em backward, não mudam.
- **Remissão a passo pelo nome da atividade (PD22).** Plano, protocolo e skill `conjunto-semente` citavam passos do RS Banyan por ordinal ("Módulo 3, Etapa 2, 1º passo"). Passam a citar módulo, etapa e nome da atividade; o guia de procedimentos deixou de dizer que o ordinal "continua contável". Os ordinais foram conferidos contra o guia antes da troca e estavam corretos. Alcance: **redação**.

Fundamento: decisão do pesquisador de 2026-11-22, na revisão de `data/pendencias.json`.

O que não se alterou: as entradas anteriores deste histórico que citam ordinais, o forward ou o estado `resolvida` registram o estado da data e não se reescrevem; os artefatos das changes arquivadas também não.

## 2026-11-22 — Correções de registro e de aderência (change `correcoes-de-registro-e-aderencia`)

- **Planilha de aderência preserva o preenchimento manual (PD27).** `sementes planilha` regravava `data/semente_aderencia.csv` inteira e apagaria as colunas preenchidas à mão. Passa a ler a planilha anterior e a conservar as colunas manuais de cada linha, casada por `id` e `base` e confirmada pelo título normalizado. Se a regravação perderia conteúdo manual não vazio (linha sem par, título divergente, coluna fora do esquema), nada é gravado e o código é REPROVADO, com cada `id` × base × coluna nomeado; planilha anterior ilegível dá DADOS. A gravação passa por arquivo temporário. As colunas manuais estão declaradas num só lugar (`colunas()` em `src/rsl/sementes.py`). O autoteste ganhou casos que reprovam a gravação sem leitura e o descarte em vez da recusa; o caso acrescentado na verificação (linha vazia de base que deixou de existir é omitida) falha quando a linha vazia sem par é recusada. A skill `conjunto-semente` ("Retirar uma semente") ganhou o passo da planilha, e o README a trata como artefato misto. Nenhuma perda ocorreu: as colunas manuais estavam vazias.
- **`--retorno` obrigatório em `busca registrar` (PD28).** O parser exige o argumento, e o `-h` o mostra fora de colchetes; a sinopse em `docs/procedimentos.md` (M3/E2) foi atualizada.
- **Nome da coluna em `busca aderencia` (PD29).** A docstring e a saída citavam `indexado`; passam a citar a coluna pela declaração de `src/rsl/sementes.py` (`indexada`, `recuperada`).
- **`pendencias` deixa de mandar reconstituir o registro.** Com o registro de execução ausente, orienta registrar a primeira execução com `busca registrar`, como decidido em 2026-11-19 e no descarte da PD02 nesta data; um caso do autoteste o exige.

Alcance: **instrumento**. Fundamento: decisão do pesquisador de 2026-11-22, na tarefa 4.1 da change `guia-de-procedimentos` (PD27 a PD29). Saíram de `data/pendencias.json` PD27, PD28 e PD29.

O que não se alterou: a forma da planilha de aderência (colunas, ordem, separador, codificação); `busca sensibilidade`; strings, critérios e limiares; o conteúdo das colunas manuais, que continua sem conferência de domínio.

## 2026-11-22 — STRs geradas do quadro, conteúdo do quadro e plural por base (change `strings-geradas-do-quadro`)

Emenda de **escopo** e de **busca**, com a revisão de 2026-11-22 das questões, das facetas e do controle terminológico.

- **Ajustes do pesquisador anteriores à change**, lidos no diff do protocolo e do plano (redação confirmada pelo pesquisador em 2026-11-22): QER1 e OE1 passam a "propostos, especificados, aplicados ou avaliados"; OE4 passa a "Examinar limitações, lacunas, incompatibilidades e insuficiências de integração entre práticas educacionais e fatores situacionais identificadas nos artefatos", como a QER4; o objetivo geral passa a "e os fatores situacionais associados à sua aplicação", em vez de "e/ou … que condicionam"; o CE6 passa a "associados à sua aplicação"; o núcleo de FCT3 perde `prática`, `practice` e `práctica`. Alcance: **escopo** (OE4, objetivo geral, QER1, OE1) e **busca** (FCT3).
- **"e" × "e/ou" em dois níveis.** A QGR e o objetivo geral, com "e", tratam do recorte da revisão; o CE6 e a EB4, com "e/ou", tratam da inclusão de cada estudo. A frase foi acrescentada ao parágrafo de adaptação do PICo. O CE6 não muda.
- **STR gerada do quadro.** Cada STR passa a ser a união dos termos do quadro da faceta (três camadas, pt/en/es) menos os subsumidos por outro termo da mesma STR, por sequência contígua de palavras com a mesma grafia, acento e hífen inclusive. A tabela de STRs é gravada por `strings gerar --gravar`; `conferir` reprova a STR diferente da gerada e o termo do quadro em mais de uma faceta (atribuição única), e a gravação é recusada nesse caso.
- **B3 — artefatos conceituais em FCT1, no campo tópico.** `modelo conceitual`, `modelagem conceitual`, `esquema conceitual`, `modelo semântico` e `taxonomia`, com os equivalentes en/es, passam à STR1. Reverte parte da emenda v2. Risco aceito: volta o ruído que a emenda v2 retirou (taxonomia de Bloom, por exemplo). `taxonomia`/`taxonomy` subsumem as formas facetadas, que saem da STR.
- **C1 — atribuição única entre FCT2 e FCT4.** `nível de ensino`, `modalidade de ensino`, `instituição de ensino`, `ambiente de aprendizagem` e `infraestrutura educacional`, com os equivalentes en/es (inclusive `learning infrastructure`), saem de FCT4 e ficam em FCT2. `instituição educacional`, variante pt de `instituição de ensino` que estava só em FCT4, foi tratada como parte do mesmo conceito e também passou a FCT2 (interpretação do agente, a confirmar). Amplia a âncora de domínio e reverte parte da emenda v2; o efeito se mede na sonda EB5 − EB4. Retirada a duplicata de `ensino superior` em FCT2 pt (fica a do núcleo).
- **Retiradas do quadro.** `população-alvo`, `recurso disponível` e os equivalentes (`target population`, `available resource`, `población destinataria`, `recurso disponible`) saem do quadro e de STR4 e passam a ser variáveis de extração do G4 (`docs/parametros_complementares.md`). Saem também as formas que estavam no quadro e fora das strings, recalculadas antes da edição e iguais às do design: FCT1 `ontológico`, `ontológica`, `análise facetada`, `análise de facetas`, `representação formal`, `ontological`, `facet analysis`, `formal representation`, `análisis facetado`, `análisis de facetas`, `representación formal`; FCT2 `educativo`, `estudiante`, `alumno`, `docente`; FCT4 `contexto de aplicação`, `contexto de uso`, `application context`, `context of use`, `contexto de aplicación`.
- **Formas acrescentadas por simetria entre idiomas (C2, C4), sem tabela prévia de aprovação, por decisão do pesquisador.** Expansão terminológica assistida por IA (Claude Opus 5.5), para revisão do pesquisador pelo diff e transcrição ao LOG_IA:
  - FCT1, próximos: `taxonomy` (en), `taxonomía facetada` (es), `taxonomía` (es);
  - FCT2, núcleo: `ensino e aprendizagem`, `trilha de aprendizagem`, `aprendizagem do estudante`, `ensino híbrido`, `aprendizagem online`, `aprendizagem ao longo da vida`, `sistema de gestão da aprendizagem` (pt); `enseñanza y aprendizaje`, `itinerario de aprendizaje`, `aprendizaje del estudiante`, `aprendizaje combinado`, `aprendizaje en línea`, `aprendizaje a lo largo de la vida`, `sistema de gestión del aprendizaje` (es);
  - FCT2, relacionados: `objeto de aprendizagem`, `aprendiz` (pt); `learning object`, `learner` (en);
  - FCT4, núcleo: `situação de uso` (pt), que subsume `situação de uso educacional`;
  - FCT4, relacionados: `sensível ao contexto` (pt).
- **Fontes dos instrumentos.** ERIC Thesaurus e UNESCO Thesaurus em itens distintos em `docs/02`, a ERIC primeiro. Endereços do ERIC Thesaurus e do Brased indicados pelo pesquisador e não verificados pelo agente, gravados na coluna `Caminho` da tabela de instrumentos de `docs/03`.
- **Plural declarado por base.** A declaração de cobertura de cada ficha ganha a linha `plural` (`explícito` | `pela lematização`); `pela lematização` exige a linha "Lematização" da seção 1 verificada por medição, com `(BDn/<id>)`. Nenhuma base tem a lematização medida, e todas declaram `explícito`. A ERIC perdeu a frase "Plural regular omitido onde a lematização o alcança" e ganhou o plural regular dos termos, todos visíveis nas strings da ficha (expansão assistida por IA, a revisar com as demais).
- **Fichas atualizadas a partir das STRs regeradas.** WoS, Scopus e BRAPCI: strings e blocos regerados da STR nos idiomas e camadas declarados, mantidas as flexões que a ficha já trazia. ERIC: `practice` deu lugar aos termos de prática que a STR3 traz; a `STR1b`, no resumo, mantém subsumidos em campo próprio. As consultas de EB2, EB3 e EB4 da ERIC passaram do teto de caracteres da ficha e foram partidas no grupo 🟥 ou 🟧, sem retirar termo; as partes estão registradas na ficha.

Fundamento: decisões do pesquisador de 2026-11-22 (proposta e design da change).

Alcance: **escopo** e **busca**. Nenhuma execução está registrada, de modo que nenhuma contagem fica vencida. O teste de aderência e a sonda EB5 − EB4 medem o efeito na primeira execução.

O autoteste ganhou casos para STR editada à mão, termo em duas facetas com recusa da gravação, gravação que preserva o restante byte a byte, subsumido aceito na ficha, plural sem lastro numa só base, linha `plural` retirada e o domínio `plural` na gramática; cada um falhou com a conferência correspondente desligada.

O que não se alterou e por quê:

- as fichas continuam autorais: não há gerador de fichas, e a garantia sobre o plural vem da conferência;
- a simetria entre idiomas não é conferida por máquina: equivalência de tradução não se decide por contagem;
- WoS, Scopus e BRAPCI declaram `plural: explícito` sem que o plural tenha sido acrescentado aos termos que só estão no singular; o relato os lista, e a decisão fica com o pesquisador;
- a faceta auxiliar local (B5) e a revisão das sementes (B4) ficam fora desta change;
- as entradas anteriores deste histórico registram o estado da data e não se reescrevem.

## 2026-11-22 — Parâmetros da busca por base, estratégia de proximidade e fichas renomeadas (revisão da change `strings-geradas-do-quadro`)

Decisões do pesquisador na revisão da change, em 2026-11-22.

- **Skills da busca sem base nomeada.** O que difere de uma base para outra é parâmetro da ficha, não regra da skill.
  - `expressoes-de-busca`: a tabela de sintaxe por base (ERIC, BRAPCI, Web of Science, Scopus) deu lugar à tabela dos parâmetros e de onde cada um se declara. O teto da ERIC, que a skill dava como medido, saiu: nenhuma execução registrada o sustentava.
  - `facetacao-e-termos-livres`: a armadilha "a BRAPCI não lê as facetas" virou "lista curada não lê as facetas", e o passo do comprimento das consultas da ERIC virou o passo do teto declarado.
  - A fração de registros sem termo das facetas temáticas, que a skill citava, não tem execução registrada no repositório. Em `expressoes-de-busca`, ficou como medida a refazer na primeira execução.
- **Teto de caracteres como parâmetro da base.** A declaração de cobertura ganha a linha obrigatória `teto de caracteres`, com um número inteiro ou `nenhum`.
  - Com número, `conferir` mede cada consulta executável e reprova a base em que alguma passe do teto. Com `nenhum`, relata a maior consulta.
  - Valores declarados: ERIC 1400, regra de bolso não medida, com a origem na seção 1; WoS, Scopus e BRAPCI `nenhum`, porque o comprimento máximo não está verificado.
  - A lista de comprimentos transcrita na prosa da ficha da ERIC saiu. O leitor calcula os comprimentos, e eles eram iguais à lista, consulta por consulta.
- **Plural × lematização.** O parâmetro `plural` (`explícito` | `pela lematização`) já existia na declaração. As skills passam a dizer como ele governa a composição.
- **Estratégia de proximidade.** A ficha pode ter a subseção `### Estratégia de proximidade` na seção 4. É discussão, e o leitor a ignora. A skill `ficha-de-busca-por-base` diz o que ela discute.
- **Fichas renomeadas.** `docs/busca_base_<sigla>.md` passou a `docs/procedimentos_busca_<sigla>.md`, com `git mv`. Mudaram o padrão `[documentos] ficha` e as referências na configuração, no README, nas skills, no autoteste e em `data/pendencias.json`.

Alcance: **de redação** e de conferência. Nenhuma expressão nem string mudou: o teto da ERIC é o mesmo que já governava a partição.

O que não se alterou e por quê:

- **Decisão do pesquisador ainda em aberto.** WoS, Scopus e BRAPCI continuam com `plural: explícito` e termos só no singular. Falta decidir entre acrescentar os plurais e medir a lematização.
- **Proximidade.** Nenhuma ficha ganhou a subseção de estratégia de proximidade. O conteúdo é discussão metodológica por base, e fica a pedido.
- **Outras skills.** Ainda citam base `busca-nas-bases`, `deduplicacao`, `conferencias-da-busca`, `filtragens`, `parecer-sobre-protocolo`, `conjunto-semente`, `conferir-referencia` e `validacao-vocabulario-controlado`. Estão fora das skills de geração da busca e ficam para decisão do pesquisador.
- **Gerador de fichas.** Não há script no repositório que componha as fichas. Elas são escritas com roteiro descartável sobre o leitor, e um gerador seria outra change.
- **Registros antigos.** As entradas anteriores deste histórico e as changes arquivadas mantêm o nome antigo das fichas.

Cada caso novo do autoteste — teto abaixo da maior consulta, linha de teto ausente, valor de teto deformado, estratégia de proximidade com bloco — falhou com a conferência correspondente desligada na memória.

## 2026-11-23 — Histórico sem contagens, endereço único dos instrumentos e geração das fichas (decisão do ReT)

Decisões do pesquisador na verificação da change `strings-geradas-do-quadro`.

- **Histórico sem contagens.** As entradas traziam totais de termos, de sementes e de caracteres e o resultado das conferências e do autoteste. Esses números se transcreviam e passavam a contradizer os artefatos na alteração seguinte. A verificação achou o caso: a entrada anterior a esta citava um resultado do autoteste que já não era o corrente. O histórico passa a guardar só a decisão: o que mudou, por nome, e o valor de parâmetro decidido. A contagem se calcula do artefato; o resultado das conferências vai ao relato da change ou da tarefa. As contagens das entradas anteriores foram retiradas, por exceção expressa à regra de não reescrever entradas antigas. A regra está no README (Três registros), no AGENTS §7 e na skill `registrar-decisao`. As tarefas que mandavam citar contagem no histórico foram ajustadas: as da change `strings-geradas-do-quadro` e a de `catalogo-de-apoio`. Alcance: **instrumento** (forma do registro).
- **Endereço dos instrumentos num lugar só.** O endereço de cada instrumento de controle terminológico estava nas referências de `docs/02` e na coluna `Caminho` da tabela de instrumentos de `docs/03`, com divergências de grafia (Brased e UNESCO). Passa a existir só na coluna `Caminho`, que o leitor exige e confere. As referências de `docs/02` (TBCI, Brased, ERIC Thesaurus, UNESCO Thesaurus) remetem à linha da tabela. A entrada de 2026-11-22 e os artefatos da change deixaram de repetir o endereço. Alcance: **redação**.
- **Skill de otimização das strings sem base nomeada.** A seção de fatos de sintaxe por base deu lugar às dimensões a verificar em cada base. Os fatos que só a skill trazia, sem fonte citada, foram para a seção 1 da ficha de cada base, como **Não verificado**: aspas, sinônimos e limite da busca em todos os campos (WoS); locução aproximada com plurais (Scopus); derivação desativada, mínimo de letras antes do curinga e API (ERIC). Alcance: **instrumento**.
- **STR com termo em duplicidade reprova.** A leitura deduplicava a STR antes da comparação com a gerada, e o termo repetido passava em `conferir` sem reprovar. A verificação o tinha descrito como mensagem enganosa, e isso foi retificado. Passa a reprovar em `conferir` e em `strings gerar`, com a mesma mensagem, e `--gravar` a desfaz. Alcance: **instrumento**.
- **Geração das fichas, proposta.** Abre-se a change `geracao-das-fichas-de-busca`:
  - ficha mista, com as seções 3 e 4 geradas a partir da STR e de parâmetros de composição declarados na ficha;
  - plural explícito gerado por regra de pt, en e es, com exceções declaradas pelo pesquisador;
  - recusa da flexão que a regra não decide;
  - `plural` por idioma.
  A PD26 passa a apontar para ela. A coordenação com `namespace-de-comandos-e-skills` (nome do comando e decisão C1/C2 da ficha) está registrada em ambas. Alcance, quando aplicada: **busca**.

O que não se alterou e por quê:

- **ABNT.** As referências de `docs/02` dos instrumentos deixam de ter o "Disponível em" que a ABNT NBR 6023 pede para documento online. A consequência foi apontada ao pesquisador antes de ele mandar seguir, sem objeção registrada.
- **Fichas.** As strings das fichas não mudam por estas decisões. O plural de WoS, Scopus e BRAPCI continua pendente (PD26) até a aplicação da change nova.
- **Lastro dos fatos de sintaxe.** Os fatos levados às fichas não foram conferidos na documentação oficial. Ficam como **Não verificado** até a conferência ou a primeira execução.

## 2026-11-23 — "Ficha" passa a "procedimento de busca" (decisão C1 do ReT)

Decisão do pesquisador sobre a questão C1/C2 da change `namespace-de-comandos-e-skills`.

- **O que estava.** O artefato de cada base se chamava "ficha" no conceito, na skill `ficha-de-busca-por-base` e na chave `[documentos] ficha`. Os arquivos já se chamavam `docs/procedimentos_busca_<sigla>.md`. A change de namespace deixava em aberto manter "ficha" (C2) ou passar a "procedimento de busca" (C1).
- **O que passa a valer.** C1: o conceito passa a ser "procedimento de busca". A change `namespace-de-comandos-e-skills` renomeia a skill para `procedimento-de-busca-por-base`, a chave para `[documentos] procedimento`, com a antiga aceita por uma rodada, e o texto do guia, do README e do código. O comando da change `geracao-das-fichas-de-busca` nasce como `procedimentos gerar`, sem alias. As tarefas do ramo C2 saíram da change de namespace. Alcance: **redação** (nomes); nenhuma string, critério ou parâmetro muda.

O que não se alterou e por quê:

- **Nada foi renomeado ainda.** A skill, a chave e o texto continuam com "ficha" até a aplicação da change de namespace. A change `geracao-das-fichas-de-busca` também conserva, por ora, o seu nome e o da capacidade `geracao-das-fichas`: o nome de change e de capacidade é rótulo de planejamento, e renomeá-los antes da aplicação não muda o que se entrega.
- **Entradas anteriores do histórico** continuam dizendo "ficha"; o histórico não se reescreve por mudança de nome.

## 2026-11-23 — Catálogo de apoio, passo de adaptação e marcadores de apoio (change `catalogo-de-apoio`)

Aplicação da change `catalogo-de-apoio`, proposta e aprovada pelo pesquisador.

- **O que estava.** O guia de procedimentos (`docs/procedimentos.md`) era a única fonte do mapeamento passo → fonte, skill e script, mas nada o lia. A contagem declarada no topo era a do modelo, e o guia listava também o passo de geração das STRs, sem marca. Os passos sem skill nem script não diziam se a ausência era decisão ou lacuna. Skill órfã, comando citado inexistente e contagem divergente não reprovavam.
- **Passo de adaptação.** O guia passa a declarar os passos do modelo, mais um passo de adaptação do projeto — a geração das STRs —, e o total. O passo leva a marca `(adaptação do projeto)`. O plano (§1.4) ganha uma nota que remete ao guia, e a descrição do modelo não muda. Alcance: **instrumento** (forma do guia).
- **Marcadores de apoio.** O passo sem skill nem script declara `Apoio: manual — <razão>` ou `Apoio: lacuna — <razão>`. `lacuna` só vale para as duas lacunas reconhecidas: `avaliacao-da-necessidade` (pesquisas preliminares, revisões anteriores, biblioteca especializada e obras de referência, em M1/E1, M1/E2 e M2/E1) e `busca-complementar` (acervos especiais e pessoais, em M3/E3). Os demais passos sem apoio são `manual`. Alcance: **instrumento**.
- **Citações acrescentadas.** `questao-e-objetivos` nos passos de M2/E2, `relato-prisma` na tabela de composição do portfólio e na normalização do relatório, `busca-nas-bases` na exportação de metadados e nos alertas. Alcance: **redação**.
- **Papel das skills.** O guia declara o papel de cada skill (procedimento, instrumento, artefato ou transversal) na seção "Papel das skills". As transversais são `registrar-decisao`, `rastreabilidade`, `revisao-geral-do-projeto`, `conferir-referencia` e `relato-prisma`. `fichamento` é a de instrumento; `conjunto-semente` e `ficha-de-busca-por-base`, as de artefato. Alcance: **redação**.
- **Catálogo gerado.** `python3 -m rsl catalogo gerar` lê o guia, as skills e o parser, imprime o catálogo e confere: a contagem de passos, a cobertura de apoio, as skills citadas e órfãs, os comandos e as opções citados, os comandos não citados, as citações de nome antigo em documento vivo e o catálogo defasado. `--gravar` grava `docs/catalogo_de_apoio.md` de forma atômica. O catálogo é saída de geração e não se edita à mão. O guia ganha a seção "Catálogo de apoio" e a linha de `catalogo gerar` nas conferências transversais; o README, o caminho no mapa e a ordem guia → `catalogo gerar` → `--gravar`. Alcance: **instrumento**.

O que não se alterou e por quê:

- **Nenhuma skill criada.** `avaliacao-da-necessidade` e `busca-complementar` ficam como lacuna declarada até decisão do pesquisador. Criá-las agora seria decisão metodológica tomada pelo agente.
- **Nenhum comando ou skill renomeado.** As renomeações são da change `namespace-de-comandos-e-skills`, que usa o catálogo como guarda. A varredura de nomes antigos fica inativa enquanto não houver alias declarado.
- **Protocolo, procedimentos de busca, conjunto-semente, strings, expressões, critérios, bases e `config.toml`** não mudam.
- **A classificação manual/lacuna e o papel de cada skill** foram propostos pelo agente na aplicação, pela leitura do design. Revê-los é alteração do guia, seguida de `catalogo gerar --gravar`.
