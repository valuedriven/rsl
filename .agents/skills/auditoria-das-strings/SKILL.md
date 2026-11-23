---
name: auditoria-das-strings
description: "Audita as strings de busca e o controle terminológico de protocolos de revisão sistemática ou de escopo organizados por facetas: auditar strings quanto a redundância, polissemia, lacunas e rendimento contra o conjunto-semente, e julgar a saída de `strings gerar` e `documentos conferir`. Use ao auditar ou otimizar strings, ajustar descritores, diagnosticar volume excessivo ou sementes perdidas."
---

# Auditoria das strings de busca

## Quando usar

Quando houver protocolo de revisão sistemática, integrativa ou de escopo com facetas e strings booleanas a ajustar — por pedido de "otimizar as strings", "melhorar a recuperação", "ajustar os descritores" ou por diagnóstico de volume excessivo ou de sementes perdidas. Serve também a construir o controle terminológico de um protocolo novo, usando os mesmos critérios em ordem direta.

Não serve a busca pontual na literatura nem a revisão de texto do protocolo.

## Princípio que governa tudo

**O ruído de um termo não se julga nele mesmo, e sim no produto com as outras âncoras da expressão.** `learn*` é inofensivo numa busca educacional; sob conjunção com `"knowledge representation"` e `"semantic model"`, arrasta a literatura inteira de aprendizado de máquina. `taxonom*` com âncora educacional traz taxonomia de Bloom em volume industrial. `"concept map"` no domínio educacional designa técnica de ensino, não artefato documentário. Nenhum desses termos é ruim; são ruins ali. Todo juízo sobre termo isolado é provisório até se examinar a conjunção em que ele vai operar.

Corolário: **sensibilidade e precisão não se trocam termo a termo.** A maior parte do ganho vem de reescrever a forma, não de cortar alcance — truncamento, não subsunção, estratificação por campo e atribuição única rendem precisão sem custo de recall. Só depois disso se discute o que remover.

## Procedimento

### 1. Extrair a arquitetura antes de olhar os termos

Ler o protocolo e registrar: quantas facetas; quais são âncoras obrigatórias; qual expressão é de fato executada em base e quais são calculadas localmente ou por derivação; quais bases, em que ordem; qual o conjunto-semente; qual a regra de ajuste. Essa arquitetura decide o que cada critério pode e não pode mudar.

Atenção particular a protocolos que **executam uma expressão e derivam as outras localmente**. Neles, a qualidade das facetas não executadas afeta a classificação, não a recuperação — e por isso erros ali passam despercebidos e são os mais graves.

### 2. Rodar o diagnóstico mecânico

O diagnóstico mecânico é feito pelos comandos do projeto, não por script copiado para a
skill:

- `python3 -m rsl strings gerar` calcula cada STR a partir do quadro terminológico, com a
  subsunção já aplicada, e exibe a diferença para a tabela do protocolo; recusa termo em
  duas facetas;
- `python3 -m rsl documentos conferir` relata a coerência entre protocolo e procedimentos de
  busca, incluindo a consulta acima do teto de caracteres da base e o termo numa só forma de
  número.

O que se rodam são comandos; o que esta skill ensina é julgar a saída: a diferença que
`strings gerar` mostra é redundância a retirar ou termo que o quadro não tinha? O teto
estourado pede divisão da consulta ou revisão da faceta? A leitura não pega isso a olho —
um protocolo real tinha 75 termos redundantes em 356 e 22 termos em duas facetas ao mesmo
tempo, nenhum deles visível.

Rodar os mesmos comandos sobre o resultado, ao fim, e comparar as duas saídas. É o que
transforma afirmação em medida.

### 3. Aplicar os onze critérios

Na ordem das quatro ordens abaixo. Os de forma primeiro, porque liberam espaço; os de validação por último, porque dependem dos demais.

### 4. Conferir contra o conjunto-semente, termo a termo

