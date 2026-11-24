# Tasks

## 1. Condição de acesso (pesquisador)

- [x] 1.1 Pesquisador confere no próprio navegador os termos de uso e as condições de acesso programático de `www.vocabularyserver.com` (`services.php`) e registra o resultado. Bloqueia os grupos 5 e 6. Verificar pela existência do registro (design D7); a PD32 é atualizada na 6.3.

## 2. Endereço lido do protocolo

- [x] 2.1 Em `leitura.py`, retirar a exigência de cliente com o nome da sigla e reprovar marcador entre chaves diferente de `{idioma}` no `Caminho`, nomeando o instrumento e o marcador; atualizar as descrições de `T_INSTRUMENTOS` e `D_MODO` em `gramatica.py`. Verificar com `documentos gramatica`, que mostra o marcador e não fala em cliente por sigla, e com `configuracao mostrar`, que deixa de sair com PROTOCOLO_ILEGIVEL.
- [x] 2.2 Resolver o endereço por instrumento e idioma no planejamento (design D2), devolvido junto com o instrumento. Verificar com caso de autoteste: termo `es` da UNESCO resolve para `/unesco/es/services.php`, sem `{idioma}` nem `/en/`, e marcador desconhecido reprova com PROTOCOLO_ILEGIVEL.
- [x] 2.3 Trocar o caso "instrumento Automático sem cliente" de `autoteste/protocolo.py` pelo caso do marcador desconhecido e demonstrar que ele reprova desfazendo temporariamente a verificação e vendo o autoteste falhar. Verificar com `projeto autoteste` sem falha.

## 3. Cliente TemaTres único

- [x] 3.1 Substituir `termos/clientes/` por um cliente TemaTres que recebe o endereço resolvido, a partir da lógica atual do `tbci` (design D1); retirar o cliente SPARQL da UNESCO. `versao_instrumento` passa a trazer título e `lastMod` de `fetchVocabularyData`. Verificar que `grep -rn "vocabularyserver\|vocabularies.unesco" src/rsl` não acha endereço fixo e que `termos validar xyz` com sigla fora do protocolo sai com USO.
- [x] 3.2 Acrescentar `verifying your browser` e `just a moment` aos marcadores de bloqueio de `termos/http.py` (design D6). Verificar com caso de autoteste sobre corpo em memória que essas páginas levantam FonteExterna.
- [x] 3.3 Proposta de estatuto: casamento exato, preferido ou não, gera estatuto de descritor; sem casamento, termo livre não localizado (requisito "Rótulo encontrado é proposto como descritor"). Verificar com casos de autoteste sobre respostas TemaTres em memória.

## 4. Reabertura e planilha

- [x] 4.1 Acrescentar `forma_no_instrumento` a `planilha.campos_validacao` no `config.toml`, depois de `rotulo_autorizado`, e preencher só com o que o serviço informar (design D3). Verificar com `termos exportar` sobre cópia em `RSL_CONFIG` de ensaio, que traz a coluna, e que as linhas existentes a recebem vazia.
- [x] 4.2 Reabertura em `carrega()` (design D4): linha sem decisão, de instrumento `Automático`, pendente manual ou com `url_consultada` fora do endereço resolvido vigente, volta a aguardar consulta; com decisão, é preservada e listada. Verificar com os casos do requisito "Autoteste prova endereço resolvido e reabertura", demonstrando que o autoteste falha com a regra desligada.
- [x] 4.3 Refazer o caso de modo manual de `autoteste/validacao.py` sobre cópia alterada, sem exigir instrumento `Manual` no protocolo vigente. Verificar com `projeto autoteste` sem falha sobre o protocolo só com instrumentos `Automático`.
- [x] 4.4 Atualizar a skill `validacao-vocabulario-controlado` (§1 regra de `Automático` e `Caminho`, §4 coluna nova, §5 comandos) e os textos de ajuda de `termos` em `__main__.py`. Verificar com `catalogo gerar` sem divergência.

## 5. Protocolo e sondagem

- [x] 5.1 (Tabela ajustada pelo pesquisador em 2026-11-24; falta a verificação, que depende da 2.1.) Pesquisador troca, na linha da UNESCO, `/en/` por `/{idioma}/` e retira a observação abaixo da tabela. Verificar com `configuracao mostrar` (os dois endereços resolvidos da UNESCO) e `documentos conferir`.
- [x] 5.2 Com a 1.1 concluída, `termos sondar`, uma requisição por vez. Verificar na saída: os cinco endereços resolvidos respondem JSON TemaTres, o termo inexistente não casa, e se a resposta distingue termo não preferido. Parada em FONTE_EXTERNA encerra a tarefa e volta ao pesquisador.
- [x] 5.3 Ajustar o preenchimento de `forma_no_instrumento` ao que a sonda mediu, ou deixá-lo vazio com a observação, se a resposta não distinguir. Verificar com caso de autoteste sobre o payload capturado na sonda.

## 6. Validação refeita

- [x] 6.1 `termos exportar` e conferência de que toda linha sem decisão aguarda consulta. Verificar contando na planilha, por instrumento, as linhas com `status_proposto` vazio, e conferindo que não há linha pendente de validação manual.
- [x] 6.2 `termos validar todos`. Verificar que toda linha tem `url_consultada` no endereço resolvido vigente e `arquivo_evidencia` existente em `data/evidencia/`; parada em FONTE_EXTERNA é relatada ao pesquisador, sem nova tentativa.
- [x] 6.3 Atualizar PD03, PD05, PD06 e PD32 em `data/pendencias.json` (consulta automatizada feita; idiomas declarados pelas instâncias, como evidência da cópia), excluindo a que ficar resolvida e levando ao registro devido o que a encerrou. Verificar com `projeto pendencias`.

## 7. Integração

- [x] 7.1 `projeto autoteste`, `documentos conferir` e `catalogo gerar` sem falha; `openspec validate validacao-terminologica-por-servico-tematres --strict` válido.

## Workflow follow-up

- Arquivar a change depois da revisão do pesquisador e sincronizar a spec `validacao-terminologica`.
