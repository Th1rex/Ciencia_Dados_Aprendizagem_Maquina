<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# PBL — Biblioteca em Foco

## Identificação

- Estudante ou equipe: Thiago Regis Vieira Rocha
- Turma: Sistemas de Informação
- Data de realização: 22/10/2026
- Integrantes e contribuições: Thiago Regis Vieira Rocha

## Situação-problema

Uma biblioteca universitária enfrenta filas em horários específicos e baixa utilização de alguns serviços. A coordenação deseja melhorar o atendimento e planejar recursos. Este é um cenário didático.

**Público-alvo:** estudantes usuários, equipe de atendimento e gestão.

**Questão norteadora:** como os dados podem orientar o planejamento da biblioteca e a oferta de serviços sem identificar ou discriminar seus usuários?

## Investigação em equipe

1. Delimitem o problema e a decisão a apoiar.
2. Registrem o que já sabem e o que precisam investigar.
3. Formulem duas perguntas de negócio.
4. Definam a unidade de análise, os atributos e o alvo, quando houver.
5. Justifiquem a abordagem e indiquem se uma análise descritiva já seria suficiente.
6. Proponham avaliação, cuidados com os dados e limitações.

## Canvas da equipe

| Campo | Registro |
| --- | --- |
| Problema e decisão | A biblioteca tem filas concentradas em certos horários no balcão de empréstimo e devolução, enquanto alguns serviços (salas de estudo em grupo, repositório digital, oficinas de normalização ABNT) são pouco usados. As decisões a apoiar são: (1) quantos atendentes escalar em cada dia e faixa horária; (2) quais serviços reorganizar, divulgar melhor, mudar de horário ou descontinuar. |
| Público-alvo | Estudantes, que sofrem com as filas e podem não conhecer os serviços; equipe de atendimento, que recebe a escala de trabalho; gestão, que decide sobre alocação de pessoal, horários e orçamento dos serviços. |
| O que sabemos | Há relatos de filas em horários específicos e de serviços ociosos. A biblioteca já gera registros em sistemas existentes: empréstimos e devoluções com data e hora no sistema de gestão do acervo, entradas pela catraca, reservas de salas e a escala da equipe. O calendário acadêmico (provas, entrega de TCC, férias) é conhecido com antecedência. |
| O que precisamos investigar | Em quais dias, horários e semanas do semestre a fila de fato ocorre e qual o tempo de espera real; se os picos acompanham o calendário acadêmico; se a baixa utilização vem de desconhecimento, horário inadequado ou falta de necessidade; quais registros existem, por quanto tempo são guardados e se têm falhas. |
| Pergunta de negócio 1 | Em quais dias da semana e faixas horárias a demanda no balcão supera a capacidade da equipe, e quantos atendimentos devemos esperar por faixa horária nas próximas semanas para montar a escala? |
| Pergunta de negócio 2 | Quais serviços têm baixa utilização e quais padrões de uso das visitas indicam quando e como esses serviços poderiam ser melhor oferecidos? |
| Unidade de análise e período | Pergunta 1: faixa horária de 1 hora em um dia (dia × hora) no balcão de atendimento. Pergunta 2: visita anonimizada (da entrada à saída) e serviço por semana. Período: os três últimos semestres letivos, para captar a variação entre semanas de aula, provas e férias. |
| Atributos, unidades e origem pretendida | Data e dia da semana (categoria) e faixa horária (hora), do próprio registro; semana do semestre (número) e período acadêmico (aulas, provas, entrega de TCC, férias), do calendário acadêmico; feriado (sim/não), do calendário institucional; atendentes no turno (pessoas), da escala da equipe; empréstimos e devoluções (contagem por hora), do sistema do acervo; entradas (contagem por hora), da catraca; reservas de salas (contagem por dia), do sistema de reservas; tempo de espera (minutos), por amostra com senha eletrônica ou observação; para cada visita, duração (minutos) e serviços usados (sim/não por serviço); horas de oferta de cada serviço (horas por semana); motivo de não uso e satisfação (escala de 1 a 5), por pesquisa anônima. |
| Alvo e momento em que será conhecido, ou ausência de alvo | Pergunta 1: o alvo é o número de atendimentos no balcão por faixa horária (contagem), conhecido ao fim de cada faixa. A previsão é feita com uma a duas semanas de antecedência para montar a escala, então só entram atributos conhecidos antes disso (calendário, histórico, escala planejada); entradas da catraca na mesma hora não podem ser usadas, porque seria vazamento de dados. Pergunta 2: não há alvo, pois não existem categorias prévias de perfis de uso. |
| Abordagem e justificativa | Primeiro, análise descritiva: mapa de calor de atendimentos por dia e hora e taxa de uso por serviço. Ela provavelmente já responde à parte diagnóstica das duas perguntas (onde estão os picos e quais serviços estão ociosos). Para a pergunta 1, só se o padrão variar muito entre semanas, usa-se aprendizado supervisionado de regressão, porque o alvo é numérico e o histórico traz o valor real. Para a pergunta 2, usa-se aprendizado não supervisionado (agrupamento, como k-means) de visitas anonimizadas pelos serviços usados, duração e horário, porque não existe rótulo de perfil e o objetivo é descobrir padrões. |
| Alternativa sem ML | Média de atendimentos por dia e faixa horária nos semestres anteriores, com reforço da escala por regra nas semanas de prova e entrega de TCC; senha eletrônica para medir a fila; pesquisa curta com estudantes sobre os serviços pouco usados; teste de mudança de horário ou divulgação em um serviço por vez. |
| Como avaliar a proposta | Regressão: separação temporal (treino com semestres anteriores, teste no último semestre), erro médio absoluto (MAE) em atendimentos por hora e comparação com a alternativa sem ML (média histórica); o modelo só é adotado se for claramente melhor. Agrupamento: coeficiente de silhueta e validação com a equipe para ver se os grupos fazem sentido e levam a alguma ação. Negócio: piloto de algumas semanas comparando antes e depois o tempo médio de espera (minutos), a porcentagem de faixas horárias com fila e o uso semanal dos serviços reorganizados. |
| Privacidade e limitações | Privacidade (LGPD): finalidade restrita ao planejamento; uso de contagens agregadas por faixa horária sempre que possível; nenhum dado de nome, matrícula ou títulos emprestados (revela interesses pessoais); se for preciso ligar registros de uma mesma visita, pseudonimização com descarte do identificador ao fim; nenhum atributo como idade, gênero, cor, deficiência ou curso para decidir quem recebe qual serviço, evitando discriminação; nenhum resultado divulgado para grupos com menos de 10 pessoas; acesso restrito e prazo de retenção definido; aviso aos usuários sobre o uso dos dados. Limitações: a catraca mede entradas, não fila; registros podem falhar (catraca liberada, sistema fora do ar); a demanda reprimida não aparece nos dados (quem desistiu pela fila não é registrado); obras, greves e mudanças de calendário quebram o padrão histórico; uso não mede satisfação; correlação não prova causa. |

