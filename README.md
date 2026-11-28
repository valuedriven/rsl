# RSL-01 — Representação do conhecimento sobre práticas educacionais e seus fatores situacionais

Revisão sistemática de literatura sobre modelos conceituais, ontologias e outros sistemas de
organização do conhecimento que representam formalmente práticas do processo de
ensino-aprendizagem e os fatores situacionais que condicionam a sua aplicação.

Conduzida pelo **RS Banyan**, com o **PRISMA** como diretriz de apresentação.

Este arquivo é a **porta de entrada** do repositório: como executar, onde fica cada coisa e
quem a escreve. **O que se faz, em que ordem e com que apoio** — módulos, etapas, passos,
comandos com os parâmetros e índices da busca — está em
[`docs/procedimentos.md`](docs/procedimentos.md). Nenhum dos dois repete o conteúdo dos
documentos que indexam.

## Como executar

Toda operação passa por um ponto de entrada único, a partir da raiz do projeto, com
**Python 3.11+** e só a biblioteca padrão:

```bash
PYTHONPATH=src python3 -m rsl <subcomando>     # ou, de dentro de src/: python3 -m rsl …
python3 -m rsl                                 # sem subcomando: a ajuda, com os códigos
python3 -m rsl <subcomando> -h                 # parâmetros de cada subcomando
```

Nos documentos, os comandos aparecem como `python3 -m rsl …`, com `src/` no caminho de
importação. A configuração é `config.toml`, na raiz; a variável de ambiente `RSL_CONFIG`
aponta outro arquivo, para ensaio e autoteste. O que cada chave significa está nos
comentários do próprio `config.toml`; a forma que o leitor exige do protocolo, dos procedimentos de busca e
do arquivo de sementes, em `python3 -m rsl documentos gramatica`; o valor em uso de cada parâmetro e a
sua origem, em `python3 -m rsl configuracao mostrar`. O mapeamento de cada passo do guia às skills e aos
comandos, conferido contra as skills e o parser, sai de `python3 -m rsl catalogo gerar`
(ensaio; `--gravar` regrava o catálogo).

Os dados das sementes ficam na coleção do Zotero de `[zotero]` (biblioteca e coleção), e
só `sementes copiar` e `sementes completar` acessam o Zotero. A via de acesso, para ler e para
escrever, é a de `[zotero] acesso`: `local` (o Zotero aberto na máquina do pesquisador, com o
acesso local habilitado nas preferências, sem chave) ou `web` (a API web, com a chave).
Nenhum subcomando troca de via sozinho: pedido recusado numa via sai com FONTE_EXTERNA, sem
repetir pela outra. Na via local, o Zotero fechado também sai com FONTE_EXTERNA, e a mensagem
diz que ele tem de estar aberto com o acesso local habilitado.

A chave da API web só se exige na via `web`. Ela é emitida pelo pesquisador, com escrita só
na biblioteca de grupo, e fica fora do controle de versão: na variável de ambiente
`ZOTERO_API_KEY` ou, na falta dela, na linha `ZOTERO_API_KEY=<chave>` do `.env` da raiz. O
`.env` tem de estar no `.gitignore`; se não estiver, a leitura é recusada com CONFIGURACAO. A
chave nunca se grava em arquivo versionado nem se imprime, e em relato aparecem só os quatro
últimos caracteres. Na via `web`, sem a chave, esses dois subcomandos saem com CONFIGURACAO e
os demais funcionam, porque leem a cópia da coleção em `[dados] zotero`, sem rede. Antes de
`sementes copiar` pela via `web`, sincronizar o Zotero: a API web não vê edição ainda não
sincronizada.

A premissa é manter a mesma via em toda a sessão: as versões que a cópia registra só valem na
via que a leu. `sementes completar` recusa com DADOS a cópia lida por outra via (a cópia sem
via registrada conta como `web`), e `sementes copiar` avisa quando a via mudou desde a cópia
anterior.

Na via `local`, a leitura dispensa chave, mas a escrita exige duas credenciais da API local:
a chave da API local (`ZOTERO_LOCAL_API_KEY`) e o identificador do servidor
(`ZOTERO_SERVER_ID`). Elas ficam onde fica a chave web (variável de ambiente ou linha do
`.env` listado no `.gitignore`), com as mesmas guardas, e só se leem no primeiro pedido de
escrita. Sem elas, a escrita sai com CONFIGURACAO antes de qualquer pedido. O pesquisador as
obtém no Zotero da máquina, aberto e com o acesso local habilitado:

