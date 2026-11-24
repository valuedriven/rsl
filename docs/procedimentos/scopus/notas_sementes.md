**Anatomia da perda.** Executar em ordem, com o DOI da semente; a primeira que devolver zero é a causa.

| # | Consulta | Se devolver zero |
| :---: | :--- | :--- |
| 1 | `DOI(<DOI>)` | a base não indexa o estudo: sai do denominador |
| 2 | `DOI(<DOI>) AND PUBYEAR > 2016 AND PUBYEAR < 2027 AND (LANGUAGE(portuguese) OR LANGUAGE(english) OR LANGUAGE(spanish)) AND (DOCTYPE(ar) OR DOCTYPE(re) OR DOCTYPE(cp) OR DOCTYPE(ch))` | um filtro a exclui: identificar qual critério |
| 3 | `DOI(<DOI>) AND TITLE-ABS-KEY(🟦) AND TITLE-ABS-KEY(🟨)` | o vocabulário não a alcança: emenda de termo |
| 4 | `DOI(<DOI>) AND TITLE-ABS-KEY((🟦) W/5 (🟨))` | a proximidade a exclui: variante "Forma ampla" |
