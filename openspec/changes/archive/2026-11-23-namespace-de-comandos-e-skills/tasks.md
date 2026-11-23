# Tasks

## 1. Decisões e preparação

- [x] 1.1 Confirmar com o pesquisador a decisão C1/C2 para o artefato “ficha” e registrar a
  escolha no histórico. Verificar que a escolha está escrita e que as tarefas do ramo não
  escolhido ficam explicitamente puladas.
- [x] 1.2 Confirmar o grupo `documentos` (em vez de `protocolo`) para `conferir` e
  `gramatica`; se o pesquisador preferir `protocolo`, atualizar a tabela canônica antes de
  implementar. Verificar que a tabela do design e a do proposal citam o mesmo grupo.
- [x] 1.3 Confirmar que a change `catalogo-de-apoio` está implementada e que
  `python3 -m rsl catalogo gerar` sai 0. Verificar que o catálogo lista as 21 skills e os 17
  caminhos atuais.
- [x] 1.3a Conferir se a change `geracao-das-fichas-de-busca` foi aplicada. Se foi,
  acrescentar `procedimentos gerar` à tabela canônica, ao requisito "Ponto de entrada único" e
  ao inventário do catálogo, com o nome `procedimentos gerar` (C1), e incluir a skill
  `flexao-por-base` nas skills que ficam. Verificar que `catalogo gerar` não acusa
  comando nem skill órfã.
- [x] 1.4 Inventariar as citações vivas dos nomes antigos com
  `grep -rn -E 'conferir-dados|sementes planilha|busca aderencia|termos sonda|busca fidelidade|busca sensibilidade|otimizar-strings|busca-nas-bases|deduplicacao|filtragens|ficha-de-busca-por-base|\[documentos\] ficha'`
  e, para o conceito, `grep -rn -i -w -E 'fichas?'` nos documentos vivos (C1).
  Verificar que o inventário separa documentos vivos, skills, specs e histórico/arquivo.

## 2. Comandos canônicos e aliases

- [x] 2.1 Implementar no parser os grupos `documentos`, `dados`, `projeto`,
  `configuracao`, `aderencia` e `conferencia`, com as ações canônicas da tabela do design.
  Verificar com `python3 -m rsl -h` que todos os caminhos aparecem.
- [x] 2.2 Implementar os aliases ocultos dos nomes antigos, executando a mesma função e
  emitindo aviso com o nome canônico. Verificar que `python3 -m rsl busca aderencia` executa
  `aderencia medir` e avisa.
- [x] 2.3 Garantir que a ajuda lista apenas nomes canônicos. Verificar com
  `python3 -m rsl -h` e com a ajuda de cada grupo que nenhum alias aparece.
- [x] 2.4 Garantir que os códigos de saída e o comportamento não mudam: `documentos
  conferir` 0, `dados conferir` 5, `projeto autoteste` 6, `catalogo gerar` 0. Verificar os
  quatro códigos.
- [x] 2.5 Acrescentar ao autoteste os casos de alias: executa a operação, avisa, não aparece
  na ajuda e, numa cópia sem o alias, o nome antigo sai com USO. Verificar que os casos
  falham quando o alias é removido da cópia.

## 3. Skills

- [x] 3.1 Renomear `otimizar-strings-revisao-sistematica` para `auditoria-das-strings`:
  pasta, frontmatter `name`, descrição e remissões. Verificar com
  `grep -rn "otimizar-strings"` que só restam histórico, arquivo e tabela de correspondência.
- [x] 3.2 Renomear `busca-nas-bases` para `execucao-da-busca`: pasta, `name` e remissões.
  Verificar que o catálogo encontra a skill no passo “Executar expressões de busca”.
- [x] 3.3 Renomear `deduplicacao` para `controle-de-duplicatas`: pasta, `name` e remissões.
  Verificar que o catálogo a associa ao passo “Controlar duplicatas”.
