Atividade Prática — Detetives dos Dados

Ciência de Dados e Aprendizagem de Máquina — Aula 01

Tema: Introdução à Ciência de Dados e Big Data
Metodologia: Trabalho em equipe
Tempo: 20 minutos
Entregável: Mapa do Problema de Ciência de Dados

---

1. Identificação da equipe

Campo| Resposta
Turma:| Sistemas de Informação
Data:| 19/08/2026
Equipe:|
Integrante 1:| Thiago Regis Vieira Rocha
Integrante 2:| Eduardo Santos Morais
Integrante 3:|
Integrante 4:|
Integrante 5:|

---

2. Objetivo da atividade

Nesta atividade, sua equipe deverá analisar um problema real e pensar como uma equipe de Ciência de Dados poderia utilizar dados para compreender a situação e apoiar uma decisão.

O objetivo não é desenvolver um sistema ou modelo de Machine Learning neste momento.

O objetivo é aprender a pensar como um cientista de dados:

«Problema → Dados → Informação → Análise → Decisão → Benefício»

---

3. Escolha do problema

Escolha uma área para investigar:

* [ ] Comércio
* [ ] Banco
* [ ] Saúde
* [ ] Transporte
* [ ] Educação
* [ ] Entretenimento
* [ ] Indústria
* [ ] Meio ambiente
* [ ] Esportes
* [x] Outra: Serviços automotivos (oficinas mecânicas)

Problema escolhido

Descreva, em poucas linhas, o problema que sua equipe pretende analisar.

«O setor de oficinas mecânicas carrega um estereótipo negativo: muitos clientes acreditam que serão enganados, seja com serviços desnecessários, seja com valores inflados. Além disso, o agendamento ainda é feito por telefone ou WhatsApp, e não existe uma forma simples de comparar preço e qualidade entre oficinas. O TechMotors busca trazer "paredes de vidro" para esse processo, usando os dados de preços, agendamentos e avaliações da plataforma para dar mais transparência ao cliente e mais informação de gestão à oficina.»

4. Quem possui esse problema?

Identifique a organização, grupo ou público afetado pelo problema.

Quem possui ou enfrenta esse problema?

«Clientes que precisam de serviços de manutenção básica para o carro ou a moto, como troca de óleo, filtros, alinhamento, balanceamento e freios, e não sabem em qual oficina confiar.»

Quem é afetado pelo problema?

«Os clientes, que sofrem com demora no atendimento, má qualidade do serviço e insegurança sobre o valor cobrado, e as oficinas de pequeno e médio porte, que têm dificuldade para atrair clientes e organizar a agenda.»

---

5. Por que esse problema é importante?

Explique por que vale a pena investigar esse problema utilizando dados.

Qual é o impacto do problema?

«A frota brasileira tem cerca de 123,97 milhões de veículos (SENATRAN, 2024), e todos precisam de manutenção. Sem informação clara, o cliente escolhe a oficina por indicação ou pelo que está mais perto, sem saber se o preço é justo ou se o serviço é de qualidade.

A utilização dos dados permite comparar preços entre oficinas, identificar quais oficinas são mais bem avaliadas e entender quais serviços e horários têm mais procura.

Dessa forma, o cliente escolhe com mais segurança, e a oficina passa a enxergar seu faturamento, seus serviços agendados e sua reputação.»

---

6. Qual decisão precisa ser tomada?

Imagine que sua equipe foi contratada para ajudar uma organização.

Qual decisão a organização precisa tomar?

«Para o cliente: em qual oficina agendar o serviço, considerando preço, avaliação e horário disponível.

Para a oficina: como ajustar seus preços e seus horários de atendimento de acordo com a demanda e com o que as outras oficinas praticam.

A decisão será baseada nas informações obtidas por meio da análise dos dados da plataforma TechMotors.»

---

7. Identificação dos dados

Agora pense:

«Quais dados seriam necessários para compreender esse problema?»

Liste pelo menos 5 dados.

