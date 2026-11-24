"""Leitura da fonte do procedimento de busca de cada base.

A fonte (`[documentos] procedimento_fonte`) é o que se edita: `procedimento.toml`, de esquema
fechado declarado na gramática, e os fragmentos de prosa de nome fixo. O procedimento de
busca é saída de `procedimentos gerar` e não se lê.

A validação reprova a base com PROTOCOLO_ILEGIVEL, nomeando a base, a tabela e o campo, ou o
fragmento e a linha; as demais bases não são afetadas. A marca PENDENTE reprova antes de
tudo, com a lista completa das marcas numa só mensagem. Nenhum valor de base está aqui: o
que difere de base para base vem da fonte.
"""

import re
import tomllib

from . import gramatica as G
from .erros import ProtocoloInvalido

_PENDENTE = re.compile(rf"\b{G.PENDENTE}\b")


def documento(sigla, pasta):
    return f"{G.FONTE} de {sigla} ({pasta})"


# ------------------------------------------------------------------- marca PENDENTE
def pendentes(dado, fragmentos):
    """Todas as marcas PENDENTE: ["tabela.campo" ou "fragmento:linha"], na ordem do texto."""
    saida = []

    def percorre(valor, caminho):
        if isinstance(valor, str):
            if _PENDENTE.search(valor):
                saida.append(caminho)
        elif isinstance(valor, list):
            for i, x in enumerate(valor):
                percorre(x, f"{caminho}[{i + 1}]" if isinstance(x, (dict, list)) or
                         len(valor) > 1 else caminho)
        elif isinstance(valor, dict):
            for k, v in valor.items():
                percorre(v, f"{caminho}.{k}" if caminho else k)
    percorre(dado, "")
    for nome in sorted(fragmentos):
        for n, linha in enumerate(fragmentos[nome].splitlines(), 1):
            if _PENDENTE.search(linha):
                saida.append(f"{nome}:{n}")
    return saida


# ------------------------------------------------------------------- esquema fechado
def _valida_tabela(decl, valor, onde, doc):
    """Confere um item de tabela contra a declaração: campos desconhecidos, obrigatórios,
    tipos e domínios, e recursivamente as subtabelas."""
    if not isinstance(valor, dict):
        raise ProtocoloInvalido(decl, f"{onde}: não é tabela", doc)
    conhecidos = {c.chave for c in decl.campos} | {s.local for s in decl.subtabelas}
    desconhecidos = sorted(set(valor) - conhecidos)
    if desconhecidos:
        raise ProtocoloInvalido(decl, f"{onde}: campo desconhecido {desconhecidos} "
                                      f"(admitidos: {sorted(conhecidos)})", doc)
    for c in decl.campos:
        if c.chave not in valor:
            if c.exigido:
                raise ProtocoloInvalido(c, f"{onde}: falta o campo obrigatório "
                                           f"`{c.chave}`", doc)
            continue
        v = valor[c.chave]
        if not c.aceita(v):
            raise ProtocoloInvalido(c, f"{onde}: `{c.chave}` não é {c.tipo_valor} "
                                       f"({v!r})", doc)
        if c.dominio and isinstance(v, str) and c.tipo_valor == "texto" \
                and v not in c.dominio:
            raise ProtocoloInvalido(c, f"{onde}: `{c.chave}` = {v!r} fora do domínio; "
                                       f"admitidos: {list(c.dominio)}", doc)
        if c.dominio and c.tipo_valor == "lista de textos":
            fora = [x for x in v if x not in c.dominio]
            if fora:
                raise ProtocoloInvalido(c, f"{onde}: `{c.chave}` com {fora} fora do "
                                           f"domínio; admitidos: {list(c.dominio)}", doc)
    for s in decl.subtabelas:
        _valida_presenca(s, valor.get(s.local), f"{onde}.{s.local}" if onde else s.local,
                         doc)


