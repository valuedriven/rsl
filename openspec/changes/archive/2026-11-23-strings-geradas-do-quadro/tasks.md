# Tasks

## 1. Geração das STRs (D1, D2, D3)

- [x] 1.1 Implementar o cálculo da STR esperada por faceta a partir do quadro lido, com a
  subsunção por sequência contígua e grafia exata (D2) e a ordem do quadro (D3). Verificar
  pelos cenários de "STR é a união do quadro da faceta" e "Termo subsumido sai da STR" do
  spec `geracao-das-strings`, e comparar a lista de subsumidos com a saída do script de
  auditoria da skill `otimizar-strings-revisao-sistematica` sobre o protocolo corrente,
  explicando cada diferença (hífen, acento).
- [x] 1.2 Criar o subcomando `python3 -m rsl strings gerar`. Sem `--gravar`, ele exibe as
  diferenças por faceta e os subsumidos com o termo que os subsume, e sai com REPROVADO
  quando há diferença. Com `--gravar`, substitui só as células de string, de forma atômica.
  Verificar com `strings gerar -h`, com um ensaio sobre o protocolo corrente (que deve
  listar a retirada de `prática`/`practice`/`práctica` de STR3) e com uma gravação numa
  cópia temporária, comparando por `diff` que nenhuma linha fora da tabela de STRs muda.
- [x] 1.3 Registrar `strings gerar` na ajuda e no requisito "Ponto de entrada único".
  Verificar que `python3 -m rsl` sem subcomando lista `strings`.

## 2. Conferências novas (D4, D5)

- [x] 2.1 Fazer `conferir` reprovar uma STR diferente da esperada, nomeando os termos a mais
  e a menos e `strings gerar` como correção. Verificar no protocolo corrente: deve reprovar
  STR3 e as demais STRs pelos subsumidos.
- [x] 2.2 Fazer `conferir` reprovar uma forma normalizada presente no quadro de duas
  facetas, e `strings gerar --gravar` recusar a gravação nesse caso. Verificar no protocolo
  corrente: deve nomear as formas comuns a FCT2 e FCT4.
- [x] 2.3 Fazer `cobertura.py` aceitar, na string da base, o termo do quadro subsumido por
  termo da STR, e relatá-lo por base sem reprovar. Verificar pelo cenário "Subsumido em
  campo próprio" com a `STR1b` da ERIC.
- [x] 2.4 Acrescentar ao autoteste os casos de STR editada à mão, termo em duas facetas
  (com recusa da gravação), gravação que preserva o restante do arquivo e subsumido aceito
  na ficha. Demonstrar que cada caso reprova sem a conferência correspondente, desligando-a
  temporariamente. Verificar que `python3 -m rsl autoteste` não tem falha.

## 3. Plural declarado por base (D6)

- [x] 3.1 Acrescentar à gramática a linha `plural` (`explícito` | `pela lematização`) da
  declaração de cobertura, com PROTOCOLO_ILEGIVEL para ausência ou valor fora do domínio.
  Verificar em `python3 -m rsl gramatica` e pelos cenários de "Plural declarado por base".
- [x] 3.2 Reprovar a base que declara `pela lematização` sem a linha "Lematização"
  verificada por medição e com citação `(BDn/<id>)`. Relatar, em `explícito`, os termos
  numa só forma de número e não alcançados por truncamento. Verificar pelos cenários de
  "Plural pela lematização exige lematização medida" e "Termo só no singular relatado".
- [x] 3.3 Acrescentar ao autoteste a injeção de `pela lematização` sem lastro numa só base e
  a retirada da linha `plural`. Verificar que só a base injetada reprova e que a retirada dá
  PROTOCOLO_ILEGIVEL.
- [x] 3.4 Declarar `plural: explícito` nas quatro fichas e, na ERIC, retirar a frase "Plural
  regular omitido onde a lematização o alcança" e repor os plurais regulares. Verificar que
  `conferir` não reprova por plural e anotar o relato de termos numa só forma, por base.
- [x] 3.5 Atualizar a skill `ficha-de-busca-por-base` (a medição da lematização de cada base
  na primeira execução, e o significado da linha `plural`) e a skill `expressoes-de-busca`,
  cuja linha da ERIC afirma "lematiza plural regular" sem medição registrada e passa a "não
  medido". Verificar com `grep -n -i lematiz .agents/skills/*/SKILL.md` que nenhuma afirmação
  de comportamento fica sem registro de medição.

## 4. Conteúdo do quadro e do instrumento de extração (D7)