## Registro de colaboração

| Integrante | Papel | Contribuição |
| --- | --- | --- |
| Thiago Regis Vieira Rocha | Responsável único (trabalho individual) | Delimitação do problema, levantamento do que se sabe e do que investigar, formulação das perguntas de negócio, definição de dados e abordagem, proposta de avaliação, análise de privacidade e redação do canvas e da síntese. |

## Conclusão da equipe

**Proposta:** começar com análise descritiva dos registros já existentes para localizar os picos de fila e os serviços ociosos; usar regressão para prever a demanda por faixa horária e montar a escala somente se ela superar a média histórica; usar agrupamento de visitas anonimizadas para entender padrões de uso e reorganizar a oferta dos serviços. Tudo com dados agregados, sem identificar usuários e sem usar atributos pessoais nas decisões.

**Dúvida ainda aberta:** quais registros a biblioteca realmente mantém e com que qualidade (a catraca registra a saída? existe alguma medida de tempo de espera?) e se a baixa utilização dos serviços se deve a desconhecimento ou a falta de necessidade, o que os dados de uso não respondem sozinhos e exige pesquisa com os estudantes.

**Feedback recebido e melhoria realizada:** PREENCHER após a apresentação

## Síntese para apresentação (2 minutos)

A biblioteca tem dois problemas: filas em horários específicos e serviços pouco usados. As decisões que queremos apoiar são quantos atendentes escalar por horário e quais serviços reorganizar.

Formulamos duas perguntas. A primeira: em quais dias e horários a demanda supera a capacidade, e quantos atendimentos esperar nas próximas semanas? A segunda: quais serviços estão ociosos e que padrões de uso explicam isso?

Os dados já existem: empréstimos e devoluções com horário, catraca, reservas de salas, escala da equipe e calendário acadêmico. A unidade de análise é a faixa de uma hora em cada dia, nos três últimos semestres.

A primeira etapa é descritiva, com um mapa de calor por dia e hora, e ela provavelmente já resolve boa parte do problema. Para a primeira pergunta, o alvo é o número de atendimentos por hora, um número, então usaríamos regressão, mas só se ela prever melhor que a média histórica. Para a segunda, não há rótulo de perfil, então usaríamos agrupamento de visitas anonimizadas.

Avaliamos com separação temporal e erro médio em atendimentos por hora, e, na prática, com um piloto medindo o tempo de espera antes e depois.

Respondendo à questão norteadora: trabalhamos com contagens agregadas, sem nome, matrícula ou histórico de leitura, e não usamos idade, gênero ou curso para decidir quem recebe qual serviço. Uma limitação importante é que quem desistiu por causa da fila não aparece nos dados, por isso a proposta inclui uma pesquisa anônima com os estudantes.

## Entrega

Canvas preenchido e síntese para apresentação de dois minutos. Avaliar coerência da pergunta, dados, abordagem, responsabilidade e colaboração. [Voltar ao início](README.md).

