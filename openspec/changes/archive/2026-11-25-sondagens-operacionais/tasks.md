# Tarefas

## 1. Gramática e validação da fonte

- [x] 1.1 Em `src/rsl/gramatica.py`, tornar `texto` opcional em `[[sondagens.consultas]]` e
  acrescentar `expressao`, `consulta`, `sem_proximidade` e `metade` (`faceta`, `parte`), com
  descrição, e a lista fechada de marcas de referência (design D7). Verificar:
  `python3 -m rsl documentos gramatica` mostra os campos novos e a exclusividade entre
  `texto` e `expressao`.
- [x] 1.2 Em `src/rsl/fonte.py`, validar a camada que depende só da fonte (design D2):
  exclusividade de `texto`/`expressao`, forma das transformações, `parte` ∈ {1, 2}, faceta
  existente, `sem_proximidade` só com proximidade declarada e marcas de referência em
  `texto`, com PROTOCOLO_ILEGIVEL nomeando sondagem e consulta. Verificar com uma cópia da
  fonte da Scopus, cuja SD4 tem a prosa atual: a leitura reprova, nomeando SD4, a consulta 1
  e `EB4`.
- [x] 1.3 Acrescentar ao autoteste um caso por recusa de 1.2 (spec: "Referência inválida
  reprova", "Consulta literal sem marca de referência"), inclusive o caso com a conferência
  de marcas desligada. Verificar: `python3 -m rsl projeto autoteste` passa, e cada caso falha
  com a validação correspondente desligada.

## 2. Resolução na composição e roteiro

- [x] 2.1 Em `src/rsl/procedimentos.py`, implementar `sem_proximidade` e `metade` como
  parâmetros da composição de uma expressão de consulta única (design D3). Também
  implementar a resolução de uma consulta de sondagem: expressão com bloco, `consulta` por
  id ou `mais_longa` com desempate pela ordem, transformação só em consulta única e
  reprovação quando o texto passa do `teto`. Verificar: resolução da WoS SD5 igual, caractere
  a caractere, ao texto de EB4 em `consultas_executaveis()`.
- [x] 2.2 Fazer `roteiro` receber a composição e renderizar a consulta por referência com a
  origem e o número de caracteres no rótulo e só o texto no bloco (design D5). Ajustar o
  chamador em `texto_procedimento`. Verificar: `python3 -m rsl procedimentos gerar wos`
  (ensaio) só muda o roteiro de sondagens.
- [x] 2.3 Acrescentar ao autoteste os casos de resolução: igual ao bloco da seção 4,
  `mais_longa`, `sem_proximidade` (difere do teste só no operador), `metade` (a união das
  partes é a string da faceta, em ordem) e cada referência inválida da camada de composição.
  Verificar: `python3 -m rsl projeto autoteste` passa, e cada caso falha com a resolução
  correspondente desligada.

## 3. Registro com o texto resolvido

- [x] 3.1 Em `src/rsl/sondagens.py`, montar a composição da base e gravar o literal resolvido
  de cada consulta antes de aplicar `--submetido` (design D6). Atualizar a docstring.
  Verificar no autoteste, numa cópia: o registro de uma sondagem com `expressao` grava o
  texto de EB, não a referência, e o caso falha se o registro gravar a referência.

## 4. Migração das fontes

- [x] 4.1 Migrar as 8 consultas para `expressao` (WoS SD5; Scopus SD2, com `sem_proximidade`
  no controle, e SD4; ERIC SD12 com `consulta = "mais_longa"`; BRAPCI SD4, com `metade` da
  faceta 🟦 nos controles). Reescrever os passos e pré-requisitos que mandavam copiar o bloco
  do procedimento gerado, sem mudar objetivo, leituras nem a pergunta de cada sondagem.
  Verificar: `procedimentos gerar <sigla>` (ensaio) das 4 bases sem erro, com a diferença
  revisada e restrita às sondagens migradas.
- [x] 4.2 Gravar os 4 procedimentos (`procedimentos gerar <sigla> --gravar`). Verificar: nenhum
  bloco de consulta de sondagem nos 4 procedimentos contém marca de referência (por
  `grep`), e `documentos conferir` termina com OK.

## 5. Integração

- [x] 5.1 Rodar `python3 -m rsl documentos conferir`, `python3 -m rsl dados conferir` e
  `python3 -m rsl projeto autoteste`. Verificar: os três terminam com OK, e os resultados já
  registrados da WoS (SD1 a SD3) continuam aceitos.
  Escopo acrescentado por decisão do pesquisador: o autoteste já tinha 7 falhas antes da
  change, vindas dos primeiros resultados reais da WoS. A regeneração do autoteste passou a
  usar o registro de execução (`registro_de_execucao`), como `procedimentos gerar`. O
  resultado fabricado por `registro_com_sondagem` passou a ser de uma sondagem ainda não
  verificada na fonte.
- [x] 5.2 Conferir se `docs/procedimentos.md` (sinopse de `sondagens registrar`) e a skill
  `executar-sondagens-de-sintaxe` (§4, §7) precisam mencionar a consulta por referência, e
  ajustá-las se precisarem. O guia é editado pelo pesquisador e tem alteração local não
  commitada, então partir da versão corrente. Verificar: `catalogo gerar` (ensaio) sem
  diferença inesperada.

## Workflow follow-up

- Arquivar a change depois da revisão do pesquisador e sincronizar a spec
  `sondagens-por-base`.
