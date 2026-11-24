# Design

## Context

Ver proposal.md (Why). Estado de partida, verificado em 2026-11-24:

- `termos/tematres.py` faz `search` e casamento exato (preferido e depois não preferido).
  Sem casamento, devolve termo livre não localizado e não faz mais nenhuma requisição.
- `fetchSimilar` (sondas de 2026-11-24, as cinco instâncias) devolve um texto só, sem
  identificador; sugestão útil só em `teaching method` (ERIC); sem sugestão, `"result": []`.
  Rendimento ruim: substituído.
- `suggestDetails` (sondagem de 2026-11-24, ERIC, UNESCO en, TBCI, Brased) responde nas
  versões 3.5.2 e 3.6.1, com os itens no formato de `search` (`term_id`, `string`,
  `no_term_string`, `order`). **Não é prefixo do rótulo inteiro**: casa pelo início de
  palavra, em qualquer posição, do termo preferido e da entrada não preferida (`Self teaching
  methods` → `Self instruction`; `organização do conhecimento` → também `sistemas de
  organização do conhecimento`; `educacional` → `Abordagem Educacional`). Sem item, a
  resposta não traz `result`. Na primeira sondagem (6 termos não localizados): 1 item em 3,
  3 itens em 1 (UNESCO `teaching method`), nenhum em 2. Na segunda (`termos sondar`): termo
  de uma palavra devolve dezenas de itens em ordem alfabética (ERIC `educational` 48, Brased
  `educacional` 50, Brased `educação` 50, que param em "C"). **Não verificado:** se o serviço
  limita a lista (o número redondo e o corte alfabético sugerem que sim).
- `match` devolveu, nos 6 termos sondados, itens que só compartilham palavras com o termo
  (`knowledge organization` → `Work organization`): descartado.
- A reabertura atual (`carrega`) reabre linha pendente manual e linha de outro endereço.
- A linha do termo no CT é decidida só por `decisao_ReT` (`termos/decisao.py`). A
  `status_proposto` não entra nesse cálculo.

## Goals / Non-Goals

**Goals:**
- Dar ao ReT o conceito mais próximo do instrumento quando o termo não casa, com a
  evidência bruta da sugestão e da busca.
- Reconsulta das linhas não localizadas da validação anterior por construção.

**Non-Goals:**
- Medida própria de similaridade (distância de edição, radicalização) no código: a
  similaridade é a do serviço.
- Propor descritor a partir de candidato, ou mudar a regra da linha do CT.
- Escolher entre vários itens: a escolha é do ReT (D1).

## Decisions

### D1. Prefixo do serviço, candidato só com item único

Sem casamento exato: `suggestDetails` com o termo inteiro. Um único item: candidato, com o
identificador do próprio item e as relações colhidas como hoje; a forma é a do item
(`no_term_string` texto: a entrada casada é não preferida, e o rótulo é o preferido a que
ela remete). Vários itens: nenhum é escolhido; `sugestao_similar` traz todos os devolvidos, na
ordem do serviço, por longa que seja a lista (decisão do pesquisador, 2026-11-24), e a linha
fica termo livre não localizado; `observacao_tecnica` registra quantos vieram e o
`cant_result` do serviço, porque o serviço pode limitar a lista. Nenhum item: termo livre não localizado
com `SEM_SUGESTAO`.

*Alternativa descartada:* regra estreita do item único (candidato só se casou pelo rótulo
preferido e o rótulo começa pelo termo). Implementada e revertida em 2026-11-24 por decisão
do pesquisador, que a julgou de resultado insatisfatório: dos 9 itens únicos da validação,
retiraria 6 de candidato. O item único segue candidato, a conferir pelo ReT.

*Alternativa descartada:* `fetchSimilar` confirmado por busca (versão anterior desta
change). Rendimento ruim na sondagem, e a sugestão não traz identificador.

*Alternativa descartada:* escolher entre vários itens pela diferença de número (sufixo
`s`, `es`). Regra do código, dependente de idioma; a escolha fica com o ReT (decisão do
pesquisador, 2026-11-24).

*Alternativa descartada:* `match`. Itens que compartilham palavras, não o conceito.

*Alternativa descartada:* truncagem por radical. Escolher o radical é critério do código ou
do pesquisador, não do instrumento.

*Alternativa descartada:* tomar os itens de `search` do próprio termo. A busca casa por
substring e devolve muitos itens; o prefixo é mais estreito e é o próprio serviço que o
aplica.

### D2. Status e colunas

Status novo em `planejamento.py`: `STATUS_CANDIDATO = "candidato por similaridade (a
conferir pelo ReT)"`. Coluna nova `sugestao_similar` em `planilha.campos_validacao`, depois
de `forma_no_instrumento`, com a sugestão, ou com `SEM_SUGESTAO = "(o serviço não sugeriu
termo)"`. Os campos de conceito (`rotulo_autorizado`, `uri_conceito`, forma e relações) são
os do candidato. Na linha candidata, `observacao_tecnica` diz que eles são do candidato
sugerido e não do termo.

*Alternativa descartada:* colunas separadas para o candidato (`candidato_rotulo`,
`candidato_uri`...). Dobraria as colunas de conceito, e o status já diz de quem são.

### D3. Reabertura por construção

Em `motivo_reabertura`, para instrumento `Automático`, mais um motivo: `status_proposto` =
termo livre não localizado e `sugestao_similar` vazia. O sentinela `SEM_SUGESTAO` é o que
distingue "consultado sem sugestão" de "nunca consultado". Por isso a coluna nunca fica
vazia em linha não localizada consultada. Linha com decisão segue a regra atual: preservada
e listada.

### D4. Evidência

O registro bruto da linha ganha `suggestDetails`, ao lado de `busca` e das relações, no
mesmo arquivo de evidência da linha.

### D5. Sonda antes de validar

`termos sondar` chama `suggestDetails` para cada termo de prova e para o termo inexistente,
e mostra os itens. A validação só se refaz depois de o pesquisador ver a sonda.

## Risks / Trade-offs

- [Item único de conceito diferente] → o prefixo pode dar um só item que não é o conceito
  (`teaching` → `Teaching Assistants`). O status diz "a conferir pelo ReT", e
  `sugestao_similar` mostra a entrada casada. A decisão continua na `decisao_ReT`.
- [Diferença fora do fim do termo] → o prefixo não acha (`knowledge organization` na
  UNESCO). O termo fica não localizado: é limite da estratégia, não ausência do conceito.
- [Volume] → até seis requisições a mais por termo não localizado (`suggestDetails`, cinco
  relações), uma por vez, com pausa de 1 s.

## Migration Plan

1. Código, configuração e autoteste.
2. `termos sondar`: o pesquisador confere os itens de `suggestDetails`.
3. `termos exportar` (as linhas não localizadas sem decisão voltam a aguardar consulta) e
   `termos validar todos`.

Reversão: `git revert`. A planilha regrava-se do protocolo. A evidência das linhas
reconsultadas foi substituída no mesmo arquivo e não volta com a reversão (decisão do
pesquisador, 2026-11-24: corrige-se o texto, não o mecanismo).
