# RSL-01 — Representação do conhecimento sobre práticas educacionais e seus fatores situacionais

Revisão sistemática de literatura sobre modelos conceituais, ontologias e outros sistemas de
organização do conhecimento que representam formalmente práticas do processo de
ensino-aprendizagem e os fatores situacionais que condicionam a sua aplicação.

Conduzida pelo **RS Banyan**, com o **PRISMA** como diretriz de apresentação.

Este arquivo é a **porta de entrada** e a **memória operacional** do repositório: diz onde
cada assunto está decidido, em que ordem o trabalho corre e o que cada comando executa. Não
repete o conteúdo dos documentos.

## Como o repositório se organiza

| Onde | O que é |
| --- | --- |
| `docs/` | conteúdo da revisão: plano, protocolo e fichas de busca; os arquivos do pesquisador e os que o agente mantém |
| `data/` | o que é alimentado — os JSON, o histórico e as exportações — e o que os scripts gravam nele: as planilhas e CSVs na raiz, a evidência em `evidencia/` e as cópias em `arquivo/` |
| `src/rsl/` | pacote de execução: ponto de entrada único `python3 -m rsl <subcomando>` |
| `config.toml` | configuração dos scripts: caminho do protocolo, valores padrão dos parâmetros não estruturais, padrão de caminho das fichas e arquivos de dados |
| `.agents/skills/` | competências metodológicas e operacionais do agente |
| `AGENTS.md` | contrato de trabalho do agente: como ele se comporta, não o que o projeto decide |

Este pacote reúne o **plano**, o **protocolo**, as **fichas de busca** e o **histórico**,
em `data/historico.md`. Os demais instrumentos e o portfólio não integram este repositório.

## Mapa

| Caminho | O que contém | Consultar quando |
| --- | --- | --- |
| `docs/01_plano.md` | Plano: contexto, objetivos, método, escopo, cronograma, recursos, custos, qualidade, riscos e uso de IA | entender o desenho e os limites da revisão |
| `docs/02_protocolo_informacoes_gerais.md` | Protocolo, informações gerais: título, vínculo institucional, projeto, tópicos preliminares, objeto e recorte | conferir o que a revisão examina e o que fica fora |
| `docs/03_protocolo_estrategia_pesquisa.md` | Protocolo, estratégias de pesquisa: questão de revisão (QGR, QERn), facetas e âncoras, instrumentos de controle terminológico, vocabulário, strings, expressões e notas explicativas, critérios de elegibilidade, fontes, regra de ajuste do conjunto-semente, procedimentos, instrumentos e ferramentas. Fonte única desses dados e dos parâmetros que declara | montar ou conferir a busca |
| arquivo de sementes (`[documentos] sementes` do `config.toml`) | Conjunto-semente: uma tabela `[[sementes]]` por estudo, campo a campo — dados bibliográficos (`id`, `autores`, `ano`, `titulo`, `veiculo`, `volume`, `numero`, `paginas`, `doi`), aferição (`bases`, `facetas`, `papel`), conferência (`verificacao`, `tipo`, `alinhamento`, `nota`, `veiculo_conferido`, `eric`) e `observacoes`. Único lugar de dado de semente | compor ou conferir o conjunto-semente |
| `docs/busca_base_wos.md` | ficha da Web of Science: sintaxe, strings por faceta, expressões, variantes, conjunto-semente e ressalvas | executar ou auditar esta base |
| `docs/busca_base_scopus.md` | ficha da Scopus, mesma estrutura | idem |
| `docs/busca_base_eric.md` | ficha da ERIC, mesma estrutura | idem |
| `docs/busca_base_brapci.md` | ficha da BRAPCI, mesma estrutura | idem |
| `src/rsl/` (`conferir`, `conferir-dados`, `autoteste`, `mostrar`, `pendencias`, `gramatica`) | leitura e conferência do protocolo e das fichas, conferência dos arquivos alimentados, autoteste único, resumo dos parâmetros em uso e contrato de forma do protocolo | antes de executar qualquer subcomando, e após alterar o protocolo ou uma ficha |
| `src/rsl/` (`busca …`) | registro das execuções no `registro_execucao.json`, derivação local das expressões, aderência, fidelidade e sonda de sensibilidade | registrar execução, calcular a pertinência de cada registro, testar a busca |
| `src/rsl/` (`termos …`) | validação terminológica nos instrumentos que o protocolo declara por faceta: consulta automatizada onde há cliente (módulo de mesma sigla em `src/rsl/termos/clientes/`) e linha pendente de validação manual nos demais, com a planilha como registro | conferir o estatuto de cada termo |
| `src/rsl/` (`sementes …`) | planilha de aderência a partir do arquivo de sementes, com o papel e a conferência de cada semente, e o ensaio seco impresso no terminal | montar o instrumento do teste de aderência, uma linha por semente e por base |
| `data/historico.md` | Histórico: decisões relevantes sobre a revisão, inclusive as emendas, com data, alcance e fundamento | saber o que já foi decidido e por quê |
| `data/pendencias.json` | Pendências: ações ainda a executar, cada uma com origem, o que bloqueia, ação sugerida, responsável e estado | saber o que falta fazer |
| `config.toml` | caminho do protocolo e do arquivo de sementes, padrões dos parâmetros não estruturais, padrão de caminho das fichas, arquivos de dados, arquivos de saída e campos das planilhas | mudar o arquivo do protocolo ou das sementes, um padrão, o local das fichas ou de um arquivo |

