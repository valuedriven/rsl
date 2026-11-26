**Se a SE5 não aparecer.** Consultar `Duque` em *Local de pesquisa* = **Autor**, abrir o registro e ler resumo e palavras-chave.

| Achado | Leitura |
| :--- | :--- |
| o resumo ou as palavras-chave trazem `ontologia` | falha de campo, não de vocabulário |
| nem o resumo nem as palavras-chave trazem o termo | falha de vocabulário da faceta 🟦 |
| a consulta por `Duque` devolve zero | opção *Autor* inoperante ou registro não indexado: registrar antes de usar o campo no *backward search* |

**Anatomia da perda.** A causa da perda não se atribui a olho:
`python3 -m rsl aderencia diagnosticar <sigla>` monta, da composição desta base, as
consultas por nível com os DOIs das sementes não recuperadas, lê da execução registrada os
níveis que já a têm e atribui a causa pelo primeiro nível em que o DOI desaparece — não
indexada, filtro, âncoras, proximidade ou faceta não âncora. O comando exige que a fonte
declare `[composicao] doi`; sem a declaração, recusa e nomeia o campo.
