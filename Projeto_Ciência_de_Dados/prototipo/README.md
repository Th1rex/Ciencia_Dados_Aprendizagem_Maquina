# Protótipo: escolha de oficinas mecânicas (CRISP-DM)

> ⚠️ **Protótipo com DADOS SIMULADOS.** Nenhum registro representa oficina, cliente ou avaliação real.
> Ele existe para provar que o pipeline completo funciona (ETL → estatística → modelos → dashboard) antes da coleta dos dados reais.
> Os resultados validam o **método**. Eles **não** são evidência do comportamento real de clientes.

**Pergunta principal:** os clientes escolhem a oficina mais pela nota, pela distância ou pelo preço?
**Subpergunta:** quais características separam as oficinas mais bem avaliadas das demais?

---

## Como rodar

Os comandos precisam ser executados **de dentro da pasta `prototipo`**. No Windows (PowerShell), a partir da pasta do repositório clonado:

```powershell
cd (Get-ChildItem -Directory "Projeto_Ci*").FullName   # entra em Projeto_Ciência_de_Dados (evita digitar o acento)
cd prototipo
pip install -r requirements.txt
python src\executar_tudo.py              # gera dados, trata, modela e grava resultados/
python -m streamlit run dashboard\app.py # abre a dashboard em http://localhost:8501
```

A dashboard só funciona enquanto o último comando estiver rodando. Fechar o PowerShell (ou apertar Ctrl+C) derruba o `localhost:8501`.

Tudo usa a semente `42`: com as mesmas versões das bibliotecas, rodar de novo produz os mesmos números.

## Estrutura

```text
prototipo/
├── data/
│   ├── raw/          oficinas_brutas.csv, clientes_brutos.csv, escolhas_brutas.csv, parametros_simulacao.json
│   └── processed/    oficinas_tratadas.csv, escolhas_modelagem.csv, oficinas.db (SQLite)
├── src/
│   ├── gerar_dados.py     Fase 2: gera a base simulada (com "sujeira" proposital)
│   ├── preparacao.py      Fase 3: limpeza, outliers, atributos, SQLite
│   ├── analise.py         Fases 4-5: estatística, logit condicional, ML, clusters, SQL
│   └── executar_tudo.py   roda as etapas em ordem
├── sql/consultas.sql      consultas de demonstração (KPIs, ranking, funções de janela)
├── dashboard/app.py       Fase 6: dashboard Streamlit em 5 abas
└── resultados/resultados.json
```

---

## CRISP-DM aplicado

### 1. Entendimento do negócio

- **Problema:** o cliente compara várias oficinas antes de escolher. Queremos saber qual fator pesa mais.
- **Hipóteses:** H1 nota maior → mais escolha · H2 menor distância → mais escolha · H3 preço menor → mais escolha · H4 nº de avaliações funciona como sinal de confiança · H5 oficinas bem avaliadas têm perfil diferente.
- **Critério de sucesso do protótipo:** o pipeline precisa **recuperar os parâmetros** usados na simulação, com sinal certo, ordem certa e valor dentro do IC 95%. Se recuperar, o método está pronto para a base real.

### 2. Entendimento dos dados: fontes avaliadas

| Fonte | Tipo | Uso no projeto |
|---|---|---|
| IQA/Ipsos (2026), via Portal da Autopeça. Cerca de 400 entrevistas nacionais | Pesquisa de percepção | **Ancoragem dos parâmetros.** Confiança 33%, qualidade 17%, garantia 17%, preço 8%. Tipos: independentes 53%, concessionárias 20%, centros automotivos 17% |
| Maia et al. (2021), *Inova+ Cadernos de Graduação* (FIEPR). Estudo de caso Jeff Car (Divinópolis/MG) | Estudo de caso qualitativo (Matriz GUT, 5W2H), sem amostra de clientes | Contexto: problemas de atendimento e tempo de espera. **Não fornece dados** |
| Muritiba-BA (ResearchGate) | Avaliação de qualidade de serviço em 1 oficina | **NÃO LIDO:** ResearchGate e Academia.edu bloquearam o acesso. Pendente: baixar o PDF manualmente e avaliar |
| Moysés (2024), *O papel da qualidade para melhoria da competitividade…* (IQA) | Artigo de opinião, sem dados | Contexto teórico: qualidade como investimento e base da confiança do consumidor. Não cita oficinas |
| Moysés (2024), *A qualidade como pilar para a sustentabilidade…* (IQA) | Artigo de opinião sobre ESG/ISO | **Sem relação** com escolha de oficina. Sugestão: remover das referências |
| Moysés (2023), *A busca pela excelência…* (IQA) | Artigo de opinião sobre indústria/montadoras, sem dados | Contexto geral do setor. Relevância baixa |
| IBM (2015), *IBM SPSS Modeler CRISP-DM Guide* | Metodologia | Estrutura do projeto e lista de entregáveis por fase (ver "Entregáveis CRISP-DM") |