Em `data/` (caminhos em `[dados]` do `config.toml`), a procedência de cada arquivo:

| Caminho | O que contém | Quem escreve |
| --- | --- | --- |
| `data/registro_execucao.json` | resultados da execução das consultas nas bases: sondagens de sintaxe, estado da interface, retornos, exportações, conferências e aderência, por base; e, em cada execução registrada, o arquivo e a conferência do retorno | pesquisador e `busca registrar` |
| `data/historico.md` | Histórico: decisões relevantes sobre a revisão, com data, alcance e fundamento | pesquisador |
| `data/pendencias.json` | ações ainda a executar, identificadas por `PDnn` | pesquisador e agente, a pedido |
| `data/execucoes/<base>/` | exportações intactas das bases | pesquisador |
| `data/evidencia/` | respostas brutas das consultas: instrumentos de controle terminológico (`<instrumento>/`) e conferência de referências (`referencias/`, arquivos `SEn_…` nomeados pelo `id` da semente) | subcomandos `termos` e agente, a pedido |
| `data/` (raiz) | planilhas e CSVs gravados pelos subcomandos (nomes em `[dados]` e `[saidas]` do `config.toml`): `validacao_terminologica.csv`, `semente_aderencia.csv`, `registros.csv`, `contagens_busca.csv`, `ordem_triagem.csv`, `fidelidade_eb<n>.csv` e `sensibilidade_<base>.csv`; a planilha de validação é o registro do estatuto dos termos | subcomandos e pesquisador (planilha de validação) |
| `data/evidencia/` | resposta bruta de cada consulta terminológica | `termos validar` |
| `data/arquivo/` | cópias anteriores, com `SHA256` | migrações |

As pastas `execucoes/`, `evidencia/` e `arquivo/` são criadas quando o primeiro arquivo chega.

O que é **derivado do documento não vira arquivo**: questão, facetas, instrumentos,
strings, expressões, critérios e fontes são lidos do protocolo a cada execução, e a forma de
cada base, da ficha correspondente. Em `data/` guarda-se o que alguém **alimenta** — o
registro das execuções e a evidência bruta das consultas — e a planilha de validação, registro do
estatuto dos termos, lida e regravada por `termos exportar`, `termos validar` e `termos importar`.

### Três registros, três finalidades

Cada registro guarda um tipo de informação, e nenhum repete o outro:

| Registro | Guarda | Não guarda |
| --- | --- | --- |
| `data/historico.md` | **decisões** relevantes sobre a revisão — emendas, escolhas de método, de escopo e de instrumento —, com data, alcance e fundamento | ação por fazer; resultado de consulta |
| `data/pendencias.json` | **ações ainda a executar**, cada uma com `id`, `origem`, o que bloqueia, ação sugerida, responsável e `estado` (`aberta`, `resolvida` ou `descartada`) | decisão; resultado de consulta |
| `data/registro_execucao.json` | **resultados da execução das consultas** nas bases — sondagens, retornos, exportações e conferências | decisão; ação por fazer |

- Pendência resolvida muda de `estado` e ganha `resolucao`, com o que a fechou; não é
  apagada. Se a resolução envolveu decisão, a
  decisão vai para o histórico, e o resultado de consulta, para o registro de execução.
- A pendência remete à sua `origem` (ficha, protocolo, plano, comando) em vez de copiar o
  conteúdo dela: a ressalva "não verificado" continua na ficha, e a pendência aponta para ela.

### Configuração e parâmetros

`config.toml`, na raiz, é lido pelo pacote `src/rsl/` com `tomllib` (**Python 3.11+**, só
biblioteca padrão), sob demanda: importar um módulo não lê nada; a leitura acontece quando um
subcomando a pede. A variável de ambiente `RSL_CONFIG` aponta outro arquivo, para ensaio e
autoteste. Ele traz:

- `protocolo` — o arquivo do protocolo a ser lido; o protocolo não o sobrescreve;
- `[padroes]` — valor padrão de cada parâmetro não estrutural que o protocolo pode declarar:
  recorte, limiar de aderência (aplicado só às sementes de validação), faixa de
  sensibilidade, limiar de divergência da fidelidade e sensibilidade mínima da calibração
  da triagem assistida;
- os parâmetros que o protocolo não declara: dimensões obrigatórias dos critérios e a do
  recorte temporal, mínimo de termos por string, ano de recência e tamanho-alvo da amostra
  da sonda (`[busca]`), arquivos de dados (`[dados]`), arquivos de saída (`[saidas]`) e
  campos das planilhas;
- `[documentos] ficha` — padrão de caminho da ficha de cada base, com `{sigla}`
  (`docs/busca_base_{sigla}.md`);
- `[documentos] sementes` — o arquivo do conjunto-semente. Os documentos citam o arquivo
  por esta chave, não pelo caminho; ausente, o subcomando para com CONFIGURACAO, nomeando a
  chave e o caminho.

