# Tasks

## 1. Colunas manuais declaradas uma vez (D3, PD29)

- [x] 1.1 Marcar em `colunas()` (`src/rsl/sementes.py`) quais colunas são manuais e expor
  essa lista. Verificar que `sementes planilha` gera a planilha com o mesmo cabeçalho, na
  mesma ordem: comparar com `data/semente_aderencia.csv` atual antes e depois.
- [x] 1.2 Fazer a docstring e o texto impresso de `busca aderencia`
  (`src/rsl/busca/aderencia.py`) citarem a coluna pela declaração da 1.1, e não por
  literal. Verificar com `grep -rn "indexado\b" src/rsl`, que não deve achar nenhuma
  menção à coluna.

## 2. Preservação e recusa na regravação (D1, D2, D4)

- [x] 2.1 Ler a planilha anterior, quando existe, com o mesmo dialeto da gravação. Arquivo
  ilegível levanta DadosInvalidos (DADOS) e não regrava. Verificar com um arquivo
  corrompido num diretório temporário.
- [x] 2.2 Casar cada linha nova com a anterior por `id`, `base` e título normalizado, e
  copiar as colunas manuais da anterior. Coluna ausente na anterior conta como vazia.
  Verificar pelos cenários "Preenchimento conservado", "Coluna derivada atualizada" e
  "Primeira geração" do spec.
- [x] 2.3 Antes de gravar, levantar o conteúdo manual não vazio que ficaria sem destino:
  linha sem par, título divergente ou coluna fora do esquema com valor. Havendo algum,
  listar `id` × `base` × coluna (e o título divergente), sair com REPROVADO e não tocar no
  arquivo. Linha sem par e vazia é omitida. Verificar pelos cenários de recusa do spec.
- [x] 2.4 Gravar num temporário no mesmo diretório e substituir o anterior só depois de
  fechado. Verificar que, depois de uma recusa, o `SHA256` da planilha não muda.
- [x] 2.5 Acrescentar ao autoteste (`src/rsl/autoteste/sementes.py`, com `ctx.com_config`
  apontando a saída para um diretório temporário) os casos de preservação, de semente
  renumerada recusada, de linha sem par recusada e de primeira geração, com `id`, bases e
  títulos tirados das sementes lidas. Verificar que `python3 -m rsl autoteste` passa.
- [x] 2.6 Demonstrar que os casos reprovam: reverter localmente a gravação para
  `open("w")` sem leitura e ver o caso de preservação falhar; trocar a recusa por descarte
  e ver o caso de recusa falhar; depois restaurar. Registrar o resultado no relato da
  change.
  Resultado (2026-11-22, `python3 -m rsl autoteste`, 234 casos executados): com a leitura
  retirada (`perdas = []`), 6 falhas — preservação, tipo novo com manuais conservadas, e as
  quatro recusas (renumerada, sem par, coluna fora do esquema, ilegível); com a recusa
  trocada por descarte (`if False:`), 3 falhas — renumerada, sem par e coluna fora do
  esquema. `src/rsl/sementes.py` restaurado e conferido idêntico ao anterior por `diff`.
- [x] 2.7 Atualizar a documentação da planilha:
  - no `README.md`, a linha do Mapa de `data/semente_aderencia.csv` ("regravada inteira a
    cada execução" passa a "regravada a cada execução, com as colunas manuais
    preservadas");
  - no `README.md`, em Precedência, a planilha de aderência entra como artefato misto, com
    as colunas manuais editadas no próprio arquivo;
  - na skill `conjunto-semente`, "Retirar uma semente": um passo para a planilha de
    aderência (transferir à mão o preenchimento das renumeradas e esvaziar o da retirada,
    porque `sementes planilha` recusa a regravação até isso ser feito).

  Verificar relendo as três passagens contra o comportamento da 2.3.

## 3. Retorno obrigatório em `busca registrar` (D5, PD28)

- [x] 3.1 Declarar `--retorno` com `required=True` em `src/rsl/__main__.py`. Verificar
  que `python3 -m rsl busca registrar wos EB4 x.txt` sai com USO nomeando `--retorno`, sem
  criar o registro, e que `-h` mostra `--retorno RETORNO` fora de colchetes.
- [x] 3.2 Atualizar a sinopse de `busca registrar` em `docs/procedimentos.md`, M3/E2:
  transcrever o `-h` novo e retirar "(sem ele, nada é registrado e o código é USO)".
  Verificar comparando a sinopse com a saída de `-h`.

## 4. Orientação para registro ausente (D6)

- [x] 4.1 Trocar a mensagem de `src/rsl/dados.py` (`cmd_pendencias`) para orientar o
  registro da primeira execução com `python3 -m rsl busca registrar`. Verificar que
  `python3 -m rsl pendencias` mostra a linha nova e não contém "reconstitua".
- [x] 4.2 Acrescentar ao autoteste o caso que exige, com o registro ausente, que a linha
  de `pendencias` nomeie `busca registrar`. Verificar que ele falha com a mensagem antiga
  e passa com a nova.

## 5. Integração

- [x] 5.1 Rodar `python3 -m rsl conferir` (esperado OK), `python3 -m rsl autoteste`
  (esperado PARCIAL só pelos casos dependentes do registro de execução, com os casos novos
  executados) e `python3 -m rsl sementes planilha` sobre a planilha real (esperado OK e
  conteúdo idêntico ao anterior, conferido por `SHA256`). Registrar os números no relato.
  Resultado (2026-11-22): `conferir` 0 OK; `conferir-dados` 5 DADOS (registro de execução
  ausente, como antes); `autoteste` 6 PARCIAL, 235 casos executados sem falha e 7 não
  executados (os dependentes do registro), contra 225 + 7 antes da change — os 10 novos são
  9 da planilha de aderência e 1 do registro ausente; `sementes planilha` 0 OK, SHA256 de
  `data/semente_aderencia.csv` igual antes e depois (`2712bd0b…72934`) e saída no terminal
  idêntica à de antes da change.
- [x] 5.2 Em `data/pendencias.json`, excluir PD27, PD28 e PD29, e registrar no
  `data/historico.md` a entrada da change com alcance **instrumento** e o que não mudou
  (forma da planilha, `busca sensibilidade`, strings, critérios e limiares).

## 6. Sugestões da verificação

- [x] 6.1 Acrescentar ao autoteste o cenário "Linha anterior sem preenchimento" para base
  que deixou de existir (linha vazia com base fictícia, ausente da tabela de bases).
  Resultado (2026-11-22): o caso reprova a mutação que recusa a linha vazia sem par
  (`if not preenchidas and nova is not None:`), com 2 falhas — ele e o de semente sem par
  vazia; a planilha é restaurada ao fim do caso, para não contaminar o seguinte.
  `autoteste` 6 PARCIAL, 236 casos executados sem falha e 7 não executados.
- [x] 6.2 `src/rsl/busca/registro.py` importa `CMD_REGISTRAR` de `src/rsl/dados.py`, sem
  cópia própria: o caso do registro ausente e as mensagens de `busca` usam a mesma constante.
- [x] 6.3 Corrigir no `proposal.md` (Impact) a menção a `src/rsl/busca/execucao.py`, que
  não mudou (D5).

## Workflow follow-up

- Verificar a change (`openspec-verify-change`) e arquivá-la depois da revisão do
  pesquisador.
- Commit pelo pesquisador.
