# Design

## Context

Ver `proposal.md` — Why. O estado que condiciona o desenho:

- o campo `papel` é obrigatório no esquema e alimenta a leitura, a distribuição exibida por
  `configuracao mostrar`, o relato da aderência e a coluna da planilha;
- a aderência medida hoje é 1/10 (1/9 de validação, 11,1%, Wilson 2,0%–43,5%, REPROVADA);
- `diagnostico-das-perdas-da-busca` (em curso) e `registro-completo-da-execucao` (em curso)
  tocam `busca/aderencia.py`; a primeira referencia as sementes por `id` (SE2, SE3, SE4,
  SE7, SE8 na Scopus);
- a planilha `semente_aderencia.csv` não tem nenhuma coluna manual preenchida.

## Goals / Non-Goals

**Goals:**
- Uma única aderência, sobre o conjunto, com o intervalo de Wilson.
- `papel` deixa de existir no esquema, na leitura, na planilha, no relatório e nos testes.
- Um arquivo de sementes com `papel` reprova, em vez de ter o campo ignorado.

**Non-Goals:**
- Substituir a SE4 ou renumerar sementes — change `substituicao-da-se4`.
- Alterar o limiar de 80%, o denominador por base (`indexada`) ou o casamento por prefixo.
- Corrigir a aderência de 1/10.

## Decisions

**D1. Remover o campo, não reduzi-lo a um valor único.** Manter `papel = "validação"`
obrigatório preservaria o vocabulário da divisão e o código que o lê, sem uso. O campo sai
do esquema; o arquivo atual é migrado no mesmo passo. Alternativa rejeitada: manter o campo
com um único valor admitido.

**D2. `papel` vira campo desconhecido e reprova.** O esquema é fechado: campo desconhecido
reprova nomeando a semente e o campo. É garantia por construção — um arquivo antigo falha
alto, em vez de perder o campo em silêncio. Alternativa rejeitada: aceitar e ignorar
`papel` por compatibilidade; o projeto lê só a versão vigente.

**D3. O intervalo de Wilson fica, sobre o conjunto.** O intervalo mede a precisão da
estimativa, não a divisão; retirá-lo junto com o `papel` perderia informação. Ele passa a
ser calculado sobre o mesmo numerador e denominador da aderência única. Alternativa
rejeitada: voltar ao relato sem intervalo.

**D4. Um único relato, com a aderência que decide.** O relato deixa de ter as seções
"validação" e "desenvolvimento" e passa a ter uma proporção, o intervalo e a comparação com
o limiar, identificada como a que decide a passagem. O total deixa de ser "informativo".

**D5. A distribuição por base fica; a por papel sai.** `configuracao mostrar` continua
exibindo a distribuição por base e as incidências, que são o mapa de cobertura; a
distribuição por papel perde o objeto. O mesmo vale para o relatório interno
(`relatorio.py`).

**D6. O requisito "Conjunto de validação não vazio" é removido, não substituído.** A
leitura já exige tabela `[[sementes]]` não vazia; um requisito "conjunto não vazio" seria
duplicação. A remoção não afeta a reprovação de arquivo vazio.

**D7. A planilha perde a coluna `papel` e é regenerada.** A coluna vinha do campo; sem ele,
não há de onde lê-la. As colunas manuais estão vazias hoje; a regravação que perderia
preenchimento manual continua recusada pela regra existente. Alternativa rejeitada: manter
a coluna vazia para compatibilidade — coluna morta.

**D8. A exceção de papel em "Saídas preservadas" é atualizada.** O bloco é um requisito
corrente e citava o relato por papel e a coluna `papel`; deixá-lo intacto seria texto morto.
A garantia de preservação continua para derivação, fidelidade e sensibilidade; na aderência,
a forma corrente é o relato único com intervalo e o prefixo como indício.

**D9. Fora dos IDs.** Esta change não remove nem renumera semente. A SE4 continua na
posição SE4 e como semente — apenas deixa de ter papel. A substituição é a change seguinte,
o que evita conflito com as referências por `id` da change de anatomia.

**D10. Remover os quatro campos de conferência e sobra, e fundir `observacoes` em `nota`.**
`tipo`, `alinhamento` e `eric` estão vazios nas 10 sementes; `observacoes` guarda editores,
evento, local e editora, que cabem no texto livre de `nota`. Manter os campos produz
pendência sem conteúdo (PD01) e uma coluna `tipo` sem uso na planilha. A migração transcreve
o texto de `observacoes` para `nota`, sem perder informação. Alternativa rejeitada: manter
`tipo` para classificação futura — campo vazio não é dado; se a classificação voltar a ser
necessária, entra como campo próprio com decisão registrada.

## Risks / Trade-offs

- **[A aderência de 1/10 continua]** → A change não a apresenta como correção; o proposal e
  o relato dizem que a perda é da `diagnostico-das-perdas-da-busca`.
- **[Conflito com as changes em curso em `busca/aderencia.py`]** → Implementar depois de
  `diagnostico-das-perdas-da-busca` ou coordenar o diff; a mudança é localizada em
  `avalia_aderencia` e no relato, sem tocar no casamento por título nem na leitura de
  execuções.
- **[Arquivo de sementes antigo reprova]** → A remoção dos cinco campos das 10 sementes
  entra no mesmo passo; o erro nomeia a semente e o campo.
- **[Conteúdo de `observacoes` que se perde na fusão]** → A migração transcreve o texto
  para `nota`, semente a semente; a conferência cobre SE4, SE5, SE6 e SE10, as únicas com
  sobra.
- **[Perda de preenchimento manual na planilha]** → Hoje as colunas manuais estão vazias;
  `tipo` é derivada, não manual; a regravação que perderia preenchimento continua recusada,
  sem gravar.

## Migration Plan

1. Remover `papel`, `tipo`, `alinhamento`, `eric` e `observacoes` das 10 tabelas de
   `docs/conjunto_semente.toml`, transcrevendo `observacoes` para `nota`.
2. Remover os campos e o domínio da gramática; ajustar a leitura, as pendências
   (`tipo`/`alinhamento`), a distribuição e o relatório de configuração.
3. Reescrever o relato de aderência e remover as colunas `papel` e `tipo` da planilha.
4. Ajustar os autotestes: remover os casos de papel e de `tipo`/`alinhamento` e cobrir os
   cinco campos retirados como desconhecidos.
5. Atualizar protocolo, skills e guia; regenerar o catálogo.
6. Regenerar a planilha; rodar `documentos conferir`, `dados conferir` e `projeto autoteste`.
7. Registrar a decisão em `data/historico.md`.

Reversão: reverter o commit; a planilha se regenera e o arquivo de sementes volta com o
campo. Não há dado manual a perder.
