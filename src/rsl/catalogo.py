"""Catálogo de apoio: deriva do guia de procedimentos as visões por passo, por skill e por
comando, e confere a integridade das citações.

A fonte é `docs/procedimentos.md`. O catálogo `docs/catalogo_de_apoio.md` é saída de
geração: `catalogo gerar --gravar` o regrava, e `catalogo gerar` reprova quando ele está
defasado. Não existe segundo arquivo de mapeamento.

Gramática de leitura do guia (a forma do guia é contrato):

- `## M<n> — <título>` abre um módulo; outro título `## ` encerra a leitura dos passos;
- `### E<n> — <título>` abre uma etapa; `#### ` abre um trecho de prosa e tabela da etapa,
  sem passos, até o próximo `###` ou `##`;
- `- <passo>` na coluna 0 é um passo; a marca `(adaptação do projeto)` no fim declara o
  passo de adaptação; sem ela, o passo é do modelo;
- `  - <Rótulo>: <valor>` é um subitem do passo; os rótulos são `Fonte`, `Script`, `Skill`,
  `Apoio` e `Ordem`; rótulo fora dessa lista é forma ilegível (DADOS);
- linha indentada que não começa por `-` continua o subitem anterior;
- em `Script:`, cada trecho em crase que começa por `python3 -m rsl` é uma citação de
  comando; o caminho são as palavras minúsculas que o parser reconhece, as opções são os
  `--longos`; posicionais e placeholders (`SIGLA`, `BASE`…) não são caminho nem opção;
- em `Skill:`, cada trecho em crase é uma skill;
- `Apoio: manual — <razão>` ou `Apoio: lacuna — <razão>`, só no passo sem skill nem script.

Fora dos módulos, o guia declara a contagem (`<n> passos do modelo … totalizando <t>`), a
tabela da seção "Conferências transversais" (comandos transversais) e a tabela da seção
"Papel das skills" (papel de cada skill).

As conferências são funções puras sobre `Entradas`; o autoteste as executa sobre cópias em
memória e com uma regra desligada por vez.
"""

import dataclasses
import json
import re

from . import config as _config
from .erros import DadosInvalidos
from .saida import Saida

GUIA = "docs/procedimentos.md"
CATALOGO = "docs/catalogo_de_apoio.md"
SKILLS = ".agents/skills"
COMANDO = "python3 -m rsl catalogo gerar --gravar"

# O RS Banyan tem 63 passos (plano §1.4). É o modelo, não parâmetro do projeto.
MODELO = 63
MARCA_ADAPTACAO = "(adaptação do projeto)"
ROTULOS = ("Fonte", "Script", "Skill", "Apoio", "Ordem")
TIPOS_APOIO = ("manual", "lacuna")
PAPEIS = ("procedimento", "instrumento", "artefato", "transversal")
SECAO_TRANSVERSAIS = "Conferências transversais"
SECAO_PAPEIS = "Papel das skills"

# Skills renomeadas: {nome antigo: nome canônico}. Os comandos antigos vêm de
# `__main__.ALIASES`. Ambos alimentam a varredura de nomes antigos e a tabela de
# correspondência; vazios, a regra fica inativa.
SKILLS_RENOMEADAS = {}

# Regras, na ordem do relato. Cada problema leva a regra que o produziu; o autoteste
# desliga uma por vez.
REGRAS = ("contagem", "cobertura", "skill_existe", "skill_nome", "skill_orfa", "skill_papel",
          "comando_existe", "comando_opcao", "comando_orfao", "nome_antigo", "defasado")


# ------------------------------------------------------------------------ entradas
@dataclasses.dataclass(frozen=True)
class Comando:
    opcoes: frozenset
    ajuda: str = ""


@dataclasses.dataclass(frozen=True)
class Entradas:
    """Tudo o que o catálogo lê. O autoteste substitui um campo por uma cópia alterada."""
    guia: str | None
    skills: dict          # pasta → texto do SKILL.md ("" se ausente)
    grupos: frozenset     # prefixos de caminho que são grupo, como tuplas
    comandos: dict        # caminho (tupla) → Comando, só as folhas
    aliases: dict         # caminho antigo (texto) → caminho canônico (texto)
    renomeadas: dict      # skill antiga → skill canônica
    vivos: dict           # caminho relativo → texto, documentos e skills vivos
    gravado: str | None   # texto do catálogo gravado, ou None


