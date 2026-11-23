# Tasks

## 1. Forma do guia e passo de adaptação

- [ ] 1.1 Substituir a contagem do topo de `docs/procedimentos.md` por “63 passos do modelo,
  mais um passo de adaptação do projeto — a geração das STRs —, totalizando 64”; marcar o
  passo novo com `(adaptação do projeto)`. Verificar com `grep -n "adaptação do projeto\|sessenta e quatro" docs/procedimentos.md` e pela contagem de itens por etapa.
- [ ] 1.2 Acrescentar as citações que faltam: `questao-e-objetivos` nos quatro passos de
  M2/E2; `relato-prisma` na tabela de composição e na normalização; `busca-nas-bases` na
  exportação e nos alertas; `relato-prisma` na revisão de conteúdo. Verificar que cada
  citação nova corresponde a uma skill existente.
- [ ] 1.3 Acrescentar `Apoio: manual — <razão>` ou `Apoio: lacuna — <razão>` apenas aos
  passos que continuarem sem skill nem script depois de 1.2; usar `lacuna` só para as duas
  lacunas reconhecidas (`avaliacao-da-necessidade` e `busca-complementar`). Verificar que
  nenhum passo fica sem skill, script ou marcador e que nenhum passo tem skill e manual ao
  mesmo tempo.
- [ ] 1.4 Declarar no guia o papel das skills: procedimento, instrumento, artefato ou
  transversal; listar as transversais (`registrar-decisao`, `rastreabilidade`,
  `revisao-geral-do-projeto`, `conferir-referencia`, `relato-prisma`). Verificar que as 21
  skills aparecem uma vez nessa classificação.
- [ ] 1.5 Acrescentar a nota em `docs/01_plano.md` §1.4: o modelo tem 63 passos; o projeto
  acrescenta um passo de adaptação declarado no guia. Verificar que o plano não passa a
  dizer que o modelo tem 64.

## 2. Implementação do catálogo

- [ ] 2.1 Criar `src/rsl/catalogo.py` com a gramática de leitura do guia (módulo, etapa,
  passo, Fonte, Script, Skill, Apoio, continuação de linha). Verificar com um teste de
  leitura sobre o guia corrente: 64 passos, 14 etapas e 4 módulos.
- [ ] 2.2 Implementar as visões por passo, por skill e por script, e a lista de cobertura
  por etapa. Verificar que um passo com skill e script aparece nas três visões e que um
  passo sem apoio aparece na cobertura.
- [ ] 2.3 Implementar a conferência de skills: existência em `.agents/skills/`, `name` do
  frontmatter igual à pasta, e órfã/transversal. Verificar com uma skill citada inexistente
  e uma skill existente não citada; ambas devem reprovar.
- [ ] 2.4 Implementar a conferência de comandos a partir do parser: caminho, opções longas,
  placeholders ignorados e comando não citado. Verificar com `busca inexistente`,
  `termos validar --opcao-que-nao-existe` e `SIGLA`; os dois primeiros reprovam, o terceiro
  não é tratado como comando.
- [ ] 2.5 Implementar a conferência de contagem: `modelo = 63`, contagem dos passos com
  origem `adaptação`, `total = modelo + adaptação`; passo extra sem marca reprova. Verificar
  com 63 + 1 = 64 e com uma cópia que acrescenta um passo sem marca.
- [ ] 2.6 Implementar a varredura de nomes antigos em documentos e skills vivas, com isenção
  de `data/historico.md`, `openspec/changes/archive/` e da tabela de correspondência.
  Verificar que uma skill que cita `busca aderencia` reprova enquanto o alias existir.
- [ ] 2.7 Implementar `--gravar` atômico, a saída `--json` e o código REPROVADO quando o
  catálogo gravado está defasado. Verificar que uma falha durante `--gravar` deixa o arquivo
  anterior intacto.
- [ ] 2.8 Registrar `catalogo gerar` no parser de `src/rsl/__main__.py`, com ajuda e
  sinopse, e verificar com `python3 -m rsl catalogo gerar -h`.
- [ ] 2.9 Gerar `docs/catalogo_de_apoio.md` e conferir que o cabeçalho declara a fonte e o
  comando de geração e que o arquivo não é editado à mão.

## 3. Autoteste

- [ ] 3.1 Acrescentar o grupo “catálogo” em `src/rsl/autoteste/__init__.py`. Verificar que
  `python3 -m rsl autoteste` passa a listar o grupo.
- [ ] 3.2 Implementar os casos: skill citada inexistente; skill existente não citada;
  comando inexistente; opção inexistente; passo extra sem marca; passo sem marcador;
  catálogo defasado; citação de nome antigo. Verificar que cada caso reprova com REPROVADO
  ou DADOS, conforme a regra.
- [ ] 3.3 Demonstrar que cada caso falha quando a conferência correspondente é desligada na
  memória. Verificar que, com as conferências ligadas, o autoteste não tem falha nova.

## 4. Documentação e integração

- [ ] 4.1 Atualizar o `README.md`: incluir `docs/catalogo_de_apoio.md` no mapa, com “quem
  escreve” = `catalogo gerar --gravar`, e o comando na seção de execução. Verificar que o
  caminho aparece uma vez e que o comando documentado roda como escrito.
- [ ] 4.2 Acrescentar ao guia a seção que explica o catálogo, a conta 63 + adaptação e os
  marcadores de apoio, e incluir `catalogo gerar` na tabela de conferências transversais.
  Verificar que a seção não repete o conteúdo do catálogo e que o comando não fica sem
  citação no próprio guia.
- [ ] 4.3 Rodar `python3 -m rsl conferir` (0), `conferir-dados` (5, registro ausente),
  `autoteste` (6 PARCIAL, sem falha nova) e `catalogo gerar` (0). Registrar os códigos no
  relato da change.
- [ ] 4.4 Registrar a decisão no histórico com a skill `registrar-decisao`, citando o
  passo de adaptação, os marcadores de apoio e a criação do catálogo, sem transcrever
  contagem (README, Três registros). Verificar que a entrada cita o comando e o arquivo
  gerado.
- [ ] 4.5 Validar a change com `openspec validate --change catalogo-de-apoio --strict` e
  corrigir o que for apontado.

## Workflow follow-up

- Arquivar `strings-geradas-do-quadro` antes desta change, porque o delta de
  `interface-de-comando` já inclui `strings gerar`.
- Arquivar esta change depois da revisão do pesquisador.
- A change `namespace-de-comandos-e-skills` depende desta: o catálogo é o guarda que prova
  que nenhuma referência ficou órfã depois das renomeações.
