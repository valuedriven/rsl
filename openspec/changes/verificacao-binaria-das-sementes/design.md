# Design

## Decisões

### 1. Tipo booleano no esquema, não vocabulário controlado de texto

O estado é binário: conferido ou pendente. Um vocabulário de texto ("CONFIRMADA",
"A CONFERIR") repete o defeito, porque a redação volta a decidir o estado. O tipo
booleano do TOML impede o defeito na leitura: `verificacao = "CONFIRMADA"` reprova.

*Alternativa:* aceitar as duas redações no contador. Corrige o caso visto e deixa a
próxima redação contar errado em silêncio. Descartada.

### 2. Ausente é pendente

Campo opcional ausente vale `false`. Assim semente nova sem conferência aparece em
`projeto pendencias` sem exigir que se escreva `false`.

### 3. O texto da verificação vai para `nota`

O texto trazia onde e como se conferiu (página oficial, Crossref, data, evidência bruta).
Perdê-lo quebraria a rastreabilidade da conferência. A `nota` já reunia esse registro;
o texto vai para o início dela, sem o prefixo de estado, que o booleano substitui.

## Riscos

- [Arquivo de sementes antigo, com texto] → reprova alto, nomeando a semente e o campo.
