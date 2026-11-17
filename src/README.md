# Scripts — RS Banyan

Quatro scripts e este README. Nada mais mora em `src/`: os dados, os derivados e as
saídas ficam em `data/`.

## 1. Arquitetura: uma fonte, dois níveis de conferência

O documento `docs/2_protocolo/03_protocolo_estrategia_pesquisa.md` é a **fonte única** da
questão, das facetas, do vocabulário, das strings, das expressões, dos critérios, das
fontes e do conjunto-semente. `src/protocolo.py --gerar` deriva dele os JSON de `data/`.

Cada JSON derivado carrega dois blocos:

```json
"fonte":    {"arquivo": "docs/2_protocolo/03_protocolo_estrategia_pesquisa.md", "sha256": "…"},
"derivado": {"sha256": "…", "chaves": ["…"]}
```

- `fonte.sha256` detecta **documento alterado sem regerar**. Todo consumidor recusa
  rodar nesse estado, em vez de trabalhar com vocabulário vencido.
- `derivado.sha256` detecta **campo derivado editado à mão**, cobrindo exatamente o
  subconjunto declarado em `SUBSETS`, no `protocolo.py`. Campo autoral pode ser editado
  livremente: o estatuto de validação de cada termo e os metadados de cada semente.

Dois arquivos são **mistos** — derivados e autorais no mesmo JSON:

| Arquivo | Derivado | Autoral |
| :--- | :--- | :--- |
| `data/descritores.json` | tabelas por camada e idioma, termos, instrumentos, `livre` | bloco `estatuto` de cada termo: validação, evidência, decisão |
| `data/sementes.json` | referências, mapa por base, distribuição, limiar | verificação, escopo, tipo, alinhamento, nota, veículo, `eric` |

`--gerar` **preserva o que é autoral**: casa o estatuto por `(faceta, idioma, termo
normalizado)` e a semente por DOI ou título normalizado. Termo ou semente retirado do
protocolo não é apagado: fica com `no_protocolo=false` e é reportado por `--pendencias`,
para decisão. Apagar evidência conferida por geração automática seria o defeito que o
projeto combate.

Dois arquivos são **auxiliares**, criados só se ausentes e nunca reescritos:
`data/consultas.json` e `data/pendencias.json`.

## 2. Onde cada coisa mora

| Caminho | O que é | Quem escreve |
| :--- | :--- | :--- |
| `data/questoes.json` | questão principal, QS1–QS4, estrutura PICo | `--gerar` |
| `data/facetas.json` | palavras significativas: nome, cor, âncora | `--gerar` |
| `data/descritores.json` | controle terminológico por faceta + estatuto | `--gerar` + validação |
| `data/strings.json` | string de cada faceta e composição E1–E4 | `--gerar` |
| `data/criterios.json` | critérios de inclusão/exclusão e recorte | `--gerar` |
| `data/fontes.json` | bases, ordem, via de acesso, acervos, ferramenta | `--gerar` |
| `data/sementes.json` | conjunto-semente + metadados de conferência | `--gerar` + pesquisador |
| `data/consultas.json` | registro das execuções | `--registrar` |
| `data/pendencias.json` | estado das pendências abertas | pesquisador |
| `data/execucoes/<base>/` | exportações intactas das bases | pesquisador |
| `data/saida/derivacao/` | `registros.csv`, `io2_contagens.csv`, `ordem_triagem.csv`, `fidelidade_E<n>.csv` | `--derivar`, `--fidelidade` |
| `data/saida/semente/` | `Conjunto_Semente.md`, `semente_aderencia.csv` | `gen_semente.py` |
| `data/saida/validacao/` | `validacao_termologica.csv` (exportação) | `validar_termos.py` |
| `data/evidencia/{tbci,unesco}/` | resposta bruta de cada consulta | `validar_termos.py` |
| `data/arquivo/` | cópias anteriores, com `SHA256` | migrações e conferências |

`data/arquivo/` guarda cópias anteriores, com `SHA256`, para provar o que mudou em
migrações. Está vazio: o arquivo de `pre-migracao` — estado de 16/11/2026, com a planilha
de 373 linhas — foi descartado por decisão de 17/11/2026, depois de conferida a migração.
O registro da migração está no Anexo A.

## 3. Ordem de execução

```bash
python3 src/protocolo.py --gerar                              # 0. deriva os JSON
python3 src/protocolo.py --conferir                           # confere o documento
python3 src/protocolo.py --conferir-dados                     # confere os JSON entre si
python3 src/protocolo.py --conferir --autoteste               # prova que as conferências reprovam
```

