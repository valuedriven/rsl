# RSL-01 — Representação do conhecimento sobre práticas educacionais e seus fatores situacionais

Revisão sistemática de literatura sobre modelos conceituais, ontologias e outros sistemas de
organização do conhecimento que representam formalmente práticas do processo de
ensino-aprendizagem e os fatores situacionais que condicionam a sua aplicação.

Conduzida pelo **RS Banyan**, com o **PRISMA** como diretriz de apresentação.

Este arquivo é a **porta de entrada** do repositório: como executar, onde fica cada coisa e
quem a escreve. **O que se faz, em que ordem e com que apoio** — módulos, etapas, passos,
comandos com os parâmetros e índices da busca — está em
[`docs/procedimentos.md`](docs/procedimentos.md). Nenhum dos dois repete o conteúdo dos
documentos que indexam.

## Como executar

Toda operação passa por um ponto de entrada único, a partir da raiz do projeto, com
**Python 3.11+** e só a biblioteca padrão:

```bash
PYTHONPATH=src python3 -m rsl <subcomando>     # ou, de dentro de src/: python3 -m rsl …
python3 -m rsl                                 # sem subcomando: a ajuda, com os códigos
python3 -m rsl <subcomando> -h                 # parâmetros de cada subcomando
```

Nos documentos, os comandos aparecem como `python3 -m rsl …`, com `src/` no caminho de
importação. A configuração é `config.toml`, na raiz; a variável de ambiente `RSL_CONFIG`
aponta outro arquivo, para ensaio e autoteste. O que cada chave significa está nos
comentários do próprio `config.toml`; a forma que o leitor exige do protocolo, das fichas e
do arquivo de sementes, em `python3 -m rsl gramatica`; o valor em uso de cada parâmetro e a
sua origem, em `python3 -m rsl mostrar`. O mapeamento de cada passo do guia às skills e aos
comandos, conferido contra as skills e o parser, sai de `python3 -m rsl catalogo gerar`
(ensaio; `--gravar` regrava o catálogo).

### Códigos de saída

Todo subcomando termina com um destes códigos, e toda saída diferente de OK termina com uma
linha que nomeia o código:

| Código | Nome | Quando |
| --- | --- | --- |
| 0 | OK | a operação terminou e nada reprovou |
| 1 | REPROVADO | uma conferência ou condição de aceite reprovou o conteúdo |
| 2 | USO | argumento ou subcomando inválido |
| 3 | CONFIGURACAO | `config.toml` ausente, inválido ou incompleto, ou protocolo inexistente |
| 4 | PROTOCOLO_ILEGIVEL | protocolo ou ficha fora da gramática que o leitor exige |
| 5 | DADOS | arquivo alimentado, exportação ou arquivo de entrada ausente ou ilegível |
| 6 | PARCIAL | autoteste sem falha, com casos não executados |
| 7 | FONTE_EXTERNA | fonte externa com erro, bloqueio, captcha ou limite excedido |

Quando mais de uma condição ocorre, vale a mais grave: CONFIGURACAO, PROTOCOLO_ILEGIVEL,
DADOS, FONTE_EXTERNA, REPROVADO, PARCIAL.

## Mapa

Cada caminho aparece uma vez. Caminho marcado *sob demanda* é criado quando o primeiro
arquivo chega. Os caminhos de `data/` vêm de `[dados]` e `[saidas]` do `config.toml`, e os
documentos de sementes e fichas, de `[documentos]`; os documentos citam esses arquivos pela
chave, não pelo caminho.

