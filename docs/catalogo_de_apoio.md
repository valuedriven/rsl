# Catálogo de apoio — skills e comandos por passo

Gerado de `docs/procedimentos.md` por `python3 -m rsl catalogo gerar --gravar`. **Não editar à mão**: altera-se o guia e regenera-se. A conferência `python3 -m rsl catalogo gerar` reprova este arquivo quando ele está defasado.

Passos: 63 do modelo + 1 de adaptação do projeto = 64.

## Por passo

### M1 — Planejamento (exequibilidade da revisão) › E1 — Definição dos objetivos

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Realizar pesquisas preliminares sobre o tema | modelo | plano §1.1 | — | — | lacuna — skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| Consultar pesquisadores da área sobre as intenções iniciais | modelo | — | — | — | manual — contato do pesquisador com especialistas, fora do repositório |
| Elaborar o escopo da revisão e discuti-lo com a orientação | modelo | plano §2.1 a §2.4 | — | — | manual — decisão do pesquisador com a orientação |
| Elaborar os objetivos da revisão | modelo | plano §1.2 e §1.3; | `questao-e-objetivos` | — | — |

### M1 — Planejamento (exequibilidade da revisão) › E2 — Avaliação da necessidade

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Pesquisar revisões sistemáticas anteriores | modelo | — | — | — | lacuna — skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| Consultar biblioteca especializada no tema | modelo | `docs/02_protocolo_informacoes_gerais.md` §Bibliotecas especializadas; papel VT no plano §4.2 | — | — | lacuna — skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| Decidir sobre a execução da revisão | modelo | plano §1.1 e §2.2 | `registrar-decisao` | — | — |

### M1 — Planejamento (exequibilidade da revisão) › E3 — Viabilização dos instrumentos operacionais

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Preparar o protocolo de revisão (IO 1) | modelo | `docs/02_protocolo_informacoes_gerais.md`; `docs/03_protocolo_estrategia_pesquisa.md` | — | `gramatica` | — |
| Preparar a tabela de composição do portfólio (IO 2) | modelo | plano §2.3 | `relato-prisma` | — | — |
| Preparar o fluxograma da revisão (IO 3) | modelo | plano §1.4 (método de apresentação) e §6.3 | `relato-prisma` | — | — |
| Preparar o formulário de fichamento (IO 4) | modelo | protocolo §Instrumentos; `docs/parametros_complementares.md` | `fichamento` | — | — |
| Preparar o glossário (IO 5) | modelo | plano §2.3 | `fichamento` | — | — |
| Definir a ferramenta de gestão de dados bibliográficos | modelo | protocolo §Ferramentas; plano §4.1 | — | — | manual — decisão de gestão do pesquisador |
| Definir as ferramentas de visualização da informação | modelo | — | — | — | manual — decisão de gestão do pesquisador |

### M1 — Planejamento (exequibilidade da revisão) › E4 — Definição da equipe

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Relacionar os agentes aptos a auxiliar na revisão | modelo | plano §4.2 | — | — | manual — gestão da equipe, decisão do pesquisador |
| Validar a proposta de equipe com a orientação | modelo | plano §4.2 | — | — | manual — decisão do pesquisador com a orientação |
| Preparar a planilha de competências (IO 6) | modelo | plano §4.2 (a planilha está fora deste repositório) | — | — | manual — instrumento mantido fora do repositório |

### M1 — Planejamento (exequibilidade da revisão) › E5 — Elaboração do cronograma

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Relacionar as tarefas de cada etapa | modelo | plano §3.2 e §3.3 | — | — | manual — planejamento do pesquisador |
| Validar a estimativa de prazos com a orientação | modelo | plano §3.1 | — | — | manual — decisão do pesquisador com a orientação |
| Preparar o cronograma (IO 7) | modelo | plano §3.2 (o cronograma está fora deste repositório e é o único lugar das datas) | — | — | manual — instrumento mantido fora do repositório |

