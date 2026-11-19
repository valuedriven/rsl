# Design

## Context

Motivação em `proposal.md`. Estado do código que condiciona a abordagem:

- `src/protocolo.py` carrega `config.toml` na importação e deriva dele constantes de módulo:
  `IDIOMAS`, `FICHAS`, `BASES`, `BDS`, `COR_FACETA`. Os leitores do protocolo recebem o texto
  `t` e são chamados por `analisa(t)`, que monta o dicionário `d`; o autoteste chama os
  mesmos leitores sobre cópias alteradas do texto.
- `validar_termos.py`, `derivar_expressoes.py` e `gen_semente.py` importam essas constantes
  no carregamento do módulo (`MODO_DE`, `BASE_CANONICA`, `BD_DE`, `SLUG_DE_BD`, `BASES`).
- Os leitores de tabela são posicionais. `fontes()` lê o nome da base em `cels[1]`, que no
  protocolo atual já é a coluna `Sigla`: o nome lido hoje é `wos`, não "Web of Science".
- A leitura do protocolo vigente já reprova (`tabelas()` não reconhece o quadro).

## Goals / Non-Goals

**Goals:**
- Uma única fonte para cada parâmetro estrutural, com reprovação ruidosa na ausência.
- Leitura de tabela pelo nome da coluna, não pela posição.
- Valores estruturais disponíveis aos três scripts consumidores pelo mesmo caminho (`d`).

**Non-Goals:**
- Alterar os parâmetros não estruturais (`[padroes]` restantes, `[expressoes]`,
  `[conferencia]`, `[dados]`, `[planilha]`) e a sua regra de precedência.
- Alterar os clientes automáticos (consulta, endereços de API, formato de resposta).
- Editar o protocolo ou as fichas: são edições do pesquisador (ver Migration Plan).

## Decisions

### D1. Estrutura sai das constantes de módulo e entra em `d`
`IDIOMAS`, `FICHAS`, `BASES`, `BDS` e `COR_FACETA` deixam de existir como constantes. `analisa(t)`
passa a devolver `d["idiomas"]`, `d["bases"]` (lista de `{id, sigla, nome, ficha}`) e
`d["instrumentos"]` (por sigla, com modo, caminho, idiomas e facetas, além do índice por
faceta usado no planejamento). Funções que hoje leem as constantes passam a recebê-las de `d`.
Os consumidores obtêm `d` por uma função de `protocolo.py` que lê o protocolo uma vez por
execução (cache) e termina com a mensagem do leitor quando ele reprova.

*Alternativa rejeitada*: ler o protocolo na importação, preservando as constantes. Quebra o
autoteste, que precisa ler cópias alteradas do texto com a mesma gramática, e faz qualquer
`import protocolo` falhar quando o documento está em edição.

### D2. Leitor de tabela pelo cabeçalho
Um leitor comum devolve as linhas de uma tabela como dicionários indexados pelo nome da
coluna e reprova quando falta coluna exigida ou há coluna repetida. Os nomes exigidos de
cada tabela estrutural — `ID Base`, `Sigla`, `Nome da base`; `Sigla`, `Instrumento`, `Modo`,
`Caminho`, `Idiomas`, `FCTs`; `ID Semente`, `Semente`, `Bases` — são gramática do leitor no
código, como `ROTULO_CAMADA`. Colunas extras (ex.: `Justificativa`) são ignoradas.

*Alternativa considerada*: declarar os cabeçalhos no `config.toml`, como já se faz com
`[expressoes] colunas`. Rejeitada: o cabeçalho é contrato de formato, não parâmetro do
projeto, e outra cópia dele no `config.toml` reabriria a duplicação que a mudança fecha. A
tabela de expressões não muda nesta mudança.

### D3. Quadro terminológico: idioma pelo cabeçalho
O cabeçalho `| FCTn | pt | en | es |` dá a faceta e os idiomas. O primeiro quadro fixa a
ordem e o conjunto de `d["idiomas"]`; os demais têm de ter o mesmo conjunto (ordem livre).

### D4. Configuração: chaves retiradas são proibidas
`valida_config` deixa de exigir as cinco chaves e passa a reprovar se alguma delas estiver
presente, com mensagem que diz que o valor vem do protocolo. Isso impede, por construção,
que uma cópia antiga no `config.toml` volte a ser lida ou a confundir quem edita.

