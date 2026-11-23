# Spec Delta

## MODIFIED Requirements

### Requirement: Nomes antigos em documento vivo
A conferência SHALL procurar nomes antigos de comandos e skills em documentos e skills
vivos e nas mensagens do código de `src/rsl/`, e MUST reprovar a citação.
`data/historico.md`, `openspec/changes/archive/`, a tabela de correspondência do catálogo e
os arquivos de código que guardam a correspondência de nomes ou exercitam os nomes antigos
no autoteste MUST ser isentos. Nome antigo composto (com espaço ou hífen) SHALL ser
reconhecido também sem prefixo, como numa mensagem do programa; nome de uma palavra só
SHALL exigir o prefixo `rsl ` ou a crase. A forma de flag da correspondência das specs
(`--conferir-dados`) e o nome de módulo (`gramatica.py`) MUST NOT ser tomados por citação
de alias.

#### Scenario: Skill cita comando antigo
- **WHEN** uma skill viva cita o nome antigo de um comando, mantido como alias, em vez do
  nome canônico
- **THEN** a conferência reprova, nomeando a skill e o comando antigo

#### Scenario: Histórico não é escaneado
- **WHEN** `data/historico.md` cita o nome antigo de um comando
- **THEN** a conferência não reprova por essa citação

#### Scenario: Mensagem do programa cita comando antigo
- **WHEN** uma mensagem em `src/rsl/` cita o nome antigo composto de um comando, mantido
  como alias, sem `rsl ` nem crase
- **THEN** a conferência reprova, nomeando o arquivo, a linha e o nome canônico

#### Scenario: Forma de flag e nome de módulo
- **WHEN** uma spec cita `--conferir-dados` ou um docstring cita `gramatica.py`
- **THEN** a conferência não reprova por essa citação
