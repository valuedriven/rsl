---
name: revisao-geral-do-projeto
description: Faz a revisão geral do estado do projeto de revisão sistemática — percorre o estado do ciclo, executa as conferências e os autotestes que o README declara, confere o lastro das afirmações, examina facetas, strings, conjunto-semente e critérios, e entrega os achados classificados com evidência e natureza do conserto. Use ao revisar o projeto inteiro, ao preparar uma rodada de emendas, ao auditar o estado antes de uma execução, e ao verificar se pendências, histórico e fichas descrevem o estado corrente.
---

# Revisão geral do projeto

A revisão geral **produz** achados percorrendo o estado do projeto inteiro. Não se confunde
com o parecer: o parecer **confere** achados que chegam prontos
(`parecer-sobre-protocolo`). Aqui se procura o que ninguém apontou ainda.

Ela não escreve, não acessa fonte externa e não decide. O produto é um relatório; a promoção
de um achado a pendência ou a change depende de pedido do pesquisador.

## 1. Estado

Ler o `README.md` e dizer em que módulo e etapa o projeto está. Levantar o que está em curso:

- changes abertas, com as tarefas concluídas e as pendentes;
- arquivos modificados sem commit;
- pendências registradas e o estado de cada uma.

Não inferir estado de memória: ler os artefatos — `data/pendencias.json`, `data/historico.md`,
a lista de changes e o estado do repositório. Pendência que descreve estado já mudado é
achado, não contexto.

## 2. Conferências automáticas

Executar, **só em leitura**, as conferências e os autotestes que o `README.md` declara. A
skill não fixa comandos: eles estão no README e mudam com o projeto.

Relatar quantos casos rodaram, quantos **não** rodaram e por quê. Caso não executado não é
caso aprovado: a ausência de um arquivo alimentado deixa a conferência correspondente sem
prova, e isso se declara.

## 3. Lastro das afirmações

Toda afirmação de "verificado" ou "medido" tem de apontar para evidência que existe. Conferir
contra o artefato citado — arquivo, linha, execução, contagem.

- Pendências e histórico têm de descrever o estado corrente.
- Toda decisão quantitativa tem de ter números registrados; número não registrado se declara
  não registrado, nunca se reconstrói de memória.
- Falha de acesso ou de registro não é ausência de informação: fica pendência registrada.

## 4. Facetas e strings

Examinar os pontos que a experiência do projeto mostra que se perdem:

- termo que aparece em mais de uma faceta;
- termo genérico que satisfaz a faceta quase sempre;
- conceito da questão sem termo na string;
- operador que muda a definição operacional entre bases;
- sonda que não mede o que declara medir.

## 5. Conjunto-semente

Examinar: circularidade entre ajuste e aferição; tamanho e intervalo de confiança do limiar;
incidência esperada por base; estado da conferência dos metadados.

## 6. Critérios

A regra vive no instrumento que prevalece, segundo a precedência do `README.md`. Todo critério
tem justificativa, e a nomenclatura é a mesma entre os instrumentos.

## Produto

Relatório com:

- o resultado primeiro;
- a tabela do que se executou — leitura ou conferência — e o resultado de cada item;
- os achados, cada um com a evidência (`arquivo:linha` ou comando), o estatuto epistêmico
  (verificado, inferido ou hipótese), a classe de conferência de `parecer-sobre-protocolo`
  (por remissão), a natureza do conserto (unilateral, decisão do pesquisador ou código) e a
  garantia proposta;
- o que não se fez e por quê;
- as frentes sugeridas, com o impacto de cada uma.

Não copiar para o relatório as classes nem as regras de `parecer-sobre-protocolo`: remeter.

## Três regras próprias

1. **Comportamento de código só se afirma depois de ler o código.** O autoteste cobre o
   comportamento que exercita, não o que o código faz fora dele. Afirmação sobre o código
   sem leitura é hipótese, e se declara como tal.
2. **A varredura de um padrão abrange o projeto inteiro**, não só o lugar onde ele foi visto
   primeiro. Padrão encontrado numa ficha se procura nas demais, nos documentos e no código.
3. **A revisão não escreve, não acessa fonte externa e não decide.** Indexação, dado
   bibliográfico e sintaxe de base ficam como inferência até a conferência pela skill própria
   (`conferir-referencia`, `busca-nas-bases`). Achado que exige decisão vira alternativa
   apresentada ao pesquisador; promovê-lo a pendência ou a change depende de pedido dele.

## Remissões

Estado do projeto e comandos: `README.md`. Classes de achado e medição do que se raciocina:
`parecer-sobre-protocolo`. Vocabulário, facetas e strings: `facetacao-e-termos-livres` e
`expressoes-de-busca`. Sementes: `conjunto-semente`. Critérios: `criterios-de-elegibilidade`.
Decisão e propagação: `registrar-decisao`. Lacunas e síntese: `sintese-e-lacunas`.