def _valida_presenca(decl, valor, onde, doc):
    """Tabela única ou lista de tabelas: presença, quantidade mínima e cada item."""
    if valor is None:
        if decl.exigido:
            raise ProtocoloInvalido(decl, f"falta {decl.rotulo}", doc)
        return
    if decl.multipla:
        if not isinstance(valor, list) or not all(isinstance(x, dict) for x in valor):
            raise ProtocoloInvalido(decl, f"{onde}: não é lista de tabelas "
                                          f"({decl.rotulo})", doc)
        if len(valor) < decl.minimo:
            raise ProtocoloInvalido(decl, f"{onde}: {len(valor)} item(ns); exige ao menos "
                                          f"{decl.minimo}", doc)
        for i, item in enumerate(valor, 1):
            _valida_tabela(decl, item, f"{onde}[{i}]", doc)
    else:
        _valida_tabela(decl, valor, onde, doc)


def valida_esquema(dado, doc, raiz=G.T_RAIZ):
    """O esquema fechado de um arquivo TOML: raiz, tabelas e campos."""
    tabelas = [t for t in G.ELEMENTOS if isinstance(t, G.TabelaFonte)
               and t.documento == raiz.documento and t.pai is None and t is not raiz]
    conhecidos = {c.chave for c in raiz.campos} | {t.chave for t in tabelas}
    desconhecidos = sorted(set(dado) - conhecidos)
    if desconhecidos:
        raise ProtocoloInvalido(raiz, f"chave desconhecida {desconhecidos} (admitidas: "
                                      f"{sorted(conhecidos)})", doc)
    _valida_tabela(raiz, {k: v for k, v in dado.items() if k in
                          {c.chave for c in raiz.campos}}, "", doc)
    for t in tabelas:
        _valida_presenca(t, dado.get(t.chave), t.chave, doc)


# ------------------------------------------------------------------ validações da fonte
def _citacao(valor, bd, elemento, onde, doc):
    m = re.fullmatch(G.F_CITACAO.padrao, valor or "")
    if not m:
        raise ProtocoloInvalido(elemento, f"{onde}: citação {valor!r} fora da forma "
                                          f"`BDn/<id>`", doc)
    if m.group(1) != bd:
        raise ProtocoloInvalido(elemento, f"{onde}: cita {valor!r}, de outra base; a "
                                          f"citação tem de ser de {bd}", doc)


def _verificacao(item, nome, tabela, bd, sondagens, doc):
    """Situação de um elemento ou regra: `medicao` exige citação; `nao_verificado`,
    sondagem que o liste ou o motivo de não a ter."""
    onde = f"{tabela.chave} {nome!r}"
    situacao = item["situacao"]
    if situacao == G.SITUACAO_MEDICAO:
        if not item.get("citacao"):
            raise ProtocoloInvalido(G.C_CITACAO, f"{onde}: `situacao = \"medicao\"` sem "
                                                 f"`citacao`", doc)
    if item.get("citacao"):
        _citacao(item["citacao"], bd, G.C_CITACAO, onde, doc)
    sd = item.get("sondagem")
    if sd is not None:
        if sd not in sondagens:
            raise ProtocoloInvalido(tabela, f"{onde}: sondagem {sd!r} não existe em "
                                            f"[[sondagens]]", doc)
        if nome not in sondagens[sd]["elementos"]:
            raise ProtocoloInvalido(tabela, f"{onde}: a sondagem {sd} não lista o elemento "
                                            f"em `elementos`", doc)
    if situacao == G.SITUACAO_NAO_VERIFICADO and sd is None and not item.get("sem_sondagem"):
        raise ProtocoloInvalido(tabela, f"{onde}: `nao_verificado` sem `sondagem` nem "
                                        f"`sem_sondagem`", doc)


def _ciclo(sondagens):
    """Primeiro ciclo em `depende_de`, como lista de ids; None se não há."""
    estado = {}

    def visita(sd, pilha):
        estado[sd] = 1
        for dep in sondagens[sd].get("depende_de", []):
            if estado.get(dep) == 1:
                return pilha[pilha.index(dep):] + [dep] if dep in pilha else [sd, dep]
            if dep not in estado:
                achado = visita(dep, pilha + [dep])
                if achado:
                    return achado
        estado[sd] = 2
        return None
    for sd in sondagens:
        if sd not in estado:
            achado = visita(sd, [sd])
            if achado:
                return achado
    return None


