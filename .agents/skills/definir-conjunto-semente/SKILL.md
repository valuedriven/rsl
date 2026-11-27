---
name: definir-conjunto-semente
description: "Define o conjunto-semente: compõe, confere e mantém o conjunto de estudos que afere o recall das expressões de busca no teste de aderência (`testar-aderencia-das-expressoes`), e o distingue dos estudos da leitura exploratória. Use ao montar ou alterar o conjunto-semente, ao conferir as suas referências, ao fazer o ensaio seco contra as facetas e ao tratar de distribuição por base ou acervo pessoal."
---

# Conjunto-semente

Instrumento de **aferição de recall**: um conjunto de estudos que a busca tem
obrigação de recuperar. Se não os recupera, a busca está mal desenhada — e é isso, e
só isso, que o conjunto-semente mede.

## 1. Composto antes da busca, por caminho independente dela

A exigência que dá sentido ao instrumento. Semente colhida da própria busca mede a
busca contra si mesma e confirma o que já se esperava encontrar.

As sementes são indicadas pelos pesquisadores, e é esse o caminho independente: a origem
não se registra semente a semente.

## 2. O que NÃO é o conjunto-semente

**Não é a leitura exploratória.** O passo "Verificar estudos iniciais sobre o
tema" (M2/E1) do RS Banyan pede os estudos
inicialmente consultados acerca do tema — a leitura que precede a delimitação. São
outro conjunto, de outra função, em `docs/02`, seção Estudos inicialmente consultados:

| | Conjunto-semente | Leitura exploratória |
| --- | --- | --- |
| Função | aferir recall | situar o tema, fixar fronteiras |
| Regras (ajuste, fórmula de recuperação) | protocolo, seção Conjunto-semente | — |
| Vive no | arquivo de `[documentos] sementes` do `config.toml` | `docs/02`, Estudos inicialmente consultados |
| Recorte temporal | obrigatório | **dispensado** — leitura de fundamentação pode ser anterior |

Confundi-los já aconteceu: o conjunto-semente ocupou esse passo e a leitura
exploratória desapareceu do instrumento.

Também **não é amostra** nem portfólio, e não se usa para estimar nada.

## 3. Composição, em duas etapas

A primeira indica candidatos; a segunda confere cada um em fonte e decide. O estado
de conferência de cada referência fica registrado — ver `conferir-referencia`.

Três exigências de qualificação:

- **todos primários** — revisão sistemática não serve de semente;
- **todos dentro do recorte temporal**, para que o teste de aderência meça o desenho
  da busca e não os critérios de elegibilidade;
- **todos com conferência declarada pelo pesquisador** (`verificacao = true`) dos dados
  bibliográficos do item no Zotero.

## 4. Registrar a semente: dados no Zotero, controle no arquivo de sementes

Os **dados** de cada semente — autoria, ano, título, veículo, volume, número, páginas,
resumo e palavras-chave — ficam no item da coleção `sementes` da biblioteca de grupo do
Zotero (`[zotero]` do `config.toml`). O **controle e o juízo** ficam numa tabela
`[[sementes]]` do arquivo de `[documentos] sementes`. O **DOI** liga os dois. Os comandos não
consultam o Zotero: leem a cópia da coleção (`[dados] zotero`), gravada por
`python3 -m rsl sementes copiar`.

Semente nova, em ordem:

1. **no Zotero**, acrescentar o item pela varinha "Adicionar item por identificador", com o
   DOI, na coleção `sementes`, e conferir os dados contra a fonte — ver
   `conferir-referencia`. Item criado à mão só com o DOI fica vazio, e a leitura reprova;
2. sincronizar o Zotero e rodar `sementes copiar`;
3. rodar `sementes metadados` (OpenAlex) e, para a semente sem resumo,
   `sementes metadados --fonte crossref`; sem resumo em fonte nenhuma, o pesquisador o
   preenche no Zotero, se o estudo o tiver;
