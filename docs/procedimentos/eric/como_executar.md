1. Executar as consultas de EB4, na ordem em que aparecem acima, e exportar cada uma em arquivo próprio, `eric_<consulta>.ris` (`eric_4a1.ris`, …), em `data/execucoes/eric/`. A exportação aceita até 200 registros por lote (BD3/sd15-2026-11-26): consulta com retorno acima disso exige mais de uma exportação.
2. Aplicar o filtro de data da página e anotar o retorno antes e depois, com o rótulo exato do filtro.
3. Registrar as execuções, uma por arquivo: `python3 -m rsl busca registrar eric EB4 <arquivo> --retorno <n>`; rodar `busca derivar`. O retorno da base é a união deduplicada, nunca a soma: o número que vai às contagens da busca é o dos únicos, com o bruto ao lado.
4. Executar EB5 (5a e 5b) uma única vez e registrar com `EB5`.
5. Medir a aderência (seção 5). Abaixo do limiar de aderência (`limiar_aderencia`, `python3 -m rsl configuracao mostrar`), passar à contingência das variantes.
