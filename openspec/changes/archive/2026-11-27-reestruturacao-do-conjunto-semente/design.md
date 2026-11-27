# Design

## Context

Ver `proposal.md` — Why. O estado que condiciona o desenho:

- `leitura.sementes()` monta, para cada semente, um dicionário com `id`, `autores`, `ano`,
  `titulo`, `veiculo`, `volume`, `numero`, `paginas`, `doi`, `bases`, `facetas`, a
  conferência e a `chave` "Autor ano". `aderencia medir` (casamento por título),
  `aderencia diagnosticar` (DOI), `procedimentos gerar` (lista das sementes com DOI),
  `configuracao mostrar` e `projeto pendencias` consomem esse dicionário.
- Nenhum código lê as colunas manuais de `semente_aderencia.csv`.
- A coleção `sementes` fica na biblioteca de grupo "fatores". Dos 21 itens, só 1 tem resumo
  e palavras-chave. Dois itens não estão no TOML, e quatro dos antigos divergem dele (SE1,
  SE3, SE10; diferença só de caixa na SE10).
- A API local do Zotero só permite leitura e depende do Zotero aberto. O conector só
  acrescenta. A API web lê e grava com chave.
- Numa consulta de teste (SE14), a OpenAlex devolveu `abstract_inverted_index` e
  `keywords` com pontuação, sem chave. As `keywords` são atribuídas pela OpenAlex: não são
  as do autor nem as da base.
- A spec `interface-de-comando` proíbe `sementes sincronizar`.
- Plugins do Zotero instalados: Linter for Zotero, ZotMeta e Zoplicate. Nenhum usa a
  OpenAlex, e nenhum pode ser acionado pela linha de comando.

## Goals / Non-Goals

**Goals:**
- O dicionário de semente que os consumidores recebem não muda de forma, exceto `facetas`,
  que vira `alinhamento_facetas`. Muda só de onde cada campo vem.
- Todo comando que usa sementes funciona sem rede e sem Zotero aberto.
- Escrita no Zotero só acrescenta ou completa, exceto a retirada de item da coleção, que
  depende de pedido explícito.
- A migração não perde dado conferido: o que o TOML tinha e o Zotero não tem é acertado no
  Zotero antes de sair do TOML.

**Non-Goals:**
- Criar no Zotero o registro bibliográfico de semente nova. O pesquisador acrescenta o item
  pelo DOI, na interface, com ou sem o Linter.
- Conferir as palavras-chave da OpenAlex contra o vocabulário de cada base.
- Ler o Zotero pela API local.

## Decisions

**D1. Junção pelo DOI na leitura, com o mesmo dicionário de saída.** `leitura.sementes()`
lê o TOML e a cópia da coleção, casa pelo DOI normalizado (caixa baixa, sem prefixo de URL)
e monta o dicionário de hoje com os campos bibliográficos vindos da cópia. Os consumidores
não mudam.
- *Alternativa:* cada consumidor consultar a cópia. Espalharia a junção por cinco
  módulos.
- *Alternativa:* chave do item do Zotero como ligação. Recusada pelo pesquisador: é opaca e
  só vale nessa biblioteca.

**D2. Cópia da coleção versionada, lida da API web.** `sementes copiar` grava a resposta
bruta da API (itens de topo da coleção, formato `json`) em `[dados] zotero`, por exemplo
`data/zotero_sementes.json`, com a biblioteca, a coleção, a versão da biblioteca e a data e
hora da leitura. Os campos se extraem da resposta bruta na leitura, sem transcrição. Antes
de gravar, o comando relata o que mudou em relação à cópia anterior.
- *Alternativa:* API local, sem chave. Recusada: depende do Zotero aberto e lê edições
  ainda não sincronizadas. Com a chave, um caminho só basta para ler e gravar.
- *Alternativa:* ler o Zotero ao vivo em todo comando. Recusada: os comandos dependeriam
  da rede, e o resultado de ontem não se reproduziria.

