#### Partição por recusa da proximidade ou do comprimento

Disparo: a interface recusa o bloco executado por proximidade entre grupos deste tamanho ou por extensão. Forma: partir o grupo 🟦 em subconjuntos, cada um com o grupo 🟨 inteiro, repetindo os filtros em cada parte, e unir por deduplicação. Registrar a partição como adaptação. A emenda declara `- Execução: particionada` e escreve as partes literais.

#### Fracionamento do intervalo temporal

Disparo: execução em bloco falha ou trunca o retorno. Forma: repetir a expressão com cada faixa, unir por deduplicação e registrar o retorno de cada faixa.

```
AND PY=(2017-2021)
AND PY=(2022-2026)
```

#### Idioma

Disparo: sondagem de `LA=` aceita (`TS=ontology AND LA=Portuguese`) e valores conferidos na lista da interface. Forma: anexar ao final da expressão. Valor recusado: aplicar o limite por refinamento e anotar no registro.

```
AND LA=(English OR Portuguese OR Spanish)
```

#### Truncamento

Não usar curinga. Disparo: aderência abaixo do limiar de aderência (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`). Forma: testar `ontolog*`, `educat*`, `contextualiz*`; a adoção exige emenda.

#### Camada de precisão

Disparo: retorno alto demais para a triagem. Aplicar nesta ordem, medindo cada passo contra o conjunto-semente:

1. reduzir a distância de `NEAR/5` entre as âncoras;
2. passar a faceta 🟨 para `AK=` ou `TI=`, mantendo a 🟦 em `TS=`:

```
TS=(<faceta 1>) AND AK=(<faceta 2>) AND PY=(2017-2026)
```

3. refinar por categoria, conferindo os rótulos na interface; declarar a restrição no relatório e compensá-la por *backward search* de uma geração:

```
AND WC=("Education & Educational Research" OR "Education, Scientific Disciplines" OR "Information Science & Library Science" OR "Computer Science, Artificial Intelligence" OR "Computer Science, Information Systems" OR "Computer Science, Interdisciplinary Applications" OR "Computer Science, Theory & Methods")
```

Regra: camada com aderência abaixo do limiar de aderência (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`) é reprovada. Não acrescentar facetas a EB4 para reduzir o retorno.

