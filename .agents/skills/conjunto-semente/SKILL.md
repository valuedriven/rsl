---
name: conjunto-semente
description: Compõe, confere e mantém o conjunto-semente que afere o recall das expressões de busca, e o distingue dos estudos da leitura exploratória. Use ao montar ou alterar o conjunto-semente, ao conferir as suas referências, ao fazer o ensaio seco contra as facetas, e ao tratar de distribuição por base ou acervo pessoal.
---

# Conjunto-semente

Instrumento de **aferição de recall**: um conjunto de estudos que a busca tem
obrigação de recuperar. Se não os recupera, a busca está mal desenhada — e é isso, e
só isso, que o conjunto-semente mede.

## 1. Composto antes da busca, por caminho independente dela

A exigência que dá sentido ao instrumento. Semente colhida da própria busca mede a
busca contra si mesma e confirma o que já se esperava encontrar.

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
- **todos conferidos em fonte**, com autor, título, veículo, ano e DOI.

## 4. Registrar a semente no arquivo de sementes

Cada semente é uma tabela `[[sementes]]` do arquivo apontado por `[documentos] sementes`
do `config.toml`. É o **único lugar** de dado de semente: não há outro arquivo a
reconciliar. O esquema é fechado e está em `python3 -m rsl documentos gramatica`; campo desconhecido
reprova, para que erro de digitação não passe como campo ignorado.

- **Dados bibliográficos, campo a campo**: `autores` (lista), `ano` (inteiro), `titulo`,
  `veiculo`, e, quando a fonte os traz, `volume`, `numero`, `paginas` e `doi` (só
  `10.x/…`, sem `DOI:` nem URL). Transcrever da fonte conferida, **nunca de memória** —
  ver `conferir-referencia`. O que a fonte não traz fica vazio. DOI ausente não reprova:
  `python3 -m rsl projeto pendencias` o relata, porque o DOI é a chave de conferência.
- **`observacoes`**: o que a referência traz e não cabe em outro campo (editores, evento,
  local, editora), transcrito como está. Nada da referência se perde.
- **`bases` é indexação, não recuperação**: as siglas das bases que indexam a semente, da
  tabela de bases do protocolo. Semente que a base não indexa sai do denominador daquela
  base. O que a busca recuperou é resultado e fica na planilha (§7).
- **`facetas` é juízo do pesquisador**: as `FCTn` que o estudo trata, julgadas a partir do
  **resumo ou do texto completo**, **nunca do ensaio seco** (§6). O valor do campo está em
  contrastar as duas coisas — semente declarada em FCT2 sem termo de FCT2 no título indica
  lacuna de vocabulário —, e copiar o ensaio tornaria o contraste circular. Vazia, vira
  pendência; semente de validação sem nenhuma faceta âncora também é relatada, enquanto o
  pesquisador não decide a regra.
- **`papel`**: `desenvolvimento` ou `validação` (§7).
- **Conferência**: `verificacao`, `tipo`, `alinhamento`, `nota`, `veiculo_conferido`,
  `eric`. `tipo` e `alinhamento` vazios são relatados como pendência.

O `id` é `SEn`, em **sequência a partir de SE1, sem lacuna**: lacuna ou `id` fora de
sequência reprova a leitura.

### Retirar uma semente: sai de tudo e renumera as seguintes

Semente retirada não fica guardada em lugar nenhum. A retirada tem cinco passos, no mesmo
trabalho:

1. **tirar a tabela `[[sementes]]` e renumerar as seguintes** — retirar SE3 faz SE4 a SE10
   passarem a SE3 a SE9;
2. **evidência bruta** em `data/evidencia/`: remover os arquivos `SEn_…` da semente
   retirada e renomear os das renumeradas para o `id` novo. `python3 -m rsl
   dados conferir` reprova evidência de `id` inexistente, mas **não** detecta arquivo de
   renumerada esquecido com um `id` que ainda existe: esse fica atribuído à semente
   errada sem que nada reprove, e a renomeação tem de ser conferida a olho;
3. **planilha de aderência** (`semente_aderencia.csv`): transferir à mão o preenchimento
   das renumeradas e esvaziar o da retirada — apagar as linhas da semente retirada e
   trocar o `id` das linhas de cada renumerada pelo `id` novo, sem mexer no título, que
   acompanha a linha. `python3 -m rsl aderencia planilhar` casa as linhas por `id`, `base` e
   título, e **recusa a regravação** (REPROVADO, sem gravar) enquanto houver preenchimento
   em linha sem par ou com título divergente, nomeando cada `id` × base × coluna;
