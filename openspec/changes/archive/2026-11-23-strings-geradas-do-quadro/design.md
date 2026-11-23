# Design

## Context

- O protocolo traz o quadro terminológico (quatro facetas, três camadas, pt/en/es) e a tabela
  "Strings de busca por faceta", escrita à mão.
- `rsl conferir` exige só STR ⊆ quadro. As fichas são conferidas contra a STR por
  `cobertura.py`. Pela regra "Termo da base deriva da STR", termo que conste só do quadro
  reprova.
- Não existe gerador de STRs nem de fichas.
- Estado medido em 2026-11-22, depois dos ajustes do pesquisador:
  - `conferir` reprova (código 1), porque STR3 e as fichas WoS, Scopus e BRAPCI trazem
    `prática`/`practice`/`práctica`, que saíram do quadro de FCT3;
  - o script de auditoria da skill `otimizar-strings-revisao-sistematica` acha 87 termos
    subsumidos em 305;
  - 12 formas estão em FCT2 e FCT4 ao mesmo tempo;
  - 46 formas estão no quadro e fora das strings.
  Esses números se recalculam na implementação, e não se transcrevem.
- Decisões do pesquisador nesta change, tomadas em 2026-11-22:
  - o gerador grava no protocolo;
  - as formas fora das strings saem do quadro, exceto as de B3 e C1;
  - os termos de B3 operam no campo tópico inteiro;
  - nível, modalidade e instituição de ensino, ambiente de aprendizagem e infraestrutura
    educacional ficam só em FCT2;
  - população-alvo e recurso disponível saem do quadro e vão para o G4;
  - "e" × "e/ou": níveis diferentes, ambos corretos (D9);
  - endereços do ERIC Thesaurus e do Brased indicados pelo pesquisador (D8).
- O pesquisador já corrigiu o objetivo geral (para "e" e "associados") e o OE1 (quatro
  operações). Resta a duplicação "à a" no objetivo geral.

## Goals / Non-Goals

**Goals:**
- STR reprodutível a partir do quadro, com divergência reprovada nos dois sentidos.
- Atribuição única do quadro garantida por conferência, com demonstração de que reprova.
- Plural de cada base declarado, sem afirmar lematização não medida.

**Non-Goals:**
- Gerar as fichas. A forma de cada base (campos, truncamento, partição, redução) é decisão
  autoral por base.
- Conferir a simetria entre idiomas por máquina. Equivalência de tradução não se decide por
  contagem, e a simetria é corrigida no conteúdo do quadro, com revisão do pesquisador.
- Faceta auxiliar local (B5), revisão das sementes (B4), execução das buscas.

## Decisions

**D1. O gerador grava a tabela de STRs no protocolo; o `conferir` exige igualdade.**
- O pesquisador escolheu a gravação. Pelo AGENTS §3, a geração adotada se declara no
  README, e se altera a fonte (o quadro), não a saída (a tabela de STRs).
- A gravação substitui só a terceira coluna das linhas `STRn` e é atômica: grava num
  temporário e depois renomeia.
- O `conferir` compara a STR lida com a calculada. Assim, a edição manual da STR é
  reprovada mesmo sem que ninguém rode o gerador.
- Alternativas descartadas:
  - só conferir, sem gravar: foi preterida pelo pesquisador;
  - gerar a STR na leitura e eliminar a tabela: quebraria a gramática, as fichas, que
    citam `STRn`, e a legibilidade do protocolo.

**D2. Subsunção por sequência contígua de palavras, com grafia exata.**
- Um termo `a` subsume `b` quando as palavras de `a` aparecem, contíguas e na ordem, em
  `b`.
- A comparação é sensível a caixa baixa, acento e hífen, e não admite flexão.
- A regra é conservadora porque o comportamento das bases quanto a diacríticos e hífen não
  está medido (fichas, seção 1). Deixar de retirar custa só comprimento; retirar demais
  custa recall.