def arvore(ap):
    """(grupos, comandos) a partir do parser: a existência vem do parser, não de lista."""
    import argparse                                                  # noqa: PLC0415
    grupos, comandos = set(), {}

    def percorre(p, caminho):
        subs = [a for a in p._actions if isinstance(a, argparse._SubParsersAction)]
        if not subs:
            opcoes = {o for a in p._actions for o in a.option_strings if o.startswith("--")}
            comandos[caminho] = Comando(frozenset(opcoes), p.description or "")
            return
        if caminho:
            grupos.add(caminho)
        for s in subs:
            for nome, filho in s.choices.items():
                percorre(filho, caminho + (nome,))

    percorre(ap, ())
    return frozenset(grupos), comandos


def _vivos(raiz):
    """Documentos e skills vivos: README, docs/*.md (menos o catálogo gerado), as skills e as
    specs principais. Histórico e changes arquivadas não entram."""
    arquivos = [raiz / "README.md", *sorted((raiz / "docs").glob("*.md")),
                *sorted((raiz / SKILLS).glob("*/SKILL.md")),
                *sorted((raiz / "openspec" / "specs").glob("**/*.md"))]
    saida = {}
    for f in arquivos:
        rel = f.relative_to(raiz).as_posix()
        if rel != CATALOGO and f.is_file():
            saida[rel] = f.read_text(encoding="utf-8")
    return saida


def carrega(raiz=None):
    """As entradas do projeto, lidas do disco."""
    from .__main__ import ALIASES, _parser                          # noqa: PLC0415
    raiz = raiz or _config.RAIZ
    guia = raiz / GUIA
    if not guia.is_file():
        raise DadosInvalidos(f"guia de procedimentos ausente: {GUIA}")
    skills = {}
    pasta = raiz / SKILLS
    if pasta.is_dir():
        for d in sorted(p for p in pasta.iterdir() if p.is_dir()):
            f = d / "SKILL.md"
            skills[d.name] = f.read_text(encoding="utf-8") if f.is_file() else ""
    ap, _ = _parser()
    grupos, comandos = arvore(ap)
    cat = raiz / CATALOGO
    return Entradas(
        guia=guia.read_text(encoding="utf-8"), skills=skills, grupos=grupos,
        comandos=comandos, aliases=dict(ALIASES), renomeadas=dict(SKILLS_RENOMEADAS),
        vivos=_vivos(raiz),
        gravado=cat.read_text(encoding="utf-8") if cat.is_file() else None)


# ---------------------------------------------------------------------- leitura do guia
@dataclasses.dataclass
class Citacao:
    texto: str            # o trecho em crase, sem `python3 -m rsl`
    caminho: tuple        # palavras de caminho reconhecidas (ou a tentativa)
    opcoes: tuple
    erro: str = ""        # caminho inexistente ou incompleto


@dataclasses.dataclass
class Passo:
    modulo: str
    etapa: str
    nome: str
    origem: str
    linha: int
    fonte: list = dataclasses.field(default_factory=list)
    skills: list = dataclasses.field(default_factory=list)
    scripts: list = dataclasses.field(default_factory=list)   # Citacao
    apoio: list = dataclasses.field(default_factory=list)     # textos de Apoio:

    @property
    def onde(self):
        return f"{self.modulo.split(' ')[0]}/{self.etapa.split(' ')[0]} › {self.nome}"


@dataclasses.dataclass
class Guia:
    passos: list
    declarada: tuple | None      # (modelo, total) declarados no topo
    transversais: list           # Citacao, da tabela de conferências transversais
    papeis: dict                 # skill → [papéis declarados]
    modulos: list                # títulos, na ordem
    etapas: list                 # (módulo, etapa), na ordem


_CRASE = re.compile(r"`([^`]+)`")
_RSL = re.compile(r"^python3\s+-m\s+rsl\b\s*(.*)$", re.S)
_PALAVRA = re.compile(r"[a-z][a-z0-9-]*")
_OPCAO = re.compile(r"--[a-z][a-z0-9-]*")


