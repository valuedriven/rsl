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
| `docs/` | conteúdo da revisão: IO 0 e IO 1, o Anexo A e as fichas de busca |
| `data/` | dados do projeto: os dez JSON, as exportações, as saídas dos scripts e o arquivo |
| `src/` | quatro scripts de execução |
| `.agents/skills/` | 19 competências metodológicas e operacionais do agente |
| `AGENTS.md` | contrato de trabalho do agente: como ele se comporta, não o que o projeto decide |

Este pacote reúne o **IO 0**, o **IO 1**, o **Anexo A** e as quatro **fichas de busca**. Os
IO 2 a IO 7 e o portfólio não integram este repositório.

## Mapa

| Caminho | O que contém | Consultar quando |
| --- | --- | --- |
| `docs/01_plano.md` | IO 0: contexto, objetivos, método, escopo, cronograma, recursos, custos, qualidade, riscos e uso de IA | entender o desenho e os limites da revisão |
| `docs/historico.md` | Anexo A: linha do tempo das decisões, verificações, calibração das buscas, emendas e pendências | saber o que já foi decidido, verificado ou está em aberto |
| `docs/02_protocolo_informacoes_gerais.md` | IO 1, informações gerais: título, vínculo institucional, projeto, tópicos preliminares, objeto e recorte | conferir o que a revisão examina e o que fica fora |
| `docs/03_protocolo_estrategia_pesquisa.md` | IO 1, estratégias de pesquisa: questão de revisão (QGR, QER1–QER4), facetas, strings, expressões, critérios de elegibilidade, fontes e conjunto-semente. Fonte única dos JSON | montar ou conferir a busca |
| `docs/strings_busca_1_Web_of_Science.md` | ficha da Web of Science: sintaxe, strings por faceta, expressões, variantes, conjunto-semente e ressalvas | executar ou auditar esta base |
| `docs/strings_busca_2_Scopus.md` | ficha da Scopus, mesma estrutura | idem |
| `docs/strings_busca_3_ERIC.md` | ficha da ERIC, mesma estrutura | idem |
| `docs/strings_busca_4_BRAPCI.md` | ficha da BRAPCI, mesma estrutura | idem |
| `src/protocolo.py` | leitor do protocolo: confere e deriva os JSON de `data/` | antes de executar qualquer script, e após alterar o protocolo |
| `src/derivar_expressoes.py` | registro das consultas, derivação local das expressões não executadas, aderência e fidelidade | registrar execução, calcular a pertinência de cada registro, testar a busca |
| `src/validar_termos.py` | validação assistida no TBCI e no UNESCO Thesaurus | conferir o estatuto de cada termo |
| `src/gen_semente.py` | geração do instrumento de aderência a partir do conjunto-semente | montar a planilha de aferição de uma base |

Em `data/`, a procedência de cada arquivo:

| Caminho | O que contém | Quem escreve |
| --- | --- | --- |
| `data/questoes.json` | questão geral (QGR), QER1–QER4 e estrutura PICo | `--gerar` |
| `data/facetas.json` | palavras significativas: nome, cor e âncora de cada faceta | `--gerar` |
| `data/descritores.json` | controle terminológico por faceta e estatuto de validação de cada termo | `--gerar` + validação |
| `data/strings.json` | string de cada faceta e composição das quatro expressões | `--gerar` |
| `data/criterios.json` | critérios de inclusão e de exclusão e recorte temporal | `--gerar` |
| `data/fontes.json` | bases, ordem de execução, via de acesso, acervos e ferramenta | `--gerar` |
| `data/sementes.json` | conjunto-semente e metadados de conferência de cada referência | `--gerar` + pesquisador |
| `data/consultas.json` | registro das execuções: base, expressão, data e hora, retorno | `--registrar` |
| `data/registro_execucao.json` | sondagens de sintaxe, estado da interface, retornos, exportações, conferências e aderência, por base | pesquisador |
| `data/pendencias.json` | estado das tarefas e pendências abertas | pesquisador |
| `data/execucoes/<base>/` | exportações intactas das bases | pesquisador |
| `data/saida/` | planilhas, CSVs e instrumentos gerados pelos scripts | scripts |
| `data/evidencia/` | resposta bruta de cada consulta terminológica | `validar_termos.py` |
| `data/arquivo/` | cópias anteriores, com `SHA256` — sem conteúdo no momento: o arquivo do estado anterior à migração (16/11) foi descartado em 17/11 | migrações |

