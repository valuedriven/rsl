# Tasks

Tarefas marcadas **(pesquisador)** dependem de ação humana: emitir a chave, decidir
divergências, autorizar gravação no Zotero, confirmar o alinhamento. A transição tem duas
fases (design D13): na fase 1 o arquivo de sementes guarda os dados bibliográficos completos;
a redução dos campos é a fase 2.

# Fase 1 — transição, com o arquivo de sementes completo

## 1. Preparação

- [x] 1.1 Arquivar `verificacao-binaria-das-sementes` e `fidelidade-por-base-e-casamento-por-campo`, com specs sincronizadas; verificar que `openspec list --json` não as lista mais e que `openspec validate reestruturacao-do-conjunto-semente --strict` continua aprovado
- [x] 1.2 **(pesquisador)** Emitir a chave da API web do Zotero com escrita só na biblioteca de grupo "fatores" e guardá-la fora do controle de versão (`ZOTERO_API_KEY` ou `.env` listado no `.gitignore`); verificar com `git check-ignore .env` e sem imprimir o valor
- [x] 1.3 Guardar a cópia bruta atual da coleção (API local, só leitura) como ponto de restauração em `data/evidencia/zotero/`; verificar que o arquivo traz os 21 itens atuais

## 2. Cópia da coleção do Zotero

- [x] 2.1 Acrescentar `[zotero]` (`biblioteca`, `colecao`) e `[dados] zotero` ao `config.toml` e ao esquema da configuração; verificar com `python3 -m rsl configuracao mostrar`, que exibe as chaves e a origem delas
- [x] 2.2 Implementar o acesso à API web: chave lida de `ZOTERO_API_KEY`, nunca impressa, com só os 4 últimos caracteres em relato, e CONFIGURACAO sem a variável; verificar com um autoteste que procura a chave inteira na saída e nos arquivos gravados, e que reprova se a encontrar
- [x] 2.3 Implementar `sementes copiar`: resposta bruta dos itens de topo da coleção com biblioteca, coleção, versão e data e hora; relato do que foi acrescentado, retirado e alterado em relação à cópia anterior; verificar contra a coleção real e com um autoteste sobre duas cópias sintéticas
- [x] 2.4 Documentar no README a chave, `[zotero]` e a cópia (Três registros e comandos), e regenerar `docs/catalogo_de_apoio.md`; verificar com `python3 -m rsl catalogo gerar` sem divergência
- [x] 2.5 Ler a chave também do `.env` da raiz, recusado com CONFIGURACAO quando o `.gitignore` não o lista; ajustar README, guia e skill; verificar com autotestes (chave do `.env`; `.env` fora do `.gitignore` recusado sem imprimir a chave; sem variável nem `.env`, CONFIGURACAO)

## 3. Conferência de migração entre TOML e Zotero

- [x] 3.1 Implementar o relato de migração, que compara campo a campo os dados bibliográficos do TOML atual com a cópia: autores (sobrenome), ano, título, veículo, volume, número e páginas; verificar que ele aponta as divergências já conhecidas (SE1 páginas, SE3 volume e número, SE10 caixa)
- [x] 3.2 **(pesquisador)** Decidir cada divergência e corrigir **no Zotero**, inclusive SE13 (número de artigo) e SE19 (ano e páginas contra o Crossref); verificar com `sementes copiar` e o relato de migração sem divergência a resolver

## 4. OpenAlex, fonte complementar e último recurso

