# Spec Delta

## MODIFIED Requirements

### Requirement: Conjunto-semente lido do arquivo de sementes
O conjunto-semente SHALL ser lido do arquivo TOML localizado por `[documentos] sementes`,
uma tabela `[[sementes]]` por estudo, com os campos do esquema estruturado declarado na
gramática:

- bibliográficos: `id` (`SEn`, único), `autores` (lista não vazia), `ano` (inteiro),
  `titulo`, `veiculo`, e os opcionais `volume`, `numero`, `paginas` e `doi`;
- aferição: `bases` (siglas que indexam a semente), `facetas` (opcional, `FCTn` informadas
  pelo pesquisador) e `papel`;
- conferência, opcionais: `verificacao`, `tipo`, `alinhamento`, `nota`,
  `veiculo_conferido` e `eric`;
- `observacoes`, opcional: o que a referência traz e não cabe em outro campo.

Autoria, ano, título e DOI MUST ser lidos dos campos, sem extração por padrão de texto, e
nenhum outro arquivo SHALL guardar dado de semente.

#### Scenario: Título com ponto
- **WHEN** o `titulo` de uma semente contém um ponto seguido de maiúscula
- **THEN** o título lido é o campo inteiro

#### Scenario: Semente sem DOI
- **WHEN** uma semente não tem `doi`
- **THEN** a leitura aprova, e `pendencias` relata o DOI ausente

#### Scenario: Lacuna na numeração
- **WHEN** o arquivo tem SE1, SE2 e SE4, sem SE3
- **THEN** a leitura aprova

#### Scenario: Distribuição calculada
- **WHEN** o arquivo é lido
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas do campo `bases`, e a distribuição por papel, do campo `papel`

### Requirement: Arquivo de sementes fora do esquema reprova
Arquivo de sementes ausente MUST terminar com CONFIGURACAO, nomeando a chave e o caminho.
MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo: TOML inválido; campo
obrigatório ausente ou de tipo errado; campo desconhecido; `id` fora da forma `SEn` ou
repetido; `doi` fora da forma `10.x/…`; base fora da tabela de bases, com outra grafia ou
repetida; faceta fora da tabela de facetas ou repetida; `papel` fora do domínio.

#### Scenario: Papel fora do domínio
- **WHEN** uma semente traz `papel = "teste"`
- **THEN** a leitura reprova, nomeando a semente e os valores admitidos

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Faceta inexistente
- **WHEN** a semente SE7 traz `facetas = ["FCT9"]` e a tabela de facetas vai até FCT4
- **THEN** a leitura reprova, nomeando SE7 e a faceta

#### Scenario: Campo desconhecido
- **WHEN** uma semente traz o campo `titlo`, o campo retirado `escopo` ou o campo
  `semente` do esquema intermediário
- **THEN** a leitura reprova, nomeando a semente e o campo

#### Scenario: Arquivo ausente
- **WHEN** `[documentos] sementes` aponta um arquivo que não existe
- **THEN** o subcomando termina com CONFIGURACAO, nomeando a chave e o caminho, e nenhuma
  semente é presumida

## ADDED Requirements

### Requirement: Juízo pendente relatado, sem reprovar
`pendencias` SHALL relatar, nomeando a semente, sem reprovar a leitura:

- `facetas` vazia ou ausente;
- semente de validação cujas `facetas` não incluem nenhuma faceta marcada `Sim` na coluna
  "Âncora obrigatória" da tabela de facetas. O caso fica como pendência até o pesquisador
  decidir a regra;
- `tipo` ou `alinhamento` vazios.

#### Scenario: Facetas a informar
- **WHEN** a semente SE3 não traz `facetas`
- **THEN** a leitura aprova, e `pendencias` relata SE3 com facetas a informar

#### Scenario: Validação sem âncora
- **WHEN** a semente de validação SE5 traz `facetas = ["FCT3"]`, e FCT1 e FCT2 são as
  âncoras
- **THEN** a leitura aprova, e `pendencias` relata SE5 sem faceta âncora

### Requirement: Semente retirada não deixa resto
Semente retirada SHALL sair do arquivo, das saídas regeneradas e da evidência bruta.
`conferir-dados` MUST reprovar arquivo de `data/evidencia/referencias/` nomeado com um
`SEn` que não está no arquivo de sementes, nomeando o arquivo.

#### Scenario: Evidência de semente retirada
- **WHEN** SE10 é retirada do arquivo e `SE10_crossref.json` continua em
  `data/evidencia/referencias/`
- **THEN** `conferir-dados` reprova, nomeando `SE10_crossref.json`

#### Scenario: Planilha regenerada
- **WHEN** SE10 é retirada e `sementes planilha` é executado
- **THEN** `semente_aderencia.csv` não traz linha de SE10

### Requirement: Referência exibida a partir dos campos
`mostrar` SHALL exibir cada semente como referência legível, montada dos campos na ordem
autores, ano, título, veículo, volume, número, páginas e DOI, omitindo o campo vazio. A
referência exibida MUST NOT ser gravada em arquivo nem no protocolo.

#### Scenario: Campo opcional vazio
- **WHEN** uma semente não tem `paginas`
- **THEN** a referência exibida não traz marcador de páginas

### Requirement: Autoteste prova a reprovação do esquema estruturado
O autoteste SHALL injetar numa cópia do arquivo de sementes, a partir das sementes lidas,
cada um destes defeitos e exigir PROTOCOLO_ILEGIVEL: `ano` como texto, `autores` vazia,
`doi` fora da forma, faceta fora da tabela, faceta repetida e o campo `semente` do esquema
intermediário. O autoteste SHALL também exigir que `conferir-dados` reprove a evidência de
semente inexistente.

#### Scenario: Defeito não detectado
- **WHEN** a cópia com o campo `semente` é aprovada
- **THEN** o autoteste falha, nomeando o defeito
