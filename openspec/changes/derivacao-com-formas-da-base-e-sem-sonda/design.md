# Design

## Contexto

O casamento local fica em `src/rsl/busca/derivacao.py`:

- `carrega_facetas(b)` lê `b.d["strings"][fid]["termos"]`, os termos da STR do protocolo,
  sem formas de número e iguais para todas as bases;
- `padrao(termo)` aceita `(?:e?s)?` depois de cada palavra;
- `facetas_atingidas(reg, facetas)` aplica esses padrões a título, resumo e palavras-chave
  normalizados (`markdown.normaliza`).

Três comandos usam essas funções: `derivar`, `fidelidade` (`src/rsl/busca/fidelidade.py`)
e, indiretamente, `aderencia` (`src/rsl/busca/aderencia.py`). Os três obtêm os registros
por `carrega_consultas(b)` → `coleta(validas)` → `identifica`, sem filtrar por expressão. Já
a sensibilidade seleciona por expressão (`registros_da_expressao(base, ident, validas)`).

Os termos que cada base recebe saem de `Composicao(ctx, d, fonte).strings[fid]["termos"]`
(`src/rsl/procedimentos.py`):

- é a lista da STR restrita aos idiomas da fonte, menos a redução declarada;
- traz as formas de número, quando o plural é `explícito`;
- traz o radical truncado, quando a fonte declara `[[radical]]`.

É a mesma lista que vai à §3 e às consultas do procedimento gerado.

## Objetivos / Fora do escopo

**Objetivos:**

- o casamento local de cada base sai da mesma composição que produz a consulta daquela
  base: o vocabulário não se copia nem se reconstrói;
- uma única seleção de registros do corpus, usada pelos três comandos.

**Fora do escopo:**

- proximidade e restrição de campo no casamento local;
- casamento por variante ortográfica ou por diacrítico além do que `normaliza` já faz.

## Decisões

### 1. Vocabulário por base a partir de `Composicao`

Para cada base presente nas execuções lidas:

1. `le_fonte(ctx, d, sigla)`, depois `Composicao(ctx, d, fonte)`;
2. a composição com flexão indecidível reprova, como em `gera_base`, nomeando a base;
3. de cada faceta se tomam os `termos`, e somam-se as formas de número de cada termo sem
   `*`, por `flexao.formas_de_numero` com os idiomas do quadro (`idiomas_do_termo`) e as
   exceções da composição.

O resultado é `{sigla: {fid: {"termos": [...], "padroes": [...]}}}`, e `facetas_atingidas`
recebe as facetas da base do registro.

`padrao` perde o sufixo `(?:e?s)?`. A palavra com `*` vira prefixo livre (`\w*`), como
hoje. As palavras se ligam por `\s+` sobre o texto normalizado, de modo que hífen e
pontuação continuam equivalentes a espaço.

*Alternativas consideradas:*

- **Ampliar a regex com `y→ies` e outras regras.** Reproduziria de modo aproximado o que
  `flexao.py` já faz com regra e exceção declarada; divergiria dela a cada exceção nova.
  Descartada pelo princípio de garantia por construção.
- **Usar `formas_de_numero` sobre os termos do protocolo, sem `Composicao`.** Ignoraria a
  redução, o radical e os idiomas declarados por base, e o casamento local voltaria a ser
  outra lista, diferente da consulta. Descartada.
- **Somar formas de número só quando o plural é `explícito`.** Numa base que lematiza, a
  string não traz o plural, mas a base o casa. Sem as formas, o casamento local perderia
  exatamente o que a base recupera. Por isso se somam sempre. A soma não muda a consulta,
  só o casamento local.

### 2. Seleção do corpus num lugar só

Em `registro.py`, uma função separa as consultas válidas em:

- **lidas**: a expressão é `b.executada`;
- **deixadas de fora**: as demais, com o motivo: `sonda` para `b.sonda`, `execução
  direta de conferência` para as outras.

`derivar`, `fidelidade` (conjunto derivado) e `aderencia` usam só as lidas, e imprimem as
duas listas antes do resultado. A sensibilidade não muda: já seleciona por expressão.

*Alternativa considerada:* filtrar só a sonda. As execuções diretas de EB2 e EB3 também
inflam as contagens brutas e a coluna `duplicata_de`. Como são subconjuntos da executada,
não acrescentam registro ao corpus. Descartada.

### 3. Prova no autoteste

Em `src/rsl/autoteste/busca.py`, dois casos novos, com exportações sintéticas (RIS) num
diretório temporário e um registro de execução apontado por configuração de ensaio
(`RSL_CONFIG`), como os demais casos de dados:

- **Plural irregular.** Toma da composição de uma base uma forma de número cujo plural o
  sufixo `s`/`es` não alcança. Exige que o casamento novo reconheça a faceta e que
  `padrao` com o sufixo antigo não a reconheça. A forma é escolhida a partir dos termos
  lidos, não de literal; não havendo nenhuma, o caso fica não executado (PARCIAL).
- **Registro só da sonda.** Monta a executada com N registros e a sonda com N + 1. Exige
  que `registros.csv`, `ordem_triagem.csv` e a contagem da executada tenham N, e que uma
  semente igual ao registro excedente não conte na aderência.

## Riscos / Compromissos

- [Ler a fonte de cada base deixa a derivação dependente de fontes válidas] → é a mesma
  exigência de `procedimentos gerar`. Fonte ilegível sai com PROTOCOLO_ILEGIVEL, nomeando a
  base. Isso é melhor do que derivar com um vocabulário diferente do executado.
- [Somar formas de número numa base que lematiza pode casar registro que a base não
  casou] → aparece como "só no conjunto derivado" na fidelidade, que é onde deve aparecer.
- [Os 2 registros da EB2 da Scopus perdidos pela âncora FCT1 continuam fora] → fica
  divergência residual esperada, medida pela fidelidade; a causa é a mesma do aviso de
  "casamento local não confirmou as âncoras".

## Plano de migração

1. Implementar e rodar o autoteste.
2. Regenerar as saídas da Scopus:
   - `busca derivar`;
   - `conferencia fidelidade EB2` e `conferencia fidelidade EB3`;
   - `aderencia medir`;
   - `conferencia sensibilidade scopus`, que deve sair idêntica.
3. As saídas gravadas em 2026-11-25 estão fora do controle de versão: não há o que
   reverter. A volta atrás é o código anterior.
