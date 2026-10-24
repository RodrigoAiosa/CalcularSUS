"""Importa valores oficiais da Tabela Unificada do SIGTAP para o CalcularSUS.

Uso:
    python3 scripts/importar_sigtap.py TabelaUnificada_202610_v2610151110.zip
    python3 scripts/importar_sigtap.py caminho/para/tb_procedimento.txt

O zip (ou o tb_procedimento.txt extraído) é publicado todo mês pelo DATASUS:
    https://sigtap.datasus.gov.br  ->  Download da Tabela Unificada

Saída: api/sigtap_dados.py (não edite à mão; rode o script de novo a cada competência).

Como o valor é calculado
------------------------
O layout de tb_procedimento.txt é de largura fixa; os valores vêm em centavos
(VL_SH, VL_SA, VL_SP). Regra usada aqui:
    valor = VL_SA, se > 0 (procedimento ambulatorial; já é o total)
    valor = VL_SH + VL_SP, caso contrário (procedimento hospitalar)
Valor 0 significa que o procedimento existe na tabela, mas NÃO tem valor
próprio (ex.: consulta na atenção primária, financiada por repasse per capita).

ATENÇÃO: os valores do SIGTAP são o repasse federal por procedimento. Não são o
custo total do atendimento (estados e municípios complementam).
"""
import sys
import zipfile
from pathlib import Path

# item_id do CalcularSUS -> código do procedimento no SIGTAP (10 dígitos, sem pontuação)
MAPEAMENTO = {
    "consulta_basica": "0301010064",         # Consulta médica em atenção primária
    "consulta_especialista": "0301010072",   # Consulta médica em atenção especializada
    "consulta_odonto": "0301010153",         # Primeira consulta odontológica programática
    "upa": "0301060096",                     # Atendimento médico em unidade de pronto atendimento
    "samu": "0301030103",                    # SAMU 192: suporte básico de vida terrestre
    "hemograma": "0202020380",               # Hemograma completo
    "raio_x": "0204030153",                  # Radiografia de tórax (PA e perfil)
    "ultrassom": "0205020143",               # Ultrassonografia obstétrica
    "tomografia": "0206030010",              # Tomografia computadorizada de abdômen superior
    "ressonancia": "0207010064",             # Ressonância magnética de crânio
    "parto_normal": "0310010039",            # Parto normal
    "cesarea": "0411010034",                 # Operação cesariana
    "uti_diaria": "0802010083",              # Diária de UTI adulto (UTI II)
    "hemodialise": "0305010107",             # Hemodiálise (máximo 3 sessões por semana)
    "catarata": "0405050372",                # Facoemulsificação com LIO dobrável
}
# Sem equivalente no SIGTAP: vacina (PNI) e medicamentos (ver BPS/CMED).

LARGURA_MIN = 336


def abrir_linhas(caminho: Path):
    if caminho.suffix.lower() == ".zip":
        with zipfile.ZipFile(caminho) as z:
            nomes = z.namelist()
            if any(n.startswith("/") or ".." in n.split("/") for n in nomes):
                raise SystemExit("zip com caminhos suspeitos; abortando")
            with z.open("tb_procedimento.txt") as f:
                for linha in f:
                    yield linha.decode("latin-1").rstrip("\r\n")
    else:
        with open(caminho, encoding="latin-1") as f:
            for linha in f:
                yield linha.rstrip("\r\n")


def main(caminho: Path, saida: Path):
    codigos = {c: i for i, c in MAPEAMENTO.items()}
    achados, competencia = {}, None

    for linha in abrir_linhas(caminho):
        if len(linha) < LARGURA_MIN:
            continue
        co = linha[0:10]
        competencia = competencia or linha[330:336]
        if co not in codigos:
            continue
        sh = int(linha[282:294]) / 100
        sa = int(linha[294:306]) / 100
        sp = int(linha[306:318]) / 100
        achados[codigos[co]] = {
            "codigo": co,
            "codigo_fmt": f"{co[0:2]}.{co[2:4]}.{co[4:6]}.{co[6:9]}-{co[9]}",
            "nome": linha[10:260].strip(),
            "competencia": linha[330:336],
            "sa": round(sa, 2),
            "sh": round(sh, 2),
            "sp": round(sp, 2),
            "valor": round(sa if sa > 0 else sh + sp, 2),
        }

    faltando = sorted(set(MAPEAMENTO) - set(achados))
    if faltando:
        raise SystemExit(f"códigos não encontrados na tabela: {faltando}")

    comp_fmt = f"{competencia[4:6]}/{competencia[0:4]}"
    linhas = [
        '"""GERADO por scripts/importar_sigtap.py - não edite à mão."""',
        f"COMPETENCIA = {competencia!r}  # AAAAMM",
        f"COMPETENCIA_FMT = {comp_fmt!r}",
        f"ARQUIVO_ORIGEM = {caminho.name!r}",
        "",
        "PROCEDIMENTOS = {",
    ]
    for item_id in MAPEAMENTO:
        linhas.append(f"    {item_id!r}: {achados[item_id]!r},")
    linhas.append("}")
    saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"{len(achados)} procedimentos, competência {comp_fmt} -> {saida}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raiz = Path(__file__).resolve().parent.parent
    main(Path(sys.argv[1]), raiz / "api" / "sigtap_dados.py")