Nº| Dado necessário| Por que esse dado é importante?
1| Preço de cada serviço por oficina| Permite comparar quanto cada oficina cobra pelo mesmo serviço.
2| Agendamentos (data e horário)| Permite identificar os dias e horários de maior procura.
3| Serviços solicitados| Permite identificar quais serviços são mais procurados.
4| Avaliações (estrelas e comentários)| Permite medir a qualidade percebida de cada oficina.
5| Situação do agendamento e localização da oficina| Permite ver quantos agendamentos são concluídos, recusados ou cancelados, e em quais regiões estão as oficinas.

---

8. Que informações queremos descobrir?

Os dados, quando analisados, podem gerar informações úteis.

O que sua equipe gostaria de descobrir a partir dos dados?

Pergunta 1

«Quanto o preço de um mesmo serviço varia entre as oficinas?»

Pergunta 2

«Quais serviços, dias e horários têm mais agendamentos?»

Pergunta 3

«Quais oficinas recebem as melhores avaliações e o que elas têm em comum?»

Pergunta 4

«Quantos agendamentos são concluídos, recusados ou cancelados em cada oficina?»

---

9. Quais padrões podemos procurar?

Pense como um cientista de dados.

Sua equipe poderia procurar:

* [x] Tendências
* [x] Comparações
* [ ] Grupos semelhantes
* [x] Comportamentos recorrentes
* [x] Valores fora do padrão
* [x] Relações entre variáveis
* [x] Mudanças ao longo do tempo
* [ ] Outros: __________

Explique um padrão que vocês gostariam de encontrar

«Gostaríamos de identificar serviços em que o preço varia muito de uma oficina para outra e oficinas com preços fora do padrão. Também queremos verificar se as oficinas que mais recusam ou cancelam agendamentos recebem avaliações piores, e em quais dias e horários a procura aumenta.»

---

10. Qual análise poderia ser realizada?

Como os dados poderiam ser analisados?

Marque uma ou mais possibilidades:

* [x] Análise descritiva
* [x] Comparação entre grupos
* [x] Análise temporal
* [x] Visualização por gráficos
* [x] Identificação de padrões
* [ ] Classificação
* [ ] Previsão
* [ ] Agrupamento
* [ ] Outra: __________

Explique

«Os dados podem ser analisados por meio de gráficos e comparações de preço entre oficinas para o mesmo serviço. Também é possível fazer uma análise temporal dos agendamentos por dia e horário e comparar as avaliações com a quantidade de agendamentos concluídos, recusados e cancelados. Os resultados aparecem para a oficina em um painel (dashboard) com faturamento e serviços agendados.»

---

11. Qual decisão poderia ser tomada?

Depois de analisar os dados, imagine que sua equipe encontrou informações importantes.

Que decisão poderia ser tomada com base nos resultados?

«Com base nos resultados, o cliente poderia escolher uma oficina com preço justo e boa avaliação. A oficina poderia ajustar seus preços, abrir mais horários nos períodos de maior procura e melhorar o atendimento nos pontos em que é mal avaliada.»

---

12. Qual seria o benefício?

Qual seria o possível benefício da decisão para a organização ou para as pessoas envolvidas?

«O benefício seria trazer mais transparência e confiança para a contratação de serviços mecânicos. O cliente economiza tempo e dinheiro e evita serviços desnecessários, e a oficina atrai mais clientes, organiza melhor a agenda e acompanha seu faturamento.»

---

13. Os 5 Vs do Big Data

Analise o problema escolhido pela equipe.

V| Pergunta| Resposta da equipe
Volume| Existe uma grande quantidade de dados?| Ainda não. Hoje a base tem poucos registros de teste, mas cresce a cada agendamento, preço cadastrado e avaliação.
Velocidade| Os dados são gerados ou processados rapidamente?| Sim. Os dados são gerados a cada agendamento, mudança de situação e avaliação, e o painel da oficina é atualizado na hora.
Variedade| Existem diferentes tipos ou formatos de dados?| Sim. Existem valores, datas e horários, categorias de serviço, notas, comentários em texto e localização das oficinas.
Veracidade| Os dados podem apresentar erros ou problemas de qualidade?| Sim. Preços "a partir de" ou "sob orçamento" não mostram o valor final, e avaliações podem ser injustas ou falsas.
Valor| Os dados podem gerar algum benefício ou apoiar decisões?| Sim. Os dados ajudam o cliente a escolher a oficina e a oficina a ajustar preços e horários.

