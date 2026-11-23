# Spec Delta

## ADDED Requirements

### Requirement: Catálogo sem correspondência de nomes
O catálogo MUST NOT trazer tabela de correspondência entre nomes antigos e canônicos, nem no
arquivo gravado nem na saída `--json`. A conferência MUST NOT ter regra de nome antigo:
depois da remoção dos aliases, o catálogo não guarda lista de nomes antigos de comando, de
skill ou de chave de configuração.

#### Scenario: Catálogo gravado
- **WHEN** se executa `python3 -m rsl catalogo gerar --gravar`
- **THEN** `docs/catalogo_de_apoio.md` não tem a seção "Correspondência de nomes"

#### Scenario: Saída JSON
- **WHEN** se executa `python3 -m rsl catalogo gerar --json`
- **THEN** a saída não tem o campo `correspondencia`

## REMOVED Requirements

### Requirement: Nomes antigos em documento vivo
**Reason**: Decisão do pesquisador nesta change: a varredura de nome antigo, a tabela de
correspondência e o registro de skills renomeadas saem junto com os aliases, em vez de
ficarem como proteção contra regressão.
**Migration**: Nenhuma no uso. O nome antigo de comando passa a ser recusado com USO, e
a chave antiga com CONFIGURACAO (requisito "Nomes antigos recusados" de
`interface-de-comando`). Comando citado no guia continua conferido pela existência no
parser. Fora do guia, nada impede de forma automática que um documento volte a citar um
nome antigo de comando ou de skill.
