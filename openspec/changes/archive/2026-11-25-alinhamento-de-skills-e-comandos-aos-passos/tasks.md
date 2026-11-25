# Tasks

## 1. Decisões abertas do design

- [x] 1.1 Reler cada skill e propor ao pesquisador a tabela final de nomes (design D5), com o passo
  principal de `filtrar-estudos` e os nomes novos de `src/rsl/conferencia.py` e `src/rsl/fichas.py`.
  Verificar: tabela confirmada pelo pesquisador e registrada no design.
- [x] 1.2 Inventariar as regras de `procedimento-de-busca-por-base`, `execucao-da-busca`,
  `auditoria-das-strings`, `revisao-geral-do-projeto` e `rastreabilidade`, com o destino de cada uma
  (design D6). Verificar: toda regra tem exatamente um destino; movimento que mude regra, e não só
  lugar, apresentado ao pesquisador antes de seguir.

## 2. Regras de papel e de âncora no catálogo

- [x] 2.1 Ler no guia os rótulos `Skill principal:` e `Script principal:` e rejeitar rótulo fora da
  forma (spec: Marca de principal no passo). Verificar: guia com `Skill (principal):` reprova na
  leitura, nomeando passo e rótulo.
- [x] 2.2 Substituir `PAPEIS` por principal, subordinada e transversal e ler a tabela "Skills
  subordinadas" (design D1, D3). Verificar: papel `artefato` reprova; skill sem papel reprova.
- [x] 2.3 Implementar as regras de âncora de skill, de subordinada e de comando (spec: Skill principal
  ancorada em um passo; Skill subordinada ligada à sua principal; Comando ancorado em um passo).
  Verificar com `python3 -m rsl catalogo gerar` sobre guias de prova para cada cenário da spec.
- [x] 2.4 Mostrar principal e apoio nas visões por passo, por skill e por comando, no arquivo gravado
  e no `--json`. Verificar: `catalogo gerar --json` traz o papel da citação em cada passo.
- [x] 2.5 Acrescentar ao autoteste um caso por regra nova, sobre o guia corrente (spec: Autoteste das
  âncoras). Verificar: `python3 -m rsl projeto autoteste` reprova cada injeção e, com a regra
  desligada, o caso falha.
- [x] 2.6 Migrar `docs/procedimentos.md`, ainda com os nomes atuais: marcar a principal de cada passo e
  os comandos principais (design D4), passar `documentos conferir`, `dados conferir` e
  `projeto autoteste` a apoio em "Montar o protocolo", citar `busca derivar` como apoio nos passos
  que alimenta, reescrever a seção "Papel das skills" e a descrição da forma do guia. Verificar:
  `catalogo gerar --gravar` e, em seguida, `catalogo gerar` saem OK.

## 3. Renomeação e fusão das skills

- [x] 3.1 Renomear as pastas e o `name` das skills pela tabela confirmada em 1.1, atualizando o guia
  na mesma tarefa. Verificar: `catalogo gerar` sai OK depois de `--gravar`.
- [x] 3.2 Fundir `revisao-geral-do-projeto` e `rastreabilidade` em `revisar-projeto`, transversal,
  dona das conferências transversais. Verificar: as regras inventariadas em 1.2 para as duas estão na
  skill nova, cada uma uma vez.
- [x] 3.3 Atualizar as remissões entre skills. Verificar: busca textual por cada nome antigo em
  `.agents/skills/` sem ocorrência.
- [x] 3.4 Atualizar o cenário da spec `catalogo-de-apoio` e as citações de skill no `README.md`.
  Verificar: busca textual por cada nome antigo em `README.md` e `openspec/specs/` sem ocorrência,
  salvo as que o delta desta change substitui.

## 4. Redistribuição de escopo

- [x] 4.1 Enxugar `gerar-procedimento-de-busca`, levando sintaxe e roteiro de sondagens, flexão,
  aplicação de critério, montagem de expressão e sementes às skills donas, com remissão de uma linha
  (design D6). Verificar contra o inventário de 1.2: nenhuma regra perdida nem duplicada.
