# Tasks

## 1. Pré-requisitos

- [ ] 1.1 Verificar que `expressoes-literais-por-base` está arquivada e as suas specs promovidas (`openspec list --json` sem ela; `openspec/specs/cobertura-por-base/spec.md` contém "Termos do bloco conferem com as facetas declaradas")
- [ ] 1.2 Verificar que `data/registro_execucao.json` existe (PD02, `higiene-de-rastreabilidade`) com `python3 src/protocolo.py --conferir-dados`, que não pode mais reportar o arquivo ausente

## 2. Medições (pesquisador, primeira sessão na WoS e na Scopus)

- [ ] 2.1 Registrar como execuções fora do corpus as contagens de EB4 e de EB5 como estão. Verificar que cada execução tem `id` no registro e que `--conferir-dados` passa
- [ ] 2.2 Registrar a contagem de EB4 com STR3 sem a forma isolada (`practice`, `prática`, `práctica`). Verificar o `id` no registro
- [ ] 2.3 Registrar a contagem de EB5 acrescida de `conceptual model*` na STR1, para medir o que D3 acrescenta. Verificar o `id` no registro
- [ ] 2.4 Conferir na fonte o resumo da SE4, para saber se contém termo de STR2 além do título. Verificar que o resultado está anotado com a fonte

## 3. Decisões do pesquisador

- [ ] 3.1 Apresentar ao pesquisador as medições do grupo 2 e obter as decisões D1, D2, D3 e D4. Verificar que cada decisão consta de `data/historico.md`, citando a execução (`BDn/<id>`) em que se apoia
- [ ] 3.2 Para cada exigência condicional desta change (disjunção das strings, sonda sem proximidade, sensibilidade decomposta) não adotada, remover a spec correspondente. Recusadas todas, declarar `skip_specs: true`. Verificar com `openspec validate revisao-das-strings-por-faceta`
- [ ] 3.3 Para todo termo incluído, registrar no histórico se alguma semente o motivou. Verificar que `conjunto-semente-independente` recebeu a reclassificação, se houver

## 4. Emenda do protocolo

- [ ] 4.1 Emendar quadro e strings em `docs/03_protocolo_estrategia_pesquisa.md` conforme 3.1 e, se D1 (a), implementar no mesmo passo em `--conferir` a exigência "Termo de string pertence a uma só faceta", com o caso de autoteste. Verificar com `--conferir --autoteste` que o protocolo passa e o caso reprova pelo motivo esperado
- [ ] 4.2 Regenerar as strings e os blocos literais das quatro fichas a partir do protocolo. Verificar com `--conferir` e `--conferir-dados` que as quatro bases passam
- [ ] 4.3 Se `data/validacao_termologica.csv` existir, rodar `python3 src/validar_termos.py --importar`. Verificar que os termos retirados ficaram como linha fora do protocolo, sem perder decisão

## 5. Sonda sem proximidade (se D4 a)

- [ ] 5.1 Acrescentar à EB5 das fichas da WoS e da Scopus o bloco literal "sem proximidade" e, no mesmo passo, a conferência por base da exigência "Sonda sem proximidade onde as âncoras usam proximidade", com o caso de autoteste. Verificar que o caso reprova só a base injetada e que a BRAPCI e a ERIC não exigem o bloco
- [ ] 5.2 Permitir a `--registrar` declarar a variante da sonda e gravá-la na execução. Verificar com um registro sintético que as duas variantes coexistem em execuções distintas
- [ ] 5.3 Fazer `--sensibilidade` relatar a perda por proximidade em saída separada quando as duas variantes estão registradas, e declarar "não calculada" quando falta uma. Verificar com dados sintéticos e confirmar que, sem variante, a saída é idêntica à anterior
- [ ] 5.4 Atualizar a skill `ficha-de-busca-por-base`, a seção "Como executar" das fichas e o README (M3/E2, sensibilidade). Verificar que o README descreve as duas perdas e quando cada uma é calculada

## 6. Integração

- [ ] 6.1 Registrar a emenda de busca em `data/historico.md`, com data, alcance e fundamento, e rodar `python3 src/protocolo.py --conferir --autoteste` e `python3 src/derivar_expressoes.py --autoteste`. Verificar que todos os casos executados têm o resultado esperado

## Workflow follow-up

- Reexecução e teste de aderência seguem o fluxo do protocolo depois da emenda.
- Arquivar a change depois da revisão.