- A subsunção vale entre idiomas da mesma STR, porque a STR é uma só disjunção.
- Alternativa descartada: comparar sem acento e sem hífen. Retiraria, por exemplo,
  `ontology-based modeling`, cuja tokenização varia por base.

**D3. Ordem e unicidade.**
- A ordem segue o cabeçalho do quadro (pt, en, es), as camadas e a ordem dentro da célula.
  Isso coincide com a ordem atual das STRs e minimiza a diferença revisada.
- A forma repetida entre idiomas entra uma vez.

**D4. Atribuição única conferida sobre a forma normalizada.**
- Usa a mesma normalização de `cobertura.py` (`normaliza`). Duas facetas com a mesma forma
  normalizada reprovam.
- A conferência roda em `conferir` e bloqueia `strings gerar --gravar`, porque gerar com
  duplicação produziria duas STRs que se implicam (critério 4 da skill de otimização).

**D5. Fichas podem usar o subsumido.**
- A ERIC executa `STR1` no título e `STR1b`, que é subconjunto específico, no resumo. Com
  a subsunção, `ontology engineering` e `ontology design pattern` saem da STR1, e a regra
  atual reprovaria a ERIC por "consta só do quadro".
- O subsumido passa a contar como derivado da STR e é relatado por base, para que o
  redundante no mesmo campo fique visível e seja retirado na atualização das fichas (C6).
- Alternativa descartada: declarar o subsumido na redução da ficha. Misturaria redução, que
  é perda declarada, com especificidade de campo, que não é perda.

**D6. Plural por base, sem gerador de fichas.**
- O pesquisador pediu que "scripts que geram as fichas" avaliassem a lematização. Esses
  scripts não existem, e as fichas são autorais.
- A garantia fica na conferência: a linha `plural` na declaração de cobertura, e
  `pela lematização` só com a linha "Lematização" medida e citada.
- Hoje nenhuma das quatro fichas tem lematização medida. Por isso as quatro passam a
  `explícito`, e a ERIC volta a trazer os plurais regulares.
- O relato de termo numa só forma de número não reprova, porque substantivo não contável
  (`education`, `pedagogia`) não tem plural de uso, e a reprovação seria ruído.
- A medição da lematização entra como verificação da primeira execução de cada base, pela
  skill `ficha-de-busca-por-base`.

**D7. Conteúdo do quadro, conforme as decisões do pesquisador.**
- B3: em FCT1, `modelo conceitual`, `modelagem conceitual`, `esquema conceitual`,
  `modelo semântico` e `taxonomia`, e os equivalentes en/es, permanecem ou entram no quadro
  e passam à STR.
- C1: `nível de ensino`, `modalidade de ensino`, `instituição de ensino`, `ambiente de
  aprendizagem` e `infraestrutura educacional`, com os equivalentes en/es (inclusive
  `learning infrastructure`), saem do quadro de FCT4 e ficam em FCT2. O que faltar em FCT2
  é acrescentado lá.
- `população-alvo`, `recurso disponível` e os equivalentes (`target population`,
  `población destinataria`, `available resource`, `recurso disponible`) saem do quadro. São
  variáveis de extração (critério 5 da skill de otimização) e, como âncora de domínio,
  seriam polissêmicos (critério 7). O G4 do instrumento de extração passa a nomeá-los, para
  que o dado retirado da busca seja de fato coletado.
- As formas que hoje estão no quadro e fora das strings saem do quadro, exceto as de B3 e
  C1. Pela medição de 2026-11-22 são 20; a lista se recalcula antes de retirar e, se
  divergir desta, a diferença vai ao pesquisador antes de qualquer edição:
  - FCT1: `análise de facetas`, `análise facetada`, `análisis de facetas`, `análisis
    facetado`, `facet analysis`, `formal representation`, `representação formal`,
    `representación formal`, `ontological`, `ontológico`, `ontológica`;
  - FCT2: `educativo`, `estudiante`, `alumno`, `docente`;
  - FCT4: `contexto de aplicação`, `contexto de aplicación`, `application context`,
    `contexto de uso`, `context of use`.
  As strings não mudam por isso: essas formas já estavam fora delas.
