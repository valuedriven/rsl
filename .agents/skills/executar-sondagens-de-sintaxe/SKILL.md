---
name: executar-sondagens-de-sintaxe
description: "Executa as sondagens de sintaxe pelo roteiro de cada base (M3/E2): apura como a base trata cada elemento de sintaxe (campo, operador, aspas, truncamento, lematização, proximidade, agrupamento, filtros, limites, exportação), desenha o roteiro, lê e registra cada sondagem e dá ao elemento a sua situação. Use ao apurar a sintaxe de uma base, ao escrever ou revisar o roteiro de sondagens, ao interpretar o retorno de uma sondagem executada e ao decidir que situação o elemento passa a ter."
---

# Executar as sondagens de sintaxe

Uma sondagem responde a **uma** pergunta sobre o comportamento de uma base: "o prefixo de
campo restringe?", "as aspas exigem a sequência?", "o curinga trunca?". Ela existe porque a
documentação de uma base e o seu comportamento divergem com frequência, e uma estratégia de
busca montada sobre comportamento suposto falha em silêncio.

A sondagem é **desenhada antes** de ser executada: objetivo, consultas, o que observar e o
que cada resultado significa ficam escritos no roteiro do procedimento de busca da base. Só
então se executa. Sondagem desenhada depois do resultado justifica o resultado, não o testa.

## 1. O que apurar em cada base

Cada elemento de sintaxe é uma entrada de `[[sintaxe]]` da fonte do procedimento da base, com
**categoria** (as categorias mínimas estão no domínio da gramática; toda base tem ao menos um
elemento de cada) e **situação**. Elementos a apurar, todos — o que a base não tiver se
registra como inexistente, com a fonte da ausência:

- **campos**: rótulo ou *tag*, o que cada um cobre (título, resumo, palavras-chave de autor,
  palavras-chave atribuídas, descritor controlado), e se a restrição de campo funciona de
  fato;
- **operadores**: booleanos, precedência, caixa, operador implícito entre palavras;
- **frase**: aspas, e o que acontece com hífen, barra e parêntese dentro delas; se as aspas
  desligam a lematização e o localizador interno de sinônimos, ou formam locução aproximada,
  que já inclui plurais e admite truncamento, e se há uma segunda forma de locução, exata;
- **truncamento e curinga**: símbolo, mínimo de caracteres antes do curinga, se o curinga
  desliga a lematização (o radical truncado recupera as flexões, mas não a variante
  ortográfica: `color*` não alcança `colour`), se a derivação de radicais está desativada
  (correspondência exata mesmo sem aspas), e se o curinga é aceito dentro de locução entre
  aspas;
- **lematização**: plural regular, irregular, idiomas em que é documentada — e, até ser
  **medida** por sondagem registrada (`declarar-flexao-por-base`), o elemento é
  `nao_verificado` e a fonte declara `plural = "explícito"`;
- **diacríticos**: não presumir que `ontolog*` recupere `ontología`, nem que `prática` e
  `pratica` sejam equivalentes; testar com semente conhecida em cada língua;
- **proximidade**: operador, distância padrão, se aceita grupos de cada lado;
- **agrupamento**: parênteses, mistura de campos num grupo, grupo isolado;
- **limites**: teto de caracteres da consulta — que alimenta `teto` em `[cobertura]` —, de
  operadores booleanos (que pode variar com o campo pesquisado), de conjuntos por sessão, de
  **retorno exibido** e de **exportação**;
- **filtros**: ano, idioma, tipo documental, revisão por pares, texto completo — e para cada
  um **se vai na consulta ou só na interface**, e se convive com o resto da sintaxe;
- **vocabulário controlado** próprio da base e o campo em que opera;
- **idioma de indexação** dos registros;
- **exportação**: formatos, campos incluídos, tamanho do lote.

**Documentação não é comportamento.** Bases já contradisseram a própria documentação —
curinga que devolve zero, operador que zera o retorno quando há grupo, teto de retorno não
anunciado. O que a expressão usa e só a documentação sustenta fica marcado como a medir, e a
sondagem é obrigatória antes da primeira execução numa base. Em base regional ou de nicho, de
capacidade booleana em geral não documentada, sondam-se ao menos parênteses aninhados, aspas,
truncamento e comprimento máximo da consulta.

