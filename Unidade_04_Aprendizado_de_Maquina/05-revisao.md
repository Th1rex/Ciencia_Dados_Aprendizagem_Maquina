<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Questões de revisão — Registro individual

## Identificação

- Estudante ou equipe: **Thiago Regis Vieira Rocha**
- Turma: **Sistemas de Informação**
- Data de realização: **22/10/2026**
- Integrantes e contribuições (se em equipe): **Não se aplica: registro individual.**

Responda com suas palavras e apresente os cálculos quando solicitados. Os números dos exercícios manuais não são os resultados do laboratório.

## 1. Explique a diferença entre regra programada para bloquear uma palavra e modelo de spam treinado com exemplos.

**Resposta:** Na regra programada, uma pessoa escreve explicitamente a decisão, por exemplo "se a mensagem contém 'grátis', bloquear". Ela é simples e transparente, mas rígida: bloqueia mensagens legítimas que usam a palavra, deixa passar variações como "gr4tis" e precisa ser atualizada à mão a cada novo golpe. No modelo, o algoritmo recebe mensagens já rotuladas como spam ou legítima e ajusta as relações a partir delas, combinando muitos sinais ao mesmo tempo (palavras, remetente, links). Depois, aplica o que aprendeu a mensagens novas. Ele generaliza melhor, mas depende da qualidade dos rótulos, pode reproduzir erros do histórico e precisa ser reavaliado com o tempo. As duas abordagens podem coexistir: uma regra de privacidade continua programada mesmo quando o filtro é um modelo.

## 2. Por que codificar evadiu/permaneceu como 1/0 não transforma classificação em regressão?

**Resposta:** O tipo de tarefa depende do significado do alvo, não da forma como ele é armazenado. 0 e 1 são só rótulos de duas categorias, e poderiam ser "A" e "B". Não existe "evadiu 0,5" nem ordem ou distância com sentido entre as classes. A pergunta continua sendo "qual categoria?", e a avaliação continua sendo por acertos e erros de classe (matriz de confusão), não por distância numérica. Um escore de probabilidade pode acompanhar a classe, mas a saída final continua sendo uma categoria.

## 3. Uma biblioteca quer estimar empréstimos e descobrir perfis. Que tarefas correspondem a cada pergunta?

**Resposta:** Estimar empréstimos é **regressão** (aprendizado supervisionado): o alvo é uma quantidade numérica, por exemplo empréstimos por semana, e há histórico com os valores reais para treinar. Descobrir perfis é **agrupamento** (aprendizado não supervisionado): não existem categorias de perfil definidas antes, então o algoritmo reúne usuários ou visitas semelhantes segundo atributos como horário, serviços usados e duração. Os grupos são interpretados depois por pessoas.

## 4. O que são atributo, alvo e unidade de análise no laboratório educacional?

**Resposta:** A **unidade de análise** é cada linha da tabela: um estudante fictício em um semestre. Os **atributos** são as entradas conhecidas no momento da previsão (fim da semana 4): `frequencia_sem4` (% de frequência), `nota_sem4` (nota de 0 a 10) e `entregas_sem4` (entregas de 0 a 8). O **alvo** é `evasao_fim_semestre`, a resposta que se quer prever: 0 = permaneceu, 1 = evadiu, conhecida só ao fim do semestre. Em cada exemplo de treino, o valor conhecido do alvo é o rótulo.

## 5. Por que calcular a mediana antes de dividir os dados pode invalidar a avaliação?

**Resposta:** Porque a mediana usada para preencher as ausências passaria a incluir valores do teste. Assim, informação do teste vazaria para o ajuste do modelo: o teste deixaria de ser composto por exemplos realmente não vistos, e a avaliação tenderia a ficar otimista. No uso real, a mediana só poderia ser calculada com os dados disponíveis até o momento do treino. O correto é dividir primeiro e aprender a mediana só com o treino. Com validação cruzada, ela deve ser aprendida dentro de cada parte de treino, e é isso que o `Pipeline` garante.

## 6. Em uma matriz didática com TN=80, FP=5, FN=10, TP=5, calcule acurácia e sensibilidade. O resultado é suficiente para aprovar o modelo?

**Resposta:**

- Total = 80 + 5 + 10 + 5 = 100.
- Acurácia = (TN + TP) / total = (80 + 5) / 100 = **0,85 (85%)**.
- Sensibilidade = TP / (TP + FN) = 5 / (5 + 10) = 5 / 15 = **0,333 (33,3%)**.

**Não é suficiente.** Há 85 casos negativos (80 + 5) e 15 positivos. Um modelo que sempre previsse "negativo" teria TN = 85 e TP = 0, ou seja, a mesma acurácia de 0,85, sem identificar nenhum positivo. O modelo, portanto, não supera a referência em acurácia e deixa de identificar 10 dos 15 casos positivos (dois terços). Para decidir, seria preciso comparar com a referência, avaliar a sensibilidade e as consequências dos falsos negativos e confirmar o resultado em validação e teste independentes.

