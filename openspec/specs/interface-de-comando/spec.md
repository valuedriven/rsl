# interface-de-comando Specification

## Purpose

Oferecer um ponto de entrada único para as operações do projeto, com códigos de saída que
distinguem a reprovação do conteúdo da falha em ler, e com nomes previsíveis para os
comandos e para os arquivos que eles gravam.

## Requirements

### Requirement: Ponto de entrada único
Toda operação SHALL ser executada por `python3 -m rsl <subcomando>`, a partir da raiz do
projeto. Os subcomandos SHALL ser estes:

- `conferir`, `conferir-dados`, `autoteste`, `mostrar`, `pendencias` e `gramatica`;
- `sementes sincronizar` e `sementes planilha`;
- `termos sonda`, `termos exportar`, `termos validar <sigla>` e `termos importar`;
- `busca registrar`, `busca derivar`, `busca aderencia`, `busca fidelidade` e
  `busca sensibilidade`.

Os scripts `src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
`src/gen_semente.py` MUST NOT continuar existindo como ponto de entrada.

#### Scenario: Ajuda
- **WHEN** se executa `python3 -m rsl` sem subcomando
- **THEN** a ajuda lista os subcomandos e a saída tem o código USO

#### Scenario: Script antigo
- **WHEN** se procura `src/protocolo.py` ou `src/gen_semente.py`
- **THEN** o arquivo não existe, e nenhum documento do projeto cita o script antigo como
  comando

### Requirement: Correspondência com os nomes das specs
As specs que citam as operações pelos nomes antigos SHALL ser lidas por esta
correspondência:

| Nome antigo | Subcomando |
| --- | --- |
| `--conferir` | `conferir` |
| `--conferir-dados` | `conferir-dados` |
| `--autoteste` | `autoteste` |
| `--mostrar` | `mostrar` |
| `--pendencias` | `pendencias` |
| `--sincronizar` | `sementes sincronizar` |
| `gen_semente.py` | `sementes planilha` |
| `--sonda` | `termos sonda` |
| `--exportar` | `termos exportar` |
| `--validar` | `termos validar` |
| `--importar` | `termos importar` |
| `--registrar` | `busca registrar` |
| `--derivar` | `busca derivar` |
| `--aderencia` | `busca aderencia` |
| `--fidelidade` | `busca fidelidade` |
| `--sensibilidade` | `busca sensibilidade` |

O comportamento exigido por essas specs MUST NOT mudar com a troca de nome.

#### Scenario: Requisito antigo
- **WHEN** uma spec exige que `--conferir` reprove um defeito
- **THEN** `python3 -m rsl conferir` reprova esse defeito

### Requirement: Autoteste único
`python3 -m rsl autoteste` SHALL executar, numa só chamada, todos os autotestes do projeto,
inclusive a prova da composição da derivação, e informar a contagem de cada grupo.

#### Scenario: Composição incluída
- **WHEN** se executa `python3 -m rsl autoteste`
- **THEN** o resumo traz os casos da prova da composição ao lado dos demais grupos

### Requirement: Códigos de saída semânticos
Todo subcomando SHALL terminar com um destes códigos, e com nenhum outro:

| Código | Nome | Quando |
| --- | --- | --- |
| 0 | OK | a operação terminou e nada reprovou |
| 1 | REPROVADO | uma conferência ou uma condição de aceite reprovou o conteúdo: problema de coerência, `busca registrar` recusado, fidelidade acima do limiar, autoteste com caso que falhou |
| 2 | USO | argumento ou subcomando inválido |
| 3 | CONFIGURACAO | `config.toml` ausente, inválido ou incompleto, ou chave `protocolo` que aponta arquivo inexistente |
| 4 | PROTOCOLO_ILEGIVEL | protocolo ou ficha fora da gramática que o leitor exige |
| 5 | DADOS | arquivo alimentado, exportação ou arquivo de entrada ausente ou ilegível |
| 6 | PARCIAL | autoteste sem falha, com casos não executados |
| 7 | FONTE_EXTERNA | fonte externa com erro, bloqueio, captcha ou limite excedido |

Quando mais de uma condição ocorre, vale a de maior gravidade, nesta ordem: CONFIGURACAO,
PROTOCOLO_ILEGIVEL, DADOS, FONTE_EXTERNA, REPROVADO, PARCIAL.

#### Scenario: Protocolo ilegível não é reprovação
- **WHEN** o protocolo não tem a seção "Expressões de busca" e se executa `conferir`
- **THEN** a saída tem o código PROTOCOLO_ILEGIVEL, e não REPROVADO, e a mensagem nomeia a
  seção

#### Scenario: Coerência reprovada
- **WHEN** o protocolo é legível e uma STR tem termo fora do quadro da sua faceta
- **THEN** `conferir` sai com REPROVADO

#### Scenario: Configuração inválida
- **WHEN** o `config.toml` não é TOML válido
- **THEN** qualquer subcomando sai com CONFIGURACAO, e a mensagem nomeia o arquivo

#### Scenario: Arquivo alimentado ausente
- **WHEN** `data/registro_execucao.json` não existe e se executa `busca derivar`
- **THEN** a saída tem o código DADOS, e a mensagem nomeia o arquivo

#### Scenario: Autoteste parcial
- **WHEN** o autoteste não tem falha e tem casos não executados
- **THEN** a saída tem o código PARCIAL, e não OK

### Requirement: Códigos documentados e exibidos
A tabela de códigos de saída SHALL constar da ajuda de `python3 -m rsl` e do README. Toda
saída diferente de OK MUST trazer, na última linha, o nome do código.

#### Scenario: Última linha
- **WHEN** `conferir` reprova
- **THEN** a última linha da saída contém `REPROVADO`

### Requirement: Importação sem efeito
Importar qualquer módulo de `rsl` MUST NOT ler o `config.toml`, ler o protocolo, gravar
arquivo nem encerrar o processo. A leitura SHALL acontecer só quando um subcomando a
pede.

#### Scenario: Configuração inválida e importação
- **WHEN** o `config.toml` é inválido e se importa o módulo de derivação
- **THEN** a importação conclui sem erro, e o erro de configuração só aparece quando um
  subcomando é executado

### Requirement: Convenção de nomes
Os subcomandos SHALL ser verbos no infinitivo, em português e sem acento, agrupados por
atividade quando houver mais de um por atividade. Os arquivos que os subcomandos gravam
SHALL seguir estas regras:

- `snake_case`, em português e sem acento;
- o nome é o substantivo do conteúdo;
- quando há um arquivo por chave (expressão, base), o sufixo é a chave em minúsculas
  (`fidelidade_eb2.csv`, `sensibilidade_wos.csv`).

O nome de cada arquivo de entrada e de saída SHALL vir do `config.toml`.

#### Scenario: Saída por expressão
- **WHEN** `busca fidelidade` confere a EB2
- **THEN** a saída gravada se chama `fidelidade_eb2.csv`

#### Scenario: Planilha de validação
- **WHEN** a configuração é a do projeto
- **THEN** a planilha de validação se chama `validacao_terminologica.csv`
