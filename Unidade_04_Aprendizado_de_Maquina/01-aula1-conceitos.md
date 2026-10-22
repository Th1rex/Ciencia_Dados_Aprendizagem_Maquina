<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Aula 1 — Conceitos e classificação de problemas

## Identificação

- Estudante ou equipe: Thiago Regis Vieira Rocha
- Turma: Sistemas de Informação
- Data de realização: 20/10/2026
- Integrantes e contribuições (se em equipe): Thiago Regis Vieira Rocha

## Objetivos

Distinguir programação tradicional e Machine Learning, identificar atributos e alvo e diferenciar classificação, regressão e agrupamento.

## 1. Explicação com suas palavras

1. **Como um modelo aprende com dados?**  
   O modelo recebe exemplos históricos, cada um descrito por atributos e, quando existe, pela resposta correta (alvo). O algoritmo de treino ajusta os parâmetros internos do modelo para que as previsões fiquem o mais próximas possível das respostas reais, reduzindo o erro a cada ajuste. Depois do treino, o modelo aplica os padrões que encontrou a dados novos que nunca viu. A diferença para a programação tradicional é que lá o programador escreve as regras; em Machine Learning as regras são inferidas a partir dos dados.

2. **Qual diferença entre algoritmo e modelo?**  
   O algoritmo é o procedimento de aprendizado, a "receita" genérica, como árvore de decisão, regressão linear ou k-means. O modelo é o resultado de executar esse algoritmo sobre um conjunto de dados específico: ele carrega os parâmetros aprendidos e é o que efetivamente faz as previsões. O mesmo algoritmo treinado com dados diferentes gera modelos diferentes.

3. **Compare uma regra de bloqueio de palavra com um modelo de spam.**  
   A regra de bloqueio é programação tradicional: alguém define manualmente algo como "se a mensagem contém 'grátis', bloquear". Ela é simples e fácil de explicar, mas é rígida: bloqueia mensagens legítimas que usam a palavra (falso positivo), é burlada com variações como "gr4tis" e exige manutenção manual a cada novo golpe. O modelo de spam aprende, a partir de mensagens já rotuladas como spam ou legítima, combinações de vários sinais ao mesmo tempo (palavras, remetente, quantidade de links, horário) e devolve uma probabilidade. Ele generaliza melhor e pode ser retreinado com exemplos novos, mas depende de dados rotulados de qualidade e é mais difícil de explicar do que uma regra.

4. **Dê um exemplo de atributo e alvo e defina o momento da previsão.**  
   Na previsão de evasão de alunos, os atributos podem ser frequência nas aulas, notas do primeiro bimestre e número de acessos ao ambiente virtual. O alvo é a situação ao fim do semestre: evadiu ou permaneceu. O momento da previsão é o fim do primeiro bimestre, quando ainda dá tempo de intervir. Por isso, o modelo só pode usar informações disponíveis até esse momento; usar a nota final, por exemplo, seria vazamento de dados, porque essa informação não existe na hora em que a previsão precisa ser feita.

## 2. Quadro comparativo

| Critério | Supervisionado | Não supervisionado |
| --- | --- | --- |
| Presença de alvo no treino | Sim. Cada exemplo de treino traz a resposta conhecida (rótulo). | Não. Os dados têm apenas atributos, sem resposta associada. |
| Pergunta que pode responder | "Qual é a classe ou o valor deste novo caso?" Ex.: este cliente vai pagar? Quanto vamos vender? | "Que padrões ou grupos existem nos dados? O que foge do normal?" |
| Tipo de saída | Uma categoria (classificação) ou um número (regressão). | Grupos, estruturas, pontuação de anomalia ou representação reduzida dos dados. |
| Tarefas e exemplo | Classificação (spam/legítima) e regressão (tempo de espera em minutos). | Agrupamento (perfis de compra), detecção de anomalias e redução de dimensionalidade. |
| Dados necessários | Histórico com atributos e alvo rotulado, em quantidade e qualidade suficientes. | Atributos relevantes e comparáveis entre si (geralmente normalizados), sem necessidade de rótulo. |
| Forma de avaliação | Comparação das previsões com as respostas reais em dados de teste separados: acurácia, precisão, recall e F1 (classificação); MAE, RMSE e R² (regressão). | Sem gabarito: métricas internas, como silhueta e inércia, mais interpretação e validação por especialistas do negócio. |
| Limitação | Rotular é caro e demorado; rótulos errados ou enviesados são aprendidos; o modelo tem dificuldade com situações ausentes do histórico. | Resultado difícil de validar; os grupos podem não ter significado prático; depende de escolhas do analista (número de grupos, variáveis, escala). |

## 3. Situações-problema

Os casos são cenários didáticos. Escolha **pelo menos cinco** e justifique sua classificação pelo significado do alvo ou por sua ausência.