- [x] 4.1 Implementar `sementes metadados`: uma consulta por DOI, em sequência, com agente de usuário genérico e sem e-mail; resposta bruta em `data/evidencia/openalex/<doi-normalizado>.json`; 404 vira "sem registro"; outra resposta ou erro de rede interrompe sem nova tentativa; verificar com autotestes sobre respostas simuladas (200, 404, 429), sem rede
- [x] 4.2 Executar `sementes metadados` para as 19 sementes; verificar que existe um arquivo por DOI com registro e que o relato informa resumo e número de palavras-chave de cada semente
- [x] 4.3 Estender `dados conferir` para reprovar arquivo de `openalex/` cujo DOI não está no arquivo de sementes; verificar com um autoteste que injeta um arquivo de DOI inexistente e exige a reprovação
- [x] 4.4 Gravar o marcador `<doi-normalizado>.404` com a data e hora no 404, e consultar por padrão só o DOI sem resultado registrado (`--todas` refaz todas); estender `dados conferir` aos marcadores e a `crossref/`; verificar com autotestes (404 deixa marcador; segunda execução só consulta as pendentes; marcador de DOI inexistente reprova)
- [x] 4.5 Implementar `sementes metadados --fonte crossref` (D12): só sementes sem resumo em fonte nenhuma, uma consulta por vez, mesmas regras de parada, resposta bruta em `data/evidencia/crossref/`; nunca automático depois de erro da OpenAlex; `sementes completar` usa o resumo do Crossref na falta do da OpenAlex; verificar com autotestes sobre respostas simuladas (elegíveis só as sem resumo; erro da OpenAlex não aciona o Crossref; resumo JATS reconstruído sem marcação)
- [x] 4.6 Relatar em `projeto pendencias`, calculado das fontes: "sem resposta da OpenAlex (não consultada ou interrompida)", "sem registro na OpenAlex", "resumo ausente em todas as fontes — preencher no Zotero (pesquisador)"; verificar com autotestes dos três casos
- [x] 4.7 Executar `sementes metadados --fonte crossref` para as sementes elegíveis; verificar que o relato lista cada uma com resumo ou sem resumo, e que `projeto pendencias` relata as que ficam para o pesquisador

## 5. Complemento da coleção

- [x] 5.1 Implementar `sementes completar`: plano por item (resumo só onde está vazio, palavras-chave como etiquetas automáticas novas, itens fora do TOML relatados); `--gravar` item a item com controle de versão; parada sem nova tentativa em conflito, limite ou pedido de espera; `--retirar <DOI>` tira o item só da coleção; cópia regravada ao fim; verificar com autotestes sobre um servidor simulado (resumo preenchido preservado, etiquetas preservadas, conflito interrompe, sem `--gravar` nada muda)
- [x] 5.2 Executar `sementes completar` sem `--gravar` e apresentar o plano; verificar que nenhum item mudou, comparando a versão da biblioteca antes e depois
- [x] 5.3 **(pesquisador)** Autorizar e executar `sementes completar --gravar --retirar 10.5753/wetie.2023.236130 --retirar 10.5220/0012471400003645`; verificar que a nova cópia tem 19 itens, todos com DOI do TOML, e que os dois itens retirados continuam na biblioteca
- [x] 5.4 Retirar a recusa de `--retirar` para DOI do arquivo de sementes, postergada para a fase 2 (10.6); verificar que o autoteste não exige mais a recusa

## 6. Junção e alinhamento, com o arquivo completo

