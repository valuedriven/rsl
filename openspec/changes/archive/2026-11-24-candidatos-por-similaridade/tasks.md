# Tasks

## 1. Cliente e proposta

- [x] 1.1 Em `termos/planejamento.py`, acrescentar `STATUS_CANDIDATO` e `SEM_SUGESTAO` (design D2). Em `termos/tematres.py`, depois de busca sem casamento exato, consultar `suggestDetails` com o termo inteiro; item único vira candidato, com as relações dele; vários itens vão todos para `sugestao_similar`, sem escolha (design D1); gravar `suggestDetails` no registro bruto (design D4). Verificar com casos de autoteste sobre respostas em memória: os quatro desfechos do requisito "Termo sem casamento exato consulta a similaridade", com respostas capturadas na sondagem de 2026-11-24 (ERIC e UNESCO `teaching method`).
- [x] 1.2 Acrescentar `sugestao_similar` a `planilha.campos_validacao` no `config.toml`, depois de `forma_no_instrumento`, e preenchê-la só em linha sem casamento exato, com a sugestão ou `SEM_SUGESTAO`. Verificar com `termos exportar` sobre cópia em `RSL_CONFIG` de ensaio, que traz a coluna.

## 2. Reabertura

- [x] 2.1 Em `motivo_reabertura` (`termos/validacao.py`), reabrir linha de instrumento `Automático`, sem decisão, com termo livre não localizado e `sugestao_similar` vazia (design D3); com decisão, preservar e listar. Verificar com os casos do requisito "Linha não localizada sem similaridade volta a aguardar consulta" em planilha em memória, demonstrando que o autoteste falha com a regra desligada.
- [x] 2.2 Contar as linhas candidatas no resumo de `grava_planilha`. Verificar no resumo do ensaio da 1.2.

## 3. Sonda e documentação

- [x] 3.1 `termos sondar` mostra os itens de `suggestDetails` para cada termo de prova e para o termo inexistente (design D5). Verificar com caso de autoteste que a sonda não grava nada, rodando `termos sondar` uma vez e conferindo que a planilha não mudou (sha1 antes e depois); parada em FONTE_EXTERNA encerra a tarefa e volta ao pesquisador.
- [x] 3.2 Atualizar a skill `validacao-vocabulario-controlado` (§4 status candidato e coluna `sugestao_similar`, §5 sonda) e regenerar o catálogo se a ajuda mudar. Verificar com `catalogo gerar` sem divergência.

## 4. Validação refeita (depois da conferência da sonda pelo pesquisador)

- [x] 4.1 Pesquisador confere na saída da 3.1 os itens de `suggestDetails` e autoriza seguir. Verificar pela resposta do pesquisador na conversa.
- [x] 4.2 `termos exportar` e `termos validar todos`. Verificar contando na planilha, por instrumento, os status propostos; nenhuma linha de termo livre não localizado com `sugestao_similar` vazia; toda linha com `arquivo_evidencia` existente. Parada em FONTE_EXTERNA é relatada ao pesquisador, sem nova tentativa.

## 5. Integração

- [x] 5.1 `projeto autoteste` sem falha, `documentos conferir` e `catalogo gerar` sem falha; `openspec validate candidatos-por-similaridade --strict` válido.
