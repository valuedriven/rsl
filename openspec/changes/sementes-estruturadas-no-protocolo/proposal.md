# Proposal

## Why

O conjunto-semente é lido da tabela `ID Semente | Semente | Bases`, e a coluna `Semente`
traz a referência inteira como texto livre. O leitor extrai autoria, ano, título e DOI por
expressão regular:

- o título termina "no primeiro ponto seguido de maiúscula ou de dígito" (`_titulo()`);
- o DOI tem de ser o último elemento da célula (`_doi()`).

Uma referência com ponto no título, com subtítulo ou com o DOI fora do fim é lida errado
**sem reprovar**. O título lido é o que liga a semente ao metadado em `sementes.json` e o
que o ensaio seco confronta com as facetas. As tarefas de conferência na fonte da change
`conjunto-semente-independente` (2.3) vão mexer nessas referências, e cada mudança arrisca
uma leitura silenciosamente errada.

Decisão do pesquisador (2026-11-19): o conjunto-semente passa a um bloco TOML estruturado
dentro do protocolo, lido com `tomllib`, da biblioteca padrão.

## What Changes

- **BREAKING (forma do protocolo):** a seção "Conjunto-semente" troca a tabela por um
  bloco cercado ```` ```toml ````, com uma tabela `[[semente]]` por estudo e os campos
  separados:
  - `id`, `autores` (lista), `ano`, `titulo`, `veiculo`;
  - `volume`, `numero`, `paginas` e `doi`, opcionais;
  - `bases` (lista de siglas);
  - `papel` (`desenvolvimento` ou `validação`), que vem da coluna `Papel` acrescentada por
    `conjunto-semente-independente`.
- **O leitor reprova, com PROTOCOLO_ILEGIVEL:**
  - bloco ausente, duplicado ou TOML inválido;
  - campo obrigatório ausente ou de tipo errado;
  - campo desconhecido;
  - base fora da tabela de bases;
  - numeração `SEn` fora de sequência;
  - DOI fora da forma `10.x/…`.
- **Os campos são transcritos da referência atual, sem completar dado algum de memória.**
  O que a referência não traz fica vazio e vira pendência de conferência.
- **A ligação com `sementes.json` (por DOI ou título) não muda.** O metadado autoral
  continua em `sementes.json`.
- **`rsl mostrar` exibe cada semente na forma de referência**, montada dos campos, para
  leitura humana.
- **Coordenação:** a coluna `Papel`, já implementada por `conjunto-semente-independente`,
  passa ao campo `papel` do bloco. As exigências daquela change continuam valendo sobre o
  campo: domínio fechado e conjunto de validação não vazio.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-do-protocolo`: "Conjunto-semente lido de tabela" é substituído pela leitura do
  bloco TOML, com campos estruturados e reprovação por campo.
- `gramatica-do-protocolo` (criada por `refatoracao-dos-scripts`): a seção
  "Conjunto-semente" passa a exigir um bloco TOML com o esquema de campos declarado, e não
  mais uma tabela.

## Impact

- `docs/03_protocolo_estrategia_pesquisa.md`, seção "Conjunto-semente": troca de forma,
  com o mesmo conteúdo. É emenda de forma, registrada em `data/historico.md`.
- `src/rsl/leitura.py`, `src/rsl/gramatica.py`, `src/rsl/relatorio.py` e o autoteste.
- `data/sementes.json`: sem mudança de esquema. `sementes sincronizar` tem de manter
  todas as ligações.
- `conjunto-semente-independente`: as exigências sobre a coluna `Papel` passam a valer
  sobre o campo `papel`. Se aquela change já estiver arquivada, as specs promovidas são
  ajustadas por esta.
- `.agents/skills/conjunto-semente/`: forma de registro da semente no protocolo.
- **Risco declarado:** um bloco cercado pode não sobreviver à exportação a partir de um
  editor de texto. Esse caso reprova (bloco ausente ou inválido), em vez de passar em
  silêncio.
- **Depende de:** `refatoracao-dos-scripts` arquivada.
