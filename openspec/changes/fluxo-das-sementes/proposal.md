# Proposal

## Why

Com o Zotero como fonte única (change `zotero-como-fonte-unica`), a cópia versionada da
coleção de sementes e parte da evidência bruta delas passam a ser redundantes. O fluxo de
gestão das sementes acumula arquivos de apoio (cópia, respostas da OpenAlex e do Crossref,
conferência de referências, pontos de restauração) que o pesquisador não lê e que o
repositório versiona.

## What Changes

- `data/zotero_sementes.json` deixa de ser versionado e vira cache em `tmp/`, obtido pelo
  cliente parametrizável.
- `docs/conjunto_semente.toml` continua como o arquivo do juízo do pesquisador (DOI, bases,
  alinhamento das facetas, verificação, nota). Revisá-lo para eliminar informação excessiva.
- Reavaliar cada subpasta de evidência das sementes:
  - `data/evidencia/openalex/` e `data/evidencia/crossref/`: cache para reproduzir, lido por
    `sementes metadados` e `sementes completar`;
  - `data/evidencia/referencias/`: prova da conferência de referências;
  - `data/evidencia/zotero/`: pontos de restauração antes de cada escrita, possivelmente
    redundantes se a escrita local do Zotero 10 oferecer meio de desfazer.
- Expurgar o que não sustenta a informação vigente.
- Revisar a skill `definir-conjunto-semente` e o mapa do `README.md`.

Fora do escopo: o cliente do Zotero (change 1). Esta change não gera entrada no
`data/historico.md`.

Depende de: `zotero-como-fonte-unica`.

## Capabilities

### New Capabilities
<!-- nenhuma -->

### Modified Capabilities
- `metadados-das-sementes`: cópia da coleção como cache; destino e permanência das
  respostas da OpenAlex e do Crossref; pontos de restauração.
- `leitura-do-protocolo`: "Semente retirada não deixa resto na evidência" e a junção com o
  Zotero, conforme o destino da evidência.

## Impact

- Código: `src/rsl/sementes.py`, `src/rsl/metadados.py`, `src/rsl/zotero.py`,
  `src/rsl/dados.py` (`problemas_evidencia`), autotestes de sementes e de Zotero.
- Dados: `data/zotero_sementes.json`, `data/evidencia/{openalex,crossref,referencias,zotero}/`.
- Skill: `.agents/skills/definir-conjunto-semente/`.
- Documentação: `README.md`, `docs/catalogo_de_apoio.md`.
