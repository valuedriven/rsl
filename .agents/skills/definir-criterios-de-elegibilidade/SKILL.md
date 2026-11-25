---
name: definir-criterios-de-elegibilidade
description: "Define os critérios de elegibilidade (M3/E1): critérios de inclusão e exclusão, regra de inclusão entre as dimensões do objeto, regra de borda e regra de exceção, e o destino de cada critério na fonte do procedimento de cada base. Use ao redigir ou revisar critério de elegibilidade, ao levar um critério a uma base e ao tratar de contra-escopo, recorte ou revisão autônoma."
---

# Critérios de elegibilidade

Os critérios são a conversão do recorte em **regra aplicável por outra pessoa**. O
teste de qualidade é um só: dois revisores que nunca conversaram chegam à mesma
decisão lendo o critério.

Esta skill diz como elaborar, conferir e aplicar critérios. Os critérios do projeto, a
regra de inclusão vigente, o documento que é a fonte deles e o lugar do histórico estão
no `README.md` e nos documentos que ele indexa. Ler de lá; não presumir.

## 1. A regra de inclusão é única e vive numa fonte

Quando o objeto da revisão tem mais de uma dimensão, a regra de inclusão tem de dizer
como elas se combinam: todas exigidas (conjunção) ou basta uma (disjunção). É decisão de
método do pesquisador, com consequência direta sobre o que entra e sobre que lacunas se
podem enunciar ao final.

**A regra é enunciada uma só vez, no documento que o projeto declara prevalente.** Os
demais documentos (plano, critério de cada filtragem, procedimentos de busca, formulários) remetem a ela
ou a reproduzem sem mudar o sentido. Formulações divergentes da mesma regra — uma
conjuntiva, outra disjuntiva, outra mais larga que as duas no critério de uma filtragem —
são defeito comum e grave: cada revisor aplica uma, e a concordância mede a divergência
dos textos, não o julgamento.

Conferir:
- a regra em cada lugar em que aparece, contra a fonte;
- o critério de cada filtragem: pode ser mais tolerante na dúvida, mas não pode admitir
  o que a regra exclui por definição, nem exigir o que a regra dispensa;
- que pertencer a só uma das dimensões do recorte (o tipo de artefato, o domínio) não
  baste quando a regra exige outra coisa, e que algum critério diga isso.

## 2. Contribuição contra operação sobre a contribuição

A distinção que decide muitos casos difíceis.

| | Descrição | Decisão típica |
| --- | --- | --- |
| **Contribuição** do tipo que o recorte pede | o estudo produz o objeto da revisão | incluído |
| **Operação sobre** a contribuição | o estudo usa, pondera, prioriza, transfere ou aplica o objeto sem o produzir | excluído, se o recorte não abrange a operação |

A operação pressupõe a contribuição e não a produz. Estudo cuja **única** contribuição
seja uma operação é excluído; o que, além dela, produza o objeto do recorte é incluído
**pelo que produz** — e no fichamento registra-se só o que pertence ao recorte.

A distinção só exclui se algum critério a enunciar. Conferir qual critério do protocolo
vigente faz esse trabalho.

## 3. Retirar um critério pode tornar elegível o que se queria excluir

Um critério pode ser o único que alcança certa classe de estudos. Quando ele sai — por
mudança de escopo, fusão de critérios ou simplificação da tabela —, essa classe passa a
entrar sem que ninguém tenha decidido incluí-la.

Antes de suprimir, fundir ou reescrever um critério, perguntar: **que critério passa a
excluir isto?** Para cada classe que o critério alcançava, apontar o critério que a
alcança depois da mudança. Não havendo resposta, ou o critério fica, ou a inclusão da
classe é decidida e registrada como emenda de elegibilidade.

Fazer a mesma pergunta ao renumerar: remissões ao número antigo (procedimentos,
procedimentos de busca, formulários) passam a apontar outro critério, ou nenhum.

