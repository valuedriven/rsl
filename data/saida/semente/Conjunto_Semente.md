# Conjunto-semente — instrumento do teste de aderência

**10 estudos**, todos primários e dentro do recorte temporal, conforme a seção *Acervos pessoais* do protocolo. As referências e o mapa por base são lidos daquele documento; este instrumento é derivado dele e não o substitui.

## 1. Para que serve

O conjunto-semente é o controlo externo da busca: estudos que o pesquisador **já sabe** serem pertinentes, reunidos antes da execução e por caminho independente dela. A expressão é executada e se pergunta quantos deles ela recupera.

A pergunta que o teste responde não é se a busca achou coisa boa, e sim **se ela deixou de achar coisa que se sabia existir**. Perder uma semente conhecida indica que a busca perde também o que não se conhece.

**Limiar do protocolo: 80%.** Abaixo dele, revisa-se o controlo terminológico antes de prosseguir, com emenda registrada no Anexo A. O limiar é decisão do projeto, não norma da literatura, e consta como tal no relato.

## 2. Composição por base — conferida contra o mapa do protocolo

São **incidências por base**, não estudos distintos: um mesmo estudo pode estar indexado em mais de uma base.

| Base | Incidências |
| :--- | :---: |
| WoS | 4 |
| Scopus | 6 |
| ERIC | 3 |
| BRAPCI | 2 |
| **Total** | **15** |

10 registros únicos: 4 estudos em mais de uma base e 6 em uma só.

> **10 sementes sem metadados em `data/sementes.json`.** As colunas de conferência, escopo e tipo saem em branco para elas. O instrumento pode ser executado; o que falta é registro, não dado de busca.

> **10 sementes com metadados pendentes.** O campo marcado `A CONFERIR` ou `PENDÊNCIA` não foi verificado nesta rodada; o instrumento registra a pendência em vez de a esconder.

> - **SE1. Alvarenga 2023** — verificação, escopo, tipo, alinhamento
> - **SE2. Das 2022** — verificação, escopo, tipo, alinhamento
> - **SE3. Chi 2018** — verificação, escopo, tipo, alinhamento
> - **SE4. Shvets 2024** — verificação, escopo, tipo, alinhamento
> - **SE5. Sousa 2018** — verificação, escopo, tipo, alinhamento
> - **SE6. Iatrellis 2019** — verificação, escopo, tipo, alinhamento
> - **SE7. Chimalakonda 2020** — verificação, escopo, tipo, alinhamento
> - **SE8. Cenka 2023** — verificação, escopo, tipo, alinhamento
> - **SE9. Piriyapongpipat 2024** — verificação, escopo, tipo, alinhamento
> - **SE10. Khoo 2020** — verificação, escopo, tipo, alinhamento

## 3. Referências

**SE1. Alvarenga, V. B. L., & Cristovão, H. M. (2023).** Objetos de aprendizagem organizados com base no padrão LOM-IEEE adaptado a uma ontologia operacional de domínio na web semântica.
- Bases esperadas: BRAPCI

**SE2. Das, S., Naskar, D., & Roy, S. (2022).** Reorganizing Educational Institutional Domain using Faceted Ontological Principles.
- DOI: `10.5771/0943-7444-2022-1-6`
- Bases esperadas: WoS, Scopus

**SE3. Chi, Y.-L., Chen, T.-Y., & Hung, C. (2018).** Learning adaptivity in support of flipped learning: An ontological problem-solving approach.
- DOI: `10.1111/exsy.12246`
- Bases esperadas: Scopus

**SE4. Shvets, O., Murtazin, K., Meeter, M., & Piho, G. (2024).** Towards a Domain Model for Learning and Teaching.
- DOI: `10.5220/0012471400003645`
- Bases esperadas: Scopus

**SE5. Sousa, E. E. de, & Duque, C. (2018).** Modelo de sistema da informação para gerar feedback no ensino baseado na teoria da atividade.
- DOI: `10.5433/1981-8920.2018v23n1p271`
- Bases esperadas: BRAPCI

