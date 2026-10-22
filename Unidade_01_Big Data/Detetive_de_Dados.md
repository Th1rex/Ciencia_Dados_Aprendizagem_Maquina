19/08

# Atividade Prática — Detetives dos Dados

## Ciência de Dados e Aprendizagem de Máquina — Aula 01

**Tema:** Introdução à Ciência de Dados e Big Data
**Metodologia:** Trabalho em equipe
**Tempo:** 20 minutos
**Entregável:** Mapa do Problema de Ciência de Dados

---

## 1. Identificação da equipe

| Campo             | Resposta |
| ----------------- | -------- |
| **Turma:**        | SI 7/8 Noturno |
| **Data:**         | 19/08/2026 |
| **Equipe:**       |  |
| **Integrante 1:** | Rafael Batista Mota |
| **Integrante 2:** | Thiago Regis Vieira Rocha |
| **Integrante 3:** | Gabriel Landim Donadel de Farias |
| **Integrante 4:** | Eduardo Santos Morais |
| **Integrante 5:** | -- |
| **Integrante 6:** | -- |

---

## 2. Objetivo da atividade

Nesta atividade, sua equipe deverá analisar um **problema real** e pensar como uma equipe de Ciência de Dados poderia utilizar dados para compreender a situação e apoiar uma decisão.

O objetivo não é desenvolver um sistema ou modelo de Machine Learning neste momento.

O objetivo é aprender a **pensar como um cientista de dados**:

> **Problema → Dados → Informação → Análise → Decisão → Benefício**

---

## 3. Escolha do problema

Área escolhida:

* [x] Comércio
* [ ] Banco
* [ ] Saúde
* [ ] Transporte
* [ ] Educação
* [ ] Entretenimento
* [ ] Indústria
* [ ] Meio ambiente
* [ ] Esportes
* [ ] Outra: __________________________

### Problema escolhido

**Descreva, em poucas linhas, o problema que sua equipe pretende analisar.**

> Uma loja de roupas de shopping está acumulando muita mercadoria no estoque que não vende, gerando prejuízo e ocupando espaço que poderia ser usado para produtos novos.
---

## 4. Quem possui esse problema?

**Quem possui ou enfrenta esse problema?**

> Os gestores e o setor de compras/estoque da loja de roupas.

### Quem é afetado pelo problema?

> A empresa (que perde dinheiro com capital parado) e os clientes (que encontram menos variedade de novidades na arara).

---

## 5. Por que esse problema é importante?

**Qual é o impacto do problema?**

> O impacto financeiro e operacional é severo. Manter mercadorias paradas gera custos de armazenagem, depreciação acelerada do produto (roupa sai de moda rápido), risco de perdas por avaria e, principalmente, custo de oportunidade, já que o dinheiro investido naqueles itens parados poderia estar alocado em coleções novas e de alta demanda. Investigar isso com dados permite estancar o sangramento financeiro e otimizar a saúde do caixa da empresa

---

## 6. Qual decisão precisa ser tomada?

**Qual decisão a organização precisa tomar?**

> A organização precisa decidir qual seria a media ideal de produtos (quantidades) deve ser encomendado para as próximas coleções, além de definir estratégias dinâmicas de preço para escoar o estoque atual parado de forma a recuperar o máximo de valor possível sem prejudicar a marca
---

# 7. Identificação dos dados

| Nº | Dado necessário | Por que esse dado é importante? |
| -: | --------------- | ------------------------------- |
| 1 | Histórico de vendas | Mostra quais produtos venderam mais rápido e quais encalharam |
| 2 | Data/Horário das compras | Ajuda a identificar picos de movimento e sazonalidade |
| 3 | Valores (Custo e Preço) | Permite calcular a margem de lucro real de cada item |
| 4 | Tamanhos e Cores | Indica se o problema de encalhe está concentrado em numerações específicas |
| 5 | Tempo de permanência no estoque | Revela exatamente há quantos dias o produto está parado na loja |

---

# 8. Que informações queremos descobrir?

### Pergunta 1