**Parâmetros estruturais** não têm padrão e não constam do `config.toml`: são lidos só do
protocolo, e a ausência ou o valor inválido reprova a leitura, nomeando tabela, linha e
campo. São a composição das expressões, de onde se identificam a executada (a única
expressão com grupo `OR`) e a sonda (a única formada só pelas âncoras) — nenhuma ou mais de
uma candidata reprova; as facetas e as âncoras (tabela `Id faceta | Faceta | Âncora
obrigatória`, com `Sim` ou `Não`); os instrumentos de controle terminológico (tabela
`Sigla | Instrumento | Modo | Caminho | Idiomas | FCTs`, com `Modo` `Manual` ou
`Automático` — este exige cliente de mesma sigla em `src/rsl/termos/clientes/`); as bases
(tabela "Bases de dados": `ID Base`, `Sigla`, `Nome da base`), cuja ficha se localiza pela
sigla; e os idiomas do quadro terminológico, lidos do cabeçalho `| FCTn | pt | en | es |`,
com os termos de cada célula separados por vírgula. O **conjunto-semente** também é
estrutural, mas vem só do arquivo de sementes (`[documentos] sementes`): esquema fechado,
exibido por `python3 -m rsl gramatica`, com `id` (`SEn`, único, em sequência a partir de
SE1, sem lacuna), os dados bibliográficos campo a campo (`autores` em lista, `ano` inteiro,
`doi` na forma `10.x/…`), `bases` (siglas da tabela de bases, na grafia exata), `facetas`
(`FCTn` da tabela de facetas), `papel` (`desenvolvimento` ou `validação`), os campos de
conferência e `observacoes`; campo exigido ausente, campo de outro tipo ou desconhecido
reprova, nomeando a semente e o campo. Nada se extrai da referência por padrão de texto.
DOI ausente, `facetas` vazia, semente de validação sem faceta âncora e `tipo` ou
`alinhamento` vazios não reprovam: `pendencias` os relata. A faixa de sensibilidade é lida das notas
explicativas citadas pela executada (`< N%` e `> M%`).
A forma de execução de cada base (`- Execução: única` ou `particionada`) é declarada na
própria ficha. As chaves antigas (`padroes.composicao`, `padroes.ancoras`,
`padroes.executada`, `padroes.sonda`, `cores`, `fichas`, `instrumentos`, `idiomas`,
`[expressoes]`) reprovam a configuração se voltarem a ela, e chave fora do esquema também.
A forma que o leitor exige do protocolo, das fichas e do arquivo de sementes — seções,
tabelas, colunas, rótulos, marcadores, identificadores, campos e frases de onde se lê um
parâmetro — é o
contrato exibido por `python3 -m rsl gramatica`, a partir da única declaração no código
(`src/rsl/gramatica.py`); não há cópia mantida à mão.

**Precedência (parâmetros não estruturais):** o valor declarado no protocolo prevalece sobre
o padrão; o padrão vale só quando o protocolo não declara o parâmetro. Trecho do protocolo presente e ilegível reprova a
conferência, sem cair no padrão. `python3 -m rsl mostrar` exibe o valor em uso e a origem de
cada parâmetro. Configuração ausente, inválida ou incompleta faz o subcomando parar com o
código CONFIGURACAO e mensagem que nomeia a chave.

### Scripts

Toda operação se executa por um ponto de entrada único, a partir da raiz do projeto:

```bash
PYTHONPATH=src python3 -m rsl <subcomando>     # ou, de dentro de src/: python3 -m rsl …
python3 -m rsl                                 # sem subcomando: a ajuda, com os códigos
```

Neste README os comandos aparecem como `python3 -m rsl …`, com `src/` no caminho de
importação. Os subcomandos se agrupam por atividade: `conferir`, `conferir-dados`,
`autoteste`, `mostrar`, `pendencias`, `gramatica`; `sementes planilha`;
`termos sonda|exportar|validar <sigla>|importar`; `busca
registrar|derivar|aderencia|fidelidade|sensibilidade`. Todo subcomando termina com um destes
códigos de saída, e toda saída diferente de OK termina com uma linha que nomeia o código:

| Código | Nome | Quando |
| --- | --- | --- |
| 0 | OK | a operação terminou e nada reprovou |
| 1 | REPROVADO | uma conferência ou condição de aceite reprovou o conteúdo: problema de coerência, `busca registrar` recusado, fidelidade acima do limiar, autoteste com caso que falhou |
| 2 | USO | argumento ou subcomando inválido |
| 3 | CONFIGURACAO | `config.toml` ausente, inválido ou incompleto, ou chave `protocolo` que aponta arquivo inexistente |
| 4 | PROTOCOLO_ILEGIVEL | protocolo ou ficha fora da gramática que o leitor exige (`gramatica`) |
| 5 | DADOS | arquivo alimentado, exportação ou arquivo de entrada ausente ou ilegível |
| 6 | PARCIAL | autoteste sem falha, com casos não executados |
| 7 | FONTE_EXTERNA | fonte externa com erro, bloqueio, captcha ou limite excedido |

Quando mais de uma condição ocorre, vale a mais grave: CONFIGURACAO, PROTOCOLO_ILEGIVEL,
DADOS, FONTE_EXTERNA, REPROVADO, PARCIAL. Os arquivos gravados seguem `snake_case`, em
português e sem acento, com o substantivo do conteúdo e, quando há um por chave, a chave em
minúsculas (`fidelidade_eb2.csv`, `sensibilidade_wos.csv`).

