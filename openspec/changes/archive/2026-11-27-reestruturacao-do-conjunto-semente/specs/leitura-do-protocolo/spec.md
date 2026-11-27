# Spec Delta

## ADDED Requirements

### Requirement: Conjunto-semente lido do arquivo mínimo de sementes
O conjunto-semente SHALL ser lido do arquivo TOML de `[documentos] sementes`, uma tabela
`[[sementes]]` por estudo, com o esquema mínimo da gramática: `id`, `doi`,
`referencia_curta` e `bases`, obrigatórios, e `alinhamento_facetas`, `verificacao` e `nota`,
opcionais. Os dados bibliográficos, o resumo e as palavras-chave MUST vir da cópia da coleção
do Zotero, e o arquivo de sementes MUST NOT guardá-los.

#### Scenario: Arquivo atual
- **WHEN** o arquivo de sementes tem as sementes de SE1 a SE19 com os campos do esquema
  mínimo, e a cópia da coleção tem um item para cada DOI
- **THEN** a leitura aprova, e a distribuição por base exibida por `configuracao mostrar` é
  calculada do campo `bases`

#### Scenario: Título vindo do Zotero
- **WHEN** o título do item do Zotero de uma semente contém um ponto seguido de maiúscula
- **THEN** o título lido é o campo inteiro do item

#### Scenario: Distribuição calculada
- **WHEN** o arquivo é lido
- **THEN** a contagem por base, as incidências e as sementes em mais de uma base são
  calculadas do campo `bases`

### Requirement: Verificação declarada pelo pesquisador
`verificacao = true` SHALL significar que o pesquisador declara conferidos os dados
bibliográficos do item no Zotero, e a declaração basta, sem registro de onde e como se
conferiu. `false` ou ausente é conferência pendente. Texto ou outro tipo MUST reprovar a
leitura.

#### Scenario: Verificação como texto
- **WHEN** uma semente traz `verificacao = "CONFIRMADA"`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo

#### Scenario: Verificação pendente
- **WHEN** uma semente traz `verificacao = false` ou não traz o campo
- **THEN** a leitura aprova, e `projeto pendencias` relata a verificação pendente

#### Scenario: Verificação conferida
- **WHEN** uma semente traz `verificacao = true` sem `nota`
- **THEN** `projeto pendencias` não relata verificação pendente para ela

### Requirement: Arquivo mínimo de sementes fora do esquema reprova
Arquivo de sementes ausente MUST terminar com CONFIGURACAO, nomeando a chave e o caminho.
MUST reprovar com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo: TOML inválido; campo
obrigatório ausente ou de tipo errado; campo desconhecido; `id` fora da forma `SEn`,
repetido ou fora da sequência a partir de SE1; `doi` ausente, fora da forma `10.x/…` ou
repetido; base fora da tabela de bases, com outra grafia ou repetida; chave de
`alinhamento_facetas` fora da tabela de facetas, ou com frase vazia.

#### Scenario: Lacuna na numeração
- **WHEN** o arquivo tem SE1, SE2 e SE4, sem SE3
- **THEN** a leitura reprova, nomeando SE4 e o `id` esperado, SE3

#### Scenario: Sigla com outra grafia
- **WHEN** a semente SE2 cita a base `WoS` e a tabela de bases declara `wos`
- **THEN** a leitura reprova, nomeando SE2 e a sigla

#### Scenario: Faceta inexistente no alinhamento
- **WHEN** a semente SE7 traz `alinhamento_facetas = { FCT9 = "ontologia" }` e a tabela de
  facetas vai até FCT4
- **THEN** a leitura reprova, nomeando SE7 e a faceta

#### Scenario: Frase de alinhamento vazia
- **WHEN** a semente SE7 traz `alinhamento_facetas = { FCT1 = "" }`
- **THEN** a leitura reprova, nomeando SE7 e FCT1

#### Scenario: Semente sem DOI
- **WHEN** uma semente não traz `doi`
- **THEN** a leitura reprova, nomeando a semente e o campo `doi`

#### Scenario: Campo desconhecido
- **WHEN** uma semente traz o campo `titlo`, os campos retirados `autores`, `ano`, `titulo`,
  `veiculo`, `volume`, `numero`, `paginas`, `facetas` ou `veiculo_conferido`, os campos
  retirados antes `escopo`, `papel`, `tipo`, `alinhamento`, `eric` e `observacoes`, ou o
  campo `semente` do esquema intermediário
- **THEN** a leitura reprova, nomeando a semente e o campo

#### Scenario: Arquivo ausente
- **WHEN** `[documentos] sementes` aponta um arquivo que não existe
- **THEN** o subcomando termina com CONFIGURACAO, nomeando a chave e o caminho, e nenhuma
  semente é presumida

