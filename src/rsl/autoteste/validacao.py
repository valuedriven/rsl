"""Autoteste do planejamento da validação terminológica por instrumento."""

import copy

from .. import gramatica as G
from ..leitura import instrumentos_do_termo
from ..markdown import lista
from ..termos.tematres import item_exato
from ..termos.planejamento import STATUS_MANUAL, estado_inicial
from .textos import celula, coluna, troca_celula


def casos(ctx, g):
    """Sobre o protocolo e cópias alteradas: todos os instrumentos da faceta são
    planejados, instrumento cuja coluna FCTs perde a faceta não é, só nos idiomas que o
    instrumento cobre, e o modo `Manual` faz a linha nascer pendente de validação manual."""
    t, d = ctx.texto, ctx.protocolo()
    L = d["locais"]

    def planejados(dd, fid):
        return {i["sigla"] for idioma in dd["idiomas"]
                for i in instrumentos_do_termo(dd, fid, idioma)}

    # Vários instrumentos: a faceta com mais instrumentos tem todos planejados. Sem faceta
    # com mais de um, o caso não prova nada e falha.
    por_faceta = d["instrumentos_por_faceta"]
    fid = max(por_faceta, key=lambda f: len(por_faceta[f]))
    declarados = {i["sigla"] for i in por_faceta[fid] if set(i["idiomas"]) & set(d["idiomas"])}
    g.testa(f"faceta com vários instrumentos ({fid}) planeja todos",
            len(declarados) > 1 and planejados(d, fid) == declarados,
            f"declarados {sorted(declarados)}, planejados {sorted(planejados(d, fid))}")

    # Instrumento retirado: a faceta sai da coluna FCTs da linha dele, na cópia do texto.
    if len(por_faceta[fid]) < 2:
        g.falha(f"instrumento retirado de {fid}: a faceta não tem dois instrumentos para "
                f"retirar um")
    else:
        sigla = por_faceta[fid][-1]["sigla"]
        idx, cab = L["instrumento"][sigla], L["cabecalho_instrumentos"]
        k = coluna(t, cab, G.T_INSTRUMENTOS.colunas[5])
        mutante = troca_celula(t, idx, k, ", ".join(
            f for f in lista(celula(t, idx, k)) if f != fid))
        dm = ctx.com_texto(mutante).protocolo()
        g.testa(f"faceta {fid} retirada da coluna FCTs de {sigla}: {sigla} não é planejado",
                mutante != t and sigla not in planejados(dm, fid)
                and planejados(dm, fid) == planejados(d, fid) - {sigla},
                f"planejados {sorted(planejados(dm, fid))}")

    # Filtro por idioma: um instrumento passa a cobrir só um dos idiomas.
    dm = copy.deepcopy(d)
    inst = dm["instrumentos_por_faceta"][fid][0]
    so = inst["idiomas"][0]
    inst["idiomas"] = [so]
    fora = [i for i in dm["idiomas"] if i != so]
    g.testa(f"{inst['sigla']} restrito a {so} só é planejado em {so}",
            bool(fora)
            and inst["sigla"] in {i["sigla"] for i in instrumentos_do_termo(dm, fid, so)}
            and all(inst["sigla"] not in {i["sigla"] for i in instrumentos_do_termo(dm, fid, x)}
                    for x in fora))

    # Endereço resolvido: o instrumento com mais idiomas recebe, numa cópia, um Caminho com
    # o marcador; cada idioma resolve para o seu endereço, sem o marcador nem o segmento de
    # outro idioma. Sem instrumento com dois idiomas, o caso não prova nada e falha.
    multi = max(d["instrumentos"].values(), key=lambda i: len(i["idiomas"]))
    if len(multi["idiomas"]) < 2:
        g.falha("endereço por idioma: nenhum instrumento com dois idiomas")
    else:
        sigla = multi["sigla"]
        k = coluna(t, L["cabecalho_instrumentos"], G.T_INSTRUMENTOS.colunas[3])
        base = "https://exemplo.invalid/servico/"
        mutante = troca_celula(t, L["instrumento"][sigla], k,
                               f"{base}{G.MARCADOR_IDIOMA}/services.php")
        dm = ctx.com_texto(mutante).protocolo()
        fid_m = dm["instrumentos"][sigla]["facetas"][0]
        for idioma in multi["idiomas"]:
            enderecos = [i["endereco"] for i in instrumentos_do_termo(dm, fid_m, idioma)
                         if i["sigla"] == sigla]
            outros = [x for x in multi["idiomas"] if x != idioma]
            g.testa(f"{sigla}: termo em {idioma} resolve para /{idioma}/services.php",
                    enderecos == [f"{base}{idioma}/services.php"]
                    and not any("{" in e or any(f"/{o}/" in e for o in outros)
                                for e in enderecos),
                    f"instrumento {sigla}, idioma {idioma}: {enderecos}")
    # Endereço único: Caminho sem marcador vale igual para todos os idiomas do instrumento.
    unico = next((i for i in d["instrumentos"].values()
                  if G.MARCADOR_IDIOMA not in i["caminho"]), None)
    if unico is None:
        g.falha("endereço único: nenhum instrumento sem marcador no Caminho")
    else:
        enderecos = {i["endereco"] for x in unico["idiomas"]
                     for i in instrumentos_do_termo(d, unico["facetas"][0], x)
                     if i["sigla"] == unico["sigla"]}
        g.testa(f"{unico['sigla']}: Caminho sem marcador é o endereço de todos os idiomas",
                enderecos == {unico["caminho"]}, f"{sorted(enderecos)}")

    # Modo manual, sobre cópia do texto: o primeiro instrumento da faceta passa a `Manual`
    # (ou a `Automático`, se já for manual, para haver os dois modos). Não depende de o
    # protocolo vigente declarar instrumento manual.
    sigla = por_faceta[fid][0]["sigla"]
    k = coluna(t, L["cabecalho_instrumentos"], G.T_INSTRUMENTOS.colunas[2])
    modo_doc = {v: c for c, v in G.D_MODO.valores.items()}
    novo = G.MODO_AUTOMATICO if d["instrumentos"][sigla]["modo"] == G.MODO_MANUAL \
        else G.MODO_MANUAL
    mutante = troca_celula(t, L["instrumento"][sigla], k, modo_doc[novo])
    dm = ctx.com_texto(mutante).protocolo()
    plano = [i for idioma in dm["idiomas"] for i in instrumentos_do_termo(dm, fid, idioma)]
    manuais = [i for i in plano if i["modo"] == G.MODO_MANUAL]
    autos = [i for i in plano if i["modo"] != G.MODO_MANUAL]
    g.testa(f"cópia com {sigla} em {modo_doc[novo]}: o manual nasce pendente de validação "
            f"manual e o automático não",
            mutante != t and bool(manuais) and bool(autos)
            and all(estado_inicial(i).get("status_proposto") == STATUS_MANUAL for i in manuais)
            and all(estado_inicial(i).get("status_proposto") != STATUS_MANUAL for i in autos),
            f"{len(manuais)} manual(is), {len(autos)} automático(s) planejados em {fid}")


    # Cliente TemaTres: o identificador vem do item que casou, e não do primeiro da resposta.
    # A resposta põe de propósito o outro conceito antes do que casa.
    resposta = {"result": {
        "1": {"term_id": 157, "string": "sistemas de organização do conhecimento"},
        "2": {"term_id": 613, "string": "organização do conhecimento"}}}
    achado = item_exato(resposta, "organização do conhecimento")
    g.testa("TemaTres: identificador do item que casou, não o primeiro da resposta",
            achado[:2] == ("organização do conhecimento", "613"), f"devolveu {achado}")
    g.testa("TemaTres: sem casamento exato não há identificador",
            item_exato(resposta, "conhecimento") == (None, None, None))

