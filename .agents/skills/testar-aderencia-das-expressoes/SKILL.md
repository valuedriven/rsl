---
name: testar-aderencia-das-expressoes
description: "Realiza o teste de aderência das expressões de busca (M3/E2): mede o recall contra o conjunto-semente e diagnostica cada semente não recuperada pela anatomia da perda. Use ao aferir aderência, ao receber exportação de uma base, ao investigar por que um estudo esperado não foi recuperado e ao decidir se a busca está aprovada para prosseguir."
---

# Teste de aderência ao conjunto-semente

Mede uma coisa só: **a busca recupera os estudos que tinha obrigação de recuperar?**
É o portão do Módulo 3 — reprovado, não se prossegue.

## 1. Executar

```
python3 -m rsl aderencia medir
```

Lê o conjunto-semente e, de `data/registro_execucao.json`, só as execuções da expressão
executada (a sonda e as execuções diretas de conferência ficam de fora), casa por título
normalizado e pelo DOI, relatando por qual dos dois casou, e, na falta de ambos, procura
candidato por prefixo de título; imprime um **relato único** sobre o
conjunto-semente, todo de validação: a proporção recuperada, o intervalo de Wilson a 95%
sobre o mesmo numerador e denominador, e a comparação com o limiar, que decide a passagem.
**Prefixo é indício, nunca acerto**: o candidato por
prefixo sem o DOI da semente é impresso como `[? ]` e **não entra no numerador** — exige
conferência humana; o prefixo confirmado pelo DOI conta, pelo DOI. A razão impressa é sobre as
sementes informadas; a indexação declarada de cada semente é o campo `bases` do arquivo de
sementes.

O conjunto-semente é lido do arquivo de sementes (`[documentos] sementes` do
`config.toml`), e os dados de cada semente (título, resumo, palavras-chave), da cópia da
coleção do Zotero (`[dados] zotero`), ligada pelo DOI; a regra de ajuste e o limiar, do
protocolo. No arquivo, o campo `bases` declara **indexação**, não recuperação: a
recuperação é o resultado deste teste, calculado das exportações, e não se transcreve. O
alinhamento das facetas, juízo do pesquisador, é o contraponto da anatomia da perda: semente
alinhada a uma faceta sem termo dela no título, nas palavras-chave ou no resumo aponta lacuna
de vocabulário. Semente retirada
muda o denominador; recall de antes e de depois só se comparam com o registro da retirada
em `data/historico.md` (ver `definir-conjunto-semente`, §4). As exportações das bases são a
única entrada externa, depositam-se em `data/execucoes/<base>/` e se registram com
`busca registrar` antes do teste; sinopse em `docs/procedimentos.md`, M3/E2, e caminhos no
`README.md`, seção Mapa.

Antes de executar a busca, o **ensaio seco** antecipa o que cada semente entrega às facetas:

```
python3 -m rsl aderencia ensaiar
```

Imprime, por semente e faceta, os termos encontrados e o campo onde apareceram (T título,
P palavras-chave, R resumo), quantas sementes satisfazem a composição da executada só pelo
título e pelos três campos, o campo ausente na cópia e a faceta alinhada sem termo. Não
grava nada. É ensaio, não medição: as palavras-chave vêm da OpenAlex, e não da base, e a
base pode indexar outros campos. Campo ausente não é termo ausente. Quem mede é
`aderencia medir`; quem explica cada perda é a anatomia (§3).

## 2. Limiar e consequência

| | |
| --- | --- |
| **Limiar** | 80% sobre a UNIÃO das bases, aplicado ao conjunto-semente inteiro |
| **Decide** | a aderência do conjunto: um numerador, um denominador |
| **Incerteza** | o intervalo de Wilson a 95%, junto da proporção |
| **Abaixo** | revisão obrigatória do controlo terminológico antes de prosseguir, com emenda ao protocolo |

Sobre a **união**, não por base: nenhuma base isolada tem obrigação de trazer tudo, e
exigir 80% de cada uma reprovaria buscas corretas.

Limiar sem consequência é ornamento. A consequência está declarada e cumpre-se.

## 3. Anatomia da perda

Para cada semente não recuperada, **quatro consultas restritas ao DOI do estudo**
isolam a causa. Só a execução separa as quatro — atribuir a perda a uma causa sem
correr todas é adivinhação, e já se adivinhou errado neste projeto.

| # | Consulta | Responde |
| --- | --- | --- |
| 1 | o DOI sozinho, sem filtro | a base **indexa** o estudo? |
| 2 | o DOI com os filtros de ano, idioma e tipo de documento | foi o **filtro**? |
| 3 | o DOI com as duas facetas-âncora | foi o **vocabulário**? |
| 4 | o DOI com o operador de proximidade aplicado | foi a **proximidade**? |

A ordem importa: cada consulta acrescenta uma restrição à anterior, e a primeira que
devolver zero nomeia a causa.

**O limiar informa quando revisar, não o que revisar.** O diagnóstico de cada semente perdida
se faz mesmo que o limiar global seja atingido: qual faceta falhou, qual termo a teria
recuperado, se é caso isolado ou classe de termos.

## 4. O que a medição deste projeto ensinou

- **Retenção de proximidade medida em par mínimo é LIMITE INFERIOR**, não estimativa.
  Sonda deu 11,0%; nas facetas completas foram 15,4% e 18,1%. Prever a partir da sonda
  errou por larga margem, e foi preciso retratar.
- **Ausência de vocabulário não é ausência do conceito.** Fração medida por presença
  de termo é teto do que se pode descartar por essa via, não estimativa de
  irrelevância.
- **A exportação pode cegar a medida.** Registro sem palavras-chave ou sem resumo não
  pode ser aferido por vocabulário. Conferir a cobertura de campo antes de concluir —
  ver `avaliar-resultados-da-busca`.

## 5. Reprovação

Reprovação não se contorna baixando o limiar. Ou o vocabulário melhora, ou a
reprovação é declarada como limitação com emenda registrada.

## 6. Registrar

Contagens, data, base, arquivo de exportação, sementes recuperadas e não
recuperadas, e para cada perda o resultado das quatro consultas. Número que entre em
documento é **calculado a partir dos dados**, nunca transcrito — `AGENTS.md` §7.
