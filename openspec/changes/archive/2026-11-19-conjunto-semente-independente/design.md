# Design

## Context

A motivação está em `proposal.md`. Estado observado em 2026-11-19:

- `sementes()` em `src/protocolo.py` lê a tabela com as colunas fixadas em
  `COLUNAS_SEMENTES = ("ID Semente", "Semente", "Bases")`. As colunas exigidas são lidas
  pelo nome, via `tabela_da_secao`.
- `gen_semente.py` (`csv_out`) já gera uma linha por semente e por base da tabela, com
  `esperada_na_base`. A primeira versão da proposta errava nesse ponto e foi retificada.
- `aderencia()` em `derivar_expressoes.py` imprime recuperadas/total e adverte que o
  denominador correto é a coluna `indexada`, preenchida à mão. Não relata intervalo.
- `data/sementes.json` guarda só metadado autoral, ligado por DOI ou título. O papel é
  decisão de protocolo, não metadado de conferência, e por isso fica na tabela do
  protocolo.
- A exigência principal "Saídas preservadas" proíbe mudar a saída da aderência. O delta a
  modifica explicitamente, e a mudança não passa em silêncio.

## Goals / Non-Goals

**Goals:**
- A aderência que decide a passagem é medida sobre sementes que não orientaram o
  vocabulário.
- O relato mostra a incerteza da estimativa.

**Non-Goals:**
- Escolher as sementes novas ou o tamanho do conjunto. A escolha é do pesquisador; a
  busca de candidatas segue a skill `conjunto-semente`.
- Conferir a indexação das sementes nas bases pelo agente sem acesso autorizado. Isso é
  consulta à fonte, feita pelo pesquisador ou pelo agente via a interface pública, quando
  os termos de uso permitirem.
- Mudar o denominador: continua sendo `indexada`, conferida à mão.

## Decisions

**D-a. Papel como coluna da tabela do protocolo, não em `sementes.json`.** Quem decide que
uma semente é de validação é o protocolo, e o que o protocolo declara é parâmetro
estrutural (README). Alternativa: um campo autoral em `sementes.json`. Foi rejeitada
porque o metadado autoral é de conferência e o `--sincronizar` o preserva, mas não o trata
como decisão de método.

**D-b. Critério para classificar uma semente como desenvolvimento.** Proposta para o
pesquisador: é de desenvolvimento toda semente que motivou a inclusão, a manutenção ou a
retirada de um termo, com o registro dessa ligação no histórico. A SE4 é de
desenvolvimento por registro explícito (manutenção de `modelo de domínio`). As demais
dependem de reconstituição, ou da declaração do pesquisador de que não orientaram termo.

**D-c. Intervalo de Wilson, não intervalo normal.** Com n pequeno e proporção perto de 1,
o intervalo normal sai assimétrico de forma errada e ultrapassa 100%. O Wilson tem
cobertura adequada nessa faixa e usa só a biblioteca padrão. O cálculo para 8/10 foi
conferido: 49,0% a 94,3%.

**D-d. O limiar continua sendo o do protocolo, aplicado só à validação.** Alterar o
limiar ou o tamanho mínimo é D2 da proposta, decisão do pesquisador. Esta change dá o
instrumento, não o valor.

**D-e. Conjunto de validação vazio reprova.** Sem semente de validação, a aderência
decisória não tem denominador, e a passagem não poderia ser julgada. O defeito é impedido
na leitura, não descoberto em M3/E2.

**D-f. Casamento por prefixo é indício, não recuperação.** O título truncado pode gerar
falso positivo, e a skill `teste-de-aderencia` já exige conferência humana. O prefixo é
impresso como `[? ]`, fica fora do numerador e só entra na contagem depois de registrado
na coluna `recuperada`. O casamento exato continua contando como recuperação.

## Risks / Trade-offs

- [Conjunto de validação pequeno: as sementes novas ainda não existem] → o intervalo
  aparece no relato, e o pesquisador vê a imprecisão em vez de ler 80% como estimativa.
- [Reclassificar sementes depois de ver a aderência] → a classificação se registra no
  histórico **antes** da primeira aderência registrada. A tarefa de classificação vem antes
  de qualquer execução.
- [Sementes novas com o mesmo viés de procedência das atuais, achadas pelos mesmos
  termos] → recomendar ao pesquisador uma procedência independente da string (citação,
  indicação de especialista, sumário de periódico) e registrá-la por semente.
- [A coluna nova quebra a leitura de protocolos antigos] → o projeto lê só a versão
  vigente, e a ausência da coluna reprova com mensagem que a nomeia.

## Migration Plan

1. O pesquisador classifica as sementes atuais e decide se amplia o conjunto.
2. A coluna `Papel` entra no protocolo junto com a leitura que a exige, no mesmo passo,
   para `--conferir` não ficar reprovado.
3. A aderência e a planilha passam a relatar por papel. `semente_aderencia.csv` é
   regenerado, e não há planilha preenchida a migrar, porque nenhuma aderência foi
   registrada.

## Open Questions

- Fonte de busca das sementes novas. Não muda specs nem tarefas, só o conteúdo da tabela.
