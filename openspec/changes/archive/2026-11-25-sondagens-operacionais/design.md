# Design

## Contexto

A fonte de cada base é lida em duas etapas, nesta ordem:

1. `le_fonte` (`src/rsl/fonte.py`) valida a forma do `procedimento.toml`, as sondagens
   incluídas.
2. `Composicao` (`src/rsl/procedimentos.py`) monta as strings flexionadas e as consultas de
   cada expressão a partir do protocolo, com âncoras, proximidade, consultas de campo,
   disjunção separada e partição pelo teto.

`roteiro(fonte, registro)` escreve o roteiro de sondagens a partir só da fonte. Por isso não
tem acesso ao texto das expressões. `sondagens.registra` também lê só a fonte e grava
`c["texto"]` como texto submetido.

Os 8 casos atuais, conferidos na fonte de cada base:

| Base | Sondagem | Necessidade |
| --- | --- | --- |
| WoS | SD5 teste | EB4 inteira |
| Scopus | SD2 controle | EB5 com `AND` no lugar de `W/5` |
| Scopus | SD2 teste | EB5 inteira |
| Scopus | SD4 teste | EB4 inteira |
| ERIC | SD12 teste | a consulta mais longa de EB4 (particionada) |
| BRAPCI | SD4 teste | EB5 inteira |
| BRAPCI | SD4 controle | metade 1 da faceta 🟦 com a faceta 🟨 (EB5 = #1 AND #2) |
| BRAPCI | SD4 controle | metade 2 da faceta 🟦 com a faceta 🟨 |

## Objetivos / Não objetivos

**Objetivos:** o texto de toda consulta de sondagem sai literal no roteiro, sempre igual à
composição corrente. Uma referência inválida reprova antes de gerar. Uma consulta em prosa
com marca de referência reprova.

**Não objetivos:**

- transformação livre, como expressão regular ou substituição de texto;
- transformação sobre expressão de várias consultas;
- resolver `onde`;
- conferir a "literalidade" de `texto` além das marcas de referência: não há como saber, em
  geral, se uma cadeia é sintaxe válida de uma base.

## Decisões

**1. Referência resolvida na composição, não cópia na fonte.** O texto vem de `Composicao`,
a mesma que escreve a seção 4. Assim, o bloco da sondagem e o da expressão não divergem por
construção. A alternativa, colar o literal na fonte, foi descartada pelo pesquisador: duplica
o dado e fica defasada em silêncio quando as strings mudam.

**2. Validação em duas camadas.** O que depende só da fonte fica em `le_fonte`:

- `texto` e `expressao` exclusivos;
- forma de `consulta`, `sem_proximidade` e `metade`;
- `parte` ∈ {1, 2};
- `faceta` entre as facetas da composição da fonte;
- `sem_proximidade` só com `[composicao] proximidade` declarada;
- marcas de referência em `texto`.

O que depende da composição fica na resolução, em `Composicao`, com ProtocoloInvalido
nomeando sondagem e consulta:

- a expressão existe e tem bloco (estatuto em `ESTATUTOS_COM_BLOCO`);
- `consulta` existe, ou é exigida quando há várias consultas;
- a transformação só se aplica a expressão de consulta única.

Toda geração e todo registro passam pela resolução, então a referência inválida nunca chega
ao roteiro.

**3. Transformações como parâmetros da composição.** `sem_proximidade` é um sinalizador em
`_ancoras`/`_texto`: as âncoras saem na mesma forma da proximidade, no mesmo campo, com
`AND` no lugar do operador, de modo que controle e teste diferem só nele (spec "Controle sem
proximidade"). Retificação da primeira redação, que remetia ao caminho sem proximidade
(cada âncora no seu próprio campo): esse caminho mudaria também a estrutura da consulta.
`metade` troca os termos da faceta na parte correspondente antes
de `_texto`. A divisão é sobre a lista de termos já flexionada, em ordem: a parte 1 leva
`ceil(n/2)` termos. Não se usa substituição sobre o texto final, porque `W/5` ou um termo
podem aparecer em mais de um lugar, e uma troca textual pode casar em silêncio onde não
devia. A alternativa de deixar Scopus SD2 e BRAPCI SD4 com controle literal pequeno foi
descartada pelo pesquisador, porque mudaria a pergunta dessas sondagens: "grupos inteiros" e
"consulta longa".

**4. `mais_longa` como seletor.** É a única seleção que o roteiro atual precisa (ERIC SD12,
que mede o comprimento máximo). O identificador explícito (`"1a2"`) fica disponível para
outros casos. Em empate de comprimento, vale a primeira consulta na ordem da seção 4, o que
torna o resultado determinístico.

**5. Renderização.** `roteiro` recebe a composição. A consulta por referência ganha, na
linha de rótulo, a origem e o número de caracteres. Exemplos: "EB4, consulta 1a2, 1.870
caracteres"; "EB5, sem proximidade"; "EB5, metade 1 de 2 da faceta 🟦". O bloco cercado
contém só o texto. O número de caracteres atende ao passo da WoS SD5 sem contagem manual.

**6. Registro grava o literal resolvido.** `sondagens.registra` monta a composição da base e
resolve as consultas antes de aplicar `--submetido`. O registro guarda o que foi à base
naquela data. A alternativa de gravar a referência foi descartada: ela mudaria de sentido
quando as strings mudassem, e o registro deixaria de reproduzir o que se submeteu.

**7. Marcas de referência.** A lista é fechada e fica na gramática:

- a expressão regular `\b(EB|STR|FCT)\d+\b`;
- a locução "procedimento gerado";
- as cores declaradas em `[composicao.FCTn] cor` da fonte.

A lista é detecção, não garantia. A garantia por construção é a referência. A detecção
existe para impedir que o defeito conhecido volte. A demonstração de que reprova é o caso do
autoteste com a conferência desligada, conforme a spec.

## Riscos / compromissos

- [Falso positivo: consulta literal legítima com `EB4` ou uma cor] → Improvável nas bases
  atuais. A mensagem nomeia a marca, e o pesquisador pode reformular. Não se cria válvula de
  escape.
- [Falso negativo: prosa sem marca, como "a consulta longa"] → Aceito: a detecção cobre o
  padrão observado. A revisão do roteiro (skill `executar-sondagens-de-sintaxe` §10) continua
  responsável pelo resto.
- [Registro mais lento, porque agora compõe a base] → Custo de uma composição, irrelevante.
- [Metade do controle passa do teto da base] → A transformação não particiona. Se o texto
  resolvido passar do `teto` declarado, a resolução reprova, nomeando a sondagem, em vez de
  escrever uma consulta que a base recusaria.
- [Leitura dos resultados antigos] → Os resultados já gravados guardam o texto declarado na
  época, inclusive em prosa. Não se reescrevem. `dados conferir` não compara texto
  registrado com a fonte, então não reprovam.

## Plano de migração

1. Implementar gramática, validação, resolução, renderização e registro, com o autoteste.
2. Migrar as 8 consultas nas 4 fontes. Reescrever os passos que mandavam copiar o bloco
   (WoS SD5, Scopus SD2/SD4, ERIC SD12, BRAPCI SD4) e o pré-requisito "o procedimento gerado,
   para copiar…", que fica sem objeto.
3. `procedimentos gerar` (ensaio, revisado) → `--gravar` para as 4 bases → `documentos
   conferir` → `dados conferir` → `projeto autoteste`.

Reversão: `git revert`. As fontes migradas não são lidas pela versão anterior (`expressao`
seria campo fora do esquema), por isso código e dados se revertem juntos.
