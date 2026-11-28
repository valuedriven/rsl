# Tarefas

## 1. Transformações novas na consulta por referência

- [x] 1.1 Na gramática das consultas de sondagem, acrescentar os campos opcionais `distancia`
  (inteiro) e `restricao` (tabela com `termos`). Verificar: `documentos gramatica` mostra os
  dois, e uma fonte sem eles gera o mesmo texto de antes. As sondagens existentes da Scopus e
  da BRAPCI, com `sem_proximidade` e `metade`, saem idênticas no ensaio de `procedimentos
  gerar`.
- [x] 1.2 Na composição da consulta por referência, aplicar `distancia` e `restricao` sobre
  as âncoras e os grupos, e não sobre o texto final, combinando-as com `sem_proximidade` e
  `metade` (spec `sondagens-por-base`: "Transformações declaradas da referência"; design D6).
  Verificar: há um caso no autoteste para cada cenário do requisito. Cada caso falha com a
  transformação desligada.
- [x] 1.3 Implementar as recusas novas de "Referência inválida reprova". Verificar: um caso no
  autoteste para cada item novo da lista, com PROTOCOLO_ILEGIVEL e o nome da sondagem, da
  consulta e da transformação. O caso da distância igual à da base falha quando a conferência
  de transformação nula é retirada.
- [x] 1.4 No roteiro, nomear cada transformação na origem da consulta e listar os termos de
  `restricao` com a marca "fora do protocolo". Verificar: o caso do autoteste confere a marca
  e falha sem ela.
- [x] 1.5 Conferir que `sondagens registrar` grava, na consulta transformada, o literal
  resolvido no momento do registro. Verificar: um caso no autoteste registra uma consulta com
  `restricao` e confere os termos no texto gravado.
- [x] 1.6 Provar no autoteste o cenário "Strings alteradas depois da declaração": com as
  strings alteradas, as consultas com `distancia` e com `restricao` acompanham a composição,
  sem edição da fonte, e a transformação continua aplicada. Verificar: os dois casos passam e
  falham com a consulta congelada no texto anterior.

## 2. Controle terminológico da FCT2 e da FCT3

- [x] 2.1 Apresentar ao pesquisador os equivalentes en e es do design D1, a lista dos termos
  en e es que saem e a colisão `teaching practice` × `teacher practice`. Depois da revisão
  dele, gravar as linhas "Termo livre" en e es da FCT2 e da FCT3 no protocolo. Verificar: a
  linha gravada é a aprovada, e as linhas pt e de descritores ficam como o pesquisador as
  deixou (`git diff` do protocolo).
- [x] 2.2 Rodar `termos importar`, para reconciliar a planilha de validação com o quadro.
  Verificar: os termos novos aparecem sem estatuto, as decisões anteriores ficam preservadas,
  e nenhuma linha se apaga.
Fora do escopo por decisão do pesquisador (`data/historico.md`, 2026-11-28): a validação dos
termos novos (antigas 2.3 a 2.5) foi suprimida nesta change, depois que o serviço TemaTres
passou a recusar a conexão do cliente Python. Os termos ficam livres e assim se declaram.
A consulta pelo navegador, a importação das respostas e a lista para o ReT vão para a change
geral de otimização das consultas terminológicas (PD41). Nada disso foi feito aqui.

- [x] 2.6 Propor as exceções de flexão do design D4: os não contáveis novos e a retirada das
  exceções sem termo no quadro. Gravar depois da revisão do pesquisador. Verificar:
  - `strings gerar`, em ensaio, mostra para a FCT2 só as formas singulares dos não contáveis,
    e para a FCT3 o singular e o plural;
  - `documentos conferir` não acusa exceção sem termo.
- [x] 2.7 Registrar no histórico, com a skill `registrar-decisao`, as decisões arquiteturais
  desta etapa:
  - os termos novos da FCT2 e da FCT3 e os que saíram;
  - os equivalentes aprovados;
  - a supressão da validação desses termos.

  A entrada não leva contagem. Verificar: a entrada nomeia os termos e o alcance
  (**busca**), e o pesquisador a revisou.

