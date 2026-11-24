# geracao-das-strings Specification

## Purpose

Calcular as strings de busca por faceta (STR) a partir do quadro terminológico do protocolo,
de modo que a STR seja reprodutível a partir do quadro e não divirja dele sem reprovar.

## Requirements

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

### Requirement: Termo subsumido sai da STR
Um termo SHALL ficar fora da STR quando outro termo da mesma STR estiver contido nele como
sequência contígua de palavras inteiras, com a mesma grafia, acentos e hífen inclusive. A
subsunção MUST NOT admitir flexão, troca de acento nem separação de hífen.

#### Scenario: Locução contida
- **WHEN** o quadro de FCT1 tem `ontology` e `domain ontology`
- **THEN** a STR esperada contém `"ontology"` e não contém `"domain ontology"`

#### Scenario: Hífen não é separador
- **WHEN** o quadro de FCT1 tem `ontology` e `ontology-based modeling`
- **THEN** `"ontology-based modeling"` permanece na STR esperada

#### Scenario: Acento distingue
- **WHEN** o quadro de uma faceta tem `ontologia` e `ontología de dominio`, sem `ontología`
- **THEN** `"ontología de dominio"` permanece na STR esperada

#### Scenario: Flexão não subsume
- **WHEN** o quadro tem `thesaurus` e `thesauri`
- **THEN** os dois permanecem na STR esperada

### Requirement: Geração exibe antes de gravar
`strings gerar` SHALL exibir, por faceta, os termos que a STR esperada acrescenta e retira
em relação à STR do protocolo, e os subsumidos com o termo que os subsume, sem gravar. Com
`--gravar`, MUST reescrever só as células de string da tabela "Strings de busca por faceta",
e nenhum outro trecho do protocolo.

#### Scenario: Ensaio
- **WHEN** se executa `python3 -m rsl strings gerar` com STR3 diferente da esperada
- **THEN** a saída lista, para FCT3, os termos a acrescentar e a retirar; o protocolo não
  muda, e o código é REPROVADO

#### Scenario: Ensaio sem diferença
- **WHEN** todas as STRs são iguais às esperadas
- **THEN** a saída diz que não há diferença, e o código é OK

#### Scenario: Gravação
- **WHEN** se executa `python3 -m rsl strings gerar --gravar`
- **THEN** a tabela de STRs do protocolo passa a conter as STRs esperadas; o restante do
  arquivo fica idêntico, byte a byte; e `rsl documentos conferir` não reprova por STR divergente

#### Scenario: Gravação interrompida
- **WHEN** a gravação falha antes de terminar
- **THEN** o protocolo anterior permanece intacto

### Requirement: Protocolo ilegível não é gravado
`strings gerar` MUST NOT gravar quando a leitura do protocolo reprova, nem quando o quadro
tem termo em mais de uma faceta. Nesses casos, SHALL sair com o código da reprovação, sem
tocar no arquivo.

#### Scenario: Atribuição única violada
- **WHEN** `learning environment` consta dos quadros de FCT2 e FCT4 e se executa `strings
  gerar --gravar`
- **THEN** a saída nomeia o termo e as duas facetas, o código é REPROVADO, e o protocolo não
  muda

### Requirement: Autoteste prova a geração e a recusa
O autoteste SHALL provar, numa cópia, que a STR editada à mão é reprovada por `documentos conferir`;
que a gravação produz STR igual à esperada e preserva o restante do arquivo; e que termo em
duas facetas impede a gravação.

#### Scenario: STR editada à mão
- **WHEN** o autoteste acrescenta a uma cópia da STR1 um termo que não está no quadro
- **THEN** `documentos conferir` reprova com REPROVADO, e o autoteste falha se não reprovar
