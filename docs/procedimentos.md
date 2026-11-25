# Guia de procedimentos — módulos, etapas e passos

O que se faz, em que ordem e com que apoio. A revisão segue o **RS Banyan** (plano,
`docs/01_plano.md` §1.4): quatro módulos, catorze etapas e 63 passos do modelo, mais quatro
passos de adaptação do projeto — a geração das STRs, a definição do conjunto-semente, a
geração dos procedimentos de busca e as sondagens de sintaxe —, totalizando 67. Os passos de adaptação levam a marca `(adaptação
do projeto)`. Os títulos de módulo e de etapa são os do plano §1.4;
os passos do modelo seguem a ordem da estrutura
fornecida pelo pesquisador, atribuída a Borges (2020). **Essa estrutura de passos não foi
conferida na tese.**

Cada passo é uma linha na forma genérica, válida para o modelo e para a prática do
projeto. O que é específico do projeto não está aqui: está na fonte indicada sob o passo.
Sob cada passo, quando houver:

- **Fonte** — documento e seção onde a decisão está; prevalece sobre este guia.
- **Script principal** e **Script** — sinopse do comando, transcrita de
  `python3 -m rsl <subcomando> -h`, que é a fonte dos parâmetros. Como executar, o mapa dos
  caminhos e os códigos de saída: `README.md`. O comando marcado principal é o que executa a
  atividade do passo; sem a marca, apoia um passo cuja atividade é de outro.
