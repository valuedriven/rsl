# Design

## Context

- **Estado depois de `strings-geradas-do-quadro`:**
  - a tabela de STRs do protocolo é gerada do quadro;
  - as fichas são autorais e se conferem contra a STR (`cobertura.py`);
  - a declaração de cobertura tem `idiomas`, `camadas`, `plural`, `teto de caracteres` e
    `derivações`;
  - `conferir` mede o comprimento das consultas executáveis;
  - o termo só no singular é relatado, sem reprovar.
- **As fichas divergem em pontos que nenhum parâmetro declara hoje:**
  - **campo:** grupo envolvido por `TS=(…)` ou `TITLE-ABS-KEY(…)` na WoS e na Scopus;
    prefixo por termo (`abstract:termo`) na ERIC;
  - **aspas:** em todo termo na WoS e na Scopus; na ERIC, só na locução;
  - **proximidade** entre as âncoras;
  - **forma de execução:** única, particionada (ERIC) ou curada (BRAPCI);
  - **subconjunto por campo e forma radical** da ERIC (`STR1b`, palavras-raiz de FCT2),
    descritos hoje em prosa.
- **Não há script que componha as fichas.** As fichas atuais foram escritas com roteiro
  descartável.
- **O leitor já isola o que a geração precisa:** os blocos cercados por subseção (`STRn`,
  `EBn`), a forma longa, o bloco rotulado como não executado, as consultas curadas e as
  subseções ignoradas.
- **Lematização:** nenhuma base a tem medida. As fichas que citam documentação a
  documentam por idioma (por exemplo, inglês na WoS), e não para a base inteira.

## Goals / Non-Goals

**Goals:**
- Blocos de string e de expressão reprodutíveis a partir da STR e dos parâmetros da ficha,
  com a divergência reprovada por base.
- Plural completo por construção onde a base declara plural explícito, sem forma
  adivinhada.
- O que difere entre bases declarado como parâmetro, e não em prosa nem em código.

**Non-Goals:**
- Gerar a seção 1, a seção 2, a prosa e a forma curada.
- Truncamento automático: alcançar o plural por curinga depende de medir o curinga e os
  diacríticos em cada base, e fica para outra change.
- Morfologia completa de pt, en e es. A regra cobre o plural regular e declara indecidível
  o resto.
- Escolher, pelo pesquisador, o subconjunto por campo e a forma radical. Continuam escolhas
  autorais, só que declaradas em tabela.

## Decisions

**D1. Ficha mista, no padrão da tabela de STRs.** Decisão do pesquisador, de 2026-11-23.
- A geração substitui só os blocos cercados das subseções `STRn` e de subconjunto, na seção
  3, e `EBn`, na seção 4. Usa a gravação atômica com releitura de `geracao.py`, que se
  reaproveita.
- Alternativa descartada: gerar a ficha inteira a partir de um arquivo de parâmetros. Daria
  mais garantia por construção, mas prenderia a campos a prosa autoral e a seção 1, que tem
  fonte e estado por linha. A migração também seria maior.

**D2. Parâmetros de composição na ficha, numa tabela própria.**
- A tabela "Parâmetros de composição" fica na seção 3, junto da declaração de cobertura.
  Linhas:
  - `campo`, por faceta, com a forma `envolve` (grupo dentro do campo) ou `prefixa`
    (campo antes de cada termo);
  - `aspas` (`todo termo` | `locução`);
  - `proximidade` (operador e distância, ou `nenhum`);
  - `filtros` (`seção 2`).
- Subconjunto por campo e forma radical: tabelas "Subconjuntos por campo" e "Forma
  radical", com os termos de cada um. Substituem a prosa da ERIC.
- Os filtros vêm da coluna de expressão da seção 2, que já existe e já é conferida contra
  os critérios do protocolo. O gerador não duplica a sintaxe do filtro.
- Pelo AGENTS e por D10 de `strings-geradas-do-quadro`, o que difere de base para base é
  parâmetro da ficha. Nenhum perfil de base fica no código.
