# TechMotors – Análise de Dados com CRISP-DM

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SEU-USUARIO/TechMotors-CRISP-DM-Analysis/blob/main/notebooks/pratica_crispdm_techmotors.ipynb)

Parte prática do trabalho de **Ciência de Dados e Aprendizagem de Máquina (A1)**, com a Profa. Kadidja Valéria, no Centro Universitário do Distrito Federal (UDF). O projeto aplica as seis fases do **CRISP-DM** ao **TechMotors**, plataforma web de agendamento de manutenção automotiva desenvolvida no nosso TCC. O objetivo é segmentar os perfis de manutenção dos proprietários para recomendar pacotes preventivos e prever o risco de não comparecimento (*no-show*) nos agendamentos.

O repositório reúne uma análise em **SQL** (validações de qualidade e KPIs), um **notebook em Python (Google Colab)** com diagrama de dispersão com regressão linear e modelagem (K-means e classificadores com validação temporal), além de um **dashboard** de três páginas feito em Python (Pandas, Matplotlib e Seaborn) no lugar do Power BI.

> **Dados simulados.** A plataforma TechMotors ainda não possui histórico em produção. A base foi gerada pelo notebook com **1.000 agendamentos** e a mesma estrutura relacional do TCC (`Cliente`, `Oficina`, `TipoServico`, `CanalAgendamento` e `Agendamento`), incluindo regras de negócio como a ausência de bot automático de confirmação via WhatsApp nas oficinas do Plano Básico. Também foram inseridos erros de qualidade propositais. Os números demonstram o método e **não são resultados do sistema em produção**.

## Perguntas de análise

| Pergunta | Responsável | Técnica | Resposta (dados simulados) |
|---|---|---|---|
| **P1.** Quais perfis de manutenção existem entre os proprietários e qual pacote recomendar a cada um? | Eduardo Santos Morais | K-means e regras "perfil → pacote" | 3 perfis (Preventivo / Clube Tech, Uso Moderado, Corretivo / Alta Km), silhueta 0,34 |
| **P2.** É possível prever se um agendamento resultará em não comparecimento (*no-show*)? | Thiago Regis Vieira Rocha | Regressão logística, árvore de decisão e Random Forest | Sim nas Oficinas Pro (recall 0,82); nas Oficinas Básicas o recall cai para 0,36 por falta de confirmação via WhatsApp |

## Dados

Base bruta em `techmotors_data/`, de 2 jan. a 30 dez. 2026, com 12 agendamentos datados de 2027 (erro proposital).

| Tabela | Linhas | Conteúdo |
|---|---:|---|
| `agendamento` | 1.000 | Cada agendamento: cliente, oficina, serviço, canal, data, antecedência, valor, confirmação WhatsApp e *no-show* |
| `cliente` | 250 | Proprietário (e-mail fictício), idade, plano de fidelidade, ano/km do veículo e pontuação |
| `oficina` | 8 | Oficinas parceiras no DF, região, capacidade de boxes e plano (`pro` ou `basico`) |
| `tipo_servico` | 6 | Serviços automotivos, categoria (`Preventiva` ou `Corretiva`) e valor base |
| `canal_agendamento` | 4 | App TechMotors, Site Web, WhatsApp Bot e Telefone/Balcão |

Tabelas geradas pelo notebook em `techmotors_data/processed/`: `base_analitica` (988 linhas × 22 colunas após limpeza), `regressao_dispersao`, `perfis_kmeans`, `metricas_modelos`, `recall_por_plano` e `saida_job_semanal` (perfil, pacote recomendado e alerta de confirmação de cada cliente).

## Principais resultados

| Resultado | Valor | Fonte |
|---|---|---|
| Campos nulos em `valorEstimado` / `confirmouWhatsapp` | 18 / 14 | SQL V1 |
| Valores não positivos (`valorEstimado <= 0`) / `kmAtual < 0` | 6 / 4 | SQL V2 |
| Agendamentos com data futura (2027) | 12 (removidos) | SQL V3 |
| Veículos com ano impossível (`anoVeiculo = 2099`) | 5 (corrigidos) | SQL V4 |
| Prováveis erros de digitação (> 10× mediana do serviço) | 15 (corrigidos ÷ 100) | SQL V5 |
| Agendamentos de Oficinas Básicas sem confirmação WhatsApp | 301 de 341 (88,3%) | SQL V6 |
| Volume previsto / receita realizada / perda por *no-show* | R$ 882,0 mil / R$ 574,1 mil / R$ 307,8 mil | SQL KPI 1 |
| Maior serviço em volume financeiro estimado | Revisão Geral (R$ 215,4 mil · 24,4%) | SQL KPI 3 |
| Principal canal digital de agendamento | App TechMotors (37,7%) | SQL KPI 4 |
| Taxa de *no-show* geral (base limpa) | 30,2% | SQL KPI 1 |
| Manutenção preventiva: < 250 pts × ≥ 550 pts de fidelidade | 25,4% × 87,6% | SQL consulta B |
| Regressão linear custo médio × quilometragem (todos os clientes) | custo = 8,37 × km(mil) + 236 · R² = 0,76 | Notebook, seção 3.5 |
| Inclinação da reta: Plano Padrão × Clube Tech | 7,85 (R² 0,83) × 4,08 (R² 0,49) | Notebook, seção 3.5 |
| Perfis de manutenção (K-means, k = 3, silhueta 0,34, ARI 0,90) | Preventivo 108 · Moderado 79 · Corretivo 63 | Notebook, Fase 4 |
| Melhor modelo para *no-show* (Random Forest) | Recall 0,72 · Precisão 0,67 · F1 0,69 · AUC 0,80 | Notebook, Fase 4 |
| Recall do Random Forest: Oficina Básica × Oficina Pro | 0,36 × 0,82 | Notebook, Fase 5 |
| Clientes com alerta ativo de confirmação no job semanal | 87 de 250 | Notebook, Fase 6 |

