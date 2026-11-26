---
name: conferir-referencia
description: Confere referência bibliográfica na fonte e registra o seu estado de conferência, sem preencher dado de memória. Use ao acrescentar, normalizar, corrigir ou completar qualquer referência dos instrumentos — conjunto-semente, leitura exploratória, obras de referência, normas técnicas — e ao responder dúvida sobre autoria, ano, veículo, número de norma ou paginação.
---

# Conferir uma referência na fonte

Regra dura, e a razão de ser desta skill: **dado bibliográfico não se preenche de memória.**
Autor, título, veículo, ano, volume, número, páginas, DOI, número de norma — nenhum. Modelo
de linguagem produz referência plausível e inexistente, e numa revisão sistemática isso
contamina o registro e destrói a reprodutibilidade.

## O que conta como fonte

Em ordem de preferência:

1. o **registro da base** que indexa o item (Web of Science, Scopus, ERIC, BRAPCI);
2. a **página do editor** ou o DOI resolvido;
3. o **catálogo do emissor**, para norma técnica — foi assim que se obteve
   `IEEE 1484.12.1-2020`, com a edição anterior `-2002` registrada como superada;
4. o **repositório institucional**, para tese e dissertação — foi assim que se obteve o ano
   de 2020 e a grafia do programa na tese de Borges;
5. o **próprio documento**, quando em mãos.

Captura de tela ou a resposta bruta da consulta ficam anexadas. **Conferência sem evidência
não é conferência.**

## O que NÃO conta como fonte

- memória do modelo;
- outra referência do mesmo projeto que também não foi conferida;
- citação de terceiro — confere-se o item, não quem o citou;
- resultado de busca que não resolve até o registro do item.

## Três estados, e cada referência carrega o seu

| Estado | Significa |
| --- | --- |
| **Consultada e conferida em fonte** | o conteúdo foi lido e os dados batem com a fonte |
| **Conferida quanto aos dados bibliográficos, sem consulta ao conteúdo** | os dados batem; a obra ainda não foi lida |
| **Designada para consulta, com dados não conferidos em fonte** | nem lida nem conferida |

Lista preliminar **não se apresenta como fundamentação já conferida**. O estado de cada item
fica ao lado dele e muda à medida que a consulta ocorra.

## Procedimento

1. Verificar se o item já tem estado registrado — conjunto-semente no arquivo de
   sementes (`[documentos] sementes` do `config.toml`), com os dados bibliográficos e a
   conferência campo a campo; leitura exploratória em `docs/02`, seção Estudos
   inicialmente consultados; obras de referência em `docs/02`, seção Obras de referência
   a consultar.
2. Não tendo, consultar a fonte. Havendo busca na web disponível, usá-la e **resolver até o
   registro do item**; não havendo, dizer que não se pode conferir aqui e deixar o item como
   designado — **não preencher**.
3. Registrar na fonte única: os dados conferidos, o estado e onde se conferiu. No arquivo
   de sementes, o estado é `verificacao = true` (conferida) ou `false` (pendente), e onde e
   como se conferiu vai em `nota`.
4. Atualizar o instrumento correspondente e conferir o texto final nele.
5. Havendo divergência com o que estava escrito, **retificar explicitamente** no relato ao
   pesquisador. Não corrigir em silêncio.

## Casos que já ocorreram, e o que ensinaram

- **Remédio impossível.** Um parecer externo mandou "uniformizar com a referência do
  protocolo". O protocolo não tinha referência alguma àquela obra. Conferir que o alvo da
  correção existe antes de aplicá-la.
- **Iniciais certas, ano ausente.** Só o ano faltava. Conferir campo a campo, não a
  referência como bloco.
- **Duas edições vigentes.** Norma com edição superada e edição ativa: registram-se as duas
  e diz-se qual se cita, fixada no momento da consulta conforme a que o estudo analisado
  empregue.
- **Pendência já declarada.** O mesmo parecer apontou como defeito uma referência em APA que
  o instrumento **já declarava** como "normalização em ABNT NBR 6023 pendente". Ler o que o
  documento declara antes de registrar achado.

## Normalização

ABNT NBR 6023. Onde a normalização ainda não foi feita, **declarar a pendência** em vez de
normalizar por aproximação — normalização inventada é dado inventado com outra aparência.