**SE6. Iatrellis, O., Kameas, A., & Fitsilis, P. (2019).** EDUC8 ontology: semantic modeling of multi-facet learning pathways.
- DOI: `10.1007/s10639-019-09872-9`
- Bases esperadas: ERIC

**SE7. Chimalakonda, S., & Nori, K. V. (2020).** An ontology based modeling framework for design of educational technologies.
- DOI: `10.1186/s40561-020-00135-6`
- Bases esperadas: ERIC, WoS, Scopus

**SE8. Cenka, B. A. N., Santoso, H. B., & Junus, K. (2023).** Personal learning environment toward lifelong learning: an ontology-driven conceptual model.
- DOI: `10.1080/10494820.2022.2039947`
- Bases esperadas: ERIC, Scopus

**SE9. Piriyapongpipat, P., Goldin, S., & Ditcharoen, N. (2024).** An alternative approach to ontology-based curriculum development in higher education.
- DOI: `10.1186/s40561-024-00307-8`
- Bases esperadas: WoS, Scopus

**SE10. Khoo, C. S. G., & Kan, R. Y. P. (2020).** An ontology for conceptual analysis of signature pedagogies.
- DOI: `10.5771/9783956507762`
- Bases esperadas: WoS

## 4. Ensaio seco — o que o título entrega às facetas

Casamento por frase inteira entre cada título e os termos das quatro facetas, nos três idiomas. **É ensaio, não execução**: a busca procura em título, resumo e palavras-chave, de modo que a semente sem termo no título ainda pode ser recuperada pelo resumo.

| id | 🟦 FCT1 | 🟨 FCT2 | 🟥 FCT3 | 🟧 FCT4 | EB4 pelo título (duas âncoras e uma temática) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| SE1 | `ontologia` | — | — | — | **não** |
| SE2 | — | `educational` | — | — | **não** |
| SE3 | — | — | — | — | **não** |
| SE4 | `domain model` | — | — | — | **não** |
| SE5 | — | — | — | — | **não** |
| SE6 | `ontology` | — | — | — | **não** |
| SE7 | `ontology`, `ontology-based modeling` | `educational` | — | — | **não** |
| SE8 | `ontology` | `learning environment`, `lifelong learning` | — | — | **não** |
| SE9 | `ontology` | `education`, `higher education` | — | — | **não** |
| SE10 | `ontology` | — | — | — | **não** |

**0 de 10 satisfazem as duas âncoras e uma faceta temática pelo título.** Nas demais, a recuperação depende do resumo — e é nelas que a etapa 2 do procedimento exige cuidado: ausência na exportação pode ser falha da busca ou ausência do termo em todos os campos indexados.

## 5. Planilha a preencher

`semente_aderencia.csv`, uma linha por semente e por base — 10 × 4 = 40 linhas. Preencher durante a execução, não depois: as colunas de registro são a evidência do teste.

| Coluna | O que registrar |
| :--- | :--- |
| `id` | identificador da semente (SEn), conforme o protocolo |
| `autores_ano` | autoria abreviada e ano |
| `titulo` | título, como consta na referência do protocolo |
| `tipo` | primário ou secundário — preencher em sementes.json |
| `escopo` | DENTRO, FRONTEIRA ou ÂNCORA AUSENTE — preencher em sementes.json |
| `verificacao` | estado de conferência da referência — preencher em sementes.json |
| `base` | WoS, Scopus, ERIC ou BRAPCI |
| `esperada_na_base` | sim se o mapa do protocolo indica esta base |
| `indexada` | etapa 1: sim ou não, por busca de título. **obrigatório** |
| `data_etapa1` | data da busca de título |
| `recuperada` | etapa 2: sim ou não, por busca na exportação de EB4 |
| `como_localizada` | DOI, título ou não localizada |
| `data_etapa2` | data da conferência na exportação |
| `observacao` | o que explica o não: termo ausente, campo não indexado, recorte |

> `indexada` em branco impede o cálculo: sem ela não há denominador. `recuperada` só se preenche onde `indexada` = sim.

