# Design

## Context

O guia (`docs/procedimentos.md`) é a fonte; o catálogo (`docs/catalogo_de_apoio.md`) é saída de
`catalogo gerar`, que hoje confere existência e órfãs de skill e de comando, cobertura de cada passo,
contagem e o papel de cada skill na tabela "Papel das skills" (`PAPEIS` em `src/rsl/catalogo.py`). Os
subitens de passo que o leitor reconhece são `Fonte`, `Script`, `Skill`, `Apoio` e `Ordem`. Não há
distinção entre citação principal e de apoio, e por isso a conferência não pode dizer se uma skill
extrapola o seu passo.

Restrições herdadas: corte seco de nomes, sem alias nem correspondência (change
`remocao-dos-aliases-de-transicao`); `busca fidelidade` e `busca sensibilidade` estão na lista de nomes
recusados de `src/rsl/autoteste/nomes_antigos.py`; `data/historico.md` só recebe decisão arquitetural.

## Goals / Non-Goals

**Goals:**
- Tornar a relação skill → passo e comando → passo legível no guia e conferida por construção.
- Dar a cada skill um nome que diga o passo e um escopo que não o exceda.
- Reunir a revisão interna do projeto numa skill transversal.

**Non-Goals:**
- Mudar o conteúdo metodológico das skills além do que a redistribuição de escopo exige: texto
  movido entre skills preserva a regra; não se reescrevem critérios nem procedimentos.
- Renomear comandos ou mudar a gramática `grupo ação`; reorganizar `src/rsl/` por etapa.

## Decisions

### D1. Papéis de skill: principal, subordinada, transversal

| Papel | Regra |
| --- | --- |
| principal | é **principal** em exatamente um passo; pode ser citada como apoio em outros |
| subordinada | complementa a principal de um passo; é citada (como apoio) nesse passo; nunca é principal |
| transversal | sem passo próprio; nunca é principal; pode ser citada como apoio em qualquer passo |

Cada passo tem **no máximo uma** skill principal. Passo manual ou só com apoio não precisa de
principal.

Alternativa rejeitada: manter procedimento/instrumento/artefato. Classificam a natureza da skill, não a
sua relação com o passo, e foi essa relação que ficou sem guarda.

### D2. Marca de principal por rótulo de subitem

Dois rótulos novos, ao lado dos existentes:

```
- Realizar teste de aderência das expressões de busca
  - Fonte: …
  - Script principal: `python3 -m rsl aderencia planilhar` — …
  - Script principal: `python3 -m rsl aderencia medir` — …
  - Skill principal: `testar-aderencia-das-expressoes`
  - Skill: `definir-conjunto-semente`
```

`Skill:` e `Script:` passam a significar apoio. O rótulo é contrato do leitor e erro de forma
reprova. Alternativas rejeitadas: sufixo `(principal)` após o nome (mistura marca e citação na mesma
célula e complica o parser de sinopse); "a primeira skill citada é a principal" (convenção invisível:
uma reordenação muda o papel sem que ninguém perceba).

### D3. Subordinadas declaradas com a principal que complementam

A tabela "Papel das skills" dá lugar a duas tabelas: uma com papel por skill e outra, "Skills
subordinadas", com `subordinada | principal que complementa`. O passo da subordinada é derivado: é o
passo em que a sua principal é principal. A conferência exige que a subordinada seja citada nesse
passo.

### D4. Comandos: âncora sem renomeação

Cada comando do parser é **principal em exatamente um passo** ou está declarado na tabela de
conferências transversais (e então não é principal em passo nenhum). Diferente das skills, **um passo
pode ter mais de um comando principal**: os quatro `termos …` são todos do controle terminológico e
`busca derivar`, `conferencia fidelidade` e `conferencia sensibilidade` são todos de "Avaliar a
pertinência". Âncoras propostas, a revisar na implementação:

| Comando | Passo principal | Apoio |
| --- | --- | --- |
| `busca derivar` | M3/E2 Avaliar a pertinência e a relevância dos resultados | Controlar duplicatas; 1ª filtragem (ordem de leitura); Registrar os resultados quantitativos (IO 2) |
| `documentos conferir`, `dados conferir`, `projeto autoteste` | transversais | citados como apoio em "Montar o protocolo" |
| `documentos gramatica` | M1/E3 Preparar o protocolo (IO 1) | — |
| demais | o passo que já os cita | — |

Alternativa rejeitada: juntar as três operações de "Avaliar a pertinência" num grupo. O grupo natural
seria `busca`, e `busca fidelidade` e `busca sensibilidade` são nomes recusados; um grupo novo
renomearia comandos de dois dias atrás para ganho só cosmético, já que a âncora resolve o
desalinhamento.

### D5. Renomeação, fusão e âncora das skills

