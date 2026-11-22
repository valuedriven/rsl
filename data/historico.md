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

## 2026-11-19 — Scripts reunidos no pacote `src/rsl` (decisão de instrumento)

Os quatro scripts (`src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e `src/gen_semente.py`) deram lugar ao pacote `src/rsl/`, com um ponto de entrada único, `python3 -m rsl <subcomando>`, a partir da raiz e com `src/` no caminho de importação (`PYTHONPATH=src`). Change `refatoracao-dos-scripts`.

- **Comandos.** As opções viraram subcomandos por atividade: `conferir`, `conferir-dados`, `autoteste` (agora um só, com a prova da composição e a aderência por papel), `mostrar`, `pendencias`, `gramatica`; `sementes sincronizar|planilha`; `termos sonda|exportar|validar|importar`; `busca registrar|derivar|aderencia|fidelidade|sensibilidade`. A correspondência com os nomes antigos está na spec `interface-de-comando`. README, skills, fichas e plano citam os subcomandos.
- **Códigos de saída.** Passam a distinguir a reprovação do conteúdo da falha em ler: 0 OK, 1 REPROVADO, 2 USO, 3 CONFIGURACAO, 4 PROTOCOLO_ILEGIVEL, 5 DADOS, 6 PARCIAL, 7 FONTE_EXTERNA. Antes, conferência reprovada, protocolo ilegível, configuração inválida e arquivo ausente saíam todos com 1, e o autoteste parcial saía com 0.
- **Nomes de arquivo.** A planilha de validação passa a `data/validacao_terminologica.csv` (a grafia anterior, "termológica", remete a calor); a saída de fidelidade, a `fidelidade_eb<n>.csv`. Todos os caminhos de entrada e de saída vêm do `config.toml` (`[dados]`, `[saidas]`).
- **Gramática do protocolo.** A forma que o leitor exige do protocolo e das fichas está declarada num só lugar do código e é exibida por `python3 -m rsl gramatica`. O leitor ficou mais estrito em dois pontos: o cabeçalho de seção tem de estar no nível declarado, e a linha de cada camada do quadro terminológico (núcleo, próximos, relacionados) passa a ser exigida, com PROTOCOLO_ILEGIVEL. Antes, a linha ausente era lida como camada vazia e reprovada como incoerência.
- **Fonte externa.** A validação terminológica deixou de repetir a requisição depois de erro de rede e de seguir para o termo seguinte depois de falha. Agora interrompe na hora, sem nova tentativa, conforme o AGENTS.md §9.

Fundamento: a exploração de 2026-11-19 verificou códigos de saída ambíguos, conteúdo fixado no código (caminhos, nomes de saída, literais do protocolo vigente nas mutações do autoteste), duas normalizações Unicode diferentes, código morto e a nova tentativa automática em `validar_termos.py` (proposta da change).

Alcance: **instrumento, não método**. Composição, critérios, limiares, strings e recorte não mudam. Antes da migração, gravou-se uma referência com o código antigo sobre exportações e um registro de execução sintéticos. Com o código novo, `mostrar` e `conferir` saíram idênticos byte a byte, e `registros.csv`, `contagens_busca.csv`, `ordem_triagem.csv`, a fidelidade e as duas sensibilidades também, com o nome novo. A comparação das duas normalizações (NFKD e NFD) sobre os termos do protocolo e das fichas e sobre os textos sintéticos não achou diferença, e ficou a NFKD. Valores que estavam fixos no código passaram ao `config.toml` sem mudança de valor: ano de recência da ordem de triagem (`busca.ano_recencia = 2022`), tamanho-alvo da amostra da sonda (`busca.amostra_sensibilidade = 50`) e dimensão do recorte (`conferencia.dimensao_recorte`). Nenhuma execução está registrada (PD02): nenhuma contagem fica vencida.

Mudanças de comportamento fora da forma, registradas para conferência:

- `termos validar --faceta n` passou a filtrar a faceta. Antes, comparava `FCTn` com `n` e não consultava nenhum termo.
- O cliente da UNESCO colhe os rótulos de TG, TE e TR nos idiomas que o protocolo declara para o instrumento (hoje `en, es`), e não mais em `en, es, fr`, que estavam fixos no código.
- A sonda dos clientes usa termos do próprio protocolo, e não termos fixos.
- O campo `forma` das execuções registradas passa a dizer `registrada por busca registrar`.

## 2026-11-20 — Emenda de forma do protocolo e leitor ajustado (change `reestruturacao-do-protocolo`)

O pesquisador reestruturou o protocolo depois de bf6b9bf, e o leitor deixou de lê-lo (`rsl conferir` saía com 4, PROTOCOLO_ILEGIVEL). A change `reestruturacao-do-protocolo` ajustou a gramática e o leitor ao documento escrito, sem pedir mudança de forma ao protocolo. Mudanças de forma, todas feitas pelo pesquisador e agora aceitas pelo leitor:

- **Facetas em tabela.** A lista "Palavras significativas da questão de revisão" deu lugar à tabela "Facetas da questão de revisão" (`Id faceta | Faceta | Âncora obrigatória`, com `Sim`/`Não`). As âncoras são lidas da coluna, sem padrão no `config.toml` (`padroes.ancoras` saiu); tabela sem âncora reprova.
- **Nova tabela de expressões, com notas.** A tabela passou a `ID | Expressão de busca | Função protocolar`, sem as colunas Natureza e Detalhamento, e ganhou a subseção "Notas explicativas" (N1–N4). A executada e a sonda passaram a ser identificadas pela composição (a executada é a única com grupo OR; a sonda, a única formada só pelas âncoras), por decisão do pesquisador de 2026-11-20; saíram `[expressoes]`, `padroes.executada` e `padroes.sonda`. A faixa de sensibilidade (5% a 15%) é lida da nota citada pela executada (N3). O parágrafo de operadores de proximidade saiu do protocolo; a proximidade continua nas fichas.
- **Conjunto-semente em arquivo próprio.** A tabela de sementes saiu do protocolo para `docs/conjunto_semente.toml` (`[[sementes]]` com `id`, `semente`, `bases`, `papel`), localizado por `[documentos] sementes` do `config.toml`; o protocolo não cita o caminho, por decisão do pesquisador de 2026-11-20. A seção "Conjunto-semente" do protocolo mantém a regra de ajuste e a fórmula. O formato é intermediário: a decomposição do campo `semente` fica com a change `sementes-estruturadas-no-protocolo`. As 10 sementes lidas do arquivo dão autoria, ano, título, DOI, bases e papel idênticos aos lidos da tabela de bf6b9bf, e a mesma distribuição (wos 4, scopus 6, eric 3, brapci 2; desenvolvimento 1, validação 9).
- **"Ferramenta de gestão bibliográfica" substituída** pelas tabelas "Procedimentos", "Instrumentos" e "Ferramentas", que o leitor não interpreta.
- **Critérios renumerados de CE1 a CE9.** CE6 é a regra única de inclusão por adequação temática; os critérios de exclusão temática nomeados (antigos CE8 a CE12) e o de localização de itens (antigo CE6) não estão mais na tabela. O fundamento dessa mudança de conteúdo não foi registrado nesta change.
- **P5 corrigido.** Citava "CE7, regras de exceção e borda e CE8–CE15"; passou a "CE6 (adequação temática) e CE7–CE9".
- **Marcador da estrutura da questão** reescrito como "A estrutura da questão…".

Divergências que o levantamento da change não previa, encontradas quando a leitura voltou a passar, e decididas pelo pesquisador em 2026-11-20:

- **Separador do quadro terminológico.** O quadro passou a separar os termos por vírgula, e não mais por `\- `. Sem ajuste, o leitor lia cada célula como um termo só, sem reprovar. A gramática passou a declarar a vírgula como separador, e o separador antigo reprova. Nenhum termo do quadro de 73cf68a tinha vírgula interna.
- **Dimensão "Localização de itens"** retirada de `conferencia.dimensoes_criterio`, acompanhando a tabela de critérios.
- **STR2 alinhada ao quadro de FCT2.** O pesquisador retirou 23 termos do quadro de FCT2. Dez continuam no quadro de FCT3 ou FCT4 (`método de ensino`, `estratégia de ensino`, `teaching practice`, `teaching method`, `teaching strategy`, `learning design`, `método de enseñanza`, `estrategia de enseñanza`, `situação de aprendizagem`, `situación de aprendizaje` — parte do D1 da change `revisao-das-strings-por-faceta`), e treze não estão em faceta nenhuma (`processo de ensino-aprendizagem`, `objeto de aprendizagem`, `trilha de aprendizagem`, `resultado de aprendizagem`, `classroom teaching`, `teaching-learning`, `learning process`, `learning object`, `learning analytics`, `learning outcome`, `teaching-learning process`, `proceso de enseñanza-aprendizaje`, `resultado de aprendizaje`). Os 23 saíram de STR2 (87 → 64 termos) e das strings de FCT2 das fichas (wos e scopus 22 cada, brapci 7; a ERIC não usa esses termos).
- **Critérios nas fichas** renumerados pelo mapa aprovado: CE1–CE5 iguais; a linha de texto completo (antigo CE6) saiu; antigo CE7 → CE6; não pertinência (CE8) e contra-escopo (CE9–CE12) fundidos numa linha, CE6; CE13/CE14 → CE7/CE8; CE15 → CE9.

Alcance: **forma** para os itens da emenda do pesquisador; **busca** para STR2 e as strings de FCT2 das fichas, que perderam termos e mudam o que EB4 e a sonda EB5 recuperam; **elegibilidade** para a renumeração dos critérios. Nenhuma execução está registrada (`data/registro_execucao.json` ausente), de modo que nenhuma contagem fica vencida; o teste de aderência ainda não foi feito com as strings novas. Depois da change, `rsl conferir` sai com 0, `rsl autoteste` executa 202 casos sem falha (PARCIAL, 10 casos dependentes do registro de execução não executados) e `rsl conferir-dados` sai com 5, pelo registro de execução ausente.

Pendência de método, levada ao pesquisador: N3 diz que a fração elegível de 5% a 15% em EB5 − EB4 "é inconclusiva e requer análise qualitativa"; `rsl busca sensibilidade` relata essa faixa como "decisão de mérito do pesquisador, a registrar como emenda". O código não foi alterado.

## 2026-11-20 — Decisões sobre as pendências da change `reestruturacao-do-protocolo` (decisão do ReT)

- **Faixa inconclusiva da sonda.** Vale a regra de N3: uma fração elegível de EB5 − EB4 abaixo do limite inferior favorece a manutenção da executada; acima do superior exige reconsideração e, se necessário, emenda; entre os dois é inconclusiva e requer análise qualitativa. `rsl busca sensibilidade` passou a relatar as três faixas nesses termos; antes chamava a faixa intermediária de "decisão de mérito".
- **Texto completo não restringe a busca.** A linha "texto completo" saiu das quatro fichas, e a variante de contingência `AND OPENACCESS(1)` saiu da ficha da Scopus, com a ressalva que a acompanhava. A falta de texto completo é tratada na triagem (P4), e não na busca.
- **Skill `criterios-de-elegibilidade` genérica.** A skill deixou de citar critérios e regras deste protocolo (CE7, CE12, regra de borda e de exceção vigentes) e remete ao README e ao protocolo. Fica a pergunta de método que ela ensina: que critério passa a excluir o que um critério retirado alcançava.
- **Efeito das strings novas.** O efeito da retirada dos 23 termos de STR2 sobre EB4 e EB5 será avaliado na busca (teste de aderência e sonda de sensibilidade), e não antes.

Alcance: **instrumento** (relato da sensibilidade e skill) e **busca** (sem restrição por acesso aberto na Scopus). Limiares, strings e critérios não mudam por estas decisões.

## 2026-11-20 — Conjunto-semente estruturado campo a campo (change `sementes-estruturadas-no-protocolo`)

O arquivo de sementes (`[documentos] sementes` do `config.toml`) passou do esquema intermediário (`id`, `semente` em texto livre, `bases`, `papel`) ao esquema estruturado, e é agora o único lugar de dado de semente. Decisões do pesquisador de 2026-11-19 e 2026-11-20, registradas na proposta da change.

- **Campos estruturados.** Os dados bibliográficos são campos (`autores` em lista, `ano` inteiro, `titulo`, `veiculo`, `volume`, `numero`, `paginas`, `doi`), e não se extraem mais da referência por padrão de texto: `_titulo()` e `_doi()` saíram do leitor. Entraram `facetas` (FCTn informadas pelo pesquisador) e `observacoes` (o que a referência traz e não cabe em outro campo, transcrito como está: SE4 "SciTePress"; SE5 "(UEL)"; SE6 "(Springer)"; SE10 os editores, "Aalborg, Dinamarca" e "Ergon Verlag"). `bases` passa a significar indexação, e não recuperação. A transcrição foi feita campo a campo, sem os leitores de padrão e sem completar dado de memória. A reconstituição a partir do campo `semente` não deixou sobra em nenhuma das 10 sementes. O texto de `semente` diferia da célula da tabela de bf6b9bf só pelo escape `\.` em SE2, SE3, SE7 e SE8, e a diferença foi apresentada ao pesquisador antes da gravação.
- **Fusão dos dados de conferência, com o mesmo conteúdo.** `verificacao`, `tipo`, `alinhamento`, `nota`, `veiculo_conferido` e `eric` passaram de `data/sementes.json` ao arquivo de sementes, casados por DOI. A conferência campo a campo deu 0 diferença nas 10 sementes. `data/sementes.json` foi removido, e com ele `sementes sincronizar`, a ligação por DOI ou título, o aviso de entrada órfã e as chaves `[dados] sementes` e `[planilha] campos_autorais` do `config.toml`.
- **`escopo` retirado.** Estava vazio nas 10 sementes, o que foi verificado antes da retirada. A planilha de aderência perdeu a coluna. Campo `escopo` no arquivo reprova como campo desconhecido.
- **Sequência de `id` mantida, com renumeração na retirada.** O `id` continua em sequência a partir de SE1, sem lacuna. Retirar uma semente renumera as seguintes. A retirada renomeia a evidência bruta, atualiza `data/pendencias.json` e registra neste histórico a correspondência entre `id` antigo e novo (skill `conjunto-semente`, §4). Evidência `SEn_…` de `id` que não está no arquivo reprova `conferir-dados`. A conferência percorre só a subpasta `referencias/` de `[dados] evidencia` (decisão do pesquisador de 2026-11-20).
- **DOI ausente é pendência, não reprovação.** `pendencias` relata o DOI ausente, as facetas vazias, a semente de validação sem faceta âncora e `tipo` ou `alinhamento` vazios. Nenhuma semente atual está sem DOI. As 10 aparecem com facetas a informar (PD20). A regra para semente de validação sem âncora fica em branco por decisão do pesquisador (PD21). Com `facetas` vazia, só se relata "facetas a informar", e a falta de âncora não é relatada à parte (decisão do pesquisador de 2026-11-20).

Fundamento: o leitor de padrão lia sem reprovar, e errado, referência com ponto no título, com subtítulo ou com DOI fora do fim. Os metadados de conferência viviam noutro arquivo, ligados por um elo frágil (proposta da change).

Alcance: **instrumento**. Composição, critérios, limiares, strings, recorte e o próprio conjunto de sementes não mudam. Conferências sobre o estado depois da change:

- a distribuição exibida por `mostrar` é idêntica à de antes: 10 sementes, 15 incidências; wos 4, scopus 6, eric 3, brapci 2; desenvolvimento 1, validação 9;
- `semente_aderencia.csv` tem as mesmas 40 linhas, menos a coluna `escopo`. A coluna `titulo` difere nas 40 linhas só pelo ponto final, que `_titulo()` incluía e o campo `titulo` não traz;
- o ensaio seco é idêntico.

`rsl conferir` sai com 0. `rsl autoteste` executa 224 casos sem falha (PARCIAL, 7 casos dependentes do registro de execução não executados; eram 10, e os 3 de `sementes.json` saíram com o arquivo). `rsl conferir-dados` sai com 5, pelo registro de execução ausente (PD02).

O que não se alterou e por quê:

- as entradas anteriores deste histórico citam o caminho e o esquema vigentes na data, e não se reescrevem;
- a mudança de forma do protocolo já foi registrada pela entrada de `reestruturacao-do-protocolo`;
- `conferir-dados` não confere se a evidência de um `id` existente é mesmo daquela semente. Depois de uma renumeração, arquivo não renomeado passa em silêncio. Comparar o DOI da evidência com o `doi` da semente fica em aberto, para decisão do pesquisador (design da change, Open Questions).

## 2026-11-22 — Fator de impacto como critério não aplicável e retirada do ASReview (decisão do ReT)

- **CE10 — Fator de impacto, ação "Não aplicável".** O critério que o RS Banyan prevê em M3/E1 entra na tabela de critérios do protocolo só para documentação: não é aplicado na seleção. As quatro fichas ganharam a linha CE10 na seção 2, como `conferir` exige. A gramática do protocolo passou a admitir "Não aplicável" no domínio de 'Ação' (`src/rsl/gramatica.py`); `mostrar` conta os critérios por ação. Alcance: **critérios** (documental) e **instrumento** (gramática). Resolve PD24.
- **ASReview fora do escopo, com a calibração da triagem assistida.** A priorização da fila por aprendizado ativo saiu do plano (decisão 5b da §3.3, que deixa de ter subdivisão; §4.1, §6.1, §6.2, §7, §8.1 e §8.2) e, com ela, a calibração que só a ela servia: o parâmetro `padroes.calibracao_triagem` saiu do `config.toml` e do código (`config.py`, `leitura.py`) e, se voltar, reprova a configuração como chave desconhecida; a skill `calibracao-da-triagem` foi apagada; o guia de procedimentos perdeu o índice correspondente. A classificação assistida por LLM na 1ª filtragem (decisão 5) não muda. As pendências PD15 e PD30 foram apagadas por decisão do pesquisador, e a PD11 deixou de citar a calibração. Alcance: **método** (triagem) e **instrumento**.

Fundamento: decisão do pesquisador de 2026-11-22, na tarefa 4.1 da change `guia-de-procedimentos`.

Conferências depois das alterações: `rsl conferir` sai com 0 e relata 10 critérios (5 incluir, 4 excluir, 1 não aplicável); `rsl autoteste`, 224 casos sem falha (PARCIAL, 7 dependentes do registro de execução não executados), como antes; `rsl conferir-dados`, 5 (DADOS, registro de execução ausente), como antes.

O que não se alterou: as entradas anteriores deste histórico que citam o ASReview ou `calibracao_triagem` registram o estado da data e não se reescrevem.
