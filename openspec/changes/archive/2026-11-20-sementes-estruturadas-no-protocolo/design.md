# Design

## Context

A motivação está em `proposal.md`, e os requisitos, nas specs desta change. Aqui,
"arquivo de sementes" é o arquivo apontado por `[documentos] sementes` do `config.toml`, e
nenhum trecho fixa o caminho.

O ponto de partida é o estado deixado por `reestruturacao-do-protocolo`, arquivada em
2026-11-20:

- o arquivo de sementes, com a tabela `[[sementes]]`;
- o esquema intermediário (`id`, `semente`, `bases` e `papel`), declarado na gramática;
- o `id` exigido em sequência a partir de SE1;
- autoria, ano, título e DOI ainda extraídos de `semente` por `_titulo()` e `_doi()`.

O estado verificado em 2026-11-20, depois do arquivamento:

- **O arquivo de sementes tem 10 sementes**, de SE1 a SE10, com SE4 em
  `desenvolvimento` e as demais em `validação`. Os campos são só `id`, `semente`, `bases`
  e `papel`. A equivalência com a tabela retirada do protocolo (bf6b9bf) está registrada
  em `data/historico.md`.
- **As referências seguem uma forma próxima da APA, com variações:**
  - SE10 traz editores, nome e local do evento;
  - algumas referências repetem o ano depois do veículo.
- **`data/sementes.json` existe** (chaves `versao` e `estudos`). Pela verificação feita
  na preparação desta change, ele tem as 10 sementes, ligadas por `doi:…`, com:
  - `verificacao` e `nota` preenchidos;
  - `veiculo_conferido = "sim"`;
  - `escopo`, `tipo`, `alinhamento` e `eric` vazios.

  O conteúdo campo a campo não foi conferido de novo depois do arquivamento. A tarefa 1.5
  o confere.
- **A evidência bruta é nomeada pelo `id`**: `data/evidencia/referencias/SE10_crossref.json`
  e `.md`.
- **A transcrição de 1.2–1.3 ainda existe** num scratchpad de sessão anterior, ainda com
  a tabela `[[semente]]` (no singular). É um diretório temporário, e a tarefa 1.5 prevê
  refazê-la se ela sumir.
- **O ensaio seco** (`sementes.py`) mede os termos de cada faceta presentes no título. Não
  é declaração de faceta.

## Goals / Non-Goals

**Goals:**
- Um único lugar por semente, sem extração por padrão de texto e sem ligação entre
  arquivos.
- Transcrição e migração que não percam nem inventem dado.
- Retirada de semente sem resto silencioso.
- Nenhum documento fixa o caminho do arquivo de sementes.

**Non-Goals:**
- Conferir as referências na fonte. Isso cabe à skill `conferir-referencia`.
- Preencher `facetas`, `tipo` ou `alinhamento`. São juízos do pesquisador.
- Decidir a regra para semente de validação sem faceta âncora. O pesquisador deixou a
  regra em branco (2026-11-20): o caso só é relatado, e a pendência fica aberta.
- Normalizar as referências pela ABNT. A exibição de `mostrar` é só para leitura.
- Reescrever entradas já registradas em `data/historico.md`. São registro datado.

## Decisions

### D1. Arquivo próprio, localizado pelo `config.toml`

O arquivo de sementes tem a tabela `[[sementes]]`. O caminho vem de `[documentos]
sementes`, e o protocolo não o cita (decisão de 2026-11-20). Essas duas coisas já foram
feitas por `reestruturacao-do-protocolo`, e esta change não as altera.

O mesmo vale para a documentação: README, skills e artefatos citam o arquivo pela chave,
e não pelo caminho. Assim, mudar o caminho no `config.toml` não deixa nenhum texto
desatualizado. A gramática já não traz o caminho, e o cenário "Caminho fora da gramática"
procura o valor configurado, e não um caminho fixo.

As regras da seção "Conjunto-semente" (regra de ajuste, fórmula de recuperação) ficam no
protocolo.

