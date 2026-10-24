"""Dados do CalcularSUS.

Como os valores são tratados
----------------------------
- custo_sus: custo de referência do item para o sistema (estimativa). Quando o
  SIGTAP traz um valor equivalente e ele é igual ao custo_sus, o item fica
  "validado" (valor oficial).
- valor_sigtap: repasse federal oficial da Tabela SIGTAP (api/sigtap_dados.py,
  gerado por scripts/importar_sigtap.py). None = sem valor próprio na tabela.
- bps: preço de compra pública de medicamentos (api/bps_dados.py, gerado por
  scripts/importar_bps.py). Quando existe, substitui o custo_sus do item; fica
  "validado" só se a amostra for robusta (>= 30 compras, preços pouco dispersos).
- valor_particular: preço aproximado de mercado (estimativa; ver CMED).

Ainda sem fonte oficial: vacina, atenção primária/odontologia/SAMU (custo real) e
antirretrovirais (compra centralizada, fora do BPS). Os PARÂMETROS macro abaixo
foram conferidos em reportagens/fontes públicas.
"""

# --------------------------------------------------------------------------
# Parâmetros macro (editáveis pelo usuário na interface)
# --------------------------------------------------------------------------
PARAMETROS = {
    # Carga tributária bruta de 2025: 32,4% do PIB (Tesouro Nacional).
    "carga_tributaria_pct": 32.4,
    # Fatia dos tributos que vira gasto público em saúde (União + estados +
    # municípios). Derivada: ~R$ 1.398,53 per capita (2019, CFM/Siops) x
    # população da época / arrecadação total ≈ 12%. É uma aproximação.
    "parcela_saude_pct": 12.0,
    # Censo 2022 (IBGE).
    "populacao": 203_080_756,
    # Gasto público per capita em saúde (3 esferas), dado de 2019 (CFM/Siops).
    "gasto_per_capita_ano": 1398.53,
    "gasto_per_capita_dia": 3.83,
    # PLOA 2026: aplicação da União em ações e serviços públicos de saúde.
    "orcamento_saude_uniao_2026_bi": 245.6,
}

FONTES = [
    {
        "titulo": "Carga tributária bruta de 32,4% do PIB em 2025 (recorde da série)",
        "url": "https://www.folhape.com.br/economia/carga-tributaria-do-brasil-sobe-para-324-do-pib-em-2025-maior-valor/479905/",
    },
    {
        "titulo": "CFM: Brasil gasta R$ 3,83 ao dia com a saúde de cada habitante (2019, Siops)",
        "url": "https://portal.cfm.org.br/noticias/brasil-gasta-r-383-ao-dia-com-a-saude-de-cada-habitante/",
    },
    {
        "titulo": "PLOA 2026 prevê R$ 245,6 bilhões para saúde",
        "url": "https://medicinasa.com.br/?p=143004",
    },
    {
        "titulo": "SIGTAP - Tabela de Procedimentos do SUS (DATASUS), competência 10/2026",
        "url": "https://sigtap.datasus.gov.br",
    },
    {
        "titulo": "BPS - Banco de Preços em Saúde, compras públicas (dados abertos do Ministério da Saúde)",
        "url": "https://dadosabertos.saude.gov.br/dataset/bps",
    },
]

# --------------------------------------------------------------------------
# Itens: atendimentos, exames, procedimentos e medicamentos
# custo_sus        -> custo estimado para o sistema público, por unidade (R$)
# valor_particular -> preço de mercado aproximado do mesmo item (R$) ou None
# --------------------------------------------------------------------------
CATEGORIAS = {
    "atendimentos": "Atendimentos e consultas",
    "exames": "Exames",
    "procedimentos": "Procedimentos e internações",
    "medicamentos": "Medicamentos (tratamento de 1 mês)",
}