O nome é o verbo do passo-âncora no infinitivo + o objeto; quando o verbo do passo é genérico
("Realizar"), usa-se o verbo da atividade ("testar"). Nomes a confirmar ao reler cada skill (ver Open
Questions).

| Atual | Nova | Papel | Passo principal / principal que complementa |
| --- | --- | --- | --- |
| `questao-e-objetivos` | `redigir-questoes-de-revisao` | principal | M2/E2 Redigir as questões de revisão (apoio em M1/E1 objetivos e M2/E2) |
| `facetacao-e-termos-livres` | `destacar-termos-da-questao` | principal | M3/E1 Destacar as palavras significativas |
| `validacao-vocabulario-controlado` | `estabelecer-controle-terminologico` | principal | M3/E1 Estabelecer o controle terminológico |
| `auditoria-das-strings` | `gerar-strings-de-busca` | principal | M3/E1 Gerar as strings de busca (adaptação) |
| `expressoes-de-busca` | `elaborar-expressoes-de-busca` | principal | M3/E1 Elaborar as expressões de busca |
| `criterios-de-elegibilidade` | `definir-criterios-de-elegibilidade` | principal | M3/E1 Definir os critérios |
| `procedimento-de-busca-por-base` | `gerar-procedimento-de-busca` | principal | M3/E1 Gerar o procedimento de busca (adaptação) |
| `flexao-por-base` | `declarar-flexao-por-base` | subordinada | de `gerar-procedimento-de-busca` |
| `parecer-sobre-protocolo` | `validar-protocolo` | principal | M3/E1 Validar o protocolo com pesquisador expert |
| `execucao-da-busca` | `executar-expressoes-de-busca` | principal | M3/E2 Executar expressões de busca |
| `sondagens-de-sintaxe` | `executar-sondagens-de-sintaxe` | principal | M3/E2 Executar as sondagens (adaptação) |
| `teste-de-aderencia` | `testar-aderencia-das-expressoes` | principal | M3/E2 Realizar teste de aderência |
| `conjunto-semente` | `definir-conjunto-semente` | principal | M3/E1 Definir conjunto semente (adaptação) (apoio em Realizar teste de aderência e em Incluir estudos de acervos) |
| `conferencias-da-busca` | `avaliar-resultados-da-busca` | principal | M3/E2 Avaliar a pertinência e a relevância |
| `controle-de-duplicatas` | `controlar-duplicatas` | principal | M3/E3 Controlar duplicatas |
| `filtragem-dos-estudos` | `filtrar-estudos` | principal | M3/E3 Analisar os títulos (1ª filtragem) (apoio na 2ª e 3ª filtragem, em Aplicar os critérios e em Confirmar a seleção) |
| `fichamento` | `coletar-dados-dos-estudos` | principal | M3/E4 Coletar dados (apoio em IO 4 e IO 5) |
| `sintese-e-lacunas` | `analisar-conteudo-dos-estudos` | principal | M4/E1 Realizar a análise de conteúdo |
| `relato-prisma` | `redigir-relatorio` | principal | M4/E2 Redigir o texto final |
| `revisao-geral-do-projeto` + `rastreabilidade` | `revisar-projeto` | transversal | — |
| `conferir-referencia` | mantém | transversal | — |
| `registrar-decisao` | mantém | transversal | — |

Resultado: 22 skills — 18 principais, 1 subordinada, 3 transversais.

### D6. Redistribuição de escopo

Regra: o texto vai para a skill do passo em que a atividade acontece; a skill que o perde fica com
uma remissão de uma linha. Movimentos previstos:

- `procedimento-de-busca-por-base` → sintaxe e roteiro de sondagens para `executar-sondagens-de-sintaxe`;
  plural e exceções para `declarar-flexao-por-base`; aplicação de critério por base para
  `definir-criterios-de-elegibilidade`; montagem de expressão para `elaborar-expressoes-de-busca`;
  sementes para `definir-conjunto-semente`. Fica: escrever a fonte, gerar e conferir o procedimento.
- `execucao-da-busca` → registro e leitura de sondagem para `executar-sondagens-de-sintaxe`.
- `auditoria-das-strings` → o procedimento de auditoria geral (arquitetura, confronto termo a termo
  com as sementes, emendas, pendências de verificação, entregáveis) para `revisar-projeto`; os 11
  critérios, o princípio e o julgamento da saída de `strings gerar` ficam em `gerar-strings-de-busca`;
  as seções "Sintaxe por base" e "Regras duras" distribuem-se pelos passos em que cada regra se aplica
  (inventário, C11 e C12).
- `revisao-geral-do-projeto` + `rastreabilidade` → `revisar-projeto`, com o método das
  correspondências como uma das seções da revisão.

Movimento que mude uma regra, e não só o lugar dela, é decisão do pesquisador e fica fora desta
change.