Os subcomandos leem o protocolo e os artefatos de `data/`; nenhum decide conteúdo —
conferem, derivam e registram. Quatro invariantes valem para todos:

- **Uma fonte por dado.** O vocabulário, as expressões, os critérios e os parâmetros que
  declara vêm do protocolo; a forma da busca, da ficha da base; o resto, do `config.toml`.
  Não há cópia intermediária nem valor de parâmetro no código.
- **O que é autoral se preserva.** O arquivo de sementes (`[documentos] sementes`), com a
  conferência de cada semente, as execuções em `registro_execucao.json` e a declaração de
  cobertura nas fichas são editados pelo pesquisador; nenhum subcomando grava o arquivo de
  sementes, `busca registrar` só acrescenta ou atualiza a execução que ele mesmo confere e
  `termos importar` preserva as decisões da validação na planilha.
- **Semente retirada sai de tudo; termo retirado fica registrado.** Semente retirada sai do
  arquivo de sementes, das saídas regeneradas e da evidência bruta, e as seguintes se
  renumeram, com a correspondência de `id` registrada em `data/historico.md`; evidência
  `SEn_…` de semente que não está no arquivo reprova `conferir-dados`. Termo retirado do
  protocolo permanece na planilha de validação como linha fora do protocolo. Termo vigente do protocolo ausente da string de uma base só passa se a ficha o
  declarar na redução; sem declaração, a conferência daquela base reprova — e só daquela.
  O vigente é a string (STR) do protocolo: termo que só consta do quadro terminológico não é
  esperado na base e, se aparecer nela, reprova. As fichas são operacionais — forma vigente,
  sem cabeçalho, histórico nem justificativa.
- **O identificador é a chave.** Tudo se identifica pelo código do protocolo — `QGR`/`QERn`,
  `FCTn`, `STRn`, `EBn`, `CEn`, `BDn`, `SEn` —, e não por posição. Cada semente tem um só
  lugar, o arquivo de sementes; não há ligação entre arquivos a manter.

`conferir` verifica a **coerência interna** do protocolo, não valores esperados: numeração
dos identificadores, camadas do vocabulário, string contida no quadro da sua faceta,
âncoras em todas as expressões, executada igual à união das específicas (a sonda ser a
conjunção das âncoras é garantido pela própria identificação), dimensões obrigatórias dos critérios, justificativa preenchida em
todo critério de elegibilidade, faixa de sensibilidade, instrumentos com idiomas e facetas
do protocolo, ficha existente para cada sigla de base, IDs de critério da seção 2 de cada
ficha iguais aos da tabela do protocolo e sementes citando só siglas da tabela de bases; a
distribuição das sementes por base e por papel é calculada do arquivo de sementes.
Protocolo, ficha ou arquivo de sementes fora da gramática sai com PROTOCOLO_ILEGIVEL, nomeando o elemento do contrato; incoerência,
com REPROVADO. `conferir-dados` reprova
arquivo alimentado ausente ou fora do protocolo, evidência bruta `SEn_…` de semente que não
está no arquivo de sementes, a execução que declara exportação
inexistente, a citação do registro de execução numa ficha sem identificador `(BDn/<id>)`, com `BDn` de outra base ou remetendo a execução
inexistente — e, por base, termo vigente fora da string sem redução declarada e termo fora
da STR dentro dela, mesmo em flexão.
`autoteste` injeta defeitos numa cópia em memória e exige que cada conferência reprove pelo
motivo e com o código esperados — inclusive configuração inválida, precedência, parâmetro
estrutural ausente ou inválido, cada elemento exigido da gramática, ficha divergente do
protocolo, arquivos alimentados, composição das expressões que quebra as relações entre
executada, específicas, geral e sonda, e aderência por papel —, numa só chamada e com a
contagem de cada grupo. As cópias defeituosas são geradas da estrutura lida, não de literais
do protocolo vigente: semente nova ou faixa alterada dentro do válido não quebram o
autoteste. Sem os arquivos alimentados, o resultado é PARCIAL, com o número de casos que não
rodaram.
`mostrar` exibe cada semente como referência montada dos campos, sem gravar. `pendencias`
relata sem escrever. Os comandos estão no fluxo
de trabalho, em M3.

## Fluxo de trabalho — RS Banyan

O RS Banyan organiza a revisão em **quatro módulos, catorze etapas e sessenta e três
passos**, sustentados por sete instrumentos próprios. O **PRISMA** não conduz a
execução: é a diretriz de apresentação do relato. A sequência abaixo segue os módulos e as
etapas; os passos detalhados, com responsável e data, estão no cronograma.

| Módulo | Etapas | O que decide |
| --- | --- | --- |
| **M1 — Planejamento** | 5: objetivos; necessidade; instrumentos operacionais; equipe; cronograma | se a revisão deve e pode ser feita, com que equipe, instrumentos e prazo |
| **M2 — Questão de revisão** | 2: tópicos preliminares; delimitação do assunto | o que exatamente se pergunta e o que fica fora da pergunta |
| **M3 — Pesquisa bibliográfica** | 4: estratégias; localização dos estudos; seleção; extração | como se busca, o que entra no portfólio e o que se extrai de cada item |
| **M4 — Discussão e redação** | 3: interpretação; registro e validação; preparação textual e divulgação | o que os achados significam, como se relatam e onde se publicam |

