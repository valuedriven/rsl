# Proposal

## Why

Os nomes públicos dos comandos e das skills não seguem o mesmo regime dos passos: há ação
nominal (`termos sonda`, `sementes planilha`), substantivo onde o passo pede verbo
(`busca aderencia`, `busca fidelidade`), o teste de aderência está dividido entre dois
grupos e a skill `otimizar-strings-revisao-sistematica` carrega um script embutido que
duplica `strings gerar` e `conferir`. O catálogo de apoio, criado na change anterior, agora
dá o guarda para renomear sem deixar referência órfã.

## What Changes

- **BREAKING — namespace canônico dos comandos.** Os comandos passam a ser `grupo ação`,
  com ação no infinitivo:

  | Hoje | Canônico |
  | --- | --- |
  | `conferir` | `documentos conferir` |
  | `conferir-dados` | `dados conferir` |
  | `gramatica` | `documentos gramatica` |
  | `autoteste` | `projeto autoteste` |
  | `mostrar` | `configuracao mostrar` |
  | `pendencias` | `projeto pendencias` |
  | `sementes planilha` | `aderencia planilhar` |
  | `busca aderencia` | `aderencia medir` |
  | `termos sonda` | `termos sondar` |
  | `busca fidelidade` | `conferencia fidelidade` |
  | `busca sensibilidade` | `conferencia sensibilidade` |

  `busca registrar`, `busca derivar`, `termos exportar`, `termos validar`,
  `termos importar`, `strings gerar` e `catalogo gerar` permanecem; `procedimentos gerar`, se a
  change `geracao-das-fichas-de-busca` vier antes, já nasce com o nome canônico.
- **Aliases temporários.** Cada nome antigo continua funcionando como alias oculto por uma
  rodada. O catálogo acusa citação de nome antigo em documento vivo; quando a lista zerar,
  uma change posterior remove os aliases.
- **Renomeações de skills**:
  - `otimizar-strings-revisao-sistematica` → `auditoria-das-strings`;
  - `busca-nas-bases` → `execucao-da-busca`;
  - `deduplicacao` → `controle-de-duplicatas`;
  - `filtragens` → `filtragem-dos-estudos`;
  - `ficha-de-busca-por-base` → `procedimento-de-busca-por-base`, pela decisão C1 do
    pesquisador (2026-11-23): o conceito passa de “ficha” a “procedimento de busca”, como o
    caminho `docs/procedimentos_busca_<sigla>.md` já faz.
- **Script embutido removido.** O bloco `auditar_strings.py` de
  `otimizar-strings-revisao-sistematica` sai; a skill passa a chamar `strings gerar` e
  `documentos conferir`. Se a auditoria genérica ainda for útil fora do projeto, ela vira
  módulo de `src/rsl` com teste.
- **Documentação e remissões** atualizadas: specs, README, guia, skills, comentários do
  `config.toml`, pendências vivas e mensagens do autoteste.
- **Catálogo regenerado** com a tabela de correspondência antigo → novo.

Não mudam: protocolo, fichas, conjunto-semente, strings, expressões, critérios, bases,
contagens de busca e os dados de execução.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `interface-de-comando`: os subcomandos canônicos passam a ser os do namespace C; os nomes
  antigos viram aliases temporários, com política de remoção; a convenção de nomes passa a
  distinguir grupo, ação e alias.

## Impact

- Código: `src/rsl/__main__.py` (parser, aliases e ajuda); mensagens de autoteste que citam
  comandos.
- Specs: delta em `interface-de-comando`; o spec `catalogo-de-apoio` é o guarda das
  citações.
- Documentos: `README.md`, `docs/procedimentos.md`, `docs/catalogo_de_apoio.md` (regenerado)
  e `data/historico.md`.
- Skills: as cinco renomeadas; todas as que citam
  comandos ou nomes antigos.
- Configuração: a chave `[documentos] ficha` passa a `[documentos] procedimento` (C1), com a
  antiga aceita por uma rodada; os demais ajustes são comentários do `config.toml`.
- Dados: `data/pendencias.json` nas pendências vivas que citam comandos; nenhuma decisão
  histórica é reescrita.
- Dependência: o catálogo de apoio precisa estar implementado e conferindo antes desta
  change; as renomeações são provadas por ele.

## Fora de escopo

- Remover os aliases: change posterior, quando não houver citação viva de nome antigo.
- Criar `avaliacao-da-necessidade` e `busca-complementar`: decisão metodológica pendente.
- Renomear módulos internos de `src/rsl/` que já seguem o nome da atividade.
- Alterar o significado de qualquer comando; só o caminho público muda.