### M2 — Questão de revisão (direcionamento) › E1 — Identificação de tópicos preliminares

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Consultar obras de referência da área | modelo | `docs/02_protocolo_informacoes_gerais.md` §Obras de referência a consultar | — | — | lacuna — skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| Consultar biblioteca especializada no tema | modelo | `docs/02_protocolo_informacoes_gerais.md` §Bibliotecas especializadas | — | — | lacuna — skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| Verificar estudos iniciais sobre o tema | modelo | `docs/02_protocolo_informacoes_gerais.md` §Estudos inicialmente consultados acerca do tema da revisão | `conferir-referencia` | — | — |

### M2 — Questão de revisão (direcionamento) › E2 — Delimitação do assunto

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Especificar a temática da revisão | modelo | `docs/02_protocolo_informacoes_gerais.md` §Especificação da temática da revisão | `questao-e-objetivos` | — | — |
| Delimitar a abordagem sobre a temática | modelo | `docs/02_protocolo_informacoes_gerais.md` §Delimitação da abordagem sobre a temática | `questao-e-objetivos` | — | — |
| Identificar o objeto de estudo da revisão | modelo | `docs/02_protocolo_informacoes_gerais.md` §Objeto de estudo da revisão | `questao-e-objetivos` | — | — |
| Especificar o objeto de estudo da revisão | modelo | `docs/02_protocolo_informacoes_gerais.md` §Objeto da revisão | `questao-e-objetivos` | — | — |
| Redigir as questões de revisão e registrá-las no protocolo (IO 1) | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Questão de revisão | `questao-e-objetivos` | — | — |

### M3 — Pesquisa bibliográfica (busca e avaliação da evidência) › E1 — Elaboração das estratégias de pesquisa

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Destacar as palavras significativas da questão de revisão | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Facetas da questão de revisão | `facetacao-e-termos-livres` | — | — |
| Estabelecer o controle terminológico | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Controle terminológico e §Instrumentos para controle terminológico | `validacao-vocabulario-controlado`; `otimizar-strings-revisao-sistematica` | `termos sonda`; `termos exportar`; `termos validar`; `termos importar` | — |
| Gerar as strings de busca por faceta a partir do quadro terminológico | adaptação | `docs/03_protocolo_estrategia_pesquisa.md` §Controle terminológico; a tabela §Strings de busca por faceta é saída de geração e não se edita à mão | `facetacao-e-termos-livres`; `otimizar-strings-revisao-sistematica` | `strings gerar`; `strings gerar` | — |
| Elaborar as expressões de busca | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Strings de busca por faceta, §Expressões de busca e §Notas explicativas; ficha de cada base §3 e §4 | `expressoes-de-busca`; `ficha-de-busca-por-base` | — | — |
| Definir os critérios de elegibilidade | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Critérios de elegibilidade; ficha de cada base §2 | `criterios-de-elegibilidade` | — | — |
| Avaliar e definir as fontes de pesquisa | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Fontes de informação (§Bases de dados, §Acervos especiais, §Acervos pessoais); ficha de cada base §1 | `ficha-de-busca-por-base` | — | — |
| Definir a ferramenta de gestão bibliográfica | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Ferramentas e §Procedimentos | — | — | manual — decisão de gestão do pesquisador |
| Montar o protocolo de revisão (IO 1) | modelo | `docs/02_protocolo_informacoes_gerais.md`; `docs/03_protocolo_estrategia_pesquisa.md`; LOG_IA como apêndice, plano §8.3 | `rastreabilidade`; `revisao-geral-do-projeto` | `conferir`; `conferir-dados`; `autoteste` | — |
| Validar o protocolo com pesquisador expert | modelo | plano §6.1 (validação do protocolo por revisor expert) | `parecer-sobre-protocolo`; `registrar-decisao` | — | — |

