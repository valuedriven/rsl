# RSL-01 — Representação do conhecimento sobre práticas educacionais e seus fatores situacionais

Revisão sistemática de literatura sobre modelos conceituais, ontologias e outros sistemas de
organização do conhecimento que representam formalmente práticas do processo de
ensino-aprendizagem e os fatores situacionais que condicionam a sua aplicação.

Conduzida pelo **RS Banyan**, com o **PRISMA** como diretriz de apresentação. Integra a
pesquisa de doutorado de Junilson Pereira Souza no PPGGOC/ECI/UFMG, sob orientação da
Profa. Dra. Elisângela Cristina Aganette.

Este arquivo é a **porta de entrada** do repositório: indica onde cada assunto está decidido
e não repete o conteúdo dos documentos.

## Como o repositório se organiza

| Onde | O que é |
| --- | --- |
| `docs/` | conteúdo da revisão: instrumentos, plano, protocolo e fichas de busca |
| `data/` | dados do projeto: os nove JSON, as exportações, as saídas dos scripts e o arquivo |
| `src/` | quatro scripts de execução e o `README.md` que os explica |
| `.agents/skills/` | 19 competências metodológicas e operacionais do agente |
| `AGENTS.md` | contrato de trabalho do agente: como ele se comporta, não o que o projeto decide |

## Mapa

| Caminho | O que contém | Consultar quando |
| --- | --- | --- |
| `docs/0_io_rs_banyan/` | IO 0 a IO 7 preenchidos | ler o instrumento vigente de uma etapa |
| `docs/1_gestao/01_plano.md` | contexto, objetivos, método, escopo, cronograma, custos, qualidade, riscos e uso de IA | entender o desenho e os limites da revisão |
| `docs/1_gestao/log.md` | Anexo A: linha do tempo das decisões, verificações, calibração das buscas, emendas e pendências | saber o que já foi decidido, verificado ou está em aberto |
| `docs/2_protocolo/02_protocolo_aspectos_preliminares.md` | tópicos preliminares, delimitação do assunto, objeto e recorte | conferir o que a revisão examina e o que fica fora |
| `docs/2_protocolo/03_protocolo_estrategia_pesquisa.md` | questão de revisão, questões secundárias, facetas, strings, expressões, critérios de elegibilidade, fontes e conjunto-semente | montar ou conferir a busca |
| `docs/2_protocolo/03_1_Strings_Busca_1_Web_of_Science.md` | ficha da Web of Science: sintaxe, strings nativas, execução, aderência e ressalvas | executar ou auditar esta base |
| `docs/2_protocolo/03_2_Strings_Busca_2_Scopus.md` | ficha da Scopus, mesma estrutura | idem |
| `docs/2_protocolo/03_3_Strings_Busca_3_ERIC.md` | ficha da ERIC, mesma estrutura | idem |
| `docs/2_protocolo/03_4_trings_Busca_4_BRAPCI.md` | ficha da BRAPCI, mesma estrutura | idem |
| `src/protocolo.py` | leitor do protocolo: confere e deriva os JSON de `data/` | antes de executar qualquer script, e após alterar o protocolo |
| `src/derivar_expressoes.py` | registro das consultas, derivação local de E1 a E3, aderência e fidelidade | registrar execução, calcular a pertinência de cada registro, testar a busca |
| `src/validar_termos.py` | validação assistida no TBCI e no UNESCO Thesaurus | conferir o estatuto de cada termo |
| `src/gen_semente.py` | geração do instrumento de aderência a partir do conjunto-semente | montar a planilha de aferição de uma base |
| `docs/3_portfolio/` | destino do portfólio | guardar os registros selecionados |

Em `data/`, a procedência de cada arquivo:

| Caminho | O que contém | Quem escreve |
| --- | --- | --- |
| `data/questoes.json` | questão principal, QS1–QS4 e estrutura PICo | `--gerar` |
| `data/facetas.json` | palavras significativas: nome, cor e âncora de cada faceta | `--gerar` |
| `data/descritores.json` | controle terminológico por faceta e estatuto de validação de cada termo | `--gerar` + validação |
| `data/strings.json` | string de cada faceta e composição das expressões E1–E4 | `--gerar` |
| `data/criterios.json` | critérios de inclusão e de exclusão e recorte temporal | `--gerar` |
| `data/fontes.json` | bases, ordem de execução, via de acesso, acervos e ferramenta | `--gerar` |
| `data/sementes.json` | conjunto-semente e metadados de conferência de cada referência | `--gerar` + pesquisador |
| `data/consultas.json` | registro das execuções: base, expressão, data e hora, retorno | `--registrar` |
| `data/pendencias.json` | estado das tarefas e pendências abertas | pesquisador |
| `data/execucoes/<base>/` | exportações intactas das bases | pesquisador |
| `data/saida/` | planilhas, CSVs e instrumentos gerados pelos scripts | scripts |
| `data/evidencia/` | resposta bruta de cada consulta terminológica | `validar_termos.py` |
| `data/arquivo/` | cópias anteriores, com `SHA256` — vazio: o arquivo da migração de 16/11 foi descartado | migrações |

## Por onde começar

