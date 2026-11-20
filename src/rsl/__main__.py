"""Ponto de entrada único: `python3 -m rsl <subcomando>`, a partir da raiz do projeto.

Com `src/` fora do caminho de importação: `PYTHONPATH=src python3 -m rsl <subcomando>`.

Este é o único módulo que encerra o processo. Os demais devolvem um código de saída ou
levantam uma exceção tipada (`erros.py`), que é convertida aqui no código correspondente.
"""

import argparse
import sys

from . import erros
from .saida import Saida, linha_final, tabela

AJUDA = f"""\
Códigos de saída (todos os subcomandos):
{tabela()}
Quando mais de uma condição ocorre, vale a mais grave: CONFIGURACAO, PROTOCOLO_ILEGIVEL,
DADOS, FONTE_EXTERNA, REPROVADO, PARCIAL. Toda saída diferente de OK termina com uma linha
que nomeia o código.
"""


class _Parser(argparse.ArgumentParser):
    """Erro de argumento sai com USO, e a última linha nomeia o código."""

    def error(self, message):
        self.print_usage(sys.stdout)
        print(f"{self.prog}: erro: {message}")
        print(linha_final(Saida.USO))
        raise SystemExit(int(Saida.USO))


def _cmd(modulo, funcao, contexto=True):
    """Adia a importação do módulo do subcomando até ele ser executado."""
    def executa(ctx, a):
        import importlib                                            # noqa: PLC0415
        mod = importlib.import_module(f"rsl.{modulo}")
        return getattr(mod, funcao)(ctx, a)
    executa.contexto = contexto
    return executa


