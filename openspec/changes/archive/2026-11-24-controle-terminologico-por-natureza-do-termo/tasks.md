# Tasks

## 1. Forma nova do controle terminológico (leitura restabelecida)

- [x] 1.1 Declarar na gramática o título `CTn (FCTn)` (nível 3, na seção "Controle terminológico"), o identificador `CT`, os rótulos "Termo livre", "Descritores correspondentes" e "Termos sinônimos ou relacionados", com os nomes internos `livre`, `descritores` e `relacionados`, e o cabeçalho com a primeira célula não lida. Verificar com `documentos gramatica`, que deve exibir as formas novas e nenhuma antiga.
- [x] 1.2 Reescrever a leitura das tabelas: identificação pelo título; reprovação de título fora da forma, número divergente, duas facetas, faceta inexistente, CT repetido, tabela sem título e cabeçalho antigo `| FCTn |`; rótulo comparado inteiro; rótulo desconhecido, repetido ou ausente reprovados (design D1, D2). Verificar que `grep -rn "nucleo\|proximos\|R_NUCLEO\|R_PROXIMOS" src/rsl` não acha resto fora de comentário histórico.
- [x] 1.3 Manter no protocolo os quatro rótulos "Termos sinônimos ou relacionados" (a correção para "e/ou" planejada aqui foi retirada: decisão 2 retificada pelo pesquisador em 2026-11-24, ver design). Verificar que `documentos conferir` deixa de sair com PROTOCOLO_ILEGIVEL. Pode ainda sair com REPROVADO, que é resolvido no grupo 2.
- [x] 1.4 Atualizar os autotestes de protocolo, geração e procedimentos para a forma nova e acrescentar um caso por defeito de forma do requisito "Autoteste prova as reprovações do controle terminológico". Demonstrar que cada caso reprova com PROTOCOLO_ILEGIVEL, revertendo temporariamente a verificação correspondente e vendo o autoteste falhar. Verificar com `projeto autoteste` sem falha.

## 2. Critério pela natureza do termo

- [x] 2.1 Fixar o domínio de `decisao_ReT` (`descritor`, `sinônimo ou relacionado`, `termo livre`, vazio; sem distinção de caixa) e reprovar valor fora dele em `termos importar`. Verificar com caso de autoteste sobre planilha em memória.
- [x] 2.2 Implementar a regra da linha esperada (design D3) sobre as decisões do termo nos instrumentos planejados para a faceta e o idioma dele, sem usar `status_proposto`. Verificar com os casos do requisito "Autoteste prova o domínio e a regra da linha": precedência, pendência manual, proposta da máquina e planilha ausente.
- [x] 2.3 Em `documentos conferir`: retirar a reprovação de célula vazia; reprovar o termo repetido entre linhas do mesmo CT e idioma; reprovar o termo fora da linha esperada, lendo a planilha de `[dados] validacao`; tratar a planilha ausente como pendência para o termo em "Termo livre"; terminar com DADOS se a planilha estiver ilegível (design D4, D5). Verificar com autoteste que injeta cada defeito e demonstra a reprovação, com e sem planilha.
- [x] 2.4 Aplicar a regra ao protocolo: sem planilha, todo termo das linhas "Descritores correspondentes" e "Termos sinônimos ou relacionados" passa para "Termo livre" do mesmo CT e idioma, na ordem atual. Verificar que `documentos conferir` não reprova pela classificação e que o conjunto de termos de cada CT e idioma é o mesmo de antes, comparando o conjunto lido antes e depois.
- [x] 2.5 Regenerar as STRs com `strings gerar --gravar`. Verificar que, para cada STR, o conjunto de termos é igual ao do `HEAD` (só a ordem muda), comparando os conjuntos calculados e não transcritos, e que `documentos conferir` não reprova por STR.

## 3. Retirada do corte `camadas`