| Caminho | O que contém | Quem escreve |
| --- | --- | --- |
| `docs/01_plano.md` | plano: contexto, objetivos, base metodológica, escopo, cronograma, recursos, custos, qualidade, riscos e uso de IA | pesquisador |
| `docs/02_protocolo_informacoes_gerais.md` | protocolo, informações gerais: tópicos preliminares, delimitação do assunto e objeto | pesquisador |
| `docs/03_protocolo_estrategia_pesquisa.md` (`protocolo`) | protocolo, estratégias de pesquisa: questão, facetas, controle terminológico, strings, expressões, critérios, fontes, conjunto-semente, procedimentos, instrumentos e ferramentas; fonte única dos parâmetros que declara | pesquisador; a tabela "Strings de busca por faceta", `strings gerar --gravar`, a partir do quadro terminológico |
| `docs/conjunto_semente.toml` (`[documentos] sementes`) | conjunto-semente, uma tabela `[[sementes]]` por estudo; único lugar de dado de semente | pesquisador; nenhum subcomando grava |
| `docs/procedimentos_busca_<sigla>.md` (`[documentos] ficha`) | ficha de cada base: sintaxe, critérios, strings com a declaração de cobertura (inclusive os parâmetros `plural` e `teto de caracteres`), expressões, estratégia de proximidade, execução, conjunto-semente e ressalvas | pesquisador e agente, a pedido |
| `docs/parametros_complementares.md` | instrumento de extração e síntese: grupos de extração, cobertura conceitual, granularidade e grau de formalização | pesquisador |
| `docs/procedimentos.md` | guia de procedimentos: módulos, etapas e passos, com fonte, script, skill e apoio; fonte do catálogo de apoio | pesquisador e agente, a pedido |
| `docs/catalogo_de_apoio.md` | catálogo de apoio: skills e comandos por passo, por skill e por comando, e cobertura por etapa; saída de geração, não se edita à mão | `catalogo gerar --gravar`, a partir do guia de procedimentos |
| `data/historico.md` | decisões, inclusive emendas | pesquisador; agente, a pedido |
| `data/pendencias.json` | ações ainda a executar, `PDnn` | pesquisador; agente, a pedido |
| `data/registro_execucao.json` (`[dados] registro`) — *sob demanda* | resultados das consultas nas bases, por base e por execução | pesquisador e `busca registrar` |
| `data/execucoes/<base>/` (`[dados] execucoes`) — *sob demanda* | exportações intactas das bases | pesquisador |
| `data/validacao_terminologica.csv` (`[dados] validacao`) — *sob demanda* | estatuto de cada termo; preserva as decisões e as linhas fora do protocolo | `termos exportar`, `termos validar`, `termos importar`; decisões pelo pesquisador |
| `data/evidencia/<instrumento>/` (`[dados] evidencia`) — *sob demanda* | resposta bruta de cada consulta terminológica | `termos validar` |
| `data/evidencia/referencias/` | resposta bruta da conferência de referências, `SEn_…` pelo `id` da semente | agente, a pedido |
| `data/semente_aderencia.csv` (`[saidas] aderencia`) | planilha do teste de aderência, uma linha por semente e por base; regravada a cada execução, com as colunas manuais preservadas | `sementes planilha` |
| `data/registros.csv`, `data/contagens_busca.csv`, `data/ordem_triagem.csv` (`[saidas]`) — *sob demanda* | registros com pertinência e marcas, contagens por base e expressão, ordem da 1ª filtragem | `busca derivar` |
| `data/fidelidade_<expressao>.csv` (`[saidas] fidelidade`) — *sob demanda* | divergências entre derivação e execução direta | `busca fidelidade` |
| `data/sensibilidade_<base>.csv` (`[saidas] sensibilidade`) — *sob demanda* | perda da sonda e amostra a classificar; preserva a coluna `elegivel` | `busca sensibilidade`; classificação pelo pesquisador |
| `data/arquivo/` — *sob demanda* | cópias anteriores, com `SHA256` | migrações |
| `config.toml` | configuração dos scripts | pesquisador; nenhum subcomando grava |
| `src/rsl/` | pacote de execução | — |
| `openspec/specs/` | requisitos dos scripts | — |
| `.agents/skills/` | competências metodológicas e operacionais do agente | — |
| `AGENTS.md` | contrato de trabalho do agente | — |

O que é **derivado do documento não vira arquivo**: questão, facetas, instrumentos,
strings, expressões, critérios e fontes são lidos do protocolo a cada execução, e a forma de
cada base, da ficha. Em `data/` fica o que alguém alimenta e o que os subcomandos gravam.
Os demais instrumentos do RS Banyan e o portfólio não integram este repositório.

### Três registros, três finalidades

| Registro | Guarda | Não guarda |
| --- | --- | --- |
| `data/historico.md` | **decisões** relevantes sobre a revisão — emendas, escolhas de método, de escopo e de instrumento —, com data, alcance e fundamento | ação por fazer; resultado de consulta; contagem — de termos, de sementes, de caracteres, de casos — e resultado de conferência ou de autoteste |
| `data/pendencias.json` | **ações ainda a executar**, e só elas, com `id`, `origem`, o que bloqueia, ação sugerida e responsável | ação concluída ou descartada; decisão; resultado de consulta |
| `data/registro_execucao.json` | **resultados da execução das consultas** nas bases — sondagens, retornos, exportações e conferências | decisão; ação por fazer |