def _parser():
    ap = _Parser(prog="python3 -m rsl", description=__doc__, epilog=AJUDA,
                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(title="subcomandos", metavar="<subcomando>")

    def novo(pai, nome, ajuda, modulo, funcao, contexto=True):
        p = pai.add_parser(nome, help=ajuda, description=ajuda, epilog=AJUDA,
                           formatter_class=argparse.RawDescriptionHelpFormatter)
        p.set_defaults(executa=_cmd(modulo, funcao, contexto))
        return p

    novo(sub, "conferir", "lê o protocolo e as fichas e relata problemas de coerência",
         "conferencia", "cmd_conferir")
    novo(sub, "conferir-dados", "confere os arquivos alimentados contra o protocolo",
         "dados", "cmd_conferir_dados")
    novo(sub, "autoteste", "injeta defeitos em cópias e exige que cada conferência os "
         "reprove com o código esperado", "autoteste", "cmd_autoteste")
    novo(sub, "mostrar", "resume o que foi lido e os parâmetros em uso, com a origem",
         "relatorio", "cmd_mostrar")
    novo(sub, "pendencias", "relata as pendências dos artefatos, sem escrever",
         "dados", "cmd_pendencias")
    novo(sub, "gramatica", "exibe o contrato de forma que o leitor exige do protocolo e "
         "das fichas", "relatorio", "cmd_gramatica", contexto=False)

    sem = sub.add_parser("sementes", help="metadado das sementes e instrumento de aderência")
    sub_sem = sem.add_subparsers(title="subcomandos", metavar="<subcomando>")
    novo(sub_sem, "sincronizar", "reconcilia o arquivo de sementes com o protocolo",
         "dados", "cmd_sincronizar")
    novo(sub_sem, "planilha", "grava a planilha do teste de aderência e imprime o ensaio "
         "seco", "sementes", "cmd_planilha")

    ter = sub.add_parser("termos", help="validação terminológica por instrumento")
    sub_ter = ter.add_subparsers(title="subcomandos", metavar="<subcomando>")
    novo(sub_ter, "sonda", "consulta de prova em cada cliente automatizado; não grava",
         "termos.validacao", "cmd_sonda")
    novo(sub_ter, "exportar", "reconstrói a planilha de validação a partir do protocolo, "
         "sem rede", "termos.validacao", "cmd_exportar")
    p = novo(sub_ter, "validar", "consulta, no instrumento Automático de sigla SIGLA (ou "
             "em todos: `todos`), os termos ainda sem estatuto", "termos.validacao",
             "cmd_validar")
    p.add_argument("sigla", metavar="SIGLA")
    p.add_argument("--faceta", type=int, help="restringe a uma faceta (número n de FCTn)")
    novo(sub_ter, "importar", "reconcilia a planilha com o protocolo, preservando as "
         "decisões", "termos.validacao", "cmd_importar")

    bus = sub.add_parser("busca", help="registro das execuções, derivação e testes da busca")
    sub_bus = bus.add_subparsers(title="subcomandos", metavar="<subcomando>")
    p = novo(sub_bus, "registrar", "registra uma execução e confere o retorno declarado "
             "contra o arquivo", "busca.execucao", "cmd_registrar")
    p.add_argument("base", metavar="BASE")
    p.add_argument("expressao", metavar="EXPRESSAO")
    p.add_argument("arquivo", metavar="ARQUIVO")
    p.add_argument("--retorno", type=int, help="retorno que a base exibiu")
    p.add_argument("--data-hora", help="data e hora da consulta, ISO 8601 (padrão: agora)")
    p.add_argument("--justificar", default="",
                   help="motivo aceito para retorno declarado divergente do arquivo")
    novo(sub_bus, "derivar", "deriva as expressões não executadas, as contagens e a ordem "
         "de triagem", "busca.derivacao", "cmd_derivar")
    novo(sub_bus, "aderencia", "teste de aderência ao conjunto-semente, por papel",
         "busca.aderencia", "cmd_aderencia")
    p = novo(sub_bus, "fidelidade", "compara o conjunto derivado com a execução direta",
             "busca.fidelidade", "cmd_fidelidade")
    p.add_argument("expressao", metavar="EXPRESSAO")
    p.add_argument("arquivo", metavar="ARQUIVO")
    p = novo(sub_bus, "sensibilidade", "mede a perda da sonda para a executada e grava a "
             "amostra a classificar", "busca.sensibilidade", "cmd_sensibilidade")
    p.add_argument("base", metavar="BASE", nargs="?", default=None)
    return ap, {"sementes": sem, "termos": ter, "busca": bus}


def _mensagem(e, ctx):
    if isinstance(e, erros.ConfiguracaoInvalida):
        return f"Configuração inválida — {e}"
    if isinstance(e, erros.ProtocoloInvalido):
        from .gramatica import SEMENTES                               # noqa: PLC0415
        if ctx is None:
            onde = ""
        elif e.documento == SEMENTES:
            onde = f" ({ctx.caminho_sementes})"
        else:
            onde = f" ({ctx.caminho_protocolo})"
        return f"Protocolo ilegível{onde} — {e}"
    if isinstance(e, erros.DadosInvalidos):
        return f"Dados ausentes ou ilegíveis — {e}"
    if isinstance(e, erros.FonteExterna):
        return f"Fonte externa interrompida — {e}"
    return str(e)


def main(argv=None):
    ap, grupos = _parser()
    a = ap.parse_args(argv)
    executa = getattr(a, "executa", None)
    if executa is None:
        argv = sys.argv[1:] if argv is None else argv
        grupo = grupos.get(argv[0]) if argv else None
        (grupo or ap).print_help(sys.stdout)
        print(linha_final(Saida.USO))
        return int(Saida.USO)
    from .contexto import Contexto                                  # noqa: PLC0415
    ctx = None
    try:
        if executa.contexto:
            ctx = Contexto.carrega()
        codigo = Saida(executa(ctx, a))
    except erros.ErroRSL as e:
        print(_mensagem(e, ctx))
        codigo = e.codigo
    if codigo != Saida.OK:
        print(linha_final(codigo))
    return int(codigo)


if __name__ == "__main__":
    sys.exit(main())
