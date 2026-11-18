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
| `src/` | scripts de execução |
| `config.toml` | configuração dos scripts: caminho do protocolo, valores padrão dos parâmetros, fichas, arquivos de dados e instrumentos |
| `.agents/skills/` | competências metodológicas e operacionais do agente |
| `AGENTS.md` | contrato de trabalho do agente: como ele se comporta, não o que o projeto decide |

Este pacote reúne o **plano**, o **protocolo**, as **fichas de busca** e o **histórico**,
em `data/historico.md`. Os demais instrumentos e o portfólio não integram este repositório.

## Mapa

| Caminho | O que contém | Consultar quando |
| --- | --- | --- |
| `docs/01_plano.md` | Plano: contexto, objetivos, método, escopo, cronograma, recursos, custos, qualidade, riscos e uso de IA | entender o desenho e os limites da revisão |
| `docs/02_protocolo_informacoes_gerais.md` | Protocolo, informações gerais: título, vínculo institucional, projeto, tópicos preliminares, objeto e recorte | conferir o que a revisão examina e o que fica fora |
| `docs/03_protocolo_estrategia_pesquisa.md` | Protocolo, estratégias de pesquisa: questão de revisão (QGR, QERn), facetas, instrumentos de controle terminológico, vocabulário, strings, expressões, critérios de elegibilidade, fontes e conjunto-semente. Fonte única desses dados e dos parâmetros que declara | montar ou conferir a busca |
| `docs/busca_base_1_web_of_science.md` | ficha da Web of Science: sintaxe, strings por faceta, expressões, variantes, conjunto-semente e ressalvas | executar ou auditar esta base |
| `docs/busca_base_2_scopus.md` | ficha da Scopus, mesma estrutura | idem |
| `docs/busca_base_3_eric.md` | ficha da ERIC, mesma estrutura | idem |
| `docs/busca_base_4_brapci.md` | ficha da BRAPCI, mesma estrutura | idem |
| `src/protocolo.py` | leitor do protocolo: confere documento e arquivos alimentados, e reconcilia o metadado das sementes | antes de executar qualquer script, e após alterar o protocolo |
| `src/derivar_expressoes.py` | registro das execuções no `registro_execucao.json`, derivação local das expressões, aderência, fidelidade e sonda de sensibilidade | registrar execução, calcular a pertinência de cada registro, testar a busca |
| `src/validar_termos.py` | validação terminológica nos instrumentos que o protocolo declara por faceta: consulta automatizada onde há cliente (TBCI, UNESCO Thesaurus) e linha pendente de validação manual nos demais, com a planilha como registro | conferir o estatuto de cada termo |
| `src/gen_semente.py` | geração da planilha de aderência a partir do conjunto-semente, com o ensaio seco impresso no terminal | montar o instrumento do teste de aderência, uma linha por semente e por base |
| `data/historico.md` | Histórico: decisões relevantes sobre a revisão, inclusive as emendas, com data, alcance e fundamento | saber o que já foi decidido e por quê |
| `data/pendencias.json` | Pendências: ações ainda a executar, cada uma com origem, o que bloqueia, ação sugerida, responsável e estado | saber o que falta fazer |
| `config.toml` | caminho do protocolo, padrões dos parâmetros, fichas, arquivos de dados, instrumentos e campos das planilhas | mudar o arquivo do protocolo, um padrão ou um instrumento |

Em `data/` (caminhos em `[dados]` do `config.toml`), a procedência de cada arquivo:

| Caminho | O que contém | Quem escreve |
| --- | --- | --- |
| `data/sementes.json` | metadados de conferência de cada semente, ligados por DOI ou título | pesquisador, reconciliado por `--sincronizar` |
| `data/registro_execucao.json` | resultados da execução das consultas nas bases: sondagens de sintaxe, estado da interface, retornos, exportações, conferências e aderência, por base; e, em cada execução registrada, o arquivo e a conferência do retorno | pesquisador e `--registrar` |
| `data/historico.md` | Histórico: decisões relevantes sobre a revisão, com data, alcance e fundamento | pesquisador |
| `data/pendencias.json` | ações ainda a executar, identificadas por `PDnn` | pesquisador e agente, a pedido |
| `data/execucoes/<base>/` | exportações intactas das bases | pesquisador |
| `data/` (raiz) | planilhas e CSVs gerados pelos scripts: `validacao_termologica.csv`, `semente_aderencia.csv`, `registros.csv`, `contagens_busca.csv`, `ordem_triagem.csv`, `fidelidade_EB<n>.csv` e `sensibilidade_<base>.csv`; a planilha de validação é o registro do estatuto dos termos | scripts e pesquisador (planilha de validação) |
| `data/evidencia/` | resposta bruta de cada consulta terminológica | `validar_termos.py` |
| `data/arquivo/` | cópias anteriores, com `SHA256` | migrações |

