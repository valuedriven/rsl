# Spec Delta

## MODIFIED Requirements

### Requirement: Bases lidas da tabela do protocolo
As bases SHALL ser lidas da tabela "Bases de dados": identificador `BDn`, sigla e nome. Sigla
e identificador MUST ser únicos. A fonte do procedimento de busca de cada base SHALL ser
localizada pela sigla, no padrão `[documentos] procedimento_fonte` do `config.toml`. Fonte
inexistente MUST reprovar, nomeando a base e o caminho. O procedimento de busca gerado SHALL
ser gravado no padrão `[documentos] procedimento`. A ausência do procedimento gerado MUST
reprovar `documentos conferir` só naquela base, com `procedimentos gerar <sigla> --gravar`
como correção, e MUST NOT impedir a leitura da fonte.

#### Scenario: Procedimento de busca da sigla não existe
- **WHEN** o padrão é `docs/procedimentos/{sigla}` e não existe
  `docs/procedimentos/eric/procedimento.toml`
- **THEN** a leitura reprova, nomeando BD3, a sigla `eric` e o caminho procurado

#### Scenario: Procedimento ainda não gerado
- **WHEN** a fonte da ERIC existe e `docs/procedimentos_busca_eric.md` não existe
- **THEN** `documentos conferir` reprova só a ERIC, indicando `procedimentos gerar eric
  --gravar`

#### Scenario: Padrão sem a sigla
- **WHEN** `[documentos] procedimento` ou `[documentos] procedimento_fonte` não contém
  `{sigla}`
- **THEN** o script termina com erro de configuração que nomeia a chave

#### Scenario: Sigla repetida
- **WHEN** duas linhas da tabela têm a sigla `eric`
- **THEN** a leitura reprova, nomeando a sigla
