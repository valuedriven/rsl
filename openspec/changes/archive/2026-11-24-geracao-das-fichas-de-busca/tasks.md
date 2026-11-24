# Tasks

## 0. Pré-condição

- [x] 0.1 Confirmar que `strings-geradas-do-quadro` e `namespace-de-comandos-e-skills` estão
  arquivadas e que as specs principais trazem `Plural declarado por base`, `Termo só no
  singular relatado` e o requisito "Ponto de entrada único" com os nomes canônicos.
  Verificar com `openspec show cobertura-por-base --type spec`, `openspec show
  interface-de-comando --type spec` e `openspec validate geracao-das-fichas-de-busca
  --strict`.

## 1. Fonte do procedimento (D2)

- [x] 1.1 Declarar na gramática:
  - o esquema de `procedimento.toml` (tabelas, campos, tipos, exigências e domínios de D2);
  - os fragmentos admitidos e a forma de cada um;
  - o esquema do resultado de sondagem;
  - o do arquivo de exceções.

  Exibi-los em `documentos gramatica`, com o grupo da fonte no lugar da forma do markdown do
  procedimento. Verificar pelos cenários de `gramatica-do-protocolo`.
- [x] 1.2 Implementar o leitor da fonte, localizado por `[documentos] procedimento_fonte`.
  Ele tem estas validações:
  - esquema;
  - medição com citação;
  - cláusula do filtro;
  - fragmentos (nome desconhecido, títulos proibidos, linha `- Execução:`);
  - PROTOCOLO_ILEGIVEL por base.

  Acrescentar a chave ao `config.toml` e à leitura da configuração. Verificar pelos
  cenários de `fonte-do-procedimento`.
- [x] 1.2a Declarar as categorias mínimas de sintaxe na gramática e exigir que cada uma tenha
  elemento em cada base. Implementar a marca `PENDENTE` em campos e fragmentos, com a lista
  completa das marcas numa só reprovação. Verificar pelos cenários "Categoria esquecida" e
  "Fonte recém-iniciada".
- [x] 1.3 Retirar de `fichas.py` e da gramática a leitura do markdown do procedimento:
  cabeçalhos exatos, reconhecimento de campo e de filtro por texto e subseções ignoradas.
  Verificar com `grep -n -E 'TS=|TITLE-ABS-KEY|abstract:' src/rsl/*.py`, que não deve achar
  nada fora do autoteste.

- [x] 1.4 Criar `python3 -m rsl procedimentos iniciar <sigla>` (D9). Ele usa um modelo
  textual na gramática, preenche o derivável e marca `PENDENTE` o resto. Recusa a base fora
  do protocolo e a pasta existente, e grava de forma atômica. Verificar pelos cenários de
  "Início da fonte de uma base nova" e "Início recusado", numa cópia do protocolo com uma
  base fictícia.

## 2. Roteiro de sondagens (D5)

- [x] 2.1 Validar `[[sondagens]]`:
  - campos;
  - leitura inconclusiva;
  - estado no domínio;
  - elementos existentes;
  - ciclo em `depende_de`;
  - elemento `nao_verificado` com `sondagem` ou `sem_sondagem`.

  Relatar a sondagem sem elemento. Verificar pelos cenários de `sondagens-por-base`.
- [x] 2.2 Aceitar `bases.BDn.sondagens[]` no registro de execução. Fazer `dados conferir`
  validar o resultado (campos, `id` único, `sondagem` existente na fonte, `leitura`
  declarada) e resolver a citação em `execucoes` ou em `sondagens`. Relatar o resultado não
  incorporado à fonte. Verificar pelos cenários modificados de "Verificação por medição
  remete a execução registrada" e por "Resultado ainda não levado à fonte".
- [x] 2.3 Criar `python3 -m rsl sondagens registrar <sigla> <SDn>`, com:
  - `--retorno` por consulta declarada;
  - `--leitura`;
  - `--data-hora` obrigatório;
  - `--evidencia` obrigatório e existente;
  - `--submetido` e `--observacao`, opcionais.

  A gravação no registro é atômica, cria o arquivo quando falta e exibe a citação e a
  mudança a aplicar na fonte. Verificar pelos cenários de "Registro do resultado por
  comando", "Forma do resultado registrado" e "Registro recusado sem lastro", numa cópia do
  registro.

## 3. Flexão dos termos (D4)

- [x] 3.1 Implementar a flexão por regra de pt, en e es: núcleo, regras regulares e
  terminações indecidíveis. Verificar pelos cenários de "Plural por regra regular" e
  "Flexão indecidível reprova".