- Alternativa descartada: um perfil de sintaxe por base no código. Esconderia num lugar não
  autoral uma decisão que é da ficha.

**D3. Ordem e forma do bloco.**
- A ordem é a da STR. A flexão de cada termo vem logo depois dele, na ordem do plural
  regular e depois das exceções.
- Os termos repetidos depois da flexão entram uma vez, pela grafia exata.
- O bloco de expressão segue a composição do protocolo, com o grupo de cada faceta entre
  parênteses, sempre, sem depender da precedência da base. A proximidade é aplicada entre
  os grupos das âncoras, como as fichas fazem hoje.

**D4. Partição pelo teto.**
- Com teto numérico, a consulta que passa do teto tem o grupo OR da faceta não âncora de
  maior comprimento dividido em partes contíguas, até cada consulta caber.
- As âncoras ficam íntegras em todas as partes. Se as âncoras não couberem sozinhas, a
  geração reprova.
- As partes recebem os rótulos `4a1`, `4a2`… que a ERIC já usa, e a união dos termos das
  partes é conferida contra o grupo original.
- A forma de execução passa a `particionada` quando há parte. A ficha declara a forma, e a
  geração reprova se ela disser `unica` e for preciso partir.

**D5. Flexão por regra, com exceções, e recusa do indecidível.** Decisão do pesquisador,
de 2026-11-23.
- **Núcleo flexionado:**
  - en: a última palavra;
  - pt e es: as palavras até a primeira preposição, artigo ou contração (`de`, `do`, `da`,
    `em`, `no`, `na`, `ao`, `para`, `por`, `com`; `del`, `en`, `al`, `a`, `y`, `con`).
- **Regras regulares:**
  - en: `-y` depois de consoante dá `-ies`; `-s`, `-x`, `-z`, `-ch` e `-sh` dão `-es`; o
    resto ganha `-s`;
  - pt: vogal ganha `-s`; `-m` dá `-ns`; `-r` e `-z` dão `-es`; `-al`, `-ol` e `-ul` dão
    `-ais`, `-óis` e `-uis`; `-ável`/`-ível` dão `-áveis`/`-íveis`; `-ês` dá `-eses`;
  - es: vogal átona ganha `-s`; consoante ganha `-es`; `-z` dá `-ces`; `-ión` dá
    `-iones`.
- **Indecidível**, que reprova sem exceção:
  - pt: `-ão`, `-s` e `-x` finais, `-il` e `-el` sem acento;
  - en: `-f`/`-fe`, e as terminações de classe adjetiva ou de nome não contável típico
    (`-al`, `-ic`, `-ive`, `-ous`, `-ing`, `-ed`, `-able`);
  - es: vogal tônica `-í`/`-ú`, `-s` átono, e `-en`/`-an` que ganham acento no plural;
  - o termo com conjunção (`e`, `and`, `y`) no núcleo.
- Errar a forma custa ruído e uma forma inventada na string; omitir custa recall. A
  recusa evita os dois e põe a decisão no arquivo de exceções, com origem.
- **Alternativas descartadas:**
  - lista declarada de todo plural: mais conservadora, mas o trabalho manual cresce com o
    quadro e não protege o termo novo;
  - morfologia por dicionário externo: dependência nova e não auditável.

**D6. Arquivo de exceções.**
- TOML, em `docs/flexoes.toml`, com `[documentos] flexoes` no `config.toml`, no padrão do
  arquivo de sementes. Tabelas `[[flexoes]]` com:
  - `termo`, `idioma` e `tipo`, que é `irregular`, `nao_contavel` ou `vetada`;
  - `formas`, para `irregular` e `vetada`;
  - `origem`.
- A forma do arquivo é exibida por `gramatica`.
- O par irregular latino/grego que `cobertura.py` reconhece hoje no relato passa a ser
  exceção declarada. A heurística sai: o que era palpite vira dado com origem.
- A exceção nova proposta pelo agente entra com `origem` que diga isso, e o ensaio a
  lista. Ela é expansão assistida por IA e vai ao LOG_IA, para validação do pesquisador.

