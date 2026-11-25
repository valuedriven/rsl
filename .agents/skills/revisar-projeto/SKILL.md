---
name: revisar-projeto
description: "Revisa o projeto de revisão sistemática por inteiro, sem passo próprio — percorre o estado do ciclo, executa as conferências transversais (`documentos conferir`, `dados conferir`, `projeto autoteste`) e as demais que o guia declara, confere o lastro das afirmações e a correspondência entre os componentes (questão, objetivos, facetas, quadro, strings, critérios, remissões), conduz a auditoria geral das strings e entrega os achados classificados com evidência e natureza do conserto. Use ao revisar o projeto inteiro, ao auditar as strings do protocolo, ao preparar uma rodada de emendas, ao auditar o estado antes de uma execução, ao verificar se dois componentes concordam e ao decidir como impedir que uma divergência volte."
---

# Revisar o projeto

A revisão **produz** achados percorrendo o estado do projeto inteiro. Não se confunde
com o parecer: o parecer **confere** achados que chegam prontos (`validar-protocolo`).
Aqui se procura o que ninguém apontou ainda.

Ela não escreve, não acessa fonte externa e não decide. O produto é um relatório; a promoção
de um achado a pendência ou a change depende de pedido do pesquisador.

O princípio que orienta o conserto de cada achado é o do `AGENTS.md` §8: **garantia por
construção, não por conferência**, e verificação reprovada se corrige na causa, nunca
afrouxando a verificação.

## 1. Estado

Ler o `README.md` e `docs/procedimentos.md` e dizer em que módulo e etapa o projeto está. Levantar o que está em curso:

- changes abertas, com as tarefas concluídas e as pendentes;
- arquivos modificados sem commit;
- pendências registradas e o estado de cada uma.

Não inferir estado de memória: ler os artefatos — `data/pendencias.json`, `data/historico.md`,
a lista de changes e o estado do repositório. Pendência que descreve estado já mudado é
achado, não contexto.

## 2. Conferências automáticas

Executar, **só em leitura**, as conferências e os autotestes que `docs/procedimentos.md`
declara (seção Conferências transversais). A skill não fixa comandos: eles estão no guia e
mudam com o projeto.

Relatar quantos casos rodaram, quantos **não** rodaram e por quê. Caso não executado não é
caso aprovado: a ausência de um arquivo alimentado deixa a conferência correspondente sem
prova, e isso se declara.

## 3. Lastro das afirmações

Toda afirmação de "verificado" ou "medido" tem de apontar para evidência que existe. Conferir
contra o artefato citado — arquivo, linha, execução, contagem.

- Pendências e histórico têm de descrever o estado corrente.
- Toda decisão quantitativa tem de ter números registrados; número não registrado se declara
  não registrado, nunca se reconstrói de memória.
- Falha de acesso ou de registro não é ausência de informação: fica pendência registrada.

## 4. Correspondência entre os componentes

### As correspondências que têm de valer

| De | Para | Garantida por |
| --- | --- | --- |
| questão secundária | objetivo específico | conferência manual: o objetivo nomeia o tema da questão, conferido contra o protocolo (`docs/03`) |
| objeto | questão principal | conferência manual: as mesmas operações nomeadas |
| regra de inclusão | elegibilidade e 1ª filtragem | fonte única documental: a regra no protocolo e no critério da 1ª filtragem; o plano remete. Conferência manual |
| quadro terminológico | strings | construção: `strings gerar` compõe as STRs do quadro, e `documentos conferir` reprova STR divergente da gerada e termo em duas facetas |
| facetas | expressões de busca | construção: `procedimentos gerar` compõe os blocos das STRs, e `documentos conferir` reprova composição que cite string inexistente ou omita âncora |
| seção do plano (`docs/01`) | remissão de outro instrumento | citação por chave; conferência manual ao alterar a seção |
| contra-escopo | critérios de exclusão | conferência manual: cada revisão autônoma com o seu critério |

Onde a coluna diz conferência manual, dizê-lo no registro — não apresentá-la como garantia
de construção.