> Quais categorias de vestuário e faixas de preço apresentam a maior taxa de encalhe após 90 dias da chegada a loja?

### Pergunta 2

> Existe algum desbalanceamento na grade de tamanhos (por exemplo, compramos muito o tamanho GG e falta o M)?

### Pergunta 3

> Qual é o impacto financeiro mensal gerado pelo custo de oportunidade e pela armazenagem dos produtos parados?

### Pergunta 4

> Qual é o período exato do ano em que as vendas desaceleram a ponto de transformar mercadorias normais em estoque encalhado?

---

# 9. Quais padrões podemos procurar?

* [x] Tendências
* [x] Comparações
* [x] Grupos semelhantes
* [x] Comportamentos recorrentes
* [x] Valores fora do padrão
* [x] Relações entre variáveis
* [x] Mudanças ao longo do tempo
* [ ] Outros: __________________________

### Explique um padrão que vocês gostariam de encontrar

> Queremos buscar comportamentos recorrentes e correlações temporais, como a tendência de que roupas de cores específicas ou tecidos mais pesados lancem raízes no estoque sempre que chegam após o pico do inverno. Identificar esse padrão comportamental no consumo do cliente impede que o erro de compra se repita no ciclo seguinte

---

# 10. Qual análise poderia ser realizada?

* [x] Análise descritiva
* [x] Comparação entre grupos
* [x] Análise temporal
* [x] Visualização por gráficos
* [x] Identificação de padrões
* [ ] Classificação
* [ ] Previsão
* [ ] Agrupamento
* [ ] Outra: __________________________

### Explique

> A análise descritiva será usada para consolidar o volume de vendas e o tempo de estoque. Faremos uma comparação entre grupos de produtos e aplicaremos análise temporal para plotar gráficos de linha mostrando o fluxo de saída ao longo dos meses. Isso permitirá agrupar os itens em quadrantes de desempenho.

---

# 11. Qual decisão poderia ser tomada?

> Com base nos insights gerados pela análise de dados, a diretoria comercial poderá cortar em até 40% os pedidos futuros de aquisição dos modelos e fornecedores com histórico de baixo giro, redirecionando esse orçamento para linhas de produtos validadas pelo público. Paralelamente, decidir por uma estratégia de liquidação segmentada acelerará a recuperação do capital investido.

---

# 12. Qual seria o benefício?

> Os benefícios diretos incluem a recuperação expressiva de capital de giro, a liberação de espaço físico precioso no centro de distribuição e nas lojas para receber coleções altamente lucrativas, a redução drástica de custos com perdas e inventário obsoleto, e o aumento geral da margem de lucro operacional da empresa

---

# 13. Os 5 Vs do Big Data

| V              | Pergunta                                                   | Resposta da equipe                                               |
| -------------- | ---------------------------------------------------------- | -----------------------------------------------------------------|
| **Volume**     | Existe uma grande quantidade de dados?                     | Sim, milhares de registros de vendas e notas fiscais de estoque. |
| **Velocidade** | Os dados são gerados ou processados rapidamente?           | Sim, a cada venda no caixa o sistema atualiza o estoque na hora. |
| **Variedade**  | Existem diferentes tipos ou formatos de dados?             | Sim.                                                             |
| **Veracidade** | Os dados podem apresentar erros ou problemas de qualidade? | Sim, produtos podem ser cadastrados com códigos errados ou dar baixa incorreta no sistema. |
| **Valor**      | Os dados podem gerar algum benefício ou apoiar decisões?   | Sim, evitam compras erradas e prejuízos financeiros. |

### Qual dos 5 Vs é mais relevante para o problema?

> Valor.

### Justifique

> Embora o volume e a velocidade sejam importantes, o propósito central de analisar os dados de estoque não é apenas lidar com grandes massas de informação, mas sim extrair valor acionável — ou seja, transformar números frios em decisões estratégicas que protejam a margem de lucro da empresa e otimizem o negócio.

---

# 14. Mapa do Problema de Ciência de Dados

