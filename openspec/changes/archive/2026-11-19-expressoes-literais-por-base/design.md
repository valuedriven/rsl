# Design

## Context

A ficha é a fonte da **forma**; o protocolo é a fonte do **vocabulário**. O leitor
`src/protocolo.py` lê as strings por faceta de blocos cercados na seção 3 e trata o texto
dos blocos de cada `EBn` como a consulta a executar. Ele não conhece sintaxe de base: campo,
tag e operador vêm do texto da ficha.

Hoje a ERIC já entrega blocos literais, porque a base não aceita campos diferentes no mesmo
grupo e a expressão se desdobra em quatro consultas de campo único. WoS, Scopus e BRAPCI
entregam `#n`, que na WoS e na Scopus dependem da numeração atribuída pela sessão e na
BRAPCI não existe. A subseção de âncoras em proximidade é lida pelo leitor, mas nenhuma
conferência a consome. A conferência atual exige bloco apenas para expressão executada, de
fidelidade ou sonda; não confere o conteúdo do bloco contra a seção 3.

Não há execução registrada e `data/registro_execucao.json` não existe (PD02), então nenhuma
contagem fica vencida por esta mudança.

## Goals / Non-Goals

**Goals:**

- Cada expressão que se executa é um bloco literal, submetido como está, sem montagem.
- A conferência impede que o bloco volte a referenciar conjunto, que se defase da seção 3 e
  que a expressão derivada padrão volte a ter bloco.
- A leitura continua sem sintaxe de base fixada no código.
- A ERIC não muda de consulta.

**Non-Goals:**

- Alterar a composição das expressões no protocolo.
- Alterar a derivação local, a aderência ou a sensibilidade.
- Executar as buscas ou medir os tetos das bases.
- Adotar geração da seção 4 (ver Decisão 4).

## Decisions

### 1. Expandida única, com a ERIC como exceção

A forma passa a ser um bloco por expressão. A ERIC permanece particionada em quatro
consultas porque a base zera grupo que mistura `title:` e `abstract:`; ali "única" não é
uma opção sintática, e a forma já é literal.

*Alternativas:* manter a forma por conjuntos com ordem de criação fixa (depende da numeração
da sessão e não se reproduz a partir da ficha); manter as duas formas como pares (duas
fontes da mesma consulta, que divergem na primeira emenda). A expandida é a única que uma
terceira pessoa reproduz a partir da ficha sozinha, e é a que corresponde ao que o README
já declara — uma execução da cobertura por base.

### 2. Bloco só onde há execução

EB4 e EB5 em todas as bases; EB2 e EB3 na WoS e na Scopus, onde o teste de fidelidade as
executa. EB1 não tem bloco (nunca se executa) e, na BRAPCI, EB2 e EB3 também não (derivadas
localmente). A linha `**Facetas:**` e o estatuto permanecem em todas.

A conferência recusa bloco na expressão derivada padrão. A forma longa, quando a ficha a
declara, é representação não executada e fica fora dessa regra: o bloco nela não é forma
que se submete.

*Alternativa:* manter blocos compostos nas derivadas. Rejeitada: seriam formas que ninguém
submete e que defasam sem que a conferência as veja; a regra de recusa impede que voltem.

### 3. O grupo das âncoras entra inline; a subseção de proximidade sai

Com o bloco literal, o grupo 🟦 em proximidade com o 🟨 aparece dentro de cada expressão. A
subseção `### #5 — as duas âncoras em proximidade` deixa de existir como forma: mantê-la
seria um fragmento que ninguém submete e uma segunda cópia a defasar. O leitor aceita a
ausência (a ERIC nunca a teve) e nenhuma conferência usa `ancoras`; a instrução de partição
por recusa de proximidade migra para *Variantes*, que o leitor ignora.

*Alternativa:* manter `#5` como definição reusada — é exatamente a forma por conjuntos que
esta mudança remove.

### 4. Guarda por conferência de termos, não por geração

`--conferir` ganha duas dimensões: (a) bloco de expressão executada, de fidelidade ou de
sonda não referencia `#n`; (b) o conjunto de termos de cada bloco é o das strings das
facetas que o `**Facetas:**` declara. Operadores, prefixos de campo, parênteses, `NEAR/n` e
`W/n`, e valores dentro de cláusula de filtro (`DT=`, `LA=`, `DOCTYPE(`, `LANGUAGE(`) não
são termos.

*Por que não geração:* gerar a seção 4 exigiria um modelo de montagem por base, isto é,
sintaxe de base no leitor, que o projeto evita de propósito; e tornaria a ficha parcialmente
saída. *Por que não basta a conferência atual:* ela só exige que exista bloco.

**Limite declarado:** a conferência compara o conjunto de termos, não a topologia. Um termo
posto no grupo errado, ou um `OR` onde a composição pede `AND`, não é detectado por ela. A
topologia continua guardada pela coerência pós-execução (`EB4 = EB2 ∪ EB3`, `EB5 ⊃ EB4`) e
pela linha de facetas; a conferência nova cobre a falha silenciosa, que é a defasagem de
termo.

### 5. `#n` proibido só nos blocos que se executam

A proibição alcança o bloco da executada, das de fidelidade e da sonda. A tabela de
composição no topo da seção 4 continua em prosa, como leitura, e não é bloco cercado — não
é alcançada pela conferência.

### 6. Teto desconhecido é estado da ficha, não promessa

As consultas passam a ter ~4,1k na BRAPCI e ~10k na WoS e na Scopus. Nenhuma das três
declara o comprimento máximo; a seção 1 registra **não verificado** e a primeira execução é
a sondagem. Recusa por extensão não se contorna em execução: vira emenda que declara
`- Execução: particionada` e escreve as partes literais, mantendo as mesmas âncoras em todas
e unindo por deduplicação.

## Risks / Trade-offs

- **A consulta de ~10k pode ser recusada** → a sonda é a primeira tarefa de execução; a
  variante de partição está prevista e a adoção é emenda registrada, não ajuste silencioso.
- **As fichas de WoS e Scopus quase dobram** → é o preço de não haver montagem; a tabela de
  composição em prosa preserva a leitura, e o bloco é o que se submete.
- **A conferência de termos não vê topologia** → a coerência pós-execução cobre a topologia;
  o limite fica escrito no código e no relato da conferência.
- **A conferência nova pode reprovar a ERIC já na primeira execução** → é defeito existente
  (blocos nunca conferidos contra a seção 3); corrige-se a ficha, não se afrouxa a
  conferência.
- **Sem `data/registro_execucao.json` (PD02), a aceitação não pode ser registrada** → a
  change entrega a forma; o estatuto "aceita" fica pendente e a tarefa de sonda permanece
  bloqueada até o registro existir.
- **Reversão depois de executar** → antes da primeira execução, reverter é só reverter a
  change. Depois, voltar à forma anterior invalida as contagens: registra-se em
  `data/historico.md` e no registro de execução.

## Migration Plan

1. Aplicar as fichas e a conferência na mesma change; rodar `--conferir` e `--autoteste`.
2. Corrigir o que a conferência nova reprovar nas fichas, sem afrouxá-la.
3. Registrar a decisão no histórico e ajustar PD07, PD08 e PD10.
4. Sondar os tetos na primeira execução; se recusar, emenda de partição.

## Open Questions

Nenhuma que altere a spec ou a abordagem. O teto de cada base é incógnita **medida**, tratada
pela tarefa de sonda, não por decisão de desenho.
