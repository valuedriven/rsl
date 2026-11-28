# Tasks

## 1. Sondagens no Zotero (só com autorização do pesquisador)

Escrevem na biblioteca do pesquisador. Cada uma só roda depois de autorização expressa, numa
coleção de teste, uma requisição por vez, com parada a qualquer recusa ou limite (AGENTS §9).
Os resultados vão para "Resultados das sondagens" em `design.md`, não para `data/historico.md`.

- [x] 1.1 Com o Zotero aberto e o acesso local habilitado pelo pesquisador, ler pela API local a coleção de `[zotero] colecao` em `groups/5969244`. Verificação: a resposta tem os mesmos itens e versão da leitura pela API web, registrados em design.md.
- [x] 1.2 Na coleção de teste, tentar pela API local um `POST collections` (subcoleção) e um `PATCH` de etiqueta num item de teste. Verificação: status HTTP e corpo de cada resposta registrados em design.md. Se a escrita for recusada, a frase de D2 fica como está; se for aceita, ajustá-la.
- [x] 1.3 O pesquisador cria (ou autoriza criar) a coleção das buscas e informa o nome dela e a biblioteca. Verificação: o nome está em `[zotero] search_collection` e a biblioteca em `[zotero] library` do `config.toml`, exibidos por `configuracao mostrar`.
- [x] 1.4 Importar numa coleção de teste uma exportação pequena atual (WoS EB2 e Scopus EB2) e reexportá-la em RIS pelas duas vias, com `limit`/`start`. Verificação: em design.md, o número de registros, a paginação observada e, campo a campo, o que `le_arquivo` lê do original e da reexportação. Também a igualdade ou não das listas ordenadas de `chave_dedup`.
- [x] 1.5 Se 1.4 mostrar perda de campo lido pelo leitor ou chave divergente, parar e apresentar as alternativas ao pesquisador antes do grupo 4. Verificação: decisão registrada em design.md (D4/D7) ou nenhuma divergência registrada.

## 2. Configuração: via, coleção das buscas e pasta de temporários

- [x] 2.1 Acrescentar `tmp/` ao `.gitignore`. Verificação: `git check-ignore tmp/x` responde `tmp/x`.
- [x] 2.2 Acrescentar ao `ESQUEMA` de `src/rsl/config.py` as chaves `zotero.acesso`, `zotero.library`, `zotero.search_collection` e `dados.temporarios`, e ao `config.toml` `acesso = "web"`, `temporarios = "tmp"` e `execucoes = "tmp/execucoes"`, com os comentários. Verificação: `python3 -m rsl configuracao mostrar` exibe as três com a origem.
- [x] 2.3 Na carga da configuração, recusar com CONFIGURACAO: `acesso` fora de `local`/`web`; `temporarios` não listado no `.gitignore`; `execucoes` fora de `temporarios`. Verificação: casos novos em `autoteste/configuracao.py`, cada um reprovando com a mutação e passando sem ela.
- [x] 2.4 Atualizar o mapa de `data/` no `README.md`: linha de `tmp/` (cache e regeneráveis, fora do git) e linha de `[dados] execucoes`. Na seção do Zotero, descrever a via `[zotero] acesso`, a chave exigida só na via web e a coleção das buscas. Verificação: o texto cita só chaves que `configuracao mostrar` exibe.

## 3. Cliente único com duas vias

