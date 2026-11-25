# Strings de busca — ERIC

<!-- Gerado por `python3 -m rsl procedimentos gerar eric --gravar` a partir de `docs/procedimentos/eric`, do protocolo e do arquivo de sementes. Não editar: a edição à mão reprova em `documentos conferir`. -->

## 1. Estado de verificação da sintaxe

| Elemento | Categoria | Situação | Fonte | Sondagem |
| :--- | :--- | :--- | :--- | :--- |
| Nomes de campo (`title`, `abstract`, `descriptor`, `educationlevel`, `language`, `publicationtype`, `pubyear`, `author`, `source`, `institution`, `sponsor`, `audience`, `assessment`, `law`, `location`, `e_yearadded`, `iesgrantcontractnum`) e filtros (`pubyearmin`, `pubyearmax`) | campos | Verificado em fonte oficial | painel *Advanced Search Tips* de `eric.ed.gov/?advanced` | — |
| Campos de casamento exato (`descriptorx`, `sourcex`, `locationx`, `lawx`, `assessmentx`) e prefixo `+` | campos | Verificado em fonte oficial; comportamento **não medido** | painel *Advanced Search Tips* de `eric.ed.gov/?advanced` | — |
| Prefixo de campo restringe de fato | campos | **Não verificado** | — | SD1 |
| Parênteses para agrupamento | agrupamento | **Não verificado** | — | SD2 |
| Condição externa a um grupo | agrupamento | **Não verificado** | — | SD3 |
| Campos diferentes num mesmo grupo | agrupamento | **Não verificado** | — | SD5 |
| `pubyearmin`/`pubyearmax` junto a um grupo | filtros | **Não verificado** | — | SD6 |
| `pubyearmin`/`pubyearmax` ligados por `AND` em consulta sem parênteses | filtros | **Não verificado** | — | SD7 |
| Truncamento com `*` | truncamento | **Não verificado**; a skill `executar-sondagens-de-sintaxe` afirma que a ERIC não trunca; contradição registrada em `data/pendencias.json` | — | SD8 |
| Mínimo de três letras antes do `*` | truncamento | **Não verificado**; afirmado sem fonte na skill `auditoria-das-strings` até 2026-11-23; conferir também na documentação oficial | — | SD8 |
| Derivação automática de radicais desativada, com casamento exato sem aspas | lematizacao | **Não verificado**; afirmado sem fonte na skill `auditoria-das-strings` até 2026-11-23; conferir também na documentação oficial | — | SD10 |
| API pública de exportação | exportacao | **Não verificado** | — | sem sondagem: verificação documental, não sondagem: conferir na documentação oficial; afirmado sem fonte na skill `auditoria-das-strings` até 2026-11-23 |
| Lematização | lematizacao | **Não verificado** | — | SD10 |
| Aspas como frase | frase | **Não verificado** | — | SD9 |
| Campo `descriptor` | vocabulario_controlado | **Não verificado** | — | SD11 |
| Comprimento máximo da consulta | limite_consulta | **Não verificado**; 1.400 é regra de bolso, declarada como teto de caracteres na declaração de cobertura até medir | — | SD12 |
| Negação com prefixo `-` | operadores | Verificado em fonte oficial; não medida | painel *Advanced Search Tips* de `eric.ed.gov/?advanced` | — |
| Hífen como separador de palavras (`ontology-driven`, `e-learning`) | frase | **Não verificado** | — | SD13 |
| Teto de retorno exibido | limite_retorno | **Não verificado** | — | SD14 |
| Teto de exportação por lote | limite_exportacao | **Não verificado** | — | SD15 |
| Controles `Include Synonyms` e `Include Dead terms` | vocabulario_controlado | **Não verificado** | — | sem sondagem: não localizados na interface; nenhuma expressão depende deles |
| Operador de proximidade | proximidade | **Não verificado** | — | sem sondagem: verificação documental antes de sondagem: o painel *Advanced Search Tips* não foi conferido quanto a proximidade; nenhuma expressão depende dele |
| Idioma do título e do resumo indexados | idioma_indexacao | **Não verificado** | — | SD16 |

Nomes de campo verificados no painel *Advanced Search Tips* de `eric.ed.gov/?advanced`; comportamento **não verificado** — medir pelas sondagens abaixo e registrar cada uma.

### Sondagens a executar

Uma consulta por vez, sem nova tentativa automática; parar diante de captcha, aviso de atividade atípica ou bloqueio, e registrar.

#### SD1 — saber se `title:` restringe a busca ao título, em vez de ser ignorado

**Elementos verificados:** Prefixo de campo restringe de fato (Não verificado).

**Pré-requisitos.**

- busca de `eric.ed.gov` aberta no navegador do pesquisador, sem filtro de data e sem `Peer reviewed only`

**Consulta 1 — controle**, em caixa de busca.

