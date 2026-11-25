# Inventário das regras a redistribuir (tarefa 1.2)

Base: as cinco skills de origem do design D6, lidas na versão corrente em 2026-11-25. Cada linha é
uma regra ou bloco de regras com um só destino. Os destinos usam os nomes novos (D5). "Fica" = fica
na skill de origem, já renomeada. "Remissão" = a origem guarda uma linha que aponta o destino.
"Funde" = o destino já enuncia a regra; a cópia da origem sai e não se acrescenta texto.

Marcadores: **[D]** movimento que muda a regra, e não só o lugar dela; vai ao pesquisador antes
de seguir (ver "Decisões" ao fim). **[dup]** duplicação já existente entre skills, registrada aqui
e não tratada, a menos que o movimento passe por ela.

## A. `procedimento-de-busca-por-base` → `gerar-procedimento-de-busca`

| # | Regra (linhas) | Destino |
| --- | --- | --- |
| A1 | Procedimento = protocolo de busca da base; a string da base não é a do protocolo; duas fontes (vocabulário × forma) (8–19) | fica |
| A2 | Escreve-se a fonte, gera-se o procedimento; arquivos da fonte; gramática; ordem quadro → strings → fonte → gerar → gravar → conferir (21–40) | fica |
| A3 | Procedimento operacional: só decisão final, sem exclusão, sem justificativa, sem número em prosa (42–60) | fica |
| A4 | Escopo e remissões às skills vizinhas (62–65) | fica, reescrita como remissão |
| A5 | Tabela de operações; divergência procedimento × protocolo; base nova é decisão de escopo (67–88) | fica |
| A6 | Ler antes de escrever, na ordem (90–107) | fica |
| A7 | Situações de `[[sintaxe]]` e evidência exigida; lastro `(BDn/<id>)` (111–126) | `executar-sondagens-de-sintaxe`; remissão |
| A8 | Roteiro de sondagens em `[[sondagens]]`; registro pelo comando; elemento a `medicao`; `[[regras_de_montagem]]` com situação (128–134) | `executar-sondagens-de-sintaxe` (funde com §1, §4 dela e com B3) |
| A9 | Documentação não é comportamento; sondagem obrigatória antes da 1ª execução (136–139) | `executar-sondagens-de-sintaxe` (funde com B2) |
| A10 | Elementos a apurar (campos, operadores, frase, truncamento, lematização, proximidade, agrupamento, limites, filtros, vocabulário, idioma, exportação) (141–162) | `executar-sondagens-de-sintaxe` |
| A11 | Onde pesquisar: documentação pública, uma página por vez, sem nova tentativa; página que não abriu é pendência (164–169) | `executar-sondagens-de-sintaxe` |
| A12 | Destinos de critério por base (`consulta`, `ancora`, `interface`, `variante`, `aproximado`, `dispensado`, `nao`) e as três regras: busca não restringe além do protocolo; domínio por âncora; dispensar é decisão registrada (171–196) | `definir-criterios-de-elegibilidade`, seção nova "Critério por base"; remissão. A frase "o ano confere-se no retorno" funde com a de `elaborar-expressoes-de-busca` **[dup]** |
| A13 | O que a forma pode e não pode mudar (203–220) | `elaborar-expressoes-de-busca`, Parte 2; remissão |
| A14 | Declaração de cobertura `[cobertura]` e `[[reducao]]` (222–225) | fica (escrita da fonte) |
| A15 | Parâmetros `plural`, `teto`, `morfologia`, `radical`; motivo de redução (227–249) | `plural` → `declarar-flexao-por-base` (funde com §1 dela); `teto` funde com a tabela de `elaborar-expressoes-de-busca`; `morfologia`, `radical` e motivo de redução ficam |
| A16 | `[composicao]`, `[[composicao.facetas]]`, `[[consultas_de_campo]]`, `[[subconjuntos]]` (251–256) | fica (escrita da fonte) |
| A17 | Decisões metodológicas de cobertura são do pesquisador (258–261) | fica |
| A18 | Cinco expressões mantêm composição e contenção; `[[execucao.expressoes]]` e estatuto (265–269) | composição: funde com `elaborar-expressoes-de-busca`; `[[execucao.expressoes]]`: fica |
| A19 | Forma de execução `unica`/`particionada`/`curada`; termo só no singular na curada (270–273) | fica; a frase do singular funde com §3 de `declarar-flexao-por-base` |
| A20 | Regras de montagem (274–275) | fica (funde com A8 no que é situação) |
| A21 | Estratégia de proximidade: o que discutir (276–295) | `elaborar-expressoes-de-busca` (montagem); remissão. O fragmento continua escrito na fonte |
| A22 | `como_executar.md` e `variantes.md` (296–304) | fica |
| A23 | Sementes no procedimento: o gerador lista, a fonte só observa, o estado não entra (308–311) | `compor-conjunto-semente`; remissão |
| A24 | Ressalvas (312–314) | fica |
| A25 | Forma: o que a gramática exige; base nova não muda código (316–325) | fica |
| A26 | Conferir e registrar, passos 1–5 (327–363) | fica |
| A27 | Ao entregar (365–369) | fica |
| A28 | Remissões (371–380) | fica, atualizada |