4. rodar `sementes completar` (plano) e, revisado, `sementes completar --gravar`;
5. **no arquivo de sementes**, a tabela da semente, no esquema fechado de
   `python3 -m rsl documentos gramatica` (campo desconhecido reprova):

- **`doi`**, obrigatório, só `10.x/…`, sem `DOI:` nem URL, sem repetição;
- **`referencia_curta`**, obrigatória: `<sobrenome do primeiro autor> <ano>: <início do
  título>`. Serve para ler o arquivo e é conferida contra o item: `documentos conferir`
  reprova a que não confere e mostra a forma sugerida;
- **`bases` é indexação, não recuperação**: as siglas das bases que indexam a semente, da
  tabela de bases do protocolo. Semente que a base não indexa sai do denominador daquela
  base. O que a busca recuperou é resultado, calculado das exportações por
  `aderencia medir` (§7), e não se transcreve;
- **`alinhamento_facetas` é juízo do pesquisador**: para cada `FCTn` que o estudo trata, uma
  frase curta com o motivo, julgada a partir do **resumo ou do texto completo** e **nunca do
  ensaio seco** (§6). A frase descreve o conceito e **não repete o termo** que o ensaio
  procura: o valor do campo está em contrastar as duas coisas — semente alinhada a FCT3 sem
  termo de FCT3 no título, nas palavras-chave ou no resumo indica lacuna de vocabulário —,
  e repetir o termo tornaria o contraste circular. O código não confere isso: é juízo.
  Ausente, vira pendência; semente sem nenhuma faceta âncora também é relatada, enquanto o
  pesquisador não decide a regra;
- **`verificacao`**, booleano: `true` quando o pesquisador declara conferidos os dados do
  item no Zotero, e a declaração basta; `false` ou ausente é conferência pendente, e texto
  reprova a leitura;
- **`nota`**, opcional: só informação relativa à revisão sistemática — limitação da semente
  para o teste (sem resumo publicado, indexação de fonte secundária, natureza do estudo) ou
  pendência específica dela. Não guarda dado bibliográfico, que fica no Zotero (o que o tipo
  do item não comporta vai ao campo *Extra*, como `publisher: …`), nem o conteúdo do estudo,
  que vai ao alinhamento, nem registro de conferência ou de decisão, que vão a `verificacao`
  e ao histórico.

A autoria com quatro ou mais autores se exibe como "primeiro autor et al.".

O `id` é `SEn`, em **sequência a partir de SE1, sem lacuna**: lacuna ou `id` fora de
sequência reprova a leitura.

### Retirar uma semente: sai de tudo e renumera as seguintes

Semente retirada não fica guardada em lugar nenhum. A retirada tem quatro passos, no mesmo
trabalho:

1. **tirar a tabela `[[sementes]]` e renumerar as seguintes** — retirar SE3 faz SE4 a SE10
   passarem a SE3 a SE9. Substituir uma semente no mesmo `id` não renumera;
2. **evidência bruta** em `data/evidencia/`: remover os arquivos `SEn_…` da semente
   retirada e renomear os das renumeradas para o `id` novo. `python3 -m rsl
   dados conferir` reprova evidência de `id` inexistente, mas **não** detecta arquivo de
   renumerada esquecido com um `id` que ainda existe: esse fica atribuído à semente
   errada sem que nada reprove, e a renomeação tem de ser conferida a olho. A resposta da
   OpenAlex (`openalex/`) é nomeada pelo DOI: a das renumeradas não muda, e a da retirada
   se remove — `dados conferir` reprova a que ficar;
3. **`data/pendencias.json`**: atualizar as menções aos `id` renumerados;
4. **`data/historico.md`**: registrar a retirada — data, `id`, referência, motivo — e a
   **correspondência entre `id` antigo e novo**. As entradas anteriores não se reescrevem:
   citam o `id` vigente na data, e a correspondência permite lê-las. Sem esse registro, o
   recall de antes e o de depois não se comparam, porque o denominador mudou. Nenhuma
   verificação automática o exige: a semente retirada não deixa marca para conferir.

