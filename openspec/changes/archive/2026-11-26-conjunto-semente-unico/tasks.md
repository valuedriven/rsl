# Tasks

## 1. Esquema, leitura e protocolo

- [x] 1.1 Remover `papel`, `tipo`, `alinhamento`, `eric` e `observacoes` de `docs/conjunto_semente.toml` (10 tabelas, com o texto de `observacoes` transcrito para `nota`), da gramática (`C_PAPEL`, `D_PAPEL`, `PAPEL_*`, `C_TIPO`, `C_ALINHAMENTO`, `C_ERIC` e `C_OBSERVACOES`), da leitura, das pendências (`CAMPOS_PENDENTES` em `dados.py`) e da exibição de `relatorio.py`; verificar com `python3 -m rsl documentos gramatica` (14 campos), `python3 -m rsl configuracao mostrar` e `python3 -m rsl documentos conferir` aprovado
- [x] 1.2 Atualizar os autotestes de sementes, protocolo e gramática: remover os casos de papel e de `tipo`/`alinhamento` e cobrir os cinco campos retirados como desconhecidos; verificar com `python3 -m rsl projeto autoteste` e com a reintrodução de cada um numa cópia do arquivo, que deve reprovar
- [x] 1.3 Atualizar o protocolo (§Conjunto-semente) e a skill `definir-conjunto-semente` (§4, §7 e §8): remover a divisão por papel, o campo `observacoes` e os campos `tipo`, `alinhamento` e `eric`, e a linha `tipo` da planilha; verificar que não restam esses campos no texto de semente e que `python3 -m rsl documentos conferir` aprova
- [x] 1.4 Registrar a decisão em `data/historico.md` (conjunto único de validação; campos retirados; `observacoes` incorporada a `nota`) e atualizar `data/pendencias.json`: remover PD01, resolvida pela retirada de `tipo` e `alinhamento`, e atualizar PD18 e PD21 (PD20 mantida); verificar com `python3 -m rsl projeto pendencias`

## 2. Aderência, planilha e guia

- [x] 2.1 Reescrever `src/rsl/busca/aderencia.py` para um único conjunto: uma proporção, um denominador, o intervalo de Wilson sobre ele e uma única decisão pelo limiar; verificar com `python3 -m rsl aderencia medir` (um relato, 10 sementes, sem seção de desenvolvimento)
- [x] 2.2 Remover as colunas `papel` e `tipo` de `src/rsl/sementes.py` e a contagem de alinhamento do resumo; regenerar a planilha; verificar com `python3 -m rsl aderencia planilhar` (cabeçalho sem `papel` nem `tipo`, 40 linhas, colunas manuais vazias e preservadas)
- [x] 2.3 Atualizar os autotestes de busca, protocolo, sementes e dados (relato único com Wilson; distribuição sem papel; planilha sem `tipo`, com o caso de coluna derivada passando a `verificacao`; pendência sem `tipo`/`alinhamento`); verificar com `python3 -m rsl projeto autoteste`
- [x] 2.4 Atualizar a skill `testar-aderencia-das-expressoes` (§1 e §2) e o guia `docs/procedimentos.md` (remover "Aderência de desenvolvimento" e "por papel"); regenerar `docs/catalogo_de_apoio.md` e verificar com `python3 -m rsl catalogo gerar` sem divergência

## 3. Verificação integrada

- [x] 3.1 Rodar `python3 -m rsl documentos conferir`, `python3 -m rsl dados conferir`, `python3 -m rsl aderencia planilhar`, `python3 -m rsl catalogo gerar` e `python3 -m rsl projeto autoteste`; verificar os cinco com código 0
- [x] 3.2 Conferir que o arquivo de sementes não tem `papel`, `tipo`, `alinhamento`, `eric` nem `observacoes`, e que os textos de semente não os citam; verificar com `grep -n` no arquivo, nas fontes dos procedimentos, na skill e nos deltas, e revisar o diff
