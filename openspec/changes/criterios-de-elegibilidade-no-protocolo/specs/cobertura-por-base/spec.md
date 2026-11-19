# Spec Delta

## ADDED Requirements

### Requirement: Critérios da ficha conferem com o protocolo

O conjunto de IDs de critério citados na seção 2 de cada ficha SHALL ser igual ao conjunto
de IDs da tabela de critérios do protocolo. ID citado que não existe no protocolo, ou
critério do protocolo ausente da ficha, MUST reprovar só a conferência daquela base,
nomeando ficha e ID.

#### Scenario: Ficha cita critério inexistente

- **WHEN** o protocolo é renumerado e o CE9 passa a CE10, e a ficha da WoS ainda cita CE9
  como "Outros tipos documentais"
- **THEN** a conferência da WoS reprova, nomeando CE9 como ausente do protocolo e CE10 como
  ausente da ficha, e as demais bases corrigidas não reprovam

#### Scenario: Critério agrupado numa linha

- **WHEN** a ficha cita `CE1 / CE2` numa mesma linha
- **THEN** os dois IDs contam como citados

#### Scenario: Fichas em dia

- **WHEN** as quatro fichas citam exatamente os IDs do protocolo
- **THEN** essa dimensão não reprova nenhuma base

### Requirement: Autoteste prova a reprovação do critério defasado

O autoteste SHALL injetar, numa cópia, um ID de critério inexistente na ficha de uma única
base e exigir que só aquela base reprove.

#### Scenario: Defeito injetado numa base

- **WHEN** o autoteste troca CE9 por CE99 na ficha da Scopus
- **THEN** a conferência da Scopus reprova e as das demais bases não reprovam
