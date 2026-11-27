# Proposal

## Why

O controle do conjunto-semente está dividido entre `docs/conjunto_semente.toml` e
`data/semente_aderencia.csv`, e a planilha não entrega nada próprio. As colunas manuais
nunca são lidas pelo código. A recuperação já se calcula das exportações, e a indexação
declarada já está em `bases`. O arquivo de sementes, por sua vez, repete à mão dados
bibliográficos que o Zotero do grupo já guarda, e a repetição já diverge do Zotero (SE1,
SE3, SE10). O campo `facetas` guarda só siglas e não diz por que a semente pertence a cada
faceta. O ensaio seco olha só o título, enquanto a busca alcança título, resumo e
palavras-chave, de modo que o resultado só serve como limite inferior.

O pesquisador decidiu:
- o **controle e o juízo** ficam no arquivo de sementes, e os **dados** ficam no Zotero;
- o TOML guarda o mínimo possível, e o **DOI** liga os dois;
- resumo e palavras-chave vêm da **OpenAlex**;
- as sementes vêm sempre dos pesquisadores.

## What Changes

- **Arquivo de sementes mínimo.** **BREAKING**: cada `[[sementes]]` passa a ter só `id`,
  `doi`, `bases`, `alinhamento_facetas`, `verificacao` e, se for o caso, `nota`. Saem do
  esquema `autores`, `ano`, `titulo`, `veiculo`, `volume`, `numero`, `paginas`, `facetas` e
  `veiculo_conferido`; qualquer um deles passa a reprovar como campo desconhecido. O `doi`
  passa a ser **obrigatório**: semente sem DOI reprova a leitura, e a pendência "DOI
  ausente" deixa de existir.
- **Zotero como fonte dos dados.** Autoria, ano, título, veículo, volume, número, páginas,
  resumo e palavras-chave de cada semente vêm do item da coleção `sementes` (biblioteca de
  grupo) que tem o mesmo DOI. Os comandos não consultam o Zotero ao vivo: leem uma
  **cópia da coleção** versionada no repositório. A leitura junta TOML e cópia pelo DOI. DOI
  do TOML sem item na cópia reprova, e item da cópia sem DOI no TOML é relatado.
- **Resumo e palavras-chave pela OpenAlex.** Um subcomando consulta a OpenAlex por DOI, um de
  cada vez, e grava a resposta bruta. Outro grava no Zotero, pela API web com chave do
  pesquisador, o resumo onde ele está vazio e as palavras-chave como etiquetas automáticas.
  Esse mesmo subcomando retira da coleção os itens indicados, só a pedido explícito.
- **`alinhamento_facetas` no lugar de `facetas`.** É uma tabela de `FCTn` para uma frase
  curta com o motivo do alinhamento, por exemplo
  `alinhamento_facetas = { FCT1 = "ontologia de domínio", FCT2 = "cursos de pós-graduação" }`.
  Chave fora das facetas do protocolo e frase vazia reprovam. O agente propõe as frases a
  partir do título, das palavras-chave e do resumo, e o pesquisador confirma.
- **Excluir a planilha de aderência.** **BREAKING**: saem `data/semente_aderencia.csv`, a
  chave `[saidas] aderencia` e `aderencia planilhar`. O ensaio seco passa a ser
  `aderencia ensaiar`, que só imprime no terminal.
- **Ensaio seco por campo.** O ensaio verifica título, palavras-chave e resumo e diz em
  qual campo cada termo foi encontrado. Também aponta a faceta que está em
  `alinhamento_facetas` mas não tem termo em campo nenhum: é indício de lacuna de
  vocabulário.
- **Enxugar `nota`.** Saem a fórmula de conferência repetida, o resumo do conteúdo (que
  passa ao alinhamento) e os dados da referência (que passam aos campos do Zotero). A
  `nota` fica para observação do pesquisador.
- **Retirar o controle de origem**, e com ele os restos de exigência de origem ou de
  procedimento de composição por semente no protocolo, nas skills e nas specs.
- **Atualizar a coleção `sementes`**: remover os itens que não estão no TOML, acertar
  as divergências bibliográficas antes de tirar os campos do TOML, e preencher resumo e
  palavras-chave.
- Ajustar as skills `definir-conjunto-semente`, `testar-aderencia-das-expressoes` e
  `conferir-referencia`, o README, o guia de procedimentos, o catálogo, os procedimentos de
  busca regenerados, os textos de `aderencia medir` e de `aderencia diagnosticar` que citam
  a planilha, e os autotestes.
- Fora do escopo: a regra para semente sem faceta âncora (PD21), a etapa de indexação base
  por base, e a conferência das palavras-chave da OpenAlex contra o vocabulário de cada
  base.

## Capabilities

### New Capabilities
- `metadados-das-sementes`: a OpenAlex consultada por DOI com resposta bruta, a gravação
  no Zotero pela API web, a cópia da coleção e o seu relato de diferenças, e o ensaio
  seco por campo sobre o texto da cópia.

### Modified Capabilities
- `leitura-do-protocolo`: esquema mínimo do arquivo de sementes (DOI obrigatório,
  `alinhamento_facetas`, retirada dos campos bibliográficos e de `veiculo_conferido`), a
  junção com a cópia do Zotero pelo DOI, as pendências das sementes e a retirada da
  planilha de aderência.
- `interface-de-comando`: sai `aderencia planilhar` e entram `aderencia ensaiar` e os
  subcomandos de `sementes`.
- `derivacao-das-expressoes`: requisitos que remetem às facetas das sementes e ao
  denominador da planilha.

## Impact

- Código: `gramatica.py` (esquema), `leitura.py` (junção pelo DOI), `contexto.py` (cópia
  em memória para os autotestes), `sementes.py` (fim da planilha, ensaio por campo),
  `dados.py` (pendências), `busca/aderencia.py` e `busca/anatomia.py` (textos), `config.py`,
  `config.toml` (`[zotero]`, `[dados]`, fim de `[saidas] aderencia`), um módulo novo para a
  OpenAlex e para o Zotero, e os autotestes.
- Dados: `docs/conjunto_semente.toml` migrado; `data/semente_aderencia.csv` removido; cópia
  da coleção e respostas brutas da OpenAlex em `data/`.
- Sistemas externos: a OpenAlex (leitura) e a API web do Zotero (leitura e escrita na
  biblioteca de grupo), com chave emitida em nome do pesquisador, mantida fora do
  repositório e nunca impressa.
- Conflito: as changes `verificacao-binaria-das-sementes` e
  `fidelidade-por-base-e-casamento-por-campo` estão completas e não arquivadas, e mexem na
  mesma spec. Arquivar as duas antes de sincronizar esta.
