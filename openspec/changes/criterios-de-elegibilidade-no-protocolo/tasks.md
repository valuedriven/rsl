# Tasks

## 1. Decisões do pesquisador

- [x] 1.1 Obter do pesquisador a forma da D1: critério novo com renumeração, conteúdo do CE6, ou a recomendação do design (inclusão própria e contra-escopo como exclusões). Verificar que a decisão consta em `data/historico.md`
- [x] 1.2 Obter a decisão D2, o tratamento das revisões sistemáticas no CE4 (incluídas e destinadas ao conjunto suplementar, ou regra própria). Verificar o registro no histórico
- [x] 1.3 Obter a decisão D3: em qual filtragem se verifica a disponibilidade do texto completo (CE5). Verificar o registro no histórico
- [x] 1.4 Obter do pesquisador se adota cada exigência desta change (justificativa obrigatória; critérios da ficha conferidos). Exigência recusada tem a sua spec removida. Recusadas as duas, declarar `skip_specs: true` e verificar com `openspec validate criterios-de-elegibilidade-no-protocolo`

## 2. Protocolo e plano

- [x] 2.1 Escrever na tabela de critérios de `docs/03_protocolo_estrategia_pesquisa.md` a regra de inclusão, a regra de borda e o contra-escopo, na forma decidida em 1.1 e com a redação aprovada pelo pesquisador. Verificar com `python3 src/protocolo.py --conferir` que numeração e dimensões passam
- [x] 2.2 Ajustar CE4 e CE5 conforme 1.2 e 1.3, e preencher as justificativas de CE5 e CE6 com a redação do pesquisador. Verificar que nenhuma linha da tabela tem a coluna "Justificativa" vazia
- [x] 2.3 Substituir em `docs/01_plano.md` (linha 82 e vizinhança) a regra e o contra-escopo por remissão ao protocolo. Verificar com `grep -n "Regra de borda\|Ficam fora do recorte" docs/01_plano.md` que só resta a remissão
- [x] 2.4 Se houve dimensão nova, atualizar `[conferencia] dimensoes_criterio` no `config.toml`. Verificar com `--mostrar`

## 3. Referências

- [x] 3.1 Atualizar a seção 2 das quatro fichas para os IDs vigentes. Verificar que os IDs citados em cada ficha são exatamente os do protocolo
- [x] 3.2 Atualizar as menções a critério no README (M3/E3) e nas skills `criterios-de-elegibilidade` e `filtragens`, localizadas por `grep -rn "CE[0-9]" README.md .agents/skills`. Verificar que nenhuma menção cita ID inexistente

## 4. Conferências (conforme 1.4)

- [x] 4.1 Implementar em `--conferir` a exigência "Critério de elegibilidade tem justificativa", com o caso de autoteste correspondente. Verificar com `--conferir --autoteste` que o caso reprova pelo motivo esperado e que o protocolo corrigido passa
- [x] 4.2 Implementar a exigência "Critérios da ficha conferem com o protocolo", por base, com o caso de autoteste que injeta um ID inexistente numa única ficha. Verificar que só aquela base reprova
- [x] 4.3 Descrever as duas conferências no README, na lista do que `--conferir` verifica. Verificar que a descrição corresponde ao comportamento

## 5. Integração

- [x] 5.1 Registrar a emenda de critérios em `data/historico.md`, com data, alcance e fundamento, e rodar `python3 src/protocolo.py --conferir --autoteste`. Verificar que todos os casos executados têm o resultado esperado

## Workflow follow-up

- Concluir antes de M3/E3: as três filtragens aplicam os critérios desta versão.
- Arquivar a change depois da revisão.
