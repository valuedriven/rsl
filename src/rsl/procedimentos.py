"""Geração do procedimento de busca de cada base, inteiro, a partir do protocolo, do arquivo de
sementes, da fonte da base (`fonte.py`) e da flexão dos termos (`flexao.py`).

O procedimento (`[documentos] procedimento`) é saída: `procedimentos gerar` mostra a
diferença e, com `--gravar`, substitui o arquivo de forma atômica; `documentos conferir`
reprova o arquivo que difere do que se geraria. O esqueleto e o texto fixo são forma e vêm
da gramática; o que difere de base para base vem da fonte.

A composição devolve, além do texto, a estrutura (termos de cada faceta em cada consulta):
é dela que as conferências de cobertura leem, sem reconhecer campo nem filtro pelo texto.
"""

import difflib
import itertools
import os
import re
import string

from . import gramatica as G
from .config import RAIZ
from .erros import ProtocoloInvalido, Reprovado, Uso
from .flexao import Indecidivel, formas, formas_de_numero, le_excecoes
from .fonte import le_fonte, ordem_das_sondagens
from .geracao import grava_atomico
from .leitura import CAMADAS
from .saida import Saida, mais_grave


# --------------------------------------------------------------------- vocabulário
def idiomas_do_termo(d, fid):
    """{termo: [idiomas]} do quadro da faceta: o idioma de cada termo da STR."""
    f = next(x for x in d["tabelas"] if x["id"] == fid)
    saida = {}
    for i in d["idiomas"]:
        for c in CAMADAS:
            for t in f["camadas"][i][c]:
                saida.setdefault(t, [])
                if i not in saida[t]:
                    saida[t].append(i)
    return saida


def vigentes(fonte, d, fid):
    """Termos da STR da faceta nos idiomas e camadas que a fonte declara, na ordem da STR,
    menos a redução declarada."""
    cob = fonte["dado"]["cobertura"]
    idiomas = cob["idiomas"].get(fid, [])
    camadas = CAMADAS if cob["camadas"] == G.CAMADAS_TODAS else (CAMADAS[0],)
    f = next(x for x in d["tabelas"] if x["id"] == fid)
    admitidos = {t for i in idiomas for c in camadas for t in f["camadas"][i][c]}
    reduzidos = {r["termo"] for r in fonte["dado"].get("reducao", []) if r["faceta"] == fid}
    return [t for t in d["strings"][fid]["literais"] if t in admitidos and t not in reduzidos]


def flexiona(fonte, d, fid, termos, excecoes, flexao=True):
    """(termos com as formas de número logo depois de cada um, [(termo, forma, origem,
    idioma)], [Indecidivel]). Só nos idiomas da faceta com plural explícito."""
    idioma_de = idiomas_do_termo(d, fid)
    da_faceta = fonte["dado"]["cobertura"]["idiomas"].get(fid, [])
    # Forma de número de outro termo da STR da faceta (`thesauri` de `thesaurus`) não se
    # flexiona de novo, ainda que o bloco (um subconjunto) traga só ela.
    ja_flexionados = formas_de_numero(list(d["strings"][fid]["literais"]) + list(termos),
                                      lambda x: idioma_de.get(x, []), excecoes)
    saida, flexoes, indecidiveis = [], [], []
    for t in termos:
        if t not in saida:
            saida.append(t)
        if not flexao or t in ja_flexionados:
            continue
        for i in idioma_de.get(t, []):
            if i not in da_faceta or fonte["plural"].get(i) != G.PLURAL_EXPLICITO:
                continue
            try:
                for forma, origem in formas(t, i, excecoes):
                    flexoes.append((t, forma, origem, i))
                    if forma not in saida:
                        saida.append(forma)
            except Indecidivel as e:
                indecidiveis.append(e)
    return saida, flexoes, indecidiveis


# ---------------------------------------------------------------------- literais
def literal(termo, aspas):
    if aspas == G.ASPAS_TODO_TERMO or re.search(r"[\s-]", termo):
        return f'"{termo}"'
    return termo


def interior(termos, campo, forma, aspas):
    """Os termos ligados por OR, com o campo em cada um quando a forma é `prefixa`."""
    pre = campo if forma == G.FORMA_PREFIXA else ""
    return " OR ".join(pre + literal(t, aspas) for t in termos)


def grupo(termos, campo, forma, aspas):
    dentro = interior(termos, campo, forma, aspas)
    return f"{campo}({dentro})" if forma == G.FORMA_ENVOLVE else f"({dentro})"


