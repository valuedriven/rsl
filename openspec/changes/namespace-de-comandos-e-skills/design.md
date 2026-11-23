# Design

## Context

O catálogo de apoio (`catalogo-de-apoio`) passa a ler `docs/procedimentos.md`, o parser, as
skills e os documentos vivos. Ele é o guarda desta change: uma renomeação só termina quando
o catálogo não encontra mais o nome antigo em documento vivo.

O estado corrente tem 17 caminhos de comando e 21 skills. Os nomes misturam verbo e
substantivo (`termos sonda`, `sementes planilha`, `busca aderencia`), o teste de aderência
está dividido entre `sementes` e `busca`, e a skill
`otimizar-strings-revisao-sistematica` embute um script que duplica `strings gerar` e
`conferir`. A renomeação das fichas para `docs/procedimentos_busca_<sigla>.md` já está feita.

Ver `proposal.md` — Why.

## Goals / Non-Goals

**Goals:**

- Um regime único de nomes: `grupo ação`, ação no infinitivo, grupo nomeando artefato ou
  domínio.
- Preservar compatibilidade por uma rodada, com aliases ocultos e aviso.
- Alinhar as skills aos passos, sem renomear o que já corresponde.
- Remover o script embutido da skill de strings.
- Fazer o catálogo provar que nenhuma referência viva ficou órfã.

**Non-Goals:**

- Remover os aliases nesta change; isso é a change seguinte.
- Renomear módulos internos de `src/rsl/` que já seguem o nome da atividade.
- Alterar o comportamento de qualquer comando; só o caminho público muda.
- Decidir a criação de novas skills; a lacuna permanece declarada.
- Reescrever histórico, changes arquivadas ou specs históricas.

## Decisions

### D1 — Semântica do namespace

O caminho é `grupo ação`:

- **grupo** = artefato ou domínio: `documentos`, `dados`, `projeto`, `configuracao`,
  `termos`, `strings`, `catalogo`, `aderencia`, `busca`, `conferencia`;
- **ação** = verbo no infinitivo, em português e sem acento.

Topo sem grupo natural continua verbo (`conferir` não existe mais; `documentos conferir`
assume). O topo `catalogo` é grupo porque o artefato tem duas operações possíveis no futuro
(`gerar`, `conferir`); hoje só `gerar` é implementado.

Alternativa descartada: manter os comandos planos e só documentar a correspondência. Não
resolve a ação nominal nem a divisão do teste de aderência.

### D2 — Tabela canônica

| Hoje | Canônico | Alias |
| --- | --- | --- |
| `conferir` | `documentos conferir` | `conferir` |
| `conferir-dados` | `dados conferir` | `conferir-dados` |
| `gramatica` | `documentos gramatica` | `gramatica` |
| `autoteste` | `projeto autoteste` | `autoteste` |
| `mostrar` | `configuracao mostrar` | `mostrar` |
| `pendencias` | `projeto pendencias` | `pendencias` |
| `sementes planilha` | `aderencia planilhar` | `sementes planilha` |
| `busca aderencia` | `aderencia medir` | `busca aderencia` |
| `termos sonda` | `termos sondar` | `termos sonda` |
| `busca fidelidade` | `conferencia fidelidade` | `busca fidelidade` |
| `busca sensibilidade` | `conferencia sensibilidade` | `busca sensibilidade` |
| `busca registrar` | `busca registrar` | — |
| `busca derivar` | `busca derivar` | — |
| `termos exportar` | `termos exportar` | — |
| `termos validar` | `termos validar` | — |
| `termos importar` | `termos importar` | — |
| `strings gerar` | `strings gerar` | — |
| `catalogo gerar` | `catalogo gerar` | — |
| — | `procedimentos gerar` | — |

A linha de `procedimentos gerar` vale só se a change `geracao-das-fichas-de-busca` for
aplicada antes desta. Pela decisão C1 (D6), aquela change cria o comando já com o nome
canônico, sem alias.

`busca derivar` permanece: “derivação” é o termo técnico do projeto, e o comando produz
expressões não executadas, contagens e ordem de triagem. O catálogo declara o papel dele no
passo “Avaliar a pertinência e a relevância”.

### D3 — Aliases

Cada alias é um parser oculto que:

- executa a mesma função do canônico;
- imprime uma linha de aviso com o nome canônico;
- não aparece na ajuda (`help=argparse.SUPPRESS`);
- não aparece na tabela de comandos do catálogo, só na tabela de correspondência.

O catálogo lê a lista de aliases do parser e varre documentos e skills vivas. Uma citação
de alias em documento vivo reprova; a tabela de correspondência, o histórico e as changes
arquivadas são isentos.

A remoção dos aliases é uma change posterior, quando a lista de citações vivas zerar. O
critério não é prazo, é a lista zerada.

Alternativa descartada: trocar os nomes sem alias. Quebraria comandos salvos e citações
enquanto a migração não terminasse.

### D4 — Aderência em um só grupo

`aderencia planilhar` gera a planilha e o ensaio seco; `aderencia medir` mede o recall por
papel. Os dois comandos deixam de ficar em grupos diferentes e passam a ser lidos na mesma
ordem do passo “Realizar teste de aderência”.

### D5 — Conferências em grupo próprio

`conferencia fidelidade` e `conferencia sensibilidade` deixam o grupo `busca`. A mudança
alinha o comando à skill `conferencias-da-busca` e ao vocabulário do guia, que já trata os
dois como conferências pós-execução. `busca registrar` e `busca derivar` continuam em
`busca`.

