# Proposta

## Por quê

As primeiras execuções registradas da Scopus (BD2/EX1 a EX4, em 2026-11-25) expuseram dois
defeitos das conferências pós-execução. Por causa deles, a derivação, a fidelidade e a
aderência medem o instrumento em vez de medir a busca.

1. **Plural aproximado no casamento local.** A derivação casa os termos das strings do
   **protocolo**, que estão sem as formas de número. Para isso usa uma expressão regular que
   admite só o sufixo `s`/`es` em cada palavra. Por isso `"learning activity"` não casa
   `learning activities`. A fidelidade de EB2 na Scopus reprovou com 34,4% de divergência
   simétrica (61 na execução direta, 40 no conjunto derivado). Dos 21 registros que ficaram
   só na execução direta, 19 caíram porque o casamento local não reconheceu a FCT3. Neles o
   termo aparece no plural irregular: `learning activities` em 17, `educational strategies`
   em um, e no outro em forma do mesmo tipo. Os outros 2 caíram porque a âncora FCT1 não
   casou localmente: é a aproximação que a fidelidade existe para medir, e esta mudança não
   a trata. A string que a base recebeu já trazia as formas plurais: o defeito é da
   derivação, não da busca.
2. **A sonda entra no corpus.** `busca derivar`, `conferencia fidelidade` e `aderencia
   medir` leem **todas** as execuções registradas, inclusive a da sonda (EB5). Pelo
   protocolo, a sonda fica fora do corpus. Na Scopus, os 949 registros que só a EB5 traz
   foram rotulados como da executada: `contagens_busca.csv` registra EB4 = 1082 (são 133),
   e `ordem_triagem.csv` tem 1.082 registros. A aderência contou a SE6 como recuperada,
   embora ela só apareça na EB5. As execuções diretas das expressões de conferência (EB2,
   EB3) também entram, e duplicam as contagens brutas.

## O que muda

- **O casamento local usa os termos que a base recebeu.** Em cada base, o vocabulário de
  cada faceta é o da string composta para aquela base, já com as formas de número geradas
  por regra e por exceção declarada, e com o radical truncado onde a fonte o declara. A
  esse vocabulário se somam as formas de número dos termos, quando a base declara o plural
  `pela lematização`. O sufixo aproximado `s`/`es` deixa de existir. Assim, o casamento
  local e a consulta passam a sair da mesma composição.
- **O corpus é só a executada.** A derivação, o conjunto derivado da fidelidade e a
  aderência passam a ler apenas as execuções registradas da expressão executada. A sonda e
  as execuções diretas das expressões de conferência ficam de fora. A sensibilidade
  continua lendo a executada e a sonda, cada uma pela sua execução, e a fidelidade continua
  lendo a execução direta pelo arquivo que recebe.
- **O relato diz o que entrou.** Cada uma das três conferências nomeia as execuções lidas e
  as que deixou de fora, com o motivo.
- **O autoteste prova os dois casos.** Um caso com plural irregular falha no casamento
  antigo e passa no novo; outro, com registro só da sonda, prova que ele não entra nas
  contagens, na ordem de triagem nem na aderência.

Fora do escopo:

- reproduzir localmente a proximidade (`W/5`, `NEAR/5`) e a restrição de campo: continuam
  aproximações, e é a fidelidade que as mede;
- mudar limiares, a composição ou qualquer string;
- tratar a perda das sementes da Scopus, que se diagnostica pelas quatro consultas por DOI
  (skill `testar-aderencia-das-expressoes`).

## Capacidades

### Novas capacidades

Nenhuma.

### Capacidades modificadas

- `derivacao-das-expressoes`: dois requisitos novos, "Casamento local pelos termos da
  base" e "Corpus da derivação é a executada". O requisito "Saídas preservadas" é
  modificado e passa a admitir as diferenças que esta mudança produz.

## Impacto

- Código:
  - `src/rsl/busca/derivacao.py`: `padrao` e `carrega_facetas` passam a ser por base, a
    partir de `Composicao`;
  - `src/rsl/busca/registro.py`: seleção das consultas por expressão;
  - `src/rsl/busca/fidelidade.py`, `src/rsl/busca/aderencia.py`: leem só a executada;
  - `src/rsl/procedimentos.py`: só se for preciso expor os termos por faceta e por base,
    sem mudar o que gera;
  - autoteste: `src/rsl/autoteste/busca.py`.
- Saídas: `contagens_busca.csv`, `ordem_triagem.csv`, `registros.csv` e
  `fidelidade_eb<n>.csv` mudam de conteúdo. As que foram gravadas em 2026-11-25 estão fora
  do controle de versão, e regeneram-se depois da implementação.
- Documentação: o comentário de `padrao` e a docstring do pacote `busca`. A sinopse em
  `docs/procedimentos.md` só muda se a descrição dos comandos mudar.