# ------------------------------------------------------------------ composição
class Composicao:
    """Os blocos da base: strings da §3 e consultas de cada expressão, com a estrutura."""

    def __init__(self, ctx, d, fonte, flexao=True):
        self.d, self.fonte = d, fonte
        self.excecoes = le_excecoes(ctx)
        self.aspas = fonte["dado"]["composicao"]["aspas"]
        self.flexoes, self.indecidiveis, self.problemas = [], [], []
        self.faceta_de = {s["id"]: fid for fid, s in d["strings"].items()}
        self.strings = {}          # fid → {"id", "termos", "campo", "forma"}
        radical = {r["faceta"]: r for r in fonte["dado"].get("radical", [])}
        for fid in d["strings"]:
            comp = fonte["composicao"][fid]
            if fid in radical:
                r = radical[fid]
                self.strings[fid] = {"id": r["id"], "termos": list(r["termos"]),
                                     "campo": r["campo"], "forma": G.FORMA_PREFIXA
                                     if r["campo"] and comp["forma"] == G.FORMA_PREFIXA
                                     else comp["forma"], "radical": True,
                                     "rotulo": r["rotulo"]}
                continue
            termos, flex, indec = flexiona(fonte, d, fid, vigentes(fonte, d, fid),
                                           self.excecoes, flexao)
            self.flexoes += [(fid,) + x for x in flex]
            self.indecidiveis += indec
            self.strings[fid] = {"id": d["strings"][fid]["id"], "termos": termos,
                                 "campo": comp["campo"], "forma": comp["forma"]}
        self.subconjuntos = {}
        for s in fonte["dado"].get("subconjuntos", []):
            termos, flex, indec = flexiona(fonte, d, s["faceta"], s["termos"],
                                           self.excecoes, flexao)
            self.flexoes += [(s["faceta"],) + x for x in flex]
            self.indecidiveis += indec
            forma = fonte["composicao"][s["faceta"]]["forma"]
            self.subconjuntos[s["id"]] = {"id": s["id"], "faceta": s["faceta"],
                                          "termos": termos, "campo": s["campo"],
                                          "forma": forma, "rotulo": s["rotulo"]}
        self.clausulas = [c["clausula"] for c in fonte["dado"]["criterios"]
                          if c["destino"] == G.DESTINO_CONSULTA]
        self.expressoes = {e["id"]: self._expressao(e["id"])
                           for e in fonte["dado"]["execucao"]["expressoes"]}

    # ---- estatuto e rótulos
    def estatuto(self, ident):
        declarado = next(e.get("estatuto") for e in self.fonte["dado"]["execucao"]["expressoes"]
                         if e["id"] == ident)
        if declarado:
            return declarado
        p = self.d["papeis"]
        if ident == p["executada"]:
            return "executada"
        if ident == p["sonda"]:
            return "sonda"
        if ident in p["especificas"]:
            return "fidelidade"
        return "derivada"

    def _rotulo_faceta(self, fid):
        return self.fonte["composicao"][fid].get("rotulo") or fid

    # ---- consultas
    def _ancoras(self, partes):
        """Texto das âncoras: com proximidade, no mesmo campo, entre parênteses."""
        prox = self.fonte["proximidade"]
        if prox is None or len(partes) != 2:
            return [grupo(p["termos"], p["campo"], p["forma"], self.aspas) for p in partes]
        a, b = partes
        if a["forma"] != G.FORMA_ENVOLVE or (a["campo"], a["forma"]) != (b["campo"], b["forma"]):
            raise ProtocoloInvalido(G.D_PROXIMIDADE, "proximidade entre âncoras exige as duas "
                                                     "no mesmo campo, na forma `envolve`",
                                    self.fonte["doc"])
        op = f"{prox['operador']}/{prox['distancia']}"
        ia = interior(a["termos"], "", G.FORMA_ENVOLVE, self.aspas)
        ib = interior(b["termos"], "", G.FORMA_ENVOLVE, self.aspas)
        return [f"{a['campo']}(({ia}) {op} ({ib}))"]

    def _texto(self, ancoras, outros):
        """(texto, [(índice do grupo em `outros`, alternativa)]) de uma consulta."""
        partes = list(self._ancoras(ancoras))
        for g in outros:
            if len(g) == 1:
                partes.append(grupo(g[0]["termos"], g[0]["campo"], g[0]["forma"], self.aspas))
            else:
                partes.append("(" + " OR ".join(grupo(x["termos"], x["campo"], x["forma"],
                                                      self.aspas) for x in g) + ")")
        return " AND ".join(partes) + "".join(" " + c for c in self.clausulas)

    def _parte(self, fid, campo_q):
        """A string de uma faceta numa consulta: a da consulta de campo, se há."""
        if campo_q is not None and campo_q["faceta"] == fid:
            alvo = self.subconjuntos.get(campo_q["string"]) or self.strings[fid]
            forma = self.fonte["composicao"][fid]["forma"]
            return {"fid": fid, "termos": alvo["termos"], "campo": campo_q["campo"],
                    "forma": forma}
        s = self.strings[fid]
        return {"fid": fid, "termos": s["termos"], "campo": s["campo"], "forma": s["forma"]}

    def _expressao(self, ident):
        estatuto = self.estatuto(ident)
        if estatuto not in G.ESTATUTOS_COM_BLOCO:
            return {"id": ident, "estatuto": estatuto, "consultas": []}
        if self.fonte["dado"]["execucao"]["forma"] == "curada" and \
                ident == self.d["executada"]:
            consultas = [{"id": f"{n}", "rotulo": f"{c['grupo']} — consulta {n}",
                          "texto": c["consulta"], "termos": None, "facetas": c["facetas"]}
                         for n, c in enumerate(self.fonte["dado"]["curadas"], 1)]
            return {"id": ident, "estatuto": estatuto, "consultas": consultas}
        n = ident[len(G.I_EB.prefixo):]
        ancoras_ids = [g[0] for g in self.d["papeis"]["ancoras"]]
        grupos = self.d["expressoes"][ident]
        campos = self.fonte["dado"].get("consultas_de_campo") or [None]
        separada = self.fonte["dado"]["composicao"]["disjuncao"] == G.DISJUNCAO_SEPARADA
        alternativas = []          # por grupo não âncora: (alternativas, separado?)
        for g in grupos:
            if g[0] in ancoras_ids and len(g) == 1:
                continue
            if separada and len(g) > 1:
                alternativas.append([([x], True) for x in g])
            else:
                alternativas.append([(g, False)])
        combinacoes = list(itertools.product(campos, *alternativas))
        multiplas = len(combinacoes) > 1 or campos != [None]
        consultas = []
        for k, (campo_q, *escolhas) in enumerate(combinacoes):
            letra = string.ascii_lowercase[k] if multiplas else ""
            rotulos = [campo_q["rotulo"]] if campo_q else []
            rotulos += [self._rotulo_faceta(self.faceta_de[g[0]]) for g, sep in escolhas if sep]
            rotulo = " × ".join(rotulos)
            escolha = [g for g, _ in escolhas]
            ancoras = [self._parte(self.faceta_de[a], campo_q) for a in ancoras_ids]
            outros = [[self._parte(self.faceta_de[x], campo_q) for x in g] for g in escolha]
            consultas += self._particiona(ident, n, letra, rotulo, ancoras, outros)
        return {"id": ident, "estatuto": estatuto, "consultas": consultas}

    def _particiona(self, ident, n, letra, rotulo, ancoras, outros):
        """Uma consulta, ou as partes contíguas do maior grupo não âncora até caber no teto."""
        teto = self.fonte["teto"]

        def consulta(ident_c, rot, outros_):
            termos = {}
            for p in ancoras + [x for g in outros_ for x in g]:
                termos.setdefault(p["fid"], [])
                termos[p["fid"]] += [t for t in p["termos"] if t not in termos[p["fid"]]]
            return {"id": ident_c, "rotulo": rot, "texto": self._texto(ancoras, outros_),
                    "termos": termos}
        inteira = consulta(f"{n}{letra}", rotulo, outros)
        if teto is None or len(inteira["texto"]) <= teto:
            return [inteira]
        if self.fonte["dado"]["execucao"]["forma"] == "unica":
            raise Reprovado(f"{self.fonte['sigla']}: {ident} — consulta "
                            f"{inteira['id'] or ident} com {len(inteira['texto'])} caracteres, "
                            f"acima do teto ({teto}), e `[execucao] forma = \"unica\"`")
        sem_outros = self._texto(ancoras, [])
        if len(sem_outros) > teto or not outros:
            raise Reprovado(f"{self.fonte['sigla']}: {ident} — as âncoras sozinhas têm "
                            f"{len(sem_outros)} caracteres, acima do teto ({teto})")
        # O grupo a partir: o de maior comprimento entre os não âncora.
        gi, xi = max(((i, j) for i, g in enumerate(outros) for j in range(len(g))),
                     key=lambda ij: len(interior(outros[ij[0]][ij[1]]["termos"], "",
                                                 G.FORMA_ENVOLVE, self.aspas)))
        alvo = outros[gi][xi]
        partes, atual = [], []
        for t in alvo["termos"]:
            tentativa = atual + [t]
            mud = [list(g) for g in outros]
            mud[gi][xi] = dict(alvo, termos=tentativa)
            if len(self._texto(ancoras, mud)) <= teto:
                atual = tentativa
                continue
            if not atual:
                raise Reprovado(f"{self.fonte['sigla']}: {ident} — o termo {t!r} sozinho com "
                                f"as demais facetas passa do teto ({teto})")
            partes.append(atual)
            atual = [t]
        partes.append(atual)
        if [t for p in partes for t in p] != alvo["termos"]:
            raise Reprovado(f"{self.fonte['sigla']}: {ident} — a união das partes difere do "
                            f"grupo original")
        saida = []
        letra = letra or "a"
        for k, p in enumerate(partes, 1):
            mud = [list(g) for g in outros]
            mud[gi][xi] = dict(alvo, termos=p)
            rot = f"{rotulo + ', ' if rotulo else ''}parte {k} de {len(partes)}"
            saida.append(consulta(f"{n}{letra}{k}", rot, mud))
        return saida

    def consultas_executaveis(self):
        """[(expressão, id da consulta, rótulo, texto)] do que vai à base."""
        return [(e["id"], c["id"], c["rotulo"], c["texto"])
                for e in self.expressoes.values() for c in e["consultas"]]


