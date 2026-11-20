# Proposal

## Why

`src/protocolo.py` tem 3212 linhas e reúne leitura, conferência, fichas, cobertura, dados
alimentados, autoteste e CLI. Os outros três scripts o importam e analisam o protocolo
**no momento da importação**. A exploração de 2026-11-19 verificou os seguintes defeitos,
que não aparecem como reprovação, mas tiram a confiança no que os scripts dizem:

- **O código de saída 1 significa coisas diferentes.** Conferência reprovada, protocolo
  ilegível, configuração inválida e arquivo alimentado ausente saem todos com 1. O
  autoteste parcial sai com 0.
- **Há conteúdo fixado fora do `config.toml`.**
  - `derivar_expressoes.py` fixa o caminho do `registro_execucao.json` e o nome de cada
    saída.
  - `gen_semente.py` fixa os caminhos de `sementes.json` e da planilha.
  - As mutações do autoteste procuram literais do protocolo atual (`"| SE10 |"`,
    `"**< 5%**"`, `"| brased |"`), e qualquer emenda legítima as quebra.
- **A gramática que o leitor exige do protocolo não está documentada.** Títulos de seção,
  cabeçalhos, rótulos e padrões estão espalhados em cerca de 25 expressões regulares.
- **Há código morto e duplicado.** `relatorio_bases()` não é chamada. Existem duas
  `normaliza()` com normalizações Unicode diferentes (NFKD e NFD).
- **Os nomes são incoerentes.** Os scripts seguem três padrões (`protocolo`,
  `derivar_expressoes`, `gen_semente`), e a planilha de validação se chama
  `validacao_termologica.csv`, com erro de grafia ("termológica" refere-se a calor).
- **`validar_termos.py` repete a requisição automaticamente depois de um erro de rede**,
  o que o AGENTS.md §9 proíbe.

O momento é este porque nenhuma execução foi registrada, e a única saída gerada em `data/`
é `semente_aderencia.csv`, que se regenera. A change `conjunto-semente-independente` já
alterou o código, sem commit em 2026-11-19. A change `revisao-das-strings-por-faceta`
ainda vai mexer no `protocolo.py`, e fazer a refatoração antes dela evita conflito e
retrabalho.

## What Changes

- **O código passa ao pacote `src/rsl/`.** A leitura, as conferências, as fichas, a
  cobertura, os dados alimentados, a derivação, a validação terminológica, o instrumento de
  aderência e o autoteste ficam em módulos coesos. Importar um módulo não lê configuração
  nem protocolo.
- **BREAKING: um ponto de entrada único, `python3 -m rsl <subcomando>`.** Os subcomandos se
  agrupam por atividade (`conferir`, `conferir-dados`, `autoteste`, `mostrar`,
  `pendencias`, `gramatica`, `sementes …`, `termos …`, `busca …`). Os scripts
  `src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
  `src/gen_semente.py` deixam de existir. README, skills e fichas migram para os
  subcomandos.
- **BREAKING: códigos de saída semânticos e iguais em todos os subcomandos:** 0 OK, 1
  REPROVADO, 2 USO, 3 CONFIGURACAO, 4 PROTOCOLO_ILEGIVEL, 5 DADOS, 6 PARCIAL e
  7 FONTE_EXTERNA.
- **Contrato de gramática do protocolo.** Os literais de forma que o leitor exige ficam num
  único lugar do código. O contrato legível é impresso a partir dele (`rsl gramatica`), e
  não há cópia mantida à mão.
- **Retirada do conteúdo fixado e do código morto:**
  - todos os caminhos de entrada e de saída vêm do `config.toml`;
  - as mutações do autoteste são geradas a partir da estrutura lida, e não de literais do
    protocolo atual;
  - as docstrings deixam de descrever a composição vigente;
  - sai uma das duas `normaliza()` e sai `relatorio_bases()`.
- **BREAKING: convenção de nomes.**
  - Os subcomandos usam verbo no infinitivo.
  - Os arquivos derivados usam `snake_case` em português, sem acento, com o substantivo do
    conteúdo e o sufixo de chave em minúsculas.
  - `validacao_termologica.csv` passa a `validacao_terminologica.csv`, e
    `fidelidade_EB<n>.csv` passa a `fidelidade_eb<n>.csv`.
- **Fonte externa sem nova tentativa automática.** Erro de rede, bloqueio, captcha ou
  limite interrompe a validação terminológica com o código FONTE_EXTERNA.

## Capabilities

### New Capabilities

- `interface-de-comando`: o ponto de entrada único, os subcomandos, os códigos de saída,
  a convenção de nomes dos subcomandos e dos arquivos derivados, e a ausência de efeito na
  importação.
- `gramatica-do-protocolo`: o contrato de forma que o leitor exige do protocolo e das
  fichas (seções, tabelas, colunas, rótulos e padrões), com fonte única e exibição a partir
  do próprio leitor.

### Modified Capabilities

- `leitura-do-protocolo`:
  - "Nenhum parâmetro fixado no código" passa a valer para todo `src/` e para os caminhos de
    saída;
  - o autoteste deixa de depender de literais do protocolo vigente;
  - o protocolo ilegível e a configuração inválida ganham código próprio;
  - o autoteste parcial sai com PARCIAL.
- `derivacao-das-expressoes`: "Saídas preservadas" admite a renomeação dos arquivos de
  saída pela convenção, com o conteúdo idêntico.
- `validacao-terminologica`: falha de fonte externa interrompe sem nova tentativa, com o
  código próprio; o nome da planilha vem da configuração.

## Impact

- **Código.** `src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
  `src/gen_semente.py` são substituídos por `src/rsl/`.
- **Configuração.** O `config.toml` ganha os nomes dos arquivos de saída e o nome corrigido
  da planilha de validação.
- **Documentação.** README (comandos de M3 e seção Scripts), as skills em `.agents/skills/`
  que citam comandos e as fichas `docs/busca_base_*.md`, onde citarem comandos.
- **Fora do alcance.** O conteúdo do protocolo não muda. As saídas mudam só de nome,
  conforme a convenção.
- **Ordem.**
  - Esta change parte do código com as alterações de `conjunto-semente-independente`
    (papel da semente, aderência por papel, intervalo de Wilson), depois de elas terem
    commit.
  - Ela precede `sementes-estruturadas-no-protocolo`.
  - Deve ser arquivada antes de `revisao-das-strings-por-faceta` implementar a sua parte
    em código.