- [x] 3.1 Retirar o campo `camadas` do esquema da `[cobertura]`, do modelo de `procedimentos iniciar`, da composição dos blocos, da cobertura e da tabela de cobertura do procedimento gerado. Verificar com autoteste que uma fonte que ainda declara `camadas` reprova como campo desconhecido.
- [x] 3.2 Retirar `camadas = "todas"` das quatro fontes `docs/procedimentos/*/procedimento.toml` e regenerar os procedimentos com `procedimentos gerar <sigla> --gravar`. Verificar que `documentos conferir` passa e que o diff dos `docs/procedimentos_busca_*.md` só traz a linha `camadas` retirada e a ordem nova dos termos.
- [x] 3.3 Procurar "núcleo", "camada", "próximos" e "Termos centrais" no texto autoral das fontes (`como_executar.md`, `variantes.md`) e corrigir o que se refere às linhas do controle terminológico, sem tocar no uso linguístico de "núcleo", como o núcleo da locução em `flexao`. Verificar com `grep`, listando no relato o que ficou e por quê.

## 4. Skills, histórico e pendências

- [x] 4.1 Atualizar a skill `facetacao-e-termos-livres` §2: linhas pela natureza do termo, regra da decisão do ReT e termo sem decisão em "Termo livre". Atualizar também a skill `procedimento-de-busca-por-base`, nos trechos que falam em usar só o núcleo, porque o corte foi retirado. Verificar com `catalogo gerar`, que deve passar sem divergência.
- [x] 4.2 Registrar em `data/historico.md` as decisões 1 a 8 do design, com a retificação da decisão 5, e declarar que as linhas vazias significam "não validado". Verificar que nenhuma contagem foi transcrita.
- [x] 4.3 Atualizar a PD03 em `data/pendencias.json`: a validação decide a linha de cada termo pela regra nova, e até lá todos ficam em "Termo livre". Verificar com `projeto pendencias`.

## 5. Integração

- [x] 5.1 Executar `projeto autoteste`, `documentos conferir`, `strings gerar` (ensaio) e `procedimentos gerar <sigla>` (ensaio) para as quatro bases. Verificar código OK em todos e nenhuma diferença pendente. Executados em 2026-11-24 e aceitos pelo pesquisador. `documentos conferir`, `strings gerar` e `procedimentos gerar` saíram com código OK e sem diferença. `projeto autoteste` saiu PARCIAL (código 6), porque `data/registro_execucao.json` não existe, também no `HEAD`; isso fica fora desta change.

## 6. Acréscimos da verificação (decisões 9 a 13)

- [x] 6.1 Declarar na gramática as linhas da STR (termo livre e descritores) e usá-las na geração e na conferência; reprovar termo de "Termos sinônimos ou relacionados" na STR, nomeando a linha. Verificar com autoteste que reprova ao reverter a regra.
- [x] 6.2 Retirar `[conferencia] minimo_termos_string` do esquema, do `config.toml`, do leitor e da conferência, e registrá-la como chave retirada. Verificar com autoteste nomeado que reprova ao reverter.
- [x] 6.3 Exigir `Termo` na primeira célula do cabeçalho de cada CT. Verificar com autoteste que reprova ao reverter.
- [x] 6.4 Substituir en e es da linha "Termo livre" pelos equivalentes dos termos pt; regenerar STRs e procedimentos. Verificar com `documentos conferir`.
- [x] 6.5 Tornar construtivo o caso "forma única com partição necessária" do autoteste, que dependia do comprimento corrente das STRs.
- 6.6 Retirada da change (retificação da decisão 13, 2026-11-24): fora do escopo, segue no follow-up. Texto original: Executar `termos sondar`, `termos exportar`, `termos validar tbci` e `termos validar unesco`, em sequência, e apresentar as propostas ao pesquisador, que preenche `decisao_ReT`. Mover os termos pela regra, regenerar e conferir.
- [x] 6.7 Registrar as decisões 9 a 13 em `data/historico.md` e atualizar PD31.

## Workflow follow-up

- Validação terminológica (fora do escopo da change): `termos sondar`, `termos exportar` e `termos validar` em TBCI e UNESCO, com acesso externo autorizado pelo pesquisador; ERIC e Brased consultados à mão pelo pesquisador; `decisao_ReT` preenchida pelo ReT; reclassificação no CT pela regra; regeneração de STRs e procedimentos. Termo novo revelado pela validação é ampliação: exige registro no histórico e novo teste de aderência.
- Arquivar a change depois da verificação.