# ------------------------------------------------------------------ texto gerado
def _tabela(colunas, linhas, centro=()):
    cab = "| " + " | ".join(colunas) + " |"
    sep = "| " + " | ".join(":---:" if i in centro else ":---" for i in range(len(colunas))) \
        + " |"
    return [cab, sep] + ["| " + " | ".join(x.replace("|", "\\|") for x in l) + " |"
                         for l in linhas]


def _estudo(s):
    nomes = [a.split(",")[0].strip() for a in s["autores"]]
    if len(nomes) == 1:
        quem = nomes[0]
    elif len(nomes) == 2:
        quem = f"{nomes[0]} & {nomes[1]}"
    else:
        quem = f"{nomes[0]} et al."
    return f"{quem} ({s['ano']})"


def _situacao(item):
    texto = G.SITUACAO_TEXTO[item["situacao"]]
    if item.get("citacao"):
        texto += f" ({item['citacao']})"
    if item.get("nota"):
        texto += f"; {item['nota']}"
    return texto


def _sondagem_celula(item):
    if item.get("sondagem"):
        return item["sondagem"]
    if item.get("sem_sondagem"):
        return f"sem sondagem: {item['sem_sondagem']}"
    return "—"


def _cor(fonte, fid):
    cor = fonte["composicao"][fid].get("cor")
    return f" {cor}" if cor else ""


