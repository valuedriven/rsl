# Proposal

## Why

A revisão de 2026-11-22 das questões, das facetas e do controle terminológico apontou que as
STRs são escritas à mão e divergem do quadro sem que nada reprove. Os problemas encontrados
foram: termos subsumidos (87 de 305), assimetria entre idiomas, termos em duas facetas do
quadro e termos retirados que continuam no quadro sem marca. O pesquisador já ajustou a QER1,
o OE4, o CE6 e o núcleo de FCT3. Com isso, `rsl conferir` passou a reprovar: STR3 e as fichas
ainda trazem `prática`/`practice`/`práctica`, que saíram do quadro. Esta change torna o quadro
a fonte das STRs e fecha os defeitos de modo que não voltem.

## What Changes

- **Geração das STRs a partir do quadro.** Um subcomando novo, `python3 -m rsl strings
  gerar`, calcula cada STR como a união dos termos do quadro da faceta (três camadas, três
  idiomas) menos os subsumidos por outro termo da mesma STR. Sem `--gravar`, só exibe a
  diferença; com `--gravar`, reescreve a tabela "Strings de busca por faceta" do protocolo.
  **BREAKING** para o fluxo de trabalho: a tabela de STRs deixa de ser editada à mão e passa
  a ser saída de geração dentro do protocolo.
- **`conferir` exige STR igual à gerada** e **reprova termo do quadro presente em mais de
  uma faceta**, ou seja, a atribuição única (C1).
- **Termo subsumido aceito nas fichas.** A string de uma base pode usar um termo do quadro
  subsumido por termo vigente da STR, para que a estratificação por campo da ERIC (`STR1` no
  título, `STR1b` no resumo) continue válida. A conferência relata, sem reprovar, os
  subsumidos presentes em cada ficha.
- **Plural declarado por base (C7).** A declaração de cobertura de cada ficha passa a dizer
  se o plural é `explícito` ou `pela lematização`. `pela lematização` exige a linha
  "Lematização" da seção 1 verificada, com citação da execução registrada.
- **Teto de caracteres como parâmetro da base (D10).** A declaração de cobertura de cada
  ficha passa a ter a linha obrigatória `teto de caracteres`, com um inteiro ou `nenhum`.
  `conferir` mede cada consulta executável e reprova a base que passar do teto; com
  `nenhum`, relata a maior consulta.
- **Estratégia de proximidade (D11).** A ficha pode ter a subseção
  `### Estratégia de proximidade`, na seção 4; o leitor a ignora como forma executável.
- **Conteúdo do protocolo, por decisão do pesquisador:**
  - reintroduzir em FCT1 os termos de modelo conceitual, modelo semântico e taxonomia
    isolada, nos três idiomas e no campo tópico (B3);
  - retirar de FCT4 `nível de ensino`, `modalidade de ensino`, `instituição de ensino`,
    `ambiente de aprendizagem` e `infraestrutura educacional`, com os equivalentes em en e
    es, que passam a operar só em FCT2 (C1);
  - retirar do quadro `população-alvo` e `recurso disponível`, com os equivalentes, que
    passam a ser só variáveis de extração do G4 no instrumento de extração;
  - retirar do quadro as 20 formas que hoje estão nele e fora das strings, exceto as que B3
    e C1 já decidiram;
  - completar a simetria entre idiomas do quadro, incluindo `taxonomía facetada` (C2, C4).
    O agente edita o protocolo diretamente, sem tabela prévia de aprovação, e lista no
    histórico e no relato cada forma acrescentada, para revisão do pesquisador pelo diff;
  - regerar as quatro STRs (B2, C6).
- **"e" × "e/ou" em dois níveis.** A QGR e o objetivo geral ("e") tratam do recorte da
  revisão; o CE6 e a EB4 ("e/ou") tratam da inclusão de cada estudo. Uma frase no
  parágrafo de adaptação do PICo declara isso.
