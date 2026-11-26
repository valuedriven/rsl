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
- conferência, opcionais: `verificacao`, `nota` e `veiculo_conferido`. O campo `nota`
  reúne o registro de conferência e o que a referência traz e não cabe em outro campo
  (editores, evento, local, editora).

Autoria, ano, título e DOI MUST ser lidos dos campos, sem extração por padrão de texto, e
nenhum outro arquivo SHALL guardar dado de semente.

#### Scenario: Arquivo atual
- **WHEN** o arquivo de sementes tem as 10 sementes de SE1 a SE10, com os campos do
  esquema estruturado
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

### Requirement: Arquivo de sementes fora do esquema reprova
Arquivo de sementes ausente MUST terminar com CONFIGURACAO, nomeando a chave e o caminho.
MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo: TOML inválido; campo
obrigatório ausente ou de tipo errado; campo desconhecido; `id` fora da forma `SEn`,
repetido ou fora da sequência a partir de SE1; `doi` fora da forma `10.x/…`; base fora da tabela de bases, com outra grafia ou
repetida; faceta fora da tabela de facetas ou repetida.

#### Scenario: Lacuna na numeração
- **WHEN** o arquivo tem SE1, SE2 e SE4, sem SE3
- **THEN** a leitura reprova, nomeando SE4 e o `id` esperado, SE3

#### Scenario: Papel fora do domínio
- **WHEN** uma semente traz `papel = "teste"`
- **THEN** a leitura reprova, nomeando a semente e o campo `papel` como desconhecido,
  porque o campo foi retirado do esquema

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Faceta inexistente
- **WHEN** a semente SE7 traz `facetas = ["FCT9"]` e a tabela de facetas vai até FCT4
- **THEN** a leitura reprova, nomeando SE7 e a faceta

#### Scenario: Campo desconhecido
- **WHEN** uma semente traz o campo `titlo`, o campo retirado `escopo`, os campos retirados
  `papel`, `tipo`, `alinhamento`, `eric` e `observacoes`, ou o campo `semente` do esquema
  intermediário
- **THEN** a leitura reprova, nomeando a semente e o campo

#### Scenario: Arquivo ausente
- **WHEN** `[documentos] sementes` aponta um arquivo que não existe
- **THEN** o subcomando termina com CONFIGURACAO, nomeando a chave e o caminho, e nenhuma
  semente é presumida

### Requirement: Dado ou juízo pendente relatado, sem reprovar
`projeto pendencias` SHALL relatar, nomeando a semente, sem reprovar a leitura:

- `doi` ausente;
- `facetas` vazia ou ausente;
- semente com `facetas` preenchida que não inclui nenhuma faceta marcada `Sim` na coluna
  "Âncora obrigatória" da tabela de facetas. O caso fica como pendência até o pesquisador
  decidir a regra. Com `facetas` vazia ou ausente, só se relata "facetas a informar": a
  falta de âncora decorre dela e não é relatada à parte.

#### Scenario: DOI a obter
- **WHEN** a semente SE6 não traz `doi`
- **THEN** a leitura aprova, e `projeto pendencias` relata SE6 com DOI ausente

#### Scenario: Facetas a informar
- **WHEN** a semente SE3 não traz `facetas`
- **THEN** a leitura aprova, e `projeto pendencias` relata SE3 com facetas a informar

#### Scenario: Validação sem âncora
- **WHEN** a semente SE5 traz `facetas = ["FCT3"]`, e FCT1 e FCT2 são as âncoras
- **THEN** a leitura aprova, e `projeto pendencias` relata SE5 sem faceta âncora

#### Scenario: Validação sem facetas
- **WHEN** a semente SE3 não traz `facetas`
- **THEN** `projeto pendencias` relata SE3 com facetas a informar, e não relata SE3 sem
  faceta âncora

## REMOVED Requirements

### Requirement: Conjunto de validação não vazio
**Reason**: A divisão entre sementes de validação e de desenvolvimento foi removida; todo o
conjunto é de validação, e o requisito perdeu o objeto.

**Migration**: Nenhuma ação sobre o arquivo de sementes. A conferência deixa de reprovar
por falta de semente de validação; conjunto vazio continua reprovando pela exigência de
tabela `[[sementes]]` não vazia.
