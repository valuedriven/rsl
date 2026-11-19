# Tasks

## 1. Conferência do bloco executado

- [x] 1.1 Em `src/protocolo.py`, recusar referência a conjunto `#n` nos blocos das expressões com estatuto executada, fidelidade ou sonda, nomeando base e expressão; verificar que a conferência da WoS reprova o bloco atual `#5 AND (#3 OR #4) AND …` e que a da ERIC não reprova por esse motivo
- [x] 1.2 Conferir o conjunto de termos de cada bloco contra as strings das facetas que o `**Facetas:**` declara, ignorando operadores, prefixos de campo, parênteses, `NEAR/n`, `W/n` e valores de cláusula de filtro; verificar que a conferência reprova um termo alterado só na seção 3 e um termo estranho no bloco, e que aceita os valores de `DT=` e o operador de proximidade
- [x] 1.3 Estender o autoteste com os dois defeitos — `#n` devolvido ao bloco e termo defasado —, um por base, exercitar também um bloco de fidelidade e um de sonda, exigir as duas mensagens do termo defasado (termo ausente e termo estranho) e verificar que `python3 src/protocolo.py --autoteste` passa e que cada defeito reprova só a base afetada
- [x] 1.4 Recusar bloco na expressão derivada padrão, sem alcançar a forma longa, e provar no autoteste que só a base afetada reprova; verificar que as fichas correntes continuam aprovadas

## 2. Fichas da WoS e da Scopus

- [x] 2.1 Montar os blocos literais de EB2, EB3, EB4 e EB5 por substituição das strings da seção 3, sem digitar termo, e verificar que nenhum bloco contém `#n` e que o tamanho de cada um bate com a soma das facetas mais filtros (EB4 ≈ 9,9k na WoS e ≈ 10k na Scopus)
- [x] 2.2 Substituir as expressões pelos blocos literais nas duas fichas, remover o bloco da EB1 e retirar a subseção de âncoras em proximidade, levando a instrução de partição para *Variantes* e declarando que a emenda atualiza `- Execução: particionada` e escreve as partes literais; verificar que `python3 src/protocolo.py --conferir` aprova as duas bases
- [x] 2.3 Acrescentar na seção 1 a linha de comprimento máximo da consulta como **não verificado** e reescrever "Como executar" para submeter o bloco como está, sem definir conjuntos; verificar que a ficha não contém mais instrução de montagem nem `#n` em bloco de expressão

## 3. Ficha da BRAPCI

- [x] 3.1 Expandir EB4 e EB5 em blocos literais por substituição das strings da seção 3 e remover os blocos de EB1, EB2 e EB3, que são derivadas localmente; verificar `python3 src/protocolo.py --conferir` aprovando a BRAPCI
- [x] 3.2 Reescrever "Como executar" e a variante de partição para o bloco literal, mantendo a regra de teto de 1.000 registros e declarando que a emenda atualiza `- Execução: particionada` e escreve as partes literais; verificar que não resta instrução de "montar em arquivo por substituição"

## 4. Ficha da ERIC

- [x] 4.1 Rodar a conferência nova sobre a ERIC, que já tem blocos literais, e corrigir o que ela reprovar; verificar `python3 src/protocolo.py --conferir` aprovando a ERIC sem alterar nenhuma consulta

## 5. Skill da ficha

- [x] 5.1 Inverter em `.agents/skills/ficha-de-busca-por-base/SKILL.md` a regra da "segunda cópia" e atualizar o contrato de forma — bloco literal obrigatório nas expressões que se executam, subseção de âncoras não exigida; verificar por leitura que nenhuma passagem da skill manda montar por conjuntos ou apresentar `#n` como forma executável

## 6. Registro da decisão e pendências

- [x] 6.1 Registrar a decisão no `data/historico.md` com o alcance (forma de execução das quatro bases) e verificar que o registro nomeia a data e o que fica não verificado
- [x] 6.2 Reescrever PD07, PD08 e PD10 para o que resta medir — teto da consulta expandida e combinação de conjunto com filtros, onde ainda houver — e verificar que as três constam de `data/pendencias.json` com `estado: aberta`

## 7. Integração

- [x] 7.1 Rodar `python3 src/protocolo.py --conferir` e `python3 src/protocolo.py --autoteste` e verificar que as quatro bases passam e que os defeitos injetados reprovam
- [x] 7.2 Verificar que nenhuma execução registrada fica vencida — `data/registro_execucao.json` não existe — e registrar essa condição na entrega

## Workflow follow-up

- Criar `data/registro_execucao.json` e `data/execucoes/` (PD02) antes de registrar qualquer sonda.
- Sondar o teto de cada base com o bloco de EB5 e depois o de EB4; registrar aceitação, comprimento e retorno no registro de execução.
- Recusa por extensão: emenda que declara `- Execução: particionada` e escreve as partes literais, com as mesmas âncoras em todas e união por deduplicação.
- Arquivar a change depois da revisão; a aceitação das consultas continua não verificada até a sonda do pesquisador.