- [x] 4.2 Levar o registro e a leitura de sondagem de `executar-expressoes-de-busca` para
  `executar-sondagens-de-sintaxe`. Verificar contra o inventário de 1.2.
- [x] 4.3 Levar o procedimento de auditoria geral de `gerar-strings-de-busca` para `revisar-projeto`,
  mantendo os 11 critérios na primeira. Verificar contra o inventário de 1.2.
- [x] 4.4 Ajustar a `description` de cada skill ao passo-âncora e ao papel. Verificar: toda
  `description` nomeia a atividade do passo principal (ou, na subordinada, a principal que
  complementa) e não promete atividade de outro passo.

## 5. Módulos

- [x] 5.1 Renomear `src/rsl/conferencia.py` e `src/rsl/fichas.py` (e `autoteste/fichas.py`) pelos
  nomes confirmados em 1.1 e atualizar os importadores (design D7). Verificar:
  `python3 -m rsl projeto autoteste` sem caso novo falho e `grep -rn "fichas\|from .conferencia"
  src/rsl` sem resíduo.

## 6. Citações fora do guia

- [x] 6.1 Atualizar as ações sugeridas e as origens de `data/pendencias.json` que citam skill, e a nota
  de estado corrente da fonte da ERIC; manter as notas datadas das fontes (design D8); regenerar os
  procedimentos se a fonte mudou. Verificar: `python3 -m rsl procedimentos gerar` sem diferença
  inesperada e `python3 -m rsl documentos conferir` OK.

## 7. Integração

- [x] 7.1 Executar `catalogo gerar`, `documentos conferir`, `dados conferir` e `projeto autoteste` e
  relatar o resultado no relato da change, separando falhas preexistentes das desta change.
- [x] 7.2 Busca textual por cada nome antigo de skill no repositório, fora de `openspec/changes/archive/`
  e das notas datadas mantidas em D8. Verificar: zero ocorrências, ou cada uma justificada no relato.

## Relato da aplicação (2026-11-25)

- **1.1 e 1.2.** Decisões do pesquisador registradas no design (Open Questions); inventário das
  regras em `inventario.md`, com o destino de cada uma e as quatro decisões D1–D4.
- **2.3.** Os onze cenários da spec rodados sobre cópias do guia em memória: cada um reprova com a
  mensagem que nomeia skill, comando ou passo; o guia corrente passa, e com ele o cenário "vários
  comandos principais no mesmo passo". O rótulo `Skill (principal):` termina com DADOS na leitura.
- **2.5.** Onze casos novos no grupo do catálogo; cada um reprova com a regra ligada e deixa de
  reprovar com ela desligada (o de rótulo fora da forma é de leitura, sem regra a desligar).
- **2.6.** `documentos gramatica` saiu da tabela de conferências transversais: é principal em
  "Preparar o protocolo de revisão (IO 1)" (D4), e a regra nova reprova comando transversal e
  principal ao mesmo tempo. O "quando executar" da tabela passou para a sinopse do passo.
- **3.3 e 7.2.** Busca textual por cada nome antigo. Ocorrências que ficam, cada uma justificada:
  - `openspec/specs/catalogo-de-apoio/spec.md:17` (`questao-e-objetivos`): o delta desta change
    substitui o cenário; sai na sincronização do arquivamento;
  - `auditoria-das-strings` nas notas datadas ("até 2026-11-23") das fontes de WoS, Scopus e ERIC
    e nos procedimentos gerados a partir delas: mantidas pelo D8;
  - `categoria: "conferencias-da-busca"` em `data/pendencias.json`: rótulo de categoria, que o
    código não lê, e não citação de skill;
  - "conjunto-semente", "fichamento" e "rastreabilidade" como substantivos comuns nas skills,
    nos documentos e nas specs; nenhuma ocorrência em forma de citação de skill.
- **5.1.** Resíduo de "fichas" em `src/rsl` fora dos módulos renomeados: a chave de configuração
  retirada `fichas` (`config.py`, `autoteste/configuracao.py`), que o leitor recusa e a spec
  `leitura-do-protocolo` cita, e deve ficar; a API do `Contexto` (`ficha()`, `com_fichas`,
  `_fichas`) e `relatorio.execucao_das_fichas`, resíduo do nome anterior ao C1 fora do D7, não
  renomeados nesta change.