## B. `execucao-da-busca` → `executar-expressoes-de-busca`

| # | Regra (linhas) | Destino |
| --- | --- | --- |
| B1 | Regras de segurança (8–25) | fica |
| B2 | Sondagem obrigatória antes da 1ª execução; afirmações da ERIC e da BRAPCI sem sondagem (PD27, PD09, PD10) (39–48) | o portão ("antes da 1ª execução, o roteiro") fica em uma linha; o resto vai a `executar-sondagens-de-sintaxe` (funde com A9) |
| B3 | Registro da sondagem: data e hora, retorno, leitura, evidência; o registro imprime a mudança na fonte (50–53) | `executar-sondagens-de-sintaxe` (funde com §3 dela e com A8) |
| B4 | O que executar; só EB4 é definitiva (27–37) | fica |
| B5 | Ao receber as contagens (55–70) | fica |
| B6 | Exportação; ano no retorno; contagem da tela × exportação (72–88) | fica **[dup]** ano no retorno também em `elaborar-expressoes-de-busca` |
| B7 | Registrar (90–100) | fica |

## C. `auditoria-das-strings` → `gerar-strings-de-busca`

| # | Regra (linhas) | Destino |
| --- | --- | --- |
| C1 | Quando usar (8–12) | fica, reescrita para o passo |
| C2 | Princípio: ruído sob a conjunção; sensibilidade e precisão não se trocam termo a termo (14–18) | fica (é o fundamento do critério 7) |
| C3 | §1 Extrair a arquitetura (22–26) | `revisar-projeto` |
| C4 | §2 Diagnóstico mecânico: julgar a saída de `strings gerar` e de `documentos conferir`; rodar antes e depois (28–47) | fica (D1) |
| C5 | §3 Aplicar os onze critérios, na ordem (49–51) | fica |
| C6 | §4 Conferência termo a termo contra o conjunto-semente; perda em número de sementes (53–57) | `revisar-projeto` |
| C7 | §5 Declarar a adaptação por base (59–61) | funde com `gerar-procedimento-de-busca` (A13–A16 já a exigem) |
| C8 | §6 Tabela de emendas: emenda, razão, efeito, risco (63–65) | `revisar-projeto` |
| C9 | §7 Pendências de verificação na execução; teste-piloto (67–69) | `revisar-projeto` |
| C10 | Os onze critérios e a auditoria de rendimento por termo a posteriori (71–103) | fica |
| C11a | Locução, lematização e sinônimos; curinga desliga lematização (109) | `executar-sondagens-de-sintaxe`, elementos a apurar (funde com A10); a enumeração de pares ortográficos funde com o critério 3 (fica) |
| C11b | Derivação automática; mínimo de letras antes do curinga (111) | `executar-sondagens-de-sintaxe` (funde com A10, truncamento) |
| C11c | Precedência; parêntese em torno de cada faceta é obrigatório (113) | `elaborar-expressoes-de-busca` |
| C11d | Limite de operadores varia com o campo; nunca o campo de todos os campos (115) | limite → `executar-sondagens-de-sintaxe` (funde com A10, limites); campo → `elaborar-expressoes-de-busca` |
| C11e | Campos e forma de execução por base; estratificação replicada no cálculo local (117) | funde com o critério 9 (fica) e com A16/A19 |
| C11f | Exportação reprodutível: API pública preferida, parâmetros registrados (119) | `executar-expressoes-de-busca`, Exportação |
| C11g | Bases monodomínio — inversão de âncora (121) | `elaborar-expressoes-de-busca` |
| C11h | Bases regionais e de nicho: teste-piloto; decompor em consultas curtas (123) | teste-piloto → `executar-sondagens-de-sintaxe`; decomposição funde com a forma curada (A19, fica em `gerar-procedimento-de-busca`) |
| C11i | Sempre verificar: curinga em locução, limite de caracteres, diacríticos (125) | `executar-sondagens-de-sintaxe` (funde com A10; diacríticos acrescentado à lista) |
| C12a | Nunca retirar termo para reduzir volume; ordem de tratamento do excesso (129) | fica |
| C12b | Termo que resgata semente sozinho fica (130) | fica |
| C12c | Termos de desfecho não entram na string (131) | `destacar-termos-da-questao` |
| C12d | Teto de triagem com a aritmética que o sustenta (132) | `filtrar-estudos` |
| C12e | Expansão terminológica por IA exige validação humana (133) | `estabelecer-controle-terminologico`; "IA não decide inclusão" funde com `filtrar-estudos` §4 |
| C12f | Limiar informa quando revisar; diagnóstico individual de cada semente perdida (134) | funde com `testar-aderencia-das-expressoes` §3 (anatomia da perda) |
| C12g | Conjunto-semente usado na construção não é medida independente (135) | a independência funde com o papel desenvolvimento/validação (`compor-conjunto-semente` §7, `testar-aderencia-das-expressoes` §2); a prescrição "backward **e forward** search" **não se move**: fica em `gerar-strings-de-busca` e vira pendência em `data/pendencias.json` (diverge do protocolo P11) |
| C13 | Entregáveis; versão enxuta (137–146) | `revisar-projeto` |

