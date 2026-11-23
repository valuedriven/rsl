# Tasks

## 0. Pré-condição

- [ ] 0.1 Confirmar que `strings-geradas-do-quadro` está arquivada e que as specs principais
  `cobertura-por-base` e `interface-de-comando` trazem `Plural declarado por base`, `Termo só
  no singular relatado` e `strings gerar`. Verificar com `openspec show cobertura-por-base
  --type spec` e `openspec validate geracao-das-fichas-de-busca --strict`.

## 1. Flexão dos termos (D5, D6)

- [ ] 1.1 Implementar a flexão por regra de pt, en e es: o núcleo flexionado, as regras
  regulares e as terminações indecidíveis de D5. Verificar pelos cenários de "Plural por
  regra regular" e "Flexão indecidível reprova" da spec `flexao-dos-termos`.
- [ ] 1.2 Ler o arquivo de exceções (`[documentos] flexoes`, `docs/flexoes.toml`), com
  `irregular`, `nao_contavel` e `vetada`, `origem` obrigatória e PROTOCOLO_ILEGIVEL para
  origem ausente, tipo fora do domínio e duplicata. Relatar a exceção órfã. Expor a forma do
  arquivo em `python3 -m rsl gramatica`. Verificar pelos cenários de "Exceções declaradas
  pelo pesquisador".
- [ ] 1.3 Retirar de `cobertura.py` a heurística de plural irregular (`_PLURAIS_IRREGULARES`)
  e passar o reconhecimento às exceções declaradas. Verificar que nenhum par aceito hoje
  passa a reprovar sem exceção correspondente na migração (grupo 5).

## 2. Parâmetros de composição e plural por idioma (D2, D7)

- [ ] 2.1 Acrescentar à gramática e ao leitor das fichas a tabela "Parâmetros de composição"
  (`campo` por faceta com `envolve`/`prefixa`, `aspas`, `proximidade`, `filtros`) e as
  tabelas "Subconjuntos por campo" e "Forma radical". Verificar pelos cenários de
  "Parâmetros de composição declarados na ficha" e em `python3 -m rsl gramatica`.
- [ ] 2.2 Fazer a linha `plural` aceitar valor por idioma e a linha "Lematização" aceitar
  estado por idioma, com a conferência do lastro por idioma. Verificar pelos cenários
  modificados de `cobertura-por-base`.

## 3. Geração das fichas (D1, D3, D4)

- [ ] 3.1 Compor os blocos de string e de subconjunto, e os de expressão, a partir da STR,
  da declaração de cobertura, dos parâmetros e da flexão, na ordem de D3. Verificar pelos
  cenários de "Composição dos blocos a partir da STR".
- [ ] 3.2 Implementar a partição pelo teto, com âncoras íntegras, conferência da união dos
  termos e reprovação das âncoras acima do teto. Verificar pelos cenários de "Partição pelo
  teto de caracteres".
- [ ] 3.3 Criar `python3 -m rsl procedimentos gerar [<sigla>] [--gravar]`, com ensaio por bloco e
  com as formas flexionadas e a sua origem (`regra` ou `exceção`). Gravar só os blocos
  gerados, de forma atômica e com releitura; recusar a gravação diante de flexão
  indecidível ou de leitura reprovada. Verificar com `procedimentos gerar -h`, com o ensaio sobre
  as fichas correntes e com uma gravação numa cópia, comparada por `diff`: nada fora dos
  blocos gerados muda.
- [ ] 3.4 Registrar `procedimentos gerar` na ajuda e no requisito "Ponto de entrada único".
  Verificar que `python3 -m rsl` sem subcomando lista `procedimentos`.

## 4. Conferências e autoteste (D8)

- [ ] 4.1 Fazer `conferir` reprovar, por base, o bloco gerado que difere da geração,
  nomeando o bloco e `procedimentos gerar <sigla> --gravar`. Verificar com um bloco editado numa
  cópia.
- [ ] 4.2 Fazer o termo só no singular reprovar em idioma de plural explícito, salvo
  `nao_contavel`, `vetada` ou truncamento declarado, inclusive na forma curada. Verificar
  pelos cenários de "Termo só no singular reprova".
