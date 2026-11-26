# Diagnóstico das perdas da busca — execução e verificação

Guia desta change: o que se implementa, o que o pesquisador faz na base, o que se verifica
em cada etapa e o que cada resultado permite decidir. O porquê está em `proposal.md`, o
comportamento exigido nas specs (`specs/anatomia-da-perda`, `specs/analise-da-sensibilidade`)
e o como em `design.md`. As tarefas rastreadas estão em `tasks.md`.

Os comandos partem da raiz do projeto e usam `PYTHONPATH=src python3 -m rsl …`. Abaixo
aparecem abreviados como `rsl …`.

## Antes de começar

| Condição | Como conferir |
|---|---|
| A change `derivacao-com-formas-da-base-e-sem-sonda` está implementada (de preferência arquivada) | `openspec list`; `rsl projeto autoteste` sai OK |
| A Scopus tem a EB4 e a EB5 registradas | `rsl aderencia medir` lista BD2/EX1 como lida e BD2/EX4 como sonda |
| A amostra de sensibilidade está classificada por inteiro | `rsl conferencia sensibilidade scopus` imprime a fração elegível (hoje, 30/53) |
| `data/sensibilidade_scopus.csv` está com `;` | o editor de planilha não pode regravá-lo com vírgula: o comando deixaria de ler a classificação |

## A. Implementação (agente)

Seguir `tasks.md` na ordem dos grupos 1 a 3. Cada grupo traz os seus testes e a sua
documentação. Verificação por grupo:

| Grupo | Verificação que encerra o grupo |
|---|---|
| 1. Restrição por DOI | `rsl documentos gramatica` mostra `[composicao] doi`; o autoteste reprova `doi` sem `{doi}`; `rsl documentos conferir` sai OK |
| 2. Anatomia da perda | o autoteste do grupo passa e **falha** com a atribuição trocada e com a conferência de subconjunto desligada; `rsl aderencia diagnosticar scopus` imprime o roteiro e não grava |
| 3. Análise da sensibilidade | o autoteste do grupo passa e **falha** com a exclusão de candidato desligada e com a simulação contando a executada; `rsl conferencia simular scopus` grava `data/candidatos_scopus.csv` |
| 4. Integração | `rsl projeto autoteste`, `rsl documentos conferir`, `rsl dados conferir` e `rsl catalogo gerar` saem OK |

Teste que nunca falha não protege nada. Cada caso novo do autoteste tem de ser visto
falhando com o defeito que o motivou, e o relato da implementação diz como isso foi feito.

## B. Anatomia da perda na Scopus (pesquisador e agente)

### B1. Roteiro (agente)

```
rsl aderencia diagnosticar scopus
```

Saída esperada:

- sementes diagnosticadas: **SE2, SE3, SE4, SE7, SE8**, com o DOI de cada uma;
- texto dos níveis **1, 2 e 3**, a submeter;
- níveis **4 e 5** lidos de BD2/EX4 (sonda) e BD2/EX1 (executada), sem submissão;
- o comprimento de cada nível e o exemplo da chamada de registro.

Nada é gravado nesta etapa.

### B2. Submissão (pesquisador, no navegador, com o acesso institucional)

Na busca avançada da Scopus, para os níveis 1, 2 e 3, um de cada vez:

1. colar o texto do nível **exatamente como o roteiro imprimiu**, a partir do terminal ou de
   arquivo, nunca reescrito;
2. anotar o retorno exibido;
3. com retorno maior que zero, exportar em RIS com todos os campos e salvar em
   `data/evidencia/anatomia/scopus/n<N>_<data-hora>.ris`;
4. anotar a data e a hora da submissão.

São 3 submissões. Diante de captcha, aviso de atividade atípica ou limite excedido, parar e
relatar; não tentar outra rota.

### B3. Registro e resultado (agente)

```
rsl aderencia diagnosticar scopus \
  --retorno 1 <K1> --exportacao 1 data/evidencia/anatomia/scopus/n1_<…>.ris \
  --retorno 2 <K2> --exportacao 2 data/evidencia/anatomia/scopus/n2_<…>.ris \
  --retorno 3 <K3> [--exportacao 3 …] \
  --data-hora <AAAA-MM-DDTHH:MM>
```

(`--exportacao N` só quando `K` > 0.)

O que o comando confere antes de gravar, e o que fazer quando reprova:

