# metadados-das-sementes Specification

## Purpose
Obter, guardar e usar os dados bibliográficos e textuais das sementes a partir da coleção
do Zotero e da OpenAlex, ligados ao arquivo de sementes pelo DOI, de modo reprodutível e
sem acesso ao vivo nos comandos de análise.

## Requirements

### Requirement: Cópia da coleção do Zotero
`sementes copiar` SHALL ler, pela via de acesso de `[zotero] acesso`, os itens de topo da
coleção configurada em `[zotero]` e gravar a resposta bruta no arquivo de `[dados] zotero`,
com a biblioteca, a coleção, a versão da biblioteca, a via usada e a data e hora da leitura.
Antes de gravar, o comando SHALL relatar os itens acrescentados, os retirados e os campos
alterados em relação à cópia anterior.

#### Scenario: Primeira cópia
- **WHEN** se executa `sementes copiar` sem cópia anterior
- **THEN** a resposta bruta da coleção fica gravada em `[dados] zotero`, com a data e hora da leitura, e o relato lista todos os itens como acrescentados

#### Scenario: Item alterado no Zotero
- **WHEN** o título de um item mudou no Zotero desde a cópia anterior
- **THEN** o relato nomeia o DOI do item, o campo `titulo` e os dois valores antes de gravar a nova cópia

#### Scenario: Cópia pela via local
- **WHEN** `[zotero] acesso = "local"` e se executa `sementes copiar`
- **THEN** a cópia gravada registra a via `local`, e a diferença para uma cópia anterior lida
  pela via `web` se relata pelos mesmos campos

### Requirement: Comandos de análise não consultam o Zotero
Todo subcomando que usa sementes, exceto `sementes copiar` e `sementes completar`, SHALL ler
os dados do Zotero só da cópia em `[dados] zotero`, sem acesso à rede, e SHALL imprimir a
data e hora da cópia lida.

#### Scenario: Sem rede
- **WHEN** se executa `aderencia medir` sem acesso à rede e com a cópia presente
- **THEN** a medição termina normalmente e informa a data da cópia usada

#### Scenario: Cópia ausente
- **WHEN** o arquivo de `[dados] zotero` não existe
- **THEN** o subcomando sai com o código DADOS e a mensagem indica `sementes copiar`

### Requirement: Campos extraídos do item do Zotero
A leitura SHALL extrair de cada item da cópia, sem transcrição: autores (criadores do tipo
autor, na ordem do item), ano (da data interpretada pelo Zotero), título, veículo (título da
publicação, dos anais ou do livro, conforme o tipo do item), volume, número, páginas, DOI
(do campo DOI ou, na falta, da linha `DOI:` do campo extra), resumo e palavras-chave (as
etiquetas do item).

#### Scenario: Trabalho em anais
- **WHEN** o item é do tipo trabalho em anais
- **THEN** o veículo da semente é o título dos anais do item

#### Scenario: DOI no campo extra
- **WHEN** o item não tem o campo DOI preenchido e o campo extra traz `DOI: 10.5771/9783956507762-484`
- **THEN** o DOI do item é `10.5771/9783956507762-484`

#### Scenario: Item sem título
- **WHEN** o item casado com uma semente tem título vazio, nenhum autor ou nenhum ano
- **THEN** a leitura reprova, citando o `id` da semente, o DOI e a chave do item

### Requirement: Chave da API web fora do projeto
Quando a via de acesso é `web`, o acesso à API web do Zotero SHALL usar a chave da variável
de ambiente `ZOTERO_API_KEY` ou, na falta dela, a da linha `ZOTERO_API_KEY=` do `.env` da raiz
do projeto. O `.env` MUST ser recusado com CONFIGURACAO quando o `.gitignore` não o listar. A
chave MUST NOT ser gravada em arquivo versionado nem impressa; em relato, só os quatro
últimos caracteres podem aparecer.

#### Scenario: Chave no .env
- **WHEN** `ZOTERO_API_KEY` não está definida e o `.env` listado no `.gitignore` traz a linha
  da chave
- **THEN** `sementes copiar` usa a chave do `.env`

#### Scenario: .env fora do .gitignore
- **WHEN** o `.env` traz a chave e o `.gitignore` não o lista
- **THEN** `sementes copiar` sai com CONFIGURACAO, nomeando o `.gitignore`, sem imprimir a chave

#### Scenario: Variável ausente
- **WHEN** `[zotero] acesso = "web"` e se executa `sementes copiar` sem `ZOTERO_API_KEY`
  definida e sem `.env`
