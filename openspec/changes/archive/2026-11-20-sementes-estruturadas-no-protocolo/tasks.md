# Tasks

Nas tarefas, "arquivo de sementes" é o arquivo apontado por `[documentos] sementes` do
`config.toml`. Toda verificação que procura o caminho usa o valor lido dessa chave, e não
um caminho fixo.

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
- [x] 1.4 Confirmar o ponto de partida: `reestruturacao-do-protocolo` está em
  `openspec/changes/archive/`, `openspec validate sementes-estruturadas-no-protocolo`
  aprova, e `rsl conferir` sai com 0, lendo as 10 sementes do arquivo de sementes no
  esquema intermediário. Guardar a saída de `rsl mostrar` (distribuição por base e por
  papel) para a comparação de 2.2.
- [x] 1.5 Localizar a transcrição de 1.2–1.3. Em 2026-11-20 ela estava no scratchpad da
  sessão `0431b7b3…` (`conjunto_semente.toml`, `transcricao.py`, `reconstitui.py`,
  `migra.py`), ainda com a tabela `[[semente]]` no singular.
  - Se ela não existir mais, refazer 1.2 e 1.3 com o mesmo método, partindo do campo
    `semente`.
  - Se existir, trocar a tabela para `[[sementes]]` e refazer a reconstituição de D5
    contra o campo `semente` atual do arquivo de sementes, e não mais contra a célula da
    tabela de bf6b9bf.

  Em qualquer caso, refazer a conferência de 1.3 contra o `data/sementes.json` atual.
  Verificar que:
  - nenhuma semente tem sobra fora dos campos e de `observacoes`;
  - toda diferença entre o texto de `semente` e a célula antiga é apresentada ao
    pesquisador antes de seguir;
  - os `id` seguem SE1 a SE10, sem lacuna.

## 2. Leitor, gramática e arquivo (no mesmo passo)

- [x] 2.1 Trocar na gramática o esquema intermediário do arquivo de sementes pelo
  estruturado de D2. Verificar que:
  - `rsl gramatica` exibe os 19 campos, com tipo e exigência, e não exibe `semente`;
  - o `id` aparece com a exigência de sequência a partir de SE1.
- [x] 2.2 Trocar em `leitura.py` a extração de `semente` pela leitura dos campos,
  removendo `_titulo()` e `_doi()`. No mesmo passo, gravar o arquivo de sementes com o
  conteúdo de 1.5. O protocolo não muda. Verificar que:
  - `rsl conferir` sai com 0;
  - a distribuição por base e por papel em `rsl mostrar` é a mesma guardada em 1.4;
  - uma cópia com SE1, SE2 e SE4, sem SE3, reprova com PROTOCOLO_ILEGIVEL, nomeando SE4.
- [x] 2.3 Remover `data/sementes.json`, `ligacao_semente`, `sincroniza_sementes`,
  `cmd_sincronizar`, o subcomando `sementes sincronizar`, o aviso de órfãs, as chaves
  `[dados] sementes` e `[planilha] campos_autorais` do `config.toml` e do esquema de
  `config.py`, e a coluna `escopo` da planilha. Passar `sementes planilha`,
  `conferir-dados` e `pendencias` a ler os campos de `d["sementes"]` (D7). Verificar que:
  - `grep -rn "sementes.json\|ligacao_semente\|campos_autorais\|sincroniz" src/ config.toml`
    volta vazio;
  - `src/` não contém o valor de `[documentos] sementes`. O caminho só é lido da
    configuração;
  - `config.toml` com a chave antiga `[dados] sementes` reprova, como as outras chaves
    fora do esquema;
  - `semente_aderencia.csv` regenerado tem as mesmas linhas de antes, menos a coluna
    `escopo`.
- [x] 2.4 Relatar em `pendencias` (D4) `doi` ausente, `facetas` vazia, semente de
  validação sem faceta âncora, e `tipo` ou `alinhamento` vazios. Verificar que, com o
  arquivo de 2.2:
  - as 10 sementes aparecem com facetas a informar, e nenhuma reprova;
  - a semente sem `doi`, se houver, aparece com DOI ausente;
  - uma cópia sem o `doi` de SE1 aprova, e `pendencias` relata SE1 com DOI ausente.
