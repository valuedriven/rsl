# Design

## Context

- **Estado atual.**
  - O procedimento de busca de cada base é um markdown autoral, lido por `src/rsl/fichas.py`
    por meio de um contrato de forma: cabeçalhos exatos, campo reconhecido pelo prefixo do
    texto (`TS=`, `abstract:`), filtros reconhecidos por expressão regular e subseções
    ignoradas pelo título.
  - `cobertura.py` confere o procedimento contra a STR, e `dados.py` confere a citação
    `(BDn/<id>)` contra `bases.BDn.execucoes` do registro de execução.
- **Os quatro procedimentos têm o mesmo esqueleto**, com seções 1 a 6. Quase metade do
  conteúdo é derivável:
  - o título;
  - o mapa das facetas;
  - as strings;
  - a composição e as expressões;
  - os IDs dos critérios;
  - a tabela de sementes;
  - o texto fixo de execução, fidelidade, sensibilidade e retorno zero.

  O resto é conhecimento da base: sintaxe e o seu estado, destino dos critérios, regras de
  montagem, variantes, como executar, observações de semente e ressalvas.
- **Proveniência da sintaxe medida.** O conteúdo sobre o comportamento das bases, como as
  regras de montagem da ERIC, foi preenchido pelo agente a partir de sondagens que o
  pesquisador executou sob orientação. O pesquisador informou em 2026-11-23 que as
  verificações e sondagens da ERIC já foram feitas. Nenhuma está no registro de execução,
  que ainda não existe, e a decisão de 2026-11-19 do histórico rebaixou essas medições a
  "Não verificado" por falta de dado que as sustentasse. Por isso há afirmações de medição
  sem lastro e contradições entre seções. Por exemplo:
  - a seção 4 da ERIC diz "regras medidas", e a seção 1 marca os mesmos elementos como não
    verificados;
  - a skill `execucao-da-busca` afirma que `ontolog*` devolve 0 na ERIC, e o procedimento
    dá o truncamento como não verificado.
- **Forma curada:** o leitor a suporta, mas nenhum procedimento atual a usa. A versão
  anterior desta change dizia que a BRAPCI usava forma curada, o que estava desatualizado.

## Goals / Non-Goals

**Goals:**
- Um procedimento por base inteiramente reprodutível a partir de fontes que se editam,
  com a forma uniforme por construção.
- O conhecimento próprio da base declarado como dado, quando é dado, e como fragmento,
  quando é prosa.
- O que o pesquisador deve testar em cada base descrito como roteiro executável, ligado ao
  elemento que verifica e ao resultado registrado.
- O plural completo por construção, onde a base o declara explícito.

**Non-Goals:**
- Gerar o conteúdo autoral, como a variante, o como executar ou a ressalva. O gerador o
  posiciona e o formata; quem o escreve é o agente ou o pesquisador.
- Comando que altere a fonte a partir do resultado registrado. `sondagens registrar` só
  grava o registro e exibe a mudança a aplicar: a fonte se edita pelo agente ou pelo
  pesquisador, e a biblioteca padrão do Python não escreve TOML preservando comentários.
- Truncamento automático e morfologia completa.

## Decisions

**D1. Procedimento como saída, fonte por base (alternativa B).** Decisão do pesquisador,
2026-11-23. Substitui a ficha mista.

```
protocolo (STR, EB, CE, bases) --+
arquivo de sementes -------------+
docs/flexoes.toml ---------------+--> procedimentos gerar --> docs/procedimentos_busca_<sigla>.md
docs/procedimentos/<sigla>/      |                            (saída; não se edita)
  procedimento.toml (dados) -----+
  *.md (fragmentos de prosa) ----+
```

- **Alternativas descartadas:**
  - **ficha mista:** a forma diverge onde o gerador não alcança, e o contrato frágil de
    leitura do markdown continua;
  - **fonte única em TOML (A):** prosa longa em cadeia TOML é ruim de revisar, e a prosa é
    justamente a parte que mais se edita.
