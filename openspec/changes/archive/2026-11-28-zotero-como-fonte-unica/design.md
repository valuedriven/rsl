# Design

## Context

Motivação em `proposal.md` (Why). Estado atual, conferido no código e nos dados:

- `src/rsl/zotero.py` tem um cliente só da API web (`Cliente`, base `https://api.zotero.org`,
  chave no cabeçalho `Zotero-API-Key`), com uma requisição por vez, sem nova tentativa, e
  parada em 412, 429, 503, `Backoff` e `Retry-After`. O teste injeta o servidor simulado
  pelo parâmetro `abrir`. `sementes copiar` e `sementes completar` constroem o cliente
  diretamente com `Cliente(chave_api())`.
- `[zotero]` tem `biblioteca = "groups/5969244"` e `colecao` (a coleção das sementes). Não há
  chave de via nem de coleção das buscas.
- As exportações estão em `data/execucoes/<base>/*.ris`, ignoradas pelo git (`*.ris` no
  `.gitignore`). As 8 execuções de `data/registro_execucao.json` (WoS e Scopus, EB2 a EB5)
  declaram o caminho em `arquivo`. O caminho resolve-se em dois lugares que não compartilham
  código: `caminho_do_arquivo` em `src/rsl/busca/registro.py`, usado por `coleta` e por
  `busca/sensibilidade.py`, e um trecho próprio em `src/rsl/dados.py` (conferência do
  registro). `[dados] execucoes` só aparece no autoteste de dados e no `README.md`.
- Conferido por leitura das 8 exportações: nenhuma traz cabeçalho com data de exportação. A
  única tag de data (`DA`) aparece em um registro da WoS e é campo do registro.
- `chave_dedup` (DOI em minúsculas ou, sem DOI, título normalizado com 120 caracteres) já é a
  identidade de registro usada na deduplicação e na sensibilidade.
- A configuração é validada contra um esquema fechado (`ESQUEMA` em `src/rsl/config.py`):
  chave nova precisa entrar no esquema, e chave fora dele reprova.

Não verificado, e por isso objeto das sondagens do grupo 1 de `tasks.md`: se a API local do
Zotero 10.0.8 instalado aceita escrita; se ela lê a biblioteca de grupo pelo mesmo caminho
`groups/<id>`; se as duas vias exportam a coleção em RIS (`format=ris`) com paginação; e se
o RIS que o Zotero reexporta preserva os campos que o leitor das análises usa (título,
resumo, palavras-chave, ano, DOI, autores, veículo, idioma, tipo). O que se sabe da API local
vem da documentação do Zotero (endereço `http://localhost:23119/api/`, mesmos caminhos da API
web, sem chave, acesso habilitado nas preferências). Isso é informação de uso declarado, não
de comportamento desta instalação.

## Goals / Non-Goals

**Goals:**
- Um só construtor de cliente, escolhido pela configuração, de que todo acesso ao Zotero
  depende. Nenhum ponto do código constrói cliente por conta própria.
- O identificador da execução como função pura e testável, sem depender do Zotero.
- Um só ponto de resolução do arquivo de uma execução, usado por todos os consumidores.
- Defeito de configuração (cache dentro de `data/`, `tmp/` fora do `.gitignore`) impedido na
  leitura da configuração, e não detectado depois.

**Non-Goals:**
- Nenhum subcomando novo. A importação das exportações para o Zotero, o registro do
  identificador e da coleção de cada execução e o comando que preenche o cache são da change
  `fluxo-da-execucao-de-busca`.
- A cópia das sementes continua em `data/zotero_sementes.json` até a change
  `fluxo-das-sementes`.
- Os pontos de restauração (`data/evidencia/zotero/`) não mudam aqui.
- As saídas regeneráveis de `[saidas] pasta` continuam em `data/` até a change
  `avaliacao-dos-resultados-da-busca`. A pasta de temporários nasce agora, mas só o cache das
  exportações passa a exigi-la.