- **Skill principal** e **Skill** — competência em `.agents/skills/` que orienta a execução. A
  skill principal é a que conduz a atividade do passo, no máximo uma por passo; as demais
  são de apoio. O papel de cada skill está em [Papel das skills](#papel-das-skills).
- **Apoio** — só no passo sem skill nem script: `manual — <razão>` quando a atividade é do
  pesquisador, de gestão ou está fora do repositório; `lacuna — <razão>` quando falta uma
  skill ou um script e a decisão está pendente.

Os passos não são numerados, e os demais documentos citam um passo pelo módulo, pela etapa
e pelo nome da atividade, nunca pelo ordinal. Valores de parâmetro e
limiar não se transcrevem: o valor em uso e a origem saem de `python3 -m rsl configuracao mostrar`.

---

## M1 — Planejamento (exequibilidade da revisão)

### E1 — Definição dos objetivos

- Realizar pesquisas preliminares sobre o tema
  - Fonte: plano §1.1
  - Apoio: manual — pesquisa exploratória do pesquisador, anterior às expressões de busca e sem
    procedimento sistemático
- Consultar pesquisadores da área sobre as intenções iniciais
  - Apoio: manual — contato do pesquisador com especialistas, fora do repositório
- Elaborar o escopo da revisão e discuti-lo com a orientação
  - Fonte: plano §2.1 a §2.4
  - Apoio: manual — decisão do pesquisador com a orientação
- Elaborar os objetivos da revisão
  - Fonte: plano §1.2 e §1.3;
  - Skill: `redigir-questoes-de-revisao`

### E2 — Avaliação da necessidade

- Pesquisar revisões sistemáticas anteriores
  - Apoio: manual — busca exploratória do pesquisador, anterior às expressões de busca e sem
    procedimento sistemático
- Consultar biblioteca especializada no tema
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Bibliotecas especializadas; papel VT
    no plano §4.2
  - Apoio: manual — consulta do pesquisador às bibliotecas, fora do repositório
- Decidir sobre a execução da revisão
  - Fonte: plano §1.1 e §2.2
  - Skill: `registrar-decisao`

### E3 — Viabilização dos instrumentos operacionais

- Preparar o protocolo de revisão (IO 1)
  - Fonte: `docs/02_protocolo_informacoes_gerais.md`; `docs/03_protocolo_estrategia_pesquisa.md`
  - Script principal: `python3 -m rsl documentos gramatica` — o contrato de forma que o leitor
    exige; consultar ao redigir ou reestruturar o protocolo, um procedimento de busca ou o
    arquivo de sementes. Conferências na seção
    [Conferências transversais](#conferências-transversais)
- Preparar a tabela de composição do portfólio (IO 2)
  - Fonte: plano §2.3
  - Skill: `redigir-relatorio`
- Preparar o fluxograma da revisão (IO 3)
  - Fonte: plano §1.4 (método de apresentação) e §6.3
  - Skill: `redigir-relatorio`
- Preparar o formulário de fichamento (IO 4)
  - Fonte: protocolo §Instrumentos; `docs/parametros_complementares.md`
  - Skill: `coletar-dados-dos-estudos`
- Preparar o glossário (IO 5)
  - Fonte: plano §2.3
  - Skill: `coletar-dados-dos-estudos`
- Definir a ferramenta de gestão de dados bibliográficos
  - Fonte: protocolo §Ferramentas; plano §4.1
  - Apoio: manual — decisão de gestão do pesquisador
- Definir as ferramentas de visualização da informação
  - Apoio: manual — decisão de gestão do pesquisador

### E4 — Definição da equipe

- Relacionar os agentes aptos a auxiliar na revisão
  - Fonte: plano §4.2
  - Apoio: manual — gestão da equipe, decisão do pesquisador
- Validar a proposta de equipe com a orientação
  - Fonte: plano §4.2
  - Apoio: manual — decisão do pesquisador com a orientação
- Preparar a planilha de competências (IO 6)
  - Fonte: plano §4.2 (a planilha está fora deste repositório)
  - Apoio: manual — instrumento mantido fora do repositório

### E5 — Elaboração do cronograma

- Relacionar as tarefas de cada etapa
  - Fonte: plano §3.2 e §3.3
  - Apoio: manual — planejamento do pesquisador
- Validar a estimativa de prazos com a orientação
  - Fonte: plano §3.1
  - Apoio: manual — decisão do pesquisador com a orientação
- Preparar o cronograma (IO 7)
  - Fonte: plano §3.2 (o cronograma está fora deste repositório e é o único lugar das datas)
  - Apoio: manual — instrumento mantido fora do repositório

---

## M2 — Questão de revisão (direcionamento)

### E1 — Identificação de tópicos preliminares

- Consultar obras de referência da área
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Obras de referência a consultar
  - Skill: `conferir-referencia`
- Consultar biblioteca especializada no tema
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Bibliotecas especializadas
  - Apoio: manual — consulta do pesquisador às bibliotecas, fora do repositório
- Verificar estudos iniciais sobre o tema
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Estudos inicialmente consultados acerca
    do tema da revisão
  - Skill: `conferir-referencia`

### E2 — Delimitação do assunto

- Especificar a temática da revisão
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Especificação da temática da revisão
  - Skill: `redigir-questoes-de-revisao`
- Delimitar a abordagem sobre a temática
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Delimitação da abordagem sobre a temática
  - Skill: `redigir-questoes-de-revisao`
- Identificar o objeto de estudo da revisão
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Objeto de estudo da revisão
  - Skill: `redigir-questoes-de-revisao`
- Especificar o objeto de estudo da revisão
  - Fonte: `docs/02_protocolo_informacoes_gerais.md` §Objeto da revisão
  - Skill: `redigir-questoes-de-revisao`
- Redigir as questões de revisão e registrá-las no protocolo (IO 1)
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Questão de revisão
  - Skill principal: `redigir-questoes-de-revisao`

---

## M3 — Pesquisa bibliográfica (busca e avaliação da evidência)

### E1 — Elaboração das estratégias de pesquisa

- Destacar as palavras significativas da questão de revisão
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Facetas da questão de revisão
  - Skill principal: `destacar-termos-da-questao`
- Estabelecer o controle terminológico
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Controle terminológico e
    §Instrumentos para controle terminológico
  - Script principal: `python3 -m rsl termos sondar` — consulta de prova em cada endereço
    resolvido dos instrumentos `Automático`, um por idioma; não grava. Executar antes de
    validar.
  - Script principal: `python3 -m rsl termos exportar` — reconstrói a planilha de validação a
    partir do protocolo, sem rede, reabrindo as linhas que deixaram de valer
  - Script principal: `python3 -m rsl termos validar [--faceta FACETA] SIGLA` — `SIGLA`:
    instrumento `Automático` da tabela de instrumentos, ou `todos`; `--faceta`: número n de
    `FCTn`
  - Script principal: `python3 -m rsl termos importar` — reconcilia a planilha com o protocolo,
    preservando as decisões
  - Skill principal: `estabelecer-controle-terminologico`
  - Skill: `gerar-strings-de-busca`
- Gerar as strings de busca por faceta a partir do quadro terminológico (adaptação do projeto)
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Controle terminológico; a tabela
    §Strings de busca por faceta é saída de geração e não se edita à mão
  - Script principal: `python3 -m rsl strings gerar` — ensaio: exibe, por faceta, os termos a
    acrescentar e a retirar e os subsumidos; não grava
  - Script principal: `python3 -m rsl strings gerar --gravar` — regrava só as células de string;
    recusado se o quadro tiver termo em mais de uma faceta
  - Ordem: quadro → `strings gerar` → `strings gerar --gravar`
  - Skill principal: `gerar-strings-de-busca`
  - Skill: `destacar-termos-da-questao`
- Elaborar as expressões de busca
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Strings de busca por faceta,
    §Expressões de busca e §Notas explicativas
  - Skill principal: `elaborar-expressoes-de-busca`
- Definir os critérios de elegibilidade
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Critérios de elegibilidade
  - Skill principal: `definir-criterios-de-elegibilidade`
- Avaliar e definir as fontes de pesquisa
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Fontes de informação (§Bases de
    dados, §Acervos especiais, §Acervos pessoais)
  - Apoio: manual — escolha das fontes pelo pesquisador, registrada no protocolo
- Definir conjunto semente (adaptação do projeto)
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Conjunto-semente e §Acervos pessoais;
    arquivo de sementes (`[documentos] sementes` do `config.toml`); plano §6.2
  - Skill principal: `definir-conjunto-semente`
- Definir a ferramenta de gestão bibliográfica
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Ferramentas e §Procedimentos
  - Apoio: manual — decisão de gestão do pesquisador
- Montar o protocolo de revisão (IO 1)
  - Fonte: `docs/02_protocolo_informacoes_gerais.md`; `docs/03_protocolo_estrategia_pesquisa.md`;
    LOG_IA como apêndice, plano §8.3
  - Script: `python3 -m rsl documentos conferir`; `python3 -m rsl dados conferir`;
    `python3 -m rsl projeto autoteste` (ver [Conferências transversais](#conferências-transversais))
  - Skill: `revisar-projeto`
- Gerar o procedimento de busca de cada base a partir da fonte (adaptação do projeto)
  - Fonte: fonte do procedimento de cada base (`[documentos] procedimento_fonte`: o
    `procedimento.toml` e os fragmentos de prosa); arquivo de exceções de flexão
    (`[documentos] flexoes`); o procedimento de busca é saída de geração e não se edita à mão
  - Script principal: `python3 -m rsl procedimentos iniciar SIGLA` — base nova: cria a fonte
    da base já registrada no protocolo, com o derivável preenchido e o resto marcado
    `PENDENTE`; não sobrescreve fonte existente
  - Script principal: `python3 -m rsl procedimentos gerar [SIGLA]` — ensaio: exibe, por seção, a
    diferença para o gravado e as formas de número acrescentadas, com a origem; não grava
  - Script principal: `python3 -m rsl procedimentos gerar [SIGLA] --gravar` — substitui o
    procedimento inteiro, de forma atômica; recusado com leitura reprovada ou flexão
    indecidível
  - Ordem: fonte do procedimento de cada base → `procedimentos gerar` →
    `procedimentos gerar --gravar` → `documentos conferir`
  - Skill principal: `gerar-procedimento-de-busca`
  - Skill: `declarar-flexao-por-base`; `executar-sondagens-de-sintaxe`
- Validar o protocolo com pesquisador expert
  - Fonte: plano §6.1 (validação do protocolo por revisor expert)
  - Skill principal: `validar-protocolo`
  - Skill: `registrar-decisao`

### E2 — Localização dos estudos

- Realizar teste de aderência das expressões de busca
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Conjunto-semente e §Acervos pessoais;
    arquivo de sementes (`[documentos] sementes` do `config.toml`); plano §6.2
  - Script principal: `python3 -m rsl aderencia planilhar` — grava a planilha do teste de
    aderência e imprime o ensaio seco
  - Script principal: `python3 -m rsl aderencia medir` — teste de aderência ao
    conjunto-semente, por papel; lê as execuções registradas
  - Skill principal: `testar-aderencia-das-expressoes`
  - Skill: `definir-conjunto-semente`
- Acessar as fontes de pesquisa na ordem predefinida
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Bases de dados (ordem e via de
    acesso); procedimento de busca de cada base §1 (estado de verificação da sintaxe); plano §7
  - Skill: `executar-expressoes-de-busca`
- Executar as sondagens de sintaxe pelo roteiro de cada base (adaptação do projeto)
  - Fonte: procedimento de busca de cada base §1, "Sondagens a executar", na ordem das
    dependências
  - Script principal: `python3 -m rsl sondagens registrar SIGLA SDn --retorno RETORNO
    … --leitura LEITURA --data-hora DATA_HORA --evidencia EVIDENCIA [--submetido K TEXTO]
    [--observacao OBSERVACAO]` — `SDn`: sondagem do roteiro da base; `--retorno`: uma vez por
    consulta declarada, na ordem; `--leitura`: número da leitura observada; `--data-hora`: ISO
    8601, obrigatória, sem padrão; `--evidencia`: arquivo existente, obrigatório. Grava em
    `[dados] registro` e exibe a citação e a mudança a aplicar na fonte, que não altera;
    aplicá-la na fonte e regenerar o procedimento
  - Skill principal: `executar-sondagens-de-sintaxe`
  - Skill: `executar-expressoes-de-busca`
- Executar expressões de busca
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Expressões de busca e §Notas
    explicativas; procedimento de busca de cada base §4 (Como executar, Variantes previstas) e §6
  - Script principal: `python3 -m rsl busca registrar --retorno RETORNO [--data-hora DATA_HORA]
    [--justificar JUSTIFICAR] BASE EXPRESSAO ARQUIVO` — `BASE`: sigla da tabela de bases;
    `EXPRESSAO`: identificador da expressão no protocolo; `ARQUIVO`: exportação intacta;
    `--retorno`: retorno que a base exibiu;
    `--data-hora`: ISO 8601, padrão agora; `--justificar`: motivo aceito para retorno
    divergente do arquivo
  - Skill principal: `executar-expressoes-de-busca`
- Avaliar a pertinência e a relevância dos resultados
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Notas explicativas; plano §6.2
  - Script principal: `python3 -m rsl busca derivar` — deriva as expressões não executadas, as
    contagens e a ordem de triagem
  - Script principal: `python3 -m rsl conferencia fidelidade EXPRESSAO ARQUIVO` — compara o
    conjunto derivado com a execução direta; `ARQUIVO`: exportação da execução direta da
    expressão
  - Script principal: `python3 -m rsl conferencia sensibilidade [BASE]` — mede a perda da
    sonda para a executada e grava a amostra a classificar; sem `BASE`, todas as bases
  - Skill principal: `avaliar-resultados-da-busca`; índices na tabela abaixo
- Exportar metadados dos resultados
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; exportações intactas
    no caminho `[dados] execucoes` (mapa no `README.md`)
  - Skill: `executar-expressoes-de-busca`
- Criar alertas de busca nas bases
  - Fonte: plano §3.1
  - Skill: `executar-expressoes-de-busca`
- Registrar os resultados quantitativos na tabela de composição do portfólio (IO 2)
  - Fonte: plano §6.2; contagens em `[saidas] contagens`, gravadas por `busca derivar`
  - Script: `python3 -m rsl busca derivar` — grava as contagens em `[saidas] contagens`
  - Skill: `redigir-relatorio`

#### Índices da localização dos estudos

Medidos sobre as execuções registradas em `[dados] registro`. Limiar e origem: o protocolo
prevalece onde declara; o padrão está em `[padroes]` do `config.toml`; o valor em uso e a
origem saem de `python3 -m rsl configuracao mostrar`. Saídas em `[saidas]`, na pasta `[saidas] pasta`.

| Índice | O que mede | Numerador / denominador | Limiar e origem | Script ou manual | Saída |
| --- | --- | --- | --- | --- | --- |
| Retorno declarado × lido | se a exportação traz o número de registros que a base exibiu | igualdade entre `--retorno` e os registros lidos do arquivo | igualdade; divergência só com `--justificar` (ressalva no procedimento de busca da base) | `busca registrar`; `busca derivar` reconfere e para com DADOS se o arquivo mudou | `[dados] registro` (`registros_lidos`, `status`) |
| Contagens bruta e única | registros por base e por expressão, executada e derivadas | contagem, com e sem duplicatas; a sonda fica fora | sem limiar; derivada só se aceita após a fidelidade | `busca derivar` | `[saidas] contagens` |
| Duplicatas | registros repetidos no mesmo DOI ou título normalizado, entre as execuções registradas | contagem; nada é apagado | sem limiar | `busca derivar` | `[saidas] registros`, coluna `duplicata_de` |
| Recorte temporal | registros dentro, fora e sem ano | contagem por situação | linha "fora" igual a zero; recorte no critério de intervalo temporal do protocolo, padrão `recorte_ano_min` | `busca derivar` (terminal) | `[saidas] registros`, coluna `recorte` |
| Âncoras não confirmadas | registros únicos em que o casamento local não confirma as âncoras | sem âncora confirmada / registros únicos | sem limiar: aviso, nenhum registro descartado | `busca derivar` (terminal) | `[saidas] registros`, coluna `ancoras_confirmadas` |
| Ordem de triagem | ordem de leitura da 1ª filtragem, não critério | riqueza das expressões atingidas, recência e ano | `[busca] ano_recencia` | `busca derivar` | `[saidas] ordem_triagem` |
| Aderência de validação | recall da busca sobre as sementes que decidem a passagem | sementes de validação recuperadas por título exato / sementes de validação; denominador definitivo: as indexadas, coluna `indexada` preenchida à mão; com intervalo de Wilson a 95% | `limiar_aderencia`: regra de ajuste em protocolo §Conjunto-semente | `aderencia medir` (terminal); conferência manual na planilha | `[saidas] aderencia` (planilha de `aderencia planilhar`) |
| Aderência de desenvolvimento | recall sobre as sementes que orientaram o vocabulário | recuperadas / sementes de desenvolvimento | não decisória | `aderencia medir` (terminal) | terminal |
| Indício por prefixo | semente com título casado só por prefixo | contagem; fora do numerador | conferência humana obrigatória | `aderencia medir` (terminal) e manual | coluna `recuperada` da planilha |
| Divergência da fidelidade | quanto a derivação local difere da execução direta da mesma expressão | (só na direta + só na derivada) / união | `divergencia_fidelidade` | `conferencia fidelidade` | `[saidas] fidelidade` |
| Perda da sonda | registros da sonda que a executada não recupera, por base | só na sonda / registros da sonda | sem limiar: tamanho da perda, não decide | `conferencia sensibilidade` | terminal; `[saidas] sensibilidade` |
| Fração elegível da amostra | quanto da perda da sonda seria elegível | elegíveis / amostra sistemática (tamanho-alvo `[busca] amostra_sensibilidade`) | `sensibilidade`: faixa nas notas explicativas citadas pela executada | manual (coluna `elegivel`); o cálculo sai de `conferencia sensibilidade` reexecutada com a amostra inteira classificada | `[saidas] sensibilidade` |
| Cobertura de campo | registros sem palavras-chave ou sem resumo, que cegam a aderência | registros sem o campo / registros da exportação, por base | fração declarada por base (plano §6.2) | manual | relato, como limitação da base |
| Coerência entre expressões | se as relações de continência do protocolo se verificam no retorno de cada base | relações do protocolo §Expressões de busca | relações do protocolo (plano §6.2) | manual | registro de execução |

Concordância entre revisores e contagens do fluxo PRISMA são da seleção (M3/E3).

### E3 — Seleção dos estudos

- Analisar os títulos dos registros (1ª filtragem) e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; ordem de leitura em
    `[saidas] ordem_triagem`
  - Skill principal: `filtrar-estudos`
  - Script: `python3 -m rsl busca derivar` — grava a ordem de leitura em `[saidas]
    ordem_triagem`
- Analisar os resumos (2ª filtragem) e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos
  - Skill: `filtrar-estudos`
- Analisar os textos completos (3ª filtragem) e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; plano §6.3
  - Skill: `filtrar-estudos`
- Aplicar os critérios de elegibilidade e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Critérios de elegibilidade
  - Skill: `definir-criterios-de-elegibilidade`; `filtrar-estudos`
- Controlar duplicatas e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos; plano §6.2 (dupla
    passagem de deduplicação); marca `duplicata_de` em `[saidas] registros`
  - Skill principal: `controlar-duplicatas`
  - Script: `python3 -m rsl busca derivar` — grava os registros com a marca `duplicata_de` da
    primeira passagem, por identificador
- Analisar as listas de referências dos estudos selecionados e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos e §Acervos especiais;
    plano §3.3 e §7
  - Skill: `conferir-referencia`
- Incluir estudos de acervos especiais e pessoais e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Acervos especiais e §Acervos pessoais
    (nenhum dos dois é fonte autônoma de inclusão: o acervo pessoal compõe o conjunto-semente;
    a ausência de busca nos acervos especiais é limitação declarada no relato)
  - Skill: `definir-conjunto-semente`; `redigir-relatorio`
- Confirmar a seleção por avaliação dupla independente e registrar no IO 2
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos (concordância e
    terceiro revisor); plano §6.1 e §6.2 (kappa)
  - Skill: `filtrar-estudos`

### E4 — Extração de dados

- Organizar os arquivos do portfólio definitivo
  - Fonte: convenção de nomeação no `README.md` §Convenções
  - Apoio: manual — gestão de arquivos pela convenção do README
- Padronizar os arquivos de fichamento
  - Fonte: `README.md` §Convenções
  - Apoio: manual — gestão de arquivos pela convenção do README
- Coletar dados com o formulário de fichamento (IO 4)
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos e §Instrumentos;
    `docs/parametros_complementares.md`; uso de IA no plano §8
  - Skill principal: `coletar-dados-dos-estudos`
  - Skill: `conferir-referencia`

---

## M4 — Discussão e redação

### E1 — Interpretação do conhecimento

- Realizar a análise bibliométrica dos estudos
  - Fonte: plano §3.1; `docs/03_protocolo_estrategia_pesquisa.md` §Bases de dados
  - Skill: `analisar-conteudo-dos-estudos`
- Realizar a análise de conteúdo dos estudos
  - Fonte: `docs/03_protocolo_estrategia_pesquisa.md` §Procedimentos;
    `docs/parametros_complementares.md`
  - Skill principal: `analisar-conteudo-dos-estudos`

### E2 — Registro e validação do conteúdo

- Redigir o texto final
  - Skill principal: `redigir-relatorio`
  - Skill: `analisar-conteudo-dos-estudos`
- Formatar as seções do relatório
  - Fonte: plano §1.4 (método de apresentação) e §6.3; declaração de uso de IA a partir do
    LOG_IA, plano §8.3
  - Skill: `redigir-relatorio`
- Revisar o conteúdo do texto final
  - Skill: `redigir-relatorio`; `conferir-referencia`

### E3 — Preparação textual e divulgação

- Revisar a língua e o estilo do texto final
  - Apoio: manual — revisão textual do pesquisador
- Traduzir o resumo do relatório
  - Apoio: manual — tradução pelo pesquisador
- Normalizar e formatar o relatório
  - Fonte: `README.md` §Convenções
  - Skill: `conferir-referencia`; `redigir-relatorio`
- Registrar e publicar o relatório
  - Fonte: plano §2.3
  - Apoio: manual — submissão e registro fora do repositório

---

## Conferências transversais

Valem em qualquer etapa. A regra de cada conferência está nas specs e no código; aqui, só
quando executar e o que relatam.

| Comando | Quando executar | O que relata |
| --- | --- | --- |
| `python3 -m rsl documentos conferir` | após alterar o protocolo, um procedimento de busca ou o arquivo de sementes, e antes de qualquer execução | problemas de coerência do protocolo e dos procedimentos de busca |
| `python3 -m rsl dados conferir` | após alimentar `data/` ou registrar uma execução | arquivos alimentados confrontados com o protocolo |
| `python3 -m rsl projeto autoteste` | após alterar o código, a configuração ou a gramática | se cada conferência reprova os defeitos injetados com o código esperado |
| `python3 -m rsl configuracao mostrar` | antes de citar um parâmetro ou limiar | o que foi lido e os parâmetros em uso, com a origem |
| `python3 -m rsl projeto pendencias` | ao revisar o estado do projeto | pendências encontradas nos artefatos, sem escrever |
| `python3 -m rsl catalogo gerar` | após alterar este guia, uma skill ou um comando; `--gravar` regrava o catálogo | citações de skill e de comando, cobertura de apoio, contagem de passos e catálogo defasado |

Promover um achado de `projeto pendencias` a pendência registrada em `data/pendencias.json` é
decisão do pesquisador. Decisão que altere questão, facetas, critérios ou busca é emenda:
altera-se a fonte e registra-se em `data/historico.md` (skill `registrar-decisao`).

## Catálogo de apoio

Este guia é a fonte do mapeamento passo → skill e comando; `docs/catalogo_de_apoio.md` é a
visão derivada dele, por passo, por skill e por comando, com a cobertura por etapa. O
catálogo é saída de geração (`python3 -m rsl catalogo gerar --gravar`) e não se edita à
mão: altera-se este guia e regenera-se.

A forma deste guia é o contrato que o catálogo lê: módulo em `## M<n> — `, etapa em
`### E<n> — `, passo em `- ` na coluna 0 e os subitens `Fonte`, `Script principal`, `Script`,
`Skill principal`, `Skill`, `Apoio` e `Ordem` indentados sob o passo. A conferência do
catálogo exige:

- **contagem** — os passos sem marca são do modelo e têm de ser 63, o número do RS Banyan;
  os marcados `(adaptação do projeto)` são do projeto; o total declarado no topo é a soma;
- **apoio** — todo passo cita skill ou comando, ou declara `Apoio: manual` ou
  `Apoio: lacuna` com a razão; `lacuna` é relatada, mas não reprova;
- **citações** — toda skill citada existe e tem o `name` igual à pasta; toda skill existente
  é citada num passo ou declarada transversal em [Papel das skills](#papel-das-skills); todo
  comando e opção citados existem no parser; todo comando do parser é citado num passo ou
  na tabela de conferências transversais;
- **papel e âncora das skills** — toda skill tem um papel; a principal é principal em
  exatamente um passo; o passo tem no máximo uma skill principal; a subordinada declara a
  principal que complementa e é citada no passo dela; subordinada e transversal nunca são
  principais;
- **âncora dos comandos** — todo comando citado é principal em exatamente um passo ou está na
  tabela de conferências transversais, e não as duas coisas; um passo pode ter mais de um
  comando principal.

## Papel das skills

Cada skill tem um papel, declarado aqui e não inferido do nome. Skill **principal** conduz a
atividade de um passo: é `Skill principal` em exatamente um passo e pode ser citada como apoio
em outros. Skill **subordinada** complementa a principal de um passo: é citada nesse passo e
nunca é principal. Skill **transversal** não tem passo próprio: nunca é principal e pode ser
citada como apoio em qualquer passo.

| Papel | Skills |
| --- | --- |
| principal | `redigir-questoes-de-revisao`; `destacar-termos-da-questao`; `estabelecer-controle-terminologico`; `gerar-strings-de-busca`; `elaborar-expressoes-de-busca`; `definir-criterios-de-elegibilidade`; `gerar-procedimento-de-busca`; `validar-protocolo`; `executar-expressoes-de-busca`; `executar-sondagens-de-sintaxe`; `testar-aderencia-das-expressoes`; `definir-conjunto-semente`; `avaliar-resultados-da-busca`; `controlar-duplicatas`; `filtrar-estudos`; `coletar-dados-dos-estudos`; `analisar-conteudo-dos-estudos`; `redigir-relatorio` |
| subordinada | `declarar-flexao-por-base` |
| transversal | `registrar-decisao`; `revisar-projeto`; `conferir-referencia` |

### Skills subordinadas

O passo da subordinada é o passo em que a sua principal é principal.

| Subordinada | Principal que complementa |
| --- | --- |
| `declarar-flexao-por-base` | `gerar-procedimento-de-busca` |
