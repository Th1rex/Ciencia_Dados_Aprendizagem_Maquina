![][image1]

**TEMPLATE** 

**Definição do Projeto** 

**de Ciência de Dados** 

**Unidade III \- Gestão de Projetos** 

**Equipe** 

**Turma** 

**Professor(a)** 

**Data** 

**PBL \+ trabalho em equipes** 

Defina um problema real, o público-alvo, os objetivos e as perguntas de negócio antes de iniciar a análise.  
**Unidade:** III \- Gestão de Projetos 

**Metodologia:** PBL \+ trabalho em equipes 

**Entregável:** Documento de definição do projeto 

**Finalidade:** delimitar um problema real e orientar o desenvolvimento do projeto de Ciência de Dados.  Preencha todos os campos com informações objetivas, verificáveis e coerentes entre si. 

**1\. Identificação do projeto** 

| Campo  | Preenchimento |
| :---- | :---- |
| Título provisório do projeto | TechMotors: análise de preços, demanda e avaliações em uma plataforma de agendamento de serviços mecânicos |
| Curso / disciplina | Sistemas de Informação / Ciência de Dados e Aprendizagem de Máquina |
| Turma | Sistemas de Informação |
| Equipe | Thiago Regis Vieira Rocha \| Eduardo Santos Morais |
| Integrantes e funções iniciais | Thiago Regis Vieira Rocha – Gestor de Projeto e Analista de Dados \| Eduardo Santos Morais – Desenvolvedor Full Stack e Engenharia de Dados |
| Professor(a) | Eliel da Silva Cruz |
| Data de elaboração | 16/09/2026 |
| Versão do documento | 0.2 |

**2\. Visão geral** 

**2.1 Resumo do projeto**   
O TechMotors é uma plataforma web de agendamento de serviços mecânicos que faz a intermediação entre clientes e oficinas aprovadas pela administração. O cliente agenda o serviço já sabendo a faixa de preço praticada (valor fixo, "a partir de" ou sob orçamento), escolhe os serviços desejados e, após a conclusão, avalia a oficina, alimentando a nota média e o ranking. A oficina recebe agenda semanal, painel de métricas com serviços agendados e receita estimada, e o administrador acompanha indicadores gerais da plataforma. Nesta disciplina, a equipe utilizará os dados gerados pela plataforma (preços, agendamentos e avaliações), complementados por dados públicos da frota de veículos, para analisar a variação de preços, os padrões de demanda e a qualidade percebida das oficinas.

**2.2 Declaração do projeto em uma frase**  
Nosso projeto utilizará **\[dados ou fonte\]** para compreender/prever **\[fenômeno\]**, apoiando **\[público ou  organização\]** na decisão de **\[decisão ou ação\]**. 

**Versão da equipe: alfa 1.0**  

Nosso projeto utilizará **os dados de preços, agendamentos e avaliações registrados na plataforma TechMotors, complementados pelos dados públicos da frota de veículos do Distrito Federal (SENATRAN)**, para compreender **a variação de preços dos serviços mecânicos básicos, a concentração da demanda e os fatores associados às melhores avaliações**, apoiando **clientes e oficinas mecânicas de pequeno e médio porte** na decisão de **escolher a oficina mais adequada e definir preços e horários de atendimento**. 

**3\. Contexto e definição do problema** 

**3.1 Contexto** 

Descreva a situação atual, o ambiente em que o problema ocorre e as evidências iniciais que demonstram sua  relevância. 

 Onde o problema ocorre? Na contratação de serviços mecânicos básicos (troca de óleo, filtros, velas, correias, alinhamento, balanceamento e freios) em oficinas de pequeno e médio porte do Distrito Federal.

 Quem é afetado? Clientes proprietários de veículos (carros e motos) e as oficinas mecânicas.

 Quais sinais, dados ou relatos indicam sua existência? Relatos de experiências com profissionais desqualificados ou de má-fé, que reforçam um estereótipo negativo sobre o setor (PALERMO; PUGLIESE, 2022); agendamento ainda feito por telefone ou WhatsApp, inclusive em redes consolidadas; e diferença de preço para o mesmo serviço entre oficinas, sem uma forma simples de comparação.

 Por que é importante investigá-lo agora? A frota brasileira chegou a cerca de 123,97 milhões de veículos registrados (SENATRAN, 2024), o que mantém alta a demanda por manutenção. Além disso, a plataforma TechMotors já está implementada e registra os dados necessários para a análise, permitindo transformar o sistema desenvolvido no TCC em uma fonte de dados para apoiar decisões.