```bash
python3 src/derivar_expressoes.py --registrar wos E4 data/execucoes/wos/e4.ris --retorno 18432
python3 src/derivar_expressoes.py --derivar
python3 src/derivar_expressoes.py --aderencia
python3 src/derivar_expressoes.py --fidelidade E2 data/execucoes/wos/e2_conferencia.ris
```

```bash
python3 src/gen_semente.py
```

```bash
python3 src/validar_termos.py --sonda                         # obrigatório antes de validar
python3 src/validar_termos.py --exportar
python3 src/validar_termos.py --validar tbci
python3 src/validar_termos.py --validar unesco
python3 src/validar_termos.py --importar                      # traz as decisões da planilha
```

Todos os comandos rodam da raiz do repositório. `--gerar` recusa gerar se o documento
estiver fora da forma esperada, e todo consumidor recusa rodar com derivado defasado.

## 4. `protocolo.py` — o leitor do documento

Deriva os sete arquivos de conteúdo e cria os dois auxiliares se ausentes.

- `--conferir` reprova: faceta sem camada em algum idioma, termo repetido na mesma
  camada, string fora do padrão `"termo" OR …`, termo de string ausente da tabela do
  controle terminológico, composição das expressões fora do previsto, E4 que não seja a
  interseção de E2 com E3, recorte diferente de 2017, limiar diferente de 80 %, âncoras
  que não sejam as facetas 1 e 2, critério de dimensão obrigatória ausente, base ausente,
  semente sem título ou sem base, distribuição que contradiga a prosa, `taxonomy`/
  `taxonomies` presentes nas strings ou `taxonomia` ausente.
- `--conferir-dados` reprova JSON ausente, derivado defasado, campo derivado adulterado,
  faceta divergente entre arquivos, termo de string ausente de `descritores.json`, termo
  do protocolo sem bloco de estatuto e consulta que aponte arquivo inexistente.
- `--autoteste` injeta nove defeitos no documento e três nas assinaturas e exige que
  todas as conferências os reprovem — inclusive a prova de que **edição de campo autoral
  é aprovada** e a de que campo derivado adulterado é reprovado.
- `--pendencias` relata, sem escrever: semente com campo `A CONFERIR`/`PENDÊNCIA`, termo
  sem estatuto, termo ou semente fora do protocolo, consulta sem execução registrada.
- `--mostrar` resume o que leu.

## 5. `derivar_expressoes.py` — E4 executada, E1–E3 derivadas

As quatro expressões não são quatro buscas. Todas começam por strings 1 + 2 e apenas
acrescentam facetas, de modo que **E1, E2 e E3 são subconjuntos estritos de E4** e a união
das quatro é exatamente E4. Executa-se **E4, a de cobertura, uma vez por base**,
exporta-se o resultado, e a pertinência de cada registro às demais é calculada aqui. De 16
execuções (4 × 4 bases) para 4.

O script **não exclui registro algum, não decide inclusão e não substitui o teste de
fidelidade**. As contagens de E1 a E3 são **derivadas** e assim devem ser declaradas no
IO 2 e no relatório; `io2_contagens.csv` já traz a coluna `procedencia`.

### 5.1 Registro da consulta — `--registrar`

A derivação não lê a pasta de exportações: lê o **registro** feito por `--registrar`.

```bash
python3 src/derivar_expressoes.py --registrar wos E4 data/execucoes/wos/e4.ris --retorno 18432
```

O script lê o arquivo, conta os registros e compara com o retorno que a base exibiu:

- iguais → grava a consulta como `valida`;
- diferentes → **recusa registrar**, porque arquivo trocado, exportação parcial e teto de
  retorno da base produzem contagens que não descrevem a busca. Se a diferença for
  conhecida e aceitável — é o caso do teto de 1.000 registros da BRAPCI —, repete-se com
  `--justificar "motivo"` e a entrada fica `divergente_justificada`.

`--derivar` reconfere a contagem contra o arquivo: se ele mudou, para em vez de derivar
sobre outra coisa. A data e a hora gravadas são **operacionais**; a data oficial de
execução continua sendo a do IO 7.

A ERIC é executada em mais de um arquivo (`eric_4a.ris`, `eric_4b.ris`): cada arquivo é
uma consulta registrada, e a deduplicação da base acontece na derivação.

### 5.2 Deduplicação — marca, não apaga

