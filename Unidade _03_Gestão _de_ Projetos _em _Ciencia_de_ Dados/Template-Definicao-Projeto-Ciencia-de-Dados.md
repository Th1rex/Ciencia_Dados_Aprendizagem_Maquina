 # Template - Definição do Projeto de Ciência de Dados

**Unidade:** III - Gestão de Projetos  
**Metodologia:** PBL + trabalho em equipes  
**Entregável:** Documento de definição do projeto

> **Finalidade:** delimitar um problema real e orientar o desenvolvimento do projeto de Ciência de Dados. Preencha todos os campos com informações objetivas, verificáveis e coerentes entre si.

## 1. Identificação do projeto

| Campo | Preenchimento |
|---|---|
| Título provisório do projeto |TechMotors|
| Curso / disciplina |Ciencia de Dados e Aprendizage de Maquina|
| Turma |Sistemas de Informação|
| Equipe |Thiago Regis Vieira Rocha | Eduardo Santos Morais|
| Integrantes e funções iniciais |Thiago Regis Gestor de Projetos - Eduardo Dev FullStack|
| Professor(a) |Eliel|
| Data de elaboração |16/09|
| Versão do documento |0.1|

## 2. Visão geral

### 2.1 Resumo do projeto
Plataforma de agendamento de serviços mecânicos, fornecendo a intermediação entre o cliente e a oficina “QUALIFICADA e com boas avaliações”, o cliente pode marcar o serviço na plataforma já ciente dos possíveis valores, além da escolha personalizada do tipo do serviço, após a finalização do serviço o cliente pode avaliar a mecânica assim retornando o ranking de avaliação para mais ou menos, além disso é fornecido a mecânica os horários de agendamento, com calendário e dashboard dos seus serviços fornecidos e faturamento gerado. 

### 2.2 Declaração do projeto em uma frase
Nosso projeto utilizará os dados de avaliações, histórico de serviços e faturamento para compreender/prever a reputação das oficinas e a demanda de serviços, apoiando os motoristas na decisão de escolha do melhor prestador e as oficinas na gestão financeira e de horários.

**Versão da equipe:**
0.1
________________________________________________________________________________

## 3. Contexto e definição do problema

### 3.1 Contexto

Descreva a situação atual, o ambiente em que o problema ocorre e as evidências iniciais que demonstram sua relevância.

- Onde o problema ocorre?
   - **No ecossistema de manutenção automotiva (oficinas mecânicas e auto centers).**
- Quem é afetado?
   - **Clientes (motoristas) que sofrem com a falta de previsibilidade de preços e confiança na qualidade; e Oficinas que têm dificuldades na gestão de agenda e retenção de clientes.**
- Quais sinais, dados ou relatos indicam sua existência?
    - **A ociosidade de horários nas oficinas, o alto volume de orçamentos informais via aplicativos de mensagens sem conversão em serviços, e a dificuldade relatada por clientes em encontrar mecânicos de confiança fora de seu círculo social.**
- Por que é importante investigá-lo agora?
   - **A digitalização de serviços tradicionais é uma demanda crescente. Otimizar esse fluxo através da organização dos dados gera lucro para as oficinas e segurança para o consumidor.**


________________________________________________________________________________

### 3.2 Problema central

Clientes e donos de oficinas enfrentam a falta de transparência em orçamentos, dificuldade na validação da qualidade técnica e má gestão de agendas no contexto de manutenção automotiva preventiva e corretiva, produzindo perda de tempo, imprevisibilidade financeira e ociosidade operacional.
### 3.3 Evidências iniciais

| Evidência | Fonte | O que ela indica? | Confiabilidade / limitação |
|---|---|---|---|
| Variação excessiva de preços para o mesmo serviço. |Pesquisa de mercado / Relatos de clientes.|Assimetria de informações no mercado automotivo.|Alta / Limitada à região de pesquisa.|
| Horários ociosos ao longo da semana nas oficinas. |Observação direta / Entrevistas com mecânicos.|Má distribuição e controle de agendamentos.|Média / Depende do porte da oficina.|

## 4. Público-alvo e partes interessadas

### 4.1 Público-alvo principal

| Aspecto | Descrição |
|---|---|
| Quem são os usuários ou beneficiários? | Motoristas pessoa física e gestores de oficinas mecânicas. |
| Quais necessidades possuem? | Motoristas precisam de previsibilidade de preço e confiança técnica. Oficinas precisam de organização de fluxo e visibilidade de faturamento. |
| Como são afetados pelo problema? | Gastam tempo excessivo cotando serviços ou gerenciando agendas manualmente. |
| Que decisão ou ação poderão tomar com os resultados? | Clientes: Qual oficina escolher baseada no ranking. Oficinas: Quais dias/horários precisam de promoções ou realocação de equipe (baseado no dashboard). |

### 4.2 Partes interessadas

