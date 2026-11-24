## MODIFIED Requirements

### Requirement: STR é a união do quadro da faceta
A STR esperada de uma faceta SHALL conter todo termo das linhas "Termo livre" e
"Descritores correspondentes" do CT dessa faceta, nos idiomas do cabeçalho, uma única vez,
exceto o subsumido. A linha "Termos sinônimos ou relacionados" MUST NOT entrar na STR. A
ordem SHALL ser a dos idiomas do cabeçalho; dentro do idioma, a das linhas (termo livre,
descritores correspondentes); dentro da linha, a do CT.

#### Scenario: Termo acrescentado ao quadro
- **WHEN** o pesquisador acrescenta `taxonomía facetada` à linha "Termo livre" do CT1, em es
- **THEN** a STR esperada de FCT1 contém `"taxonomía facetada"` na posição dos termos es da
  linha "Termo livre"

#### Scenario: Termo retirado do quadro
- **WHEN** `practice` sai do CT3
- **THEN** a STR esperada de FCT3 não contém `"practice"`

#### Scenario: Mesma forma em dois idiomas
- **WHEN** `educacional` consta das colunas pt e es do CT2
- **THEN** a STR esperada contém `"educacional"` uma vez

#### Scenario: Termo em duplicidade na STR do protocolo
- **WHEN** a STR1 do protocolo traz `"ontology"` duas vezes, e os demais termos são os da
  STR esperada
- **THEN** `documentos conferir` e `strings gerar` reprovam a STR1 com a mesma mensagem, que diz
  `'ontology'` em DUPLICIDADE e o número de ocorrências; e `strings gerar --gravar` grava a
  STR com o termo uma vez

#### Scenario: Termo reclassificado
- **WHEN** `ontology` passa da linha "Termo livre" para "Descritores correspondentes" do CT1
- **THEN** a STR esperada de FCT1 tem os mesmos termos, e `ontology` muda de posição

#### Scenario: Termo em sinônimos ou relacionados
- **WHEN** `thesauri` está na linha "Termos sinônimos ou relacionados" do CT1, em `en`
- **THEN** a STR esperada de FCT1 não contém `"thesauri"`, e a ausência não reprova

#### Scenario: Termo de sinônimos ou relacionados posto na STR
- **WHEN** a STR1 do protocolo traz `"thesauri"`, que está só na linha "Termos sinônimos ou
  relacionados" do CT1
- **THEN** `documentos conferir` reprova a STR1, dizendo que o termo está numa linha que não
  entra na STR, e `strings gerar --gravar` grava a STR sem ele
