# Proposal

## Why

O protocolo passou a declarar, em tabelas próprias, o que até aqui só o `config.toml` sabia:
a sigla e o modo de cada instrumento com os idiomas e as facetas que cobre, a sigla e a ficha
de cada base, as bases em que cada semente está indexada e os idiomas do quadro
terminológico. Manter as mesmas informações nos dois lugares cria duas fontes que podem
divergir em silêncio; e a leitura atual já reprova o protocolo vigente ("esperava uma tabela
por faceta, achei []"), porque o formato das tabelas mudou.

## What Changes

- **BREAKING** Saem do `config.toml` `[padroes.composicao]`, `[cores]`, `[fichas.*]`,
  `[instrumentos.*]` e `idiomas`. Esses parâmetros passam a ser **estruturais**: lidos só do
  protocolo (ou da ficha, no caso da forma de execução), sem padrão; ausência ou valor
  inválido reprova a leitura, nomeando a tabela, a linha e o campo.
- Facetas: a linha `Faceta n (FCTn): nome (âncora obrigatória k)` deixa de ter cor; a âncora
  vem entre parênteses. O leitor deixa de extrair e de exigir cor.
- Instrumentos: lidos da tabela `Sigla | Instrumento | Modo | Caminho | Idiomas | FCTs`.
  `Modo` admite `Manual` ou `Automático`; o cliente automático é escolhido pela sigla, e
  `Automático` sem cliente correspondente reprova. `Caminho` é a referência do instrumento,
  não o endereço da API, que continua no cliente.
- Quadro terminológico: `| FCTn | pt | en | es |`; o idioma de cada coluna é o nome no
  cabeçalho, não a posição. Os idiomas do projeto passam a ser os do cabeçalho, iguais nas
  tabelas de todas as facetas.
- Bases: lidas da tabela "Bases de dados" (`ID Base`, `Sigla`, `Nome da base`). A ficha de
  cada base é localizada pela sigla, por um padrão de caminho no `config.toml`
  (`docs/busca_base_{sigla}.md`); as quatro fichas são renomeadas para esse padrão. A sigla é
  também a chave de linha de comando de `derivar_expressoes.py`.
- Conjunto-semente: lido da tabela `ID Semente | Semente | Bases`; cada base citada tem de
  ser sigla da tabela de bases, com grafia exata. Saem o mapa por estudo e a conferência
  prosa × mapa da distribuição, porque o protocolo não traz mais essas declarações.
- Fichas: a forma de execução (`única` ou `particionada`) passa a ser declarada na própria
  ficha, numa linha fixa; ausência reprova a conferência daquela base. O emoji de faceta
  deixa de ser lido; a forma curada reconhece a faceta só por `FCTn`.
- Autoteste: os casos de precedência desses parâmetros dão lugar a casos de ausência e de
  valor inválido, cada um demonstrando que reprova.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-do-protocolo`: a regra "todo parâmetro tem padrão no `config.toml`" ganha a classe
  dos parâmetros estruturais, sem padrão; novas leituras de facetas, quadro, bases e
  sementes; sai a conferência da distribuição em prosa.
- `validacao-terminologica`: instrumentos lidos de tabela do protocolo (sigla, modo,
  caminho, idiomas, facetas), sem mapa na configuração.
- `derivacao-das-expressoes`: as bases vêm do protocolo, não de `[fichas]`.
- `cobertura-por-base`: a ficha é localizada pelo protocolo e declara a própria forma de
  execução; o emoji deixa de identificar a faceta.

## Impact

- Código: `src/protocolo.py` (esquema da configuração, leitores de facetas, instrumentos,
  quadro, bases e sementes, `IDIOMAS` e `FICHAS` deixam de ser constantes de módulo,
  `--mostrar`, `--conferir`, `--autoteste`); `src/validar_termos.py` (modo, sigla e idiomas
  do instrumento; nomes dos clientes); `src/derivar_expressoes.py` (bases); `src/gen_semente.py`
  (bases).
- Configuração: `config.toml` perde cinco blocos e ganha o padrão de caminho da ficha.
- Documentos (pré-requisito da execução): as fichas passam a `docs/busca_base_<sigla>.md`, com
  as referências atualizadas (`README.md`, `config.toml`, `data/pendencias.json`, skill
  `busca-nas-bases`); siglas da tabela de bases na coluna "Bases" das sementes; linha de forma
  de execução em cada ficha.
- Saídas: as siglas das bases passam de `WoS`, `BRAPCI`… para `wos`, `brapci`… nos relatórios
  e nos arquivos de contagem; a sigla do instrumento na planilha de validação passa a ser a
  do protocolo (`tbci`, `unesco`, `eric`, `brased`). Não há planilha gravada hoje
  (`data/validacao_termologica.csv` ausente), logo não há dado a migrar.