Qual dos 5 Vs é mais relevante para o problema?

«Veracidade.»

Justifique

«A veracidade é a mais relevante porque o problema central é a falta de confiança no setor. Se os preços ou as avaliações exibidos na plataforma não forem confiáveis, o cliente continua sem saber em quem acreditar, e a plataforma perde o sentido.»

---

14. Mapa do Problema de Ciência de Dados

Complete o fluxo abaixo:

┌─────────────────────┐
│       PROBLEMA      │
│ Falta de confiança  │
│ e de informação ao  │
│ escolher oficina    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│        DADOS        │
│ Preços, agendamen-  │
│ tos, avaliações e   │
│ localização         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│     INFORMAÇÕES     │
│ Variação de preços, │
│ demanda e oficinas  │
│ mais bem avaliadas  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       ANÁLISE       │
│ Gráficos, compara-  │
│ ções e análise ao   │
│ longo do tempo      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       DECISÃO       │
│ Escolher a oficina; │
│ ajustar preços e    │
│ horários            │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│      BENEFÍCIO      │
│ Mais transparência  │
│ e confiança no      │
│ atendimento         │
└─────────────────────┘

Resuma cada etapa

Problema:

«Falta de confiança e de informação clara sobre preço e qualidade na hora de escolher uma oficina mecânica.»

Dados:

«Preços dos serviços por oficina, agendamentos (data, horário e situação), serviços solicitados, avaliações e localização das oficinas.»

Informação:

«Variação de preços para o mesmo serviço, serviços e horários de maior procura, oficinas mais bem avaliadas e taxa de agendamentos concluídos, recusados e cancelados.»

Análise:

«Análise descritiva, comparação entre oficinas, análise temporal e visualização por gráficos e painéis.»

Decisão:

«O cliente escolhe a oficina com preço justo e boa avaliação; a oficina ajusta preços e horários de atendimento.»

Benefício:

«Mais transparência e confiança na contratação de serviços mecânicos e melhor gestão para as oficinas.»

---

15. Preparação para apresentação

A equipe terá 2 minutos para apresentar sua proposta.

Organizem a apresentação seguindo esta estrutura:

1. Nosso problema

«Nosso problema é a falta de confiança e de informação clara sobre preço e qualidade na hora de escolher uma oficina mecânica.»

2. Precisamos destes dados

«Precisamos de dados como preços dos serviços por oficina, agendamentos, serviços solicitados, avaliações e localização das oficinas.»

3. Queremos descobrir

«Queremos descobrir quanto o preço varia entre oficinas, quais serviços e horários têm mais procura e quais oficinas são mais bem avaliadas.»

4. Pretendemos analisar

«Pretendemos analisar os dados por meio de gráficos, comparações entre oficinas e análise ao longo do tempo.»

5. A decisão poderia ser

«A decisão poderia ser o cliente escolher a oficina com melhor custo e avaliação, e a oficina ajustar seus preços e horários.»

6. O benefício esperado é

«O benefício esperado é trazer transparência para o setor, aumentar a confiança do cliente e ajudar a oficina a gerir seus serviços e seu faturamento.»

---

16. Checklist da equipe

Antes de entregar, confira:

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

17. Reflexão final

Responda individualmente ou em equipe:

«Ter muitos dados significa necessariamente tomar boas decisões? Por quê?»

Resposta:

«Não. Ter muitos dados não significa necessariamente tomar boas decisões. É preciso que os dados sejam confiáveis e que sejam organizados, analisados e interpretados corretamente. No TechMotors, mil avaliações não ajudam o cliente se forem falsas ou injustas, e preços "a partir de" não mostram o valor real do serviço. Por isso, a qualidade dos dados importa mais do que a quantidade.»

---

Entrega

Produto final

A equipe deverá entregar:

Mapa do Problema de Ciência de Dados

contendo:

Problema
   ↓
Dados necessários
   ↓
Informações desejadas
   ↓
Análise
   ↓
Decisão
   ↓
Benefício esperado

Formato sugerido: Markdown, PDF ou documento disponibilizado pelo professor.

Apresentação: 2 minutos por equipe.