Dentro da mesma base, registro com o mesmo DOI — ou, na falta dele, o mesmo título
normalizado — recebe em `duplicata_de` o identificador da primeira ocorrência. Nada é
apagado: o registro continua em `registros.csv`. As contagens do IO 2 usam os **únicos**;
`registros_com_duplicatas` sai ao lado, para que a diferença seja visível e não silenciosa.

### 5.3 Recorte temporal

O protocolo define o recorte como **2017 em diante**, sem teto; o script toma o ano
corrente como limite superior. O recorte é aplicado **na busca** em todas as bases: na
própria consulta na Web of Science, na Scopus e na BRAPCI; pelo **filtro da página de
resultados** na ERIC, onde os operadores de ano zeram o retorno em consulta com grupos.
Aqui o recorte é apenas **conferência**.

O script imprime três números — dentro, fora e sem ano legível —, informa de que bases
vieram os retirados e grava a coluna `recorte` em `registros.csv`. Os três vão ao IO 2.
**A linha "fora" deveria ser zero em todas as bases**: registro fora da janela indica
divergência entre o declarado e o devolvido, e isso se investiga antes de prosseguir.
Registro **sem ano legível não é descartado**: fica no conjunto, marcado, para decisão uma
a uma na 1ª filtragem, porque descartar por ausência de metadado seria corte cego.

### 5.4 Ordem de triagem (Medida 4)

A fila é ordenada por duas chaves combinadas: **pertinência às expressões mais ricas**
primeiro — a geral, de quatro facetas, à frente das de três e da de cobertura — e, em
seguida, **recência**, com 2022–2026 antes de 2017–2021.

O portfólio continua definido por 2017 em diante: a ordem não exclui nada. Serve para que,
se o prazo apertar, o que ficar por ler seja o menos provável — e o resíduo seja um número
exato, declarável como limitação, em vez de um corte cego.

### 5.5 Aderência ao conjunto-semente — `--aderencia`

Lê `data/sementes.json` e confere quais dos dez estudos aparecem nas consultas
registradas. **Não aplica o recorte temporal**: o conjunto-semente valida o desenho da
busca, não os critérios de elegibilidade.

O script imprime a razão recuperados/informados, que **não é a aderência**. O denominador
correto são as sementes que cada base **indexa**, apurado à mão em
`data/saida/semente/semente_aderencia.csv`, gerado por `gen_semente.py`: semente ausente
por não ser indexada não conta contra a string. Cada ausência exige diagnóstico — qual
termo a teria alcançado. Instrumento completo e limiar de 80 %:
`data/saida/semente/Conjunto_Semente.md`.

### 5.6 Fidelidade — obrigatória

Nenhuma contagem derivada é aceita antes dele. Executar **E2 e E3 diretamente na base**,
exportar, e comparar:

```bash
python3 src/derivar_expressoes.py --fidelidade E2 data/execucoes/wos/e2_conferencia.ris
```

O script reporta a divergência simétrica — a proporção de registros que estão em apenas um
dos dois conjuntos — e **reprova acima de 10 %**, encerrando com código de erro.
Reprovado, volta-se às execuções separadas por expressão, com registro de emenda ao
protocolo.

A divergência esperada é pequena e tem origem conhecida: `TS=` e `TITLE-ABS-KEY` alcançam
o *Keywords Plus* e aplicam lematização; o casamento local vê apenas título, resumo e
palavras-chave exportados, e aproxima a lematização por flexão simples de plural. É
exatamente essa aproximação que o teste mede.

### 5.7 Zero derivado não é zero medido

Contagem derivada igual ou próxima de zero **não pode ser relatada como achado sem
execução direta daquela expressão na base**. O casamento local vê apenas título, resumo e
palavras-chave como exportados, aproxima a lematização e não alcança o processamento
próprio da base: um zero aqui pode ser limitação do método, não ausência de literatura.

A distinção importa porque, nesta revisão, zero em E2, E3 ou E1 **é um achado possível e
relevante** — significaria que a literatura representa artefatos no domínio educacional
mas não as práticas, ou não os fatores situacionais, ou nunca as quatro facetas juntas. É
justamente a lacuna que a pesquisa quer caracterizar, e por isso não pode repousar sobre
uma aproximação local.

Zero em E4 é outra coisa: sendo E4 o próprio portfólio, zero ali é quase sempre defeito de
consulta, e se investiga antes de qualquer registro.

### 5.8 Formatos aceitos

RIS, exportação *Plain text* da Web of Science, CSV e TSV. O script informa quantos
registros leu de cada arquivo — e essa contagem é conferida contra a do registro da
consulta.

