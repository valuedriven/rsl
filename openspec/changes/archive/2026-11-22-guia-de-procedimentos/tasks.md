# Tasks

## 1. Guia de procedimentos (`docs/procedimentos.md`)

- [x] 1.1 Criar `docs/procedimentos.md` com abertura curta (modelo, origem da estrutura fornecida pelo pesquisador e não conferida na tese, remissão ao plano §1.4) e os 4 módulos e 14 etapas como títulos; verificar que os títulos de etapa coincidem com o plano §1.4
- [x] 1.2 Redigir os 63 passos na ordem da estrutura fornecida, cada um como item sem numeração e sem a palavra "passo", verbo no infinitivo + objeto na forma genérica (design D2); verificar a contagem por etapa (M1: 4/3/7/3/3; M2: 3/5; M3: 8/7/8/3; M4: 2/3/4 = 63) e que nenhum item começa por ordinal ou por "Passo"
- [x] 1.3 Acrescentar a cada passo, quando aplicável, os sub-itens Fonte (documento e seção), Script e Skill; verificar que toda skill citada existe em `.agents/skills/` e que toda seção citada existe no documento
- [x] 1.4 Transcrever a sinopse de cada comando a partir de `python3 -m rsl <subcomando> -h`, no passo em que é usado, com todos os parâmetros (`termos validar SIGLA|todos [--faceta N]`, `busca registrar BASE EXPRESSAO ARQUIVO [--retorno N] [--data-hora ISO] [--justificar TEXTO]`, `busca sensibilidade [BASE]` etc.); verificar comando a comando contra `-h` que nenhum parâmetro falta ou sobra
- [x] 1.5 Em M3/E2, incluir a tabela de índices (design D3) com o que mede, numerador/denominador, limiar e origem, script ou "manual" e saída; verificar cada índice automático no módulo que o calcula em `src/rsl/busca/` e cada saída em `[saidas]` do `config.toml`, e que nenhum valor de limiar está transcrito
- [x] 1.6 Incluir a seção de conferências transversais (`conferir`, `conferir-dados`, `autoteste`, `mostrar`, `gramatica`, `pendencias`) com quando executar e o que cada uma relata em uma linha; verificar que não repete regra das specs
- [x] 1.7 Verificar que o guia não copia conteúdo do protocolo, do plano ou do `config.toml` (sem fórmula de expressão, faixa de critérios, valores de limiar ou listas de termos): procurar por `STR1`, `CE1`, `%` e números de limiar

## 2. README reduzido

- [x] 2.1 Inventariar cada bloco do README atual e anotar onde a informação já está (artefato e seção) ou que é exclusiva; verificar que todo bloco exclusivo tem destino no README novo ou no guia
- [x] 2.2 Reescrever o `README.md` conforme design D1: identificação, como executar, mapa único dos caminhos com quem escreve, códigos de saída, três registros, precedência, convenções, uso de IA e remissão a `docs/procedimentos.md`; preservar a versão corrente do pesquisador (alteração staged da seção "Uso de IA"); verificar que a tabela de códigos coincide com a saída de `python3 -m rsl` (spec `interface-de-comando`)
- [x] 2.3 Verificar que nenhum caminho aparece mais de uma vez no mapa e que todo caminho citado existe ou é declarado como criado sob demanda

## 3. Remissões das skills

- [x] 3.1 Atualizar as remissões ao README em `revisao-geral-do-projeto`, `teste-de-aderencia` ("seção Scripts"), `ficha-de-busca-por-base`, `criterios-de-elegibilidade`, `validacao-vocabulario-controlado` e `registrar-decisao` para o lugar novo de cada informação; verificar com `grep -rn README .agents/skills` que toda remissão restante aponta para seção existente

## 4. Pendências

- [x] 4.1 Apresentar ao pesquisador as divergências do design D5 e a substituição das remissões por ordinal (D4), cada uma com origem, o que bloqueia e ação sugerida; registrar em `data/pendencias.json` somente as que ele aprovar, e verificar com `python3 -m rsl conferir-dados`

## 5. Integração

- [x] 5.1 Executar `python3 -m rsl conferir`, `conferir-dados` e `autoteste` e verificar que os códigos de saída são os mesmos de antes da change (nenhum código ou dado foi alterado). Ressalva de 2026-11-22: por decisão do pesquisador na tarefa 4.1, código, configuração e dados mudaram (CE10 "Não aplicável" e retirada do ASReview); as três conferências foram reexecutadas depois e os códigos continuam 0, 5 e 6