- [x] 2.5 Fazer `conferir-dados` reprovar evidência `SEn_…` de semente inexistente (D6).
  Verificar que, no estado atual, `SE10_crossref.*` não reprova.
- [x] 2.6 Exibir em `rsl mostrar` a referência montada dos campos. Verificar com uma
  semente sem `paginas` que não sai marcador vazio, e confirmar que nenhum arquivo é
  gravado.

## 3. Autoteste

- [x] 3.1 Acrescentar ao autoteste os defeitos do esquema estruturado da spec, gerados a
  partir das sementes lidas, e o caso da evidência de semente inexistente. Os casos do
  esquema intermediário que continuam valendo (sequência, sigla, papel, campo
  desconhecido, arquivo ausente) permanecem. Verificar que:
  - cada defeito reprova com o código esperado, inclusive a lacuna na numeração;
  - um caso marcado para esperar aprovação faz o autoteste falhar (desfazer a marcação
    depois);
  - o caso "conjunto sem validação" reprova sobre o arquivo.
- [x] 3.2 Acrescentar os casos que aprovam com pendência: `doi` ausente, `facetas` vazia
  e semente de validação sem faceta âncora. Verificar que aprovam e que `pendencias` os
  relata.

## 4. Coordenação e documentação

- [x] 4.1 Atualizar PD01 em `data/pendencias.json`: tirar `escopo` e `sementes.json`,
  citar o arquivo de sementes pela chave `[documentos] sementes` e manter `tipo` e
  `alinhamento`. Abrir duas pendências do pesquisador:
  - "facetas das sementes a informar";
  - "regra para semente de validação sem faceta âncora", que fica aberta, com a regra em
    branco por decisão de 2026-11-20.
- [x] 4.2 Atualizar as skills `conjunto-semente` e `teste-de-aderencia`. A skill
  `conjunto-semente` passa a dizer:
  - como registrar a semente no arquivo de `[documentos] sementes`, sem citar o caminho;
  - que `bases` é indexação e `facetas` é juízo a partir do resumo ou do texto, nunca do
    ensaio seco;
  - que a retirada sai de tudo e renumera as seguintes (D3), com renomeação da evidência
    bruta, atualização de `pendencias.json` e registro da correspondência de `id` em
    `historico.md`.

  Verificar que `grep -rn "sementes.json\|sincronizar\|ID Semente | Semente" .agents/`
  volta vazio e que `.agents/` não contém o valor de `[documentos] sementes`.
- [x] 4.3 Atualizar o README:
  - Mapa e Scripts;
  - as regras "O que é autoral se preserva" e "Nada se apaga por sincronização";
  - a descrição do conjunto-semente.

  As menções ao arquivo de sementes passam a citar a chave `[documentos] sementes`, e não
  o caminho. Hoje há três menções fixas, no Mapa, na lista de chaves de `[documentos]` e
  na descrição do conjunto-semente. Verificar que:
  - `grep -n "sementes.json\|sincronizar\|ID Semente | Semente" README.md` volta vazio;
  - o README não contém o valor de `[documentos] sementes`.
- [x] 4.4 Registrar em `data/historico.md` a estruturação do conjunto-semente, com data,
  alcance e fundamento. O alcance é: campos estruturados, fusão dos dados de conferência
  (mesmo conteúdo), `escopo` retirado, sequência de `id` mantida com renumeração na
  retirada, e DOI ausente como pendência. As entradas anteriores não são alteradas. A
  mudança de forma do protocolo já foi registrada por `reestruturacao-do-protocolo`.
  Rodar `rsl conferir`, `rsl conferir-dados` e `rsl autoteste`. Verificar que cada um
  termina com o código esperado para o estado de `data/`.

## Workflow follow-up

- Arquivar a change depois da revisão.
