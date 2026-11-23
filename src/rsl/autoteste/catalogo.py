"""Autoteste do catálogo de apoio: cada conferência reprova o defeito que lhe cabe, e o caso
falha quando a regra correspondente é desligada.

As cópias se geram da estrutura lida — "o primeiro passo", "a primeira linha Skill:", "o
primeiro grupo do parser", "o primeiro passo com marcador de apoio" —, não de literais do
guia vigente. A gravação só acontece em arquivo temporário, nunca no catálogo do projeto.
Nenhum caso depende do registro de execução.
"""

import dataclasses
import json
import os
import re
import tempfile

from .. import catalogo as C
from .. import geracao
from ..saida import Saida
from . import resultado

R, D, OK = Saida.REPROVADO, Saida.DADOS, Saida.OK


def _executa(desligadas=()):
    return lambda e: [m for _r, m in C.confere(e, desligadas=frozenset(desligadas))]


def _caso(g, nome, mutante, original, regra, trecho, codigo=R):
    """O defeito reprova com `codigo` e `trecho`; com `regra` desligada, o trecho some."""
    g.espera(nome, mutante, original, _executa(), codigo, trecho)
    if regra and mutante is not None:
        _cod, msgs = resultado(lambda: _executa({regra})(mutante))
        g.testa(f"com a regra '{regra}' desligada, o caso falha: {nome}",
                not any(trecho in m for m in msgs), f"ainda acusa: {msgs[:1]}")


def _apos_linha(texto, n, nova):
    """`texto` com `nova` inserida depois da linha `n` (1-based)."""
    linhas = texto.split("\n")
    return "\n".join(linhas[:n] + [nova] + linhas[n:])


def _troca_linha(texto, n, nova):
    linhas = texto.split("\n")
    linhas[n - 1:n] = [] if nova is None else [nova]
    return "\n".join(linhas)


def _primeira(texto, prefixo):
    """Número (1-based) da primeira linha que começa por `prefixo`, ou None."""
    for n, linha in enumerate(texto.split("\n"), 1):
        if linha.startswith(prefixo):
            return n
    return None


def _grava_em(e, caminho, interrompe=False):
    """`catalogo gerar --gravar` sobre `caminho`; com `interrompe`, a renomeação falha."""
    original = geracao.os.replace
    if interrompe:
        def falha(*_a, **_k):
            raise OSError("renomeação interrompida (autoteste)")
        geracao.os.replace = falha
    try:
        return C.gera(e, gravar=True, caminho=caminho, saida=lambda *_: None), None
    except OSError as x:
        return None, x
    finally:
        geracao.os.replace = original


