---
name: relato-prisma
description: Prepara o relato da revisão em conformidade com o PRISMA — lista de verificação respondida item a item, diagrama de fluxo, declaração das adaptações e das limitações. Use ao redigir o relatório, ao montar o fluxograma PRISMA, ao responder a lista do PRISMA, e ao declarar uso de IA, limitações ou não aplicabilidade de itens.
---

# Relato em conformidade com o PRISMA

O PRISMA é **diretriz de apresentação** — padrão do que precisa constar do relatório
—, e não modelo de condução, papel que cabe ao RS Banyan. Os dois operam em planos
complementares: o RS Banyan diz **como executar**; o PRISMA, **o que relatar**.

## 1. A adaptação é declarada, item a item, em três classes

Não basta dizer que o PRISMA foi concebido para revisões de efeitos de intervenções.
Cada item da lista recebe uma classe, e a classificação consta da seção de métodos:

| Classe | Itens |
| --- | --- |
| **Aplicáveis sem adaptação** | fontes, estratégia de busca, critérios de elegibilidade, processo de seleção, processo de extração, fluxo de identificação e triagem, registro do protocolo, financiamento, conflitos de interesse |
| **Não aplicáveis**, com justificativa | os que pressupõem medida de efeito, síntese estatística, meta-análise, certeza da evidência por GRADE e risco de viés por instrumentos de ensaio clínico — **não há efeito a medir** |
| **Adaptados**, com a adaptação explicitada | caracterização dos artefatos, comparação por cobertura, granularidade e grau de formalização, e síntese narrativa no lugar da quantitativa |

## 2. Avaliação dos artefatos não é avaliação de risco de viés

**Erro de categoria a evitar.** Documentação, disponibilidade, licença, alinhamento a
padrão ou ontologia de topo e evidência de avaliação são **qualidade e condições de
reutilização dos artefatos**, e é com esse nome que o procedimento figura.

Risco de viés qualifica a confiança no **estimador de efeito** de um estudo primário,
e aqui não há estimador de efeito. Por isso a declaração de não aplicabilidade dos
itens de risco de viés fica **separada** da avaliação dos artefatos, e **não é
substituída por ela**.

## 3. O diagrama de fluxo

Identificação, triagem, elegibilidade e inclusão, com as exclusões **justificadas e
quantificadas em cada passagem**. As contagens vêm do registro das contagens da busca,
alimentado por `deduplicacao` e `filtragens`.

O fluxograma não é ilustração: é a prestação de contas de cada registro que entrou e
não saiu.

## 4. As limitações que têm de constar

- **Acervos especiais não buscados directamente** — a ausência de busca nos
  repositórios de especificações técnicas é limitação metodológica, e o backward
  search de uma geração é mitigação parcial, não equivalente. Consequência: a
  cobertura dos artefatos do domínio **não se apresenta como exaustiva**, e as lacunas
  são lacunas na literatura alcançada.
- **Cobertura de campo das exportações** — a fração de registros sem palavras-chave ou
  resumo é ponto cego declarado por base, nunca silenciado.
- **Reprovação em conferência**, se houver — aderência abaixo do limiar, fidelidade da
  derivação que não coincidiu. Reprovação declarada vale mais do
  que limiar afrouxado.

## 5. Declaração de uso de IA

Redigida a partir do **LOG_IA**, na forma exigida pelo periódico-alvo, na seção de
métodos. **A IA não é autora nem co-autora**, conforme ICMJE e COPE.

A declaração diz onde a IA atuou e o que ela **não** fez: não excluiu estudo algum,
não foi avaliador independente, e não participou da decisão na 3ª filtragem.

## 6. Normalização e referências

ABNT NBR 6023. Cada referência carrega o seu **estado de conferência** — consultada e
conferida em fonte; conferida quanto aos dados, sem consulta ao conteúdo; designada
para consulta. Lista preliminar não se apresenta como fundamentação já conferida. Ver
`conferir-referencia`.

## 7. Registro prévio

O protocolo é registrado no OSF Registries **antes do início das buscas definitivas**.
É o que impede alteração de critério depois de conhecido o retorno — defeito que
nenhuma conferência posterior detecta.
