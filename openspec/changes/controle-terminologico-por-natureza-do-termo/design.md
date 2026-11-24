# Design

## Context

- Motivação e escopo: ver `proposal.md`.
- Estado em 2026-11-24, antes da change:
  - o protocolo traz a forma nova (`### CTn (FCTn)`, primeira célula do cabeçalho vazia,
    rótulos novos, entre eles "Termos sinônimos ou relacionados");
  - `documentos conferir` sai com PROTOCOLO_ILEGIVEL, porque `tabelas()` identifica a faceta
    pela primeira célula do cabeçalho e os rótulos de linha antigos estão fixos na gramática;
  - `data/validacao_terminologica.csv` não existe;
  - as quatro fontes de procedimento declaram `camadas = "todas"`, e nenhuma usa o corte
    `"nucleo"`.
- Regra do plano (`docs/01_plano.md`, riscos e M3/E1): termo sem consulta registrada é termo
  livre. Isso decide o lugar de todo termo sem decisão do ReT.
- A planilha de validação é indexada por (faceta, idioma, termo, instrumento), sem a linha do
  CT. Mover um termo de linha não deixa linha da planilha sem par.
- `decisao_ReT` é hoje texto livre. `termos importar` preserva o valor sem interpretá-lo.

## Goals / Non-Goals

**Goals:**
- Garantir por construção que o protocolo não apresenta como descritor, sinônimo ou
  relacionado um termo sem a decisão correspondente.
- Restabelecer a leitura do protocolo na forma nova, sem tolerar a forma antiga em silêncio.
- Manter as STRs, como conjunto de termos, idênticas às de antes da change.

**Non-Goals:**
- Executar a validação terminológica ou decidir `decisao_ReT` de qualquer termo.
- Redefinir um corte por teto de caracteres sob o critério novo.
- Gerar o CT a partir da planilha: o CT continua autoral, e a conferência o mantém coerente.

## Decisions

Decisões do pesquisador, tomadas em 2026-11-24 nesta exploração:

| # | Decisão |
| --- | --- |
| 1 | Título `### CTn (FCTn)`; mesmo número; uma faceta por CT |
| 2 | Linhas "Termo livre", "Descritores correspondentes", "Termos sinônimos ou relacionados" |
| 3 | Nomes internos `livre`, `descritores`, `relacionados` |
| 4 | Critério pela natureza do termo, segundo a regra da `decisao_ReT` (D3 abaixo) |
| 5 | Termo sem decisão vai para "Termo livre" (regra do plano); célula vazia admitida |
| 6 | Uma change só |
| 7 | Corte `camadas` retirado |
| 8 | Planilha ausente gera pendência e não reprova o termo em "Termo livre" |

A decisão 2 foi retificada na implementação, em 2026-11-24: o rótulo planejado era "Termos
sinônimos e/ou relacionados", e o pesquisador decidiu manter "Termos sinônimos ou
relacionados", como já estava no protocolo.

Decisões acrescentadas pelo pesquisador na verificação, em 2026-11-24:

| # | Decisão |
| --- | --- |
| 9 | A STR é composta só pelas linhas "Termo livre" e "Descritores correspondentes"; "Termos sinônimos ou relacionados" não entra, e termo dessa linha posto na STR reprova (D7) |
| 10 | Retirado o mínimo de termos por STR (`[conferencia] minimo_termos_string`) |
| 11 | A primeira célula do cabeçalho de cada CT é `Termo`, e outra reprova (retifica D1 nesse ponto) |
| 12 | Na linha "Termo livre", as colunas en e es passam a conter só os equivalentes dos termos pt |
| 13 | Validação automática (TBCI, UNESCO) executada pelo agente; `decisao_ReT` preenchida pelo pesquisador |

