"""Autoteste dos nomes antigos recusados: cada nome de comando renomeado pela change
`namespace-de-comandos-e-skills` sai com USO no parser real.

A lista abaixo é dado de teste, não do produto: o parser não guarda nome antigo. Como
contraprova, o canônico de cada nome antigo, consultado pelo mesmo detector, tem de ser
aceito; assim um parser que recusasse tudo não passaria. Nada é executado: o parser só é
consultado.
"""

import argparse
import contextlib
import io

from .. import __main__ as M
from ..saida import Saida

# {nome antigo: canônico}, como na change que os renomeou.
NOMES_ANTIGOS = {
    "conferir": "documentos conferir",
    "conferir-dados": "dados conferir",
    "gramatica": "documentos gramatica",
    "autoteste": "projeto autoteste",
    "mostrar": "configuracao mostrar",
    "pendencias": "projeto pendencias",
    "sementes planilha": "aderencia ensaiar",
    "aderencia planilhar": "aderencia ensaiar",
    "busca aderencia": "aderencia medir",
    "termos sonda": "termos sondar",
    "busca fidelidade": "conferencia fidelidade",
    "busca sensibilidade": "conferencia sensibilidade",
}


def _folha(ap, caminho):
    """O parser da folha `caminho` (lista de palavras), ou None."""
    p = ap
    for nome in caminho:
        subs = [a for a in p._actions if isinstance(a, argparse._SubParsersAction)]
        p = next((s.choices[nome] for s in subs if nome in s.choices), None)
        if p is None:
            return None
    return p


def _codigo(ap, caminho):
    """Código de saída do parser para `caminho`, com um valor fictício para cada posicional
    obrigatório da folha; None quando o parser aceita e resolve uma operação."""
    p = _folha(ap, caminho)
    extra = [] if p is None else [
        "autoteste" for x in p._actions
        if not x.option_strings and x.required and x.dest != "help"
        and x.nargs not in ("?", "*")]
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            a = ap.parse_known_args(list(caminho) + extra)[0]
        except SystemExit as x:
            return x.code
    return None if getattr(a, "executa", None) is not None else int(Saida.USO)


def casos(_ctx, g):
    ap, _ = M._parser()
    for antigo, canonico in sorted(NOMES_ANTIGOS.items()):
        cod = _codigo(ap, antigo.split())
        g.testa(f"`{antigo}` sai com USO", cod == int(Saida.USO), f"código {cod}")
        cod = _codigo(ap, canonico.split())
        g.testa(f"contraprova: `{canonico}` é aceito", cod is None, f"código {cod}")