- [x] 4.1 Recalcular, sobre o protocolo corrente, as formas do quadro que estão fora das
  STRs, excluídas as de B3 e C1, e comparar com as 20 listadas no design (D7). Se a lista
  for igual, ela é a que sai; se divergir, apresentar a diferença ao pesquisador antes de
  qualquer edição. Verificar pela comparação impressa.
- [x] 4.2 Acrescentar diretamente ao quadro de `docs/03` as equivalências entre idiomas
  que faltam (C2, C4), a partir dos casos do design, sem tabela prévia de aprovação, por
  decisão do pesquisador. Listar cada forma acrescentada, por faceta, camada e idioma, para
  o histórico (7.3), o LOG_IA e o relato da aplicação. Verificar que `conferir` não reprova
  e que a lista confere com o `git diff` do quadro.
- [x] 4.3 Editar o quadro de `docs/03`:
  - retirar as formas confirmadas em 4.1;
  - aplicar B3;
  - C1: retirar de FCT4 `nível de ensino`, `modalidade de ensino`, `instituição de ensino`,
    `ambiente de aprendizagem` e `infraestrutura educacional`, com os equivalentes en/es
    (inclusive `learning infrastructure`), e acrescentar a FCT2 os que lá faltarem;
  - retirar `população-alvo`, `recurso disponível` e os equivalentes en/es;
  - retirar a duplicata de `ensino superior` em FCT2 pt.
  Verificar que `conferir` não reprova mais por atribuição única e que nenhuma das formas
  retiradas consta do quadro (`grep`).
- [x] 4.4 Acrescentar ao G4 de `docs/parametros_complementares.md` a população-alvo e os
  recursos disponíveis, como fatores situacionais declarados no artefato. Verificar que o
  G4 os nomeia e que a lista de cobertura conceitual continua coerente com ele.

## 5. Regeração das STRs e atualização das fichas (B2, C6)

- [x] 5.1 Executar `strings gerar` como ensaio, conferir a diferença e, em seguida,
  `strings gerar --gravar`, sem aprovação prévia; o ensaio vai no relato da aplicação. Verificar que `conferir` não reprova por STR e registrar a
  contagem de termos por STR antes e depois, calculada pelo comando, e rodar o script de
  auditoria da skill sobre o resultado, que deve mostrar zero subsumidos.
- [x] 5.2 Atualizar as strings das quatro fichas a partir das STRs regeradas: retirar os
  subsumidos no mesmo campo, acrescentar os termos novos nos idiomas e camadas declarados e
  revisar à mão as consultas curadas da BRAPCI. Verificar que `conferir` não reprova
  nenhuma base e que o relato de subsumidos só lista termos em campo próprio (`STR1b` da
  ERIC).
- [x] 5.3 Medir o comprimento de cada consulta da ERIC contra o teto declarado na ficha e,
  se passar, particionar sem retirar termo. Verificar o comprimento por comando e
  registrá-lo na ficha.

## 6. Fontes dos instrumentos e redação das questões (D8, D9)

- [x] 6.1 Desdobrar `docs/02:19` em dois itens, primeiro o ERIC Thesaurus e depois o UNESCO
  Thesaurus. Verificar que cada item tem uma referência.
- [x] 6.2 Aplicar os endereços do ERIC Thesaurus e do Brased indicados pelo pesquisador na
  coluna `Caminho` da tabela de instrumentos de `docs/03`, lugar único do endereço; as
  referências de `docs/02` remetem à linha da tabela (revisão de 2026-11-23). Conferir em
  `src/rsl/termos/planejamento.py` se essa coluna é usada para os instrumentos manuais e, se
  for, rodar `termos exportar` num diretório temporário. Verificar com `conferir` e com
  `grep -n -i -E 'vocabularyserver.com/(eric|brased)|gov.br/inep' docs/*.md`, que não deve
  achar nada.
- [x] 6.3 Acrescentar ao parágrafo de adaptação do PICo, logo abaixo da QGR em `docs/03`, a
  frase de D9: a conjunção da QGR é do recorte da revisão, e a regra de inclusão de cada
  estudo é a disjunção do CE6. A frase é gravada diretamente e citada no relato da aplicação. Verificar
  que `conferir` não reprova e que o leitor continua reconhecendo o marcador "A estrutura
  da questão…".
- [x] 6.4 Corrigir "associados à a sua aplicação" para "associados à sua aplicação" no
  objetivo geral (`docs/01_plano.md`). Verificar com `grep -n 'à a sua' docs/01_plano.md`,
  que não deve achar nada.

## 7. Documentação e registro

