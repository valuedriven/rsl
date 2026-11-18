# Spec Delta

## ADDED Requirements

### Requirement: Autoteste prova a reprovação por base
O autoteste SHALL injetar um defeito na ficha de uma única base e exigir que a conferência
dessa base reprove e que a das demais não reprove.

#### Scenario: Defeito só na BRAPCI
- **WHEN** o autoteste devolve à ficha da BRAPCI um termo que só consta do quadro
- **THEN** a conferência da BRAPCI reprova e as das demais bases passam; outro resultado
  faz o autoteste falhar