As pastas `execucoes/`, `evidencia/` e `arquivo/` são criadas quando o primeiro arquivo chega.

O que é **derivado do documento não vira arquivo**: questão, facetas, instrumentos,
strings, expressões, critérios e fontes são lidos do protocolo a cada execução, e a forma de
cada base, da ficha correspondente. Em `data/` guarda-se o que alguém **alimenta** — o
metadado das sementes e o registro das execuções — e a planilha de validação, registro do
estatuto dos termos, lida e regravada por `validar_termos.py`.

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

`config.toml`, na raiz, é lido por `src/protocolo.py` com `tomllib` (**Python 3.11+**, só
biblioteca padrão). Ele traz:

- `protocolo` — o arquivo do protocolo a ser lido; é o único parâmetro que o protocolo não
  sobrescreve;
- `[padroes]` — valor padrão de cada parâmetro que o protocolo pode declarar: recorte, limiar
  de aderência, faixa de sensibilidade, âncoras, expressão executada, sonda, composição das
  expressões, limiar de divergência da fidelidade e sensibilidade mínima da calibração da
  triagem assistida;
- os parâmetros que o protocolo não declara: dimensões obrigatórias dos critérios, mínimo de
  termos por string, natureza que identifica a executada e a sonda, fichas das bases,
  arquivos de dados, cores das facetas, campos das planilhas;
- `[instrumentos]` — sigla, idiomas cobertos e modo de consulta (`tbci`, `unesco` ou
  `manual`) de cada instrumento; quais instrumentos valem para cada faceta vem do protocolo.

**Precedência:** o valor declarado no protocolo prevalece sobre o padrão; o padrão vale só
quando o protocolo não declara o parâmetro. Trecho do protocolo presente e ilegível reprova a
conferência, sem cair no padrão. `python3 src/protocolo.py --mostrar` exibe o valor em uso e
a origem de cada parâmetro. Configuração ausente, inválida ou incompleta faz os scripts
pararem com mensagem que nomeia a chave.

### Scripts

Os scripts leem o protocolo e os artefatos de `data/`; nenhum decide conteúdo — conferem,
derivam e registram. Quatro invariantes valem para todos:

- **Uma fonte por dado.** O vocabulário, as expressões, os critérios e os parâmetros que
  declara vêm do protocolo; a forma da busca, da ficha da base; o resto, do `config.toml`.
  Não há cópia intermediária nem valor de parâmetro no código.
- **O que é autoral se preserva.** Os metadados de conferência em `sementes.json`, as
  execuções em `registro_execucao.json` e a declaração de cobertura nas fichas são editados
  pelo pesquisador; `--sincronizar` só reconcilia sementes, `--registrar` só acrescenta ou
  atualiza a execução que ele mesmo confere e `--importar` preserva as decisões da
  validação na planilha.
- **Nada se apaga por sincronização.** Semente retirada do protocolo permanece no arquivo
  com o seu metadado e é reportada por `--conferir-dados` e por `--pendencias`, para decisão;
  termo retirado do protocolo permanece na planilha de validação como linha fora do
  protocolo. Termo vigente do protocolo ausente da string de uma base só passa se a ficha o
  declarar na redução; sem declaração, a conferência daquela base reprova — e só daquela.
  O vigente é a string (STR) do protocolo: termo que só consta do quadro terminológico não é
  esperado na base e, se aparecer nela, reprova. As fichas são operacionais — forma vigente,
  sem cabeçalho, histórico nem justificativa.
- **O identificador é a chave.** Tudo se identifica pelo código do protocolo — `QGR`/`QERn`,
  `FCTn`, `STRn`, `EBn`, `CEn`, `BDn`, `SEn` —, e não por posição. Na semente, a ligação com
  o protocolo é feita por DOI ou título, de modo que o rótulo pode mudar sem perder o
  metadado.

`--conferir` verifica a **coerência interna** do protocolo, não valores esperados: numeração
dos identificadores, camadas do vocabulário, string contida no quadro da sua faceta,
âncoras em todas as expressões, sonda igual à conjunção das âncoras, executada igual à
união das específicas, dimensões obrigatórias dos critérios, faixa de sensibilidade,
instrumentos resolvidos pela configuração, fichas ligadas às bases e distribuição do
conjunto-semente. `--conferir-dados` reprova arquivo alimentado ausente ou fora do
protocolo, a execução que declara exportação inexistente e, por base, termo vigente fora da
string sem redução declarada e termo fora da STR dentro dela, mesmo em flexão.
`--autoteste` injeta defeitos numa cópia e exige que cada conferência reprove pelo motivo
esperado — inclusive configuração inválida, precedência e ficha divergente do protocolo.
`--sincronizar` religa a semente por DOI ou título, sem tocar no que já foi conferido; rodar
duas vezes não muda nada. `--pendencias` relata sem escrever. Os comandos estão no fluxo de
trabalho, em M3.

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
   ("Instrumentos para controle terminológico"), nos idiomas que cada um cobre
   (`config.toml`). Instrumento sem cliente automatizado gera linha pendente de validação
   manual. Termo sem consulta registrada é termo livre e não pode ser apresentado como
   descritor autorizado.