def citacao(trecho, grupos, comandos):
    """A citação de comando em `trecho` (texto em crase), ou None se não for comando."""
    m = _RSL.match(trecho.strip())
    if not m:
        return None
    resto = m.group(1)
    caminho, erro = (), ""
    for tok in resto.split():
        if not _PALAVRA.fullmatch(tok):
            break
        tentativa = caminho + (tok,)
        if tentativa in comandos:
            caminho = tentativa
            break
        if tentativa in grupos:
            caminho = tentativa
            continue
        erro = f"caminho inexistente: `{' '.join(tentativa)}`"
        caminho = tentativa
        break
    if not erro and caminho not in comandos:
        erro = (f"caminho incompleto: `{' '.join(caminho)}` é grupo, não comando" if caminho
                else "citação sem caminho de comando")
    return Citacao(resto.strip(), caminho, tuple(_OPCAO.findall(resto)), erro)


def _secoes(texto):
    """{título de seção `## `: linhas} fora dos módulos."""
    secoes, atual = {}, None
    for linha in texto.split("\n"):
        if linha.startswith("## "):
            atual = linha[3:].strip()
            secoes[atual] = []
        elif atual is not None:
            secoes[atual].append(linha)
    return secoes


def _celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def le_guia(texto, grupos, comandos):
    """O guia lido pela gramática do módulo. Forma ilegível levanta DadosInvalidos com a
    linha e o passo."""
    passos, modulos, etapas = [], [], []
    modulo = etapa = None
    prosa = False
    ultimo = None          # [rótulo, valor] do último subitem
    pendentes = []         # (passo, rótulo, valor, linha) a fechar no fim

    def erro(n, msg):
        raise DadosInvalidos(f"{GUIA}, linha {n}: {msg}")

    for n, linha in enumerate(texto.split("\n"), 1):
        if linha.startswith("## "):
            m = re.match(r"## (M\d+) — (.+)$", linha)
            modulo = f"{m.group(1)} — {m.group(2).strip()}" if m else None
            if modulo:
                modulos.append(modulo)
            etapa, prosa, ultimo = None, False, None
            continue
        if modulo is None:
            continue
        if linha.startswith("### "):
            m = re.match(r"### (E\d+) — (.+)$", linha)
            if not m:
                erro(n, f"título de etapa fora da forma `### E<n> — <título>`: {linha!r}")
            etapa = f"{m.group(1)} — {m.group(2).strip()}"
            etapas.append((modulo, etapa))
            prosa, ultimo = False, None
            continue
        if linha.startswith("#### "):
            prosa, ultimo = True, None
            continue
        if not linha.strip():
            ultimo = None
            continue
        if prosa:
            continue
        if linha.startswith("- "):
            if etapa is None:
                erro(n, f"passo fora de etapa: {linha!r}")
            nome = linha[2:].strip()
            origem = "modelo"
            if nome.endswith(MARCA_ADAPTACAO):
                nome, origem = nome[: -len(MARCA_ADAPTACAO)].strip(), "adaptação"
            passos.append(Passo(modulo, etapa, nome, origem, n))
            ultimo = None
            continue
        m = re.match(r"  - ([^:]+):\s?(.*)$", linha)
        if m and not linha.startswith("   "):
            if not passos or passos[-1].etapa != etapa or passos[-1].modulo != modulo:
                erro(n, f"subitem fora de passo: {linha!r}")
            rotulo = m.group(1).strip()
            if rotulo not in ROTULOS:
                erro(n, f"passo '{passos[-1].nome}': subitem '{rotulo}' fora da gramática "
                        f"(rótulos: {', '.join(ROTULOS)})")
            ultimo = [rotulo, m.group(2)]
            pendentes.append((passos[-1], ultimo, n))
            continue
        if linha.startswith("  ") and not linha.lstrip().startswith("-"):
            if ultimo is None:
                erro(n, f"continuação sem subitem: {linha!r}")
            ultimo[1] += " " + linha.strip()
            continue
        if linha.startswith(("|", "---")) or not linha.startswith((" ", "-")):
            continue            # tabela, separador ou prosa da etapa: não são passos
        erro(n, f"linha fora da gramática do guia: {linha!r}")

    for passo, (rotulo, valor), _n in pendentes:
        if rotulo == "Fonte":
            passo.fonte.append(valor.strip())
        elif rotulo == "Skill":
            passo.skills.extend(_CRASE.findall(valor))
        elif rotulo == "Script":
            for trecho in _CRASE.findall(valor):
                c = citacao(trecho, grupos, comandos)
                if c:
                    passo.scripts.append(c)
        elif rotulo == "Apoio":
            passo.apoio.append(valor.strip())

    cabeca = texto.split("\n## ", 1)[0]
    m = re.search(r"(\d+)\s+passos\s+do\s+modelo.*?totalizando\s+(\d+)", cabeca, re.S)
    declarada = (int(m.group(1)), int(m.group(2))) if m else None

    secoes = _secoes(texto)
    transversais = []
    for linha in secoes.get(SECAO_TRANSVERSAIS, []):
        if linha.startswith("|"):
            for trecho in _CRASE.findall(_celulas(linha)[0]):
                c = citacao(trecho, grupos, comandos)
                if c:
                    transversais.append(c)
    papeis = {}
    for linha in secoes.get(SECAO_PAPEIS, []):
        if linha.startswith("|"):
            cel = _celulas(linha)
            if len(cel) >= 2 and cel[0] in PAPEIS:
                for s in _CRASE.findall(cel[1]):
                    papeis.setdefault(s, []).append(cel[0])
    return Guia(passos, declarada, transversais, papeis, modulos, etapas)