**Preenchimento:** 

O processo de contratação de serviços automotivos básicos ainda é informal e descentralizado. O cliente depende de indicações pessoais, ligações e mensagens para descobrir quais oficinas atendem o serviço desejado, quanto cobram e se têm horário disponível, sem um meio de comparar preço e reputação antes da contratação. Do lado das oficinas, a agenda costuma ser controlada manualmente e a divulgação depende do boca a boca, o que dificulta atrair novos clientes e reduzir o tempo ocioso.

A plataforma TechMotors foi desenvolvida para centralizar esse processo e, por isso, passou a registrar dados estruturados sobre preços por oficina, serviços solicitados, datas e horários, situação dos agendamentos e avaliações dos clientes. Esses dados ainda não são analisados de forma sistemática, e é esse o espaço explorado por este projeto de Ciência de Dados.

**3.2 Problema central** 

Formule o problema de maneira específica, sem antecipar uma solução. 

**Modelo:** \[Público/organização\] enfrenta \[problema observável\] no contexto de \[situação\], produzindo  \[consequência ou impacto\]. 

**Problema definido:** 

	**Clientes que precisam de manutenção básica de veículos no Distrito Federal enfrentam a falta de informações comparáveis sobre preço, disponibilidade e qualidade das oficinas no contexto da contratação do serviço, que ainda ocorre por indicação pessoal, telefone ou mensagens, produzindo desconfiança em relação ao setor, risco de pagar valores acima da média ou por serviços desnecessários e, para as oficinas de pequeno e médio porte, dificuldade de atrair clientes, definir preços competitivos e organizar a agenda.** 

**3.3 Evidências iniciais**

| Evidência  | Fonte  | O que ela indica?  | Confiabilidade / limitação |
| :---- | :---- | :---- | ----- |
| 1\. Falta de referência sobre oficinas com serviço de qualidade | Palermo e Pugliese (2022), Revista O Mecânico | Existe um estereótipo negativo sobre o setor, associado a práticas comerciais abusivas e à dificuldade do cliente leigo de avaliar a necessidade e o preço justo do serviço | Fonte setorial e qualitativa; não mede a frequência do problema |
| 2\. Agendamento prévio ainda pouco disponível ao próprio usuário | Análise de soluções correlatas feita no TCC (JM Auto Centro, High Torque, AppBarber, Oficina SaaS) | Mesmo oficinas com presença digital encaminham o agendamento para telefone ou WhatsApp, sem confirmação automática de horário | Amostra pequena (4 soluções), observação da própria equipe |
| 3\. Variação de preços para o mesmo serviço | Catálogo de preços cadastrado na plataforma TechMotors | Na base de teste, a troca de óleo varia de R$ 70,00 (valor fixo) a R$ 95,00 ("a partir de") entre três oficinas | Os dados atuais são fictícios (base de teste); a evidência precisa ser confirmada com preços reais de oficinas do DF |

**4\. Público-alvo e partes interessadas** 

**4.1 Público-alvo principal** 

| Aspecto  | Descrição |
| :---- | :---- |
| Quem são os usuários ou beneficiários? | Clientes proprietários de veículos (carros e motos) do Distrito Federal que contratam serviços de manutenção básica |
| Quais necessidades possuem? | Atendimento mais eficiente e agendado, transparência sobre preços e referências confiáveis sobre a qualidade das oficinas |
| Como são afetados pelo problema? | Com demora no atendimento, má qualidade do serviço e insegurança sobre o valor cobrado |
| Que decisão ou ação poderão tomar com os resultados? | Escolher oficinas com base em preço, avaliação e disponibilidade, e avaliar positivamente os locais com boa qualidade de serviço |

**4.2 Partes interessadas** 

| Parte interessada  | Interesse no projeto  | Influência  | Forma de envolvimento |
| :---- | :---- | :---- | :---- |
| Oficinas mecânicas parceiras | Entender a demanda por serviço e horário, posicionar o preço em relação às demais e melhorar a reputação | Alta | Fornecem os dados de preços, disponibilidade e atendimentos por meio da plataforma; recebem os indicadores no painel |
| Clientes da plataforma | Comparar oficinas por preço e qualidade antes de agendar | Média | Geram os dados de agendamento e avaliação; respondem ao questionário de validação |
| Administrador da plataforma TechMotors | Monitorar a qualidade das oficinas, aprovar cadastros e moderar avaliações | Média | Acompanha os indicadores consolidados no painel administrativo |
| Professor da disciplina (Eliel da Silva Cruz) | Avaliar a aplicação do ciclo de Ciência de Dados a um problema real | Alta | Valida a definição do projeto e avalia os entregáveis |

