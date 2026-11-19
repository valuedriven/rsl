# Spec Delta

## ADDED Requirements

### Requirement: Forma de execução declarada na ficha
Cada ficha SHALL declarar a sua forma de execução numa linha `- Execução: única` ou
`- Execução: particionada`. Linha ausente, repetida ou com outro valor MUST reprovar a
conferência daquela base, nomeando a ficha; nenhum valor padrão é presumido.

#### Scenario: Ficha sem declaração
- **WHEN** a ficha da ERIC não tem a linha de execução
- **THEN** a conferência da ERIC reprova, nomeando a ficha, e as demais bases não são afetadas

#### Scenario: Valor fora do domínio
- **WHEN** a ficha declara `- Execução: dividida`
- **THEN** a conferência daquela base reprova, nomeando o valor e os admitidos

### Requirement: Faceta da forma curada identificada pelo código
Na forma curada da ficha, a faceta de cada consulta SHALL ser identificada pelo código
`FCTn`. Símbolo gráfico (emoji, cor) MUST NOT identificar faceta.

#### Scenario: Consulta marcada só por emoji
- **WHEN** a célula de facetas de uma consulta curada traz `🟦` sem `FCT1`
- **THEN** a consulta é lida sem faceta atribuída