**D3. Mapeamento de campos do Zotero.**
- `autores`: os criadores do tipo `author`, como "Sobrenome, Nome", na ordem do item.
- `ano`: o ano de `meta.parsedDate`. Sem ano, reprova.
- `titulo`: `title`.
- `veiculo`: `publicationTitle`, `proceedingsTitle` ou `bookTitle`, conforme `itemType`.
- `volume`, `numero` (`issue`) e `paginas` (`pages`): como estão no item.
- `doi`: `DOI` ou, na falta, a linha `DOI:` de `extra`.
- `resumo` (`abstractNote`) e `palavras_chave` (as etiquetas do item): campos novos do
  dicionário, usados só pelo ensaio.

Título vazio, ano ausente ou nenhum autor reprova a leitura, como hoje, e a mensagem cita o
DOI e a chave do item.

**D4. Chave da API web.** Fica na variável de ambiente `ZOTERO_API_KEY` ou, na falta dela,
na linha `ZOTERO_API_KEY=` do `.env` da raiz, emitida pelo pesquisador com escrita só na
biblioteca de grupo. O `.env` só é aceito se o `.gitignore` o listar: do contrário, a leitura
sai com CONFIGURACAO, porque a chave iria ao controle de versão no próximo `git add`. Nunca se grava em arquivo do projeto
nem se imprime; em relato, aparecem só os quatro últimos caracteres. A biblioteca e a
coleção ficam em `[zotero]` do `config.toml` (`biblioteca = "groups/<id>"`,
`colecao = "<chave>"`). Sem a variável, os subcomandos que acessam o Zotero saem com
CONFIGURACAO e os demais funcionam.

**D5. OpenAlex: uma consulta por vez, resposta bruta por DOI.** `sementes metadados`
consulta `https://api.openalex.org/works/doi:<doi>` para cada semente e grava a resposta em
`data/evidencia/openalex/<doi-normalizado>.json`.
- As consultas são sequenciais e sem nova tentativa (AGENTS.md §9). Resposta 429, 403 ou
  diferente de 200 e 404 interrompe tudo e é relatada.
- 404 vira pendência "sem registro na OpenAlex", não ausência de resumo.
- Não se envia e-mail nem identificação pessoal; o agente de usuário é genérico.
- O resumo se reconstrói de `abstract_inverted_index`, e as palavras-chave são
  `keywords[].display_name`.
- O nome do arquivo vem do DOI, não do `id`: retirar ou renumerar semente não exige
  renomear evidência.
- O 404 deixa um marcador `<doi-normalizado>.404` com a data e hora, para que "sem registro
  na OpenAlex" não se confunda com "não consultada" nem com "consulta interrompida" (falha
  de acesso não é ausência de informação).
- Por padrão, só se consulta o DOI sem resultado registrado; `--todas` refaz todas.

**D6. Gravação no Zotero: completar, não sobrescrever.** `sementes completar` lê as
respostas brutas da OpenAlex e a cópia da coleção, e imprime o que faria:
- resumo onde `abstractNote` está vazio;
- palavras-chave como etiquetas automáticas (`type = 1`), acrescentadas às que já existem
  e nunca apagadas;
- itens a retirar, só os indicados em `--retirar <DOI>`, e só da coleção, sem apagar o
  item.

Com `--gravar`, aplica tudo isso pela API web, item a item, com `If-Unmodified-Since-Version`.
Conflito de versão (412), limite de uso ou `Backoff` interrompem a gravação sem nova
tentativa. Ao terminar, regrava a cópia (D2). Antes da primeira gravação, a cópia anterior
fica guardada como ponto de restauração.
- *Alternativa:* sobrescrever o resumo sempre. Recusada: apagaria o resumo da SE1, que veio
  de outra fonte.
- *Alternativa:* criar itens novos a partir da OpenAlex. Recusada: o registro bibliográfico
  ficaria transcrito de uma fonte secundária, e esse é o papel do pesquisador com o Zotero
  (Non-Goals).