Montar tabela com uma linha por semente e uma coluna por faceta, anotando **qual termo ancora cada faceta naquela semente**, sobre título, resumo e palavras-chave publicados. É o teste que revela falha de sensibilidade real: num caso, uma semente dependia exclusivamente de `pedagog*` para a âncora de domínio, e esse termo estava apenas numa faceta que não compõe a expressão executada.

Se o protocolo propuser expressão alternativa ou contingência, rodar o mesmo teste contra ela e **relatar a perda em número de sementes**, não em impressão.

### 5. Declarar a adaptação por base

Sem código de campo declarado por base, a busca não é reprodutível, e a omissão é comum. Produzir tabela com: campo e sintaxe da expressão por base, filtros de interface, e particularidades verificadas. Ver *Sintaxe: o que verificar em cada base*; o valor de cada base vem do procedimento de busca dela.

### 6. Registrar as emendas

Uma linha por alteração, com quatro colunas: **emenda, razão, efeito esperado e risco**. A coluna de risco não é opcional: emenda sem custo declarado não é auditável, e é ela que se defende em banca. Toda alteração de protocolo é emenda e precisa constar do relato.

### 7. Separar o que não se resolve em gabinete

Listar as pendências de verificação na execução, com o que fazer em cada desfecho. Nunca afirmar comportamento de interface que não se confirmou. Se a documentação pública de uma base não disser o que se precisa saber, dizer isso e prescrever teste-piloto — não presumir.

## Os onze critérios

### Forma — como escrever o que já se queria dizer

**1. Não subsunção.** Termo cujo recall esteja contido no de outro da mesma string não se repete nela. `ontology` já recupera `domain ontology`, `upper ontology` e `ontology design pattern`; `education` já recupera `higher education` e `distance education`. Registrar o subsumido na tabela e tirá-lo da string.

**2. Separação entre inventário conceitual e expressão executável.** A tabela de controle terminológico registra o espaço conceitual completo, subsumidos inclusive, porque é dela que se defende a cobertura. A string é artefato operacional e segue economia própria. Confundir os dois produz strings de 90 operadores que recuperam o que 45 recuperariam.

**3. Truncamento sobre enumeração, com variante ortográfica explícita.** Truncar o radical no ponto que une as três línguas quando possível: `educa*` absorve education, educational, educación, educativo, educacional e educação. Enumerar à parte os pares que o truncamento não une: `organization`/`organisation`, `modeling`/`modelling`, `thesaur*`/`tesaur*`.

### Arquitetura — o que cada faceta pode conter

**4. Atribuição única.** Cada termo pertence a uma faceta só. Em protocolo que calcula pertinência localmente, termo em duas facetas faz uma implicar a outra e a expressão deixa de discriminar: uma "sonda de precisão máxima" passa a medir a si mesma. A regra incide sobre o termo, não sobre a cadeia de caracteres — que `"educational setting"` contenha `educa` não a torna termo da faceta de domínio.

**5. Distinção entre termo de recuperação e variável de extração.** Nível de ensino, modalidade, instituição, população-alvo, recurso disponível não são termos de busca: são coisas que se extraem do estudo incluído. Todo documento do recorte as satisfaz trivialmente, logo não discriminam. Migram para o instrumento de fichamento.

**6. Correspondência faceta ↔ questão.** Cada questão específica precisa de vocabulário que a sustente. Conferir uma a uma. Questões sobre avaliação, reúso, manutenção, granularidade ou grau de formalização costumam ficar sem faceta alguma. A solução é **faceta auxiliar de uso exclusivamente local**, que não entra em expressão executada: ordena a fila da leitura integral e alimenta a extração, sem alterar o conjunto recuperado — e por isso pode conter termos ambíguos sem custo, já que nunca filtra nada.

### Rendimento — o que cada termo faz na prática

**7. Polissemia sob a conjunção.** O critério central, enunciado acima. Testar mentalmente cada termo contra as outras âncoras antes de mantê-lo.