- [x] 3.1 Em `src/rsl/zotero.py`, fazer `Cliente` receber a via (base local sem chave, base web com chave) e criar a fábrica `cliente(ctx)`. Mensagens nomeiam a via; erro de conexão na via local diz que o Zotero tem de estar aberto com o acesso local habilitado. Verificação: autoteste com servidor simulado para as duas vias.
- [x] 3.2 Trocar `Cliente(chave_api())` em `cmd_copiar` e `cmd_completar` pela fábrica. Ler a chave só na via web. Registrar `via` na cópia gravada, sem torná-la campo exigido por `le_copia`, para que a cópia atual continue legível. Verificação: caso "via local sem chave" não sai com CONFIGURACAO; a cópia atual de `data/zotero_sementes.json` continua lida por `aderencia medir`.
- [x] 3.3 Garantir que erro em pedido de escrita vira FONTE_EXTERNA sem novo pedido. Na via local, a mensagem indica `acesso = "web"`. Verificação: caso que conta zero pedidos à base web depois da recusa local, e que reprova se a recusa for silenciada.
- [x] 3.4 Atualizar a docstring de `zotero.py` (acesso, vias, regras de parada nas duas). Verificação: `projeto autoteste` sem regressão nos casos de Zotero existentes (chave, cópia, campos, OpenAlex, completar).
- [x] 3.5 Credenciais da escrita local (escopo acrescentado pela sondagem 1.2, por decisão do pesquisador): `ZOTERO_LOCAL_API_KEY` e `ZOTERO_SERVER_ID` lidos como a chave web só no primeiro pedido de escrita local, enviados só na escrita, ausência é CONFIGURACAO sem pedido; procedimento de obtenção no README. Verificação: autoteste com credenciais sintéticas (cabeçalhos da leitura e da escrita, ausência, chave não impressa), sem ler o `.env` real.
- [x] 3.6 Mesma via em toda a sessão (decisão do pesquisador depois da 1.1, D2a): `completa` recusa com DADOS, sem pedido, a cópia de outra via (sem `via` conta como web); `copia` avisa a troca de via. Verificação: autoteste com cópia web, cópia sem `via` e controle com cópia local.

## 4. Coleções, identificador e obtenção da exportação

- [x] 4.1 Implementar `subcolecoes`, `localiza` (zero → ausente; duas homônimas ou com o mesmo identificador no início → DADOS, nomeando as chaves) e `garante` (cria só quando chamada por quem escreve). Verificação: autoteste com servidor simulado: localização, ausência na leitura sem criação e homônimas reprovando.
- [x] 4.2 Implementar `identificador_execucao` em `src/rsl/busca/registro.py`, conforme D4. Verificação: autoteste prova a invariância à ordem, a diferença com um registro a mais e a diferença com a mesma lista em outra data e hora.
- [x] 4.3 Implementar `obtem_exportacao` (RIS paginado, escrita atômica) e extrair `grava_texto` de `grava_json`, mantendo a recusa de conteúdo com a chave. Verificação: autoteste com servidor simulado: arquivo final legível por `le_arquivo` com o número de registros servido; interrupção no meio deixa o anterior intacto; conteúdo com a chave não é gravado.

## 5. Ponto único de resolução da exportação

- [x] 5.1 Substituir `caminho_do_arquivo` por `exportacao(cfg, c)` (D6) e usá-la em `coleta`, `busca/sensibilidade.py` e na conferência do registro em `src/rsl/dados.py`, retirando o trecho próprio de resolução. Verificação: `grep -rn "caminho_do_arquivo\|RAIZ / caminho" src/rsl` não acha resolução de exportação fora de `exportacao`.
- [x] 5.2 Exportação ausente sai com DADOS, nomeando a execução e indicando a obtenção do Zotero, sem pedido ao Zotero. Verificação: autoteste com execução que tem `identificador` e cache vazio, e com cliente simulado que reprova se for chamado.
- [x] 5.3 Ajustar `autoteste/dados.py` ao novo `[dados] execucoes`. Verificação: `python3 -m rsl projeto autoteste` passa.
- [x] 5.4 Leitura RIS (D9, decisão do pesquisador na 1.5): BOM, `A1`, `C3`, primeiro `DO`, tipo canônico. Verificação: autoteste do leitor com controle; efeito nas análises atuais medido nas duas rodadas e registrado em D9.

## 6. Integração

- [x] 6.1 Com a configuração do projeto, rodar `projeto autoteste`, `documentos conferir`, `dados conferir` e `busca derivar` (ensaio). Verificação: as 8 execuções atuais continuam lidas de `data/execucoes/` pelo campo `arquivo`, com as contagens registradas em D9 (leitor corrigido: 75 repetidos, 156 únicos; únicos da Scopus 58 em EB4 e 15 em EB2), calculadas de novo nesta rodada.
- [x] 6.2 Rodar `openspec validate zotero-como-fonte-unica --strict`. Verificação: sem erro nem aviso.

## Workflow follow-up

- Arquivar a change depois da revisão do pesquisador e sincronizar as specs `acesso-ao-zotero` e `metadados-das-sementes`.
- Revalidar as changes dependentes (`fluxo-das-sementes`, `fluxo-da-execucao-de-busca`, `recursos-das-sondagens`) contra os nomes definidos aqui (`identificador`, `[zotero] library`, `[zotero] search_collection`, `[dados] temporarios`).
- Sem entrada em `data/historico.md` (decisão de ferramenta).