- [x] 3.4 Renomear `filtragens` para `filtragem-dos-estudos`: pasta, `name` e remissões.
  Verificar que os três passos de filtragem continuam citando a skill.
- [x] 3.5 Renomear (C1) `ficha-de-busca-por-base` para `procedimento-de-busca-por-base`,
  atualizar o texto do guia/README e a chave `[documentos] ficha` para
  `[documentos] procedimento`, aceitando a chave antiga por uma rodada. Verificar que o
  leitor aceita as duas chaves e que a antiga sai da configuração do projeto.
- [x] 3.6 Remover o bloco `auditar_strings.py` de `auditoria-das-strings` e trocar as
  instruções por `strings gerar` e `documentos conferir`. Verificar que a skill não contém
  bloco de código Python executável e que as remissões aos comandos existem.
- [x] 3.7 Ajustar as descrições das skills renomeadas para conter o vocabulário do passo
  (executar busca, controlar duplicatas, filtrar estudos, auditar strings). Verificar que o
  catálogo associa cada uma ao passo correspondente.

## 4. Referências vivas

- [x] 4.1 Atualizar o `README.md`: comandos, exemplos e mapa; nenhuma citação de nome
  antigo. Verificar com `grep` e com o catálogo.
- [x] 4.2 Atualizar `docs/procedimentos.md`: todas as sinopses, a tabela de conferências
  transversais e as remissões de skill. Verificar que cada comando documentado roda como
  escrito.
- [x] 4.3 Atualizar as specs principais que citam comandos antigos. Verificar com
  `grep -rn` em `openspec/specs/` que só restam nomes canônicos.
- [x] 4.4 Atualizar os comentários do `config.toml`, as pendências vivas em
  `data/pendencias.json` e as mensagens do autoteste que citam comandos. Verificar que o
  histórico e as changes arquivadas não foram tocados.
- [x] 4.5 Regenerar `docs/catalogo_de_apoio.md` e rodar `catalogo gerar`; a conferência deve
  acusar zero nomes antigos em documento vivo. Verificar que a tabela de correspondência
  lista todos os aliases.
- [x] 4.6 Atualizar (C1) a chave de configuração e as referências ao conceito
  “procedimento de busca” no guia, README e código.
  Verificar que `conferir` e `conferir-dados` usam o caminho novo.

## 5. Integração e encerramento

- [x] 5.1 Rodar `documentos conferir` (0), `dados conferir` (5), `projeto autoteste`
  (6 PARCIAL, sem falha nova) e `catalogo gerar` (0). Registrar os códigos no relato.
- [x] 5.2 Rodar o autoteste com os casos novos e confirmar que cada um falha quando a
  conferência correspondente é desligada. Verificar que nenhum caso novo depende do registro
  de execução.
- [x] 5.3 Registrar a emenda no histórico com a skill `registrar-decisao`: namespace,
  aliases, skills renomeadas, C1 e remoção do script embutido. Verificar que a entrada
  cita a lista antigo → novo.
- [x] 5.4 Validar a change com `openspec validate namespace-de-comandos-e-skills --strict` e
  corrigir o que for apontado.
- [x] 5.5 Abrir a change de remoção dos aliases, com o critério “zero citações vivas” e a
  lista de aliases a remover. Verificar que a change nova cita esta como dependência.

## Workflow follow-up

- Arquivar esta change depois da revisão do pesquisador.
- A remoção dos aliases é a change seguinte; não faz parte desta.
- As skills `avaliacao-da-necessidade` e `busca-complementar` continuam como lacuna
  declarada até decisão do pesquisador.
- [x] 5.6 Corrigir as mensagens do programa que citavam aliases (`busca/fidelidade.py`,
  `busca/derivacao.py`, `gramatica.py`) e estender a varredura do catálogo a `src/rsl/`,
  com nome composto reconhecido sem prefixo (achado da verificação). Verificar que a
  varredura reprova cada uma das três mensagens antigas e que o autoteste tem casos que
  falham com a regra desligada e com as exclusões (flag, módulo) retiradas.