# ------------------------------------------------- cliente TemaTres, bloqueio e reabertura
def cliente(ctx, g):
    """Sobre respostas e corpos em memória e sobre uma planilha em memória: a proposta de
    estatuto do cliente TemaTres, a consulta de similaridade, a sonda, a interrupção por
    página anti-robô e a reabertura das linhas de instrumento `Automático` (pendente manual,
    de outro endereço, ou não localizada sem consulta de similaridade)."""
    from ..erros import FonteExterna                                # noqa: PLC0415
    from ..termos import http                                       # noqa: PLC0415
    from ..termos import validacao as V                             # noqa: PLC0415
    from ..termos.planejamento import (OBS_AGUARDANDO,              # noqa: PLC0415
                                       SEM_SUGESTAO, STATUS_AUTORIZADO, STATUS_CANDIDATO,
                                       STATUS_NAO_LOCALIZADO, TERMO_INEXISTENTE)
    from ..termos.tematres import (FORMA_NAO_PREFERIDO,             # noqa: PLC0415
                                   FORMA_PREFERIDO, proposta, sonda, valida)

    # Itens de `search` do ERIC capturados na sonda de 2026-11-24 (termo 'educational'):
    # `no_term_string` false é preferido; texto é a entrada do não preferido.
    eric = {"result": {
        "104": {"term_id": 104, "string": "Academic Accommodations (Disabilities)",
                "isMetaTerm": 0,
                "no_term_string": "Accommodations for Disabled (Educational Settings)",
                "index": None, "order": 1},
        "6259": {"term_id": 6259, "string": "Demonstrations (Educational)", "isMetaTerm": 0,
                 "no_term_string": False, "index": "|11913|1619|4495|1021|6259", "order": 2},
        "107": {"term_id": 107, "string": "Access to Education", "isMetaTerm": 0,
                "no_term_string": "Educational Access", "index": None, "order": 3}}}
    got = proposta(eric, "demonstrations (educational)")
    g.testa("TemaTres (payload da sonda): rótulo preferido propõe descritor, forma preferido",
            got == (STATUS_AUTORIZADO, "Demonstrations (Educational)", "6259",
                    FORMA_PREFERIDO), f"{got}")
    got = proposta(eric, "Educational  access")
    g.testa("TemaTres (payload da sonda): rótulo não preferido propõe descritor, com o "
            "rótulo e o identificador do preferido, forma não preferido",
            got == (STATUS_AUTORIZADO, "Access to Education", "107", FORMA_NAO_PREFERIDO),
            f"{got}")
    got = proposta(eric, "access to education")
    g.testa("TemaTres: o `string` de uma entrada de não preferido não conta como casamento "
            "do preferido", got[0] == STATUS_NAO_LOCALIZADO, f"{got}")
    got = proposta(eric, "educational")
    g.testa("TemaTres (payload da sonda): só correspondência parcial → termo livre não "
            "localizado", got == (STATUS_NAO_LOCALIZADO, None, None, None), f"{got}")
    sem_campo = {"result": {"9": {"term_id": 9, "string": "Ontology"}}}
    got = proposta(sem_campo, " ontology ")
    g.testa("TemaTres: item sem o campo da forma propõe descritor com forma vazia",
            got == (STATUS_AUTORIZADO, "Ontology", "9", ""), f"{got}")
    plural = {"result": {"5": {"term_id": 5, "string": "learning environments",
                               "no_term_string": False}}}
    g.testa("TemaTres: só a forma plural na resposta → termo livre não localizado",
            proposta(plural, "learning environment")[0] == STATUS_NAO_LOCALIZADO)
    g.testa("TemaTres: resposta sem `result` → termo livre não localizado",
            proposta({"resume": {"cant_result": 0}}, "x")[0] == STATUS_NAO_LOCALIZADO)

    similaridade(g, valida, sonda, ctx.protocolo(), {
        "SEM_SUGESTAO": SEM_SUGESTAO, "CANDIDATO": STATUS_CANDIDATO,
        "NAO_LOC": STATUS_NAO_LOCALIZADO, "AUTORIZADO": STATUS_AUTORIZADO,
        "INEXISTENTE": TERMO_INEXISTENTE})

    # Página anti-robô no lugar do JSON interrompe, pelos marcadores.
    for corpo in ("<html><title>Just a moment...</title></html>",
                  "<p>Verifying your browser before accessing the site</p>"):
        try:
            http.sem_bloqueio(corpo, "https://exemplo.invalid/services.php")
            g.falha(f"página anti-robô não interrompeu: {corpo[:40]!r}")
        except FonteExterna as e:
            g.ok(f"página anti-robô interrompe (FonteExterna): {str(e)[:70]}")
    g.testa("corpo JSON TemaTres não é tomado por bloqueio",
            http.sem_bloqueio('{"resume": {"status": "available"}}', "u").startswith("{"))

    # Reabertura, sobre uma planilha em memória gerada das linhas do protocolo.
    d = ctx.protocolo()

    class EmMemoria(V.Planilha):
        def __init__(self, linhas_):
            super().__init__(ctx)
            self.linhas_ = linhas_

        def existente(self):
            return {self.chave(r["faceta"], r["idioma"], r["termo"], r["instrumento"]): r
                    for r in self.linhas_}

    base = V.carrega(ctx, d, EmMemoria([]))
    auto = [ln for ln in base
            if d["instrumentos"][ln["_v"]["instrumento"]]["modo"] == G.MODO_AUTOMATICO]
    if len(auto) < 8:
        g.falha("reabertura: menos de oito linhas de instrumento automático no protocolo")
        return
    a, b, c, e, n, s_, x, cv = auto[:8]
    antigo = "https://endereco-antigo.invalid/sparql"

    def linha(ln, **campos):
        return {"faceta": ln["faceta"], "idioma": ln["idioma"], "termo": ln["termo"],
                "instrumento": ln["_v"]["instrumento"], **campos}
    existentes = [
        linha(a, status_proposto=STATUS_MANUAL, observacao_tecnica="manual"),
        linha(b, status_proposto=STATUS_AUTORIZADO, url_consultada=antigo + "?q=1",
              arquivo_evidencia="evidencia/x/antigo.json"),
        linha(c, status_proposto=STATUS_AUTORIZADO, url_consultada=antigo,
              decisao_ReT="descritor", arquivo_evidencia="evidencia/x/decidido.json"),
        linha(e, status_proposto=STATUS_AUTORIZADO,
              url_consultada=e["endereco"] + "?task=search&arg=x&output=json",
              arquivo_evidencia="evidencia/x/vigente.json"),
        # Não localizada da validação anterior à similaridade: sem `sugestao_similar`.
        linha(n, status_proposto=STATUS_NAO_LOCALIZADO,
              url_consultada=n["endereco"] + "?task=search&arg=x&output=json",
              arquivo_evidencia="evidencia/x/sem-similar.json"),
        linha(s_, status_proposto=STATUS_NAO_LOCALIZADO, sugestao_similar=SEM_SUGESTAO,
              url_consultada=s_["endereco"] + "?task=search&arg=x&output=json",
              arquivo_evidencia="evidencia/x/sem-sugestao.json"),
        linha(x, status_proposto=STATUS_NAO_LOCALIZADO, decisao_ReT="termo livre",
              url_consultada=x["endereco"] + "?task=search&arg=x&output=json",
              arquivo_evidencia="evidencia/x/decidida.json"),
        # Candidato do endereço vigente, sem decisão: não é reconsultado, qualquer que seja
        # a forma ou a posição do termo no rótulo.
        linha(cv, status_proposto=STATUS_CANDIDATO, rotulo_autorizado="Outro conceito",
              forma_no_instrumento="não preferido", sugestao_similar="x → Outro conceito [2]",
              url_consultada=cv["endereco"] + "?task=search&arg=x&output=json",
              arquivo_evidencia="evidencia/x/candidato.json"),
    ]
    pl = EmMemoria(existentes)
    novas = {(ln["faceta"], ln["idioma"], ln["termo"], ln["_v"]["instrumento"]): ln["_v"]
             for ln in V.carrega(ctx, d, pl)}

    def v(ln):
        return novas[(ln["faceta"], ln["idioma"], ln["termo"], ln["_v"]["instrumento"])]
    rotulo = lambda ln: f"{ln['termo']!r} ({ln['idioma']}) em {ln['_v']['instrumento']}"  # noqa: E731
    g.testa(f"reabertura: linha pendente manual sem decisão volta a aguardar consulta "
            f"— {rotulo(a)}",
            v(a)["status_proposto"] == "" and v(a)["observacao_tecnica"] == OBS_AGUARDANDO,
            f"{v(a)['status_proposto']!r}")
    g.testa(f"reabertura: linha de outro endereço sem decisão volta a aguardar consulta, "
            f"sem evidência na linha — {rotulo(b)}",
            v(b)["status_proposto"] == "" and v(b)["url_consultada"] == ""
            and v(b)["arquivo_evidencia"] == "", f"{v(b)['status_proposto']!r}")
    preservadas = [p_[:2] for p_ in pl.preservadas]
    g.testa(f"reabertura: linha de outro endereço com decisão é preservada e listada "
            f"— {rotulo(c)}",
            v(c)["status_proposto"] == STATUS_AUTORIZADO and v(c)["url_consultada"] == antigo
            and v(c)["decisao_ReT"] == "descritor"
            and (c["termo"], c["_v"]["instrumento"]) in preservadas,
            f"preservadas {pl.preservadas}")
    g.testa(f"reabertura: linha do endereço vigente não é reconsultada — {rotulo(e)}",
            v(e)["status_proposto"] == STATUS_AUTORIZADO
            and v(e)["arquivo_evidencia"] == "evidencia/x/vigente.json")
    g.testa(f"reabertura: não localizada sem `sugestao_similar` e sem decisão volta a "
            f"aguardar consulta — {rotulo(n)}",
            v(n)["status_proposto"] == "" and v(n)["observacao_tecnica"] == OBS_AGUARDANDO
            and v(n)["arquivo_evidencia"] == "", f"{v(n)['status_proposto']!r}")
    g.testa(f"reabertura: não localizada já consultada sem sugestão não é reconsultada "
            f"— {rotulo(s_)}",
            v(s_)["status_proposto"] == STATUS_NAO_LOCALIZADO
            and v(s_)["sugestao_similar"] == SEM_SUGESTAO
            and v(s_)["arquivo_evidencia"] == "evidencia/x/sem-sugestao.json")
    g.testa(f"reabertura: não localizada sem `sugestao_similar` com decisão é preservada e "
            f"listada — {rotulo(x)}",
            v(x)["status_proposto"] == STATUS_NAO_LOCALIZADO
            and v(x)["decisao_ReT"] == "termo livre"
            and v(x)["arquivo_evidencia"] == "evidencia/x/decidida.json"
            and (x["termo"], x["_v"]["instrumento"]) in preservadas,
            f"preservadas {pl.preservadas}")
    g.testa(f"reabertura: candidato do endereço vigente não é reconsultado — {rotulo(cv)}",
            v(cv)["status_proposto"] == STATUS_CANDIDATO
            and v(cv)["arquivo_evidencia"] == "evidencia/x/candidato.json")
    g.testa("reabertura: contagem das linhas reabertas e preservadas",
            pl.reabertas == 3 and len(pl.preservadas) == 2,
            f"{pl.reabertas} reabertas, {len(pl.preservadas)} preservadas")