- Simetria (C2, C4): por decisão do pesquisador, o agente acrescenta as equivalências
  faltantes diretamente no quadro, sem tabela prévia de aprovação. A validação humana
  exigida para expansão terminológica assistida por IA (skill de otimização; P8) passa a
  ser feita depois: cada forma acrescentada é listada, por faceta, camada e idioma, na
  entrada do histórico e no relato da aplicação, e a lista vai para o LOG_IA. A revisão
  pelo pesquisador se faz sobre o diff. Os casos levantados na revisão de 2026-11-22 são:
  - FCT1: `taxonomy`/`taxonomía`/`taxonomía facetada`;
  - FCT2: os termos do núcleo en sem pt/es; `objeto de aprendizaje` sem `learning
    object`/`objeto de aprendizagem`; `aprendiz` só em es;
  - FCT4: `situação de uso educacional` × `situation of use`, e `contexto sensível`;
  - FCT2 es: a saída de `educativo` deixa `educacional` (pt) sem o adjetivo es
    correspondente.

**D8. Fontes dos instrumentos (C7).**
- `docs/02:19` é um único item de lista com duas referências, o ERIC Thesaurus e o UNESCO
  Thesaurus. Ele é desdobrado em dois itens, com a ERIC primeiro.
- Endereços indicados pelo pesquisador para o ERIC Thesaurus, em lugar de
  `vocabularyserver.com/eric/`, e para o Brased, em lugar da página do INEP em `gov.br` e de
  `vocabularyserver.com/brased/`.
- O endereço de cada instrumento fica num lugar só: a coluna `Caminho` da tabela
  "Instrumentos para controle terminológico" de `docs/03`, que o leitor exige e confere como
  URL. As referências de `docs/02` remetem à linha da tabela, e esta change não repete o
  endereço (revisão de 2026-11-23).
- O agente não verificou os endereços; eles são do pesquisador. Os dois instrumentos são de
  modo `Manual`, sem cliente automatizado. Se o código usar a coluna `Caminho` para eles,
  por exemplo para preencher `url_consultada` na planilha de validação, a mudança é
  conferida por `termos exportar` num diretório temporário.

**D9. "e" × "e/ou" em dois níveis.**
- Decisão do pesquisador: a QGR e o objetivo geral, com "e", tratam do recorte da revisão,
  que examina as duas dimensões no conjunto. O CE6 e a EB4, com "e/ou", tratam da inclusão
  de cada estudo.
- A declaração vai para o parágrafo de adaptação do PICo, logo abaixo da QGR, porque é ali
  que o leitor encontra o "e". O CE6 já justifica a disjunção e não muda.
- Alternativa descartada: conjunção também no estudo. Exigiria a EB1 como busca definitiva
  e esvaziaria a QER4, que depende da comparação entre soluções parciais.

**D10. Parâmetros da geração da busca por base.** Decisão do pesquisador, de 2026-11-22,
na revisão desta change.
- As skills que compõem a busca por base não citam base. O que difere de base para base é
  **parâmetro**: declarado na ficha, lido pelo leitor e conferido por `conferir`.
- `plural` já é parâmetro (`explícito` | `pela lematização`). As skills passam a dizer como
  ele governa a composição: com `explícito`, a string traz as duas formas de número; com
  `pela lematização`, só a forma do quadro.
- O teto de comprimento da consulta passa a ser parâmetro, na linha `teto de caracteres` da
  declaração de cobertura. O valor é um número inteiro de caracteres ou `nenhum`. A linha
  ausente ou ilegível reprova. Com número, `conferir` reprova a base em que alguma consulta
  executável passa do teto. Com `nenhum`, `conferir` relata, sem reprovar, a maior consulta.
