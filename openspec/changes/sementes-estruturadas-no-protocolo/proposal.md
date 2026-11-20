# Proposal

> O nome da change (`sementes-estruturadas-no-protocolo`) é anterior às decisões de
> 2026-11-20: o conjunto-semente sai do protocolo para um arquivo TOML próprio, localizado
> pelo `config.toml`. O nome foi mantido para não recriar a change.
>
> **Depende de `reestruturacao-do-protocolo`.** Aquela change leva a tabela de sementes
> para `docs/sementes.toml` num formato intermediário (`id`, `semente` em texto livre,
> `bases`, `papel`), que o pesquisador já criou. Esta change parte desse arquivo e o
> estrutura. Os requisitos aqui modificados são os que ficam nas specs depois do
> arquivamento daquela.

## Why

Os dados de cada semente estão hoje em dois lugares, ligados por um elo frágil:

- **Em `docs/sementes.toml`**, o campo `semente` traz a referência inteira como texto
  livre, como fazia a tabela do protocolo. O leitor extrai autoria, ano, título e DOI por
  expressão regular:
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
  - o TOML é um **arquivo próprio**, `docs/sementes.toml`, com tabela `[[sementes]]`,
    como o pesquisador o criou;
  - o caminho fica no `config.toml` (`[documentos] sementes`), e o protocolo não o cita;
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

- **Campo `semente` decomposto.** O arquivo `docs/sementes.toml` troca o texto livre por
  campos, e o esquema fechado passa a ser:
  - os dados bibliográficos: `id`, `autores` (lista), `ano`, `titulo`, `veiculo`, mais
    `volume`, `numero`, `paginas` e `doi`, opcionais;
  - `bases`: lista das siglas das bases que indexam a semente;
  - `facetas`: lista opcional de `FCTn`, informada pelo pesquisador;
  - `papel`: `desenvolvimento` ou `validação`;
  - os dados de conferência, opcionais: `verificacao`, `tipo`, `alinhamento`, `nota`,
    `veiculo_conferido`, `eric`;
  - `observacoes`, opcional: o que a referência traz e não cabe em outro campo.

  O campo `semente` sai, e com ele `_titulo()` e `_doi()`. As regras da seção
  "Conjunto-semente" do protocolo (regra de ajuste, fórmula de recuperação) não mudam.
- **A leitura reprova, com PROTOCOLO_ILEGIVEL**, além do que `reestruturacao-do-protocolo`
  já faz reprovar (TOML inválido, arquivo ausente com CONFIGURACAO):
  - campo obrigatório do esquema novo ausente ou de tipo errado;
  - campo desconhecido;
  - `id` fora da forma `SEn` ou repetido;
  - DOI fora da forma `10.x/…`;
  - faceta fora da tabela de facetas do protocolo, ou repetida.
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

- `leitura-do-protocolo`: "Conjunto-semente lido do arquivo de sementes", o esquema
  intermediário deixado por `reestruturacao-do-protocolo`, é substituído pela leitura com
  esquema estruturado, `facetas`, dados de conferência e `observacoes`. Entram as
  pendências de juízo, a retirada sem resto e a referência exibida a partir dos campos.
- `gramatica-do-protocolo`: o esquema do arquivo de sementes exibido pela gramática passa
  aos campos novos.
- `interface-de-comando`: `sementes sincronizar` sai da lista de subcomandos e da
  correspondência de nomes.
- `derivacao-das-expressoes`: `sementes.json` sai dos arquivos lidos da configuração, e a
  planilha de aderência perde `escopo` e passa a ler os dados de conferência do arquivo de
  sementes.

## Impact

- `docs/sementes.toml`: reescrito com os campos estruturados, a partir da transcrição e da
  migração conferidas. O protocolo não muda.
- `data/sementes.json`: removido, depois de migrado e conferido campo a campo.
- `data/evidencia/referencias/SE10_crossref.*`: permanecem, porque SE10 continua no
  conjunto. A regra nova vale para retiradas futuras.
- `data/pendencias.json`, PD01: deixa de citar `escopo` e `sementes.json`.
- Código: `src/rsl/leitura.py`, `gramatica.py`, `relatorio.py`, `sementes.py`,
  `dados.py`, `config.py`, `__main__.py` e o autoteste.
- `config.toml` (`[dados] sementes` e `[planilha] campos_autorais` saem), `README.md`
  (Mapa, Scripts, regras de preservação e de sincronização) e as skills
  `conjunto-semente` e `teste-de-aderencia`.
- **Dependências:** `refatoracao-dos-scripts` está arquivada (2026-11-20);
  `reestruturacao-do-protocolo` precisa estar arquivada antes da tarefa 2.1.
