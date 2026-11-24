# Design

## Context

Ver proposal.md (Why). Estado de partida, verificado em 2026-11-24:

- A tabela de instrumentos declara os quatro como `Automático`, com `Caminho` em
  `https://www.vocabularyserver.com/<instância>/services.php`; a linha da UNESCO traz `/en/`,
  e uma frase abaixo da tabela diz para trocar por `/es/`.
- `configuracao mostrar` termina com PROTOCOLO_ILEGIVEL: `eric` e `brased` sem cliente.
- Clientes atuais: `tbci` (TemaTres, endereço fixo no módulo) e `unesco` (SPARQL do
  endpoint oficial `vocabularies.unesco.org`).
- Planilha: 71 linhas, nenhuma com `decisao_ReT`; 28 de `eric` e `brased` pendentes de
  validação manual; as de `tbci` e `unesco` consultadas em endereços que deixam de ser os
  vigentes (o do `tbci` muda só de domínio, sem `www`).
- Sondagem de 2026-11-24 (agente, uma requisição por vez): `eric/services.php` e
  `brased/services.php` responderam JSON TemaTres; a página HTML de `tbci` e a página
  principal do servidor responderam com verificação anti-robô, e a sondagem parou. O
  pesquisador conferiu à mão os quatro endereços.
- As instâncias são cópias: a descrição do ERIC diz basear-se no arquivo de
  `eric.ed.gov` (lastMod 2023-05-09); a do Brased tem lastMod 2020-02-16 e declara só
  relações hierárquicas.

## Goals / Non-Goals

**Goals:**
- Protocolo legível com os quatro instrumentos `Automático`.
- Endereço de consulta só no protocolo, inclusive a variação por idioma.
- Reconsulta de todas as linhas sem decisão garantida pela construção, sem comando nem
  opção de "refazer".

**Non-Goals:**
- Retirar o modo `Manual` do domínio.
- Cliente para serviço que não seja TemaTres.
- Avaliar se a cópia em vocabularyserver.com é evidência de autoridade suficiente: a
  decisão de usá-la é do pesquisador e está tomada; o relato a declara.
- Preencher `decisao_ReT`.

## Decisions

### D1. Um cliente TemaTres, endereço vindo do protocolo

O pacote `termos/clientes/`, com um módulo por sigla, dá lugar a um cliente TemaTres que
recebe o endereço resolvido. A lógica atual do `tbci` (busca, casamento exato por item,
`fetchAlt/Up/Down/Related/Notes`) é a base, com o endereço como parâmetro.

*Alternativa descartada:* manter um módulo por sigla, todos importando um núcleo comum.
Manteria a regra "cliente com o nome da sigla" sem nada que a justifique, e o endereço
continuaria duplicado entre protocolo e código.

*Consequência:* o cliente SPARQL da UNESCO sai. A evidência da UNESCO passa da fonte
oficial à cópia TemaTres — escolha do pesquisador.

### D2. Marcador `{idioma}` no `Caminho`

O leitor resolve o endereço por (instrumento, idioma): troca `{idioma}` pelo código do
idioma do quadro (`en`, `es`). Qualquer outro `{...}` reprova. A planejamento devolve o
endereço resolvido junto com o instrumento, e é ele que o cliente usa e que se compara com a
`url_consultada`.

*Alternativas descartadas:* uma linha por idioma (`unesco-en`, `unesco-es`), que divide o
instrumento e orfana as linhas da planilha; troca de `/en/` por `/es/` fixada no código, que
põe valor de parâmetro no código.

Não se exige `{idioma}` em instrumento com mais de um idioma: uma instância TemaTres pode
ser multilíngue (PD04).

### D3. Estatuto proposto e forma do termo

Casamento exato de rótulo → `STATUS_AUTORIZADO` (decisão do pesquisador: preferido ou não).
`STATUS_EQUIVALENTE` deixa de ser produzido pelo cliente; continua admitido na leitura da
planilha, por haver linhas antigas.

Nova coluna `forma_no_instrumento` em `planilha.campos_validacao` (`config.toml`), depois de
`rotulo_autorizado`. Preenchida só com a marca que a resposta TemaTres traz; se o item não
traz a marca, a coluna fica vazia com a observação correspondente — nunca inferida, por
exemplo, de `fetchAlt` vazio.