## 2. Onde pesquisar

Na documentação pública do provedor, que se lê sem autenticação. Ler página pública de ajuda
é consulta, não automação de interface — uma página por vez, **sem nova tentativa após
erro**, e isso se diz expressamente a quem for delegada a leitura. Executar consulta na base
segue as regras de acesso do `AGENTS.md` §9 (§7 desta skill). Página que não abriu
é pendência registrada, nunca "a base não tem".

## 3. Situação de cada elemento e evidência exigida

| Situação | Evidência exigida |
| --- | --- |
| `oficial` | página de ajuda ou documentação do provedor; em `fonte`, o título da página |
| `secundaria` | material de terceiro — treinamento, guia de biblioteca |
| `medicao` | sondagem ou execução registrada, citada em `citacao = "BDn/<id>"` da própria base |
| `nao_verificado` | com `sondagem = "SDn"` do roteiro, ou `sem_sondagem` com o motivo |
| `inexistente` | a fonte da ausência; não localizar não é não existir |

**Toda menção ao registro de execução nomeia a execução ou a sondagem** `(BDn/<id>)`, com
`BDn` da própria base e o `id` existente no registro; a conferência dos dados reprova a fonte
sem esse lastro, e só aquela base. Instrução que apenas manda registrar diz "registro de
execução", sem o caminho.

## 4. O roteiro

Todo elemento `nao_verificado` que se possa testar ganha uma sondagem em `[[sondagens]]` da
fonte: objetivo, pré-requisitos, consultas de controle e de teste, passos, o que observar,
leituras (uma delas inconclusiva) e evidência, desenhados como nas seções 5 e 6. Regra de
montagem que a composição pressupõe vai a `[[regras_de_montagem]]`, com a mesma exigência de
situação.

O roteiro se executa antes da primeira execução numa base, na ordem das dependências. Já se
afirmou que a ERIC não trunca (`ontolog*` devolve 0) e que a BRAPCI tem teto de 1.000
registros no retorno; nenhuma das duas afirmações tem sondagem registrada (PD27, PD09, PD10),
e o roteiro as sonda.

## 5. Desenho

**Uma variável por vez.** Entre o controle e o teste muda uma coisa só: o prefixo, as aspas,
o curinga, o operador. Se mudam duas, a diferença de retorno não diz qual das duas a causou.
Quando a pergunta envolve várias formas (o curinga depois de oito, três e duas letras), cada
forma é um teste contra o mesmo controle.

**Par teste e controle.** O controle é uma consulta cujo comportamento já se conhece ou se
aceita: termo comum, sem o elemento sob teste, com retorno não nulo. O teste é o controle
com a variável alterada. Sem controle não há comparação: um retorno isolado não diz se o
elemento funcionou.

**Tamanho mínimo que expõe o comportamento.** O termo do controle tem retorno grande o
bastante para que a diferença apareça (dezenas, não unidades) e pequeno o bastante para que
os registros possam ser abertos e conferidos. Termo raro demais dá zero nos dois lados e não
distingue nada; termo amplo demais pode bater no teto de retorno da base.

**Conferência nos registros.** O número não basta quando a hipótese é sobre o conteúdo: para
"o prefixo restringe ao título", abrir alguns registros do teste e ver o termo no título;
para "as aspas exigem a sequência", abrir registros que estão só no controle e ver as
palavras separadas. O roteiro diz quantos registros abrir e o que procurar neles.

**Dependência.** Uma sondagem que usa parênteses depende da que verificou os parênteses;
uma que usa o prefixo de campo depende da que verificou o prefixo. A dependência é
declarada, e o roteiro se executa na ordem dela. Se a sondagem de que outra depende não
confirmou o elemento, a dependente não se executa: o resultado dela seria ilegível.

## 6. Leituras

Antes de executar, escrevem-se as **leituras**: cada resultado observável possível, a
conclusão que ele sustenta e a situação que o elemento passa a ter. Toda sondagem tem ao
menos duas leituras, e uma delas é a **inconclusiva**, que deixa o elemento não verificado.

