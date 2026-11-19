# Tasks

## 1. Pré-requisito: documentos no formato novo

- [x] 1.1 Renomear com `git mv` as fichas para `docs/busca_base_<sigla>.md` (`wos`, `scopus`,
  `eric`, `brapci`) e atualizar as referências em `README.md`, `config.toml`,
  `data/pendencias.json` e `.agents/skills/busca-nas-bases/SKILL.md`; verificar por `grep`
  que não resta `busca_base_[0-9]` fora de `openspec/changes/archive`
- [x] 1.2 No protocolo, passar a coluna `Bases` do conjunto-semente para as siglas da tabela
  de bases (`WoS`→`wos`, `Scopus`→`scopus`, `ERIC`→`eric`, `BRAPCI`→`brapci`), sem tocar nas
  demais colunas; verificar por `grep` que não restam as grafias antigas nessa coluna e
  mostrar o diff ao pesquisador
- [x] 1.3 Acrescentar `- Execução: …` a cada ficha (ERIC `particionada`; WoS, Scopus e BRAPCI
  `única`, valores do `config.toml` atual); verificar uma ocorrência por ficha com `grep`

## 2. Leitor de tabela e configuração

- [x] 2.1 Implementar o leitor de tabela por nome de coluna (design D2), reprovando coluna
  exigida ausente e coluna repetida; verificar com casos de autoteste que reprovam cada um
- [x] 2.2 Em `valida_config`, deixar de exigir `padroes.composicao`, `cores`, `fichas`,
  `instrumentos` e `idiomas` e reprovar a presença de qualquer um (design D4); verificar com
  caso de autoteste que injeta `[fichas.wos]` numa cópia da configuração e exige reprovação

## 3. Facetas, quadro e idiomas

- [x] 3.1 Reescrever a leitura da linha de faceta (design D6): sem cor, âncora entre
  parênteses, hífen no nome; retirar a conferência "cor não declarada"; verificar que FCT3 é
  lida com o nome "Práticas do processo de ensino-aprendizagem" e que linha com âncora mal
  formada reprova em autoteste
- [x] 3.2 Ler o quadro com idioma pelo cabeçalho e expor `d["idiomas"]` (design D3); casos de
  autoteste que reprovam: idioma repetido, célula de idioma vazia, conjunto de idiomas
  diferente entre facetas; caso que aprova colunas em outra ordem
- [x] 3.3 Retirar a constante `IDIOMAS` e passar todos os seus usos em `protocolo.py` para
  `d["idiomas"]`; verificar por `grep` que `IDIOMAS` não resta em `src/protocolo.py`

## 4. Instrumentos

- [x] 4.1 Ler a tabela de instrumentos (Sigla, Instrumento, Modo, Caminho, Idiomas, FCTs) e
  montar `d["instrumentos"]` com índice por faceta; reprovar sigla repetida, campo vazio,
  `Modo` fora de `Manual`/`Automático`, idioma fora de `d["idiomas"]`, faceta inexistente em
  `FCTs` e faceta do quadro sem instrumento; um caso de autoteste por reprovação
- [x] 4.2 Em `validar_termos.py`, criar `CLIENTES = {sigla: função}` e substituir `MODO_DE`
  pela leitura de `d`; `--validar` aceita as siglas `Automático` e `todos` (design D5);
  verificar `python3 src/validar_termos.py --help` e o planejamento sobre o protocolo atual
- [x] 4.3 Conferir em `protocolo.py` que todo instrumento `Automático` tem cliente (importação
  tardia); verificar com caso de autoteste que marca `eric` como `Automático` e exige
  reprovação
- [x] 4.4 Ajustar os casos de autoteste do planejamento da validação (instrumento retirado,
  filtro por idioma, modo manual) à tabela nova; verificar que todos executam e aprovam

## 5. Bases, fichas e sementes

- [x] 5.1 Ler a tabela "Bases de dados" por cabeçalho (ID Base, Sigla, Nome da base) e
  localizar a ficha pelo padrão `[documentos] ficha` do `config.toml` (padrão sem `{sigla}`
  reprova a configuração); reprovar sigla ou ID repetido e ficha inexistente; retirar
  `FICHAS`, `BASES`, `BDS`; verificar que o nome lido de BD1 é "Web of Science (Core
  Collection)" e, em autoteste, que sigla sem ficha reprova
- [x] 5.2 Ler a forma de execução da linha `- Execução:` da ficha, reprovando ausência,
  repetição e valor inválido só na base afetada; verificar com caso de autoteste sobre a
  ficha da ERIC sem a linha
- [x] 5.3 Retirar `COR_FACETA` e o seu uso em `consultas_curadas()` (design D9); verificar que
  `--conferir` dá as mesmas consultas curadas e facetas que antes
- [x] 5.4 Reescrever `sementes()` sobre a tabela do conjunto-semente e reduzir
  `distribuicao()` ao cálculo; retirar `_mapa` e a conferência prosa × mapa; reprovar semente
  sem base e sigla fora da tabela de bases; caso de autoteste com `WoS` que exige reprovação
- [x] 5.5 Passar `derivar_expressoes.py` e `gen_semente.py` a `d["bases"]`, com `--base`
  aceitando sigla ou `BDn`; verificar a mensagem de base inválida e uma derivação sobre o
  protocolo atual

## 6. Exibição e documentação

- [x] 6.1 Ajustar `--mostrar` para exibir os parâmetros estruturais com origem "protocolo" e
  a forma de execução com origem na ficha; verificar a saída
- [x] 6.2 Retirar do `config.toml` as cinco chaves e os comentários correspondentes e
  acrescentar `[documentos] ficha = "docs/busca_base_{sigla}.md"`; verificar que `--conferir`
  lê a configuração resultante
- [x] 6.3 Atualizar `README.md` (linhas sobre `config.toml`, `[instrumentos]`, fichas e
  idiomas) e as docstrings de `protocolo.py` e `validar_termos.py`; verificar por `grep` que
  não restam referências a `[fichas]`, `[instrumentos]`, `[cores]` ou `idiomas` do
  `config.toml`

## 7. Integração

- [x] 7.1 Rodar `--conferir` e `--autoteste` sobre o protocolo editado; verificar zero
  problemas, zero defeitos não detectados e o relato separado dos casos não executados
- [x] 7.2 Comparar prova da composição, deriváveis e mapa de bases antes e depois da mudança,
  com siglas comparadas sem distinção de caixa; verificar que coincidem

## Workflow follow-up

- Arquivar a mudança depois da revisão do pesquisador e sincronizar as specs.