**8. Poder discriminante.** Dois modos de falha opostos. O termo quase universal — `practice`, `prática`, `práctica` isolados, presentes em todo texto acadêmico — satisfaz tudo. O de rendimento esperado nulo — `"available resource"`, `"contextualização"` — não acrescenta nada. Ambos destroem a informação da faceta.

**9. Estratificação por campo.** Termo de alta ambiguidade fora do domínio vai para título e palavras-chave; termo específico vai para o campo tópico inteiro. A hipótese é empírica: quem faz um modelo de domínio ou uma taxonomia declara-o no título ou nas palavras-chave, e a ocorrência apenas no corpo do resumo é menção incidental. Replicar a mesma estratificação no cálculo local, se houver, ou os dois deixam de coincidir.

### Validação — como se sabe que ficou certo

**10. Simetria multilíngue.** Todo conceito presente em todas as línguas do protocolo, ou a ausência declarada. Conferir coluna por coluna: um protocolo real tinha "taxonomia" em português e "faceted taxonomy" em inglês, sem "taxonomy" nem "taxonomía" — falha que nenhuma leitura corrida pega.

**11. Confronto com instrumento de controle, e proveniência quando não há.** Validar descritores contra tesauro da área, preferindo os multilíngues quando o protocolo tem mais de uma língua. Onde a validação estiver dispensada por serem termos livres, exigir **registro de origem** de cada um: semente, busca-piloto ou literatura de referência. Dispensar descritor autorizado é legítimo; dispensar rastreabilidade não.

Nenhum dos onze é conclusivo antes da execução. Por isso prescrever sempre **auditoria de rendimento por termo** a posteriori: quantos registros cada termo recuperou sozinho e quantos deles sobreviveram à primeira filtragem. Termo de rendimento único nulo e volume alto é candidato à poda; termo de rendimento único positivo fica, mesmo com volume alto. A poda só se efetiva por emenda registrada e com reexecução.

## Sintaxe: o que verificar em cada base

O fato de sintaxe é **da base**, não desta skill: vai para o procedimento de busca da base, com a fonte e o estado de verificação (skill `procedimento-de-busca-por-base`), e se reconfere quando a interface muda. Esta seção lista as dimensões em que as bases divergem e o efeito de cada uma sobre a string. Nenhuma se presume igual de uma base para outra.

**Locução, lematização e sinônimos.** Em algumas bases as aspas desligam a lematização e o localizador interno de sinônimos; em outras formam locução aproximada, que já inclui plurais e admite truncamento dentro dela, e há uma segunda forma de locução, exata, que não admite truncamento. O curinga também pode desligar a lematização: o radical truncado recupera as flexões, mas não a variante ortográfica (`color*` não alcança `colour`). Daí a enumeração explícita dos pares ortográficos, e daí o plural declarado por base no procedimento de busca, nunca presumido pela skill.

**Derivação automática e curinga.** Há base com derivação de radicais desativada, em que a correspondência é exata mesmo sem aspas, e base que exige um mínimo de letras antes do curinga. As duas coisas mudam o que o truncamento alcança e se verificam antes de truncar.

**Precedência dos operadores.** Há base que processa OR antes de AND, e base que não declara a ordem. O **parêntese em torno de cada faceta é obrigatório** em todas: o que é inócuo onde a precedência ajuda é o que salva a expressão onde ela atrapalha.

**Limite de operadores e campo de busca.** O limite de operadores booleanos pode variar com o campo pesquisado. Há busca em todos os campos com limite muito menor que o da busca por tópico, e ela, além disso, recupera por texto que não é título, resumo nem palavras-chave. Em revisão sistemática, usar o campo de tópico ou os campos nomeados, nunca o de todos os campos.

**Campos e forma de execução.** Os rótulos de campo (tópico, título, palavras-chave de autor, palavras-chave atribuídas), os filtros de ano, idioma e tipo documental e a forma de execução (consulta única ou histórico de busca com conjuntos numerados) variam de base para base. O procedimento de busca declara os da base; a skill exige só que a estratificação por campo do critério 9 seja replicada no cálculo local.