```
ontology
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o prefixo `title:`.

```
title:ontology
```

**Passos.**

1. submeter o controle e anotar o retorno exibido
2. submeter o teste e anotar o retorno exibido
3. abrir três registros do teste e conferir se `ontology` está no título

**Observar.**

- retorno exibido de cada consulta
- presença do termo no título dos registros abertos

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < teste < controle, e os três registros abertos têm `ontology` no título | o prefixo de campo restringe ao título | Verificado por medição |
| 2 | teste = controle, teste = 0, ou registro aberto sem o termo no título | não se distingue se o prefixo restringe; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD2 — saber se um grupo entre parênteses com `OR` é aceito e alarga o retorno

**Elementos verificados:** Parênteses para agrupamento (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com o prefixo de campo verificado

**Consulta 1 — controle**, em caixa de busca.

```
title:ontology AND abstract:education
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o grupo entre parênteses com `OR`.

```
(title:ontology OR title:ontologies) AND abstract:education
```

**Passos.**

1. submeter o controle e anotar o retorno
2. submeter o teste e anotar o retorno

**Observar.**

- retorno exibido
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste ≥ controle > 0 | os parênteses agrupam | Verificado por medição |
| 2 | teste = 0 sem mensagem, teste < controle, ou mensagem de erro | o agrupamento não se confirma; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD3 — saber se um grupo com `OR` sem condição fora dele devolve zero

**Elementos verificados:** Condição externa a um grupo (Não verificado); grupo entre parênteses com `OR` precisa de condição fora dele (Não verificado).
**Depende de:** SD2.

**Pré-requisitos.**

- SD2 registrada com os parênteses verificados

**Consulta 1 — controle**, em caixa de busca.

```
(title:ontology OR title:ontologies) AND abstract:education
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: sem condição fora do grupo.

```
(title:ontology OR title:ontologies)
```

**Passos.**

1. submeter o controle e anotar o retorno
2. submeter o teste e anotar o retorno e a mensagem exibida

**Observar.**

- retorno exibido
- mensagem de erro ou de aviso, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | controle > 0 e teste = 0 sem mensagem | o grupo com `OR` precisa de condição fora dele | Verificado por medição |
| 2 | teste > 0, ou mensagem de erro | a regra não se confirma; levar ao pesquisador antes de mudar a composição | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta, o retorno e a mensagem visíveis

#### SD4 — saber que formas de condição externa satisfazem o grupo

**Elementos verificados:** a condição externa pode ser de campo, de texto livre ou outro grupo, antes ou depois (Não verificado).
**Depende de:** SD3.

**Pré-requisitos.**

- SD3 registrada com a regra confirmada

**Consulta 1 — controle**, em caixa de busca.

```
(title:ontology OR title:ontologies) AND abstract:education
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: condição de campo antes do grupo.

```
abstract:education AND (title:ontology OR title:ontologies)
```

**Consulta 3 — teste**, em caixa de busca. Muda em relação ao controle: condição de texto livre.

```
(title:ontology OR title:ontologies) AND education
```

**Consulta 4 — teste**, em caixa de busca. Muda em relação ao controle: condição que é outro grupo.

```
(title:ontology OR title:ontologies) AND (abstract:education OR abstract:learning)
```

**Passos.**

1. submeter o controle e anotar o retorno
2. submeter cada teste, um por vez, e anotar o retorno

**Observar.**

- retorno exibido de cada consulta

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | os três testes > 0, e o primeiro teste = controle | a condição externa pode ser de campo, de texto livre ou outro grupo, antes ou depois | Verificado por medição |
| 2 | algum teste = 0, ou o primeiro teste ≠ controle | alguma forma de condição externa não funciona; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD5 — saber se `title:` e `abstract:` na mesma disjunção devolvem zero

**Elementos verificados:** Campos diferentes num mesmo grupo (Não verificado); um grupo não mistura campos: `title:` e `abstract:` na mesma disjunção devolvem zero (Não verificado).
**Depende de:** SD3.

**Pré-requisitos.**

- SD3 registrada com a regra confirmada

**Consulta 1 — controle**, em caixa de busca.

```
(title:ontology OR title:ontologies) AND abstract:education
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: dois campos no mesmo grupo.

```
(title:ontology OR abstract:ontologies) AND abstract:education
```

**Passos.**

1. submeter o controle e anotar o retorno
2. submeter o teste e anotar o retorno e a mensagem exibida

**Observar.**

- retorno exibido
- mensagem de erro ou de aviso, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | controle > 0 e teste = 0 sem mensagem | um grupo não mistura campos | Verificado por medição |
| 2 | teste > 0, ou mensagem de erro | a regra não se confirma; levar ao pesquisador antes de mudar as consultas de campo | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta, o retorno e a mensagem visíveis

#### SD6 — saber se `pubyearmin`/`pubyearmax` ao lado de um grupo devolvem zero

**Elementos verificados:** `pubyearmin`/`pubyearmax` junto a um grupo (Não verificado); `pubyearmin`/`pubyearmax` não convivem com grupo: o recorte vem do filtro da página (Não verificado).
**Depende de:** SD3.

**Pré-requisitos.**

- SD3 registrada com a regra confirmada

**Consulta 1 — controle**, em caixa de busca.

```
(title:ontology OR title:ontologies) AND abstract:education
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o filtro de ano na consulta.