**5\. Objetivos do projeto** 

**5.1 Objetivo geral** 

Escreva um objetivo que indique o que será analisado, para qual finalidade e em qual contexto. Inicie com um  verbo no infinitivo. 

**Objetivo geral:** 

Analisar os dados de preços, agendamentos e avaliações registrados na plataforma TechMotors, complementados pelos dados da frota de veículos do Distrito Federal, para identificar padrões de variação de preço, de demanda e de qualidade percebida que apoiem clientes na escolha de oficinas e oficinas na definição de preços e horários de atendimento.

**5.2 Objetivos específicos** 

Defina de três a cinco objetivos mensuráveis e compatíveis com o prazo do projeto. 

| Nº  | Objetivo específico  | Evidência de conclusão |
| :---- | :---- | :---- |
| 1 | Extrair, pseudonimizar e tratar os dados das tabelas de oficinas, serviços oferecidos, agendamentos e avaliações da plataforma | Base tratada em CSV, sem dados pessoais, com dicionário de dados e relatório de inconsistências corrigidas |
| 2 | Medir a variação de preço de cada serviço do catálogo entre oficinas, por modalidade de preço e por região administrativa | Tabela com mínimo, máximo, mediana e coeficiente de variação por serviço, e gráfico comparativo |
| 3 | Identificar os serviços, dias da semana e faixas de horário com maior demanda | Mapa de calor de agendamentos por dia e horário e ranking de serviços mais solicitados |
| 4 | Verificar a associação entre o comportamento da oficina (taxa de recusa, cancelamento e conclusão) e a nota média recebida | Teste de correlação documentado, com resultado e limitações descritos no relatório |
| 5 | Disponibilizar os principais indicadores em um painel e validar sua utilidade com potenciais usuários | Painel publicado e questionário respondido por pelo menos 5 potenciais usuários (clientes ou oficinas) |

**5.3 Verificação dos objetivos** 

Marque após revisar: 

☐ São específicos e escritos com clareza. 

☐ Podem ser verificados por meio de entregáveis ou métricas. 

☐ São viáveis com os dados, recursos e tempo disponíveis. 

☐ Estão diretamente relacionados ao problema central. 

☐ Consideram os usuários e a decisão que será apoiada. 

**6\. Perguntas de negócio** 

As perguntas de negócio orientam a coleta, a análise e a comunicação dos resultados. Evite perguntas que  possam ser respondidas apenas com "sim" ou "não". 

| Nº  | Pergunta de negócio  | Decisão apoiada  | Dados necessários  | Análise ou indicador possível |
| :---- | ----- | :---- | :---- | :---- |
| 1 | Quanto varia o preço de um mesmo serviço entre as oficinas e em quais serviços essa variação é maior? | Cliente: escolher a oficina. Oficina: posicionar o próprio preço | Serviços oferecidos (preço, modalidade de preço), catálogo de serviços, bairro e cidade da oficina | Mínimo, máximo, mediana e coeficiente de variação por serviço; boxplot por serviço |
| 2 | Quais serviços, dias da semana e horários concentram mais agendamentos? | Oficina: definir a disponibilidade semanal e a equipe por turno | Agendamentos (data e hora, serviço, situação) | Contagem por serviço; mapa de calor dia × horário |
| 3 | Quais fatores estão associados às oficinas com melhor avaliação? | Cliente: confiar na nota exibida. Administrador: priorizar o acompanhamento de oficinas | Avaliações (estrelas), agendamentos por situação, preços praticados | Correlação de Spearman entre nota média e taxas de recusa, cancelamento e conclusão, e preço médio |
| 4 | Qual é a proporção de agendamentos concluídos, recusados e cancelados por oficina? | Administrador: manter ou rever o cadastro da oficina. Oficina: reduzir recusas | Agendamentos (situação, oficina, motivo do cancelamento) | Taxa de conclusão, de recusa e de cancelamento por oficina; funil solicitado → confirmado → concluído |
| 5 | Como a oferta de oficinas aprovadas se distribui em relação à frota de veículos de cada região do DF? | Administrador: definir regiões prioritárias para captar novas oficinas | Endereço e coordenadas das oficinas; frota por município ou região (SENATRAN) | Veículos por oficina aprovada em cada região; mapa da oferta |