A marca foi medida na sondagem de 2026-11-24: cada item de `search` traz `no_term_string`.
Com valor `false`, `string` é termo preferido; com texto, o item é a entrada do termo não
preferido `no_term_string`, que remete ao preferido `string`, e o `term_id` é o do
preferido. O casamento procura primeiro o rótulo preferido e só depois o não preferido; no
segundo caso, `rotulo_autorizado` e as relações são as do preferido. Esse significado do
campo foi inferido do padrão das respostas (no ERIC, `Educational Access` → `Access to
Education`, sem `index`), não conferido em documentação do TemaTres. Nas sondas de TBCI,
UNESCO e Brased o campo veio sempre `false`.

### D4. Reabertura por construção

Em `carrega()`, para cada linha existente de instrumento `Automático`, sem `decisao_ReT`:

- `status_proposto` = pendente de validação manual → volta a `estado_inicial`;
- `url_consultada` não vazia e que não começa pelo endereço resolvido vigente → volta a
  `estado_inicial` (campos de consulta limpos; `arquivo_evidencia` limpo na linha, arquivo
  mantido em `data/evidencia/`).

Com `decisao_ReT`, a linha é mantida e entra numa lista impressa por `termos exportar`,
`termos importar` e `termos validar`. Como a regra mora na reconstrução da planilha,
qualquer mudança futura de `Caminho` reabre as linhas afetadas sem passo manual.

*Alternativa descartada:* opção `termos validar --refazer`. Depende de alguém lembrar de
usá-la; a linha velha continuaria parecendo válida.

### D5. Sonda por endereço

`termos sondar` percorre (instrumento, idioma resolvido): `fetchVocabularyData`, os termos de
prova daquele idioma e o termo inexistente, e imprime o que a resposta traz sobre a forma do
termo. A ordem é sequencial, com a pausa do cliente, e para no primeiro `FonteExterna`.

### D6. Bloqueio por verificação anti-robô

Os marcadores de `termos/http.py` ganham `verifying your browser` e `just a moment`. Mesmo
sem eles, o corpo HTML no lugar de JSON já interrompe (`json_de`); os marcadores tornam a
mensagem explícita. Nenhuma pausa maior, nova tentativa ou outro endereço.

### D7. Termos de uso: conferidos, sem termos explícitos; automação conservadora

Conferência feita pelo pesquisador em 2026-11-24, no navegador: a raiz de
`www.vocabularyserver.com` não traz termos de uso; os termos, quando existem, são próprios de
cada instância, e as páginas `sobre.php` das instâncias consultadas trazem só informação
genérica. Nenhuma das quatro instâncias declara termos explícitos de uso nem de acesso
programático.

Decisão do pesquisador (2026-11-24): seguir com a consulta automatizada a `services.php`,
o serviço público documentado do TemaTres, nas condições que o código impõe — uma
requisição por vez, pausa de 1 s, identificação de uso acadêmico no `User-Agent`, nenhuma
nova tentativa, parada imediata em 403, 429, 5xx ou página de verificação anti-robô.

*Alternativa descartada:* pedir autorização ao operador antes de automatizar — a validação
ficaria parada sem prazo, e a consulta manual também não tem termos explícitos.

Ausência de termos não é autorização: a decisão aceita o risco residual, indicado pela
proteção anti-robô das páginas HTML do servidor. Este registro encerra a condição de acesso
da PD32.

## Risks / Trade-offs

- [Verificação anti-robô no meio da validação] → a validação para com FONTE_EXTERNA, o que
  foi consultado fica gravado; a retomada é decisão do pesquisador, nunca automática.
- [Sem termos de uso explícitos (D7)] → volume baixo, sequencial, com parada imediata;
  qualquer bloqueio encerra a automação e volta ao pesquisador.
- [Cópias desatualizadas: ERIC 2023, Brased 2020] → `versao_instrumento` registra título e
  `lastMod` de `fetchVocabularyData`, para o relato declarar a data da cópia.
- [Brased só com relações hierárquicas] → `termos_relacionados_TR` vazio é esperado nele e
  não indica falha.
- [Termo não preferido proposto como descritor] → a coluna `forma_no_instrumento` preserva
  a distinção quando o serviço a informa; a decisão final continua na `decisao_ReT`.
- [Volume de requisições] → até seis por termo encontrado (busca e cinco relações), uma por
  vez, com pausa de 1 s.

## Migration Plan

1. Código, configuração e autoteste.
2. Pesquisador troca `/en/` por `/{idioma}/` na linha da UNESCO e retira a observação.
3. `projeto autoteste`, `configuracao mostrar`, `termos exportar` (todas as linhas sem
   decisão voltam a aguardar consulta).
4. `termos sondar`; ajuste do cliente à forma medida; `termos validar todos`.

Reversão: `git revert` do código; a planilha regrava-se do protocolo e a evidência bruta
anterior não é apagada.
