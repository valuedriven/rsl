---
name: avaliar-resultados-da-busca
description: "Avalia a pertinência e a relevância dos resultados da busca (M3/E2) em três dimensões — coerência entre as expressões, fidelidade da derivação local e cobertura de campo nas exportações. Use após registrar uma execução ou receber exportação, ao diagnosticar contagem estranha e ao verificar se a derivação local das expressões reproduz a execução direta."
---

# Conferências da busca

Três conferências pós-execução, um princípio: **cada uma produz número, limiar e
consequência declarada.** Sem a consequência, a conferência é decorativa.

E uma advertência que vale para as três, e que este projeto aprendeu da pior maneira:

> **Conferir é necessário e não é suficiente.** A conferência de coerência reprovou
> uma base ruidosamente e **aprovou outra em silêncio sob o mesmo defeito**, porque
> conferência só encontra o que já aconteceu. A garantia vem da construção.

## 1. Coerência entre as expressões

A arquitetura de contenção é consequência da composição das facetas:

```
EB1 ⊆ EB2 ⊆ EB4     EB1 ⊆ EB3 ⊆ EB4     EB4 = EB2 ∪ EB3     EB4 ⊂ EB5
|EB1| ≤ min(|EB2|, |EB3|) ≤ |EB4| ≤ |EB5|
```

**Limiar:** as desigualdades verificam-se. **Consequência:** reexecução na base e
registro do defeito.

Quatro regras de diagnóstico:

- **Incoerência não se explica por hipótese.** Perguntar ao pesquisador o que foi
  efectivamente submetido, com o texto da consulta. Hipóteses operacionais inventadas
  custaram uma rodada inteira; quatro respostas dele eliminaram todas.
- **O defeito costuma estar no procedimento de busca, não no motor.** `EB2 > EB4` veio de operador de
  proximidade e filtro de tipo de documento aplicados a EB4 e não a EB2 — assimetria
  gerada por quem escreveu o procedimento de busca.
- **Nunca afirmar o que uma execução não pode ter feito.** Um argumento de teoria dos
  conjuntos vale sob a premissa, **não medida**, de que o motor aplica o operador como
  documentado. Foi preciso retratar exactamente isso.
- **Aprovação silenciosa não é aprovação.** Contagens coerentes atestam que não há
  essa incoerência, e nada mais.

## 2. Fidelidade da derivação

EB1 tem a pertinência **calculada localmente** sobre os registros exportados; EB2 e EB3
se executam apenas no teste de fidelidade, e EB5 é a sonda de sensibilidade.
O teste afere se o cálculo reproduz a base.

Procedimento: executar EB2 e EB3 **directamente** na base (estado 2 de execução, o
experimental), e comparar com a contagem derivada localmente dos mesmos registros. A
sonda de EB5 se mede à parte, por `conferencia sensibilidade`, e não se confunde com fidelidade.

**Limiar: coincidência exacta das contagens.** Não aproximada — a derivação é
determinística e qualquer diferença denuncia divergência entre o que a base entende e
o que o derivador aplica.

**Consequência:** a derivação local é abandonada e as expressões passam a ser
executadas uma a uma, com o custo de execução que isso traz.

O retorno da execução experimental **não compõe o corpus** e descarta-se após a
comparação.

## 3. Cobertura de campo nas exportações

A aferição por vocabulário só alcança o que a exportação traz. Registro sem
palavras-chave ou sem resumo é **cego** para o teste de aderência e para a derivação
local.

Medir, por base: quantos registros da exportação não têm `KW`/`DE`/`ID`, quantos não
têm `AB`, e a fração que isso representa.

**Limiar:** a fração é declarada, qualquer que seja. **Consequência:** entra no relato
como limitação daquela base, e nunca se silencia.

Medido aqui: 4 dos 64 registros da BRAPCI sem palavras-chave — 6% de ponto cego numa
das quatro bases. E 8 registros de 2027 numa exportação da Scopus, que revelaram
filtro de ano sem limite superior. **O filtro confere-se no retorno, não na consulta.**

## 4. Ao concluir

As três produzem número que entra em documento — e número em documento é **calculado
na geração**, nunca transcrito da conversa. Reprovação em qualquer delas é emenda ao
protocolo: `registrar-decisao`.
