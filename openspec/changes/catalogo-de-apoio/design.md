# Design

## Context

O guia `docs/procedimentos.md` já tem, sob cada passo, as linhas `Fonte`, `Script` e
`Skill`. Ele é a única fonte do mapeamento, mas nenhum comando o lê: `conferir` lê o
protocolo e as fichas, e o autoteste não conhece o guia. O estado corrente tem 64 passos
(63 do modelo mais o passo de geração das STRs), 21 skills e 17 caminhos de comando; 29
passos não citam skill nem script. A renomeação das fichas para
`docs/procedimentos_busca_<sigla>.md` já está feita e é consumida pelo catálogo.

Ver `proposal.md` — Why.

## Goals / Non-Goals

**Goals:**

- Derivar do guia uma visão por passo, por skill e por script, sem um segundo arquivo de
  mapeamento.
- Reprovar citação de skill/comando inexistente, skill órfã, comando não integrado, passo
  sem apoio declarado e contagem de passos divergente.
- Declarar a origem `modelo` ou `adaptação` de cada passo.
- Provar a conferência pelo autoteste, com um caso para cada defeito.

**Non-Goals:**

- Renomear comandos ou skills; isso é a change seguinte.
- Criar as skills `avaliacao-da-necessidade` e `busca-complementar`; a decisão fica
  registrada como lacuna até o pesquisador decidir.
- Substituir o guia como fonte: o catálogo é saída de geração.
- Ler o conteúdo semântico dos passos ou julgar se a skill é adequada; a conferência é
  estrutural.
- Validar as seções citadas em `Fonte`; isso seria outra conferência.

## Decisions

### D1 — O guia é a fonte; o catálogo é gerado

O catálogo é derivado de `docs/procedimentos.md` e gravado em
`docs/catalogo_de_apoio.md`. A alternativa — um manifesto TOML com passos, skills e
comandos — foi descartada porque criaria uma segunda fonte para o mesmo dado e obrigaria o
pesquisador a editar dois lugares. O catálogo gerado é uma visão, não um novo instrumento.

Consequência: a forma do guia passa a ser um contrato de leitura. O leitor precisa de uma
gramática de linha, descrita em D3.

### D2 — Um comando, dois modos

`python3 -m rsl catalogo gerar [--gravar] [--json]`:

- sem `--gravar`: imprime o catálogo, confere e sai com REPROVADO se houver inconsistência;
- com `--gravar`: grava o arquivo de forma atômica e só então sai OK;
- `--json`: emite a mesma informação em estrutura legível por máquina.

O desenho espelha `strings gerar`: o ensaio é o padrão, e a gravação é explícita. A
alternativa — `catalogo conferir` separado de `catalogo gerar` — foi descartada porque
duplicaria a mesma conferência em dois comandos.

### D3 — Gramática de linha do guia

O leitor percorre o guia em três níveis:

- `## M...` — módulo;
- `### E...` — etapa;
- `- ...` no início da linha — passo;
- `  - Fonte:`, `  - Script:`, `  - Skill:`, `  - Apoio:` — subitens do passo.

Regras:

- linha de continuação é a que não começa por `-` e está indentada sob o subitem;
- um passo pode ter vários `Script:` e vários `Skill:`, separados por `;`;
- a sinopse do comando pode ocupar mais de uma linha e conter placeholders em crase;
- o leitor extrai de cada `Script:` o caminho canônico (`python3 -m rsl ...`) e as opções
  `--longa`; posicionais e placeholders (`SIGLA`, `BASE`, `EXPRESSAO`, `ARQUIVO`,
  `RETORNO`, `DATA_HORA`, `JUSTIFICAR`) não são caminhos nem opções;
- o marcador `Apoio:` é obrigatório apenas quando não há skill nem script; a razão é o
  texto depois do travessão.

A alternativa — regex sobre todas as crases — foi descartada: `SIGLA` entre crases seria
lido como comando, e a sinopse multilinha seria truncada.

### D4 — Skills: existência, nome e papel

A conferência lê `.agents/skills/*/SKILL.md`, extrai o `name` do frontmatter e exige:

- toda skill citada no guia existe;
- `name` é igual ao nome da pasta;
- toda skill existente é citada ou declarada transversal.

Skill transversal é a que incide em mais de um módulo ou em passos de naturezas diferentes:
`registrar-decisao`, `rastreabilidade`, `revisao-geral-do-projeto`, `conferir-referencia`,
`relato-prisma`. Skill de artefato nomeia o artefato (`conjunto-semente`,
`ficha-de-busca-por-base`); skill de procedimento nomeia a atividade
(`teste-de-aderencia`, `execucao-da-busca`). O catálogo registra o papel; a conferência não
tenta inferi-lo do nome.

### D5 — Comandos: parser como fonte da existência

A conferência constrói a árvore de comandos a partir do parser de `__main__.py` — não de
uma lista escrita à mão — e exige:

- o caminho citado existe;
- cada opção `--longa` citada existe naquele caminho;
- todo caminho do parser é citado ou declarado transversal.

Os comandos transversais (`conferir`, `conferir-dados`, `autoteste`, `mostrar`,
`pendencias`, `gramatica`) aparecem na seção de conferências transversais do guia, não sob
um passo. O catálogo os trata como transversais, não como órfãos.

Aliases de renomeação só existirão na change seguinte; quando existirem, o catálogo deve
distinguir o nome canônico do alias e acusar citação de alias em documento vivo.

### D6 — Cobertura: manual e lacuna são declarações

Passo sem skill e sem script recebe um dos marcadores:

```markdown
  - Apoio: manual — <razão>
  - Apoio: lacuna — <razão>
```

