# Spec Delta

## ADDED Requirements

### Requirement: Conferências leem a fonte
As conferências desta capacidade SHALL ler a estrutura derivada da fonte do procedimento da
base (`fonte-do-procedimento`), e não o markdown gerado, que se confere só por igualdade
(`geracao-dos-procedimentos`). O campo e o filtro de cada bloco SHALL vir de `[composicao]`
e de `[[criterios]]`, e MUST NOT ser reconhecidos pelo texto do bloco.

#### Scenario: Correspondência com a fonte
- **WHEN** a conferência examina o que antes lia nas seções 1, 2 e 3, nos blocos e na forma
  curada
- **THEN** lê, respectivamente, `[[sintaxe]]`, `[[criterios]]`, `[cobertura]` e
  `[[reducao]]`, os blocos compostos pelo gerador e `[[curadas]]`

#### Scenario: Campo declarado, não inferido
- **WHEN** a fonte da ERIC declara FCT1 no campo `title`
- **THEN** a conferência trata FCT1 da ERIC como campo `title`, sem ler o prefixo do bloco

#### Scenario: Invariante protege contra gerador errado
- **WHEN** o autoteste faz o compositor omitir um termo da STR3 no bloco de EB4 de uma base
- **THEN** a conferência "Termos do bloco conferem com as facetas declaradas" reprova só
  aquela base

## RENAMED Requirements

- FROM: `### Requirement: Termo só no singular relatado`
- TO: `### Requirement: Termo só no singular reprova`

## MODIFIED Requirements

### Requirement: Forma de execução declarada no procedimento de busca
A fonte do procedimento de cada base SHALL declarar a forma de execução em `[execucao]
forma`, com o valor `unica`, `particionada` ou `curada`. O campo ausente ou com outro valor
MUST reprovar a conferência daquela base, nomeando a fonte, e nenhum valor padrão é
presumido. O procedimento gerado SHALL trazer a linha `- Execução: <forma>` uma única vez.

#### Scenario: Procedimento de busca sem declaração
- **WHEN** `[execucao]` da fonte da ERIC não tem `forma`
- **THEN** a conferência da ERIC reprova, nomeando a fonte, e as demais bases não são
  afetadas

#### Scenario: Valor fora do domínio
- **WHEN** a fonte declara `forma = "dividida"`
- **THEN** a conferência daquela base reprova, nomeando o valor e os admitidos

### Requirement: Verificação por medição remete a execução registrada
Toda citação de execução ou de sondagem na fonte do procedimento SHALL ter a forma `BDn/<id>`
(no texto, `(BDn/<id>)`), com o `BDn` da própria base. Isso vale para os campos `citacao` e
para o texto dos fragmentos e dos demais campos. Também SHALL estar nessa forma toda menção
ao arquivo de registro de execução.

A conferência dos arquivos alimentados MUST reprovar, só naquela base, nomeando a fonte, o
campo ou a linha e a referência, nestes casos:
- falta o identificador;
- o `BDn` é de outra base;
- o `id` não existe em `bases.BDn.execucoes` nem em `bases.BDn.sondagens` do registro.

#### Scenario: Citação sem identificador de execução
- **WHEN** o elemento "`NEAR/x` entre grupos" da WoS tem `situacao = "medicao"` e
  `citacao = "BD1"`
- **THEN** `dados conferir` reprova a WoS, nomeando o elemento e a falta do identificador, e
  as demais bases não são afetadas

#### Scenario: Citação em prosa
- **WHEN** `notas_sintaxe.md` da BRAPCI diz "apurada por medição, com as sondagens em
  `data/registro_execucao.json` (BD4)"
- **THEN** `dados conferir` reprova a BRAPCI pela falta do identificador, e as demais bases
  não são afetadas

#### Scenario: Base trocada na citação
- **WHEN** um elemento de `[[sintaxe]]` da ERIC tem `citacao = "BD1/sonda-near"`
- **THEN** `dados conferir` reprova a ERIC, nomeando a citação de outra base

