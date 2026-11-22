# Guia de procedimentos — módulos, etapas e passos

O que se faz, em que ordem e com que apoio. A revisão segue o **RS Banyan** (plano,
`docs/01_plano.md` §1.4): quatro módulos, catorze etapas e sessenta e três passos. Os
títulos de módulo e de etapa são os do plano §1.4; os passos seguem a ordem da estrutura
fornecida pelo pesquisador, atribuída a Borges (2020). **Essa estrutura de passos não foi
conferida na tese.**

Cada passo é uma linha na forma genérica, válida para o modelo e para a prática do
projeto. O que é específico do projeto não está aqui: está na fonte indicada sob o passo.
Sob cada passo, quando houver:

- **Fonte** — documento e seção onde a decisão está; prevalece sobre este guia.
- **Script** — sinopse do comando, transcrita de `python3 -m rsl <subcomando> -h`, que é a
  fonte dos parâmetros. Como executar, o mapa dos caminhos e os códigos de saída: `README.md`.
- **Skill** — competência em `.agents/skills/` que orienta a execução.

Os passos não são numerados, e os demais documentos citam um passo pelo módulo, pela etapa
e pelo nome da atividade, nunca pelo ordinal. Valores de parâmetro e
limiar não se transcrevem: o valor em uso e a origem saem de `python3 -m rsl mostrar`.

---

## M1 — Planejamento (exequibilidade da revisão)

### E1 — Definição dos objetivos

- Realizar pesquisas preliminares sobre o tema
  - Fonte: plano §1.1
- Consultar pesquisadores da área sobre as intenções iniciais
- Elaborar o escopo da revisão e discuti-lo com a orientação
  - Fonte: plano §2.1 a §2.4
- Elaborar os objetivos da revisão
  - Fonte: plano §1.2 e §1.3; a formulação canônica das questões está no protocolo
    (`docs/03_protocolo_estrategia_pesquisa.md` §Questão de revisão)
  - Skill: `questao-e-objetivos`

### E2 — Avaliação da necessidade

- Pesquisar revisões sistemáticas anteriores
- Consultar biblioteca especializada no tema
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Bibliotecas especializadas; papel VT
    no plano §4.2
- Decidir sobre a execução da revisão
  - Fonte: plano §1.1 e §2.2
  - Skill: `registrar-decisao`

### E3 — Viabilização dos instrumentos operacionais