## D. `revisao-geral-do-projeto` → `revisar-projeto`

| # | Regra | Destino |
| --- | --- | --- |
| D1 | Produz achados (o parecer confere); não escreve, não acessa fonte, não decide | `revisar-projeto` |
| D2 | §1 Estado; §2 Conferências automáticas, caso não executado não é aprovado; §3 Lastro | `revisar-projeto` |
| D3 | §4 Facetas e strings (lista de cinco pontos) | `revisar-projeto` **[dup]** com os critérios 4, 6 e 8 de `gerar-strings-de-busca`: passa a remeter a eles |
| D4 | §5 Conjunto-semente; §6 Critérios | `revisar-projeto` |
| D5 | Produto; três regras próprias; remissões | `revisar-projeto`; a remissão a `execucao-da-busca` para sintaxe de base passa a `executar-sondagens-de-sintaxe` |

## E. `rastreabilidade` → `revisar-projeto`

| # | Regra | Destino |
| --- | --- | --- |
| E1 | Princípio: garantia por construção | `revisar-projeto`, por remissão ao `AGENTS.md` §8, que já o enuncia **[dup]** |
| E2 | §1 Correspondências que têm de valer, e o que garante cada uma | `revisar-projeto`, seção "Correspondências"; "Garantida por" atualizada com o comando que hoje a garante, ou "conferência manual" (D3) |
| E3 | §2 Método em quatro passos | `revisar-projeto` |
| E4 | §3 Quatro correspondências críticas; defasagem | `revisar-projeto` |
| E5 | "Não há guarda automática neste repositório" | retirada: desatualizada (D3) |
| E6 | Erro de conferência não é defeito do documento | `revisar-projeto` **[dup]** com `AGENTS.md` §8 |
| E7 | §4 Três divergências reais | `revisar-projeto`, encurtada a um parágrafo com os três casos e a lição comum (D4) |
| E8 | §5 Conferir | `revisar-projeto` |

## Decisões

Decididas pelo pesquisador em 2026-11-25: D1 fica em `gerar-strings-de-busca`; D2 distribuir pelos passos, sem mover o forward search; D3 corrigir na fusão; D4 manter encurtados. Registro no design, Open Questions.

- **D1** — C4: o julgamento da saída de `strings gerar` acontece no passo "Gerar as strings", em que
  esse comando é principal. Ficar em `gerar-strings-de-busca` contraria a letra do D6 ("diagnóstico
  para `revisar-projeto`"); ir para `revisar-projeto` tira da skill do passo a leitura do comando
  principal dele.
- **D2** — C11 e C12 não estão no D6. Várias são regras de outros passos ("inversão de âncora em base
  monodomínio" → expressões; "termos de desfecho não entram na string" → destacar termos;
  "expansão por IA exige validação humana" → controle terminológico; "teto de triagem com
  aritmética" → filtrar; "diagnóstico individual da semente perdida" → aderência, que já o tem
  na anatomia da perda). A regra "prescrever ampliação por backward **e forward** search" diverge
  do protocolo (P11: backward de uma geração) e da divisão desenvolvimento/validação que o projeto
  adotou; movê-la para `compor-conjunto-semente` criaria contradição.
- **D3** — E2/E5: "Não há guarda automática neste repositório" está desatualizado: `strings gerar`
  compõe as strings do quadro, `documentos conferir` e `catalogo gerar` conferem. Mover o texto sem
  mudança mantém uma afirmação falsa; corrigi-la muda o conteúdo.
- **D4** — E7: exemplos históricos (o design já os aponta como candidatos a corte).