3. **Strings por faceta.** Qualificação do vocabulário: substituição de palavra isolada pela
   forma composta, desdobramento da notação compacta e inclusão das formas morfológicas.
4. **As cinco expressões.** A de cobertura — `EB4 = STR1 + STR2 + (STR3 OR STR4)` — é a
   **única executada como busca definitiva**; as demais são calculadas localmente em M3/E2.
   `EB4` equivale a `EB2 ∪ EB3`, e `EB5 = STR1 + STR2` é a **sonda de sensibilidade**,
   executada uma única vez e fora do corpus.
5. **Critérios de elegibilidade.** Inclusão e exclusão, com a regra única de inclusão —
   práticas **e/ou** fatores situacionais — e a regra de borda.
6. **Fontes.** Web of Science, Scopus, ERIC e BRAPCI, nessa ordem; acesso pelo Portal da
   CAPES com CAFe nas duas primeiras. A ausência de busca direta nos acervos especiais é
   limitação declarada, mitigada por backward search.
7. **Conjunto-semente.** Estudos e incidências esperadas por base, no protocolo. É
   instrumento de aferição, não lista de incluídos.
8. **Ferramentas e registro de uso de IA.** Zotero para gestão e deduplicação, Rayyan para
   triagem cega e ASReview para priorização; o uso de IA é registrado ação a ação no LOG_IA,
   apêndice do protocolo.

```bash
# confere documento, dados e guardas
python3 src/protocolo.py --conferir
python3 src/protocolo.py --conferir-dados
python3 src/protocolo.py --conferir --autoteste
python3 src/protocolo.py --mostrar      # parâmetros em uso e a origem de cada um

# validação terminológica: sonda obrigatória antes de validar
python3 src/validar_termos.py --sonda
python3 src/validar_termos.py --exportar
python3 src/validar_termos.py --validar tbci
python3 src/validar_termos.py --validar unesco
python3 src/validar_termos.py --importar

# instrumento de aderência: planilha por semente e por base, e ensaio seco no terminal
python3 src/gen_semente.py
```

**Arquivos.** O vocabulário vem do protocolo, lido a cada execução; não há JSON derivado a
regerar. `--sincronizar` mexe apenas no metadado das
sementes: religa a semente de `sementes.json` por DOI ou título, preservando o que já foi
conferido. A validação grava o estatuto na própria planilha
`data/validacao_termologica.csv` e a resposta bruta em
`data/evidencia/<instrumento>/`; `--importar` reconcilia a planilha com o protocolo,
preservando decisões e linhas fora do protocolo. O conjunto-semente gera
`data/semente_aderencia.csv` — uma linha por semente e por base — e imprime o ensaio seco
no terminal; não grava guia em arquivo.

**Garantias.** `--conferir` reprova o documento fora da forma; `--conferir-dados` reprova
arquivo alimentado ausente ou fora do protocolo, execução que declara exportação inexistente
e, por base, termo vigente ausente sem redução declarada ou termo fora da STR presente.
`--sincronizar` não apaga
semente retirada do protocolo: ela permanece e é reportada, para decisão. `--autoteste` injeta
defeitos numa cópia e exige que as conferências os reprovem.

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
5. **Aderência.** Mede o recall contra o conjunto-semente; o denominador é o que cada base
   indexa, conferido à mão, e o limiar (regra de ajuste do protocolo) vale **sobre a união
   das bases**.
6. **Fidelidade.** Executa as duas específicas diretamente na WoS e na Scopus e compara com a
   derivação; divergência acima do limiar (`divergencia_fidelidade`) reprova o método.
7. **Coerência e cobertura.** Confere as relações de continência entre as expressões —
   `EB4 = EB2 ∪ EB3` e `EB5 ⊃ EB4` — e a cobertura de campo da exportação. A conferência é
   condição necessária e não suficiente: o que garante a coerência é a construção —
   expressões uniformes e execução única da de cobertura —, não a verificação.
8. **Sensibilidade.** `--sensibilidade` mede quanto `EB5` recupera que `EB4` não, e grava
   a amostra a classificar. O que decide é a fração **elegível** dessa amostra, classificada
   à mão, contra a faixa de sensibilidade do protocolo (detalhamento de EB5).