### D6 — Skills

| Hoje | Canônico | Tipo |
| --- | --- | --- |
| `otimizar-strings-revisao-sistematica` | `auditoria-das-strings` | procedimento |
| `busca-nas-bases` | `execucao-da-busca` | procedimento |
| `deduplicacao` | `controle-de-duplicatas` | procedimento |
| `filtragens` | `filtragem-dos-estudos` | procedimento |
| `ficha-de-busca-por-base` | `procedimento-de-busca-por-base` | artefato |

As demais ficam: `questao-e-objetivos`, `facetacao-e-termos-livres`,
`validacao-vocabulario-controlado`, `expressoes-de-busca`, `criterios-de-elegibilidade`,
`conferencias-da-busca`, `teste-de-aderencia`, `fichamento`, `sintese-e-lacunas`,
`relato-prisma`, `conjunto-semente`, `conferir-referencia`, `parecer-sobre-protocolo`,
`registrar-decisao`, `rastreabilidade`, `revisao-geral-do-projeto`.

A regra: skill de procedimento nomeia a atividade; skill de artefato nomeia o artefato;
skill transversal nomeia a operação. Não se codifica módulo/etapa/passo no nome; a posição
vive no catálogo.

Decisão C1/C2 para a ficha, **decidida C1** pelo pesquisador em 2026-11-23:

- **C1**: assumir “procedimento de busca” também no conceito; renomear a skill, o texto do
  guia/README e a chave `[documentos] ficha` para `[documentos] procedimento`, com aceitação
  temporária da chave antiga no leitor.
- **C2**: manter “ficha” como conceito e `ficha-de-busca-por-base` como nome; o caminho
  `docs/procedimentos_busca_<sigla>.md` é só convenção de arquivo.

Vale C1. As tarefas do ramo C2 ficam fora da change. O nome antigo da skill e a chave
`[documentos] ficha` entram na tabela de correspondência do catálogo, e a chave antiga é
aceita pelo leitor por uma rodada.

### D7 — Script embutido

O bloco `auditar_strings.py` de `otimizar-strings-revisao-sistematica` sai. A skill passa a
chamar:

- `python3 -m rsl strings gerar` para a diferença entre quadro e STR;
- `python3 -m rsl documentos conferir` para a conferência.

Se a auditoria genérica ainda for útil fora deste projeto, ela vira módulo de `src/rsl` com
teste; não fica copiada dentro de uma skill. A skill não ensina a operar a ferramenta; ela
diz como julgar o resultado.

### D8 — Varredura de referências vivas

Arquivos vivos:

- `README.md`;
- `docs/*.md` (exceto `docs/conjunto_semente.toml` e os documentos de dados);
- `.agents/skills/**/SKILL.md`;
- `openspec/specs/**/*.md` (specs principais);
- `config.toml` (comentários);
- `data/pendencias.json` (somente pendências vivas);
- `src/rsl/autoteste/**/*.py` (mensagens).

Isentos:

- `data/historico.md`;
- `openspec/changes/archive/`;
- a tabela de correspondência do catálogo;
- a própria change de renomeação, quando cita o nome antigo para descrevê-lo.

A varredura é a mesma do catálogo; não se cria uma segunda lista.

### D9 — Autoteste

Casos novos:

- cada alias executa a operação canônica e emite aviso;
- a ajuda não lista alias;
- o catálogo reprova uma skill viva que cita alias;
- o catálogo não reprova a tabela de correspondência;
- remover um alias (em cópia) faz o nome antigo sair com USO.

### D10 — Migração

1. Implementar os canônicos e os aliases.
2. Renomear as skills e atualizar as remissões vivas.
3. Remover o script embutido.
4. Renomear a chave e o texto do artefato (C1).
5. Regenerar o catálogo; a conferência deve acusar zero nomes antigos em documento vivo.
6. Rodar `documentos conferir`, `dados conferir`, `projeto autoteste`, `catalogo gerar`.
7. Registrar a emenda no histórico.

Rollback: manter os canônicos e restaurar os nomes antigos como canônicos, deixando os novos
como aliases; nenhum dado é perdido.

## Risks / Trade-offs

- [Aliases viram dívida permanente] → o critério de remoção é a lista de citações vivas
  zerada; a change de remoção é explícita.
- [Ajuda fica poluída] → aliases são ocultos; a tabela de correspondência fica no catálogo.
- [C1 mexe em config e código] → o leitor aceita a chave antiga por uma rodada, e o
  catálogo acusa o nome antigo em documento vivo até a lista zerar.
- [Renomear skill quebra remissões em skills e documentos] → o catálogo varre skills e
  documentos vivos; a change só encerra com zero citações.
- [Pendências vivas citam comandos antigos] → atualizar só as pendências abertas; o
  histórico não se reescreve.
- [Autoteste parcial] → o código 6 continua sendo PARCIAL por falta de registro; os casos
  novos não dependem dele.
- [Comando `documentos conferir` parece só protocolo] → a ajuda diz “protocolo,
  procedimentos de busca e sementes”; o catálogo registra o escopo.

## Open Questions

- ~~`documentos` ou `protocolo` como grupo de `conferir` e `gramatica`~~: **decidido
  `documentos`** pelo pesquisador em 2026-11-23, porque `gramatica` também cobre sementes e
  procedimentos de busca.
- Criar as skills `avaliacao-da-necessidade` e `busca-complementar`: fora desta change; a
  lacuna fica declarada.
