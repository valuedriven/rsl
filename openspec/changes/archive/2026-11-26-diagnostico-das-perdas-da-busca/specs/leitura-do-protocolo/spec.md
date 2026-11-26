# Spec Delta

## MODIFIED Requirements

### Requirement: Resultado parcial do autoteste declarado
Quando houver caso não executado, o autoteste SHALL declarar que o resultado é parcial e
terminar com o código PARCIAL, desde que nenhum caso executado tenha falhado. Havendo
falha, o código é REPROVADO, e a mensagem informa também os casos não executados. O número
de casos não executados SHALL vir de contagem feita pelo próprio autoteste (um caso trocado
pelo aviso, ou número calculado dos dados); o bloco que deixa de rodar por retorno
antecipado SHALL ser relatado como bloco inteiro, de tamanho não contado, e MUST NOT levar
número escrito à mão.

#### Scenario: Arquivos alimentados ausentes
- **WHEN** `projeto autoteste` termina sem falha e com casos não executados
- **THEN** a última mensagem diz que o autoteste é parcial, quantos casos não rodaram e por
  quê, e o código de saída é PARCIAL

#### Scenario: Falha com casos não executados
- **WHEN** um caso executado falha e há casos não executados
- **THEN** o código de saída é REPROVADO, e a mensagem informa os casos não executados

#### Scenario: Bloco não executado
- **WHEN** um grupo encerra antes dos seus casos por falta de dado de ensaio
- **THEN** o relato diz que o restante do bloco não foi executado e por quê, sem número de
  casos, e o código de saída é PARCIAL

#### Scenario: Contagem à mão recusada
- **WHEN** um grupo chama o aviso de casos não executados no formato antigo, com o número
  como primeiro argumento
- **THEN** a chamada é recusada no próprio autoteste, em vez de relatar um número que não
  foi contado