| Caso | Situação-problema |
| --- | --- |
| 1 Educação | Prever evadiu/permaneceu com histórico rotulado de turmas anteriores. |
| 2 Saúde | Estimar o tempo de espera em minutos a partir de registros de atendimento. |
| 3 Comércio | Descobrir perfis de compra sem categorias prévias de clientes. |
| 4 Finanças | Prever inadimplente/adimplente com contratos e desfechos conhecidos. |
| 5 Segurança digital | Distinguir spam/legítima com mensagens já revisadas. |
| 6 Comércio | Estimar o total de vendas em reais na próxima semana. |
| 7 Educação | Agrupar perfis de acesso ao ambiente virtual sem rótulo de evasão. |
| 8 Saúde | Classificar exames em categorias previamente definidas por especialistas. |

| Caso escolhido | Alvo ou ausência de alvo | Categoria, quantidade ou grupos? | Abordagem e justificativa | Dados necessários e limitação |
| --- | --- | --- | --- | --- |
| 3 Comércio | Ausência de alvo: não existem categorias prévias de clientes. | Grupos | Não supervisionado (agrupamento, ex.: k-means). O objetivo é descobrir perfis pela semelhança no comportamento de compra, sem rótulo para aprender. | Histórico de compras por cliente (frequência, recência, ticket médio, categorias de produto). Limitação: os grupos precisam ser interpretados por uma pessoa, o número de grupos é escolha do analista e o resultado depende das variáveis usadas. |
| 2 Saúde | Alvo: tempo de espera em minutos, já registrado nos atendimentos anteriores. | Quantidade | Supervisionado (regressão). O alvo é numérico e contínuo, e os registros históricos fornecem o valor real para o modelo aprender. | Registros com horário de chegada, dia da semana, tipo de atendimento, tamanho da fila, profissionais disponíveis e tempo de espera real. Limitação: emergências e surtos atípicos distorcem a previsão, e registros incompletos ou com horários errados prejudicam o modelo. |
| 5 Segurança digital | Alvo: rótulo spam/legítima das mensagens já revisadas. | Categoria | Supervisionado (classificação binária). Existem exemplos rotulados e a saída é uma de duas classes. | Mensagens rotuladas com texto, remetente, links e anexos. Limitação: os padrões de spam mudam com o tempo e exigem retreino, um falso positivo bloqueia mensagem legítima e as classes podem estar desbalanceadas. |
| 4 Finanças | Alvo: desfecho inadimplente/adimplente dos contratos já encerrados. | Categoria | Supervisionado (classificação). O desfecho conhecido serve de rótulo e a saída é uma classe. | Contratos com renda, valor, prazo, histórico de pagamento e desfecho. Limitação: só há dados de quem recebeu crédito (viés de seleção), o histórico pode reproduzir discriminação e os dados pessoais exigem cuidado com a LGPD. |
| 7 Educação | Ausência de alvo: não há rótulo de evasão. | Grupos | Não supervisionado (agrupamento de perfis de acesso, ex.: ativos, esporádicos, inativos). Sem rótulo, não é possível treinar um modelo para prever evasão, apenas encontrar padrões. Contrasta com o caso 1, em que o mesmo tema vira classificação porque o rótulo existe. | Logs do ambiente virtual (frequência de login, tempo online, atividades entregues, materiais acessados). Limitação: o modelo não prevê evasão diretamente, estar no grupo "inativo" não significa ter evadido e acesso não mede aprendizado. |

## 4. Raciocínio crítico

“Detectar fraude” define sozinho o tipo de aprendizado? Compare o uso de exemplos rotulados e a busca de operações atípicas sem rótulos.

Não. "Detectar fraude" é um objetivo de negócio, não um tipo de aprendizado; o que define a abordagem é o que os dados disponíveis oferecem, principalmente a existência ou não de um alvo.

Se a empresa tem um histórico de transações já marcadas como fraude ou legítima (por exemplo, após investigação ou contestação do cliente), o problema é **supervisionado de classificação**: o modelo aprende as características das fraudes conhecidas e prevê a classe de cada nova transação. A vantagem é que dá para medir o desempenho com precisão e recall comparando com os rótulos reais. As limitações são que a fraude é rara (classes muito desbalanceadas), o rótulo demora a ser confirmado e o modelo tende a não reconhecer golpes de um tipo que nunca apareceu no histórico.

Sem rótulos, o problema é **não supervisionado**, com detecção de anomalias ou agrupamento: o modelo aprende como é o comportamento normal (valores, horários, locais e frequência habituais) e sinaliza as operações que fogem desse padrão. A vantagem é conseguir apontar golpes novos sem precisar de exemplos anteriores. A limitação é que atípico não é sinônimo de fraude: uma compra alta legítima ou uma viagem ao exterior também são atípicas, o que gera falsos positivos e exige revisão humana.

Na prática, as duas abordagens costumam ser combinadas: a detecção de anomalias gera alertas, analistas revisam esses alertas, e os casos confirmados viram rótulos que depois treinam um classificador supervisionado.

## Entrega

Salve este arquivo preenchido. Critérios: distinção conceitual, pertinência dos dados, justificativa e clareza. [Voltar ao início](README.md).


## Entrega

Salve este arquivo preenchido. Critérios: distinção conceitual, pertinência dos dados, justificativa e clareza. [Voltar ao início](README.md).
