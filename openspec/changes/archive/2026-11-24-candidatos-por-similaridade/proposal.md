# Proposta

## Why

Na validação de 2026-11-24, 59 das 71 linhas da planilha ficaram como termo livre não
localizado. Isso foi contado em `data/validacao_terminologica.csv` pelo `status_proposto`. O
casamento exato não aceita variação de número nem de grafia: `teaching method` não casa com
`Teaching Methods` no ERIC. A sondagem de `fetchSimilar` (2026-11-24) teve rendimento
ruim: sugestão útil só em `teaching method`, e nas demais sondas a sugestão aparecia só
quando o termo já casava exatamente. A sondagem de `suggestDetails` (2026-11-24), que
devolve, já com identificador, os termos em que alguma palavra começa pela sequência enviada, achou o conceito
no plural em 4 de 6 termos não localizados (`teaching method` → `Teaching Methods`,
`educational practice` → `Educational Practices`, `ontologia` → `ontologias`), mas devolveu
3 itens para `teaching method` na UNESCO. `match` devolveu itens que só compartilham
palavras com o termo e foi descartado. Sem consultar o instrumento por prefixo, o ReT decide
sobre termos livres sem saber que existe um conceito próximo.

## What Changes

- Termo sem casamento exato passa por `suggestDetails` com o termo inteiro, no mesmo
  endereço resolvido. Não há truncagem por radical.
- Status novo, **candidato por similaridade (a conferir pelo ReT)**, quando o serviço
  devolve **um único** item. A linha recebe rótulo, identificador, forma e relações do
  candidato; a sugestão vai para a coluna nova `sugestao_similar`.
- Com vários itens, o código não escolhe: todos vão para `sugestao_similar`, com rótulo e
  identificador, e o termo continua termo livre não localizado; a escolha é do ReT (decisão
  do pesquisador, 2026-11-24). Sem item, termo livre não localizado, e `sugestao_similar`
  registra que não houve sugestão. A coluna nunca fica vazia numa linha consultada.
- **BREAKING** (dados): termo livre não localizado, sem decisão e sem consulta de
  similaridade registrada volta a aguardar consulta. As linhas da validação de 2026-11-24
  são reconsultadas sem passo manual.
- `termos sondar` passa a mostrar a resposta de `suggestDetails` para os termos de prova e
  para o termo inexistente.
- A linha do termo no CT continua decidida só pela `decisao_ReT`. O candidato nunca vira
  descritor por si.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `validacao-terminologica`: proposta de estatuto sem casamento exato, coluna da sugestão,
  reabertura da linha não localizada sem consulta de similaridade, sonda e autoteste
  correspondentes.

## Impact

- Código: `src/rsl/termos/tematres.py` (consulta de similaridade e proposta),
  `src/rsl/termos/planejamento.py` (status novo), `src/rsl/termos/validacao.py`
  (reabertura e contagem), `src/rsl/autoteste/validacao.py`.
- Configuração: coluna `sugestao_similar` em `planilha.campos_validacao` do `config.toml`.
- Dados: `data/validacao_terminologica.csv`. As linhas de termo livre não localizado e sem
  decisão são reconsultadas; a reconsulta substitui a evidência anterior no mesmo arquivo de
  `data/evidencia/`.
- Fonte externa: uma requisição a mais por termo não localizado (`suggestDetails`), mais
  as cinco de relações quando há candidato. Valem as mesmas
  condições de acesso (uma requisição por vez, pausa, parada em bloqueio).
- Skill `validacao-vocabulario-controlado`: status novo e coluna nova.
