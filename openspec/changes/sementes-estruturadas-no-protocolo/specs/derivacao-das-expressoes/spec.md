# Spec Delta

## MODIFIED Requirements

### Requirement: Arquivos de entrada e de saída lidos da configuração
A derivação, a aderência, a fidelidade, a sensibilidade e o instrumento de aderência
SHALL obter do `config.toml` o caminho de cada arquivo que leem ou gravam. Isso inclui
`registro_execucao.json`, `semente_aderencia.csv` e as saídas na raiz de `data/`. O
arquivo do conjunto-semente é exceção: o caminho dele vem do apontamento no protocolo,
porque é parâmetro estrutural, e MUST NOT constar do `config.toml`.

#### Scenario: Registro em outro caminho
- **WHEN** o `config.toml` aponta o registro de execução para outro caminho
- **THEN** `busca registrar`, `busca derivar` e `conferir-dados` leem e gravam esse
  caminho, e as mensagens o nomeiam

#### Scenario: Chave antiga do arquivo de sementes
- **WHEN** o `config.toml` traz a chave `[dados] sementes`
- **THEN** a configuração reprova, nomeando a chave, como as demais chaves fora do esquema

### Requirement: Planilha de aderência traz o papel

A planilha gerada pelo instrumento de aderência SHALL ter, em cada linha, o papel da
semente lido do arquivo do conjunto-semente. Os dados de conferência SHALL vir do mesmo
arquivo, e a planilha MUST NOT trazer a coluna `escopo`.

#### Scenario: Coluna de papel
- **WHEN** `sementes planilha` gera a planilha
- **THEN** cada linha traz a coluna `papel` com `desenvolvimento` ou `validação`, igual ao
  campo `papel` da semente no arquivo do conjunto-semente

#### Scenario: Sem coluna de escopo
- **WHEN** `sementes planilha` gera a planilha
- **THEN** o cabeçalho não traz `escopo`
