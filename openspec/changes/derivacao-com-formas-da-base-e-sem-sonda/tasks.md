# Tarefas

## 1. Corpus da derivação é a executada

- [x] 1.1 Em `src/rsl/busca/registro.py`, criar a seleção que separa as consultas válidas em
  lidas (expressão executada) e deixadas de fora, com o motivo: `sonda` ou `execução direta
  de conferência` (design, decisão 2). Verificar: sobre o registro atual, a seleção lê só
  BD2/EX1 e deixa de fora EX2 e EX3, como conferência, e EX4, como sonda.
- [x] 1.2 Usar a seleção em `derivar` (`derivacao.py`), no conjunto derivado de `fidelidade`
  (`fidelidade.py`) e em `aderencia` (`aderencia.py`), imprimindo as lidas e as deixadas
  de fora antes do resultado (spec: "Corpus da derivação é a executada", "Relato das
  execuções lidas"). Verificar: `busca derivar` grava a EB4 da Scopus com 133 registros em
  `contagens_busca.csv` e em `ordem_triagem.csv`, e `aderencia medir` deixa de contar a SE6.
- [x] 1.3 Acrescentar a `src/rsl/autoteste/busca.py` o caso "registro só da sonda" (design,
  decisão 3). Verificar: `python3 -m rsl projeto autoteste` passa, e o caso falha com a
  seleção desligada, ou seja, com a leitura de todas as execuções.

## 2. Casamento local pelos termos da base

- [x] 2.1 Em `src/rsl/busca/derivacao.py`, montar o vocabulário por base a partir de
  `Composicao`, somando as formas de número dos termos sem `*` e reprovando a flexão
  indecidível com o nome da base (design, decisão 1). `facetas_atingidas` passa a usar as
  facetas da base do registro. Verificar: na Scopus, o vocabulário da FCT3 contém
  `learning activities` e é igual à lista da STR3 da §3 do procedimento gerado, somadas as
  formas de número.
- [x] 2.2 Retirar de `padrao` o sufixo `(?:e?s)?` e atualizar a docstring dele. A docstring
  do pacote `busca` passa a dizer de onde vem o vocabulário e qual é o corpus. Verificar:
  `padrao("conceptual model")` não casa `conceptual modeles`, e `padrao("ontolog*")` casa
  `ontologies`.
- [x] 2.3 Acrescentar a `src/rsl/autoteste/busca.py` o caso "plural irregular", com a forma
  tomada da composição e não de literal (design, decisão 3). Verificar: o autoteste passa,
  e o caso falha com `padrao` antigo sobre os termos do protocolo.

## 3. Regeneração e conferência com dados reais

- [x] 3.1 Regenerar as saídas da Scopus: `busca derivar`, `conferencia fidelidade EB2` e
  `EB3`, `aderencia medir`, `conferencia sensibilidade scopus`. Verificar:
  - `sensibilidade_scopus.csv` é idêntico byte a byte ao gravado antes da mudança
    (copiá-lo antes para o diretório de rascunho);
  - a fidelidade de EB2 cai abaixo de 34,4%;
  - os registros que ainda divergem estão em `fidelidade_eb2.csv`, cada um com a causa
    conferida: âncora ou termo.
- [x] 3.2 Rodar `python3 -m rsl projeto autoteste`, `documentos conferir` e `dados
  conferir`. Verificar: os três saem OK.
- [x] 3.3 Conferir se `docs/procedimentos.md` descreve `busca derivar`, `conferencia
  fidelidade` ou `aderencia medir` de modo que esta mudança desmente. Se descreve, corrigir
  pelo guia e regenerar o catálogo (`catalogo gerar --gravar`). Verificar: `catalogo gerar`
  sai OK.

## Workflow follow-up

- Arquivar a change e sincronizar a spec `derivacao-das-expressoes`.
- Relatar ao pesquisador os novos resultados de fidelidade e aderência da Scopus. A decisão
  sobre eles é dele.
