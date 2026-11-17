---
name: fichamento
description: Extrai dados de cada estudo incluído para o formulário de fichamento, com pré-preenchimento assistido e conferência campo a campo no texto-fonte. Use ao fichar estudo, ao extrair dados do portfólio, ao preencher o IO 4, e ao decidir como registrar achado que não cabe nas categorias previstas.
---

# Fichamento

Extração dos dados de cada estudo incluído para o IO 4. É aqui que o portfólio vira
material analisável — e é aqui que um erro se propaga para toda a síntese sem deixar
rastro.

## 1. Os campos, e a que questão cada um serve

Cada campo responde a uma questão secundária. Campo sem questão não se preenche, e
questão sem campo não se responde.

| Campo | Questão |
| --- | --- |
| Artefatos: tipo, escopo, granularidade, grau de formalização | QS1 |
| Entidades e relações: como representa práticas; definições de prática, estratégia, método, técnica, atividade, intervenção, abordagem | QS2 |
| **Fatores situacionais** | QS3 |
| Avaliação, alinhamento, reuso, manutenção, lacunas | QS4 |
| Contexto de utilização | registro, **não** amplia o objeto |

## 2. Fink é referência de partida, não enquadramento

No campo de fatores situacionais, as cinco categorias de Fink — contexto específico
da situação, contexto geral, natureza do assunto, características dos aprendizes,
características do docente — orientam a codificação e **não a restringem**.

> Fator situacional que não corresponda a nenhuma delas é registrado no campo
> **"outros fatores"**, com a sua própria designação, e **constitui achado da
> revisão**. Não se força fator algum a uma das cinco.

Forçar o enquadramento transforma achado em ausência, e a ausência depois é lida como
lacuna da literatura quando é lacuna da codificação.

Registrar também o **vínculo entre fator e prática**, inclusive sob a forma de
regras, dependências e restrições — é o que a QS3 pede além da identificação.

## 3. Contexto de utilização, e o que ele não é

Estudo que apresente uma ontologia **e** uma implementação em grafo de conhecimento
entra pelo modelo e pela formalização; a implementação registra-se como **contexto de
utilização** e **não amplia o objeto de análise**. A instanciação está fora do recorte
— ver `questao-e-objetivos`, os três níveis.

## 4. Assistência de IA, e o seu limite

A IA **pré-preenche** os campos a partir do texto completo. Depois disso:

- **cada campo é conferido no texto-fonte** — sem excepção, inclusive os que parecem
  óbvios;
- os passos de **citação** e de **analítica** são integralmente humanos;
- **nenhuma extração entra na ficha sem conferência**, e nenhuma referência entra sem
  verificação na fonte — ver `conferir-referencia`;
- ferramenta, modelo, versão, data, finalidade e prompt vão para o **LOG_IA**.

Pré-preenchimento não conferido é a forma mais eficiente de propagar alucinação para
dentro da síntese, porque depois ninguém volta ao texto original.

## 5. Vocabulário do autor contra vocabulário da revisão

O estudo chama de "estratégia" o que outro chama de "método". **Registrar os dois**:
o termo do autor, literal, e o termo da revisão a que se mapeia. O mapeamento é
achado da QS2, não ruído a normalizar.

Termo novo que apareça com frequência vai ao glossário (IO 5) — e se for conceito que
o vocabulário de busca não cobria, é **ampliação conceitual**, com as consequências
que `facetacao-e-termos-livres` descreve.

## 6. Registrar

Uma ficha por estudo, nomeada no padrão do projeto com sufixo `_FICHA`. Campo não
aplicável declara-se como tal, e não fica vazio — vazio é ambíguo entre "não se
aplica" e "não foi lido".
