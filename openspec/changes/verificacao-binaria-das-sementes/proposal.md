# Proposta

## Por quê

O campo `verificacao` do arquivo de sementes era texto livre, e o estado de conferência se
lia pelo começo do texto: `aderencia planilhar` contava como confirmada só a semente cujo
texto começa por "CONFIRMADA", e a pendência se reconhecia por "A CONFERIR" ou
"PENDÊNCIA". Três sementes conferidas (SE4, SE11 e SE12) foram registradas com outra
redação ("DADOS BIBLIOGRÁFICOS CONFIRMADOS — …") e passaram a contar como não confirmadas,
sem que nenhuma leitura reprovasse. O estado dependia da redação.

## O que muda

- `verificacao` passa a booleano: `true` quando os dados bibliográficos foram conferidos;
  `false` ou ausente é conferência pendente, relatada por `projeto pendencias`. Texto ou
  outro tipo reprova a leitura com PROTOCOLO_ILEGIVEL.
- Onde e como se conferiu vai para `nota`, que já reunia o registro de conferência.
- A planilha de aderência mostra `sim` ou `não` na coluna `verificacao`.
- Migração: as 12 sementes passam a `verificacao = true`, e o texto anterior vai para o
  início da `nota`, sem o prefixo de estado.
- `veiculo_conferido` não muda.

## Capacidades

### Novas
- nenhuma

### Modificadas
- `leitura-do-protocolo`: o requisito do conjunto-semente declara o tipo de `verificacao`.

## Impacto

`gramatica.py` (tipo booleano em `CampoToml`), `leitura.py`, `dados.py`, `sementes.py`,
autoteste das sementes, skills `definir-conjunto-semente` e `conferir-referencia`,
`docs/conjunto_semente.toml`.
