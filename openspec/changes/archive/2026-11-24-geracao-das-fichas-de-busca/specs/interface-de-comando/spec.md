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
