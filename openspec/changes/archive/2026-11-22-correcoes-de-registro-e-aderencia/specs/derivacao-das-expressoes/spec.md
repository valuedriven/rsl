# Spec Delta

## ADDED Requirements

### Requirement: Regravação da planilha de aderência preserva o preenchimento manual
`sementes planilha` SHALL regravar `semente_aderencia.csv` conservando, em cada linha, as
colunas preenchidas à mão (`indexada`, `data_etapa1`, `recuperada`, `como_localizada`,
`data_etapa2` e `observacao`). A linha anterior casa com a nova por `id` e `base`, e só
casa se o título for o mesmo, sem distinguir acento nem caixa. As demais colunas MUST vir
sempre do arquivo de sementes e da tabela de bases.

#### Scenario: Preenchimento conservado
- **WHEN** a planilha traz `indexada = sim` e `observacao` preenchida na linha SE2 × wos,
  e `sementes planilha` é executado de novo, sem mudança no arquivo de sementes
- **THEN** a linha SE2 × wos sai com o mesmo `indexada` e a mesma `observacao`

#### Scenario: Coluna derivada atualizada
- **WHEN** o `tipo` de SE2 é preenchido no arquivo de sementes e a planilha já traz
  colunas manuais de SE2
- **THEN** a regravação traz o `tipo` novo e conserva as colunas manuais de SE2

#### Scenario: Primeira geração
- **WHEN** `semente_aderencia.csv` não existe
- **THEN** `sementes planilha` grava a planilha com as colunas manuais vazias

#### Scenario: Linha anterior sem preenchimento
- **WHEN** a planilha traz uma linha de semente ou de base que deixou de existir, com as
  colunas manuais vazias
- **THEN** a regravação omite essa linha e sai OK

### Requirement: Regravação recusada quando perderia preenchimento manual
`sementes planilha` MUST NOT gravar a planilha quando a regravação perderia conteúdo não
vazio da planilha anterior: coluna manual de linha sem par, de linha cujo título mudou, ou
de coluna fora do esquema. O subcomando SHALL sair com REPROVADO, nomeando cada `id`,
`base` e coluna afetados, e deixar o arquivo anterior intacto.

#### Scenario: Semente renumerada
- **WHEN** SE3 é retirada, SE4 passa a SE3, e a planilha traz `indexada` preenchida na
  linha SE3 × scopus com o título da semente retirada
- **THEN** `sementes planilha` sai com REPROVADO, nomeando SE3 × scopus e o título
  divergente, e `semente_aderencia.csv` não muda

#### Scenario: Semente retirada com preenchimento
- **WHEN** SE10 sai do arquivo de sementes e a planilha traz `recuperada` preenchida em
  SE10 × wos
- **THEN** `sementes planilha` sai com REPROVADO, nomeando SE10 × wos e a coluna
  `recuperada`, e `semente_aderencia.csv` não muda

#### Scenario: Coluna acrescentada à mão
- **WHEN** a planilha traz uma coluna fora do esquema com algum valor preenchido
- **THEN** `sementes planilha` sai com REPROVADO, nomeando a coluna, e
  `semente_aderencia.csv` não muda

#### Scenario: Planilha anterior ilegível
- **WHEN** `semente_aderencia.csv` existe e não é CSV legível
- **THEN** `sementes planilha` sai com DADOS, nomeando o arquivo, e não o regrava

### Requirement: Autoteste prova a preservação da planilha de aderência
O autoteste SHALL gerar a planilha num diretório temporário, preencher colunas manuais,
regravá-la e exigir que o preenchimento seja conservado. SHALL também exigir a recusa,
com o arquivo intacto, para semente renumerada e para linha sem par com preenchimento.
Os valores e os `id` usados MUST vir das sementes lidas, e não de literais.

#### Scenario: Regravação que apaga
- **WHEN** a regravação grava a planilha sem ler a anterior
- **THEN** o autoteste falha no caso de preservação

#### Scenario: Recusa ausente
- **WHEN** a regravação descarta a linha sem par com preenchimento
- **THEN** o autoteste falha no caso de recusa

### Requirement: Retorno declarado obrigatório no registro de execução
`busca registrar` SHALL exigir `--retorno` na validação de argumentos. Sem ele, o
subcomando MUST sair com USO antes de ler qualquer arquivo, e nada é registrado. A ajuda
(`-h`) SHALL apresentar `--retorno` como obrigatório.

#### Scenario: Sem retorno
- **WHEN** `busca registrar wos EB4 exportacao.txt` é executado sem `--retorno`
- **THEN** o subcomando sai com USO, nomeia `--retorno` como argumento exigido, e o
  registro de execução não muda

#### Scenario: Ajuda
- **WHEN** `busca registrar -h` é executado
- **THEN** a sinopse mostra `--retorno RETORNO` fora de colchetes

### Requirement: Registro de execução ausente remete à primeira execução registrada
Quando `[dados] registro` não existe, `pendencias` SHALL relatar a ausência e orientar o
registro da primeira execução com `busca registrar`. A orientação MUST NOT mandar
reconstituir o registro a partir das fichas ou da memória.

#### Scenario: Registro ausente
- **WHEN** `pendencias` é executado sem `registro_execucao.json`
- **THEN** a linha da ausência nomeia `busca registrar` e não contém "reconstitua"