def ordem_das_sondagens(sondagens):
    """Ids na ordem de `depende_de` e, dentro dela, na ordem do id (sem ciclo)."""
    feitos, saida = set(), []
    numero = {sd: int(sd[len(G.I_SD.prefixo):]) for sd in sondagens}
    pendentes_ = sorted(sondagens, key=numero.get)
    while pendentes_:
        prontos = [sd for sd in pendentes_
                   if set(sondagens[sd].get("depende_de", [])) <= feitos]
        proximo = prontos[0]
        saida.append(proximo)
        feitos.add(proximo)
        pendentes_.remove(proximo)
    return saida


def _valida_sondagens(lista, nomes, doc):
    sondagens = {}
    for i, s in enumerate(lista, 1):
        sd = s["id"]
        if not G.I_SD.casa(sd):
            raise ProtocoloInvalido(G.I_SD, f"sondagens[{i}]: id {sd!r} fora da forma SDn",
                                    doc)
        if sd in sondagens:
            raise ProtocoloInvalido(G.T_SONDAGENS, f"sondagem {sd} repetida", doc)
        sondagens[sd] = s
    esperado = [f"{G.I_SD.prefixo}{n}" for n in range(1, len(lista) + 1)]
    if sorted(sondagens, key=lambda x: int(x[2:])) != esperado:
        raise ProtocoloInvalido(G.I_SD, f"ids {sorted(sondagens)} fora da sequência "
                                        f"{esperado}", doc)
    for sd, s in sondagens.items():
        for el in s["elementos"]:
            if el not in nomes:
                raise ProtocoloInvalido(G.T_SONDAGENS, f"{sd}: elemento {el!r} não existe em "
                                                       f"[[sintaxe]] nem em "
                                                       f"[[regras_de_montagem]]", doc)
        if not any(l["estado"] == G.SITUACAO_NAO_VERIFICADO for l in s["leituras"]):
            raise ProtocoloInvalido(G.T_SOND_LEITURAS, f"{sd}: falta a leitura inconclusiva "
                                                        f"(estado \"nao_verificado\")", doc)
        for dep in s.get("depende_de", []):
            if dep not in sondagens:
                raise ProtocoloInvalido(G.T_SONDAGENS, f"{sd}: depende de {dep!r}, que não "
                                                       f"existe", doc)
    ciclo = _ciclo(sondagens)
    if ciclo:
        raise ProtocoloInvalido(G.T_SONDAGENS, f"ciclo em `depende_de`: "
                                               f"{' → '.join(ciclo)}", doc)
    return sondagens


def _valida_fragmentos(fonte_bruta, doc):
    admitidos = sorted(G.FRAGMENTOS)
    fragmentos = fonte_bruta.get("fragmentos", {})
    for nome in fonte_bruta.get("arquivos", sorted(fragmentos)) or []:
        if nome == "procedimento.toml":
            continue
        if nome not in G.FRAGMENTOS:
            raise ProtocoloInvalido(G.FR_FRAGMENTOS, f"arquivo {nome!r} não é fragmento "
                                                     f"admitido ({admitidos})", doc)
    for nome in fragmentos:
        if nome not in G.FRAGMENTOS:
            raise ProtocoloInvalido(G.FR_FRAGMENTOS, f"fragmento {nome!r} não é admitido "
                                                     f"({admitidos})", doc)
    if G.FRAGMENTO_OBRIGATORIO not in fragmentos:
        raise ProtocoloInvalido(G.FR_FRAGMENTOS, f"falta o fragmento "
                                                 f"{G.FRAGMENTO_OBRIGATORIO!r}", doc)
    for nome, texto in fragmentos.items():
        quatro = G.FRAGMENTOS[nome][1]
        cercado = False
        for n, linha in enumerate(texto.splitlines(), 1):
            if linha.strip().startswith("```"):
                cercado = not cercado
                continue
            if cercado:
                continue
            m = re.match(r"^(#{1,6})\s", linha)
            if m and (len(m.group(1)) <= 3 or (len(m.group(1)) == 4 and not quatro)):
                raise ProtocoloInvalido(G.FR_FRAGMENTOS, f"{nome}:{n}: título "
                                                         f"{linha.strip()[:60]!r} quebraria o "
                                                         f"esqueleto", doc)
            if linha.strip().startswith(G.LINHA_EXECUCAO):
                raise ProtocoloInvalido(G.FR_FRAGMENTOS, f"{nome}:{n}: a linha "
                                                         f"`{G.LINHA_EXECUCAO}` só vem da "
                                                         f"fonte (`[execucao] forma`)", doc)
    return fragmentos


