# Design

## Context

A motivação está em `proposal.md`. Estado observado em 2026-11-19:

- `data/registro_execucao.json` não existe. `conferir_dados()` em `src/protocolo.py` já
  reporta isso, mas não liga a ausência às fichas que citam o arquivo como fonte.
- As fichas citam o registro em tabela (WoS, Scopus, seção 1) e em prosa (ERIC, BRAPCI,
  cabeçalho), sempre no máximo com `(BDn)`, nunca com a execução.
- O registro guarda execuções por base em `bases.<BDn>.execucoes[]`, cada uma com `id`
  (ver `_problemas_registro`). Não há chave separada para sondagem: uma sondagem é uma
  execução com `id` próprio.
- O autoteste dos arquivos alimentados (`_autoteste_dados`) já conta como não executados
  os casos que dependem do registro, e `CASOS_DADOS` fixa quantos são.
- `.agents/skills/` tem 21 skills. Nenhuma descreve uma revisão geral do projeto. A mais
  próxima é `parecer-sobre-protocolo`. A descrição dela cobre a "autoavaliação crítica dos
  instrumentos", mas o corpo trata de conferir achados que já vêm prontos (as cinco
  classes, medir o que o parecer raciocina, declinar), não de produzi-los. Nenhum script
  confere a lista de skills do README.

## Goals / Non-Goals

**Goals:**
- Toda afirmação de medição numa ficha aponta para uma execução que existe.
- Pendências e histórico descrevem o estado corrente.
- A revisão geral do projeto passa a ser procedimento, reproduzível e com o alcance
  declarado.

**Non-Goals:**
- Criar o registro de execução ou preencher medições: só com dados que o pesquisador
  fornecer (PD02).
- Validar o *conteúdo* da execução citada, por exemplo se ela de fato mediu `NEAR/x`. A
  conferência garante a existência do lastro, não a pertinência dele.

## Decisions

**D-a. A citação nomeia a execução: `(BDn/<id>)`.** Alternativa considerada: exigir apenas
que a base tenha alguma execução registrada. Foi rejeitada porque qualquer execução
satisfaria a citação, inclusive uma que não mediu nada daquilo. O identificador amarra a
afirmação a um registro específico, e o custo é só escrever o `id`.

**D-b. Detecção por menção ao caminho do registro, em qualquer linha da ficha.** O caminho
vem de `[dados] registro` do `config.toml`, não fixado no código. Alternativa: ler só a
tabela da seção 1. Foi rejeitada porque ERIC e BRAPCI fazem a afirmação em prosa no
cabeçalho e escapariam.

**D-c. A conferência fica em `--conferir-dados`, não em `--conferir`.** Ela depende de
arquivo alimentado, e `--conferir` confere só a coerência interna do documento. A
reprovação é por base, seguindo a exigência "Reprovação é por base".

**D-d. Saída para as linhas atuais: decisão do pesquisador.**
- (a) Reconstituir as execuções no registro e citar `(BDn/<id>)`.
- (b) Rebaixar para **Não verificado**, sem citar o registro.

Esta change não escolhe; a tarefa 1.1 obtém a decisão. Sem dados, o padrão recomendado é
(b), porque não há o que citar.

**D-e. Pendências desatualizadas mudam de estado, não são apagadas.** Segue a regra do
README: `estado` passa a `resolvida` e o registro ganha `resolucao`. PD01 é reescrita para
o que resta (o metadado das sementes), porque a ação que ela descreve continua aberta.

**D-f. Revisão geral como skill, separada do parecer (saída a, recomendada).** A
separação segue a fronteira entre produzir achados e conferir achados de outrem. A
revisão geral **gera** achados percorrendo o projeto. O parecer **confere** achados que
chegam prontos. A revisão reaproveita do parecer as cinco classes de achado e a regra
"medir o que só se raciocina", por remissão e sem cópia. Na saída (a), a descrição de
`parecer-sobre-protocolo` perde "autoavaliação" e remete à skill nova. A saída (b), que
amplia o parecer, evita uma skill a mais, mas junta duas atividades que se acionam em
momentos diferentes.

