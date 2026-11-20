# Design

## Context

A motivação está em `proposal.md`. Os requisitos estão nas specs desta change. O que
condiciona a abordagem, verificado em 2026-11-19:

- **Blocos de `src/protocolo.py`:**

  | Linhas | Bloco |
  | --- | --- |
  | 63–195 | configuração e constantes |
  | 200–330 | Markdown e tabelas |
  | 333–925 | leitura do protocolo |
  | 926–1312 | fichas |
  | 1313–1572 | cobertura |
  | 1572–1900 | análise, conferência e relatório |
  | 1899–2290 | dados alimentados |
  | 2292–3160 | autoteste |
  | 3164–3212 | CLI |

- **Efeitos na importação:**
  - `protocolo.py` lê `CFG` e pode sair com `SystemExit`;
  - `derivar_expressoes.py:79` e `gen_semente.py:39` executam `protocolo.dados()`;
  - `derivar_expressoes.py:395` calcula `_PROBLEMAS_DA_COMPOSICAO`.
- **`ProtocoloInvalido`** é transformado em item da lista de problemas por `conferir()`
  (l. 1719), e por isso sai com o mesmo código da incoerência.
- **Código morto:** `relatorio_bases()` (l. 1868) não é chamada.
- **Duas `normaliza()`:** a de `protocolo.py` usa NFKD; a de `derivar_expressoes.py:130`,
  NFD.
- **Retentativa:** `validar_termos.py:121` (`http()`) repete a requisição depois de erro
  de rede.
- **Estado de `data/`:** contém `historico.md`, `pendencias.json`, `sementes.json` e
  `semente_aderencia.csv`, gerado por `gen_semente.py` e regenerável. Nenhuma outra saída
  existe, então renomear não exige migração de arquivo.
- **Trabalho sem commit:** os números de linha acima são do commit `29e9691`. A árvore de
  trabalho tem alterações sem commit de `conjunto-semente-independente` em `protocolo.py`,
  `derivar_expressoes.py` e `gen_semente.py`. A refatoração parte delas, depois do commit.
- **Estado das conferências:** `--conferir` sai com 0 e `--conferir-dados` sai com 1, por
  falta do `registro_execucao.json` (PD02).
- **Restrição:** só a biblioteca padrão do Python 3.11+.

## Goals / Non-Goals

**Goals:**
- Refatorar sem mudança de resultado, provada por comparação com uma referência gravada
  antes do primeiro passo.
- Fazer cada defeito de forma, de configuração e de dados chegar ao pesquisador com um
  código distinto.

**Non-Goals:**
- Mudar o conteúdo do protocolo, das fichas ou dos critérios de conferência.
- Mudar a forma do conjunto-semente; isso é a change `sementes-estruturadas-no-protocolo`.
- Empacotar para instalação (`pyproject`, `pip install`). O ponto de entrada é
  `python3 -m rsl` com `src/` no caminho. O README declara a forma de chamar.
- Introduzir framework de testes. O autoteste continua sendo a trava, agora num só
  subcomando.

## Decisions

### D1. Estrutura do pacote

```
src/rsl/
  __main__.py      despacho dos subcomandos (argparse com subparsers)
  saida.py         Saida(IntEnum) e a função que termina com o nome do código
  config.py        Configuracao: carregada sob demanda, valida chaves
  contexto.py      Contexto(config, protocolo lido, fichas) criado pelo subcomando
  gramatica.py     declarações de forma; a única fonte dos literais
  markdown.py      secao, tabelas, desescapa, normaliza
  leitura.py       questões, facetas, quadro, instrumentos, strings, expressões,
                   critérios, fontes, sementes
  fichas.py        forma de execução, strings e expressões da ficha, critérios da ficha
  cobertura.py
  conferencia.py   analisa, papéis, conferir
  dados.py         conferir-dados, sincronizar, pendências
  relatorio.py     mostrar, gramatica
  busca/           registrar, derivar, aderência, fidelidade, sensibilidade, leitores RIS/WoS
  termos/          planejamento, planilha, clientes (tbci, unesco), cliente HTTP
  sementes.py      planilha de aderência e ensaio seco
  autoteste/       um módulo por grupo, com o registro de casos
```

A forma de `src/rsl/` com `python3 -m rsl` exige estar em `src/` ou ter `PYTHONPATH=src`.
O README documenta a chamada `PYTHONPATH=src python3 -m rsl …`.

Alternativa considerada: `src/rsl.py` como script único. Foi rejeitada porque manteria um
arquivo grande.

Alternativa considerada: `src/protocolo.py` como fachada. Foi rejeitada por decisão do
pesquisador (2026-11-19): a fachada atende busca, termos e sementes, não só o protocolo.

### D2. Contexto explícito em vez de estado global

Hoje `_CACHE`, `CFG`, `DOC` e `_D` são variáveis de módulo. Passam a atributos de um
`Contexto` que o subcomando cria e passa às funções. O autoteste cria contextos sobre
cópias em memória (texto do protocolo, configuração alterada) sem reimportar módulos,
o que hoje o obriga a carregar `derivar_expressoes.py` por `importlib` (l. 3100).

### D3. Exceções tipadas e um único ponto de saída

Cada falha tem a sua exceção, e cada exceção corresponde a um código:

| Exceção | Código |
| --- | --- |
| `ConfiguracaoInvalida` | CONFIGURACAO |
| `ProtocoloInvalido` | PROTOCOLO_ILEGIVEL |
| `DadosInvalidos` | DADOS |
| `FonteExterna` | FONTE_EXTERNA |

Só `__main__` converte exceção em código. Nenhum módulo chama `sys.exit` nem levanta
`SystemExit`.

