# Tasks

## 1. Referência

- [x] 1.0 Verificar que as alterações de `conjunto-semente-independente` em `src/` estão em
  commit (`git status --short src/` vazio) e que `python3 src/protocolo.py --conferir` sai
  com 0. Sem isso, não seguir: a referência sairia de um código intermediário.
- [x] 1.1 Gravar no scratchpad a referência de D9:
  - saída de `python3 src/protocolo.py --mostrar` e `--conferir`;
  - saída e contagem por grupo de `--conferir --autoteste` e de
    `src/derivar_expressoes.py --autoteste`;
  - `registros.csv`, `contagens_busca.csv`, `ordem_triagem.csv`, `fidelidade_EB2.csv` e
    `sensibilidade_<base>.csv`, gerados sobre exportações sintéticas e um registro de
    execução sintético, também no scratchpad, sem tocar em `data/`.

  Verificar que um script de comparação reprova quando um byte da referência é alterado.
- [x] 1.2 Comparar as duas `normaliza()` (NFKD e NFD) sobre todos os termos do protocolo e
  sobre os textos das exportações sintéticas. Verificar o resultado: lista vazia permite
  seguir; diferença é relatada ao pesquisador antes do grupo 3 (D6).

## 2. Esqueleto, saída e configuração

- [x] 2.1 Criar `src/rsl/` com `__main__.py`, `saida.py` (`Saida` com os oito códigos da
  spec), `config.py` (carga sob demanda) e `contexto.py`. Verificar que
  `PYTHONPATH=src python3 -m rsl` exibe a ajuda com a tabela de códigos e sai com 2.
- [x] 2.2 Definir as exceções tipadas e o único ponto que as converte em código (D3).
  Verificar que `grep -rn "sys.exit\|SystemExit" src/rsl` só encontra `__main__.py`.
- [x] 2.3 Verificar a importação sem efeito com um `config.toml` inválido apontado por
  variável de ambiente de teste. Verificar que `python3 -c "import rsl.conferencia"`
  conclui sem erro e que `python3 -m rsl conferir` sai com 3.

## 3. Leitura, gramática e conferência

- [x] 3.1 Criar `gramatica.py` com os elementos de D4, cobrindo todas as seções, tabelas,
  rótulos, marcadores, identificadores e frases-padrão hoje lidos por `protocolo.py` e
  pelas fichas. Verificar que nenhum título de seção ou nome de coluna aparece como
  literal fora de `gramatica.py` (busca em `src/rsl`).
- [x] 3.2 Mover `markdown.py`, `leitura.py`, `fichas.py`, `cobertura.py` e
  `conferencia.py`, com uma só `normaliza()`, sem `relatorio_bases()`, e com os leitores
  devolvendo a localização de cada valor (D5). Verificar que `mostrar` e `conferir` batem
  com a referência, salvo a última linha com o código.
- [x] 3.3 Fazer `conferir` propagar `ProtocoloInvalido` como PROTOCOLO_ILEGIVEL. Verificar
  com uma cópia sem a seção "Expressões de busca" que o código é 4, e com um termo de STR
  fora do quadro que o código é 1.
- [x] 3.4 Implementar `rsl gramatica`. Verificar que a saída lista a seção
  "Conjunto-semente", as colunas da tabela de bases e as formas de identificador, e que não
  contém sigla de base nem `FCTn` concreto.

## 4. Dados alimentados e sementes

- [x] 4.1 Mover `conferir-dados`, `sementes sincronizar` e `pendencias` para `dados.py`, e
  a planilha de aderência e o ensaio seco para `sementes.py` (`sementes planilha`), com
  todos os caminhos lidos da configuração. Verificar que:
  - `conferir-dados` sai com 5 por falta do `registro_execucao.json`;
  - `sementes sincronizar` rodado duas vezes sobre uma cópia não muda o arquivo;
  - `sementes planilha` grava no caminho configurado.

## 5. Busca