## 7. Valores reais 100, 120, 140 e previsões 110, 115, 130. Calcule MAE e informe a unidade se o alvo for vendas em reais.

**Resposta:**

- Erros absolutos: |100 − 110| = 10; |120 − 115| = 5; |140 − 130| = 10.
- MAE = (10 + 5 + 10) / 3 = 25 / 3 ≈ **8,33**.
- Unidade: **reais (R$)**. Em média, a previsão erra cerca de R$ 8,33 nas vendas, para mais ou para menos.

## 8. Um R² de -0,2 significa “20% de acertos negativos”? Explique.

**Resposta:** Não. R² não é porcentagem de acertos. Ele compara a soma dos erros quadráticos do modelo com a soma dos desvios quadráticos do alvo em relação à média do conjunto avaliado: R² = 1 − SQ_erros / SQ_total. Com R² = −0,2, SQ_erros = 1,2 × SQ_total, ou seja, o erro quadrático do modelo é 20% **maior** do que o de simplesmente prever a média dos valores. O modelo é pior do que essa referência trivial. Possíveis causas: modelo inadequado, atributos sem informação, sobreajuste ou diferença entre os dados de treino e de avaliação.

## 9. Uma árvore tem acurácia 1,00 no treino e 0,65 na validação. Que hipótese investigar e como?

**Resposta:** A principal hipótese é **sobreajuste**: a árvore decorou o treino, inclusive o ruído, e não generaliza. Como investigar:

1. Verificar a complexidade: profundidade, número de folhas e se `max_depth` está sem limite com folhas muito pequenas.
2. Comparar configurações mais simples por validação cruzada **só no treino**, limitando `max_depth` e aumentando `min_samples_leaf`, e observar se a diferença entre treino e validação diminui e a validação melhora.
3. Olhar a média e a dispersão entre as partes da validação cruzada, não uma única divisão.
4. Comparar com a referência (classe majoritária) para saber se 0,65 é melhor que o trivial.

Também vale descartar outros problemas: registros duplicados, atributo com vazamento ou validação com distribuição diferente do treino. Se a escolha final for feita assim, o teste continua reservado para avaliar uma única vez.

## 10. Por que escolher a profundidade pelo teste prejudica a estimativa final?

**Resposta:** Porque o teste passa a fazer parte do desenvolvimento. Ao testar várias profundidades e ficar com a que acertou mais no teste, escolhe-se justamente a configuração que se encaixou melhor naqueles 150 exemplos, inclusive por acaso. A acurácia do teste fica otimista e deixa de ser uma estimativa honesta para dados realmente novos: o teste deixa de ser "não visto". O certo é escolher a profundidade por validação no treino e usar o teste uma única vez. Se a escolha for refeita depois de ver o teste, é preciso um novo teste independente.

## 11. Baixa frequência associada à evasão demonstra causa? Proponha explicação alternativa.

**Resposta:** Não. Associação não é causalidade: mostra só que as duas coisas aparecem juntas nos dados. Explicação alternativa: uma **terceira causa** pode gerar as duas. Um estudante que começa a trabalhar em horário de aula, ou que enfrenta dificuldade financeira ou um problema familiar, passa a faltar e, depois, tranca o curso. Nesse caso, aumentar a frequência por obrigação não resolveria a causa da evasão. Também pode haver **causalidade reversa**: o estudante que já decidiu sair deixa de frequentar as aulas. Para demonstrar causa, seria preciso um estudo com desenho causal, como uma intervenção comparada com grupo de controle.

## 12. Um modelo sinaliza um estudante como possível evasão. Que ação responsável pode ser adotada?

**Resposta:** Tratar a sinalização como motivo para **oferecer apoio**, nunca como certeza ou punição. Concretamente:

1. Um profissional de apoio revisa o caso antes de qualquer contato e pode descartar a sinalização.
2. O estudante recebe um convite voluntário e discreto para conversa, monitoria ou orientação, sem dizer que ele "vai evadir".
3. O estudante pode recusar, pedir para não ser contatado de novo, saber quais dados foram usados e contestar.
4. A sinalização não afeta notas, bolsas nem registros.
5. Os dados ficam com acesso restrito e prazo de retenção definido.

Como o modelo erra (falsos negativos), a mesma oferta deve continuar aberta a todos os estudantes.

## Fontes adicionais consultadas

**Nenhuma fonte além do material da disciplina: material do estudante do Módulo IV (Profa. Kadidja Valéria, UDF, 2026) e o notebook do laboratório. Declaração de uso de IA: usei o Claude (Anthropic) como apoio para redigir e organizar as respostas. Conferi os cálculos das questões 6 e 7 manualmente e as definições com o material da disciplina, e sou responsável pelo conteúdo.**

[Voltar ao início](README.md).

