# Tarefas

## 1. Restrição por DOI na fonte

- [ ] 1.1 Em `src/rsl/gramatica.py`, acrescentar a `[composicao]` o campo opcional `doi`,
  que exige o marcador `{doi}` (spec `anatomia-da-perda`: "Restrição por DOI declarada na
  fonte"). Verificar: `documentos gramatica` mostra o campo, e o autoteste ganha um caso
  em que `doi = "DO="` reprova a base com PROTOCOLO_ILEGIVEL, nomeando `composicao` e
  `doi`.
- [ ] 1.2 Na fonte da Scopus, declarar `[composicao] doi` e o elemento `[[sintaxe]]`
  "Restrição por DOI". A situação é conferida na fonte oficial da Scopus no momento da
  declaração (`oficial`, com a citação) ou fica `nao_verificado` (design, plano de
  migração). Verificar: `documentos conferir` sai OK, e `procedimentos gerar scopus` mostra
  só o elemento novo em §1.

## 2. Anatomia da perda

- [ ] 2.1 Criar `src/rsl/busca/anatomia.py` com a seleção das sementes diagnosticadas
  (aderência não recuperada na base, com DOI; sem DOI, listadas à parte) e a montagem dos
  níveis 1 a 5 a partir da composição (design, decisões 1 e 2). Sem proximidade, a montagem
  funde os níveis 3 e 4; base sem `doi` e expressão particionada saem com REPROVADO. Verificar:
  sobre a Scopus atual, as sementes diagnosticadas são SE2, SE3, SE4, SE7 e SE8; os níveis
  4 e 5 vêm de BD2/EX4 e BD2/EX1; e o texto do nível 3 difere do 4 só pelo operador de
  proximidade.
- [ ] 2.2 Implementar o modo roteiro de `aderencia diagnosticar <base>` em `__main__.py`
  (sem `--retorno`: imprime e não grava, com o comprimento de cada nível e o aviso acima do
  teto). Verificar: `aderencia diagnosticar scopus` imprime os níveis 1 a 3 e o exemplo da
  chamada, e nenhum arquivo de `data/` muda (`git status` e horários).
- [ ] 2.3 Implementar o modo resultado: `--retorno N K`, `--exportacao N ARQ`,
  `--data-hora`, a conferência retorno × lidos (DADOS), a coerência entre níveis (REPROVADO,
  decisão 4), a causa pelo primeiro nível vazio, o aviso de datas diferentes e a gravação de
  `anatomia_<base>.csv` e `anatomia_consultas_<base>.csv` (chaves novas em `config.toml`).
  Verificar com exportações sintéticas, no autoteste da tarefa 2.4.
- [ ] 2.4 Acrescentar a `src/rsl/autoteste/busca.py` o grupo "anatomia da perda", com uma
  fonte de ensaio e exportações sintéticas: uma semente por causa, retorno que não confere,
  nível faltando, DOI que reaparece, DOI estranho, base sem `doi`. Verificar: `projeto
  autoteste` passa. Com a atribuição trocada (último nível vazio em vez do primeiro) e com a
  conferência de subconjunto desligada, os casos correspondentes falham.
- [ ] 2.5 Trocar a tabela da anatomia nos `notas_sementes.md` das fontes (Scopus, WoS,
  BRAPCI) pela remissão a `aderencia diagnosticar`. Ancorar o comando no passo de medir a
  aderência de `docs/procedimentos.md`, regenerar procedimentos (`procedimentos gerar
  --gravar`) e catálogo (`catalogo gerar --gravar`). Verificar: `documentos conferir` e
  `catalogo gerar` saem OK, e a seção 5 dos procedimentos não traz mais 🟦/🟨 em consulta.

## 3. Análise da sensibilidade

- [ ] 3.1 Criar `src/rsl/busca/simulacao.py`: leitura da amostra (DADOS se incompleta), da
  perda (sonda − executada) e o casamento da amostra pela chave; facetas reconhecidas por
  grupo e divergências do casamento local (spec `analise-da-sensibilidade`). Verificar:
  sobre a Scopus atual, a amostra casa 53 de 53, e o relato mostra quantos elegíveis têm
  FCT3 ou FCT4 localmente.
- [ ] 3.2 Implementar os candidatos (decisão 5), a gravação de `candidatos_<base>.csv` e a
  simulação com `--termo FCTn TERMO` (decisão 6, com Wilson). Recusar âncora e faceta
  inexistente com USO, e relatar os limites. Verificar: na Scopus, nenhum candidato é
  reconhecido pelo vocabulário da base; com `--termo`, o total da executada ampliada é 133
  mais o acréscimo relatado.
- [ ] 3.3 Registrar `conferencia simular <base>` em `__main__.py`, com a chave
  `[saidas] candidatos`, e ancorar o comando no passo da sonda de sensibilidade de
  `docs/procedimentos.md`, regenerando o catálogo. Verificar: `conferencia simular -h`
  mostra `--termo`, e `catalogo gerar` sai OK.
- [ ] 3.4 Acrescentar a `src/rsl/autoteste/busca.py` o grupo "análise da sensibilidade",
  com executada e sonda sintéticas e amostra classificada: casamento da amostra,
  candidato já no vocabulário excluído, contagem da simulação só sobre a perda, amostra
  incompleta (DADOS), âncora recusada (USO). Verificar: o autoteste passa; com a exclusão
  desligada e com a simulação contando registros da executada, os casos correspondentes
  falham.

## 4. Integração

- [ ] 4.1 Rodar `projeto autoteste`, `documentos conferir`, `dados conferir` e `catalogo
  gerar`. Verificar: todos saem OK.
- [ ] 4.2 Rodar o roteiro de `aderencia diagnosticar scopus` e `conferencia simular scopus`
  com os dados reais, e conferir à mão uma linha de cada saída. Na anatomia, o texto
  impresso é o que o README manda submeter. Em `candidatos_scopus.csv`, recontar à mão o
  acréscimo de um candidato. Verificar: as duas conferências batem; registrar o resultado
  no relato ao pesquisador.

## Workflow follow-up

- O pesquisador submete os níveis 1 a 3 na Scopus e registra o resultado (README da change,
  passo B).
- Relatar ao pesquisador a causa por semente e os candidatos, para a decisão sobre a
  emenda. A decisão é dele.
- Arquivar a change e sincronizar as specs `anatomia-da-perda` e `analise-da-sensibilidade`.
