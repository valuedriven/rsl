# Spec Delta

## ADDED Requirements

### Requirement: Execução da sonda identifica a variante

O registro de uma execução da sonda SHALL identificar a variante: com proximidade (padrão)
ou sem proximidade. Base que exige a variante e tem registrada só uma das duas MUST ter a
sensibilidade por proximidade relatada como não calculada, com o motivo, e nunca como zero.

#### Scenario: Registro da variante
- **WHEN** o pesquisador registra a EB5 da WoS declarando a variante sem proximidade
- **THEN** a execução fica no registro com a expressão EB5 e a variante identificada, e a
  execução com proximidade continua distinta

#### Scenario: Variante faltante
- **WHEN** só a EB5 com proximidade está registrada na Scopus
- **THEN** `--sensibilidade scopus` relata a perda por restrição e declara a perda por
  proximidade não calculada, nomeando a execução que falta

### Requirement: Sensibilidade decompõe a perda

Onde as duas variantes da sonda estiverem registradas, `--sensibilidade` SHALL relatar, além
da perda por restrição (`EB5 \ EB4`), a perda por proximidade (sonda sem proximidade menos
sonda com proximidade), cada uma com a sua amostra a classificar à mão, em saída separada.
Sem a variante registrada, as saídas existentes MUST permanecer idênticas.

#### Scenario: Duas perdas
- **WHEN** as duas variantes da EB5 e a EB4 da WoS estão registradas
- **THEN** o relato mostra as duas frações, e a amostra da perda por proximidade é gravada
  em arquivo distinto do de `sensibilidade_wos.csv`

#### Scenario: Sem variante
- **WHEN** a base não usa proximidade
- **THEN** a saída de `--sensibilidade` é a mesma de antes da mudança