#### Scenario: Citação de sondagem registrada
- **WHEN** um elemento da WoS cita `BD1/sd1-2026-12-02` e o registro tem esse `id` em
  `bases.BD1.sondagens`
- **THEN** essa dimensão não reprova

#### Scenario: Execução citada inexistente
- **WHEN** a fonte da Scopus cita `BD2/sonda-w5` e o registro não tem esse `id` em BD2
- **THEN** `dados conferir` reprova a Scopus, nomeando a referência ausente

#### Scenario: Registro ausente
- **WHEN** a fonte cita uma execução e `data/registro_execucao.json` não existe
- **THEN** `dados conferir` reprova aquela base pela citação sem lastro, além de relatar o
  arquivo ausente

#### Scenario: Elemento não verificado
- **WHEN** o elemento tem `situacao = "nao_verificado"` e não cita o registro
- **THEN** essa dimensão não reprova

#### Scenario: Citação válida
- **WHEN** a fonte da WoS cita `BD1/sonda-near` e o registro tem esse `id` em
  `bases.BD1.execucoes`
- **THEN** essa dimensão não reprova

### Requirement: Critérios do procedimento de busca conferem com o protocolo
O conjunto dos IDs de `[[criterios]]` da fonte de cada base SHALL ser igual ao conjunto de
IDs da tabela de critérios do protocolo. Um ID que não existe no protocolo, ou um critério
do protocolo ausente da fonte, MUST reprovar só a conferência daquela base, nomeando a fonte
e o ID.

#### Scenario: Procedimento de busca cita critério inexistente
- **WHEN** o protocolo é renumerado e a fonte de uma base ainda cita o ID antigo
- **THEN** a conferência daquela base reprova, nomeando o ID citado como ausente do
  protocolo e o vigente como ausente da fonte; as demais bases, já corrigidas, não reprovam

#### Scenario: Critério agrupado numa linha
- **WHEN** uma linha de `[[criterios]]` tem `ids = ["CE1", "CE2"]`
- **THEN** os dois IDs contam como citados

#### Scenario: Procedimentos de busca em dia
- **WHEN** as quatro fontes citam exatamente os IDs do protocolo
- **THEN** essa dimensão não reprova nenhuma base

### Requirement: Teto de caracteres declarado por base
`[cobertura]` da fonte de cada base SHALL ter `teto`, com um número inteiro positivo de
caracteres ou `"nenhum"`. O campo ausente, ou com outro valor, MUST reprovar com
PROTOCOLO_ILEGIVEL, nomeando a fonte e o campo.

#### Scenario: Linha ausente
- **WHEN** `[cobertura]` da fonte da WoS não tem `teto`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a fonte e o campo

#### Scenario: Valor ilegível
- **WHEN** `teto = "curto"`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando o domínio do teto

### Requirement: Estratégia de proximidade não é forma executável
O fragmento `estrategia_de_proximidade.md` da fonte SHALL ser texto de discussão. Bloco
cercado nele não entra no derivado da base, não se executa e não se confere. O fragmento não
é exigido. O gerador o escreve na subseção `### Estratégia de proximidade` da seção 4.

#### Scenario: Bloco cercado na estratégia de proximidade
- **WHEN** a fonte da WoS ganha `estrategia_de_proximidade.md` com um bloco cercado
- **THEN** o derivado da WoS é igual ao de antes, e o procedimento ganha só a subseção

### Requirement: Plural declarado por base
`[cobertura] plural` da fonte de cada base SHALL ter uma destas formas:
- um valor único, `explícito` ou `pela lematização`, que vale para todos os idiomas da base;
- uma tabela por idioma, como `{ en = "pela lematização", pt = "explícito", es = "explícito" }`,
  cobrindo todos os idiomas que `[cobertura] idiomas` usa.

Os casos abaixo MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a fonte e o campo:
- o campo ausente;
- o valor fora do domínio;
- o idioma sem valor.

