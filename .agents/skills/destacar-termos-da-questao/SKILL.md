---
name: destacar-termos-da-questao
description: "Destaca as palavras significativas da questão de revisão (M3/E1): extrai as expressões-chave e monta, por faceta, os termos e as linhas do quadro terminológico pela natureza do termo (termo livre, descritores correspondentes, sinônimos ou relacionados) nos três idiomas. Use ao criar, acrescentar, retirar, traduzir ou reorganizar termo de busca e vocabulário das facetas."
---

# Facetação e termos livres

Da questão de revisão saem as **expressões-chave**; de cada expressão-chave, um
**termo livre**, que é a unidade com que as expressões de busca se compõem. Esta
skill cobre a estrutura. A consulta a tesauro é outra: `estabelecer-controle-terminologico`.

## 1. Uma faceta por expressão-chave

Nesta revisão são quatro, e a sua natureza decide a arquitetura de busca:

| | Faceta | Papel |
| --- | --- | --- |
| 1 | Artefatos de representação e organização do conhecimento | **âncora** |
| 2 | Domínio educacional | **âncora** |
| 3 | Práticas do processo de ensino-aprendizagem | temática |
| 4 | Fatores situacionais | temática |

**Âncora é obrigatória em toda expressão.** As temáticas compõem as demais. Daí a
arquitetura de contenção `EB1 ⊆ EB2 ⊆ EB4`, `EB1 ⊆ EB3 ⊆ EB4` e `EB4 ⊆ EB5` — exigir
mais facetas restringe. "Geral" nomeia a composição, não o alcance: a expressão das
quatro facetas é a **mais restritiva**, e serve de sonda de precisão, nunca de critério
de exclusão.

## 2. Três linhas pela natureza do termo, três idiomas

Cada faceta tem uma tabela sob `### CTn (FCTn)` em `docs/03_protocolo_estrategia_pesquisa.md`,
com o cabeçalho `| Termo | pt | en | es |` e as linhas "Termo livre", "Descritores correspondentes" e "Termos sinônimos ou
relacionados" (`livre` · `descritores` · `relacionados`), em `pt`, `en`, `es`. A forma exata
está em `python3 -m rsl documentos gramatica`.

A linha **não é distância conceitual nem grau de confiança**: é a **natureza do termo**, e
resulta da decisão do ReT (`decisao_ReT`) na planilha de validação, sobre os instrumentos
planejados para a faceta e o idioma do termo:

- descritor autorizado em pelo menos um instrumento → "Descritores correspondentes";
- senão, USE/UP ou TR de um descritor em pelo menos um → "Termos sinônimos ou relacionados";
- senão → "Termo livre".

**Termo sem decisão do ReT é termo livre** — inclusive o de instrumento manual ainda não
consultado, o que só tem proposta da máquina (`status_proposto`) e todo termo enquanto a
planilha não existe. Linhas de descritores e de sinônimos vazias significam "não validado",
não "inexistente". Mover um termo de linha sem a decisão correspondente reprova em
`documentos conferir`; a reclassificação vem da validação
(`estabelecer-controle-terminologico`), e depois dela se regeneram STRs e procedimentos. O mesmo
termo não fica em duas linhas do mesmo CT e idioma.

**A STR da faceta é composta pelas linhas "Termo livre" e "Descritores correspondentes"**,
e só por elas: "Termos sinônimos ou relacionados" documenta a relação do termo com o
vocabulário controlado e não entra na STR. Termo dessa linha posto na STR reprova em
`documentos conferir`; levá-lo à busca é decidir que ele é termo livre, e isso se registra.
Não há mínimo de termos por STR: o tamanho resulta do quadro. Se um corte por teto de
caracteres voltar a ser necessário, decide-se sob este critério, por change.

**Termos de desfecho não entram na string.** São escassos em título e resumo e derrubam a
sensibilidade sem ganho de precisão. Vão para faceta auxiliar local e para a extração.

Controle terminológico **paralelo**, e não substitutivo, entre Ciência da Informação
e Educação: as duas tradições nomeiam a mesma coisa de modos diferentes, e usar o
vocabulário de uma só perde recall na outra.

## 3. Desdobramento morfológico contra ampliação conceitual

A distinção mais importante desta skill.

| | Desdobramento | Ampliação |
| --- | --- | --- |
| O que é | variante de forma do mesmo conceito — plural, grafia, ordem das palavras | conceito que o vocabulário não cobria |
| Reversível | sim | não |
| Exige emenda no histórico (`data/historico.md`) | não | **sim** |
| Exige novo teste de aderência | não | **sim** |

Tratar ampliação como desdobramento é alterar o recorte sem registrar.

## 4. Quatro armadilhas medidas neste projeto

- **As regras de qualificação casam a FORMA, não o lema.** Acrescentar `taxonomies`
  reintroduziu nas strings um termo que a decisão havia excluído na forma singular.
  Todo acréscimo pergunta: existe regra de qualificação que devia alcançar esta
  forma e não alcança?
- **A redução ao singular é de EXIBIÇÃO, e vem depois da qualificação.** A string
  executada conserva os plurais, porque base que não lematiza perde registro se o
  plural sair. Inverter a ordem produziu lacuna de 84 termos entre quadro e strings.
- **Lista curada não lê as facetas.** Na base executada por consultas curadas uma a uma,
  todo acréscimo ao quadro exige revisitar aquela lista à mão: a regeração das STRs não a
  alcança.
- **Ensaio seco silencioso não é ensaio reprovado.** Um acréscimo conceitual pode não
  ser acionado por nenhuma das sementes — o ensaio nada diz sobre ele.

## 5. Depois de alterar

A ordem é a do README (Precedência): **quadro → `strings gerar` → procedimentos de busca → `documentos conferir`**.
Altera-se o quadro, nunca a STR: a tabela de strings do protocolo é saída de geração.

1. Alterar o quadro terminológico do protocolo, sem pôr o mesmo termo em duas facetas.
2. Rodar `python3 -m rsl strings gerar` e ler a diferença: termos a acrescentar, a retirar
   e subsumidos, cada um com o termo que o subsume. Depois, `strings gerar --gravar`. A
   guarda é automática: `documentos conferir` reprova a STR diferente da gerada e o termo do quadro
   em duas facetas, e a gravação é recusada nesse caso. A regra de subsunção é a grafia
   exata, acento e hífen inclusive; o que ela não retira é decisão de forma da base.
3. Atualizar o procedimento de busca de cada base a partir das STRs regeradas, aplicando os parâmetros
   que ela declara (`gerar-procedimento-de-busca`):
   - retirar o subsumido do mesmo campo do termo que o subsume; o subsumido em campo
     próprio é aceito e relatado;
   - com `plural: explícito`, trazer as duas formas de número; com `pela lematização`, só a
     forma do quadro.
4. Com `teto de caracteres` numérico, particionar sem retirar termo a consulta que passar
   do teto. `documentos conferir` mede cada consulta e reprova a base que passar.
5. Rodar `documentos conferir` e ler também os relatos, que não reprovam: subsumidos por base, a maior
   consulta da base sem teto e termos numa só forma de número em procedimento de busca de plural explícito.

Depois, `elaborar-expressoes-de-busca` para recompor, e `registrar-decisao` para o histórico.
