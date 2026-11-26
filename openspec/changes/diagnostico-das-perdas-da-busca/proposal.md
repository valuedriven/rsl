# Proposta

## Por quê

As primeiras execuções da Scopus (BD2/EX1 a EX4, em 2026-11-25) reprovaram nas duas
conferências que medem perda. Nos dois casos, o projeto mede quanto se perde, mas não ajuda
a descobrir por quê.

1. **Aderência.** 1 das 6 sementes esperadas na Scopus foi recuperada. As outras 5 não
   aparecem nem na exportação da sonda (EB5). O procedimento manda aplicar a anatomia da
   perda: quatro consultas por semente, restritas ao DOI. Hoje isso tem três problemas:
   - a tabela da anatomia é prosa escrita à mão em `notas_sementes.md`, com os marcadores
     🟦 e 🟨 no lugar das strings;
   - a consulta 3 da tabela não acumula os filtros da consulta 2, embora a skill exija que
     cada consulta acrescente uma restrição à anterior;
   - nada lê os resultados: o pesquisador submete até 20 consultas e atribui a causa a olho.
2. **Sensibilidade.** 30 dos 53 registros da amostra de EB5 \ EB4 são elegíveis (56,6%),
   muito acima do limite de 15%. O protocolo exige reconsiderar a EB4, mas não há
   instrumento que diga o que esses elegíveis têm que a EB4 não alcança, nem quanto cada
   ampliação do vocabulário custaria.

A decisão de emenda precisa dessas duas respostas, e convém decidir com as duas na mão: a
mesma emenda pode ter de corrigir a perda das sementes e a perda de sensibilidade, e assim a
base é reexecutada uma vez só.

## O que muda

- **Anatomia da perda montada e lida pelo projeto.** `aderencia diagnosticar <base>`:
  - toma as sementes esperadas na base que a executada não recuperou;
  - monta, a partir da composição da base, uma consulta por nível com os DOIs dessas
    sementes agrupados por `OR`. Os níveis são cumulativos:
    1. só os DOIs;
    2. mais os filtros;
    3. mais as âncoras sem proximidade;
    4. mais a proximidade;
  - o nível cuja expressão já tem execução registrada (a sonda) se lê da exportação
    registrada, em vez de ser submetido;
  - recebe a exportação e o retorno de cada nível submetido, atribui a cada semente a causa
    da perda (o primeiro nível em que o DOI dela some) e grava o resultado.

  A submissão continua manual, no navegador do pesquisador.
- **Restrição por DOI declarada na fonte.** A forma da restrição por DOI difere entre as
  bases. Por isso passa a ser declarada na fonte de cada uma, em `[composicao]`, como os
  demais elementos de sintaxe. A base sem a declaração não é diagnosticada, e a recusa nomeia
  o campo que falta.
- **Análise da perda da sensibilidade.** `conferencia simular <base>`, sobre a amostra já
  classificada e a exportação da sonda:
  1. relata quais facetas o casamento local reconhece em cada registro da amostra;
  2. lista os termos candidatos, tirados das palavras-chave dos registros elegíveis. Para
     cada termo informa quantos elegíveis e quantos não elegíveis da amostra ele alcança e
     quantos registros acrescentaria à executada;
  3. com `--termo`, simula a executada ampliada com os termos dados: elegíveis da amostra
     recuperados e registros acrescentados.

  O comando não altera string, protocolo nem fonte.
- **Fragmentos de prosa.** A tabela da anatomia, escrita à mão em `notas_sementes.md`, dá
  lugar à remissão ao comando, e os procedimentos são regenerados.

Fora do escopo:

- consultar a base por programa: não há via de acesso programático verificada, e as
  consultas seguem no navegador do pesquisador;
- base de execução particionada: o diagnóstico recusa, nomeando a base;
- decidir a emenda, escolher termos ou alterar a executada. Isso é decisão do pesquisador, e
  o comando só informa;
- preencher as colunas manuais da planilha de aderência: o comando sugere, e quem preenche é
  o pesquisador.

Pré-requisito: a change `derivacao-com-formas-da-base-e-sem-sonda` (implementada, ainda não
arquivada). Esta change usa o vocabulário por base e a seleção do corpus introduzidos nela.

## Capacidades

### Novas capacidades

- `anatomia-da-perda`: as consultas por nível montadas da composição, a restrição por DOI
  declarada na fonte, a leitura das exportações e a atribuição da causa da perda por semente.
- `analise-da-sensibilidade`: o casamento local na amostra classificada da sonda, os termos
  candidatos e a simulação da executada ampliada sobre a exportação da sonda.

### Capacidades modificadas

Nenhuma. Os comandos novos seguem os requisitos que já existem de convenção de nomes
(`interface-de-comando`) e de ancoragem no guia (`catalogo-de-apoio`), sem alterá-los.

## Impacto

- Código:
  - `src/rsl/busca/anatomia.py` e `src/rsl/busca/simulacao.py` (novos);
  - `src/rsl/gramatica.py`: campo `doi` em `[composicao]`;
  - `src/rsl/__main__.py`: os dois subcomandos;
  - autoteste: `src/rsl/autoteste/busca.py`.
- Configuração: `config.toml`, `[saidas]`: `anatomia`, `anatomia_consultas`, `candidatos`.
- Fontes: `[composicao] doi` nas bases que o declararem, e os `notas_sementes.md`.
- Documentação: guia de procedimentos (`docs/procedimentos.md`), que ancora os dois comandos,
  e o catálogo regenerado.
- Saídas novas: `anatomia_<base>.csv`, `anatomia_consultas_<base>.csv`,
  `candidatos_<base>.csv`.