**D7. `alinhamento_facetas` como tabela TOML embutida.** As chaves são as `FCTn` do
protocolo e os valores, texto não vazio.
- Tabela vazia ou ausente vira pendência.
- Semente sem faceta âncora é relatada (PD21).
- O agente propõe as frases a partir da cópia (título, palavras-chave, resumo) e as
  apresenta ao pesquisador. Só grava no TOML o que ele confirmar. Nenhum campo de "proposto"
  entra no esquema: a confirmação está no próprio controle de versão.
- A frase descreve o conceito e não repete o termo que o ensaio encontra. A skill diz isso,
  porque é juízo e o código não tem como conferir.

**D8. Ensaio seco por campo, em `aderencia ensaiar`.** Para cada semente e faceta, o ensaio
imprime os termos encontrados, cada um marcado com o campo onde apareceu (T título, P
palavras-chave, R resumo). Também imprime:
- quantas sementes satisfazem a composição da executada só pelo título e quantas pelos
  três campos juntos;
- a semente com a faceta em `alinhamento_facetas` e sem termo dela em campo nenhum, como
  indício de lacuna de vocabulário;
- resumo ou palavras-chave ausentes na cópia, sinalizados como "campo ausente" e não como
  "sem termo".

O casamento é o de hoje (frase inteira, sem acento nem caixa). `aderencia planilhar` sai, e
o nome antigo dá USO.

**D9. Subcomandos sob `sementes`.** `sementes metadados`, `sementes completar` e
`sementes copiar`. `sementes sincronizar` continua sem existir e dá USO, como a spec exige.
- *Alternativa:* um só comando que consulta e grava. Recusada: a consulta externa, a
  escrita no Zotero e a leitura da cópia falham por motivos diferentes, e separá-las deixa
  cada falha numa etapa.

**D10. Retirada de semente mais simples.** Sem planilha e com a evidência nomeada pelo DOI,
os passos da skill são três:
1. tirar a tabela do TOML e renumerar as seguintes;
2. atualizar as menções em `data/pendencias.json`;
3. registrar a retirada no histórico, com a correspondência entre os `id` antigos e os
   novos.

Retirar o item da coleção é pedido à parte (`completar --retirar`).

**D11. Recuperação também pelo DOI.** Sem a coluna `recuperada`, não sobra registro humano
que confirme o casamento por prefixo de título. Com o DOI obrigatório, `aderencia medir`
passa a contar como recuperada a semente cujo DOI aparece na exportação da executada, além
do casamento exato de título, e o relato diz por qual dos dois casou. Isso aplica a
fórmula do protocolo, que prevê recuperação "por identificador bibliográfico quanto por
correspondência de referência". O casamento por prefixo sem DOI continua sendo só indício.
- *Alternativa:* manter a confirmação humana num campo do TOML por semente e base.
  Recusada: devolveria ao TOML o controle por base que a planilha tinha.

**D12. Fonte complementar e último recurso.** O resumo que a OpenAlex não traz (404 ou 200
sem `abstract_inverted_index`) pode vir do Crossref, por `sementes metadados --fonte
crossref`, que consulta só as sementes ainda sem resumo em fonte nenhuma (nem na OpenAlex, nem
no item do Zotero) e grava a resposta bruta em `data/evidencia/crossref/<doi-normalizado>.json`,
com as mesmas regras de D5.
- O complemento **não é automático depois de erro**: erro de rede, bloqueio, limite ou
  resposta inesperada da OpenAlex interrompe a execução (AGENTS.md §9: sem nova tentativa e
  sem outra rota). Só 404 e 200 sem resumo, que não são erro, tornam a semente elegível, e a
  consulta ao Crossref é uma execução à parte, pedida.
