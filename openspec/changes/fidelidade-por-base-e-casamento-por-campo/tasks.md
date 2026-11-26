# Tarefas

## 1. Fidelidade por base

- [x] 1.1 `conferencia fidelidade BASE EXPRESSAO [ARQUIVO]`, com o derivado só da executada da base e a execução direta registrada quando não há arquivo; verificado com `conferencia fidelidade -h` e com a conferência da WoS e da Scopus
- [x] 1.2 `[saidas] fidelidade` com `{base}` e `{expressao}`; a configuração sem um deles reprova; verificado no autoteste de configuração (dois casos)
- [x] 1.3 Autoteste: a fidelidade de uma base não conta o registro de outra; sem arquivo, lê a execução registrada; verificado que o caso falha com a mistura reintroduzida

## 2. Casamento por trecho

- [x] 2.1 `segmentos_do` e `facetas_atingidas` por trecho, com o separador compartilhado com os leitores; verificado no registro doi:10.3390/computers10100128 da WoS, que deixa de ser derivado na EB3
- [x] 2.2 Autoteste de fronteira (entre palavras-chave e entre título e resumo, com controle do termo inteiro); verificado que os dois casos falham com o texto único reintroduzido

## 3. Documentos

- [x] 3.1 Guia (`docs/procedimentos.md`), `README.md` e skill `avaliar-resultados-da-busca` (limiar configurado, comparação por base); `catalogo gerar` sem divergência e `documentos conferir` aprovado
- [x] 3.2 `projeto autoteste` com todos os casos aprovados

## Relato

Conferências refeitas em 2026-11-26 com o código corrigido, sobre as execuções registradas
em `data/registro_execucao.json` (BD1/EX1–EX4, BD2/EX1–EX4): fidelidade da EB2 e da EB3 na
WoS e na Scopus sem divergência — os conjuntos derivados coincidem com as execuções
diretas. Os números se recalculam com `python3 -m rsl conferencia fidelidade <base> <EBn>`.
