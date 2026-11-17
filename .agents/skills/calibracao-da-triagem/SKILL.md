---
name: calibracao-da-triagem
description: Conduz o estudo de viabilidade e a calibração da triagem assistida por aprendizado ativo antes do primeiro uso, e decide se ela é adotada. Use ao calibrar o ASReview, ao medir sensibilidade, ao definir amostra de referência, e ao decidir entre triagem assistida e integralmente humana.
---

# Calibração da triagem assistida

A ferramenta **ordena a fila de leitura; não decide inclusão**. A calibração responde
a uma pergunta só: a ordenação é boa o bastante para valer a pena? Não sendo, a
triagem permanece integralmente humana — e o cronograma não depende da adoção.

## 1. As cinco definições do procedimento

**(1) Sorteio.** Amostra por sorteio aleatório simples sobre o corpus deduplicado,
com **semente registrada no LOG_IA**, de modo que o sorteio seja reproduzível. Não se
compõe a amostra por conveniência nem pelos primeiros registros de cada base.

**(2) Representatividade.** Sorteio estratificado por base de origem, em proporção ao
número de registros que cada uma contribui após a deduplicação, e a distribuição
obtida é conferida contra a do corpus antes de a amostra ser usada.

**(3) Independência dos conjuntos.** A amostra parte-se em **dois conjuntos
disjuntos**, de ajuste e de aferição, em dois terços e um terço. O modelo ajusta-se
só no primeiro; a sensibilidade afere-se só no segundo.

> Sensibilidade medida no conjunto que ajustou o modelo é **otimista por construção**
> e não sustenta a decisão de adotar ou recusar. Era a pergunta mais séria do parecer
> externo sobre este ponto.

**(4) Falsos negativos.** Cada item relevante que a fila deixar na cauda é registrado
**individualmente**, com o motivo provável. Falso negativo em item do conjunto-semente
**reprova a calibração**, independentemente da sensibilidade agregada.

**(5) Sensibilidade não estimável.** Menos de 30 relevantes no conjunto de aferição e
o intervalo de confiança fica largo demais para decidir: a triagem permanece
integralmente humana. **A dúvida resolve-se contra a adoção da ferramenta.**

## 2. Limiar e consequência

| | |
| --- | --- |
| Tamanho da amostra | mín(N; máx(0,20·N; 200)) sobre o corpus deduplicado — nunca excede o corpus |
| **Limiar** | sensibilidade ≥ **95%** no conjunto de aferição |
| **Consequência** | abaixo, a triagem permanece integralmente humana, com emenda ao protocolo |

## 3. As três condições da adoção, que a calibração não dispensa

- **Calibração prévia** — a ferramenta não entra em produção sem conjunto de
  referência rotulado à mão e sensibilidade aferida.
- **Fila percorrida INTEGRALMENTE**, sem interrupção por saturação aparente. É esta a
  mitigação do viés de reforço que a priorização introduz: a priorização altera a
  **ordem** de leitura, nunca o **conjunto** lido.
- **Registro no LOG_IA a cada execução**, com versão da ferramenta e do modelo,
  porque a ordenação da fila é decisão assistida e precisa ser reprodutível.

## 4. O que a adoção não contrata

**Prazo.** O cronograma de quatro meses **não depende** da adoção. A ferramenta
antecipa a leitura dos pertinentes dentro de uma fila que é lida por inteiro de todo
modo; não reduz o conjunto lido e, por isso, não reduz o tempo de leitura.

O risco que traz é **operacional**: ferramenta adotada precisa estar operante antes
da 1ª filtragem, e a curva de aprendizado corre por conta do ReT.

Afirmar ganho de prazo foi divergência entre instrumentos, apanhada pelo parecer.

## 5. Independência em relação ao revisor

O revisor **não vê a classificação da IA** nem a decisão do outro revisor antes de
registrar a sua. A saída da IA abre-se depois do desbloqueio da rodada e serve à
conferência das divergências, não à formação da decisão. Ver `filtragens`.

## 6. Estado

Pendência **P13**, aberta: o estudo de viabilidade nunca foi feito. Até que seja, a
triagem é integralmente humana por omissão — que é o estado seguro.
