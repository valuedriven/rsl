# Spec Delta

## Purpose

Compor os blocos de string e de expressão de cada ficha de base a partir da STR do protocolo
e dos parâmetros de composição da ficha, de modo que a forma executada numa base seja
reprodutível e não divirja do protocolo sem reprovar.

## ADDED Requirements

### Requirement: Ficha mista com blocos gerados
Na ficha de cada base, SHALL ser saída de geração os blocos cercados das subseções `STRn` e
das subseções de subconjunto por campo, da seção 3, e os blocos cercados das expressões
`EBn`, da seção 4. O restante da ficha SHALL ser autoral, e a geração MUST NOT alterá-lo.
O restante abrange a seção 1, a seção 2, a declaração de cobertura, a tabela de parâmetros
de composição, a prosa, a estratégia de proximidade, a forma curada, a seção 5 e a seção 6.

#### Scenario: Prosa preservada
- **WHEN** o pesquisador reescreve a prosa de "Como executar" da ficha da WoS e se executa
  `procedimentos gerar wos --gravar`
- **THEN** a prosa reescrita permanece byte a byte, e só os blocos gerados mudam

#### Scenario: Forma curada autoral
- **WHEN** a ficha da BRAPCI declara a execução curada
- **THEN** a geração não toca nas consultas curadas, que continuam conferidas como antes

### Requirement: Parâmetros de composição declarados na ficha
A ficha SHALL ter a tabela "Parâmetros de composição". Ela declara, por faceta, o campo e a
forma do termo no campo, com o grupo envolvido pelo campo ou o prefixo de campo por termo. A
tabela declara também a regra de aspas (todo termo, ou só a locução), o operador de
proximidade entre as âncoras, com a distância, ou `nenhum`, e os filtros de critério, por
remissão à seção 2. Parâmetro ausente ou fora do domínio MUST reprovar com
PROTOCOLO_ILEGIVEL, nomeando a ficha e o parâmetro.

#### Scenario: Campo ausente
- **WHEN** a tabela da ficha da Scopus não declara o campo de FCT3
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a ficha, FCT3 e o parâmetro

### Requirement: Subconjunto por campo e forma radical declarados em tabela
O subconjunto de uma faceta num campo próprio e a forma radical SHALL ser declarados em
tabela da ficha, com o campo e os termos que contêm, e não em prosa. Termo do subconjunto
que não está na STR da faceta nem é subsumido por termo dela MUST reprovar a base.

#### Scenario: Subconjunto declarado
- **WHEN** a ficha da ERIC declara o subconjunto `STR1b` de FCT1, no resumo, com os seus
  termos
- **THEN** o bloco de `STR1b` traz só esses termos, no campo declarado, e cada termo tem
  de estar na STR1 ou ser subsumido por termo dela

### Requirement: Composição dos blocos a partir da STR
O bloco de string de cada faceta SHALL conter os termos da STR nos idiomas e camadas que a
declaração de cobertura declara, menos a redução declarada. A eles se somam as formas de
número da flexão (`flexao-dos-termos`), na ordem da STR, cada flexão logo após o seu
termo. O bloco de cada expressão SHALL ser a composição do protocolo, com os blocos de
string das facetas, o operador de proximidade declarado entre as âncoras e os filtros da
seção 2.

#### Scenario: Termo novo na STR
- **WHEN** a STR2 ganha `aprendizagem online` e a ficha da Scopus declara FCT2 em pt
- **THEN** o ensaio de `procedimentos gerar scopus` lista, para STR2, `"aprendizagem online"` e
  `"aprendizagens online"` a acrescentar

#### Scenario: Termo reduzido
- **WHEN** a ficha da ERIC declara `massive open online course` na redução de FCT2
- **THEN** o bloco de STR2 da ERIC não o contém

### Requirement: Partição pelo teto de caracteres
Com teto numérico, a geração SHALL partir o grupo OR das facetas que não são âncora em
tantas consultas quantas forem precisas para que cada uma caiba no teto. A partição MUST
NOT retirar termo nem partir o grupo de uma âncora. Se as âncoras sozinhas não couberem no
teto, a geração MUST reprovar, nomeando a base, a expressão e o comprimento das âncoras.

#### Scenario: Expressão acima do teto
- **WHEN** a ficha da ERIC declara teto 1400 e a EB4 composta tem 2.739 caracteres
- **THEN** o gerador produz consultas de até 1.400 caracteres cada, com as âncoras íntegras
  em todas, e a união dos termos das partes é a do grupo original

#### Scenario: Âncoras acima do teto
- **WHEN** o teto declarado é menor que o comprimento das duas âncoras juntas
- **THEN** `procedimentos gerar` reprova, nomeando a base, a expressão e o comprimento, e não grava

### Requirement: Geração exibe antes de gravar
`procedimentos gerar` SHALL exibir, por base e por bloco, os termos a acrescentar e a retirar e as
formas geradas pela flexão, sem gravar. O ensaio MUST sair com REPROVADO quando há
diferença. Com `--gravar`, SHALL substituir só os blocos gerados, de forma atômica, depois
de reler o arquivo corrente. A gravação MUST ser recusada se o arquivo mudou durante a
execução, se a leitura reprova ou se alguma flexão é indecidível. Sem sigla, o comando age
sobre todas as bases da tabela do protocolo.

#### Scenario: Ensaio com diferença
- **WHEN** a ficha da WoS traz `"teaching strategy"` sem `"teaching strategies"`, e
  `teaching strategy` não é exceção não contável
- **THEN** `procedimentos gerar wos` lista `"teaching strategies"` a acrescentar em STR3 e em
  cada expressão que usa FCT3, não grava, e sai com REPROVADO

#### Scenario: Gravação interrompida
- **WHEN** a gravação falha antes de terminar
- **THEN** a ficha anterior permanece intacta

### Requirement: Conferência dos blocos gerados
`conferir` SHALL reprovar, por base, o bloco gerado que difere do que `procedimentos gerar`
produziria, nomeando a base, o bloco e `procedimentos gerar` como correção. As demais bases não
são afetadas.

#### Scenario: Bloco editado à mão
- **WHEN** alguém acrescenta à mão um termo ao bloco de EB4 da Scopus
- **THEN** `conferir` reprova a Scopus, nomeando EB4 e `procedimentos gerar scopus --gravar`; as
  demais bases passam

### Requirement: Autoteste prova a geração das fichas
O autoteste SHALL provar, numa cópia, cada caso abaixo e cada caso MUST falhar com a
conferência ou a recusa correspondente desligada:
- o bloco editado à mão reprova só a sua base;
- a gravação regenera o bloco e preserva o restante da ficha byte a byte;
- a gravação interrompida deixa a ficha intacta;
- a partição respeita o teto e conserva os termos;
- âncoras acima do teto impedem a gravação;
- o parâmetro de composição ausente dá PROTOCOLO_ILEGIVEL.

#### Scenario: Conferência desligada
- **WHEN** a comparação entre bloco e geração é desligada
- **THEN** o caso do bloco editado à mão falha
