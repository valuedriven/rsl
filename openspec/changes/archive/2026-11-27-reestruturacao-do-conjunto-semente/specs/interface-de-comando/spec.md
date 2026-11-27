# Spec Delta

## MODIFIED Requirements

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
- `aderencia ensaiar` e `aderencia medir`;
- `sementes copiar`, `sementes metadados` e `sementes completar`;
- `busca registrar` e `busca derivar`;
- `conferencia fidelidade` e `conferencia sensibilidade`.

Os nomes antigos definidos na change `namespace-de-comandos-e-skills` MUST NOT ser aceitos,
conforme o requisito “Nomes antigos recusados”. Os scripts
`src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
`src/gen_semente.py` MUST NOT continuar existindo como ponto de entrada. O subcomando
`sementes sincronizar` MUST NOT existir, porque o conjunto-semente não tem mais arquivo
separado a reconciliar. O subcomando `aderencia planilhar` MUST NOT existir, porque a
planilha de aderência foi retirada.

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

#### Scenario: Ensaio seco sem planilha
- **WHEN** se executa `python3 -m rsl aderencia ensaiar`
- **THEN** o ensaio seco é impresso e nenhum arquivo é gravado

#### Scenario: Ajuda do complemento do Zotero
- **WHEN** se executa `python3 -m rsl sementes completar -h`
- **THEN** a ajuda mostra as opções `--gravar` e `--retirar`, e diz que, sem `--gravar`,
  nada é gravado no Zotero

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
| `gen_semente.py` | `aderencia ensaiar` |
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
não tem sucessor: requisito que o cite fica sem efeito. Requisito que exija de
`gen_semente.py` a gravação da planilha de aderência também fica sem efeito, porque a
planilha foi retirada.

#### Scenario: Requisito antigo
- **WHEN** uma spec exige que `--conferir` reprove um defeito
- **THEN** `python3 -m rsl documentos conferir` reprova esse defeito

### Requirement: Nomes antigos recusados
Os nomes antigos de comando renomeados pela change `namespace-de-comandos-e-skills` MUST NOT
ser aceitos: cada um MUST terminar com o código USO, sem executar operação. A chave antiga
`[documentos] ficha` do `config.toml` MUST reprovar com o código CONFIGURACAO, e a mensagem
MUST nomear `[documentos] procedimento`. A chave retirada `[saidas] aderencia` MUST reprovar
com o código CONFIGURACAO, e a mensagem MUST dizer que a planilha de aderência foi retirada.

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

#### Scenario: Planilha retirada
- **WHEN** se executa `python3 -m rsl aderencia planilhar`
- **THEN** a saída tem o código USO, e nenhum arquivo é gravado

#### Scenario: Chave da planilha na configuração
- **WHEN** o `config.toml` traz `[saidas] aderencia`
- **THEN** qualquer subcomando que lê a configuração sai com CONFIGURACAO, e a mensagem diz
  que a planilha de aderência foi retirada
