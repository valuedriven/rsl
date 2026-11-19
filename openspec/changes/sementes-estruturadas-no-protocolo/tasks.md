# Tasks

## 1. Pré-requisitos e decisões

- [ ] 1.1 Verificar que `refatoracao-dos-scripts` está arquivada (`openspec list --json`
  sem ela; `openspec/specs/gramatica-do-protocolo/spec.md` existe). Perguntar ao
  pesquisador se o protocolo é editado como `.md` ou exportado de um editor de texto, e
  registrar a resposta no design.
- [ ] 1.2 Transcrever no scratchpad as 10 sementes para o bloco TOML de D1, sem completar
  dado de memória. Rodar a reconstituição de D4 e apresentar ao pesquisador as sobras de
  cada semente, como editores e evento da SE10. Verificar que:
  - cada sobra tem destino decidido (campo existente, campo novo no esquema ou
    descartada com justificativa);
  - a decisão consta de `data/historico.md`.

## 2. Leitor, gramática e protocolo (no mesmo passo)

- [ ] 2.1 Acrescentar à gramática o elemento de bloco cercado com esquema (D2, D3) e o
  esquema do conjunto-semente. Verificar que `rsl gramatica` exibe os campos com tipo e
  exigência.
- [ ] 2.2 Substituir em `leitura.py` a leitura da tabela pela do bloco, removendo
  `_titulo()` e `_doi()`. No mesmo passo, trocar a tabela pelo bloco de 1.2 em
  `docs/03_protocolo_estrategia_pesquisa.md`. Verificar que:
  - `rsl conferir` sai com 0;
  - a distribuição por base em `rsl mostrar` é a mesma da referência anterior à troca.
- [ ] 2.3 Exibir em `rsl mostrar` a referência montada dos campos. Verificar com uma
  semente sem `paginas` que não sai marcador vazio, e confirmar que nenhum arquivo é
  gravado.

## 3. Autoteste e dados alimentados

- [ ] 3.1 Acrescentar ao autoteste os oito defeitos da spec, mais `papel` fora do domínio, gerados das sementes lidas.
  Verificar que:
  - cada um reprova com PROTOCOLO_ILEGIVEL;
  - um caso marcado para esperar aprovação faz o autoteste falhar (desfazer a marcação
    depois).
- [ ] 3.2 Rodar `rsl sementes sincronizar` sobre uma cópia de `data/sementes.json`.
  Verificar que:
  - o arquivo sai idêntico;
  - as 10 ligações casam;
  - `rsl pendencias` não relata semente órfã.

## 4. Coordenação e documentação

- [ ] 4.1 Ajustar as exigências sobre a coluna `Papel` para o campo `papel`: na spec
  promovida, se `conjunto-semente-independente` estiver arquivada; na delta dela, se não
  estiver. Verificar com `openspec validate` na change afetada, ou na spec, e com o caso
  de autoteste "conjunto sem validação" reprovando sobre o bloco.
- [ ] 4.2 Atualizar a skill `conjunto-semente` (como registrar a semente no protocolo) e o
  README (Mapa e seção Scripts, onde descrevem a tabela de sementes). Verificar que
  `grep -rn "ID Semente | Semente"` em `README.md` e `.agents/` volta vazio.
- [ ] 4.3 Registrar em `data/historico.md` a emenda de forma do conjunto-semente, com data,
  alcance (só forma, mesmo conteúdo) e fundamento. Rodar `rsl conferir`,
  `rsl conferir-dados` e `rsl autoteste`. Verificar que cada um termina com o código
  esperado para o estado de `data/`.

## Workflow follow-up

- Arquivar a change depois da revisão.