- [x] 3.2 Ler `docs/flexoes.toml` (`[documentos] flexoes`): `irregular`, `nao_contavel` e
  `vetada`, com `origem` obrigatória, PROTOCOLO_ILEGIVEL para o inválido e relato da exceção
  órfã. Verificar pelos cenários de "Exceções declaradas pelo pesquisador".
- [x] 3.3 Retirar `_PLURAIS_IRREGULARES` de `cobertura.py` e passar o reconhecimento às
  exceções. Verificar, na migração (grupo 6), que nenhum par aceito hoje reprova sem a
  exceção correspondente.

## 4. Geração dos procedimentos (D1, D3, D4)

- [x] 4.1 Declarar o esqueleto e o texto fixo na gramática, este condicionado ao estatuto
  das expressões (D3). Verificar pelo cenário "Linha condicionada ao estatuto".
- [x] 4.2 Compor os blocos de string, de subconjunto, de radical e de expressão a partir da
  STR, de `[cobertura]`, de `[composicao]`, das consultas de campo, das cláusulas e da
  flexão. Verificar pelos cenários de "Composição dos blocos a partir da STR" e "Consultas
  de campo e subconjuntos".
- [x] 4.3 Implementar a partição pelo teto, com âncoras íntegras, a conferência da união
  dos termos e a reprovação das âncoras acima do teto e da forma `unica` com partição.
  Verificar pelos cenários de "Partição pelo teto de caracteres".
- [x] 4.4 Montar o procedimento inteiro, seções 1 a 6, com o roteiro de sondagens na seção 1
  e a tabela de sementes filtrada pela base. Verificar pela tabela de origem de "Procedimento
  inteiro é saída de geração" e pelos cenários de "Roteiro escrito no procedimento".
- [x] 4.5 Criar `python3 -m rsl procedimentos gerar [<sigla>] [--gravar]`; registrar
  `procedimentos` e `sondagens` na ajuda. O ensaio mostra
  a diferença por seção e as formas flexionadas com a sua origem. A gravação é atômica,
  com releitura, e é recusada diante de leitura reprovada, flexão indecidível ou fonte
  alterada. Registrar o subcomando na ajuda. Verificar com `procedimentos gerar -h`, com o
  ensaio sobre as fontes e com a gravação numa cópia.

## 5. Conferências e autoteste (D6)

- [x] 5.1 Fazer `documentos conferir` reprovar, por base, o procedimento que difere da
  geração ou que não existe, nomeando a linha e `procedimentos gerar <sigla> --gravar`.
  Verificar com um termo editado à mão numa cópia.
- [x] 5.2 Passar as conferências de `cobertura-por-base` à estrutura derivada da fonte:
  - critérios;
  - forma de execução;
  - teto;
  - plural por idioma;
  - lematização medida;
  - citação;
  - termo só no singular, que passa a reprovar, inclusive na forma curada e nos
    subconjuntos.

  Verificar pelos cenários modificados e acrescentados.
- [x] 5.3 Acrescentar ao autoteste os casos de `fonte-do-procedimento`,
  `geracao-dos-procedimentos`, `sondagens-por-base` e `flexao-dos-termos`. Acrescentar
  também o invariante contra gerador errado. Mostrar que cada caso falha com a validação ou
  a conferência correspondente desligada. Verificar que `python3 -m rsl projeto autoteste`
  não tem falha e relata os casos não executados.

## 6. Migração das bases (D7)

- [x] 6.1 Transcrever as quatro bases para `docs/procedimentos/<sigla>/`, com
  `procedimento.toml` e os fragmentos, a partir dos procedimentos atuais. Atribuir uma
  categoria a cada elemento de sintaxe e acrescentar o elemento de cada categoria que faltar,
  como `nao_verificado`. A ERIC é o caso de prova. Parâmetro que a fonte não exprima
  interrompe a migração para decisão.
- [x] 6.2 Onde a verificação se contradiz, transcrever a situação mais conservadora
  (`nao_verificado`) e registrar a contradição em `data/pendencias.json`, com a origem, sem
  resolvê-la. Na ERIC, todos os elementos e regras de montagem ditos medidos entram como
  `nao_verificado`, com sondagem no roteiro: as sondagens serão refeitas pelo pesquisador
  (decisão de 2026-11-23), e nenhum resultado antigo se reconstrói. Isso vale para as
  "regras medidas" da seção 4 e para o truncamento afirmado na skill `execucao-da-busca`.
  A PD09 continua aberta.