A skill é de competência metodológica e operacional. Os comandos de conferência não são
fixados nela: ela manda executar os que o README declara, como o contrato exige. O
conteúdo vem da revisão de 2026-11-19 e das retificações que essa revisão exigiu:

1. **Estado.** Em que módulo e etapa o projeto está (README). Trabalho em curso: changes
   abertas, arquivos sem commit e pendências registradas.
2. **Conferências automáticas.** Executar as conferências e os autotestes que o README
   declara, só em leitura. Relatar quantos casos rodaram e quantos **não** rodaram, e
   por quê.
3. **Lastro das afirmações.** Toda afirmação de "verificado" ou "medido" tem de apontar
   para evidência que existe. Pendências e histórico têm de descrever o estado corrente.
   Toda decisão quantitativa tem de ter números registrados.
4. **Facetas e strings.** Pontos a examinar:
   - termo que aparece em mais de uma faceta;
   - termo genérico que satisfaz a faceta quase sempre;
   - conceito da questão sem termo na string;
   - operador que muda a definição operacional entre bases;
   - sonda que não mede o que declara medir.
5. **Conjunto-semente.** Pontos a examinar: circularidade entre ajuste e aferição,
   tamanho e intervalo de confiança do limiar, incidência esperada por base e estado da
   conferência dos metadados.
6. **Critérios.** A regra vive no instrumento que prevalece. Todo critério tem
   justificativa. A nomenclatura é a mesma entre os instrumentos.
7. **Produto.** Contém:
   - o resultado primeiro;
   - a tabela do que se executou;
   - os achados, cada um com a evidência (`arquivo:linha` ou comando), a classe
     (verificado, inferido ou hipótese), a natureza do conserto (unilateral, decisão do
     pesquisador ou código) e a garantia proposta;
   - o que não se fez;
   - as frentes sugeridas.

Três regras próprias da skill:
- **Comportamento de código só se afirma depois de ler o código.** Essa é a lição da
  retificação sobre `gen_semente.py`.
- **A varredura de um padrão abrange o projeto inteiro, não só o lugar em que ele foi
  visto primeiro.** Essa é a lição das citações em prosa da ERIC e da BRAPCI.
- **A revisão não escreve, não acessa fonte externa e não decide.** Indexação, dado
  bibliográfico e sintaxe de base ficam como inferência até serem conferidos pelas
  skills próprias (`conferir-referencia`, `busca-nas-bases`). Achado que exige decisão
  vira alternativa apresentada ao pesquisador. Promover o achado a pendência ou a change
  depende de pedido do pesquisador.

**D-g. Verificação da skill por cobertura, sem conferência automática.** A skill é texto
que o agente segue, e não há script que a exerça. Para não trocar a verificação por
"reler", a tarefa da skill faz a prova por cobertura, em dois passos:
- todo achado da revisão de 2026-11-19 e toda retificação dela correspondem a um passo
  ou a uma regra da skill;
- percorrer o roteiro sobre o estado corrente não deixa de lado nenhum achado ainda
  aberto nas quatro changes.

Não se cria conferência automática de skills. Seria uma garantia nova, fora do escopo
desta change.

## Risks / Trade-offs

- [A conferência nova reprova as quatro fichas no estado atual] → é o comportamento
  pretendido. As linhas são corrigidas (tarefa 2) antes de ativar a conferência
  (tarefa 3), e `--conferir-dados` já reprova hoje pelo registro ausente, de modo que nada
  que passava passa a reprovar.
- [Falso positivo: menção ao registro em instrução, como "registrar em
  `data/registro_execucao.json`"] → a regra vale para toda menção. Instrução de registro
  passa a dizer "no registro de execução" sem o caminho, ou cita a execução. Documentar na
  skill `ficha-de-busca-por-base`.
- [Sem registro, o autoteste não exercita a conferência] → os casos constam como não
  executados, como já ocorre (exigência "Resumo do autoteste distingue caso não
  executado"). Para provar que a conferência reprova, a tarefa 3.3 usa registro sintético
  numa cópia em memória.

## Migration Plan

1. Decisão D-d e correção das linhas das fichas.
2. Conferência nova, com autoteste.
3. Pendências e histórico.

Para reverter, basta remover a conferência; as fichas corrigidas continuam válidas.
