# Design

## Context

A motivação está em `proposal.md`, e os requisitos, nas specs desta change. O ponto de
partida é o estado deixado por `reestruturacao-do-protocolo`:

- `docs/sementes.toml`, localizado por `[documentos] sementes`;
- o esquema intermediário `[[sementes]]` com `id`, `semente`, `bases` e `papel`,
  declarado na gramática;
- autoria, ano, título e DOI ainda extraídos de `semente` por `_titulo()` e `_doi()`.

O estado verificado em 2026-11-20:

- **`docs/sementes.toml` tem 10 sementes**, com SE4 em `desenvolvimento` e as demais em
  `validação`. Os `id`, `bases` e `papel` coincidem com a tabela retirada do protocolo
  (bf6b9bf).
- **As referências seguem uma forma próxima da APA, com variações:**
  - SE10 traz editores, nome e local do evento;
  - algumas referências repetem o ano depois do veículo.
- **`data/sementes.json` (versão 2) tem as 10 sementes**, ligadas por `doi:…`, com:
  - `verificacao` e `nota` preenchidos;
  - `veiculo_conferido = "sim"`;
  - `escopo`, `tipo`, `alinhamento` e `eric` vazios.
- **A evidência bruta é nomeada pelo `id`**: `data/evidencia/referencias/SE10_crossref.json`
  e `.md`.
- **O ensaio seco** (`sementes.py`) mede os termos de cada faceta presentes no título. Não
  é declaração de faceta.

## Goals / Non-Goals

**Goals:**
- Um único lugar por semente, sem extração por padrão de texto e sem ligação entre
  arquivos.
- Transcrição e migração que não percam nem inventem dado.
- Retirada de semente sem resto silencioso.

**Non-Goals:**
- Conferir as referências na fonte. Isso cabe à skill `conferir-referencia`.
- Preencher `facetas`, `tipo` ou `alinhamento`. São juízos do pesquisador.
- Decidir a regra para semente de validação sem faceta âncora. O pesquisador deixou a
  regra em branco (2026-11-20): o caso só é relatado, e a pendência fica aberta.
- Normalizar as referências pela ABNT. A exibição de `mostrar` é só para leitura.

## Decisions

### D1. Arquivo próprio, localizado pelo `config.toml`

O arquivo é `docs/sementes.toml`, com a tabela `[[sementes]]`, nomes que o pesquisador
escolheu ao criá-lo. O caminho vem de `[documentos] sementes`, e o protocolo não o cita
(decisão de 2026-11-20). Essas duas coisas já são feitas por `reestruturacao-do-protocolo`,
e esta change não as altera.

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
| bibliográfico | `id` | texto `SEn` | obrigatório, único |
| | `autores` | lista de texto | obrigatória, não vazia |
| | `ano` | inteiro | obrigatório |
| | `titulo`, `veiculo` | texto | obrigatórios |
| | `volume`, `numero`, `paginas` | texto | opcionais |
| | `doi` | texto `10.x/…` | opcional |
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

### D3. Identificador estável, sem exigência de sequência

Na forma anterior desta change, o `id` tinha de seguir a sequência a partir de SE1. Isso
não combina com a retirada de sementes. Retirar SE3 obrigaria a renumerar SE4 a SE10, e a
renumeração quebraria os nomes da evidência bruta (`SE10_crossref.json`) e as menções em
`historico.md` e `pendencias.json`.

Decisão: o `id` tem a forma `SEn` e é único, e lacunas são admitidas. Um `id` retirado não
deve ser reutilizado. A leitura não tem como verificar o reuso, porque a semente retirada
não deixa marca no arquivo: a regra fica na skill `conjunto-semente`, e essa limitação é
declarada.

### D4. Pendências, não reprovações

Reprova o que é incoerência mecânica: sigla de base ou de faceta inexistente, tipo errado,
campo desconhecido. Vira pendência o que é juízo ainda não feito:

- `facetas` vazia;
- semente de validação sem nenhuma faceta âncora, conforme a coluna "Âncora obrigatória"
  da tabela de facetas. Fica como pendência até o pesquisador decidir a regra;
