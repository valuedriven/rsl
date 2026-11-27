"""DOI para comparação e para nome de arquivo.

Um só lugar para a normalização: a junção do arquivo de sementes com a cópia da coleção do
Zotero, a recuperação pelo DOI em `aderencia medir`, a anatomia da perda e o nome das
respostas brutas da OpenAlex comparam o DOI da mesma forma.
"""

import re

_PREFIXO = re.compile(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", re.IGNORECASE)


def normaliza(valor):
    """DOI para comparação: caixa baixa, sem o prefixo de URL do DOI nem `doi:`."""
    s = str(valor or "").strip()
    return _PREFIXO.sub("", s).strip().lower()


def nome_arquivo(valor):
    """Nome de arquivo derivado do DOI normalizado: `/` e outros caracteres fora de
    `[a-z0-9._-]` viram `_`. O nome vem do DOI, não do `id` da semente: renumerar semente
    não exige renomear evidência."""
    return re.sub(r"[^a-z0-9._-]", "_", normaliza(valor)) + ".json"