- **Consequência (AGENTS §3).** Altera-se a fonte, não a saída. O README declara o
  procedimento como saída e a ordem: quadro → `strings gerar` → `procedimentos gerar` →
  `documentos conferir`.

**D2. Forma da fonte.** `docs/procedimentos/<sigla>/`, localizada por `[documentos]
procedimento_fonte = "docs/procedimentos/{sigla}"`.

- **`procedimento.toml`.** O esquema está na gramática; nenhum valor de base fica no código.

  | Tabela | Campos | Vai para |
  | --- | --- | --- |
  | `[[sintaxe]]` | `elemento`, `categoria` (categorias mínimas da gramática), `idioma` (só em `lematizacao`), `situacao` (`oficial`, `secundaria`, `medicao`, `nao_verificado`, `inexistente`), `fonte`, `citacao` (`BDn/<id>`, exigida em `medicao`), `sondagem` (`SDn`) ou `sem_sondagem` (motivo), `nota` | §1, tabela |
  | `[[criterios]]` | `ids` (`["CE1","CE2"]`), `rotulo`, `destino` (`consulta`, `interface`, `variante`, `aproximado`, `dispensado`, `nao`), `como`, `clausula` (sintaxe do filtro, quando `consulta` ou `variante`) | §2 e filtros dos blocos |
  | `[cobertura]` | `idiomas` por faceta, `camadas`, `plural` (único ou por idioma), `teto`, `derivacoes` | §3, declaração |
  | `[[reducao]]` | `faceta`, `termo`, `motivo` | §3, redução |
  | `[composicao]` | por faceta (`[[composicao.facetas]]`): `faceta`, `campo`, `forma` (`envolve` ou `prefixa`) e `rotulo` (opcional); `aspas` (`todo_termo` ou `locucao`); `proximidade` (`operador`, `distancia`, ou `nenhum`); `disjuncao` (`em_linha` ou `consultas_separadas`, decisão de 2026-11-23) | blocos |
  | `[[consultas_de_campo]]` | `letra`, `faceta`, `string` (`STRn` ou subconjunto), `campo`, `rotulo` | partes `2a1`, `2b1`… |
  | `[[subconjuntos]]`, `[[radical]]` | `id` (`STR1b`), `faceta`, `campo`, `termos`, `rotulo` | §3, strings extras |
  | `[execucao]` | `forma` (`unica`, `particionada`, `curada`); por expressão, `estatuto`, só quando difere do papel lido do protocolo | §4 |
  | `[[regras_de_montagem]]` | `texto`, `situacao`, `sondagem` ou `citacao` | §4, "Como esta base exige a montagem" |
  | `[[curadas]]` | `grupo`, `consulta`, `facetas` (`FCTn`) | §4, forma curada |
  | `[[sementes]]` | `id`, `observacao` | §5, coluna Observação |
  | `ressalvas` | lista de textos | §6 |
  | `[[sondagens]]` | ver D5 | §1, roteiro |

- **Fragmentos de nome fixo.** Todos são opcionais, salvo `como_executar.md`:

  | Fragmento | Posição no procedimento |
  | --- | --- |
  | `notas_sintaxe.md` | §1, depois da tabela (regra de execução, campos auxiliares) |
  | `estrategia_de_proximidade.md` | §4, subseção própria |
  | `como_executar.md` | §4, "Como executar" |
  | `variantes.md` | §4, "Variantes previstas"; títulos só em `####` |
  | `notas_execucao.md` | §4, depois das linhas fixas de execução |
  | `notas_sementes.md` | §5, depois do limiar |

  O fragmento não pode ter título de nível 1 a 3, nem `####` fora de `variantes.md`, nem a
  linha `- Execução:`. Violação reprova com PROTOCOLO_ILEGIVEL, nomeando fragmento e linha.
  Fragmento de nome desconhecido na pasta também reprova: um nome errado não pode sumir em
  silêncio.