`conferir()` deixa de transformar `ProtocoloInvalido` em problema e o propaga. Para o
autoteste, a conferência devolve um `Resultado` com `codigo` e `problemas`, e o caso
compara o código esperado.

Alternativa considerada: manter a lista de problemas e inferir o código pelo texto. Foi
rejeitada por ser conferência por texto, o que contraria a garantia por construção.

### D4. Gramática como dados declarados

`gramatica.py` declara elementos (`Secao`, `Tabela(colunas exigidas)`, `RotuloLinha`,
`Marcador`, `Identificador(prefixo)`, `FrasePadrao(regex, descricao)`). Cada elemento tem
um nome, o documento a que pertence (protocolo ou ficha) e o nível de exigência.

Os leitores recebem o elemento, não o literal. A exceção de forma leva o elemento, e a
mensagem usa o nome dele. `rsl gramatica` percorre as declarações e as imprime.

O autoteste percorre os elementos exigidos e, para cada um, gera a cópia sem ele ou com
ele deformado. Essa geração é garantida por construção: elemento novo sem gerador de
defeito falha o autoteste (spec `gramatica-do-protocolo`).

Alternativa considerada: um `docs/gramatica_protocolo.md` escrito à mão, conferido por
autoteste. Foi rejeitada porque detecta a divergência depois em vez de impedi-la.

### D5. Mutações do autoteste geradas da estrutura

As mutações deixam de procurar literais (`"| SE10 |"`, `"**< 5%**"`). Cada mutação
localiza o alvo pela estrutura já lida: a linha da tabela cujo identificador é o último
`SEn` lido, a célula da coluna `Bases` dessa linha, o trecho em que a faixa de
sensibilidade foi encontrada (posição devolvida pelo leitor). Para isso, os leitores
passam a devolver, além do valor, a localização dele no texto (linha e trecho).

Alternativa considerada: um protocolo de teste fixo em `tests/fixtures/`. Foi rejeitada
porque o requisito vigente é provar as conferências sobre o documento corrente, e um
segundo protocolo para manter divergiria do real.

### D6. Uma `normaliza()`

Fica a NFKD de `protocolo.py`. Antes de unificar, a tarefa 1.2 compara as duas sobre
todos os termos do protocolo e sobre os títulos e resumos das exportações sintéticas. Se
houver diferença, ela é relatada ao pesquisador antes de prosseguir, porque muda o
casamento de termos e, portanto, a derivação.

### D7. Configuração

Os nomes dos arquivos derivados passam a uma seção nova, `[saidas]`, do `config.toml`:
`registros`, `contagens`, `ordem_triagem`, `fidelidade = "fidelidade_{expressao}.csv"`,
`sensibilidade = "sensibilidade_{base}.csv"` e `aderencia`. Os marcadores `{expressao}` e
`{base}` são preenchidos em minúsculas.

Em `[dados]`, `validacao` passa a `data/validacao_terminologica.csv`, e entra
`execucoes = "data/execucoes"`. Chave desconhecida reprova a configuração, como hoje.

### D8. Cliente HTTP sem retentativa

`termos/http.py` faz uma requisição e classifica o resultado em três tipos: resposta útil,
termo ausente ou `FonteExterna`. A pausa entre requisições continua como constante do
cliente (`PAUSA`), porque é política de acesso ao serviço, não parâmetro do projeto. Ela
fica junto do endereço, que também pertence ao cliente (spec `validacao-terminologica`).

A detecção de captcha é heurística, feita por marcadores no corpo da resposta, e está
declarada como tal no código e no README.

### D9. Ordem de migração com referência

Antes de qualquer movimento, grava-se uma referência no scratchpad: a saída de
`--mostrar`, de `--conferir` e dos autotestes, e a derivação, a fidelidade e a
sensibilidade sobre exportações sintéticas. Cada grupo de tarefas termina comparando com
ela. A divergência permitida é só a que as specs nomeiam: nome de arquivo, códigos de
saída e mensagens finais com o nome do código.

## Risks / Trade-offs

- **[Mudança de comando quebra o hábito e as skills]** → a migração do README, das skills
  e das fichas está na mesma tarefa que remove o script antigo. Uma busca por `src/*.py`
  na documentação tem de voltar vazia.
- **[Contagem de casos do autoteste muda com a geração estrutural]** → o resumo nomeia os
  grupos, e a tarefa compara grupo a grupo com a referência. Grupo que perdeu caso tem de
  ser justificado.
- **[`normaliza()` única muda casamento]** → D6: medir antes e perguntar ao pesquisador se
  houver diferença.
- **[Conflito com as changes ativas]** → `revisao-das-strings-por-faceta` tem tarefas de
  código pendentes que citam `src/protocolo.py` e `--conferir`, e elas são reescritas
  para o pacote (tarefa 9.2). As alterações de `conjunto-semente-independente` já estão no
  código: a tarefa 1.0 exige o commit delas antes de gravar a referência, para que a
  referência inclua aderência por papel e o intervalo de Wilson.
- **[Heurística de captcha falha em silêncio]** → o caminho conservador é tratar como
  `FonteExterna` qualquer resposta 200 cujo corpo não seja o formato esperado (JSON ou
  SPARQL JSON). Assim, a falha de reconhecimento interrompe a validação em vez de seguir
  adiante.

## Migration Plan

1. Gravar a referência (D9).
2. Criar o pacote e mover o código por blocos, mantendo os scripts antigos como chamadas
   ao pacote até o grupo 8. Cada bloco termina comparando com a referência.
3. Trocar os códigos de saída e o cliente HTTP.
4. Renomear as saídas e a planilha na configuração.
5. Migrar a documentação e remover os scripts antigos no mesmo passo.

Rollback: até o passo 5, os scripts antigos continuam funcionando. Depois dele, o rollback
é reverter o commit.
