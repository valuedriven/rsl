# Prova por cobertura — revisão de 2026-11-19

Data: 2026-11-19. Fonte dos achados: `revisao-2026-11-19.md`, nesta change. Skill
conferida: `.agents/skills/revisao-geral-do-projeto/SKILL.md`.

**Procedimento.** Cada achado e cada retificação da revisão foi ligado ao passo ou à regra
da skill que o produziria. Depois, o roteiro foi percorrido sobre o estado corrente, só em
leitura, para verificar se algum achado ainda aberto nas quatro changes fica sem passo.

## 1. Achados e retificações da revisão

| Achado ou retificação | Onde está na revisão | Passo ou regra da skill |
| --- | --- | --- |
| Conferências executadas e casos que não rodaram por falta de arquivo alimentado | §1, tabela | Passo 2 |
| Change concluída sem commit e sem arquivamento | §1, texto após a tabela | Passo 1 |
| Fichas citam evidência inexistente | §2.1 | Passo 3, com a reprovação provada no passo 2 |
| Pendências desatualizadas (PD01, PD13, PD14) | §2.2 | Passos 1 e 3 |
| Emenda v2 sem números registrados | §2.3 | Passo 3 |
| Termos repetidos em mais de uma faceta | §3a | Passo 4 |
| `practice`, `prática` e `práctica` isolados em STR3 | §3b | Passo 4 |
| "Modelo conceitual" fora de STR1 | §3c | Passo 4 |
| Sonda que não mede a perda por proximidade e definição operacional que muda entre bases | §3d | Passo 4 |
| Hipótese sobre a recuperação da SE4 | §3e | Passo 5 e regra 3 (fica como inferência até conferir na fonte) |
| Circularidade entre ajuste e sementes | §4, primeiro item | Passo 5 |
| Tamanho do conjunto e intervalo de confiança do limiar | §4, segundo item | Passo 5 |
| Coluna "Bases" possivelmente incompleta | §4, terceiro item | Passo 5 |
| Metadados das 10 sementes pendentes | §4, quarto item e parágrafo final | Passos 5 e 3 |
| Regra operacional de inclusão fora do protocolo | §5, primeiro item | Passo 6 |
| CE4 ambíguo sobre revisões sistemáticas | §5, segundo item | Passo 6 |
| CE5 e a numeração das filtragens | §5, terceiro item | Passo 6 |
| O que não se fez | "O que não fiz" | Produto |
| Frentes sugeridas | "Por onde seguir" | Produto |
| **Retificação:** `gen_semente.py` gera linha por semente e por base da tabela, não só pela base declarada | §4, terceiro item, retificado em `conjunto-semente-independente/proposal.md` (D3) | Regra 1, com o passo 5 |
| **Retificação:** a varredura das citações abrange as quatro fichas, não só WoS e Scopus | §2.1, ampliado em `higiene-de-rastreabilidade/proposal.md` | Regra 2, com o passo 3 |
| **Atualização de estado:** `expressoes-literais-por-base` tinha 14 tarefas na revisão; está arquivada com 15/15 | §1 | Passo 1 |

Nenhuma linha ficou sem passo ou regra correspondente.

## 2. Percurso sobre o estado corrente

Leitura feita em 2026-11-19, sem alterar a árvore além do que esta change já altera.

| Frente aberta | Achado ainda aberto | Passo que o cobre |
| --- | --- | --- |
| `higiene-de-rastreabilidade` | Citações sem lastro nas quatro fichas | Passo 3 |
| `higiene-de-rastreabilidade` | PD01, PD02 e PD17 abertas | Passos 1 e 3 |
| `higiene-de-rastreabilidade` | Fundamento quantitativo da v2 não registrado | Passo 3 |
| `higiene-de-rastreabilidade` | Garantia contra a citação sem lastro | Produto ("garantia proposta") |
| `higiene-de-rastreabilidade` | Revisão geral sem procedimento | Passos 1 a 6 e regras 1 a 3 |
| `revisao-das-strings-por-faceta` | D1 — termos repetidos entre facetas | Passo 4 |
| `revisao-das-strings-por-faceta` | D2 — termos genéricos em STR3 | Passo 4 |
| `revisao-das-strings-por-faceta` | D3 — "modelo conceitual" fora de STR1 | Passo 4 |
| `revisao-das-strings-por-faceta` | D4 — sonda não mede proximidade; definição entre bases | Passo 4 |
| `revisao-das-strings-por-faceta` | SE4 — hipótese sobre ordem dos termos | Passo 5 e regra 3 |
| `conjunto-semente-independente` | D1 — circularidade entre ajuste e aferição | Passo 5 |
| `conjunto-semente-independente` | D2 — tamanho e intervalo de confiança | Passo 5 |
| `conjunto-semente-independente` | D3 — incidência por base | Passo 5 |
| `conjunto-semente-independente` | D4 — metadado das sementes | Passos 5 e 3 |
| `criterios-de-elegibilidade-no-protocolo` | D1 — regra de inclusão e regra de borda fora do protocolo | Passo 6 |
| `criterios-de-elegibilidade-no-protocolo` | D2 — CE4 e revisões sistemáticas | Passo 6 |
| `criterios-de-elegibilidade-no-protocolo` | D3 — CE5 e numeração das filtragens | Passo 6 |
| `criterios-de-elegibilidade-no-protocolo` | D4 — justificativas ausentes | Passo 6 |

Estado observado no momento do percurso:

- quatro changes abertas: `higiene-de-rastreabilidade` (3/19 tarefas naquele momento), `revisao-das-strings-por-faceta`
  (0/17), `conjunto-semente-independente` (0/13) e `criterios-de-elegibilidade-no-protocolo` (0/14);
- as conferências rodam, e 10 casos dos arquivos alimentados não rodam por ausência de
  `data/registro_execucao.json` — o passo 2 os relata como não executados, não como aprovados;
- PD01, PD02 e PD17 abertas; PD13 e PD14 resolvidas nesta change;
- nenhum achado aberto nas quatro changes ficou sem passo.

## 3. Resultado

A tabela de 2026-11-19 não tem linha sem correspondência, e o percurso não deixou achado
aberto sem passo. A skill cobre a revisão que a originou.