As pastas de dados brutos e de arquivo — `execucoes/`, `evidencia/` e `arquivo/` — são
criadas quando o primeiro arquivo chega e não existem hoje. O conteúdo atual de `data/` são
os dez JSON e `saida/`.

### Scripts

Os quatro scripts leem o documento do protocolo e os JSON de `data/`; nenhum decide
conteúdo — conferem e derivam. Três invariantes valem para todos:

- **Uma fonte.** `src/protocolo.py --gerar` lê `docs/03_protocolo_estrategia_pesquisa.md` e
  grava os sete JSON. Alterado o documento, os derivados ficam defasados e todo consumidor
  recusa rodar até a regeração.
- **Duas assinaturas por JSON.** `fonte.sha256` detecta documento alterado sem regerar;
  `derivado.sha256` cobre o subconjunto derivado e detecta campo editado à mão. O que é
  autoral — o estatuto de validação em `descritores.json` e os metadados de conferência em
  `sementes.json` — pode ser editado livremente, e `--gerar` o preserva.
- **Nada se apaga por geração.** Termo ou semente retirado do protocolo fica com
  `no_protocolo=false` e é reportado por `--pendencias`, para decisão.
- **O identificador é a chave.** Os itens dos JSON são identificados pelo código do
  protocolo — `QGR`/`QERn`, `FCTn`, `STRn`, `EBn`, `CEn`, `BDn`, `SEn` —, e não por número
  de posição; a composição das expressões é dada em `STRn`.

`--conferir` reprova documento fora da forma esperada — seções, identificadores, camadas de
vocabulário, strings, composição das expressões, critérios, bases e distribuição do
conjunto-semente. `--conferir-dados` reprova JSON ausente, derivado defasado, campo
adulterado e divergência entre arquivos. `--autoteste` injeta defeitos numa cópia e exige
que as conferências os reprovem, inclusive a prova de que edição de campo autoral é
aprovada. `--pendencias` relata sem escrever. Os comandos estão no fluxo de trabalho, em M3.

## Fluxo de trabalho — RS Banyan

O RS Banyan organiza a revisão em **quatro módulos, catorze etapas e sessenta e três
passos**, sustentados por sete Instrumentos Operacionais. O **PRISMA** não conduz a
execução: é a diretriz de apresentação do relato. A sequência abaixo segue os módulos e as
etapas; os passos detalhados, com responsável e data, estão no IO 7.

| Módulo | Etapas | O que decide |
| --- | --- | --- |
| **M1 — Planejamento** | 5: objetivos; necessidade; instrumentos operacionais; equipe; cronograma | se a revisão deve e pode ser feita, com que equipe, instrumentos e prazo |
| **M2 — Questão de revisão** | 2: tópicos preliminares; delimitação do assunto | o que exatamente se pergunta e o que fica fora da pergunta |
| **M3 — Pesquisa bibliográfica** | 4: estratégias; localização dos estudos; seleção; extração | como se busca, o que entra no portfólio e o que se extrai de cada item |
| **M4 — Discussão e redação** | 3: interpretação; registro e validação; preparação textual e divulgação | o que os achados significam, como se relatam e onde se publicam |

**M1 e M2 correm em paralelo**, com o controle terminológico iniciado no primeiro mês. Cada
marco é de **passa ou não passa**: reprovado, a correção se faz na fonte, a geração se
refaz e a decisão se registra no Anexo A. Nenhuma etapa é suprimida por prazo.

### M1 — Planejamento (E1–E5)

Decide a **exequibilidade** da revisão.

1. **E1 — objetivos.** Fixa a questão do projeto e o objetivo geral, com um objetivo
   específico por questão secundária.
2. **E2 — necessidade.** Justifica a revisão, delimita o escopo e o contra-escopo e
   distribui os cinco problemas representacionais entre esta revisão e as autônomas.
3. **E3 — instrumentos operacionais.** Viabiliza os sete Instrumentos Operacionais, IO 1 a
   IO 7; neste pacote estão o IO 0, que organiza o planejamento, e o IO 1.
4. **E4 — equipe.** Define os papéis: ReT, RTG, VT, APB, Revisores 1 e 2 e RE.
5. **E5 — cronograma.** Compromete os marcos quinzenais e a data-limite dos revisores,
   anterior à execução das buscas definitivas.

