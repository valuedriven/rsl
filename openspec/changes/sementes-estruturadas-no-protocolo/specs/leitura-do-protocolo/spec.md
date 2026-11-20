# Spec Delta

## REMOVED Requirements

### Requirement: Conjunto-semente lido de tabela
**Reason**: Com a referência em texto livre, a extração de título e DOI depende de
expressão regular e pode ler errado sem reprovar. Os metadados de conferência ficavam em
`data/sementes.json`, ligados por DOI ou título extraído. Por decisão do pesquisador
(2026-11-19 e 2026-11-20), o conjunto-semente passa a um arquivo TOML próprio, apontado
pelo protocolo e com os dados de conferência.

**Migration**: Transcrever cada linha da tabela, campo a campo, para uma tabela
`[[semente]]` de `docs/conjunto_semente.toml`, sem completar dado de memória. Copiar de
`sementes.json` os dados de conferência, exceto `escopo`. Ver "Conjunto-semente lido do
arquivo apontado".

## MODIFIED Requirements

### Requirement: Conferência verifica coerência interna
`--conferir` SHALL reprovar contradições internas: termo de STR ausente do quadro da faceta;
expressão sem as âncoras; executada que não seja a união das específicas; sonda que não seja a
conjunção das âncoras; semente sem base ou com base fora da tabela de bases; dimensão de
critério em uso não declarada no protocolo; faixa de sensibilidade com inferior ≥ superior.

#### Scenario: Termo da string fora do quadro
- **WHEN** uma STR contém um termo que não consta do quadro da sua faceta
- **THEN** `--conferir` reprova, nomeando a faceta e o termo

#### Scenario: Dimensão de critério com grafia do protocolo
- **WHEN** a lista de dimensões em uso tem "Idioma" e o protocolo declara CE3 com "Idioma"
- **THEN** `--conferir` não reprova por dimensão de critério

#### Scenario: Distribuição das sementes não é declarada em prosa
- **WHEN** o conjunto-semente está só no arquivo apontado, sem parágrafo de incidências no
  protocolo
- **THEN** `--conferir` não reprova por distribuição; a distribuição por base é calculada do
  campo `bases` do arquivo e exibida

## ADDED Requirements

### Requirement: Conjunto-semente lido do arquivo apontado
O conjunto-semente SHALL ser lido do arquivo TOML apontado pela seção "Conjunto-semente"
do protocolo, com uma tabela `[[semente]]` por estudo. Os campos são:

| Campo | Tipo | Exigência |
| --- | --- | --- |
| `id` | texto `SEn` | obrigatório, único |
| `autores` | lista de texto | obrigatória, não vazia |
| `ano` | inteiro | obrigatório |
| `titulo` | texto | obrigatório |
| `veiculo` | texto | obrigatório |
| `volume`, `numero`, `paginas` | texto | opcionais |
| `doi` | texto `10.x/…`, sem prefixo `https://doi.org/` | opcional |
| `bases` | lista de siglas da tabela de bases: bases que indexam a semente | obrigatória, não vazia |
| `facetas` | lista de `FCTn` da tabela de facetas, informada pelo pesquisador | opcional |
| `papel` | `desenvolvimento` ou `validação` | obrigatório |
| `verificacao`, `tipo`, `alinhamento`, `nota`, `veiculo_conferido`, `eric` | texto | opcionais |
| `observacoes` | texto: o que a referência traz e não cabe em outro campo | opcional |

Autoria, ano, título e DOI MUST ser lidos dos campos, sem extração por padrão de texto.
Os valores são lidos como estão, sem correção nem complemento. Nenhum outro arquivo SHALL
guardar dado de semente.

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

### Requirement: Arquivo do conjunto-semente reprova fora do esquema
A leitura SHALL reprovar com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo quando
houver, nestes casos:

- apontamento ausente ou duplicado na seção;
- arquivo apontado inexistente;
- TOML inválido;
- campo obrigatório ausente;
- campo com tipo errado;
- campo desconhecido;
- `id` fora da forma `SEn` ou repetido;
- `doi` fora da forma `10.x/…`;
- base que não seja sigla da tabela de bases, na grafia exata, ou repetida;
- faceta que não seja `FCTn` da tabela de facetas, ou repetida;
- `papel` fora do domínio.

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
- **WHEN** uma semente traz o campo `titlo`, ou o campo retirado `escopo`
- **THEN** a leitura reprova, nomeando a semente e o campo

#### Scenario: Arquivo ausente
- **WHEN** o protocolo aponta `docs/conjunto_semente.toml` e o arquivo não existe
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando o caminho, e nenhuma semente
  é presumida

### Requirement: Juízo pendente relatado, sem reprovar
`pendencias` SHALL relatar, nomeando a semente, sem reprovar a leitura:

- `facetas` vazia ou ausente;
- semente de validação cujas `facetas` não incluem nenhuma faceta marcada como âncora
  obrigatória na tabela de facetas. O caso fica como pendência até o pesquisador decidir
  a regra;
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
`SEn` que não está no arquivo do conjunto-semente, nomeando o arquivo.

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

### Requirement: Autoteste prova a reprovação do arquivo
O autoteste SHALL injetar numa cópia, a partir das sementes lidas, cada um destes
defeitos e exigir PROTOCOLO_ILEGIVEL:

- apontamento retirado;
- apontamento duplicado;
- arquivo apontado inexistente;
- TOML quebrado;
- campo obrigatório retirado;
- campo desconhecido;
- `ano` como texto;
- base fora da tabela;
- faceta fora da tabela;
- `id` repetido;
- `papel` fora do domínio.

O autoteste SHALL também exigir que `conferir-dados` reprove a evidência de semente
inexistente.

#### Scenario: Defeito não detectado
- **WHEN** a cópia com campo desconhecido é aprovada
- **THEN** o autoteste falha, nomeando o defeito
