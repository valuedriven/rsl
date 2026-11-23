# catalogo-de-apoio Specification

## Purpose

Deriva do guia de procedimentos um catálogo de skills e scripts por passo, verifica a
integridade das citações e declara a cobertura de apoio de cada passo.

## Requirements

### Requirement: Catálogo derivado do guia
O sistema SHALL ler `docs/procedimentos.md` e produzir um catálogo com módulo, etapa, passo,
origem, fonte, skills e scripts. O catálogo SHALL ter visão por passo, por skill e por
script, sem exigir um segundo arquivo de mapeamento. Guia ausente ou ilegível MUST terminar
com o código DADOS.

#### Scenario: Passo com skill e script
- **WHEN** um passo cita `questao-e-objetivos` e `busca registrar`
- **THEN** o catálogo mostra o passo nas visões por passo, por skill e por script

#### Scenario: Passo sem apoio
- **WHEN** um passo não cita skill nem script
- **THEN** o catálogo o lista na visão de cobertura, sem omiti-lo

#### Scenario: Guia ausente
- **WHEN** `docs/procedimentos.md` não existe
- **THEN** o comando termina com DADOS, nomeando o arquivo

### Requirement: Passo de adaptação
O catálogo SHALL registrar a origem de cada passo como `modelo` ou `adaptação`. A
conferência SHALL exigir `modelo = 63`, contar os passos marcados como adaptação e exigir
`total = modelo + adaptação`. Passo extra sem a marca ou contagem divergente MUST reprovar.

#### Scenario: Conta 63 + 1
- **WHEN** o guia tem 63 passos do modelo e um passo marcado como adaptação
- **THEN** a conferência aceita 64 passos e registra a origem de cada um

#### Scenario: Passo extra sem marca
- **WHEN** o guia tem 64 passos e nenhum está marcado como adaptação
- **THEN** a conferência reprova, nomeando o passo sem origem

#### Scenario: Contagem declarada errada
- **WHEN** o guia declara 63 passos e lista 64, sem explicar a diferença
- **THEN** a conferência reprova com a contagem encontrada e a declarada

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
- **WHEN** `registrar-decisao` é declarada transversal e citada em mais de um passo
- **THEN** a conferência não a trata como órfã e registra o papel transversal

### Requirement: Comandos e opções citados
Todo caminho de comando em uma linha `Script:` SHALL existir no parser; toda opção longa
MUST existir para aquele caminho. Todo comando do parser MUST ser citado ou declarado
transversal. Placeholders como `SIGLA`, `BASE`, `EXPRESSAO` e `ARQUIVO` MUST ser ignorados
como comando. Caminho ou opção inexistente MUST reprovar.

#### Scenario: Comando inexistente
- **WHEN** um passo cita `python3 -m rsl busca inexistente`
- **THEN** a conferência reprova, nomeando o caminho e o passo

#### Scenario: Opção inexistente
- **WHEN** um passo cita `python3 -m rsl termos validar --opcao-que-nao-existe tbci`
- **THEN** a conferência reprova, nomeando a opção

#### Scenario: Placeholder não é comando
- **WHEN** a sinopse é `python3 -m rsl termos validar [--faceta FACETA] SIGLA`
- **THEN** `SIGLA` não é tratado como comando nem como opção

#### Scenario: Comando não citado
- **WHEN** `projeto pendencias` existe no parser e não é citado nem declarado transversal
- **THEN** a conferência reprova, nomeando o comando não integrado

### Requirement: Cobertura declarada
Todo passo SHALL ter ao menos uma skill, um script, `Apoio: manual — razão` ou
`Apoio: lacuna — razão`. A razão MUST ser não vazia. Passo sem qualquer um deles ou com
razão vazia MUST reprovar. `Apoio: lacuna` MUST ser relatado sem, por si só, reprovar.

#### Scenario: Passo com skill
- **WHEN** um passo cita uma skill existente
- **THEN** não é exigido marcador de apoio manual

#### Scenario: Passo sem apoio e sem marcador
- **WHEN** um passo não cita skill, não cita script e não tem marcador
- **THEN** a conferência reprova, nomeando o passo

#### Scenario: Razão vazia
- **WHEN** um passo tem `Apoio: manual —` sem razão
- **THEN** a conferência reprova, nomeando o passo

#### Scenario: Lacuna declarada
- **WHEN** um passo tem `Apoio: lacuna — skill a decidir`
- **THEN** a conferência relata a lacuna e não reprova por ela

### Requirement: Catálogo gravado e atualizado
`catalogo gerar --gravar` SHALL gravar `docs/catalogo_de_apoio.md` de forma atômica. Sem
`--gravar`, o comando SHALL imprimir o catálogo e terminar com REPROVADO se alguma
conferência falhar ou se o arquivo gravado estiver defasado. `--json` SHALL emitir o
catálogo legível por máquina.

#### Scenario: Gravação
- **WHEN** se executa `python3 -m rsl catalogo gerar --gravar`
- **THEN** o arquivo é gravado e a conferência seguinte sai OK

#### Scenario: Catálogo defasado
- **WHEN** o guia muda e `docs/catalogo_de_apoio.md` não é regravado
- **THEN** `catalogo gerar` sem `--gravar` reprova, nomeando o arquivo defasado

#### Scenario: Falha sem gravação parcial
- **WHEN** uma conferência reprova durante `--gravar`
- **THEN** o arquivo anterior permanece intacto

#### Scenario: Saída JSON
- **WHEN** se executa `python3 -m rsl catalogo gerar --json`
- **THEN** a saída contém os passos, as skills e os comandos em estrutura legível por máquina

### Requirement: Nomes antigos em documento vivo
A conferência SHALL procurar nomes antigos de comandos e skills em documentos e skills
vivos e MUST reprovar a citação. `data/historico.md`, `openspec/changes/archive/` e a
tabela de correspondência do catálogo MUST ser isentos.

#### Scenario: Skill cita comando antigo
- **WHEN** uma skill viva cita `busca aderencia` e o nome canônico é `aderencia medir`
- **THEN** a conferência reprova, nomeando a skill e o comando antigo

#### Scenario: Histórico não é escaneado
- **WHEN** `data/historico.md` cita `sementes planilha`
- **THEN** a conferência não reprova por essa citação

### Requirement: Autoteste do catálogo
Cada conferência do catálogo SHALL ter um caso de autoteste que injeta o defeito
correspondente. O caso MUST falhar quando a conferência é desligada e MUST reprovar com o
código esperado quando ela está ligada.

#### Scenario: Skill inexistente no autoteste
- **WHEN** o autoteste injeta uma skill citada inexistente
- **THEN** o caso reprova com REPROVADO; com a conferência desligada, o caso falha

#### Scenario: Contagem no autoteste
- **WHEN** o autoteste injeta um passo extra sem marca de adaptação
- **THEN** o caso reprova com REPROVADO; com a conferência desligada, o caso falha
