# Proposal

## Why

A avaliação de `data/pendencias.json` feita em 2026-11-22 confirmou no código quatro
defeitos. Nenhum deles reprova uma conferência, mas todos levam quem lê a ajuda, a saída ou
a planilha a errar, e dois deles podem destruir trabalho ou orientar uma ação que o
histórico já rejeitou:

- **`sementes planilha` apaga o preenchimento manual (PD27).** `src/rsl/sementes.py:127`
  grava `semente_aderencia.csv` com `open("w")`, sem ler o arquivo anterior. Reexecutar o
  subcomando perde `indexada`, `data_etapa1`, `recuperada`, `como_localizada`,
  `data_etapa2` e `observacao`. Ainda não houve perda, porque essas colunas estão vazias na
  planilha atual. É o momento de corrigir: o teste de aderência (M3/E2) é o próximo passo
  que as preenche.
- **`--retorno` parece opcional (PD28).** `src/rsl/__main__.py:94` declara o argumento
  sem `required`, mas `src/rsl/busca/execucao.py:36` sai com USO sem ele. A ajuda contradiz
  o comportamento.
- **Coluna citada com nome errado (PD29).** `src/rsl/busca/aderencia.py` cita `indexado`
  na docstring (linha 74) e na saída impressa ao usuário (linha 131). A planilha usa
  `indexada`.
- **`pendencias` manda reconstituir o registro.** `src/rsl/dados.py:252` orienta
  "reconstitua o registro a partir das fichas". O histórico de 2026-11-19 ("Citações de
  medição sem lastro rebaixadas") decidiu não reconstituir. O registro passa a existir na
  primeira execução, com `busca registrar`.

## What Changes

- `sementes planilha` preserva as colunas preenchidas à mão quando regrava a planilha,
  casando cada linha por `id` e `base`, como `busca sensibilidade` preserva `elegivel`.
  Linha de semente ou base que deixou de existir não fica na planilha. Se a regravação
  perderia algum preenchimento manual, por exemplo de semente retirada ou renumerada, o
  subcomando recusa e não grava.
- `busca registrar` passa a exigir `--retorno` no parser: a ausência sai com USO pela
  própria validação de argumentos, e o `-h` mostra o argumento como obrigatório. A sinopse
  transcrita em `docs/procedimentos.md` é atualizada.
- A docstring e a saída de `busca aderencia` usam o nome de coluna `indexada`.
- O relato de registro de execução ausente, em `pendencias`, orienta registrar a primeira
  execução com `busca registrar`, e não reconstituir o registro.
- O autoteste ganha um caso que reprova a perda das colunas manuais na regravação.

Fora do escopo: o conteúdo de `data/pendencias.json` e do README, as decisões sobre PD22,
PD25 e PD26 e qualquer mudança em strings, critérios ou limiares.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `derivacao-das-expressoes`: a planilha de aderência preserva as colunas manuais na
  regravação; `busca registrar` exige o retorno declarado; o relato de registro ausente
  remete à primeira execução registrada.

## Impact

- Código: `src/rsl/sementes.py`, `src/rsl/__main__.py`, `src/rsl/busca/aderencia.py`,
  `src/rsl/busca/registro.py` (passa a importar `CMD_REGISTRAR` de `src/rsl/dados.py`, sem
  cópia própria), `src/rsl/dados.py` e o autoteste. `src/rsl/busca/execucao.py` não muda: a
  verificação de `--retorno` dentro de `registrar()` continua (design, D5).
- Documentação: a sinopse de `busca registrar` em `docs/procedimentos.md` e a descrição de
  `data/semente_aderencia.csv` no mapa do `README.md` ("regravada inteira a cada execução").
- Dados: `data/semente_aderencia.csv` não muda de forma. A regravação passa a conservar o
  que o pesquisador preencheu.
- Pendências resolvidas pela change: PD27, PD28 e PD29.