def _plural(cobertura, idiomas_base, doc):
    """{idioma: valor} do plural, único ou por idioma."""
    plural = cobertura["plural"]
    dominio = G.D_PLURAL_F.dominio
    if isinstance(plural, str):
        if plural not in dominio:
            raise ProtocoloInvalido(G.D_PLURAL_F, f"plural {plural!r} fora do domínio; "
                                                  f"admitidos: {list(dominio)}", doc)
        return {i: plural for i in idiomas_base}
    fora = {k: v for k, v in plural.items() if v not in dominio}
    if fora:
        raise ProtocoloInvalido(G.D_PLURAL_F, f"plural {fora} fora do domínio; admitidos: "
                                              f"{list(dominio)}", doc)
    faltam = [i for i in idiomas_base if i not in plural]
    if faltam:
        raise ProtocoloInvalido(G.D_PLURAL_F, f"plural sem valor para {faltam}", doc)
    return {i: plural[i] for i in idiomas_base}


def _teto(valor, doc):
    if valor == G.TETO_NENHUM:
        return None
    if isinstance(valor, int) and valor > 0:
        return valor
    raise ProtocoloInvalido(G.D_TETO_F, f"teto {valor!r} não é inteiro positivo de "
                                        f"caracteres nem {G.TETO_NENHUM!r}", doc)


