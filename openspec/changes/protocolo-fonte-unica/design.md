# Design

## Context

Motivação em `proposal.md` (Why). Estado atual relevante:

- `src/protocolo.py` (~2.000 linhas) já lê do markdown questões, facetas, quadro, strings,
  expressões, critérios, recorte, limiar, fontes e sementes, mas **também** fixa no código os
  valores esperados (`previsto`, `COMPOSICAO`, `EB4`/`EB5`, `2017`, `0.80`, dimensões, quatro
  QER, mínimo de oito sementes, âncoras) e as listas `RETIRADOS_V2`/`ACRESCENTADOS_V2`.
- Verificado nesta exploração: para cada faceta, `quadro − STR` coincide exatamente com
  `RETIRADOS_V2` (FCT1 24/24, FCT2 22/22, FCT3 0/0, FCT4 8/8). A lista pode ser calculada a
  partir do protocolo.
- `--conferir` reprova hoje: `"Idioma(s)"` (código) × `"Idioma"` (CE3).
- O protocolo tem agora a seção **"Instrumentos para controle terminológico"**, uma linha por
  faceta, nomes separados por vírgula (FCT1: TBCI e UNESCO Thesaurus; FCT2–FCT4: ERIC
  Thesaurus, Brased/INEP e UNESCO Thesaurus). A linha de instrumentos saiu das tabelas do
  quadro, e com ela a dispensa de validação de FCT4. O leitor atual lê a linha antiga da
  tabela (`f["instrumentos"]`, `f["livre"]`) e fixa `INSTRUMENTO_POR_IDIOMA`.
- `validar_termos.py` tem cliente para TBCI e UNESCO; não para ERIC Thesaurus nem Brased/INEP.
- `derivar_expressoes.py` fixa `LIMITE_DIVERGENCIA = 0.10` e `LIMITE_SENSIBILIDADE = (0.05,
  0.15)`. O par 5%/15% está no protocolo (EB5); 10% não está.
- Python 3.12.3; os scripts usam só a biblioteca padrão. O caminho do protocolo é fixado em
  `protocolo.py` (`DOC`) e repetido nos docstrings dos scripts.

## Goals / Non-Goals

**Goals:**
- Nenhum valor de parâmetro fixado no código; o protocolo prevalece sobre o padrão.
- Termo retirado não volta por construção: a STR define o que vale.
- A conferência continua reprovando, com autoteste, todo defeito que reprova hoje, exceto os
  que eram só divergência de valor fixado.
- Nenhuma dependência nova.

**Non-Goals:**
- Mudar conteúdo científico: termos, critérios, limiares e composições permanecem os mesmos.
- Reescrever `derivar_expressoes.py`, `gen_semente.py` ou os clientes TBCI/UNESCO além do
  necessário para ler parâmetros.
- Criar cliente automatizado para ERIC Thesaurus ou Brased/INEP.
- Resumir o texto das skills.

## Decisions

### D1. Vigente = STR do protocolo; o quadro só classifica
`esperado(base, faceta) = {t ∈ STR(faceta) : idioma(t) ∈ idiomas declarados, camada(t) ∈
camadas declaradas}`, com idioma e camada obtidos do quadro. Termo da base é aceito se
corresponde (flexão ou derivação declarada) a um termo de `STR(faceta)`; se corresponde só a
termo do quadro, reprova como "não está na string do protocolo".
*Alternativa:* marcar os retirados no quadro do markdown. Rejeitada: mantém uma segunda
marcação a sincronizar, e a STR já registra o que vale.
*Efeito:* `ACRESCENTADOS_V2` perde a função: o composto está na STR ou não está.

### D2. Conferência de coerência, não de valor
Cada `!= valor` fixado é substituído por uma relação entre partes do documento:
- composição: cada expressão contém as âncoras; a executada é a união das específicas (o
  terceiro grupo é a união dos grupos distintivos); a sonda é a conjunção das âncoras;