- **6.1.** Além das ações sugeridas e origens, a descrição da PD27 e a nota da ERIC, ambas no
  presente, passaram a citar `executar-sondagens-de-sintaxe`, para onde a afirmação sobre o
  truncamento da ERIC foi levada (4.2). `procedimentos gerar` mostrou só essa diferença, na ERIC;
  as outras três bases saíram sem diferença. Registrada a PD32 (forward search, decisão D2).
- **7.1.** `catalogo gerar`: OK. `documentos conferir`: OK. `dados conferir`: DADOS,
  `data/registro_execucao.json` ausente — igual à linha de base, antes da change.
  `projeto autoteste`: 525 casos executados, 2 falhos, 9 não executados (registro de execução
  ausente). As 2 falhas são preexistentes: a linha de base, com as alterações desta change
  guardadas, tem as mesmas 2 em 504 casos:
  - "descritor decidido na linha de descritores" (classificação do controle terminológico);
  - "marcador de apoio sem razão" (catálogo): o caso troca só a primeira linha do `Apoio:` do
    primeiro passo, cuja razão continua na linha seguinte; a continuação devolve a razão e o
    defeito injetado não chega à conferência. Defeito do caso, não da regra.

## Ajustes da verificação (2026-11-25)

- **Guia.** "Gerar o procedimento de busca de cada base" movido para logo antes de "Validar o
  protocolo com pesquisador expert", com a sua parte da `Ordem`; passo de adaptação novo
  "Definir conjunto semente", após "Avaliar e definir as fontes de pesquisa"; topo do guia
  em 63 + 4 = 67. `compor-conjunto-semente` renomeada `definir-conjunto-semente` e passada a
  principal (decisão do pesquisador); remissões em skills e em `data/pendencias.json`
  atualizadas; delta da spec com os dois cenários que a citavam.
- **Coerência com a ordem nova.** Os passos da E1 anteriores à geração do procedimento deixam
  de citá-lo: "Elaborar as expressões" (§3 e §4 da Fonte e `gerar-procedimento-de-busca` como
  apoio), "Definir os critérios" (§2) e "Avaliar e definir as fontes" (§1 e a skill de apoio).
  Este último, sem skill nem script, passa a `Apoio: manual — escolha das fontes pelo
  pesquisador, registrada no protocolo`. As citações nos passos da E2, posteriores à geração,
  ficam.
- **Autoteste "marcador de apoio sem razão".** A injeção trocava só a primeira linha do
  `Apoio:`; `_troca_subitem` troca o subitem com as continuações, também nos casos vizinhos
  que usavam o mesmo alvo. O grupo do catálogo sai sem falha.
- **Autoteste "descritor decidido na linha de descritores".** Duas dependências do quadro
  corrente: a injeção substituía a célula de descritores (apagando `education`, que a STR2
  traz) e a planilha de prova não trazia a classificação já existente (descritores de FCT1
  cobrados como termo livre). A injeção passa a acrescentar o termo, e a planilha de prova
  parte da classificação corrente do protocolo. Antes da correção, o caso reprovava pela
  mensagem a mais — prova de que a asserção de exclusividade morde.
- **Resíduo "fichas".** `Contexto.ficha`/`com_fichas`/`_fichas` → `procedimento`/
  `com_procedimentos`/`_procedimentos`; `Config.ficha` → `procedimento`; chave interna
  `ficha` da base → `procedimento`; `relatorio.execucao_das_fichas` →
  `execucao_dos_procedimentos`. Ficam as chaves de configuração retiradas `fichas` e
  `documentos.ficha`, que o leitor recusa de propósito.
- **Resultado.** `catalogo gerar` OK; `documentos conferir` OK; `procedimentos gerar` sem
  diferença nas quatro bases; `projeto autoteste`: 525 executados, 0 falhas, 9 não executados
  (registro de execução ausente), código PARCIAL.

## Workflow follow-up

- Verificar a change (openspec-verify) e arquivá-la, sincronizando a spec `catalogo-de-apoio`.
- Não registrar em `data/historico.md`: a reestruturação é de instrumento, não arquitetural.
