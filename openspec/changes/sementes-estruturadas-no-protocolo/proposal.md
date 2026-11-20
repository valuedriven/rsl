# Proposal

> O nome da change (`sementes-estruturadas-no-protocolo`) é anterior à decisão de
> 2026-11-20: o conjunto-semente sai do protocolo para um arquivo TOML próprio, apontado
> pelo protocolo. O nome foi mantido para não recriar a change.

## Why

Os dados de cada semente estão hoje em dois lugares, ligados por um elo frágil:

- **No protocolo**, a tabela `ID Semente | Semente | Bases | Papel` traz a referência
  inteira como texto livre. O leitor extrai autoria, ano, título e DOI por expressão
  regular:
  - o título termina "no primeiro ponto seguido de maiúscula ou de dígito" (`_titulo()`);
  - o DOI tem de ser o último elemento da célula (`_doi()`).

  Referência com ponto no título, com subtítulo ou com o DOI fora do fim é lida errado
  **sem reprovar**.
- **Em `data/sementes.json`**, os metadados de conferência (verificação, tipo,
  alinhamento, nota…) ligam-se à semente por DOI ou título lido daquela extração. Para
  manter a ligação existem `ligacao`, `sementes sincronizar` e o aviso de entrada órfã.
  Esses mecanismos só existem porque os dados estão separados.

Decisões do pesquisador:

- 2026-11-19: o conjunto-semente passa a TOML estruturado, lido com `tomllib`.
- 2026-11-20:
  - o TOML é um **arquivo próprio**, `docs/conjunto_semente.toml`, apontado pela seção
    "Conjunto-semente" do protocolo;
  - ele **absorve os dados de conferência**, e `data/sementes.json` deixa de existir;
  - `bases` registra a **indexação** da semente na base. A recuperação pela busca continua
    calculada em `semente_aderencia.csv`;
  - entra o campo `facetas`, **informado pelo pesquisador**;
  - `veiculo`, `volume`, `numero`, `paginas` e `papel` ficam, e `escopo` sai;
  - o que a transcrição não encaixa em nenhum campo vai para o campo novo `observacoes`;
  - a regra para semente de validação sem faceta âncora fica em branco: o caso só é
    relatado;
  - **semente retirada sai de tudo**: do TOML, das saídas regeneradas e da evidência
    bruta. A retirada fica registrada em `data/historico.md`.

## What Changes

- **BREAKING (forma do protocolo):** a seção "Conjunto-semente" troca a tabela por uma
  linha que aponta o arquivo `docs/conjunto_semente.toml`. As regras que acompanham a
  seção (regra de ajuste, fórmula de recuperação) ficam no protocolo, porque são método e
  não dado.
- **Arquivo `docs/conjunto_semente.toml`**, com uma tabela `[[semente]]` por estudo e
  esquema fechado:
  - os dados bibliográficos: `id`, `autores` (lista), `ano`, `titulo`, `veiculo`, mais
    `volume`, `numero`, `paginas` e `doi`, opcionais;
  - `bases`: lista das siglas das bases que indexam a semente;
  - `facetas`: lista opcional de `FCTn`, informada pelo pesquisador;
  - `papel`: `desenvolvimento` ou `validação`;
  - os dados de conferência, opcionais: `verificacao`, `tipo`, `alinhamento`, `nota`,
    `veiculo_conferido`, `eric`;
  - `observacoes`, opcional: o que a referência traz e não cabe em outro campo.
- **A leitura reprova, com PROTOCOLO_ILEGIVEL:**
  - apontamento ausente, duplicado ou para arquivo inexistente;
  - TOML inválido;
  - campo obrigatório ausente ou de tipo errado;
  - campo desconhecido;
  - `id` fora da forma `SEn` ou repetido;
  - DOI fora da forma `10.x/…`;
  - base ou faceta fora das respectivas tabelas do protocolo, ou repetida;
  - `papel` fora do domínio;
  - conjunto sem semente de validação.
- **Relatado em `pendencias`, sem reprovar:**
  - `facetas` vazia;
  - semente de validação sem faceta âncora, enquanto o pesquisador não decide a regra;
  - campo de conferência vazio (`tipo`, `alinhamento`).
- **Saem:** `data/sementes.json`, `ligacao`, `sementes sincronizar`, o aviso de entrada
  órfã, `[dados] sementes` e `[planilha] campos_autorais` do `config.toml`, e a coluna
  `escopo` da planilha de aderência.
- **Evidência bruta de semente inexistente reprova `conferir-dados`.** Assim, nada de uma
  semente retirada sobra em silêncio.
- **`rsl mostrar` exibe cada semente na forma de referência**, montada dos campos.
- **Os campos são transcritos da referência atual e de `sementes.json`, sem completar dado
  de memória.** O que a fonte não traz fica vazio e vira pendência.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-do-protocolo`: "Conjunto-semente lido de tabela" é substituído pela leitura do
  arquivo apontado, com esquema fechado, `facetas`, dados de conferência e `observacoes`. O
  cenário de distribuição em "Conferência verifica coerência interna" passa a citar o
  arquivo.
- `gramatica-do-protocolo`: a seção "Conjunto-semente" passa a exigir o apontamento do
  arquivo, e a gramática exibe o esquema do arquivo.
- `interface-de-comando`: `sementes sincronizar` sai da lista de subcomandos e da
  correspondência de nomes.
- `derivacao-das-expressoes`: `sementes.json` sai dos arquivos lidos da configuração, o
  caminho do conjunto-semente vem do protocolo, e a planilha de aderência perde `escopo`.

## Impact

- `docs/03_protocolo_estrategia_pesquisa.md`, seção "Conjunto-semente": a tabela sai e
  entra o apontamento. É emenda de forma, registrada em `data/historico.md`.
- Novo `docs/conjunto_semente.toml`.
- `data/sementes.json`: removido, depois de migrado e conferido campo a campo.
- `data/evidencia/referencias/SE10_crossref.*`: permanecem, porque SE10 continua no
  conjunto. A regra nova vale para retiradas futuras.
- `data/pendencias.json`, PD01: deixa de citar `escopo` e `sementes.json`.
- Código: `src/rsl/leitura.py`, `gramatica.py`, `relatorio.py`, `sementes.py`,
  `dados.py`, `config.py`, `__main__.py` e o autoteste.
- `config.toml`, `README.md` (Mapa, Scripts, regras de preservação e de sincronização) e
  as skills `conjunto-semente` e `teste-de-aderencia`.
- **Dependência satisfeita:** `refatoracao-dos-scripts` está arquivada (2026-11-20).