- **Categorias mínimas.** Cada elemento de sintaxe tem `categoria`, e cada uma destas tem ao
  menos um elemento por base, ainda que `inexistente`: `campos`, `operadores`, `frase`,
  `truncamento`, `lematizacao`, `proximidade`, `agrupamento`, `limite_consulta`,
  `limite_retorno`, `limite_exportacao`, `filtros`, `vocabulario_controlado`,
  `idioma_indexacao` e `exportacao`. É a lista "elementos a apurar, todos" da skill, que passa
  a ser forma declarada na gramática: um recurso esquecido reprova por construção, em vez de
  depender da releitura. A regra do plural pela lematização se lê pela categoria, e não pelo
  nome do elemento.
- **Marca `PENDENTE`.** Um campo ou uma linha de fragmento com `PENDENTE` reprova a leitura
  da base e lista todas as marcas de uma vez. Uma fonte incompleta não gera procedimento.
- Os **rótulos dos critérios** e o **estatuto** das expressões ficam na fonte porque o
  protocolo não os escreve na forma do procedimento. Os **IDs** continuam conferidos contra o
  protocolo.

**D3. Esqueleto e texto fixo no gerador, como forma.**
- O esqueleto (títulos, ordem, separadores, colunas) e o texto fixo são forma. Ficam
  declarados uma vez, no módulo da gramática ou num modelo junto dele. Esse texto fixo é:
  - a frase "Lida por…";
  - as linhas de fidelidade, sensibilidade e retorno zero;
  - o procedimento em duas etapas e o limiar do conjunto-semente.
- O texto fixo é **condicionado ao dado**:
  - a linha de fidelidade só sai quando alguma expressão tem o estatuto de fidelidade
    executada;
  - a de sensibilidade, só quando a sonda é executada.

  Parâmetro do projeto, como limiar e nome de configuração, entra por remissão ao
  `configuracao mostrar`, como hoje, e nunca como valor.
- O texto específico da base entra por fragmento (`notas_execucao.md`). Não há
  sobrescrita do texto fixo: a ressalva da BRAPCI sobre retorno zero passa a nota
  complementar.
- **Números calculados** (quantidade de consultas, de partes) não entram em prosa. O rótulo
  "parte k de n" das partições continua, porque o gerador o calcula e ele não pode ficar
  defasado.

**D4. Composição, ordem, partição e flexão** (mantidas da versão anterior):
- os blocos de string seguem a ordem da STR, com a flexão logo depois de cada termo e o
  termo repetido entrando uma vez;
- o bloco de expressão é a composição do protocolo, com cada grupo entre parênteses, a
  proximidade entre as âncoras e os filtros tirados de `criterios.clausula` com `destino =
  consulta`;
- **partição pelo teto:** parte-se o grupo OR da faceta não âncora de maior comprimento, em
  partes contíguas; as âncoras ficam íntegras; a união dos termos das partes é conferida;
  âncoras que sozinhas passam do teto reprovam; `forma = unica` com partição necessária
  também reprova. Com consultas de campo, a partição se faz dentro de cada uma, com rótulos
  `<n><letra><k>` (`2a1`);
- **flexão por regra de pt, en e es, com exceções e recusa do indecidível:** é a D5
  anterior, com o mesmo núcleo, as mesmas regras e as mesmas terminações indecidíveis;
- **arquivo de exceções:** `docs/flexoes.toml`, `[documentos] flexoes`, com
  `irregular`, `nao_contavel` e `vetada` e `origem` obrigatória. A heurística
  `_PLURAIS_IRREGULARES` sai de `cobertura.py`;
- **plural por idioma:** a linha "Lematização" com estado por idioma; a medição é uma
  sondagem do roteiro (D5).

**D5. Roteiro de sondagens.** Para o pesquisador, a sondagem é um **procedimento de teste
executável**, não uma frase.