**M1 e M2 correm em paralelo**, com o controle terminológico iniciado no primeiro mês. Cada
marco é de **passa ou não passa**: reprovado, a correção se faz na fonte, a geração se
refaz e a decisão se registra no histórico. Nenhuma etapa é suprimida por prazo.

### M1 — Planejamento (E1–E5)

Decide a **exequibilidade** da revisão.

1. **E1 — objetivos.** Fixa a questão do projeto e o objetivo geral, com um objetivo
   específico por questão secundária.
2. **E2 — necessidade.** Justifica a revisão, delimita o escopo e o contra-escopo e
   distribui os cinco problemas representacionais entre esta revisão e as autônomas.
3. **E3 — instrumentos operacionais.** Viabiliza os sete instrumentos do RS Banyan; neste pacote estão o plano, o protocolo e as fichas de busca.
4. **E4 — equipe.** Define os papéis: ReT, RTG, VT, APB, Revisores 1 e 2 e RE.
5. **E5 — cronograma.** Compromete os marcos quinzenais e a data-limite dos revisores,
   anterior à execução das buscas definitivas.

**Fonte:** `docs/01_plano.md`, seções 1 a 3; equipe e cronograma detalhados
na planilha de competências e no cronograma, fora deste pacote. **Scripts:** nenhum — o produto é decisão registrada.

### M2 — Questão de revisão (E1–E2)

Decide **o que se pergunta** e **o que fica fora**.

1. **E1 — tópicos preliminares.** Levanta obras de referência, bibliotecas especializadas e
   os estudos inicialmente consultados. Esses três estudos **não são o conjunto-semente**:
   foram lidos como fundamentação, e o conjunto-semente existe para aferir a busca, não
   para confirmá-la.
2. **E2 — delimitação do assunto.** Fixa a temática, a abordagem, o objeto e o recorte; na
   estratégia, converte tudo em questão geral pelo PICo com desfecho acrescido e em
   QER1–QER4.

**Fonte:** `docs/02_protocolo_informacoes_gerais.md`, Etapas 1 e 2; questão e
questões secundárias em `docs/03_protocolo_estrategia_pesquisa.md`. **Scripts:**
nenhum nesta etapa; a questão é lida de `docs/03_protocolo_estrategia_pesquisa.md`, onde
M3/E1 a formaliza.
Skill: `questao-e-objetivos`; os critérios de elegibilidade derivam dela e são formalizados
em M3/E1, com a skill `criterios-de-elegibilidade`.

### M3 — Pesquisa bibliográfica (E1–E4)

Decide **como se busca**, **o que entra no portfólio** e **o que se extrai**.

#### E1 — Estratégias de pesquisa

Produz o protocolo executável. A ordem importa: o vocabulário alimenta as strings, as
strings alimentam as expressões, e as expressões só se executam depois de o conjunto-semente
existir.

1. **Facetação.** Quatro facetas, com duas âncoras obrigatórias — artefatos de representação
   e domínio educacional —, vocabulário nos três idiomas e camadas núcleo, próximos e
   relacionados.
2. **Validação terminológica.** Nos instrumentos que o protocolo declara para cada faceta
   ("Instrumentos para controle terminológico"), nos idiomas que cada um cobre (coluna
   `Idiomas` da mesma tabela). Instrumento `Manual` gera linha pendente de validação
   manual. Termo sem consulta registrada é termo livre e não pode ser apresentado como
   descritor autorizado.
3. **Strings por faceta.** Qualificação do vocabulário: substituição de palavra isolada pela
   forma composta, desdobramento da notação compacta e inclusão das formas morfológicas.
4. **As cinco expressões.** A de cobertura — `EB4 = STR1 AND STR2 AND (STR3 OR STR4)` — é a
   **única executada como busca definitiva**; as demais são calculadas localmente em M3/E2.
   `EB4` equivale a `EB2 ∪ EB3`, e `EB5 = STR1 AND STR2` é a **sonda de sensibilidade**,
   executada uma única vez e fora do corpus.
5. **Critérios de elegibilidade.** Inclusão e exclusão, de CE1 a CE9, com a regra única de
   inclusão por adequação temática (CE6) — práticas **e/ou** fatores situacionais — e o
   domínio de aplicação educacional (CE7 e CE8).
6. **Fontes.** Web of Science, Scopus, ERIC e BRAPCI, nessa ordem; acesso pelo Portal da
   CAPES com CAFe nas duas primeiras. A ausência de busca direta nos acervos especiais é
   limitação declarada, mitigada por backward search.
7. **Conjunto-semente.** Estudos e incidências esperadas por base, no arquivo de sementes
   (`[documentos] sementes`), com os dados bibliográficos, as bases que indexam cada
   semente (indexação, não recuperação), as facetas informadas pelo pesquisador, o papel e
   a conferência, campo a campo; a regra de ajuste e a
   fórmula de recuperação ficam no protocolo. É instrumento de aferição, não lista de incluídos: só as
   sementes de **validação** decidem a passagem; as de **desenvolvimento** orientaram o
   vocabulário e são relatadas como não decisórias.
