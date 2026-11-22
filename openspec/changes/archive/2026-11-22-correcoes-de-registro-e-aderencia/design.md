# Design

## Context

Ver `proposal.md` (Why) e o spec delta de `derivacao-das-expressoes`.

- `src/rsl/sementes.py` monta todas as linhas de `semente_aderencia.csv` com as colunas
  manuais vazias e grava com `open("w")`.
- `busca sensibilidade` (`src/rsl/busca/sensibilidade.py`) já conserva uma coluna manual,
  `elegivel`, que lê do arquivo anterior por `chave` antes de regravar. É o precedente do
  projeto.
- Retirar uma semente **renumera as seguintes** (skill `conjunto-semente`, "Retirar uma
  semente"). Por isso `id` sozinho não identifica a semente entre duas gravações: depois
  da retirada de SE3, o `SE3` antigo e o `SE3` novo são estudos diferentes.
- `busca aderencia` não lê a planilha. A coluna `indexada` só aparece no texto que ele
  imprime e na docstring, e ali está escrita `indexado`.
- O parser (`src/rsl/__main__.py`) já converte erro de argumento em USO, com a linha final
  que nomeia o código.

## Goals / Non-Goals

**Goals:**

- A regravação nunca descarta em silêncio conteúdo manual não vazio.
- O nome das colunas manuais tem um único lugar no código, usado pelo gerador, pela
  preservação e pelo texto de `busca aderencia`.

**Non-Goals:**

- Migrar automaticamente o preenchimento de uma semente renumerada para o `id` novo. A
  correspondência entre `id` antigo e novo está no histórico, e a transferência é do
  pesquisador.
- Conferir o conteúdo das colunas manuais (domínio de `indexada`, forma das datas).
- Alterar `busca sensibilidade`.

## Decisions

**D1. Casamento por `id` e `base`, confirmado pelo título.** A linha anterior casa com a
nova quando `id` e `base` coincidem e o título normalizado (a mesma `normaliza()` do
ensaio seco) é igual.

- Alternativa: só `id` e `base`, como a sensibilidade faz com `chave`. Rejeitada: depois de
  uma renumeração, isso atribuiria o preenchimento de uma semente a outra, sem que nada
  reprovasse. É o mesmo defeito que a skill aponta na evidência bruta.
- Alternativa: DOI e base. Rejeitada: o DOI pode faltar, e falta de DOI é pendência, não
  reprovação.
- Custo aceito: corrigir um erro de grafia no título de uma semente que já tem
  preenchimento faz a regravação ser recusada (D2). O pesquisador corrige o título na
  planilha também e regrava.

**D2. Recusa total em vez de descarte ou arquivo à parte.** Se algum conteúdo manual não
vazio ficaria sem destino, nada é gravado, e a saída lista cada `id` × `base` × coluna.

- Alternativa: descartar e avisar. Rejeitada: aviso no terminal não impede a perda.
- Alternativa: mover as linhas órfãs para `data/arquivo/`. Rejeitada por ora: cria um
  segundo lugar de dado de aderência, e a retirada de semente é rara e já exige trabalho
  manual (quatro passos na skill).
- O código é REPROVADO, por analogia com `busca registrar` recusado: a planilha anterior é
  legível, e a condição de aceite da regravação falhou. CSV ilegível é DADOS.

**D3. Colunas manuais declaradas uma vez.** `colunas()` passa a distinguir as colunas
derivadas das manuais com uma marca na própria declaração. A preservação, a recusa e o
texto de `busca aderencia` leem essa declaração. Assim o nome `indexada` fica num só
lugar e PD29 não tem como voltar. A planilha não muda de forma: mesmas colunas, mesma
ordem, mesmo separador e codificação `utf-8-sig`.

**D4. Coluna ausente na planilha anterior é coluna vazia.** Uma planilha anterior sem uma
das colunas manuais é lida como se a coluna estivesse vazia, porque não há o que perder.
Uma coluna fora do esquema só causa recusa se tiver valor.

**D5. `--retorno` com `required=True`.** O parser passa a recusar a falta. A verificação
dentro de `registrar()` continua, porque é o contrato da função e não depende de quem a
chama. A mensagem de USO é a do parser.

**D6. Mensagem de registro ausente a partir do nome do subcomando.** A orientação de
`pendencias` passa a "registre a primeira execução com `python3 -m rsl busca
registrar`". O teste do autoteste não depende da frase inteira: confere só que a linha
nomeia o subcomando.

## Risks / Trade-offs

- [Gravação interrompida no meio deixa a planilha truncada] → gravar num arquivo
  temporário no mesmo diretório e substituir o anterior só depois de fechado o temporário.
- [Pesquisador edita a planilha numa planilha eletrônica que troca o separador ou a
  codificação] → a leitura usa o mesmo dialeto da gravação. Arquivo que não lê vira DADOS
  (D2), e não perda.
- [Correção de grafia no título leva à recusa] → a `normaliza()` do projeto ignora caixa,
  acento, espaço e pontuação. Só uma diferença de letra ou de dígito causa recusa. É
  aceitável: a recusa é ruidosa, e a perda seria silenciosa.

## Migration Plan

A planilha atual tem todas as colunas manuais vazias. A primeira execução depois da
mudança é igual à de hoje, sem nada a migrar. Para desfazer, basta reverter o commit,
porque a forma do arquivo não muda.