**7\. Hipóteses iniciais**  
Registre suposições que serão investigadas, sem apresentá-las como conclusões. 

| Hipótese  | Como poderá ser testada?  | Resultado que a refutaria? |
| :---- | :---- | :---- |
| H1. Serviços com preço na modalidade "a partir de" apresentam maior variação de preço entre oficinas do que os serviços com preço fixo | Comparar o coeficiente de variação dos preços por modalidade (fixo × "a partir de") para os mesmos serviços | Coeficiente de variação igual ou menor na modalidade "a partir de" |
| H2. Oficinas com maior taxa de recusa ou de cancelamento recebem notas médias menores | Correlação de Spearman entre as taxas por oficina e a nota média, considerando apenas oficinas com número mínimo de avaliações | Correlação nula ou positiva, ou ausência de significância estatística |
| H3. A demanda se concentra nos serviços de manutenção preventiva e no período da manhã | Distribuição de frequência dos agendamentos por categoria de serviço e por faixa de horário | Distribuição uniforme entre categorias ou concentração em outro período |

**8\. Dados necessários e viabilidade** 

| Conjunto ou fonte  de dados  | Variáveis principais  | Formato  | Acesso / responsável  | Qualidade esperada |
| :---- | ----- | :---- | ----- | ----- |
| Banco de dados da plataforma TechMotors | Oficinas (bairro, cidade, coordenadas, nota média, situação de aprovação); serviços oferecidos (preço, modalidade, duração); agendamentos (data e hora, serviço, situação, valor estimado, motivo do cancelamento); avaliações (estrelas, comentário, data) | SQLite, exportado para CSV | Acesso direto ao banco do projeto / Eduardo Santos Morais (extração) | Estrutura boa (chaves e restrições de valores no banco), porém com volume baixo e inconsistências conhecidas (item 8.1) |
| Frota de veículos – SENATRAN | Quantidade de veículos por município ou UF e por tipo de veículo | CSV ou XLSX (dados abertos) | Download público / Thiago Regis Vieira Rocha | Alta (fonte oficial), porém agregada; não detalha as regiões administrativas do DF |
| Questionário com potenciais usuários | Perfil (cliente ou oficina), critérios de escolha de oficina, percepção de utilidade do painel | Google Forms, exportado para CSV | Aplicação pela equipe / Thiago Regis Vieira Rocha | Média: amostra pequena e por conveniência |

**8.1 Avaliação inicial dos dados** 

 **Disponibilidade:** o banco da plataforma está disponível para a equipe desde já; os dados do SENATRAN são públicos; o questionário será aplicado pela equipe.

 **Volume e período coberto:** a base atual é de teste e contém 5 oficinas (3 aprovadas), 10 serviços no catálogo em 6 categorias, 14 ofertas de serviço com preço, 5 agendamentos e 1 avaliação, com datas entre julho e agosto de 2026. Esse volume é insuficiente para conclusões estatísticas. A equipe usará uma base simulada, gerada por script e identificada como tal, para construir e validar o processo de análise, e substituirá por dados reais caso haja uso piloto com oficinas antes da entrega. Frota: dados do SENATRAN de 2024.

 **Dados ausentes, duplicados ou inconsistentes previstos:** preço nulo nos serviços "sob orçamento"; agendamentos com mais de um serviço registram apenas o primeiro serviço, embora a duração e o valor somem todos; nota média e total de avaliações da base de teste (ex.: 4,8 com 213 avaliações) sem registros correspondentes na tabela de avaliações; data de atualização do agendamento não registra a mudança de situação, o que impede medir o tempo de resposta da oficina; CNPJ gravado com e sem pontuação.

 **Necessidade de integração entre fontes:** cruzar a cidade e a UF das oficinas com a frota do SENATRAN; cruzar as respostas do questionário com os indicadores do painel apenas de forma agregada.

 **Restrições legais, contratuais ou institucionais:** a base contém dados pessoais (nome, CPF, e-mail, telefone e placa de veículo), sujeitos à LGPD; os dados serão usados apenas para fins acadêmicos; os dados do SENATRAN são abertos.

