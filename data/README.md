# Dados do projeto

Os JSON abaixo são os artefatos de máquina da revisão. A **fonte única** é
`docs/2_protocolo/03_protocolo_estrategia_pesquisa.md`: `src/protocolo.py --gerar` lê o
documento e deriva o que é derivado, preservando o que é autoral.

| Arquivo | Procedência | Editar à mão? |
| :--- | :--- | :--- |
| `questoes.json` | derivado | não — altere o protocolo e regenere |
| `facetas.json` | derivado | não |
| `descritores.json` | **misto**: tabelas derivadas, `estatuto` autoral | sim, apenas o bloco `estatuto` |
| `strings.json` | derivado | não |
| `criterios.json` | derivado | não |
| `fontes.json` | derivado | não |
| `sementes.json` | **misto**: referências derivadas, conferência autoral | sim, apenas os campos autorais |
| `consultas.json` | auxiliar, escrito por `--registrar` | sim, para corrigir ou anotar |
| `pendencias.json` | auxiliar, escrito pelo pesquisador | sim |

Campos autorais de `sementes.json`: `verificacao`, `escopo`, `tipo`, `alinhamento`, `nota`,
`veiculo_conferido`, `eric`. Campos autorais de `descritores.json`: tudo o que está dentro
de `estatuto[idioma][termo].validacoes`.

Cada arquivo derivado ou misto guarda dois selos:

- `fonte.sha256` — o `sha256` do documento do protocolo no momento da geração. Se o
  documento mudar sem `--gerar`, todos os scripts recusam rodar.
- `derivado.sha256` — o `sha256` do subconjunto derivado do próprio arquivo. Se um campo
  derivado for editado à mão, os scripts recusam rodar; campo autoral pode ser editado
  livremente.

Termo ou semente retirado do protocolo **não** é apagado: fica com `no_protocolo=false`, e
`src/protocolo.py --pendencias` o reporta para decisão.

## Pastas

| Caminho | O que contém |
| :--- | :--- |
| `execucoes/<base>/` | exportações das bases, intactas, como vieram da interface |
| `saida/derivacao/` | `registros.csv`, `io2_contagens.csv`, `ordem_triagem.csv`, `fidelidade_E<n>.csv` |
| `saida/semente/` | `Conjunto_Semente.md` e `semente_aderencia.csv` |
| `saida/validacao/` | `validacao_termologica.csv`, exportação a partir de `descritores.json` |
| `evidencia/{tbci,unesco}/` | resposta bruta de cada consulta terminológica |
| `arquivo/` | cópias anteriores com `SHA256`, para provar o que mudou |

`arquivo/pre-migracao/` é o estado de 16/11/2026, anterior à reestruturação dos arquivos.
Serve de linha de base: o conteúdo dos derivados foi conferido campo a campo contra ele.

## Regenerar

```bash
python3 src/protocolo.py --gerar          # depois de alterar o protocolo
python3 src/protocolo.py --conferir-dados # confere os JSON entre si
python3 src/gen_semente.py                # instrumento de aderência
python3 src/validar_termos.py --exportar  # planilha de validação
```

Nada em `saida/` é fonte: pode ser regerado a qualquer momento. `consultas.json`,
`pendencias.json` e os metadados autorais, não.