- [x] 7.1 Declarar no README a geração das STRs: no Mapa, quem escreve a tabela de STRs; e,
  na Precedência, a ordem quadro → `strings gerar` → fichas → `conferir`. Acrescentar o passo
  em `docs/procedimentos.md`, trabalhando sobre a versão corrente, que tem alterações do
  pesquisador. Verificar que os comandos documentados rodam como escritos.
- [x] 7.2 Atualizar a skill `facetacao-e-termos-livres` §5, onde "A conferência é manual:
  não há guarda automática" deixa de ser verdade, e a ordem de alteração. Verificar a
  coerência com o README.
- [x] 7.2a Na skill `questao-e-objetivos`, trocar os caminhos `docs/01`, `docs/02` e
  `docs/03` por "o plano, seção Objetivos" e "o protocolo, seção Questão de revisão",
  corrigindo a remissão do §5, que aponta as questões em `docs/02`. Verificar com
  `grep -n 'docs/0' .agents/skills/questao-e-objetivos/SKILL.md`, que não deve achar
  nada.
- [x] 7.3 Registrar no histórico, com a skill `registrar-decisao`, a emenda desta change:
  - os ajustes do pesquisador de 2026-11-22 (QER1, OE1, OE4, objetivo geral, CE6, núcleo
    de FCT3), com redação confirmada por ele;
  - a leitura de "e" × "e/ou" em dois níveis (D9);
  - B3, C1 e a reversão parcial da emenda v2;
  - a retirada das formas fora das strings e de população-alvo e recurso disponível, com a
    passagem ao G4;
  - as formas acrescentadas por simetria, listadas por faceta, camada e idioma;
  - os endereços do ERIC Thesaurus e do Brased;
  - a regeração das STRs;
  - o plural explícito.
  Alcance: escopo e busca, com os riscos do design. Verificar que a entrada não transcreve
  contagem (README, Três registros; regra de 2026-11-23): as contagens de 5.1 vão ao relato
  da aplicação.
- [x] 7.4 Integração: rodar `conferir`, `conferir-dados` e `autoteste` e relatar os códigos
  e os casos não executados. Esperado: `conferir` 0; `conferir-dados` 5 (registro de
  execução ausente, como antes); `autoteste` sem falha.

## 8. Parâmetros da busca por base, proximidade e renomeação (revisão de 2026-11-22)

- [x] 8.1 Renomear as fichas com `git mv` para `docs/procedimentos_busca_<sigla>.md` e
  atualizar `[documentos] ficha`, o README, as skills, o autoteste de configuração e
  `data/pendencias.json` (D12). Verificar com `grep -rn busca_base` fora do histórico, das
  changes arquivadas e dos artefatos desta change, que não deve achar nada em documento
  vivo, e com `conferir` 0.
- [x] 8.2 Ler a linha `teto de caracteres` na declaração de cobertura: um número inteiro ou
  `nenhum`, e reprovar a linha ausente ou ilegível. Conferir o comprimento de cada consulta
  executável contra o teto, reprovando só aquela base, e relatar a maior consulta quando o
  valor é `nenhum` (D10).
- [x] 8.3 Ignorar na leitura a subseção `### Estratégia de proximidade` (D11).
- [x] 8.4 Autoteste:
  - teto menor que a maior consulta, numa só base, reprova só essa base;
  - linha `teto de caracteres` retirada dá PROTOCOLO_ILEGIVEL;
  - valor ilegível dá PROTOCOLO_ILEGIVEL;
  - subseção de estratégia de proximidade com bloco cercado não altera o derivado.
  Mostrar que cada caso falha com a conferência desligada.
- [x] 8.5 Declarar `teto de caracteres` nas quatro fichas: ERIC 1400, com a origem na
  seção 1; as demais `nenhum`, porque o comprimento não está verificado. Tirar da prosa da
  ERIC a lista transcrita de comprimentos.
- [x] 8.6 Skills:
  - `ficha-de-busca-por-base`: os parâmetros da geração (plural, teto) e como governam a
    composição; a estratégia de proximidade.
  - `expressoes-de-busca`: Parte 2 sem base nomeada, com o teto como parâmetro.
  - `facetacao-e-termos-livres`: §4 e §5 sem base nomeada (D13).
- [x] 8.7 Integração e histórico: `conferir`, `conferir-dados` e `autoteste`, com os
  códigos no relato, e uma entrada no histórico, sem contagem.

## Workflow follow-up

- O teste de aderência e a sonda EB5 − EB4 medem, na primeira execução, o efeito das STRs
  regeradas; esse passo segue o fluxo do protocolo e não integra esta change.
- Arquivar a change depois da revisão do pesquisador.