#### Scenario: Linha ausente
- **WHEN** `[cobertura]` da fonte da Scopus não tem `plural`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a fonte e o campo

#### Scenario: Valor fora do domínio
- **WHEN** `plural = "omitido"` na fonte da WoS
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, citando os dois valores admitidos

#### Scenario: Valor por idioma
- **WHEN** a fonte da WoS declara `plural = { en = "pela lematização", pt = "explícito", es = "explícito" }`
- **THEN** a flexão acrescenta plural só aos termos pt e es, e o en exige a lematização
  medida para en

#### Scenario: Idioma sem valor
- **WHEN** a base usa pt, en e es, e `plural` traz só en e pt
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando `es`

### Requirement: Plural pela lematização exige lematização medida
Para cada idioma com `pela lematização`, a fonte SHALL ter um elemento de `[[sintaxe]]` de
`categoria = "lematizacao"` com `situacao = "medicao"` e `citacao` de execução ou sondagem
registrada daquela base. O elemento com `idioma` vale para esse idioma; o elemento sem
`idioma` vale para todos. A conferência MUST reprovar só aquela base quando, para o idioma,
não há elemento medido com citação.

#### Scenario: Lematização não verificada
- **WHEN** a fonte da ERIC declara `plural = "pela lematização"` e o único elemento de
  `lematizacao` é `nao_verificado`
- **THEN** `documentos conferir` reprova a ERIC, nomeando a declaração e o elemento sem
  medição; as demais bases não são afetadas

#### Scenario: Lematização medida
- **WHEN** a fonte declara `plural = "pela lematização"` e o elemento de `lematizacao`, sem
  `idioma`, é `medicao` com `citacao = "BD3/sonda-plural"`
- **THEN** essa dimensão não reprova em `documentos conferir`, porque a medição vale para
  todos os idiomas, e a existência de `BD3/sonda-plural` é conferida por `dados conferir`

#### Scenario: Lematização medida num idioma só
- **WHEN** a fonte da WoS declara en `pela lematização`, e o elemento de `lematizacao` com
  `idioma = "en"` é `medicao` com `citacao = "BD1/sd5-2026-12-02"`
- **THEN** essa dimensão não reprova em `documentos conferir`, e a existência da citação é
  conferida por `dados conferir`

#### Scenario: Plural explícito
- **WHEN** a fonte declara `plural = "explícito"`
- **THEN** a situação dos elementos de `lematizacao` não reprova

### Requirement: Termo só no singular reprova
Em idioma com plural explícito, a conferência MUST reprovar, por base, o termo da STR
presente nos blocos da base numa só forma de número. A reprovação nomeia a faceta, o termo e
o idioma, e não vale quando:
- o termo é `nao_contavel` no arquivo de exceções (`flexao-dos-termos`);
- o termo tem forma `vetada` no arquivo de exceções;
- um truncamento declarado na fonte alcança o termo.

A regra vale também para a forma curada e para os subconjuntos, que são as partes da fonte
onde se escrevem termos à mão.

#### Scenario: Plural esquecido
- **WHEN** a ERIC declara plural explícito em en, e o subconjunto `STR1b` da fonte traz
  `metadata schema` sem `metadata schemas` e sem exceção
- **THEN** `documentos conferir` reprova a ERIC, nomeando `metadata schema`, FCT1 e en; as
  demais bases passam

#### Scenario: Plural esquecido na forma curada
- **WHEN** uma consulta de `[[curadas]]` da fonte traz `"teaching strategy"` sem `"teaching
  strategies"` e sem exceção, e a base declara plural explícito em en
- **THEN** `documentos conferir` reprova a base, nomeando `teaching strategy`, FCT3 e en;
  as demais bases passam

#### Scenario: Não contável
- **WHEN** o bloco traz `"education"` só no singular e o arquivo de exceções declara
  `education`, en, `nao_contavel`
- **THEN** essa dimensão não reprova
