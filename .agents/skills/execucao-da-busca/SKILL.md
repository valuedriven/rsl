---
name: execucao-da-busca
description: Conduz a EXECUÇÃO da busca — executar as expressões de busca nas bases Web of Science, Scopus, ERIC e BRAPCI — e o registro dos retornos, sob as regras de segurança do acesso institucional federado. Use quando o pesquisador for executar busca numa base, reportar contagens de execução, anexar exportação, ou tratar de acesso CAFe, sondagem de sintaxe e registro de execução.
---

# Executar e registrar busca nas bases

## REGRAS DE SEGURANÇA — antes de tudo

Violar qualquer uma pode suspender o acesso de **toda a instituição**, não só o do
pesquisador. Não há exceção, não há urgência que justifique.

- **Nunca** pedir, ler, armazenar, digitar, repetir ou inferir a senha CAFe/UFMG/PUC/CAPES.
  A autenticação federada é feita **pelo pesquisador, no navegador dele**. Um agente não
  autentica em nome dele, nem "só para testar".
- **Nenhuma requisição em paralelo.** Nenhum rastejamento. **Nenhuma nova tentativa
  automática** depois de erro.
- **Parada imediata e completa** diante de captcha, aviso de atividade atípica, bloqueio ou
  limite excedido. Parar, relatar ao pesquisador, **não** tentar outra rota, outro IP, outra
  base ou outro horário.
- A sessão CAFe **não** autentica chamadas de API: a da Scopus exige IP institucional ou
  `insttoken`, a da Web of Science exige licença contratada. A rota padrão é busca e
  exportação feitas pelo pesquisador na interface.
- Chave de API, havendo, só a emitida em nome do pesquisador, em `.env` no `.gitignore`,
  **nunca impressa** — em log, só os quatro últimos caracteres.

## O que executar

As expressões vivem nos quatro procedimentos de busca, uma por base, em `docs/`:
`procedimentos_busca_wos.md`, `procedimentos_busca_scopus.md`,
`procedimentos_busca_eric.md` e `procedimentos_busca_brapci.md`. **Nunca ditar uma expressão de
memória nem reescrevê-la na conversa.** Se o procedimento de busca estiver defasado, corrigi-lo e registrar
a correção no histórico (`data/historico.md`).

Só **EB4** é busca definitiva nas bases. EB1 tem a pertinência calculada localmente sobre os
registros exportados; EB2 e EB3 vão à base apenas no teste de fidelidade da derivação; e
**EB5** roda uma única vez como sonda de sensibilidade, fora do corpus.

## Antes da primeira execução numa base

**Sondagem de sintaxe obrigatória.** Nunca supor que a base aceita o que a documentação
diz. O que cada base aceita, e com que evidência, está na seção 1 do procedimento de busca
da própria base; os elementos não verificados têm, ali, o **roteiro de sondagens** — as
consultas de controle e de teste, o que observar e o que cada resultado significa. Executar
as sondagens pelo roteiro, na ordem das dependências, antes da primeira execução
(desenho e leitura: `sondagens-de-sintaxe`). Já se afirmou que a ERIC não trunca
(`ontolog*` devolve 0) e que a BRAPCI tem teto de 1.000 registros no retorno; nenhuma das
duas afirmações tem sondagem registrada (PD27, PD09, PD10), e o roteiro as sonda.

Registrar cada sondagem com o comando do projeto (sinopse em `docs/procedimentos.md`), com a
data e a hora em que foi feita, o retorno de cada consulta, a leitura observada e a
evidência. Sondagem sem evidência não é sondagem. O registro imprime a mudança a aplicar
na fonte do procedimento; aplicá-la e regenerar o procedimento.

## Ao receber as contagens

1. **Anotar como vieram**, sem arredondar e sem reordenar, com base, data, edição da
   base e o texto efectivamente submetido.

2. **Incoerência não se explica por hipótese.** Perguntar ao pesquisador o que foi
   submetido, com o texto da consulta. Hipóteses operacionais inventadas custaram uma
   rodada inteira; quatro respostas dele eliminaram todas.

3. **Nunca afirmar o que uma execução não pode ter feito.** Um argumento de teoria dos
   conjuntos vale sob a premissa, não medida, de que o motor aplica o operador como
   documentado. Já foi preciso retratar exactamente isso.

A conferência das contagens entre si — contenção, fidelidade da derivação, cobertura
de campo — é de `conferencias-da-busca`, e **não dispensa esta anotação**: ela é o
insumo daquela.

## Exportação

Exportar em RIS ou CSV, com todos os campos que a base oferecer — e conferir que a
exportação traz o que se espera **antes** de a tratar como corpus:

- **o filtro de ano confere-se no RETORNO, não na consulta.** Uma exportação da
  Scopus trouxe 8 registros de 2027 sob filtro que se supunha fechado.
- **a contagem da exportação bate com a contagem da tela?** Não batendo, há teto de
  retorno — a BRAPCI tem 1.000 — ou a exportação foi parcial.

O que vem depois não é desta skill:

| Tarefa | Skill |
| --- | --- |
| deduplicar o que veio de várias bases | `controle-de-duplicatas` |
| medir recall contra o conjunto-semente | `teste-de-aderencia` |
| coerência entre expressões, fidelidade, cobertura de campo | `conferencias-da-busca` |

## Registrar

Contagens, data, base, edição da base, texto submetido e capturas vão para
`data/registro_execucao.json`, na base correspondente. Troca de vínculo institucional vai
para as **contagens da busca**, por poder alterar o que a base entrega. Os procedimentos de busca de `docs/` são
operacionais: carregam a sintaxe verificada, as strings, as expressões, a forma de execução
e as variantes vigentes — sem registro, estado, histórico nem justificativa de decisão.

Medida nova que entre em documento é **calculada a partir dos dados**, nunca transcrita da
conversa — ver `AGENTS.md` §7. Retenção de proximidade medida em par mínimo é **limite inferior**:
11,0% na sonda contra 15,4% e 18,1% nas facetas completas.
