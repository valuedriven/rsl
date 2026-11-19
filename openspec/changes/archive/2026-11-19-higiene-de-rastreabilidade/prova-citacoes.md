# Prova da conferência da citação — registro sintético

Data: 2026-11-19. Tarefa 3.3 desta change.

O autoteste permanente (`--conferir --autoteste`) só executa os casos das conferências dos
arquivos alimentados quando `data/registro_execucao.json` existe, como a especificação
exige. Como o registro ainda não existe, esta prova foi feita à parte: `_problemas_citacoes_registro`
foi chamada sobre uma cópia em memória das quatro fichas e um registro sintético, com as
execuções `sonda-near` e `sonda-w5` em todas as bases.

| Caso | Base alvo | Resultado |
| --- | --- | --- |
| Citação sem identificador — `` `data/registro_execucao.json` (BD1) `` | WoS | reprovou só a WoS, nomeando ficha e linha |
| Execução inexistente — `(BD2/sonda-w5x)` | Scopus | reprovou só a Scopus |
| Execução de outra base — `(BD1/sonda-near)` na ficha da ERIC | ERIC | reprovou só a ERIC, nomeando a base trocada |
| Citação em prosa sem identificador | BRAPCI | reprovou só a BRAPCI |
| Citação válida — `(BD1/sonda-near)` | WoS | não reprovou |
| Registro ausente — `(BD4/sonda-near)` sem registro | BRAPCI | reprovou só a BRAPCI, por citação sem lastro |

Resultado: 6 de 6 casos com o resultado esperado; em cada defeito injetado, nenhuma outra
base reprovou. O autoteste permanente cobre os quatro primeiros casos quando o registro
existir.