def _frontmatter_nome(texto):
    m = re.match(r"---\n(.*?)\n---", texto, re.S)
    if not m:
        return None
    for linha in m.group(1).split("\n"):
        if linha.startswith("name:"):
            return linha[5:].strip().strip("\"'")
    return None


# ------------------------------------------------------------------------ conferência
def _apoio(valor):
    """(tipo, razão) de um `Apoio:`; razão vazia se faltar o travessão ou o texto."""
    m = re.match(r"(\w+)\s*(?:—\s*(.*))?$", valor)
    if not m:
        return valor, ""
    return m.group(1), (m.group(2) or "").strip()


def _padroes_antigos(e):
    """(nome antigo, canônico, regex) para comandos e skills renomeados."""
    saida = []
    for antigo, novo in e.aliases.items():
        corpo = r"\s+".join(re.escape(p) for p in antigo.split())
        saida.append((antigo, novo, re.compile(rf"(?:rsl\s+|`){corpo}(?![\w-])")))
    for antigo, novo in e.renomeadas.items():
        saida.append((antigo, novo, re.compile(rf"(?<![\w-]){re.escape(antigo)}(?![\w-])")))
    return saida


def confere(e, g=None, desligadas=frozenset()):
    """Lista de (regra, mensagem). `g` é o guia já lido; `desligadas`, regras puladas."""
    g = g or le_guia(e.guia, e.grupos, e.comandos)
    problemas = []

    def acusa(regra, msg):
        if regra not in desligadas:
            problemas.append((regra, msg))

    # contagem
    n_mod = sum(p.origem == "modelo" for p in g.passos)
    n_ad = sum(p.origem == "adaptação" for p in g.passos)
    if g.declarada is None:
        acusa("contagem", f"{GUIA} não declara a contagem (`<n> passos do modelo … "
                          f"totalizando <t>`)")
    else:
        dm, dt = g.declarada
        if dm != MODELO:
            acusa("contagem", f"o guia declara {dm} passos do modelo; o modelo tem {MODELO}")
        if dt != len(g.passos):
            acusa("contagem", f"contagem divergente: o guia declara {dt} passos e lista "
                              f"{len(g.passos)}")
        if dt - dm != n_ad:
            acusa("contagem", f"o guia declara {dt - dm} passo(s) de adaptação e marca "
                              f"{n_ad} com {MARCA_ADAPTACAO}")
    if n_mod != MODELO:
        acusa("contagem", f"{n_mod} passos sem a marca {MARCA_ADAPTACAO}, mas o modelo tem "
                          f"{MODELO}: passo sem origem declarada")

    # cobertura
    for p in g.passos:
        tem = bool(p.skills or p.scripts)
        if not tem and not p.apoio:
            acusa("cobertura", f"passo sem skill, script ou marcador `Apoio:`: {p.onde}")
        for valor in p.apoio:
            tipo, razao = _apoio(valor)
            if tipo not in TIPOS_APOIO:
                acusa("cobertura", f"`Apoio: {valor}` com tipo fora de {TIPOS_APOIO}: "
                                   f"{p.onde}")
            elif not razao:
                acusa("cobertura", f"`Apoio: {tipo}` sem razão: {p.onde}")
            if tem:
                acusa("cobertura", f"`Apoio:` em passo que já tem skill ou script: {p.onde}")

    # skills
    citadas = {}
    for p in g.passos:
        for s in p.skills:
            citadas.setdefault(s, []).append(p)
            if s not in e.skills:
                acusa("skill_existe", f"skill citada inexistente `{s}` em .agents/skills/: "
                                      f"{p.onde}")
    for s in g.papeis:
        if s not in e.skills:
            acusa("skill_existe", f"skill citada inexistente `{s}` na tabela "
                                  f"\"{SECAO_PAPEIS}\"")
    for pasta, texto in sorted(e.skills.items()):
        nome = _frontmatter_nome(texto)
        if nome != pasta:
            acusa("skill_nome", f"skill `{pasta}`: `name` do frontmatter é "
                                f"{nome!r}, diferente do nome da pasta")
        papel = g.papeis.get(pasta, [])
        if pasta not in citadas and "transversal" not in papel:
            acusa("skill_orfa", f"skill não citada em nenhum passo nem declarada "
                                f"transversal: `{pasta}`")
        if len(papel) != 1:
            acusa("skill_papel", f"skill `{pasta}` com {len(papel)} papel(éis) na tabela "
                                 f"\"{SECAO_PAPEIS}\"; exige-se um")

    # comandos
    citados = set()
    origem = [(p.onde, c) for p in g.passos for c in p.scripts]
    origem += [(f"seção \"{SECAO_TRANSVERSAIS}\"", c) for c in g.transversais]
    for onde, c in origem:
        if c.erro:
            acusa("comando_existe", f"{c.erro} — {onde}")
            continue
        citados.add(c.caminho)
        validas = e.comandos[c.caminho].opcoes
        for o in c.opcoes:
            if o not in validas:
                acusa("comando_opcao", f"opção inexistente `{o}` em "
                                       f"`{' '.join(c.caminho)}` — {onde}")
    alias = {tuple(a.split()) for a in e.aliases}
    for caminho in sorted(e.comandos):
        if caminho not in citados and caminho not in alias:
            acusa("comando_orfao", f"comando não citado em passo nem declarado transversal: "
                                   f"`{' '.join(caminho)}`")

    # nomes antigos em documento vivo
    for antigo, novo, rx in _padroes_antigos(e):
        for arq, texto in sorted(e.vivos.items()):
            for m in rx.finditer(texto):
                n = texto.count("\n", 0, m.start()) + 1
                acusa("nome_antigo", f"{arq}:{n}: cita o nome antigo `{antigo}`; o canônico "
                                     f"é `{novo}`")

    # catálogo gravado
    if "defasado" not in desligadas:
        esperado = renderiza(e, g)
        if e.gravado is None:
            acusa("defasado", f"{CATALOGO} não existe: rode `{COMANDO}`")
        elif e.gravado.replace("\r\n", "\n") != esperado:
            acusa("defasado", f"{CATALOGO} defasado em relação ao guia: rode `{COMANDO}`")
    return problemas


