# Proposal

## Why

A verificação dos termos em vocabulários controlados grava uma planilha
(`data/validacao_terminologica.csv`) com 19 colunas, que mistura o resultado técnico da
consulta com a decisão do pesquisador. Ela também guarda em `data/evidencia/<instrumento>/` a
resposta bruta de cada consulta, inclusive de termos já fora do protocolo ou de consultas já
refeitas. O pesquisador precisa ver o estatuto vigente de cada termo e a sua decisão, sem o
excesso.

## What Changes

- Revisar a forma da planilha de validação pelo critério de quem a edita. A decisão do
  pesquisador (`decisao_ReT`, `justificativa_ReT`) fica num formato confortável de editar
  (CSV ou TOML). O que só o script grava e lê vai para JSON ou para `tmp/`. O formato
  decide-se no design.
- Reduzir as colunas ao que sustenta a decisão vigente.
- Reavaliar `data/evidencia/{brased,eric,tbci,unesco,instrumentos}/`. As duas alternativas
  são versionar só a evidência da consulta vigente de cada termo do protocolo, ou levar a
  resposta bruta a `tmp/` e reconsultar para reproduzir. Decide o pesquisador.
- Expurgar a evidência de termos fora do protocolo e de consultas substituídas.
- Sincronizar os registros sempre a partir dos termos do protocolo: a decisão, a linha
  técnica e a evidência de termo retirado são removidas, sem histórico de termos.
- Revisar a skill `estabelecer-controle-terminologico`.

Independente do Zotero e das demais changes. Esta change não gera entrada no
`data/historico.md`.

## Capabilities

### New Capabilities
<!-- nenhuma -->

### Modified Capabilities
- `validacao-terminologica`: forma e colunas do registro da validação; destino e
  permanência da evidência bruta por instrumento.
- `interface-de-comando`: chave `[dados] validacao` e `[planilha] campos_validacao`, se o
  formato mudar.

## Impact

- Código: `src/rsl/termos/{validacao,decisao,planejamento,tematres}.py`, autotestes de
  validação.
- Dados: `data/validacao_terminologica.csv`, `data/evidencia/{brased,eric,tbci,unesco,instrumentos}/`.
- Configuração: `[dados] validacao`, `[planilha]`.
- Skill: `.agents/skills/estabelecer-controle-terminologico/`.
