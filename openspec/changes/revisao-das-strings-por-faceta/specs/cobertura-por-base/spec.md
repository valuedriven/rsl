# Spec Delta

## ADDED Requirements

### Requirement: Sonda sem proximidade onde as âncoras usam proximidade

Ficha cujo bloco da sonda combina as âncoras por operador de proximidade (`NEAR/n`, `W/n`)
SHALL trazer, na mesma expressão, um segundo bloco literal rotulado "sem proximidade", com
as âncoras unidas por `AND` e os mesmos termos e filtros. Ausência do bloco MUST reprovar
só aquela base. Ficha sem proximidade nas âncoras MUST NOT ter esse bloco.

#### Scenario: Sonda com proximidade sem a variante
- **WHEN** a EB5 da WoS usa `NEAR/5` entre as âncoras e não traz o bloco "sem proximidade"
- **THEN** a conferência da WoS reprova, nomeando a EB5 e o bloco ausente, e as demais bases
  não são afetadas

#### Scenario: Variante com termos divergentes
- **WHEN** o bloco "sem proximidade" da Scopus omite um termo da STR1 presente no bloco
  com proximidade
- **THEN** a conferência da Scopus reprova pela exigência "Termos do bloco conferem com as
  facetas declaradas", nomeando o termo

#### Scenario: Base sem proximidade
- **WHEN** a sonda da BRAPCI une as âncoras por `AND`
- **THEN** a variante não é exigida, e a sua presença reprova a BRAPCI como bloco redundante

### Requirement: Autoteste prova a exigência da sonda sem proximidade

O autoteste SHALL remover, numa cópia, o bloco "sem proximidade" da ficha de uma única base
com proximidade e exigir que só aquela base reprove.

#### Scenario: Defeito injetado
- **WHEN** o autoteste remove o bloco "sem proximidade" da EB5 da WoS
- **THEN** a conferência da WoS reprova e as demais não reprovam