ITENS = [
    # ---------------- Atendimentos ----------------
    {"id": "consulta_basica", "categoria": "atendimentos",
     "nome": "Consulta médica na UBS (atenção básica)", "unidade": "consulta",
     "custo_sus": 100.00, "valor_particular": 250.00},
    {"id": "consulta_especialista", "categoria": "atendimentos",
     "nome": "Consulta com médico especialista", "unidade": "consulta",
     "custo_sus": 150.00, "valor_particular": 350.00},
    {"id": "consulta_odonto", "categoria": "atendimentos",
     "nome": "Atendimento odontológico", "unidade": "atendimento",
     "custo_sus": 80.00, "valor_particular": 200.00},
    {"id": "upa", "categoria": "atendimentos",
     "nome": "Atendimento de urgência na UPA", "unidade": "atendimento",
     "custo_sus": 350.00, "valor_particular": 800.00},
    {"id": "samu", "categoria": "atendimentos",
     "nome": "Chamado do SAMU (ambulância)", "unidade": "chamado",
     "custo_sus": 1500.00, "valor_particular": 3000.00},
    {"id": "vacina", "categoria": "atendimentos",
     "nome": "Vacina (dose média do calendário)", "unidade": "dose",
     "custo_sus": 50.00, "valor_particular": 150.00},

    # ---------------- Exames ----------------
    {"id": "hemograma", "categoria": "exames",
     "nome": "Hemograma completo", "unidade": "exame",
     "custo_sus": 4.11, "valor_particular": 40.00},
    {"id": "raio_x", "categoria": "exames",
     "nome": "Raio-X de tórax", "unidade": "exame",
     "custo_sus": 9.50, "valor_particular": 100.00},
    {"id": "ultrassom", "categoria": "exames",
     "nome": "Ultrassonografia obstétrica", "unidade": "exame",
     "custo_sus": 24.20, "valor_particular": 150.00},
    {"id": "tomografia", "categoria": "exames",
     "nome": "Tomografia computadorizada (abdômen)", "unidade": "exame",
     "custo_sus": 138.63, "valor_particular": 700.00},
    {"id": "ressonancia", "categoria": "exames",
     "nome": "Ressonância magnética (crânio)", "unidade": "exame",
     "custo_sus": 268.75, "valor_particular": 1500.00},

    # ---------------- Procedimentos / internações ----------------
    {"id": "parto_normal", "categoria": "procedimentos",
     "nome": "Parto normal (com internação)", "unidade": "parto",
     "custo_sus": 1500.00, "valor_particular": 10000.00},
    {"id": "cesarea", "categoria": "procedimentos",
     "nome": "Parto cesáreo (com internação)", "unidade": "parto",
     "custo_sus": 2000.00, "valor_particular": 15000.00},
    {"id": "uti_diaria", "categoria": "procedimentos",
     "nome": "Diária de UTI adulto (tipo II)", "unidade": "diária",
     "custo_sus": 2500.00, "valor_particular": 7000.00},
    {"id": "hemodialise", "categoria": "procedimentos",
     "nome": "Sessão de hemodiálise", "unidade": "sessão",
     "custo_sus": 251.57, "valor_particular": 600.00},
    {"id": "catarata", "categoria": "procedimentos",
     "nome": "Cirurgia de catarata", "unidade": "cirurgia",
     "custo_sus": 900.00, "valor_particular": 5000.00},

    # ---------------- Medicamentos ----------------
    {"id": "losartana", "categoria": "medicamentos",
     "nome": "Losartana 50 mg (30 comprimidos) - pressão alta", "unidade": "mês",
     "custo_sus": 3.00, "valor_particular": 20.00},
    {"id": "metformina", "categoria": "medicamentos",
     "nome": "Metformina 850 mg (60 comprimidos) - diabetes", "unidade": "mês",
     "custo_sus": 8.00, "valor_particular": 25.00},
    {"id": "insulina_nph", "categoria": "medicamentos",
     "nome": "Insulina NPH (frasco 10 mL)", "unidade": "frasco",
     "custo_sus": 25.00, "valor_particular": 70.00},
    {"id": "omeprazol", "categoria": "medicamentos",
     "nome": "Omeprazol 20 mg (28 cápsulas)", "unidade": "mês",
     "custo_sus": 4.00, "valor_particular": 20.00},
    {"id": "salbutamol", "categoria": "medicamentos",
     "nome": "Salbutamol spray - asma", "unidade": "frasco",
     "custo_sus": 12.00, "valor_particular": 40.00},
    {"id": "antirretroviral", "categoria": "medicamentos",
     "nome": "Antirretrovirais (esquema mensal HIV)", "unidade": "mês",
     "custo_sus": 250.00, "valor_particular": None},
    {"id": "alto_custo", "categoria": "medicamentos",
     "nome": "Medicamento de alto custo (ex.: adalimumabe)", "unidade": "dose",
     "custo_sus": 3500.00, "valor_particular": 6000.00},
]

from sigtap_dados import COMPETENCIA_FMT, PROCEDIMENTOS  # noqa: E402  (gerado por scripts/importar_sigtap.py)
from bps_dados import PERIODO as BPS_PERIODO, PRECOS as BPS_PRECOS  # noqa: E402  (gerado por scripts/importar_bps.py)

SIGTAP_COMPETENCIA = COMPETENCIA_FMT