- **THEN** a saída tem o código CONFIGURACAO, e nenhum outro subcomando deixa de funcionar por isso

#### Scenario: Chave não impressa
- **WHEN** qualquer subcomando que acessa o Zotero termina, com sucesso ou com erro
- **THEN** a saída e os arquivos gravados não contêm a chave inteira

### Requirement: Consulta à OpenAlex por DOI
`sementes metadados` SHALL consultar a OpenAlex pelo DOI de cada semente, uma consulta por
vez, e gravar a resposta bruta em `data/evidencia/openalex/`, num arquivo cujo nome deriva
do DOI normalizado. A consulta MUST NOT enviar e-mail nem identificação pessoal do
pesquisador.

#### Scenario: Resposta gravada
- **WHEN** a OpenAlex responde 200 para o DOI de uma semente
- **THEN** a resposta bruta fica gravada no arquivo do DOI, e o relato informa se ela traz resumo e quantas palavras-chave

#### Scenario: DOI sem registro
- **WHEN** a OpenAlex responde 404 para um DOI
- **THEN** nenhuma resposta se grava para esse DOI, só o marcador do 404 com a data e hora, a semente aparece como "sem registro na OpenAlex" e a consulta segue para o DOI seguinte

#### Scenario: Só as pendentes
- **WHEN** se executa `sementes metadados` sem `--todas` e alguns DOIs já têm resposta ou marcador de 404
- **THEN** só os DOIs sem resultado registrado são consultados

### Requirement: Parada na OpenAlex sem nova tentativa
Diante de uma resposta da OpenAlex diferente de 200 e 404, ou de um erro de rede,
`sementes metadados` SHALL interromper as consultas restantes sem nova tentativa e relatar o
DOI e a resposta.

#### Scenario: Limite excedido
- **WHEN** a OpenAlex responde 429 na quinta consulta
- **THEN** as consultas restantes não se fazem, as quatro respostas anteriores ficam gravadas e a saída nomeia o DOI e o código 429

### Requirement: Resumo complementar pelo Crossref
`sementes metadados --fonte crossref` SHALL consultar o Crossref, uma consulta por vez e com
as mesmas regras de parada da OpenAlex, só para as sementes sem resumo em fonte nenhuma: sem
resumo na resposta da OpenAlex (ou com o marcador do 404) e sem resumo no item da cópia da
coleção. A resposta bruta SHALL ser gravada em `data/evidencia/crossref/`, com nome derivado
do DOI. A consulta ao Crossref MUST NOT ser feita automaticamente depois de erro, bloqueio ou
limite da OpenAlex.

#### Scenario: Semente sem resumo na OpenAlex
- **WHEN** a resposta da OpenAlex de uma semente não traz resumo e o item do Zotero também não
- **THEN** `sementes metadados --fonte crossref` consulta o Crossref para esse DOI e grava a resposta

#### Scenario: Erro na OpenAlex
- **WHEN** `sementes metadados` é interrompido por erro de rede na OpenAlex
- **THEN** nenhuma consulta ao Crossref é feita nessa execução

### Requirement: Pendência de dados das sementes calculada das fontes
`projeto pendencias` SHALL relatar, por semente e sem reprovar, calculando das respostas
gravadas, dos marcadores de 404 e da cópia: "sem resposta da OpenAlex (não consultada ou
interrompida)", "sem registro na OpenAlex" e "resumo ausente em todas as fontes", esta com a
indicação de que o pesquisador preenche o resumo no Zotero.

#### Scenario: Consulta interrompida
- **WHEN** a consulta à OpenAlex foi interrompida antes do DOI de uma semente
- **THEN** `projeto pendencias` relata a semente como sem resposta da OpenAlex, e não como sem registro nem como sem resumo

#### Scenario: Último recurso
- **WHEN** nem a OpenAlex, nem o Crossref, nem o item do Zotero trazem resumo para uma semente
- **THEN** `projeto pendencias` relata "resumo ausente em todas as fontes", indicando o preenchimento no Zotero pelo pesquisador

### Requirement: Plano de complemento do Zotero
`sementes completar` SHALL imprimir, por item, o que gravaria no Zotero a partir das
respostas da OpenAlex, do Crossref e da cópia da coleção: o resumo da OpenAlex ou, na falta
dele, o do Crossref, só onde ele está vazio, e as
palavras-chave como etiquetas automáticas que ainda não existem no item. Sem `--gravar`, o
comando MUST NOT gravar nada.

