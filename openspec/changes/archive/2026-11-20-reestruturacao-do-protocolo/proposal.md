# Proposal

## Why

O pesquisador reestruturou o protocolo (`docs/03_protocolo_estrategia_pesquisa.md`) depois
do commit bf6b9bf, e o leitor não o lê mais: `rsl conferir` sai com 4
(PROTOCOLO_ILEGIVEL) já na primeira seção que mudou. Enquanto a leitura não voltar a
aprovar, nenhum subcomando que dependa do protocolo roda, e a change
`sementes-estruturadas-no-protocolo` está parada à espera disso.

A mudança é de forma: a gramática do leitor tem de acompanhar o documento que o
pesquisador escreveu, e não o contrário.

## What Changes

Modificações do protocolo, já feitas pelo pesquisador, que o leitor passa a aceitar:

- **BREAKING (forma) — Facetas em tabela.** A seção "Palavras significativas da questão de
  revisão" sai. Entra "Facetas da questão de revisão", com a tabela
  `Id faceta | Faceta | Âncora obrigatória`. As âncoras são lidas da coluna, com `Sim` ou
  `Não`.
- **BREAKING (forma) — Expressões de busca reestruturadas.** A tabela passa a
  `ID | Expressão de busca | Função protocolar`, e as colunas "Natureza" e "Detalhamento"
  saem. A subseção `### Notas explicativas` traz uma nota `- Nn — …` por função, citada na
  tabela como `(Nn)`. O parágrafo "Operadores de proximidade e restrição por campo" sai do
  protocolo. A proximidade continua tratada nas fichas de busca.
- **Executada e sonda identificadas pela composição**, por decisão do pesquisador
  (2026-11-20). A executada é a única expressão com grupo `OR`, e a sonda é a única
  formada só pelas âncoras. Saem a seção `[expressoes]` do `config.toml` e os padrões
  `padroes.executada` e `padroes.sonda`.
- **Faixa de sensibilidade lida da nota da executada.** Os limites `< N%` e `> M%` estão
  agora em N3, que é a nota de EB4. Antes eram lidos do detalhamento da sonda.
- **BREAKING (forma) — Conjunto-semente em arquivo próprio.** A tabela de sementes sai do
  protocolo e vai para `docs/conjunto_semente.toml`, com `[[sementes]]` e os campos `id`,
  `semente`, `bases` e `papel`. O caminho fica no `config.toml` (`[documentos] sementes`)
  e o protocolo não o cita, por decisão do pesquisador (2026-11-20). A seção
  "Conjunto-semente" continua no protocolo, com a regra de ajuste e a fórmula de
  recuperação. Este formato é **intermediário**: a decomposição de `semente` em campos
  fica com `sementes-estruturadas-no-protocolo`.
- **Seção "Ferramenta de gestão bibliográfica" retirada.** O conteúdo passou às tabelas
  "Procedimentos", "Instrumentos" e "Ferramentas", que o leitor não interpreta.
- **Marcador da estrutura da questão reescrito**, como "A estrutura da questão…".
- **Critérios renumerados de CE1 a CE9**, sem lacuna.
- **P5 corrigido.** O procedimento citava "CE7, regras de exceção e borda e CE8–CE15",
  numeração que não existe mais. Passa a citar CE6 (adequação temática) e CE7–CE9.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-do-protocolo`: as facetas e âncoras são lidas da tabela, e a linha
  `Faceta n (FCTn)` sai. O conjunto-semente é lido do arquivo de sementes, e não mais de
  tabela do protocolo. Executada e sonda são identificadas pela composição. Entram as
  notas explicativas, com a faixa lida da nota da executada. O cabeçalho da tabela de
  expressões é conferido contra a gramática. Mudam os parâmetros estruturais.
- `gramatica-do-protocolo`: o contrato passa a cobrir também o arquivo de sementes.
- `derivacao-das-expressoes`: as deriváveis vêm dos papéis identificados pela composição.
  O caminho do arquivo de sementes vem do `config.toml`, e o papel da planilha de
  aderência vem desse arquivo.

## Impact

- `src/rsl/gramatica.py`:
  - saem `S_PALAVRAS`, `F_FACETA`, `F_ANCORA`, `T_SEMENTES`, `S_FERRAMENTA` e
    `F_FERRAMENTA`;
  - mudam `M_ESTRUTURA`, `T_EXPRESSOES` e `F_FAIXA`;
  - entram a tabela de facetas, as notas explicativas e o esquema do arquivo de sementes.
- `src/rsl/leitura.py`:
  - funções afetadas: `facetas`/`ancoras`, `expressoes`, a leitura das sementes e
    `fontes`, de onde sai `ferramenta_gestao`;
  - `_titulo()` e `_doi()` continuam, agora sobre o campo `semente`.
- `src/rsl/config.py` e `config.toml`:
  - saem `[expressoes]`, `padroes.executada`, `padroes.sonda` e `padroes.ancoras`;
  - entra `[documentos] sementes`;
  - o cabeçalho que diz que o conjunto-semente "vem só do protocolo" é reescrito.
- `src/rsl/conferencia.py` e `relatorio.py` (`mostrar`), além do autoteste.
- `docs/03_protocolo_estrategia_pesquisa.md`: só P5. As demais mudanças já foram feitas
  pelo pesquisador.
- `docs/conjunto_semente.toml`, já criado pelo pesquisador, passa a ser lido. `data/sementes.json`
  continua como está até `sementes-estruturadas-no-protocolo`.
- `data/historico.md`: registro da emenda de forma.
- `README.md` e as skills que citam a tabela de sementes, a coluna Natureza ou as
  "Palavras significativas".
- **Desbloqueia** `sementes-estruturadas-no-protocolo`, que retoma depois do arquivamento
  desta.