### O método, em quatro passos

1. **Achar a fonte comum.** Duas coisas que precisam concordar ou saem da mesma
   fonte, ou vão divergir. Se não há fonte comum, criá-la é o conserto.
2. **Medir a divergência corrente**, com número. "Há divergência" não é achado;
   "84 termos nas strings ausentes do quadro, 47 por supressão de plural e 37 por
   introdução na qualificação" é.
3. **Perguntar: o que impede que volte?** Se a resposta for "reler", não está fechado.
4. **Escrever a regra que impede o retorno** — uma fonte única, uma conferência
   obrigatória, uma remissão por chave — e demonstrar que ela reprova o defeito que a
   motivou. **Regra que nunca reprova não protege nada.**

As divergências reais deste projeto tiveram a mesma forma — **a mesma informação escrita em
dois lugares**: quadro × strings, 84 termos, por ordem das operações (o quadro saía da lista
registrada, as strings da qualificada); remissão a seção errada do plano, dois meses sem
detecção, consertada com citação por chave; objeto × questão, duas operações perdidas,
consertada com harmonização e conferência objetivo↔questão.

### As correspondências críticas

- **Regra de inclusão** — problema que seja objeto desta revisão e carregue critério de
  exclusão; numeração descontínua; exclusão sem critério; recorte invertido; regra de
  inclusão que deixe de ser disjuntiva ou de alcançar a 1ª filtragem.
- **Quadro × strings** — quadro do protocolo montado a partir de vocabulário diferente do
  das strings.
- **Remissão de seção** — numeração do plano descontínua ou repetida; qualquer documento
  remetendo a seção extinta.
- **Notação compacta** — termo em notação de variante, com barra ou parêntese, sem
  desdobramento.

Some-se a defasagem: **documento coerente e velho em relação à fonte**. Nada o
denuncia senão a conferência.

### Conferir

1. Percorrer as correspondências da tabela e apontar, para cada uma, o documento que é
   fonte.
2. Medir a divergência corrente, com número.
3. Se a conferência motivar decisão arquitetural, registrá-la no histórico
   (`data/historico.md`, skill `registrar-decisao`).

## 5. Facetas e strings

Examinar os pontos que a experiência do projeto mostra que se perdem, pelos critérios de
`gerar-strings-de-busca` (atribuição única, poder discriminante, correspondência faceta ↔
questão):

- termo que aparece em mais de uma faceta;
- termo genérico que satisfaz a faceta quase sempre;
- conceito da questão sem termo na string;
- operador que muda a definição operacional entre bases;
- sonda que não mede o que declara medir.

## 6. Conjunto-semente

Examinar: circularidade entre ajuste e aferição; tamanho e intervalo de confiança do limiar;
incidência esperada por base; estado da conferência dos metadados.

## 7. Critérios

A regra vive no instrumento que prevalece, segundo a precedência do `README.md`. Todo critério
tem justificativa, e a nomenclatura é a mesma entre os instrumentos.

## 8. Auditoria geral das strings

Quando o pedido é auditar ou otimizar as strings do protocolo inteiro. Os critérios e o
julgamento da saída de `strings gerar` são de `gerar-strings-de-busca`; aqui, o percurso da
auditoria e o que ela entrega.

### Extrair a arquitetura antes de olhar os termos

Ler o protocolo e registrar: quantas facetas; quais são âncoras obrigatórias; qual expressão é de fato executada em base e quais são calculadas localmente ou por derivação; quais bases, em que ordem; qual o conjunto-semente; qual a regra de ajuste. Essa arquitetura decide o que cada critério pode e não pode mudar.

Atenção particular a protocolos que **executam uma expressão e derivam as outras localmente**. Neles, a qualidade das facetas não executadas afeta a classificação, não a recuperação — e por isso erros ali passam despercebidos e são os mais graves.

### Conferir contra o conjunto-semente, termo a termo