| Conferência | Reprovação | O que fazer |
|---|---|---|
| registros lidos = retorno, por nível | DADOS | reexportar o nível ou corrigir o retorno anotado |
| cada nível contém só DOIs diagnosticados | REPROVADO | a consulta submetida não é a do roteiro: submeter de novo o texto impresso |
| cada nível é subconjunto do anterior | REPROVADO | idem, ou a base mudou entre as submissões: refazer os três níveis na mesma sessão |

Saídas: `data/anatomia_scopus.csv`, com a causa por semente, e
`data/anatomia_consultas_scopus.csv`, com o texto, a origem, o retorno, o arquivo e a data
de cada nível.

### B4. Verificação do resultado (agente, à mão, uma vez)

- Para uma semente, abrir a exportação do primeiro nível em que ela aparece e confirmar o
  DOI. Depois confirmar que ele não está no nível seguinte.
- Se uma causa for `proximidade` e o aviso de datas diferentes aparecer, a causa fica **a
  conferir**: a sonda é de 2026-11-25, e a base pode ter indexado o estudo depois.

### B5. O que cada causa implica (decisão do pesquisador)

| Causa | Consequência prevista no projeto |
|---|---|
| `não indexada` | a semente sai do denominador: preencher `indexada = não` na planilha de aderência (o comando só sugere) |
| `filtro` | identificar o critério pelo ano, idioma e tipo relatados; filtro errado é emenda |
| `âncoras` | vocabulário ou campo de FCT1/FCT2 não alcança o estudo: emenda de termo |
| `proximidade` | variante "Forma ampla" do procedimento (trocar `W/5` por `AND`), com emenda |
| `faceta não âncora` | não ocorre nas 5 sementes de hoje, porque nenhuma está na EB5 |
| `presente na executada` | falha do casamento por título da aderência, não da busca: corrigir o título no arquivo de sementes ou registrar o casamento |

## C. Análise da sensibilidade na Scopus (agente)

### C1. Facetas e candidatos

```
rsl conferencia simular scopus
```

Verificar no relato:

- a amostra casa **53 de 53** registros da perda (949);
- quantos dos 30 elegíveis o casamento local reconhece em FCT3 ou FCT4. O esperado é zero ou
  quase. Elegível listado como divergência é caso de aproximação do casamento local, e não
  de vocabulário;
- quantos elegíveis não têm palavras-chave (hoje há 4 registros sem palavras-chave na
  amostra) e por isso não contribuem candidatos;
- a remissão aos limites: casamento local e amostra de 53.

Saída: `data/candidatos_scopus.csv`.

### C2. Simulação dos termos que o pesquisador escolher

```
rsl conferencia simular scopus --termo FCT3 "<termo>" [--termo FCT4 "<termo>" …]
```

Para o conjunto e para cada termo, o relato traz: elegíveis recuperados de 30 (com o
intervalo de Wilson), não elegíveis recuperados de 23 e o total da executada ampliada (133
mais o acréscimo).

Referência para comparar: adotar a EB5 como executada recupera os 30 de 30, com 1.082
registros, ou seja, 949 a mais.

### C3. Verificação do resultado (agente, à mão, uma vez)

Escolher um candidato de `candidatos_scopus.csv` e recontar o acréscimo com uma busca
textual normalizada na exportação da EB5, menos os registros da EB4. O número tem de bater.

### C4. O que a análise permite decidir (decisão do pesquisador)

- **Quais termos entram:** um candidato é indício de coocorrência. Ele só entra se
  representar prática de ensino-aprendizagem (FCT3) ou fator situacional (FCT4), se for
  validado nos instrumentos (`termos validar`) e se tiver os equivalentes em pt e es.
- **Que forma a emenda toma:** ampliar FCT3/FCT4, adotar a EB5 como executada ou combinar
  com a variante da anatomia. O critério é o custo de triagem (acréscimo) frente aos
  elegíveis recuperados.

## D. Depois da decisão

Esta change termina na informação para decidir. A emenda, a regeneração das strings e dos
procedimentos e a **reexecução da Scopus** (EB2 a EB5) ficam fora dela. Convém reexecutar
uma vez só, com a anatomia e a análise da sensibilidade já levadas à mesma emenda.

## O que esta change não faz

- não consulta a Scopus por programa: não há via de acesso programático verificada;
- não diagnostica base particionada (ERIC): o comando recusa, nomeando a base;
- não preenche a planilha de aderência nem a amostra;
- não escolhe termos, não altera strings, protocolo ou fonte, além da declaração de `doi`.
