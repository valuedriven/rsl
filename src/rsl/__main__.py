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
    """(parser, {grupo: parser do grupo})."""
    ap = _Parser(prog="python3 -m rsl", description=__doc__, epilog=AJUDA,
                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(title="subcomandos", metavar="<subcomando>")
    grupos = {}          # nome do grupo → parser do grupo (para a ajuda do grupo)
    acoes = {}           # nome do grupo → subparsers do grupo

    def grupo(nome, ajuda=None):
        """O grupo `nome`, criado na primeira chamada (com a ajuda) e reusado nas demais."""
        if nome not in acoes:
            kw = {"help": ajuda} if ajuda else {}
            g = sub.add_parser(nome, description=ajuda, **kw)
            grupos[nome] = g
            acoes[nome] = g.add_subparsers(title="subcomandos", metavar="<subcomando>")
        return acoes[nome]

    def novo(nome_grupo, nome, ajuda, modulo, funcao, contexto=True):
        p = grupo(nome_grupo).add_parser(
            nome, help=ajuda, description=ajuda, epilog=AJUDA,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        p.set_defaults(executa=_cmd(modulo, funcao, contexto))
        return p

    grupo("documentos", "protocolo, fontes dos procedimentos de busca e sementes: "
          "conferência e gramática")
    novo("documentos", "conferir", "lê o protocolo e a fonte de cada procedimento de busca, "
         "confere o procedimento gravado contra a geração e relata problemas de coerência",
         "coerencia", "cmd_conferir")
    novo("documentos", "gramatica", "exibe o contrato de forma que o leitor exige do "
         "protocolo, da fonte dos procedimentos de busca, do arquivo de sementes, do arquivo "
         "de exceções de flexão e do resultado de sondagem", "relatorio", "cmd_gramatica",
         contexto=False)

    grupo("dados", "arquivos alimentados pela execução")
    novo("dados", "conferir", "confere os arquivos alimentados contra o protocolo",
         "dados", "cmd_conferir_dados")

    grupo("projeto", "autoteste das conferências e pendências dos artefatos")
    novo("projeto", "autoteste", "injeta defeitos em cópias e exige que cada conferência "
         "os reprove com o código esperado", "autoteste", "cmd_autoteste")
    novo("projeto", "pendencias", "relata as pendências dos artefatos, sem escrever",
         "dados", "cmd_pendencias")

    grupo("configuracao", "parâmetros em uso e a sua origem")
    novo("configuracao", "mostrar", "resume o que foi lido e os parâmetros em uso, com a "
         "origem", "relatorio", "cmd_mostrar")

    grupo("termos", "validação terminológica por instrumento")
    novo("termos", "sondar", "consulta de prova em cada endereço resolvido dos instrumentos "
         "Automático, um por idioma; não grava",
         "termos.validacao", "cmd_sonda")
    novo("termos", "exportar", "reconstrói a planilha de validação a partir do protocolo, "
         "sem rede, reabrindo as linhas que deixaram de valer", "termos.validacao",
         "cmd_exportar")
    p = novo("termos", "validar", "consulta, no endereço resolvido do instrumento "
             "Automático de sigla SIGLA (ou de todos: `todos`), os termos ainda sem "
             "estatuto", "termos.validacao",
             "cmd_validar")
    p.add_argument("sigla", metavar="SIGLA")
    p.add_argument("--faceta", type=int, help="restringe a uma faceta (número n de FCTn)")
    novo("termos", "importar", "reconcilia a planilha com o protocolo, preservando as "
         "decisões", "termos.validacao", "cmd_importar")

    grupo("strings", "strings de busca por faceta geradas do quadro")
    p = novo("strings", "gerar", "calcula cada STR a partir do quadro terminológico e "
             "exibe a diferença para a tabela do protocolo; sem --gravar, nada é gravado",
             "geracao", "cmd_gerar")
    p.add_argument("--gravar", action="store_true",
                   help="substitui só as células de string da tabela do protocolo, de "
                        "forma atômica; recusado se o quadro tiver termo em duas facetas")

    grupo("procedimentos", "procedimento de busca de cada base, gerado da fonte da base, "
          "do protocolo e do arquivo de sementes")
    p = novo("procedimentos", "gerar", "gera o procedimento de busca da base SIGLA (sem "
             "sigla, de todas as bases da tabela do protocolo) e exibe a diferença para o "
             "gravado, por seção, com as formas de número e a sua origem; sem --gravar, nada "
             "é gravado. O procedimento é saída: edita-se a fonte "
             "(`[documentos] procedimento_fonte`), nunca o procedimento",
             "procedimentos", "cmd_gerar")
    p.add_argument("sigla", metavar="SIGLA", nargs="?", default=None,
                   help="sigla da base; sem ela, todas as bases")
    p.add_argument("--gravar", action="store_true",
                   help="substitui o procedimento inteiro, de forma atômica, depois de reler "
                        "as fontes; recusado com leitura reprovada, flexão indecidível ou "
                        "fonte alterada durante a execução")
    p = novo("procedimentos", "iniciar", "cria a fonte do procedimento de busca de uma base "
             "já registrada no protocolo, com o derivável preenchido e os campos não "
             "deriváveis marcados PENDENTE; não sobrescreve fonte existente",
             "procedimentos", "cmd_iniciar")
    p.add_argument("sigla", metavar="SIGLA")

    grupo("sondagens", "resultado das sondagens de sintaxe do roteiro de cada base")
    p = novo("sondagens", "registrar", "grava no registro de execução o resultado da "
             "sondagem SDn da base SIGLA e exibe a citação e a mudança a aplicar na fonte; "
             "não altera a fonte", "sondagens", "cmd_registrar")
    p.add_argument("sigla", metavar="SIGLA")
    p.add_argument("sondagem", metavar="SDn")
    p.add_argument("--retorno", action="append", type=int, default=[],
                   help="retorno exibido, uma vez por consulta declarada, na ordem")
    p.add_argument("--leitura", type=int, help="número da leitura observada (1, 2, …)")
    p.add_argument("--data-hora", help="data e hora da sondagem, ISO 8601; obrigatório, sem "
                                       "padrão: o registro costuma ser posterior à sondagem")
    p.add_argument("--evidencia", action="append", default=[],
                   help="arquivo de evidência (um ou mais); obrigatório e existente: sondagem "
                        "sem evidência não se registra")
    p.add_argument("--submetido", nargs=2, action="append", default=[],
                   metavar=("K", "TEXTO"),
                   help="texto efetivamente submetido na consulta K, quando difere do "
                        "declarado")
    p.add_argument("--observacao", default="", help="observação livre")

    grupo("catalogo", "catálogo de apoio: skills e comandos por passo do guia de "
          "procedimentos")
    p = novo("catalogo", "gerar", "deriva do guia de procedimentos o catálogo de skills e "
             "comandos por passo, imprime-o e confere as citações, a cobertura, a contagem "
             "de passos e o catálogo gravado; sem --gravar, nada é gravado",
             "catalogo", "cmd_gerar", contexto=False)
    p.add_argument("--gravar", action="store_true",
                   help="grava docs/catalogo_de_apoio.md de forma atômica; recusado se "
                        "alguma conferência reprovar")
    p.add_argument("--json", action="store_true",
                   help="emite o catálogo e os problemas em JSON")

    grupo("aderencia", "teste de aderência ao conjunto-semente")
    novo("aderencia", "planilhar", "grava a planilha do teste de aderência e imprime o "
         "ensaio seco", "sementes", "cmd_planilha")
    novo("aderencia", "medir", "teste de aderência ao conjunto-semente",
         "busca.aderencia", "cmd_aderencia")
    p = novo("aderencia", "diagnosticar", "anatomia da perda: monta as consultas por nível "
             "com o DOI das sementes não recuperadas; sem --retorno, imprime o roteiro e não "
             "grava", "busca.anatomia", "cmd_diagnosticar")
    p.add_argument("base", metavar="BASE")
    p.add_argument("--retorno", nargs=2, action="append", default=[],
                   metavar=("N", "K"), type=int,
                   help="retorno K exibido pelo nível N submetido; um por nível")
    p.add_argument("--exportacao", nargs=2, action="append", default=[],
                   metavar=("N", "ARQUIVO"),
                   help="exportação do nível N, quando K > 0")
    p.add_argument("--data-hora", help="data e hora da submissão, ISO 8601; obrigatória com "
                                       "resultado, sem padrão")

    grupo("busca", "registro das execuções e derivação das expressões")
    p = novo("busca", "registrar", "registra uma execução e confere o retorno declarado "
             "contra o arquivo", "busca.execucao", "cmd_registrar")
    p.add_argument("base", metavar="BASE")
    p.add_argument("expressao", metavar="EXPRESSAO")
    p.add_argument("arquivo", metavar="ARQUIVO")
    p.add_argument("--retorno", type=int, required=True, help="retorno que a base exibiu")
    p.add_argument("--data-hora", help="data e hora da consulta, ISO 8601 (padrão: agora)")
    p.add_argument("--justificar", default="",
                   help="motivo aceito para retorno declarado divergente do arquivo")
    novo("busca", "derivar", "deriva as expressões não executadas, as contagens e a ordem "
         "de triagem", "busca.derivacao", "cmd_derivar")

    grupo("conferencia", "conferências pós-execução da busca")
    p = novo("conferencia", "fidelidade", "compara o conjunto derivado com a execução "
             "direta", "busca.fidelidade", "cmd_fidelidade")
    p.add_argument("base", metavar="BASE")
    p.add_argument("expressao", metavar="EXPRESSAO")
    p.add_argument("arquivo", metavar="ARQUIVO", nargs="?", default=None,
                   help="exportação da execução direta (padrão: a registrada da expressão "
                        "na base)")
    p = novo("conferencia", "sensibilidade", "mede a perda da sonda para a executada e "
             "grava a amostra a classificar", "busca.sensibilidade", "cmd_sensibilidade")
    p.add_argument("base", metavar="BASE", nargs="?", default=None)
    p = novo("conferencia", "simular", "analisa a perda da sensibilidade: facetas "
             "reconhecidas na amostra, termos candidatos e, com --termo, a executada "
             "ampliada", "busca.simulacao", "cmd_simular")
    p.add_argument("base", metavar="BASE")
    p.add_argument("--termo", nargs=2, action="append", default=[],
                   metavar=("FCTn", "TERMO"),
                   help="termo a acrescentar à faceta não âncora FCTn na simulação; repetível")

    return ap, grupos


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
