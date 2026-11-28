# Design

## Context

Hoje a validação terminológica tem um único registro, `data/validacao_terminologica.csv`,
com 24 colunas: cinco de identificação (`faceta`, `faceta_nome`, `ancora`, `idioma`,
`termo`) e dezenove de `[planilha] campos_validacao`, que misturam três coisas — o estado da
consulta, a resposta do instrumento e a decisão do ReT. O mesmo arquivo é escrito por
`termos exportar`, `termos validar` e `termos importar`, e lido por `documentos conferir`,
`dados conferir` e `projeto pendencias`. A evidência bruta de cada consulta mora em
`data/evidencia/<instrumento>/<hash16>.json`, com o nome derivado de
`instrumento|idioma|termo`, e é sobrescrita na reconsulta.

As restrições que moldam a solução:

- só a biblioteca padrão, em Python 3.11+; `tomllib` lê TOML, mas não escreve;
- **uma fonte por dado**: o protocolo descreve as linhas; os registros guardam só o que não
  se deriva dele;
- o arquivo de decisões é editado à mão pelo pesquisador; o resultado técnico é escrito pelo
  script;
- a evidência bruta é prova de autoridade, não saída regenerável; a consulta externa não se
  repete de graça;
- a configuração dirige os caminhos, e chave fora do esquema reprova.

As decisões de formato foram tomadas com o pesquisador: decisões em TOML; resultado técnico
em JSON; evidência vigente dos termos do protocolo versionada. Ver `proposal.md` — Why.

## Goals / Non-Goals

**Goals:**

- Separar o registro pelo critério de quem o edita: decisão em TOML, resultado técnico em
  JSON.
- Reduzir o que o pesquisador lê e edita ao que sustenta a decisão vigente.
- Manter versionada só a evidência da consulta vigente dos termos do protocolo, com expurgo
  por construção na reconstrução dos registros.
- Remover decisão, linha técnica e evidência de termo retirado do protocolo, sem histórico
  de termos.
- Conservar os comandos, os códigos de saída e as regras de reabertura e de consulta.
- Migrar o CSV legado com verificação de equivalência, sem leitor permanente do formato
  antigo.

**Non-Goals:**

- Mudar a consulta ao TemaTres, a regra de casamento exato, a similaridade ou o domínio de
  `decisao_ReT`.
- Mudar a gramática do protocolo, a tabela de instrumentos ou o planejamento por faceta e
  idioma.
- Levar evidência para o Zotero, para `tmp/` ou para outro sistema; isso pertence às changes
  `zotero-como-fonte-unica`, `fluxo-das-sementes` e `recursos-das-sondagens`.
- Guardar consultas substituídas ou histórico de decisões.
- Criar interface gráfica ou planilha; o arquivo de decisões é texto.

## Decisions

### 1. Dois arquivos, duas responsabilidades

`[dados] validacao` aponta `data/validacao_terminologica.toml`, o **arquivo de decisões**.
`[dados] consulta_terminologica` aponta `data/consulta_terminologica.json`, o **resultado
técnico**. A chave lógica dos dois é `(faceta, idioma, termo normalizado, instrumento)`.

O arquivo de decisões guarda uma tabela `[[decisoes]]` por chave decidida do protocolo, com `faceta`,
`idioma`, `termo`, `instrumento` e, quando houver, `decisao_ReT`, `justificativa_ReT` e
`data_decisao`. Tabela sem nenhum dos três campos de decisão não é escrita. O resultado
técnico guarda um objeto por chave **consultada** (ou interrompida), não por chave pendente:
a ausência significa "aguardando consulta". Linha de instrumento `Manual` também não é
gravada; a pendência manual se deriva do modo do instrumento no protocolo.

Alternativas: manter um CSV único, apenas reduzido, manteria a mistura que o proposal quer
eliminar e obrigaria o script a reescrever decisão e resposta juntas. Guardar a decisão em
JSON seria pior para editar à mão: sem comentários, com aspas e vírgulas estruturais. Guardar
o resultado técnico em TOML não traz vantagem: ninguém o edita, e o escritor TOML teria de
ser mantido para os dois arquivos.

