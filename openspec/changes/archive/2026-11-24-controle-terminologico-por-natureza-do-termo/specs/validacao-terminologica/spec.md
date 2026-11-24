## ADDED Requirements

### Requirement: Domínio da decisão do ReT
A coluna `decisao_ReT` da planilha de validação SHALL admitir só `descritor`, `sinônimo ou
relacionado`, `termo livre` ou vazio, sem distinção de caixa. O vazio significa "sem
decisão". Valor fora do domínio MUST reprovar em `termos importar` e em `documentos
conferir`, nomeando o termo, a faceta, o idioma, o instrumento e o valor.

#### Scenario: Valor fora do domínio
- **WHEN** a planilha traz `decisao_ReT = autorizado` para `ontology` (FCT1, en, unesco)
- **THEN** `termos importar` reprova, nomeando o termo, o instrumento e os valores admitidos

#### Scenario: Caixa diferente
- **WHEN** a planilha traz `decisao_ReT = Descritor`
- **THEN** o valor é lido como `descritor`

### Requirement: Linha do termo resulta da decisão do ReT
A linha esperada de um termo no CT SHALL ser calculada sobre as decisões do ReT desse termo,
na faceta e no idioma dele, nos instrumentos planejados para ele: `descritores`, se alguma
decisão for `descritor`; senão `relacionados`, se alguma for `sinônimo ou relacionado`;
senão `livre`. `status_proposto` MUST NOT entrar no cálculo.

#### Scenario: Descritor em um instrumento
- **WHEN** `ontology` (FCT1, en) é `descritor` na UNESCO e `termo livre` no ERIC
- **THEN** a linha esperada é "Descritores correspondentes"

#### Scenario: Equivalente sem descritor
- **WHEN** `thesauri` (FCT1, en) é `sinônimo ou relacionado` na UNESCO e não tem outra decisão
- **THEN** a linha esperada é "Termos sinônimos ou relacionados"

#### Scenario: Instrumento manual pendente
- **WHEN** `learning context` (FCT4, en) está pendente de validação manual no ERIC e não tem
  decisão em outro instrumento
- **THEN** a linha esperada é "Termo livre"

#### Scenario: Proposta da máquina sem decisão
- **WHEN** `ontology` tem `status_proposto` de descritor autorizado na UNESCO e `decisao_ReT`
  vazia
- **THEN** a linha esperada é "Termo livre"

#### Scenario: Planilha ausente
- **WHEN** a planilha de validação não existe
- **THEN** a linha esperada de todo termo é "Termo livre"

### Requirement: Autoteste prova o domínio e a regra da linha
O autoteste SHALL verificar, sobre planilhas em memória, o domínio de `decisao_ReT` e a
regra da linha esperada: precedência de `descritor` sobre `sinônimo ou relacionado`,
pendência manual e proposta da máquina levando a `livre`, e valor fora do domínio
reprovado. Caso não verificado MUST fazer o autoteste falhar.

#### Scenario: Precedência invertida
- **WHEN** o autoteste dá a um termo `sinônimo ou relacionado` num instrumento e `descritor`
  noutro, e a linha calculada não é `descritores`
- **THEN** o autoteste falha, nomeando o caso