- papéis: executada e sonda identificadas pela coluna Natureza da tabela de expressões
  (textos em `[expressoes]` do `config.toml`); mais de uma reprova, nenhuma vale o padrão;
- âncoras: lidas de "Palavras significativas" ("âncora obrigatória");
- recorte, limiar e faixa de sensibilidade: lidos; reprova se o trecho existe e o valor é
  ilegível, ou se incoerente (inferior ≥ superior);
- quantidade de QER e de sementes: sem mínimo fixado; reprova ausência e incoerência entre
  prosa e mapa da distribuição.

### D3. `config.toml`: padrão para todo parâmetro, protocolo prevalece
**Formato: TOML**, lido com `tomllib` (biblioteca padrão desde o Python 3.11; ambiente em
3.12.3). Não há dependência nova, e o comentário é nativo: cada grupo e cada parâmetro se
explica no próprio arquivo. `tomllib` só lê; o `config.toml` é editado pelo pesquisador e
nenhum script o grava.
*Alternativas:* YAML (exige PyYAML) e JSON (biblioteca padrão, sem comentário), ambas
preteridas pelo pesquisador.

**Conteúdo** (nomes finais na implementação):
```
protocolo     "docs/03_protocolo_estrategia_pesquisa.md"
fichas        {wos: {bd, arquivo}, ...}
dados         {sementes, registro, validacao}
expressoes    {composicao: {EB1: [...], ...}, papeis: {executada: "<marcador>", sonda: "<marcador>"}}
ancoras       [FCT1, FCT2]
recorte       {ano_min: 2017}
limiares      {aderencia: 0.80, sensibilidade: [0.05, 0.15],
               divergencia_fidelidade: 0.10, minimo_termos_string: 20}
criterios     {dimensoes: [Intervalo temporal, Idioma, Tipo documental, ...]}
instrumentos  {"Tesauro Brasileiro de Ciência da Informação": {modo: tbci, idiomas: [pt]},
               "UNESCO Thesaurus": {modo: unesco, idiomas: [en, es]},
               "ERIC Thesaurus": {modo: manual, idiomas: [en]},
               "Brased/INEP": {modo: manual, idiomas: [pt]}}
planilha      {campos_validacao: [...], campos_autorais: [...]}
```
**Precedência.** Para cada parâmetro, o leitor tenta o protocolo; se o protocolo declara,
vale o protocolo; se não declara (trecho ausente), vale o padrão. Trecho presente e ilegível
**reprova** — não cai no padrão, para que erro de redação não passe em silêncio. Cada valor
carrega a sua origem, exibida em `--mostrar`.
Parâmetros que só a configuração tem (fichas, dados, mapa de instrumentos, campos da
planilha, marcadores) seguem a mesma regra: o protocolo não os declara, logo vale o padrão.
**Exceção:** a chave `protocolo` (caminho do documento) não admite sobrescrita, porque é ela
que localiza a fonte. `derivar_expressoes.py`, `validar_termos.py` e `gen_semente.py` obtêm o
caminho via `protocolo.py`, e os docstrings passam a remeter ao `config.toml` em vez de
repetir o caminho.
*Fica no código:* a gramática do leitor do markdown (rótulos de camada, `FUNCIONAIS`,
`OPERADORES`, seções da ficha). Não é parâmetro do projeto.

### D4. Instrumentos por faceta, da seção dedicada
O leitor lê a seção "Instrumentos para controle terminológico": `- FCTn: nome, nome, ...`.
Cada nome é casado (normalizado, sem acento e sem caixa) com uma chave de
`config.toml:instrumentos`, que dá o modo e os idiomas cobertos. O termo de uma faceta é
planejado para cada instrumento da faceta cujos idiomas incluam o idioma do termo. Nome sem
chave reprova; faceta do quadro sem linha reprova. A linha de instrumentos das tabelas do
quadro deixa de ser lida.
O nome "IBICT — Tesauro Brasileiro de Ciência da Informação" casa com a chave pelo trecho do
nome do tesauro; o casamento é por inclusão da chave no texto, e duas chaves que casem o
mesmo item reprovam por ambiguidade.
*Termo livre:* o estatuto fixado "faceta declarada termo livre por decisão" sai do código. Com
o protocolo atual nenhuma faceta é dispensada; o termo não localizado num instrumento continua
sendo termo livre, como hoje (`STATUS_NAO_LOCALIZADO`).
*Idiomas por instrumento* são propriedade do instrumento, não da revisão: ficam no
`config.toml`. UNESCO Thesaurus: inglês e espanhol, **informado pelo pesquisador**. TBCI
(pt), ERIC Thesaurus (en) e Brased/INEP (pt) são presunção a conferir na fonte antes de
gravar o padrão.