1. **Plano** — `docs/1_gestao/01_plano.md`: por que a revisão existe, com que prazo e sob que riscos.
2. **Protocolo** — `docs/2_protocolo/02_protocolo_aspectos_preliminares.md`: o que se pergunta e o que fica fora.
3. **Estratégia** — `docs/2_protocolo/03_protocolo_estrategia_pesquisa.md`: como se busca, com que critérios e com que conjunto-semente.
4. **Fichas por base** — `03_1` a `03_4`: o que executar em cada base, na sintaxe dela.
5. **Anexo A** — `docs/1_gestao/log.md`: o que já foi decidido, verificado e o que está pendente.

## Precedência

- O **IO 1** prevalece sobre qualquer formulação feita em outro documento; o plano e a estratégia remetem a ele.
- O **Anexo A** é o único lugar do histórico.
- A data **oficial** de execução consta **exclusivamente do IO 7**; `data/consultas.json`
  registra data e hora operacionais de cada consulta, como rastro técnico do registro.

## Scripts

Podem ser executados da raiz do repositório. `src/README.md` é o manual de execução;
aqui fica o essencial.

**Protocolo como fonte**

```bash
python3 src/protocolo.py --conferir               # lê o documento e relata problemas
python3 src/protocolo.py --conferir-dados         # confere os JSON de data/ entre si
python3 src/protocolo.py --conferir --autoteste   # prova que as conferências reprovam
python3 src/protocolo.py --gerar                  # deriva os JSON
python3 src/protocolo.py --pendencias             # relata pendências, sem escrever
```

`docs/2_protocolo/03_protocolo_estrategia_pesquisa.md` é a fonte única da questão, das
facetas, do vocabulário, das strings, das expressões, dos critérios, das fontes e do
conjunto-semente. `--gerar` deriva dele sete JSON:

- `questoes.json`, `facetas.json`, `strings.json`, `criterios.json` e `fontes.json` —
  integralmente derivados;
- `descritores.json` — tabelas derivadas e o estatuto de validação de cada termo, autoral;
- `sementes.json` — referências e mapa por base derivados, e a conferência de cada
  semente, autoral.

Cada arquivo guarda o `sha256` do documento e o `sha256` do próprio subconjunto derivado:
o primeiro detecta documento alterado sem regerar; o segundo, campo derivado editado à
mão. `--gerar` nunca sobrescreve o que é autoral, e termo ou semente retirado do protocolo
permanece preservado, com `no_protocolo=false`, para decisão.

`data/consultas.json` e `data/pendencias.json` são auxiliares: criados só se ausentes e
nunca reescritos por `--gerar`.

**Derivação das expressões e testes**

```bash
python3 src/derivar_expressoes.py --registrar wos E4 data/execucoes/wos/e4.ris --retorno 18432
python3 src/derivar_expressoes.py --derivar
python3 src/derivar_expressoes.py --aderencia
python3 src/derivar_expressoes.py --fidelidade E2 data/execucoes/wos/e2_conferencia.ris
```

O `--derivar` não lê a pasta de exportações: lê as consultas registradas. O `--registrar`
confere o retorno que a base exibiu contra os registros do arquivo e **recusa registrar
quando divergem**, salvo justificativa explícita — é o caso do teto de 1.000 da BRAPCI.
Grava, em `data/saida/derivacao/`, `registros.csv`, `io2_contagens.csv` e
`ordem_triagem.csv`; o teste de fidelidade grava `fidelidade_E<n>.csv`. Nenhum registro é
excluído: repetido no mesmo DOI ou título é marcado em `duplicata_de`, e as contagens do
IO 2 usam os únicos, com o número bruto ao lado.

**Validação terminológica**

```bash
python3 src/validar_termos.py --sonda        # obrigatório antes de validar
python3 src/validar_termos.py --exportar     # planilha a partir do JSON
python3 src/validar_termos.py --validar tbci
python3 src/validar_termos.py --validar unesco
python3 src/validar_termos.py --importar     # traz as decisões da planilha
```

O registro é o bloco `estatuto` de `data/descritores.json`; a planilha em
`data/saida/validacao/` é exportação, e as decisões voltam ao JSON por `--importar`. Cada
consulta grava uma resposta bruta em `data/evidencia/`. O script recupera e registra; não
decide.

**Conjunto-semente**

```bash
python3 src/gen_semente.py
```

Gera, em `data/saida/semente/`, `Conjunto_Semente.md` e `semente_aderencia.csv`.

As exportações das bases não integram este repositório: depositam-se em
`data/execucoes/<base>/` e se registram com `--registrar` antes de executar `--derivar` ou
`--aderencia`. O vocabulário, os termos e o conjunto-semente vêm do protocolo, por
`--gerar`.

## Convenções

- **Português do Brasil**, redação formal, objetiva e enxuta.
- Referências normalizadas pela **ABNT NBR 6023**, cada uma com o seu estado de conferência.
- Datas de execução no **IO 7**; histórico no **Anexo A**.
- Nomeação dos arquivos de estudo: `Ano_DuasPrimeirasPalavras_TIPO_UltimoSobrenomeAutor`,
  com sufixo `_FICHA` para fichamentos.

## Autoria e uso de IA

**Junilson Pereira Souza** — responsabilidade técnica. Orientação: **Profa. Dra. Elisângela
Cristina Aganette**.

A assistência de inteligência artificial é declarada e registrada ação a ação no LOG_IA,
apêndice do IO 1. A IA **não é autora**, conforme ICMJE e COPE. As regras de uso estão em
`docs/1_gestao/01_plano.md`, seção 8.