def _facetas_da_expressao(comp, ident):
    fonte, d = comp.fonte, comp.d
    partes = []
    for g in d["expressoes"][ident]:
        nomes = [f"{comp.faceta_de[x]}{' (' + fonte['composicao'][comp.faceta_de[x]]['cor'] + ')' if fonte['composicao'][comp.faceta_de[x]].get('cor') else ''}"
                 for x in g]
        partes.append(nomes[0] if len(nomes) == 1 else "(" + " OR ".join(nomes) + ")")
    return " AND ".join(partes)


def _fragmento(fonte, nome):
    texto = fonte["fragmentos"].get(nome, "").strip("\n")
    return [texto, ""] if texto else []


def _resultados(registro, bd, sd):
    if not registro:
        return []
    base = (registro.get("bases") or {}).get(bd) or {}
    return [r for r in base.get("sondagens") or [] if isinstance(r, dict)
            and r.get("sondagem") == sd]


def roteiro(fonte, registro=None):
    """Linhas da subseção de sondagens, na ordem de `depende_de` e do id."""
    sondagens = fonte["sondagens"]
    if not sondagens:
        return []
    situacao = {s["elemento"]: s["situacao"] for s in fonte["dado"]["sintaxe"]}
    situacao.update({r["texto"]: r["situacao"]
                     for r in fonte["dado"].get("regras_de_montagem", [])})
    L = [G.ESQUELETO["s1_sondagens"], "", G.TEXTO_FIXO["s1_seguranca"], ""]
    for sd in ordem_das_sondagens(sondagens):
        s = sondagens[sd]
        L += [f"#### {sd} — {s['objetivo']}", ""]
        L.append("**Elementos verificados:** " + "; ".join(
            f"{e} ({G.SITUACAO_TEXTO[situacao[e]].strip('*')})" for e in s["elementos"]) + ".")
        if s.get("depende_de"):
            L.append(f"**Depende de:** {', '.join(s['depende_de'])}.")
        L += ["", "**Pré-requisitos.**", ""] + [f"- {x}" for x in s["pre_requisitos"]] + [""]
        for k, c in enumerate(s["consultas"], 1):
            muda = f" Muda em relação ao controle: {c['muda']}." if c.get("muda") else ""
            L += [f"**Consulta {k} — {c['papel']}**, em {c['onde']}.{muda}", "", "```",
                  c["texto"], "```", ""]
        L += ["**Passos.**", ""] + [f"{k}. {x}" for k, x in enumerate(s["passos"], 1)] + [""]
        L += ["**Observar.**", ""] + [f"- {x}" for x in s["observar"]] + [""]
        L += _tabela(("#", "Resultado", "Conclusão", "Estado"),
                     [(str(k), l["resultado"], l["conclusao"],
                       G.SITUACAO_TEXTO[l["estado"]].strip("*"))
                      for k, l in enumerate(s["leituras"], 1)], centro=(0,)) + [""]
        L += ["**Evidência a registrar.**", ""] + [f"- {x}" for x in s["evidencia"]] + [""]
        feitos = _resultados(registro, fonte["bd"], sd)
        if feitos:
            L += ["**Resultados registrados.**", ""] + [
                f"- ({fonte['bd']}/{r.get('id')}) {r.get('data_hora')}: leitura "
                f"{(r.get('leitura') or {}).get('numero')}" for r in feitos] + [""]
    return L


