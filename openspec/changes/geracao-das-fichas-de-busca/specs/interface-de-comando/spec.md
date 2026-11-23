# Spec Delta

## MODIFIED Requirements

### Requirement: Ponto de entrada único
Toda operação SHALL ser executada por `python3 -m rsl <subcomando>`, a partir da raiz do
projeto. Os subcomandos SHALL ser estes:

- `conferir`, `conferir-dados`, `autoteste`, `mostrar`, `pendencias` e `gramatica`;
- `sementes planilha`;
- `strings gerar` e `procedimentos gerar [<sigla>]`;
- `termos sonda`, `termos exportar`, `termos validar <sigla>` e `termos importar`;
- `busca registrar`, `busca derivar`, `busca aderencia`, `busca fidelidade` e
  `busca sensibilidade`.

Os scripts `src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
`src/gen_semente.py` MUST NOT continuar existindo como ponto de entrada. O subcomando
`sementes sincronizar` MUST NOT existir, porque o conjunto-semente não tem mais arquivo
separado a reconciliar.

#### Scenario: Ajuda
- **WHEN** se executa `python3 -m rsl` sem subcomando
- **THEN** a ajuda lista os subcomandos, inclusive `strings` e `procedimentos`, e a saída tem o código USO

#### Scenario: Ajuda do subcomando de geração
- **WHEN** se executa `python3 -m rsl strings gerar -h`
- **THEN** a ajuda mostra a opção `--gravar` e diz que, sem ela, nada é gravado

#### Scenario: Ajuda do subcomando de geração das fichas
- **WHEN** se executa `python3 -m rsl procedimentos gerar -h`
- **THEN** a ajuda mostra a sigla opcional e a opção `--gravar`, e diz que, sem a sigla,
  o comando age sobre todas as bases e que, sem `--gravar`, nada é gravado

#### Scenario: Script antigo
- **WHEN** se procura `src/protocolo.py` ou `src/gen_semente.py`
- **THEN** o arquivo não existe, e nenhum documento do projeto cita o script antigo como
  comando

#### Scenario: Sincronização retirada
- **WHEN** se executa `python3 -m rsl sementes sincronizar`
- **THEN** a saída tem o código USO, e nenhum documento do projeto cita o subcomando como
  comando
