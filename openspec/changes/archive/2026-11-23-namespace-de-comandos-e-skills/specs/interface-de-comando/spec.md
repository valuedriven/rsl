# Spec Delta

## MODIFIED Requirements

### Requirement: Ponto de entrada único
Toda operação SHALL ser executada por `python3 -m rsl <subcomando>`, a partir da raiz do
projeto. Os subcomandos canônicos SHALL ser estes:

- `documentos conferir` e `documentos gramatica`;
- `dados conferir`;
- `projeto autoteste` e `projeto pendencias`;
- `configuracao mostrar`;
- `termos sondar`, `termos exportar`, `termos validar <sigla>` e `termos importar`;
- `strings gerar`;
- `catalogo gerar`;
- `aderencia planilhar` e `aderencia medir`;
- `busca registrar` e `busca derivar`;
- `conferencia fidelidade` e `conferencia sensibilidade`.

Os nomes antigos definidos na change `namespace-de-comandos-e-skills` MUST funcionar como
aliases temporários, conforme o requisito “Aliases de transição”. Os scripts
`src/protocolo.py`, `src/derivar_expressoes.py`, `src/validar_termos.py` e
`src/gen_semente.py` MUST NOT continuar existindo como ponto de entrada. O subcomando
`sementes sincronizar` MUST NOT existir, porque o conjunto-semente não tem mais arquivo
separado a reconciliar.

#### Scenario: Ajuda
- **WHEN** se executa `python3 -m rsl` sem subcomando
- **THEN** a ajuda lista apenas os subcomandos canônicos e a saída tem o código USO

#### Scenario: Ajuda do subcomando de geração
- **WHEN** se executa `python3 -m rsl strings gerar -h`
- **THEN** a ajuda mostra a opção `--gravar` e diz que, sem ela, nada é gravado

#### Scenario: Script antigo
- **WHEN** se procura `src/protocolo.py` ou `src/gen_semente.py`
- **THEN** o arquivo não existe, e nenhum documento do projeto cita o script antigo como
  comando

#### Scenario: Sincronização retirada
- **WHEN** se executa `python3 -m rsl sementes sincronizar`
- **THEN** a saída tem o código USO, e nenhum documento do projeto cita o subcomando como
  comando

#### Scenario: Catálogo no ponto de entrada
- **WHEN** se executa `python3 -m rsl catalogo gerar -h`
- **THEN** a ajuda descreve a geração do catálogo e a saída não tem código de erro

#### Scenario: Comando canônico agrupado
- **WHEN** se executa `python3 -m rsl aderencia medir`
- **THEN** a operação mede a aderência ao conjunto-semente, como antes fazia o comando de
  aderência do grupo `busca`, hoje alias

### Requirement: Convenção de nomes
Os subcomandos SHALL ser `grupo ação` quando houver grupo natural, com a ação no infinitivo,
em português e sem acento; o topo pode ser verbo quando não houver grupo. O grupo SHALL
nomear o artefato ou domínio (`documentos`, `dados`, `projeto`, `configuracao`, `termos`,
`strings`, `catalogo`, `aderencia`, `busca`, `conferencia`). Os arquivos que os subcomandos
gravam SHALL seguir estas regras:

- `snake_case`, em português e sem acento;
- o nome é o substantivo do conteúdo;
- quando há um arquivo por chave (expressão, base), o sufixo é a chave em minúsculas
  (`fidelidade_eb2.csv`, `sensibilidade_wos.csv`).

O nome de cada arquivo de entrada e de saída SHALL vir do `config.toml`.

#### Scenario: Saída por expressão
- **WHEN** `conferencia fidelidade` confere a EB2
- **THEN** a saída gravada se chama `fidelidade_eb2.csv`

#### Scenario: Planilha de validação
- **WHEN** a configuração é a do projeto
- **THEN** a planilha de validação se chama `validacao_terminologica.csv`

#### Scenario: Ação nominal recusada
- **WHEN** se tenta registrar um comando cuja ação é substantivo, como a sonda do grupo
  `termos`
- **THEN** o nome canônico é `termos sondar` e o substantivo só vale como alias temporário

## ADDED Requirements

### Requirement: Aliases de transição
Os nomes antigos de comando SHALL continuar funcionando como aliases ocultos até que nenhum
documento ou skill viva os cite. O alias MUST executar a mesma operação do nome canônico e
MUST emitir aviso de nome antigo. O catálogo MUST acusar citação de alias em documento
vivo. A remoção dos aliases SHALL ocorrer em change própria.

#### Scenario: Alias executa a operação
- **WHEN** se executa o nome antigo de `aderencia medir`, mantido como alias
- **THEN** a operação de `aderencia medir` é executada e a saída avisa que o nome é antigo

#### Scenario: Alias não aparece na ajuda
- **WHEN** se executa `python3 -m rsl`
- **THEN** a ajuda lista apenas os nomes canônicos

#### Scenario: Remoção posterior
- **WHEN** a change de remoção dos aliases é aplicada
- **THEN** o nome antigo termina com o código USO, e nenhum documento vivo o cita
