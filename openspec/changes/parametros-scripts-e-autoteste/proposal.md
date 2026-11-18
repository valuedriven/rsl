# Proposal

## Why

A verificação da change `protocolo-fonte-unica` apontou dois avisos e duas sugestões. O
requisito "Nenhum parâmetro fixado no código" só foi cumprido em `src/protocolo.py`:
`derivar_expressoes.py` ainda fixa a composição e os papéis das expressões (EB1 a EB5) e as
siglas das bases, e `gen_semente.py` fixa as siglas das bases. Além disso, parte do
comportamento novo foi verificado só à mão — o planejamento da validação por instrumento e
a reprovação por base — e o resumo do autoteste pode ser lido como aprovação quando os casos
dos arquivos alimentados não rodam.

## What Changes

- `derivar_expressoes.py` deixa de fixar EB1 a EB5: a prova da composição passa a usar as
  relações lidas do protocolo (âncoras, específicas, executada, sonda), expostas por
  `src/protocolo.py`; deixa de fixar o mapa slug → sigla das bases, que passa a vir de
  `[fichas]` do `config.toml`.
- `gen_semente.py` deixa de fixar a lista de bases, que passa a vir de `[fichas]`.
- `src/protocolo.py` expõe os papéis das expressões (âncoras, específicas, gerais, executada,
  sonda) calculados uma única vez, usados pela conferência de coerência e pela derivação.
- Autoteste ganha casos para o planejamento da validação terminológica: faceta com vários
  instrumentos, instrumento retirado da linha, filtro por idioma do instrumento e
  instrumento manual.
- Autoteste ganha caso de reprovação por base: só a ficha alterada reprova.
- Resumo do autoteste distingue caso não executado de caso aprovado.

## Capabilities

### New Capabilities

- `derivacao-das-expressoes`: derivação local das expressões e instrumento de aderência sem
  composição, papéis nem bases fixados no código.

### Modified Capabilities

Criadas pela change `protocolo-fonte-unica`, ainda não arquivada; esta change só lhes
acrescenta requisitos (ADDED). Arquivar `protocolo-fonte-unica` antes desta.

- `leitura-do-protocolo`: papéis das expressões expostos uma única vez; resumo do autoteste
  com casos não executados.
- `cobertura-por-base`: autoteste da reprovação por base.
- `validacao-terminologica`: autoteste do planejamento por instrumento.

## Impact

- **Código:** `src/derivar_expressoes.py`, `src/gen_semente.py`, `src/protocolo.py`
  (papéis das expressões e autoteste).
- **Dependência de arquivamento:** `protocolo-fonte-unica` deve ser arquivada antes, para
  que as capacidades existam em `openspec/specs/`.
- **Fora do escopo:** mudança de comportamento da derivação, da aderência, da fidelidade ou
  da sensibilidade; as saídas para o protocolo atual devem ser idênticas.
