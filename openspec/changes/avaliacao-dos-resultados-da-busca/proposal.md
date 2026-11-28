# Proposal

## Why

As análises posteriores à busca (sensibilidade, fidelidade, anatomia da perda, aderência,
candidatos e ordem de triagem) gravam em `data/` saídas regeneráveis ao lado de arquivos que
carregam juízo do pesquisador. O caso principal é a coluna `elegivel` de
`sensibilidade_<base>.csv`. Há ainda uma leitura analítica órfã
(`data/leitura_sensibilidade_wos.md`), que nenhum script, skill ou documento cita. Separar o
que se recalcula do que se julga evita perder juízo numa regeneração e tira do repositório o
que não precisa estar nele.

## What Changes

- Pasta `analise/` na raiz, ao lado de `docs/` (o que se planeja) e `data/` (o que se
  registra), para o que se julga: classificações e leituras do pesquisador sobre os
  resultados.
- Saídas regeneráveis (`registros.csv`, `contagens_busca.csv`, `ordem_triagem.csv`,
  `fidelidade_*`, `candidatos_*`, `anatomia_*`) vão para `tmp/`, fora do git. O pesquisador
  decide se `ordem_triagem.csv` continua versionada, porque é sobre ela que a triagem
  trabalha.
- `sensibilidade_<base>.*` vai para `analise/`, preservando a classificação `elegivel`.
- Garantia por construção: o script recusa gravar coluna de juízo fora de `analise/` e não
  sobrescreve juízo existente ao regenerar.
- Formato de cada arquivo pelo critério de quem o edita: o que o pesquisador edita fica num
  formato confortável de editar; o que só o script lê vai para JSON ou `tmp/`.
- Identidade do registro nas análises: passa à chave do item no Zotero se a sondagem da
  change 3 confirmar que a mesclagem preserva as coleções; senão, continua na chave de
  deduplicação atual.
- O pesquisador decide o destino de `data/leitura_sensibilidade_wos.md` (`analise/` ou
  expurgo).
- Revisar as skills `avaliar-resultados-da-busca` e `testar-aderencia-das-expressoes`.

Esta change não gera entrada no `data/historico.md`.

Depende de: `fluxo-da-execucao-de-busca`.

## Capabilities

### New Capabilities
<!-- nenhuma -->

### Modified Capabilities
- `analise-da-sensibilidade`: lugar e forma do arquivo de sensibilidade; preservação da
  classificação.
- `anatomia-da-perda`: lugar das saídas; nível lido da execução registrada no arquivo novo.
- `derivacao-das-expressoes`: "Saídas preservadas" e "Arquivos de entrada e de saída lidos
  da configuração".
- `interface-de-comando`: chaves `[saidas]` e a chave nova da pasta `analise/`.

## Impact

- Código: `src/rsl/busca/{sensibilidade,fidelidade,anatomia,aderencia,simulacao,derivacao}.py`,
  `src/rsl/derivado.py`, `src/rsl/config.py`, autotestes de busca e de derivado.
- Dados: arquivos de saída em `data/`, `data/leitura_sensibilidade_wos.md`.
- Configuração: `[saidas]`, chave nova da pasta `analise/`.
- Skills: `avaliar-resultados-da-busca`, `testar-aderencia-das-expressoes`.
- Documentação: mapa do `README.md`.