```bash
# 1. Identificador do servidor: ler o cabeçalho Zotero-Server-ID da resposta.
curl -i http://localhost:23119/api/

# 2. Chave da API local: ler o parâmetro `key` do JSON da resposta.
curl -d '{ "appName": "<nome da aplicação>" }' -H "Content-Type: application/json" \
     -H "Zotero-Server-ID: <Zotero-Server-ID>" -X POST http://localhost:23119/api/local/authorize
```

Os dois valores vão para o `.env` (`ZOTERO_SERVER_ID=…` e `ZOTERO_LOCAL_API_KEY=…`), nunca
para arquivo versionado nem para a conversa com o agente.

Os registros recuperados nas bases ficam na coleção das buscas, cujo nome é
`[zotero] search_collection`, na raiz da biblioteca de `[zotero] library` (sem ela, na de
`[zotero] biblioteca`). A biblioteca vale como `groups/<id>` ou pelo endereço da biblioteca
de grupo no site. Dentro da coleção, há uma subcoleção por base, nomeada pela sigla, e,
dentro dela, uma coleção por execução, cujo nome começa pelo identificador da execução. As
duas chaves não têm padrão e entram no `config.toml` depois de o pesquisador criar a
coleção. O subcomando que precisa da coleção e não tem `search_collection` sai com
CONFIGURACAO; a coleção ausente na raiz, ou duas com o mesmo nome, saem com DADOS. Os subcomandos de análise e de conferência não consultam o Zotero: leem a
exportação de cada execução do cache em `[dados] execucoes` ou, na execução registrada só
com o caminho do arquivo, desse caminho. Exportação ausente no disco sai com DADOS.

### Códigos de saída

Todo subcomando termina com um destes códigos, e toda saída diferente de OK termina com uma
linha que nomeia o código:

| Código | Nome | Quando |
| --- | --- | --- |
| 0 | OK | a operação terminou e nada reprovou |
| 1 | REPROVADO | uma conferência ou condição de aceite reprovou o conteúdo |
| 2 | USO | argumento ou subcomando inválido |
| 3 | CONFIGURACAO | `config.toml` ausente, inválido ou incompleto, ou protocolo inexistente |
| 4 | PROTOCOLO_ILEGIVEL | protocolo ou procedimento de busca fora da gramática que o leitor exige |
| 5 | DADOS | arquivo alimentado, exportação ou arquivo de entrada ausente ou ilegível |
| 6 | PARCIAL | autoteste sem falha, com casos não executados |
| 7 | FONTE_EXTERNA | fonte externa com erro, bloqueio, captcha ou limite excedido |

Quando mais de uma condição ocorre, vale a mais grave: CONFIGURACAO, PROTOCOLO_ILEGIVEL,
DADOS, FONTE_EXTERNA, REPROVADO, PARCIAL.

## Mapa

Cada caminho aparece uma vez. Caminho marcado *sob demanda* é criado quando o primeiro
arquivo chega. Os caminhos de `data/` vêm de `[dados]` e `[saidas]` do `config.toml`, e os
documentos de sementes e procedimentos de busca, de `[documentos]`; os documentos citam esses arquivos pela
chave, não pelo caminho.

