## ADDED Requirements

### Requirement: Papel de cada skill
Toda skill existente SHALL ter exatamente um papel declarado no guia: `principal`, `subordinada` ou
`transversal`. Skill sem papel, com mais de um papel ou com papel fora desses três MUST reprovar.

#### Scenario: Skill sem papel
- **WHEN** existe `.agents/skills/skill-nova/` e o guia não lhe atribui papel
- **THEN** a conferência reprova, nomeando a skill

#### Scenario: Papel antigo
- **WHEN** o guia atribui a uma skill o papel `artefato`
- **THEN** a conferência reprova, nomeando a skill e o papel não reconhecido

### Requirement: Marca de principal no passo
O guia SHALL distinguir, sob cada passo, a citação principal da de apoio pelos rótulos
`Skill principal:` e `Script principal:`; `Skill:` e `Script:` SHALL significar apoio. O catálogo SHALL
mostrar, em cada visão, se a citação é principal ou de apoio. A forma dos rótulos é contrato do leitor.

#### Scenario: Passo com principal e apoio
- **WHEN** um passo tem `Skill principal: \`testar-aderencia-das-expressoes\`` e `Skill: \`definir-conjunto-semente\``
- **THEN** o catálogo mostra a primeira como principal e a segunda como apoio desse passo

#### Scenario: Rótulo fora da forma
- **WHEN** um passo tem o subitem `Skill (principal):`
- **THEN** a leitura do guia reprova, nomeando o passo e o rótulo

### Requirement: Skill principal ancorada em um passo
Toda skill de papel `principal` SHALL ser principal em exatamente um passo. Todo passo SHALL ter no
máximo uma skill principal. Skill de papel `subordinada` ou `transversal` MUST NOT ser principal em
passo algum. Cada violação MUST reprovar.

#### Scenario: Principal sem passo
- **WHEN** a skill `redigir-relatorio` tem papel `principal` e não é principal em nenhum passo
- **THEN** a conferência reprova, nomeando a skill

#### Scenario: Principal em dois passos
- **WHEN** a skill `filtrar-estudos` é principal na 1ª e na 2ª filtragem
- **THEN** a conferência reprova, nomeando a skill e os dois passos

#### Scenario: Passo com duas principais
- **WHEN** um passo tem duas linhas `Skill principal:`
- **THEN** a conferência reprova, nomeando o passo

#### Scenario: Transversal como principal
- **WHEN** `registrar-decisao`, de papel `transversal`, aparece como `Skill principal:` em um passo
- **THEN** a conferência reprova, nomeando a skill e o passo

### Requirement: Skill subordinada ligada à sua principal
Toda skill de papel `subordinada` SHALL declarar no guia a skill principal que complementa. A principal
declarada MUST existir e ter papel `principal`, e a subordinada MUST ser citada no passo em que essa
principal é principal. Cada violação MUST reprovar.

#### Scenario: Subordinada sem principal declarada
- **WHEN** `declarar-flexao-por-base` tem papel `subordinada` e não declara principal
- **THEN** a conferência reprova, nomeando a skill

#### Scenario: Subordinada fora do passo da principal
- **WHEN** `declarar-flexao-por-base` complementa `gerar-procedimento-de-busca` e não é citada no passo em que esta é principal
- **THEN** a conferência reprova, nomeando a subordinada e o passo

### Requirement: Comando ancorado em um passo
Todo comando do parser SHALL ser principal em exatamente um passo ou estar declarado na tabela de
conferências transversais, e não ambas as coisas. Um passo MAY ter mais de um comando principal.
Comando sem âncora, principal em mais de um passo, ou transversal e principal ao mesmo tempo MUST
reprovar.

#### Scenario: Vários comandos principais no mesmo passo
- **WHEN** `busca derivar`, `conferencia fidelidade` e `conferencia sensibilidade` são `Script principal:` do mesmo passo
- **THEN** a conferência aceita, e cada um é principal nesse passo

#### Scenario: Comando só de apoio
- **WHEN** `busca derivar` é citado só em linhas `Script:` e não é transversal
- **THEN** a conferência reprova, nomeando o comando sem passo principal

#### Scenario: Comando principal em dois passos
- **WHEN** `busca derivar` é `Script principal:` em dois passos
- **THEN** a conferência reprova, nomeando o comando e os dois passos

#### Scenario: Transversal como principal
- **WHEN** `documentos conferir` está na tabela de conferências transversais e é `Script principal:` de um passo
- **THEN** a conferência reprova, nomeando o comando e o passo

### Requirement: Autoteste das âncoras
Cada regra de papel e de âncora SHALL ter um caso de autoteste que injeta o defeito correspondente
sobre o guia corrente. O caso MUST falhar quando a regra é desligada e MUST reprovar com REPROVADO
quando ela está ligada.

#### Scenario: Skill principal em dois passos no autoteste
- **WHEN** o autoteste marca a mesma skill como principal em dois passos
- **THEN** o caso reprova com REPROVADO; com a regra desligada, o caso falha

#### Scenario: Comando sem âncora no autoteste
- **WHEN** o autoteste troca o único `Script principal:` de um comando por `Script:`
- **THEN** o caso reprova com REPROVADO; com a regra desligada, o caso falha

## MODIFIED Requirements

### Requirement: Catálogo derivado do guia
O sistema SHALL ler `docs/procedimentos.md` e produzir um catálogo com módulo, etapa, passo,
origem, fonte, skills e scripts. O catálogo SHALL ter visão por passo, por skill e por
script, sem exigir um segundo arquivo de mapeamento. Guia ausente ou ilegível MUST terminar
com o código DADOS.

#### Scenario: Passo com skill e script
- **WHEN** um passo cita `redigir-questoes-de-revisao` e `busca registrar`
- **THEN** o catálogo mostra o passo nas visões por passo, por skill e por script

#### Scenario: Passo sem apoio
- **WHEN** um passo não cita skill nem script
- **THEN** o catálogo o lista na visão de cobertura, sem omiti-lo

#### Scenario: Guia ausente
- **WHEN** `docs/procedimentos.md` não existe
- **THEN** o comando termina com DADOS, nomeando o arquivo

### Requirement: Skills citadas e órfãs
Toda skill citada em um passo SHALL existir em `.agents/skills/`; o `name` do frontmatter
MUST ser igual ao nome da pasta. Toda skill existente MUST ser citada ao menos uma vez ou
declarada transversal no guia. Skill citada inexistente ou skill existente não citada MUST
reprovar.

#### Scenario: Skill citada inexistente
- **WHEN** um passo cita `skill-que-nao-existe`
- **THEN** a conferência reprova, nomeando a skill e o passo

#### Scenario: Skill órfã
- **WHEN** existe `.agents/skills/skill-nova/` e nenhum passo a cita
- **THEN** a conferência reprova, nomeando a skill não integrada

#### Scenario: Skill transversal declarada
- **WHEN** `registrar-decisao` é declarada transversal e citada como apoio em mais de um passo
- **THEN** a conferência não a trata como órfã e registra o papel transversal