- [x] 6.1 Na gramática e na leitura: `doi` obrigatório; `alinhamento_facetas` opcional (chave `FCTn` da tabela, frase não vazia, tabela e não lista), ao lado de `facetas`; cópia da coleção obrigatória (DADOS com `sementes copiar` se ausente); junção pelo DOI (DOI sem item ou com mais de um reprova com DADOS; item a mais relatado), trazendo `resumo` e `palavras_chave` da cópia; campos bibliográficos ainda do TOML; verificar com `python3 -m rsl documentos gramatica` e com autotestes para DOI ausente, DOI repetido, DOI sem item, chave do alinhamento fora da tabela, frase vazia e lista no lugar da tabela, todos reprovando
- [x] 6.2 Atualizar `projeto pendencias`: alinhamento a informar, sem faceta âncora (pelo alinhamento), resumo ou palavras-chave ausentes na cópia, item fora do arquivo de sementes, divergência entre TOML e Zotero por campo; retirar "DOI ausente"; verificar com autotestes e com `python3 -m rsl projeto pendencias`
- [x] 6.3 Propor, a partir da cópia (título, palavras-chave, resumo), a frase de cada faceta das 19 sementes, descrevendo o conceito sem repetir o termo do ensaio, e apresentá-las ao pesquisador; verificar que cada proposta cita só `FCTn` da tabela de facetas
- [x] 6.4 **(pesquisador)** Confirmar ou corrigir as frases propostas; verificar que a resposta cobre as 19 sementes
- [x] 6.5 Gravar no TOML o alinhamento confirmado em `alinhamento_facetas`, mantendo os demais campos; verificar com `python3 -m rsl documentos conferir` e com `python3 -m rsl aderencia ensaiar`, que lista as facetas alinhadas sem termo
- [x] 6.7 Acrescentar `referencia_curta` (D14), opcional na fase 1: forma `<sobrenome> <ano>: <início do título>`, conferida contra a cópia em `documentos conferir` (sobrenome do primeiro autor; ano do item; começo do título por palavras inteiras, sem acento, caixa nem pontuação; reticências aceitas), sem reprovar a leitura; `projeto pendencias` relata a ausente com a forma sugerida; verificar com autotestes (forma correta aprova; sobrenome trocado reprova; título que não é começo do item reprova; ausente vira pendência com sugestão)
- [x] 6.8 **(pesquisador)** Revisar as referências curtas sugeridas para as 19 sementes e colá-las no TOML (ou pedir ao agente que as grave); verificar com `python3 -m rsl documentos conferir`
- [x] 6.6 Registrar em `data/historico.md` a decisão de método (dados no Zotero e controle no TOML, DOI obrigatório, planilha retirada, recuperação também pelo DOI, resumo pela OpenAlex com o Crossref como complemento e o pesquisador como último recurso) e atualizar `data/pendencias.json` (PD20 passa a alinhamento; PD21 mantida); verificar com `python3 -m rsl projeto pendencias` e `python3 -m rsl dados conferir`

## 6A. Substituição de SE16, SE17 e SE18 (decisão do pesquisador, 2026-11-27)

- [x] 6A.1 Levar o campo retirado `observacoes` das três sementes novas para o fim da `nota`, sem alterar o texto; remover as respostas da OpenAlex e do Crossref dos três DOIs retirados; verificar que o conteúdo foi preservado e que nenhum DOI retirado continua no TOML
- [x] 6A.2 **(pesquisador)** Acrescentar à coleção `sementes` os itens dos três DOIs novos e sincronizar o Zotero; registrar o motivo da substituição, para o histórico
- [x] 6A.3 `sementes copiar` → `sementes metadados` → `sementes metadados --fonte crossref` → `sementes completar` (plano) → **(pesquisador)** `sementes completar --gravar --retirar` dos três DOIs antigos; verificar com `documentos conferir` e com a coleção de 19 itens, todos com DOI do TOML
- [x] 6A.4 Propor as frases de alinhamento das três sementes novas e regenerar os procedimentos de busca (`procedimentos gerar --gravar`), conferindo a lista de sementes de cada base; registrar a substituição no histórico, com o motivo

## 7. Ensaio seco e fim da planilha

- [x] 7.1 Implementar `aderencia ensaiar`: termos por faceta em título, palavras-chave e resumo, com marca do campo; contagem pela composição da executada só pelo título e pelos três campos; "campo ausente"; facetas alinhadas sem termo; ressalva sobre a origem das palavras-chave; nada gravado; verificar com autotestes (termo só no resumo, campo ausente, faceta alinhada sem termo) e com a execução real sobre a cópia
- [x] 7.2 Remover `aderencia planilhar`, a gravação da planilha, `data/semente_aderencia.csv` e `[saidas] aderencia`; o comando antigo dá USO e a chave antiga dá CONFIGURACAO com mensagem própria; verificar com autotestes dos dois casos e com `git status` mostrando o CSV removido
- [x] 7.3 Atualizar a skill `testar-aderencia-das-expressoes` (etapas sem planilha), o README (arquivos e comandos) e o guia `docs/procedimentos.md`; regenerar o catálogo; verificar com `grep -rn "semente_aderencia\|planilhar"` sem ocorrência fora do arquivo de changes e com `python3 -m rsl catalogo gerar` sem divergência

