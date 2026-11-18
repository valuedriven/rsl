# Tasks

## 1. Papéis das expressões em `protocolo.py`

- [ ] 1.1 Implementar `papeis(d)` (D1), gravar em `d["papeis"]` em `analisa()` e fazer `_coerencia_expressoes` usá-la; verificar com `--mostrar`/inspeção que as específicas são EB2 e EB3, a geral EB1, a executada EB4 e a sonda EB5, e que `--conferir --autoteste` continua passando

## 2. `derivar_expressoes.py` e `gen_semente.py`

- [ ] 2.1 Registrar, antes de alterar, a saída de `_prova_da_composicao()`, `DERIVAVEIS`, `BASE_CANONICA`, `BD_DE` e `SLUG_DE_BD` (linha de base)
- [ ] 2.2 Reescrever `_prova_da_composicao` pelas relações de D2, sem identificador de expressão fixado; verificar que a prova não reporta problema no protocolo atual, que `DERIVAVEIS` coincide com a linha de base e que, com a executada alterada numa composição em memória, a prova reprova
- [ ] 2.3 Derivar `BASE_CANONICA` de `protocolo.FICHAS` (D3); verificar que `BASE_CANONICA`, `BD_DE` e `SLUG_DE_BD` coincidem com a linha de base
- [ ] 2.4 Trocar `BASES` de `gen_semente.py` por `protocolo.BASES`; verificar que a lista e a ordem coincidem com a anterior
- [ ] 2.5 Verificar com `grep -nE '"EB[0-9]"|"WoS"|"BRAPCI"' src/derivar_expressoes.py src/gen_semente.py` que não sobra identificador fixado fora de mensagens de ajuda e exemplos de uso

## 3. Autoteste

- [ ] 3.1 Acrescentar `_autoteste_validacao` (D4) com os casos de instrumentos e verificar que passam e que cada um falha se a condição for invertida
- [ ] 3.2 Acrescentar a `_autoteste_bases` o caso de defeito só na BRAPCI e verificar que passa
- [ ] 3.3 Fazer o resumo do autoteste informar à parte os casos não executados e o motivo; verificar que, sem `data/sementes.json`, o resumo diz que os casos dos arquivos alimentados não foram executados

## 4. Integração

- [ ] 4.1 Rodar `python3 -I -S src/protocolo.py --conferir --autoteste`, `--mostrar` e `--pendencias`, `python3 -I -S src/derivar_expressoes.py --help` e `python3 -I -S src/gen_semente.py`; verificar que passam ou que só falham pela ausência dos arquivos de `data/`, como antes

## Workflow follow-up

- Arquivar `protocolo-fonte-unica` antes desta change.
- Arquivar esta change depois da revisão do pesquisador.