**D7. Plural por idioma.**
- A linha `plural` aceita valor único ou valor por idioma.
- A linha "Lematização" da seção 1 aceita estado por idioma. A citação `(BDn/<id>)` se
  confere como hoje, inclusive por `conferir-dados`, que já confere a citação fora da linha
  do registro.
- A medição é a sonda pareada, singular e plural do mesmo termo na mesma data. O
  procedimento fica na skill `flexao-por-base`, e o resultado, no registro de execução.

**D8. Termo só no singular passa a reprovar.**
- Com o gerador, o termo só no singular num idioma de plural explícito só existe por
  edição à mão ou por exceção. A exceção cala a reprovação; a edição à mão já reprova como
  bloco divergente.
- A regra vale também para a forma curada, que é a única parte autoral com termos. É ali
  que o plural esquecido ainda pode entrar.

**D9. Skill `flexao-por-base`, de competência metodológica.**
- Cobre:
  - como decidir entre plural explícito e lematização, por idioma;
  - como medir a lematização;
  - como julgar não contável e irregular;
  - o que conferir no ensaio.
- Não ensina o comando, que fica na documentação técnica. A `ficha-de-busca-por-base`
  passa a descrever a ficha mista e a ordem quadro → `strings gerar` → `procedimentos gerar` →
  `conferir`.

## Risks / Trade-offs

- [As fichas atuais têm muitos termos que a regra declara indecidíveis, e a primeira
  geração reprova até as exceções existirem] → as tarefas de migração montam o arquivo de
  exceções por idioma. As propostas pelo agente são listadas para revisão do pesquisador
  antes da gravação.
- [O plural explícito aumenta o comprimento das consultas e pode levar WoS, Scopus e
  BRAPCI a partir quando ganharem teto numérico] → a partição é por construção. Hoje as três
  declaram teto `nenhum`, e o relato da maior consulta continua.
- [A regra do núcleo em pt e es flexiona formas pouco usadas, como `ensinos superiores`]
  → custa comprimento, não recall. A forma vetada é a saída quando a forma for polissêmica
  ou enganosa.
- [Os parâmetros de composição descrevem a ERIC com dificuldade: prefixo por termo, aspas
  só em locução, subconjunto e radical] → a ERIC é o caso de prova da migração. Se a tabela
  não a expressar, a change para e o parâmetro que falta é decidido antes de prosseguir.
- [Conflito com `namespace-de-comandos-e-skills`] → o pesquisador decidiu C1 em
  2026-11-23: o conceito passa de "ficha" a "procedimento de busca". O comando desta change
  nasce com o nome canônico, `procedimentos gerar`, sem alias, e a tabela canônica daquela
  change tem a linha (tarefa 1.3a dela). A skill `ficha-de-busca-por-base`, a chave
  `[documentos] ficha` e a palavra "ficha" no texto são renomeadas por aquela change; esta
  usa os nomes vigentes, e a que for aplicada depois acompanha a outra.

## Migration Plan

1. Arquivar `strings-geradas-do-quadro`, de que esta change depende.
2. Código e autoteste: flexão, leitura dos parâmetros, geração, conferências.
3. Acrescentar às fichas a tabela de parâmetros e as tabelas de subconjunto e radical,
   transcritas das fichas atuais. A transcrição se confere: o ensaio de `procedimentos gerar` sem
   flexão nova deve reproduzir os blocos atuais. Toda diferença se explica antes de
   seguir.
4. Montar o arquivo de exceções a partir das reprovações de indecidível, por idioma, e
   revisá-lo com o pesquisador.
5. Fazer o ensaio de `procedimentos gerar` para todas as bases, revisar e gravar.
6. Rodar `conferir`, `conferir-dados` e `autoteste`; os resultados vão ao relato da change.
7. Atualizar a documentação, as skills e o histórico, sem contagem, e resolver a pendência
   do plural.

Reversão: o git restaura as fichas. Nenhuma execução está registrada.

## Open Questions

- Rótulo das partes quando a partição muda o número de consultas de uma expressão que já
  tinha partes. É decisão de nomeação, sem efeito na spec, e se fixa na implementação da
  partição.
