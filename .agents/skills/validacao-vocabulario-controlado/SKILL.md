---
name: validacao-vocabulario-controlado
description: Consulta os instrumentos de controlo terminológico, registra a evidência e atribui estatuto a cada termo — descritor autorizado, termo livre ou pendência. Use ao validar vocabulário, consultar tesauro, decidir se um termo pode ser apresentado como descritor, ou tratar de TBCI, UNESCO Thesaurus, ERIC Thesaurus e Brased.
---

# Validação de vocabulário controlado

Esta skill existe porque é aqui que se inventa dado sem perceber. Um modelo de
linguagem produz com facilidade um descritor plausível e inexistente, e numa revisão
sistemática isso contamina o registro e destrói a reprodutibilidade.

## 1. A regra única, para as quatro facetas

- **Os instrumentos de cada faceta são os que o protocolo declara** na tabela da seção
  "Instrumentos para controle terminológico" (coluna `FCTs`). Não se presume instrumento
  por idioma nem por faceta: o que não está na tabela não é instrumento de linha alguma da
  planilha.
- **O que é propriedade do instrumento** — sigla, modo, caminho e idiomas que cobre — está
  na mesma linha da tabela (forma em `python3 -m rsl documentos gramatica`). Cada termo é planejado para cada instrumento
  da sua faceta que cubra o seu idioma.
- **`Caminho` é o endereço do serviço consultado**, não referência de relato. Admite o
  marcador `{idioma}`, trocado por cada idioma da coluna `Idiomas` (o endereço resolvido);
  sem ele, o mesmo endereço vale para todos os idiomas. Outro marcador entre chaves reprova
  a leitura. O código não fixa endereço de instrumento: mudar o `Caminho` muda a consulta.
- **Instrumento `Automático`** é consultado por um único cliente do serviço TemaTres
  (`services.php`), no endereço resolvido, qualquer que seja a sigla.
- **Instrumento `Manual`** gera linha com o estatuto "pendente de validação manual":
  consulta-se à mão e registra-se a evidência como em qualquer outra linha. Pendente não é
  "não encontrado".
- **Linha que deixou de valer volta a aguardar consulta.** Linha sem `decisao_ReT` de
  instrumento `Automático`, pendente de validação manual ou consultada fora do endereço
  resolvido vigente, ou termo livre não localizado sem `sugestao_similar`, é reaberta na
  reconstrução da planilha; a evidência anterior fica em `data/evidencia/` até a
  reconsulta, que a **substitui** no mesmo arquivo: quem quiser guardá-la copia antes. Com `decisao_ReT`, a linha é preservada e listada na saída: decidir se
  a decisão se mantém sobre a evidência de outro endereço.

## 2. A distinção que a regra preserva

> Um termo **pode** ser usado na estratégia de busca sem validação terminológica — a
> busca não depende de autoridade. E **não pode** ser apresentado como descritor
> autorizado sem o registro da consulta que o confirmou.

Duas consequências operacionais:

- **Retorno não vazio numa base é evidência de USO do termo na indexação. Só a página
  do tesauro é evidência de AUTORIDADE.** As duas não se substituem.
- **Retorno vazio numa sondagem por descritor não prova que o conceito não tenha
  descritor**: prova que aquela grafia não é ele. Na sondagem da ERIC, 13 de 15
  devolveram retorno e duas devolveram zero — e o zero não autoriza concluir ausência.

## 3. Nunca registrar ausência por falha de consulta

**Linha sem evidência é pendência, não resultado.** Instrumento fora do ar, consulta
que não resolveu, página que não abriu: a linha permanece pendente, com o motivo. O
contrário — anotar "não encontrado" — produz uma afirmação que ninguém fez.

Toda consulta grava a **resposta bruta**. Validação sem evidência anexada não é
validação.

## 4. O registro é o instrumento

O registro é a própria planilha `data/validacao_terminologica.csv`, com as colunas de
`[planilha] campos_validacao` do `config.toml` e uma linha por termo, idioma e instrumento. Ela é construída a partir das tabelas do protocolo e
guarda o estatuto de cada termo: `termos exportar` reconstrói a planilha e `termos importar` a
reconcilia com o protocolo, preservando as colunas `decisao_ReT`, `justificativa_ReT` e
`data_decisao` e as linhas de termo retirado. Não há JSON intermediário.

- **Rótulo com correspondência exata** no instrumento, sem distinção de caixa e de espaços,
  é proposto como descritor, seja o termo do instrumento preferido ou não preferido
  (decisão do pesquisador).