def similaridade(g, valida, sonda, d, S):
    """A consulta por prefixo (`suggestDetails`) do cliente TemaTres sobre respostas em
    memória: item único, item único por entrada não preferida, vários itens sem escolha, sem
    item, e o casamento exato sem a consulta; e a sonda mostrando os itens de cada termo."""
    end = "https://exemplo.invalid/services.php"
    vazio = {"result": [], "resume": {"cant_result": 0}}
    # Respostas de `suggestDetails` capturadas na sondagem de 2026-11-24.
    eric_tm = {"result": {"1021": {"term_id": "1021", "string": "Teaching Methods",
                                   "isMetaTerm": None, "no_term_string": False, "order": 3}},
               "resume": {"cant_result": 1}}
    unesco_tm = {"result": {
        "6885": {"term_id": "6885", "string": "Self instruction", "isMetaTerm": None,
                 "no_term_string": "Self teaching methods", "order": 1},
        "6859": {"term_id": "6859", "string": "Teaching method innovations",
                 "isMetaTerm": None, "no_term_string": False, "order": 2},
        "6917": {"term_id": "6917", "string": "Teaching methods", "isMetaTerm": None,
                 "no_term_string": False, "order": 3}}, "resume": {"cant_result": 3}}
    sem_item = {"resume": {"status": "available", "cant_result": 0}}   # UNESCO, sem `result`

    def consultas(respostas):
        feitas = []

        def consulta(task, arg):
            feitas.append((task, arg))
            return f"{end}?task={task}&arg={arg}", respostas.get((task, arg), vazio)
        return consulta, feitas

    # 1. Item único (ERIC): candidato, com o conceito do item e as relações dele.
    c, feitas = consultas({("suggestDetails", "teaching method"): eric_tm,
                           ("fetchAlt", "1021"): {"result": {
                               "1": {"string": "Teaching Methods"},
                               "2": {"string": "Instructional Methods"}}}})
    reg, status, dados, obs, _, _ = valida("teaching method", end, "v", c)
    g.testa("prefixo (resposta da sonda do ERIC): item único → candidato, com o conceito do "
            "item e `sugestao_similar`",
            status == S["CANDIDATO"] and dados.get("sugestao_similar") == "Teaching Methods [1021]"
            and dados.get("rotulo_autorizado") == "Teaching Methods"
            and dados.get("uri_conceito", "").endswith("arg=1021")
            and dados.get("forma_no_instrumento") == "preferido"
            and dados.get("equivalentes_USE_UP") == "Instructional Methods"
            and "candidato" in obs and "suggestDetails" in reg,
            f"{status} {dados} {obs!r}")
    # 2. Item único por entrada não preferida: o rótulo é o preferido a que ela remete.
    so_np = {"result": {"6885": unesco_tm["result"]["6885"]}}
    c, feitas = consultas({("suggestDetails", "self teaching"): so_np})
    reg, status, dados, obs, _, _ = valida("self teaching", end, "v", c)
    g.testa("prefixo: item único por entrada não preferida → candidato com o preferido, forma "
            "não preferido, e a entrada na sugestão",
            status == S["CANDIDATO"] and dados.get("rotulo_autorizado") == "Self instruction"
            and dados.get("forma_no_instrumento") == "não preferido"
            and dados.get("sugestao_similar") == "Self teaching methods → Self instruction [6885]",
            f"{status} {dados}")
    # 2b. Item único com o termo no meio do rótulo (resposta do Brased, 2026-11-24): também
    # candidato; a conferência é do ReT.
    meio = {"result": {"7816": {"term_id": "7816", "string": "Organização do Ambiente "
                                "Educacional", "isMetaTerm": None, "no_term_string": False,
                                "order": 1}}}
    c, feitas = consultas({("suggestDetails", "ambiente educacional"): meio})
    reg, status, dados, obs, _, _ = valida("ambiente educacional", end, "v", c)
    g.testa("prefixo: item único com o termo no meio do rótulo → candidato",
            status == S["CANDIDATO"]
            and dados.get("rotulo_autorizado") == "Organização do Ambiente Educacional"
            and dados.get("sugestao_similar") == "Organização do Ambiente Educacional [7816]",
            f"{status} {dados} {obs!r}")
    # 3. Vários itens (UNESCO): nenhum escolhido, todos na sugestão, na ordem do serviço.
    c, feitas = consultas({("suggestDetails", "teaching method"): unesco_tm})
    reg, status, dados, obs, _, _ = valida("teaching method", end, "v", c)
    g.testa("prefixo (resposta da sonda da UNESCO): vários itens → não localizado, sem "
            "escolha, os três na sugestão, sem consultar relações",
            status == S["NAO_LOC"] and set(dados) == {"sugestao_similar"}
            and dados["sugestao_similar"] == ("Self teaching methods → Self instruction "
                                              "[6885]; Teaching method innovations [6859]; "
                                              "Teaching methods [6917]")
            and [t for t, _ in feitas] == ["search", "suggestDetails"] and "ReT" in obs
            and "devolveu 3 itens" in obs and "declarada pelo serviço: 3" in obs,
            f"{status} {dados} {feitas}")
    # 4. Sem item (resposta sem `result`).
    c, feitas = consultas({("suggestDetails", "x y"): sem_item})
    reg, status, dados, obs, _, _ = valida("x y", end, "v", c)
    g.testa("prefixo: sem item → não localizado, `sugestao_similar` diz que o serviço não "
            "sugeriu",
            status == S["NAO_LOC"] and dados == {"sugestao_similar": S["SEM_SUGESTAO"]}
            and [t for t, _ in feitas] == ["search", "suggestDetails"]
            and "suggestDetails" in reg, f"{status} {dados} {feitas}")
    # Casamento exato: a consulta por prefixo não é feita, e a coluna fica vazia.
    busca = {"result": {"1021": {"term_id": 1021, "string": "Teaching Methods",
                                 "no_term_string": False}}}
    c, feitas = consultas({("search", "teaching methods"): busca})
    reg, status, dados, obs, _, _ = valida("teaching methods", end, "v", c)
    g.testa("prefixo: casamento exato não consulta o prefixo, `sugestao_similar` vazia",
            status == S["AUTORIZADO"] and not dados.get("sugestao_similar")
            and "suggestDetails" not in [t for t, _ in feitas], f"{status} {feitas}")

    # Sonda: mostra os itens de cada termo de prova e do inexistente; nada é gravado.
    auto = next((i for i in d["instrumentos"].values()
                 if i["modo"] == G.MODO_AUTOMATICO), None)
    if auto is None:
        g.falha("sonda: nenhum instrumento automático no protocolo")
        return
    idioma = auto["idiomas"][0]
    c, feitas = consultas({("suggestDetails", S["INEXISTENTE"]): eric_tm})
    saida = []
    sonda(d, auto, idioma, end, saida.append, c)
    texto = "\n".join(saida)
    prefixos = [a for t, a in feitas if t == "suggestDetails"]
    g.testa("sonda: consulta o prefixo de cada termo de prova e do inexistente, e mostra os "
            "itens ou a ausência deles",
            S["INEXISTENTE"] in prefixos and len(prefixos) >= 2
            and "1 item(ns): Teaching Methods [1021]" in texto
            and f"0 item(ns): {S['SEM_SUGESTAO']}" in texto, f"prefixos {prefixos}")


