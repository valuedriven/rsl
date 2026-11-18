---
name: validacao-vocabulario-controlado
description: Consulta os instrumentos de controlo terminológico, registra a evidência e atribui estatuto a cada termo — descritor autorizado, termo livre ou pendência. Use ao validar vocabulário, consultar tesauro, decidir se um termo pode ser apresentado como descritor, ou tratar de TBCI, UNESCO Thesaurus, ERIC Thesaurus e Brased.
---

# Validação de vocabulário controlado

Esta skill existe porque é aqui que se inventa dado sem perceber. Um modelo de
linguagem produz com facilidade um descritor plausível e inexistente, e numa revisão
sistemática isso contamina o registro e destrói a reprodutibilidade.

## 1. A regra única, para as quatro facetas

- **Os instrumentos de cada faceta são os que o protocolo declara** na seção
  "Instrumentos para controle terminológico". Não se presume instrumento por idioma nem
  por faceta: o que não está na seção não é instrumento de linha alguma da planilha.
- **O que é propriedade do instrumento** — sigla, idiomas que cobre e modo de consulta —
  está em `[instrumentos]` do `config.toml` (ver `README.md`). Cada termo é planejado para
  cada instrumento da sua faceta que cubra o seu idioma.
- **Instrumento sem cliente automatizado** (modo `manual`) gera linha com o estatuto
  "pendente de validação manual": consulta-se à mão e registra-se a evidência como em
  qualquer outra linha. Pendente não é "não encontrado".

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

O registro é a própria planilha `data/validacao_termologica.csv`, com 22 colunas e uma
linha por termo e instrumento. Ela é construída a partir das tabelas do protocolo e
guarda o estatuto de cada termo: `--exportar` reconstrói a planilha e `--importar` a
reconcilia com o protocolo, preservando as colunas `decisao_ReT`, `justificativa_ReT` e
`data_decisao` e as linhas de termo retirado. Não há JSON intermediário. É ela o
instrumento de controlo, e **não se duplica em documento algum** — o protocolo (`docs/03`) declara a
regra e aponta para ela.

## 5. Geração e execução

Os comandos, nesta ordem:

| Comando | O que faz |
| --- | --- |
| `python3 src/validar_termos.py --sonda` | mede o que cada instrumento aceita, com contagem e captura. **Obrigatório antes de tudo** |
| `python3 src/validar_termos.py --exportar` | reconstrói a planilha a partir do protocolo, sem rede; não decide nada |
| `python3 src/validar_termos.py --validar tbci` | consulta o TBCI, grava a evidência e propõe o estatuto |
| `python3 src/validar_termos.py --validar unesco` | idem para o UNESCO Thesaurus; `--validar ambos --faceta 1` restringe a uma faceta |
| `python3 src/validar_termos.py --importar` | reconcilia a planilha com o protocolo, preservando decisões e linhas fora do protocolo |

A resposta bruta de cada consulta é gravada em
`data/evidencia/<instrumento>/<hash>.json`, e `arquivo_evidencia` na planilha aponta
para ela: **linha sem evidência correspondente é linha inválida**. O script recupera e
registra; não exclui, não reescreve termo e não preenche `decisao_ReT`.

Campos que decidem: `instrumento`, `consultado_em`, `status_proposto`,
`rotulo_autorizado`, `arquivo_evidencia`, `url_consultada`, `decisao_ReT`,
`justificativa_ReT`. A decisão final e a incorporação de termos relacionados e
específicos são do ReT com a Validação Temática — a ferramenta recupera e registra.

Estado corrente: verificar na planilha e em `python3 src/protocolo.py --pendencias`;
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