| Caminho | O que contém | Quem escreve |
| --- | --- | --- |
| `docs/01_plano.md` | plano: contexto, objetivos, base metodológica, escopo, cronograma, recursos, custos, qualidade, riscos e uso de IA | pesquisador |
| `docs/02_protocolo_informacoes_gerais.md` | protocolo, informações gerais: tópicos preliminares, delimitação do assunto e objeto | pesquisador |
| `docs/03_protocolo_estrategia_pesquisa.md` (`protocolo`) | protocolo, estratégias de pesquisa: questão, facetas, controle terminológico, strings, expressões, critérios, fontes, conjunto-semente, procedimentos, instrumentos e ferramentas; fonte única dos parâmetros que declara | pesquisador; a tabela "Strings de busca por faceta", `strings gerar --gravar`, a partir do quadro terminológico |
| `docs/conjunto_semente.toml` (`[documentos] sementes`) | conjunto-semente, uma tabela `[[sementes]]` por estudo, com o controle e o juízo do pesquisador; os dados de cada semente ficam no Zotero, ligados pelo DOI | pesquisador; nenhum subcomando grava |
| `docs/procedimentos/<sigla>/` (`[documentos] procedimento_fonte`) | fonte do procedimento de busca de cada base: `procedimento.toml` (sintaxe e roteiro de sondagens, critérios, declaração de cobertura com `plural` e `teto`, composição, execução, regras de montagem, sementes, ressalvas) e fragmentos de prosa de nome fixo; esquema em `documentos gramatica` | pesquisador e agente, a pedido; base nova começa por `procedimentos iniciar` |
| `docs/procedimentos_busca_<sigla>.md` (`[documentos] procedimento`) | procedimento de busca de cada base, inteiro: sintaxe e roteiro de sondagens, critérios, strings, expressões, execução, conjunto-semente e ressalvas; saída de geração, não se edita à mão | `procedimentos gerar --gravar`, a partir da fonte, do protocolo, do arquivo de sementes e do de exceções |
| `docs/flexoes.toml` (`[documentos] flexoes`) | exceções de flexão de número dos termos das STR, por idioma (irregular, não contável, vetada), cada uma com a origem | pesquisador; agente, a pedido, com revisão antes de gravar |
| `docs/parametros_complementares.md` | instrumento de extração e síntese: grupos de extração, cobertura conceitual, granularidade e grau de formalização | pesquisador |
| `docs/procedimentos.md` | guia de procedimentos: módulos, etapas e passos, com fonte, script, skill e apoio; fonte do catálogo de apoio | pesquisador e agente, a pedido |
| `docs/catalogo_de_apoio.md` | catálogo de apoio: skills e comandos por passo, por skill e por comando, e cobertura por etapa; saída de geração, não se edita à mão | `catalogo gerar --gravar`, a partir do guia de procedimentos |
| `data/historico.md` | decisões arquiteturais, inclusive emendas | pesquisador; agente, a pedido |
| `data/pendencias.json` | ações ainda a executar, `PDnn` | pesquisador; agente, a pedido |
| `data/registro_execucao.json` (`[dados] registro`) — *sob demanda* | resultados das consultas nas bases, por base: execuções (`execucoes`) e sondagens de sintaxe (`sondagens`) | pesquisador, `busca registrar` e `sondagens registrar` |
| `data/execucoes/<base>/` — *sob demanda* | exportações intactas das bases, das execuções registradas só com o caminho do arquivo (campo `arquivo` do registro), lidas desse caminho até migrarem para o Zotero | pesquisador |
| `tmp/` (`[dados] temporarios`) — *sob demanda* | cache do que se obtém do Zotero e saídas regeneráveis; fora do controle de versão (listada no `.gitignore`, ou a configuração reprova) e regenerável a partir do Zotero | subcomandos que obtêm do Zotero |
| `tmp/execucoes/<sigla>/<identificador>.ris` (`[dados] execucoes`) — *sob demanda* | cache da exportação de cada execução que tem coleção no Zotero, obtida dela em RIS; tem de ficar dentro de `[dados] temporarios`, ou a configuração reprova | obtenção do Zotero |
| `data/validacao_terminologica.toml` (`[dados] validacao`) — *sob demanda* | decisões do ReT, uma tabela `[[decisoes]]` por termo, idioma e instrumento do protocolo; a decisão de termo retirado é removida na sincronização | pesquisador, só os campos `decisao_ReT`, `justificativa_ReT` e `data_decisao`; `termos exportar` e `termos importar` normalizam o arquivo |
| `data/consulta_terminologica.json` (`[dados] consulta_terminologica`) — *sob demanda* | resultado técnico: uma linha por chave consultada, com a resposta do instrumento e o caminho da evidência; a ausência significa "aguardando consulta" | `termos validar`, `termos exportar` e `termos importar`; não se edita à mão |
| `data/evidencia/<instrumento>/` (`[dados] evidencia`) — *sob demanda* | resposta bruta da consulta vigente de cada termo do protocolo, `<16 hex>.json`; a de termo retirado é expurgada | `termos validar`; expurgo por `termos exportar` e `termos importar` |
| `data/evidencia/referencias/` | resposta bruta da conferência de referências, `SEn_…` pelo `id` da semente | agente, a pedido |
| `data/evidencia/openalex/` | resposta bruta da OpenAlex por semente, `<DOI normalizado>.json`, nomeada pelo DOI e não pelo `id` | `sementes metadados` |
| `data/evidencia/zotero/` | pontos de restauração da coleção de sementes, gravados antes de cada escrita no Zotero | `sementes completar --gravar`; agente, a pedido |
| `data/zotero_sementes.json` (`[dados] zotero`) | cópia da coleção de sementes do Zotero: resposta bruta, lida pela via de `[zotero] acesso`, com biblioteca, coleção, versão da biblioteca, via (nas cópias gravadas a partir do registro da via) e data e hora da leitura; os comandos de análise a leem em vez de consultar o Zotero | `sementes copiar`; `sementes completar --gravar` |
| `data/registros.csv`, `data/contagens_busca.csv`, `data/ordem_triagem.csv` (`[saidas]`) — *sob demanda* | registros com pertinência e marcas, contagens por base e expressão, ordem da 1ª filtragem | `busca derivar` |
| `data/fidelidade_<base>_<expressao>.csv` (`[saidas] fidelidade`) — *sob demanda* | divergências entre derivação e execução direta | `conferencia fidelidade` |
| `data/sensibilidade_<base>.csv` (`[saidas] sensibilidade`) — *sob demanda* | perda da sonda e amostra a classificar; preserva a coluna `elegivel` | `conferencia sensibilidade`; classificação pelo pesquisador |
| `data/arquivo/` — *sob demanda* | cópias anteriores, com `SHA256` | migrações |
| `config.toml` | configuração dos scripts | pesquisador; nenhum subcomando grava |
| `src/rsl/` | pacote de execução | — |
| `openspec/specs/` | requisitos dos scripts | — |
| `.agents/skills/` | competências metodológicas e operacionais do agente | — |
| `AGENTS.md` | contrato de trabalho do agente | — |