**Fonte:** `docs/01_plano.md` (IO 0), seções 1 a 3; equipe e cronograma detalhados
nos IO 6 e IO 7, fora deste pacote. **Scripts:** nenhum — o produto é decisão registrada.

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
nenhum nesta etapa; a questão entra em `data/questoes.json` na primeira geração de M3/E1.
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
2. **Validação terminológica.** Consulta sistemática restrita ao TBCI, para o português, e
   ao UNESCO Thesaurus, para inglês e espanhol. O ERIC Thesaurus e o Brased são referência
   documental; a faceta de fatores situacionais é **termo livre por decisão**. Termo sem
   consulta registrada é termo livre e não pode ser apresentado como descritor autorizado.
3. **Strings por faceta.** Qualificação do vocabulário: substituição de palavra isolada pela
   forma composta, desdobramento da notação compacta e inclusão das formas morfológicas.
4. **As quatro expressões.** A de cobertura é a **única executada**; as outras três são
   subconjuntos estritos dela, calculados localmente em M3/E2.
5. **Critérios de elegibilidade.** Quatro critérios de inclusão e cinco de exclusão, com a
   regra única de inclusão — práticas **e/ou** fatores situacionais — e a regra de borda.
6. **Fontes.** Web of Science, Scopus, ERIC e BRAPCI, nessa ordem; acesso pelo Portal da
   CAPES com CAFe nas duas primeiras. A ausência de busca direta nos acervos especiais é
   limitação declarada, mitigada por backward search.
7. **Conjunto-semente.** Dez estudos, quinze incidências e distribuição 6/4/3/2 por base
   Scopus, WoS, ERIC e BRAPCI. É instrumento de aferição, não lista de incluídos.
8. **Ferramentas e registro de uso de IA.** Zotero para gestão e deduplicação, Rayyan para
   triagem cega e ASReview para priorização; o uso de IA é registrado ação a ação no LOG_IA,
   apêndice do IO 1.

```bash
# deriva os JSON do protocolo e confere documento, dados e guardas
python3 src/protocolo.py --gerar
python3 src/protocolo.py --conferir
python3 src/protocolo.py --conferir-dados
python3 src/protocolo.py --conferir --autoteste

# validação terminológica: sonda obrigatória antes de validar
python3 src/validar_termos.py --sonda
python3 src/validar_termos.py --exportar
python3 src/validar_termos.py --validar tbci
python3 src/validar_termos.py --validar unesco
python3 src/validar_termos.py --importar

# instrumento de aderência: guia e planilha por semente e por base
python3 src/gen_semente.py
```

**Arquivos.** A fonte é `docs/03_protocolo_estrategia_pesquisa.md`; `--gerar`
deriva os sete JSON de `data/` — `questoes.json`, `facetas.json`, `descritores.json`,
`strings.json`, `criterios.json`, `fontes.json` e `sementes.json` — e cria os auxiliares
`consultas.json` e `pendencias.json` só se ausentes. A validação grava o estatuto em
`descritores.json` e a resposta bruta em `data/evidencia/{tbci,unesco}/`; a planilha em
`data/saida/validacao/validacao_termologica.csv` é exportação, e as decisões voltam por
`--importar`. O conjunto-semente gera `data/saida/semente/Conjunto_Semente.md` e
`semente_aderencia.csv`.

**Garantias.** Cada JSON guarda o `sha256` do documento e o do próprio subconjunto derivado:
o primeiro detecta documento alterado sem regerar; o segundo, campo derivado editado à mão.
`--gerar` preserva o que é autoral — o estatuto de cada termo e a conferência de cada
semente — e não apaga termo ou semente retirado do protocolo: marca `no_protocolo=false`.
`--conferir` reprova o documento fora da forma; `--conferir-dados` reprova JSON defasado ou
adulterado; `--autoteste` injeta defeitos e exige que as conferências os reprovem.

**Condição de passagem:** viabilidade das strings e IO 1 validado por revisor expert.
Reprovado, volta-se ao vocabulário e registra-se a emenda no Anexo A.
Skills: `facetacao-e-termos-livres`, `validacao-vocabulario-controlado`,
`expressoes-de-busca` e `conjunto-semente`.

#### E2 — Localização dos estudos

Executa a busca e transforma a exportação em conjunto verificável.

1. **Sondagem de sintaxe.** Obrigatória na ERIC e na BRAPCI antes de qualquer execução; o
   procedimento e as ressalvas estão na ficha da base. Automação de interface só depois de
   conferidos os termos de uso, e a autenticação federada é feita pelo pesquisador.
