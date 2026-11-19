# Design

## Context

A motivação está em `proposal.md`, e os requisitos, nas specs desta change. O ponto de
partida é o pacote `src/rsl/` e a gramática declarada de `refatoracao-dos-scripts`, que
precisa estar arquivada.

O estado verificado em 2026-11-19:

- **A tabela atual tem 10 sementes e a coluna `Papel`**, com SE4 em `desenvolvimento` e
  as demais em `validação`.
- **As referências seguem uma forma próxima da APA, com variações:**
  - SE10 traz editores e o nome do evento;
  - algumas referências repetem o ano depois do veículo;
  - SE10 traz o DOI do volume, não o do capítulo (ficha da WoS e change
    `conjunto-semente-independente`, D4).
- **`sementes.json` liga cada semente por `ligacao` = `doi:…` ou título normalizado.**
  Todas as 10 têm DOI, então a ligação não depende do título hoje.
- **O protocolo traz escapes de Markdown** (`\-`, `2012\.`). Isso indica exportação de um
  editor de texto. É inferência, não confirmada.

## Goals / Non-Goals

**Goals:**
- Ler as sementes sem extração por padrão de texto.
- Garantir que a transcrição não perca nem invente dado.

**Non-Goals:**
- Conferir as referências na fonte. Isso é a tarefa 2.3 de
  `conjunto-semente-independente`, com a skill `conferir-referencia`.
- Mudar o significado ou o domínio de `papel`. O campo só migra da coluna `Papel`
  acrescentada por `conjunto-semente-independente`, com as mesmas exigências.
- Normalizar as referências pela ABNT no protocolo. A exibição de `mostrar` é só para
  leitura.

## Decisions

### D1. Forma do bloco

```toml
[[semente]]
id = "SE1"
autores = ["Alvarenga, V. B. L.", "Cristovão, H. M."]
ano = 2023
titulo = "Objetos de aprendizagem organizados com base no padrão LOM-IEEE adaptado a uma ontologia operacional de domínio na web semântica"
veiculo = "Revista Ibero-Americana de Ciência da Informação (RICI)"
volume = "16"
numero = "1"
doi = "10.26512/rici.v16.n1.2023.47618"
bases = ["brapci"]
papel = "validação"
```

`volume`, `numero` e `paginas` são texto, porque há valores como `"6-21"` e `"S1"`. O `ano`
é inteiro, porque é comparado ao recorte.

Alternativa considerada: manter a tabela com colunas estruturadas, opção (c) da
exploração. O pesquisador preferiu TOML.

### D2. Esquema fechado

Campo desconhecido reprova. Isso impede por construção o erro de digitação que hoje
passaria como campo ignorado (`titlo`). Campo novo exige mudança da gramática, que o
autoteste passa a cobrir.

### D3. Um bloco por seção, localizado pela gramática

O leitor procura, dentro da seção "Conjunto-semente", blocos cercados de linguagem
`toml`. Zero ou mais de um bloco reprova. Bloco de outra linguagem é ignorado.

### D4. Transcrição verificável

A migração não usa os leitores de padrão (`_titulo`, `_doi`) para gerar o bloco
automaticamente. Usá-los propagaria o defeito que motiva a change.

A transcrição é feita campo a campo a partir do texto da célula, e a conferência é
mecânica. Para cada semente, a concatenação dos campos tem de reconstituir o texto da
célula, admitidas só a pontuação, o ano repetido e os rótulos `DOI:`. Cada sobra é
listada para o pesquisador decidir: os editores e o local da SE10, por exemplo, não têm
campo.

Alternativa considerada: acrescentar `editores` e `evento`. Fica para o pesquisador, na
tarefa 1.2, porque muda o esquema.

### D5. Ligação preservada

`sementes sincronizar` continua casando por DOI ou título. A tarefa 3.2 confere que as 10
ligações de `sementes.json` casam depois da troca, sem entrada nova nem órfã.

## Risks / Trade-offs

- **[Editor de texto destrói o bloco na exportação]** → reprova com PROTOCOLO_ILEGIVEL
  (spec). A tarefa 1.1 pergunta ao pesquisador como o protocolo é editado. Se for por
  editor, o README passa a dizer que a seção se edita no `.md`.
- **[Dado perdido na transcrição]** → a reconstituição da D4 lista toda sobra, e nenhuma
  sobra se descarta sem decisão.
- **[Conflito com `conjunto-semente-independente`]** → aquela change já implementou a
  coluna `Papel` (verificado na árvore de trabalho em 2026-11-19, ainda sem commit). O
  papel migra como campo, com o mesmo domínio e a mesma regra de validação não vazia. A
  tarefa 4.1 ajusta a spec promovida ou a delta, conforme o estado daquela change.

## Migration Plan

1. O pesquisador confirma a forma de edição do protocolo e o destino das sobras.
2. No mesmo passo:
   - o leitor do bloco e a gramática;
   - a troca da tabela pelo bloco no protocolo;
   - o autoteste.

   Assim, `conferir` não fica reprovado entre um passo e outro.
3. `sementes sincronizar` sem mudança no arquivo.

Rollback: reverter o commit. A tabela antiga está no histórico do git.
