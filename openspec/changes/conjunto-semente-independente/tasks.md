# Tasks

## 1. Decisões do pesquisador (antes de qualquer aderência registrada)

- [ ] 1.1 Obter a decisão D1: (a) separar desenvolvimento e validação, (b) conjunto único com aderência relatada com e sem as sementes que orientaram termos, ou (c) conjunto único com limitação declarada. Fora de (a), remover `specs/`, declarar `skip_specs: true`, pular os grupos 3 e 4 e verificar com `openspec validate conjunto-semente-independente`
- [ ] 1.2 Obter a decisão D2: tamanho-alvo do conjunto e manutenção do limiar. Verificar que a decisão consta em `data/historico.md`, com o fundamento
- [ ] 1.3 Classificar cada semente atual como desenvolvimento ou validação pelo critério do design (D-b), com a SE4 em desenvolvimento por registro. Verificar que a classificação está no histórico com data anterior a qualquer execução em `data/registro_execucao.json`

## 2. Conferência na fonte (independente de D1)

- [ ] 2.1 Conferir na fonte a indexação de cada uma das 10 sementes nas quatro bases (skill `conjunto-semente`, sem automação de interface que os termos de uso não permitam), registrando a data e a fonte de cada conferência. Verificar que nenhuma célula foi preenchida de memória
- [ ] 2.2 Corrigir a coluna "Bases" do protocolo e a seção 5 das fichas conforme 2.1. Verificar com `python3 src/protocolo.py --conferir` que a distribuição por base exibida bate com a conferência
- [ ] 2.3 Conferir na fonte autoria, título, veículo, ano e DOI de cada semente (skill `conferir-referencia`), incluindo o DOI do capítulo da SE10, se existir, e preencher o metadado em `data/sementes.json`. Verificar com `--pendencias` que nenhuma semente resta com verificação pendente sem motivo registrado

## 3. Papel no protocolo (se D1 a)

- [ ] 3.1 Acrescentar a coluna `Papel` à tabela do conjunto-semente, com a classificação de 1.3 e as sementes novas aprovadas pelo pesquisador, e, no mesmo passo, a leitura em `src/protocolo.py` que a exige e reprova papel ausente, fora do domínio ou conjunto de validação vazio. Verificar com `--conferir` que o protocolo passa
- [ ] 3.2 Acrescentar ao autoteste papel ausente, papel fora do domínio e conjunto sem validação. Verificar com `--conferir --autoteste` que cada caso reprova pelo motivo esperado
- [ ] 3.3 Exibir em `--mostrar` a contagem por papel, total e por base. Verificar a saída contra a tabela

## 4. Aderência por papel (se D1 a)

- [ ] 4.1 Acrescentar a coluna `papel` à planilha de `gen_semente.py`. Verificar que cada linha gerada traz o papel da tabela do protocolo
- [ ] 4.2 Separar em `--aderencia` o relato de validação e o de desenvolvimento, comparar só o de validação ao limiar e mostrar o intervalo de Wilson a 95%. Verificar com dados sintéticos que 8/10 resulta em 80% (49,0%–94,3%) e que o desenvolvimento não compensa a validação
- [ ] 4.3 Atualizar as skills `teste-de-aderencia` e `conjunto-semente` e o README (M3/E2, aderência) para o relato por papel. Verificar que o README diz qual aderência decide a passagem

## 5. Integração

- [ ] 5.1 Registrar a emenda do conjunto-semente em `data/historico.md` e rodar `python3 src/protocolo.py --conferir --autoteste` e `python3 src/derivar_expressoes.py --autoteste`. Verificar que todos os casos executados têm o resultado esperado

## Workflow follow-up

- Coordenar com `revisao-das-strings-por-faceta`: termo novo motivado por uma semente a reclassifica como desenvolvimento.
- Arquivar a change depois da revisão.