### Requirement: Pendência de semente relatada, sem reprovar
`projeto pendencias` SHALL relatar, nomeando a semente, sem reprovar a leitura:

- `alinhamento_facetas` vazio ou ausente;
- alinhamento sem nenhuma faceta marcada `Sim` em "Âncora obrigatória", enquanto o
  pesquisador não decide a regra; com o alinhamento vazio, só "alinhamento a informar";
- item do Zotero sem resumo ou sem palavras-chave na cópia da coleção;
- semente sem registro na OpenAlex.

#### Scenario: Alinhamento a informar
- **WHEN** a semente SE3 não traz `alinhamento_facetas`
- **THEN** a leitura aprova, e `projeto pendencias` relata SE3 com alinhamento a informar

#### Scenario: Validação sem âncora
- **WHEN** a semente SE5 traz `alinhamento_facetas = { FCT3 = "metodologia da problematização" }`,
  e FCT1 e FCT2 são as âncoras
- **THEN** a leitura aprova, e `projeto pendencias` relata SE5 sem faceta âncora

#### Scenario: Validação sem alinhamento
- **WHEN** a semente SE3 não traz `alinhamento_facetas`
- **THEN** `projeto pendencias` relata SE3 com alinhamento a informar, e não relata SE3 sem
  faceta âncora

#### Scenario: Resumo ausente
- **WHEN** o item do Zotero da semente SE5 não tem resumo na cópia da coleção
- **THEN** a leitura aprova, e `projeto pendencias` relata SE5 com resumo ausente

### Requirement: Semente retirada não deixa resto na evidência
Semente retirada SHALL sair do arquivo de sementes e das saídas regeneradas. `dados
conferir` MUST reprovar arquivo da subpasta `referencias/` de `[dados] evidencia` nomeado
com um `SEn` que não está no arquivo de sementes, e arquivo das subpastas `openalex/` e
`crossref/` — resposta ou marcador de 404 — cujo DOI não está no arquivo de sementes,
nomeando o arquivo. As outras subpastas da evidência MUST
NOT ser conferidas por essa regra.

#### Scenario: Evidência de semente retirada
- **WHEN** SE10 é retirada do arquivo e `SE10_crossref.json` continua em
  `data/evidencia/referencias/`
- **THEN** `dados conferir` reprova, nomeando `SE10_crossref.json`

#### Scenario: Resposta da OpenAlex de semente retirada
- **WHEN** a semente de DOI `10.5753/wetie.2023.236130` é retirada e a resposta da OpenAlex
  desse DOI continua em `data/evidencia/openalex/`
- **THEN** `dados conferir` reprova, nomeando o arquivo

#### Scenario: Renumeração sem renomear evidência
- **WHEN** SE15 é retirada e as seguintes são renumeradas
- **THEN** nenhum arquivo de `data/evidencia/openalex/` precisa ser renomeado, e `dados
  conferir` aprova

### Requirement: Autoteste prova a reprovação do esquema mínimo
O autoteste SHALL injetar numa cópia do arquivo de sementes, a partir das sementes lidas,
cada um destes defeitos e exigir PROTOCOLO_ILEGIVEL: `doi` ausente, `doi` fora da forma,
`doi` repetido, faceta do alinhamento fora da tabela, frase de alinhamento vazia, lacuna na
numeração dos `id`, campo bibliográfico retirado (`titulo`) e o campo `semente` do esquema
intermediário.

#### Scenario: DOI ausente reprova
- **WHEN** o autoteste retira o `doi` de uma semente numa cópia
- **THEN** a cópia reprova com PROTOCOLO_ILEGIVEL; se for aprovada, o autoteste falha

#### Scenario: Defeito não detectado
- **WHEN** a cópia com o campo `semente` é aprovada
- **THEN** o autoteste falha, nomeando o defeito

### Requirement: Autoteste prova a reprovação da junção com o Zotero
O autoteste SHALL injetar numa cópia da coleção o item de uma semente sem título, e retirar
dela o item de outra semente, e exigir a reprovação em cada caso. SHALL também exigir que
`dados conferir` reprove a evidência de semente inexistente.

#### Scenario: Item sem título
- **WHEN** o autoteste esvazia o título do item de uma semente numa cópia da coleção
- **THEN** a leitura reprova; se for aprovada, o autoteste falha

#### Scenario: Item retirado da cópia
- **WHEN** o autoteste retira da cópia da coleção o item de uma semente
- **THEN** a leitura reprova com DADOS; se for aprovada, o autoteste falha

### Requirement: Semente casada com o item do Zotero pelo DOI
A leitura SHALL casar cada semente com o item da cópia da coleção que tem o mesmo DOI,
comparado em caixa baixa e sem prefixo de URL. DOI do arquivo de sementes sem item na cópia,
ou com mais de um item, MUST reprovar com DADOS, nomeando a semente e o DOI. Item da cópia
cujo DOI não está no arquivo de sementes SHALL ser relatado, sem reprovar.

