# Spec Delta

## MODIFIED Requirements

### Requirement: Conjunto-semente lido do arquivo de sementes
O conjunto-semente SHALL ser lido do arquivo TOML localizado por `[documentos] sementes`,
uma tabela `[[sementes]]` por estudo, com os campos do esquema estruturado declarado na
gramática:

- bibliográficos: `id` (`SEn`, único e em sequência a partir de SE1), `autores` (lista não vazia), `ano` (inteiro),
  `titulo`, `veiculo`, e os opcionais `volume`, `numero`, `paginas` e `doi`;
- aferição: `bases` (siglas que indexam a semente) e `facetas` (opcional, `FCTn` informadas
  pelo pesquisador);
- conferência, opcionais: `verificacao`, `nota` e `veiculo_conferido`. `verificacao` é
  booleano: `true` quando os dados bibliográficos foram conferidos; `false` ou ausente é
  conferência pendente; texto ou outro tipo MUST reprovar a leitura. O campo `nota`
  reúne o registro de conferência, com onde e como se conferiu, e o que a referência traz
  e não cabe em outro campo (editores, evento, local, editora).

Autoria, ano, título e DOI MUST ser lidos dos campos, sem extração por padrão de texto, e
nenhum outro arquivo SHALL guardar dado de semente.

#### Scenario: Arquivo atual
- **WHEN** o arquivo de sementes vigente tem as sementes do esquema estruturado, em
  sequência a partir de SE1
- **THEN** a leitura aprova, e a distribuição por base exibida por `configuracao mostrar` é
  a mesma exibida antes da troca do esquema intermediário pelo estruturado

#### Scenario: Título com ponto
- **WHEN** o `titulo` de uma semente contém um ponto seguido de maiúscula
- **THEN** o título lido é o campo inteiro

#### Scenario: Semente sem DOI
- **WHEN** uma semente não tem `doi`
- **THEN** a leitura aprova, e `projeto pendencias` relata o DOI ausente

#### Scenario: Distribuição calculada
- **WHEN** o arquivo é lido
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas do campo `bases`

#### Scenario: Verificação como texto
- **WHEN** uma semente traz `verificacao = "CONFIRMADA"`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo

#### Scenario: Verificação pendente
- **WHEN** uma semente traz `verificacao = false` ou não traz o campo
- **THEN** a leitura aprova, `projeto pendencias` relata a verificação pendente e a planilha
  de aderência mostra `não` na coluna `verificacao`

#### Scenario: Verificação conferida
- **WHEN** uma semente traz `verificacao = true`
- **THEN** `projeto pendencias` não relata verificação pendente para ela, e a planilha
  mostra `sim`