### D5. Modo do instrumento e registro de clientes
O registro de clientes fica em `validar_termos.py` como `CLIENTES = {sigla: função}`
(`tbci`, `unesco`); é conhecimento da ferramenta, não parâmetro do projeto. `protocolo.py`
confere `Automático` contra esse registro por importação tardia, dentro da função de
conferência, para não criar importação circular na carga dos módulos. O `--validar` de
`validar_termos.py` passa a aceitar as siglas lidas como `Automático` (e `ambos` vira
`todos`).

*Alternativa rejeitada*: lista de clientes em `protocolo.py`. Duplicaria o registro e
permitiria um cliente declarado sem função.

### D6. Linha de faceta
Padrão: `Faceta n (FCTn): <nome>` com sufixo opcional `(âncora obrigatória k)` ao fim. O nome é
todo o resto, hífens incluídos. Linha com travessão residual ou com parêntese de âncora mal
formado reprova.

### D7. Bases e fichas
A ficha é localizada pela sigla, por um padrão de caminho no `config.toml` (chave
`[documentos] ficha = "docs/busca_base_{sigla}.md"`, relativa à raiz), parâmetro de caminho
como os de `[dados]`. O padrão tem de conter `{sigla}`; a chave não se chama `fichas`, que é
proibida (D4). As quatro fichas são renomeadas com `git mv` para preservar o histórico.

*Alternativas rejeitadas*: coluna de caminho no protocolo (decisão do pesquisador: a sigla
basta); ficha que declara a própria sigla, com varredura de `docs/` (uma busca no lugar de um
caminho calculado, e duas fichas com a mesma sigla só se detectariam depois).

A forma de execução é lida da ficha pela linha `- Execução: única|particionada`
(exatamente uma), normalizada internamente para `unica`/`particionada`. O nome da base passa
a vir da coluna `Nome da base`, corrigindo a leitura posicional de `fontes()`.

### D8. Sementes
`sementes(t)` lê a tabela do subtítulo "Conjunto-semente", reaproveitando a extração de
autoria, ano, título e DOI sobre a célula `Semente`. `distribuicao()` passa a só calcular
(sem `declarado`); a conferência prosa × mapa e o parser `_mapa` saem.

### D9. Emoji
Sai `COR_FACETA` e o laço que o consulta em `consultas_curadas()`. Medido nas quatro fichas
atuais: nenhuma célula de facetas da forma curada tem emoji sem `FCTn`; a retirada não muda
nenhuma leitura atual.

## Risks / Trade-offs

- [Protocolo e fichas ainda fora do formato] → a leitura reprova até as edições do
  pesquisador (Migration Plan, passo 1). É o comportamento pretendido; a implementação não
  afrouxa a leitura para passar.
- [Siglas em minúsculas mudam as saídas] → declarado no requisito "Saídas preservadas"; a
  comparação antes/depois é feita sem distinção de caixa.
- [Arquivos alimentados com sigla antiga] → hoje não há `sementes.json`,
  `registro_execucao.json` nem planilha de validação em `data/`. Se forem recriados de cópia
  antiga, a conferência dos dados reprova a sigla desconhecida em vez de migrá-la em silêncio.
- [Importação tardia de `validar_termos` em `protocolo.py`] → acoplamento explícito e
  localizado; coberto por caso de autoteste (`Automático` sem cliente reprova).
- [Endereços de `Caminho` não conferidos] → o leitor exige só URL bem formada; não acessa a
  rede.

## Migration Plan

1. Documentos (o agente executa, a pedido do pesquisador): renomear as fichas para
   `docs/busca_base_<sigla>.md` e atualizar as referências; passar a coluna `Bases` das
   sementes para as siglas da tabela de bases; acrescentar `- Execução: …` a cada ficha (ERIC
   `particionada`; WoS, Scopus e BRAPCI `única`, conforme o `config.toml` atual).
2. Implementar em `protocolo.py` (D1–D4, D6–D9) e nos consumidores (D1, D5).
3. Retirar as cinco chaves do `config.toml`.
4. Rodar `--conferir`, `--mostrar` e `--autoteste`; conferir as saídas da derivação contra as
   anteriores, sem distinção de caixa nas siglas.
5. Reversão: `git revert` do commit; protocolo e fichas editados continuam legíveis por
   humanos, e o `config.toml` anterior volta com o revert.
