# Protótipo: código, dados e dashboard

Esta é a parte técnica do projeto. A visão geral, a identificação da equipe e o passo a passo de instalação estão no [README do projeto](../README.md). O relatório CRISP-DM completo está em [`docs/documentacao.md`](../docs/documentacao.md).

> ⚠️ **Dados simulados.** Nenhum registro representa oficina, cliente ou avaliação real.

## Executar (PowerShell, dentro desta pasta)

```powershell
python -m pip install -r requirements.txt
python src\executar_tudo.py               # gera dados, trata, modela e cria figuras
python -m streamlit run dashboard\app.py  # dashboard em http://localhost:8501
```

A semente é `42`. Com as mesmas versões das bibliotecas, rodar de novo produz os mesmos números.

## Estrutura

```text
prototipo/
├── data/
│   ├── raw/          oficinas_brutas.csv, clientes_brutos.csv, escolhas_brutas.csv, parametros_simulacao.json
│   └── processed/    oficinas_tratadas.csv, escolhas_modelagem.csv, oficinas.db (SQLite)
├── src/
│   ├── gerar_dados.py     gera a base simulada (com "sujeira" proposital para o ETL)
│   ├── preparacao.py      limpeza, outliers, atributos novos e SQLite
│   ├── analise.py         estatística, logit condicional, ML, clusters, SQL, hipóteses e ranking
│   ├── gerar_figuras.py   figuras PNG usadas no documento
│   └── executar_tudo.py   roda as etapas em ordem
├── sql/consultas.sql      consultas de demonstração (KPIs, ranking, funções de janela)
├── dashboard/app.py       dashboard Streamlit em 5 abas
└── resultados/
    ├── resultados.json    todos os números (lidos pela dashboard)
    └── figuras/           fig1 a fig6
```

## Pipeline

| Etapa | Script | Entrada | Saída |
|---|---|---|---|
| 1. Simulação | `gerar_dados.py` | parâmetros no código | `data/raw/*` |
| 2. Preparação | `preparacao.py` | `data/raw/*` | `data/processed/*` e log de tratamento |
| 3. Análise | `analise.py` + `sql/consultas.sql` | `data/processed/*` | `resultados/resultados.json` |
| 4. Figuras | `gerar_figuras.py` | `resultados.json` | `resultados/figuras/*.png` |
| 5. Dashboard | `dashboard/app.py` | `data/processed/*` + `resultados.json` | interface web |

## Dicionário de dados

### `oficinas_tratadas.csv` (1.200 linhas, 1 por oficina)

| Variável | Tipo | Descrição | Tratamento aplicado |
|---|---|---|---|
| id_oficina | texto | Identificador `OF0001…` | 12 duplicatas removidas |
| nome_oficina | texto | Nome fictício | — |
| regiao / estado | texto | Região administrativa / UF (DF) | Grafia padronizada (50 casos) |
| latitude, longitude | decimal | Localização simulada | — |
| tipo | categoria | Independente, Concessionária, Centro automotivo, Especializada | — |
| nota | decimal 1–5 | Nota média | 5 valores impossíveis corrigidos (45 → 4,5). 15 ausentes mantidos (oficina sem avaliação) |
| quantidade_avaliacoes | inteiro | Nº de avaliações | Outliers sinalizados (IQR), não removidos |
| preco_medio | R$ | Preço médio de uma revisão básica | 8 textos "R$ 1.234,56" convertidos. 24 ausentes imputados pela mediana do tipo |
| preco_imputado | 0/1 | 1 = preço veio da imputação | Atributo criado |
| quantidade_servicos | inteiro | Nº de serviços oferecidos | — |
| anos_funcionamento | decimal | Tempo de mercado | 3 negativos corrigidos (erro de sinal) |
| garantia_estendida | 0/1 | Oferece garantia além da legal | — |
| log_avaliacoes, log_preco | decimal | Logaritmo das variáveis assimétricas | Atributo criado |
| nota_ajustada | decimal | Média bayesiana `(n·nota + m·média)/(n + m)`, com m = mediana de avaliações | Atributo criado |
| faixa_preco | categoria | Quartil de preço | Atributo criado |
| grupo_avaliacao | categoria | Alta (nota ≥ 4,6), Baixa (≤ 4,0), Intermediária e Poucas avaliações (menos de 10) | Atributo criado |
| outlier_* | 0/1 | Sinalização IQR por variável | Atributo criado |

### `escolhas_modelagem.csv` (16.000 linhas, 1 por par cliente × oficina comparada)

Tem todas as colunas acima, mais `id_cliente`, `distancia_km` (linha reta × 1,3), `faixa_distancia` e `escolhida` (1 = oficina escolhida pelo cliente, 0 = preterida).

### SQLite `oficinas.db`

Tabelas `oficinas`, `clientes` e `escolhas`, ligadas por `id_oficina` e `id_cliente`. As consultas estão em `sql/consultas.sql`.

## Usar dados reais

1. Coloque os arquivos reais em `data/raw/` com as mesmas colunas e apague `parametros_simulacao.json`.
2. Rode `python src\executar_tudo.py --dados-reais`. Essa opção pula a simulação.
3. Revise na dashboard os textos que falam em "dados simulados".

Se não houver `escolhas_brutas.csv` (escolha observada), a pergunta principal precisa de outro alvo, e isso exige alterar `analise.py`. As opções estão na seção 15 do documento.
