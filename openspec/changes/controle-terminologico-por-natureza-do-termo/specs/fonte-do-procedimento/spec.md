## MODIFIED Requirements

### Requirement: Início da fonte de uma base nova
`python3 -m rsl procedimentos iniciar <sigla>` SHALL criar, de forma atômica, a pasta da
fonte da base, com `procedimento.toml` e `como_executar.md`. O que é derivável do protocolo,
do quadro e do arquivo de sementes vem preenchido; o que exige apuração na base ou decisão do
pesquisador vem com a marca `PENDENTE`. `plural` vem `explícito`, que vale até a lematização
ser medida.

#### Scenario: O que vem preenchido
- **WHEN** se executa `procedimentos iniciar lisa` para base registrada no protocolo
- **THEN** a fonte traz preenchidos uma linha de `[[criterios]]` por critério do protocolo
  (`ids` e `rotulo`), os idiomas do quadro por faceta, `plural = "explícito"`, uma linha de
  `[[sementes]]` por semente com `lisa` em `bases` e um elemento de `[[sintaxe]]` por
  categoria mínima, `nao_verificado`; e não traz o campo `camadas`

#### Scenario: O que vem pendente
- **WHEN** se executa `procedimentos iniciar lisa`
- **THEN** vêm com `PENDENTE` o destino e o *como* de cada critério, o teto, as derivações,
  a composição, a forma de execução, a sondagem de cada elemento e `como_executar.md`