## 3. Strings, fontes e procedimentos

- [x] 3.1 Rodar `strings gerar`, revisar o ensaio e depois `strings gerar --gravar`.
  Verificar: o ensaio sai sem termo a acrescentar nem a retirar, e a STR2 tem `ensino` e
  `aprendizagem` e não tem `ensino e aprendizagem`.
- [x] 3.2 Levar ao pesquisador a escolha do design D5 sobre `learner` e `learners` na lista
  própria da STR2 da ERIC, e aplicá-la na fonte da ERIC. Verificar: a lista da fonte é a
  escolhida, e o relato da tarefa registra a escolha.
- [x] 3.3 Na fonte da WoS, declarar `[composicao] doi = "DO=({doi})"`, com a cautela da PD40
  no roteiro do diagnóstico (design D8). Verificar: `aderencia diagnosticar wos` deixa de
  recusar e imprime os níveis, e nenhum arquivo de `data/` muda (`git status`).
- [x] 3.4 Na fonte da WoS e na da Scopus, declarar a sondagem da grade do design D7, a
  seguinte da sequência de cada base, com `elementos = []`. Verificar: a leitura das duas
  fontes sai sem PROTOCOLO_ILEGIVEL, e a sondagem é relatada como sem elemento.
- [x] 3.5 Regenerar os quatro procedimentos: `procedimentos gerar <sigla>` em ensaio,
  revisado, e depois `--gravar`. Verificar:
  - os blocos de EB1 a EB5 trazem as STRs novas;
  - a consulta 1 da grade é idêntica ao bloco de EB5 da §4;
  - as consultas 2 e 3 diferem dela só no operador entre as âncoras;
  - nenhuma consulta passa do teto de caracteres que `documentos conferir` relata. A que
    passar se registra como achado, sem encurtar a string.

## 4. Diagnóstico sem mistura de vocabulários

- [x] 4.1 Em `aderencia diagnosticar`, ler um nível de execução registrada só quando o texto
  registrado é o vigente da expressão; sem texto, ou com texto diferente, o nível vai ao
  roteiro, com o motivo (spec `anatomia-da-perda`: "Nível lido da execução registrada";
  design D9). Verificar:
  - na WoS, os níveis 4 e 5 saem "a submeter", com texto diferente do vigente;
  - na Scopus, saem "a submeter", sem texto registrado;
  - no autoteste, o caso falha com a conferência desligada, e os casos anteriores, com o
    texto vigente no registro sintético, continuam lendo os níveis 4 e 5.

## 5. Integração

- [x] 5.1 Rodar `projeto autoteste`, `documentos conferir` e `catalogo gerar`. Verificar: os
  três saem OK.
- [x] 5.2 Rodar `aderencia ensaiar` e relatar, por semente, as facetas encontradas com o
  quadro novo, marcando o resultado como ensaio sobre os metadados da OpenAlex, e não como
  recuperação. Verificar: o relato traz a composição de EB5 e de EB4 nas sementes, antes e
  depois do quadro novo.

## Workflow follow-up

- O pesquisador submete, no navegador e com o acesso institucional dele, uma consulta por
  vez:
  - na WoS e na Scopus, a sondagem da grade;
  - na Scopus, os níveis 1 a 3 do diagnóstico;
  - na WoS, se quiser, os níveis do diagnóstico.

  Ele registra com `sondagens registrar <sigla> <SDn>` e `aderencia diagnosticar <sigla>
  --retorno …`, com a evidência em `data/evidencia/sondagens/<sigla>/`.
- Relatar, por base:
  - os retornos da grade;
  - o limite inferior do ruído;
  - a comparação com a EB5 de 2026-11-25, que mistura a FCT2 e a data;
  - o teto de aderência do ensaio, como inferência.

  É a base da decisão sobre a proximidade.
- Abrir a change da emenda: proximidade, EB4 com FCT3 ∨ FCT4 levada para a triagem, notas N3
  e N4, encerramento da PD38, e depois as execuções definitivas (PD31).
- Arquivar esta change e sincronizar a spec `sondagens-por-base`.