### M3 — Pesquisa bibliográfica (busca e avaliação da evidência) › E2 — Localização dos estudos

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Realizar teste de aderência das expressões de busca | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Conjunto-semente e §Acervos pessoais; arquivo de sementes (`[documentos] sementes` do `config.toml`); plano §6.2 | `conjunto-semente`; `teste-de-aderencia` | `sementes planilha`; `busca aderencia` | — |
| Acessar as fontes de pesquisa na ordem predefinida | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Bases de dados (ordem e via de acesso); ficha de cada base §1 (estado de verificação da sintaxe); plano §7 | `busca-nas-bases` | — | — |
| Executar expressões de busca | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Expressões de busca e §Notas explicativas; ficha de cada base §4 (Como executar, Variantes previstas) e §6 | `busca-nas-bases` | `busca registrar` | — |
| Avaliar a pertinência e a relevância dos resultados | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Notas explicativas; plano §6.2 | `conferencias-da-busca` | `busca derivar`; `busca fidelidade`; `busca sensibilidade` | — |
| Exportar metadados dos resultados | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; exportações intactas no caminho `[dados] execucoes` (mapa no `README.md`) | `busca-nas-bases` | — | — |
| Criar alertas de busca nas bases | modelo | plano §3.1 | `busca-nas-bases` | — | — |
| Registrar os resultados quantitativos na tabela de composição do portfólio (IO 2) | modelo | plano §6.2; contagens em `[saidas] contagens`, gravadas por `busca derivar` | `relato-prisma` | — | — |

### M3 — Pesquisa bibliográfica (busca e avaliação da evidência) › E3 — Seleção dos estudos

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Analisar os títulos dos registros (1ª filtragem) e registrar no IO 2 | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; ordem de leitura em `[saidas] ordem_triagem` | `filtragens` | — | — |
| Analisar os resumos (2ª filtragem) e registrar no IO 2 | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos | `filtragens` | — | — |
| Analisar os textos completos (3ª filtragem) e registrar no IO 2 | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; plano §6.3 | `filtragens` | — | — |
| Aplicar os critérios de elegibilidade e registrar no IO 2 | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Critérios de elegibilidade | `criterios-de-elegibilidade`; `filtragens` | — | — |
| Controlar duplicatas e registrar no IO 2 | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; plano §6.2 (dupla passagem de deduplicação); marca `duplicata_de` em `[saidas] registros` | `deduplicacao` | — | — |
| Analisar as listas de referências dos estudos selecionados e registrar no IO 2 | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos e §Acervos especiais; plano §3.3 e §7 | `conferir-referencia` | — | — |
| Incluir estudos de acervos especiais e pessoais e registrar no IO 2 | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Acervos especiais e §Acervos pessoais | — | — | lacuna — skill a decidir (busca-complementar): inclusão de acervos especiais e pessoais sem procedimento declarado |
| Confirmar a seleção por avaliação dupla independente e registrar no IO 2 | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos (concordância e terceiro revisor); plano §6.1 e §6.2 (kappa) | `filtragens` | — | — |

### M3 — Pesquisa bibliográfica (busca e avaliação da evidência) › E4 — Extração de dados

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Organizar os arquivos do portfólio definitivo | modelo | convenção de nomeação no `README.md` §Convenções | — | — | manual — gestão de arquivos pela convenção do README |
| Padronizar os arquivos de fichamento | modelo | `README.md` §Convenções | — | — | manual — gestão de arquivos pela convenção do README |
| Coletar dados com o formulário de fichamento (IO 4) | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos e §Instrumentos; `docs/parametros_complementares.md`; uso de IA no plano §8 | `fichamento`; `conferir-referencia` | — | — |