#### Scenario: DOI sem item
- **WHEN** a semente SE19 tem um DOI que nenhum item da cópia traz
- **THEN** a leitura reprova com DADOS, nomeando SE19, o DOI e `sementes copiar`

#### Scenario: Item a mais na coleção
- **WHEN** a cópia traz o item de DOI `10.5220/0012471400003645`, que nenhuma semente cita
- **THEN** a leitura aprova, e `projeto pendencias` relata o item como fora do arquivo de
  sementes

#### Scenario: DOI com caixa ou prefixo diferente
- **WHEN** o arquivo traz `10.1111/EXSY.12246` e o item traz `https://doi.org/10.1111/exsy.12246`
- **THEN** a semente casa com o item

### Requirement: Referência curta conferida contra o Zotero
`referencia_curta` SHALL ter a forma `<sobrenome> <ano>: <início do título>`, conferida
contra o item da cópia: o ano igual ao do item, o resto sem acento, caixa nem pontuação. `documentos conferir` MUST reprovar a que não
confere, nomeando a semente e a forma sugerida; a leitura MUST NOT reprovar por isso.

#### Scenario: Sobrenome trocado
- **WHEN** o sobrenome da referência curta não é o do primeiro autor do item
- **THEN** `documentos conferir` reprova, nomeando a semente e a forma sugerida

#### Scenario: Ano trocado
- **WHEN** o ano da referência curta não é o do item
- **THEN** `documentos conferir` reprova, nomeando a semente e a forma sugerida

#### Scenario: Reticências finais
- **WHEN** a referência curta termina em `…` depois das primeiras palavras do título do item
- **THEN** `documentos conferir` aprova

#### Scenario: Referência curta conferida
- **WHEN** a semente traz `referencia_curta = "Alvarenga 2023: Objetos de aprendizagem organizados…"` e o item do Zotero tem Alvarenga como primeiro autor, ano 2023 e título que começa por essas palavras
- **THEN** `documentos conferir` aprova

#### Scenario: Título corrigido no Zotero
- **WHEN** o título do item mudou no Zotero e a referência curta não começa mais pelas mesmas palavras
- **THEN** `documentos conferir` reprova, nomeando a semente e a forma sugerida, e `aderencia medir` continua funcionando

#### Scenario: Referência curta ausente
- **WHEN** a semente não traz `referencia_curta`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo

### Requirement: Alinhamento das facetas por frase
`alinhamento_facetas` SHALL ser uma tabela TOML cujas chaves são `FCTn` da tabela de facetas
do protocolo e cujos valores são frases curtas, não vazias, que explicam por que a semente
se alinha à faceta. Faceta ausente da tabela significa semente não alinhada a ela.

#### Scenario: Alinhamento lido
- **WHEN** a semente traz
  `alinhamento_facetas = { FCT1 = "ontologia de domínio", FCT2 = "ensino de matemática na educação básica" }`
- **THEN** a leitura aprova, e a semente fica alinhada à FCT1 e à FCT2, com as duas frases

#### Scenario: Forma de lista recusada
- **WHEN** a semente traz `alinhamento_facetas = ["FCT1", "FCT2"]`
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL, nomeando a semente e o campo

## REMOVED Requirements

### Requirement: Conjunto-semente lido do arquivo de sementes
**Reason**: o arquivo de sementes passa ao esquema mínimo: os dados bibliográficos vêm do Zotero, o DOI é obrigatório e `facetas` dá lugar a `alinhamento_facetas`.
**Migration**: ver "Conjunto-semente lido do arquivo mínimo de sementes"; migrar o arquivo conforme o plano de migração do design.

### Requirement: Arquivo de sementes fora do esquema reprova
**Reason**: o domínio de reprovação muda: DOI ausente reprova, os campos bibliográficos passam a desconhecidos e a faceta é validada no alinhamento.
**Migration**: ver "Arquivo mínimo de sementes fora do esquema reprova".

### Requirement: Dado ou juízo pendente relatado, sem reprovar
**Reason**: o DOI ausente deixa de ser pendência (passa a reprovar), e `facetas` dá lugar a `alinhamento_facetas`; entram resumo ausente e semente sem registro na OpenAlex.
**Migration**: ver "Pendência de semente relatada, sem reprovar".

### Requirement: Semente retirada não deixa resto
**Reason**: a planilha de aderência deixa de existir, e a evidência da OpenAlex, nomeada pelo DOI, entra na conferência.
**Migration**: ver "Semente retirada não deixa resto na evidência".

### Requirement: Autoteste prova a reprovação do esquema estruturado
**Reason**: o esquema estruturado é substituído pelo mínimo, e o DOI ausente passa a reprovar.
**Migration**: ver "Autoteste prova a reprovação do esquema mínimo".