# ------------------------------------------------- decisão do ReT e linha do termo no CT
def _planilha(linhas):
    """Texto CSV mínimo da planilha de validação, com as colunas exigidas."""
    from ..termos.decisao import COLUNAS_EXIGIDAS                   # noqa: PLC0415
    colunas = list(COLUNAS_EXIGIDAS) + ["status_proposto"]
    corpo = [";".join(colunas)]
    corpo += [";".join(r.get(c, "") for c in colunas) for r in linhas]
    return "\n".join(corpo) + "\n"


def classificacao(ctx, g):
    """Domínio de `decisao_ReT`, regra da linha esperada e conferência cruzada CT × planilha,
    sobre planilhas em memória e cópias do protocolo. Tudo gerado da estrutura lida: o
    primeiro termo livre da primeira faceta, os instrumentos planejados para ele."""
    from ..conferencia import conferir                              # noqa: PLC0415
    from ..saida import Saida                                       # noqa: PLC0415
    from ..termos.decisao import (esperada, fora_do_dominio, le_planilha,  # noqa: PLC0415
                                  linhas_esperadas)
    from . import resultado                                         # noqa: PLC0415
    from .textos import edita_celula                                # noqa: PLC0415
    t, d = ctx.texto, ctx.protocolo()
    L = d["locais"]
    livre, desc, rel = (r.interno for r in G.LINHAS_CT)
    # Um termo com dois instrumentos planejados, para provar a precedência entre eles.
    alvo = None
    for f in d["tabelas"]:
        for i in d["idiomas"]:
            insts = [x["sigla"] for x in instrumentos_do_termo(d, f["id"], i)]
            if f["linhas"][i][livre] and len(insts) > 1:
                alvo = (f, i, f["linhas"][i][livre][0], insts)
                break
        if alvo:
            break
    if alvo is None:
        g.falha("nenhum termo com dois instrumentos planejados: a precedência não é provada")
        return
    f, idioma, termo, insts = alvo
    fid = f["id"]
    nao_planejado = next((s for s in d["instrumentos"] if s not in insts), None)

    def linha(decisoes, status=None):
        rs = [{"faceta": fid, "idioma": idioma, "termo": termo, "instrumento": s,
               "decisao_ReT": v, "status_proposto": (status or {}).get(s, "")}
              for s, v in decisoes.items()]
        return esperada(linhas_esperadas(d, rs), fid, idioma, termo)

    a, b = insts[0], insts[1]
    g.testa("precedência: descritor num instrumento e sinônimo noutro → descritores",
            linha({a: "sinônimo ou relacionado", b: "descritor"}) == desc)
    g.testa("descritor num instrumento e termo livre noutro → descritores",
            linha({a: "descritor", b: "termo livre"}) == desc)
    g.testa("só sinônimo ou relacionado → relacionados",
            linha({a: "sinônimo ou relacionado"}) == rel)
    g.testa("decisão com outra caixa (`Descritor`) é lida como descritor",
            linha({a: "Descritor"}) == desc)
    g.testa("pendência manual sem decisão → livre",
            linha({a: ""}, {a: STATUS_MANUAL}) == livre)
    g.testa("proposta da máquina sem decisão do ReT → livre",
            linha({a: ""}, {a: "descritor autorizado (a conferir pelo ReT)"}) == livre)
    g.testa("candidato por similaridade sem decisão do ReT → livre",
            linha({a: ""}, {a: "candidato por similaridade (a conferir pelo ReT)"}) == livre)
    g.testa("planilha ausente → livre", esperada(linhas_esperadas(d, None), fid, idioma,
                                                termo) == livre)
    if nao_planejado:
        g.testa(f"decisão em instrumento não planejado para o termo ({nao_planejado}) não "
                f"classifica", linha({nao_planejado: "descritor"}) == livre)
    fora = [{"faceta": fid, "idioma": idioma, "termo": termo, "instrumento": a,
             "decisao_ReT": "autorizado"}]
    g.testa("valor fora do domínio é reprovado (o que `termos importar` usa)",
            bool(fora_do_dominio(fora)) and "autorizado" in fora_do_dominio(fora)[0])
    cod, msgs = resultado(lambda: le_planilha("faceta;termo\nFCT1;x\n", "planilha"))
    g.testa("planilha sem as colunas exigidas é ilegível (DADOS)", cod == Saida.DADOS,
            f"{cod.name} {msgs[:1]}")

    # Conferência cruzada: cópias do protocolo e planilhas em memória.
    q = L["quadro"][fid]
    k = coluna(t, q["cabecalho"], idioma)
    movido = edita_celula(edita_celula(t, q[livre], k,
                                       lambda c: ", ".join(x.strip() for x in c.split(",")
                                                           if x.strip() != termo)),
                          q[desc], k, lambda c: termo)

    def com(texto, plan):
        return lambda m: conferir(ctx.com_texto(m).com_validacao(texto if plan is None
                                                                   else _planilha(plan)))
    decide = [{"faceta": fid, "idioma": idioma, "termo": termo, "instrumento": a,
               "decisao_ReT": "descritor"}]
    R = Saida.REPROVADO
    g.espera("termo sem decisão movido para Descritores, sem planilha", movido, t,
             com(None, None), R, (repr(termo), "a linha esperada é 'Termo livre'"))
    g.espera("termo sem decisão movido para Descritores, com planilha sem decisão", movido, t,
             com(None, [{**decide[0], "decisao_ReT": ""}]), R,
             (repr(termo), "a linha esperada é 'Termo livre'", "pela decisão do ReT"))
    g.espera("descritor decidido ainda em Termo livre", t + "\n", t,
             com(None, decide), R,
             (repr(termo), f"a linha esperada é {G.R_DESCRITORES.texto!r}"))
    # Reclassificado, o termo muda de posição na STR: a única reprovação é a da ordem, que
    # `strings gerar --gravar` corrige ("Termo reclassificado", geracao-das-strings).
    cod, msgs = resultado(lambda: com(None, decide)(movido))
    g.testa("descritor decidido na linha de descritores: nenhuma reprovação de classificação, "
            "só a STR em outra ordem",
            bool(msgs) and all("ordem diferente" in m for m in msgs), f"{cod.name} {msgs[:2]}")
    g.espera("decisão fora do domínio na planilha", t + "\n", t,
             com(None, [{**decide[0], "decisao_ReT": "autorizado"}]), R,
             ("fora do domínio", "'autorizado'", repr(termo)))
    g.espera("planilha ilegível", t + "\n", t,
             lambda m: conferir(ctx.com_texto(m).com_validacao("faceta;termo\nx;y\n")),
             Saida.DADOS, "ilegível")
    repetido = edita_celula(t, q[desc], k, lambda c: termo)
    g.espera("termo em duas linhas do mesmo CT e idioma", repetido, t, com(None, None), R,
             (repr(termo), "mais de uma linha", f["ct"]))
    outro = next((i for i in d["idiomas"] if i != idioma), None)
    if outro:
        k2 = coluna(t, q["cabecalho"], outro)
        mesma = edita_celula(t, q[livre], k2, lambda c: f"{c}, {termo}" if c else termo)
        cod, msgs = resultado(lambda: conferir(ctx.com_texto(mesma).com_validacao(None)))
        g.testa("mesma forma em Termo livre de dois idiomas não reprova por repetição",
                mesma != t and not any("mais de uma linha" in m for m in msgs),
                f"{msgs[:1]}")
    # Célula vazia admitida: o próprio documento corrente, aprovado para o autoteste rodar,
    # tem de ter alguma célula vazia; senão o caso não prova nada e falha.
    vazias = [(x["id"], i, c) for x in d["tabelas"] for i in d["idiomas"]
              for c in (desc, rel) if not x["linhas"][i][c]]
    cod, msgs = resultado(lambda: conferir(ctx))
    g.testa("célula vazia no CT não reprova (documento corrente com células vazias aprova)",
            bool(vazias) and cod == Saida.OK, f"{len(vazias)} vazias, {cod.name} {msgs[:1]}")