Montar tabela com uma linha por semente e uma coluna por faceta, anotando **qual termo ancora cada faceta naquela semente**, sobre título, resumo e palavras-chave publicados. É o teste que revela falha de sensibilidade real: num caso, uma semente dependia exclusivamente de `pedagog*` para a âncora de domínio, e esse termo estava apenas numa faceta que não compõe a expressão executada.

Se o protocolo propuser expressão alternativa ou contingência, rodar o mesmo teste contra ela e **relatar a perda em número de sementes**, não em impressão.

### Registrar as emendas

Uma linha por alteração, com quatro colunas: **emenda, razão, efeito esperado e risco**. A coluna de risco não é opcional: emenda sem custo declarado não é auditável, e é ela que se defende em banca. Toda alteração de protocolo é emenda e precisa constar do relato.

### Separar o que não se resolve em gabinete

Listar as pendências de verificação na execução, com o que fazer em cada desfecho. Nunca afirmar comportamento de interface que não se confirmou. Se a documentação pública de uma base não disser o que se precisa saber, dizer isso e prescrever teste-piloto — não presumir.

### Entregáveis da auditoria

1. Protocolo revisado, **no mesmo layout do original** — mesmos títulos de seção, mesma ordem, mesmo formato de tabela. Conferir por comparação automática dos títulos, não a olho.
2. Tabela de emendas com razão, efeito esperado e risco.
3. Saída de `strings gerar` e de `documentos conferir`, antes e depois.
4. Lista de pendências de verificação na execução.

Perguntar antes de produzir só se a arquitetura do protocolo for ambígua quanto a **qual expressão é executada em base**, porque disso depende todo o resto. As demais dúvidas resolvem-se propondo com a justificativa à vista e marcando o ponto para decisão.

Se for pedida versão enxuta, retirar a camada de justificativa — preâmbulo de versão, marcadores de alteração, linhas explicativas acrescentadas às tabelas, tabelas comparativas, teste de mesa e anexo de emendas — e preservar as otimizações no texto. Dizer depois, na resposta, o que a fidelidade ao layout original obrigou a descartar.

## Produto

Relatório com:

- o resultado primeiro;
- a tabela do que se executou — leitura ou conferência — e o resultado de cada item;
- os achados, cada um com a evidência (`arquivo:linha` ou comando), o estatuto epistêmico
  (verificado, inferido ou hipótese), a classe de conferência de `validar-protocolo`
  (por remissão), a natureza do conserto (unilateral, decisão do pesquisador ou código) e a
  garantia proposta;
- o que não se fez e por quê;
- as frentes sugeridas, com o impacto de cada uma.

Não copiar para o relatório as classes nem as regras de `validar-protocolo`: remeter.

## Três regras próprias

1. **Comportamento de código só se afirma depois de ler o código.** O autoteste cobre o
   comportamento que exercita, não o que o código faz fora dele. Afirmação sobre o código
   sem leitura é hipótese, e se declara como tal.
2. **A varredura de um padrão abrange o projeto inteiro**, não só o lugar onde ele foi visto
   primeiro. Padrão encontrado num procedimento de busca se procura nas demais, nos documentos e no código.
3. **A revisão não escreve, não acessa fonte externa e não decide.** Indexação, dado
   bibliográfico e sintaxe de base ficam como inferência até a conferência pela skill própria
   (`conferir-referencia`, `executar-sondagens-de-sintaxe`). Achado que exige decisão vira
   alternativa apresentada ao pesquisador; promovê-lo a pendência ou a change depende de
   pedido dele.

## Remissões

Mapa e precedência: `README.md`; etapas e comandos: `docs/procedimentos.md`. Classes de achado e medição do que se raciocina:
`validar-protocolo`. Vocabulário, facetas e strings: `destacar-termos-da-questao`,
`gerar-strings-de-busca` e `elaborar-expressoes-de-busca`. Sementes: `definir-conjunto-semente`.
Critérios: `definir-criterios-de-elegibilidade`. Decisão e propagação: `registrar-decisao`.
Lacunas e síntese: `analisar-conteudo-dos-estudos`.