8. **Ferramentas e registro de uso de IA.** Zotero para gestão e deduplicação, Rayyan para
   triagem cega e ASReview para priorização; o uso de IA é registrado ação a ação no LOG_IA,
   apêndice do protocolo.

```bash
# confere documento, dados e guardas
python3 -m rsl conferir
python3 -m rsl conferir-dados
python3 -m rsl autoteste
python3 -m rsl mostrar          # parâmetros em uso e a origem de cada um
python3 -m rsl gramatica        # a forma que o leitor exige do protocolo e das fichas

# validação terminológica: sonda obrigatória antes de validar
python3 -m rsl termos sonda
python3 -m rsl termos exportar
python3 -m rsl termos validar tbci
python3 -m rsl termos validar unesco
python3 -m rsl termos importar

# instrumento de aderência (planilha e ensaio seco no terminal)
python3 -m rsl sementes planilha
```

**Arquivos.** O vocabulário vem do protocolo, lido a cada execução; não há JSON derivado a
regerar. As sementes vêm só do arquivo de sementes, editado pelo pesquisador; nenhum
subcomando o grava. A validação grava o estatuto na própria planilha
`data/validacao_terminologica.csv` e a resposta bruta em
`data/evidencia/<instrumento>/`; `termos importar` reconcilia a planilha com o protocolo,
preservando decisões e linhas fora do protocolo. Erro de rede, bloqueio, captcha, limite ou
resposta fora do formato interrompe `termos validar` na hora, sem nova tentativa e sem
consultar o termo seguinte: o que já foi consultado fica gravado, a linha do termo
interrompido registra a condição, e o código é FONTE_EXTERNA. A detecção de captcha é
heurística, por marcadores no corpo; por isso resposta fora do formato esperado também
interrompe. O conjunto-semente gera
`data/semente_aderencia.csv` — uma linha por semente e por base, com a coluna `papel` — e
imprime o ensaio seco no terminal; não grava guia em arquivo.

**Garantias.** `conferir` reprova o documento fora da forma; `conferir-dados` reprova
arquivo alimentado ausente ou fora do protocolo, execução que declara exportação inexistente,
citação do registro de execução sem identificador `(BDn/<id>)`, de outra base ou de execução
inexistente, e, por base, termo vigente ausente sem redução declarada ou termo fora da STR
presente, e evidência bruta de semente que não está no arquivo de sementes. `autoteste` injeta
defeitos numa cópia e exige que as conferências os reprovem com o código esperado.

**Condição de passagem:** viabilidade das strings e protocolo validado por revisor expert.
Reprovado, volta-se ao vocabulário e registra-se a emenda no histórico.
Skills: `facetacao-e-termos-livres`, `validacao-vocabulario-controlado`,
`expressoes-de-busca`, `ficha-de-busca-por-base` e `conjunto-semente`.

#### E2 — Localização dos estudos

Executa a busca e transforma a exportação em conjunto verificável.

1. **Sondagem de sintaxe.** Obrigatória na ERIC e na BRAPCI antes de qualquer execução; o
   procedimento e as ressalvas estão na ficha da base. Automação de interface só depois de
   conferidos os termos de uso, e a autenticação federada é feita pelo pesquisador.
2. **Execução.** Executa-se **a expressão de cobertura uma vez por base** — e não as
   cinco —, com o recorte temporal aplicado na busca na WoS, na Scopus e na BRAPCI e pelo
   filtro da página de resultados na ERIC. Na ERIC, a expressão se desdobra em quatro
   consultas de campo único, unidas na derivação. A sonda de sensibilidade, `EB5`, roda
   uma única vez por base e fica fora do corpus.
3. **Registro e exportação.** A exportação fica intacta em `data/execucoes/<base>/`; cada
   consulta é registrada com o retorno que a base exibiu.
4. **Derivação local.** As demais são calculadas sobre a exportação da de cobertura, com
   deduplicação dentro da base — a segunda ocorrência é marcada em `duplicata_de`, e nada é
   apagado.
5. **Aderência.** Mede o recall contra o conjunto-semente; o denominador definitivo é o que
   cada base indexa, conferido à mão, e o limiar (regra de ajuste do protocolo) vale
   **sobre a união das bases**. O relato separa as sementes de **validação** das de
   **desenvolvimento**: só a validação é comparada ao limiar, e só ela traz o intervalo de
   Wilson a 95%. O desenvolvimento é não decisório e não compensa a validação. O casamento
   por prefixo é indício e não entra no numerador: exige conferência humana.
6. **Fidelidade.** Executa as duas específicas diretamente na WoS e na Scopus e compara com a
   derivação; divergência acima do limiar (`divergencia_fidelidade`) reprova o método.
7. **Coerência e cobertura.** Confere as relações de continência entre as expressões —
   `EB4 = EB2 ∪ EB3` e `EB5 ⊃ EB4` — e a cobertura de campo da exportação. A conferência é
   condição necessária e não suficiente: o que garante a coerência é a construção —
   expressões uniformes e execução única da de cobertura —, não a verificação.