Tirar o item da coleção do Zotero é pedido à parte, depois da retirada do arquivo:
`python3 -m rsl sementes completar --retirar <DOI>` (plano) e, autorizado, com `--gravar`.
O item sai só da coleção e continua na biblioteca.

## 5. Incidências por base contra estudos distintos

O erro de leitura mais fácil deste instrumento, e o parecer externo tropeçou nele.

A soma das quantidades por base é de **incidências**: um mesmo estudo indexado em
duas bases conta duas vezes. As incidências e os estudos distintos calculam-se do campo
`bases` do arquivo de sementes, e não se transcrevem.

**Declarar que são incidências, e publicar o mapa por estudo.** Sem o mapa, a
distribuição não se confere.

## 6. Ensaio seco contra as facetas

Antes de executar, aplicar as facetas a cada semente e ver quais seriam acionadas.
É diagnóstico de vocabulário, não de busca.

**Ensaio silencioso não é ensaio reprovado.** Um acréscimo conceitual pode não ser
acionado por nenhuma das sementes — o ensaio nada diz sobre ele, e tratar o silêncio
como aprovação é erro.

```
python3 -m rsl aderencia ensaiar
```

O comando lê as sementes do arquivo de sementes e o título, as palavras-chave e o resumo de
cada uma da cópia da coleção do Zotero, e **imprime no terminal**, por semente e faceta, os
termos encontrados e o campo onde apareceram, quantas sementes satisfazem a composição da
executada só pelo título e pelos três campos, o campo ausente na cópia e a faceta alinhada
sem termo. Não grava arquivo. As palavras-chave vêm da OpenAlex, e não da base: é ensaio,
não medição.

## 7. O procedimento: indexação e recuperação

Duas etapas, e a ordem importa:

- **Etapa 1 — indexação.** Buscar o título entre aspas, sem recorte temporal e sem as
  expressões da revisão. Semente que a base não indexa **sai do denominador daquela
  base** e se registra no campo `bases` do arquivo de sementes, como cobertura, não como
  falha da busca.
- **Etapa 2 — recuperação.** `python3 -m rsl aderencia medir` procura a semente na
  exportação da executada, pelo DOI e pelo título, **sem reexecutar a busca**, e diz por
  qual dos dois a encontrou. Prefixo de título sem o DOI é indício e se confere à mão.

Semente com conferência pendente — `verificacao = false` ou ausente — aparece em
`projeto pendencias`. O teste pode ser executado; o que falta é registro, não dado de busca,
e a pendência se reporta em vez de se esconder.

**Conjunto único.** Todo o conjunto-semente é de validação: não há sementes de
desenvolvimento relatadas à parte, e a aderência que decide a passagem é a do conjunto.

## 8. Limiar e consequência

O teste de aderência exige **80%** sobre a união das bases, contando **todas as sementes**
do conjunto. Abaixo disso, revisão obrigatória do controlo terminológico antes de
prosseguir, com emenda ao protocolo. O relato traz o intervalo de Wilson a 95%: com
conjunto pequeno, o intervalo mostra a imprecisão em vez de deixar ler 80% como estimativa.
Ver `testar-aderencia-das-expressoes`, que é onde a medição acontece.

Acrescentar ou retirar semente altera o denominador do teste: é emenda, e exige
reaferição. Registrar — `registrar-decisao`.

## 9. Sementes no procedimento de busca

O gerador lista, no procedimento de busca de cada base, as sementes que o arquivo de sementes
atribui àquela base, com o DOI de lá; a fonte do procedimento só acrescenta a observação por
semente (`[[sementes]]`) e, quando preciso, `notas_sementes.md`. O **estado** da aderência não
entra: está no registro de execução.