#### Scenario: Resumo já preenchido
- **WHEN** o item já tem resumo e a OpenAlex traz outro
- **THEN** o plano não inclui o resumo desse item

#### Scenario: Sem --gravar
- **WHEN** se executa `sementes completar` sem `--gravar`
- **THEN** o plano é impresso e nenhum item do Zotero muda

### Requirement: Gravação no Zotero só acrescenta
Com `--gravar`, `sementes completar` SHALL aplicar o plano item a item, com controle de
versão do item, sem apagar etiqueta nem sobrescrever resumo. Conflito de versão, limite de
uso ou pedido de espera do Zotero SHALL interromper a gravação sem nova tentativa. Ao
terminar, o comando SHALL regravar a cópia da coleção.

#### Scenario: Conflito de versão
- **WHEN** o item foi alterado no Zotero depois da cópia e a gravação recebe conflito de versão
- **THEN** a gravação para nesse item, os itens anteriores ficam gravados e a saída nomeia o DOI e pede uma nova `sementes copiar`

#### Scenario: Etiquetas existentes preservadas
- **WHEN** um item com 15 etiquetas recebe 5 palavras-chave da OpenAlex, 2 delas já existentes
- **THEN** o item fica com 18 etiquetas

### Requirement: Retirada de item da coleção a pedido
`sementes completar` SHALL retirar da coleção só os itens cujo DOI for indicado em
`--retirar`, e só com `--gravar`. A retirada MUST NOT apagar o item da biblioteca. DOI de
semente do arquivo de sementes em `--retirar` MUST ser recusado com USO, sem pedido ao Zotero. Sem
`--retirar`, os itens da coleção cujo DOI não está no arquivo de sementes SHALL aparecer só
no relato.

#### Scenario: Item fora do arquivo de sementes
- **WHEN** a coleção tem um item cujo DOI não está no arquivo de sementes e não se passa `--retirar`
- **THEN** o relato lista o item, e ele continua na coleção

#### Scenario: Retirada de semente ativa recusada
- **WHEN** se executa `sementes completar --gravar --retirar` com o DOI de uma semente do arquivo de sementes
- **THEN** a saída tem o código USO, e nenhum item do Zotero muda

#### Scenario: Retirada pedida
- **WHEN** se executa `sementes completar --retirar 10.5753/wetie.2023.236130 --gravar`
- **THEN** o item sai da coleção `sementes` e continua na biblioteca do grupo

### Requirement: Ensaio seco por campo
`aderencia ensaiar` SHALL procurar os termos de cada faceta no título, nas palavras-chave e
no resumo de cada semente, por frase inteira e sem distinguir acento nem caixa, e imprimir
cada termo encontrado com o campo onde apareceu. O comando MUST NOT gravar arquivo.

#### Scenario: Termo só no resumo
- **WHEN** o termo `ontology` da FCT1 aparece no resumo e não aparece no título
- **THEN** o ensaio imprime `ontology` na FCT1 dessa semente com a marca do resumo

#### Scenario: Nada gravado
- **WHEN** se executa `aderencia ensaiar`
- **THEN** nenhum arquivo do projeto é criado ou alterado

### Requirement: Composição da executada no ensaio
`aderencia ensaiar` SHALL relatar quantas sementes satisfazem a composição da expressão
executada só pelo título e quantas pelos três campos juntos. O relato SHALL dizer que é
ensaio e que as palavras-chave vêm da OpenAlex, e não da base.

#### Scenario: Contagem nos dois níveis
- **WHEN** o ensaio termina
- **THEN** a saída traz as duas contagens, cada uma com o total de sementes, e a ressalva sobre a origem das palavras-chave

### Requirement: Campo ausente não é termo ausente
Quando a cópia não traz resumo ou palavras-chave de uma semente, `aderencia ensaiar` SHALL
marcar o campo como ausente para essa semente, separado do resultado sem termo.

#### Scenario: Semente sem resumo
- **WHEN** o item de uma semente não tem resumo
- **THEN** o ensaio marca "resumo ausente" para a semente, e a falta de termo no resumo não se apresenta como resultado

### Requirement: Faceta alinhada sem termo
`aderencia ensaiar` SHALL listar, para cada semente, as facetas presentes em
`alinhamento_facetas` sem nenhum termo da faceta em campo algum, como indício de lacuna de
vocabulário.

#### Scenario: Indício de lacuna
- **WHEN** a semente tem a FCT3 no alinhamento e nenhum termo da FCT3 no título, nas palavras-chave ou no resumo
- **THEN** o ensaio lista a FCT3 dessa semente como faceta alinhada sem termo
