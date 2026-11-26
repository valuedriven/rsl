# Desenho

## Contexto

`conferencia sensibilidade` já recebe a base e lê, por `registros_da_expressao`, as
exportações registradas de uma expressão numa base. A fidelidade passa a seguir o mesmo
padrão e reutiliza essa função para a execução direta registrada.

## Decisões

1. **Base obrigatória, arquivo opcional.** A base é o que impede a mistura, por construção.
   O arquivo fica opcional porque a execução direta já está no registro. A alternativa de
   deduzir a base do arquivo registrado não cobriria o arquivo não registrado.
2. **Trechos em vez de texto único.** `segmentos_do` devolve o título, o resumo e cada
   palavra-chave, normalizados à parte. `texto_do` continua existindo para o autoteste que
   reproduz o casamento antigo. O separador `SEPARADOR_VALORES` mora em `leitores.py`, que
   o usa ao unir valores, e o casamento o importa: os dois lados não divergem.
3. **Saída com as duas chaves.** `MARCADORES` admite mais de um marcador por padrão, e a
   configuração sem um deles é recusada.

## Riscos / Compromissos

- [Palavra-chave que contenha `;` no próprio valor] → seria partida em duas. Nenhuma
  exportação conhecida faz isso.
- [Frase que atravessa pontuação dentro do resumo] → continua casando, porque não se
  verificou como as bases a tratam; fica fora do escopo.
