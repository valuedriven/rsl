# geracao-dos-procedimentos Specification

## Purpose

Compor o procedimento de busca de cada base, inteiro, a partir do protocolo, do arquivo de
sementes, da fonte da base e da flexão dos termos, de modo que o arquivo seja reprodutível,
tenha a mesma forma em todas as bases e não possa divergir das suas fontes sem reprovar.

## Requirements

### Requirement: Procedimento inteiro é saída de geração
O procedimento de busca de cada base, no caminho de `[documentos] procedimento`, SHALL ser
inteiramente produzido por `procedimentos gerar`. Nenhuma parte dele é autoral, e toda
correção se faz na fonte, no protocolo ou no arquivo de sementes.

#### Scenario: Prosa vem da fonte
- **WHEN** o pesquisador reescreve `como_executar.md` da WoS e executa `procedimentos gerar
  wos --gravar`
- **THEN** a subseção "Como executar" do procedimento da WoS passa a ser o fragmento
  reescrito, e nada mais muda

### Requirement: Origem de cada parte do procedimento
O conteúdo de cada parte do procedimento gerado SHALL vir só da origem que a gramática
declara para ela: o protocolo, o arquivo de sementes filtrado pela base, a fonte da base, o
arquivo de exceções ou o texto fixo. Os cenários dão a correspondência.

#### Scenario: Correspondência das partes
- **WHEN** se gera o procedimento de qualquer base
- **THEN** cada parte vem desta origem:

  | Parte | Origem |
  | --- | --- |
  | título | nome da base na tabela de bases do protocolo |
  | §1 tabela, roteiro de sondagens, notas | `[[sintaxe]]`, `[[sondagens]]`, `notas_sintaxe.md` |
  | §2 | `[[criterios]]`, com os IDs conferidos contra o protocolo |
  | §3 mapa, declaração, redução | facetas do protocolo, `[cobertura]`, `[[reducao]]` |
  | §3 blocos de string | STR do protocolo, `[cobertura]`, `[composicao]`, `[[subconjuntos]]`, `[[radical]]` e flexão |
  | §4 composição e tabela de execução | composição e papéis do protocolo; `[execucao]` |
  | §4 linhas fixas | texto fixo da gramática, condicionado ao estatuto das expressões; `notas_execucao.md` |
  | §4 montagem, curadas, proximidade | `[[regras_de_montagem]]`, `[[curadas]]`, `estrategia_de_proximidade.md` |
  | §4 expressões e blocos | composição do protocolo, blocos de string, `[composicao]`, cláusulas de `[[criterios]]`, partição |
  | §4 como executar, variantes | `como_executar.md`, `variantes.md` |
  | §5 | sementes cuja lista `bases` contém a sigla, observação de `[[sementes]]` da fonte, texto fixo, `notas_sementes.md` |
  | §6 | `ressalvas` |

#### Scenario: Semente com DOI no arquivo de sementes
- **WHEN** a SE1 tem `doi` no arquivo de sementes e `bases = ["brapci"]`
- **THEN** a linha da SE1 no procedimento da BRAPCI traz o DOI

### Requirement: Esqueleto único
Todo procedimento gerado SHALL ter o mesmo esqueleto, declarado na gramática:
- os títulos e a sua ordem;
- o separador entre seções;
- as colunas das tabelas;
- o formato do título de cada expressão, `### EBn (<função>)`;
- a linha `- Execução: <forma>`.

A subseção opcional SHALL aparecer só quando há dado ou fragmento que a alimente. Número
calculado (de consultas, de termos, de partes) MUST NOT aparecer em prosa. O rótulo "parte k
de n" das partições é a única exceção.

#### Scenario: Subseção sem fonte
- **WHEN** a fonte da Scopus não tem `estrategia_de_proximidade.md`
- **THEN** o procedimento da Scopus não tem a subseção "Estratégia de proximidade"