### D7. Módulos

`src/rsl/conferencia.py` contém `conferir()` de `documentos conferir`, e o nome colide com o grupo
`conferencia` (fidelidade e sensibilidade, em `busca/`). `src/rsl/fichas.py` guarda as formas de
execução e é resíduo do nome anterior ao C1. Ambos são renomeados — `conferencia.py` → `coerencia.py`,
`fichas.py` → `derivado.py`, `autoteste/fichas.py` → `autoteste/derivado.py` — e os importadores
(`dados.py`, `cobertura.py`, `relatorio.py` e quatro módulos de `autoteste/`) atualizados. O autoteste
`autoteste/fichas.py` acompanha.

### D8. Citações de nome antigo fora do guia

- Remissões entre skills, `README.md` e ações sugeridas de `data/pendencias.json`: atualizadas.
- Notas datadas nas fontes `docs/procedimentos/*/procedimento.toml` ("afirmado sem fonte na skill
  `auditoria-das-strings` até 2026-11-23"): **mantidas**. Descrevem um estado passado com data;
  reescrevê-las atribuiria a afirmação a uma skill que não existia.
- Nota de estado corrente na fonte da ERIC ("a skill `execucao-da-busca` afirma…"): atualizada para o
  nome novo, porque descreve o presente.
- Cenários da spec `catalogo-de-apoio` que citam skills: atualizados no delta.

## Risks / Trade-offs

- [Nome antigo esquecido fora do guia, sem varredura que o denuncie] → busca textual por cada nome
  antigo como tarefa de verificação, registrada no relato da change; a varredura automática foi
  retirada por decisão do pesquisador e não volta.
- [Redistribuição perde ou duplica regra] → antes de mover, inventariar as regras da skill de origem;
  depois, conferir que cada uma está em exatamente um lugar.
- [Regra de âncora reprova o guia corrente inteiro na primeira execução] → migrar guia e regras na
  mesma tarefa; o autoteste injeta cada defeito sobre o guia já migrado.
- [Fusão de `revisao-geral-do-projeto` e `rastreabilidade` gera skill longa] → o método de
  correspondências vira seção; o que for só exemplo histórico é candidato a corte, a decidir com o
  pesquisador.

## Migration Plan

1. Regras novas no catálogo e autoteste, com o guia ainda nos nomes atuais (marca de principal já
   aplicada).
2. Renomeação e fusão das skills, guia e catálogo regenerado no mesmo passo.
3. Redistribuição de escopo, skill a skill.
4. Módulos e importadores.
5. Citações fora do guia; `catalogo gerar`, `documentos conferir` e `projeto autoteste`.

Reversão: a change não toca dados nem protocolo; reverte-se pelo controle de versão.

## Open Questions

Resolvidas pelo pesquisador em 2026-11-25 (tarefa 1.1):

- Nomes finais: a tabela D5 confirmada como está.
- `filtrar-estudos`: principal na 1ª filtragem (onde vivem o critério próprio da skill e a assistência
  de IA); apoio na 2ª e 3ª filtragem, em "Aplicar os critérios" e em "Confirmar a seleção". O nome
  `filtrar-estudos` é mantido.
- Módulos: `coerencia.py` e `derivado.py` (D7).

Resolvidas pelo pesquisador em 2026-11-25 (tarefa 1.2; inventário em `inventario.md`):

- O julgamento da saída de `strings gerar` fica em `gerar-strings-de-busca`, skill do passo em que o
  comando é principal (D6 ajustado).
- "Sintaxe por base" e "Regras duras" de `auditoria-das-strings` distribuem-se pelos passos. A
  prescrição "backward e forward search" não se move: diverge do protocolo (P11) e vira pendência.
- A afirmação "não há guarda automática" de `rastreabilidade` está desatualizada e se corrige na
  fusão; "Garantida por" passa a nomear o comando que hoje garante cada correspondência.
- Os exemplos históricos de `rastreabilidade` entram em `revisar-projeto` encurtados.

Decididas pelo pesquisador em 2026-11-25, na verificação:

- Passo de adaptação novo em M3/E1, "Definir conjunto semente", logo após "Avaliar e definir as
  fontes de pesquisa". A skill do conjunto-semente passa a principal desse passo e, pela regra de
  nome de D5, chama-se `definir-conjunto-semente` (antes `compor-conjunto-semente`, subordinada de
  `testar-aderencia-das-expressoes`). O guia passa a 63 + 4 = 67 passos.
- "Gerar o procedimento de busca de cada base" move-se para logo antes de "Validar o protocolo com
  pesquisador expert", com a parte da `Ordem` que lhe cabe (fonte → `procedimentos gerar` →
  `--gravar` → `documentos conferir`); o passo das strings fica com quadro → `strings gerar` →
  `--gravar`.
