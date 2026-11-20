# Design

## Context

A motivação está em `proposal.md`, e os requisitos, nas specs desta change. O ponto de
partida é o pacote `src/rsl/` e a gramática declarada de `refatoracao-dos-scripts`
(arquivada em 2026-11-20).

O estado verificado em 2026-11-20:

- **A tabela do protocolo tem 10 sementes e a coluna `Papel`**, com SE4 em
  `desenvolvimento` e as demais em `validação`.
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

### D1. Arquivo próprio, apontado pelo protocolo

A seção "Conjunto-semente" do protocolo traz uma única linha de apontamento, com o rótulo
declarado na gramática:

```markdown
Arquivo: `docs/conjunto_semente.toml`
```

O caminho é relativo à raiz do projeto. O caminho não vai para o `config.toml`, porque o
conjunto-semente é parâmetro estrutural e só vem do protocolo, como diz o cabeçalho do
`config.toml`. O protocolo continua sendo a fonte, e o arquivo é um anexo dele.

As regras da seção (regra de ajuste, fórmula de recuperação) ficam no protocolo.

Alternativa descartada: bloco ```` ```toml ```` dentro do protocolo, que era a forma
anterior desta change. O pesquisador preferiu o arquivo próprio. Com ele desaparece também
o risco de um editor de texto destruir o bloco ao exportar o `.md`.

### D2. Esquema fechado

```toml
[[semente]]
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
(`titlo`, `observacao` ou o `escopo` retirado) passe como campo ignorado.

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

- **Dados bibliográficos:** transcritos campo a campo do texto da célula. A conferência é
  mecânica. Para cada semente, a concatenação dos campos tem de reconstituir o texto da
  célula, admitidas só a pontuação, o ano repetido e os rótulos `DOI:`, depois de somado o
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
- **[Protocolo lido sem o arquivo]** → o apontamento é obrigatório, e arquivo ausente
  reprova. A seção não fica vazia em silêncio.
- **[Retirada sem registro no histórico]** → não há verificação automática (D6). Fica na
  skill e é declarado. Uma alternativa seria guardar no TOML uma marca de retirada, mas o
  pesquisador decidiu que a semente sai de tudo.
- **[Reuso de `id`]** → também não é verificável (D3). Pela regra da skill, o `id` não se
  reutiliza.
- **[Juízo de faceta contaminado pelo ensaio seco]** → a skill orienta o preenchimento a
  partir do resumo ou do texto completo, e não do resultado do ensaio.

## Migration Plan

1. Transcrição com `observacoes` (D5) e migração dos dados de conferência, conferidas no
   scratchpad.
2. No mesmo passo, para `conferir` não ficar reprovado entre um passo e outro:
   - o leitor do arquivo e a gramática;
   - o arquivo `docs/conjunto_semente.toml`;
   - a troca da tabela pelo apontamento no protocolo;
   - a remoção de `sementes.json`, de `sincronizar` e das chaves do `config.toml`;
   - o autoteste.
3. Ajuste de PD01, do README e das skills.

Rollback: reverter o commit. A tabela e o `sementes.json` antigos ficam no histórico do
git.