- O teto não exige medição citada, diferentemente de `pela lematização`. Um teto baixo
  demais custa partição, não recall; um teto alto demais aparece como recusa da interface.
  A origem do número vai na linha "Comprimento máximo da consulta" da seção 1.
- Consulta executável é cada bloco das expressões da seção 4, salvo o da forma longa e o
  rotulado "não é a forma executada", e cada consulta da forma curada.
- O comprimento é `len` do texto do bloco, que é o que se cola na interface. A lista de
  comprimentos transcrita na prosa da ficha da ERIC sai: o número é calculado, não
  transcrito.
- Não há script no repositório que componha as fichas. Elas são escritas pelo agente com
  roteiro descartável sobre o leitor. Um gerador de fichas seria outra change.

**D11. Estratégia de proximidade na ficha.** A ficha pode ter a subseção
`### Estratégia de proximidade`, na seção 4. Ela é prosa de discussão e não é lida como forma
executável: o leitor a ignora, como "Como executar" e "Variantes". A skill
`ficha-de-busca-por-base` diz o que ela discute. A subseção não é exigida.

**D12. Fichas renomeadas.** `docs/busca_base_<sigla>.md` passa a
`docs/procedimentos_busca_<sigla>.md`, com o padrão em `[documentos] ficha`. Mudam as
referências vivas: configuração, README, skills, autoteste e pendências. O histórico e as
changes arquivadas mantêm o nome antigo. As specs principais passam a citar o padrão novo
pela delta: o requisito "Bases lidas da tabela do protocolo" de `leitura-do-protocolo` entra
como MODIFIED, com o exemplo de cenário atualizado, e a spec principal muda no sync.

**D13. Skills sem base nomeada.** Saem das skills `expressoes-de-busca` e
`facetacao-e-termos-livres` as menções a base específica: a tabela de sintaxe por base, o teto
da ERIC e a lista curada da BRAPCI. A lição de cada defeito fica, sem o nome da base. O que
é de uma base fica na ficha dela. As menções em outras skills (`busca-nas-bases`,
`deduplicacao`, `conferencias-da-busca`, `filtragens`, `conjunto-semente`,
`conferir-referencia`, `validacao-vocabulario-controlado`) ficam para decisão do
pesquisador.

## Risks / Trade-offs

- [`nível de ensino` e afins em STR2 ampliam a âncora de domínio e revertem parte da emenda
  v2] → registrar como emenda de busca; o efeito é medido na sonda EB5 − EB4 e no volume da
  primeira execução.
- [B3 no campo tópico traz de volta o ruído retirado pela emenda v2, como a taxonomia de
  Bloom] → declarado no histórico como risco aceito; a auditoria de rendimento por termo,
  depois da execução, decide a poda por nova emenda.
- [Plural explícito na ERIC pode passar do teto de 1.400 caracteres] → medir o comprimento
  de cada consulta depois da atualização; passando do teto, particionar como a ficha já
  prevê (`execucao: particionada`), sem retirar termo.
- [A subsunção conservadora deixa redundância residual com acento ou hífen] → aceitável:
  custa comprimento, não recall.
- [A gravação no protocolo pode sobrescrever uma edição concorrente do pesquisador] → o
  gerador lê o arquivo corrente imediatamente antes de gravar e só substitui as células de
  string; o ensaio sem `--gravar` é o passo padrão.
- [Fichas desatualizadas depois de cada regeração] → `conferir` reprova a ficha que diverge
  da STR. É a garantia atual, mantida.

## Migration Plan

Ordem:
1. código e autoteste;
2. recálculo da lista das formas a retirar;
3. edição do quadro e do G4;
4. `strings gerar` como ensaio, revisado, e depois `--gravar`;
5. fichas;
6. `conferir` e `autoteste`;
7. documentação, skills e histórico.

Reversão: o histórico do git restaura protocolo e fichas. Nenhum dado de execução existe
para invalidar.
