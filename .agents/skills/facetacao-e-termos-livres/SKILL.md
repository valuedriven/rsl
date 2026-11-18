---
name: facetacao-e-termos-livres
description: Extrai expressões-chave da questão de revisão e monta a estrutura de termos livres por faceta, com descritores, sinónimos, termos derivados e as camadas núcleo, próximos e relacionados nos três idiomas. Use ao criar, acrescentar, retirar, traduzir ou reorganizar termo de busca e vocabulário das facetas.
---

# Facetação e termos livres

Da questão de revisão saem as **expressões-chave**; de cada expressão-chave, um
**termo livre**, que é a unidade com que as expressões de busca se compõem. Esta
skill cobre a estrutura. A consulta a tesauro é outra: `validacao-vocabulario-controlado`.

## 1. Uma faceta por expressão-chave

Nesta revisão são quatro, e a sua natureza decide a arquitetura de busca:

| | Faceta | Papel |
| --- | --- | --- |
| 1 | Artefatos de representação e organização do conhecimento | **âncora** |
| 2 | Domínio educacional | **âncora** |
| 3 | Práticas do processo de ensino-aprendizagem | temática |
| 4 | Fatores situacionais | temática |

**Âncora é obrigatória em toda expressão.** As temáticas compõem as demais. Daí a
arquitetura de contenção `EB1 ⊆ EB2 ⊆ EB4`, `EB1 ⊆ EB3 ⊆ EB4` e `EB4 ⊆ EB5` — exigir
mais facetas restringe. "Geral" nomeia a composição, não o alcance: a expressão das
quatro facetas é a **mais restritiva**, e serve de sonda de precisão, nunca de critério
de exclusão.

## 2. Três camadas, três idiomas

`nucleo` · `proximos` · `relacionados`, em `pt`, `en`, `es`, nas tabelas de controle
terminológico de `docs/03_protocolo_estrategia_pesquisa.md`.

A camada não é grau de confiança: é **distância conceitual ao termo livre**. Ela
decide o que se corta primeiro quando uma consulta encosta no teto de caracteres de
uma base, e é por camada que se discute precisão.

Controle terminológico **paralelo**, e não substitutivo, entre Ciência da Informação
e Educação: as duas tradições nomeiam a mesma coisa de modos diferentes, e usar o
vocabulário de uma só perde recall na outra.

## 3. Desdobramento morfológico contra ampliação conceitual

A distinção mais importante desta skill.

| | Desdobramento | Ampliação |
| --- | --- | --- |
| O que é | variante de forma do mesmo conceito — plural, grafia, ordem das palavras | conceito que o vocabulário não cobria |
| Reversível | sim | não |
| Exige emenda no histórico (`data/historico.md`) | não | **sim** |
| Exige novo teste de aderência | não | **sim** |

Tratar ampliação como desdobramento é alterar o recorte sem registrar.

## 4. Quatro armadilhas medidas neste projeto

- **As regras de qualificação casam a FORMA, não o lema.** Acrescentar `taxonomies`
  reintroduziu nas strings um termo que a decisão havia excluído na forma singular.
  Todo acréscimo pergunta: existe regra de qualificação que devia alcançar esta
  forma e não alcança?
- **A redução ao singular é de EXIBIÇÃO, e vem depois da qualificação.** A string
  executada conserva os plurais, porque base que não lematiza perde registro se o
  plural sair. Inverter a ordem produziu lacuna de 84 termos entre quadro e strings.
- **A BRAPCI não lê as facetas.** As suas consultas são curadas uma a uma; todo
  acréscimo exige revisitar aquela lista à mão.
- **Ensaio seco silencioso não é ensaio reprovado.** Um acréscimo conceitual pode não
  ser acionado por nenhuma das sementes — o ensaio nada diz sobre ele.

## 5. Depois de alterar

1. Conferir, termo a termo, que todo termo da string tem contrapartida no quadro da
   sua faceta. **A conferência é manual**: não há guarda automática neste repositório.
2. Conferir o comprimento das consultas da ERIC, que não trunca e tem teto medido.
3. Atualizar o quadro terminológico do protocolo (`docs/03`) e as quatro fichas a partir do vocabulário corrigido.

Depois, `expressoes-de-busca` para recompor, e `registrar-decisao` para o histórico.