- O Crossref só traz resumo quando a editora o deposita, e não traz palavras-chave (`subject`
  é a classificação do periódico). Medido sobre o conjunto-semente inteiro (respostas brutas em
  `data/evidencia/openalex/` e `data/evidencia/crossref/`), todo resumo do Crossref coincide
  com o da OpenAlex, que tem também resumos ausentes no Crossref: no conjunto atual, o
  complemento não acrescentou resumo. Fica como salvaguarda para semente nova, de custo baixo.
- *Alternativa:* trocar a OpenAlex pelo Crossref como fonte principal. Recusada pela mesma
  medição: perderia as palavras-chave de todas as sementes e os resumos que só a OpenAlex
  tem, sem ganho de resumo. O Crossref segue como fonte de conferência dos dados
  bibliográficos (`conferir-referencia`), que é o seu forte: metadado depositado pela
  editora.
- **Último recurso, o pesquisador**: a semente sem resumo em fonte nenhuma fica como
  pendência "resumo ausente em todas as fontes", e o pesquisador preenche o resumo no Zotero,
  que `sementes completar` preserva (D6).
- A pendência não se transcreve: `projeto pendencias` a calcula das respostas gravadas, dos
  marcadores de 404 e da cópia — "sem resposta da OpenAlex (não consultada ou interrompida)",
  "sem registro na OpenAlex", "resumo ausente em todas as fontes".
- `sementes completar` usa o resumo da OpenAlex e, na falta dele, o do Crossref.
- *Alternativa:* Semantic Scholar. Recusada por ora: sem chave, o limite é compartilhado e
  o 429 é frequente. *Alternativa:* página da editora. Recusada: seria rastejamento (§9).

**D13. Transição em duas fases.** O arquivo de sementes guarda os dados bibliográficos
completos na primeira fase, e a redução dos campos fica para a segunda.
- **Fase 1:** `doi` passa a obrigatório; `alinhamento_facetas` entra como campo opcional, ao
  lado de `facetas`, que continua lido até a confirmação das frases; a cópia da coleção
  passa a entrada obrigatória e a leitura junta TOML e cópia pelo DOI, trazendo `resumo` e
  `palavras_chave` da cópia. Os campos bibliográficos continuam vindo do TOML, e cada
  divergência entre TOML e Zotero é pendência de `projeto pendencias`, decidida pelo
  pesquisador e corrigida no Zotero.
- **Fase 2:** saem do esquema os campos bibliográficos, `veiculo_conferido` e `facetas`; os
  dados bibliográficos passam a vir da cópia; a `nota` se enxuga; o relato de migração sai do
  código; as skills e o protocolo ficam sem os campos retirados; a retirada de semente fica
  em três passos (D10); e se adota a proteção de `--retirar` contra DOI do arquivo de
  sementes (decisão do pesquisador): tirar da coleção o item de semente ativa quebraria a
  leitura de todos os comandos, e por isso se recusa com USO.
- A change só se arquiva no fim da fase 2: as specs descrevem o estado final, e a fase 1 é
  estado intermediário da implementação.
- *Alternativa:* change própria para a fase 2. Possível, mas exigiria dividir as specs já
  escritas sem ganho para a revisão.

**D14. `referencia_curta`: identificação mínima legível no TOML.** Sem os campos
bibliográficos (fase 2), a tabela de cada semente ficaria só com `id` e DOI, ilegível para
quem edita o arquivo. `referencia_curta` é um texto curto, na forma
`"<Sobrenome do primeiro autor> <ano>: <início do título>"`, por exemplo
`referencia_curta = "Alvarenga 2023: Objetos de aprendizagem organizados com base no padrão"`.
- É auxílio de leitura, não dado: os dados continuam no Zotero. Por isso se **confere contra
  a cópia**, para não virar segunda fonte que diverge em silêncio: o sobrenome tem de ser o do
  primeiro autor do item, o ano, o do item, e o título abreviado, as primeiras palavras do título do item,
  comparados sem acento, sem caixa e sem pontuação; reticências finais são aceitas.