| Parte interessada | Interesse no projeto | Influência | Forma de envolvimento |
|---|---|---|---|
| Equipe de Desenvolvimento (Eduardo e Thiago) | Alta | Baixa / Média / Alta | Execução técnica e gestão |
| Professor(a) Eliel | Alta | Alta | Avaliação e direcionamento acadêmico |
| Oficinas parceiras | Média | Média | Fornecimento de requisitos de negócio e testes de usabilidade |

## 5. Objetivos do projeto

### 5.1 Objetivo geral

Escreva um objetivo que indique o que será analisado, para qual finalidade e em qual contexto. Inicie com um verbo no infinitivo.

Desenvolver e analisar a base de dados transacional da plataforma TechMotors para estruturar um sistema de ranqueamento de oficinas e gerar dashboards analíticos que otimizem a tomada de decisão tanto do cliente final quanto do prestador de serviço.

________________________________________________________________________________

### 5.2 Objetivos específicos

Defina de três a cinco objetivos mensuráveis e compatíveis com o prazo do projeto.

| Nº | Objetivo específico | Evidência de conclusão |
|---:|---|---|
| 1 | Estruturar a coleta e o armazenamento de dados estruturados (agendamentos, avaliações, serviços). | Banco de dados (MySQL) populado com dados iniciais ou simulados. |
| 2 | Desenvolver uma métrica (score) de ranqueamento para as oficinas com base nas avaliações dos usuários. | Algoritmo de ranking implementado e listando as oficinas ordenadamente. |
| 3 | Criar visualizações analíticas (dashboards) focadas em faturamento e ocupação de agenda. | Telas de dashboard integradas ao sistema web para visão do mecânico. |


### 5.3 Verificação dos objetivos

Marque após revisar:

- [ ] São específicos e escritos com clareza.
- [ ] Podem ser verificados por meio de entregáveis ou métricas.
- [ ] São viáveis com os dados, recursos e tempo disponíveis.
- [ ] Estão diretamente relacionados ao problema central.
- [ ] Consideram os usuários e a decisão que será apoiada.

## 6. Perguntas de negócio

As perguntas de negócio orientam a coleta, a análise e a comunicação dos resultados. Evite perguntas que possam ser respondidas apenas com “sim” ou “não”.

| Nº | Pergunta de negócio | Decisão apoiada | Dados necessários | Análise ou indicador possível |
|---:|---|---|---|---|
| 1 | Quais são as oficinas com as melhores taxas de avaliação e por quê? | Escolha da oficina pelo cliente. | Notas de avaliação (1 a 5), comentários, tipo de serviço realizado. | Média ponderada de avaliações (Ranking). |
| 2 | Qual é a sazonalidade e os dias de pico de agendamentos? | Alocação de mecânicos na oficina. | Data e hora do serviço agendado, status de conclusão. | Gráfico de linha/barras de volume de atendimentos por dia da semana. |
| 3 | Qual é o ticket médio dos serviços prestados por categoria? | Planejamento financeiro da oficina. | Valores cobrados, categorias de serviço. | Ticket médio (R$) consolidado no dashboard. |

## 7. Hipóteses iniciais

Registre suposições que serão investigadas, sem apresentá-las como conclusões.

| Hipótese | Como poderá ser testada? | Resultado que a refutaria? |
|---|---|---|
| H1. Oficinas com ranking de avaliação superior a 4.0 recebem no mínimo 40% mais agendamentos via plataforma. | Correlacionando a nota média da oficina com o volume de agendamentos mensais. | A distribuição de agendamentos se mostrar aleatória ou uniforme independente da nota. |
| H2. A exibição prévia de estimativa de valor aumenta a taxa de conclusão dos agendamentos. | Comparando a taxa de cancelamento (no-show) de serviços com valores expostos previamente vs. serviços com valor a definir. | A taxa de abandono ser igual ou maior nos serviços com estimativa de valor. |

## 8. Dados necessários e viabilidade

| Conjunto ou fonte de dados | Variáveis principais | Formato | Acesso / responsável | Qualidade esperada |
|---|---|---|---|---|
| Banco de Dados TechMotors | id_agendamento, id_oficina, data_hora, valor, status | SQL (MySQL/SQLite) | Eduardo (Dev) | Alta (dados estruturados e tipados na aplicação) |
| Tabela de Avaliações | id_avaliacao, id_oficina, nota, comentario | SQL | Eduardo (Dev) | Alta |

### 8.1 Avaliação inicial dos dados

- **Disponibilidade:**
  - Dados gerados pelo próprio uso e simulação na aplicação web (backend em Node.js/PHP).
- **Volume e período coberto:**
  - Histórico desde a ativação dos primeiros clientes teste no sistema.
- **Dados ausentes, duplicados ou inconsistentes previstos:**
- **Necessidade de integração entre fontes:** 
- **Restrições legais, contratuais ou institucionais:**
  - Necessidade de adequação à LGPD devido ao armazenamento de dados de usuários (placas de veículos, nomes, contatos).

### 8.2 Privacidade, ética e segurança