```text
┌─────────────────────┐
│       PROBLEMA      │
│  Alta evasão de     │
│  alunos no noturno  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│        DADOS        │
│ Frequência, notas,  │
│ financeiro, AVA,    │
│ perfil socioecon.   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│     INFORMAÇÕES     │
│ Fatores e perfis    │
│ associados à        │
│ desistência         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       ANÁLISE       │
│ Descritiva, temporal│
│ agrupamento e       │
│ previsão de risco   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       DECISÃO       │
│ Programa de retenção│
│ direcionado por     │
│ perfil de risco     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│      BENEFÍCIO      │
│ Menos evasão, mais  │
│ formados e recursos │
│ bem aplicados       │
└─────────────────────┘
```

### Resuma cada etapa

**Problema:**

> Excesso de roupas encalhadas no estoque da loja gerando prejuízo

**Dados:**

> Histórico de vendas, tempo no estoque, preços, tamanhos e cores.

**Informação:**

> Quais modelos, cores e tamanhos específicos ficam mais tempo parados e geram mais custo

**Análise:**

> Cruzamento de dados de tempo de estoque com volume de vendas através de gráficos.

**Decisão:**

> Diminuir compras futuras dos itens problemáticos e liquidar o estoque atual.

**Benefício:**

> Redução de prejuízos e liberação de capital de giro para mercadorias populares.

---

# 15. Preparação para apresentação

### 1. Nosso problema

> O alto volume de roupas paradas no estoque de uma loja de comércio.

### 2. Precisamos destes dados

> Histórico de vendas, tempo de permanência no estoque, preços e tamanhos dos produtos.

### 3. Queremos descobrir

> Quais modelos e numerações específicas passam mais tempo encalhados e qual é o custo real desse capital parado para a empresa.

### 4. Pretendemos analisar

> Utilizar análises descritivas e temporais com gráficos de desempenho para agrupar e classificar os produtos problemáticos.

### 5. A decisão poderia ser

> Cortar os pedidos futuros dos itens de baixo desempenho junto aos fornecedores e liquidar de forma inteligente o estoque atual.

### 6. O benefício esperado é

> Recuperar o dinheiro investido, abrir espaço para mercadorias que realmente vendem e aumentar a lucratividade do negócio.

---

# 16. Checklist da equipe

* [x] Definimos um problema real.
* [x] Identificamos quem é afetado pelo problema.
* [x] Explicamos por que o problema é importante.
* [x] Identificamos pelo menos 5 dados necessários.
* [x] Definimos perguntas que queremos responder.
* [x] Identificamos possíveis padrões.
* [x] Indicamos como os dados poderiam ser analisados.
* [x] Definimos uma possível decisão.
* [x] Identificamos o benefício esperado.
* [x] Analisamos os 5 Vs do Big Data.
* [x] Preenchemos o Mapa do Problema.
* [x] Estamos preparados para apresentar em 2 minutos.

---

# 17. Reflexão final

> **Ter muitos dados significa necessariamente tomar boas decisões? Por quê?**

**Resposta:**

> Não, ter um grande volume de dados não significa de forma alguma tomar boas decisões automaticamente. Acumular terabytes de informações sem uma governança adequada gera apenas acúmulo de ruído, o que especialistas chamam de "obesidade de dados". Para que uma decisão seja sólida, os dados precisam passar por um processo rigoroso de limpeza, validação, cruzamento e interpretação inteligente. Sem o pensamento crítico humano e o direcionamento analítico correto, uma grande quantidade de dados pode apenas nos fazer tomar decisões erradas com muito mais velocidade e confiança.

---

## Entrega

### Produto final

**Mapa do Problema de Ciência de Dados**

```text
Problema: evasão de alunos no ensino superior noturno
   ↓
Dados necessários: frequência, notas, financeiro, AVA, perfil socioeconômico
   ↓
Informações desejadas: fatores, perfis e sinais de risco de evasão
   ↓
Análise: descritiva, temporal, agrupamento e previsão de risco
   ↓
Decisão: programa de retenção direcionado por perfil
   ↓
Benefício esperado: menos evasão, mais formados, recursos bem aplicados
```

**Formato:** Markdown.
**Apresentação:** 2 minutos por equipe.