### M4 — Discussão e redação › E1 — Interpretação do conhecimento

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Realizar a análise bibliométrica dos estudos | modelo | plano §3.1; `docs/03_protocolo_estrategia_pesquisa.md` §Bases de dados | `sintese-e-lacunas` | — | — |
| Realizar a análise de conteúdo dos estudos | modelo | `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; `docs/parametros_complementares.md` | `sintese-e-lacunas` | — | — |

### M4 — Discussão e redação › E2 — Registro e validação do conteúdo

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Redigir o texto final | modelo | — | `sintese-e-lacunas`; `relato-prisma` | — | — |
| Formatar as seções do relatório | modelo | plano §1.4 (método de apresentação) e §6.3; declaração de uso de IA a partir do LOG_IA, plano §8.3 | `relato-prisma` | — | — |
| Revisar o conteúdo do texto final | modelo | — | `relato-prisma`; `conferir-referencia` | — | — |

### M4 — Discussão e redação › E3 — Preparação textual e divulgação

| Passo | Origem | Fonte | Skills | Comandos | Apoio |
| --- | --- | --- | --- | --- | --- |
| Revisar a língua e o estilo do texto final | modelo | — | — | — | manual — revisão textual do pesquisador |
| Traduzir o resumo do relatório | modelo | — | — | — | manual — tradução pelo pesquisador |
| Normalizar e formatar o relatório | modelo | `README.md` §Convenções | `conferir-referencia`; `relato-prisma` | — | — |
| Registrar e publicar o relatório | modelo | plano §2.3 | — | — | manual — submissão e registro fora do repositório |

## Por skill

| Skill | Papel | Passos | Comandos dos mesmos passos | Estado |
| --- | --- | --- | --- | --- |
| `busca-nas-bases` | procedimento | M3/E2 › Acessar as fontes de pesquisa na ordem predefinida; M3/E2 › Executar expressões de busca; M3/E2 › Exportar metadados dos resultados; M3/E2 › Criar alertas de busca nas bases | `busca registrar` | citada |
| `conferencias-da-busca` | procedimento | M3/E2 › Avaliar a pertinência e a relevância dos resultados | `busca derivar`; `busca fidelidade`; `busca sensibilidade` | citada |
| `conferir-referencia` | transversal | M2/E1 › Verificar estudos iniciais sobre o tema; M3/E3 › Analisar as listas de referências dos estudos selecionados e registrar no IO 2; M3/E4 › Coletar dados com o formulário de fichamento (IO 4); M4/E2 › Revisar o conteúdo do texto final; M4/E3 › Normalizar e formatar o relatório | — | citada |
| `conjunto-semente` | artefato | M3/E2 › Realizar teste de aderência das expressões de busca | `busca aderencia`; `sementes planilha` | citada |
| `criterios-de-elegibilidade` | procedimento | M3/E1 › Definir os critérios de elegibilidade; M3/E3 › Aplicar os critérios de elegibilidade e registrar no IO 2 | — | citada |
| `deduplicacao` | procedimento | M3/E3 › Controlar duplicatas e registrar no IO 2 | — | citada |
| `expressoes-de-busca` | procedimento | M3/E1 › Elaborar as expressões de busca | — | citada |
| `facetacao-e-termos-livres` | procedimento | M3/E1 › Destacar as palavras significativas da questão de revisão; M3/E1 › Gerar as strings de busca por faceta a partir do quadro terminológico | `strings gerar` | citada |
| `ficha-de-busca-por-base` | artefato | M3/E1 › Elaborar as expressões de busca; M3/E1 › Avaliar e definir as fontes de pesquisa | — | citada |
| `fichamento` | instrumento | M1/E3 › Preparar o formulário de fichamento (IO 4); M1/E3 › Preparar o glossário (IO 5); M3/E4 › Coletar dados com o formulário de fichamento (IO 4) | — | citada |
| `filtragens` | procedimento | M3/E3 › Analisar os títulos dos registros (1ª filtragem) e registrar no IO 2; M3/E3 › Analisar os resumos (2ª filtragem) e registrar no IO 2; M3/E3 › Analisar os textos completos (3ª filtragem) e registrar no IO 2; M3/E3 › Aplicar os critérios de elegibilidade e registrar no IO 2; M3/E3 › Confirmar a seleção por avaliação dupla independente e registrar no IO 2 | — | citada |
| `otimizar-strings-revisao-sistematica` | procedimento | M3/E1 › Estabelecer o controle terminológico; M3/E1 › Gerar as strings de busca por faceta a partir do quadro terminológico | `strings gerar`; `termos exportar`; `termos importar`; `termos sonda`; `termos validar` | citada |
| `parecer-sobre-protocolo` | procedimento | M3/E1 › Validar o protocolo com pesquisador expert | — | citada |
| `questao-e-objetivos` | procedimento | M1/E1 › Elaborar os objetivos da revisão; M2/E2 › Especificar a temática da revisão; M2/E2 › Delimitar a abordagem sobre a temática; M2/E2 › Identificar o objeto de estudo da revisão; M2/E2 › Especificar o objeto de estudo da revisão; M2/E2 › Redigir as questões de revisão e registrá-las no protocolo (IO 1) | — | citada |
| `rastreabilidade` | transversal | M3/E1 › Montar o protocolo de revisão (IO 1) | `autoteste`; `conferir`; `conferir-dados` | citada |
| `registrar-decisao` | transversal | M1/E2 › Decidir sobre a execução da revisão; M3/E1 › Validar o protocolo com pesquisador expert | — | citada |
| `relato-prisma` | transversal | M1/E3 › Preparar a tabela de composição do portfólio (IO 2); M1/E3 › Preparar o fluxograma da revisão (IO 3); M3/E2 › Registrar os resultados quantitativos na tabela de composição do portfólio (IO 2); M4/E2 › Redigir o texto final; M4/E2 › Formatar as seções do relatório; M4/E2 › Revisar o conteúdo do texto final; M4/E3 › Normalizar e formatar o relatório | — | citada |
| `revisao-geral-do-projeto` | transversal | M3/E1 › Montar o protocolo de revisão (IO 1) | `autoteste`; `conferir`; `conferir-dados` | citada |
| `sintese-e-lacunas` | procedimento | M4/E1 › Realizar a análise bibliométrica dos estudos; M4/E1 › Realizar a análise de conteúdo dos estudos; M4/E2 › Redigir o texto final | — | citada |
| `teste-de-aderencia` | procedimento | M3/E2 › Realizar teste de aderência das expressões de busca | `busca aderencia`; `sementes planilha` | citada |
| `validacao-vocabulario-controlado` | procedimento | M3/E1 › Estabelecer o controle terminológico | `termos exportar`; `termos importar`; `termos sonda`; `termos validar` | citada |

## Por comando

Caminhos lidos do parser; a ajuda é a do próprio comando (`-h`).

| Comando | Ajuda | Passos | Skills dos mesmos passos | Estado |
| --- | --- | --- | --- | --- |
| `autoteste` | injeta defeitos em cópias e exige que cada conferência os reprove com o código esperado | M3/E1 › Montar o protocolo de revisão (IO 1) | `rastreabilidade`; `revisao-geral-do-projeto` | passo |
| `busca aderencia` | teste de aderência ao conjunto-semente, por papel | M3/E2 › Realizar teste de aderência das expressões de busca | `conjunto-semente`; `teste-de-aderencia` | passo |
| `busca derivar` | deriva as expressões não executadas, as contagens e a ordem de triagem | M3/E2 › Avaliar a pertinência e a relevância dos resultados | `conferencias-da-busca` | passo |
| `busca fidelidade` | compara o conjunto derivado com a execução direta | M3/E2 › Avaliar a pertinência e a relevância dos resultados | `conferencias-da-busca` | passo |
| `busca registrar` | registra uma execução e confere o retorno declarado contra o arquivo | M3/E2 › Executar expressões de busca | `busca-nas-bases` | passo |
| `busca sensibilidade` | mede a perda da sonda para a executada e grava a amostra a classificar | M3/E2 › Avaliar a pertinência e a relevância dos resultados | `conferencias-da-busca` | passo |
| `catalogo gerar` | deriva do guia de procedimentos o catálogo de skills e comandos por passo, imprime-o e confere as citações, a cobertura, a contagem de passos e o catálogo gravado; sem --gravar, nada é gravado | — | — | transversal |
| `conferir` | lê o protocolo e as fichas e relata problemas de coerência | M3/E1 › Montar o protocolo de revisão (IO 1) | `rastreabilidade`; `revisao-geral-do-projeto` | passo |
| `conferir-dados` | confere os arquivos alimentados contra o protocolo | M3/E1 › Montar o protocolo de revisão (IO 1) | `rastreabilidade`; `revisao-geral-do-projeto` | passo |
| `gramatica` | exibe o contrato de forma que o leitor exige do protocolo e das fichas | M1/E3 › Preparar o protocolo de revisão (IO 1) | — | passo |
| `mostrar` | resume o que foi lido e os parâmetros em uso, com a origem | — | — | transversal |
| `pendencias` | relata as pendências dos artefatos, sem escrever | — | — | transversal |
| `sementes planilha` | grava a planilha do teste de aderência e imprime o ensaio seco | M3/E2 › Realizar teste de aderência das expressões de busca | `conjunto-semente`; `teste-de-aderencia` | passo |
| `strings gerar` | calcula cada STR a partir do quadro terminológico e exibe a diferença para a tabela do protocolo; sem --gravar, nada é gravado | M3/E1 › Gerar as strings de busca por faceta a partir do quadro terminológico | `facetacao-e-termos-livres`; `otimizar-strings-revisao-sistematica` | passo |
| `termos exportar` | reconstrói a planilha de validação a partir do protocolo, sem rede | M3/E1 › Estabelecer o controle terminológico | `otimizar-strings-revisao-sistematica`; `validacao-vocabulario-controlado` | passo |
| `termos importar` | reconcilia a planilha com o protocolo, preservando as decisões | M3/E1 › Estabelecer o controle terminológico | `otimizar-strings-revisao-sistematica`; `validacao-vocabulario-controlado` | passo |
| `termos sonda` | consulta de prova em cada cliente automatizado; não grava | M3/E1 › Estabelecer o controle terminológico | `otimizar-strings-revisao-sistematica`; `validacao-vocabulario-controlado` | passo |
| `termos validar` | consulta, no instrumento Automático de sigla SIGLA (ou em todos: `todos`), os termos ainda sem estatuto | M3/E1 › Estabelecer o controle terminológico | `otimizar-strings-revisao-sistematica`; `validacao-vocabulario-controlado` | passo |

## Cobertura por etapa

| Módulo | Etapa | Passos | Com skill | Com comando | Manual | Lacuna |
| --- | --- | --- | --- | --- | --- | --- |
| M1 — Planejamento (exequibilidade da revisão) | E1 — Definição dos objetivos | 4 | 1 | 0 | 2 | 1 |
| M1 — Planejamento (exequibilidade da revisão) | E2 — Avaliação da necessidade | 3 | 1 | 0 | 0 | 2 |
| M1 — Planejamento (exequibilidade da revisão) | E3 — Viabilização dos instrumentos operacionais | 7 | 4 | 1 | 2 | 0 |
| M1 — Planejamento (exequibilidade da revisão) | E4 — Definição da equipe | 3 | 0 | 0 | 3 | 0 |
| M1 — Planejamento (exequibilidade da revisão) | E5 — Elaboração do cronograma | 3 | 0 | 0 | 3 | 0 |
| M2 — Questão de revisão (direcionamento) | E1 — Identificação de tópicos preliminares | 3 | 1 | 0 | 0 | 2 |
| M2 — Questão de revisão (direcionamento) | E2 — Delimitação do assunto | 5 | 5 | 0 | 0 | 0 |
| M3 — Pesquisa bibliográfica (busca e avaliação da evidência) | E1 — Elaboração das estratégias de pesquisa | 9 | 8 | 3 | 1 | 0 |
| M3 — Pesquisa bibliográfica (busca e avaliação da evidência) | E2 — Localização dos estudos | 7 | 7 | 3 | 0 | 0 |
| M3 — Pesquisa bibliográfica (busca e avaliação da evidência) | E3 — Seleção dos estudos | 8 | 7 | 0 | 0 | 1 |
| M3 — Pesquisa bibliográfica (busca e avaliação da evidência) | E4 — Extração de dados | 3 | 1 | 0 | 2 | 0 |
| M4 — Discussão e redação | E1 — Interpretação do conhecimento | 2 | 2 | 0 | 0 | 0 |
| M4 — Discussão e redação | E2 — Registro e validação do conteúdo | 3 | 3 | 0 | 0 | 0 |
| M4 — Discussão e redação | E3 — Preparação textual e divulgação | 4 | 1 | 0 | 3 | 0 |

## Passos sem skill nem comando

| Passo | Apoio | Razão |
| --- | --- | --- |
| M1/E1 › Realizar pesquisas preliminares sobre o tema | lacuna | skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| M1/E1 › Consultar pesquisadores da área sobre as intenções iniciais | manual | contato do pesquisador com especialistas, fora do repositório |
| M1/E1 › Elaborar o escopo da revisão e discuti-lo com a orientação | manual | decisão do pesquisador com a orientação |
| M1/E2 › Pesquisar revisões sistemáticas anteriores | lacuna | skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| M1/E2 › Consultar biblioteca especializada no tema | lacuna | skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| M1/E3 › Definir a ferramenta de gestão de dados bibliográficos | manual | decisão de gestão do pesquisador |
| M1/E3 › Definir as ferramentas de visualização da informação | manual | decisão de gestão do pesquisador |
| M1/E4 › Relacionar os agentes aptos a auxiliar na revisão | manual | gestão da equipe, decisão do pesquisador |
| M1/E4 › Validar a proposta de equipe com a orientação | manual | decisão do pesquisador com a orientação |
| M1/E4 › Preparar a planilha de competências (IO 6) | manual | instrumento mantido fora do repositório |
| M1/E5 › Relacionar as tarefas de cada etapa | manual | planejamento do pesquisador |
| M1/E5 › Validar a estimativa de prazos com a orientação | manual | decisão do pesquisador com a orientação |
| M1/E5 › Preparar o cronograma (IO 7) | manual | instrumento mantido fora do repositório |
| M2/E1 › Consultar obras de referência da área | lacuna | skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| M2/E1 › Consultar biblioteca especializada no tema | lacuna | skill a decidir (avaliacao-da-necessidade): busca exploratória e de revisões anteriores sem procedimento declarado |
| M3/E1 › Definir a ferramenta de gestão bibliográfica | manual | decisão de gestão do pesquisador |
| M3/E3 › Incluir estudos de acervos especiais e pessoais e registrar no IO 2 | lacuna | skill a decidir (busca-complementar): inclusão de acervos especiais e pessoais sem procedimento declarado |
| M3/E4 › Organizar os arquivos do portfólio definitivo | manual | gestão de arquivos pela convenção do README |
| M3/E4 › Padronizar os arquivos de fichamento | manual | gestão de arquivos pela convenção do README |
| M4/E3 › Revisar a língua e o estilo do texto final | manual | revisão textual do pesquisador |
| M4/E3 › Traduzir o resumo do relatório | manual | tradução pelo pesquisador |
| M4/E3 › Registrar e publicar o relatório | manual | submissão e registro fora do repositório |
