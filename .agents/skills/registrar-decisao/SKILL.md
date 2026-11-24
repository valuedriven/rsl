---
name: registrar-decisao
description: Registra uma decisão arquitetural ou emenda do protocolo, julgando o seu alcance — de escopo, de elegibilidade ou de busca — e propagando-a às fontes e ao histórico. Use ao tomar, alterar ou reverter qualquer decisão metodológica da revisão, e ao fechar ou abrir pendência.
---

# Registrar uma decisão

O que distingue revisão sistemática de levantamento é que **a decisão fica
registrada, com a razão e a data**. Esta skill é sobre o julgamento do registro; o
ciclo de arquivos é consequência, não o ponto.

## 1. Julgar o alcance — o passo que não se automatiza

Quatro alcances, e a diferença entre eles decide o que mais precisa acontecer:

| Alcance | O que altera | O que exige além do registro |
| --- | --- | --- |
| **de redação** | só o texto | nada; **não se registra** |
| **de escopo** | o objeto da revisão | revisitar questão, objetivos e facetas |
| **de elegibilidade** | o que entra no portfólio, sem alterar a busca | revisitar critérios e o que já foi triado |
| **de busca** | as expressões | **reexecução e novo teste de aderência** |

Classificar errado para baixo é o erro caro: emenda de busca tratada como redação
deixa o portfólio incoerente com a expressão que o produziu.

## 2. O que o registro tem de dizer

**Só decisão arquitetural da revisão** — questão, escopo, critérios, método, estratégia
de busca, emenda do protocolo. Decisão de instrumento, de ferramenta ou de redação,
curadoria e manutenção de artefato e correção de defeito **não se registram**: o
artefato corrigido e o controle de versão bastam.

A entrada é curta, o mínimo que um leitor precisa para entender a decisão:

1. **o que estava e por que mudou**, numa frase;
2. **o que passa a valer, com o alcance** declarado;
3. **o que NÃO se alterou e por quê**, só quando a omissão puder ser lida como esquecimento.

O terceiro é o mais esquecido e o mais útil. Foi ele que impediu, neste projeto, que
a supressão de dois problemas do escopo tornasse elegível o estudo que os critérios
(b) e (i) excluem. Quem lê o registro daqui a um ano precisa saber que a omissão foi
decidida, não esquecida.

**O que o registro não diz: contagem.** O registro nomeia o que mudou — os termos, as sementes,
os critérios — e o valor de parâmetro decidido, não o tamanho do que mudou nem o resultado
das conferências. Número transcrito diverge na alteração seguinte e passa a contradizer o
artefato; quem precisa dele o recalcula. O que mais o registro não guarda está no
`README.md`, seção Três registros.

## 3. Onde vive cada coisa

- **O instrumento guarda a última definição.** Sem histórico, sem data.
- **O histórico (`data/historico.md`) guarda as decisões**: linha do tempo, decisões
  revogadas, emendas. O que mais se registra, e onde, está no `README.md`, seção Três registros.

## 4. O ciclo, depois do julgamento

1. alterar o documento de `docs/` que guarda a definição;
2. conferir as remissões afetadas nos demais instrumentos;
3. se a decisão for arquitetural, acrescentar a entrada curta ao histórico (§2).

## 5. Quando perguntar em vez de decidir

Decisão de **escopo, método ou elegibilidade** que o pedido não resolva: perguntar ao
ReT, com as opções e o custo de cada uma. Alteração reversível de redação: executar e
relatar.

A assimetria é deliberada — redação desfaz-se com um commit, escopo mal decidido
contamina o portfólio inteiro.
