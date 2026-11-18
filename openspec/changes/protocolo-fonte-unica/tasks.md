# Tasks

## 1. Protocolo na forma final

- [x] 1.1 Copiar a Nota de emenda (v2, 2026-11-17) integralmente, com data, para `data/historico.md` e verificar que o texto copiado é idêntico ao do protocolo (`diff`)
- [x] 1.2 Reescrever o item 7 da Nota (operadores de proximidade e restrição por campo) em uma linha na seção "Expressões de busca" e verificar que a regra consta fora da Nota
- [x] 1.3 Remover do protocolo o aviso "Versão 2" (topo), o bloco "Em relação à versão 1" das strings, a remissão "ver Nota de emenda", a Nota e a menção à Nota na regra de ajuste; verificar que `grep -niE "vers[aã]o [12]|v[12]\b|nota de emenda"` não acha nada no arquivo
- [x] 1.4 Registrar em `data/historico.md` a decisão de 18/11/2026 hoje citada no bloco das strings (`ontological engineering`, `teaching practice`, `aprendiz`) e verificar a entrada
- [x] 1.5 Resumir as explicações do protocolo (Detalhamento de EB1–EB5, Acervos especiais e pessoais, regra de ajuste, triagem, assistência de IA), preservando intactas as colunas "Justificativa" de CE e BD e os textos de que o leitor depende (D6); verificar com `git diff` que as colunas Justificativa não mudaram
- [x] 1.6 Propor ao pesquisador a entrada de `data/historico.md` sobre a criação da seção "Instrumentos para controle terminológico" e o fim da dispensa de validação de FCT4 (decisão do ReT, já aplicada no protocolo) e gravá-la após confirmação

## 2. config.toml e precedência

- [x] 2.1 Registrar os idiomas do UNESCO Thesaurus (inglês e espanhol, informados pelo pesquisador) e conferir na fonte os do TBCI, do ERIC Thesaurus e do Brased/INEP, registrando a evidência; o que não puder ser conferido fica como pendência declarada, não como padrão presumido
- [x] 2.2 Criar `config.toml` na raiz com o caminho do protocolo e padrão para todo parâmetro de D3, comentado no próprio arquivo, e verificar que `python3 -c "import tomllib; tomllib.load(open('config.toml','rb'))"` carrega
- [x] 2.3 Implementar em `protocolo.py` a carga do `config.toml` (só biblioteca padrão) e a precedência protocolo > padrão, com origem por valor; erro explícito para arquivo ausente, TOML inválido, Python anterior ao 3.11 ou chave ausente; verificar com autoteste que chave ausente reprova e que trecho ilegível do protocolo reprova em vez de cair no padrão
- [x] 2.4 Substituir `DOC`, `FICHAS`, caminhos de `data/`, `CAMPOS_VALIDACAO`, `CAMPOS_AUTORAIS` e o mínimo de termos pela leitura resolvida; fazer `derivar_expressoes.py`, `validar_termos.py` e `gen_semente.py` obterem o caminho do protocolo via `protocolo.py`; incluir em `--mostrar` o valor e a origem de cada parâmetro; verificar que `--mostrar` exibe a origem, que os valores coincidem com os atuais e que, apontando `protocolo` para um caminho inexistente, os scripts falham nomeando a chave

## 3. Coerência em lugar de valor fixado

- [x] 3.1 Ler do protocolo os papéis (executada e sonda), as âncoras, o recorte, o limiar de aderência e a faixa de sensibilidade; verificar com `--mostrar` que os valores lidos são EB4, EB5, FCT1/FCT2, 2017, 80% e 5%/15%, com origem "protocolo"
- [x] 3.2 Substituir `previsto`, `COMPOSICAO`, `exec_ != "EB4"`, `sonda != "EB5"`, recorte 2017, limiar 0,80, quatro QER, mínimo de oito sementes e dimensões fixas pelas relações de coerência de D2; verificar que `--conferir` passa no protocolo atual, inclusive sem o defeito "Idioma(s)"
- [x] 3.3 Atualizar o autoteste com um defeito injetado por relação de coerência (âncora faltando, executada ≠ união, sonda ≠ âncoras, termo da STR fora do quadro, dimensão ausente, faixa incoerente) e por regra de precedência; verificar que `--conferir --autoteste` passa e que cada defeito reprova
- [x] 3.4 Verificar com `grep` que `src/protocolo.py` não contém valor de parâmetro fora do autoteste (`0.80`, `2017`, `"EB4"`, `"TBCI"` etc.)

## 4. Cobertura por base sem listas da emenda

