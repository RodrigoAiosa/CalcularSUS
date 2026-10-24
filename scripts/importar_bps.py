"""Calcula preços de medicamentos a partir do Banco de Preços em Saúde (BPS).

Uso:
    python3 scripts/importar_bps.py ARQUIVO [ARQUIVO ...]

ARQUIVO pode ser um .csv ou um .zip contendo .csv (um por ano, ou consolidado).
Os arquivos anuais oficiais ficam em:
    https://dadosabertos.saude.gov.br/dataset/bps
    (padrão: https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/BPS/csv/AAAA_csv.zip)

Saída: api/bps_dados.py (não edite à mão; rode o script de novo ao atualizar).

Método
------
- Cada linha do BPS é uma compra pública (município, estado ou Ministério).
- Filtra o item pelo código BR (CATMAT) e pela unidade de fornecimento.
- Usa só os 3 anos mais recentes presentes nos arquivos.
- Preço do item = MEDIANA do preço unitário das compras x multiplicador da
  apresentação (ex.: 30 comprimidos). Não pondera por quantidade, porque há
  registros com quantidades absurdas (erros de digitação/unidade) na base.
- Guarda também o intervalo interquartil (p25-p75) e o número de compras.

O BPS cobre compras de medicamentos e materiais. Antirretrovirais (compra
centralizada do Ministério) não aparecem na base.
"""
import csv
import io
import statistics
import sys
import unicodedata
import zipfile
from pathlib import Path

# item_id -> (codigo BR, unidade de fornecimento, multiplicador, apresentação)
MAPEAMENTO = {
    "losartana": ("268856", "COMPRIMIDO", 30, "30 comprimidos de 50 mg"),
    "metformina": ("267691", "COMPRIMIDO", 60, "60 comprimidos de 850 mg"),
    "insulina_nph": ("271157", "FRASCO", 1, "1 frasco de insulina humana NPH 100 U/mL"),
    "omeprazol": ("267712", "CAPSULA", 28, "28 cápsulas de 20 mg"),
    "salbutamol": ("294887", "FRASCO", 1, "1 frasco de aerossol 100 mcg/dose"),
    "alto_custo": ("290058", "SERINGA", 1, "1 seringa de adalimumabe 40 mg"),
}

ALIAS = {
    "codigo": ["codigo_br", "cd_catmat", "codigo br"],
    "descricao": ["descricao_catmat", "ds_item", "descricao catmat"],
    "unidade": ["unidade_fornecimento", "un_fornecimento", "unidade de fornecimento"],
    "preco": ["preco_unitario", "vl_preco_unitario", "preco unitario"],
    "ano": ["ano_compra", "ano"],
}


def norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().strip().upper()


def achar_coluna(cabecalho, chave):
    mapa = {norm(c).lower(): c for c in cabecalho}
    for nome in ALIAS[chave]:
        if norm(nome).lower() in mapa:
            return mapa[norm(nome).lower()]
    raise SystemExit(f"coluna '{chave}' não encontrada; cabeçalho: {cabecalho}")


def abrir_csvs(caminho: Path):
    """Gera (nome, arquivo_texto) para cada CSV encontrado."""
    if caminho.suffix.lower() == ".zip":
        with zipfile.ZipFile(caminho) as z:
            for n in z.namelist():
                if n.startswith("/") or ".." in n.split("/"):
                    raise SystemExit("zip com caminhos suspeitos; abortando")
            for n in z.namelist():
                if n.lower().endswith(".csv"):
                    with z.open(n) as f:
                        yield n, io.TextIOWrapper(f, encoding="utf-8-sig", newline="")
    else:
        with open(caminho, encoding="utf-8-sig", newline="") as f:
            yield caminho.name, f


def ler_precos(caminhos):
    """{(codigo, unidade_norm): [(ano, preco), ...]} para os itens mapeados."""
    alvo = {(c, norm(u)) for c, u, _, _ in MAPEAMENTO.values()}
    achados = {}
    descricoes = {}
    total = 0
    for caminho in caminhos:
        for nome, f in abrir_csvs(Path(caminho)):
            leitor = csv.reader(f, delimiter=";")
            cab = next(leitor)
            ic, id_, iu, ip, ia = (achar_coluna(cab, k) for k in ("codigo", "descricao", "unidade", "preco", "ano"))
            ic, id_, iu, ip, ia = (cab.index(x) for x in (ic, id_, iu, ip, ia))
            for linha in leitor:
                total += 1
                chave = (linha[ic].strip(), norm(linha[iu]))
                if chave not in alvo:
                    continue
                try:
                    preco = float(linha[ip].replace(",", "."))
                    ano = int(float(linha[ia]))
                except ValueError:
                    continue
                if preco <= 0:
                    continue
                achados.setdefault(chave, []).append((ano, preco))
                descricoes[chave] = linha[id_].strip()
    return achados, descricoes, total


def quartis(valores):
    q = statistics.quantiles(valores, n=4, method="inclusive") if len(valores) >= 2 else [valores[0]] * 3
    return q[0], q[2]


def main(caminhos, saida: Path):
    achados, descricoes, total = ler_precos(caminhos)
    todos_anos = sorted({a for v in achados.values() for a, _ in v})
    if not todos_anos:
        raise SystemExit("nenhuma compra dos itens mapeados foi encontrada")
    anos_usados = todos_anos[-3:]
    periodo = f"{anos_usados[0]}-{anos_usados[-1]}"

    resultado = {}
    for item_id, (codigo, unidade, mult, apres) in MAPEAMENTO.items():
        precos = [p for a, p in achados.get((codigo, norm(unidade)), []) if a in anos_usados]
        if not precos:
            print(f"AVISO: sem compras de {item_id} em {periodo}")
            continue
        med = statistics.median(precos)
        p25, p75 = quartis(precos)
        resultado[item_id] = {
            "codigo_br": codigo,
            "descricao": descricoes[(codigo, norm(unidade))],
            "unidade_fornecimento": unidade,
            "multiplicador": mult,
            "apresentacao": apres,
            "n_compras": len(precos),
            "preco_unitario_mediana": round(med, 4),
            "valor": round(med * mult, 2),
            "valor_p25": round(p25 * mult, 2),
            "valor_p75": round(p75 * mult, 2),
        }

    linhas = [
        '"""GERADO por scripts/importar_bps.py - não edite à mão."""',
        f"PERIODO = {periodo!r}",
        f"ARQUIVOS_ORIGEM = {[Path(c).name for c in caminhos]!r}",
        f"LINHAS_LIDAS = {total}",
        "",
        "PRECOS = {",
    ]
    for item_id, dados in resultado.items():
        linhas.append(f"    {item_id!r}: {dados!r},")
    linhas.append("}")
    saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"{len(resultado)} itens, período {periodo}, {total} linhas lidas -> {saida}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    raiz = Path(__file__).resolve().parent.parent
    main(sys.argv[1:], raiz / "api" / "bps_dados.py")
