# Spec Delta

## MODIFIED Requirements

### Requirement: Nenhum parâmetro fixado no código
O código de `src/` MUST NOT conter valor de parâmetro do projeto. São parâmetros:

- composição e papel das expressões;
- âncoras, recorte e limiares;
- dimensões de critério;
- instrumentos (sigla, modo, caminho, idiomas, facetas);
- bases (sigla, ficha);
- idiomas do quadro;
- caminhos e nomes dos arquivos de dados, de entrada e de saída;
- campos da planilha;
- o caminho do próprio protocolo.

Todo parâmetro SHALL vir do protocolo, da ficha da base ou do `config.toml` na raiz. O
autoteste MUST NOT ser exceção. As cópias defeituosas que ele produz SHALL ser geradas a
partir da estrutura lida do protocolo corrente (por exemplo, "a última semente lida" ou "a
primeira base da tabela"), e não de literais do texto vigente.

Docstrings e mensagens MUST NOT descrever a composição, as siglas ou os valores vigentes
como se fossem do código.

#### Scenario: Busca por valor fixado
- **WHEN** se procura em `src/` por constante de parâmetro (ex.: `0.80`, `2017`, `"EB4"`,
  `"tbci"`, `"wos"`, `"pt"`, `"SE10"`, `"registro_execucao.json"`)
- **THEN** não há ocorrência, inclusive no autoteste

#### Scenario: Emenda legítima não quebra o autoteste
- **WHEN** o protocolo ganha uma semente nova, troca a sigla de uma base de forma coerente
  com as fichas ou altera a faixa de sensibilidade dentro do válido
- **THEN** `conferir` passa, e `autoteste` executa os mesmos grupos de casos, sem caso
  "mutação não aplicada"

### Requirement: Arquivo do protocolo é parametrizado
O caminho do documento do protocolo a ser lido SHALL vir de `config.toml`. Por ser o que
localiza o protocolo, esse parâmetro MUST NOT ser sobrescrito pelo protocolo. O caminho do
próprio `config.toml` é o único fixado: a raiz do projeto.

#### Scenario: Outro arquivo de protocolo
- **WHEN** `config.toml` aponta para outro arquivo de protocolo
- **THEN** todos os subcomandos leem esse arquivo, e `mostrar` exibe o caminho em uso

#### Scenario: Protocolo inexistente
- **WHEN** o caminho configurado não existe
- **THEN** o subcomando termina com o código CONFIGURACAO e com erro que nomeia o caminho
  e a chave do `config.toml`

### Requirement: Autoteste prova que cada conferência reprova
`autoteste` SHALL injetar, numa cópia em memória, ao menos um defeito por:

- conferência de coerência;
- regra de precedência;
- parâmetro estrutural, ausente e com valor inválido;
- elemento exigido da gramática do protocolo.

Cada defeito SHALL ser reprovado com o código esperado: REPROVADO para coerência,
PROTOCOLO_ILEGIVEL para forma e CONFIGURACAO para configuração. Defeito não detectado, ou
detectado com outro código, MUST fazer o autoteste falhar.

#### Scenario: Conferência que não reprova
- **WHEN** um defeito injetado não é detectado pela conferência correspondente
- **THEN** `autoteste` falha, nomeando o defeito

#### Scenario: Parâmetro estrutural ausente
- **WHEN** o autoteste retira de uma cópia do protocolo a coluna `Sigla` da tabela de bases
- **THEN** a leitura reprova com PROTOCOLO_ILEGIVEL; leitura que caia em valor padrão faz o
  autoteste falhar

#### Scenario: Código trocado
- **WHEN** um defeito de forma é reprovado com REPROVADO em vez de PROTOCOLO_ILEGIVEL
- **THEN** `autoteste` falha, nomeando o defeito e os dois códigos

### Requirement: Resultado parcial do autoteste declarado
Quando houver caso não executado, o autoteste SHALL declarar que o resultado é parcial e
terminar com o código PARCIAL, desde que nenhum caso executado tenha falhado. Havendo
falha, o código é REPROVADO, e a mensagem informa também os casos não executados.

#### Scenario: Arquivos alimentados ausentes
- **WHEN** `autoteste` termina sem falha e com casos não executados
- **THEN** a última mensagem diz que o autoteste é parcial, quantos casos não rodaram e por
  quê, e o código de saída é PARCIAL

#### Scenario: Falha com casos não executados
- **WHEN** um caso executado falha e há casos não executados
- **THEN** o código de saída é REPROVADO, e a mensagem informa os casos não executados
