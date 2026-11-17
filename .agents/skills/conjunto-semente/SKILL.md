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
outro conjunto, de outra função, no IO 1, Item 1, 3º passo:

| | Conjunto-semente | Leitura exploratória |
| --- | --- | --- |
| Função | aferir recall | situar o tema, fixar fronteiras |
| Fonte | IO 1, Item 2, 5º passo | IO 1, Item 1, 3º passo |
| Vive no | IO 1, Item 2, 5º passo, acervos pessoais | IO 1, Item 1, 3º passo |
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
python3 src/protocolo.py --gerar
python3 src/gen_semente.py
```

Produz, em `data/saida/semente/`, `Conjunto_Semente.md` com a composição, o procedimento,
o estado de conferência e o ensaio, e `semente_aderencia.csv` para preencher. As
referências e o mapa por base vêm do protocolo; os metadados que o documento não guarda
(verificação, escopo, tipo, alinhamento, nota) estão em `data/sementes.json`. Ver
`README.md`, seção Scripts.

## 6. Limiar e consequência

O teste de aderência exige **80%** sobre a união das bases. Abaixo disso, revisão
obrigatória do controlo terminológico antes de prosseguir, com emenda ao protocolo.
Ver `teste-de-aderencia`, que é onde a medição acontece.

Acrescentar ou retirar semente altera o denominador do teste: é emenda, e exige
reaferição. Registrar — `registrar-decisao`.