- [ ] 4.3 Acrescentar ao autoteste os casos de `geracao-das-fichas` e de `flexao-dos-termos`,
  e os de plural por idioma. Mostrar que cada caso falha com a conferência ou a recusa
  correspondente desligada. Verificar que `python3 -m rsl autoteste` não tem falha.

## 5. Migração das fichas

- [ ] 5.1 Transcrever para as quatro fichas a tabela de parâmetros e, na ERIC, as tabelas de
  subconjunto (`STR1b`) e de forma radical (FCT2), a partir da forma atual. Confirmar a
  transcrição com a flexão desligada: o ensaio deve reproduzir os blocos atuais. Explicar
  cada diferença ao pesquisador antes de seguir; parâmetro que a tabela não exprima
  interrompe a migração para decisão (design, Risks).
- [ ] 5.2 Montar `docs/flexoes.toml` a partir das reprovações de flexão indecidível e dos
  pares irregulares de hoje, por idioma. Cada exceção proposta pelo agente leva `origem` que
  o diga e vai à lista do LOG_IA. Apresentar a lista ao pesquisador e só gravar a ficha
  depois da revisão dele.
- [ ] 5.3 Rodar o ensaio de `procedimentos gerar` para todas as bases, revisar a diferença com o
  pesquisador e gravar com `--gravar`. O ensaio vai ao relato da aplicação. Verificar que
  `conferir` não reprova nenhuma base por bloco divergente nem por termo só no singular.
- [ ] 5.4 Retirar da prosa das fichas o que passou a parâmetro: a descrição da forma da
  ERIC e a frase sobre o plural. Verificar que a seção 3 não descreve em prosa o que a
  tabela declara.

## 6. Documentação, skills e registro

- [ ] 6.1 Criar a skill `flexao-por-base` (D9): decisão entre plural explícito e
  lematização por idioma, sonda pareada de medição, julgamento de não contável e
  irregular, e o que conferir no ensaio. Ela não nomeia base nem ensina o comando.
  Verificar com `grep -n -i -E '\b(WoS|Scopus|ERIC|BRAPCI|Web of Science)\b'` sobre a
  skill, que não deve achar nada.
- [ ] 6.2 Atualizar `ficha-de-busca-por-base` e `expressoes-de-busca` para a ficha mista,
  os parâmetros de composição e a ordem quadro → `strings gerar` → `procedimentos gerar` →
  `conferir`. Verificar a coerência com o README.
- [ ] 6.3 Declarar no README, no Mapa (quem escreve as fichas, e o arquivo de exceções) e na
  Precedência (a ordem de geração e as fichas como artefato misto), e acrescentar o passo
  em `docs/procedimentos.md`, trabalhando sobre a versão corrente. Verificar que os
  comandos documentados rodam como escritos.
- [ ] 6.4 Registrar a decisão no histórico com a skill `registrar-decisao`, sem contagem:
  - a ficha mista e os parâmetros de composição;
  - a flexão por regra e exceções, com a recusa do indecidível;
  - o plural por idioma;
  - a reprovação do termo só no singular;
  - as formas acrescentadas por nome de faceta e idioma, para o LOG_IA.
  Retirar de `data/pendencias.json` a pendência do plural de WoS, Scopus e BRAPCI e citar o
  `id` dela na entrada. Verificar que a entrada não transcreve número.
- [ ] 6.5 Integração: rodar `conferir`, `conferir-dados` e `autoteste` e relatar, no relato
  da change, os códigos e os casos não executados.

## Workflow follow-up

- Se `namespace-de-comandos-e-skills` já tiver sido aplicada, usar os nomes que ela fixou
  (decisão C1): `procedimento-de-busca-por-base` no lugar de `ficha-de-busca-por-base` e
  `[documentos] procedimento` no lugar de `[documentos] ficha`, e acrescentar
  `procedimentos gerar` ao catálogo. Se não, a tarefa 1.3a dela o faz.
- Medir a lematização por idioma na primeira execução de cada base, pela skill
  `flexao-por-base`, e só então considerar `pela lematização`.
- O teste de aderência mede, na primeira execução, o efeito dos plurais acrescentados.
- Arquivar a change depois da revisão do pesquisador.
