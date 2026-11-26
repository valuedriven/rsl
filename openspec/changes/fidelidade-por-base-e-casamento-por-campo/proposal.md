# Proposta

## Por quê

A primeira conferência de fidelidade da Web of Science (2026-11-26) reprovou por defeito da
ferramenta, não da derivação. Dois defeitos se somavam:

1. `conferencia fidelidade` comparava a execução direta de **uma** base com o conjunto
   derivado do corpus de **todas** as bases lidas. Os registros da outra base contavam como
   divergência, e o comando mandava registrar emenda sem fundamento (PD35).
2. O casamento local unia título, resumo e palavras-chave num só texto normalizado, e a
   normalização apagava a fronteira entre eles. Um termo de várias palavras casava
   juntando duas palavras-chave: `learning; context awareness` dava `learning context`
   (PD36).

## O que muda

- **Fidelidade por base.** `conferencia fidelidade BASE EXPRESSAO [ARQUIVO]`: o conjunto
  derivado vem só das exportações da executada da base dada. Sem `ARQUIVO`, a execução
  direta são as exportações registradas da expressão na base. **BREAKING**: a forma
  `conferencia fidelidade EXPRESSAO ARQUIVO` deixa de existir.
- **Saída por base e por expressão.** `[saidas] fidelidade` passa a exigir `{base}` e
  `{expressao}` (`fidelidade_wos_eb2.csv`), para que a conferência de uma base não
  sobrescreva a de outra.
- **Casamento por trecho.** O casamento local procura cada termo no título, no resumo e em
  cada palavra-chave, separadamente. O separador de valores é o mesmo que os leitores das
  exportações usam ao unir valores de um campo.
- **Limiar da skill.** A skill `avaliar-resultados-da-busca` passa a remeter ao limiar
  `divergencia_fidelidade` em uso (protocolo, senão `config.toml`), em vez de exigir
  coincidência exata (PD37, decisão do pesquisador).

Fora do escopo: a fronteira entre frases dentro do mesmo resumo. Não se verificou como as
bases tratam a frase que atravessa a pontuação.

## Capacidades

### Novas capacidades

Nenhuma.

### Capacidades modificadas

- `derivacao-das-expressoes`: a fidelidade é por base, e o casamento local respeita a
  fronteira entre campos e entre palavras-chave.
- `interface-de-comando`: o exemplo do nome da saída de fidelidade passa a levar a base.

## Impacto

- Código: `src/rsl/busca/fidelidade.py`, `src/rsl/busca/derivacao.py`,
  `src/rsl/busca/leitores.py`, `src/rsl/config.py`, `src/rsl/__main__.py` e os autotestes
  de busca e de configuração.
- Configuração: `[saidas] fidelidade = "fidelidade_{base}_{expressao}.csv"`.
- Documentos: `docs/procedimentos.md` (passo "Avaliar a pertinência e a relevância dos
  resultados"), `README.md` e a skill `avaliar-resultados-da-busca`.
- Saídas: `data/fidelidade_eb2.csv` e `data/fidelidade_eb3.csv` dão lugar às saídas por base.