**Conclusão importante:** das 6 referências do projeto, 5 foram lidas, e nenhuma traz dados por oficina nem uma variável observada de "cliente escolheu a oficina X". A de Muritiba não pôde ser lida. Por isso o protótipo usa simulação, e só a pesquisa IQA/Ipsos foi usada para calibrar os pesos. A pesquisa **não mede distância**, então o peso da distância é uma **suposição** do protótipo.

### Desenho da base simulada

- **1.200 oficinas** em 15 regiões administrativas do DF, com nota, nº de avaliações, preço médio da revisão, nº de serviços, anos de funcionamento, garantia estendida e tipo.
- **2.000 clientes**. Cada um compara **8 oficinas** sorteadas entre as 30 mais próximas que têm pelo menos 1 avaliação, e escolhe 1. São **16.000 linhas** de pares cliente × oficina.
- A escolha segue um logit multinomial: `utilidade = 1,10·nota − 0,85·distância + 0,45·log(avaliações) + 0,40·garantia − 0,30·log(preço) + erro`, com as variáveis padronizadas.
- Uma qualidade latente, que não é observada, gera ao mesmo tempo nota, garantia e tempo de mercado. É isso que cria diferenças reais entre oficinas bem e mal avaliadas para a subpergunta.

### Dicionário de dados (oficinas_tratadas.csv)

| Variável | Tipo | Descrição | Tratamento |
|---|---|---|---|
| id_oficina | texto | Identificador `OF0001…` | 12 duplicatas removidas |
| regiao / estado | texto | Região administrativa / UF (DF) | Grafia padronizada (50 casos) |
| latitude, longitude | decimal | Localização simulada | — |
| tipo | categoria | Independente, Concessionária, Centro automotivo, Especializada | — |
| nota | decimal 1–5 | Nota média | 5 valores impossíveis corrigidos (45 → 4,5). 15 ausentes mantidos (oficina sem avaliação) |
| quantidade_avaliacoes | inteiro | Nº de avaliações | Outliers sinalizados (IQR), não removidos |
| preco_medio | R$ | Preço médio de uma revisão básica | 8 textos "R$ 1.234,56" convertidos. 24 ausentes imputados pela mediana do tipo (`preco_imputado=1`) |
| quantidade_servicos | inteiro | Nº de serviços oferecidos | — |
| anos_funcionamento | decimal | Tempo de mercado | 3 negativos corrigidos (erro de sinal) |
| garantia_estendida | 0/1 | Oferece garantia além da legal | — |
| nota_ajustada | decimal | Média bayesiana: puxa notas com poucas avaliações para a média | Atributo criado |
| grupo_avaliacao | categoria | Alta (≥ Q3 da nota), Baixa (≤ Q1), Intermediária, Poucas avaliações (< 10) | Atributo criado |
| outlier_* | 0/1 | Sinalização IQR | Atributo criado |

Em `escolhas_modelagem.csv` entram também `id_cliente`, `distancia_km` (linha reta × 1,3) e `escolhida` (0/1).

### 3. Preparação

Todo tratamento fica registrado em `resultados.json` → `log_tratamento` e aparece na aba 5 da dashboard. Os outliers foram **mantidos**: são valores plausíveis, como oficina com muitas avaliações ou concessionária cara, e os modelos usam log e métodos robustos.

### 4. Modelagem

