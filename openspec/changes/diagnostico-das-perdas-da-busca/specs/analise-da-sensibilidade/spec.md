# Spec Delta

## Purpose

Explicar a perda medida pela sonda de sensibilidade de uma base: o que os registros
elegíveis da amostra têm que a executada não alcança, quais termos os alcançariam e quanto
cada ampliação do vocabulário custaria, estimado localmente sobre a exportação da sonda.

## ADDED Requirements

### Requirement: Entrada da análise
`conferencia simular <base>` SHALL ler a amostra classificada de `[saidas] sensibilidade`
da base e as exportações registradas da executada e da sonda. Amostra com linha sem
`elegivel`, base sem as duas execuções ou arquivo de sensibilidade ausente saem com DADOS,
sem gravar, nomeando o que falta.

#### Scenario: Amostra incompleta
- **WHEN** 4 das 53 linhas da amostra da Scopus estão classificadas
- **THEN** o comando sai com DADOS, informando 4 de 53 e remetendo à classificação

#### Scenario: Sonda não registrada
- **WHEN** a base não tem execução registrada da sonda
- **THEN** o comando sai com DADOS, nomeando a sonda e a base

### Requirement: Perda definida pela sonda e pela executada
O conjunto analisado SHALL ser o dos registros da sonda que a executada não traz, chaveados
como na sensibilidade. Cada registro da amostra SHALL ser casado com esse conjunto pela
chave; linha da amostra sem par sai com DADOS, sem gravar.

#### Scenario: Amostra da Scopus
- **WHEN** a amostra tem 53 linhas, todas classificadas, e a perda tem 949 registros
- **THEN** os 53 se casam com registros da exportação da sonda, com título, resumo e
  palavras-chave

### Requirement: Facetas reconhecidas na amostra
O comando SHALL relatar, para os elegíveis e para os não elegíveis da amostra, quantos
registros o casamento local reconhece em cada faceta, pelo vocabulário da base. Elegível
em que o casamento local reconhece faceta não âncora SHALL ser listado como divergência do
casamento local, com a chave e as facetas.

#### Scenario: Elegíveis sem faceta não âncora
- **WHEN** nenhum dos 30 elegíveis tem termo de FCT3 nem de FCT4 no título, no resumo ou nas
  palavras-chave
- **THEN** o relato traz zero elegíveis com FCT3 ou FCT4, e nenhuma divergência

#### Scenario: Divergência do casamento local
- **WHEN** um elegível da perda tem termo de FCT3 no resumo
- **THEN** ele é listado como divergência, com a chave e a faceta reconhecida

### Requirement: Termos candidatos
O comando SHALL listar como candidatos as palavras-chave, normalizadas, dos registros
elegíveis da amostra que nenhum termo do vocabulário da base reconhece. Para cada uma,
SHALL informar os elegíveis e os não elegíveis da amostra que ela alcança e os registros da
perda que acrescentaria à executada, em ordem decrescente de elegíveis e crescente de
acréscimo.

#### Scenario: Candidato da amostra
- **WHEN** `curriculum` é palavra-chave de 3 elegíveis, aparece no título, resumo ou
  palavras-chave de 4 elegíveis e de 1 não elegível, e de 60 registros da perda
- **THEN** a linha de `curriculum` traz 4 elegíveis, 1 não elegível e acréscimo de 60

#### Scenario: Palavra-chave já no vocabulário
- **WHEN** uma palavra-chave de elegível é reconhecida por termo de alguma faceta da base
- **THEN** ela não é candidata

#### Scenario: Registro sem palavras-chave
- **WHEN** elegíveis da amostra não têm palavras-chave na exportação
- **THEN** o relato informa quantos são, porque eles não contribuem candidatos

### Requirement: Candidatos gravados
O comando SHALL gravar `[saidas] candidatos` (`candidatos_<base>.csv`), com uma linha por
candidato: termo, elegíveis alcançados, não elegíveis alcançados e acréscimo. O arquivo é
saída regerável. O comando MUST NOT alterar protocolo, fonte, string nem planilha.

#### Scenario: Arquivo gravado
- **WHEN** a análise da Scopus termina
- **THEN** `data/candidatos_scopus.csv` tem uma linha por candidato, na ordem do relato

### Requirement: Simulação da executada ampliada
Com `--termo FCTn TERMO`, repetível, o comando SHALL simular a executada com os termos
acrescentados à faceta não âncora indicada, casando-os localmente nos registros da perda.
SHALL relatar, para o conjunto e para cada termo: elegíveis da amostra recuperados (com o
intervalo de Wilson), não elegíveis recuperados e registros acrescentados à executada.

#### Scenario: Conjunto de termos
- **WHEN** se executa `conferencia simular scopus --termo FCT3 curriculum --termo FCT3
  "learning system"`
- **THEN** o relato traz os elegíveis recuperados de 30, os não elegíveis de 23 e o total
  da executada ampliada (133 mais o acréscimo), para o conjunto e para cada termo

#### Scenario: Faceta âncora recusada
- **WHEN** se passa `--termo FCT1 ontology`
- **THEN** o comando sai com USO: a perda está dentro das âncoras da sonda, e ampliar âncora
  não se simula sobre ela

#### Scenario: Faceta inexistente
- **WHEN** se passa `--termo FCT9 x`
- **THEN** o comando sai com USO, nomeando as facetas não âncora do protocolo

### Requirement: Limites declarados no relato
O relato SHALL declarar que os números vêm do casamento local, que só aproxima a base, e
que a fração de elegíveis é medida na amostra, não no conjunto, e SHALL remeter à
conferência de fidelidade como a medida dessa aproximação.

#### Scenario: Relato com limites
- **WHEN** a análise da Scopus termina
- **THEN** o relato traz a aproximação do casamento local, o tamanho da amostra e a
  remissão a `conferencia fidelidade`

### Requirement: Autoteste prova a análise
O autoteste SHALL provar, com exportações sintéticas da executada e da sonda e uma amostra
classificada, o casamento da amostra, a exclusão de candidato já no vocabulário, a contagem
da simulação e a recusa por amostra incompleta.

#### Scenario: Candidato do vocabulário de volta
- **WHEN** a exclusão de palavra-chave já reconhecida pelo vocabulário é desligada
- **THEN** o autoteste falha no caso do candidato já no vocabulário

#### Scenario: Simulação fora da perda
- **WHEN** a simulação passa a contar registros da executada como acréscimo
- **THEN** o autoteste falha no caso da contagem da simulação
