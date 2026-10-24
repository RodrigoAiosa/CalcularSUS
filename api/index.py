"""API do CalcularSUS (Flask) - roda como função serverless na Vercel."""
import os
import sys

from flask import Flask, jsonify, request

# Garante que "dados.py" (mesma pasta) seja importável na Vercel e localmente.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dados import (  # noqa: E402
    BPS_PERIODO, CATEGORIAS, CENARIOS, FONTES, ITENS, PARAMETROS, SIGTAP_COMPETENCIA,
)

app = Flask(__name__)
app.json.ensure_ascii = False

_ITENS_POR_ID = {i["id"]: i for i in ITENS}


def _numero(valor, padrao, minimo=0.0, maximo=None):
    """Converte para float, aplicando padrão e limites."""
    if valor in (None, ""):
        return padrao
    try:
        n = float(str(valor).replace(",", "."))
    except ValueError:
        raise ValueError(f"valor inválido: {valor!r}")
    if n < minimo:
        raise ValueError(f"valor deve ser >= {minimo}")
    if maximo is not None and n > maximo:
        raise ValueError(f"valor deve ser <= {maximo}")
    return n


BASES = ("estimado", "sigtap")


def _base(valor):
    """'estimado' = custo de referência (padrão); 'sigtap' = repasse oficial da Tabela SIGTAP."""
    base = (valor or "estimado").strip().lower()
    if base not in BASES:
        raise ValueError(f"base inválida: {valor!r} (use {' ou '.join(BASES)})")
    return base


def _valor_unitario(item, base):
    """Valor unitário na base escolhida; None se o item não tem valor naquela base."""
    return item["valor_sigtap"] if base == "sigtap" else item["custo_sus"]


def _validar_quantidade(item, quantidade):
    """Aplica o limite anual do item (ex.: 12 meses para remédios mensais)."""
    limite = item.get("max_por_ano", 100_000)
    if quantidade > limite:
        raise ValueError(f"{item['nome']}: máximo de {limite} por ano")
    return quantidade


def _contribuicao(renda_mensal, carga_pct, parcela_saude_pct):
    renda_anual = renda_mensal * 12
    impostos_anuais = renda_anual * carga_pct / 100
    imposto_saude_anual = impostos_anuais * parcela_saude_pct / 100
    return renda_anual, impostos_anuais, imposto_saude_anual


def calcular_cesta(linhas_in, renda_mensal, carga_pct, parcela_saude_pct, base="estimado"):
    """Soma o consumo de vários itens e compara com a contribuição anual."""
    linhas = []
    sem_valor = []
    custo_total = 0.0
    particular_total = 0.0
    particular_completo = True

    for entrada in linhas_in:
        item = _ITENS_POR_ID.get(entrada.get("item_id"))
        if item is None:
            raise ValueError(f"item_id inválido: {entrada.get('item_id')!r}")
        qtd = _validar_quantidade(item, _numero(entrada.get("quantidade"), 1, 0, 100_000))
        unitario = _valor_unitario(item, base)
        if unitario is None:  # item sem valor nesta base: conta 0 e avisa
            sem_valor.append(item["nome"])
        custo = (unitario or 0) * qtd
        particular = item["valor_particular"] * qtd if item["valor_particular"] is not None else None
        custo_total += custo
        if particular is None:
            particular_completo = False
        else:
            particular_total += particular
        linhas.append({
            "item_id": item["id"],
            "nome": item["nome"],
            "unidade": item["unidade"],
            "quantidade": qtd,
            "max_por_ano": item.get("max_por_ano"),
            "custo": round(custo, 2),
            "sem_valor_base": unitario is None,
            "valor_particular": round(particular, 2) if particular is not None else None,
        })

    renda_anual, impostos_anuais, imposto_saude = _contribuicao(renda_mensal, carga_pct, parcela_saude_pct)
    tem_renda = imposto_saude > 0
    saldo = imposto_saude - custo_total

    return {
        "linhas": linhas,
        "base": base,
        "itens_sem_valor": sem_valor,
        "custo_total": round(custo_total, 2),
        "valor_particular_total": round(particular_total, 2),
        "particular_completo": particular_completo,
        "renda_anual": round(renda_anual, 2),
        "impostos_anuais": round(impostos_anuais, 2),
        "imposto_saude_anual": round(imposto_saude, 2),
        "tem_renda": tem_renda,
        # saldo > 0: contribuição cobre o consumo; saldo < 0: outros contribuintes cobrem a diferença
        "saldo": round(saldo, 2),
        "cobertura_pct": round(imposto_saude / custo_total * 100, 1) if custo_total and tem_renda else None,
        "vezes_a_contribuicao": round(custo_total / imposto_saude, 1) if tem_renda and custo_total else None,
        "anos_para_cobrir": round(custo_total / imposto_saude, 1) if tem_renda and custo_total else None,
        "premissas": {"carga_pct": carga_pct, "parcela_saude_pct": parcela_saude_pct},
    }