- Pendência resolvida ou descartada **sai** de `data/pendencias.json`; não se arquiva. O que
  a encerrou vai ao seu registro antes da exclusão: a decisão, inclusive a de descartar, ao
  histórico, que cita o `id`; o resultado de consulta, ao registro de execução. O `id` de
  pendência excluída não se reutiliza.
- A pendência remete à sua `origem` (ficha, protocolo, plano, comando) em vez de copiar o
  conteúdo dela.
- O histórico **não transcreve contagem**. Número se calcula do artefato quando se precisa
  dele (`mostrar`, `conferir`, `autoteste`), e o transcrito diverge na alteração seguinte. A
  entrada nomeia o que mudou — os termos, as sementes, os critérios — e o valor de
  parâmetro decidido (limiar, teto, recorte), não o tamanho do que mudou. O resultado das
  conferências vai ao relato da change ou da tarefa, não ao histórico.

## Precedência

- **Uma fonte por dado.** Vocabulário, expressões, critérios e os parâmetros que declara vêm
  do protocolo; a forma da busca, da ficha da base; o conjunto-semente, do arquivo de
  sementes; o resto, do `config.toml`. Não há cópia intermediária nem valor de parâmetro no
  código.
- O **protocolo** — `docs/02_protocolo_informacoes_gerais.md` e
  `docs/03_protocolo_estrategia_pesquisa.md` — prevalece sobre qualquer formulação feita em
  outro documento; o plano remete a ele.
- Sobre o `config.toml`, o protocolo prevalece em todo parâmetro que declara; o padrão vale
  só quando o protocolo não o declara, e trecho presente e ilegível reprova, sem cair no
  padrão. Os parâmetros estruturais só existem no protocolo e no arquivo de sementes.
- O **histórico** é o único lugar das decisões; `data/pendencias.json`, das ações por
  fazer; `data/registro_execucao.json`, dos resultados das consultas nas bases.
- A data **oficial** de execução consta **exclusivamente do cronograma**, que não integra
  este repositório; `data/registro_execucao.json` registra data e hora operacionais, como
  rastro técnico.
- Altera-se a fonte, não a saída: as planilhas e CSVs gravados pelos subcomandos se
  regeneram; a exceção é a planilha de validação, que é o registro do estatuto dos termos.
- A tabela **"Strings de busca por faceta"** do protocolo é saída de geração: cada STR é a
  união dos termos do quadro terminológico da faceta, menos os subsumidos. Altera-se o
  quadro, e a ordem é quadro → `strings gerar` (ensaio) → `strings gerar --gravar` →
  fichas → `conferir`. STR editada à mão, ou defasada do quadro, reprova em `conferir`.
- O **catálogo de apoio** é saída de geração do guia de procedimentos. Altera-se o guia —
  ou cria-se, renomeia-se ou retira-se uma skill ou um comando —, e a ordem é guia →
  `catalogo gerar` (ensaio e conferência) → `catalogo gerar --gravar`. Catálogo editado à
  mão, ou defasado do guia, reprova em `catalogo gerar`.
- A planilha de aderência é **artefato misto**: as colunas manuais — as que `sementes
  planilha` deixa vazias na primeira geração — editam-se no próprio arquivo e se conservam
  na regravação; as demais vêm do arquivo de sementes e da tabela de bases, e corrigem-se
  lá. A regravação que perderia preenchimento manual é recusada, sem gravar.

## Convenções

- **Português do Brasil**, redação formal, objetiva e enxuta.
- **O identificador é a chave.** Tudo se identifica pelo código do protocolo — questões,
  facetas, strings, expressões, critérios, bases e sementes —, e não por posição.
- Referências normalizadas pela **ABNT NBR 6023**, cada uma com o seu estado de conferência.
- Datas de execução no **cronograma**; decisões em `data/historico.md`.
- Nomeação dos arquivos de estudo: `Ano_DuasPrimeirasPalavras_TIPO_UltimoSobrenomeAutor`,
  com sufixo `_FICHA` para fichamentos.
- Arquivos gravados pelos subcomandos: `snake_case`, em português e sem acento, com o
  substantivo do conteúdo e, quando há um por chave, a chave em minúsculas
  (`fidelidade_eb2.csv`, `sensibilidade_wos.csv`).

## Uso de IA

A assistência de inteligência artificial é declarada e registrada ação a ação no LOG_IA,
apêndice do protocolo. A IA **não é autora**, conforme ICMJE e COPE. As regras de uso estão em
`docs/01_plano.md`, seção 8.
