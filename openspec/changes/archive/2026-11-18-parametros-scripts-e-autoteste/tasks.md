# Tasks

## 1. Papéis das expressões em `protocolo.py`

- [x] 1.1 Implementar `papeis(d)` (D1), gravar em `d["papeis"]` em `analisa()` e fazer `_coerencia_expressoes` usá-la; verificar com `--mostrar`/inspeção que as específicas são EB2 e EB3, a geral EB1, a executada EB4 e a sonda EB5, e que `--conferir --autoteste` continua passando

## 2. `derivar_expressoes.py` e `gen_semente.py`

- [x] 2.1 Registrar, antes de alterar, a saída de `_prova_da_composicao()`, `DERIVAVEIS`, `BASE_CANONICA`, `BD_DE` e `SLUG_DE_BD` (linha de base)
- [x] 2.2 Reescrever `_prova_da_composicao` pelas relações de D2, sem identificador de expressão fixado; verificar que a prova não reporta problema no protocolo atual, que `DERIVAVEIS` coincide com a linha de base e que, com a executada alterada numa composição em memória, a prova reprova
- [x] 2.3 Derivar `BASE_CANONICA` de `protocolo.FICHAS` (D3); verificar que `BASE_CANONICA`, `BD_DE` e `SLUG_DE_BD` coincidem com a linha de base
- [x] 2.4 Trocar `BASES` de `gen_semente.py` por `protocolo.BASES`; verificar que a lista e a ordem coincidem com a anterior
- [x] 2.5 Verificar com `grep -nE '"EB[0-9]"|"WoS"|"BRAPCI"' src/derivar_expressoes.py src/gen_semente.py` que não sobra identificador fixado fora de mensagens de ajuda e exemplos de uso

## 3. Autoteste

- [x] 3.1 Acrescentar `_autoteste_validacao` (D4) com os casos de instrumentos e verificar que passam e que cada um falha se a condição for invertida
- [x] 3.2 Acrescentar a `_autoteste_bases` o caso de defeito só na BRAPCI e verificar que passa
- [x] 3.3 Fazer o resumo do autoteste informar à parte os casos não executados e o motivo; verificar que, sem `data/sementes.json`, o resumo diz que os casos dos arquivos alimentados não foram executados

## 4. Escopo acrescentado pelo pesquisador (2026-11-18)

- [x] 4.1 Ler a composição na forma estrita `STRn AND STRn AND (STRn OR STRn)` em `_grupos_de_composicao`: `AND` maiúsculo como única conjunção, `OR` só dentro de parênteses; `+` e operador em minúscula reprovam com mensagem nomeada; atualizar as mutações do autoteste que usam `\+` e acrescentar as de `+` e de `and`; verificar que cada nova reprova
- [x] 4.2 Uniformizar a redação da composição com `AND`: bloco de expressões das quatro fichas, README, docstrings de `src/` e a composição exibida por `--mostrar`; verificar que `--conferir` das fichas continua passando
- [x] 4.3 Tornar `FACETAS` de `gen_semente.py` derivada do protocolo; verificar que a lista e a ordem coincidem com a anterior
- [x] 4.4 Quando houver caso não executado, o autoteste informa claramente que o resultado é parcial e que o código de saída 0 se refere apenas aos casos executados; verificar a mensagem sem `data/sementes.json`

- [x] 4.5 Uniformizar com `AND` a notação da skill `expressoes-de-busca`
- [x] 4.6 Escrever a coluna `facetas_exigidas` de `contagens_busca.csv` na forma estrita (`FCT1 AND FCT2 AND (FCT3 OR FCT4)`); verificar a saída
- [x] 4.7 Conferir o cabeçalho da tabela "Expressões de busca" contra `[expressoes] colunas` do `config.toml`, exatamente e na ordem; cabeçalho diferente reprova a leitura; acrescentar a mutação de cabeçalho renomeado e verificar que reprova

## 5. Integração

- [x] 5.1 Rodar `python3 -I -S src/protocolo.py --conferir --autoteste`, `--mostrar` e `--pendencias`, `python3 -I -S src/derivar_expressoes.py --help` e `python3 -I -S src/gen_semente.py`; verificar que passam ou que só falham pela ausência dos arquivos de `data/`, como antes

## 6. Correções da verificação

- [x] 6.1 Autoteste permanente da prova da composição (`_autoteste_composicao` em `src/derivar_expressoes.py`, chamado por `--autoteste` dos dois scripts): composição do protocolo aprovada; executada reduzida, sonda restrita, geral sem âncora e expressão a mais fora da executada reprovam pelo motivo esperado; verificar que cada caso falha quando a relação correspondente é retirada da prova
- [x] 6.2 Ensaio diferencial das saídas: versão do HEAD e versão atual sobre a mesma entrada sintética (RIS gerado dos termos do protocolo, duas bases, executada e sonda, execução direta de EB2); verificar que os arquivos de `data/` coincidem, exceto `facetas_exigidas` de `contagens_busca.csv`
- [x] 6.3 `_expressoes_validas` na ordem declarada da composição, sem supor o prefixo do identificador; lista de bases válidas de `--registrar` lida de `[fichas]`
- [x] 6.4 `_autoteste_bases` falha nomeado quando falta em `[fichas]` uma ficha que as mutações usam

## Workflow follow-up

- Arquivar `protocolo-fonte-unica` antes desta change.
- Arquivar esta change depois da revisão do pesquisador.