- **Fichas atualizadas e renomeadas.** As fichas são atualizadas a partir das STRs
  regeradas, com os subsumidos retirados onde o campo é o mesmo (C6), e passam de
  `docs/busca_base_<sigla>.md` para `docs/procedimentos_busca_<sigla>.md` (D12). O padrão
  `[documentos] ficha` acompanha o novo caminho.
- **Fontes dos instrumentos.** Separar ERIC Thesaurus e UNESCO Thesaurus em itens distintos
  em `docs/02`, com a ERIC primeiro. Usar os endereços indicados pelo pesquisador, gravados só
  na coluna `Caminho` da tabela de instrumentos de `docs/03`; `docs/02` remete a ela (C7).
- **Redação do plano:** corrigir "associados à a sua aplicação" no objetivo geral.
- **Documentação e skills:**
  - o README e `docs/procedimentos.md` declaram a geração e a ordem de execução;
  - `facetacao-e-termos-livres`, `expressoes-de-busca` e `ficha-de-busca-por-base` deixam
    de afirmar uma conferência manual que deixa de ser manual e um comportamento de
    lematização não medido;
  - `questao-e-objetivos` passa a citar "o protocolo" e "o plano", com a seção, em vez de
    caminhos de arquivo.
- **Emenda registrada no histórico**, com alcance de busca e de escopo.

Fora do escopo: a faceta auxiliar local (B5, pendente); a revisão das sementes (B4); a
execução das buscas e o teste de aderência, que seguem o fluxo do protocolo depois da
change. Não existe script que gere as fichas: elas continuam autorais, e a garantia sobre o
plural vem da conferência.

## Capabilities

### New Capabilities
- `geracao-das-strings`: cálculo das STRs a partir do quadro terminológico, regra de
  subsunção, gravação na tabela do protocolo e conferência de igualdade.

### Modified Capabilities
- `leitura-do-protocolo`: "Conferência verifica coerência interna" passa a incluir a
  atribuição única no quadro e a igualdade entre STR e STR gerada.
- `cobertura-por-base`: "Termo da base deriva da STR" passa a aceitar termo subsumido por
  termo vigente; novo requisito de declaração do plural por base, com lastro da lematização.
- `interface-de-comando`: "Ponto de entrada único" passa a listar `strings gerar`.

## Impact

- Código: `src/rsl/` (novo módulo de geração e subcomando `strings`, `conferencia.py`,
  `cobertura.py`, `fichas.py`, `gramatica.py` para a linha `plural` da declaração),
  autoteste com casos que provam cada reprovação nova.
- Documentos: `docs/03_protocolo_estrategia_pesquisa.md` (quadro, STRs, nota do PICo e
  instrumentos); `docs/02_protocolo_informacoes_gerais.md` (obras de referência);
  `docs/01_plano.md` (redação do objetivo geral); `docs/parametros_complementares.md` (G4);
  as quatro fichas, renomeadas de `docs/busca_base_*.md` para
  `docs/procedimentos_busca_*.md` (D12); `config.toml`; `README.md`; `docs/procedimentos.md`;
  `openspec/specs/leitura-do-protocolo/spec.md` (exemplo de cenário); `data/historico.md`.
- Revisão de 2026-11-22 (D10–D13): o teto de caracteres passa a ser parâmetro da
  declaração de cobertura, conferido contra o comprimento de cada consulta; a subseção
  opcional "Estratégia de proximidade" da ficha; as skills da busca deixam de citar base.
- Skills: `facetacao-e-termos-livres`, `expressoes-de-busca`, `ficha-de-busca-por-base`,
  `questao-e-objetivos`.
- Busca:
  - as STRs mudam, e a contagem final de termos é calculada na regeração;
  - população-alvo e recurso disponível saem de STR4;
  - mover `nível de ensino` e afins para STR2 amplia a âncora de domínio e reverte parte da
    emenda v2;
  - os termos de B3 trazem de volta ruído que a emenda v2 tinha retirado;
  - o plural explícito pode levar a ERIC ao teto de caracteres medido.
  Nenhuma execução está registrada, de modo que nenhuma contagem fica vencida. O teste de
  aderência mede o efeito na primeira execução.
