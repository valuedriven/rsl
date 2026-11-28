# Proposal

## Why

O resultado de uma sondagem de sintaxe mora hoje em três lugares:
- `data/registro_execucao.json` (`bases.BDn.sondagens`), com os retornos e a leitura
  observada;
- as `[[sondagens.leituras]]` da fonte do procedimento (`docs/procedimentos/<sigla>/procedimento.toml`),
  com o resultado e a conclusão possíveis;
- a tabela `[[sintaxe]]` da mesma fonte, com o estado vigente de cada elemento.

A evidência das sondagens soma cerca de 16M em `data/evidencia/sondagens/`. O roteiro é
planejamento; o observado é registro; e o mesmo resultado escrito à mão em mais de um lugar
diverge na alteração seguinte.

## What Changes

- **BREAKING**: as sondagens saem de `data/registro_execucao.json` para `data/sondagens.json`.
  O arquivo guarda, por base e por sondagem, só a última: data e hora, retornos e número da
  leitura observada. Sondagem refeita substitui a anterior.
- A fonte do procedimento guarda o roteiro (consultas, leituras possíveis) e não repete o
  observado.
- Avaliar se o estado de cada elemento em `[[sintaxe]]` passa a ser calculado da sondagem
  registrada, em vez de editado. Isso eliminaria a terceira cópia por construção.
- Reduzir `data/evidencia/sondagens/`: expurgar a evidência de sondagens refeitas e
  reavaliar a evidência exigida no registro (hoje `sondagens registrar` recusa registro sem
  arquivo de evidência). O destino da evidência que fica (repositório, `tmp/` ou anexo no
  Zotero) decide-se no design.
- Revisar a skill `executar-sondagens-de-sintaxe` e as notas de sintaxe da fonte de cada
  base, eliminando o excesso.

Fora do escopo: o registro das execuções (change 3), que fica dono de `data/execucoes.json`.
Esta change não gera entrada no `data/historico.md`.

Depende de: `zotero-como-fonte-unica`, só se a evidência for para o Zotero. Não depende da
ordem em relação à change 3.

## Capabilities

### New Capabilities
<!-- nenhuma -->

### Modified Capabilities
- `sondagens-por-base`: forma e lugar do resultado registrado; exigência de evidência;
  "Resultado registrado conferido".
- `fonte-do-procedimento`: o que a fonte guarda da sondagem; possível cálculo do estado em
  `[[sintaxe]]`.
- `gramatica-do-protocolo`: forma da fonte, se `[[sintaxe]]` mudar.
- `geracao-dos-procedimentos`: o procedimento gerado passa a ler o resultado do arquivo novo.
- `cobertura-por-base`: elemento não verificado remete à sondagem registrada no arquivo novo.

## Impact

- Código: `src/rsl/sondagens.py`, `src/rsl/fonte.py`, `src/rsl/procedimentos.py`,
  `src/rsl/gramatica.py`, `src/rsl/dados.py` (`problemas_sondagens_registradas`),
  autotestes de procedimentos e de sondagens.
- Dados: `data/registro_execucao.json` (parte das sondagens), `data/evidencia/sondagens/`.
- Documentação: `docs/procedimentos/*/procedimento.toml`, `notas_sintaxe.md`,
  `docs/procedimentos_busca_*.md` (regenerados).
- Skill: `.agents/skills/executar-sondagens-de-sintaxe/`.