**Exportação reprodutível.** Onde houver API pública de exportação, preferi-la à exportação pela interface, conferindo os parâmetros na documentação vigente e registrando-os.

**Bases monodomínio — inversão de âncora.** Em base integralmente dedicada a um domínio, exigir a faceta correspondente a esse domínio não acrescenta precisão e só subtrai sensibilidade, ao excluir o registro que não repete no resumo um vocabulário que a base pressupõe. Executar nelas a outra âncora isolada. A heterogeneidade entre bases não compromete a comparabilidade **desde que todas as facetas sejam reaplicadas uniformemente a todos os registros exportados no cálculo local** — a base decide o que é recuperado, o cálculo local decide o que é pertinente a cada expressão. É essa separação que autoriza a adaptação.

**Bases regionais e de nicho.** Capacidade booleana em geral não documentada. Prescrever teste-piloto de sintaxe antes da execução definitiva: parênteses aninhados, aspas, truncamento e comprimento máximo da consulta. Não suportada a expressão completa, decompor em consultas curtas e unir no gerenciador de referências, registrando cada consulta e cada retorno.

**Sempre verificar na execução, nunca presumir:** aceitação de curinga dentro de locução entre aspas; limite de caracteres da caixa de busca; e **comportamento quanto a diacríticos** — não presumir que `ontolog*` recupere `ontología`, nem que `prática` e `pratica` sejam equivalentes. Testar com semente conhecida em cada língua.

## Regras duras

- **Nunca retirar termo da expressão executada para reduzir volume.** É a forma mais comum de perder sensibilidade sem registro. Ordem para tratar excesso: filtros de elegibilidade na interface; refinamento reversível por categoria temática da base, com contagem antes e depois; expressão de contingência mais restrita, com revalidação pelo conjunto-semente e reversão obrigatória em caso de perda. Não há quarto passo.
- **Termo que resgata semente sozinho fica**, qualquer que seja o volume que traga.
- **Termos de desfecho não entram na string.** São escassos em título e resumo e derrubam a sensibilidade sem ganho de precisão. Vão para faceta auxiliar local e para a extração.
- **Declarar teto de triagem com a aritmética que o sustenta** quando o protocolo depender de triagem humana: registros por revisor, segundos por registro, horas resultantes. Teto sem conta é arbítrio; conta sem teto é omissão. Aferir o tempo por registro na rodada-piloto e substituir o estimado pelo observado.
- **Expansão terminológica assistida por IA exige validação humana** contra os instrumentos de controle declarados, antes de entrar no protocolo. E IA não decide inclusão nem exclusão em filtragem alguma.
- **Limiar de recuperação do conjunho-semente informa quando revisar, não o que revisar.** Exigir diagnóstico individual de cada semente perdida, mesmo que o limiar global seja atingido: qual faceta falhou, qual termo a teria recuperado, se é caso isolado ou classe de termos.
- **Conjunto-semente usado para construir as strings é medida não independente.** Prescrever ampliação por backward e forward search de uma geração e retenção de parte dos estudos fora da construção, para aferição. Relatar as duas medidas em separado.

## Entregáveis

1. Protocolo revisado, **no mesmo layout do original** — mesmos títulos de seção, mesma ordem, mesmo formato de tabela. Conferir por comparação automática dos títulos, não a olho.
2. Tabela de emendas com razão, efeito esperado e risco.
3. Saída de `strings gerar` e de `documentos conferir`, antes e depois.
4. Lista de pendências de verificação na execução.

Perguntar antes de produzir só se a arquitetura do protocolo for ambígua quanto a **qual expressão é executada em base**, porque disso depende todo o resto. As demais dúvidas resolvem-se propondo com a justificativa à vista e marcando o ponto para decisão.

Se for pedida versão enxuta, retirar a camada de justificativa — preâmbulo de versão, marcadores de alteração, linhas explicativas acrescentadas às tabelas, tabelas comparativas, teste de mesa e anexo de emendas — e preservar as otimizações no texto. Dizer depois, na resposta, o que a fidelidade ao layout original obrigou a descartar.
