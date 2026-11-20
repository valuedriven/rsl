# Tasks

## 1. Pré-requisitos, transcrição e migração

- [ ] 1.1 Verificar que `refatoracao-dos-scripts` está arquivada (`openspec list --json`
  sem ela; `openspec/specs/gramatica-do-protocolo/spec.md` existe).
- [ ] 1.2 Transcrever no scratchpad as 10 sementes para o esquema de D2, sem completar
  dado de memória. O que não cabe em outro campo vai para `observacoes`, como está, por
  exemplo editores, evento e local da SE10. Rodar a reconstituição de D5. Verificar que:
  - nenhuma semente tem sobra fora dos campos e de `observacoes`;
  - cada semente com `observacoes` não vazio é apresentada ao pesquisador.
- [ ] 1.3 Copiar no scratchpad os dados de conferência de `data/sementes.json` para o
  arquivo de 1.2, casando por DOI. Verificar que:
  - `escopo` está vazio nas 10 sementes, e, se não estiver, parar e levar ao
    pesquisador;
  - cada campo de `campos_autorais`, menos `escopo`, é igual no JSON e no TOML, nas 10
    sementes;
  - `facetas` fica vazia em todas, porque é o pesquisador quem informa.

## 2. Leitor, gramática, arquivo e protocolo (no mesmo passo)

- [ ] 2.1 Acrescentar à gramática o elemento de apontamento de arquivo com esquema (D1,
  D2) e o esquema do conjunto-semente. Verificar que `rsl gramatica` exibe o rótulo e os
  campos com tipo e exigência.
- [ ] 2.2 Substituir em `leitura.py` a leitura da tabela pela do arquivo apontado,
  removendo `_titulo()` e `_doi()`. No mesmo passo:
  - gravar `docs/conjunto_semente.toml` com o conteúdo de 1.3;
  - trocar a tabela pelo apontamento em `docs/03_protocolo_estrategia_pesquisa.md`,
    mantendo a regra de ajuste e a fórmula de recuperação.

  Verificar que:
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
  âncora, e `tipo` ou `alinhamento` vazios. Verificar que, com o arquivo de 1.3, as 10
  sementes aparecem com facetas a informar e que nenhuma reprova.
- [ ] 2.5 Fazer `conferir-dados` reprovar evidência `SEn_…` de semente inexistente (D6).
  Verificar que, no estado atual, `SE10_crossref.*` não reprova.
- [ ] 2.6 Exibir em `rsl mostrar` a referência montada dos campos. Verificar com uma
  semente sem `paginas` que não sai marcador vazio, e confirmar que nenhum arquivo é
  gravado.

## 3. Autoteste

- [ ] 3.1 Acrescentar ao autoteste os onze defeitos da spec e o caso da evidência de
  semente inexistente, gerados a partir das sementes lidas. Verificar que:
  - cada defeito reprova com o código esperado;
  - um caso marcado para esperar aprovação faz o autoteste falhar (desfazer a marcação
    depois);
  - o caso "conjunto sem validação" reprova sobre o arquivo.
- [ ] 3.2 Acrescentar os casos que aprovam com pendência: `facetas` vazia, semente de
  validação sem faceta âncora e lacuna na numeração. Verificar que aprovam e que
  `pendencias` os relata.

## 4. Coordenação e documentação

- [ ] 4.1 Atualizar PD01 em `data/pendencias.json`: tirar `escopo` e `sementes.json` e
  apontar `docs/conjunto_semente.toml`, mantendo `tipo` e `alinhamento`. Abrir a pendência
  "facetas das sementes a informar" e a pendência "regra para semente de validação sem
  faceta âncora", ambas do pesquisador. A segunda fica aberta, com a regra em branco
  por decisão de 2026-11-20.
- [ ] 4.2 Atualizar as skills `conjunto-semente` e `teste-de-aderencia`. A skill
  `conjunto-semente` passa a dizer:
  - como registrar a semente no arquivo;
  - que `bases` é indexação e `facetas` é juízo a partir do resumo ou do texto, nunca do
    ensaio seco;
  - que a retirada sai de tudo e se registra em `historico.md`;
  - que o `id` não se reutiliza.

  Verificar que `grep -rn "sementes.json\|sincronizar\|ID Semente | Semente" .agents/`
  volta vazio.
- [ ] 4.3 Atualizar o README: Mapa, Scripts, as regras "O que é autoral se preserva" e
  "Nada se apaga por sincronização", e a descrição do conjunto-semente. Verificar que
  `grep -n "sementes.json\|sincronizar\|ID Semente | Semente" README.md` volta vazio.
- [ ] 4.4 Registrar em `data/historico.md` a emenda de forma do conjunto-semente, com data,
  alcance (forma e fusão dos dados de conferência, mesmo conteúdo, `escopo` retirado) e
  fundamento. Rodar `rsl conferir`, `rsl conferir-dados` e `rsl autoteste`. Verificar que
  cada um termina com o código esperado para o estado de `data/`.

## Workflow follow-up

- Arquivar a change depois da revisão.