### 2. Forma do TOML

```toml
# Decisões do ReT sobre o controle terminológico.
# Editar só os campos decisao_ReT, justificativa_ReT e data_decisao.

[[decisoes]]
faceta = "FCT1"
idioma = "pt"
termo = "ontologia"
instrumento = "tbci"
decisao_ReT = "termo livre"
justificativa_ReT = "forma livre do singular ao lado do descritor da faceta"
data_decisao = "2026-11-26"
```

O leitor é estrito: `decisoes` é o único vetor de topo; cada tabela exige as quatro chaves de
identificação não vazias; campo desconhecido, chave duplicada ou `data_decisao` fora de
`AAAA-MM-DD` reprovam. `data_decisao` aceita a data TOML nativa (`2026-11-26`) e a converte
para texto; o escritor grava sempre texto. Justificativa multilinha é aceita; o escritor
grava com `\n` escapado, e o texto continua legível na leitura.

O escritor é um serializador pequeno e determinístico, no próprio pacote: comentário de
cabeçalho e tabelas na ordem do protocolo; a tabela de chave fora do protocolo não é
gravada. Para as strings, usa `json.dumps(..., ensure_ascii=False)`, cujos escapes
são válidos em string básica TOML e evitam um escape próprio. **Comentários escritos à mão
não sobrevivem à regravação**; o cabeçalho é reemitido pelo escritor. O conteúdo editável é
o campo de decisão, não o comentário.

Alternativas: preservar comentários exigiria edição cirúrgica do texto, com muito mais
código e risco de corromper o arquivo; um arquivo separado de comentários criaria segunda
fonte. A regravação explícita (`termos exportar`/`importar`) é o momento em que o arquivo é
normalizado.

### 3. Forma do JSON

```json
{
  "linhas": [
    {
      "faceta": "FCT1",
      "idioma": "pt",
      "termo": "ontologia",
      "instrumento": "tbci",
      "consultado_em": "2026-11-25T09:58:00-03:00",
      "versao_instrumento": "…",
      "url_consultada": "…",
      "status_proposto": "candidato por similaridade (a conferir pelo ReT)",
      "rotulo_autorizado": "ontologias",
      "forma_no_instrumento": "preferido",
      "sugestao_similar": "ontologias [155]",
      "uri_conceito": "",
      "equivalentes_USE_UP": "",
      "termos_genericos_TG": "…",
      "termos_especificos_TE": "",
      "termos_relacionados_TR": "…",
      "nota_de_escopo": "",
      "arquivo_evidencia": "evidencia/tbci/390a96d403ebbae0.json",
      "observacao_tecnica": "…"
    }
  ]
}
```

Campos opcionais vazios são omitidos, para reduzir o arquivo; a leitura os trata como vazios.
O leitor exige o vetor `linhas`, as quatro chaves de identificação e rejeita campo
desconhecido e chave duplicada. O arquivo é escrito em ordem de protocolo, com `indent=2` e
`ensure_ascii=False`. `faceta_nome` e `ancora` não são gravados: vêm do protocolo e mudariam
em duas fontes.

### 4. Configuração e chave retirada

`config.py` passa a exigir `[dados] validacao` e `[dados] consulta_terminologica`, e a seção
`[planilha]` entra em `RETIRADAS`, com mensagem que nomeia as duas chaves novas. A mensagem
específica de `planilha.campos_validacao` vem antes da mensagem da seção, para o caso mais
provável. `config.toml` perde `[planilha]` e ganha a chave nova.

### 5. Onde cada comando lê e grava

| Comando | Lê | Grava |
| --- | --- | --- |
| `termos sondar` | protocolo | nada |
| `termos exportar` | protocolo + decisões + resultado | decisões, resultado, expurgo de evidência |
| `termos validar` | protocolo + decisões + resultado | resultado e evidência (nunca decisões) |
| `termos importar` | protocolo + decisões + resultado | decisões, resultado, expurgo de evidência |
| `documentos conferir` | protocolo + decisões | nada |
| `projeto pendencias` | protocolo + decisões + resultado | nada |