**Leitura distinguível.** Cada leitura se decide pelo que se observa, sem interpretação:
"teste = 0 sem mensagem", "0 < teste < controle e os registros abertos têm o termo no
título". Leitura que exige juízo ("o retorno parece razoável") não é leitura.

**Zero sem erro é ambíguo.** Retorno zero sem mensagem pode significar que o elemento não
existe, que a sintaxe foi recusada em silêncio, que o termo não ocorre ou que a sessão
falhou. Por isso zero sem erro só confirma uma hipótese quando o controle, na mesma sessão,
tem retorno não nulo e a sondagem foi desenhada para que o zero só possa ter uma causa;
caso contrário, é leitura inconclusiva.

**Resultado que contradiz a estratégia.** Quando o resultado contradiz uma regra em que a
composição da busca se apoia, a leitura não muda a situação sozinha: ela leva ao
pesquisador, porque a correção é decisão de método, não de registro.

**Medido não quer dizer que funciona.** A situação "verificado por medição" diz como o
elemento foi verificado, não que ele funciona. "O curinga não trunca no título" é resultado
medido. A conclusão da leitura diz o que se mediu.

## 7. Evidência

Sondagem sem evidência não é sondagem. A evidência mínima é a captura da tela de cada
consulta, com a consulta e o retorno visíveis; quando a leitura depende dos registros, a
captura dos registros abertos; quando a sondagem é de exportação, o arquivo exportado.

Registram-se também a data e a hora em que a sondagem foi feita, não as do registro, e o
texto efetivamente submetido, quando difere do roteiro (a interface que reescreve a
consulta, um termo trocado por necessidade). O retorno se anota como veio, sem
arredondar.

A sondagem se registra pelo comando do projeto (sinopse em `docs/procedimentos.md`), com a
data e a hora, o retorno de cada consulta, a leitura observada e a evidência.

A sondagem se executa na sessão do pesquisador, com o acesso dele, uma consulta por vez,
sem nova tentativa automática. Captcha, aviso de atividade atípica ou bloqueio interrompem
a sondagem, e a interrupção se registra.

## 8. Do resultado à situação

Registrado o resultado, o elemento passa à situação da leitura observada, com a citação do
registro. O registro imprime a mudança a aplicar na fonte do procedimento; aplicá-la e
regenerar o procedimento. Elemento que continua não verificado mantém a sondagem no roteiro, ou ganha o
motivo de não a ter.

Elemento sem sondagem precisa de motivo escrito: verificação documental, recurso que
nenhuma consulta usa, recurso que não se localiza na interface. Não localizar não é não
existir: falha de acesso deixa o elemento não verificado, nunca inexistente.

## 9. O que uma sondagem não autoriza

- **Generalizar de um termo para todos.** O curinga que trunca `ontolog*` pode não truncar
  um termo curto; a lematização que casa `ontology` e `ontologies` pode não casar plural
  irregular. A conclusão vale para a forma testada, e a extensão a outras é hipótese.
- **Generalizar de um campo para outro, ou de um idioma para outro.** Lematização medida em
  inglês não diz nada do português.
- **Transferir resultado entre bases**, nem entre interfaces da mesma base (busca simples,
  avançada, API).
- **Valer para sempre.** Bases mudam de comportamento; a sondagem tem data, e a mudança das
  expressões de busca exige repetir as sondagens pertinentes.
- **Reconstruir sondagem antiga.** Resultado sem evidência guardada não se transcreve de
  memória nem de prosa: a sondagem se refaz.

## 10. Revisão de um roteiro

Ao revisar o roteiro de uma base, conferir, sondagem a sondagem:

- a pergunta é uma só e o objetivo a diz;
- controle e teste diferem por uma variável, e o controle tem retorno não nulo esperado;
- as leituras cobrem os resultados possíveis, e uma é inconclusiva;
- nenhuma leitura depende de juízo;
- o zero sem erro só conclui quando o desenho o torna inequívoco;
- a evidência pedida basta para outra pessoa refazer a leitura;
- as dependências estão declaradas e não há ciclo;
- todo elemento não verificado tem sondagem ou motivo.