O que é **derivado do documento não vira arquivo**: questão, facetas, instrumentos,
strings, expressões, critérios e fontes são lidos do protocolo a cada execução, e a forma de
cada base, da fonte do procedimento de busca. Em `data/` fica o que alguém alimenta e o que os subcomandos gravam.
Os demais instrumentos do RS Banyan e o portfólio não integram este repositório.

### Três registros, três finalidades

| Registro | Guarda | Não guarda |
| --- | --- | --- |
| `data/historico.md` | só **decisões arquiteturais** da revisão — questão, escopo, critérios, método, estratégia de busca e emendas do protocolo —, em entrada curta: data, decisão, alcance e fundamento | decisão de instrumento, de ferramenta ou de redação; curadoria e manutenção de artefatos; correção de defeito; ação por fazer; resultado de consulta ou de sondagem, ainda que confirme ou derrube uma regra do procedimento de busca, quando nenhuma expressão muda; constatação de estado — que decisões anteriores já estão aplicadas, que uma etapa terminou, que nada falta —; encerramento de pendência sem decisão arquitetural nova; contagem — de termos, de sementes, de caracteres, de casos — e resultado de conferência ou de autoteste |
| `data/pendencias.json` | **ações ainda a executar**, e só elas, com `id`, `origem`, o que bloqueia, ação sugerida e responsável | ação concluída ou descartada; decisão; resultado de consulta |
| `data/registro_execucao.json` | **resultados da execução das consultas** nas bases — sondagens de sintaxe (`bases.BDn.sondagens`, por `sondagens registrar`), retornos, exportações e conferências | decisão; ação por fazer |

A cópia da coleção do Zotero (`[dados] zotero`) e as respostas da OpenAlex
(`data/evidencia/openalex/`) não são registro de decisão nem de execução das buscas: são dado
de semente lido de fonte externa, versionado para que os comandos funcionem sem rede e o
resultado se reproduza. Nenhum dos três registros os transcreve.

- **Nenhum artefato guarda registro histórico** em cabeçalho ou comentário (quem aprovou,
  quando, o que se retirou): o artefato traz só o conteúdo vigente.
- Pendência resolvida ou descartada **sai** de `data/pendencias.json`; não se arquiva. O que
  a encerrou vai ao seu registro antes da exclusão: a decisão arquitetural, inclusive a de
  descartar, ao histórico, que cita o `id`; o resultado de consulta ou de sondagem, ao registro
  de execução e à fonte do procedimento de busca. Encerramento que não decide nada de
  arquitetura — a sondagem respondeu, a constatação foi feita, a ação foi executada — **não
  gera entrada no histórico**: a exclusão da pendência e o controle de versão bastam. O `id` de
  pendência excluída não se reutiliza.
- A pendência remete à sua `origem` (fonte do procedimento de busca, protocolo, plano, comando) em vez de copiar o
  conteúdo dela.
- O histórico **não transcreve contagem**. Número se calcula do artefato quando se precisa
  dele (`configuracao mostrar`, `documentos conferir`, `projeto autoteste`), e o transcrito diverge na alteração seguinte. A
  entrada nomeia o que mudou — os termos, as sementes, os critérios — e o valor de
  parâmetro decidido (limiar, teto, recorte), não o tamanho do que mudou. O resultado das
  conferências vai ao relato da change ou da tarefa, não ao histórico.

## Precedência

