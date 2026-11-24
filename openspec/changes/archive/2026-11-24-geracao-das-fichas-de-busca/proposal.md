# Proposal

## Why

O procedimento de busca de cada base (`docs/procedimentos_busca_<sigla>.md`) é escrito e
mantido à mão, e a conferência só detecta a divergência depois de ela existir:

- As strings e as expressões são cópias da STR feitas à mão. WoS, Scopus e BRAPCI declaram
  `plural: explícito`, mas a maior parte dos termos está só no singular, e a conferência
  apenas relata isso.
- Os quatro arquivos divergem na forma, sem que alguém tenha decidido isso:
  - títulos de expressão em dois formatos;
  - a seção 1 com coluna de fonte numa base e sem ela nas outras;
  - separador ausente antes da seção 4 da BRAPCI;
  - número escrito em prosa ("em 13 consultas") na ERIC;
  - a frase de forma da ERIC repete em prosa o que a declaração de cobertura diz;
  - a SE1 aparece sem DOI na BRAPCI, embora o arquivo de sementes o tenha.
- O conteúdo sobre sintaxe medida foi preenchido pelo agente a partir de sondagens que o
  pesquisador executou sob orientação. Nada liga o que se afirma à sondagem que o sustenta,
  e os textos se contradizem: a ERIC diz "regras medidas" na seção 4 e "não verificado"
  para os mesmos elementos na seção 1.