# ----------------------------------------------------------------------------- visões
def _cel(texto):
    return texto.replace("|", "\\|").replace("\n", " ")


def _lista(itens):
    return "; ".join(f"`{i}`" for i in itens) if itens else "—"


def visoes(e, g):
    """Estrutura do catálogo, usada pelo markdown e pelo JSON."""
    transversais = {c.caminho for c in g.transversais if not c.erro}
    alias = {tuple(a.split()) for a in e.aliases}
    passos = [{
        "modulo": p.modulo, "etapa": p.etapa, "passo": p.nome, "origem": p.origem,
        "fonte": p.fonte, "skills": p.skills,
        "comandos": [" ".join(c.caminho) for c in p.scripts],
        "apoio": [dict(zip(("tipo", "razao"), _apoio(a))) for a in p.apoio],
    } for p in g.passos]
    skills = []
    for s in sorted(set(e.skills) | {x for p in g.passos for x in p.skills}):
        ps = [p for p in g.passos if s in p.skills]
        papel = g.papeis.get(s, [])
        estado = ("inexistente" if s not in e.skills else
                  "citada" if ps else "transversal" if "transversal" in papel else "órfã")
        cmds = sorted({" ".join(c.caminho) for p in ps for c in p.scripts if not c.erro})
        skills.append({"skill": s, "papel": "; ".join(papel) or "—",
                       "passos": [p.onde for p in ps], "comandos": cmds, "estado": estado})
    comandos = []
    for caminho in sorted(e.comandos):
        if caminho in alias:
            continue
        ps = [p for p in g.passos if any(c.caminho == caminho for c in p.scripts)]
        estado = ("passo" if ps else "transversal" if caminho in transversais
                  else "não citado")
        comandos.append({
            "comando": " ".join(caminho), "opcoes": sorted(e.comandos[caminho].opcoes),
            "ajuda": e.comandos[caminho].ajuda, "passos": [p.onde for p in ps],
            "skills": sorted({s for p in ps for s in p.skills}), "estado": estado})
    cobertura = []
    for mod, et in g.etapas:
        ps = [p for p in g.passos if p.modulo == mod and p.etapa == et]
        tipos = [_apoio(a)[0] for p in ps for a in p.apoio]
        cobertura.append({
            "modulo": mod, "etapa": et, "passos": len(ps),
            "com_skill": sum(bool(p.skills) for p in ps),
            "com_comando": sum(bool(p.scripts) for p in ps),
            "manual": tipos.count("manual"), "lacuna": tipos.count("lacuna")})
    contagem = {"modelo": sum(p.origem == "modelo" for p in g.passos),
                "adaptacao": sum(p.origem == "adaptação" for p in g.passos),
                "total": len(g.passos)}
    correspondencia = ([{"tipo": "comando", "antigo": a, "canonico": n}
                        for a, n in sorted(e.aliases.items())]
                       + [{"tipo": "skill", "antigo": a, "canonico": n}
                          for a, n in sorted(e.renomeadas.items())])
    return {"passos": passos, "skills": skills, "comandos": comandos,
            "cobertura": cobertura, "contagem": contagem,
            "correspondencia": correspondencia}