**Observações:**
- **A ausência do bot de WhatsApp nas Oficinas Básicas distorce o sinal preditivo.** 88,3% dos agendamentos do plano Básico não possuem registro de confirmação ativa, derrubando o recall do modelo de 0,82 (Oficina Pro) para 0,36 (Oficina Básica). Esta é a "nova pergunta" revelada na Fase 5 que realimenta as Fases 2 e 3 do CRISP-DM.
- **A manutenção preventiva desacelera o custo por quilometragem.** No diagrama de dispersão (seção 3.5), o custo médio no plano Padrão cresce quase 2× mais rápido por mil km rodados (R$ 7,85 vs. R$ 4,08 no Clube Tech).
- **Todos os quatro critérios técnicos da Fase 1 foram atingidos:** silhueta > 0,25 (0,34), menor cluster ≥ 5% (25,2%), recall ≥ 0,70 (0,72 no Random Forest e 0,76 na Regressão Logística) e F1 muito superior ao modelo base (0,69 vs. 0,30).

## SQL

`techmotors.sql` (PostgreSQL / DuckDB) contém:
- **Tabelas:** criação das 5 tabelas e comandos `\copy` para carregar os CSVs.
- **V1–V6:** validações de qualidade da base bruta.
- **`agendamento_limpo`:** view com a base limpa (Fase 3).
- **KPI 1–KPI 7:** volume financeiro, receita realizada, perda por *no-show*, canais digitais, sazonalidade mensal, *no-show* por plano e ticket médio por fidelidade.
- **Consultas de apoio A e B:** visão agregada por cliente e validação da hipótese H3.

Para executar sem instalar PostgreSQL: `python scripts/rodar_sql_duckdb.py`.  
`TechMotors_Analysis.pdf` (18 páginas) traz a capa, cada consulta SQL colorida com sua tabela de resultado logo abaixo e a página final.

## Notebook (Google Colab)

`notebooks/pratica_crispdm_techmotors.ipynb` percorre as seis fases do CRISP-DM de ponta a ponta e roda diretamente no Google Colab (**Ambiente de execução → Executar tudo**).

## Dashboard

Gerado pelo próprio notebook em Python (`Pandas` + `Matplotlib` + `Seaborn`) e salvo em `Dashboard/`:

**Página 1 – Visão geral operacional:**
![Visão geral operacional](Dashboard/01_visao_geral.png)

**Página 2 – Perfis de manutenção e previsão de No-Show:**
![Perfis e modelos](Dashboard/02_modelos.png)

**Página 3 – Diagrama de dispersão (quilometragem × custo médio):**
![Diagrama de dispersão](Dashboard/03_dispersao_km_custo.png)

## Estrutura

```
├── Dashboard/                 páginas do dashboard (PNG), geradas pelo notebook com Seaborn
├── techmotors_data/           base simulada de 1.000 agendamentos (CSV)
│   └── processed/             tabelas geradas pelo notebook
├── notebooks/                 notebook CRISP-DM pronto para o Google Colab
├── scripts/                   execução do SQL no DuckDB e gerador do PDF das consultas
├── techmotors.sql             validações V1–V6, view limpa, KPIs 1–7 e consultas A e B
├── TechMotors_Analysis.pdf    relatório visual de todas as consultas SQL com resultados
├── requirements.txt
└── README.md
```

## Autores

- Eduardo Santos Morais – Pergunta 1 (perfis de manutenção e recomendação de pacotes)
- Thiago Regis Vieira Rocha – Pergunta 2 (previsão de *no-show* em agendamentos)

## Sobre

Projeto-base: TCC *TechMotors: plataforma web de agendamento de manutenção automotiva* (UDF, 2026). Metodologia: CRISP-DM (Chapman et al., 2000), seguindo o guia da disciplina.
