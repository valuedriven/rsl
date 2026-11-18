# Proposal

## Why

O protocolo (`docs/03_protocolo_estrategia_pesquisa.md`) deveria ser a fonte única de verdade,
mas hoje há segunda fonte em três lugares: o `src/protocolo.py` fixa no código valores que o
protocolo já declara (composição das expressões, recorte, limiar, dimensões dos critérios,
instrumentos de validação, listas da emenda v2); os documentos carregam histórico de versões
dentro do conteúdo vigente; e o README registra contagens e estado observado que envelhecem.
A duplicação já produz defeito: `--conferir` reprova hoje por `"Idioma"` × `"Idioma(s)"`, e o
script valida termos contra instrumentos (TBCI/UNESCO por idioma) que divergem da seção
"Instrumentos para controle terminológico" do protocolo (por faceta).

## What Changes

- **Protocolo sem histórico.** Remover o aviso "Versão 2", o bloco "Em relação à versão 1" das
  strings, a remissão "ver Nota de emenda" e a **Nota de emenda (v2)**, que passa integralmente
  para `data/historico.md`. A regra do item 7 da Nota (operadores de proximidade e restrição
  por campo) permanece em vigor e é reescrita em uma linha na seção "Expressões de busca"; a do
  item 6 (triagem estratificada) já consta da seção da ferramenta de triagem.
- **Justificativas resumidas em todos os documentos** (`docs/*.md`, `README.md`): explicações e
  racionais na prosa e nas colunas descritivas reduzidos ao mínimo operacional.
  **Preserva-se intacto** o conteúdo das colunas ou seções explicitamente intituladas
  "Justificativa" (hoje: CE1–CE9 e BD1–BD4 no protocolo).
- **README sem contagens de artefatos nem estado observado** (número de skills e de scripts,
  "não existem hoje", "sem conteúdo no momento", datas de descarte, retornos de exemplo).
  Parâmetros de método permanecem por remissão ao protocolo e ao `config.toml`.
- **Referências a v1/v2 removidas** de documentos e scripts, inclusive comentários, mensagens e
  autotestes "emenda v2".
- **BREAKING (conferência):** removidos `RETIRADOS_V2` e `ACRESCENTADOS_V2`. O termo vigente é o
  que está na STR do protocolo; o quadro terminológico passa a ser vocabulário de referência.
  O desconto do termo retirado passa a valer por construção, sem lista mantida à mão.
- **`protocolo.py` sem parâmetro fixado.** Todo parâmetro vem do protocolo ou de
  `config.toml`; a conferência verifica coerência interna, não valores esperados.
- **Novo `config.toml` na raiz** com **valor padrão para todo parâmetro** (limiares, recorte,
  composição e papel das expressões, âncoras, dimensões de critério, mapa base → ficha,
  caminhos de dados, mapa de instrumentos, campos da planilha) e com o **caminho do arquivo do
  protocolo** a ser lido, este sem sobrescrita. **Valor declarado no protocolo
  sobrescreve o padrão.** `--mostrar` exibe a origem de cada valor. Formato TOML, lido com `tomllib`
  (biblioteca padrão, Python 3.11+): nenhuma dependência nova.
- **BREAKING (validação terminológica):** `validar_termos.py` passa a obter os instrumentos de
  cada faceta da seção "Instrumentos para controle terminológico" do protocolo, e os idiomas e
  o modo de consulta de cada instrumento do `config.toml`. Instrumento sem cliente
  automatizado fica como pendência de validação manual, nunca como "não encontrado". Com o
  protocolo atual, FCT4 deixa de ser termo livre e passa a ser validada.
- `derivar_expressoes.py` passa a obter seus limiares via `protocolo.py` (única alteração nele).
- Skill `ficha-de-busca-por-base` ajustada: o desconto do retirado deixa de citar "lista de
  retirados mantida no script".

## Capabilities

### New Capabilities

- `leitura-do-protocolo`: leitura do protocolo como fonte única, com padrões em `config.toml`
  que o protocolo sobrescreve, e conferência de coerência interna do documento.
- `cobertura-por-base`: conferência da string de cada ficha de base contra o vocabulário
  vigente do protocolo (STR), com redução declarada e derivação.
- `validacao-terminologica`: escolha dos instrumentos de validação de cada termo a partir da
  seção de instrumentos do protocolo.

### Modified Capabilities

<!-- Nenhuma: o projeto ainda não tem specs em openspec/specs/. -->

## Impact

- **Código:** `src/protocolo.py` (refatoração principal), `src/validar_termos.py`
  (instrumentos por faceta, fim do estatuto de termo livre fixado), `src/derivar_expressoes.py`
  (limiares via `protocolo.py`); `src/gen_semente.py` só se usar constante removida.
- **Novo arquivo:** `config.toml` (raiz). Sem dependência externa; requisito Python 3.11+.
- **Scripts que leem o protocolo** (`derivar_expressoes.py`, `validar_termos.py`,
  `gen_semente.py`) passam a obter o caminho dele via `protocolo.py`.
- **Documentos:** `docs/03_protocolo_estrategia_pesquisa.md`, `docs/01_plano.md`,
  `docs/02_protocolo_informacoes_gerais.md`, `docs/busca_base_*.md`, `README.md`,
  `data/historico.md` (recebe a Nota de emenda e o registro da mudança de instrumentos).
- **Skills:** `.agents/skills/ficha-de-busca-por-base/SKILL.md` (ajuste pontual); remissões a
  "FCT4 termo livre" em skills e README ajustadas só no que ficar factualmente errado.
- **Fora do escopo:** resumo do texto das demais skills; alteração de conteúdo científico
  (termos, critérios, limiares) — o que muda é onde o valor vive, não o valor.