- **Campos de cada `[[sondagens]]`:**
  - `id`: `SDn`, em sequência por base;
  - `elementos`: nomes de `[[sintaxe]]` ou de `[[regras_de_montagem]]`;
  - `objetivo`: a pergunta que a sondagem responde, em uma frase;
  - `pre_requisitos`: sessão, tela, campo e opção da interface;
  - `[[sondagens.consultas]]`: `papel` (`teste` ou `controle`), `texto` literal, `onde`
    (caixa, campo, filtro), e o que muda em relação ao controle;
  - `passos`: lista ordenada;
  - `observar`: retorno exibido, mensagem, destaque no registro, texto que a interface
    reescreveu;
  - `[[sondagens.leituras]]`: `resultado` (condição observável), `conclusao` e `estado`
    (o valor de `situacao` que o elemento passa a ter). Pelo menos duas leituras, e uma
    delas tem de cobrir o resultado inconclusivo;
  - `evidencia`: o que registrar, como contagem, captura, texto submetido e data e hora;
  - `depende_de`: outras sondagens, como "aspas como frase" antes de "proximidade com
    frase".
- **Escrita no procedimento:**
  - a §1 ganha a coluna "Sondagem" na tabela;
  - a subseção `### Sondagens a executar` traz cada `#### SDn — <objetivo>`, com
    pré-requisitos, consultas em bloco cercado (com papel), passos, o que observar, uma
    tabela de leitura (resultado, conclusão, estado) e a evidência;
  - abre a subseção uma linha fixa de segurança (AGENTS §9): uma consulta por vez, sem
    nova tentativa automática, parada diante de captcha ou bloqueio;
  - as sondagens saem na ordem de `depende_de`.
- **Validações da fonte**, que reprovam a base com PROTOCOLO_ILEGIVEL:
  - elemento `nao_verificado` sem `sondagem` nem `sem_sondagem`;
  - `sondagem` que não existe;
  - sondagem sem consulta, com menos de duas leituras, sem leitura inconclusiva ou sem
    evidência;
  - leitura com `estado` fora do domínio;
  - ciclo em `depende_de`.
- A sondagem **sem elemento** é relatada, sem reprovar.
- **Registro do resultado por comando:** `sondagens registrar <sigla> <SDn> --retorno …
  --leitura k --data-hora … --evidencia …`.
  - Os retornos vêm na ordem das consultas declaradas. O texto submetido é o declarado,
    salvo `--submetido k`.
  - `--data-hora` é obrigatório, sem padrão "agora", ao contrário de `busca registrar`:
    sondagem costuma ser registrada depois de feita (é o caso da ERIC), e a data presumida
    seria falsa.
  - `--evidencia` é obrigatório, e o arquivo tem de existir: sondagem sem evidência não é
    sondagem (`execucao-da-busca`).
  - O comando grava só o registro e exibe, por elemento, a `situacao` e a `citacao` a
    aplicar na fonte. `dados conferir` relata o resultado ainda não incorporado.
  - O resultado fica em `data/registro_execucao.json`, `bases.BDn.sondagens[]`, com:
    - `id` (o identificador citável);
    - `sondagem` (`SDn`);
    - `data_hora`;
    - `consultas` (texto submetido e retorno);
    - `leitura` (a leitura escolhida);
    - `evidencia` (caminhos);
    - `observacao`.
  - A citação `(BDn/<id>)` passa a resolver em `execucoes` ou em `sondagens`.
  - `dados conferir` reprova o resultado cujo `sondagem` não existe na fonte da base.
- **O que impede o defeito encontrado.**
  - O estado `medicao` exige `citacao` resolvida.
  - Uma regra de montagem com `situacao = medicao` exige `citacao`.
  - Por isso, "regras medidas" sem lastro não podem mais ser geradas.

**D6. Conferência por igualdade e sobre a fonte.**
- `documentos conferir`, por base:
  1. lê a fonte;
  2. gera em memória;
  3. reprova se o arquivo gravado difere, nomeando a base e `procedimentos gerar <sigla>
     --gravar`.
- As conferências de `cobertura-por-base` passam a ler a estrutura derivada da fonte, e
  não o markdown. Continuam valendo como invariantes da geração e sobre o que é autoral
  (forma curada, subconjuntos, radical):
  - o termo deriva da STR;
  - os termos do bloco conferem com as facetas;
  - a composição segue o protocolo;
  - o teto;
  - os critérios conferem com o protocolo;
  - o termo só no singular.