2. **Execução.** Executa-se **a expressão de cobertura uma vez por base** — e não as
   quatro —, com o recorte temporal aplicado na busca na WoS, na Scopus e na BRAPCI e pelo
   filtro da página de resultados na ERIC. Na ERIC, a expressão se desdobra em duas
   consultas de campo único, unidas na derivação.
3. **Registro e exportação.** A exportação fica intacta em `data/execucoes/<base>/`; cada
   consulta é registrada com o retorno que a base exibiu.
4. **Derivação local.** As outras três são calculadas sobre a exportação da de cobertura, com
   deduplicação dentro da base — a segunda ocorrência é marcada em `duplicata_de`, e nada é
   apagado.
5. **Aderência.** Mede o recall contra o conjunto-semente; o denominador é o que cada base
   indexa, conferido à mão, e o limiar é **80% sobre a união das bases**.
6. **Fidelidade.** Executa as duas específicas diretamente na WoS e na Scopus e compara com a
   derivação; divergência acima de **10%** reprova o método.
7. **Coerência e cobertura.** Confere as quatro relações de continência entre as expressões —
   a geral contida em cada específica, cada específica contida na de cobertura — e a
   cobertura de campo da exportação. A conferência é condição necessária e não suficiente:
   o que garante a coerência é a construção — expressões uniformes e execução única da de
   cobertura —, não a verificação.
8. **Calibração da triagem assistida.** Antes do primeiro uso, o ASReview passa por estudo
   de viabilidade e calibração, com sensibilidade aferida em **95% ou mais**. A ferramenta
   ordena a fila; não decide inclusão.

```bash
# registra a consulta; a ERIC tem mais de um arquivo (eric_4a.ris, eric_4b.ris)
python3 src/derivar_expressoes.py --registrar wos <expressão> data/execucoes/wos/<arquivo>.ris --retorno 18432

# deriva as expressões não executadas, conta únicos e grava a ordem de triagem
python3 src/derivar_expressoes.py --derivar

# aderência ao conjunto-semente
python3 src/derivar_expressoes.py --aderencia

# fidelidade da derivação, exigida na WoS e na Scopus
python3 src/derivar_expressoes.py --fidelidade <expressão> data/execucoes/wos/<arquivo>.ris
```

**Arquivos.** `data/consultas.json` é o registro das execuções; `--derivar` lê o registro,
não a pasta de exportações. As saídas ficam em `data/saida/derivacao/`: `registros.csv`,
`io2_contagens.csv`, `ordem_triagem.csv` e um CSV de fidelidade por expressão conferida. A
aderência usa `data/sementes.json` e `data/saida/semente/semente_aderencia.csv`.

**Recusas e marcas.** `--registrar` confere o retorno declarado contra os registros do
arquivo e **recusa registrar quando divergem**, salvo justificativa explícita — o caso do
teto de 1.000 da BRAPCI. `--derivar` reconfere a contagem e para se o arquivo mudou. As
contagens do IO 2 usam os registros únicos, com o número bruto ao lado. O recorte temporal
é apenas conferido aqui, e a linha "fora" deve ser zero em todas as bases.

**Condição de passagem:** suficiência do portfólio — aderência de 80% ou mais e fidelidade
dentro de 10%. Fora disso, revisa-se o controle terminológico antes de prosseguir, com
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
   `data/saida/derivacao/ordem_triagem.csv` registra a ordem por pertinência e recência.
3. **2ª filtragem — título e resumo.** Aplica os critérios decidíveis sem o texto completo:
   recorte, idioma, tipo documental e exclusões temáticas manifestas, com kappa.
4. **3ª filtragem — texto completo.** Aplica integralmente o critério 5, com a regra de
   exceção e a regra de borda, e justifica cada exclusão. Dois revisores independentes, sem
   IA na decisão, com kappa. Divergência remanescente vai ao VT.
5. **Backward search.** Uma geração, apenas sobre os estudos incluídos. Revisões
   sistemáticas permanecem elegíveis, mas vão para **conjunto suplementar** com contagem
   própria.
6. **Registro do fluxo.** O IO 3 recebe o diagrama PRISMA com as exclusões justificadas e
   quantificadas em cada passagem.

**Arquivos e ferramentas.** `data/saida/derivacao/ordem_triagem.csv` ordena a 1ª filtragem;
Zotero, Rayyan e ASReview executam a etapa; o IO 3 é produzido fora deste pacote.
**Scripts:** nenhum — a decisão de inclusão é humana. Skills: `calibracao-da-triagem` e
`filtragens`.

