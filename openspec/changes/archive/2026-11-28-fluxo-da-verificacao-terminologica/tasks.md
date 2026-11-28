# Tasks

## 1. Configuração e esquema

- [x] 1.1 Em `src/rsl/config.py`, acrescentar `[dados] consulta_terminologica` ao esquema,
  retirar `[planilha]` e registrar `planilha.campos_validacao` e `planilha` em `RETIRADAS`,
  com mensagem que nomeia as duas chaves novas. Verificar: `python3 -m rsl projeto autoteste`
  prova os casos de chave ausente e de seção retirada, e o autoteste falha antes da mudança
  de código.
- [x] 1.2 Em `config.toml`, apontar `[dados] validacao` para
  `data/validacao_terminologica.toml`, acrescentar `[dados] consulta_terminologica =
  "data/consulta_terminologica.json"`, remover a seção `[planilha]` e atualizar os
  comentários do arquivo. Verificar: `python3 -m rsl configuracao mostrar` sai com OK e
  mostra os dois caminhos; um `config.toml` de ensaio com `[planilha]` sai com CONFIGURACAO
  nomeando as chaves novas.

## 2. Formatos e expurgo

- [x] 2.1 Criar `src/rsl/termos/registro.py` com a chave lógica, a leitura e a escrita
  estritas do TOML de decisões e do JSON de resultado técnico, incluindo a omissão de campo
  vazio e a validação de identificação, campo desconhecido, chave duplicada e
  `data_decisao` em `AAAA-MM-DD`. Verificar: autoteste de ida e volta com acento, aspas,
  barra invertida, quebra de linha e `#`; TOML e JSON ilegíveis terminam com DADOS; tabela
  sem decisão não é escrita.
- [x] 2.2 Implementar em `registro.py` o cálculo do caminho esperado da evidência para todas
  as chaves do protocolo e o expurgo dos arquivos gerenciados (`<instrumento>/<16 hex>.json`)
  que não pertencem a chave alguma, preservando as pastas reservadas (`instrumentos`,
  `sondagens`, `openalex`, `crossref`, `referencias`, `zotero`) e bloqueando o expurgo quando
  uma linha consultada aponta evidência ausente. Verificar: autoteste em diretório temporário
  cobre termo retirado, linha reaberta, reconsulta, arquivo de outro tipo e referência
  ausente; os arquivos alheios permanecem byte a byte.
- [x] 2.3 Documentar no docstring de `registro.py` a forma dos dois arquivos, a chave, a
  regra de expurgo e o que não se edita à mão. Verificar: `python3 -m rsl documentos
  gramatica` continua sem citar o formato interno e a ajuda não promete campo inexistente.

## 3. Fluxo da validação

- [x] 3.1 Refatorar `src/rsl/termos/validacao.py`: `carrega` combina decisões e resultado
  técnico; `grava_registros` grava os dois arquivos e expurga; `validar` consulta pendentes e
  grava só o resultado técnico e a evidência; `exportar` e `importar` reconstroem os dois
  arquivos, preservam a decisão de chave do protocolo, removem a decisão fora do protocolo e
  retiram a linha técnica órfã. Verificar: `python3 -m rsl projeto autoteste` cobre
  reabertura pelos três motivos, decisão de chave do protocolo preservada, decisão fora do
  protocolo removida, órfã técnica retirada e `termos validar` sem tocar no arquivo de
  decisões.
- [x] 3.2 Ajustar `src/rsl/termos/decisao.py` e `src/rsl/coerencia.py` para ler decisões do
  TOML, mantendo o domínio, a precedência e o cálculo da linha do CT. Verificar:
  `python3 -m rsl documentos conferir` sai com OK no protocolo corrente, e uma cópia em
  memória com decisão fora do domínio reprova nomeando termo, faceta, idioma e instrumento.
- [x] 3.3 Ajustar `src/rsl/dados.py` para `projeto pendencias` contar as linhas sem
  `status_proposto` e as pendências manuais a partir do protocolo e do resultado técnico, sem
  ler CSV. Verificar: `python3 -m rsl projeto pendencias` sai com OK e relata as mesmas
  pendências que o registro atual; um protocolo de ensaio com instrumento `Manual` produz a
  pendência manual sem gravar linha no JSON.
