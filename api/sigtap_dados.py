"""GERADO por scripts/importar_sigtap.py - não edite à mão."""
COMPETENCIA = '202610'  # AAAAMM
COMPETENCIA_FMT = '10/2026'
ARQUIVO_ORIGEM = 'TabelaUnificada_202610_v2610151110.zip'

PROCEDIMENTOS = {
    'consulta_basica': {'codigo': '0301010064', 'codigo_fmt': '03.01.01.006-4', 'nome': 'CONSULTA MEDICA EM ATENÇÃO PRIMÁRIA', 'competencia': '202610', 'sa': 0.0, 'sh': 0.0, 'sp': 0.0, 'valor': 0.0},
    'consulta_especialista': {'codigo': '0301010072', 'codigo_fmt': '03.01.01.007-2', 'nome': 'CONSULTA MEDICA EM ATENÇÃO ESPECIALIZADA', 'competencia': '202610', 'sa': 10.0, 'sh': 0.0, 'sp': 0.0, 'valor': 10.0},
    'consulta_odonto': {'codigo': '0301010153', 'codigo_fmt': '03.01.01.015-3', 'nome': 'PRIMEIRA CONSULTA ODONTOLOGICA PROGRAMÁTICA', 'competencia': '202610', 'sa': 0.0, 'sh': 0.0, 'sp': 0.0, 'valor': 0.0},
    'upa': {'codigo': '0301060096', 'codigo_fmt': '03.01.06.009-6', 'nome': 'ATENDIMENTO MEDICO EM UNIDADE DE PRONTO ATENDIMENTO', 'competencia': '202610', 'sa': 11.0, 'sh': 0.0, 'sp': 0.0, 'valor': 11.0},
    'samu': {'codigo': '0301030103', 'codigo_fmt': '03.01.03.010-3', 'nome': 'SAMU 192: ATENDIMENTO PRÉ-HOSPITALAR MOVEL REALIZADO PELA EQUIPE DE SUPORTE BASICO DE VIDA TERRESTRE (USB)', 'competencia': '202610', 'sa': 0.0, 'sh': 0.0, 'sp': 0.0, 'valor': 0.0},
    'hemograma': {'codigo': '0202020380', 'codigo_fmt': '02.02.02.038-0', 'nome': 'HEMOGRAMA COMPLETO', 'competencia': '202610', 'sa': 4.11, 'sh': 0.0, 'sp': 0.0, 'valor': 4.11},
    'raio_x': {'codigo': '0204030153', 'codigo_fmt': '02.04.03.015-3', 'nome': 'RADIOGRAFIA DE TORAX (PA E PERFIL)', 'competencia': '202610', 'sa': 9.5, 'sh': 0.0, 'sp': 0.0, 'valor': 9.5},
    'ultrassom': {'codigo': '0205020143', 'codigo_fmt': '02.05.02.014-3', 'nome': 'ULTRASSONOGRAFIA OBSTETRICA', 'competencia': '202610', 'sa': 24.2, 'sh': 24.2, 'sp': 0.0, 'valor': 24.2},
    'tomografia': {'codigo': '0206030010', 'codigo_fmt': '02.06.03.001-0', 'nome': 'TOMOGRAFIA COMPUTADORIZADA DE ABDOMEN SUPERIOR', 'competencia': '202610', 'sa': 138.63, 'sh': 138.63, 'sp': 0.0, 'valor': 138.63},
    'ressonancia': {'codigo': '0207010064', 'codigo_fmt': '02.07.01.006-4', 'nome': 'RESSONANCIA MAGNETICA DE CRANIO', 'competencia': '202610', 'sa': 268.75, 'sh': 268.75, 'sp': 0.0, 'valor': 268.75},
    'parto_normal': {'codigo': '0310010039', 'codigo_fmt': '03.10.01.003-9', 'nome': 'PARTO NORMAL', 'competencia': '202610', 'sa': 0.0, 'sh': 267.6, 'sp': 175.8, 'valor': 443.4},
    'cesarea': {'codigo': '0411010034', 'codigo_fmt': '04.11.01.003-4', 'nome': 'OPERAÇÃO CESARIANA', 'competencia': '202610', 'sa': 0.0, 'sh': 395.68, 'sp': 150.05, 'valor': 545.73},
    'uti_diaria': {'codigo': '0802010083', 'codigo_fmt': '08.02.01.008-3', 'nome': 'DIARIA DE UNIDADE DE TERAPIA INTENSIVA ADULTO (UTI II)', 'competencia': '202610', 'sa': 0.0, 'sh': 510.0, 'sp': 90.0, 'valor': 600.0},
    'hemodialise': {'codigo': '0305010107', 'codigo_fmt': '03.05.01.010-7', 'nome': 'HEMODIÁLISE (MÁXIMO 3 SESSÕES POR SEMANA)', 'competencia': '202610', 'sa': 251.57, 'sh': 0.0, 'sp': 0.0, 'valor': 251.57},
    'catarata': {'codigo': '0405050372', 'codigo_fmt': '04.05.05.037-2', 'nome': 'FACOEMULSIFICAÇÃO COM IMPLANTE DE LENTE INTRA-OCULAR DOBRAVEL', 'competencia': '202610', 'sa': 771.6, 'sh': 642.96, 'sp': 128.64, 'valor': 771.6},
}
