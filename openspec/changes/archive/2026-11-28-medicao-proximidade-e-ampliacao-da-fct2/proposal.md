# Proposta

## Por quê

A aderência das execuções da WoS e da Scopus de 2026-11-25 é de 1/19 (5,3%), e a sonda EB5
recupera só 3 das 12 sementes esperadas nessas duas bases. Pela simulação sobre os metadados
da OpenAlex, o que mais derruba as sementes é a proximidade entre as âncoras (`NEAR/5`,
`W/5`): os termos de FCT1 e de FCT2 ficam a mais de cinco palavras um do outro. Isso é
inferência, não medida.

Depois disso, o pesquisador tomou duas decisões:

- **A exigência de FCT3 ∨ FCT4 passa para a triagem.** A emenda da EB4 fica para depois da
  decisão sobre a proximidade.
- **Os termos livres pt da FCT2 e da FCT3 mudam no protocolo.**
  - FCT2: `educacional`, `ensino`, `aprendizagem` e `ensino-aprendizagem`. Sai `ensino e
    aprendizagem`.
  - FCT3: `prática de ensino`, `prática instrucional`, `prática docente`, `técnica de
    ensino`, `técnica instrucional` e `técnica docente`, no lugar dos cinco termos
    anteriores.

O quadro está alterado só em pt. As linhas en e es ainda são as antigas, os termos novos não
passaram pela validação terminológica, e as strings e os procedimentos estão defasados:
`strings gerar` reprova. Falta, além disso, medir a proximidade com a FCT2 nova antes de
decidi-la. As consultas da medição se montam sobre a STR2, e por isso a medição vem depois
da regeneração.

## O que muda

- **Controle terminológico da FCT2 e da FCT3 completado** pelo caminho que o projeto já
  tem. Nenhuma etapa decide pelo pesquisador. A validação nos instrumentos, a proposta de
  descritores e a decisão do ReT acabaram suprimidas (ver Fora do escopo):
  - equivalentes en e es dos termos pt, propostos pelo agente e revisados pelo pesquisador;
  - validação dos termos novos nos instrumentos que o protocolo atribui à faceta e ao idioma;
  - proposta de descritores, a partir da evidência; o ReT decide na planilha;
  - linhas do quadro conforme a `decisao_ReT`;
  - exceções de flexão dos termos novos e retirada das que ficaram sem termo;
  - registro no histórico.
- **Strings e procedimentos regenerados** nas quatro bases, na ordem do README. Nas fontes da
  ERIC, a lista própria da STR2 é conferida contra a STR2 nova.
- **Duas transformações novas na consulta por referência:**
  - `distancia = N`: a proximidade das âncoras com outra distância;
  - `restricao = { termos }`: um grupo unido por `AND`, no campo das âncoras, que conta uma
    parcela do retorno (o ruído). Os termos vêm marcados no roteiro como **fora do
    protocolo**.
- **Sondagem da grade na WoS e na Scopus,** sobre a EB5 já com a FCT2 nova:
  - o controle, com a proximidade declarada;
  - a distância 15;
  - `AND` entre as âncoras;
  - a contagem de ruído sobre a forma com `AND`.

  Os retornos entram no registro de execução por `sondagens registrar`.
- **Diagnóstico sem mistura de vocabulários.** `aderencia diagnosticar` só lê um nível de
  execução registrada quando o texto registrado é o vigente; com as strings alteradas
  depois da execução, ou sem texto registrado, o nível vai ao roteiro, com o motivo.
- **Restrição por DOI declarada na fonte da WoS** (`[composicao] doi`, com `DO=`). Com ela,
  `aderencia diagnosticar wos` deixa de recusar.

Fora do escopo:

- **A validação dos termos novos nos instrumentos, a proposta de descritores e a decisão do
  ReT:** suprimidas por decisão do pesquisador (histórico, 2026-11-28). Os termos ficam livres.
  A validação vai para a change geral de otimização das consultas terminológicas (PD41).
- **A emenda da EB4 e das notas N3 e N4,** que leva FCT3 ∨ FCT4 para a triagem, e o
  encerramento da PD38: vão para a change seguinte, com a decisão sobre a proximidade.
- **A FCT1 e a FCT4,** cujos quadros não mudam.
- **As execuções definitivas e o novo teste de aderência** (PD31).

## Capacidades

### Novas capacidades

Nenhuma.

### Capacidades modificadas

- `anatomia-da-perda`: o requisito "Nível lido da execução registrada" passa a exigir que
  o texto registrado da execução seja o vigente; sem isso, o nível vai ao roteiro, com o
  motivo.
- `sondagens-por-base`: o requisito "Transformações declaradas da referência" ganha
  `distancia` e `restricao`, e os termos de `restricao` aparecem marcados no roteiro. O
  requisito "Referência inválida reprova" ganha os casos inválidos das duas.

A validação, a geração das strings e a dos procedimentos não mudam de comportamento: mudam
os dados que elas processam.

## Impacto

- **Protocolo:** linhas en e es da FCT2 e da FCT3, as linhas de descritores conforme a
  decisão do ReT e a tabela "Strings de busca por faceta", esta regenerada.
- **Dados:**
  - `data/validacao_terminologica.csv` e a evidência em `data/evidencia/<instrumento>/`;
  - `docs/flexoes.toml`;
  - as fontes das quatro bases, com a sondagem nova e o `doi` na WoS;
  - os quatro procedimentos, regenerados;
  - `data/historico.md`.
- **Código:** a gramática das consultas de sondagem e a composição das consultas por
  referência; o autoteste.
- **Rede:** consultas aos serviços TemaTres dos instrumentos, uma por vez, sem nova
  tentativa automática.
- **Pendências:**
  - a PD31 continua: as execuções de 2026-11-25 ficam anteriores às STRs novas;
  - a PD38 perde o objeto e se encerra na change da emenda.