| Técnica | Para quê | Por que essa |
|---|---|---|
| Spearman | Correlações | Variáveis assimétricas, relação não necessariamente linear |
| **Logit condicional** | **Pergunta principal** | Cada cliente escolhe 1 entre 8. O modelo compara a escolhida com as preteridas **do mesmo cliente**. Regressão linear ou logística comum ignoraria esse agrupamento |
| Reg. Logística, Árvore, Random Forest, Gradient Boosting | Prever a oficina escolhida | Comparação de modelos, com divisão treino/teste **por cliente** |
| Permutation importance | Ranking de variáveis | Funciona para qualquer modelo. Confere o resultado do logit por outro caminho |
| Mann-Whitney / qui-quadrado + árvore rasa | Subpergunta | Comparar alta avaliação × demais e extrair regras legíveis |
| K-Means + PCA | Grupos naturais | k escolhido pela silhueta |

**PySpark:** não foi usado. Com 16 mil linhas o pandas resolve em segundos, e usar Spark aqui seria artificial. Ele faz sentido na versão com dados reais, se a coleta passar de milhões de linhas, por exemplo avaliações individuais.
**Orange:** os CSVs de `data/processed/` abrem direto no Orange (widgets File → Logistic Regression / Random Forest → Test & Score) para repetir a comparação de modelos visualmente.

### 5. Avaliação: resultados do protótipo

**Recuperação de parâmetros (logit condicional, pseudo-R² de McFadden = 0,275):**

| Variável | Estimado | Usado na simulação |
|---|---|---|
| Nota | +1,04 | +1,10 |
| Distância | −0,93 | −0,85 |
| Nº de avaliações (log) | +0,49 | +0,45 |
| Garantia estendida | +0,40 | +0,40 |
| Preço (log) | −0,29 | −0,30 |
| Anos / nº de serviços | ≈ 0 (p > 0,2) | 0 |

O método recuperou sinal e ordem de todos os parâmetros, e o valor usado na simulação ficou dentro do IC 95% em todas as 7 variáveis, incluindo as duas neutras (anos e nº de serviços), para as quais não inventou efeito. **Critério de sucesso atingido.**

**Modelos supervisionados (teste com 500 clientes):** Regressão Logística ROC-AUC 0,78, acerto top-1 de 43% (acaso: 12,5%). Gradient Boosting 0,78 / 41%. Random Forest 0,77 / 39%. Árvore 0,75 / 37%. O modelo mais simples ganhou, o que faz sentido porque os dados foram gerados por um modelo logístico.

**Ordem do trio:** nota > distância > preço, nos dois métodos.

**Subpergunta:** as oficinas de alta avaliação têm mais avaliações (mediana 56,5 × 35), mais garantia estendida (61% × 32%), mais tempo de mercado (12 × 10 anos) e preço **maior** (R$ 568 × R$ 500). O nº de serviços não difere.

**Clusters:** a melhor silhueta foi k=2, com valor 0,22, que é **fraco**. O K-Means separou basicamente quem oferece garantia de quem não oferece.

### 6. Implantação

A implantação é a dashboard Streamlit em 5 abas: visão geral, comportamento, comparação, modelagem e conclusão. Ela tem KPIs, filtros (região, tipo, preço, nota, avaliações, distância) e a seção "O que os dados mostram?".

### Entregáveis CRISP-DM (guia IBM) × protótipo

| Fase | Entregável exigido pelo guia | Situação |
|---|---|---|
| 1. Negócio | Critérios de sucesso **de negócio** | ⚠️ Falta: definir quem usa a resposta (ex.: dono de oficina decidindo entre investir em reputação ou baixar preço) |
| 1. Negócio | Critérios de sucesso **de mineração** | ✅ Recuperação de parâmetros + top-1 acima do acaso |
| 1. Negócio | Inventário de recursos, riscos e contingências | ⚠️ Falta: risco principal é não conseguir dado real de escolha; contingência é o alvo substituto |
| 2. Dados | Relatórios de coleta, descrição, exploração e qualidade | ✅ Parcial: dicionário, `log_tratamento` e abas 1-2. Falta o relatório de coleta da base real |
| 3. Preparação | Relatório de limpeza e decisões de inclusão/exclusão | ✅ `log_tratamento`. Exclusão de oficinas com menos de 10 avaliações dos grupos está justificada |
| 4. Modelagem | Design de teste, premissas, parâmetros, modelos | ✅ Divisão por cliente, semente 42, parâmetros no código |
| 5. Avaliação | Avaliação frente aos critérios de negócio e revisão do processo | ⚠️ Falta a revisão do processo (o que deu errado ou poderia ser melhor) |
| 6. Implantação | Plano de implantação, de monitoramento e manutenção, relatório final | ⚠️ Dashboard pronta. Faltam o plano de monitoramento (ex.: recoletar notas a cada 6 meses e reajustar) e o relatório final |