def texto_procedimento(ctx, d, fonte, comp, registro=None):
    """O procedimento inteiro, como texto."""
    E, T, dado = G.ESQUELETO, G.TEXTO_FIXO, fonte["dado"]
    sigla, executada, sonda = fonte["sigla"], d["executada"], d["sonda"]
    L = [E["titulo"].format(nome=fonte["nome"]), "",
         T["aviso"].format(sigla=sigla, fonte=fonte["pasta"]), ""]

    # §1
    L += [E["s1"], ""]
    L += _tabela(E["s1_colunas"], [(s["elemento"], s["categoria"], _situacao(s),
                                    s.get("fonte") or "—", _sondagem_celula(s))
                                   for s in dado["sintaxe"]]) + [""]
    L += _fragmento(fonte, "notas_sintaxe.md")
    L += roteiro(fonte, registro)
    L += [E["separador"], ""]

    # §2
    L += [E["s2"], ""]
    L += _tabela(E["s2_colunas"], [(c["rotulo"], " / ".join(c["ids"]),
                                    G.DESTINO_TEXTO[c["destino"]], c["como"])
                                   for c in dado["criterios"]], centro=(1,)) + [""]
    L += [E["separador"], ""]

    # §3
    mapa = " · ".join(f"**{f['id']}**{_cor(fonte, f['id'])}" for f in d["facetas"])
    L += [E["s3"], "", T["s3_intro"].format(mapa=mapa), "", E["s3_declaracao"], "",
          T["s3_declaracao"].format(fonte=f"{fonte['pasta']}/procedimento.toml"), ""]
    cob = dado["cobertura"]
    plural = cob["plural"] if isinstance(cob["plural"], str) else \
        "; ".join(f"{i}: {v}" for i, v in cob["plural"].items())
    derivacoes = cob.get("derivacoes") or []
    L += _tabela(("Parâmetro", "Valor"), [
        ("idiomas", "; ".join(f"{fid}: {', '.join(v)}" for fid, v in cob["idiomas"].items())),
        ("camadas", cob["camadas"]), ("plural", plural),
        ("teto de caracteres", str(cob["teto"])),
        ("derivações", " e ".join(derivacoes) if derivacoes else "nenhuma")]) + [""]
    if dado.get("reducao"):
        L += [T["s3_reducao"], ""]
        L += _tabela(("Faceta", "Termo fora da string", "Motivo"),
                     [(r["faceta"], r["termo"], r["motivo"]) for r in dado["reducao"]]) + [""]
    ancoras = set(d["ancoras"])
    for f in d["facetas"]:
        fid = f["id"]
        s = comp.strings[fid]
        n = s["id"][len(G.I_STR.prefixo):]
        extra = " — **âncora obrigatória**" if fid in ancoras else ""
        radical = f" — forma radical: {s['rotulo']}" if s.get("radical") else ""
        L += [f"### `{s['id']}` — string `#{n}` —{_cor(fonte, fid)} {fid} — {f['nome']}"
              f"{radical}{extra}", "", "```",
              grupo(s["termos"], s["campo"], s["forma"], comp.aspas), "```", ""]
        for sub in (x for x in comp.subconjuntos.values() if x["faceta"] == fid):
            m = sub["id"][len(G.I_STR.prefixo):]
            L += [f"### `{sub['id']}` — string `#{m}` —{_cor(fonte, fid)} {fid} — "
                  f"{sub['rotulo']}", "", "```",
                  grupo(sub["termos"], sub["campo"], sub["forma"], comp.aspas), "```", ""]
    L += [E["separador"], ""]

    # §4
    L += [E["s4"], "", "```"]
    linhas = []
    for ident, grupos in sorted(d["expressoes"].items(), key=lambda x: int(x[0][2:])):
        partes = [f"#{g[0][3:]}" if len(g) == 1 else
                  "(" + " OR ".join(f"#{x[3:]}" for x in g) + ")" for g in grupos]
        linhas.append((f"{ident} = {' AND '.join(partes)}",
                       G.ESTATUTO_PAPEL.get("executada" if ident == executada else
                                            "sonda" if ident == sonda else "", "")))
    largura = max(len(a) for a, _ in linhas) + 5
    L += [(a.ljust(largura) + b).rstrip() for a, b in linhas] + ["```", ""]
    por_estatuto = {}
    for e in comp.expressoes.values():
        por_estatuto.setdefault(e["estatuto"], []).append(e["id"])
    L += _tabela(("Expressão", "Execução"),
                 [(", ".join(f"**{x}**" for x in sorted(por_estatuto[k],
                                                        key=lambda y: int(y[2:]))),
                   G.EXECUCAO_TEXTO[k]) for k in G.ESTATUTOS if k in por_estatuto]) + [""]
    L.append(f"{G.LINHA_EXECUCAO} {G.FORMA_EXECUCAO_TEXTO[dado['execucao']['forma']]}")
    if "fidelidade" in por_estatuto:
        L.append(T["fidelidade"].format(expressoes="/".join(por_estatuto["fidelidade"])))
    if comp.estatuto(sonda) == "sonda":
        L.append(T["sensibilidade"].format(sonda=sonda, executada=executada))
    L.append(T["retorno_zero"].format(sonda=sonda, executada=executada))
    L.append("")
    L += _fragmento(fonte, "notas_execucao.md")
    if dado.get("regras_de_montagem"):
        L += [E["s4_montagem"], ""]
        L += _tabela(("Regra", "Situação", "Sondagem"),
                     [(r["texto"], _situacao(r), _sondagem_celula(r))
                      for r in dado["regras_de_montagem"]]) + [""]
    if fonte["fragmentos"].get("estrategia_de_proximidade.md"):
        L += [E["s4_proximidade"], ""] + _fragmento(fonte, "estrategia_de_proximidade.md")
    titulos = {e["id"]: e["titulo"] for e in dado["execucao"]["expressoes"]}
    for ident in sorted(comp.expressoes, key=lambda x: int(x[2:])):
        e = comp.expressoes[ident]
        L += [f"### {ident} ({titulos[ident]})", "",
              f"*{G.ESTATUTO_FRASE[e['estatuto']]}* **Facetas:** "
              f"{_facetas_da_expressao(comp, ident)}", ""]
        unica = len(e["consultas"]) == 1 and e["consultas"][0]["id"].isdigit()
        for c in e["consultas"]:
            if not unica:
                L += [f"**Consulta {c['id']} — {c['rotulo']}**", ""]
            L += ["```", c["texto"], "```", ""]
    L += [E["s4_como"], ""] + _fragmento(fonte, "como_executar.md")
    if fonte["fragmentos"].get("variantes.md"):
        L += [E["s4_variantes"], ""] + _fragmento(fonte, "variantes.md")
    L += [E["separador"], ""]

    # §5
    obs = {s["id"]: s["observacao"] for s in dado.get("sementes", [])}
    L += [E["s5"], "", T["s5_intro"], ""]
    L += _tabela(("#", "Estudo", "DOI ou identificador", "Observação"),
                 [(s["id"], _estudo(s), f"`{s['doi']}`" if s.get("doi") else "—",
                   obs.get(s["id"], "—")) for s in d["sementes"] if sigla in s["bases"]],
                 centro=(0,)) + [""]
    L += [T["s5_procedimento"].format(executada=executada), "", T["s5_limiar"], ""]
    L += _fragmento(fonte, "notas_sementes.md")
    L += [E["separador"], ""]

    # §6
    L += [E["s6"], ""]
    L += [f"{k}. {r}" for k, r in enumerate(dado.get("ressalvas", []), 1)]
    return "\n".join(L).rstrip("\n") + "\n"


