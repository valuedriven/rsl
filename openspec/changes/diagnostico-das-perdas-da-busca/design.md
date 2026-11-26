# Design

## Contexto

A motivação está na proposta. O que já existe e é reaproveitado:

- **Composição por base.** `procedimentos.composicao_da_base(ctx, d, sigla)` devolve a
  `Composicao` da base. Dela vêm:
  - o texto de cada expressão (`comp.expressoes[EBn]["consultas"]`);
  - as cláusulas de filtro de destino `consulta` (`comp.clausulas`);
  - os critérios de destino `interface`, na fonte.

  `Composicao.resolve` já aplica `sem_proximidade` a uma expressão referida por sondagem:
  une as âncoras por `AND` no lugar do operador. É a transformação do nível 3.
- **Sementes.** O arquivo de sementes (`[documentos] sementes`) traz DOI, título e bases
  esperadas. `aderencia.chave_titulo`/`casa_titulo` dão o casamento exato por título que
  decide "recuperada".
- **Execuções registradas.** `registro.carrega_consultas` e
  `sensibilidade.registros_da_expressao(base, ident, validas)` leem as exportações de uma
  expressão numa base. `leitores.le_arquivo` lê RIS e as demais formas aceitas.
- **Casamento local.** `derivacao.vocabulario_da_base`, `padrao` e `texto_do` (change
  `derivacao-com-formas-da-base-e-sem-sonda`).
- **Amostra.** `sensibilidade_<base>.csv` (`chave;ano;titulo;doi;amostra;elegivel`),
  chaveado por `registro.chave_dedup`.
- **Intervalo.** `aderencia.wilson`.

Restrições:

- Nenhum valor de base no código (spec `fonte-do-procedimento`).
- Consulta às bases só no navegador do pesquisador (AGENTS.md §9).
- Nomes de comando e de arquivo pela convenção (spec `interface-de-comando`).
- Todo comando ancorado num passo do guia (spec `catalogo-de-apoio`).

## Objetivos / Fora do escopo

**Objetivos:**

- o texto de cada nível sai da mesma composição que gerou as consultas executadas, sem cópia
  à mão;
- a causa de cada semente é calculada a partir das exportações, e nunca a olho;
- o custo de cada ampliação do vocabulário é calculado sobre a mesma perda que a
  sensibilidade mediu.

**Fora do escopo:**

- extrapolar para a perda inteira a fração de elegíveis da amostra (o relato dá a amostra e
  o intervalo);
- candidatos por n-gramas de título e resumo (decisão 5);
- persistir o diagnóstico no registro de execução.

## Decisões

### 1. Níveis cumulativos, com os DOIs agrupados

Uma consulta por nível, com todos os DOIs diagnosticados: `(<doi a> OR <doi b> …)`, em que
cada `<doi x>` é o modelo `[composicao] doi` com `{doi}` substituído. Os níveis são:

| Nível | Texto | Causa se o DOI some |
|---|---|---|
| 1 | `D` | não indexada |
| 2 | `D AND <cláusulas>` (+ filtros de interface relatados) | filtro |
| 3 | `D AND <sonda sem proximidade>` | âncoras |
| 4 | `D AND <sonda>` | proximidade |
| 5 | `D AND <executada>` | faceta não âncora |

O texto da sonda já contém as cláusulas, então os níveis 3 a 5 acumulam o 2. Sem
proximidade, os textos 3 e 4 coincidem, e o nível se funde.

*Alternativas:*

- **Quatro consultas por semente, como na tabela de hoje.** São até 20 submissões, com o
  mesmo poder de atribuição. Descartada.
- **Manter a consulta 3 da tabela atual (DOI + âncoras, sem filtros).** Ela não acumula o
  nível 2, e a "primeira que devolve zero" deixa de nomear uma causa só. Descartada. A
  inconsistência da tabela atual se corrige por esta change.

### 2. Níveis com execução registrada são lidos, não submetidos

Os níveis 4 e 5 são a sonda e a executada restritas aos DOIs. Com execução válida registrada
da expressão, filtra-se a exportação pelos DOIs, e o pesquisador submete só os níveis 1 a 3.

*Alternativa:* submeter os cinco níveis. Seria redundante com exportações do mesmo dia e
custaria mais duas submissões. Descartada, com o risco abaixo.

### 3. Duas fases no mesmo comando

- Sem `--retorno`, o comando imprime o roteiro e não grava nada.
- Com `--retorno N K` (um por nível submetido), `--exportacao N ARQ` (quando K > 0) e
  `--data-hora`, ele confere e grava.

