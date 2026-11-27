# Tarefas

## 1. Esquema e leitura

- [x] 1.1 Tipo `booleano` em `CampoToml` e `verificacao` booleano na gramática; ausente
  vale `false` na leitura. Verificar: `documentos gramatica` mostra o tipo; texto reprova.
- [x] 1.2 Pendência por `verificacao` diferente de `true` (`dados.campo_pendente`); planilha
  com `sim`/`não` e contagem de confirmadas pelo booleano.

## 2. Migração e documentação

- [x] 2.1 `docs/conjunto_semente.toml`: `verificacao = true` nas 12 sementes, texto anterior
  no início da `nota`, sem o prefixo de estado; os demais campos intactos (conferido com
  `tomllib`).
- [x] 2.2 Skills `definir-conjunto-semente` e `conferir-referencia`.

## 3. Prova

- [x] 3.1 Autoteste: verificação como texto reprova; `false` e ausente são pendência; `true`
  não é; regravação da planilha alterna `sim`/`não`. Verificar: cada caso falha com a
  regra desfeita (texto aceito, pendência nunca relatada, planilha com o texto do valor).
- [x] 3.2 Regenerar procedimentos e planilha; `projeto autoteste`, `documentos conferir`,
  `dados conferir` e `catalogo gerar` saem OK.
