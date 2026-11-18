# cobertura-por-base Specification

## Purpose

Conferir a string de busca de cada ficha de base contra o vocabulário vigente do protocolo,
de modo que termo retirado não volte e termo vigente não falte sem redução declarada.

## Requirements

### Requirement: Vocabulário vigente é a string do protocolo
O termo vigente de uma faceta SHALL ser o que consta da STR correspondente no protocolo,
filtrado pelos idiomas e camadas que a ficha declara. O quadro terminológico MUST servir
apenas para classificar o termo por idioma e camada, e nenhuma lista de retirados SHALL ser
mantida no código ou na ficha.

#### Scenario: Termo vigente ausente da base
- **WHEN** um termo da STR, nos idiomas e camadas declarados, falta na string da base e não
  consta da redução declarada nem é alcançado por derivação declarada
- **THEN** a conferência daquela base reprova, nomeando faceta e termo

#### Scenario: Termo do quadro fora da STR
- **WHEN** um termo consta do quadro mas não da STR
- **THEN** ele não é esperado na string da base e a ausência não reprova

### Requirement: Termo da base deriva da STR
Todo termo da string de uma base SHALL corresponder, em flexão ou pela derivação declarada, a
um termo da STR da mesma faceta. Termo que só exista no quadro, ou em lugar nenhum, MUST
reprovar.

#### Scenario: Termo retirado devolvido à base
- **WHEN** a ficha usa, mesmo em flexão, um termo que está no quadro e não está na STR
- **THEN** a conferência daquela base reprova, dizendo que o termo não está na string do
  protocolo

#### Scenario: Termo inventado
- **WHEN** a ficha usa um termo que não deriva de nenhum termo do protocolo
- **THEN** a conferência daquela base reprova, nomeando o termo

### Requirement: Composição da base segue o protocolo
As facetas de cada expressão na ficha SHALL ser as que a composição lida do protocolo
determina, e a expressão executada pela base SHALL ser a que o protocolo declara executada.

#### Scenario: Base executa outra expressão
- **WHEN** a ficha executa uma expressão diferente da declarada executada no protocolo
- **THEN** a conferência daquela base reprova, nomeando as duas

### Requirement: Reprovação é por base
Defeito na forma de uma base MUST reprovar apenas a conferência daquela base.

#### Scenario: Uma ficha divergente
- **WHEN** só a ficha da BRAPCI diverge do protocolo
- **THEN** só a conferência da BRAPCI reprova