Alternativas descartadas:
- bloco ```` ```toml ```` dentro do protocolo, que foi a primeira forma desta change;
- linha de apontamento no protocolo (`Arquivo: …`), que foi a forma seguinte. O
  pesquisador preferiu o caminho no `config.toml`.

### D2. Esquema fechado

```toml
[[sementes]]
id = "SE1"
autores = ["Alvarenga, V. B. L.", "Cristovão, H. M."]
ano = 2023
titulo = "Objetos de aprendizagem organizados com base no padrão LOM-IEEE adaptado a uma ontologia operacional de domínio na web semântica"
veiculo = "Revista Ibero-Americana de Ciência da Informação (RICI)"
volume = "16"
numero = "1"
doi = "10.26512/rici.v16.n1.2023.47618"
bases = ["brapci"]
facetas = []
papel = "validação"
verificacao = "CONFIRMADA — dados bibliográficos conferidos pelo pesquisador em 2026-11-19; conteúdo não consultado."
tipo = ""
alinhamento = ""
nota = "Conferência declarada pelo pesquisador; dados do protocolo."
veiculo_conferido = "sim"
eric = ""
observacoes = ""
```

| Grupo | Campo | Tipo | Exigência |
| --- | --- | --- | --- |
| bibliográfico | `id` | texto `SEn` | obrigatório, único, em sequência a partir de SE1 |
| | `autores` | lista de texto | obrigatória, não vazia |
| | `ano` | inteiro | obrigatório |
| | `titulo`, `veiculo` | texto | obrigatórios |
| | `volume`, `numero`, `paginas` | texto | opcionais |
| | `doi` | texto `10.x/…` | opcional; ausente vira pendência |
| aferição | `bases` | lista de siglas da tabela de bases | obrigatória, não vazia, sem repetição |
| | `facetas` | lista de `FCTn` da tabela de facetas | opcional, sem repetição |
| | `papel` | `desenvolvimento` ou `validação` | obrigatório |
| conferência | `verificacao`, `tipo`, `alinhamento`, `nota`, `veiculo_conferido`, `eric` | texto | opcionais |
| sobra | `observacoes` | texto: o que a referência traz e não cabe em outro campo | opcional |

Algumas escolhas de tipo:

- `volume`, `numero` e `paginas` são texto, porque há valores como `"6-21"` e `"S1"`.
- `ano` é inteiro, porque é comparado ao recorte.
- Campo opcional ausente equivale a vazio.

Campo desconhecido reprova. Isso impede por construção que um erro de digitação
(`titlo`, `observacao`, o `escopo` retirado ou o `semente` do esquema intermediário) passe
como campo ignorado.

**`bases` significa indexação, não recuperação.** A semente que a base não indexa sai do
denominador daquela base. O que a busca recuperou é resultado e fica em
`semente_aderencia.csv`.

**`facetas` é declaração do pesquisador sobre o conceito do estudo.** Não pode ser copiada
do ensaio seco. O valor do campo está em contrastar as duas coisas: semente declarada em
FCT2 sem termo de FCT2 no título indica lacuna de vocabulário. Copiar o ensaio tornaria o
contraste circular.

### D3. Identificador em sequência; retirada renumera

O `id` tem a forma `SEn`, é único e segue a sequência a partir de SE1, sem lacuna. É a
exigência que já está na spec principal, e o pesquisador a manteve (2026-11-20). Lacuna e
`id` fora de sequência reprovam a leitura.

Consequência: retirar uma semente renumera as seguintes. Retirar SE3, por exemplo, faz SE4
a SE10 passarem a SE3 a SE9. A renumeração é um passo da retirada, descrito na skill
`conjunto-semente`:

- **evidência bruta** em `data/evidencia/referencias/`: os arquivos `SEn_…` das sementes
  renumeradas são renomeados para o `id` novo, e os da semente retirada são removidos;
- **`data/pendencias.json`**: as menções aos `id` renumerados são atualizadas;
- **`data/historico.md`**: a entrada da retirada registra a correspondência entre `id`
  antigo e `id` novo. As entradas anteriores não são reescritas, porque citam o `id`
  vigente na data, e a correspondência permite lê-las.

Alternativa descartada: `id` estável com lacunas admitidas, que foi a forma anterior deste
D3. Ela evitava a renumeração, mas o pesquisador manteve a sequência.

Limitação: a leitura e `conferir-dados` não verificam se a evidência renomeada pertence à
semente com aquele `id`. A verificação de D6 só detecta evidência de `id` inexistente.
Depois de uma retirada no meio do conjunto, um arquivo não renomeado continua com um `id`
existente e passa em silêncio. Ver "Open Questions".

### D4. Pendências, não reprovações

Reprova o que é incoerência mecânica: sigla de base ou de faceta inexistente, tipo errado,
campo desconhecido, `id` fora de sequência. Vira pendência o que é dado ainda não obtido
ou juízo ainda não feito:

- `doi` ausente. Muitas referências legítimas não têm DOI, então a ausência não reprova.
  Mas o DOI é a chave de conferência na fonte, e a ausência precisa aparecer;
- `facetas` vazia;
- semente de validação com `facetas` preenchida e sem nenhuma faceta âncora, conforme a
  coluna "Âncora obrigatória" da tabela de facetas. Fica como pendência até o pesquisador
  decidir a regra. Com `facetas` vazia, só se relata "facetas a informar": a falta de
  âncora decorre dela, e relatá-la à parte duplicaria a mesma pendência (decisão do
  pesquisador, 2026-11-20);
- `tipo` ou `alinhamento` vazios. É o que PD01 já registra.

### D5. Transcrição e migração verificáveis

A transcrição não usa os leitores de padrão (`_titulo`, `_doi`) para gerar o arquivo.
Usá-los propagaria o defeito que motiva a change.

- **Dados bibliográficos:** transcritos campo a campo do campo `semente` do arquivo de
  sementes. A transcrição de 1.2 foi feita sobre a célula da tabela de bf6b9bf, e o texto
  de `semente` pode diferir dela (ao menos perdeu o escape `\.`). Por isso, a
  reconstituição é refeita sobre `semente` antes do uso (tarefa 1.5).
- **A conferência é mecânica.** Para cada semente, a concatenação dos campos, somado o
  campo `observacoes`, tem de reconstituir o texto de `semente`. Só se admitem diferenças
  de pontuação, o ano repetido e os rótulos `DOI:`.
- **O que não cabe em nenhum campo vai para `observacoes`**, transcrito como está, por
  decisão do pesquisador (2026-11-20). É o caso de editores, evento e local da SE10. Com
  `observacoes`, nenhum trecho da referência original se perde.
- **Dados de conferência:** copiados de `sementes.json`, casando por DOI, como faz hoje a
  `ligacao`. A conferência compara cada campo de `campos_autorais`, exceto `escopo`, com o
  valor no TOML, e exige igualdade exata. Antes de descartar `escopo`, verifica-se que está
  vazio nas 10 sementes. Se algum não estiver, a migração para e o valor vai ao
  pesquisador.
- Só depois das duas conferências aprovadas `sementes.json` é removido.

### D6. Retirada sem resto

Semente retirada sai do TOML. Nada a guarda.

- **Saídas regeneradas** (`semente_aderencia.csv`) deixam de trazê-la na regeneração
  seguinte.
- **Evidência bruta** em `data/evidencia/referencias/` é nomeada `SEn_…`. O arquivo cujo
  `id` não está no TOML reprova `conferir-dados`, nomeando o arquivo. A remoção e a
  renomeação (D3) são feitas pelo pesquisador ou pelo agente, a pedido. A verificação só
  garante que não sobra evidência de `id` inexistente. Ela percorre só a subpasta
  `referencias/` de `[dados] evidencia` (decisão do pesquisador, 2026-11-20). Outra
  subpasta, se houver, não é cobrada por essa regra.
- **`data/historico.md`** registra a retirada: data, `id`, referência, motivo e a
  correspondência de renumeração (D3). A retirada muda o denominador da recuperação, e sem
  esse registro o recall de antes e o de depois não podem ser comparados. Esse registro
  não tem verificação automática, porque a semente retirada não deixa marca para
  conferir. A exigência fica na skill `conjunto-semente`, e a limitação é declarada.

### D7. Leitores do arquivo

`sementes planilha`, `conferir-dados`, `pendencias` e `mostrar` passam a ler as sementes
de `d["sementes"]` (o leitor do protocolo), sem outro arquivo. Saem `ligacao_semente`,
`sincroniza_sementes`, `cmd_sincronizar`, a reconciliação de órfãs e a coluna `escopo` da
planilha.

## Risks / Trade-offs

- **[Dado perdido na transcrição ou na migração]** → as duas conferências de D5 listam
  toda sobra e toda diferença. Sobra da referência vai para `observacoes`; diferença na
  migração para o trabalho e vai ao pesquisador.
- **[Leitura sem o arquivo]** → arquivo ausente termina com CONFIGURACAO. Nenhuma semente
  é presumida.
- **[Transcrição feita sobre outro texto]** → a reconstituição de D5 é refeita sobre o
  campo `semente` atual (tarefa 1.5). Se a transcrição do scratchpad tiver sido apagada,
  refaz-se com o mesmo método.
- **[Evidência atribuída à semente errada depois da renumeração]** → a retirada no meio
  do conjunto renomeia evidência (D3). Um arquivo esquecido fica com um `id` que existe e
  passa por `conferir-dados`. Hoje o risco é pequeno, porque só SE10 tem evidência. Fica
  em aberto (ver "Open Questions").
- **[Retirada sem registro no histórico]** → não há verificação automática (D6). Fica na
  skill e é declarado. Uma alternativa seria guardar no TOML uma marca de retirada, mas o
  pesquisador decidiu que a semente sai de tudo.
- **[Juízo de faceta contaminado pelo ensaio seco]** → a skill orienta o preenchimento a
  partir do resumo ou do texto completo, e não do resultado do ensaio.
- **[Caminho fixado de novo num documento]** → nada impede por construção que um texto
  volte a citar o caminho. As tarefas 4.2 e 4.3 conferem por busca do valor configurado. É
  conferência, não construção, e essa limitação é declarada.

## Migration Plan

1. Transcrição com `observacoes` (D5), conferida contra o campo `semente` atual, e
   migração dos dados de conferência, conferidas no scratchpad.
2. No mesmo passo, para `conferir` não ficar reprovado entre um passo e outro:
   - o esquema novo na gramática e o leitor dos campos;
   - o arquivo de sementes reescrito com os campos;
   - a remoção de `sementes.json`, de `sincronizar` e das chaves do `config.toml`;
   - o autoteste.
3. Ajuste de PD01, do README e das skills.

O protocolo não é alterado por esta change.

Rollback: reverter o commit. O arquivo de sementes intermediário e o `sementes.json`
ficam no histórico do git.

## Open Questions

- **Conferir a atribuição da evidência bruta (decisão do pesquisador).** `conferir-dados`
  poderia comparar o DOI gravado no arquivo de evidência com o `doi` da semente de mesmo
  `id`. Isso impediria a atribuição errada depois de uma renumeração (D3). Não está no
  escopo desta change enquanto o pesquisador não decidir.
