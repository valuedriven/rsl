# Proposta

## Why

O pesquisador declarou os quatro instrumentos de controle terminológico (TBCI, UNESCO
Thesaurus, ERIC Thesaurus e Brased) como `Automático`, todos servidos por instâncias TemaTres
em `www.vocabularyserver.com`, e passou a coluna `Caminho` a ser o endereço do serviço
consultado. O código ainda exige um cliente por sigla e trata `Caminho` como referência de
relato: com a tabela nova, o protocolo é ilegível (`eric` e `brased` sem cliente) e nenhum
subcomando que lê o protocolo executa. Além disso, as linhas já gravadas como pendentes de
validação manual nunca seriam consultadas, porque a validação só consulta linha sem
estatuto.

## What Changes

- **BREAKING** `Caminho` passa a ser o endereço do serviço TemaTres consultado, lido do
  protocolo; o endereço deixa de pertencer ao cliente.
- `Caminho` admite o marcador `{idioma}`, resolvido para cada idioma da coluna `Idiomas`
  (UNESCO: `/unesco/{idioma}/services.php`). Marcador desconhecido reprova a leitura.
- **BREAKING** `Automático` passa a significar "consultado pelo cliente TemaTres no endereço
  do `Caminho`". Some a exigência de cliente com o nome da sigla; os clientes `tbci` (fixo)
  e `unesco` (SPARQL oficial) são substituídos por um cliente único.
- Rótulo encontrado com correspondência exata no instrumento é proposto como descritor,
  preferido ou não (decisão do pesquisador). A forma do termo no instrumento — preferido ou
  não preferido — é registrada em coluna própria quando o serviço a informa, e fica vazia
  quando não informa.
- Linha consultada em endereço diferente do resolvido do `Caminho` vigente, ou marcada como
  pendente de validação manual em instrumento hoje `Automático`, volta a aguardar consulta,
  salvo se tiver `decisao_ReT`: essa é preservada e apontada, nunca reaberta em silêncio.
- `termos sondar` passa a sondar cada endereço resolvido (por idioma) e a mostrar se a
  resposta distingue termo preferido de não preferido.
- O modo `Manual` permanece no domínio, com o mesmo comportamento.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `validacao-terminologica`: a semântica de `Automático` e de `Caminho` (endereço do
  serviço, com marcador `{idioma}`), a proposta de estatuto para rótulo encontrado, o
  registro da forma do termo no instrumento, a reabertura da linha consultada em outro
  endereço ou nascida manual, e os casos do autoteste correspondentes.

`gramatica-do-protocolo` e `leitura-do-protocolo` não mudam de requisito: a primeira
declara o mecanismo da gramática, não o domínio de cada coluna, e a segunda só enumera os
campos lidos do instrumento, que continuam os mesmos. A descrição do domínio `Modo` e da
tabela na gramática muda como texto de implementação.

## Impact

- Código: `src/rsl/termos/clientes/` (substituído por cliente TemaTres único),
  `src/rsl/termos/validacao.py`, `src/rsl/termos/planejamento.py`, `src/rsl/leitura.py`
  (instrumentos), `src/rsl/gramatica.py` (descrições), `src/rsl/autoteste/validacao.py` e
  `src/rsl/autoteste/protocolo.py`.
- Configuração: nova coluna em `planilha.campos_validacao` do `config.toml`.
- Dados: `data/validacao_terminologica.csv` — todas as linhas sem decisão voltam a
  aguardar consulta e são reconsultadas; a evidência bruta anterior permanece em
  `data/evidencia/`.
- Protocolo (pelo pesquisador): `Caminho` da UNESCO com `{idioma}` e retirada da
  observação em prosa abaixo da tabela.
- Skill `validacao-vocabulario-controlado`: comandos, regra de `Automático` e coluna nova.
- Pendências: PD32 (via de acesso, termos de uso), PD03, PD05, PD06.
- Fonte externa: `www.vocabularyserver.com` mostrou verificação anti-robô na página HTML;
  os termos de uso não foram conferidos e bloqueiam a validação até o pesquisador
  conferi-los.
