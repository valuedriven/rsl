# Proposta

## Por quê

O pesquisador executa as sondagens copiando cada consulta do roteiro e colando na interface
da base. Hoje 8 consultas declaradas, em 5 sondagens de 4 bases, não trazem a consulta: trazem
uma instrução em prosa dentro do bloco de código. São elas: WoS SD5, Scopus SD2 (2 consultas)
e SD4, ERIC SD12 e BRAPCI SD4 (3 consultas). Um exemplo: "o bloco de EB4 no procedimento
gerado". Nesses casos o pesquisador precisa procurar a expressão na seção 4 e, em dois deles,
montar a consulta à mão: trocar `W/5` por `AND` ou partir a faceta 🟦 em metades. Isso abre
espaço a erro de montagem justamente na sondagem que mede o comportamento da base. A gramática
já diz que `texto` é "consulta literal", mas nada confere isso.

## O que muda

- A consulta de sondagem pode declarar, no lugar de `texto`, uma **referência a uma
  expressão** do protocolo (`expressao = "EBn"`). O gerador escreve no roteiro o texto
  literal da consulta, igual ao da seção 4, e informa o número de caracteres.
- Quando a expressão tem mais de uma consulta (base particionada ou com consultas separadas),
  a referência diz qual: o identificador da consulta ou `mais_longa`.
- **Transformações declaradas, de conjunto fechado**, aplicadas na composição e não por
  substituição de texto:
  - `sem_proximidade`: as âncoras são unidas por `AND` em vez do operador de proximidade
    (Scopus SD2, controle);
  - `metade = {faceta, parte}`: a string da faceta é partida em duas metades contíguas, e
    só a metade indicada entra (BRAPCI SD4, controles).
- `sondagens registrar` grava como texto submetido o **literal resolvido**, e não a
  referência. Assim o registro guarda a consulta que de fato foi à base, mesmo que as
  strings mudem depois.
- **Consulta em prosa passa a reprovar**: `texto` com marca de referência (identificador
  `EBn`, `STRn` ou `FCTn`, "procedimento gerado", cor de faceta) reprova a base com
  PROTOCOLO_ILEGIVEL e aponta o uso de `expressao`. Também reprova a consulta que declara
  `texto` e `expressao` juntos, ou nenhum dos dois, e a que aponta expressão, consulta,
  faceta ou transformação inexistente ou não aplicável.
- **Fontes migradas**: as 8 consultas das 4 bases passam a usar `expressao`. Os passos que
  mandavam "copiar o bloco de EBn" são reescritos. Os procedimentos são regenerados.

Fora do escopo: o campo `onde` continua em prosa (caixa, seletor e filtro de interface não se
colam), e não se redesenha nenhuma sondagem. As leituras e a pergunta de cada uma continuam as
mesmas.

## Capacidades

### Novas capacidades

Nenhuma.

### Capacidades modificadas

- `sondagens-por-base`: a consulta da sondagem passa a ser literal ou referência resolvida
  (novo requisito de referência e transformações; requisitos "Consultas da sondagem", "Forma
  de cada sondagem no roteiro", "Forma do resultado registrado" e "Autoteste prova o roteiro
  e o registro" modificados).

## Impacto

- Código: `src/rsl/gramatica.py` (campos de `[[sondagens.consultas]]`), `src/rsl/fonte.py`
  (validação), `src/rsl/procedimentos.py` (resolução na `Composicao` e renderização em
  `roteiro`), `src/rsl/sondagens.py` (texto resolvido no registro), autoteste
  (`src/rsl/autoteste/procedimentos.py` ou `fontes.py`).
- Dados: `docs/procedimentos/{wos,scopus,eric,brapci}/procedimento.toml`; os quatro
  `docs/procedimentos_busca_<sigla>.md` regenerados.
- Registro de execução: sem migração. Os resultados já gravados guardam o texto que se
  declarou na época.
- Documentação: `documentos gramatica` passa a exibir os campos novos, porque é derivada da
  gramática.
