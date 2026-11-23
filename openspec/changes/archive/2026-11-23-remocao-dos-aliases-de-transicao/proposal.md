# Proposal

## Why

A change `namespace-de-comandos-e-skills` (dependência desta) renomeou comandos, skills e a
chave `[documentos] ficha`. Os nomes antigos de comando ficaram como aliases ocultos e a
chave antiga ficou aceita, com aviso, por uma rodada. Assim, comandos salvos e citações
continuaram funcionando durante a migração. Alias mantido indefinidamente vira dívida: são
dois nomes para a mesma operação. Esta change os retira, e só quando nenhum documento vivo
citar mais os nomes antigos.

## Critério de entrada

**Zero citações vivas.** `python3 -m rsl catalogo gerar` sai 0, sem nenhum problema da regra
`nome_antigo`, sobre os arquivos vivos que o catálogo varre: README, `docs/*.md`, skills, specs
principais e o código de `src/rsl/` fora de `CODIGO_ISENTO`. Também `config.toml` e
`data/pendencias.json`, conferidos por `grep`, não citam nome antigo. O critério é a lista
zerada, não um prazo. Se ela não estiver zerada, a change não se aplica.

## What Changes

- **BREAKING — aliases de comando removidos.** Saem de `ALIASES` em `src/rsl/__main__.py`
  e passam a terminar com o código USO:
  - `conferir` (canônico `documentos conferir`);
  - `conferir-dados` (`dados conferir`);
  - `gramatica` (`documentos gramatica`);
  - `autoteste` (`projeto autoteste`);
  - `mostrar` (`configuracao mostrar`);
  - `pendencias` (`projeto pendencias`);
  - `sementes planilha` (`aderencia planilhar`);
  - `busca aderencia` (`aderencia medir`);
  - `termos sonda` (`termos sondar`);
  - `busca fidelidade` (`conferencia fidelidade`);
  - `busca sensibilidade` (`conferencia sensibilidade`).
- **BREAKING — chave antiga recusada.** `[documentos] ficha` sai de `RENOMEADAS` em
  `src/rsl/config.py`. Presente, reprova como chave desconhecida, ou como chave retirada,
  com mensagem que nomeie `[documentos] procedimento`.
- **Correspondência de nomes.** Decidir se a tabela de correspondência do catálogo e a
  varredura de nome antigo continuam depois da remoção, para pegar regressão, ou se saem
  com os aliases. O registro dos nomes antigos de skill (`SKILLS_RENOMEADAS`) segue a mesma
  decisão.
- **Autoteste.** O grupo "aliases de transição" passa a provar que cada nome antigo sai com
  USO e que a chave antiga reprova; os casos de execução e aviso saem.
- **Specs.** O requisito "Aliases de transição" de `interface-de-comando` passa a declarar
  a remoção (cenário "Remoção posterior").

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `interface-de-comando`: os nomes antigos deixam de ser aceitos; o requisito "Aliases de
  transição" é substituído pela recusa com USO.
- `catalogo-de-apoio`: o destino da varredura de nome antigo e da tabela de
  correspondência depois da remoção.

## Impact

- Código: `src/rsl/__main__.py` (`ALIASES`), `src/rsl/config.py` (`RENOMEADAS`),
  `src/rsl/catalogo.py` e `src/rsl/autoteste/aliases.py`.
- Documentos: `docs/catalogo_de_apoio.md` (regenerado) e `data/historico.md`.
- Dependência: `namespace-de-comandos-e-skills` aplicada e arquivada, com o critério de
  entrada satisfeito.

## Fora de escopo

- Renomear qualquer outro comando, skill ou chave.
- Renomear os módulos internos de `src/rsl/`.
  Resíduo conhecido da decisão C1: o leitor dos procedimentos de busca continua em
  `src/rsl/fichas.py`, citado pelos `docs/procedimentos_busca_<sigla>.md`. Não é alias nem
  nome público; renomeá-lo é decisão à parte, e não condição desta change.
