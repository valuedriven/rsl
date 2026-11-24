## MODIFIED Requirements

### Requirement: Vocabulário vigente é a string do protocolo
O termo vigente de uma faceta SHALL ser o que consta da STR correspondente no protocolo,
filtrado pelos idiomas que o procedimento de busca declara. O controle terminológico MUST
servir apenas para classificar o termo por idioma, e nenhuma lista de retirados SHALL ser
mantida no código ou no procedimento de busca. Nenhum filtro por linha do CT SHALL ser
aplicado.

#### Scenario: Termo vigente ausente da base
- **WHEN** um termo da STR, nos idiomas declarados, falta na string da base e não
  consta da redução declarada nem é alcançado por derivação declarada
- **THEN** a conferência daquela base reprova, nomeando faceta e termo

#### Scenario: Termo do quadro fora da STR
- **WHEN** um termo consta do quadro mas não da STR
- **THEN** ele não é esperado na string da base e a ausência não reprova

#### Scenario: Campo camadas declarado
- **WHEN** a `[cobertura]` de uma fonte de procedimento declara `camadas = "todas"`
- **THEN** a leitura da fonte reprova o campo como desconhecido, nomeando a base e o campo
