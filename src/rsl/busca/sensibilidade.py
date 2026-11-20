"""Sonda de sensibilidade: a fração da sonda que a executada não recupera, com a amostra
a classificar à mão."""

import csv

from ..config import relativo
from ..erros import DadosInvalidos
from ..markdown import normaliza
from ..saida import Saida
from . import Busca
from .leitores import le_arquivo
from .registro import caminho_do_arquivo, carrega_consultas, chave_dedup


def registros_da_expressao(base, ident, validas):
    """Registros distintos (por chave de deduplicação) de uma expressão, numa base."""
    consultas = [c for c in validas if c.get("base") == base and c.get("expressao") == ident]
    if not consultas:
        return None
    chaves, registros = set(), []
    for c in consultas:
        caminho = caminho_do_arquivo(c)
        if not caminho.exists():
            raise DadosInvalidos(f"consulta {c.get('id')}: arquivo ausente {c.get('arquivo')}")
        for r in le_arquivo(caminho):
            k = chave_dedup(r)
            if k not in chaves:
                chaves.add(k)
                registros.append(r)
    return registros


def sensibilidade(b, base=None):
    """A perda é a diferença de conjuntos, chaveada por DOI ou título. O arquivo gravado é a
    amostra a classificar à mão: a decisão do protocolo olha a fração ELEGÍVEL entre os
    perdidos, não o tamanho da perda. Sem essa classificação, o número impresso é limite
    superior do custo em recall, não estimativa dele.

    Base sem a executada ou sem a sonda registrada é pulada e faz o subcomando sair com
    DADOS, depois de processar as demais.
    """
    _, validas = carrega_consultas(b)
    existentes = sorted({c.get("base") for c in validas})
    if base:
        _, canonica = b.exige_bd(base)
        if canonica not in existentes:
            raise DadosInvalidos(f"base {base!r} sem consulta registrada; registradas: "
                                 f"{', '.join(existentes) or 'nenhuma'}")
        alvos = [canonica]
    else:
        alvos = existentes

    amostra_alvo = b.config.valor("busca.amostra_sensibilidade")
    codigo = Saida.OK
    for sigla in alvos:
        executada = registros_da_expressao(sigla, b.executada, validas)
        sonda = registros_da_expressao(sigla, b.sonda, validas)
        if executada is None or sonda is None:
            falta = b.executada if executada is None else b.sonda
            print(f"{sigla}: sem {falta} registrada — a sonda exige {b.executada} e "
                  f"{b.sonda} registradas na mesma base. Pulada.")
            codigo = Saida.DADOS
            continue
        chaves_exec = {chave_dedup(r) for r in executada}
        perdidos = [r for r in sonda if chave_dedup(r) not in chaves_exec]
        total_sonda = len({chave_dedup(r) for r in sonda})
        fracao_perda = len(perdidos) / total_sonda if total_sonda else 0.0

        print(f"\nSONDA DE SENSIBILIDADE — {sigla}")
        print(f"  {b.sonda} recupera .......... {total_sonda}")
        print(f"  {b.executada} recupera ...... {len(chaves_exec)}")
        print(f"  só em {b.sonda} (perda) .... {len(perdidos)}  "
              f"({fracao_perda:.1%} de {b.sonda})")
        print("  Este é o TAMANHO da perda, não a fração que decide: o protocolo decide pela "
              "fração ELEGÍVEL da amostra, classificada à mão.")

        rel = b.config.saida("sensibilidade", base=sigla)
        rel.parent.mkdir(parents=True, exist_ok=True)
        passo = max(1, len(perdidos) // amostra_alvo)
        ordenados = sorted(perdidos, key=lambda x: normaliza(x["titulo"]))
        # Preserva o que o pesquisador já classificou: a amostra é dele, não do script.
        anterior = {}
        if rel.exists():
            with rel.open(encoding="utf-8-sig", newline="") as fh:
                for linha in csv.DictReader(fh, delimiter=";"):
                    anterior[linha.get("chave", "")] = linha.get("elegivel", "") or ""
        amostra = {chave_dedup(r) for i, r in enumerate(ordenados) if i % passo == 0}
        with rel.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(["chave", "ano", "titulo", "doi", "amostra", "elegivel"])
            for r in ordenados:
                k = chave_dedup(r)
                w.writerow([k, r["ano"], r["titulo"], r["doi"],
                            "sim" if k in amostra else "", anterior.get(k, "")])
        onde = relativo(rel)

        baixo, alto = b.limite_sensibilidade
        if not amostra:
            print(f"  amostra em {onde}: nenhuma perda a classificar.")
        else:
            respondidos = [anterior.get(k, "").strip() for k in amostra
                           if anterior.get(k, "").strip()]
            if len(respondidos) < len(amostra):
                print(f"  amostra em {onde}: {len(respondidos)} de {len(amostra)} "
                      f"classificados — a decisão exige a amostra inteira.")
            else:
                sim = sum(1 for v in respondidos if v.lower() in ("sim", "s", "1", "true"))
                frac_eleg = sim / len(amostra)
                print(f"  fração ELEGÍVEL na amostra: {sim}/{len(amostra)} = {frac_eleg:.1%}")
                if frac_eleg < baixo:
                    print(f"  {frac_eleg:.1%} < {baixo:.0%}: a restrição está justificada.")
                elif frac_eleg > alto:
                    print(f"  {frac_eleg:.1%} > {alto:.0%}: reconsiderar, possivelmente "
                          f"retornar a {b.sonda} como busca definitiva.")
                else:
                    print(f"  {frac_eleg:.1%} na faixa {baixo:.0%}–{alto:.0%}: decisão de "
                          f"mérito do pesquisador, a registrar como emenda.")
        print("  A decisão se registra como emenda ao protocolo.")
    return codigo


def cmd_sensibilidade(ctx, a):
    return sensibilidade(Busca(ctx), a.base)