---

## Limitações (ler antes de apresentar)

1. **Circularidade:** a ordem nota > distância > preço foi **colocada** na simulação. Apresentar isso como descoberta sobre clientes reais é metodologicamente inválido. O que dá para afirmar é: *"o método recupera corretamente os fatores quando eles existem"*.
2. **Escolha observada não existe em fontes públicas.** Plataformas mostram nota e avaliações, mas não quem comparou quais oficinas. Com dados reais há dois caminhos:
   - **Pesquisa de escolha** (questionário com cenários: "oficina A nota 4,8 a 5 km por R$ 600 × oficina B…"). Esse caminho mantém o logit condicional e responde de fato à pergunta.
   - **Proxy de procura:** usar nº de avaliações como alvo, coletando nota, avaliações e localização no Google Maps. Esse caminho responde "o que se associa a mais procura", não "o que faz o cliente escolher", e isso precisa estar escrito.
3. **Associação ≠ causa.** Mesmo com dados reais, nota alta pode ser consequência de mais clientes.
4. **Viés de sobrevivência e seleção:** só entram oficinas com presença digital.
5. **Preço** foi modelado como uma revisão padrão. Na prática varia por serviço e por carro.

## Como trocar pelos dados reais

1. Coloque os arquivos reais em `data/raw/` com as mesmas colunas (`oficinas_brutas.csv`, `clientes_brutos.csv`, `escolhas_brutas.csv`) e apague `parametros_simulacao.json`.
2. Rode `python src\executar_tudo.py --dados-reais`. Essa opção pula a geração de dados simulados.
3. Revise os textos da dashboard que falam em "dados simulados" e "valor usado na simulação". Com base real, os losangos de comparação somem do gráfico de coeficientes.

Se a base real não tiver `escolhas_brutas.csv` (escolha observada), a análise da pergunta principal precisa mudar para o alvo substituto (ver Limitações, item 2). Isso exige alterar `analise.py`.

## Referências

- IQA; IPSOS. *Confiança pesa mais que preço na escolha da oficina mecânica.* Portal da Autopeça, 14 out. 2026. https://portaldaautopeca.com.br/noticias/local/confianca-pesa-mais-que-preco-na-escolha-da-oficina-mecanica-confirma-pesquisa-iqa-ipsos/
- MAIA, D. A. da et al. Qualidade e valor para o cliente de oficinas mecânicas autorizadas: um estudo de caso na Jeff Car. *Inova+ Cadernos de Graduação*, v. 1, n. 2, p. 108-126, 2021. https://app.fiepr.org.br/revistacientifica/index.php/inovamais/article/download/508/492
- Avaliação da Qualidade do Serviço em uma Oficina Mecânica Automotiva da Cidade de Muritiba-BA. https://www.researchgate.net/publication/355932639 (**referência incompleta:** autores, ano e periódico não verificados, pois o texto não pôde ser acessado)
- MOYSÉS, C. O papel da qualidade para melhoria da competitividade no setor automotivo nacional. IQA, 2 ago. 2024. https://www.iqa.org.br/imprensa/o-papel-da-qualidade-para-melhoria-da-competitividade-no-setor-automotivo-nacional-por-claudio-moyses/
- MOYSÉS, C. A qualidade como pilar para a sustentabilidade no setor automotivo. IQA, 1 mar. 2024. https://www.iqa.org.br/imprensa/a-qualidade-como-pilar-para-a-sustentabilidade-no-setor-automotivo-por-claudio-moyses/
- MOYSÉS, C. A busca pela excelência: a qualidade automotiva no Brasil e o cenário global. IQA, 23 ago. 2023. https://www.iqa.org.br/imprensa/a-busca-pela-excelencia-a-qualidade-automotiva-no-brasil-e-o-cenario-global-por-claudio-moyses/
- IBM. *IBM SPSS Modeler CRISP-DM Guide* (versão 17.0). IBM Corporation, 2015. https://public.dhe.ibm.com/software/analytics/spss/documentation/modeler/17.0FP1/en/ModelerCRISPDM.pdf (a versão em português indicada no projeto, https://www.ibm.com/docs/pt-br/SS3RA7_18.5.0/nl/pt/BR/pdf/ModelerCRISPDM.pdf, não abriu na consulta)
