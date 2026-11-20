# Tasks

## 1. Pré-requisitos, transcrição e migração

- [x] 1.1 Verificar que `refatoracao-dos-scripts` está arquivada (`openspec list --json`
  sem ela; `openspec/specs/gramatica-do-protocolo/spec.md` existe).
- [x] 1.2 Transcrever no scratchpad as 10 sementes para o esquema de D2, sem completar
  dado de memória. O que não cabe em outro campo vai para `observacoes`, como está, por
  exemplo editores, evento e local da SE10. Rodar a reconstituição de D5. Verificar que:
  - nenhuma semente tem sobra fora dos campos e de `observacoes`;
  - cada semente com `observacoes` não vazio é apresentada ao pesquisador.
- [x] 1.3 Copiar no scratchpad os dados de conferência de `data/sementes.json` para o
  arquivo de 1.2, casando por DOI. Verificar que:
  - `escopo` está vazio nas 10 sementes, e, se não estiver, parar e levar ao
    pesquisador;
  - cada campo de `campos_autorais`, menos `escopo`, é igual no JSON e no TOML, nas 10
    sementes;
  - `facetas` fica vazia em todas, porque é o pesquisador quem informa.
- [ ] 1.4 Verificar que `reestruturacao-do-protocolo` está arquivada e que
  `rsl conferir` sai com 0, com o conjunto-semente lido de `docs/sementes.toml`.
- [ ] 1.5 Localizar a transcrição de 1.2–1.3 no scratchpad. Se ela não existir mais,
  refazer 1.2 e 1.3 com o mesmo método, partindo do campo `semente`. Se existir,
  ajustá-la à tabela `[[sementes]]` e refazer a reconstituição de D5 contra o campo
  `semente` atual de `docs/sementes.toml`, e não mais contra a célula da tabela de
  bf6b9bf. Verificar que:
  - nenhuma semente tem sobra fora dos campos e de `observacoes`;
  - toda diferença entre o texto de `semente` e a célula antiga é apresentada ao
    pesquisador antes de seguir.

## 2. Leitor, gramática e arquivo (no mesmo passo)

- [ ] 2.1 Trocar na gramática o esquema intermediário do arquivo de sementes pelo
  estruturado de D2. Verificar que `rsl gramatica` exibe os 19 campos, com tipo e
  exigência, e não exibe `semente`.
- [ ] 2.2 Trocar em `leitura.py` a extração de `semente` pela leitura dos campos,
  removendo `_titulo()` e `_doi()`, e gravar no mesmo passo `docs/sementes.toml` com o
  conteúdo de 1.5. O protocolo não muda. Verificar que:
  - `rsl conferir` sai com 0;
  - a distribuição por base e por papel em `rsl mostrar` é a mesma de antes da troca.
- [ ] 2.3 Remover `data/sementes.json`, `ligacao_semente`, `sincroniza_sementes`,
  `cmd_sincronizar`, o subcomando `sementes sincronizar`, o aviso de órfãs, as chaves
  `[dados] sementes` e `[planilha] campos_autorais` do `config.toml` e do esquema de
  `config.py`, e a coluna `escopo` da planilha. Passar `sementes planilha`,
  `conferir-dados` e `pendencias` a ler os campos de `d["sementes"]` (D7). Verificar que:
  - `grep -rn "sementes.json\|ligacao_semente\|campos_autorais\|sincroniz" src/ config.toml`
    volta vazio;
  - `config.toml` com a chave antiga `[dados] sementes` reprova, como as outras chaves
    fora do esquema;
  - `semente_aderencia.csv` regenerado tem as mesmas linhas de antes, menos a coluna
    `escopo`.
- [ ] 2.4 Relatar em `pendencias` (D4) `facetas` vazia, semente de validação sem faceta
  âncora, e `tipo` ou `alinhamento` vazios. Verificar que, com o arquivo de 2.2, as 10
  sementes aparecem com facetas a informar e que nenhuma reprova.
- [ ] 2.5 Fazer `conferir-dados` reprovar evidência `SEn_…` de semente inexistente (D6).
  Verificar que, no estado atual, `SE10_crossref.*` não reprova.
- [ ] 2.6 Exibir em `rsl mostrar` a referência montada dos campos. Verificar com uma
  semente sem `paginas` que não sai marcador vazio, e confirmar que nenhum arquivo é
  gravado.

## 3. Autoteste

- [ ] 3.1 Acrescentar ao autoteste os defeitos do esquema estruturado da spec e o caso da
  evidência de semente inexistente, gerados a partir das sementes lidas. Os casos do
  esquema intermediário, já cobertos por `reestruturacao-do-protocolo`, continuam.
  Verificar que:
  - cada defeito reprova com o código esperado;
  - um caso marcado para esperar aprovação faz o autoteste falhar (desfazer a marcação
    depois);
  - o caso "conjunto sem validação" reprova sobre o arquivo.
- [ ] 3.2 Acrescentar os casos que aprovam com pendência: `facetas` vazia, semente de
  validação sem faceta âncora e lacuna na numeração. Verificar que aprovam e que
  `pendencias` os relata.

## 4. Coordenação e documentação

- [ ] 4.1 Atualizar PD01 em `data/pendencias.json`: tirar `escopo` e `sementes.json` e
  apontar `docs/sementes.toml`, mantendo `tipo` e `alinhamento`. Abrir a pendência
  "facetas das sementes a informar" e a pendência "regra para semente de validação sem
  faceta âncora", ambas do pesquisador. A segunda fica aberta, com a regra em branco
  por decisão de 2026-11-20.
- [ ] 4.2 Atualizar as skills `conjunto-semente` e `teste-de-aderencia`. A skill
  `conjunto-semente` passa a dizer:
  - como registrar a semente em `docs/sementes.toml`;
  - que `bases` é indexação e `facetas` é juízo a partir do resumo ou do texto, nunca do
    ensaio seco;
  - que a retirada sai de tudo e se registra em `historico.md`;
  - que o `id` não se reutiliza.

  Verificar que `grep -rn "sementes.json\|sincronizar\|ID Semente | Semente" .agents/`
  volta vazio.
- [ ] 4.3 Atualizar o README: Mapa, Scripts, as regras "O que é autoral se preserva" e
  "Nada se apaga por sincronização", e a descrição do conjunto-semente. Verificar que
  `grep -n "sementes.json\|sincronizar\|ID Semente | Semente" README.md` volta vazio.
- [ ] 4.4 Registrar em `data/historico.md` a estruturação do conjunto-semente, com data,
  alcance (campos estruturados e fusão dos dados de conferência, mesmo conteúdo, `escopo`
  retirado) e fundamento. A mudança de forma do protocolo já foi registrada por
  `reestruturacao-do-protocolo`. Rodar `rsl conferir`, `rsl conferir-dados` e
  `rsl autoteste`. Verificar que cada um termina com o código esperado para o estado de
  `data/`.

## Workflow follow-up

- Arquivar a change depois da revisão.