8. **Sensibilidade.** `busca sensibilidade` mede quanto `EB5` recupera que `EB4` não, e grava
   a amostra a classificar. O que decide é a fração **elegível** dessa amostra, classificada
   à mão, contra a faixa de sensibilidade do protocolo (detalhamento de EB5).
9. **Calibração da triagem assistida.** Antes do primeiro uso, o ASReview passa por estudo
   de viabilidade e calibração, com o limiar `calibracao_triagem` do `config.toml`. A
   ferramenta ordena a fila; não decide inclusão.

```bash
# registra a consulta; na ERIC, um arquivo por consulta da forma particionada
python3 -m rsl busca registrar wos <expressão> data/execucoes/wos/<arquivo>.ris --retorno <n>

# deriva as expressões não executadas, conta únicos e grava a ordem de triagem
python3 -m rsl busca derivar

# aderência ao conjunto-semente
python3 -m rsl busca aderencia

# fidelidade da derivação, exigida na WoS e na Scopus
python3 -m rsl busca fidelidade <expressão> data/execucoes/wos/<arquivo>.ris

# sonda de sensibilidade: fração de EB5 fora de EB4, com a amostra a classificar
python3 -m rsl busca sensibilidade wos
```

**Arquivos.** `data/registro_execucao.json` é o registro documental e o rastro técnico das
execuções; `busca derivar` lê as execuções registradas, não a pasta de exportações. As
saídas ficam na raiz de `data/` (`[saidas]` do `config.toml`): `registros.csv`,
`contagens_busca.csv`, `ordem_triagem.csv`, `fidelidade_<expressão>.csv` por expressão
conferida e `sensibilidade_<base>.csv` por base sondada, com a chave em minúsculas. A
aderência usa o arquivo de sementes (`[documentos] sementes`) e `data/semente_aderencia.csv`;
o relato por papel lê o campo `papel` de cada semente, e só a validação decide a passagem.

**Recusas e marcas.** `busca registrar` confere o retorno declarado contra os registros do
arquivo e **recusa registrar quando divergem**, salvo justificativa explícita — o caso do
teto de retorno da BRAPCI (ficha da base). A execução aceita é gravada na base correspondente do
`registro_execucao.json`, com `arquivo`, `registros_lidos` e `status`; é essa entrada que
`busca derivar`, `busca aderencia` e `busca sensibilidade` leem. `busca derivar` reconfere a
contagem e para, com o código DADOS, se o arquivo mudou ou faltar. As contagens da busca usam os registros únicos, com o número bruto ao
lado. O recorte temporal é apenas conferido aqui, e a linha "fora" deve ser zero em todas as
bases.

**Condição de passagem:** suficiência do portfólio — aderência de **validação** e fidelidade
dentro dos limiares (`python3 -m rsl mostrar`). Fora disso, revisa-se o controle terminológico antes de
prosseguir, com emenda registrada. Skills: `busca-nas-bases`, `deduplicacao`,
`teste-de-aderencia` e `conferencias-da-busca`.

#### E3 — Seleção dos estudos

Converte o conjunto recuperado no **Portfólio Definitivo**. A 1ª filtragem só começa com a
calibração da triagem assistida aprovada em E2.

1. **Deduplicação entre bases.** Feita no Zotero antes da 1ª filtragem; a deduplicação
   dentro de cada base já foi feita na derivação. Par duvidoso não é fundido sem decisão.
2. **1ª filtragem — título.** Dois revisores humanos em modo cego no Rayyan, com kappa. A
   classificação assistida por LLM corre em paralelo e **não exclui**; o revisor não vê a
   saída da IA antes de registrar a sua decisão. A fila é percorrida integralmente — a
   priorização altera a ordem de leitura, nunca o conjunto lido —, e
   `data/ordem_triagem.csv` registra a ordem por pertinência e recência.
3. **2ª filtragem — título e resumo.** Aplica os critérios decidíveis sem o texto completo:
   recorte, idioma, tipo documental e exclusões temáticas manifestas, com kappa. O documento
   cujo texto completo não se localiza, depois de tentativas documentadas, é registrado como
   não localizado, e não como exclusão temática (P4).
4. **3ª filtragem — texto completo.** Confirma a elegibilidade com CE6 (adequação temática)
   e CE7 a CE9 (P5), e justifica cada exclusão pelo ID do critério. Dois revisores
   independentes, sem IA na decisão, com kappa. Divergência remanescente vai ao VT.
5. **Backward search.** Uma geração, apenas sobre os estudos incluídos. Revisões
   sistemáticas e de escopo ficam fora do portfólio de evidência primária pelo CE5 e vão para
   **conjunto suplementar** com contagem própria.
6. **Registro do fluxo.** O fluxograma PRISMA registra as exclusões justificadas e
   quantificadas em cada passagem.

**Arquivos e ferramentas.** `data/ordem_triagem.csv` ordena a 1ª filtragem;
Zotero, Rayyan e ASReview executam a etapa; o fluxograma PRISMA é produzido fora deste pacote.
**Scripts:** nenhum — a decisão de inclusão é humana. Skills: `calibracao-da-triagem` e
`filtragens`.

**Condição de passagem:** conclusão das três filtragens, com kappa calculado nas três.

#### E4 — Extração de dados