## Decisions

### D1. Um cliente, duas bases de endereço

`Cliente` recebe a via: `web` usa `https://api.zotero.org` com a chave no cabeçalho; `local`
usa `http://localhost:23119/api` sem chave e sem ler `ZOTERO_API_KEY` nem `.env`. Os caminhos
(`groups/<id>/collections/<chave>/items/top`) são os mesmos. Uma fábrica, `cliente(ctx)`, lê
`[zotero] acesso` e devolve o cliente. `cmd_copiar` e `cmd_completar` passam a usá-la. A
mensagem de erro nomeia a via. Na via local, erro de conexão diz que o Zotero tem de estar
aberto com o acesso local habilitado.

- *Alternativa: dois clientes, um por via.* Rejeitada: as regras de parada (AGENTS §9) teriam
  duas implementações, e uma poderia afrouxar sem a outra.
- *Alternativa: escolher a via sozinho (local se o Zotero responder, web se não).* Rejeitada:
  é a troca de rota que AGENTS §9 proíbe, e tornaria o resultado dependente de o Zotero estar
  aberto.

`[zotero] acesso` é parâmetro da ferramenta, não do protocolo. Recebe padrão no `config.toml`
(`"local"`, por decisão do pesquisador depois das sondagens 1.1 e 1.2) e entra no `ESQUEMA`. O valor se confere na carga da
configuração.

### D2. Escrita só pela via configurada

Qualquer resposta de erro a um pedido de escrita (`POST`, `PATCH`) vira `FonteExterna`. Não
há caminho de código que repita o pedido pela outra via: a garantia é por construção, porque o
cliente conhece uma só base.

A sondagem 1.2 mostrou que a escrita local da 10.0.8 exige `Zotero-Server-ID` (sem ele, 428)
e uma chave da API local (sem ela, 401). Por decisão do pesquisador, o cliente passa a
suportá-las: `ZOTERO_LOCAL_API_KEY` e `ZOTERO_SERVER_ID`, lidas como a chave web (variável
de ambiente ou `.env` listado no `.gitignore`), só no primeiro pedido de escrita, por
`credenciais_locais`. Assim, a leitura local continua sem ler credencial. A falta delas é
CONFIGURACAO antes do pedido. A escrita local recusada indica conferir as duas variáveis ou
escrever pela via web. O pesquisador obtém as credenciais no Zotero da máquina, pelo
procedimento do README; o agente não as obtém nem as recebe.

### D2a. Mesma via em toda a sessão

Decisão do pesquisador, depois da sondagem 1.1: a premissa é manter a mesma via em toda a
sessão. A 1.1 mostrou que as versões (da biblioteca e de cada item) só valem na via que as
leu, e que a ordem das etiquetas muda entre vias. O que a premissa protege fica garantido por
construção onde o dano é real. `completa` recusa com DADOS, antes de qualquer pedido, a cópia
de outra via (`via_da_copia`; a cópia sem `via` conta como `web`). Sem essa recusa, o plano
daria 412 em todo item. `copia` não recusa, porque é o único modo de trocar de via, mas avisa
no relato. A comparação das palavras-chave continua por lista, e a ordem dentro da mesma via
não foi medida.

### D3. Coleções localizadas pelo nome, criadas só por quem escreve

Chaves novas, nomeadas pelo pesquisador: `[zotero] search_collection` (NOME da coleção das
buscas, localizada na raiz da biblioteca) e `[zotero] library` (biblioteca das buscas). As
duas são sem padrão no código e entram no `config.toml` depois de o pesquisador criar a
coleção (tarefa 1.3). Sem `library`, as buscas ficam na biblioteca de `[zotero] biblioteca`.
As buscas ficam numa biblioteca de grupo própria (`groups/6781444`), separada da das sementes
(`groups/5969244`), por decisão do pesquisador. `library` e `biblioteca` aceitam a forma da
API (`groups/<id>`, `users/<id>`) ou o endereço da biblioteca de grupo no site
(`https://www.zotero.org/groups/<id>/<nome>`); `Configuracao.biblioteca` devolve a forma da
API, e `Configuracao.buscas` o par (biblioteca, nome).
Funções:

- `subcolecoes(cliente, biblioteca, mae)` lista as filhas (`collections/<mae>/collections`,
  ou `collections/top` com `mae` None, paginado);
- `colecao_das_buscas(ctx, cliente)` localiza a coleção das buscas pelo nome, na raiz, sem
  criar;
- `localiza(filhas, nome)` devolve a única filha com o nome, ou com o identificador no início
  do nome no caso das execuções; zero é `None`; duas ou mais é `DadosInvalidos`, nomeando as
  chaves;
- `garante(cliente, biblioteca, mae, nome)`, só para subcomandos que escrevem, cria a filha
  ausente (`POST collections`) e devolve a chave.

Nome da coleção de execução: `<identificador> <sigla> <expressão> <data>`. O identificador vem
no início, para que a localização não dependa do resto do nome, que é só legibilidade.

- *Alternativa: guardar a chave da coleção das buscas no `config.toml`.* Preterida pelo
  pesquisador: o nome é o que ele vê na interface. A homônima na raiz reprova, como as filhas.
- *Alternativa: guardar a chave de cada coleção no `config.toml`.* Rejeitada: uma chave por
  base e por execução, editada à mão, divergiria do Zotero. O registro da execução (change 3)
  guarda a chave da coleção dela. A localização pelo nome serve à criação e à conferência.

### D4. Identificador da execução: hash da execução, não dos bytes

`identificador_execucao(sigla, expressao, data_hora, registros)` = 12 primeiros hexadecimais
do SHA-256 de `json.dumps([sigla, expressao, data_hora, sorted(chave_dedup(r) for r in
registros)], ensure_ascii=False, separators=(",", ":"))`. A lista mantém as repetições: duas
cópias do mesmo registro na exportação contam duas vezes. A função fica em
`src/rsl/busca/registro.py`, ao lado de `chave_dedup`, e é pura.

Por que este objeto:

- **Não os bytes da exportação.** As exportações verificadas não embutem data, então os bytes
  seriam estáveis. Mas o arquivo original sai do disco (proposta), e o que se reobtém do
  Zotero é uma reexportação, com outros bytes. Um hash de bytes não se recalcula depois.
- **Não as chaves dos itens no Zotero.** Não existem antes da importação e mudam numa
  reimportação ou numa mesclagem de duplicatas.
- **Não só o conteúdo.** A execução é um evento: a mesma consulta, repetida noutro dia com o
  mesmo retorno, é outra execução, e ficaria com o mesmo nome de coleção. Por isso a data e
  hora entram no hash.
- **Ordem indiferente.** A ordem dos registros depende da ordenação escolhida na interface da
  base. Ordenar as chaves torna o identificador independente dela.

12 hexadecimais são 48 bits. Para algumas dezenas de execuções, a colisão é desprezível, e a
que ocorrer entre irmãs é recusada por D3 (homônimas). O identificador calcula-se no registro
da execução (change 3) a partir da exportação original da base. Recalculá-lo a partir da
reexportação do Zotero só é possível se `chave_dedup` sobreviver à ida e volta, e isso a
sondagem 1.4 mede. Essa conferência é da change 3, não desta.

### D5. Pasta de temporários garantida na configuração

Chave nova `[dados] temporarios = "tmp"`, no `ESQUEMA` e no `config.toml`.
`[dados] execucoes` passa a `"tmp/execucoes"`. Na carga da configuração, duas recusas com
`ConfiguracaoInvalida`:

1. a pasta não está listada no `.gitignore` da raiz (linha `tmp`, `tmp/`, `/tmp` ou `/tmp/`;
   mesma lógica de `_linha_ignorada`, que já protege o `.env`);
