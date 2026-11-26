# Tarefas

## 1. Restrição por DOI na fonte

- [x] 1.1 Em `src/rsl/gramatica.py`, acrescentar a `[composicao]` o campo opcional `doi`,
  que exige o marcador `{doi}` (spec `anatomia-da-perda`: "Restrição por DOI declarada na
  fonte"). Verificar: `documentos gramatica` mostra o campo, e o autoteste ganha um caso
  em que `doi = "DO="` reprova a base com PROTOCOLO_ILEGIVEL, nomeando `composicao` e
  `doi`.
- [x] 1.2 Na fonte da Scopus, declarar `[composicao] doi` e o elemento `[[sintaxe]]`
  "Restrição por DOI". A situação é conferida na fonte oficial da Scopus no momento da
  declaração (`oficial`, com a citação) ou fica `nao_verificado` (design, plano de
  migração). Verificar: `documentos conferir` sai OK, e `procedimentos gerar scopus` mostra
  só o elemento novo em §1.

## 2. Anatomia da perda

- [x] 2.1 Criar `src/rsl/busca/anatomia.py` com a seleção das sementes diagnosticadas
  (aderência não recuperada na base, com DOI; sem DOI, listadas à parte) e a montagem dos
  níveis 1 a 5 a partir da composição (design, decisões 1 e 2). Sem proximidade, a montagem
  funde os níveis 3 e 4; base sem `doi` e expressão particionada saem com REPROVADO. Verificar:
  sobre a Scopus atual, as sementes diagnosticadas são SE2, SE3, SE4, SE7 e SE8; os níveis
  4 e 5 vêm de BD2/EX4 e BD2/EX1; e o texto do nível 3 difere do 4 só pelo operador de
  proximidade.
- [x] 2.2 Implementar o modo roteiro de `aderencia diagnosticar <base>` em `__main__.py`
  (sem `--retorno`: imprime e não grava, com o comprimento de cada nível e o aviso acima do
  teto). Verificar: `aderencia diagnosticar scopus` imprime os níveis 1 a 3 e o exemplo da
  chamada, e nenhum arquivo de `data/` muda (`git status` e horários).
- [x] 2.3 Implementar o modo resultado: `--retorno N K`, `--exportacao N ARQ`,
  `--data-hora`, a conferência retorno × lidos (DADOS), a coerência entre níveis (REPROVADO,
  decisão 4), a causa pelo primeiro nível vazio, o aviso de datas diferentes e a gravação de
  `anatomia_<base>.csv` e `anatomia_consultas_<base>.csv` (chaves novas em `config.toml`).
  Verificar com exportações sintéticas, no autoteste da tarefa 2.4.
- [x] 2.4 Acrescentar a `src/rsl/autoteste/busca.py` o grupo "anatomia da perda", com uma
  fonte de ensaio e exportações sintéticas: uma semente por causa, retorno que não confere,
  nível faltando, DOI que reaparece, DOI estranho, base sem `doi`. Verificar: `projeto
  autoteste` passa. Com a atribuição trocada (último nível vazio em vez do primeiro) e com a
  conferência de subconjunto desligada, os casos correspondentes falham.
- [x] 2.5 Trocar a tabela da anatomia nos `notas_sementes.md` das fontes (Scopus, WoS,
  BRAPCI) pela remissão a `aderencia diagnosticar`. Ancorar o comando no passo de medir a
  aderência de `docs/procedimentos.md`, regenerar procedimentos (`procedimentos gerar
  --gravar`) e catálogo (`catalogo gerar --gravar`). Verificar: `documentos conferir` e
  `catalogo gerar` saem OK, e a seção 5 dos procedimentos não traz mais 🟦/🟨 em consulta.

## 3. Análise da sensibilidade

- [x] 3.1 Criar `src/rsl/busca/simulacao.py`: leitura da amostra (DADOS se incompleta), da
  perda (sonda − executada) e o casamento da amostra pela chave; facetas reconhecidas por
  grupo e divergências do casamento local (spec `analise-da-sensibilidade`). Verificar:
  sobre a Scopus atual, a amostra casa 53 de 53, e o relato mostra quantos elegíveis têm
  FCT3 ou FCT4 localmente.
- [x] 3.2 Implementar os candidatos (decisão 5), a gravação de `candidatos_<base>.csv` e a
  simulação com `--termo FCTn TERMO` (decisão 6, com Wilson). Recusar âncora e faceta
  inexistente com USO, e relatar os limites. Verificar: na Scopus, nenhum candidato é
  reconhecido pelo vocabulário da base; com `--termo`, o total da executada ampliada é 133
  mais o acréscimo relatado.
- [x] 3.3 Registrar `conferencia simular <base>` em `__main__.py`, com a chave
  `[saidas] candidatos`, e ancorar o comando no passo da sonda de sensibilidade de
  `docs/procedimentos.md`, regenerando o catálogo. Verificar: `conferencia simular -h`
  mostra `--termo`, e `catalogo gerar` sai OK.
- [x] 3.4 Acrescentar a `src/rsl/autoteste/busca.py` o grupo "análise da sensibilidade",
  com executada e sonda sintéticas e amostra classificada: casamento da amostra,
  candidato já no vocabulário excluído, contagem da simulação só sobre a perda, amostra
  incompleta (DADOS), âncora recusada (USO). Verificar: o autoteste passa; com a exclusão
  desligada e com a simulação contando registros da executada, os casos correspondentes
  falham.

## 4. Integração

- [x] 4.1 Rodar `projeto autoteste`, `documentos conferir`, `dados conferir` e `catalogo
  gerar`. Verificar: todos saem OK.
- [x] 4.2 Rodar o roteiro de `aderencia diagnosticar scopus` e `conferencia simular scopus`
  com os dados reais, e conferir à mão uma linha de cada saída. Na anatomia, o texto
  impresso é o que o README manda submeter. Em `candidatos_scopus.csv`, recontar à mão o
  acréscimo de um candidato. Verificar: as duas conferências batem; registrar o resultado
  no relato ao pesquisador.

## 5. Correções da verificação

- [x] 5.1 Seleção das sementes pela executada da base, não pelo corpus; argumento sobrando
  (exportação com retorno 0, retorno em nível lido) sai com DADOS; o resumo por causa conta
  `presente na executada`. Verificar: autoteste com casos novos, e cada um falha com a
  correção desfeita.
- [x] 5.2 Regra dos candidatos (spec `analise-da-sensibilidade`, decisão 5): excluir só a
  palavra-chave reconhecida por faceta não âncora ou igual a termo de âncora, e listar as
  excluídas com o motivo. Verificar: na Scopus, candidatas + excluídas somam as
  palavras-chave distintas dos elegíveis; no autoteste, o composto com termo de âncora é
  candidato e falha com `search` no lugar de `fullmatch`.
- [x] 5.3 Autoteste: divergência do casamento local, elegível sem palavras-chave, aviso de
  datas diferentes (com contraprova no mesmo dia), e contagem real dos casos não executados
  dos dois grupos. Verificar: cada caso falha com a regra correspondente desligada.
- [x] 5.4 Conferir na ajuda da Scopus o código de campo `DOI` da busca avançada e registrar
  a citação na entrada [[sintaxe]] "Restrição por DOI", regenerando o procedimento. O
  agrupamento por `OR`, não medido, fica pendente para a submissão do nível 1.
- [x] 5.5 Refazer a conferência da 4.2: o texto dos níveis 3 a 5 contra o procedimento
  gerado e o acréscimo de um candidato recontado por procedimento independente.
- [x] 5.6 Casos não executados contados por construção (spec `leitura-do-protocolo`,
  delta MODIFIED): `Grupo.nao_executa(motivo, *, quantos=None)`; o retorno antecipado
  relata o bloco sem número, e o número só vem de `quantos=` (um caso trocado, ou valor
  calculado dos dados). Verificar: grupos fictícios em memória dão PARCIAL com bloco, com
  contagem e com os dois; a forma antiga `nao_executa(3, "…")` é recusada.

## 6. Correções da segunda verificação

- [x] 6.1 Formas de número no alcance (design, decisões 5 e 6): as candidatas que são forma
  de número uma da outra formam um candidato só; o alcance do candidato e do termo de
  `--termo` se mede com todas as formas; o relato e `candidatos_<base>.csv` (coluna
  `formas`) mostram as que casaram. Verificar: no autoteste, o plural entra no grupo e o
  acréscimo conta o registro que só traz o plural, e falham com as formas desligadas; na
  Scopus, o acréscimo de um candidato agrupado recontado por procedimento independente.
- [x] 6.2 Resultado sem `--data-hora` sai com DADOS, como o requisito "Resultado de cada
  nível submetido". Verificar: caso no autoteste, que falha com USO.
- [x] 6.3 Grupo "contagem dos casos não executados" no autoteste, com grupos fictícios em
  memória e a conclusão extraída para `conclusao(feitos)`, a mesma que `projeto autoteste`
  usa: bloco, contagem, os dois, falha com não executados e a forma antiga recusada.
  Verificar: cada caso falha com a regra correspondente desfeita.

## Workflow follow-up

- O pesquisador submete os níveis 1 a 3 na Scopus e registra o resultado (README da change,
  passo B).
- Relatar ao pesquisador a causa por semente e os candidatos, para a decisão sobre a
  emenda. A decisão é dele.
- Arquivar a change e sincronizar as specs `anatomia-da-perda` e `analise-da-sensibilidade`.