### D5. `derivar_expressoes.py` lê limiares via `protocolo.py`
`protocolo.py` expõe a faixa de sensibilidade e o limiar de divergência, já resolvidos pela
precedência de D3. `derivar_expressoes.py` troca as duas constantes por essa leitura e nada
mais.

### D6. Documentos: regra de resumo
- Preserva-se intacta toda coluna ou seção cujo título seja "Justificativa".
- No resto, a explicação é reduzida ao que o leitor precisa para executar ou conferir: a regra
  fica, o porquê sai (ou se reduz a uma oração). Histórico ("passou a", "antes", datas de
  decisão, "versão N") sai para `data/historico.md` só quando registra decisão; o que é só
  narrativa sai.
- A Nota de emenda vai inteira, com data, para `data/historico.md`; o item 7 vira uma linha
  em "Expressões de busca".
- README: saem contagens de artefatos e estado observado; ficam estrutura, fluxo, comandos e
  remissão aos parâmetros do protocolo e do `config.toml`.

## Risks / Trade-offs

- **[Padrão mascara omissão no protocolo]** Parâmetro apagado do protocolo passa a valer pelo
  padrão sem aviso → `--mostrar` e `--conferir` listam os parâmetros em uso pelo padrão; o
  pesquisador vê a origem.
- **[Leitura de prosa frágil]** Faixa de sensibilidade e papéis saem de texto livre → trecho
  presente e ilegível reprova; autoteste injeta prosa alterada.
- **[Validação manual extensa]** ERIC Thesaurus e Brased/INEP não têm cliente: os termos de
  FCT2–FCT4 nos idiomas desses instrumentos viram pendência manual → é o que o protocolo
  declara; a pendência aparece em `--pendencias`, sem resolução automática.
- **[Mudança de estatuto de FCT4]** A faceta deixa de ser termo livre por decisão → a mudança
  já está no protocolo; o registro da decisão no histórico é do ReT (tarefa 1.6).
- **[Perda de garantia ao remover autotestes "emenda v2"]** → substituídos por autotestes
  equivalentes sob D1.
- **[Resumo apaga racional útil]** → Justificativa explícita preservada; decisões vão ao
  histórico; o git guarda o texto anterior; o pesquisador revisa o diff por documento.
- **[Exige Python 3.11+]** `tomllib` não existe em versões anteriores → a carga falha com
  mensagem que nomeia a versão mínima; o README a declara.

## Migration Plan

1. Levar o protocolo à forma final antes de mudar o leitor: mover a Nota de emenda para o
   histórico, reescrever o item 7 e resumir o protocolo, preservando os textos de que o leitor
   depende (marcadores de papel, "âncora obrigatória", seção de instrumentos, limiares).
2. Criar `config.toml` (com o caminho do protocolo) e refatorar `protocolo.py`; `--conferir` e `--autoteste` passam.
3. Ajustar `validar_termos.py` e `derivar_expressoes.py`.
4. Resumir os demais documentos e o README; ajustar as skills.
Rollback: `git revert` do conjunto; nenhum dado em `data/` é reescrito pela mudança, exceto
`historico.md`.

## Open Questions

- Nomes finais das chaves do `config.toml` e dos marcadores de papel: podem ser fixados na
  implementação sem alterar specs nem tarefas.