`manual` é decisão: a atividade é do pesquisador, de gestão ou está fora do repositório.
`lacuna` é ausência reconhecida: falta uma skill ou um script, e a decisão está pendente.
A conferência exige a razão não vazia; `lacuna` é relatada, mas não reprova por si só.

A alternativa — inferir “manual” pela ausência — foi descartada: ausência de skill não é
ausência de competência, e o guia precisa distinguir as duas.

### D7 — Passo de adaptação

O guia declara:

> 63 passos do modelo, mais um passo de adaptação do projeto — a geração das STRs —,
> totalizando 64.

O passo novo leva a marca `(adaptação do projeto)`. O catálogo tem a coluna `Origem` e a
conferência exige `modelo = 63` e `total = modelo + adaptação`. O plano continua dizendo
que o modelo tem 63 passos; a nota de adaptação fica no guia e no plano, sem alterar a
descrição do modelo.

### D8 — Forma do catálogo

`docs/catalogo_de_apoio.md` tem:

1. cabeçalho com a fonte e o comando de geração; não leva data;
2. visão por módulo/etapa/passo: origem, fonte, skills, scripts, apoio;
3. visão por skill: tipo, passos, comandos, estado;
4. visão por script: passos, skill, lê/grava, estado;
5. cobertura por etapa e lista de passos sem apoio;
6. tabela de correspondência de nomes, quando houver renomeação.

O catálogo não copia o texto das fontes; cita a seção. O conteúdo do passo é o nome do
passo, que já é a chave de leitura do guia.

### D9 — Nomes antigos

A conferência varre `README.md`, `docs/*.md`, `.agents/skills/**/SKILL.md` e as specs vivas
em busca de nomes antigos de comando e de skill. Ficam isentos `data/historico.md`,
`openspec/changes/archive/` e a tabela de correspondência do próprio catálogo. A varredura
usa a lista de aliases declarada no parser; na ausência de aliases, a regra fica inativa.

### D10 — Autoteste

O grupo “catálogo” injeta, em cópias em memória:

- skill citada inexistente;
- skill existente não citada;
- comando inexistente;
- opção inexistente;
- passo extra sem marca de adaptação;
- passo sem skill, script ou marcador;
- catálogo defasado;
- citação de nome antigo em skill viva.

Cada caso tem de reprovar com REPROVADO (ou DADOS, quando o guia falta) e falhar quando a
conferência correspondente é desligada. O autoteste não depende do registro de execução
para esses casos.

### D11 — Citações que faltam

A change acrescenta, sem criar skill:

- `questao-e-objetivos` nos quatro passos de M2/E2 (temática, abordagem, objeto, questões);
- `relato-prisma` na tabela de composição do portfólio e na normalização do relatório;
- `busca-nas-bases` na exportação de metadados e nos alertas;
- `relato-prisma` também na revisão de conteúdo, ao lado de `conferir-referencia`.

As lacunas reais ficam declaradas, não preenchidas por aproximação:

- `avaliacao-da-necessidade` — M1/E1–E2 e M2/E1;
- `busca-complementar` — M3/E3, acervos especiais e pessoais.

### D12 — Decisão sobre novas skills

Criar as duas skills agora ampliaria o escopo e exigiria decisão metodológica do
pesquisador. A change prefere deixá-las como `Apoio: lacuna — skill a decidir`, para que a
ausência seja visível e a decisão não seja tomada pelo agente. Se o pesquisador aprovar, as
skills entram em change própria; a lacuna não bloqueia a conferência.

## Risks / Trade-offs

- [Parser do guia é prosa e pode quebrar com uma edição] → a forma é declarada no guia e no
  design; o autoteste injeta linhas fora do formato e exige DADOS/PROTOCOLO_ILEGIVEL; a
  mensagem nomeia o passo e a linha.
- [Catálogo vira segunda fonte] → é gerado; a conferência reprova o arquivo defasado e o
  cabeçalho diz “não editar à mão”.
- [Falso positivo em comando citado em prosa] → só linhas `Script:` entram na conferência
  de comandos; as demais citações são varridas apenas para nomes antigos.
- [Skill transversal mal classificada] → a lista de transversais é explícita no guia; o
  catálogo não infere.
- [Contagem de passos muda com nova adaptação] → a conta é declarada e conferida; a
  diferença aparece no relatório, não em silêncio.
- [Autoteste parcial por falta de registro] → os casos do catálogo não dependem do registro;
  o código 6 continua sendo PARCIAL, não falha.
- [A renomeação das fichas ainda não está arquivada] → o catálogo lê o caminho corrente e
  não reescreve o passado; a change seguinte trata dos nomes de comando e skill.

## Migration Plan

1. Implementar o comando e a conferência; rodar sobre o guia corrente e corrigir o que ele
   reprovar (contagem, marcadores, citações).
2. Gerar `docs/catalogo_de_apoio.md`; conferir que a gravação é atômica e que a segunda
   execução sai OK.
3. Atualizar README, guia e histórico.
4. Rodar `conferir`, `conferir-dados`, `autoteste` e `catalogo gerar`.
5. Rollback: remover o comando e o arquivo gerado; os marcadores `Apoio:` permanecem
   inofensivos e podem ser mantidos.

## Open Questions

- Criar `avaliacao-da-necessidade` e `busca-complementar` ou manter as lacunas declaradas?
  A decisão não muda o desenho do catálogo; muda apenas a lista de lacunas.
- O namespace canônico dos comandos (`documentos` ou `protocolo`) é decidido na change
  seguinte; o catálogo lê o parser corrente e não fixa nomes.
