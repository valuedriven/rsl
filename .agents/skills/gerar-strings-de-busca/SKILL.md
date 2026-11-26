---
name: gerar-strings-de-busca
description: "Gera as strings de busca por faceta a partir do quadro terminológico (M3/E1): julga a saída de `strings gerar` e ajusta o quadro pelos onze critérios — não subsunção, atribuição única, polissemia sob a conjunção, poder discriminante, estratificação por campo, simetria multilíngue, entre outros. Use ao gerar ou otimizar strings, ajustar descritores e diagnosticar volume excessivo."
---

# Gerar as strings de busca

## Quando usar

No passo de gerar as strings de busca por faceta a partir do quadro terminológico: ao julgar a saída de `strings gerar` antes de gravar, e ao ajustar o quadro para que as strings rendam — por pedido de "otimizar as strings", "melhorar a recuperação", "ajustar os descritores" ou por diagnóstico de volume excessivo ou de sementes perdidas. Os mesmos critérios, em ordem direta, servem a construir o controle terminológico de um protocolo novo.

A auditoria das strings do protocolo inteiro é de `revisar-projeto`, seção 8. Não serve a busca pontual na literatura nem a revisão de texto do protocolo.

## Princípio que governa tudo

**O ruído de um termo não se julga nele mesmo, e sim no produto com as outras âncoras da expressão.** `learn*` é inofensivo numa busca educacional; sob conjunção com `"knowledge representation"` e `"semantic model"`, arrasta a literatura inteira de aprendizado de máquina. `taxonom*` com âncora educacional traz taxonomia de Bloom em volume industrial. `"concept map"` no domínio educacional designa técnica de ensino, não artefato documentário. Nenhum desses termos é ruim; são ruins ali. Todo juízo sobre termo isolado é provisório até se examinar a conjunção em que ele vai operar.

Corolário: **sensibilidade e precisão não se trocam termo a termo.** A maior parte do ganho vem de reescrever a forma, não de cortar alcance — truncamento, não subsunção, estratificação por campo e atribuição única rendem precisão sem custo de recall. Só depois disso se discute o que remover.

## Procedimento

### 1. Rodar o diagnóstico mecânico

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

### 2. Aplicar os onze critérios

Na ordem das quatro ordens abaixo. Os de forma primeiro, porque liberam espaço; os de validação por último, porque dependem dos demais.

A auditoria geral das strings — arquitetura do protocolo, confronto termo a termo com o
conjunto-semente, tabela de emendas, pendências de verificação e entregáveis — é de
`revisar-projeto`, seção 8.

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

## Sintaxe de cada base

O fato de sintaxe é **da base**, não desta skill: apura-se e registra-se na fonte do
procedimento de busca da base (`executar-sondagens-de-sintaxe`), e a forma que ele impõe à
expressão é de `elaborar-expressoes-de-busca`.

## Regras duras

- **Nunca retirar termo da expressão executada para reduzir volume.** É a forma mais comum de perder sensibilidade sem registro. Ordem para tratar excesso: filtros de elegibilidade na interface; refinamento reversível por categoria temática da base, com contagem antes e depois; expressão de contingência mais restrita, com revalidação pelo conjunto-semente e reversão obrigatória em caso de perda. Não há quarto passo.
- **Termo que resgata semente sozinho fica**, qualquer que seja o volume que traga.
- **Conjunto-semente usado para construir as strings é medida não independente**: o conjunto se compõe antes da busca, por caminho independente dela, e todo ele é de validação, sem sementes de desenvolvimento à parte (`definir-conjunto-semente`, §1 e §7). A ampliação do conjunto segue `definir-conjunto-semente`, por procedimento independente da string; o forward search não se usa, e a busca por citação do protocolo é só o backward de uma geração sobre os estudos incluídos (P11).