```
(title:ontology OR title:ontologies) AND abstract:education AND pubyearmin:2017 AND pubyearmax:2026
```

**Passos.**

1. submeter o controle e anotar o retorno
2. submeter o teste e anotar o retorno e a mensagem exibida

**Observar.**

- retorno exibido
- mensagem de erro ou de aviso, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | controle > 0 e teste = 0 sem mensagem | o filtro de ano não convive com grupo; o recorte vem do filtro da página | Verificado por medição |
| 2 | 0 < teste ≤ controle, ou mensagem de erro | a regra não se confirma; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta, o retorno e a mensagem visíveis

#### SD7 — saber se o filtro de ano na consulta sem parênteses recorta como o filtro de data da página

**Elementos verificados:** `pubyearmin`/`pubyearmax` ligados por `AND` em consulta sem parênteses (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com o prefixo de campo verificado

**Consulta 1 — controle**, em caixa de busca, com o filtro de data da página de 2017 a 2026.

```
title:ontology AND abstract:education
```

**Consulta 2 — teste**, em caixa de busca, sem filtro da página. Muda em relação ao controle: o recorte na consulta em vez do filtro da página.

```
title:ontology AND abstract:education AND pubyearmin:2017 AND pubyearmax:2026
```

**Passos.**

1. submeter o controle, aplicar o filtro de data da página de 2017 a 2026 e anotar o retorno e o rótulo exato do filtro
2. retirar o filtro da página, submeter o teste e anotar o retorno

**Observar.**

- retorno exibido de cada consulta
- rótulo exato do filtro de data da página

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste = controle > 0 | o filtro de ano na consulta sem parênteses recorta como o filtro da página | Verificado por medição |
| 2 | teste ≠ controle, ou teste = 0 | o filtro de ano na consulta não equivale ao da página; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta, o filtro e o retorno visíveis

#### SD8 — saber se o `*` trunca e com quantas letras antes dele

**Elementos verificados:** Truncamento com `*` (Não verificado); Mínimo de três letras antes do `*` (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com o prefixo de campo verificado

**Consulta 1 — controle**, em caixa de busca.

```
title:ontology
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o curinga depois de oito letras.

```
title:ontolog*
```

**Consulta 3 — teste**, em caixa de busca. Muda em relação ao controle: o curinga depois de três letras.

```
title:ont*
```

**Consulta 4 — teste**, em caixa de busca. Muda em relação ao controle: o curinga depois de duas letras.

```
title:on*
```

**Passos.**

1. submeter o controle e anotar o retorno
2. submeter cada teste, um por vez, e anotar o retorno e a mensagem exibida
3. abrir três registros do primeiro teste e conferir a forma do termo no título

**Observar.**

- retorno exibido de cada consulta
- mensagem de erro ou de aviso, se houver
- formas do termo nos títulos dos registros abertos

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | primeiro teste > controle, com formas como `ontologies` e `ontological` nos registros; segundo teste > 0; terceiro teste = 0 ou mensagem | o `*` trunca e exige ao menos três letras antes dele | Verificado por medição |
| 2 | primeiro teste = 0 sem mensagem | o `*` não trunca no campo título | Verificado por medição |
| 3 | qualquer outra combinação, ou primeiro teste = controle | não se distingue o efeito do `*`; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta, o retorno e a mensagem visíveis

#### SD9 — saber se as aspas exigem a sequência exata das palavras

**Elementos verificados:** Aspas como frase (Não verificado); sem truncamento; expressão composta sempre entre aspas (Não verificado).
**Depende de:** SD1, SD8.

**Pré-requisitos.**

- SD1 registrada com o prefixo de campo verificado
- SD8 registrada, porque a regra de montagem também fala do truncamento

**Consulta 1 — controle**, em caixa de busca.

```
abstract:knowledge AND abstract:organization
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: as palavras entre aspas.

```
abstract:"knowledge organization"
```

**Passos.**

1. submeter o controle e anotar o retorno
2. submeter o teste e anotar o retorno
3. abrir três registros do controle que não estejam no teste e conferir se o resumo traz as duas palavras separadas

**Observar.**

- retorno exibido de cada consulta
- posição das palavras nos resumos abertos

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | 0 < teste < controle, e os registros só do controle trazem as palavras separadas | as aspas exigem a sequência exata; a expressão composta vai entre aspas | Verificado por medição |
| 2 | teste = controle, ou teste = 0 | não se distingue o efeito das aspas; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD10 — saber se a ERIC casa a forma singular com a plural, ou uma palavra com as derivadas, sem que a consulta as traga

**Elementos verificados:** Lematização (Não verificado); Derivação automática de radicais desativada, com casamento exato sem aspas (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com o prefixo de campo verificado

**Consulta 1 — controle**, em caixa de busca.

```
title:ontology
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o plural no lugar do singular.

```
title:ontologies
```

**Consulta 3 — teste**, em caixa de busca. Muda em relação ao controle: uma forma derivada no lugar do substantivo.

```
title:ontological
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno
2. abrir três registros do primeiro teste e conferir se o título traz `ontologies` e não `ontology`

**Observar.**

- retorno exibido de cada consulta
- forma do termo nos títulos dos registros abertos

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | os três retornos diferem, e os registros do primeiro teste trazem só `ontologies` no título | sem lematização e sem derivação automática em inglês: o plural explícito é necessário | Verificado por medição |
| 2 | teste = controle, ou registros do primeiro teste com `ontology` no título sem `ontologies` | pode haver lematização; levar ao pesquisador antes de declarar `pela lematização` | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD11 — saber se `descriptor:` busca no descritor do tesauro ERIC e se difere de `descriptorx:`

**Elementos verificados:** Campo `descriptor` (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com o prefixo de campo verificado

**Consulta 1 — controle**, em caixa de busca.

```
abstract:thesauri
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o campo `descriptor` no lugar do resumo.

```
descriptor:Thesauri
```

**Consulta 3 — teste**, em caixa de busca. Muda em relação ao controle: o campo de casamento exato.

```
descriptorx:Thesauri
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno
2. abrir três registros do primeiro teste e conferir se `Thesauri` está entre os descritores

**Observar.**

- retorno exibido de cada consulta
- descritores dos registros abertos

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | primeiro teste > 0 e os registros abertos têm `Thesauri` entre os descritores | o campo `descriptor` busca no descritor | Verificado por medição |
| 2 | primeiro teste = 0, ou registros sem o descritor | não se confirma o campo `descriptor`; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD12 — saber se a consulta mais longa do procedimento é aceita inteira

**Elementos verificados:** Comprimento máximo da consulta (Não verificado).
**Depende de:** SD2.

**Pré-requisitos.**

- SD2 registrada com os parênteses verificados
- o procedimento gerado, para copiar as consultas

**Consulta 1 — controle**, em caixa de busca.

```
(title:ontology OR title:ontologies) AND abstract:education
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: o comprimento, perto do teto declarado.

```
a consulta mais longa de EB4 no procedimento gerado
```

**Passos.**

1. copiar do procedimento a consulta mais longa de EB4 e anotar o número de caracteres
2. submeter o controle e anotar o retorno e o texto que a caixa de busca mostra depois da submissão
3. submeter o teste e anotar o mesmo

**Observar.**

- retorno exibido
- se o texto mostrado depois da submissão é a consulta inteira
- mensagem de erro, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | teste > 0 e o texto mostrado é a consulta inteira | a base aceita ao menos o comprimento da consulta mais longa; o teto declarado se mantém | Verificado por medição |
| 2 | teste = 0, texto cortado ou mensagem de erro | o comprimento passa do limite da base; levar ao pesquisador para baixar o teto | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com o fim da consulta e o retorno visíveis

#### SD13 — saber se o hífen separa palavras, de modo que `e-learning` case `e learning`

**Elementos verificados:** Hífen como separador de palavras (`ontology-driven`, `e-learning`) (Não verificado).
**Depende de:** SD9.

**Pré-requisitos.**

- SD9 registrada com as aspas verificadas

**Consulta 1 — controle**, em caixa de busca.

```
abstract:"e-learning"
```

**Consulta 2 — teste**, em caixa de busca. Muda em relação ao controle: espaço no lugar do hífen.

```
abstract:"e learning"
```

**Consulta 3 — teste**, em caixa de busca. Muda em relação ao controle: sem hífen nem espaço.

```
abstract:elearning
```

**Passos.**

1. submeter cada consulta, uma por vez, e anotar o retorno

**Observar.**

- retorno exibido de cada consulta

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | primeiro teste = controle > 0 | o hífen separa palavras | Verificado por medição |
| 2 | primeiro teste ≠ controle, ambos > 0 | o hífen não separa palavras: forma hifenizada e forma separada são buscas distintas | Verificado por medição |
| 3 | controle = 0 | não se distingue o efeito do hífen; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela de cada consulta, com a consulta e o retorno visíveis

#### SD14 — saber se a ERIC exibe e deixa percorrer o retorno inteiro de uma busca larga

**Elementos verificados:** Teto de retorno exibido (Não verificado).

**Pré-requisitos.**

- busca de `eric.ed.gov` aberta no navegador do pesquisador

**Consulta 1 — teste**, em caixa de busca.

```
education
```

**Passos.**

1. submeter a consulta e anotar o retorno exibido
2. ir à última página de resultados pela navegação da interface, sem rastejar, e anotar a posição do último registro acessível

**Observar.**

- retorno exibido
- posição do último registro acessível
- aviso de limite, se houver

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | o último registro acessível tem a posição igual ao retorno exibido | não há teto de retorno exibido até esse tamanho | Verificado por medição |
| 2 | o último registro acessível tem posição menor que o retorno, ou há aviso de limite | há teto de retorno exibido, na posição anotada | Verificado por medição |
| 3 | a navegação não chega à última página | não se distingue o teto; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela do retorno e da última página acessível

#### SD15 — saber quantos registros a ERIC exporta de uma vez

**Elementos verificados:** Teto de exportação por lote (Não verificado).
**Depende de:** SD14.

**Pré-requisitos.**

- busca de `eric.ed.gov` aberta no navegador do pesquisador

**Consulta 1 — teste**, em caixa de busca.

```
title:ontology AND abstract:education
```

**Passos.**

1. submeter a consulta e anotar o retorno
2. abrir a opção de exportação e anotar o número máximo de registros que ela oferece ou aceita
3. exportar uma vez e contar os registros do arquivo

**Observar.**

- número máximo oferecido pela exportação
- número de registros no arquivo exportado

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | o arquivo traz todos os registros do retorno | não há teto de exportação até esse tamanho | Verificado por medição |
| 2 | o arquivo traz menos registros que o retorno, no número que a exportação anuncia | há teto de exportação por lote, no número anotado | Verificado por medição |
| 3 | a exportação falha ou o número do arquivo não corresponde a nenhum dos dois | não se distingue o teto; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela da opção de exportação
- o arquivo exportado

#### SD16 — saber se o registro de documento em português ou espanhol traz título e resumo em inglês, buscáveis pelos termos da string

**Elementos verificados:** Idioma do título e do resumo indexados (Não verificado).
**Depende de:** SD1.

**Pré-requisitos.**

- SD1 registrada com o prefixo de campo verificado

**Consulta 1 — teste**, em caixa de busca.

```
language:Portuguese AND abstract:education
```

**Passos.**

1. submeter a consulta e anotar o retorno
2. abrir três registros e anotar o idioma do título e do resumo indexados

**Observar.**

- retorno exibido
- idioma do título e do resumo nos registros abertos

| # | Resultado | Conclusão | Estado |
| :---: | :--- | :--- | :--- |
| 1 | os registros abertos têm título e resumo em inglês | a ERIC indexa em inglês o documento em outro idioma; os termos só em inglês o alcançam | Verificado por medição |
| 2 | os registros abertos têm título ou resumo só no idioma do documento | a ERIC indexa no idioma do documento; levar ao pesquisador (CE3) | Verificado por medição |
| 3 | teste = 0, ou registros sem resumo | não se distingue o idioma de indexação; levar ao pesquisador | Não verificado |

**Evidência a registrar.**

- captura da tela do retorno e de cada registro aberto

---

## 2. Critérios de elegibilidade

| Critério | ID | Na consulta? | Como |
| :--- | :---: | :--- | :--- |
| Intervalo temporal — 2017 até a data de execução | CE1 / CE2 | **No filtro da interface** | filtro de data da página de resultados, 2017 a 2026; registrar o rótulo do filtro e o retorno antes e depois |
| Idiomas — português, inglês e espanhol | CE3 | **Não** | termos só em inglês; campo `language` não usado |
| Tipo documental e revisão por pares | CE4 / CE5 | **Não** | `Peer reviewed only` desmarcada; campo `publicationtype` não usado |
| Adequação temática — regra de inclusão | CE6 | Aproximado | EB4 exige termo de prática (STR3) ou de fator situacional (STR4); a formalização se decide na triagem |
| Adequação temática — não pertinência e contra-escopo | CE6 | **Não** | exclusões temáticas manifestas na 2ª filtragem; aplicação integral na 3ª, com justificativa por ID |
| Domínio de aplicação educacional | CE7 / CE8 | **Sim**, por âncora | faceta 🟨 (FCT2) como grupo de quatro palavras-raiz, em forma radical |
| Outros tipos documentais | CE9 | **Não** | 2ª filtragem |
| Fator de impacto — não aplicável | CE10 | **Não** | não se aplica: critério só documental |

---

## 3. Strings por faceta

`STRn` é o identificador do protocolo e `#n` o número da string na composição. Mapa das facetas: **FCT1** 🟦 · **FCT2** 🟨 · **FCT3** 🟥 · **FCT4** 🟧.

### Declaração de cobertura

Declarada em `docs/procedimentos/eric/procedimento.toml`, `[cobertura]`; conferida por `python3 -m rsl documentos conferir`.

| Parâmetro | Valor |
| :--- | :--- |
| idiomas | FCT1: en; FCT2: en; FCT3: en; FCT4: en |
| plural | explícito |
| teto de caracteres | 1400 |
| derivações | morfologia e radical |

**Redução desta base.**

| Faceta | Termo fora da string | Motivo |
| :--- | :--- | :--- |
| FCT1 | educational ontological model | redução desta base |
| FCT2 | massive open online course | redução desta base |

### `STR1` — string `#1` — 🟦 FCT1 — Artefatos de representação e organização do conhecimento — **âncora obrigatória**

```
(title:"knowledge representation" OR title:"knowledge representations" OR title:"knowledge organization" OR title:"knowledge organizations" OR title:"conceptual model" OR title:"conceptual models" OR title:ontology OR title:ontologies)
```

### `STR1b` — string `#1b` — 🟦 FCT1 — Artefatos, subconjunto específico, no resumo

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern")
```

### `STR2` — string `#2` — 🟨 FCT2 — Domínio educacional — forma radical: quatro palavras-raiz no resumo — **âncora obrigatória**

```
(abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners)
```

### `STR3` — string `#3` — 🟥 FCT3 — Práticas do processo de ensino-aprendizagem

```
(abstract:"educational practice" OR abstract:"educational practices" OR abstract:"teaching method" OR abstract:"teaching methods" OR abstract:"educational strategy" OR abstract:"educational strategies" OR abstract:"learning activity" OR abstract:"learning activities" OR abstract:"educational intervention" OR abstract:"educational interventions")
```

### `STR4` — string `#4` — 🟧 FCT4 — Fatores situacionais

```
(abstract:"educational context" OR abstract:"educational contexts" OR abstract:"learning context" OR abstract:"learning contexts" OR abstract:"contextual factor" OR abstract:"contextual factors" OR abstract:"situational factor" OR abstract:"situational factors" OR abstract:"educational environment" OR abstract:"educational environments")
```

---

## 4. Expressões de busca

```
EB1 = #1 AND #2 AND #3 AND #4
EB2 = #1 AND #2 AND #3
EB3 = #1 AND #2 AND #4
EB4 = #1 AND #2 AND (#3 OR #4)     (executada)
EB5 = #1 AND #2                    (sonda de sensibilidade)
```

| Expressão | Execução |
| :--- | :--- |
| **EB4** | executar e exportar: é o corpus desta base |
| **EB5** | executar uma única vez, na mesma data; não compõe o corpus |
| **EB2**, **EB3** | executar só para o teste de fidelidade da derivação |
| **EB1** | não executar; derivação local |

- Execução: particionada
- **Fidelidade:** divergência acima de `divergencia_fidelidade` (`python3 -m rsl configuracao mostrar`) entre EB2/EB3 executadas e derivadas reprova a derivação.
- **Sensibilidade:** fração elegível de `EB5 \ EB4` abaixo do limite inferior da faixa `sensibilidade` (`python3 -m rsl configuracao mostrar`) mantém EB4; acima do superior, leva à reconsideração, com emenda.
- **Retorno zero:** EB4 = 0 ou EB5 = 0 é defeito de execução até prova em contrário; contagem derivada próxima de zero exige execução direta antes do relato.

Toda expressão é executada como duas consultas de campo único — `STR1` no título e `STR1b` no resumo —, ambas com a faceta 🟨 como grupo externo, unidas por deduplicação. Cada consulta fica dentro do teto de caracteres da declaração de cobertura; acima dele, a expressão se parte mantendo o grupo 🟦 íntegro, sem retirar termo, e as partes se unem por deduplicação.

### Como esta base exige a montagem

| Regra | Situação | Sondagem |
| :--- | :--- | :--- |
| grupo entre parênteses com `OR` precisa de condição fora dele | **Não verificado** | SD3 |
| a condição externa pode ser de campo, de texto livre ou outro grupo, antes ou depois | **Não verificado** | SD4 |
| um grupo não mistura campos: `title:` e `abstract:` na mesma disjunção devolvem zero | **Não verificado** | SD5 |
| `pubyearmin`/`pubyearmax` não convivem com grupo: o recorte vem do filtro da página | **Não verificado** | SD6 |
| sem truncamento; expressão composta sempre entre aspas | **Não verificado** | SD9 |

### EB1 (geral — as quatro facetas)

*Derivada localmente — não executar.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥) AND FCT4 (🟧)

### EB2 (específica — modelos e ontologias que representam práticas do processo de ensino-aprendizagem)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT3 (🟥)

**Consulta 2a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge representations" OR title:"knowledge organization" OR title:"knowledge organizations" OR title:"conceptual model" OR title:"conceptual models" OR title:ontology OR title:ontologies) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners) AND (abstract:"educational practice" OR abstract:"educational practices" OR abstract:"teaching method" OR abstract:"teaching methods" OR abstract:"educational strategy" OR abstract:"educational strategies" OR abstract:"learning activity" OR abstract:"learning activities" OR abstract:"educational intervention" OR abstract:"educational interventions")
```

**Consulta 2b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners) AND (abstract:"educational practice" OR abstract:"educational practices" OR abstract:"teaching method" OR abstract:"teaching methods" OR abstract:"educational strategy" OR abstract:"educational strategies" OR abstract:"learning activity" OR abstract:"learning activities" OR abstract:"educational intervention" OR abstract:"educational interventions")
```

### EB3 (específica — artefatos que formalizam os fatores situacionais do domínio educacional)

*Derivada localmente — executar apenas no teste de fidelidade.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND FCT4 (🟧)

**Consulta 3a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge representations" OR title:"knowledge organization" OR title:"knowledge organizations" OR title:"conceptual model" OR title:"conceptual models" OR title:ontology OR title:ontologies) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners) AND (abstract:"educational context" OR abstract:"educational contexts" OR abstract:"learning context" OR abstract:"learning contexts" OR abstract:"contextual factor" OR abstract:"contextual factors" OR abstract:"situational factor" OR abstract:"situational factors" OR abstract:"educational environment" OR abstract:"educational environments")
```

**Consulta 3b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners) AND (abstract:"educational context" OR abstract:"educational contexts" OR abstract:"learning context" OR abstract:"learning contexts" OR abstract:"contextual factor" OR abstract:"contextual factors" OR abstract:"situational factor" OR abstract:"situational factors" OR abstract:"educational environment" OR abstract:"educational environments")
```

### EB4 (de cobertura restrita — artefatos de representação no domínio educacional que mencionam prática ou fator situacional)

*Executada e exportada nesta base.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨) AND (FCT3 (🟥) OR FCT4 (🟧))

**Consulta 4a — artefato no título × prática**

```
(title:"knowledge representation" OR title:"knowledge representations" OR title:"knowledge organization" OR title:"knowledge organizations" OR title:"conceptual model" OR title:"conceptual models" OR title:ontology OR title:ontologies) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners) AND (abstract:"educational practice" OR abstract:"educational practices" OR abstract:"teaching method" OR abstract:"teaching methods" OR abstract:"educational strategy" OR abstract:"educational strategies" OR abstract:"learning activity" OR abstract:"learning activities" OR abstract:"educational intervention" OR abstract:"educational interventions")
```

**Consulta 4b — artefato no título × fator situacional**

```
(title:"knowledge representation" OR title:"knowledge representations" OR title:"knowledge organization" OR title:"knowledge organizations" OR title:"conceptual model" OR title:"conceptual models" OR title:ontology OR title:ontologies) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners) AND (abstract:"educational context" OR abstract:"educational contexts" OR abstract:"learning context" OR abstract:"learning contexts" OR abstract:"contextual factor" OR abstract:"contextual factors" OR abstract:"situational factor" OR abstract:"situational factors" OR abstract:"educational environment" OR abstract:"educational environments")
```

**Consulta 4c — termo específico no resumo × prática**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners) AND (abstract:"educational practice" OR abstract:"educational practices" OR abstract:"teaching method" OR abstract:"teaching methods" OR abstract:"educational strategy" OR abstract:"educational strategies" OR abstract:"learning activity" OR abstract:"learning activities" OR abstract:"educational intervention" OR abstract:"educational interventions")
```

**Consulta 4d — termo específico no resumo × fator situacional**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners) AND (abstract:"educational context" OR abstract:"educational contexts" OR abstract:"learning context" OR abstract:"learning contexts" OR abstract:"contextual factor" OR abstract:"contextual factors" OR abstract:"situational factor" OR abstract:"situational factors" OR abstract:"educational environment" OR abstract:"educational environments")
```

### EB5 (sonda de sensibilidade — as duas âncoras, sem exigir prática nem fator situacional)

*Sonda de sensibilidade — executada uma única vez; não compõe o corpus.* **Facetas:** FCT1 (🟦) AND FCT2 (🟨)

**Consulta 5a — artefato no título**

```
(title:"knowledge representation" OR title:"knowledge representations" OR title:"knowledge organization" OR title:"knowledge organizations" OR title:"conceptual model" OR title:"conceptual models" OR title:ontology OR title:ontologies) AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners)
```

**Consulta 5b — termo específico no resumo**

```
(abstract:"controlled vocabulary" OR abstract:"metadata schema" OR abstract:thesauri OR abstract:"ontology engineering" OR abstract:"ontology design pattern") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners)
```

### Como executar

1. Executar as consultas de EB4, na ordem em que aparecem acima, e exportar cada uma em arquivo próprio, `eric_<consulta>.ris` (`eric_4a1.ris`, …), em `data/execucoes/eric/`.
2. Aplicar o filtro de data da página e anotar o retorno antes e depois, com o rótulo exato do filtro.
3. Registrar as execuções, uma por arquivo: `python3 -m rsl busca registrar eric EB4 <arquivo> --retorno <n>`; rodar `busca derivar`. O retorno da base é a união deduplicada, nunca a soma: o número que vai às contagens da busca é o dos únicos, com o bruto ao lado.
4. Executar EB5 (5a e 5b) uma única vez e registrar com `EB5`.
5. Medir a aderência (seção 5). Abaixo do limiar de aderência (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`), passar à contingência das variantes.

### Variantes previstas

#### Refinamento por cruzamento título × resumo

Disparo: retorno da 4a acima do limite de triagem fixado pelo ReT e registrado nas contagens da busca. Forma: substituir a 4a pelas consultas abaixo, com o sufixo de ano; registrar o retorno antes e depois.

| # | Consulta |
| :---: | :--- |
| X2 | `title:ontology AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X3 | `title:ontology AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X4 | `title:ontology AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X6 | `title:ontologies AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X7 | `title:ontologies AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X8 | `title:ontologies AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X14 | `title:"domain model" AND abstract:"learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| X15 | `title:"domain model" AND abstract:"instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| X16 | `title:"domain model" AND abstract:"learning design" AND pubyearmin:2017 AND pubyearmax:2026` |

#### Camada 3 — descritores de artefato

Disparo: estudo que trata do artefato sem o nomear no título nem no resumo. Forma: a consulta abaixo. Antes do uso, sondar cada descritor nas formas `descriptor:` e `descriptorx:` e registrar os retornos. Adoção exige emenda.

```
(descriptor:Thesauri OR descriptor:Indexing OR descriptor:Metadata OR descriptor:"Knowledge Representation") AND (abstract:education OR abstract:educational OR abstract:learning OR abstract:teaching OR abstract:learner OR abstract:learners)
```

#### Contingência — consultas curtas, sem agrupamento

Disparo: aderência reprovada na busca por campo. Forma: executar todas as consultas abaixo, exportar e deduplicar em conjunto. Não reproduzem EB4; a adoção exige emenda e a recomposição de FCT1 AND FCT2 AND (FCT3 OR FCT4) com `AND` entre um termo de cada faceta.

| # | Consulta | # | Consulta |
| :---: | :--- | :---: | :--- |
| 1 | `"knowledge representation" AND pubyearmin:2017 AND pubyearmax:2026` | 2 | `"knowledge organization" AND pubyearmin:2017 AND pubyearmax:2026` |
| 3 | `"knowledge organization system" AND pubyearmin:2017 AND pubyearmax:2026` | 4 | `"knowledge organization systems" AND pubyearmin:2017 AND pubyearmax:2026` |
| 5 | `"controlled vocabulary" AND pubyearmin:2017 AND pubyearmax:2026` | 6 | `"controlled vocabularies" AND pubyearmin:2017 AND pubyearmax:2026` |
| 7 | `thesaurus AND pubyearmin:2017 AND pubyearmax:2026` | 8 | `thesauri AND pubyearmin:2017 AND pubyearmax:2026` |
| 9 | `"classification scheme" AND pubyearmin:2017 AND pubyearmax:2026` | 10 | `"classification schemes" AND pubyearmin:2017 AND pubyearmax:2026` |
| 11 | `"metadata schema" AND pubyearmin:2017 AND pubyearmax:2026` | 12 | `"metadata schemas" AND pubyearmin:2017 AND pubyearmax:2026` |
| 13 | `"ontology engineering" AND pubyearmin:2017 AND pubyearmax:2026` | 14 | `"ontology development" AND pubyearmin:2017 AND pubyearmax:2026` |
| 15 | `"ontology design pattern" AND pubyearmin:2017 AND pubyearmax:2026` | 16 | `"ontology-based knowledge representation" AND pubyearmin:2017 AND pubyearmax:2026` |
| 18 | `ontology AND "learning object" AND pubyearmin:2017 AND pubyearmax:2026` | 20 | `ontology AND "learning analytics" AND pubyearmin:2017 AND pubyearmax:2026` |
| 21 | `ontology AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` | 22 | `ontology AND "instructional design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 23 | `ontology AND "teaching methods" AND pubyearmin:2017 AND pubyearmax:2026` | 24 | `ontology AND "situational factors" AND pubyearmin:2017 AND pubyearmax:2026` |
| 25 | `ontology AND "educational context" AND pubyearmin:2017 AND pubyearmax:2026` | 26 | `ontologies AND "learning object" AND pubyearmin:2017 AND pubyearmax:2026` |
| 28 | `ontologies AND "learning analytics" AND pubyearmin:2017 AND pubyearmax:2026` | 29 | `ontologies AND "learning design" AND pubyearmin:2017 AND pubyearmax:2026` |
| 30 | `ontologies AND "instructional design" AND pubyearmin:2017 AND pubyearmax:2026` | 35 | `"domain model" AND education AND pubyearmin:2017 AND pubyearmax:2026` |
| 39 | `"ontological engineering" AND pubyearmin:2017 AND pubyearmax:2026` | | |

#### Negação do ruído por descritor

Disparo: necessidade de levar ao resumo termos de `STR1` hoje restritos ao título. Forma: `-descriptor:"…"`, testando um a um, antes do uso: `Educational Research`, `Research Methodology`, `Epistemology`, `Qualitative Research`.

---

## 5. Conjunto-semente

Esperadas nesta base, conforme o protocolo. Estado de conferência no arquivo de sementes (`[documentos] sementes`); aferição em `data/semente_aderencia.csv`.

| # | Estudo | DOI ou identificador | Observação |
| :---: | :--- | :--- | :--- |
| SE6 | Iatrellis et al. (2019) | `10.1007/s10639-019-09872-9` | — |
| SE7 | Chimalakonda & Nori (2020) | `10.1186/s40561-020-00135-6` | — |
| SE8 | Cenka et al. (2023) | `10.1080/10494820.2022.2039947` | alcance depende do hífen (`ontology-driven`) |

**Procedimento.** *Etapa 1:* buscar o título entre aspas, sem recorte temporal e sem as expressões; semente não indexada sai do denominador e registra-se como cobertura. *Etapa 2:* procurar a semente na exportação de EB4 por DOI e depois por título, sem reexecutar a busca.

**Limiar de aderência** (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`), sobre a união das bases. A aderência por base indica qual base e qual faceta falharam.

---

## 6. Ressalvas

1. Todos os termos são **termos livres**; não apresentar as expressões como compostas de descritores ERIC.
2. Alterar as expressões exige repetir as sondagens pertinentes da seção 1.
3. No relato, declarar a assimetria de campo em relação à Scopus: aqui a faceta 🟦 vai ao título, e as palavras-chave correspondem ao campo controlado `descriptor`.
