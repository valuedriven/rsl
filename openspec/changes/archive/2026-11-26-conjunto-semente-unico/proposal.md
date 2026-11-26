# Proposal

## Why

O conjunto-semente carrega uma divisão entre sementes de **validação** e de
**desenvolvimento** que só a SE4 foi classificada por evidência registrada; as outras nove
são "validação" por declaração. A divisão atravessa o esquema do arquivo, a leitura, a
aderência, a planilha, o relatório e os autotestes, e não entrega o que promete — a
independência do conjunto em relação à busca. O pesquisador decidiu que todo o conjunto é
de validação.

Ao mesmo tempo, o esquema carrega quatro campos que não produzem dado: `tipo`,
`alinhamento` e `eric` estão vazios nas 10 sementes, e `observacoes` guarda sobra editorial
que cabe no texto livre de `nota`. Mantê-los gera pendência sem conteúdo (PD01) e uma coluna
derivada sem uso na planilha.

A medida atual é 1/10 sementes recuperadas (1/9 de validação, 11,1%, Wilson 2,0%–43,5%,
REPROVADA). Esta change **não** corrige essa perda: ela é objeto de
`diagnostico-das-perdas-da-busca`. Esta change remove a divisão, enxuga o esquema e
simplifica o instrumento.

## What Changes

- Remover o campo `papel` do esquema do arquivo de sementes, da gramática, da leitura, da
  planilha de aderência, do relatório de configuração e dos autotestes. **BREAKING**:
  arquivo de sementes com `papel` passa a reprovar como campo desconhecido.
- Remover `tipo`, `alinhamento`, `eric` e `observacoes` do esquema; o conteúdo de
  `observacoes` (editores, evento, local, editora) é incorporado ao campo `nota`, e a
  planilha perde a coluna `tipo`. **BREAKING**: arquivo com qualquer um dos quatro campos
  passa a reprovar como campo desconhecido.
- Toda semente passa a ser de validação: a aderência decide sobre o conjunto, com um único
  numerador e denominador, e o intervalo de Wilson é calculado sobre ele.
- Remover o requisito "Conjunto de validação não vazio" e o relato separado de
  desenvolvimento; a planilha perde a coluna `papel`.
- Ajustar o protocolo (§Conjunto-semente), as skills `definir-conjunto-semente` e
  `testar-aderencia-das-expressoes`, o guia de procedimentos e o catálogo.
- Fora do escopo: substituir a SE4 e renumerar as sementes (change
  `substituicao-da-se4`); preencher `facetas` (PD20); anexar evidência às seis sementes sem
  arquivo; corrigir a aderência de 1/10.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `gramatica-do-protocolo`: o esquema do arquivo de sementes deixa de declarar `papel`,
  `tipo`, `alinhamento`, `eric` e `observacoes`, e o contrato exibido passa a ter 14
  campos.
- `leitura-do-protocolo`: a leitura não lê nem valida `papel`; não lê os quatro campos de
  conferência e sobra, cujo texto se incorpora a `nota`; caem o requisito de conjunto de
  validação não vazio e a pendência de `tipo`/`alinhamento`; a distribuição deixa de ser
  por papel.
- `derivacao-das-expressoes`: a aderência deixa de ser relatada por papel; o intervalo de
  Wilson passa a ser sobre o conjunto; a planilha perde as colunas `papel` e `tipo`.

## Impact

- **Código**: `src/rsl/gramatica.py`, `src/rsl/leitura.py`, `src/rsl/dados.py`,
  `src/rsl/busca/aderencia.py`, `src/rsl/sementes.py`, `src/rsl/relatorio.py` e os
  autotestes de busca, sementes, protocolo e gramática.
- **Documentos**: `docs/03_protocolo_estrategia_pesquisa.md`,
  `docs/procedimentos.md`, `docs/catalogo_de_apoio.md` (regenerado) e as duas skills.
- **Dados**: `docs/conjunto_semente.toml` (campos removidos e `observacoes` incorporada a
  `nota` nas 10 sementes), `data/semente_aderencia.csv` (colunas `papel` e `tipo`
  removidas, regenerada), `data/pendencias.json` (PD01 resolvida; PD18 e PD21 atualizadas)
  e `data/historico.md` (decisão).
- **Verificação**: `documentos conferir`, `dados conferir`, `aderencia planilhar`,
  `catalogo gerar` e `projeto autoteste`.
- **Não afeta**: os IDs das sementes, o Zotero e a coleção `sementes`.