- Preparar o protocolo de revisão (IO 1)
  - Fonte: `docs/02_protocolo_informacoes_gerais.md`; `docs/03_protocolo_estrategia_pesquisa.md`
  - Script: `python3 -m rsl gramatica` (forma que o leitor exige); conferências na seção
    [Conferências transversais](#conferências-transversais)
- Preparar a tabela de composição do portfólio (IO 2)
  - Fonte: plano §2.3
- Preparar o fluxograma da revisão (IO 3)
  - Fonte: plano §1.4 (método de apresentação) e §6.3
  - Skill: `relato-prisma`
- Preparar o formulário de fichamento (IO 4)
  - Fonte: protocolo §Instrumentos; `docs/parametros_complementares.md`
  - Skill: `fichamento`
- Preparar o glossário (IO 5)
  - Fonte: plano §2.3
  - Skill: `fichamento`
- Definir a ferramenta de gestão de dados bibliográficos
  - Fonte: protocolo §Ferramentas; plano §4.1
- Definir as ferramentas de visualização da informação

### E4 — Definição da equipe

- Relacionar os agentes aptos a auxiliar na revisão
  - Fonte: plano §4.2
- Validar a proposta de equipe com a orientação
  - Fonte: plano §4.2
- Preparar a planilha de competências (IO 6)
  - Fonte: plano §4.2 (a planilha está fora deste repositório)

### E5 — Elaboração do cronograma

- Relacionar as tarefas de cada etapa
  - Fonte: plano §3.2 e §3.3
- Validar a estimativa de prazos com a orientação
  - Fonte: plano §3.1
- Preparar o cronograma (IO 7)
  - Fonte: plano §3.2 (o cronograma está fora deste repositório e é o único lugar das datas)

---

## M2 — Questão de revisão (direcionamento)

### E1 — Identificação de tópicos preliminares

- Consultar obras de referência da área
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Obras de referência a consultar
- Consultar biblioteca especializada no tema
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Bibliotecas especializadas
- Verificar estudos iniciais sobre o tema
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Estudos inicialmente consultados acerca
    do tema da revisão
  - Skill: `conferir-referencia`

### E2 — Delimitação do assunto

- Especificar a temática da revisão
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Especificação da temática da revisão
- Delimitar a abordagem sobre a temática
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Delimitação da abordagem sobre a temática
- Identificar o objeto de estudo da revisão
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Objeto de estudo da revisão
- Especificar o objeto de estudo da revisão
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Objeto da revisão
- Redigir as questões de revisão e registrá-las no protocolo (IO 1)
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Questão de revisão
  - Skill: `questao-e-objetivos`

---

## M3 — Pesquisa bibliográfica (busca e avaliação da evidência)

### E1 — Elaboração das estratégias de pesquisa

- Destacar as palavras significativas da questão de revisão
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Facetas da questão de revisão
  - Skill: `facetacao-e-termos-livres`
- Estabelecer o controle terminológico
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Controle terminológico e
    §Instrumentos para controle terminológico
  - Script: `python3 -m rsl termos sonda` — consulta de prova em cada cliente automatizado;
    não grava. Executar antes de validar.
  - Script: `python3 -m rsl termos exportar` — reconstrói a planilha de validação a partir
    do protocolo, sem rede
  - Script: `python3 -m rsl termos validar [--faceta FACETA] SIGLA` — `SIGLA`: instrumento
    `Automático` da tabela de instrumentos, ou `todos`; `--faceta`: número n de `FCTn`
  - Script: `python3 -m rsl termos importar` — reconcilia a planilha com o protocolo,
    preservando as decisões
  - Skill: `validacao-vocabulario-controlado`; `otimizar-strings-revisao-sistematica`
- Elaborar as expressões de busca
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Strings de busca por faceta,
    §Expressões de busca e §Notas explicativas; ficha de cada base §3 e §4
  - Skill: `expressoes-de-busca`; `ficha-de-busca-por-base`
- Definir os critérios de elegibilidade
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Critérios de elegibilidade; ficha de
    cada base §2
  - Skill: `criterios-de-elegibilidade`
- Avaliar e definir as fontes de pesquisa
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Fontes de informação (§Bases de
    dados, §Acervos especiais, §Acervos pessoais); ficha de cada base §1
  - Skill: `ficha-de-busca-por-base`
- Definir a ferramenta de gestão bibliográfica
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Ferramentas e §Procedimentos
- Montar o protocolo de revisão (IO 1)
  - Fonte: `docs/02_protocolo_informacoes_gerais.md`; `docs/03_protocolo_estrategia_pesquisa.md`;
    LOG_IA como apêndice, plano §8.3
  - Script: `python3 -m rsl conferir`; `python3 -m rsl conferir-dados`;
    `python3 -m rsl autoteste` (ver [Conferências transversais](#conferências-transversais))
  - Skill: `rastreabilidade`; `revisao-geral-do-projeto`
- Validar o protocolo com pesquisador expert
  - Fonte: plano §6.1 (validação do protocolo por revisor expert)
  - Skill: `parecer-sobre-protocolo`; `registrar-decisao`

### E2 — Localização dos estudos

- Realizar teste de aderência das expressões de busca
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Conjunto-semente e §Acervos pessoais;
    arquivo de sementes (`[documentos] sementes` do `config.toml`); plano §6.2
  - Script: `python3 -m rsl sementes planilha` — grava a planilha do teste de aderência e
    imprime o ensaio seco
  - Script: `python3 -m rsl busca aderencia` — teste de aderência ao conjunto-semente, por
    papel; lê as execuções registradas
  - Skill: `conjunto-semente`; `teste-de-aderencia`
- Acessar as fontes de pesquisa na ordem predefinida
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Bases de dados (ordem e via de
    acesso); ficha de cada base §1 (estado de verificação da sintaxe); plano §7
  - Skill: `busca-nas-bases`
- Executar expressões de busca
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Expressões de busca e §Notas
    explicativas; ficha de cada base §4 (Como executar, Variantes previstas) e §6
  - Script: `python3 -m rsl busca registrar --retorno RETORNO [--data-hora DATA_HORA]
    [--justificar JUSTIFICAR] BASE EXPRESSAO ARQUIVO` — `BASE`: sigla da tabela de bases;
    `EXPRESSAO`: identificador da expressão no protocolo; `ARQUIVO`: exportação intacta;
    `--retorno`: retorno que a base exibiu;
    `--data-hora`: ISO 8601, padrão agora; `--justificar`: motivo aceito para retorno
    divergente do arquivo
  - Skill: `busca-nas-bases`
- Avaliar a pertinência e a relevância dos resultados
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Notas explicativas; plano §6.2
  - Script: `python3 -m rsl busca derivar` — deriva as expressões não executadas, as
    contagens e a ordem de triagem
  - Script: `python3 -m rsl busca fidelidade EXPRESSAO ARQUIVO` — compara o conjunto
    derivado com a execução direta; `ARQUIVO`: exportação da execução direta da expressão
  - Script: `python3 -m rsl busca sensibilidade [BASE]` — mede a perda da sonda para a
    executada e grava a amostra a classificar; sem `BASE`, todas as bases
  - Skill: `conferencias-da-busca`; índices na tabela abaixo
- Exportar metadados dos resultados
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; exportações intactas
    no caminho `[dados] execucoes` (mapa no `README.md`)
- Criar alertas de busca nas bases
  - Fonte: plano §3.1
- Registrar os resultados quantitativos na tabela de composição do portfólio (IO 2)
  - Fonte: plano §6.2; contagens em `[saidas] contagens`, gravadas por `busca derivar`
  - Skill: `relato-prisma`

#### Índices da localização dos estudos

Medidos sobre as execuções registradas em `[dados] registro`. Limiar e origem: o protocolo
prevalece onde declara; o padrão está em `[padroes]` do `config.toml`; o valor em uso e a
origem saem de `python3 -m rsl mostrar`. Saídas em `[saidas]`, na pasta `[saidas] pasta`.

| Índice | O que mede | Numerador / denominador | Limiar e origem | Script ou manual | Saída |
| --- | --- | --- | --- | --- | --- |
| Retorno declarado × lido | se a exportação traz o número de registros que a base exibiu | igualdade entre `--retorno` e os registros lidos do arquivo | igualdade; divergência só com `--justificar` (ressalva na ficha da base) | `busca registrar`; `busca derivar` reconfere e para com DADOS se o arquivo mudou | `[dados] registro` (`registros_lidos`, `status`) |
| Contagens bruta e única | registros por base e por expressão, executada e derivadas | contagem, com e sem duplicatas; a sonda fica fora | sem limiar; derivada só se aceita após a fidelidade | `busca derivar` | `[saidas] contagens` |
| Duplicatas | registros repetidos no mesmo DOI ou título normalizado, entre as execuções registradas | contagem; nada é apagado | sem limiar | `busca derivar` | `[saidas] registros`, coluna `duplicata_de` |
| Recorte temporal | registros dentro, fora e sem ano | contagem por situação | linha "fora" igual a zero; recorte no critério de intervalo temporal do protocolo, padrão `recorte_ano_min` | `busca derivar` (terminal) | `[saidas] registros`, coluna `recorte` |
| Âncoras não confirmadas | registros únicos em que o casamento local não confirma as âncoras | sem âncora confirmada / registros únicos | sem limiar: aviso, nenhum registro descartado | `busca derivar` (terminal) | `[saidas] registros`, coluna `ancoras_confirmadas` |
| Ordem de triagem | ordem de leitura da 1ª filtragem, não critério | riqueza das expressões atingidas, recência e ano | `[busca] ano_recencia` | `busca derivar` | `[saidas] ordem_triagem` |
| Aderência de validação | recall da busca sobre as sementes que decidem a passagem | sementes de validação recuperadas por título exato / sementes de validação; denominador definitivo: as indexadas, coluna `indexada` preenchida à mão; com intervalo de Wilson a 95% | `limiar_aderencia`: regra de ajuste em protocolo §Conjunto-semente | `busca aderencia` (terminal); conferência manual na planilha | `[saidas] aderencia` (planilha de `sementes planilha`) |
| Aderência de desenvolvimento | recall sobre as sementes que orientaram o vocabulário | recuperadas / sementes de desenvolvimento | não decisória | `busca aderencia` (terminal) | terminal |
| Indício por prefixo | semente com título casado só por prefixo | contagem; fora do numerador | conferência humana obrigatória | `busca aderencia` (terminal) e manual | coluna `recuperada` da planilha |
| Divergência da fidelidade | quanto a derivação local difere da execução direta da mesma expressão | (só na direta + só na derivada) / união | `divergencia_fidelidade` | `busca fidelidade` | `[saidas] fidelidade` |
| Perda da sonda | registros da sonda que a executada não recupera, por base | só na sonda / registros da sonda | sem limiar: tamanho da perda, não decide | `busca sensibilidade` | terminal; `[saidas] sensibilidade` |
| Fração elegível da amostra | quanto da perda da sonda seria elegível | elegíveis / amostra sistemática (tamanho-alvo `[busca] amostra_sensibilidade`) | `sensibilidade`: faixa nas notas explicativas citadas pela executada | manual (coluna `elegivel`); o cálculo sai de `busca sensibilidade` reexecutada com a amostra inteira classificada | `[saidas] sensibilidade` |
| Cobertura de campo | registros sem palavras-chave ou sem resumo, que cegam a aderência | registros sem o campo / registros da exportação, por base | fração declarada por base (plano §6.2) | manual | relato, como limitação da base |
| Coerência entre expressões | se as relações de continência do protocolo se verificam no retorno de cada base | relações do protocolo §Expressões de busca | relações do protocolo (plano §6.2) | manual | registro de execução |

Concordância entre revisores e contagens do fluxo PRISMA são da seleção (M3/E3).

### E3 — Seleção dos estudos

- Analisar os títulos dos registros (1ª filtragem) e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; ordem de leitura em
    `[saidas] ordem_triagem`
  - Skill: `filtragens`
- Analisar os resumos (2ª filtragem) e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos
  - Skill: `filtragens`
- Analisar os textos completos (3ª filtragem) e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; plano §6.3
  - Skill: `filtragens`
- Aplicar os critérios de elegibilidade e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Critérios de elegibilidade
  - Skill: `criterios-de-elegibilidade`; `filtragens`
- Controlar duplicatas e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; plano §6.2 (dupla
    passagem de deduplicação); marca `duplicata_de` em `[saidas] registros`
  - Skill: `deduplicacao`
- Analisar as listas de referências dos estudos selecionados e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos e §Acervos especiais;
    plano §3.3 e §7
  - Skill: `conferir-referencia`
- Incluir estudos de acervos especiais e pessoais e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Acervos especiais e §Acervos pessoais
- Confirmar a seleção por avaliação dupla independente e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos (concordância e
    terceiro revisor); plano §6.1 e §6.2 (kappa)
  - Skill: `filtragens`

### E4 — Extração de dados

- Organizar os arquivos do portfólio definitivo
  - Fonte: convenção de nomeação no `README.md` §Convenções
- Padronizar os arquivos de fichamento
  - Fonte: `README.md` §Convenções
- Coletar dados com o formulário de fichamento (IO 4)
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos e §Instrumentos;
    `docs/parametros_complementares.md`; uso de IA no plano §8
  - Skill: `fichamento`; `conferir-referencia`

---

## M4 — Discussão e redação

### E1 — Interpretação do conhecimento

- Realizar a análise bibliométrica dos estudos
  - Fonte: plano §3.1; `docs/03_protocolo_estrategia_pesquisa.md` §Bases de dados
  - Skill: `sintese-e-lacunas`
- Realizar a análise de conteúdo dos estudos
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos;
    `docs/parametros_complementares.md`
  - Skill: `sintese-e-lacunas`

### E2 — Registro e validação do conteúdo

- Redigir o texto final
  - Skill: `sintese-e-lacunas`; `relato-prisma`
- Formatar as seções do relatório
  - Fonte: plano §1.4 (método de apresentação) e §6.3; declaração de uso de IA a partir do
    LOG_IA, plano §8.3
  - Skill: `relato-prisma`
- Revisar o conteúdo do texto final
  - Skill: `relato-prisma`; `conferir-referencia`

### E3 — Preparação textual e divulgação

- Revisar a língua e o estilo do texto final
- Traduzir o resumo do relatório
- Normalizar e formatar o relatório
  - Fonte: `README.md` §Convenções
  - Skill: `conferir-referencia`
- Registrar e publicar o relatório
  - Fonte: plano §2.3

---

## Conferências transversais

Valem em qualquer etapa. A regra de cada conferência está nas specs e no código; aqui, só
quando executar e o que relatam.

| Comando | Quando executar | O que relata |
| --- | --- | --- |
| `python3 -m rsl conferir` | após alterar o protocolo, uma ficha ou o arquivo de sementes, e antes de qualquer execução | problemas de coerência do protocolo e das fichas |
| `python3 -m rsl conferir-dados` | após alimentar `data/` ou registrar uma execução | arquivos alimentados confrontados com o protocolo |
| `python3 -m rsl autoteste` | após alterar o código, a configuração ou a gramática | se cada conferência reprova os defeitos injetados com o código esperado |
| `python3 -m rsl mostrar` | antes de citar um parâmetro ou limiar | o que foi lido e os parâmetros em uso, com a origem |
| `python3 -m rsl gramatica` | ao redigir ou reestruturar o protocolo, uma ficha ou o arquivo de sementes | o contrato de forma que o leitor exige |
| `python3 -m rsl pendencias` | ao revisar o estado do projeto | pendências encontradas nos artefatos, sem escrever |

Promover um achado de `pendencias` a pendência registrada em `data/pendencias.json` é
decisão do pesquisador. Decisão que altere questão, facetas, critérios ou busca é emenda:
altera-se a fonte e registra-se em `data/historico.md` (skill `registrar-decisao`).