**Condição de passagem:** conclusão das três filtragens, com kappa calculado nas três.

#### E4 — Extração de dados

Transforma cada estudo incluído em dado comparável.

1. **Fichamento.** Cada estudo incluído preenche o IO 4; o pré-preenchimento assistido por
   IA é conferido campo a campo no texto-fonte. As cinco categorias de Fink são o **esquema
   de codificação**, e não um enquadramento obrigatório: fator não previsto nelas é
   registrado em "outros fatores" e constitui achado.
2. **Glossário.** O IO 5 reúne as definições e as fontes de cada conceito, validadas pelo
   pesquisador.

**Arquivos:** IO 4 e IO 5, fora deste pacote. **Scripts:** nenhum — a extração é leitura.
Skill: `fichamento`.

**Condição de passagem:** conclusão dos fichamentos.

### M4 — Discussão e redação (E1–E3)

1. **E1 — interpretação do conhecimento.** Análise bibliométrica e de conteúdo; comparação
   dos artefatos por cobertura, granularidade e grau de formalização; formulação das lacunas
   de representação. A distribuição por comunidade de origem é, por si, achado. Skill:
   `sintese-e-lacunas`.
2. **E2 — registro e validação do conteúdo.** Redação do relatório com a lista do PRISMA
   respondida item a item, cada item classificado como aplicável sem adaptação, não
   aplicável com justificativa ou adaptado ao objeto. O fluxograma vem do IO 3; as
   limitações, das decisões registradas; a declaração de uso de IA, do LOG_IA. Skill:
   `relato-prisma`.
3. **E3 — preparação textual e divulgação.** Revisão de língua, tradução do resumo,
   normalização ABNT e submissão; toda referência é conferida na fonte. Skill:
   `conferir-referencia`.

**Arquivos:** relatório e apêndices, fora deste pacote; regras de uso de IA em
`docs/01_plano.md`, seção 8. **Scripts:** nenhum.

### Atividades transversais

- **Toda decisão que altere questão, facetas, critérios ou busca é emenda.** Altera-se o
  documento-fonte — o IO 0, o IO 1 ou a ficha da base — e, quando o dado é derivado,
  regera-se com `--gerar`; a decisão se registra no Anexo A,
  `docs/historico.md`. Não se edita JSON derivado nem planilha de saída. Skill:
  `registrar-decisao`.
- **Rastreabilidade.** Questão, objetivos, facetas, quadro terminológico, strings e
  critérios precisam concordar; `--conferir` e `--conferir-dados` são a trava, e
  `--autoteste` prova que as conferências reprovam. Skill: `rastreabilidade`.
- **Referências.** Nenhum dado bibliográfico se preenche de memória: confere-se na fonte e
  registra-se o estado da conferência. Skill: `conferir-referencia`.
- **Parecer externo.** Cada achado é conferido contra o texto corrente antes de aceito; o
  parecer é hipótese sobre o documento, não constatação. Skill: `parecer-sobre-protocolo`.
- **Pendências.** `python3 src/protocolo.py --pendencias` relata o que encontra nos
  artefatos, sem escrever; promover um achado a pendência registrada é decisão do
  pesquisador.

## Precedência

- O **IO 1** — `02_protocolo_informacoes_gerais.md` e `03_protocolo_estrategia_pesquisa.md` —
  prevalece sobre qualquer formulação feita em outro documento; o IO 0 remete a ele.
- O **Anexo A** é o único lugar do histórico.
- A data **oficial** de execução consta **exclusivamente do IO 7**, que não integra este
  pacote; `data/consultas.json` registra data e hora operacionais de cada consulta, como
  rastro técnico do registro.

## Convenções

- **Português do Brasil**, redação formal, objetiva e enxuta.
- Referências normalizadas pela **ABNT NBR 6023**, cada uma com o seu estado de conferência.
- Datas de execução no **IO 7**; histórico no **Anexo A**.
- Nomeação dos arquivos de estudo: `Ano_DuasPrimeirasPalavras_TIPO_UltimoSobrenomeAutor`,
  com sufixo `_FICHA` para fichamentos.

## Autoria e uso de IA

**Junilson Pereira Souza** — responsabilidade técnica.

A assistência de inteligência artificial é declarada e registrada ação a ação no LOG_IA,
apêndice do IO 1. A IA **não é autora**, conforme ICMJE e COPE. As regras de uso estão em
`docs/01_plano.md`, seção 8.