# --------------------------------------------------------------------- geração
def gera_base(ctx, d, sigla, flexao=True, registro=None):
    """(fonte, composição, texto) da base; ProtocoloInvalido ou Reprovado sobem."""
    fonte = le_fonte(ctx, d, sigla)
    comp = Composicao(ctx, d, fonte, flexao=flexao)
    if comp.indecidiveis:
        raise Reprovado(f"{sigla}: flexão indecidível — " + "; ".join(
            f"{e.termo!r} ({e.idioma}): {e.motivo}" for e in comp.indecidiveis)
            + f"; declarar a exceção em `{ctx.config.valor('documentos.flexoes')}`")
    return fonte, comp, texto_procedimento(ctx, d, fonte, comp, registro)


def _registro(ctx):
    import json                                                     # noqa: PLC0415
    caminho = ctx.config.caminho("dados.registro")
    try:
        return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else None
    except (OSError, ValueError):
        return None


def secao_de(linhas, idx):
    """O título de seção (`## …`) que contém a linha `idx`."""
    for i in range(idx, -1, -1):
        if i < len(linhas) and linhas[i].startswith("## "):
            return linhas[i][3:]
    return "início"


def diferenca(atual, novo):
    """Linhas legíveis da diferença, agrupadas por seção, com os termos a acrescentar e a
    retirar em cada bloco."""
    a, b = (atual or "").splitlines(), novo.splitlines()
    saida, ultima = [], None
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        sec = secao_de(b, j1) if j1 < len(b) else secao_de(a, i1)
        if sec != ultima:
            saida.append(f"  [§ {sec}]")
            ultima = sec
        velhas, novas = a[i1:i2], b[j1:j2]
        if len(velhas) == len(novas) == 1 and " OR " in velhas[0] + novas[0]:
            ta = set(re.findall(r'"[^"]+"|[^\s()]+', velhas[0]))
            tb = set(re.findall(r'"[^"]+"|[^\s()]+', novas[0]))
            mais, menos = sorted(tb - ta), sorted(ta - tb)
            saida.append(f"    bloco na linha {j1 + 1}: +{len(mais)} −{len(menos)} "
                         f"{('acrescenta ' + ', '.join(mais[:12])) if mais else ''}"
                         f"{' ; retira ' + ', '.join(menos[:12]) if menos else ''}")
            continue
        for x in velhas:
            saida.append(f"    - {x[:150]}")
        for x in novas:
            saida.append(f"    + {x[:150]}")
    return saida