def calcular(item, quantidade, renda_mensal, carga_pct, parcela_saude_pct, base="estimado"):
    unitario = _valor_unitario(item, base)
    sem_valor_base = unitario is None
    custo_unit = unitario or 0.0
    particular_unit = item["valor_particular"]

    custo_total = custo_unit * quantidade
    particular_total = particular_unit * quantidade if particular_unit is not None else None

    renda_anual, impostos_anuais, imposto_saude_anual = _contribuicao(
        renda_mensal, carga_pct, parcela_saude_pct
    )

    unidades_cobertas = imposto_saude_anual / custo_unit if custo_unit else None
    cobertura_pct = (imposto_saude_anual / custo_total * 100) if custo_total else None
    economia = (particular_total - custo_total) if particular_total is not None else None

    return {
        "item": item,
        "quantidade": quantidade,
        "pago_na_hora": 0.0,
        "base": base,
        "sem_valor_base": sem_valor_base,
        "custo_unitario": round(custo_unit, 2),
        "custo_total": round(custo_total, 2),
        "valor_particular_total": round(particular_total, 2) if particular_total is not None else None,
        "diferenca_particular": round(economia, 2) if economia is not None else None,
        "renda_anual": round(renda_anual, 2),
        "impostos_anuais": round(impostos_anuais, 2),
        "imposto_saude_anual": round(imposto_saude_anual, 2),
        "unidades_cobertas_por_ano": round(unidades_cobertas, 2) if unidades_cobertas is not None else None,
        "cobertura_pct": round(cobertura_pct, 1) if cobertura_pct is not None else None,
        "premissas": {"carga_pct": carga_pct, "parcela_saude_pct": parcela_saude_pct},
    }


@app.get("/api/itens")
def listar_itens():
    return jsonify({"categorias": CATEGORIAS, "itens": ITENS})


@app.get("/api/parametros")
def parametros():
    return jsonify({
        "parametros": PARAMETROS,
        "fontes": FONTES,
        "sigtap_competencia": SIGTAP_COMPETENCIA,
        "bps_periodo": BPS_PERIODO,
    })


@app.route("/api/calcular", methods=["GET", "POST"])
def rota_calcular():
    dados = request.get_json(silent=True) if request.method == "POST" else None
    dados = dados or request.args

    item = _ITENS_POR_ID.get(dados.get("item_id"))
    if item is None:
        return jsonify({"erro": "item_id inválido ou ausente"}), 400

    try:
        quantidade = _validar_quantidade(
            item, _numero(dados.get("quantidade"), 1, minimo=0, maximo=100_000)
        )
        renda = _numero(dados.get("renda_mensal"), 0, minimo=0, maximo=10_000_000)
        carga = _numero(dados.get("carga_pct"), PARAMETROS["carga_tributaria_pct"], 0, 100)
        parcela = _numero(dados.get("parcela_saude_pct"), PARAMETROS["parcela_saude_pct"], 0, 100)
        base = _base(dados.get("base"))
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    return jsonify(calcular(item, quantidade, renda, carga, parcela, base))


@app.get("/api/cenarios")
def listar_cenarios():
    return jsonify({"cenarios": CENARIOS})


@app.route("/api/cesta", methods=["GET", "POST"])
def rota_cesta():
    """Cesta de consumo anual.

    POST JSON: {"itens": [{"item_id": "...", "quantidade": 2}], "renda_mensal": 3000, ...}
    GET: ?itens=consulta_basica:4,hemograma:2&renda_mensal=3000
    """
    if request.method == "POST":
        dados = request.get_json(silent=True) or {}
        brutos = dados.get("itens") or []
    else:
        dados = request.args
        brutos = []
        for parte in (dados.get("itens") or "").split(","):
            if not parte.strip():
                continue
            item_id, _, qtd = parte.partition(":")
            brutos.append({"item_id": item_id.strip(), "quantidade": qtd or 1})

    if not isinstance(brutos, list) or not brutos:
        return jsonify({"erro": "informe ao menos um item na cesta"}), 400
    if len(brutos) > 50:
        return jsonify({"erro": "a cesta aceita no máximo 50 itens"}), 400
    if not all(isinstance(b, dict) for b in brutos):
        return jsonify({"erro": "formato de itens inválido"}), 400

    try:
        renda = _numero(dados.get("renda_mensal"), 0, minimo=0, maximo=10_000_000)
        carga = _numero(dados.get("carga_pct"), PARAMETROS["carga_tributaria_pct"], 0, 100)
        parcela = _numero(dados.get("parcela_saude_pct"), PARAMETROS["parcela_saude_pct"], 0, 100)
        base = _base(dados.get("base"))
        return jsonify(calcular_cesta(brutos, renda, carga, parcela, base))
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@app.get("/api/saude")
def healthcheck():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