4. **`data/pendencias.json`**: atualizar as menções aos `id` renumerados;
5. **`data/historico.md`**: registrar a retirada — data, `id`, referência, motivo — e a
   **correspondência entre `id` antigo e novo**. As entradas anteriores não se reescrevem:
   citam o `id` vigente na data, e a correspondência permite lê-las. Sem esse registro, o
   recall de antes e o de depois não se comparam, porque o denominador mudou. Nenhuma
   verificação automática o exige: a semente retirada não deixa marca para conferir.

Feito o passo 3, a regravação da planilha deixa de trazer a semente retirada.

## 5. Incidências por base contra estudos distintos

O erro de leitura mais fácil deste instrumento, e o parecer externo tropeçou nele.

A soma das quantidades por base é de **incidências**: um mesmo estudo indexado em
duas bases conta duas vezes. Neste conjunto são 15 incidências para 10 estudos
distintos — 4 em mais de uma base e 6 numa só.

**Declarar que são incidências, e publicar o mapa por estudo.** Sem o mapa, a
distribuição não se confere.

## 6. Ensaio seco contra as facetas

Antes de executar, aplicar as facetas a cada semente e ver quais seriam acionadas.
É diagnóstico de vocabulário, não de busca.

**Ensaio silencioso não é ensaio reprovado.** Um acréscimo conceitual pode não ser
acionado por nenhuma das sementes — o ensaio nada diz sobre ele, e tratar o silêncio
como aprovação é erro.

```
python3 -m rsl aderencia planilhar
```

O comando lê as sementes do arquivo de sementes (`[documentos] sementes`) — dados
bibliográficos, bases, papel e conferência —, gera a planilha
`data/semente_aderencia.csv` e **imprime no terminal** a composição, o estado de
conferência e o ensaio seco — quantas sementes o título entrega às facetas e quantas
satisfazem as duas âncoras e uma faceta temática. Não grava guia em arquivo: o
instrumento é a planilha.

## 7. O instrumento: a planilha e o procedimento

`semente_aderencia.csv` tem uma linha por semente e por base — com 10 sementes e 4
bases, 40 linhas. Preencher **durante** a execução, não depois: as colunas de registro
são a evidência do teste.

| Coluna | O que registrar |
| --- | --- |
| `id` | identificador da semente (SEn), conforme o arquivo de sementes |
| `autores_ano` | autoria abreviada e ano |
| `titulo` | título, como consta na referência do arquivo de sementes |
| `tipo` | primário ou secundário — preencher no arquivo de sementes |
| `verificacao` | estado de conferência da referência — preencher no arquivo de sementes |
| `papel` | `desenvolvimento` ou `validação` — do arquivo de sementes |
| `base` | WoS, Scopus, ERIC ou BRAPCI |
| `esperada_na_base` | sim se o campo `bases` da semente indica esta base |
| `indexada` | etapa 1: sim ou não, por busca de título. **obrigatório** |
| `data_etapa1` | data da busca de título |
| `recuperada` | etapa 2: sim ou não, por busca na exportação de EB4 |
| `como_localizada` | DOI, título ou não localizada |
| `data_etapa2` | data da conferência na exportação |
| `observacao` | o que explica o não: termo ausente, campo não indexado, recorte |

O preenchimento segue duas etapas, e a ordem importa:

- **Etapa 1 — indexação.** Buscar o título entre aspas, sem recorte temporal e sem as
  expressões da revisão. Semente que a base não indexa **sai do denominador daquela
  base** e se registra como cobertura, não como falha da busca.
- **Etapa 2 — recuperação.** Procurar a semente na exportação de EB4, por DOI e depois
  por título, **sem reexecutar a busca**.

> `indexada` em branco impede o cálculo: sem ela não há denominador. `recuperada` só se
> preenche onde `indexada` = sim.

Semente com conferência pendente — `verificacao`, `tipo` ou `alinhamento` em branco, marcado `A CONFERIR` ou `PENDÊNCIA` — sai com a coluna em branco. O instrumento
pode ser executado; o que falta é registro, não dado de busca, e a pendência se reporta
em vez de se esconder.

**Papel.** Só as sementes de **validação** decidem a passagem. As de **desenvolvimento**
orientaram a inclusão, a manutenção ou a retirada de um termo e são relatadas à parte; elas
não compensam a validação. A distinção vive no campo `papel` do arquivo de sementes e é
exigida na leitura: papel ausente, fora do domínio ou conjunto de validação vazio reprova.

## 8. Limiar e consequência

O teste de aderência exige **80%** sobre a união das bases, contando **só as sementes de
validação**. Abaixo disso, revisão obrigatória do controlo terminológico antes de
prosseguir, com emenda ao protocolo. O relato traz o intervalo de Wilson a 95%: com
conjunto pequeno, o intervalo mostra a imprecisão em vez de deixar ler 80% como estimativa.
Ver `teste-de-aderencia`, que é onde a medição acontece.

Acrescentar ou retirar semente altera o denominador do teste: é emenda, e exige
reaferição. Registrar — `registrar-decisao`.