- O reconhecimento por texto de campo (`TS=`, `abstract:`) e de filtro (`PY=`, `LA=`) sai.
  O campo e o filtro vêm de `[composicao]` e de `criterios.clausula`.
- A citação `(BDn/<id>)` se procura em todo texto da fonte, inclusive nos fragmentos.

**D7. Transcrição provada e uniformização aprovada.** O pesquisador aprovou a
uniformização em 2026-11-23.
- A migração transcreve as quatro bases para a fonte. A prova tem duas partes (decisão do
  pesquisador, 2026-11-23, que substitui a prova com a flexão desligada: os plurais escritos
  à mão hoje não estão na STR, e a flexão desligada não os reproduziria):
  1. **Fora dos blocos de termos**, a diferença entre o ensaio de `procedimentos gerar` e o
     arquivo atual tem de ser só a da lista de uniformização aprovada.
  2. **Em cada bloco**, comparado como conjunto de termos com a flexão ligada, só pode haver
     acréscimo de forma flexionada (por regra ou por exceção), nunca perda de termo. A
     partição e a ordem dos termos ficam livres.

  A lista de uniformização aprovada:
  - o formato do título das EB;
  - a coluna de fonte na §1;
  - o separador antes da §4;
  - "em 13 consultas";
  - a frase de forma da §3 da ERIC;
  - o DOI da SE1;
  - a linha de sensibilidade da ERIC;
  - a coluna "Sondagem";
  - a regra de montagem como tabela;
  - o roteiro de sondagens e a coluna de categoria, que entram como conteúdo novo.
  - o rótulo das consultas: o `rotulo` da consulta de campo e, com `disjuncao =
    "consultas_separadas"`, "<rótulo da consulta de campo> × <rótulo da faceta>" (aprovação
    de 2026-11-23);
  - na ERIC (aprovação de 2026-11-23, revisada sobre o ensaio): o aviso de saída gerada no
    topo; a nota da §1 depois da tabela; "Não medido" e "Não localizados" como `nao_verificado`;
    a linha dos tetos partida por categoria; os elementos novos das categorias mínimas; CE1/CE2
    com destino `interface` e CE7/CE8 com `ancora`; a perda das linhas "*No título.*"/"*No
    resumo.*" e as frases fixas novas da §3; na §4, a frase "Regras medidas" retirada, a linha
    de composição em bloco, as frases de estatuto fixas e "Como executar" sem contagem de
    consultas; as formas acrescentadas `knowledge organizations`, `pedagogies`, `instructional
    designs`, `contextualizations` e `contextualisations`.
  - na WoS, na Scopus e na BRAPCI (aprovação de 2026-11-23): o aviso de saída gerada; as
    colunas Categoria e Sondagem; a frase de abertura da §3 sem "Uma string por faceta." (WoS)
    e sem "Flexões de número explícitas, sem truncamento." (BRAPCI); a frase da declaração; o
    "desta base" retirado da Etapa 1 (WoS); na BRAPCI, a linha EB1/EB2/EB3 unificada e as
    linhas fixas de Sensibilidade e Retorno zero ao lado do parágrafo próprio da base.
  - perda de `teaching-learning` (WoS e Scopus, escrito à mão fora da STR): resolvida pela
    inclusão do termo no quadro e na STR2 (decisão do pesquisador de 2026-11-23).
  - substantivos de processo ou de área (ensino superior, aprendizagem online, modelagem
    conceitual, educación, education e afins) são não contáveis em pt, es e en (decisão do
    pesquisador de 2026-11-23); as formas inglesas já aprovadas na ERIC ficam.
- Diferença fora da lista interrompe a migração e vai ao pesquisador.
- Contradição de verificação, como "medida" contra "não verificado" ou uma afirmação de
  skill contra o procedimento, **não se resolve na transcrição**. A situação transcrita é a
  mais conservadora (`nao_verificado`), a sondagem correspondente entra no roteiro, e a
  contradição vai a `data/pendencias.json` com a origem.