- [x] 5.1 Mover `derivar_expressoes.py` para `busca/`, sem estado de módulo, com os nomes de
  saída de `[saidas]` (D7) e com a docstring sem a composição vigente. Verificar que as
  saídas sobre os dados sintéticos são idênticas byte a byte às da referência, com os
  nomes novos.
- [x] 5.2 Converter os `sys.exit` e os `SystemExit` da busca nas exceções de D3:
  - `busca registrar` recusado → 1;
  - registro ou exportação ausente → 5;
  - fidelidade acima do limiar → 1.

  Verificar cada caso com dados sintéticos.

## 6. Termos

- [x] 6.1 Mover `validar_termos.py` para `termos/`, com o cliente HTTP de D8, sem
  retentativa e com interrupção em erro de rede, 403, 429, 5xx e corpo fora do formato
  esperado. Verificar com um servidor local de teste (stdlib `http.server` em
  `127.0.0.1`), nunca contra o serviço real, que:
  - a resposta 429 no décimo termo interrompe;
  - não há requisição seguinte;
  - os termos anteriores ficam gravados;
  - o código é 7.
- [x] 6.2 Renomear a planilha para `validacao_terminologica.csv` em `[dados]`. Verificar
  que `grep -rn termologica` sobre `src/`, `config.toml`, `README.md` e `.agents/` volta
  vazio.

## 7. Autoteste

- [x] 7.1 Reescrever as mutações a partir da estrutura lida (D5), com o código esperado
  em cada caso, e acrescentar o grupo que percorre os elementos exigidos da gramática.
  Verificar que:
  - `grep -n '"| SE\|"| wos\|\*\*< ' src/rsl/autoteste` volta vazio;
  - `rsl autoteste` executa todos os grupos da referência, mais o da gramática.
- [x] 7.2 Provar que o autoteste depende da estrutura, e não do texto, numa cópia do
  protocolo no scratchpad: acrescentar uma semente SE11 coerente e trocar a faixa de
  sensibilidade para outra válida, ajustando a ficha onde for preciso. Verificar que
  `conferir` passa e que o autoteste não reporta "mutação não aplicada".
- [x] 7.3 Provar que os códigos de saída reprovam: um caso de forma marcado para esperar
  REPROVADO tem de fazer o autoteste falhar. Verificar e desfazer a marcação.
- [x] 7.4 Verificar o autoteste parcial: sem `registro_execucao.json`, `rsl autoteste` sai
  com 6, e a última mensagem diz quantos casos não rodaram.

## 8. Documentação e remoção dos scripts antigos

- [x] 8.1 No mesmo passo:
  - reescrever os comandos do README (seções Scripts, M3/E1, M3/E2, Atividades
    transversais, Configuração e parâmetros) com `python3 -m rsl`, a chamada com
    `PYTHONPATH` e a tabela de códigos;
  - atualizar as skills e as fichas que citam comandos;
  - acrescentar `[saidas]` ao `config.toml`, com comentário;
  - remover `src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
    `src/gen_semente.py`.

  Verificar que `grep -rnE "src/[a-z_]+\.py" README.md docs .agents config.toml` volta
  vazio.
- [x] 8.2 Registrar em `data/historico.md` a mudança de comandos, de códigos e de nomes de
  arquivo (decisão de instrumento, não de método). Verificar que a entrada tem data,
  alcance e fundamento.

## 9. Integração

- [x] 9.1 Rodar `rsl conferir`, `rsl conferir-dados` e `rsl autoteste` e comparar com a
  referência de 1.1. Verificar que as únicas diferenças são as que as specs permitem.
- [x] 9.2 Atualizar as tarefas de código pendentes de `revisao-das-strings-por-faceta`, e
  as de `conjunto-semente-independente` se ainda houver alguma, para os subcomandos e
  módulos novos. Verificar com `openspec validate` em cada change alterada.

## Workflow follow-up

- Arquivar a change depois da revisão, antes de iniciar `sementes-estruturadas-no-protocolo`.
