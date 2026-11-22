# Design — guia de procedimentos

## Context

Motivação em `proposal.md`. Estado que condiciona a abordagem:

- A estrutura de 4 módulos, 14 etapas e 63 passos foi **fornecida pelo pesquisador** na
  conversa de 2026-11-21, atribuída a Borges (2020). O agente não a conferiu na tese.
- O plano (§1.4, §3.1) situa controle terminológico, strings, expressões, critérios e
  fichas em **M3/E1**, e execução, aderência e demais testes em **M3/E2**. Decisão do
  pesquisador: seguir a numeração do plano.
- O plano (§6, §7) e o protocolo (§Acervos pessoais) remetem a passos por ordinal
  ("Módulo 3, Etapa 2, 1º passo").
- A spec `interface-de-comando` exige a tabela de códigos de saída no README.
- Skills remetem ao README para comandos, mapa, nomes de arquivo, precedência e limiares;
  `teste-de-aderencia` cita a "seção Scripts".
- Os parâmetros reais da CLI são os de `python3 -m rsl <subcomando> -h`; os posicionais
  (`BASE`, `EXPRESSAO`, `ARQUIVO`, `SIGLA`) não têm texto de ajuda.

## Goals / Non-Goals

**Goals:**
- Um lugar para "o que se faz e quando" (`docs/procedimentos.md`) e outro para "como se
  executa e onde fica" (`README.md`), sem informação nos dois.
- Cada passo leva à fonte da decisão e à ferramenta que o apoia, sem copiar o conteúdo.

**Non-Goals:**
- Resolver as divergências entre o modelo e o projeto: viram pendência.
- Reproduzir datas, responsáveis ou progresso: ficam no cronograma (IO 7), fora do pacote.
- Explicar regras de conferência, gramática ou configuração: ficam nas specs, em
  `rsl gramatica`, `rsl mostrar` e no `config.toml`.

## Decisions

**D1 — Divisão entre os dois arquivos.**
`docs/procedimentos.md`: módulos, etapas, passos, remissões a fonte, script e skill; os
comandos com a sinopse completa de parâmetros aparecem **no passo em que são usados**, e
as conferências transversais (`conferir`, `conferir-dados`, `autoteste`, `mostrar`,
`gramatica`, `pendencias`) numa seção própria ao fim. `README.md`: identificação, como
executar (`PYTHONPATH`, Python 3.11+, `RSL_CONFIG`), mapa único dos caminhos com quem
escreve cada um, tabela de códigos de saída, três registros, precedência, convenções e
remissão ao guia.
*Alternativa descartada:* referência de comandos no README e só o nome do comando no guia —
obriga a ler dois arquivos para executar um passo, que é o uso dominante.

**D2 — Forma do passo.**
Item de lista, sem numeração e sem a palavra "passo": verbo no infinitivo + objeto, na
**forma genérica**, que vale para o modelo e para a prática do projeto ("Executar
expressões de busca", não "Executar a totalidade das expressões de busca"). O que é
específico do projeto não vai ao texto do passo: está na fonte de remissão. Sob o passo,
quando aplicável, sub-itens curtos:

```
- Executar expressões de busca
  - Fonte: protocolo §Expressões de busca; ficha da base §…
  - Script: `python3 -m rsl busca registrar BASE EXPRESSAO ARQUIVO [--retorno N] [--data-hora ISO] [--justificar TEXTO]`
  - Skill: `busca-nas-bases`
```

Passo sem script nem skill fica só com a linha e, havendo, a fonte. Os 63 passos
permanecem, na ordem da estrutura fornecida.
*Alternativas descartadas:* texto do modelo com sub-linha de adaptação; texto do projeto
(decisão do pesquisador).

**D3 — Índices de M3/E2.**
Tabela única no guia, sob a etapa: índice · o que mede · numerador / denominador · limiar
e origem (protocolo ou `config.toml`, visível em `rsl mostrar`) · script ou "manual" ·
saída. Índices levantados no código: retorno declarado × lido, contagens brutas e únicas
por expressão, duplicatas na base, linha "fora" do recorte, ordem de triagem, recall por
papel com intervalo de Wilson (validação), divergência simétrica da fidelidade, fração
EB5 ∖ EB4; manuais: fração elegível da amostra de sensibilidade (a calibração da triagem saiu com o
ASReview, por decisão do pesquisador de 2026-11-22). Kappa e contagens PRISMA ficam em M3/E3. O valor do limiar não se
transcreve: remete-se à origem.

**D4 — Remissões por ordinal.**
O guia não numera passos, mas preserva a ordem; o ordinal citado no plano continua
contável. Substituir o ordinal pelo texto do passo no plano e no protocolo é alteração em
documento-fonte do pesquisador: registra-se como pendência, não se faz nesta change.

**D5 — Divergências modelo × projeto.**
A forma genérica dissolve parte delas; as que persistem viram pendência em
`data/pendencias.json`, com origem no guia e no documento que decide: aderência por
conjunto-semente posterior à execução × "teste de aderência" como primeiro passo de E2;
deduplicação antes da triagem (P2) × controle de duplicatas após as filtragens; inclusão de
acervos pessoais × protocolo §Acervos pessoais; fator de impacto entre os critérios;
série IO 1–7 do modelo × I1–I8 do protocolo; avaliação de risco de viés não verificada no
protocolo; backward de uma geração (plano §3.3) × backward e forward (P11); origem da
estrutura de 63 passos não conferida na tese.

## Risks / Trade-offs

- [Skills apontam para seção que deixa de existir] → atualizar as remissões na mesma change
  e procurar por "README" nas skills antes de encerrar.
- [Sinopse de parâmetros no guia diverge da CLI] → a sinopse é transcrita de `-h` na
  implementação, e o guia remete a `-h` como fonte; a divergência é risco aceito até haver
  geração (fora de escopo).
- [Forma genérica esconde a adaptação] → a remissão de fonte em cada passo afetado é
  obrigatória, e as divergências que persistem estão nas pendências.
- [README curto perde informação útil] → antes de remover um bloco, confirmar onde ele já
  está; o que não estiver em outro artefato fica no README ou vai ao guia.