def le_fonte(ctx, d, sigla, sem_pendente=True):
    """A fonte validada da base `sigla`. ProtocoloInvalido nomeia a base e o defeito."""
    b = next((x for x in d["bases"] if x["sigla"] == sigla), None)
    if b is None:
        raise ProtocoloInvalido(G.T_BASES, f"base {sigla!r} não consta da tabela "
                                           f"({[x['sigla'] for x in d['bases']]})")
    pasta = ctx.config.fonte(sigla)
    doc = documento(sigla, pasta)
    bruta = ctx.fonte_bruta(sigla, pasta)
    if bruta is None:
        raise ProtocoloInvalido(G.T_RAIZ, f"{b['id']} {sigla!r}: fonte inexistente — "
                                          f"procurado {pasta}/procedimento.toml "
                                          f"(`documentos.procedimento_fonte` do "
                                          f"{ctx.config.nome})", doc)
    dado = bruta["toml"]
    if isinstance(dado, str):
        try:
            dado = tomllib.loads(dado)
        except tomllib.TOMLDecodeError as e:
            raise ProtocoloInvalido(G.T_RAIZ, f"procedimento.toml não é TOML válido: {e}",
                                    doc) from None
    fragmentos = dict(bruta.get("fragmentos", {}))
    marcas = pendentes(dado, fragmentos)
    if marcas and sem_pendente:
        raise ProtocoloInvalido(G.T_RAIZ, f"{len(marcas)} marca(s) {G.PENDENTE} — "
                                          f"{', '.join(marcas)}", doc)
    valida_esquema(dado, doc)
    fragmentos = _valida_fragmentos(bruta, doc)
    bd = b["id"]

    # Facetas, idiomas e expressões do protocolo: a fonte não declara o que não existe.
    facetas = [f["id"] for f in d["facetas"]]
    cobertura = dado["cobertura"]
    for fid, idiomas in cobertura["idiomas"].items():
        if fid not in facetas:
            raise ProtocoloInvalido(G.T_COBERTURA, f"idiomas: faceta {fid!r} não existe no "
                                                   f"protocolo", doc)
        fora = [i for i in idiomas if i not in d["idiomas"]]
        if fora:
            raise ProtocoloInvalido(G.T_COBERTURA, f"idiomas de {fid}: {fora} fora do quadro "
                                                   f"{list(d['idiomas'])}", doc)
    idiomas_base = [i for i in d["idiomas"]
                    if any(i in v for v in cobertura["idiomas"].values())]
    plural = _plural(cobertura, idiomas_base, doc)
    teto = _teto(cobertura["teto"], doc)

    # Sintaxe, regras e sondagens.
    sintaxe = dado["sintaxe"]
    nomes = [s["elemento"] for s in sintaxe]
    repetidos = sorted({n for n in nomes if nomes.count(n) > 1})
    if repetidos:
        raise ProtocoloInvalido(G.T_SINTAXE, f"elemento repetido {repetidos}", doc)
    for s in sintaxe:
        if "idioma" in s:
            if s["categoria"] != G.CATEGORIA_LEMATIZACAO:
                raise ProtocoloInvalido(G.T_SINTAXE, f"sintaxe {s['elemento']!r}: `idioma` "
                                                     f"só na categoria "
                                                     f"{G.CATEGORIA_LEMATIZACAO!r}", doc)
            if s["idioma"] not in d["idiomas"]:
                raise ProtocoloInvalido(G.T_SINTAXE, f"sintaxe {s['elemento']!r}: idioma "
                                                     f"{s['idioma']!r} fora do quadro", doc)
    sem_categoria = [c for c in G.CATEGORIAS if not any(s["categoria"] == c
                                                        for s in sintaxe)]
    if sem_categoria:
        raise ProtocoloInvalido(G.D_CATEGORIA, f"categoria mínima sem elemento: "
                                               f"{sem_categoria}", doc)
    regras = dado.get("regras_de_montagem", [])
    nomes_regras = [r["texto"] for r in regras]
    sondagens = _valida_sondagens(dado.get("sondagens", []), set(nomes) | set(nomes_regras),
                                  doc)
    for s in sintaxe:
        _verificacao(s, s["elemento"], G.T_SINTAXE, bd, sondagens, doc)
    for r in regras:
        _verificacao(r, r["texto"], G.T_REGRAS, bd, sondagens, doc)

    # Critérios.
    for c in dado["criterios"]:
        for cid in c["ids"]:
            if not G.I_CE.casa(cid):
                raise ProtocoloInvalido(G.T_CRITERIOS_F, f"criterios: id {cid!r} fora da "
                                                         f"forma CEn", doc)
        if c["destino"] in G.DESTINOS_COM_CLAUSULA and not c.get("clausula"):
            raise ProtocoloInvalido(G.T_CRITERIOS_F, f"criterios {'/'.join(c['ids'])}: "
                                                     f"destino {c['destino']!r} sem "
                                                     f"`clausula`", doc)

    # Redução, composição, consultas de campo, subconjuntos e forma radical.
    for r in dado.get("reducao", []):
        if r["faceta"] not in facetas:
            raise ProtocoloInvalido(G.T_REDUCAO, f"faceta {r['faceta']!r} não existe", doc)
    comp = dado["composicao"]
    por_faceta = {}
    for f in comp["facetas"]:
        if f["faceta"] not in facetas or f["faceta"] in por_faceta:
            raise ProtocoloInvalido(G.T_COMP_FACETAS, f"faceta {f['faceta']!r} inexistente "
                                                      f"ou repetida", doc)
        por_faceta[f["faceta"]] = f
    faltam = [f for f in facetas if f not in por_faceta]
    if faltam:
        raise ProtocoloInvalido(G.T_COMP_FACETAS, f"sem composição para {faltam}", doc)
    prox = comp["proximidade"]
    if isinstance(prox, str):
        if prox not in G.D_PROXIMIDADE.dominio:
            raise ProtocoloInvalido(G.D_PROXIMIDADE, f"proximidade {prox!r} fora do domínio",
                                    doc)
        prox = None
    elif set(prox) != {"operador", "distancia"} or not isinstance(prox["operador"], str) \
            or not isinstance(prox["distancia"], int):
        raise ProtocoloInvalido(G.D_PROXIMIDADE, f"proximidade {prox!r}: exige `operador` "
                                                 f"(texto) e `distancia` (inteiro)", doc)
    extras = {}
    for tab, decl in (("subconjuntos", G.T_SUBCONJUNTOS), ("radical", G.T_RADICAL)):
        for s in dado.get(tab, []):
            if s["faceta"] not in facetas:
                raise ProtocoloInvalido(decl, f"{s['id']}: faceta {s['faceta']!r} não existe",
                                        doc)
            if not re.fullmatch(rf"{G.I_STR.prefixo}\d+[a-z]?", s["id"]) or s["id"] in extras:
                raise ProtocoloInvalido(decl, f"id {s['id']!r} fora da forma STRn[letra] ou "
                                              f"repetido", doc)
            extras[s["id"]] = s
    radicais = {s["faceta"] for s in dado.get("radical", [])}
    if len(radicais) != len(dado.get("radical", [])):
        raise ProtocoloInvalido(G.T_RADICAL, "mais de uma forma radical para a mesma faceta",
                                doc)
    if dado.get("radical") and G.DERIVACAO_RADICAL not in cobertura.get("derivacoes", []):
        raise ProtocoloInvalido(G.T_RADICAL, "forma radical sem `radical` em "
                                             "`[cobertura] derivacoes`", doc)
    letras = []
    for q in dado.get("consultas_de_campo", []):
        if not re.fullmatch(r"[a-z]", q["letra"]) or q["letra"] in letras:
            raise ProtocoloInvalido(G.T_CONSULTAS_CAMPO, f"letra {q['letra']!r} fora da "
                                                         f"forma ou repetida", doc)
        letras.append(q["letra"])
        if q["faceta"] not in facetas:
            raise ProtocoloInvalido(G.T_CONSULTAS_CAMPO, f"{q['letra']}: faceta "
                                                         f"{q['faceta']!r} não existe", doc)
        sid = d["strings"][q["faceta"]]["id"] if q["faceta"] in d["strings"] else None
        if q["string"] != sid and (q["string"] not in extras
                                   or extras[q["string"]]["faceta"] != q["faceta"]):
            raise ProtocoloInvalido(G.T_CONSULTAS_CAMPO, f"{q['letra']}: string "
                                                         f"{q['string']!r} não é a STR nem "
                                                         f"um subconjunto de "
                                                         f"{q['faceta']}", doc)
    faceta_campo = {q["faceta"] for q in dado.get("consultas_de_campo", [])}
    if len(faceta_campo) > 1:
        raise ProtocoloInvalido(G.T_CONSULTAS_CAMPO, f"consultas de campo em mais de uma "
                                                     f"faceta {sorted(faceta_campo)}", doc)

    # Execução e expressões.
    execucao = dado["execucao"]
    ids_exp = [e["id"] for e in execucao["expressoes"]]
    if sorted(ids_exp) != sorted(d["expressoes"]) or len(set(ids_exp)) != len(ids_exp):
        raise ProtocoloInvalido(G.T_EXPRESSOES_F, f"expressões {ids_exp} não são as do "
                                                  f"protocolo {sorted(d['expressoes'])}", doc)
    if execucao["forma"] == "curada" and not dado.get("curadas"):
        raise ProtocoloInvalido(G.T_CURADAS, "forma curada sem [[curadas]]", doc)
    da_base = {s["id"] for s in d["sementes"] if sigla in s["bases"]}
    for s in dado.get("sementes", []):
        if s["id"] not in da_base:
            raise ProtocoloInvalido(G.T_SEMENTES_F, f"semente {s['id']!r} não tem {sigla!r} em "
                                                    f"`bases` no arquivo de sementes", doc)

    return {"sigla": sigla, "bd": bd, "nome": b["nome"], "pasta": pasta, "doc": doc,
            "dado": dado, "fragmentos": fragmentos, "sondagens": sondagens,
            "plural": plural, "teto": teto, "idiomas_base": idiomas_base,
            "proximidade": prox, "composicao": por_faceta, "extras": extras,
            "pendentes": marcas}
