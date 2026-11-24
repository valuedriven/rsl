# interface-de-comando Specification

## Purpose


Oferecer um ponto de entrada único para as operações do projeto, com códigos de saída que
distinguem a reprovação do conteúdo da falha em ler, e com nomes previsíveis para os
comandos e para os arquivos que eles gravam.

## Requirements


### Requirement: Ponto de entrada único
Toda operação SHALL ser executada por `python3 -m rsl <subcomando>`, a partir da raiz do
projeto. Os subcomandos canônicos SHALL ser estes:

- `documentos conferir` e `documentos gramatica`;
- `dados conferir`;
- `projeto autoteste` e `projeto pendencias`;
- `configuracao mostrar`;
- `termos sondar`, `termos exportar`, `termos validar <sigla>` e `termos importar`;
- `strings gerar`;
- `procedimentos gerar [<sigla>]` e `procedimentos iniciar <sigla>`;
- `sondagens registrar <sigla> <SDn>`;
- `catalogo gerar`;
- `aderencia planilhar` e `aderencia medir`;
- `busca registrar` e `busca derivar`;
- `conferencia fidelidade` e `conferencia sensibilidade`.

Os nomes antigos definidos na change `namespace-de-comandos-e-skills` MUST NOT ser aceitos,
conforme o requisito “Nomes antigos recusados”. Os scripts
`src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
`src/gen_semente.py` MUST NOT continuar existindo como ponto de entrada. O subcomando
`sementes sincronizar` MUST NOT existir, porque o conjunto-semente não tem mais arquivo
separado a reconciliar.

#### Scenario: Ajuda
- **WHEN** se executa `python3 -m rsl` sem subcomando
- **THEN** a ajuda lista apenas os subcomandos canônicos, inclusive `procedimentos` e `sondagens`, e a
  saída tem o código USO

#### Scenario: Ajuda do subcomando de geração
- **WHEN** se executa `python3 -m rsl strings gerar -h`
- **THEN** a ajuda mostra a opção `--gravar` e diz que, sem ela, nada é gravado

#### Scenario: Ajuda da geração dos procedimentos
- **WHEN** se executa `python3 -m rsl procedimentos gerar -h`
- **THEN** a ajuda mostra a sigla opcional e a opção `--gravar`. Diz também que, sem a
  sigla, o comando age sobre todas as bases, que, sem `--gravar`, nada é gravado, e que o
  procedimento é saída e se edita pela fonte

#### Scenario: Ajuda do início da fonte
- **WHEN** se executa `python3 -m rsl procedimentos iniciar -h`
- **THEN** a ajuda diz que o comando cria a fonte de uma base já registrada no protocolo, com
  os campos não deriváveis marcados `PENDENTE`, e que não sobrescreve fonte existente

#### Scenario: Script antigo
- **WHEN** se procura `src/protocolo.py` ou `src/gen_semente.py`
- **THEN** o arquivo não existe, e nenhum documento do projeto cita o script antigo como
  comando

#### Scenario: Sincronização retirada
- **WHEN** se executa `python3 -m rsl sementes sincronizar`
- **THEN** a saída tem o código USO, e nenhum documento do projeto cita o subcomando como
  comando

#### Scenario: Catálogo no ponto de entrada
- **WHEN** se executa `python3 -m rsl catalogo gerar -h`
- **THEN** a ajuda descreve a geração do catálogo e a saída não tem código de erro

#### Scenario: Comando canônico agrupado
- **WHEN** se executa `python3 -m rsl aderencia medir`
- **THEN** a operação mede a aderência ao conjunto-semente

### Requirement: Correspondência com os nomes das specs
As specs que citam as operações pelos nomes antigos SHALL ser lidas por esta
correspondência:

| Nome antigo | Subcomando |
| --- | --- |
| `--conferir` | `documentos conferir` |
| `--conferir-dados` | `dados conferir` |
| `--autoteste` | `projeto autoteste` |
| `--mostrar` | `configuracao mostrar` |
| `--pendencias` | `projeto pendencias` |
| `gen_semente.py` | `aderencia planilhar` |
| `--sonda` | `termos sondar` |
| `--exportar` | `termos exportar` |
| `--validar` | `termos validar` |
| `--importar` | `termos importar` |
| `--registrar` | `busca registrar` |
| `--derivar` | `busca derivar` |
| `--aderencia` | `aderencia medir` |
| `--fidelidade` | `conferencia fidelidade` |
| `--sensibilidade` | `conferencia sensibilidade` |

O comportamento exigido por essas specs MUST NOT mudar com a troca de nome. `--sincronizar`
não tem sucessor: requisito que o cite fica sem efeito.

#### Scenario: Requisito antigo
- **WHEN** uma spec exige que `--conferir` reprove um defeito
- **THEN** `python3 -m rsl documentos conferir` reprova esse defeito

### Requirement: Autoteste único
`python3 -m rsl projeto autoteste` SHALL executar, numa só chamada, todos os autotestes do projeto,
inclusive a prova da composição da derivação, e informar a contagem de cada grupo.

#### Scenario: Composição incluída
- **WHEN** se executa `python3 -m rsl projeto autoteste`
- **THEN** o resumo traz os casos da prova da composição ao lado dos demais grupos

### Requirement: Códigos de saída semânticos
Todo subcomando SHALL terminar com um destes códigos, e com nenhum outro:

| Código | Nome | Quando |
| --- | --- | --- |
| 0 | OK | a operação terminou e nada reprovou |
| 1 | REPROVADO | uma conferência ou uma condição de aceite reprovou o conteúdo: problema de coerência, `busca registrar` recusado, fidelidade acima do limiar, autoteste com caso que falhou |
| 2 | USO | argumento ou subcomando inválido |
| 3 | CONFIGURACAO | `config.toml` ausente, inválido ou incompleto, ou chave `protocolo` que aponta arquivo inexistente |
| 4 | PROTOCOLO_ILEGIVEL | protocolo ou procedimento de busca fora da gramática que o leitor exige |
| 5 | DADOS | arquivo alimentado, exportação ou arquivo de entrada ausente ou ilegível |
| 6 | PARCIAL | autoteste sem falha, com casos não executados |
| 7 | FONTE_EXTERNA | fonte externa com erro, bloqueio, captcha ou limite excedido |

Quando mais de uma condição ocorre, vale a de maior gravidade, nesta ordem: CONFIGURACAO,
PROTOCOLO_ILEGIVEL, DADOS, FONTE_EXTERNA, REPROVADO, PARCIAL.

#### Scenario: Protocolo ilegível não é reprovação
- **WHEN** o protocolo não tem a seção "Expressões de busca" e se executa `documentos conferir`
- **THEN** a saída tem o código PROTOCOLO_ILEGIVEL, e não REPROVADO, e a mensagem nomeia a
  seção

#### Scenario: Coerência reprovada
- **WHEN** o protocolo é legível e uma STR tem termo fora do quadro da sua faceta
- **THEN** `documentos conferir` sai com REPROVADO

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
- **WHEN** `documentos conferir` reprova
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
Os subcomandos SHALL ser `grupo ação` quando houver grupo natural, com a ação no infinitivo,
em português e sem acento; o topo pode ser verbo quando não houver grupo. O grupo SHALL
nomear o artefato ou domínio (`documentos`, `dados`, `projeto`, `configuracao`, `termos`,
`strings`, `catalogo`, `aderencia`, `busca`, `conferencia`). Os arquivos que os subcomandos
gravam SHALL seguir estas regras:

- `snake_case`, em português e sem acento;
- o nome é o substantivo do conteúdo;
- quando há um arquivo por chave (expressão, base), o sufixo é a chave em minúsculas
  (`fidelidade_eb2.csv`, `sensibilidade_wos.csv`).

O nome de cada arquivo de entrada e de saída SHALL vir do `config.toml`.

#### Scenario: Saída por expressão
- **WHEN** `conferencia fidelidade` confere a EB2
- **THEN** a saída gravada se chama `fidelidade_eb2.csv`

#### Scenario: Planilha de validação
- **WHEN** a configuração é a do projeto
- **THEN** a planilha de validação se chama `validacao_terminologica.csv`

#### Scenario: Ação nominal recusada
- **WHEN** se tenta registrar um comando cuja ação é substantivo, como a sonda do grupo
  `termos`
- **THEN** o nome canônico é `termos sondar`, e o substantivo não é aceito como comando

### Requirement: Nomes antigos recusados
Os nomes antigos de comando renomeados pela change `namespace-de-comandos-e-skills` MUST NOT
ser aceitos: cada um MUST terminar com o código USO, sem executar operação. A chave antiga
`[documentos] ficha` do `config.toml` MUST reprovar com o código CONFIGURACAO, e a mensagem
MUST nomear `[documentos] procedimento`.

#### Scenario: Comando antigo
- **WHEN** se executa `python3 -m rsl busca aderencia`
- **THEN** a saída tem o código USO, e nenhuma medição de aderência é executada

#### Scenario: Comando antigo de uma palavra
- **WHEN** se executa `python3 -m rsl conferir`
- **THEN** a saída tem o código USO

#### Scenario: Chave antiga na configuração
- **WHEN** o `config.toml` traz `[documentos] ficha`
- **THEN** qualquer subcomando que lê a configuração sai com CONFIGURACAO, e a mensagem
  nomeia a chave antiga e `[documentos] procedimento`