def primeira_divergente(atual, novo):
    a, b = (atual or "").splitlines(), novo.splitlines()
    for k, (x, y) in enumerate(itertools.zip_longest(a, b), 1):
        if x != y:
            return k, x, y
    return None


def problemas_igualdade(ctx, d):
    """[(sigla, texto)] do procedimento gravado que difere da geração ou não existe. A base
    cuja fonte não se lê não entra aqui: já reprova pela leitura."""
    saida = []
    for b in d["bases"]:
        sigla = b["sigla"]
        try:
            _, _, novo = gera_base(ctx, d, sigla, registro=_registro(ctx))
        except (ProtocoloInvalido, Reprovado):
            continue
        atual = ctx.ficha(sigla, b["ficha"])
        correcao = f"`python3 -m rsl procedimentos gerar {sigla} --gravar`"
        if atual is None:
            saida.append((sigla, f"procedimento de busca {b['ficha']} não existe; gerar com "
                                 f"{correcao}"))
            continue
        div = primeira_divergente(atual, novo)
        if div:
            k, x, _ = div
            saida.append((sigla, f"procedimento de busca {b['ficha']} difere da geração a "
                                 f"partir da linha {k} ({(x or '')[:70]!r}); o procedimento "
                                 f"é saída — corrigir na fonte e gerar com {correcao}"))
    return saida


def _ensaio_flexoes(comp):
    linhas = []
    por = {}
    for fid, termo, forma, origem, idioma in comp.flexoes:
        por.setdefault((fid, idioma), []).append(f"{forma} ({origem})")
    for (fid, idioma), fs in sorted(por.items()):
        linhas.append(f"  formas de número em {fid}, {idioma}: {', '.join(fs)}")
    return linhas


def releitura(ctx):
    """Contexto que relê do disco o que não é cópia em memória (o autoteste injeta a
    mudança da fonte entre a leitura e a gravação por aqui)."""
    return ctx.com_fichas({})


def gera(ctx, siglas=None, gravar=False, saida=print):
    """Ensaio (diferença) ou gravação dos procedimentos. Devolve o código de saída."""
    d = ctx.protocolo()
    todas = [b["sigla"] for b in d["bases"]]
    siglas = siglas or todas
    codigo = Saida.OK
    registro = _registro(ctx)
    for sigla in siglas:
        b = next(x for x in d["bases"] if x["sigla"] == sigla)
        saida(f"== {sigla} ({b['ficha']})")
        try:
            fonte, comp, novo = gera_base(ctx, d, sigla, registro=registro)
        except (ProtocoloInvalido, Reprovado) as e:
            saida(f"  {e}")
            saida("  Nada foi gravado para esta base.")
            codigo = mais_grave(codigo, e.codigo)
            continue
        for linha in _ensaio_flexoes(comp):
            saida(linha)
        caminho = RAIZ / b["ficha"]
        atual = ctx.ficha(sigla, b["ficha"])
        if atual == novo:
            saida("  Sem diferença: o procedimento gravado é o gerado.")
            continue
        for linha in diferenca(atual, novo):
            saida(linha)
        if not gravar:
            saida("  Ensaio: nada foi gravado.")
            codigo = mais_grave(codigo, Saida.REPROVADO)
            continue
        # Relê as fontes imediatamente antes de gravar: fonte que mudou recusa a gravação.
        _, _, de_novo = gera_base(releitura(ctx), d, sigla, registro=registro)
        if de_novo != novo:
            saida("  Gravação recusada: a fonte mudou durante a execução. Nada foi gravado.")
            codigo = Saida.REPROVADO
            continue
        os.makedirs(caminho.parent, exist_ok=True)
        grava_atomico(caminho, novo)
        relido = caminho.read_text(encoding="utf-8")
        if relido != novo:
            raise Reprovado(f"{sigla}: o arquivo relido difere do gerado")
        saida(f"  Gravado: {b['ficha']}.")
    return codigo