## 4. Regra de borda e regra de exceção

- **Regra de borda** — diz o que está dentro e o que está fora de uma categoria
  fronteiriça do recorte.
- **Regra de exceção** — diz quando uma característica que normalmente exclui não basta
  para excluir o estudo.

**Conferir as duas uma contra a outra, no mesmo item.** Regra de borda e regra de exceção
que se contradigam produzem decisões opostas para o mesmo estudo. Para cada regra de
exceção, construir o caso que ela salva e verificar que nenhuma regra de borda o exclui.

Onde o protocolo não tem essas regras, os casos fronteiriços são decididos pelo critério
geral: registrar cada decisão com a justificativa, para que o padrão possa virar regra
por emenda, se se repetir.

## 5. Contra-escopo, recorte e revisão autônoma — três coisas

- **contra-escopo** — o que esta revisão não faz;
- **revisão autônoma** — problema que fica para outra revisão do projeto, com critério
  de exclusão próprio;
- **fora do escopo do projeto** — problema que saiu do projeto de pesquisa; suprime-se
  do quadro e do contra-escopo, e o caso vai para o histórico.

Conferir que nenhum problema seja ao mesmo tempo objeto desta revisão e objeto de
critério de exclusão, e que cada revisão autônoma tenha o seu critério.

## 6. Critério decidível e momento de aplicação

Cada critério diz o que se observa no registro e em que filtragem se aplica: título,
título e resumo, ou texto completo. Critério que depende do texto completo não se aplica
na triagem de título, e a dúvida, nas filtragens iniciais, mantém o estudo.

Distinguir exclusão de não localização: estudo cujo texto completo não se obtém não é
excluído por mérito; é registrado como não localizado, conforme o procedimento do
projeto, e assim relatado no fluxo PRISMA.

## 7. Ao alterar

Alteração de critério é **emenda de elegibilidade** — altera o que entra sem alterar
a busca. Se alterar os termos, é emenda **de busca**, e então exige reexecução e novo
teste de aderência. Registrar o alcance no histórico: `registrar-decisao`. Conferir, na
mesma alteração, as remissões ao critério nos demais documentos (§3).

## 8. Critério por base

Na fonte do procedimento de busca de cada base, `[[criterios]]` cobre **todos** os critérios
do protocolo, inclusive os que a base não aplica (um ou mais IDs por entrada). Para cada um, um destino e o *como*; a razão, quando
houver, vai ao histórico, não à fonte:

| Destino | Quando | Exemplo de razão |
| --- | --- | --- |
| `consulta` | a sintaxe o expressa e convive com o resto; exige `clausula`, a única fonte do filtro nos blocos | cláusula de ano verificada |
| `ancora` | o critério se aplica pela faceta âncora | domínio de aplicação |
| `interface` | a base só o oferece na página, ou a cláusula quebra a consulta | operador de ano que zera consulta com grupo |
| `variante` | cláusula prevista numa variante; exige `clausula` | idioma, depois de sondado |
| `aproximado` | a busca o aproxima, e a triagem decide | inclusão temática |
| `dispensado` | a base, por constituição, já satisfaz o critério | base de um só idioma |
| `nao` | critério de leitura | adequação temática, texto completo, tipos excluídos na 2ª filtragem |

Três regras:

- **A busca não restringe além do protocolo.** Filtro que exclua tipo ou idioma admitido —
  "apenas revisado por pares", "apenas texto completo na base" — é restrição nova, não
  implementação do critério. Se parecer necessário, é recomendação ao pesquisador.
- **Critério de domínio vai por âncora**, não por filtro de categoria; categoria de assunto
  é camada de precisão, último recurso, declarada no relatório.
- **Dispensar um critério ou movê-lo para a interface é decisão registrada** no histórico,
  com o que se perde; na fonte fica só o destino e o *como*. O filtro de ano confere-se
  no retorno (`elaborar-expressoes-de-busca`).