#### Scenario: Linha condicionada ao estatuto
- **WHEN** a fonte da BRAPCI declara EB2 e EB3 como derivadas que não se executam
- **THEN** o procedimento da BRAPCI não traz a linha de fidelidade, e traz a de
  sensibilidade, porque a sonda se executa

### Requirement: Composição dos blocos a partir da STR
O bloco de string de cada faceta SHALL conter os termos da STR nos idiomas e camadas que
`[cobertura]` declara, menos a redução. Somam-se a eles as formas de número da flexão
(`flexao-dos-termos`), na ordem da STR, cada uma logo depois do seu termo. Termo repetido
entra uma vez. O campo, a forma do campo e as aspas SHALL ser os de `[composicao]`.

#### Scenario: Termo novo na STR
- **WHEN** a STR2 ganha `plataforma educacional`, sem exceção, e a fonte da Scopus declara
  FCT2 em pt com plural explícito
- **THEN** o ensaio de `procedimentos gerar scopus` lista, em STR2 e em cada expressão com
  FCT2, `"plataforma educacional"` e `"plataformas educacionais"` a acrescentar

#### Scenario: Termo reduzido
- **WHEN** a fonte da ERIC declara `massive open online course` em `[[reducao]]` de FCT2
- **THEN** nenhum bloco da ERIC o contém

#### Scenario: Prefixo por termo e aspas só na locução
- **WHEN** a fonte da ERIC declara FCT3 com campo `abstract`, `forma = "prefixa"` e
  `aspas = "locucao"`
- **THEN** o bloco de STR3 traz `abstract:pedagogy` e `abstract:"teaching strategy"`

### Requirement: Composição dos blocos de expressão
O bloco de cada expressão que se executa SHALL ser a composição do protocolo, com:
- o grupo de cada faceta entre parênteses;
- a proximidade de `[composicao]` entre as âncoras;
- as cláusulas de `[[criterios]]` com `destino = "consulta"`.

Expressão derivada que não se executa MUST NOT ter bloco.

#### Scenario: Filtros da seção 2
- **WHEN** a fonte da WoS declara CE1 com `destino = "consulta"` e `clausula = "AND
  PY=(2017-2026)"`, e CE3 com `destino = "variante"`
- **THEN** os blocos de EB2 a EB5 terminam com `AND PY=(2017-2026)`, e a cláusula de CE3
  não entra em bloco nenhum

#### Scenario: Derivada sem bloco
- **WHEN** EB1 é derivada localmente
- **THEN** a subseção de EB1 não tem bloco cercado

### Requirement: Consultas de campo e subconjuntos
Com `[[consultas_de_campo]]`, cada expressão executada SHALL ser escrita como uma consulta
por entrada, rotulada `<n><letra>`, com a faceta indicada na string e no campo declarados.
As demais facetas ficam iguais em todas as consultas. O subconjunto SHALL trazer só os
termos que declara. Termo de subconjunto ou de forma radical que não está na STR da faceta,
nem é subsumido por termo dela, MUST reprovar a base.

#### Scenario: Duas consultas de campo
- **WHEN** a fonte da ERIC declara `a` = STR1 em `title` e `b` = STR1b em `abstract`, com
  `disjuncao = "em_linha"`
- **THEN** EB4 é escrita nas consultas `4a…` e `4b…`, com a faceta FCT2 idêntica em todas

#### Scenario: Disjunção em consultas separadas
- **WHEN** a fonte da ERIC declara as consultas de campo `a` e `b` e `[composicao] disjuncao
  = "consultas_separadas"`, e a EB4 é `STR1 AND STR2 AND (STR3 OR STR4)`
- **THEN** EB4 é escrita nas consultas `4a`, `4b`, `4c` e `4d`, uma por par de consulta de
  campo e alternativa da disjunção, rotuladas "<rótulo da consulta de campo> × <rótulo da
  faceta>"; a disjunção não aparece dentro de nenhuma consulta

