# Spec Delta

## REMOVED Requirements

### Requirement: Conjunto-semente lido de tabela
**Reason**: Com a referência em texto livre, a extração de título e DOI depende de
expressão regular e pode ler errado sem reprovar. O conjunto-semente passa a um bloco
TOML com campos separados, por decisão do pesquisador (2026-11-19).

**Migration**: Transcrever cada linha da tabela para uma tabela `[[semente]]` do bloco,
campo a campo, sem completar dado de memória. Ver "Conjunto-semente lido de bloco TOML".

## ADDED Requirements

### Requirement: Conjunto-semente lido de bloco TOML
O conjunto-semente SHALL ser lido do único bloco cercado ```` ```toml ```` da seção
"Conjunto-semente", com uma tabela `[[semente]]` por estudo. Os campos são:

| Campo | Tipo | Exigência |
| --- | --- | --- |
| `id` | texto `SEn` | obrigatório |
| `autores` | lista de texto | obrigatória, não vazia |
| `ano` | inteiro | obrigatório |
| `titulo` | texto | obrigatório |
| `veiculo` | texto | obrigatório |
| `volume`, `numero`, `paginas` | texto | opcionais |
| `doi` | texto `10.x/…`, sem prefixo `https://doi.org/` | opcional |
| `bases` | lista de siglas | obrigatória, não vazia |
| `papel` | `desenvolvimento` ou `validação` | obrigatório |

Autoria, ano, título e DOI MUST ser lidos dos campos, sem extração por padrão de texto.
Os valores são lidos como estão, sem correção nem complemento.

#### Scenario: Título com ponto
- **WHEN** o `titulo` de uma semente contém um ponto seguido de maiúscula
- **THEN** o título lido é o campo inteiro

#### Scenario: Semente sem DOI
- **WHEN** uma semente não tem `doi`
- **THEN** a leitura aprova, a ligação com `sementes.json` usa o título, e `pendencias`
  relata o DOI ausente

### Requirement: Bloco do conjunto-semente reprova fora do esquema
A leitura SHALL reprovar com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo quando
houver, nestes casos:

- bloco ausente ou duplicado;
- TOML inválido;
- campo obrigatório ausente;
- campo com tipo errado;
- campo desconhecido;
- `id` fora da forma `SEn` ou fora da sequência a partir de SE1;
- `doi` fora da forma `10.x/…`.

Base que não seja sigla da tabela de bases, na grafia exata, ou base repetida também
reprova. Também reprovam o `papel` fora do domínio e o conjunto sem nenhuma semente de
validação.

#### Scenario: Papel fora do domínio
- **WHEN** uma semente traz `papel = "teste"`
- **THEN** a leitura reprova, nomeando a semente e os valores admitidos

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Campo desconhecido
- **WHEN** uma semente traz o campo `titlo`
- **THEN** a leitura reprova, nomeando a semente e o campo

#### Scenario: Bloco perdido na exportação
- **WHEN** a seção "Conjunto-semente" não tem bloco ```` ```toml ````, por exemplo porque a
  exportação de um editor o converteu em parágrafo
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a seção, e nenhuma semente é
  presumida

#### Scenario: Distribuição calculada
- **WHEN** o bloco é lido
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas do campo `bases`

### Requirement: Referência exibida a partir dos campos
`mostrar` SHALL exibir cada semente como referência legível, montada dos campos na ordem
autores, ano, título, veículo, volume, número, páginas e DOI, omitindo o campo vazio. A
referência exibida MUST NOT ser gravada em arquivo nem no protocolo.

#### Scenario: Campo opcional vazio
- **WHEN** uma semente não tem `paginas`
- **THEN** a referência exibida não traz marcador de páginas

### Requirement: Autoteste prova a reprovação do bloco
O autoteste SHALL injetar numa cópia, a partir das sementes lidas, cada um destes
defeitos e exigir PROTOCOLO_ILEGIVEL:

- bloco retirado;
- bloco duplicado;
- TOML quebrado;
- campo obrigatório retirado;
- campo desconhecido;
- `ano` como texto;
- base fora da tabela;
- `id` fora de sequência.

#### Scenario: Defeito não detectado
- **WHEN** a cópia com campo desconhecido é aprovada
- **THEN** o autoteste falha, nomeando o defeito
