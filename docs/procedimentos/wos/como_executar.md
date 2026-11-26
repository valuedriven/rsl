1. Conferir a sessão contra a seção 1, na primeira execução do dia.
2. Submeter o bloco de EB4 da seção 4 como está, sem definir conjunto e sem montar arquivo. Na primeira execução, conferir se a interface aceita a consulta inteira; recusa por extensão leva à variante "Partição por recusa da proximidade ou do comprimento", registrada como adaptação.
3. Exportar em RIS, com todos os campos, em lotes dentro do limite da base.
4. Conferir o retorno da exportação contra o da tela.
5. Registrar EB4 e EB5: `python3 -m rsl busca registrar wos EB4 <arquivo> --retorno <n>` e o mesmo com `EB5`; rodar `busca derivar` e `conferencia sensibilidade`.
6. Medir a aderência ao conjunto-semente (seção 5). Semente não recuperada: `python3 -m rsl aderencia diagnosticar wos`, que exige `[composicao] doi` na fonte.