O mesmo comando nas duas fases garante que o texto conferido é o texto impresso, pela mesma
composição. As exportações ficam onde o pesquisador as salvou; recomenda-se
`[dados] evidencia`/`anatomia/<base>/`, e o caminho vai para `anatomia_consultas_<base>.csv`.

*Alternativa:* registrar como sondagem em `registro_execucao.json`. As consultas de sondagem
são declaradas na fonte e fixas, e os DOIs aqui dependem da medição. Mudaria o esquema do
registro e de `dados conferir`. Descartada.

### 4. Conferência entre níveis por construção do resultado

Os DOIs são normalizados: caixa baixa, sem o prefixo `https://doi.org/`. Antes de atribuir
causa, o comando confere:

- cada nível contém só DOIs diagnosticados;
- cada nível é subconjunto do anterior.

Se a consulta submetida não for a montada, ou se a base mudou entre os níveis, a
incoerência reprova, em vez de produzir uma causa errada.

### 5. Candidatos pelas palavras-chave dos elegíveis

Os candidatos são as palavras-chave (campo de palavras-chave da exportação, separadas por
`;`) dos elegíveis da amostra, normalizadas, menos as que algum padrão do vocabulário da
base reconhece. O alcance de cada candidato se mede com `padrao(candidato)` sobre `texto_do`,
como `TITLE-ABS-KEY`.

*Alternativa:* n-gramas de título e resumo. Exigiria lista de palavras vazias por idioma e
geraria ruído. Palavra-chave já é termo atribuído. Descartada; qualquer termo fora da lista
se testa por `--termo`.

### 6. Simulação sobre a perda, não sobre a sonda inteira

A perda P é a sonda menos a executada. Acrescentar termos a uma faceta não âncora traz para
a executada os registros de P em que algum termo novo casa. Os registros da executada já
estão nela e não contam. A sonda e a executada têm as mesmas âncoras e a mesma proximidade
(conferido na Scopus), então P é exatamente o universo do acréscimo. Âncora não se simula
(USO): ampliá-la sai do universo da sonda.

### 7. Lugar dos comandos

- `aderencia diagnosticar`: o grupo `aderencia` é o das sementes.
- `conferencia simular`: a análise segue a `conferencia sensibilidade` e lê a saída dela.

Os dois se ancoram no guia (`docs/procedimentos.md`): no passo de medir a aderência e no
passo da sonda de sensibilidade.

Os módulos novos são `busca/anatomia.py` e `busca/simulacao.py`. As chaves novas de
`config.toml` são:

```toml
[saidas]
anatomia = "anatomia_{base}.csv"
anatomia_consultas = "anatomia_consultas_{base}.csv"
candidatos = "candidatos_{base}.csv"
```

## Riscos / Compromissos

- [A base muda entre a execução registrada (níveis 4 e 5) e a submissão dos níveis 1 a 3: o
  DOI aparece no 3 e não no 4 por indexação nova, não por proximidade] → o relato compara a
  data das execuções lidas com `--data-hora` e avisa quando diferem. A causa `proximidade`
  com datas diferentes sai marcada como a conferir.
- [O agrupamento de `DOI()` por `OR` não está medido na Scopus] → a conferência da decisão 4
  reprova DOI estranho. Retorno do nível 1 menor que o número de DOIs não reprova: é a
  própria medida de indexação. A sintaxe do modelo fica declarada em `[[sintaxe]]` com a
  situação que tiver.
- [Consulta longa: o nível 5 é EB4 inteira mais os DOIs] → na Scopus o nível 5 é lido da
  exportação e não se submete; o nível 3, o mais longo submetido, é EB5 mais os DOIs, perto
  dos 2.655 caracteres de EB4, que foram aceitos. O diagnóstico relata o comprimento de cada
  nível submetido e avisa quando passa do teto declarado na fonte (`[cobertura] teto`).
- [Palavras-chave em inglês, enquanto o protocolo exige pt/en/es] → o candidato é indício
  para o pesquisador. A tradução e a validação terminológica seguem o fluxo de termos, fora
  deste comando.
- [Amostra de 53 registros] → números da amostra com intervalo de Wilson. O acréscimo é
  contado no conjunto inteiro da perda, e não estimado.

## Plano de migração

1. Declarar `[composicao] doi` na fonte da Scopus e um elemento `[[sintaxe]]` "Restrição
   por DOI", com a situação conferida na fonte oficial da Scopus no momento da declaração
   (`oficial`, com a citação) ou `nao_verificado`. Não se preenche de memória.
2. Implementar, rodar o autoteste e regenerar procedimentos e catálogo.
3. Executar o roteiro da Scopus (README da change).

Volta atrás: o código anterior. As saídas novas são regeráveis e não substituem nenhuma
existente.