- [X] A equipe verificou se há dados pessoais ou sensíveis.
- [X] A coleta e o uso dos dados possuem finalidade legítima e explícita.
- [ ] O acesso será limitado às pessoas autorizadas.
- [X] Dados pessoais serão minimizados, anonimizados ou pseudonimizados quando necessário.
- [ ] Possíveis vieses e impactos sobre grupos serão analisados.
- [ ] A divulgação dos resultados evitará reidentificação ou exposição indevida.

**Cuidados específicos deste projeto:**
 - Senhas criptografadas no banco, e não exposição de dados de contato do cliente abertamente no ranking público das oficinas.
________________________________________________________________________________

## 9. Escopo do projeto

| Dentro do escopo | Fora do escopo |
|---|---|
| Construção da base de dados relacional. | Processamento real de pagamentos e transações financeiras (gateways de pagamento). |
| Desenvolvimento de dashboards interativos de faturamento e agendamentos. | Uso de IA preditiva avançada (ex: visão computacional para detectar falhas no carro). |
| Criação do algoritmo de ranqueamento de oficinas. | |


**Restrições conhecidas:** tempo, acesso a dados, ferramentas, infraestrutura, conhecimento técnico ou normas.

________________________________________________________________________________

## 10. Resultados e entregáveis previstos

| Entregável | Descrição | Formato | Responsável | Critério de aceite |
|---|---|---|---|---|
| Base tratada | | | | |
| Análise exploratória | | | | |
| Visualizações / painel | | | | |
| Relatório ou apresentação | | | | |
| Outro | | | | |

## 11. Critérios de sucesso

Defina como a equipe saberá se o projeto alcançou seus objetivos.

| Critério | Indicador ou evidência | Meta | Forma de verificação |
|---|---|---|---|
| Relevância para o problema | | | |
| Qualidade dos dados | | | |
| Qualidade da análise | Cálculo de avaliações. | O sistema deve refletir em tempo real (ou próximo) a mudança de nota da oficina assim que uma nova avaliação for registrada. | |
| Utilidade para o público-alvo | Navegação na tela de agendamento e leitura do painel de métricas. | O fluxo de agendamento e visualização de faturamento deve ocorrer sem erros no sistema (CRUD completo). | |
| Comunicação dos resultados | | | |

## 12. Plano inicial de trabalho

| Etapa | Atividades principais | Responsável(is) | Prazo | Dependências |
|---|---|---|---|---|
| 1. Definição | Preenchimento deste documento de escopo e arquitetura. | Thiago | Imediato | N/A |
| 2. Obtenção dos dados\Preparação dos dados  | Criação das tabelas no MySQL/SQLite e geração de dados mockados para testes. | Eduardo | Curto prazo | Etapa 1 |
| 3. Análise / modelagem | Desenvolver as lógicas de ranking e métricas financeiras (Backend/SQL). | Eduardo | | Etapa 2 |
| 4. Validação | Testes de integração entre o painel, agendamentos e base de dados. | Thiago / Eduardo | Médio prazo | Etapa 3 |
| 5. Comunicação | Apresentação final dos Dashboards e funcionamento do portal na disciplina. | Equipe | Fim do semestre | Etapa 4 |

## 13. Riscos do projeto

| Risco | Probabilidade | Impacto | Estratégia de resposta | Responsável |
|---|---|---|---|---|
| Atraso na integração Front e Back-end. | Alto | Utilizar frameworks ágeis e focar primeiro no fluxo essencial (MVP). | Thiago/Eduardo |
| Baixo volume de dados mockados limitando o dashboard. | Baixa | Médio | Criar scripts (ex: Python/Node.js) para popular o banco com dezenas de registros fictícios de agendamentos. | Eduardo |

## 14. Organização da equipe

| Integrante | Papel principal | Responsabilidades | Apoio necessário |
|---|---|---|---|
| Thiago Regis | Gestor de Projetos | Organizar o fluxo de trabalho, documentação (TCC/Relatórios), e validação de requisitos de negócio. | Alinhamento contínuo com os professores. |
| Eduardo Santos | Dev FullStack | Modelagem do banco (MySQL/SQLite), desenvolvimento do Backend (Node.js/PHP) e estruturação do frontend (HTML/CSS/JS/TS). | Definição clara de telas e métricas por parte da gestão. |


## 15. Validação da definição do projeto

Antes da entrega, confirme:

- [x] O problema é real, relevante e delimitado.
- [x] O público-alvo e as partes interessadas estão identificados.
- [x] O objetivo geral e os objetivos específicos são coerentes.
- [x] As perguntas de negócio orientam decisões concretas.
- [x] Há dados potencialmente disponíveis para responder às perguntas.
- [x] O escopo é compatível com o prazo e os recursos.
- [x] Os critérios de sucesso são mensuráveis.
- [x] Riscos, privacidade, ética e segurança foram considerados.
- [x] Funções e responsabilidades foram distribuídas.

## 16. Aprovação e registro de ajustes

| Responsável | Validação / observação | Data |
|---|---|---|
| Representante da equipe | | |
| Professor(a) / orientador(a) | | |

### Ajustes solicitados após a apresentação inicial

________________________________________________________________________________

________________________________________________________________________________