def _brl(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _bps_robusto(b):
    """Amostra suficiente (>= 30 compras) e preços pouco dispersos (p75 <= 3 x p25)."""
    return b["n_compras"] >= 30 and b["valor_p25"] > 0 and b["valor_p75"] <= 3 * b["valor_p25"]

for _i in ITENS:
    # Itens cobrados por mês só podem ser usados até 12 meses por ano.
    if _i["unidade"] == "mês":
        _i["max_por_ano"] = 12

    # Valor oficial da Tabela SIGTAP (repasse federal). Valor 0 = procedimento
    # existe, mas não tem valor próprio (ex.: atenção primária, SAMU).
    _sig = PROCEDIMENTOS.get(_i["id"])
    _i["sigtap"] = _sig
    _i["valor_sigtap"] = _sig["valor"] if _sig and _sig["valor"] > 0 else None

    # Preço de compra pública (BPS): substitui a estimativa de custo dos medicamentos.
    _bps = BPS_PRECOS.get(_i["id"])
    _i["bps"] = _bps
    if _bps:
        _i["custo_sus"] = _bps["valor"]

    # "validado" = o custo usado vem de fonte oficial: valor idêntico ao do SIGTAP
    # ou preço de compra do BPS com amostra robusta.
    _sigtap_ok = _i["valor_sigtap"] is not None and abs(_i["custo_sus"] - _i["valor_sigtap"]) < 0.005
    _bps_ok = _bps is not None and _bps_robusto(_bps)
    _i["validado"] = _sigtap_ok or _bps_ok
    _i["fonte_oficial"] = "SIGTAP" if _sigtap_ok else ("BPS" if _bps_ok else None)

    if _sigtap_ok:
        _i["fonte"] = f"SIGTAP {_sig['codigo_fmt']} - competência {SIGTAP_COMPETENCIA}"
    elif _bps:
        _i["fonte"] = (
            f"BPS (compras públicas): mediana de {_bps['n_compras']} compras em {BPS_PERIODO}, "
            f"código BR {_bps['codigo_br']} ({_bps['apresentacao']}); faixa R$ {_brl(_bps['valor_p25'])} "
            f"a R$ {_brl(_bps['valor_p75'])}"
            + ("" if _bps_ok else ". Amostra pequena ou preços muito dispersos: usar com cautela")
        )
    elif _i["valor_sigtap"] is not None:
        _vl = f"{_i['valor_sigtap']:.2f}".replace(".", ",")
        _i["fonte"] = (
            f"Custo real: estimativa. Repasse oficial SIGTAP {_sig['codigo_fmt']}: "
            f"R$ {_vl} (competência {SIGTAP_COMPETENCIA})"
        )
    elif _sig is not None:
        _i["fonte"] = (
            f"Estimativa. Procedimento SIGTAP {_sig['codigo_fmt']} existe, mas sem valor próprio "
            "(financiado por repasse global)"
        )
    elif _i["categoria"] == "medicamentos":
        _i["fonte"] = (
            "Estimativa. Não consta no SIGTAP nem no BPS (compra centralizada pelo "
            "Ministério da Saúde); validar com o Ministério"
        )
    else:
        _i["fonte"] = "Estimativa. Sem procedimento equivalente no SIGTAP"

# --------------------------------------------------------------------------
# Cenários prontos: combinações ilustrativas de consumo em 1 ano.
# As quantidades são exemplos didáticos, não protocolos clínicos.
# --------------------------------------------------------------------------
CENARIOS = [
    {
        "id": "diabetico",
        "nome": "Pessoa com diabetes",
        "descricao": "Acompanhamento regular: consultas, exames de sangue, metformina e insulina.",
        "itens": [
            {"item_id": "consulta_basica", "quantidade": 4},
            {"item_id": "consulta_especialista", "quantidade": 2},
            {"item_id": "hemograma", "quantidade": 4},
            {"item_id": "metformina", "quantidade": 12},
            {"item_id": "insulina_nph", "quantidade": 12},
        ],
    },
    {
        "id": "gestante",
        "nome": "Gestação com parto",
        "descricao": "Pré-natal, exames, ultrassons, vacinas e parto normal com internação.",
        "itens": [
            {"item_id": "consulta_basica", "quantidade": 7},
            {"item_id": "hemograma", "quantidade": 3},
            {"item_id": "ultrassom", "quantidade": 3},
            {"item_id": "vacina", "quantidade": 2},
            {"item_id": "parto_normal", "quantidade": 1},
        ],
    },
    {
        "id": "hemodialise",
        "nome": "Hemodiálise por 1 ano",
        "descricao": "Três sessões por semana (156 por ano) e acompanhamento com especialista.",
        "itens": [
            {"item_id": "hemodialise", "quantidade": 156},
            {"item_id": "consulta_especialista", "quantidade": 4},
            {"item_id": "hemograma", "quantidade": 12},
        ],
    },
    {
        "id": "uti",
        "nome": "Internação de 10 dias na UTI",
        "descricao": "Diárias de UTI com exames de imagem e laboratório durante a internação.",
        "itens": [
            {"item_id": "samu", "quantidade": 1},
            {"item_id": "uti_diaria", "quantidade": 10},
            {"item_id": "tomografia", "quantidade": 1},
            {"item_id": "raio_x", "quantidade": 2},
            {"item_id": "hemograma", "quantidade": 6},
        ],
    },
    {
        "id": "alto_custo",
        "nome": "Medicamento de alto custo",
        "descricao": "Uma dose a cada 15 dias (26 por ano) com consultas e exames de controle.",
        "itens": [
            {"item_id": "alto_custo", "quantidade": 26},
            {"item_id": "consulta_especialista", "quantidade": 4},
            {"item_id": "hemograma", "quantidade": 4},
        ],
    },
    {
        "id": "hiv",
        "nome": "Tratamento de HIV",
        "descricao": "Antirretrovirais todo mês, consultas com especialista e exames de controle.",
        "itens": [
            {"item_id": "antirretroviral", "quantidade": 12},
            {"item_id": "consulta_especialista", "quantidade": 4},
            {"item_id": "hemograma", "quantidade": 4},
        ],
    },
]