## 8. Recuperação pelo DOI

- [x] 8.1 Fazer `aderencia medir` contar como recuperada a semente cujo DOI aparece na exportação da executada, relatando se foi pelo título, pelo DOI ou pelos dois, e mantendo o prefixo sem DOI como indício; trocar o texto que remete à planilha; verificar com autotestes (título divergente e mesmo DOI; prefixo confirmado pelo DOI; prefixo sem DOI segue indício) e com `python3 -m rsl aderencia medir`
- [x] 8.2 Trocar em `aderencia diagnosticar` a sugestão "`indexada = não` na planilha" por remissão ao campo `bases`; verificar com o autoteste da anatomia e com `grep -n planilha src/rsl/busca/anatomia.py` sem ocorrência

## 9. Verificação da fase 1

- [x] 9.1 Rodar sem rede `documentos conferir`, `dados conferir`, `configuracao mostrar`, `projeto pendencias`, `aderencia ensaiar`, `aderencia medir` e `projeto autoteste`; verificar que todos terminam com código 0 e informam a data da cópia usada

# Fase 2 — redução dos campos

## 10. Esquema mínimo

- [x] 10.1 Tirar do esquema os campos bibliográficos, `veiculo_conferido` e `facetas`, que passam a reprovar como campo desconhecido; `referencia_curta` passa a obrigatório; dados bibliográficos vindos da cópia, com o mesmo dicionário de saída; item sem título, sem autor ou sem ano reprova; verificar com `python3 -m rsl documentos gramatica` e com autotestes (campo bibliográfico retirado reprova; item sem título reprova; título com ponto lido inteiro)
- [x] 10.2 Migrar `docs/conjunto_semente.toml`: tirar os campos bibliográficos, `veiculo_conferido` e `facetas`, e enxugar a `nota` (sem fórmula de conferência, sem resumo do conteúdo, sem dados da referência); verificar com `python3 -m rsl documentos conferir` e `python3 -m rsl configuracao mostrar`, com as referências exibidas iguais às da cópia
- [x] 10.3 Retirar do código o relato de migração e a pendência de divergência entre TOML e Zotero; verificar com `grep -rn migracao_sementes src/` sem ocorrência e o autoteste aprovado
- [x] 10.4 Atualizar a skill `definir-conjunto-semente` (§3, §4 esquema e retirada em três passos, §5, §6 e §9), a skill `conferir-referencia` (dados no Zotero) e o protocolo (§Conjunto-semente e o parágrafo do acervo pessoal, sem controle de origem); verificar que não restam citações de campos retirados nem de exigência de origem, com `grep -n` nas skills, no protocolo e nas specs
- [x] 10.5 Regenerar os procedimentos de busca e conferir que a lista de sementes de cada base (`id` e DOI) não mudou, salvo a forma da referência; verificar com `python3 -m rsl procedimentos gerar` e com o diff das seções de sementes
- [x] 10.6 **(pesquisador)** Decidir a proteção de `--retirar` contra DOI do arquivo de sementes; se adotada, especificá-la na spec e implementá-la com autoteste que exige a recusa
- [x] 10.7 Rodar sem rede `documentos conferir`, `dados conferir`, `configuracao mostrar`, `projeto pendencias`, `aderencia ensaiar`, `aderencia medir` e `projeto autoteste`; verificar que todos terminam com código 0 e informam a data da cópia usada

## Workflow follow-up

- Verificar a change (`openspec-verify-change`) e arquivá-la com specs sincronizadas, depois da fase 2 e da revisão do pesquisador.