- `tipo` ou `alinhamento` vazios. É o que PD01 já registra.

### D5. Transcrição e migração verificáveis

A transcrição não usa os leitores de padrão (`_titulo`, `_doi`) para gerar o arquivo.
Usá-los propagaria o defeito que motiva a change.

- **Dados bibliográficos:** transcritos campo a campo do campo `semente` de
  `docs/sementes.toml`. A transcrição de 1.2 foi feita sobre a célula da tabela de
  bf6b9bf, e o texto de `semente` pode diferir dela (ao menos perdeu o escape `\.`); por
  isso a reconstituição é refeita sobre `semente` antes do uso (tarefa 1.5). A conferência
  é mecânica. Para cada semente, a concatenação dos campos tem de reconstituir o texto de
  `semente`, admitidas só a pontuação, o ano repetido e os rótulos `DOI:`, depois de somado o
  campo `observacoes`. O que não cabe em nenhum campo vai para `observacoes`, transcrito
  como está, por decisão do pesquisador (2026-11-20). É o caso de editores, evento e local
  da SE10. A sobra deixa de ser descartável: com `observacoes`, nenhum trecho da
  referência original se perde.
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
- **Evidência bruta** em `data/evidencia/referencias/` é nomeada `SEn_…`. O arquivo de
  semente que não está no TOML reprova `conferir-dados`, nomeando o arquivo. A remoção é
  feita pelo pesquisador ou pelo agente, a pedido. A verificação só garante que não sobra
  resto em silêncio.
- **`data/historico.md`** registra a retirada: data, `id`, referência e motivo. A retirada
  muda o denominador da recuperação, e sem esse registro o recall de antes e o de depois
  não podem ser comparados. Esse registro não tem verificação automática, porque a
  semente retirada não deixa marca para conferir. A exigência fica na skill
  `conjunto-semente`, e a limitação é declarada.

### D7. Leitores do arquivo

`sementes planilha`, `conferir-dados`, `pendencias` e `mostrar` passam a ler as sementes
de `d["sementes"]` (o leitor do protocolo), sem outro arquivo. Saem `ligacao_semente`,
`sincroniza_sementes`, `cmd_sincronizar`, a reconciliação de órfãs e a coluna `escopo` da
planilha.

## Risks / Trade-offs

- **[Dado perdido na transcrição ou na migração]** → as duas conferências de D5 listam
  toda sobra e toda diferença. Sobra da referência vai para `observacoes`; diferença na
  migração para o trabalho e vai ao pesquisador.
- **[Leitura sem o arquivo]** → arquivo ausente termina com CONFIGURACAO, como já exige
  `reestruturacao-do-protocolo`. Nenhuma semente é presumida.
- **[Transcrição feita sobre outro texto]** → a reconstituição de D5 é refeita sobre o
  campo `semente` atual (tarefa 1.5), e a transcrição do scratchpad pode ter sido apagada:
  nesse caso, refaz-se com o mesmo método.
- **[Retirada sem registro no histórico]** → não há verificação automática (D6). Fica na
  skill e é declarado. Uma alternativa seria guardar no TOML uma marca de retirada, mas o
  pesquisador decidiu que a semente sai de tudo.
- **[Reuso de `id`]** → também não é verificável (D3). Pela regra da skill, o `id` não se
  reutiliza.
- **[Juízo de faceta contaminado pelo ensaio seco]** → a skill orienta o preenchimento a
  partir do resumo ou do texto completo, e não do resultado do ensaio.

## Migration Plan

1. Transcrição com `observacoes` (D5), conferida contra o campo `semente` atual, e
   migração dos dados de conferência, conferidas no scratchpad.
2. No mesmo passo, para `conferir` não ficar reprovado entre um passo e outro:
   - o esquema novo na gramática e o leitor dos campos;
   - `docs/sementes.toml` reescrito com os campos;
   - a remoção de `sementes.json`, de `sincronizar` e das chaves do `config.toml`;
   - o autoteste.
3. Ajuste de PD01, do README e das skills.

O protocolo não é alterado por esta change.

Rollback: reverter o commit. O `docs/sementes.toml` intermediário e o `sementes.json`
ficam no histórico do git.