- [x] 6.3 Provar a transcrição em duas partes (D7, decisão de 2026-11-23): fora dos blocos
  de termos, a diferença do ensaio de `procedimentos gerar` contra os arquivos atuais tem de
  ser só a das uniformizações aprovadas; em cada bloco, comparado como conjunto de termos com
  a flexão ligada, só pode haver acréscimo de forma flexionada, nunca perda de termo.
  Diferença fora disso interrompe a migração e vai ao pesquisador.
- [x] 6.4 Escrever, para cada base, o roteiro de sondagens dos elementos `nao_verificado`
  pela skill `sondagens-de-sintaxe`, e os `sem_sondagem` com motivo. Revisar o roteiro com o
  pesquisador.
- [x] 6.5 Montar `docs/flexoes.toml` a partir das reprovações de flexão indecidível e dos
  pares irregulares de hoje, por idioma. Cada exceção proposta pelo agente leva `origem` que
  o diga e vai à lista do LOG_IA. Apresentar a lista ao pesquisador antes de gravar.
- [x] 6.6 Ensaiar as quatro bases, revisar a diferença com o pesquisador e gravar. Verificar
  que `documentos conferir` não reprova nenhuma base por diferença, por termo só no singular
  ou por elemento sem sondagem.

## 7. Documentação, skills e registro

- [x] 7.1 Criar a skill `sondagens-de-sintaxe` (D8). Ela não nomeia base nem ensina comando.
  Verificar com `grep -n -i -E '\b(WoS|Scopus|ERIC|BRAPCI|Web of Science)\b'` sobre a
  skill, que não deve achar nada.
- [x] 7.2 Criar a skill `flexao-por-base`, que remete à `sondagens-de-sintaxe` para a sonda
  de lematização. Verificar com o mesmo `grep`.
- [x] 7.3 Reescrever `procedimento-de-busca-por-base`:
  - base nova começa por `procedimentos iniciar`, e a lista de `PENDENTE` é a lista de
    trabalho;
  - o agente edita a fonte e gera;
  - nunca edita o procedimento;
  - o Passo 1 produz `[[sintaxe]]` e `[[sondagens]]`;
  - o contrato de forma passa à remissão a `documentos gramatica`;
  - a ordem é quadro → `strings gerar` → `procedimentos gerar` → `documentos conferir`.

  Atualizar `execucao-da-busca` (remissão ao roteiro e registro por `sondagens
  registrar`) e
  `expressoes-de-busca`. Verificar a coerência com o README.
- [x] 7.4 Declarar no README, trabalhando sobre a versão corrente:
  - no Mapa: a fonte, o procedimento como saída e o arquivo de exceções;
  - na Precedência: a ordem de geração;
  - nos três registros: `sondagens` no registro de execução.

  Acrescentar o passo a `docs/procedimentos.md`. Verificar que os comandos documentados
  rodam como escritos.
- [x] 7.5 Registrar a decisão no histórico com a skill `registrar-decisao`, sem contagem:
  - a alternativa B, que substitui a ficha mista;
  - a uniformização aprovada;
  - o roteiro de sondagens, as categorias mínimas e os comandos `sondagens registrar` e
    `procedimentos iniciar`;
  - a decisão de refazer as sondagens da ERIC, sem reconstruir os resultados antigos;
  - a flexão por regra e exceções;
  - o plural por idioma;
  - a reprovação do termo só no singular;
  - as formas acrescentadas, por faceta e idioma, para o LOG_IA.

  Retirar de `data/pendencias.json` a pendência do plural de WoS, Scopus e BRAPCI e citar o
  `id` dela. Verificar que a entrada não transcreve número.
- [x] 7.6 Integração: rodar `documentos conferir`, `dados conferir` e `projeto autoteste` e
  relatar, no relato da change, os códigos e os casos não executados.

## Workflow follow-up

- Executar as sondagens do roteiro com o pesquisador, a começar pelas da ERIC, que ele
  decidiu refazer. Registrá-las por `sondagens registrar`, passar os elementos a `medicao`,
  com citação, e regenerar. Resolver a PD09 quando as sondagens da ERIC que ela exige
  estiverem registradas, citando o `id` no histórico.
- Fixar a convenção de pasta da evidência das sondagens (design, Open Questions).
- Medir a lematização por idioma na primeira execução de cada base e só então considerar
  `pela lematização`.
- O teste de aderência mede, na primeira execução, o efeito dos plurais acrescentados.
- Arquivar a change depois da revisão do pesquisador.