2. `[dados] execucoes` resolvido não fica dentro de `[dados] temporarios` resolvido.

A recusa 1 só vale para pasta dentro da raiz do projeto: pasta fora dela não entra no controle
de versão, e o `.gitignore` da raiz não a alcança (o autoteste usa esse caso, com diretório
temporário do sistema).

A recusa na carga torna impossível gravar cache em `data/` sem que a configuração reprove
antes. A change `fluxo-das-sementes` estende a regra 2 a `[dados] zotero`.

A mudança de `[dados] execucoes` não afeta as 8 execuções atuais, porque cada uma declara o
caminho completo em `arquivo`, e esse caminho continua resolvido como antes (D6).

### D6. Ponto único de resolução da exportação

`caminho_do_arquivo(c)` dá lugar a `exportacao(cfg, c)`, em `busca/registro.py`:

- execução com `identificador` (gravado pela change 3): `<[dados] execucoes>/<sigla>/<identificador>.ris`;
- execução sem `identificador` e com `arquivo`: o caminho de `arquivo`, como hoje.

`coleta`, `busca/sensibilidade.py` e a conferência do registro em `dados.py` passam a chamar
essa função. O trecho próprio de `dados.py` sai. Nenhum consumidor consulta o Zotero: arquivo
ausente é `DadosInvalidos`, com a execução e a indicação da obtenção. Enquanto o comando de
obtenção não existir (change 3), a indicação diz "obter a exportação do Zotero", sem nome de
comando. A change 3 a troca pelo nome do comando.

Os nomes `identificador` e `colecao_zotero` dos campos da execução são combinados com a
change 3, que os grava. Aqui só se lê `identificador`.

### D7. Obtenção da exportação

`obtem_exportacao(cliente, biblioteca, colecao, destino)` pede
`collections/<colecao>/items/top?format=ris` paginado (`limit`, `start`, `Total-Results`).
Depois concatena as páginas e grava com escrita atômica: arquivo temporário no mesmo
diretório, depois `os.replace`. `grava_json` passa a delegar a um `grava_texto` comum, que
mantém a recusa de conteúdo com a chave. Esta change não tem chamador real da função; o
autoteste a exercita com servidor simulado. Se a sondagem 1.4 mostrar que `format=ris` não
pagina numa das vias, a paginação se ajusta antes da tarefa 4.3. A interface e a spec não
mudam.

A 1.4 confirmou a paginação de `format=ris` nas duas vias. Depois que o pesquisador apagou as
coleções de teste, a via local respondeu **200 com `Total-Results: 0`** ao pedido de itens de
uma coleção que não existe mais, e não 404 (verificado em 2026-11-28 nas três coleções
apagadas). Por isso `obtem_exportacao` recusa com DADOS a coleção sem itens e não grava nada:
a execução sem registros não tem exportação, e um cache vazio passaria por legítimo.

### D9. Leitura RIS do original e da reexportação

Decisão do pesquisador depois da sondagem 1.4 (1.5). `le_ris` lê o original da base e a
reexportação do Zotero pelos mesmos campos:

- o BOM UTF-8 inicial é retirado (antes escondia o `TY` do primeiro registro da WoS);
- `A1` são autores, como `AU`;
- `C3`, onde o Zotero exporta o título dos anais, é a fonte, como `JO` e `T2`;
- só o primeiro `DO` vale (o item do Zotero guarda um DOI, e a chave se calcula dele);
- o tipo sai na forma canônica (`TIPOS_RIS`): `CONF` = `CPAPER`, e o rótulo
  `label.ris.referenceType.BOOK_CHAPTER` da Scopus = `CHAP`.