### Requirement: Partição pelo teto de caracteres
Com teto numérico, a geração SHALL partir o grupo OR de maior comprimento entre as facetas
que não são âncora, em partes contíguas, até cada consulta caber no teto. A partição MUST
NOT retirar termo nem partir o grupo de uma âncora. A união dos termos das partes SHALL ser
conferida contra o grupo original.

Os casos abaixo MUST reprovar, nomeando a base, a expressão e o comprimento:
- as âncoras sozinhas não cabem no teto;
- `[execucao] forma = "unica"` exige partição.

#### Scenario: Expressão acima do teto
- **WHEN** a fonte da ERIC declara teto 1400 e a consulta 4a composta passa disso
- **THEN** o gerador produz as consultas `4a1`, `4a2`…, todas dentro de 1.400 caracteres,
  com as âncoras íntegras, e a união dos termos é a do grupo original

#### Scenario: Âncoras acima do teto
- **WHEN** o teto é menor que o comprimento das duas âncoras juntas
- **THEN** `procedimentos gerar` reprova, nomeando a base, a expressão e o comprimento, e
  não grava

### Requirement: Ensaio antes de gravar
`procedimentos gerar [<sigla>]` SHALL exibir a diferença entre o procedimento gravado e o
gerado, por base e por seção. A diferença inclui os termos a acrescentar e a retirar em cada
bloco e as formas da flexão com a sua origem. O ensaio MUST sair com REPROVADO quando há
diferença, e não grava. Sem sigla, o comando age sobre todas as bases da tabela do
protocolo.

#### Scenario: Ensaio com diferença
- **WHEN** a fonte da WoS acabou de ganhar uma variante em `variantes.md`
- **THEN** `procedimentos gerar wos` mostra a subseção acrescentada, não grava e sai com
  REPROVADO

### Requirement: Gravação atômica do procedimento
Com `--gravar`, `procedimentos gerar` SHALL substituir o arquivo inteiro, de forma atômica,
depois de reler as fontes, e SHALL criar o procedimento ainda inexistente. A gravação MUST
ser recusada quando:
- uma fonte mudou durante a execução;
- a leitura reprova;
- uma flexão é indecidível.

#### Scenario: Gravação interrompida
- **WHEN** a gravação falha antes de terminar
- **THEN** o procedimento anterior permanece intacto

#### Scenario: Flexão indecidível
- **WHEN** a STR1 tem `classificação facetada`, sem exceção, e a base declara plural
  explícito em pt
- **THEN** `procedimentos gerar --gravar` reprova, nomeando o termo, e não grava

### Requirement: Procedimento editado à mão reprova
`documentos conferir` SHALL gerar em memória o procedimento de cada base e reprovar a base
cujo arquivo gravado difere. A reprovação nomeia a base, a primeira linha divergente e
`procedimentos gerar <sigla> --gravar` como correção. As demais bases não são afetadas.

#### Scenario: Termo acrescentado à mão
- **WHEN** alguém acrescenta à mão um termo ao bloco de EB4 do procedimento da Scopus
- **THEN** `documentos conferir` reprova a Scopus, nomeando a linha e `procedimentos gerar
  scopus --gravar`; as demais bases passam

#### Scenario: Prosa editada no procedimento
- **WHEN** alguém corrige uma ressalva diretamente no procedimento da WoS
- **THEN** `documentos conferir` reprova a WoS; a correção tem de ir a `ressalvas` na fonte

### Requirement: Autoteste prova a geração
O autoteste SHALL provar, numa cópia, cada caso abaixo:
- o procedimento editado à mão reprova só a sua base;
- a gravação produz um arquivo igual ao gerado em memória;
- a gravação interrompida deixa o arquivo intacto;
- a partição respeita o teto e conserva os termos;
- âncoras acima do teto impedem a gravação;
- a expressão derivada não ganha bloco;
- a subseção sem fonte não aparece.

Cada caso MUST falhar com a conferência ou a recusa correspondente desligada.

#### Scenario: Conferência de igualdade desligada
- **WHEN** a comparação entre o arquivo e a geração é desligada
- **THEN** o caso do procedimento editado à mão falha
