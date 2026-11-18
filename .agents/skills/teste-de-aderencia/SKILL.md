---
name: teste-de-aderencia
description: Mede o recall das expressões de busca contra o conjunto-semente e diagnostica cada semente não recuperada pela anatomia da perda. Use ao aferir aderência, ao receber exportação de uma base, ao investigar por que um estudo esperado não foi recuperado, e ao decidir se a busca está aprovada para prosseguir.
---

# Teste de aderência ao conjunto-semente

Mede uma coisa só: **a busca recupera os estudos que tinha obrigação de recuperar?**
É o portão do Módulo 3 — reprovado, não se prossegue.

## 1. Executar

```
python3 src/derivar_expressoes.py --aderencia
```

Lê o conjunto-semente e as consultas registradas em `data/consultas.json`, casa por título
normalizado e, na falta dele, por prefixo, e imprime recuperados/informados. **Prefixo é
indício, nunca acerto** — exige conferência humana. A razão impressa **não é a aderência**:
o denominador são as sementes que cada base indexa.

O conjunto-semente é lido do documento do protocolo. As exportações das bases são a
única entrada externa, depositam-se em `data/execucoes/<base>/` e se registram com
`--registrar` antes do teste; ver `README.md`, seção Scripts.

## 2. Limiar e consequência

| | |
| --- | --- |
| **Limiar** | 80% sobre a UNIÃO das bases |
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

## 4. O que a medição deste projeto ensinou

- **Retenção de proximidade medida em par mínimo é LIMITE INFERIOR**, não estimativa.
  Sonda deu 11,0%; nas facetas completas foram 15,4% e 18,1%. Prever a partir da sonda
  errou por larga margem, e foi preciso retratar.
- **Ausência de vocabulário não é ausência do conceito.** Fração medida por presença
  de termo é teto do que se pode descartar por essa via, não estimativa de
  irrelevância.
- **A exportação pode cegar a medida.** Registro sem palavras-chave ou sem resumo não
  pode ser aferido por vocabulário. Conferir a cobertura de campo antes de concluir —
  ver `conferencias-da-busca`.

## 5. Estado corrente

Pendência aberta e **reprovada**: a Scopus não atingiu o limiar, e a Web of Science
está suspensa. A anatomia da perda está desenhada e por correr para a semente 10 da
Web of Science e as sementes 3 e 4 da Scopus.

Reprovação não se contorna baixando o limiar. Ou o vocabulário melhora, ou a
reprovação é declarada como limitação com emenda registrada.

## 6. Registrar

Contagens, data, base, arquivo de exportação, sementes recuperadas e não
recuperadas, e para cada perda o resultado das quatro consultas. Número que entre em
documento é **calculado a partir dos dados**, nunca transcrito — `AGENTS.md` §7.