**8.2 Privacidade, ética e segurança** 

☐ A equipe verificou se há dados pessoais ou sensíveis. 

☐ A coleta e o uso dos dados possuem finalidade legítima e explícita. 

☐ O acesso será limitado às pessoas autorizadas. 

☐ Dados pessoais serão minimizados, anonimizados ou pseudonimizados quando necessário. ☐ Possíveis vieses e impactos sobre grupos serão analisados. 

☐ A divulgação dos resultados evitará reidentificação ou exposição indevida. 

**Cuidados específicos deste projeto:** 

A extração será feita sem as colunas de nome, CPF, e-mail, telefone, placa e foto, e os identificadores de clientes serão substituídos por códigos aleatórios. Comentários das avaliações só serão usados de forma agregada, sem citação literal que identifique o cliente. Oficinas serão identificadas por código nos resultados, salvo autorização expressa. Indicadores com menos de 5 registros não serão divulgados isoladamente, para evitar conclusões sobre oficinas com poucos dados. A base simulada será sempre identificada como simulada em gráficos e no relatório.

**9\. Escopo do projeto** 

| Dentro do escopo  | Fora do escopo |
| :---- | :---- |
| Extração, tratamento e pseudonimização dos dados da plataforma TechMotors | Processamento de pagamentos e análise de faturamento real (a plataforma não realiza transações financeiras) |
| Análise exploratória de preços, demanda, situação dos agendamentos e avaliações das oficinas do Distrito Federal | Coleta automatizada de dados de sites de terceiros (web scraping) e regiões fora do Distrito Federal |
| Painel com os indicadores e relatório final respondendo às perguntas de negócio | Modelo preditivo ou sistema de recomendação em produção dentro da plataforma (previsto como trabalho futuro) |

**Restrições conhecidas:** prazo do semestre, executado em paralelo ao TCC II (defesa em 08/12/2026); baixo volume de dados reais na plataforma; equipe de dois integrantes; banco SQLite de arquivo único; conhecimento ainda inicial da equipe em estatística inferencial.

**10\. Resultados e entregáveis previstos** 

| Entregável  | Descrição  | Formato  | Responsável  | Critério de aceite |
| ----- | :---- | :---- | :---- | :---- |
| Base tratada | Dados extraídos do banco, sem dados pessoais, com inconsistências tratadas, acompanhados de dicionário de dados | CSV + dicionário de dados (PDF ou planilha) | Eduardo Santos Morais | Nenhum dado pessoal; nenhum registro duplicado; todas as colunas descritas no dicionário |
| Análise exploratória | Estatísticas descritivas e testes das hipóteses H1 a H3 | Notebook Jupyter (Python, pandas e matplotlib) | Thiago Regis Vieira Rocha | As 5 perguntas de negócio respondidas, com gráfico e interpretação |
| Visualizações / painel | Indicadores de variação de preço, demanda e avaliação | Painel em Power BI (ou página de indicadores no painel do Administrador da plataforma) | Eduardo Santos Morais | Painel funcionando com os indicadores das perguntas 1 a 4 e filtro por serviço |
| Relatório ou   apresentação | Síntese do problema, método, resultados, limitações e recomendações | Relatório em PDF e apresentação em slides | Thiago Regis Vieira Rocha | Entregue no prazo definido pelo professor e aprovado na apresentação |
| Outro | Script de extração e pseudonimização reutilizável | Script Python | Eduardo Santos Morais | Gera a base tratada a partir do banco em uma única execução |

**11\. Critérios de sucesso** 

Defina como a equipe saberá se o projeto alcançou seus objetivos.

| Critério  | Indicador ou evidência  | Meta  | Forma de verificação |
| ----- | :---- | :---- | :---- |
| Relevância para o problema | Perguntas de negócio respondidas e ligadas a uma decisão | 5 de 5 | Revisão do relatório pela equipe e pelo professor |
| Qualidade dos dados | Percentual de campos obrigatórios preenchidos e de dados pessoais removidos | ≥ 95% de preenchimento; 0 dado pessoal na base tratada | Script de verificação aplicado à base tratada |
| Qualidade da análise | Hipóteses testadas com método, resultado e limitação descritos | 3 de 3 | Conferência do notebook e do relatório |
| Utilidade para o público alvo | Nota média de utilidade atribuída ao painel no questionário | ≥ 4 em escala de 1 a 5, com pelo menos 5 respondentes | Resultado do questionário |
| Comunicação dos   resultados | Apresentação clara dentro do tempo definido | Apresentação no tempo estabelecido pelo professor, com todas as perguntas respondidas | Avaliação do professor |