- **ERIC: sondagens refeitas.** Decisão do pesquisador, de 2026-11-23: as sondagens da ERIC
  serão refeitas, em vez de se registrarem as antigas, que não têm evidência no repositório.
  - Na migração, todo elemento e toda regra de montagem da ERIC dados como medidos entram
    como `nao_verificado`, com a sondagem no roteiro. É coerente com a decisão de
    2026-11-19, que rebaixou a medição sem lastro.
  - O agente não reconstrói retorno, data nem consulta das sondagens antigas, nem a partir
    da memória, nem da prosa atual do procedimento.
  - O pesquisador executa as sondagens pelo roteiro gerado, e cada resultado se registra
    por `sondagens registrar`. Só então o elemento passa a `medicao`, com citação.
  - A PD09 se resolve quando as sondagens que ela exige estiverem registradas.

**D8. Skills.**
- `procedimento-de-busca-por-base` é reescrita:
  - o agente escreve a fonte e gera; nunca edita o procedimento;
  - o "Contrato de forma" dá lugar à remissão a `documentos gramatica`;
  - o Passo 1 passa a produzir `[[sintaxe]]` e `[[sondagens]]`.
- `sondagens-de-sintaxe` é nova e metodológica. Não nomeia base nem ensina comando. Cobre:
  - uma variável por vez;
  - o par teste e controle, com o controle de retorno conhecido;
  - a leitura que distingue as hipóteses, inclusive "zero sem erro", que é ambíguo;
  - o tamanho mínimo que expõe o comportamento;
  - a evidência que torna o resultado auditável;
  - a passagem do resultado ao estado;
  - o que não se infere de uma sondagem, como generalizar de um termo para todos.
- `flexao-por-base` é nova, como antes. A sonda pareada de lematização é um caso de
  `sondagens-de-sintaxe`.
- `execucao-da-busca` remete ao roteiro do procedimento.

**D9. Início da fonte de uma base nova.** `procedimentos iniciar <sigla>`:
- exige a base já registrada no protocolo, porque base nova é decisão de escopo;
- recusa-se a sobrescrever uma pasta existente;
- escreve `procedimento.toml` e `como_executar.md` a partir de um modelo textual. A
  biblioteca padrão lê TOML mas não o escreve, e o modelo fica na gramática;
- preenche o que é derivável: IDs e rótulos de critério, idiomas do quadro por faceta,
  sementes da base, um elemento por categoria mínima e `plural = "explícito"`;
- marca o resto com `PENDENTE`.

A base iniciada fica reprovada até a fonte ser preenchida, e a lista de pendentes é a lista
de trabalho da skill `procedimento-de-busca-por-base`.

## Decisões de implementação (2026-11-23, a revisar pelo pesquisador)

Tomadas na implementação dos grupos 1 a 5, por serem de representação, reversíveis e não
decidirem escopo nem método; cada uma muda só a forma da fonte ou deixa a flexão mais
conservadora:

- **Esquema.** `[[composicao.facetas]]` (com `rotulo` e `cor` opcionais), `[composicao]
  disjuncao` (decisão do pesquisador) e `[[execucao.expressoes]]`, com `id`, `titulo` (o
  texto de `### EBn (<titulo>)`, que o protocolo não traz) e `estatuto` opcional. O destino
  de critério ganhou `ancora` ("**Sim**, por âncora": o critério que a âncora aplica, sem
  cláusula).
- **Leitura inconclusiva** é a leitura de `estado = "nao_verificado"`: o resultado que não
  muda o estado do elemento. Não há campo próprio.
- **Flexão, mais conservadora que o mínimo da D4:** também são indecidíveis o -ing e o -o do
  inglês, o -um/-on/-ex/-ix latinos ou gregos, a locução inglesa com preposição
  (`situation of use`, em que a última palavra não é o núcleo), o -il e o -x do português e
  o -n sem acento, o -i/-u e o -y do espanhol. O adjetivo isolado (termo de uma palavra
  com terminação adjetiva) é indecidível também em pt e es, e não só em en (decisão do
  pesquisador de 2026-11-24, na verificação): `educacional` passou a exigir exceção, com a
  mesma forma que a regra gerava. O termo que já é forma de número de outro
  termo da mesma lista (`thesauri` de `thesaurus`, pela exceção) não se flexiona de novo. A
  forma radical não se flexiona.
