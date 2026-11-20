# Spec Delta

## MODIFIED Requirements

### Requirement: Ponto de entrada único
Toda operação SHALL ser executada por `python3 -m rsl <subcomando>`, a partir da raiz do
projeto. Os subcomandos SHALL ser estes:

- `conferir`, `conferir-dados`, `autoteste`, `mostrar`, `pendencias` e `gramatica`;
- `sementes planilha`;
- `termos sonda`, `termos exportar`, `termos validar <sigla>` e `termos importar`;
- `busca registrar`, `busca derivar`, `busca aderencia`, `busca fidelidade` e
  `busca sensibilidade`.

Os scripts `src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
`src/gen_semente.py` MUST NOT continuar existindo como ponto de entrada. O subcomando
`sementes sincronizar` MUST NOT existir, porque o conjunto-semente não tem mais arquivo
separado a reconciliar.

#### Scenario: Ajuda
- **WHEN** se executa `python3 -m rsl` sem subcomando
- **THEN** a ajuda lista os subcomandos e a saída tem o código USO

#### Scenario: Script antigo
- **WHEN** se procura `src/protocolo.py` ou `src/gen_semente.py`
- **THEN** o arquivo não existe, e nenhum documento do projeto cita o script antigo como
  comando

#### Scenario: Sincronização retirada
- **WHEN** se executa `python3 -m rsl sementes sincronizar`
- **THEN** a saída tem o código USO, e nenhum documento do projeto cita o subcomando como
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

O comportamento exigido por essas specs MUST NOT mudar com a troca de nome. `--sincronizar`
não tem sucessor: requisito que o cite fica sem efeito.

#### Scenario: Requisito antigo
- **WHEN** uma spec exige que `--conferir` reprove um defeito
- **THEN** `python3 -m rsl conferir` reprova esse defeito