Efeito nas análises atuais, medido por `busca derivar`, sensibilidade e fidelidade de EB2 e
EB3, nas duas rodadas, com o leitor antigo e com o novo: a deduplicação passa de 74 para 75
repetidos, e os únicos de 157 para 156. O capítulo `10.4018/979-8-3693-1054-0.ch009`, com dois
DOIs na WoS e um na Scopus, passa a ser reconhecido como o mesmo. Os únicos da Scopus caem de
59 para 58 (EB4) e de 16 para 15 (EB2). Sensibilidade e fidelidade não mudam nas contagens. A
coluna de DOI da amostra muda em 2 linhas, e os autores da WoS ganham os de `A1`.

### D8. Autoteste

Os casos ficam nos grupos existentes (`autoteste/zotero.py`, `autoteste/configuracao.py`,
`autoteste/busca.py`, `autoteste/dados.py`), com o servidor simulado por `abrir`. Cada caso de
recusa prova que reprova (AGENTS §8): a mutação que o motiva (via inválida, `tmp/` fora do
`.gitignore`, cache em `data/`, homônimas, escrita recusada na via local) produz o código
esperado, e a configuração correta não o produz. O caso "sem troca de via" conta os pedidos
feitos à base web no servidor simulado e exige zero.

## Risks / Trade-offs

- [A API local da 10.0.8 não escreve] → `sementes completar --gravar` exige `acesso = "web"`.
  A mensagem diz isso, e o pesquisador escolhe. Nada troca de via sozinho.
- [O Zotero precisa estar aberto na via local] → erro de conexão com mensagem própria. A via
  `local` é o padrão; a via `web` fica como alternativa na configuração, sem troca automática.
- [Reexportação RIS do Zotero perde ou muda campo que o leitor usa] → a análise leria outro
  corpus. A sondagem 1.4 compara o original com a reexportação, campo a campo. Divergência
  bloqueia a migração da change 3, não esta change, que não migra nada.
- [Quem clona o repositório depende do Zotero para preencher `tmp/`] → é a decisão do
  pesquisador (Zotero canônico). A biblioteca de grupo é o ponto de reprodução, e a via `web`
  dá acesso sem o desktop.
- [Identificador truncado colide] → recusado como homônimo em D3, nunca resolvido em silêncio.
- [Escrever na biblioteca do pesquisador durante a sondagem] → só com autorização dele, numa
  coleção de teste criada para isso, e removida ao fim, por ele ou a pedido dele.

## Migration Plan

1. Sondagens (grupo 1), com autorização. Resultados neste design, em "Resultados das
   sondagens".
2. `.gitignore` ganha `tmp/`; `config.toml` ganha `[dados] temporarios`, `[zotero] acesso` e,
   depois da criação da coleção, `[zotero] library` e `[zotero] search_collection`; `[dados] execucoes` passa a
   `tmp/execucoes`.
3. Código e autoteste (grupos 2 a 5). `projeto autoteste`, `documentos conferir` e
   `dados conferir` passam com as 8 execuções atuais, que continuam lidas de `data/execucoes/`
   pelo campo `arquivo`.

Reversão: restaurar `config.toml` e `.gitignore`. Nenhum dado se move nesta change.

Esta change não gera entrada em `data/historico.md`: é decisão de ferramenta.

## Resultados das sondagens

Nada aqui se preenche de memória. As respostas brutas ficaram fora do repositório, no
diretório da sessão que rodou as sondagens; o que se registra é o observado.

### 1.1 Leitura pela API local (2026-11-28, 12:05, Zotero 10.0.8)

Pedido: `GET groups/5969244/collections/V2C73IKE/items/top?format=json`, paginado, pela via
local (`http://localhost:23119/api`, sem chave) e pela via web, em sequência, com
`le_colecao`. As duas vias responderam 200.

- Itens: 19 nas duas vias, com as mesmas chaves.
- Versões: **diferem**. A da biblioteca é 13131 na via local e 46385 na web, e a de cada um
  dos 19 itens também difere (ex.: `EHI7ECVW`, 13092 local e 46342 web). A via local numera
  as versões pelo banco da máquina, não pelo servidor.
