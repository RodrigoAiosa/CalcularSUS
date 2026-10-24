"""API do CalcularSUS (Flask) - roda como função serverless na Vercel."""
from flask import Flask, jsonify, request

try:  # execução na Vercel / pacote
    from .dados import CATEGORIAS, FONTES, ITENS, PARAMETROS
except ImportError:  # execução direta: python api/index.py
    from dados import CATEGORIAS, FONTES, ITENS, PARAMETROS

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


def calcular(item, quantidade, renda_mensal, carga_pct, parcela_saude_pct):
    custo_unit = item["custo_sus"]
    particular_unit = item["valor_particular"]

    custo_total = custo_unit * quantidade
    particular_total = particular_unit * quantidade if particular_unit is not None else None

    renda_anual = renda_mensal * 12
    impostos_anuais = renda_anual * carga_pct / 100
    imposto_saude_anual = impostos_anuais * parcela_saude_pct / 100

    unidades_cobertas = imposto_saude_anual / custo_unit if custo_unit else None
    cobertura_pct = (imposto_saude_anual / custo_total * 100) if custo_total else None
    economia = (particular_total - custo_total) if particular_total is not None else None

    return {
        "item": item,
        "quantidade": quantidade,
        "pago_na_hora": 0.0,
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
    return jsonify({"parametros": PARAMETROS, "fontes": FONTES})


@app.route("/api/calcular", methods=["GET", "POST"])
def rota_calcular():
    dados = request.get_json(silent=True) if request.method == "POST" else None
    dados = dados or request.args

    item = _ITENS_POR_ID.get(dados.get("item_id"))
    if item is None:
        return jsonify({"erro": "item_id inválido ou ausente"}), 400

    try:
        quantidade = _numero(dados.get("quantidade"), 1, minimo=0, maximo=100_000)
        renda = _numero(dados.get("renda_mensal"), 0, minimo=0, maximo=10_000_000)
        carga = _numero(dados.get("carga_pct"), PARAMETROS["carga_tributaria_pct"], 0, 100)
        parcela = _numero(dados.get("parcela_saude_pct"), PARAMETROS["parcela_saude_pct"], 0, 100)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    return jsonify(calcular(item, quantidade, renda, carga, parcela))


@app.get("/api/saude")
def healthcheck():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