def renderiza(e, g):
    """O texto de `docs/catalogo_de_apoio.md`. Sem data: o mesmo guia dá o mesmo arquivo."""
    v = visoes(e, g)
    c = v["contagem"]
    out = [
        "# Catálogo de apoio — skills e comandos por passo",
        "",
        f"Gerado de `{GUIA}` por `{COMANDO}`. **Não editar à mão**: altera-se o guia e "
        "regenera-se. A conferência `python3 -m rsl catalogo gerar` reprova este arquivo "
        "quando ele está defasado.",
        "",
        f"Passos: {c['modelo']} do modelo + {c['adaptacao']} de adaptação do projeto = "
        f"{c['total']}.",
        "",
        "## Por passo",
    ]
    atual = None
    for p in v["passos"]:
        chave = (p["modulo"], p["etapa"])
        if chave != atual:
            atual = chave
            out += ["", f"### {p['modulo']} › {p['etapa']}", "",
                    "| Passo | Origem | Fonte | Skills | Comandos | Apoio |",
                    "| --- | --- | --- | --- | --- | --- |"]
        apoio = "; ".join(f"{a['tipo']} — {a['razao']}" for a in p["apoio"]) or "—"
        out.append(f"| {_cel(p['passo'])} | {p['origem']} | "
                   f"{_cel('; '.join(p['fonte'])) or '—'} | {_lista(p['skills'])} | "
                   f"{_lista(p['comandos'])} | {_cel(apoio)} |")
    out += ["", "## Por skill", "",
            "| Skill | Papel | Passos | Comandos dos mesmos passos | Estado |",
            "| --- | --- | --- | --- | --- |"]
    for s in v["skills"]:
        out.append(f"| `{s['skill']}` | {s['papel']} | {_cel('; '.join(s['passos'])) or '—'} "
                   f"| {_lista(s['comandos'])} | {s['estado']} |")
    out += ["", "## Por comando", "",
            "Caminhos lidos do parser; a ajuda é a do próprio comando (`-h`).", "",
            "| Comando | Ajuda | Passos | Skills dos mesmos passos | Estado |",
            "| --- | --- | --- | --- | --- |"]
    for k in v["comandos"]:
        out.append(f"| `{k['comando']}` | {_cel(k['ajuda'])} | "
                   f"{_cel('; '.join(k['passos'])) or '—'} | {_lista(k['skills'])} | "
                   f"{k['estado']} |")
    out += ["", "## Cobertura por etapa", "",
            "| Módulo | Etapa | Passos | Com skill | Com comando | Manual | Lacuna |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for k in v["cobertura"]:
        out.append(f"| {k['modulo']} | {k['etapa']} | {k['passos']} | {k['com_skill']} | "
                   f"{k['com_comando']} | {k['manual']} | {k['lacuna']} |")
    out += ["", "## Passos sem skill nem comando", "",
            "| Passo | Apoio | Razão |", "| --- | --- | --- |"]
    for p in g.passos:
        if not (p.skills or p.scripts):
            for a in p.apoio or ["—"]:
                tipo, razao = _apoio(a)
                out.append(f"| {_cel(p.onde)} | {tipo} | {_cel(razao) or '—'} |")
    if v["correspondencia"]:
        out += ["", "## Correspondência de nomes", "",
                "| Tipo | Nome antigo | Nome canônico |", "| --- | --- | --- |"]
        for k in v["correspondencia"]:
            out.append(f"| {k['tipo']} | `{k['antigo']}` | `{k['canonico']}` |")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------- comando
def gera(e, gravar=False, como_json=False, caminho=None, saida=print):
    """Imprime o catálogo e confere; com `gravar`, grava `caminho` de forma atômica.

    Devolve o código de saída. Com `gravar`, a regra de catálogo defasado não se aplica
    (é o que se vai corrigir); qualquer outro problema recusa a gravação."""
    g = le_guia(e.guia, e.grupos, e.comandos) if e.guia is not None else None
    if g is None:
        raise DadosInvalidos(f"guia de procedimentos ausente: {GUIA}")
    problemas = confere(e, g, desligadas=frozenset({"defasado"}) if gravar else frozenset())
    lacunas = [(p, _apoio(a)[1]) for p in g.passos for a in p.apoio
               if _apoio(a)[0] == "lacuna"]
    texto = renderiza(e, g)
    if como_json:
        v = visoes(e, g)
        v["problemas"] = [{"regra": r, "mensagem": m} for r, m in problemas]
        v["lacunas"] = [{"passo": p.onde, "razao": r} for p, r in lacunas]
        saida(json.dumps(v, ensure_ascii=False, indent=2))
    elif not gravar:
        saida(texto)
    if not como_json:
        if lacunas:
            saida(f"Lacunas declaradas ({len(lacunas)} passo(s); relatadas, não reprovam):")
            for p, r in lacunas:
                saida(f"  - {p.onde} — {r}")
        if problemas:
            saida(f"PROBLEMAS DO CATÁLOGO ({len(problemas)}):")
            for _r, m in problemas:
                saida(f"  - {m}")
    if problemas:
        if gravar:
            saida("Gravação recusada: nada foi gravado.")
        return Saida.REPROVADO
    if gravar:
        from .geracao import grava_atomico                          # noqa: PLC0415
        destino = caminho or (_config.RAIZ / CATALOGO)
        grava_atomico(destino, texto)
        saida(f"Gravado: {CATALOGO if caminho is None else destino}.")
    return Saida.OK


def cmd_gerar(_ctx, a):
    return gera(carrega(), gravar=getattr(a, "gravar", False),
                como_json=getattr(a, "json", False))