`termos importar` continua exigindo o arquivo de decisões existente; sem ele, DADOS com a
indicação de `termos exportar`. `termos exportar` funciona com os dois registros ausentes.
`termos validar` pode rodar sem o arquivo de decisões: toda linha fica sem decisão, e a
consulta produz o resultado técnico.

### 6. Reabertura: a mesma regra, lida no resultado técnico

A regra de reabertura não muda. Para cada chave do protocolo, o script combina a decisão
(TOML) com a linha técnica (JSON). Sem decisão e sem linha técnica, a linha aguarda consulta.
Com linha técnica de instrumento `Automático`, aplica os três motivos já existentes:
pendente de validação manual, `url_consultada` fora do endereço resolvido vigente, ou termo
livre não localizado sem `sugestao_similar`. Reabrir remove a linha técnica (e a decisão não
existe, por definição); com decisão, a linha é preservada e listada. A evidência anterior
continua no diretório até a reconsulta, porque o expurgo olha a chave do protocolo, não a
referência do JSON.

### 7. Expurgo de evidência por chave, não por referência

A evidência gerenciada é `<instrumento>/<16 hex>.json` sob `[dados] evidencia`, com o nome
derivado de `instrumento|idioma|termo`. O expurgo calcula o conjunto de caminhos esperados
para **todas** as chaves do protocolo (inclusive as ainda não consultadas e as manuais) e
remove os arquivos gerenciados que não estão nesse conjunto. Assim:

- termo retirado do protocolo perde a evidência;
- linha reaberta mantém a evidência até a reconsulta substituí-la;
- reconsulta sobrescreve o mesmo arquivo;
- `instrumentos/`, `sondagens/`, `openalex/`, `crossref/`, `referencias/` e `zotero/` ficam
  intocados, porque são pastas reservadas e/ou não têm nome de 16 hex. Em particular,
  `instrumentos/` guarda a sonda de idiomas do TBCI (PD04), não é evidência de termo e
  permanece como está; a consulta substituída já é sobrescrita no mesmo arquivo, e não há
  segunda cópia a expurgar.

Antes de escrever ou expurgar, `termos exportar` e `termos importar` conferem que toda linha
técnica com `status_proposto` aponta evidência existente. Falta de evidência reprova e
impede o expurgo, para não apagar prova de autoridade por causa de um registro incompleto.

Alternativa: expurgar pelo que o JSON referencia apagaria a evidência de uma linha reaberta
no momento da reabertura, antes de a reconsulta substituí-la; o comportamento atual e a
skill dizem que ela fica até a reconsulta. A chave do protocolo resolve isso sem guardar
estado extra.

### 8. Módulos e compatibilidade do autoteste

- `src/rsl/termos/registro.py` (novo): leitura e escrita TOML/JSON, chave, validação de
  forma, caminho esperado da evidência e expurgo.
- `src/rsl/termos/validacao.py`: orquestra `carrega`, `grava_registros`, `validar`,
  `exportar` e `importar`; deixa de conhecer CSV e `[planilha]`.
- `src/rsl/termos/decisao.py`: lê decisões do TOML; `linhas_esperadas` e o domínio continuam
  iguais.
- `src/rsl/contexto.py`: `texto_decisoes` e `texto_resultado` substituem `texto_validacao`;
  `com_decisoes` e `com_resultado` substituem `com_validacao`.
- `src/rsl/dados.py`: `projeto pendencias` conta as pendências a partir do protocolo e do
  resultado técnico.
- `src/rsl/coerencia.py`, `src/rsl/autoteste/validacao.py`, `src/rsl/__main__.py` (ajuda):
  acompanham a mudança.
- `src/rsl/config.py` e `config.toml`: chaves e chave retirada.

### 9. Sincronização a partir do protocolo, sem histórico de termos

