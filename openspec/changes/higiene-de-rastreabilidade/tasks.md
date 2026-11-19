# Tasks

## 1. Decisões do pesquisador

- [ ] 1.1 Obter do pesquisador a escolha entre (a) reconstituir as medições no registro e (b) rebaixar para **Não verificado**, para cada uma das quatro citações (WoS seção 1, Scopus seção 1, ERIC e BRAPCI no cabeçalho). Verificar que a decisão consta, com data, em `data/historico.md`
- [ ] 1.2 Obter do pesquisador se adota a garantia (`cobertura-por-base`, delta desta change). Se recusar, remover `specs/` desta change, declarar `skip_specs: true` em `.openspec.yaml`, pular o grupo 3 e verificar com `openspec validate higiene-de-rastreabilidade`
- [ ] 1.3 Perguntar ao pesquisador se tem as contagens da execução da versão 1 que fundamentou a emenda de 2026-11-17. Verificar que a resposta está registrada (sim, com a fonte, ou não)
- [ ] 1.4 Obter do pesquisador a escolha para a revisão geral: (a) skill nova `revisao-geral-do-projeto`, com a `parecer-sobre-protocolo` restrita ao parecer externo, ou (b) ampliação da `parecer-sobre-protocolo`. Obter também o nome, se for diferente. Verificar que a escolha está registrada, com data, em `data/historico.md`

## 2. Fichas

- [ ] 2.1 Aplicar a decisão 1.1 em `docs/busca_base_wos.md` e `docs/busca_base_scopus.md` (seção 1) e em `docs/busca_base_eric.md` e `docs/busca_base_brapci.md` (cabeçalho). Na saída (a), só com os dados que o pesquisador fornecer, criando as execuções correspondentes no registro. Verificar com `grep -n registro_execucao docs/busca_base_*.md` que toda menção restante traz `(BDn/<id>)`
- [ ] 2.2 Trocar o caminho do registro por "registro de execução" nas instruções das fichas que só mandam registrar, sem afirmar medição. Verificar com o mesmo grep
- [ ] 2.3 Rodar `python3 src/protocolo.py --conferir` e verificar que as quatro bases passam

## 3. Conferência da citação (se adotada em 1.2)

- [ ] 3.1 Implementar em `src/protocolo.py`, dentro de `--conferir-dados`, a conferência da exigência "Verificação por medição remete a execução registrada", com o caminho do registro lido de `[dados] registro`. Verificar rodando `--conferir-dados` sobre as fichas corrigidas
- [ ] 3.2 Acrescentar ao autoteste os casos da exigência "Autoteste prova a reprovação da verificação sem lastro" (citação sem id, id inexistente, base trocada, citação em prosa) e atualizar `CASOS_DADOS`. Verificar que, sem registro, o resumo os lista como não executados
- [ ] 3.3 Executar os casos de 3.2 contra um registro sintético numa cópia em memória e verificar que cada um reprova só a base injetada
- [ ] 3.4 Documentar a regra na skill `ficha-de-busca-por-base` e no README, na descrição de `--conferir-dados`. Verificar que o README descreve exatamente o que a conferência reprova

## 4. Pendências e histórico

- [ ] 4.1 Em `data/pendencias.json`, passar PD13 e PD14 a `resolvida`, com `resolucao` que cite o caminho arquivado e o commit. Reescrever PD01 para o metadado pendente das 10 sementes. Verificar com `python3 -m json.tool data/pendencias.json`
- [ ] 4.2 Registrar em `data/historico.md` o resultado de 1.3: contagens com fonte, ou a declaração de que o fundamento quantitativo da emenda v2 não foi registrado. Verificar que a entrada tem data, alcance e fundamento
- [ ] 4.3 Rodar `python3 src/protocolo.py --pendencias` e verificar que nenhum relato contradiz `data/pendencias.json`

## 5. Skill de revisão geral (conforme 1.4)

- [ ] 5.1 Redigir a skill conforme D-f: os seis passos, o produto e as três regras próprias. Na saída (a), criar `.agents/skills/revisao-geral-do-projeto/SKILL.md`, com `name` e `description` no formato das demais skills; na saída (b), editar `.agents/skills/parecer-sobre-protocolo/SKILL.md`. Os comandos ficam por remissão ao README, e as classes de achado por remissão ao parecer, sem cópia. Verificar que a skill não nomeia comando nem caminho que o README não declare
- [ ] 5.2 Na saída (a), retirar "autoavaliação" da descrição de `parecer-sobre-protocolo` e remeter à skill nova. Verificar que nenhuma das duas descrições cobre a atividade da outra
- [ ] 5.3 Acrescentar a skill à seção "Atividades transversais" do README. Verificar com `for s in $(ls .agents/skills); do grep -q "\`$s\`" README.md || echo $s; done` que a skill nova não aparece. Em 2026-11-19, `otimizar-strings-revisao-sistematica` já estava ausente do README: apresentar isso ao pesquisador e não incluí-la sem decisão dele
- [ ] 5.4 Prova por cobertura (D-g), em duas partes:
  - fazer uma tabela que ligue cada achado e cada retificação da revisão de 2026-11-19 ao passo ou à regra da skill que o produziria. O texto da revisão está guardado em `revisao-2026-11-19.md`, nesta change; as retificações estão nos `proposal.md` das quatro changes;
  - percorrer o roteiro sobre o estado corrente, só em leitura, e confirmar que nenhum achado ainda aberto nas quatro changes fica sem passo.

  Verificar que a tabela não tem linha sem correspondência e apresentá-la ao pesquisador

## 6. Integração

- [ ] 6.1 Rodar `python3 src/protocolo.py --conferir --autoteste` e `python3 src/derivar_expressoes.py --autoteste` e verificar que todos os casos executados têm o resultado esperado

## Workflow follow-up

- Revisar, commitar e arquivar `expressoes-literais-por-base` (15/15 tarefas), por ação do pesquisador.
- Arquivar esta change depois da revisão.
