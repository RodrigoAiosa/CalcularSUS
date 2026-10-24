# CalcularSUS

Calculadora que mostra quanto custam os principais atendimentos e medicamentos do SUS.
Na porta o paciente não paga, mas a conta é paga por todos através dos impostos.

**Stack:** Python (Flask) como API serverless + HTML/JS estático, hospedado na Vercel.

## Estrutura

```
CalcularSUS/
├── api/
│   ├── index.py      # API Flask (rotas /api/*)
│   ├── dados.py          # itens, categorias, cenários, parâmetros e fontes
│   ├── sigtap_dados.py   # valores oficiais do SIGTAP (gerado pelo script)
│   └── bps_dados.py      # preços de medicamentos do BPS (gerado pelo script)
├── scripts/
│   ├── importar_sigtap.py  # importa a Tabela Unificada do SIGTAP
│   └── importar_bps.py     # calcula preços de medicamentos a partir do BPS
├── public/
│   └── index.html    # interface
└── requirements.txt
```

## Rodar localmente

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python api/index.py          # API em http://localhost:5000
```

Para testar o site completo com a mesma configuração da Vercel:

```bash
npm i -g vercel
vercel dev
```

## Deploy

```bash
vercel          # preview
vercel --prod   # produção
```

## API

| Rota | Descrição |
|------|-----------|
| `GET /api/itens` | Lista categorias e itens |
| `GET /api/parametros` | Premissas macro e fontes |
| `GET/POST /api/calcular` | Calcula um item. Parâmetros: `item_id`, `quantidade`, `renda_mensal`, `carga_pct`, `parcela_saude_pct`, `base` (`estimado` ou `sigtap`) |
| `GET /api/cenarios` | Cenários prontos (uso leve, diabetes, gestação, hemodiálise, UTI, alto custo, HIV) |
| `GET/POST /api/cesta` | Soma vários itens e compara com a contribuição anual |

Exemplos:

```
/api/calcular?item_id=consulta_basica&quantidade=4&renda_mensal=3000
/api/cesta?itens=consulta_basica:4,hemograma:2&renda_mensal=3000
```

`POST /api/cesta` aceita JSON: `{"itens": [{"item_id": "uti_diaria", "quantidade": 10}], "renda_mensal": 3000}`.

Itens cobrados por mês (ex.: medicamentos de uso contínuo) aceitam no máximo 12 por ano (`max_por_ano`).

## Interface

1. **Seus dados:** renda e premissas (carga tributária e % para saúde).
2. **Cesta do ano:** cenários prontos ou itens montados pelo usuário, com gráfico de contribuição x custo.
3. **Calculadora de um item:** custo de um item e botão para adicionar à cesta.

Os cenários ficam em `api/dados.py` (`CENARIOS`) e são exemplos didáticos, não protocolos clínicos.

## Como o cálculo funciona

- **Custo total** = custo do item × quantidade
- **Impostos que você paga por ano** = renda mensal × 12 × carga tributária
- **Parte que vai para a saúde** = impostos × % aplicado em saúde
- **Cobertura** = parte da saúde ÷ custo total do uso
- **Renda de equilíbrio** (`renda_equilibrio_mensal`) = custo do uso ÷ (12 × carga tributária × % para saúde):
  a renda mensal em que a contribuição para a saúde iguala o consumo. Com as premissas
  padrão, o cenário "Uso leve" (2 consultas com especialista, 2 de dentista e 2 na UPA, custo de
  R$ 1.160) tem equilíbrio em ~R$ 2.486 de renda mensal; abaixo disso o uso supera a contribuição.

## Dados: o que já está validado e o que falta

Premissas macro (conferidas em fontes públicas, ver `api/dados.py`):
- Carga tributária de 32,4% do PIB em 2025
- Gasto público per capita em saúde: R$ 1.398,53/ano (2019, CFM/Siops)
- PLOA 2026: R$ 245,6 bi para saúde na União
- ~12% dos tributos em saúde: **aproximação derivada**, editável na interface

### Valores oficiais (SIGTAP)

Os valores oficiais vêm da Tabela Unificada do SIGTAP (DATASUS), **competência 10/2026**,
importados por `scripts/importar_sigtap.py` para `api/sigtap_dados.py` (arquivo gerado).
Cada item tem dois valores:

- `valor_sigtap`: **repasse federal oficial** por procedimento (`None` = sem valor próprio na tabela).
- `custo_sus`: custo de referência para o sistema. É igual ao valor oficial nos itens
  `validado: true` (exames e hemodiálise) e uma **estimativa** nos demais.

A interface tem o seletor **Base dos valores**: "Custo estimado" (padrão) ou "Tabela SIGTAP".
Na API, use `base=estimado` ou `base=sigtap` em `/api/calcular` e `/api/cesta`.
Itens sem valor na base escolhida entram como R$ 0,00 e a resposta lista `itens_sem_valor`.

**Importante:** o SIGTAP é o repasse federal, não o custo total. A consulta especializada
paga R$ 10,00 e a consulta na atenção primária nem tem valor por procedimento (é financiada
por repasse per capita). Vacinas e medicamentos de uso comum também não constam na tabela.

### Atualizar para uma nova competência

```bash
# baixe TabelaUnificada_AAAAMM_*.zip em https://sigtap.datasus.gov.br (Download)
python3 scripts/importar_sigtap.py caminho/TabelaUnificada_AAAAMM_vXXXX.zip
```

O mapeamento item -> código do procedimento fica em `MAPEAMENTO` no próprio script.
O zip desta competência foi obtido de um espelho público do FTP do DATASUS
([RenatoKR/SIGTAP](https://github.com/RenatoKR/SIGTAP)); confira os valores no site oficial antes de divulgar.

### Preços de medicamentos (BPS)

Os medicamentos usam o **Banco de Preços em Saúde** (compras públicas de municípios,
estados e Ministério), período **2024-2026**, importado por `scripts/importar_bps.py`
para `api/bps_dados.py` (arquivo gerado). Método: filtra o item pelo **código BR (CATMAT)**
e pela unidade de fornecimento, e usa a **mediana** do preço unitário das compras
multiplicada pela apresentação (ex.: 30 comprimidos). Não pondera por quantidade, porque a
base tem registros com quantidades absurdas.

| Item | Código BR | Compras | Valor (mediana) | Faixa (p25-p75) | Status |
|------|-----------|---------|-----------------|-----------------|--------|
| Losartana 50 mg x30 | 268856 | 131 | R$ 1,20 | 1,05 - 1,50 | oficial (BPS) |
| Metformina 850 mg x60 | 267691 | 127 | R$ 7,50 | 6,48 - 9,00 | oficial (BPS) |
| Omeprazol 20 mg x28 | 267712 | 110 | R$ 1,68 | 1,40 - 2,24 | oficial (BPS) |
| Salbutamol aerossol | 294887 | 81 | R$ 12,23 | 10,28 - 14,25 | oficial (BPS) |
| Insulina NPH frasco | 271157 | 10 | R$ 30,40 | 24,00 - 41,70 | amostra pequena |
| Adalimumabe 40 mg | 290058 | 12 | R$ 1.838,10 | 641,15 - 3.533,00 | preços muito dispersos |

Um item só fica `validado` se tiver pelo menos 30 compras e `p75 <= 3 x p25`.

Os dados desta versão vieram de uma consolidação pública de terceiros
([brunobriani-hub/analise_dados_BPS](https://github.com/brunobriani-hub/analise_dados_BPS)),
que só limpa texto e converte tipos (removeu 19 linhas idênticas). Para usar a fonte
oficial, baixe os zips anuais em [dadosabertos.saude.gov.br/dataset/bps](https://dadosabertos.saude.gov.br/dataset/bps)
e rode:

```bash
python3 scripts/importar_bps.py 2024_csv.zip 2025_csv.zip 2026_csv.zip
```

### O que ainda falta validar

- **Antirretrovirais:** compra centralizada pelo Ministério, não aparecem no BPS.
- **Vacina:** financiada pelo PNI, sem procedimento no SIGTAP.
- **Custo real** de consulta básica, odontologia, SAMU, UPA, parto, cesárea, UTI e catarata
  (o SIGTAP traz só o repasse federal): usar SIOPS ou dados dos estados.
- **Preços "particular":** todos são estimativas; a fonte oficial é a lista da CMED (Anvisa).

## Ideias para evoluir

- Importar a tabela SIGTAP inteira e permitir escolher qualquer procedimento
- Mais medicamentos do BPS e da RENAME
- Comparar por estado/município (SIOPS)
- Compartilhar resultado como imagem
