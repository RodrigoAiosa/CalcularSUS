"""Dados do CalcularSUS.

ATENÇÃO: os valores por item (custo_sus / valor_particular) são ESTIMATIVAS
de referência e ainda precisam ser validados contra as fontes oficiais:
  - SIGTAP (tabela de procedimentos do SUS): https://sigtap.datasus.gov.br
  - BPS - Banco de Preços em Saúde (medicamentos): https://bps.saude.gov.br
  - CMED (preço máximo de medicamentos): https://www.gov.br/anvisa

Ao validar um item, troque "validado": False por True e preencha "fonte".
Os PARÂMETROS macro abaixo foram conferidos em reportagens/fontes públicas.
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
        "titulo": "SIGTAP - Tabela de Procedimentos do SUS (para validar os itens)",
        "url": "https://sigtap.datasus.gov.br",
    },
    {
        "titulo": "BPS - Banco de Preços em Saúde (para validar medicamentos)",
        "url": "https://bps.saude.gov.br",
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

_FONTE_PADRAO = "Estimativa de referência - validar no SIGTAP/BPS"

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
     "nome": "Ultrassonografia", "unidade": "exame",
     "custo_sus": 24.20, "valor_particular": 150.00},
    {"id": "tomografia", "categoria": "exames",
     "nome": "Tomografia computadorizada", "unidade": "exame",
     "custo_sus": 138.63, "valor_particular": 700.00},
    {"id": "ressonancia", "categoria": "exames",
     "nome": "Ressonância magnética", "unidade": "exame",
     "custo_sus": 268.75, "valor_particular": 1500.00},

    # ---------------- Procedimentos / internações ----------------
    {"id": "parto_normal", "categoria": "procedimentos",
     "nome": "Parto normal (com internação)", "unidade": "parto",
     "custo_sus": 1500.00, "valor_particular": 10000.00},
    {"id": "cesarea", "categoria": "procedimentos",
     "nome": "Parto cesáreo (com internação)", "unidade": "parto",
     "custo_sus": 2000.00, "valor_particular": 15000.00},
    {"id": "uti_diaria", "categoria": "procedimentos",
     "nome": "Diária de UTI adulto", "unidade": "diária",
     "custo_sus": 2500.00, "valor_particular": 7000.00},
    {"id": "hemodialise", "categoria": "procedimentos",
     "nome": "Sessão de hemodiálise", "unidade": "sessão",
     "custo_sus": 250.00, "valor_particular": 600.00},
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

for _i in ITENS:
    _i.setdefault("validado", False)
    _i.setdefault("fonte", _FONTE_PADRAO)