- Conteúdo: igual. Nos campos que `campos()` extrai, a única diferença é a **ordem** das
  etiquetas (18 itens). No `data` bruto, a ordem de `collections` difere em 1 item, e a web
  traz campos vazios que a via local omite. `meta` da web traz `createdByUser`, que a local
  não traz.

Consequências para o código, a decidir antes de usar a via local (pendências, não resolvidas
aqui):
- `diferencas` compara `palavras_chave` como lista. Trocar de via, ou só reler, relataria
  como "alterado" a mera mudança de ordem das etiquetas.
- A versão da cópia e a versão de cada item só se comparam dentro da mesma via. Um plano
  feito sobre uma cópia local e gravado pela web daria conflito (412) em todo item. Isso não
  ocorre hoje, porque a escrita usa a via da cópia, mas a cópia não impede a mistura.

### 1.2 Escrita pela API local (2026-11-28, 12:06, Zotero 10.0.8)

Pedido: `POST groups/6781444/collections`, corpo `[{"name": "sondagem 1.2 - teste (pode
apagar)"}]`, pela via local, sem nova tentativa.

- Resposta: **HTTP 428**, corpo `Zotero-Server-ID not provided`, com o cabeçalho
  `Zotero-Server-ID` na resposta, além de `X-Zotero-Version: 10.0.8` e
  `Zotero-Schema-Version: 44`. Nenhuma coleção foi criada.
- O `PATCH` de etiqueta não foi tentado: viria com a mesma pré-condição.
- Parou-se aí, pela regra de parada diante de recusa (AGENTS §9).

Segunda tentativa, autorizada pelo pesquisador (2026-11-28, 12:11): o mesmo pedido, com o
cabeçalho `Zotero-Server-ID` que a primeira resposta trouxe.

- Resposta: **HTTP 401**, corpo `API key required -- POST /api/local/authorize to obtain one`,
  cabeçalho `WWW-Authenticate: Zotero-API-Key realm="Zotero Local API"`. Nenhuma coleção foi
  criada.
- Verificado: a escrita pela API local da 10.0.8 exige, além de `Zotero-Server-ID`, uma
  chave própria da API local, obtida por um fluxo de autorização (`POST
  /api/local/authorize`). A chave da API web não foi enviada, e não se verificou se ela
  valeria aqui.
- Não verificado: como funciona esse fluxo (se pede confirmação na interface do Zotero) e se,
  com a chave, a escrita é aceita. O fluxo é autenticação e cabe ao pesquisador (AGENTS §9);
  o agente não o iniciou.
- O `PATCH` de etiqueta não foi tentado.
Terceira tentativa, com as credenciais locais obtidas pelo pesquisador e guardadas no `.env`
(2026-11-28, 12:50), pelo código de produção (`Cliente("local")`, `credenciais_locais`), um
pedido por vez:

1. `garante` na raiz de `groups/6781444` (`GET collections/top`, depois `POST collections`):
   **aceito**. A coleção `sondagem 1.2 - teste (pode apagar)` foi criada, com a chave
   `TF3S445J`. Fica para o pesquisador apagar.
2. `POST items` (item de teste na coleção `TF3S445J`): **HTTP 401**. O corpo da resposta não
   foi registrado, porque o cliente não o inclui na mensagem. Nenhum item foi criado.
3. O `PATCH` de etiqueta não foi tentado: não havia item de teste, e parou-se na recusa.

Verificado: com as duas credenciais, a API local da 10.0.8 aceitou criar coleção e recusou
criar item (401), na mesma biblioteca e com a mesma chave. Não verificado: por que o item foi
recusado (permissão da chave local por tipo de objeto, ou outra condição) e se o `PATCH` de
item existente seria aceito.

Quarta tentativa, com uma chave local nova (2026-11-28, 12:57). O pesquisador informou que a
chave anterior valia para uma só requisição. Pedidos com os cabeçalhos do cliente
(`Zotero-API-Key` com a chave local, `Zotero-Server-ID`), um por vez, com o corpo registrado:

1. `POST groups/6781444/items` (item de teste na coleção `TF3S445J`): **200**, item `6G3ZD873`
   criado, versão 5.
2. `PATCH groups/6781444/items/6G3ZD873` (etiqueta `sondagem-1.2`, com
   `If-Unmodified-Since-Version: 5`): **204**.
3. `GET` do item, sem chave: versão 6, etiqueta `sondagem-1.2`, coleção `TF3S445J`.

Verificado: com as duas credenciais, a API local da 10.0.8 aceita criar coleção, criar item e
alterar etiqueta com controle de versão. A chave nova valeu para dois pedidos de escrita
seguidos. A hipótese "a chave vale para uma só requisição" não se confirmou com esta chave.
Por que a anterior foi recusada no segundo pedido não foi verificado.

Objetos de teste a apagar pelo pesquisador: coleção `TF3S445J` e item `6G3ZD873`, em
`groups/6781444`.

- D2 (antes das credenciais): sem a chave local, a escrita pela via local é recusada (428,
  depois 401). Com elas, é aceita (acima). A mensagem de recusa local indica conferir as
  credenciais ou escrever pela via web, o que vale nos dois casos. A frase
  "a escrita exige `[zotero] acesso = "web"`" continua correta enquanto o cliente não
  suportar a chave local. Suportá-la seria escopo novo: chave, cabeçalho e regra de guarda,
  como os da chave web.

### 1.4 Ida e volta pelo Zotero (2026-11-28, 13:10–13:20, Zotero 10.0.8), parcial

Por decisão do pesquisador, os itens foram criados pela API, e não pelo importador do Zotero.
Assim, a sondagem mede o conversor desta sondagem mais a exportação RIS do Zotero, e não o
importador.

**Conversão.** Tags RIS brutas → item: `TY` → tipo (`JOUR` journalArticle, `CPAPER`/`CONF`
conferencePaper, `CHAP`/`BOOK_CHAPTER` bookSection); `TI` título; `AU` e `A1` autores, `ED`
editores; `KW` etiquetas, sem repetição exata; `AB` resumo; `PY` data; primeiro `DO`; `T2`
veículo do tipo; `VL`, `IS`, `SP`-`EP`, `UR`. Os campos válidos por tipo vieram do esquema do
Zotero instalado (`schema.json` versão 40, dentro de `omni.ja`), porque a API local não tem
`items/new` (404). Nenhum campo ficou sem lugar. Não se transportaram `N1`, `AN`, `AD`, `CP`,
`DA`, `M3`, `DB`, `C6`, `C7`, `ST`, que o leitor das análises não lê.

**Escrita, via local.** Coleção `sondagem 1.4 - teste (pode apagar)` (`6IVIFSRV`) na raiz de
`groups/6781444`, com a subcoleção `wos-eb2` (`3J83WLTY`). O `POST items` dos 49 itens da WoS
EB2 estourou o tempo limite do cliente (45 s). Uma leitura depois mostrou os 49 itens
criados. Parou-se aí: a subcoleção da Scopus EB2 não foi criada, e os 61 itens não foram
enviados.

**Reexportação, WoS EB2.** `GET collections/3J83WLTY/items/top?format=ris&limit=20`, com
`start` 0, 20 e 40, nas duas vias: 200, `Total-Results` 49, páginas de 20, 20 e 9. A
paginação funciona nas duas vias. As duas reexportações diferem em bytes só pela ordem dos
registros e das linhas, e a comparação com o original dá o mesmo resultado nas duas.

**O que `le_arquivo` lê, original × reexportação (49 registros, pares pelo título):**