- [x] 4.1 Remover `RETIRADOS_V2`, `ACRESCENTADOS_V2` e `_vigente`; calcular o esperado como STR filtrada por idioma e camada declarados (D1) e verificar que a cobertura de cada ficha dá os mesmos números de antes
- [x] 4.2 Reprovar termo da base que só exista no quadro, inclusive em flexão, e substituir os autotestes "emenda v2" por "termo do quadro fora da STR devolvido à base" (literal e em flexão na BRAPCI); verificar que reprovam
- [x] 4.3 Remover de `src/protocolo.py` toda referência a versão ou emenda (docstring, comentários, mensagens) e verificar que `grep -nE "v1\b|v2\b|_V2|emenda v2" src/` não acha nada

## 5. Validação terminológica e limiares de derivação

- [x] 5.1 Ler a seção "Instrumentos para controle terminológico" (D4), resolver cada nome pelo `config.toml` e reprovar nome não mapeado, nome ambíguo e faceta sem linha; deixar de ler a linha de instrumentos das tabelas; remover `INSTRUMENTO_POR_IDIOMA`, `STATUS_LIVRE_DECISAO` e `JUSTIFICATIVA_LIVRE`; verificar com autoteste que cada caso reprova
- [x] 5.2 Ajustar `validar_termos.py` para planejar por faceta e por idioma do instrumento, gerar pendência manual para instrumento `manual` e não usar mais o estatuto "termo livre por decisão"; verificar com o planejamento a seco (sem rede) que FCT1 → TBCI (pt) e UNESCO (idiomas do padrão), e FCT2–FCT4 → ERIC e Brased/INEP como pendência manual e UNESCO
- [x] 5.3 Trocar `LIMITE_DIVERGENCIA` e `LIMITE_SENSIBILIDADE` em `derivar_expressoes.py` pela leitura via `protocolo.py`, remover "Protocolo v2" do docstring e verificar que as mensagens de limite imprimem 10% e 5%/15%
- [x] 5.4 Verificar que `gen_semente.py` não usa constante removida (`grep`) e que roda sem erro

## 6. Documentos, README e skills

- [x] 6.1 Resumir as explicações de `docs/01_plano.md`, `docs/02_protocolo_informacoes_gerais.md` e das quatro fichas, preservando qualquer coluna ou seção "Justificativa"; verificar com `grep -niE "vers[aã]o [12]|v[12]\b"` que não há referência de versão
- [x] 6.2 No README, remover contagens de artefatos e estado observado (número de skills e de scripts, "não existem hoje", "sem conteúdo no momento", data de descarte, retorno de exemplo), as menções à emenda v2 e a de FCT4 como termo livre por decisão; documentar o `config.toml`, a regra de precedência e o Python 3.11+ como requisito; verificar com `grep`
- [x] 6.3 Ajustar `.agents/skills/ficha-de-busca-por-base/SKILL.md` (o retirado é descontado por não estar na STR, e não por lista no script) e `.agents/skills/validacao-vocabulario-controlado/SKILL.md` (FCT4 deixa de ser termo livre por decisão; instrumentos vêm da seção do protocolo); verificar com `grep -n "lista de retirados\|termo livre por decisão"` que não sobra ocorrência

## 8. Consistência entre documentos (pedido do pesquisador após a revisão)

- [x] 8.1 Gravar em `data/historico.md` a entrada da tarefa 1.6, aprovada pelo pesquisador, e verificar a entrada
- [x] 8.2 Limiares fora do protocolo por remissão ao `config.toml` (plano 6.2, 7 e 8.2; fichas; README), com `calibracao_triagem` novo em `[padroes]` e divergência da fidelidade com padrão 10%; verificar com `grep` que plano, fichas e README não trazem percentual de limiar e que `--mostrar` exibe `calibracao_triagem`
- [x] 8.3 Referências a critérios por número antigo atualizadas (protocolo e README: "critério 4" → CE5, "critério 5" → CE6) e referência do plano a "critérios de exclusão (i) e (b)" retirada; verificar com `grep "critério [0-9]"`
- [x] 8.4 Plano sem referência às expressões de busca (2.1, 3.3 e 6.2), por remissão ao protocolo; verificar com `grep`
- [x] 8.5 Remissões das questões secundárias corrigidas de `docs/02`, Etapa 2, para `docs/03`, Questão de revisão; verificar com `grep`

## 7. Integração

- [x] 7.1 Rodar `--conferir`, `--conferir --autoteste`, `--mostrar` e `--pendencias` de `protocolo.py` num ambiente sem pacotes extras (`python3 -I -S` ou venv limpo) e verificar que passam; registrar a saída de `--conferir-dados`, que reprova enquanto `sementes.json` e `registro_execucao.json` não existirem, o que não é efeito desta mudança
