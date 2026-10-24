"""GERADO por scripts/importar_bps.py - não edite à mão."""
PERIODO = '2024-2026'
ARQUIVOS_ORIGEM = ['BPS_20_26_Bruno_Briani.zip']
LINHAS_LIDAS = 342697

PRECOS = {
    'losartana': {'codigo_br': '268856', 'descricao': 'LOSARTANA POTÁSSICA, DOSAGEM:50 MG', 'unidade_fornecimento': 'COMPRIMIDO', 'multiplicador': 30, 'apresentacao': '30 comprimidos de 50 mg', 'n_compras': 131, 'preco_unitario_mediana': 0.04, 'valor': 1.2, 'valor_p25': 1.05, 'valor_p75': 1.5},
    'metformina': {'codigo_br': '267691', 'descricao': 'METFORMINA CLORIDRATO, DOSAGEM:850 MG', 'unidade_fornecimento': 'COMPRIMIDO', 'multiplicador': 60, 'apresentacao': '60 comprimidos de 850 mg', 'n_compras': 127, 'preco_unitario_mediana': 0.125, 'valor': 7.5, 'valor_p25': 6.48, 'valor_p75': 9.0},
    'insulina_nph': {'codigo_br': '271157', 'descricao': 'INSULINA, ORIGEM:HUMANA, TIPO:NPH, DOSAGEM:100U/ML, APLICAÇÃO:INJETÁVEL', 'unidade_fornecimento': 'FRASCO', 'multiplicador': 1, 'apresentacao': '1 frasco de insulina humana NPH 100 U/mL', 'n_compras': 10, 'preco_unitario_mediana': 30.4, 'valor': 30.4, 'valor_p25': 24.0, 'valor_p75': 41.7},
    'omeprazol': {'codigo_br': '267712', 'descricao': 'OMEPRAZOL, CONCENTRAÇÃO:20 MG', 'unidade_fornecimento': 'CAPSULA', 'multiplicador': 28, 'apresentacao': '28 cápsulas de 20 mg', 'n_compras': 110, 'preco_unitario_mediana': 0.06, 'valor': 1.68, 'valor_p25': 1.4, 'valor_p75': 2.24},
    'salbutamol': {'codigo_br': '294887', 'descricao': 'SALBUTAMOL, DOSAGEM:100MCG/DOSE, FORMA FARMACÊUTICA:AEROSOL ORAL', 'unidade_fornecimento': 'FRASCO', 'multiplicador': 1, 'apresentacao': '1 frasco de aerossol 100 mcg/dose', 'n_compras': 81, 'preco_unitario_mediana': 12.23, 'valor': 12.23, 'valor_p25': 10.28, 'valor_p75': 14.25},
    'alto_custo': {'codigo_br': '290058', 'descricao': 'ADALIMUMABE, CONCENTRAÇÃO:40 MG, APRESENTAÇÃO:SOLUÇÃO INJETÁVEL', 'unidade_fornecimento': 'SERINGA', 'multiplicador': 1, 'apresentacao': '1 seringa de adalimumabe 40 mg', 'n_compras': 12, 'preco_unitario_mediana': 1838.095, 'valor': 1838.1, 'valor_p25': 641.15, 'valor_p75': 3533.0},
}