- [x] 3.4 Substituir `texto_validacao`/`com_validacao` por `texto_decisoes`/`com_decisoes` e
  `texto_resultado`/`com_resultado` em `src/rsl/contexto.py`, e adaptar `src/rsl/autoteste/
  validacao.py` e a ajuda de `src/rsl/__main__.py`. Verificar: `python3 -m rsl projeto
  autoteste` passa, e `python3 -m rsl termos exportar -h` descreve os dois registros, sem
  citar planilha ou CSV.
- [x] 3.5 Acrescentar ao autoteste os casos novos de forma: decisão sem consulta, consulta
  sem decisão, decisão de termo fora do protocolo removida, linha técnica órfã retirada,
  `termos importar` com decisão fora do protocolo termina em OK e `termos exportar` com
  decisão fora do protocolo termina em OK, com a remoção informada.
  Verificar: cada caso novo falha quando a regra correspondente é desligada de propósito.

## 4. Migração do registro legado

- [x] 4.1 Escrever um script descartável de conversão do CSV legado para TOML e JSON, sem o
  commitar no pacote, e conferir campo a campo: toda linha com decisão de chave do protocolo
  vira tabela; a decisão de chave fora do protocolo é removida; toda linha com conteúdo
  técnico de chave do protocolo vira objeto; o mapa `(faceta, idioma, termo)` → linha do CT é
  idêntico ao calculado do CSV; toda referência de evidência existe. Verificar: o relatório
  da conversão não tem divergência e o CSV ainda não foi removido.
- [x] 4.2 Com a configuração nova, rodar `python3 -m rsl termos exportar` duas vezes e
  conferir que a segunda não altera os arquivos; rodar `documentos conferir`, `dados
  conferir`, `projeto autoteste` e `projeto pendencias`. Verificar: todos saem com OK, e a
  árvore de evidência só contém arquivo referenciado ou de chave do protocolo.
- [x] 4.3 Remover `data/validacao_terminologica.csv` e conferir que nenhum arquivo de
  `src/`, `docs/`, `.agents/skills/`, `README.md` ou `config.toml` o cita como fonte vigente.
  Verificar: `grep -R "validacao_terminologica.csv\|campos_validacao"` não encontra
  ocorrência fora do histórico de changes; `documentos conferir` continua OK.

## 5. Documentação e skills

- [x] 5.1 Atualizar o mapa do `README.md`: substituir a linha do CSV pelas linhas do arquivo
  de decisões, do resultado técnico e da evidência vigente, e ajustar a precedência que
  chama a planilha de exceção à regra "altera-se a fonte, não a saída". Verificar: o mapa
  cita os dois caminhos e a evidência; nenhum caminho aparece duas vezes.
- [x] 5.2 Revisar `.agents/skills/estabelecer-controle-terminologico/SKILL.md`: substituir a
  seção 4 (o registro é o instrumento) pela descrição dos dois arquivos, atualizar a regra de
  reabertura, a tabela de comandos, os campos que decidem e a evidência vigente; remover
  "Não há JSON intermediário". Verificar: a skill cita `[dados] validacao`, `[dados]
  consulta_terminologica`, o TOML editável, o JSON não editável e o expurgo; os comandos da
  tabela existem em `python3 -m rsl`.
- [x] 5.3 Atualizar as referências ao formato antigo em `docs/procedimentos.md`,
  `.agents/skills/destacar-termos-da-questao/SKILL.md` e `docs/01_plano.md` (registro de
  validação, não planilha), e regravar o catálogo de apoio. Verificar: `python3 -m rsl
  catalogo gerar` sem `--gravar` não reprova; `python3 -m rsl catalogo gerar --gravar`
  atualiza `docs/catalogo_de_apoio.md` e a descrição de `termos exportar` deixa de dizer
  "planilha".