## 6. `gen_semente.py` — instrumento do teste de aderência

Lê `data/strings.json` (termos executados) e `data/sementes.json` (referências e
metadados) e grava, em `data/saida/semente/`, o guia `Conjunto_Semente.md` e a planilha
`semente_aderencia.csv`, com uma linha por semente e por base.

O guia traz a composição por base, o estado de conferência de cada referência, as
pendências de metadado e o **ensaio seco**: casamento por frase inteira entre cada título
e os termos das quatro facetas. É ensaio, não execução — a busca procura também no resumo,
de modo que a semente sem termo no título ainda pode ser recuperada.

Semente marcada `no_protocolo=false` fica fora do instrumento e é reportada, para decisão.

## 7. `validar_termos.py` — validação terminológica assistida

O **registro** é o bloco `estatuto` de `data/descritores.json`. A planilha
`data/saida/validacao/validacao_termologica.csv` é **exportação**: serve para ler em
planilha e para registrar decisões, que voltam ao JSON por `--importar` (somente as
colunas `decisao_ReT`, `justificativa_ReT` e `data_decisao`).

Dois instrumentos de consulta sistemática, para as quatro facetas:

| Instrumento | Termos | Via |
| :--- | :--- | :--- |
| IBICT — Tesauro Brasileiro de Ciência da Informação | 89 em português | API TemaTres |
| UNESCO Thesaurus | 189 em inglês e espanhol | SPARQL |

ERIC Thesaurus, Brased/INEP, ACM CCS, LISTA, W3C e IEEE LOM são **referência documental**
pela regra única de validação terminológica: não são percorridos termo a termo. A faceta 4
— fatores situacionais — é **termo livre por decisão de protocolo**, e as suas linhas
nascem classificadas, com a decisão como procedência. **Termo livre POR DECISÃO não é
termo livre POR NÃO LOCALIZADO**, e o registro distingue os dois.

- `--sonda` é obrigatório antes de validar: confere a forma do JSON do TemaTres, os
  idiomas do UNESCO Thesaurus e a versão de cada instrumento. Não grava nada.
- `--validar` grava estatuto, versão, URL e caminho da evidência no JSON e reexporta a
  planilha. Linhas já classificadas são puladas, e o JSON é gravado a cada 20 termos.
- Falha de rede **não** é registrada como "termo não localizado": a linha fica pendente,
  com a falha anotada, e cinco falhas seguidas interrompem a execução em vez de insistir
  contra um serviço indisponível.
- Toda linha classificada aponta para um arquivo em `data/evidencia/`. **Linha sem
  evidência é linha inválida** — foi esse o defeito que originou a ressalva de procedência
  do protocolo.

O script **recupera e registra; não decide**. Nenhum termo é excluído, reescrito ou
incorporado automaticamente. TG, TE e TR revelados pela consulta entram como
**candidatos**: incorporá-los às strings é decisão do pesquisador, com o VT, e exige
regerar as fichas de busca.

Sobre a redação do passo (4) do procedimento: aplicado à letra, "excluir o termo que não se
confirme" apagaria `fatores situacionais`, `padrão de projeto de ontologia` e outros que
nenhum tesauro carrega — e que são justamente o que a categoria *termo livre* existe para
acomodar. O script não os exclui. Sugere-se: *reclassificar como termo livre, com
justificativa; excluir apenas o termo morto e a forma não-preferida cujo equivalente
autorizado já conste da string.*

Ritmo: uma requisição por vez, com pausa de 1 segundo. São serviços públicos de terceiros,
mantidos por instituições; a validação inteira soma **278 consultas** — 89 no TBCI e 189
no UNESCO —, nada que justifique paralelismo.

## 8. Pendências e histórico

`data/pendencias.json` é o **estado** do que está aberto. Não é histórico: o histórico é o
**Anexo A**, `docs/1_gestao/historico.md`. `--pendencias` relata o que encontra nos artefatos,
sem escrever; a promoção de um achado a pendência registrada é decisão do pesquisador.

## 9. Datas

A data oficial de execução consta **exclusivamente do IO 7**. `data/consultas.json` guarda
data e hora operacionais de cada consulta, como rastro técnico do registro — e assim está
declarado no `README.md` do repositório e no Anexo A.

## 10. Convenções

- **Português do Brasil**, redação formal, objetiva e enxuta.
- Datas de execução no **IO 7**; histórico no **Anexo A**.
- Saídas em CSV com separador `;` e UTF-8 com BOM, para abrir direto no Excel em português.