def cmd_gerar(ctx, a):
    d = ctx.protocolo()
    todas = [b["sigla"] for b in d["bases"]]
    if a.sigla and a.sigla not in todas:
        raise Uso(f"base {a.sigla!r} não consta da tabela de bases do protocolo ({todas})")
    return gera(ctx, [a.sigla] if a.sigla else None, gravar=a.gravar)


# ----------------------------------------------------------------------- início
def _toml_texto(v):
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


def texto_inicio(d, sigla):
    """O texto de `procedimento.toml` de uma base nova, pelo modelo da gramática."""
    b = next(x for x in d["bases"] if x["sigla"] == sigla)
    P = _toml_texto(G.PENDENTE)
    sintaxe = "\n".join(
        f"[[sintaxe]]\nelemento = {_toml_texto(c)}\ncategoria = {_toml_texto(c)}\n"
        f"situacao = \"nao_verificado\"\nsondagem = {P}\n" for c in G.CATEGORIAS)
    criterios = []
    for c in d["criterios"]:
        criterios.append(f"[[criterios]]\nids = [{_toml_texto(c['id'])}]\n"
                         f"rotulo = {_toml_texto(c['dimensao'] + ' — ' + c['acao'])}\n"
                         f"destino = {P}\ncomo = {P}\n")
    idiomas = "\n".join(f"{f['id']} = [{', '.join(_toml_texto(i) for i in d['idiomas'])}]"
                        for f in d["facetas"])
    composicao = "\n".join(f"[[composicao.facetas]]\nfaceta = {_toml_texto(f['id'])}\n"
                           f"campo = {P}\nforma = {P}\n" for f in d["facetas"])
    expressoes = "\n".join(f"[[execucao.expressoes]]\nid = {_toml_texto(e)}\ntitulo = {P}\n"
                           for e in sorted(d["expressoes"], key=lambda x: int(x[2:])))
    sementes = "\n".join(f"[[sementes]]\nid = {_toml_texto(s['id'])}\nobservacao = \"—\"\n"
                         for s in d["sementes"] if sigla in s["bases"])
    return G.MODELO_INICIO.format(nome=b["nome"], bd=b["id"], sigla=sigla,
                                  pendente=G.PENDENTE, sintaxe=sintaxe,
                                  criterios="\n".join(criterios), idiomas=idiomas,
                                  composicao=composicao, expressoes=expressoes,
                                  sementes=sementes)


def inicia(ctx, sigla, saida=print):
    d = ctx.protocolo()
    todas = [b["sigla"] for b in d["bases"]]
    if sigla not in todas:
        raise Uso(f"base {sigla!r} não consta da tabela de bases do protocolo ({todas}): base "
                  f"nova é decisão de escopo e precisa primeiro ser registrada no protocolo")
    pasta = RAIZ / ctx.config.fonte(sigla)
    if pasta.exists():
        raise Uso(f"a fonte {ctx.config.fonte(sigla)} já existe; nada foi gravado")
    texto = texto_inicio(d, sigla)
    temporaria = pasta.parent / f".tmp_{sigla}"
    os.makedirs(temporaria, exist_ok=False)
    try:
        (temporaria / "procedimento.toml").write_text(texto, encoding="utf-8")
        (temporaria / G.FRAGMENTO_OBRIGATORIO).write_text(G.PENDENTE + "\n", encoding="utf-8")
        os.rename(temporaria, pasta)
    except BaseException:
        import shutil                                               # noqa: PLC0415
        shutil.rmtree(temporaria, ignore_errors=True)
        raise
    saida(f"Criada a fonte {ctx.config.fonte(sigla)}: procedimento.toml e "
          f"{G.FRAGMENTO_OBRIGATORIO}. Os campos {G.PENDENTE} são a lista de trabalho; a base "
          f"fica reprovada até não restar nenhum (`python3 -m rsl documentos conferir`).")
    return Saida.OK


def cmd_iniciar(ctx, a):
    return inicia(ctx, a.sigla)
