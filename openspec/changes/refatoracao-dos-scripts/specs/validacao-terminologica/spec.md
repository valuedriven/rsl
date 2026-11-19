# Spec Delta

## ADDED Requirements

### Requirement: Falha de fonte externa interrompe sem nova tentativa
A consulta automatizada a um instrumento SHALL fazer uma requisição por vez, sem
concorrência e sem nova tentativa automática. As condições abaixo MUST interromper a
validação na mesma hora, sem consultar o termo seguinte, sem outra rota e sem outro
endereço, e o subcomando termina com o código FONTE_EXTERNA:

- erro de rede;
- resposta HTTP 403 ou 429;
- resposta 5xx;
- página com captcha ou aviso de atividade atípica.

O que já foi consultado e registrado antes da interrupção SHALL ficar gravado na planilha
e na evidência. A mensagem MUST nomear o instrumento, o termo, a condição encontrada e
quantos termos ficaram sem consulta.

#### Scenario: Limite excedido
- **WHEN** o instrumento responde 429 na consulta do décimo termo
- **THEN** a validação para, os nove termos anteriores ficam registrados, nenhuma
  requisição nova é feita e a saída tem o código FONTE_EXTERNA

#### Scenario: Erro de rede
- **WHEN** a primeira requisição falha por erro de rede
- **THEN** nenhuma segunda requisição é feita, e a saída tem o código FONTE_EXTERNA

#### Scenario: Termo não localizado não é falha
- **WHEN** o instrumento responde normalmente sem o termo
- **THEN** o termo é registrado como termo livre, e a validação continua

### Requirement: Planilha de validação nomeada pela configuração
O caminho e o nome da planilha de validação SHALL vir do `config.toml`. O nome configurado
para o projeto é `validacao_terminologica.csv`.

#### Scenario: Grafia corrigida
- **WHEN** se procura `termologica` em `src/`, no `config.toml`, no README e nas skills
- **THEN** não há ocorrência