A reconstrução parte sempre das chaves do protocolo. A tabela de decisão cuja chave não está
no protocolo é removida, assim como a linha técnica e a evidência dela; `termos exportar` e
`termos importar` terminam com OK e informam quantas foram removidas. Não se guarda lista de
órfãs nem histórico de termos. `documentos conferir` reprova enquanto houver decisão de chave
fora do protocolo, para que o registro defasado não passe em silêncio.

### 10. Migração de uma vez, sem leitor permanente

A conversão do CSV legado é um passo de migração, não uma funcionalidade do produto. Um
script descartável lê o CSV, escreve o TOML e o JSON, e confere a equivalência; depois o CSV
é removido e o código novo não o conhece. O CSV antigo permanece no histórico do git para
conferência e reversão. Isso evita um leitor de formato morto e a segunda fonte que ele
manteria.

Verificação de equivalência, antes de remover o CSV:

1. toda linha com decisão de chave do protocolo vira uma tabela, com os mesmos valores; a
   decisão de chave fora do protocolo é removida, sem virar tabela;
2. toda linha com conteúdo técnico vira um objeto, com os mesmos valores;
3. o mapa `(faceta, idioma, termo)` → linha do CT calculado das decisões é idêntico ao do
   CSV, pela mesma função `linhas_esperadas`;
4. toda referência de evidência do JSON existe, e toda evidência gerenciada do diretório é
   referenciada ou pertence a chave do protocolo;
5. `documentos conferir` e `projeto autoteste` passam depois da conversão;
6. `termos exportar` roda de novo e não altera o conteúdo (idempotência).

## Risks / Trade-offs

- **Serializador TOML próprio** → o risco é escape e tipo. Mitigação: usar
  `json.dumps(ensure_ascii=False)` para strings, testes com aspas, barra invertida, quebra de
  linha, acento e `#`, e leitura de volta com `tomllib`.
- **Comentário escrito à mão se perde na regravação** → documentado no cabeçalho e na skill;
  a decisão é o conteúdo, não o comentário. Alternativa de edição cirúrgica foi descartada.
- **TOML malformado por edição manual** → `tomllib` reprova com DADOS e a linha; nenhum
  arquivo é gravado parcialmente. `termos importar` valida antes de escrever.
- **Expurgo apaga evidência errada** → só arquivos de 16 hex em pasta não reservada; o
  conjunto esperado vem de todas as chaves do protocolo; referência ausente bloqueia o
  expurgo; teste cobre termo retirado, linha reaberta e pasta alheia.
- **Dois arquivos divergem** → a chave é única e normalizada; a reconstrução parte do
  protocolo, `termos exportar` e `termos importar` removem decisão de chave fora dele, e
  `documentos conferir` reprova enquanto ela existir; `projeto pendencias` lê os dois.
- **Migração perde decisão** → a conferência compara o mapa de linhas do CT e os valores
  campo a campo antes de remover o CSV; o CSV antigo fica no git.
- **Refatoração do autoteste esconde caso** → os casos existentes migram um a um, e os novos
  casos (TOML, JSON, expurgo, órfã) são provados por falha deliberada.
- **Linha manual sem evidência** → é pendência, não resultado; a justificativa registra a
  fonte consultada. O comportamento não piora em relação ao CSV.

## Migration Plan

1. Congelar o CSV legado no commit anterior à mudança.
2. Rodar o script de conversão e a conferência de equivalência (seção 10), sem remover nada;
   a conversão leva a decisão só das chaves do protocolo.
3. Atualizar `config.toml` e `config.py`; rodar `configuracao mostrar`.
4. Rodar `termos exportar` e conferir idempotência; rodar `documentos conferir`,
   `dados conferir`, `projeto autoteste` e `projeto pendencias`.
5. Remover `data/validacao_terminologica.csv` e conferir que nenhum documento, skill ou
   código o cita.
6. Reverter, se necessário: `git revert` restaura código, CSV e configuração; a evidência só
   é afetada pelo expurgo, e o git a restaura.

## Open Questions

Nenhuma pendente. A sonda da change `fluxo-da-execucao-de-busca` e o destino da evidência no
Zotero não afetam esta change, que mantém a evidência em `data/evidencia/`.
