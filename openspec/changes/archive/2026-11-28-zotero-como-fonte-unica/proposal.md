# Proposal

## Why

O Zotero passa a ser a fonte única das referências: sementes e registros recuperados nas
bases. Hoje as exportações das bases ficam em disco, fora do git (`*.ris` no `.gitignore`),
mas o registro de execução aponta para elas, e a conferência dos dados reprova quando um
arquivo registrado está ausente. Quem clona o repositório não reproduz nem confere a busca.
Esta change cria a fundação de que as changes 2, 3, 5 e 6 dependem: o acesso ao Zotero, a
organização das coleções, o identificador da execução e o cache local regenerável.

## What Changes

- Cliente do Zotero único, com via de acesso parametrizável na configuração
  (`[zotero] acesso = "local" | "web"`), para leitura e escrita. A API local do Zotero 10
  passa a ser opção de escrita. A chave da API web continua fora do controle de versão.
- Organização das coleções da revisão no Zotero: sementes, e buscas por base e por
  execução. O nome de cada coleção de execução carrega o identificador da execução.
- Identificador único da execução calculado por hash. O objeto do hash (os bytes da
  exportação ou o conjunto ordenado de identificadores dos registros) decide-se no design,
  depois de conferir se a exportação de cada base embute data.
- Pasta `tmp/` na raiz, no `.gitignore`, para cache e saídas regeneráveis. Nenhum arquivo
  temporário se grava em `data/`.
- Ponto único de obtenção das exportações registradas (hoje `caminho_do_arquivo` em
  `src/rsl/busca/registro.py`): obtém do Zotero e guarda em `tmp/`. Os consumidores
  continuam funcionando sem mudança de interface.
- Consumidor imediato: `sementes copiar` migra do cliente atual da API web para o cliente
  novo.
- **BREAKING**: `[dados] execucoes` deixa de apontar pasta versionada. A remoção de
  `data/execucoes` e a migração dos RIS atuais ficam na change `fluxo-da-execucao-de-busca`.

Sondagem inicial, antes do design: conferir a escrita pela API local do Zotero 10.0.8 (a
versão instalada) e a exportação em RIS pelas duas vias. A conferência escreve na biblioteca
do pesquisador e só roda com autorização dele, numa coleção de teste.

Fora do escopo: o fluxo das sementes (change 2), a execução e a deduplicação (change 3), as
sondagens (change 5) e as análises (change 6). Esta change não gera entrada no
`data/historico.md`, porque é decisão de ferramenta.

## Capabilities

### New Capabilities
- `acesso-ao-zotero`: via de acesso parametrizável (local ou web), organização das coleções
  da revisão, identificador da execução e cache regenerável em `tmp/`.

### Modified Capabilities
- `derivacao-das-expressoes`: o leitor de RIS lê pelos mesmos campos o original da base e a
  reexportação do Zotero (BOM, `A1`, `C3`, primeiro `DO`, tipo canônico), por decisão do
  pesquisador depois da sondagem 1.4.
- `metadados-das-sementes`: a cópia da coleção passa a ser lida pelo cliente parametrizável,
  e a chave da API web só é exigida quando a via é `web`. A mudança da cópia para cache em
  `tmp/` fica na change `fluxo-das-sementes`, que já a declara. O requisito "Comandos de
  análise não consultam o Zotero" continua como está; a mesma regra, para as exportações,
  entra em `acesso-ao-zotero`.

As chaves novas de configuração (`[zotero] acesso`, `[zotero] library`,
`[zotero] search_collection`, `[dados] temporarios`) se especificam em `acesso-ao-zotero`. Nenhum subcomando novo entra
nesta change: o comando que obtém as exportações do Zotero é da change
`fluxo-da-execucao-de-busca`. Por isso `interface-de-comando` e `leitura-do-protocolo` não
mudam.

## Impact

- Código: `src/rsl/zotero.py`, `src/rsl/config.py`, `src/rsl/contexto.py`,
  `src/rsl/busca/registro.py`, autotestes de Zotero e de configuração.
- Configuração: `config.toml` (`[zotero]`, `[dados]`, `[saidas]`), `.gitignore`.
- Documentação: mapa de `data/` no `README.md`.
- Sistema externo: biblioteca do grupo no Zotero (coleções novas).