- [x] 5.4 Fazer a varredura final de "planilha de validação", "validacao_terminologica.csv" e
  "campos_validacao" em `src/`, `docs/`, `.agents/skills/`, `README.md` e `config.toml`.
  Verificar: só restam ocorrências em registros históricos (`openspec/changes/archive/...`,
  `data/historico.md`), e cada uma é justificada como registro do que vigorava.

## 6. Integração

- [x] 6.1 Executar a sequência completa no projeto: `configuracao mostrar`, `documentos
  conferir`, `dados conferir`, `projeto autoteste`, `projeto pendencias` e `termos exportar`.
  Verificar: os códigos de saída são OK (ou PARCIAL só se houver caso não executado
  declarado), e `termos exportar` é idempotente.
- [x] 6.2 Conferir a árvore de `data/evidencia/`: contar os arquivos gerenciados por
  instrumento, comparar com as chaves do protocolo e confirmar que não há arquivo de termo
  retirado nem consulta substituída. Verificar: o conjunto de caminhos esperados calculado
  pelo script é igual ao conjunto de arquivos gerenciados no disco.
- [x] 6.3 Conferir que `data/validacao_terminologica.toml` tem uma tabela por decisão e
  nenhuma tabela sem campo de decisão, e que `data/consulta_terminologica.json` tem um objeto
  por linha consultada do protocolo, sem linha de termo retirado. Verificar: a contagem e a
  comparação de chaves saem de um script de conferência, não de leitura manual.

## 7. Sincronização a partir do protocolo

- [x] 7.1 Ajustar `_decisoes_para_gravar`, `grava_registros` e `cmd_importar` para remover a
  decisão de chave fora do protocolo, informar quantas foram removidas e terminar em OK.
  Verificar: `termos exportar` e `termos importar` no projeto saem com OK, e a decisão de
  termo retirado não permanece no TOML.
- [x] 7.2 Acrescentar a `documentos conferir` a reprovação de decisão de chave fora do
  protocolo, nomeando a chave e indicando `termos exportar`. Verificar: uma cópia em memória
  com decisão órfã reprova; o protocolo corrente aprova depois da sincronização.
- [x] 7.3 Atualizar o autoteste: decisão órfã removida por `exportar` e por `importar`,
  remoção informada e conferência reprovando enquanto ela existir; retirar as expectativas de
  preservação e de REPROVADO. Verificar: cada caso novo falha quando a regra é desligada.
- [x] 7.4 Rodar `termos exportar` no projeto, conferir que as decisões fora do protocolo
  saíram e que `documentos conferir`, `dados conferir`, `projeto autoteste` e `projeto
  pendencias` saem com OK; atualizar README, skill, guia e catálogo.

## 8. Correções da verificação

- [x] 8.1 Nomear o termo e o instrumento na mensagem de `data_decisao` fora de
  `AAAA-MM-DD`, mantendo a forma admitida. Verificar: `python3 -m rsl projeto autoteste`
  exige termo, instrumento e forma na mensagem, e o caso reprova antes do ajuste.
- [x] 8.2 Listar na reconciliação de `termos exportar` e `termos importar` cada decisão sem
  linha no resultado técnico, com termo, faceta, idioma e instrumento, além da contagem.
  Verificar: o autoteste confere a frase e o termo na saída de `termos exportar`.
- [x] 8.3 Acrescentar ao autoteste os casos de consulta interrompida no resultado técnico,
  chave duplicada no JSON e evidência ausente em `termos importar`. Verificar: cada caso
  novo falha quando a regra correspondente é desligada.
- [x] 8.4 Fazer `Registro.grava_evidencia` usar `registro.caminho_evidencia` e substituir o
  teste tautológico do caminho por um que compara o arquivo gravado ao caminho calculado.
  Verificar: a gravação e o expurgo da mesma chave convergem para o mesmo caminho.

## Workflow follow-up

- Arquivar a change depois da revisão do projeto e da aprovação do pesquisador.
- Verificar o resultado arquivado em `openspec/specs/` e a ausência de artefatos de delta
  pendentes.
