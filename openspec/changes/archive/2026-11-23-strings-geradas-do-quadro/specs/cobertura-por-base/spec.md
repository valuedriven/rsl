# Spec Delta

## MODIFIED Requirements

### Requirement: Termo da base deriva da STR
Todo termo da string de uma base SHALL corresponder, em flexão ou pela derivação declarada, a
um termo da STR da mesma faceta, ou ser termo do quadro dessa faceta subsumido por um termo
da STR, na regra de `geracao-das-strings`. Termo que só exista no quadro sem estar subsumido,
ou que não exista em lugar nenhum, MUST reprovar. O subsumido aceito SHALL ser relatado por
base, sem reprovar.

#### Scenario: Termo retirado devolvido à base
- **WHEN** a ficha usa, mesmo em flexão, um termo que está no quadro, não está na STR e não
  é subsumido por termo da STR
- **THEN** a conferência daquela base reprova, dizendo que o termo não está na string do
  protocolo

#### Scenario: Termo inventado
- **WHEN** a ficha usa um termo que não deriva de nenhum termo do protocolo
- **THEN** a conferência daquela base reprova, nomeando o termo

#### Scenario: Subsumido em campo próprio
- **WHEN** a ficha da ERIC usa `"ontology engineering"` no resumo (`STR1b`), e a STR1 tem
  `ontology` e não tem `ontology engineering`, que está no quadro de FCT1
- **THEN** a conferência da ERIC não reprova por esse termo, e o relata como subsumido por
  `ontology`

## ADDED Requirements

### Requirement: Plural declarado por base
A declaração de cobertura de cada ficha SHALL ter a linha `plural`, com o valor `explícito`
ou `pela lematização`. A linha ausente, ou com outro valor, MUST reprovar com
PROTOCOLO_ILEGIVEL.

#### Scenario: Linha ausente
- **WHEN** a declaração de cobertura da ficha da Scopus não tem a linha `plural`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a ficha e a linha

#### Scenario: Valor fora do domínio
- **WHEN** a linha `plural` da ficha da WoS diz `omitido`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, citando os dois valores admitidos

### Requirement: Plural pela lematização exige lematização medida
Ficha que declara `plural: pela lematização` SHALL ter, na seção 1, a linha "Lematização"
com o estado verificado por medição e a citação `(BDn/<id>)` de uma execução registrada
daquela base. A conferência MUST reprovar só aquela base quando a linha falta, quando o
estado não é verificado ou quando a citação falta.

#### Scenario: Lematização não verificada
- **WHEN** a ficha da ERIC declara `plural: pela lematização` e a seção 1 diz "Lematização —
  **Não verificado**"
- **THEN** `--conferir` reprova a ERIC, nomeando a declaração e a linha sem medição; as
  demais bases não são afetadas

#### Scenario: Lematização medida
- **WHEN** a ficha declara `plural: pela lematização` e a linha "Lematização" diz
  verificado por medição com `(BD3/sonda-plural)`
- **THEN** essa dimensão não reprova em `--conferir`, e a existência de `BD3/sonda-plural`
  é conferida por `--conferir-dados`, como em "Verificação por medição remete a execução
  registrada"

#### Scenario: Plural explícito
- **WHEN** a ficha declara `plural: explícito`
- **THEN** o estado da linha "Lematização" não reprova

### Requirement: Termo só no singular relatado
Em ficha com `plural: explícito`, a conferência SHALL relatar, por faceta e sem reprovar, os
termos da STR presentes na string da base em uma só forma de número e não alcançados por
truncamento.

#### Scenario: Plural esquecido
- **WHEN** a ficha da Scopus declara `plural: explícito` e traz `"teaching strategy"` sem
  `"teaching strategies"` nem truncamento que o alcance
- **THEN** `--conferir` relata `teaching strategy` em FCT3 da Scopus, e o código não muda
  por esse relato

### Requirement: Autoteste prova a reprovação do plural sem lastro
O autoteste SHALL injetar, na cópia da ficha de uma só base, a declaração `plural: pela
lematização` com a linha "Lematização" não verificada, e exigir que só aquela base reprove;
e SHALL retirar a linha `plural` e exigir PROTOCOLO_ILEGIVEL.

#### Scenario: Defeito injetado numa base
- **WHEN** o autoteste injeta `plural: pela lematização` na ficha da WoS, com a lematização
  não verificada
- **THEN** a conferência da WoS reprova, as demais não reprovam, e o autoteste falha se
  isso não ocorrer

### Requirement: Teto de caracteres declarado por base
A declaração de cobertura de cada ficha SHALL ter a linha `teto de caracteres`, com um
número inteiro positivo de caracteres (`1400` ou `1.400`) ou `nenhum`. A linha ausente, ou
com outro valor, MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a ficha e a linha.

#### Scenario: Linha ausente
- **WHEN** a declaração de cobertura da ficha da WoS não tem a linha `teto de caracteres`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a ficha e a linha

#### Scenario: Valor ilegível
- **WHEN** a linha `teto de caracteres` da ficha diz `curto`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando o domínio do teto

### Requirement: Consulta acima do teto reprova a base
Com teto numérico, a conferência SHALL medir o comprimento, em caracteres, de cada consulta
executável da base e MUST reprovar só aquela base quando alguma passar do teto, nomeando a
expressão, a consulta, o comprimento e o teto. Consulta executável é cada bloco das
expressões da seção 4, salvo a forma longa e o bloco rotulado como não executado, e cada
consulta da forma curada. Com `nenhum`, a conferência SHALL relatar, sem reprovar, a maior
consulta executável da base.

#### Scenario: Consulta acima do teto
- **WHEN** a ficha da ERIC declara `teto de caracteres | 1400` e a consulta 4a2 tem 1.450
  caracteres
- **THEN** `conferir` reprova a ERIC, nomeando EB4, a consulta 4a2, 1450 e 1400; as demais
  bases não são afetadas

#### Scenario: Consulta no limite
- **WHEN** a maior consulta da base tem exatamente o comprimento do teto declarado
- **THEN** essa dimensão não reprova

#### Scenario: Sem teto
- **WHEN** a ficha da Scopus declara `teto de caracteres | nenhum`
- **THEN** `conferir` relata a maior consulta da Scopus com o comprimento, e o código não
  muda por esse relato

### Requirement: Estratégia de proximidade não é forma executável
A subseção `### Estratégia de proximidade` da seção 4 da ficha SHALL ser ignorada pela
leitura: bloco cercado nela não entra no derivado da base, não se executa e não se confere.
A subseção não é exigida.

#### Scenario: Bloco cercado na estratégia de proximidade
- **WHEN** a ficha da WoS ganha uma subseção "Estratégia de proximidade" com um bloco
  cercado
- **THEN** o derivado da WoS é igual ao de antes e `conferir` não muda o código

### Requirement: Autoteste prova o teto e a estratégia de proximidade
O autoteste SHALL:
- declarar, na cópia da ficha de uma só base, um teto uma unidade abaixo da maior consulta
  e exigir que só aquela base reprove;
- declarar o teto igual à maior consulta, com separador de milhar, e exigir que passe;
- retirar a linha `teto de caracteres` e exigir PROTOCOLO_ILEGIVEL;
- deformar o valor do teto e exigir PROTOCOLO_ILEGIVEL;
- inserir a subseção de estratégia de proximidade com bloco cercado e exigir o derivado
  inalterado.

#### Scenario: Conferência desligada
- **WHEN** a conferência do comprimento contra o teto é desligada
- **THEN** o caso do teto abaixo da maior consulta falha