**12\. Plano inicial de trabalho** 

| Etapa  | Atividades   principais  | Responsável(is)  | Prazo  | Dependências |
| :---- | :---- | :---- | :---- | :---- |
| 1\. Definição | Revisar o problema, as perguntas de negócio e as hipóteses; validar com o professor | Thiago e Eduardo | 30/10/2026 | Aprovação deste documento |
| 2\. Obtenção dos   dados | Exportar as tabelas do banco; baixar a frota do SENATRAN; publicar o questionário | Eduardo (banco) e Thiago (SENATRAN e questionário) | 06/11/2026 | Etapa 1 |
| 3\. Preparação dos   dados | Pseudonimizar, tratar inconsistências, gerar a base simulada e o dicionário de dados | Eduardo | 13/11/2026 | Etapa 2 |
| 4\. Análise /   modelagem | Estatística descritiva, testes das hipóteses H1 a H3, cruzamento com a frota | Thiago | 24/11/2026 | Etapa 3 |
| 5\. Validação | Montar o painel; revisar os resultados; aplicar o questionário de utilidade | Eduardo (painel) e Thiago (questionário) | 01/12/2026 | Etapa 4 |
| 6\. Comunicação | Redigir o relatório e preparar a apresentação | Thiago e Eduardo | Data definida pelo professor | Etapa 5 |

**13\. Riscos do projeto** 

| Risco  | Probabilidade  | Impacto  | Estratégia de   resposta | Responsável |
| :---- | :---- | :---- | :---- | :---- |
| Volume insuficiente de dados reais para conclusões estatísticas | Alta | Alto | Usar base simulada identificada como tal para validar o método e apresentar os resultados como exploratórios; buscar uso piloto com oficinas | Thiago Regis Vieira Rocha |
| Inconsistências no modelo de dados (agendamento grava só um serviço; nota média sem avaliações correspondentes; mudança de situação sem data) | Alta | Médio | Corrigir no código antes da extração ou tratar na preparação, registrando a decisão no relatório | Eduardo Santos Morais |
| Conflito de prazo com o TCC II (defesa em 08/12/2026) | Média | Alto | Reaproveitar o banco e a documentação do TCC; manter o escopo do item 9 sem acréscimos | Thiago Regis Vieira Rocha |
| Exposição de dados pessoais (LGPD) | Baixa | Alto | Extração sem colunas pessoais e pseudonimização por script, com verificação antes de qualquer compartilhamento | Eduardo Santos Morais |

**14\. Organização da equipe** 

| Integrante  | Papel principal  | Responsabilidades  | Apoio necessário |
| :---- | :---- | :---- | :---- |
| Thiago Regis Vieira Rocha | Gestor de Projeto e Analista de Dados | Cronograma e comunicação com o professor; obtenção dos dados do SENATRAN; questionário; análise exploratória e testes das hipóteses; relatório e apresentação | Orientação do professor sobre os testes estatísticos |
| Eduardo Santos Morais | Desenvolvedor Full Stack e Engenharia de Dados | Ajustes no banco e no código da plataforma; extração e pseudonimização; base simulada; dicionário de dados; painel | Revisão dos indicadores do painel pelo gestor do projeto |

**15\. Validação da definição do projeto** 

Antes da entrega, confirme: 

☐ O problema é real, relevante e delimitado.  
☐ O público-alvo e as partes interessadas estão identificados. 

☐ O objetivo geral e os objetivos específicos são coerentes. 

☐ As perguntas de negócio orientam decisões concretas. 

☐ Há dados potencialmente disponíveis para responder às perguntas. 

☐ O escopo é compatível com o prazo e os recursos. 

☐ Os critérios de sucesso são mensuráveis. 

☐ Riscos, privacidade, ética e segurança foram considerados. 

☐ Funções e responsabilidades foram distribuídas. 

**16\. Aprovação e registro de ajustes** 

| Responsável  | Validação / observação  | Data |
| :---- | :---- | :---- |
| Representante da equipe | Eduardo e Thiago |  |
| Professor(a) / orientador(a) | Eliel da Silva Cruz  |  |

**Ajustes solicitados após a apresentação inicial** 

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ 

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

[image1]: <data:image/png;base64,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>