- **Uma fonte por dado.** Vocabulário, expressões, critérios e os parâmetros que declara vêm
  do protocolo; a forma da busca, da fonte do procedimento de busca da base; as exceções de
  flexão, do arquivo de exceções; o conjunto-semente, do arquivo de sementes; o resto, do
  `config.toml`. Não há cópia intermediária nem valor de parâmetro no
  código.
- O **protocolo** — `docs/02_protocolo_informacoes_gerais.md` e
  `docs/03_protocolo_estrategia_pesquisa.md` — prevalece sobre qualquer formulação feita em
  outro documento; o plano remete a ele.
- Sobre o `config.toml`, o protocolo prevalece em todo parâmetro que declara; o padrão vale
  só quando o protocolo não o declara, e trecho presente e ilegível reprova, sem cair no
  padrão. Os parâmetros estruturais só existem no protocolo e no arquivo de sementes.
- O **histórico** é o único lugar das decisões; `data/pendencias.json`, das ações por
  fazer; `data/registro_execucao.json`, dos resultados das consultas nas bases.
- A data **oficial** de execução consta **exclusivamente do cronograma**, que não integra
  este repositório; `data/registro_execucao.json` registra data e hora operacionais, como
  rastro técnico.
- Altera-se a fonte, não a saída: as planilhas e CSVs gravados pelos subcomandos se
  regeneram. Os registros da validação não são saída de geração: o arquivo de decisões é
  fonte editada pelo pesquisador, e o resultado técnico e a evidência são registro da
  consulta, escritos só pelo script.
- A sincronização dos registros da validação parte sempre das chaves do protocolo:
  `termos exportar` e `termos importar` removem decisão, linha técnica e evidência de termo
  retirado, sem guardar histórico de termos. `documentos conferir` reprova enquanto houver
  decisão de chave fora do protocolo.
- A tabela **"Strings de busca por faceta"** do protocolo é saída de geração: cada STR é a
  união dos termos do quadro terminológico da faceta, menos os subsumidos. Altera-se o
  quadro, e a ordem é quadro → `strings gerar` (ensaio) → `strings gerar --gravar` →
  fonte do procedimento → `procedimentos gerar` (ensaio, revisado) → `procedimentos gerar
  --gravar` → `documentos conferir`. STR editada à mão, ou defasada do quadro, reprova em
  `documentos conferir`.
- O **procedimento de busca** de cada base é saída de geração: altera-se a fonte da base
  (`docs/procedimentos/<sigla>/`), o arquivo de exceções ou o de sementes, e regenera-se.
  Procedimento editado à mão, ou defasado da fonte, reprova em `documentos conferir`. O
  resultado de uma sondagem se registra por `sondagens registrar`, que não altera a fonte: a
  mudança que ele imprime aplica-se na fonte, e regenera-se.
- O **catálogo de apoio** é saída de geração do guia de procedimentos. Altera-se o guia —
  ou cria-se, renomeia-se ou retira-se uma skill ou um comando —, e a ordem é guia →
  `catalogo gerar` (ensaio e conferência) → `catalogo gerar --gravar`. Catálogo editado à
  mão, ou defasado do guia, reprova em `catalogo gerar`.
- A **cópia da coleção de sementes** (`[dados] zotero`) é saída de leitura do Zotero: o dado
  se corrige no Zotero, e a ordem é Zotero (sincronizado) → `sementes copiar`, que relata o
  acrescentado, o retirado e o alterado antes de gravar. Cópia editada à mão some na leitura
  seguinte.

## Convenções

- **Português do Brasil**, redação formal, objetiva e enxuta.
- **O identificador é a chave.** Tudo se identifica pelo código do protocolo — questões,
  facetas, strings, expressões, critérios, bases e sementes —, e não por posição.
- Referências normalizadas pela **ABNT NBR 6023**, cada uma com o seu estado de conferência.
- Datas de execução no **cronograma**; decisões em `data/historico.md`.
- Nomeação dos arquivos de estudo: `Ano_DuasPrimeirasPalavras_TIPO_UltimoSobrenomeAutor`,
  com sufixo `_FICHA` para fichamentos.
- Arquivos gravados pelos subcomandos: `snake_case`, em português e sem acento, com o
  substantivo do conteúdo e, quando há um por chave, a chave em minúsculas
  (`fidelidade_wos_eb2.csv`, `sensibilidade_wos.csv`).

## Uso de IA

A assistência de inteligência artificial é declarada e registrada ação a ação no LOG_IA,
apêndice do protocolo. A IA **não é autora**, conforme ICMJE e COPE. As regras de uso estão em
`docs/01_plano.md`, seção 8.