**Retificação do terceiro objetivo** ("manter as STRs, como conjunto de termos, idênticas
às de antes da change"): deixou de valer. Depois da implementação o pesquisador editou o
quadro (termos retirados e acrescentados em pt), e as decisões 9 e 12 mudam o conteúdo das
STRs. A busca muda, e o teste de aderência será refeito (PD31).

A decisão 5 retifica uma proposta anterior do agente nesta mesma exploração ("o termo
pendente fica na linha atual"), que contrariava a regra do plano.

### D1. Identificação pelo título, e não pelo cabeçalho

O leitor percorre as subseções de nível 3 de "Controle terminológico". Cada uma precisa ter o
título `CTn (FCTn)`, com espaços em volta tolerados, e uma tabela. O cabeçalho dá só os
idiomas, a partir da segunda célula. A primeira célula não é lida.

A tabela sem título CT, ou com cabeçalho na forma antiga `| FCTn | … |`, **reprova** com
PROTOCOLO_ILEGIVEL. Não é ignorada. Hoje a tabela que não casa com o padrão é descartada em
silêncio, e por isso o erro atual diz "achei []" em vez de dizer o que está errado.

Alternativa considerada: aceitar as duas formas durante uma transição. Foi recusada porque o
projeto já retirou aliases de transição (change `remocao-dos-aliases-de-transicao`), e as
duas formas significam critérios diferentes.

### D2. Rótulos casados por igualdade, e não pelo início

Hoje o rótulo é casado pelo início do texto (`startswith`). Com "Termo livre" e "Termos
sinônimos…", o prefixo comum "Termo" deixaria o casamento depender da ordem de declaração. O
rótulo passa a ser comparado inteiro, depois de retirados ênfase e espaços. Rótulo
desconhecido numa linha do CT reprova, em vez de ser ignorado.

Alternativa considerada: manter o casamento por prefixo com prefixos distintos. Foi recusada
porque o defeito apareceria só quando alguém editasse o rótulo.

### D3. Domínio de `decisao_ReT` e regra de agregação

`decisao_ReT` admite `descritor`, `sinônimo ou relacionado`, `termo livre` ou vazio, sem
distinção de caixa. Valor fora do domínio reprova em `termos importar` e na conferência
cruzada.

A linha esperada de um termo (faceta, idioma) se calcula sobre as linhas da planilha desse
termo nos instrumentos planejados para ele:

```
alguma decisao = descritor                         --> descritores
senao, alguma decisao = sinonimo ou relacionado    --> relacionados
senao (termo livre, vazio, pendente manual,
       planilha ausente)                           --> livre
```

`status_proposto`, que é a proposta da máquina, não entra na regra. Só a decisão do ReT
classifica.

Alternativa considerada: classificar pelo `status_proposto` quando não houver decisão. Foi
recusada porque o protocolo passaria a afirmar autoridade sem a conferência do ReT.

### D4. Onde fica a conferência cruzada

A conferência cruzada fica em `documentos conferir`, junto da coerência interna, porque é o
comando que impede que um protocolo incoerente siga para a geração.

- A planilha é lida pelo caminho `[dados] validacao` do `config.toml`.
- Planilha ausente:
  - termo em "Termo livre" não reprova;
  - `projeto pendencias` relata a validação pendente;
  - termo nas outras linhas reprova, porque sem planilha a linha esperada é `livre`.
- Planilha ilegível não é tratada como ausente: termina com DADOS, como os demais arquivos
  alimentados.

### D5. Repetição entre linhas reprova

Pela regra D3, cada termo de cada idioma tem uma única linha esperada. A repetição dentro do
mesmo CT e idioma passa a reprovar, como a repetição dentro da mesma linha já reprova. A
mesma forma em idiomas diferentes do mesmo CT continua admitida.

### D6. Retirada do campo `camadas`

O campo sai do esquema da `[cobertura]`. A fonte que ainda o declara reprova como campo
desconhecido, que é a regra geral do esquema. Também sai das quatro fontes, do modelo de
`procedimentos iniciar` e da tabela de cobertura do procedimento gerado.

### D7. Linhas que compõem a STR

A gramática declara as linhas da STR (`LINHAS_STR`: termo livre e descritores), e a geração e
a conferência as usam. A atribuição única e a validação terminológica continuam sobre o quadro
inteiro, porque um termo de "Termos sinônimos ou relacionados" ainda é da faceta e ainda se
valida. O termo dessa linha na STR do protocolo reprova pela remissão e pela igualdade com a
STR gerada, com a mensagem que nomeia a linha.

Alternativa considerada: aceitar o termo de relacionados na STR sem exigi-lo. Foi recusada
pelo pesquisador, porque a STR deixaria de ser determinada pelo quadro.

## Risks / Trade-offs

- [O quadro fica quase todo em "Termo livre" até a validação, e o protocolo parece ter
  "perdido" os descritores.] → É a classificação correta pelo plano. O histórico registra
  que as linhas vazias significam "não validado", e não "inexistente".
- [Reclassificar depois da validação muda a ordem das STRs e exige regenerar STRs e
  procedimentos a cada lote de decisões.] → É o fluxo já existente (`strings gerar
  --gravar`, `procedimentos gerar --gravar`). A conferência reprova a STR defasada.
- [Domínio fechado de `decisao_ReT` impede registrar outra decisão, como "retirar o
  termo".] → Retirar termo é edição do quadro, registrada no histórico, e não decisão de
  classificação. Se surgir outra necessidade, o domínio é ampliado por change.
- [A conferência cruzada passa a depender de um arquivo de dados.] → O arquivo ausente tem
  comportamento definido (D4), e o autoteste cobre os dois estados.
- [Texto autoral dos procedimentos que cite "núcleo" ou "camada", como
  `docs/procedimentos/eric/` ("Camada 3 — descritores de artefato").] → Varredura na
  implementação. O que for texto autoral se corrige na fonte, e o gerado se regenera.

## Migration Plan

1. Gramática e leitor na forma nova; o protocolo volta a ser lido.
2. O protocolo recebe a classificação pela regra: todos os termos em "Termo livre".
3. Conferência cruzada, repetição e célula vazia, com autoteste que demonstra cada
   reprovação.
4. Retirada de `camadas` das fontes, da gramática e da cobertura; regeneração das STRs e dos
   procedimentos; demonstração de que o conjunto de termos de cada STR não mudou.
5. Skills, histórico e pendências.

Reversão: `git revert` dos commits da change. Não há dado externo alterado.