| Campo | Diferem | Causa verificada |
| --- | --- | --- |
| titulo, resumo, ano, id_base, idioma | 0 | — |
| palavras_chave | 42 (local), 43 (web) | só a ordem; como conjunto, 0 |
| fonte | 16 | o Zotero exporta o título dos anais (conferencePaper) em `C3`, que o leitor não lê: **perda** em toda conferência |
| tipo | 17 | 16 `CPAPER` → `CONF` (código do Zotero). 1 `''` → `JOUR`: o original da WoS começa com BOM UTF-8, e `le_ris` não lê o `TY` do primeiro registro (defeito do leitor, anterior a esta change) |
| autores | 2 | o original traz autores em `A1`, que o leitor não lê; a reexportação os traz em `AU` (ganho, não perda) |
| doi | 1 | o original traz dois `DO`, que o leitor junta (`a; b`); o item do Zotero guarda um só |

**`chave_dedup`:** as listas ordenadas **diferem** em 1 de 49, o registro dos dois `DO`
(`doi:10.4018/979-8-3693-1054-0.ch009; 10.4018/979-8-3693-1054-0` no original,
`doi:10.4018/979-8-3693-1054-0.ch009` na reexportação). Um identificador D4 calculado da
exportação original não se recalcula da reexportação para essa execução.

**Decisões do pesquisador sobre esses resultados (1.5, 2026-11-28), aplicadas em
`busca/leitores.py` (`le_ris`), ver D9:** o leitor passa a ler `C3` como fonte e a tratar
`CONF` e `CPAPER` como o mesmo tipo; só o primeiro `DO` vale; corrigem-se o BOM e o `A1`.

**Scopus EB2 (13:21–13:26).** Subcoleção `scopus-eb2` (`6NNMXNTA`). Os 61 itens foram enviados
em lotes de 10 (cerca de 12 s por lote): 200, sem falha. Reexportação local com `limit=20`: 61
registros em 20+20+20+1. Pela web, a primeira leitura viu 8 itens (sincronização em curso); a
segunda, 61.

**Mesclagem automática (verificada).** Depois do envio da Scopus, as subcoleções `wos-eb2` e
`scopus-eb2` têm 38 itens em comum, todos com chaves criadas pelo `POST` da Scopus. A
biblioteca tem 73 itens de topo (49 + 61 − 38, mais o item da 1.2). Os itens da WoS foram
mesclados nos da Scopus, que passaram a pertencer às duas coleções. O agente da mesclagem não
foi verificado (hipótese: o Zoplicate, com mesclagem automática). Efeito medido na WoS
(reexportação local depois da mesclagem, leitor antigo): título difere em 14, resumo em 38,
autores em 38, fonte em 44, palavras-chave (como conjunto) em 26 e ano em 1 (`2024` →
`2025`). Com mesclagem, a coleção de uma base deixa de reproduzir a exportação dela.
**Decisão do pesquisador (1.5, 2026-11-28):** desligar a mesclagem automática na biblioteca das
buscas. A configuração é do Zotero, feita pelo pesquisador; o código não a verifica. A
deduplicação continua nas análises, pela `chave_dedup`, e mesclagem no Zotero, se houver, só
depois de lidas as exportações. D4 e D7 ficam como estão. A change
`fluxo-da-execucao-de-busca` deve considerar isso, e a conferência que ela já prevê (registros
obtidos × `registros_lidos`) não detecta mesclagem, que não muda o número de itens da coleção.

**Comparação com o leitor corrigido (D9):**

| Reexportação | Registros | `chave_dedup` iguais | Campos que diferem |
| --- | --- | --- | --- |
| WoS, local e web (antes da mesclagem) | 49 | sim | só a ordem das palavras-chave |
| Scopus, local e web (depois da mesclagem) | 61 | sim | palavras-chave como conjunto em 21 (as da WoS, somadas pela mesclagem); nos demais, só a ordem |

Sem mesclagem, a ida e volta (conversão desta sondagem + exportação RIS do Zotero) preserva o
que o leitor lê, e a `chave_dedup` sobrevive. O identificador D4 se recalcula da
reexportação.

Objetos de teste a apagar pelo pesquisador: coleção `6IVIFSRV`, com as subcoleções
`3J83WLTY` e `6NNMXNTA` e os 72 itens.
