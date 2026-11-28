# Spec Delta

## ADDED Requirements

### Requirement: Leitura RIS do original e da reexportação do Zotero
O leitor de RIS SHALL ler pelos mesmos campos a exportação original da base e a reexportação
do Zotero. O BOM inicial MUST NOT esconder a primeira tag. `A1` SHALL contar como autor, e
`C3` como fonte. Só o primeiro `DO` de um registro SHALL valer. O tipo SHALL sair na forma
canônica, com `CONF` igual a `CPAPER` e o rótulo de capítulo da Scopus igual a `CHAP`.

#### Scenario: Arquivo com BOM
- **WHEN** a exportação começa com o BOM UTF-8 seguido de `TY  - JOUR`
- **THEN** o tipo do primeiro registro é `JOUR`

#### Scenario: Título dos anais reexportado pelo Zotero
- **WHEN** a reexportação traz `TY  - CONF` e `C3  - Anais`
- **THEN** a fonte do registro é `Anais` e o tipo é `CPAPER`

#### Scenario: Dois DOIs no registro
- **WHEN** um registro traz `DO  - 10.1/a.ch1` e `DO  - 10.1/a`
- **THEN** o DOI é `10.1/a.ch1`, e a chave de deduplicação é `doi:10.1/a.ch1`
