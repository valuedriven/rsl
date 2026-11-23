# Tasks

## 1. Chave antiga da configuração

- [x] 1.1 Mover `documentos.ficha` para `config.RETIRADAS`, com motivo que nomeie `[documentos] procedimento`, e retirar `RENOMEADAS`, `_renomeia` e o parâmetro `avisa` de `valida`; no autoteste da configuração, trocar os casos de chave renomeada por um caso que exija CONFIGURACAO com `[documentos] procedimento` na mensagem; verificar com `PYTHONPATH=src python3 -m rsl projeto autoteste` (grupo da configuração sem falha)

## 2. Comandos antigos

- [x] 2.1 Retirar `ALIASES`, `_com_aviso`, o laço de aliases, o parâmetro `aliases` de `_parser` e a forma oculta de grupo em `src/rsl/__main__.py`; verificar que `python3 -m rsl busca aderencia` e `python3 -m rsl conferir` saem com código 2 (USO)
- [x] 2.2 Substituir `src/rsl/autoteste/aliases.py` pelo grupo "nomes antigos recusados": os onze nomes antigos exigem USO e cada canônico correspondente não dá USO; verificar que o grupo passa e que reprova quando um alias é reposto temporariamente no parser (demonstração no relato abaixo, e não no histórico, que não guarda resultado de conferência)

## 3. Catálogo sem correspondência de nomes

- [x] 3.1 Retirar de `src/rsl/catalogo.py` `SKILLS_RENOMEADAS`, `CODIGO_ISENTO`, `_vivos`, `_padroes_antigos`, os campos `aliases`, `renomeadas`, `chaves` e `vivos` de `Entradas`, a regra `nome_antigo`, os filtros de alias e a seção/campo `correspondencia`; retirar do autoteste do catálogo os casos de nome antigo; verificar com o autoteste (grupo do catálogo sem falha) e com `catalogo gerar --json` sem o campo `correspondencia`
- [x] 3.2 Regravar `docs/catalogo_de_apoio.md` com `PYTHONPATH=src python3 -m rsl catalogo gerar --gravar` e verificar que a seção "Correspondência de nomes" sumiu e que `catalogo gerar` sem `--gravar` sai 0

## 4. Registro e integração

- [x] 4.1 Registrar a remoção e a decisão (opção 2) em `data/historico.md`, conferindo antes o formato das entradas existentes
- [x] 4.2 Verificar a integração: `projeto autoteste` sem nenhum caso falho (a linha de base é PARCIAL, com 9 casos não executados por `data/registro_execucao.json` ausente, e isso não muda); `grep` por `ALIASES`, `RENOMEADAS`, `SKILLS_RENOMEADAS`, `CODIGO_ISENTO` e `nome_antigo` em `src/rsl/` não encontra nada; `openspec validate remocao-dos-aliases-de-transicao` passa

## Relato da aplicação (2026-11-23)

- Demonstração da 2.2, feita com um parser montado em memória e sem alterar o código-fonte:
  com `conferir` e `busca aderencia` repostos como aliases, os dois casos correspondentes
  reprovam; com um parser que recusa todo comando, as onze contraprovas reprovam; com o
  parser real, o grupo passa.
- Linha de base do autoteste, antes da change: PARCIAL, sem caso falho e com os casos
  dos arquivos alimentados não executados (`data/registro_execucao.json` ausente).

## Workflow follow-up

- Arquivar a change depois da revisão do pesquisador.