- Divergência reprova `documentos conferir`, nomeando a semente e a forma sugerida, e não a
  leitura: os comandos de análise continuam funcionando, e só a conferência acusa o rótulo
  desatualizado (por exemplo, depois de corrigir o título no Zotero).
- `projeto pendencias` relata a semente sem `referencia_curta` e sugere a forma, calculada da
  cópia (sobrenome, ano e as oito primeiras palavras do título), para o pesquisador colar no TOML.
  Nenhum subcomando grava o TOML.
- Fase 1: opcional. Fase 2: obrigatório, porque passa a ser a única identificação legível.
- *Alternativa:* a `chave` "Autor ano" já calculada. Recusada como único recurso: não aparece
  no TOML, e "Autor ano" não distingue dois trabalhos do mesmo autor no mesmo ano.

## Risks / Trade-offs

- [As palavras-chave da OpenAlex não são as da base, e o ensaio pode acertar onde a busca
  falha, ou o contrário] → o ensaio diz que é ensaio e de onde vêm as palavras-chave; quem
  mede é `aderencia medir`, e quem explica é `aderencia diagnosticar`.
- [Semente sem resumo na OpenAlex, provável em periódico brasileiro] → "campo ausente"
  no ensaio e pendência própria. Preencher o resumo à mão no Zotero continua possível e é
  preservado (D6).
- [Cópia desatualizada em relação ao Zotero] → `copiar` relata a diferença, e os comandos
  imprimem a data da cópia que leram.
- [Edição na interface ainda não sincronizada não aparece na API web] → a skill manda
  sincronizar o Zotero antes de `copiar`.
- [O Linter ou o ZotMeta alteram dados sem que se perceba] → a diferença aparece no relato
  de `copiar` e no controle de versão da cópia.
- [Vazamento da chave] → variável de ambiente, nunca impressa, sem arquivo de chave no
  repositório.
- [Escrita visível ao grupo inteiro] → só acréscimo e complemento; a retirada depende de
  pedido explícito; há cópia anterior para restaurar.
- [A cópia passa a ser entrada obrigatória, e sem ela nada que use semente funciona] → a
  mensagem de erro aponta `sementes copiar`, e a cópia é versionada.

## Migration Plan

1. Arquivar `verificacao-binaria-das-sementes` e `fidelidade-por-base-e-casamento-por-campo`.
2. O pesquisador emite a chave e define `ZOTERO_API_KEY`; o projeto registra `[zotero]`
   no `config.toml`.
3. `sementes copiar`, com o código novo e o TOML ainda completo (fase 1, D13). Um relato de migração
   compara campo a campo o TOML e a cópia. Cada divergência é resolvida pelo pesquisador
   e corrigida **no Zotero**: páginas da SE1; volume e número da SE3; caixa da SE10; SE13 e
   SE19 contra o Crossref.
4. `sementes metadados`, depois `sementes completar` (ler o plano) e
   `sementes completar --gravar`, com `--retirar` para os dois itens fora do TOML.
5. O agente propõe as frases de `alinhamento_facetas` a partir da cópia, e o pesquisador
   confirma.
6. Migrar o TOML: tirar os campos bibliográficos e `veiculo_conferido`, trocar `facetas`
   pelo alinhamento confirmado, enxugar a `nota`.
7. Remover `data/semente_aderencia.csv` e `[saidas] aderencia`; regenerar os
   procedimentos; conferir que a lista de sementes de cada procedimento não mudou.
8. Rodar `documentos conferir`, `dados conferir`, `projeto autoteste` e `aderencia ensaiar`.

**Restauração:** o repositório volta por `git revert`. No Zotero, as gravações só
acrescentaram, e a cópia anterior ao passo 4 permite restaurar resumo e etiquetas item a
item.

## Open Questions

- O nome do arquivo da cópia (`data/zotero_sementes.json`) pode mudar na implementação sem
  efeito nas specs: o caminho vem de `[dados] zotero`.