- **Sem correspondência exata**, o termo inteiro vai à consulta `suggestDetails` do serviço,
  que devolve, com identificador, os termos do instrumento (preferidos ou entradas de não
  preferido) em que **alguma palavra começa** pelo termo — não é prefixo do rótulo inteiro.
  Um **único item**, qualquer que seja a forma (preferido ou entrada não preferida) e a
  posição do termo no rótulo: a linha é **candidato por similaridade (a conferir pelo ReT)**, e
  rótulo, identificador, forma e relações são do **candidato**, não do termo
  (`observacao_tecnica` o diz). **Vários itens**: o cliente não escolhe; todos os devolvidos
  vão para `sugestao_similar`, por longa que seja a lista, a linha fica termo livre não
  localizado, e `observacao_tecnica` registra quantos vieram e a contagem declarada pelo
  serviço, que pode limitar a lista. **Nenhum item**: termo livre não localizado. O código
  não mede proximidade nem trunca o termo. O candidato é pista para o ReT, nunca descritor
  por si: a linha do termo no CT continua decidida só pela `decisao_ReT`.
- **Termo não localizado não é conceito ausente.** A consulta não acha diferença fora do
  início das palavras (`knowledge organization` na UNESCO); termo de uma palavra devolve
  dezenas de itens sem ordem de proximidade.
- **`sugestao_similar`** só se preenche em linha sem correspondência exata: cada item como
  `entrada [id]`, ou `entrada → preferido [id]` quando casou pela entrada não preferida,
  separados por `;`, ou `(o serviço não sugeriu termo)`. Ela **nunca fica vazia** em linha consultada
  sem correspondência exata, porque é o que distingue "consultada sem sugestão" de "nunca
  consultada": linha não localizada, sem decisão e com a coluna vazia volta a aguardar
  consulta em `termos exportar`.
- **`forma_no_instrumento`** registra `preferido` ou `não preferido` só quando a resposta
  do serviço o informa; quando não informa, fica vazia e `observacao_tecnica` o diz. A
  forma nunca se infere (por exemplo, de `fetchAlt` vazio).
- **`versao_instrumento`** traz título e `lastMod` declarados pela instância em
  `fetchVocabularyData`: as instâncias são cópias, e o relato declara a data da cópia. É ela o
instrumento de controlo, e **não se duplica em documento algum** — o protocolo (`docs/03`) declara a
regra e aponta para ela.

## 5. Geração e execução

Os comandos, nesta ordem:

| Comando | O que faz |
| --- | --- |
| `python3 -m rsl termos sondar` | consulta cada endereço resolvido de cada instrumento `Automático`, um por idioma: metadados do vocabulário, termos de prova naquele idioma e um termo inexistente; mostra se a resposta distingue termo não preferido e os itens de `suggestDetails` de cada termo, inclusive do inexistente. Não grava. **Obrigatório antes de tudo** |
| `python3 -m rsl termos exportar` | reconstrói a planilha a partir do protocolo, sem rede, reabrindo as linhas que deixaram de valer; não decide nada |
| `python3 -m rsl termos validar SIGLA` | consulta, no endereço resolvido, os termos ainda sem estatuto do instrumento `Automático` de sigla SIGLA; grava a evidência e propõe o estatuto. `termos validar todos --faceta 1` consulta todos os instrumentos `Automático`, restrito a uma faceta |
| `python3 -m rsl termos importar` | reconcilia a planilha com o protocolo, preservando decisões e linhas fora do protocolo |

Uma requisição por vez, com pausa; bloqueio, verificação anti-robô, limite ou resposta fora
do formato interrompem na hora, com FONTE_EXTERNA, sem nova tentativa. Retomar é decisão
do pesquisador.

A resposta bruta de cada consulta é gravada em
`data/evidencia/<instrumento>/<hash>.json`, e `arquivo_evidencia` na planilha aponta
para ela: **linha sem evidência correspondente é linha inválida**. O script recupera e
registra; não exclui, não reescreve termo e não preenche `decisao_ReT`.

Campos que decidem: `instrumento`, `consultado_em`, `status_proposto`,
`rotulo_autorizado`, `forma_no_instrumento`, `sugestao_similar`, `arquivo_evidencia`, `url_consultada`, `decisao_ReT`,
`justificativa_ReT`. A decisão final e a incorporação de termos relacionados e
específicos são do ReT com a Validação Temática — a ferramenta recupera e registra.

Estado corrente: verificar na planilha e em `python3 -m rsl projeto pendencias`;
não presumir que a validação foi executada.

## 6. Antes do primeiro uso de um instrumento

**Sondagem de sintaxe obrigatória**, com contagem e captura. Nunca supor que o
instrumento aceita o que a documentação diz — a medição já contradisse a documentação
em duas bases deste projeto.

## 7. Ao concluir

Termo que passe a descritor autorizado muda o que se pode **afirmar**, não
necessariamente o que a busca recupera. Se a forma autorizada diferir da usada e for
incorporada à string, a alteração é **de busca**: exige reexecução e novo teste de
aderência. Registrar o alcance no histórico (`data/historico.md`) — `registrar-decisao`.
