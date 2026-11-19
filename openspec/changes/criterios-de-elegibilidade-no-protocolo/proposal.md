# Proposal

## Why

O README declara que o protocolo prevalece sobre qualquer outro documento, mas a regra
operacional de inclusão está só no plano (`docs/01_plano.md`, linha 82): a regra de borda e
a regra "práticas e/ou fatores situacionais". No protocolo, o CE6 diz apenas "Documentos não
pertinentes ao escopo temático" e não tem justificativa. Os revisores aplicam os critérios
pelo protocolo. Se a regra ficar fora dele, a 3ª filtragem aplica um critério que o
documento prevalente não enuncia, e o kappa mede a concordância sobre uma regra que não
está escrita onde deveria.

Fixar os critérios antes das filtragens (M3/E3) evita emenda durante a triagem.

## What Changes

### D1 — Regra de inclusão e regra de borda no protocolo

Três elementos estão hoje só no plano (`docs/01_plano.md`, linha 82) e vão para a tabela de
critérios do protocolo. O plano passa a remeter ao protocolo.
- a regra única de inclusão: o estudo formaliza práticas **e/ou** fatores situacionais;
- a regra de borda, inclusive a cláusula de que operações sobre fatores situacionais não
  justificam inclusão por si;
- a lista "Ficam fora do recorte", com as quatro exclusões temáticas: representação de
  evidências, apoio à decisão docente, instanciação computacional e artefato alheio a
  práticas e a fatores. Verificado por busca: nenhum dos três elementos consta de
  `docs/02` nem de `docs/03`.

A redação é do pesquisador. Ele decide:
- **(a)** se a regra vira um critério novo de inclusão, com ID próprio e renumeração; ou
- **(b)** se entra como conteúdo do CE6, que passa a ser operacional.

A alternativa (a) exige atualizar as referências numéricas nas fichas, no README e nas
skills.

### D2 — CE4 e as revisões sistemáticas

Três formulações não coincidem:
- o CE4 lista revisões sistemáticas e de escopo como tipo **incluído**;
- a justificativa do CE4 diz que elas servem "como fonte de backward search, não como
  evidência primária";
- o README (M3/E3) manda as revisões para um **conjunto suplementar com contagem própria**.

Alternativas:
- **(a)** o CE4 inclui as revisões e remete ao destino "conjunto suplementar", fixando o
  tratamento no protocolo;
- **(b)** as revisões saem do CE4 e entram por regra própria.

### D3 — CE5 e a numeração das filtragens

O CE5 diz "não localizados em texto completo na segunda filtragem, referente à leitura
seletiva". O README chama a 2ª filtragem de título e resumo e a 3ª de texto completo.

Pode ser coerente: a disponibilidade seria verificada na 2ª filtragem, antes da leitura
integral. Mas a redação admite as duas leituras. Fixar em que momento se verifica a
disponibilidade e usar a mesma nomenclatura no protocolo, no README e nas fichas.

### D4 — Justificativas ausentes

CE5 e CE6 não têm justificativa. Completar a coluna, com a redação do pesquisador.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-do-protocolo`: exigência proposta. `--conferir` reprova critério com a coluna de
  justificativa vazia, nomeando o ID, e o autoteste injeta o defeito. Garante D4 por
  construção.
- `cobertura-por-base`: exigência proposta. Todo ID de critério citado na seção 2 de uma
  ficha existe na tabela de critérios do protocolo, e cada critério do protocolo aparece na
  seção 2 de cada ficha; a divergência reprova só aquela base. Impede que uma renumeração
  (D1 a) deixe fichas defasadas sem aviso.

Se o pesquisador recusar as duas exigências, a change passa a `skip_specs: true`.

## Impact

- `docs/03_protocolo_estrategia_pesquisa.md` — tabela de critérios.
- `docs/01_plano.md` — remissão no lugar da regra.
- `README.md` — M3/E3, se mudar a nomenclatura ou a numeração.
- `docs/busca_base_*.md`, seção 2 — tabela de critérios, se a numeração mudar.
- `.agents/skills/criterios-de-elegibilidade/`, `filtragens/` — referências.
- `config.toml` — `dimensoes_criterio`, se surgir dimensão nova.
- `src/protocolo.py` — conferência e autoteste, se a exigência for adotada.
- `data/historico.md` — emenda de critérios.