9. **Calibração da triagem assistida.** Antes do primeiro uso, o ASReview passa por estudo
   de viabilidade e calibração, com o limiar `calibracao_triagem` do `config.toml`. A
   ferramenta ordena a fila; não decide inclusão.

```bash
# registra a consulta; na ERIC, um arquivo por consulta da forma particionada
python3 src/derivar_expressoes.py --registrar wos <expressão> data/execucoes/wos/<arquivo>.ris --retorno <n>

# deriva as expressões não executadas, conta únicos e grava a ordem de triagem
python3 src/derivar_expressoes.py --derivar

# aderência ao conjunto-semente
python3 src/derivar_expressoes.py --aderencia

# fidelidade da derivação, exigida na WoS e na Scopus
python3 src/derivar_expressoes.py --fidelidade <expressão> data/execucoes/wos/<arquivo>.ris

# sonda de sensibilidade: fração de EB5 fora de EB4, com a amostra a classificar
python3 src/derivar_expressoes.py --sensibilidade wos
```

**Arquivos.** `data/registro_execucao.json` é o registro documental e o rastro técnico das
execuções; `--derivar` lê as execuções registradas, não a pasta de exportações. As saídas
ficam na raiz de `data/`: `registros.csv`, `contagens_busca.csv`, `ordem_triagem.csv`,
um CSV de fidelidade por expressão conferida e um de sensibilidade por base sondada. A
aderência usa `data/sementes.json` e `data/semente_aderencia.csv`.

**Recusas e marcas.** `--registrar` confere o retorno declarado contra os registros do
arquivo e **recusa registrar quando divergem**, salvo justificativa explícita — o caso do
teto de retorno da BRAPCI (ficha da base). A execução aceita é gravada na base correspondente do
`registro_execucao.json`, com `arquivo`, `registros_lidos` e `status`; é essa entrada que
`--derivar`, `--aderencia` e `--sensibilidade` leem. `--derivar` reconfere a contagem e para
se o arquivo mudou. As contagens da busca usam os registros únicos, com o número bruto ao
lado. O recorte temporal é apenas conferido aqui, e a linha "fora" deve ser zero em todas as
bases.

**Condição de passagem:** suficiência do portfólio — aderência e fidelidade dentro dos
limiares (`--mostrar`). Fora disso, revisa-se o controle terminológico antes de prosseguir, com
emenda registrada. Skills: `busca-nas-bases`, `deduplicacao`, `teste-de-aderencia` e
`conferencias-da-busca`.

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
   recorte, idioma, tipo documental e exclusões temáticas manifestas, com kappa.
4. **3ª filtragem — texto completo.** Aplica integralmente o CE6, com a regra de
   exceção e a regra de borda, e justifica cada exclusão. Dois revisores independentes, sem
   IA na decisão, com kappa. Divergência remanescente vai ao VT.
5. **Backward search.** Uma geração, apenas sobre os estudos incluídos. Revisões
   sistemáticas permanecem elegíveis, mas vão para **conjunto suplementar** com contagem
   própria.
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
  documento-fonte — o plano, o protocolo ou a ficha da base — e, quando o dado é o metadado das
  sementes, reconcilia-se com `--sincronizar`; a decisão se registra no histórico,
  `data/historico.md`. Não se edita planilha de saída nem se corrige o produto à mão:
  corrige-se a fonte e confere-se de novo — a exceção é a planilha de validação, que é o
  registro do estatuto dos termos. Skill: `registrar-decisao`.
- **Rastreabilidade.** Questão, objetivos, facetas, quadro terminológico, strings e
  critérios precisam concordar; `--conferir` e `--conferir-dados` são a trava, e
  `--autoteste` prova que as conferências reprovam. Skill: `rastreabilidade`.
- **Referências.** Nenhum dado bibliográfico se preenche de memória: confere-se na fonte e
  registra-se o estado da conferência. Skill: `conferir-referencia`.
- **Parecer externo.** Cada achado é conferido contra o texto corrente antes de aceito; o
  parecer é hipótese sobre o documento, não constatação. Skill: `parecer-sobre-protocolo`.
- **Pendências.** As ações por fazer ficam em `data/pendencias.json`.
  `python3 src/protocolo.py --pendencias` relata o que encontra nos artefatos, sem escrever
  e sem ler esse arquivo; promover um achado a pendência registrada é decisão do
  pesquisador.

## Precedência

- O **protocolo** — `02_protocolo_informacoes_gerais.md` e `03_protocolo_estrategia_pesquisa.md` —
  prevalece sobre qualquer formulação feita em outro documento; o plano remete a ele. Sobre
  o `config.toml`, o protocolo prevalece em todo parâmetro que declara.
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