Transforma cada estudo incluído em dado comparável.

1. **Fichamento.** Cada estudo incluído preenche o formulário de fichamento; o pré-preenchimento assistido por
   IA é conferido campo a campo no texto-fonte. As cinco categorias de Fink são o **esquema
   de codificação**, e não um enquadramento obrigatório: fator não previsto nelas é
   registrado em "outros fatores" e constitui achado.
2. **Glossário.** O glossário reúne as definições e as fontes de cada conceito, validadas pelo
   pesquisador.

**Arquivos:** formulário de fichamento e glossário, fora deste pacote. **Scripts:** nenhum — a extração é leitura.
Skill: `fichamento`.

**Condição de passagem:** conclusão dos fichamentos.

### M4 — Discussão e redação (E1–E3)

1. **E1 — interpretação do conhecimento.** Análise bibliométrica e de conteúdo; comparação
   dos artefatos por cobertura, granularidade e grau de formalização; formulação das lacunas
   de representação. A distribuição por comunidade de origem é, por si, achado. Skill:
   `sintese-e-lacunas`.
2. **E2 — registro e validação do conteúdo.** Redação do relatório com a lista do PRISMA
   respondida item a item, cada item classificado como aplicável sem adaptação, não
   aplicável com justificativa ou adaptado ao objeto. O fluxograma PRISMA vem das contagens da busca; as
   limitações, das decisões registradas; a declaração de uso de IA, do LOG_IA. Skill:
   `relato-prisma`.
3. **E3 — preparação textual e divulgação.** Revisão de língua, tradução do resumo,
   normalização ABNT e submissão; toda referência é conferida na fonte. Skill:
   `conferir-referencia`.

**Arquivos:** relatório e apêndices, fora deste pacote; regras de uso de IA em
`docs/01_plano.md`, seção 8. **Scripts:** nenhum.

### Atividades transversais

- **Toda decisão que altere questão, facetas, critérios ou busca é emenda.** Altera-se o
  documento-fonte — o plano, o protocolo, a ficha da base ou o arquivo de sementes —; a
  decisão se registra no histórico,
  `data/historico.md`. Não se edita planilha de saída nem se corrige o produto à mão:
  corrige-se a fonte e confere-se de novo — a exceção é a planilha de validação, que é o
  registro do estatuto dos termos. Skill: `registrar-decisao`.
- **Rastreabilidade.** Questão, objetivos, facetas, quadro terminológico, strings e
  critérios precisam concordar; `conferir` e `conferir-dados` são a trava, e
  `autoteste` prova que as conferências reprovam. Skill: `rastreabilidade`.
- **Otimização de strings e vocabulário.** Diagnostica redundância, polissemia e lacuna no
  controle terminológico e nas strings por faceta. Skill:
  `otimizar-strings-revisao-sistematica`.
- **Referências.** Nenhum dado bibliográfico se preenche de memória: confere-se na fonte e
  registra-se o estado da conferência. Skill: `conferir-referencia`.
- **Revisão geral do projeto.** Percorre o estado do ciclo e os instrumentos, executa as
  conferências e os autotestes, confere o lastro das afirmações e entrega achados
  classificados; não escreve, não acessa fonte externa e não decide. Skill:
  `revisao-geral-do-projeto`.
- **Parecer externo.** Cada achado é conferido contra o texto corrente antes de aceito; o
  parecer é hipótese sobre o documento, não constatação. Skill: `parecer-sobre-protocolo`.
- **Pendências.** As ações por fazer ficam em `data/pendencias.json`.
  `python3 -m rsl pendencias` relata o que encontra nos artefatos, sem escrever
  e sem ler esse arquivo; promover um achado a pendência registrada é decisão do
  pesquisador.

## Precedência

- O **protocolo** — `02_protocolo_informacoes_gerais.md` e `03_protocolo_estrategia_pesquisa.md` —
  prevalece sobre qualquer formulação feita em outro documento; o plano remete a ele. Sobre
  o `config.toml`, o protocolo prevalece em todo parâmetro que declara; os parâmetros
  estruturais só existem no protocolo.
- O **histórico** é o único lugar das decisões; `data/pendencias.json`, das ações por
  fazer; `data/registro_execucao.json`, dos resultados das consultas nas bases.
- A data **oficial** de execução consta **exclusivamente do cronograma**, que não integra este
  pacote; `data/registro_execucao.json` registra data e hora operacionais de cada execução,
  como rastro técnico do registro.

## Convenções

- **Português do Brasil**, redação formal, objetiva e enxuta.
- Referências normalizadas pela **ABNT NBR 6023**, cada uma com o seu estado de conferência.
- Datas de execução no **cronograma**; histórico em `data/historico.md`.
- Nomeação dos arquivos de estudo: `Ano_DuasPrimeirasPalavras_TIPO_UltimoSobrenomeAutor`,
  com sufixo `_FICHA` para fichamentos.

## Autoria e uso de IA

**Junilson Pereira Souza** — responsabilidade técnica.

A assistência de inteligência artificial é declarada e registrada ação a ação no LOG_IA,
apêndice do protocolo. A IA **não é autora**, conforme ICMJE e COPE. As regras de uso estão em
`docs/01_plano.md`, seção 8.
