# Proposta — guia de procedimentos em módulos, etapas e passos

## Why

O `README.md` (558 linhas) mistura mapa do repositório, configuração, contrato dos scripts e
uma narrativa do fluxo que repete o plano, o protocolo, o `config.toml`, as specs e a ajuda
da CLI — inclusive valores do protocolo (fórmula de EB4, faixa CE1–CE9) que divergem na
emenda seguinte. Falta, ao mesmo tempo, o que o pesquisador precisa para operar: em que
passo do RS Banyan está cada ação e qual script ou skill a apoia, com os parâmetros reais.
Os parâmetros hoje documentados estão incompletos (`termos validar` sem `todos` e
`--faceta`; `busca registrar` sem `--data-hora` e `--justificar`; `busca sensibilidade` com
a base apresentada como obrigatória).

## What Changes

- **Novo `docs/procedimentos.md`**: o protocolo organizado nos 4 módulos e 14 etapas do RS
  Banyan, com os 63 passos na ordem da estrutura fornecida pelo pesquisador. Cada passo é
  uma linha curta, verbo no infinitivo + objeto, **sem numeração e sem o termo "passo"**,
  com a remissão ao script (`python3 -m rsl …`) e/ou à skill que o apoia, quando houver, e
  à seção do documento-fonte onde a decisão está.
- Onde a prática do projeto adapta o passo do modelo, o passo traz a adaptação por
  remissão ao documento que a decide (plano ou protocolo), sem copiar o conteúdo.
- **M3/E2 detalha os índices** gerados a partir da execução das expressões — automáticos e
  manuais —, cada um com o que mede, numerador e denominador, limiar e origem do limiar,
  script ou procedimento manual e arquivo de saída.
- **`README.md` reduzido** a guia de entrada: identificação, como executar, mapa único dos
  caminhos (com quem escreve cada um), tabela de códigos de saída, os três registros, a precedência e a remissão a
  `docs/procedimentos.md`, onde ficam os comandos com todos os parâmetros (design D1). Sai o
  que se encontra em outro artefato.
- Remissões das skills ao README atualizadas para o novo lugar de cada informação.
- Inconsistências entre o modelo, o plano e o protocolo encontradas na redação são
  **registradas como pendência**, não resolvidas no guia.

Fora de escopo, cada qual para change própria: gerar strings de referência a partir do
controle terminológico; gerar as fichas por base; conferir a ligação questão ↔ facetas ↔
critérios; script de análise e otimização de descritores; clientes para os instrumentos
`Manual` (`eric`, `brased`); texto de ajuda dos argumentos posicionais da CLI.

## Capabilities

### New Capabilities

Nenhuma. A mudança foi planejada como documental. Por decisão do pesquisador na tarefa 4.1
(2026-11-22), dois comportamentos de script mudaram sem alterar requisito de spec, porque
as specs não enumeram esses valores: a gramática admite a ação "Não aplicável" nos
critérios, e `padroes.calibracao_triagem` deixou o esquema da configuração e reprova como
chave desconhecida (ver Impact).

### Modified Capabilities

Nenhuma. O requisito "Códigos documentados e exibidos" (`interface-de-comando`) continua
atendido: a tabela de códigos permanece no README. A change declara `skip_specs: true`.

## Impact

- `README.md` reescrito; `docs/procedimentos.md` novo.
- Skills que remetem ao README: `revisao-geral-do-projeto`, `teste-de-aderencia` (cita a
  "seção Scripts"), `ficha-de-busca-por-base`, `criterios-de-elegibilidade`,
  `validacao-vocabulario-controlado`, `registrar-decisao`.
- `data/pendencias.json`: novas pendências para as divergências modelo × projeto, por
  decisão do pesquisador.
- Por decisão do pesquisador na tarefa 4.1 (2026-11-22), fora do escopo documental inicial:
  CE10 (Fator de impacto, ação "Não aplicável") no protocolo e nas quatro fichas, com o novo
  valor de ação na gramática (`src/rsl/gramatica.py`, `src/rsl/relatorio.py`); retirada do
  ASReview e da calibração da triagem assistida do plano, do `config.toml`, do código
  (`src/rsl/config.py`, `src/rsl/leitura.py`), das skills (`calibracao-da-triagem` apagada) e
  das pendências. Registro em `data/historico.md`, 2026-11-22.
