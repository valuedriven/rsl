---
name: conjunto-semente
description: Compõe, confere e mantém o conjunto-semente que afere o recall das expressões de busca, e o distingue dos estudos da leitura exploratória. Use ao montar ou alterar o conjunto-semente, ao conferir as suas referências, ao fazer o ensaio seco contra as facetas, e ao tratar de distribuição por base ou acervo pessoal.
---

# Conjunto-semente

Instrumento de **aferição de recall**: um conjunto de estudos que a busca tem
obrigação de recuperar. Se não os recupera, a busca está mal desenhada — e é isso, e
só isso, que o conjunto-semente mede.

## 1. Composto antes da busca, por caminho independente dela

A exigência que dá sentido ao instrumento. Semente colhida da própria busca mede a
busca contra si mesma e confirma o que já se esperava encontrar.

Serve também de **controlo externo do viés de reforço** da priorização por
aprendizado ativo, por ser anterior e independente.

## 2. O que NÃO é o conjunto-semente

**Não é a leitura exploratória.** O 3º passo do RS Banyan pede os estudos
inicialmente consultados acerca do tema — a leitura que precede a delimitação. São
outro conjunto, de outra função, em `docs/02`, seção Estudos inicialmente consultados:

| | Conjunto-semente | Leitura exploratória |
| --- | --- | --- |
| Função | aferir recall | situar o tema, fixar fronteiras |
| Fonte | protocolo (`docs/03`), Acervos pessoais | `docs/02`, Estudos inicialmente consultados |
| Vive no | protocolo (`docs/03`), Acervos pessoais | `docs/02`, Estudos inicialmente consultados |
| Recorte temporal | obrigatório | **dispensado** — leitura de fundamentação pode ser anterior |

Confundi-los já aconteceu: o conjunto-semente ocupou o 3º passo e a leitura
exploratória desapareceu do instrumento.

Também **não é amostra** nem portfólio, e não se usa para estimar nada.

## 3. Composição, em duas etapas

A primeira indica candidatos; a segunda confere cada um em fonte e decide. O estado
de conferência de cada referência fica registrado — ver `conferir-referencia`.

Três exigências de qualificação:

- **todos primários** — revisão sistemática não serve de semente;
- **todos dentro do recorte temporal**, para que o teste de aderência meça o desenho
  da busca e não os critérios de elegibilidade;
- **todos conferidos em fonte**, com autor, título, veículo, ano e DOI.

## 4. Incidências por base contra estudos distintos

O erro de leitura mais fácil deste instrumento, e o parecer externo tropeçou nele.

A soma das quantidades por base é de **incidências**: um mesmo estudo indexado em
duas bases conta duas vezes. Neste conjunto são 15 incidências para 10 estudos
distintos — 4 em mais de uma base e 6 numa só.

**Declarar que são incidências, e publicar o mapa por estudo.** Sem o mapa, a
distribuição não se confere.

## 5. Ensaio seco contra as facetas

Antes de executar, aplicar as facetas a cada semente e ver quais seriam acionadas.
É diagnóstico de vocabulário, não de busca.

**Ensaio silencioso não é ensaio reprovado.** Um acréscimo conceitual pode não ser
acionado por nenhuma das sementes — o ensaio nada diz sobre ele, e tratar o silêncio
como aprovação é erro.

```
python3 src/gen_semente.py
```

O comando lê as referências e o mapa por base do protocolo e os metadados autorais de
`data/sementes.json` (verificação, escopo, tipo, alinhamento, nota), gera a planilha
`data/semente_aderencia.csv` e **imprime no terminal** a composição, o estado de
conferência e o ensaio seco — quantas sementes o título entrega às facetas e quantas
satisfazem as duas âncoras e uma faceta temática. Não grava guia em arquivo: o
instrumento é a planilha.

## 6. O instrumento: a planilha e o procedimento

`semente_aderencia.csv` tem uma linha por semente e por base — com 10 sementes e 4
bases, 40 linhas. Preencher **durante** a execução, não depois: as colunas de registro
são a evidência do teste.

| Coluna | O que registrar |
| --- | --- |
| `id` | identificador da semente (SEn), conforme o protocolo |
| `autores_ano` | autoria abreviada e ano |
| `titulo` | título, como consta na referência do protocolo |
| `tipo` | primário ou secundário — preencher em `sementes.json` |
| `escopo` | DENTRO, FRONTEIRA ou ÂNCORA AUSENTE — preencher em `sementes.json` |
| `verificacao` | estado de conferência da referência — preencher em `sementes.json` |
| `base` | WoS, Scopus, ERIC ou BRAPCI |
| `esperada_na_base` | sim se o mapa do protocolo indica esta base |
| `indexada` | etapa 1: sim ou não, por busca de título. **obrigatório** |
| `data_etapa1` | data da busca de título |
| `recuperada` | etapa 2: sim ou não, por busca na exportação de EB4 |
| `como_localizada` | DOI, título ou não localizada |
| `data_etapa2` | data da conferência na exportação |
| `observacao` | o que explica o não: termo ausente, campo não indexado, recorte |

O preenchimento segue duas etapas, e a ordem importa:

- **Etapa 1 — indexação.** Buscar o título entre aspas, sem recorte temporal e sem as
  expressões da revisão. Semente que a base não indexa **sai do denominador daquela
  base** e se registra como cobertura, não como falha da busca.
- **Etapa 2 — recuperação.** Procurar a semente na exportação de EB4, por DOI e depois
  por título, **sem reexecutar a busca**.

> `indexada` em branco impede o cálculo: sem ela não há denominador. `recuperada` só se
> preenche onde `indexada` = sim.

Semente com metadado pendente — `verificacao`, `escopo`, `tipo` ou `alinhamento` em
branco, marcado `A CONFERIR` ou `PENDÊNCIA` — sai com a coluna em branco. O instrumento
pode ser executado; o que falta é registro, não dado de busca, e a pendência se reporta
em vez de se esconder.

## 7. Limiar e consequência

O teste de aderência exige **80%** sobre a união das bases. Abaixo disso, revisão
obrigatória do controlo terminológico antes de prosseguir, com emenda ao protocolo.
Ver `teste-de-aderencia`, que é onde a medição acontece.

Acrescentar ou retirar semente altera o denominador do teste: é emenda, e exige
reaferição. Registrar — `registrar-decisao`.