def casos(_ctx, g):
    e0 = C.carrega()
    g0 = C.le_guia(e0.guia, e0.grupos, e0.comandos)
    e = dataclasses.replace(e0, gravado=C.renderiza(e0, g0))
    t = e.guia

    corrente = _executa()(e)
    g.testa("o guia corrente é aprovado pelas conferências do catálogo", not corrente,
            f"{corrente[:2]}")

    # skills
    n_skill = _primeira(t, "  - Skill:")
    inexistente = "skill-inexistente-autoteste"
    m = dataclasses.replace(e, guia=_troca_linha(
        t, n_skill, t.split("\n")[n_skill - 1] + f"; `{inexistente}`"))
    _caso(g, "skill citada inexistente", m, e, "skill_existe",
          f"skill citada inexistente `{inexistente}`")

    nova = "skill-nova-autoteste"
    m = dataclasses.replace(e, skills={**e.skills, nova: f"---\nname: {nova}\n---\n"})
    _caso(g, "skill existente não citada", m, e, "skill_orfa",
          f"nem declarada transversal: `{nova}`")

    pasta = sorted(e.skills)[0]
    m = dataclasses.replace(e, skills={**e.skills, pasta: re.sub(
        r"(?m)^name:.*$", "name: outro-nome-autoteste", e.skills[pasta], count=1)})
    _caso(g, "`name` do frontmatter diferente da pasta", m, e, "skill_nome",
          f"skill `{pasta}`: `name` do frontmatter")

    s_papel = sorted(g0.papeis)[0]
    n_papel = next(n for n, linha in enumerate(t.split("\n"), 1)
                   if linha.startswith("|") and C._celulas(linha)[0] in C.PAPEIS
                   and f"`{s_papel}`" in linha)
    linha_papel = t.split("\n")[n_papel - 1]
    sem_papel = re.sub(rf"`{re.escape(s_papel)}`(;\s*)?|;\s*`{re.escape(s_papel)}`", "",
                       linha_papel, count=1)
    m = dataclasses.replace(e, guia=_troca_linha(t, n_papel, sem_papel))
    _caso(g, "skill sem papel declarado", m, e, "skill_papel",
          f"skill `{s_papel}` com 0 papel(éis)")

    # comandos
    n_script = _primeira(t, "  - Script:")
    linha_script = t.split("\n")[n_script - 1]
    grupo = " ".join(sorted(e.grupos)[0])
    folha = " ".join(sorted(e.comandos)[0])
    m = dataclasses.replace(e, guia=_troca_linha(
        t, n_script, linha_script + f"; `python3 -m rsl {grupo} inexistente`"))
    _caso(g, "comando inexistente", m, e, "comando_existe",
          f"caminho inexistente: `{grupo} inexistente`")

    m = dataclasses.replace(e, guia=_troca_linha(
        t, n_script, linha_script + f"; `python3 -m rsl {folha} --opcao-que-nao-existe`"))
    _caso(g, "opção inexistente", m, e, "comando_opcao",
          "opção inexistente `--opcao-que-nao-existe`")

    m = dataclasses.replace(e, guia=_troca_linha(
        t, n_script, linha_script + f"; `python3 -m rsl {folha} SIGLA`"))
    msgs = _executa()(m)
    g.testa("placeholder (`SIGLA`) não é tratado como comando nem como opção",
            not any("SIGLA" in x for x in msgs), f"{msgs[:1]}")

    novo = ("grupo-autoteste", "novo")
    m = dataclasses.replace(e, comandos={**e.comandos, novo: C.Comando(frozenset())},
                            grupos=e.grupos | {novo[:1]})
    _caso(g, "comando do parser não citado", m, e, "comando_orfao",
          "nem declarado transversal: `grupo-autoteste novo`")

    # contagem
    primeiro = g0.passos[0]
    extra = f"- Passo extra do autoteste\n  - Skill: `{pasta}`"
    m = dataclasses.replace(e, guia=_apos_linha(t, primeiro.linha - 1, extra))
    _caso(g, "passo extra sem marca de adaptação", m, e, "contagem",
          f"passos sem a marca {C.MARCA_ADAPTACAO}")

    _dm, dt = g0.declarada
    m = dataclasses.replace(e, guia=re.sub(rf"totalizando(\s+){dt}\b",
                                           rf"totalizando\g<1>{dt + 1}", t, count=1))
    _caso(g, "contagem declarada divergente da listada", m, e, "contagem",
          f"contagem divergente: o guia declara {dt + 1} passos e lista {len(g0.passos)}")

    # cobertura
    sem = next(p for p in g0.passos if p.apoio and not (p.skills or p.scripts))
    n_apoio = next(n for n in range(sem.linha + 1, len(t.split("\n")) + 1)
                   if t.split("\n")[n - 1].startswith("  - Apoio:"))
    m = dataclasses.replace(e, guia=_troca_linha(t, n_apoio, None))
    _caso(g, "passo sem skill, script ou marcador", m, e, "cobertura",
          f"passo sem skill, script ou marcador `Apoio:`: {sem.onde}")

    m = dataclasses.replace(e, guia=_troca_linha(t, n_apoio, "  - Apoio: manual —"))
    _caso(g, "marcador de apoio sem razão", m, e, "cobertura",
          f"`Apoio: manual` sem razão: {sem.onde}")

    m = dataclasses.replace(e, guia=_troca_linha(
        t, n_apoio, "  - Apoio: tipo-autoteste — razão do autoteste"))
    _caso(g, "marcador de apoio com tipo fora de manual/lacuna", m, e, "cobertura",
          f"com tipo fora de {C.TIPOS_APOIO}: {sem.onde}")

    com = next(p for p in g0.passos if p.skills or p.scripts)
    m = dataclasses.replace(e, guia=_apos_linha(
        t, com.linha, "  - Apoio: manual — razão do autoteste"))
    _caso(g, "marcador de apoio em passo que já tem skill ou script", m, e, "cobertura",
          f"`Apoio:` em passo que já tem skill ou script: {com.onde}")

    # catálogo gravado
    m = dataclasses.replace(e, gravado=e.gravado + "\nlinha editada à mão\n")
    _caso(g, "catálogo gravado defasado", m, e, "defasado", f"{C.CATALOGO} defasado")

    # forma do guia
    m = dataclasses.replace(e, guia=_apos_linha(t, primeiro.linha, "  - Rotulo-errado: x"))
    g.espera("subitem fora da gramática do guia", m, e,
             lambda x: C.gera(x, saida=lambda *_: None), D, "fora da gramática")
    m = dataclasses.replace(e, guia=None)
    g.espera("guia ausente", m, e, lambda x: C.gera(x, saida=lambda *_: None), D,
             C.GUIA)

    # gravação
    fd, caminho = tempfile.mkstemp(prefix="rsl_autoteste_", suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("anterior\n")
        ruim = dataclasses.replace(e, guia=_troca_linha(t, n_apoio, None))
        cod, _x = _grava_em(ruim, caminho)
        with open(caminho, encoding="utf-8") as fh:
            g.testa("conferência reprovada durante --gravar deixa o arquivo anterior intacto",
                    cod == R and fh.read() == "anterior\n", f"código {cod}")
        cod, erro = _grava_em(e, caminho, interrompe=True)
        with open(caminho, encoding="utf-8") as fh:
            g.testa("gravação interrompida deixa o arquivo anterior intacto",
                    erro is not None and fh.read() == "anterior\n", f"código {cod}")
        cod, _x = _grava_em(e, caminho)
        with open(caminho, encoding="utf-8") as fh:
            depois = dataclasses.replace(e, gravado=fh.read())
        resto = _executa()(depois)
        g.testa("gravação seguida de conferência sai OK", cod == OK and not resto,
                f"código {cod}, {resto[:1]}")
    finally:
        os.unlink(caminho)

    saidas = []
    cod = C.gera(e, como_json=True, saida=saidas.append)
    try:
        v = json.loads(saidas[0])
        ok = all(k in v for k in ("passos", "skills", "comandos")) and len(v["passos"]) == \
            len(g0.passos)
    except (ValueError, IndexError):
        ok = False
    g.testa("--json emite passos, skills e comandos", ok and cod == OK, f"código {cod}")

    # passo com skill e comando aparece nas três visões
    ambos = next((p for p in g0.passos if p.skills and any(not c.erro for c in p.scripts)),
                 None)
    if ambos is None:
        g.testa("há passo com skill e comando para conferir as três visões", False,
                "nenhum passo do guia cita skill e comando ao mesmo tempo")
    else:
        v = C.visoes(e, g0)
        skill = ambos.skills[0]
        cmd = next(" ".join(c.caminho) for c in ambos.scripts if not c.erro)
        por_passo = any(x["passo"] == ambos.nome and skill in x["skills"]
                        and cmd in x["comandos"] for x in v["passos"])
        por_skill = any(x["skill"] == skill and ambos.onde in x["passos"]
                        and cmd in x["comandos"] for x in v["skills"])
        por_cmd = any(x["comando"] == cmd and ambos.onde in x["passos"]
                      and skill in x["skills"] for x in v["comandos"])
        g.testa(f"passo com skill e comando aparece nas três visões: {ambos.onde}",
                por_passo and por_skill and por_cmd,
                f"por passo {por_passo}, por skill {por_skill}, por comando {por_cmd}")
