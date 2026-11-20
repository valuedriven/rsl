# Tasks

## 1. Ponto de partida

- [x] 1.1 Registrar no scratchpad o estado de partida:
  - a saída de `rsl conferir`, que hoje termina com 4;
  - a distribuição por base e por papel e o título, a autoria, o ano e o DOI extraídos de
    cada semente, rodando o leitor de bf6b9bf sobre o protocolo de bf6b9bf (via
    `git worktree` ou cópia);
  - a lista das divergências de forma do design (Context).

  Verificar que o arquivo de partida tem as 10 sementes e as 5 expressões com os papéis
  EB4 executada e EB5 sonda.

## 2. Gramática e leitura do protocolo

- [x] 2.1 Trocar "Palavras significativas" pela tabela de facetas (D3): declarar a seção,
  a tabela e o domínio `Sim`/`Não` na gramática, ler as âncoras da coluna e remover
  `F_FACETA`, `F_ANCORA` e `padroes.ancoras` do `config.toml` e de `config.py`. Acrescentar
  ao autoteste a âncora fora do domínio, o nome vazio e a tabela sem âncora. Verificar que:
  - `rsl mostrar` exibe as âncoras FCT1 e FCT2 com origem no protocolo;
  - `config.toml` com `padroes.ancoras` reprova com CONFIGURACAO;
  - o erro de `rsl conferir` deixa de ser o das facetas.
- [x] 2.2 Ajustar o marcador da estrutura da questão (D6). Verificar que o protocolo atual
  aprova nesse ponto e que o parágrafo retirado numa cópia continua reprovando no
  autoteste.
- [x] 2.3 Trocar o cabeçalho da tabela de expressões e implementar a identificação da
  executada e da sonda pela composição (D1). Remover `[expressoes]`, `padroes.executada`
  e `padroes.sonda` do `config.toml` e de `config.py`. Retirar de `conferir` a verificação
  "sonda que não seja a conjunção das âncoras", que passa a valer por construção.
  Acrescentar ao autoteste o cabeçalho antigo, as duas expressões com `OR` e as duas
  sondas. Verificar que:
  - `rsl mostrar` exibe EB4 executada e EB5 sonda, com origem "protocolo (composição)";
  - `grep -rn "natureza" src/ config.toml` volta vazio;
  - cada caso novo reprova com PROTOCOLO_ILEGIVEL;
  - um caso marcado para esperar aprovação faz o autoteste falhar (desfazer a marcação
    depois).
- [x] 2.4 Declarar as notas explicativas e ler a faixa das notas citadas pela executada
  (D2). Acrescentar ao autoteste a nota citada inexistente e o limite único. Verificar
  que:
  - `rsl mostrar` exibe a faixa 5%–15% com origem no protocolo;
  - numa cópia sem `<` e `>` em N3, a faixa vem do padrão, com origem "padrão
    (config.toml)".
- [x] 2.5 Ler em `conferencia.py` como a fração elegível entre os dois limites é relatada.
  Verificar e registrar no relato da tarefa se ela sai como inconclusiva, como diz N3. Se
  não sair, não mudar o código: levar ao pesquisador como pendência de método.
- [x] 2.6 Remover "Ferramenta de gestão bibliográfica" da gramática, de `fontes()` e da
  exibição de `mostrar` (D5). Verificar que `grep -rn "ferramenta_gestao\|S_FERRAMENTA"
  src/` volta vazio.

## 3. Arquivo de sementes

- [x] 3.1 Declarar na gramática o esquema intermediário do arquivo de sementes, ler
  `docs/conjunto_semente.toml` por `[documentos] sementes` e remover `T_SEMENTES` (D4). Reescrever
  o cabeçalho do `config.toml`, que diz que o conjunto-semente vem só do protocolo.
  Verificar que:
  - `rsl gramatica` exibe o grupo do arquivo de sementes, com os quatro campos;
  - a distribuição por base e por papel em `rsl mostrar` é igual à de 1.1;
  - o título, a autoria, o ano e o DOI extraídos de cada semente são iguais aos de 1.1.
    Toda diferença vai ao pesquisador antes de seguir, sem corrigir o arquivo.
- [x] 3.2 Acrescentar ao autoteste, a partir das sementes lidas, os defeitos do arquivo:
  - TOML quebrado;
  - campo obrigatório retirado;
  - campo desconhecido;
  - `id` repetido;
  - base fora da tabela;
  - `papel` fora do domínio.

  Acrescentar também o caso do arquivo ausente. Verificar que cada defeito reprova com
  PROTOCOLO_ILEGIVEL e que o arquivo ausente termina com CONFIGURACAO.
- [x] 3.3 Rodar `rsl conferir`, `rsl conferir-dados` e `rsl autoteste`. Verificar que
  `conferir` sai com 0, `autoteste` não tem falha e `conferir-dados` termina com o código
  esperado para o estado de `data/`.

## 4. Protocolo, histórico e documentação

- [x] 4.1 Corrigir P5 em `docs/03_protocolo_estrategia_pesquisa.md`. O trecho "Confirmar
  elegibilidade com CE7, regras de exceção e borda e CE8–CE15." passa a "Confirmar
  elegibilidade com CE6 (adequação temática) e CE7–CE9." O restante da célula fica como
  está. Verificar que `grep -n "CE1[0-9]" docs/03_protocolo_estrategia_pesquisa.md` volta
  vazio e que `rsl conferir` continua com 0.
- [x] 4.2 Registrar em `data/historico.md` a emenda de forma, com data, alcance e
  fundamento:
  - facetas em tabela;
  - nova tabela de expressões, com notas;
  - conjunto-semente em `docs/conjunto_semente.toml`;
  - "Ferramenta de gestão bibliográfica" substituída por Procedimentos, Instrumentos e
    Ferramentas;
  - critérios renumerados de CE1 a CE9;
  - P5 corrigido.

  Verificar que o registro cita esta change.
- [x] 4.3 Atualizar o README (Mapa, Scripts, descrição do conjunto-semente e do
  `config.toml`) e as skills que citem a forma antiga. Verificar que
  `grep -rn "Palavras significativas\|Natureza\|ID Semente | Semente\|natureza_executada"
  README.md .agents/` volta vazio, salvo menção histórica explícita.

## Workflow follow-up

- Arquivar a change depois da revisão.
- Retomar `sementes-estruturadas-no-protocolo` a partir da tarefa 1.4 dela.
