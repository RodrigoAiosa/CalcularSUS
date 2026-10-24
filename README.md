# CalcularSUS

Calculadora que mostra quanto custam os principais atendimentos e medicamentos do SUS.
Na porta o paciente não paga, mas a conta é paga por todos através dos impostos.

**Stack:** Python (Flask) como API serverless + HTML/JS estático, hospedado na Vercel.

## Estrutura

```
CalcularSUS/
├── api/
│   ├── index.py      # API Flask (rotas /api/*)
│   └── dados.py      # itens, categorias, parâmetros e fontes
├── public/
│   └── index.html    # interface
├── requirements.txt
└── vercel.json       # rewrite /api/* -> função Python
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
| `GET/POST /api/calcular` | Calcula. Parâmetros: `item_id`, `quantidade`, `renda_mensal`, `carga_pct`, `parcela_saude_pct` |

Exemplo:

```
/api/calcular?item_id=consulta_basica&quantidade=4&renda_mensal=3000
```

## Como o cálculo funciona

- **Custo total** = custo do item × quantidade
- **Impostos que você paga por ano** = renda mensal × 12 × carga tributária
- **Parte que vai para a saúde** = impostos × % aplicado em saúde
- **Cobertura** = parte da saúde ÷ custo total do uso

## Dados: o que já está validado e o que falta

Premissas macro (conferidas em fontes públicas, ver `api/dados.py`):
- Carga tributária de 32,4% do PIB em 2025
- Gasto público per capita em saúde: R$ 1.398,53/ano (2019, CFM/Siops)
- PLOA 2026: R$ 245,6 bi para saúde na União
- ~12% dos tributos em saúde: **aproximação derivada**, editável na interface

**Os valores por item (consulta, exames, medicamentos...) são estimativas** e estão
marcados com `"validado": False`. Antes de divulgar, confira cada um no
[SIGTAP](https://sigtap.datasus.gov.br) e no [BPS](https://bps.saude.gov.br) e
troque para `True`, preenchendo o campo `fonte`.

## Ideias para evoluir

- Importar a tabela SIGTAP inteira (CSV do DATASUS) em vez de itens manuais
- Separar "valor de repasse do SUS" de "custo real" por item
- Comparar por estado/município (SIOPS)
- Compartilhar resultado como imagem