- O que o pesquisador deve testar na base aparece em frases curtas ("medir na primeira
  execução"). Não há consulta de teste, controle, leitura do resultado nem evidência a
  registrar.

Esta change faz do procedimento de busca uma **saída de geração** (alternativa B,
decidida pelo pesquisador em 2026-11-23, que substitui a ficha mista da D1 anterior). O
conhecimento próprio de cada base passa a uma **fonte por base**: dados estruturados em
TOML e prosa livre em fragmentos markdown. O gerador compõe o arquivo inteiro a partir do
protocolo, do arquivo de sementes, da fonte da base e das exceções de flexão. O pesquisador
não edita o procedimento. Edita a fonte, quando quiser, ou pede ao agente.

## What Changes

- **Fonte do procedimento por base.** Fica em `docs/procedimentos/<sigla>/`, localizada por
  `[documentos] procedimento_fonte`, e tem duas partes:
  - **`procedimento.toml`**, com o que é dado:
    - os elementos de sintaxe, com situação, fonte, citação e sondagem;
    - o destino e o *como* de cada critério, com a cláusula de filtro;
    - a declaração de cobertura e a redução;
    - os parâmetros de composição: campo e forma do campo por faceta, aspas e
      proximidade;
    - as consultas de campo e os subconjuntos, a forma radical e o estatuto de cada
      expressão;
    - a forma de execução, as regras de montagem, as observações por semente e as
      ressalvas;
  - **fragmentos markdown** de nome fixo, com a prosa livre: notas de sintaxe, estratégia
    de proximidade, como executar, variantes previstas e notas do conjunto-semente.

  A forma da fonte é declarada na gramática e exibida por `documentos gramatica`.
- **Procedimento gerado por inteiro.** `python3 -m rsl procedimentos gerar [<sigla>]
  [--gravar]` monta o arquivo no esqueleto único dos exemplos atuais (seções 1 a 6).
  - **Do protocolo** vêm o título, o mapa das facetas, as strings, as expressões, os IDs
    dos critérios e a composição.
  - **Do arquivo de sementes**, filtrado pela base, vem a tabela de sementes.
  - **Da fonte** vem o resto.

  Sem `--gravar`, o comando exibe a diferença. Com `--gravar`, substitui o arquivo de forma
  atômica. **BREAKING**: o procedimento deixa de ser documento editável, e a edição à mão
  reprova em `documentos conferir`.
- **Roteiro de sondagens por base.** A fonte declara cada sondagem que o pesquisador deve
  executar. Cada uma tem:
  - os elementos de sintaxe que verifica;
  - o objetivo e os pré-requisitos;
  - as consultas literais, com papel de teste ou de controle;
  - os passos e o que observar;
  - a leitura de cada resultado possível, com o estado que dela decorre;
  - a evidência a registrar.

  O gerador as escreve no procedimento, numa subseção da seção 1, como instrução executável.
  Todo elemento não verificado aponta uma sondagem ou declara por que não a tem. Cada
  elemento de sintaxe tem uma categoria, e as categorias mínimas (campos, operadores,
  truncamento, lematização, proximidade, limites, filtros, exportação etc.) têm de estar
  cobertas em toda base, para que nenhum recurso fique esquecido.
- **`sondagens registrar <sigla> <SDn>`.** Grava o resultado no registro de execução
  (`bases.BDn.sondagens`), com:
  - os retornos de cada consulta declarada;
  - a leitura observada;
  - a data e a hora, obrigatórias;
  - a evidência, obrigatória.

  Exibe a citação `BDn/<id>` e a mudança a aplicar na fonte. A citação `(BDn/<id>)` passa a
  aceitar a sondagem registrada, e `dados conferir` relata o resultado ainda não levado à
  fonte.
- **`procedimentos iniciar <sigla>`.** Cria a fonte de uma base já registrada no protocolo,
  sem sobrescrever uma fonte existente. Vêm preenchidos critérios, idiomas, sementes, as
  categorias mínimas de sintaxe e o plural explícito. O resto vem marcado `PENDENTE`, e a
  base fica reprovada até ser preenchida.
- **Regras de montagem com lastro.** As regras do tipo "Como esta base exige" deixam a
  prosa e passam a tabela, cada uma com a sua situação e a sua sondagem. Não é mais possível
  chamar de "medida" uma regra cujo elemento a seção 1 dá como não verificado.
- **Composição, partição e flexão**, como já estavam na change:
  - os blocos de string e de expressão vêm da STR e dos parâmetros de composição;
  - a partição pelo teto mantém as âncoras íntegras;
  - o plural é gerado por regra de pt, en e es, com o arquivo de exceções
    (`[documentos] flexoes`) e a recusa da forma indecidível;
  - a linha `plural` pode ter valor por idioma;
  - o termo só no singular passa a reprovar.
- **Conferência por igualdade e sobre a fonte.**
  - `documentos conferir` reprova, por base, o procedimento que difere do que `procedimentos
    gerar` produziria.
  - As conferências de cobertura passam a ler a fonte, e não mais o markdown: critérios,
    plural, teto, forma de execução, citação de medição e forma curada.
  - O contrato de forma do markdown (cabeçalhos exatos e reconhecimento de campo e de
    filtro por texto) deixa de ser lido.
- **Skills.**
  - `procedimento-de-busca-por-base` é reescrita: o agente edita a fonte e gera; nunca edita
    o procedimento.
  - Nova skill `sondagens-de-sintaxe`, de competência metodológica: como desenhar a
    sondagem (uma variável por vez, par teste e controle, resultado que distingue as
    hipóteses), como ler o retorno zero, o que vale como evidência e como o resultado muda o
    estado do elemento.
  - Nova skill `flexao-por-base`, como antes.
  - `execucao-da-busca` passa a remeter ao roteiro.
- **Migração.**
  - Transcrever as quatro bases para a fonte.
  - Provar a transcrição: a primeira geração sem flexão nova reproduz os arquivos atuais,
    salvo as uniformizações que o pesquisador aprovou em 2026-11-23.
  - Escrever o roteiro de sondagens dos elementos não verificados.
  - Na ERIC, transcrever como não verificado o que hoje se diz medido, sem reconstruir os
    resultados antigos. O pesquisador decidiu em 2026-11-23 refazer as sondagens pelo
    roteiro gerado e registrá-las por `sondagens registrar`.
  - Registrar como pendência, sem resolver, as contradições de verificação que restarem.

Fora do escopo:
- comando que altere a fonte a partir do resultado registrado: a mudança é exibida e
  aplicada pelo agente ou pelo pesquisador;
- truncamento automático;
- medir a lematização, que depende da primeira execução.

Dependências: `strings-geradas-do-quadro` e `namespace-de-comandos-e-skills` estão
arquivadas. Esta change usa os nomes fixados por elas: `procedimento-de-busca-por-base`,
`[documentos] procedimento` e `documentos conferir`.

## Capabilities

### New Capabilities
- `fonte-do-procedimento`: forma, leitura e validação da fonte por base (TOML e
  fragmentos), categorias mínimas de sintaxe, marca `PENDENTE` e `procedimentos iniciar`,
  sem valor de projeto no código.
- `geracao-dos-procedimentos`: composição do procedimento inteiro a partir do protocolo, das
  sementes, da fonte e da flexão. Cobre a partição pelo teto, o ensaio e a gravação, a
  conferência de igualdade e o autoteste.
- `sondagens-por-base`: roteiro de sondagens na fonte, ligação entre elemento, sondagem e
  registro, escrita no procedimento, `sondagens registrar` e conferência do resultado
  registrado.
- `flexao-dos-termos`: flexão de número por regra, exceções declaradas, recusa do
  indecidível.

### Modified Capabilities
- `cobertura-por-base`:
  - as conferências leem a fonte;
  - a forma de execução, o teto, os critérios e a citação são lidos de campos da fonte;
  - o plural pode ter valor por idioma, e o termo só no singular reprova;
  - a estratégia de proximidade passa a fragmento.
- `gramatica-do-protocolo`: o contrato exibido passa a trazer a fonte do procedimento e o
  arquivo de exceções no lugar da forma do markdown do procedimento.
- `leitura-do-protocolo`: cada base passa a ser localizada pela fonte, e o procedimento
  gerado passa a ser saída.
- `interface-de-comando`: `procedimentos gerar`, `procedimentos iniciar` e `sondagens
  registrar` entram nos subcomandos canônicos.

## Impact

- **Código** em `src/rsl/`:
  - leitor da fonte, que substitui a leitura do markdown em `fichas.py`;
  - gerador do procedimento, que reaproveita a gravação atômica de `geracao.py`;
  - módulo de flexão;
  - subcomandos `procedimentos iniciar` e `sondagens registrar`, este com escrita atômica no
    registro de execução;
  - declarações da fonte, do registro de sondagem e do arquivo de exceções em
    `gramatica.py`;
  - `cobertura.py` e `dados.py`, para a citação de sondagem;
  - autoteste.
- **Configuração:** `[documentos] procedimento_fonte` e `[documentos] flexoes`. A chave
  `[documentos] procedimento` passa a ser o caminho de saída.
- **Documentos:**
  - `docs/procedimentos/<sigla>/` para as quatro bases;
  - `docs/flexoes.toml`;
  - os quatro procedimentos regravados;
  - `README.md` (Mapa e Precedência: o procedimento como saída e a fonte como lugar de
    edição);
  - `docs/procedimentos.md`;
  - `data/historico.md`, com uma entrada sem contagem;
  - `data/pendencias.json`, com as contradições de verificação, e com a pendência do plural
    resolvida na gravação.
- **Skills:**
  - `procedimento-de-busca-por-base`, reescrita;
  - `sondagens-de-sintaxe` e `flexao-por-base`, novas;
  - `execucao-da-busca` e `expressoes-de-busca`.
- **Busca:** as strings mudam com os plurais e a partição recalculada. Nenhuma execução está
  registrada, então nenhum resultado fica vencido.