- **Consequência para os cenários da spec:** `aprendizagem online` dá `aprendizagens onlines`
  pela regra, e o pesquisador o declarou não contável. O cenário "Termo novo na STR" passou
  a usar `plataforma educacional`, que a regra flexiona (correção de 2026-11-24, na
  verificação).
- **Subconjuntos** declaram termos da STR, e o gerador acrescenta as formas de número. Na
  ERIC, `STR1b` traz hoje `thesauri` sem `thesaurus`; declarado como termo da STR, o bloco
  passa a trazer `thesaurus` também. É mudança de busca, a decidir na prova da migração
  (6.3).
- **Texto fixo** segue o esqueleto da Scopus e da WoS. A linha da §5 remetia a
  `data/sementes.json`, que não existe mais; por decisão do pesquisador de 2026-11-24, na
  verificação, passou a remeter ao arquivo de sementes (`[documentos] sementes`).
- **Exceção órfã** é a de termo que não está em nenhuma STR nem em lista escrita à mão na
  fonte (subconjunto ou forma curada), onde a exceção também se aplica (correção de
  2026-11-24, na verificação).

## Risks / Trade-offs

- [O pesquisador perde a edição direta do procedimento] → é decisão dele. A fonte tem
  fragmentos em markdown para a prosa, e a gramática dá a forma de cada campo.
- [A transcrição introduz perda silenciosa] → a prova de D7: diferença fora da lista
  aprovada interrompe a migração.
- [O roteiro vira formalidade, com leituras vagas] → a validação exige a leitura
  inconclusiva e o estado de cada leitura. A skill dá o critério do que é leitura
  distinguível. A qualidade do roteiro continua sendo revisão do pesquisador, e o
  procedimento o mostra por inteiro.
- [A ERIC não cabe nos parâmetros] → a ERIC é o caso de prova (consultas de campo,
  prefixo, aspas só na locução, subconjunto, radical). O parâmetro que faltar interrompe a
  migração para decisão.
- [Muitos termos indecidíveis na primeira geração] → o arquivo de exceções se monta por
  idioma. As propostas do agente vão ao LOG_IA e são revisadas antes da gravação.
- [O gerador errado passa porque a conferência lê o que ele gera] → as conferências de
  cobertura continuam independentes do código de composição. O autoteste injeta defeito no
  gerador e no dado e exige a reprovação.

## Migration Plan

1. Código e autoteste: leitor da fonte, flexão, gerador, sondagens, conferências.
2. Transcrever as quatro bases para `docs/procedimentos/<sigla>/`, nas situações mais
   conservadoras onde houver contradição, e registrar as pendências.
3. Provar a transcrição em duas partes (D7): fora dos blocos de termos, só as
   uniformizações aprovadas; em cada bloco, com a flexão ligada, só acréscimo de forma
   flexionada, nunca perda de termo.
4. Escrever o roteiro de sondagens dos elementos não verificados de cada base e revisá-lo
   com o pesquisador. A ERIC entra com os elementos não verificados, e as suas sondagens
   serão refeitas pelo pesquisador pelo roteiro gerado.
5. Montar `docs/flexoes.toml` e revisar as exceções.
6. Ensaiar e gravar as quatro bases; rodar `documentos conferir`, `dados conferir` e
   `projeto autoteste`.
7. README, `docs/procedimentos.md`, skills e histórico, este sem contagem.

Reversão: o git restaura os procedimentos e a configuração. Nenhuma execução está
registrada.

## Open Questions

- Onde guardar a evidência das sondagens: subpasta de `[dados] evidencia` ou caminho livre
  no projeto. O comando aceita qualquer arquivo existente; a convenção se fixa com a
  primeira sondagem registrada.
- ~~O rótulo das partes quando a partição muda o número de consultas~~: decidido em
  2026-11-23 — rótulo composto (D7), com "parte k de n" calculado pelo gerador.
