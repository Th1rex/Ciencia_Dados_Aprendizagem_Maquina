<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Aula 2 — Registro do laboratório supervisionado

## Identificação

- Estudante ou equipe: **Thiago Regis Vieira Rocha**
- Turma: **Sistemas de Informação**
- Data de realização: **22/10/2026**
- Integrantes e contribuições (se em equipe): **Trabalho individual: execução do notebook, experimentos, interpretação e relatório.**

## Percurso escolhido

- [x] Python/Colab ou Jupyter.
- [ ] Orange Data Mining.

Use o [notebook de apoio](notebooks/laboratorio.ipynb) ou o [CSV sintético](dados/educacionais-sinteticos.csv). O CSV contém 600 registros fictícios. Atributos: `frequencia_sem4`, `nota_sem4`, `entregas_sem4`. Alvo: `evasao_fim_semestre` (0 permaneceu, 1 evadiu). As associações foram definidas pela simulação, sem validade empírica sobre estudantes reais.

## 1. Ambiente e reprodução

| Item | Registro |
| --- | --- |
| Ambiente e data | Jupyter com kernel Python 3, execução local de cima para baixo em 22/10/2026. |
| Versões das ferramentas/bibliotecas | Python 3.13.16, NumPy 2.5.3, pandas 3.0.5, matplotlib 3.11.2, scikit-learn 1.9.1. As versões diferem das do material (scikit-learn 1.8.0), mas todos os resultados coincidiram com os publicados. |
| Semente aleatória | 42 (`SEMENTE`), usada na simulação, na divisão, na validação cruzada e nas árvores. |
| Caminho do notebook executado ou fluxo Orange | [notebooks/laboratorio-equipe.ipynb](notebooks/laboratorio-equipe.ipynb). Resultados exportados em [notebooks/resultados_execucao.json](notebooks/resultados_execucao.json). |
| Origem dos dados e condição sintética | Dados gerados pela célula de simulação do notebook (600 registros, alvo sorteado a partir de uma probabilidade definida por fórmula). Conferi que são idênticos ao arquivo `dados/educacionais-sinteticos.csv`. São sintéticos e não representam estudantes reais da UDF. |

## 2. Problema e preparação

- Pergunta de negócio: **Quais estudantes poderiam receber um convite voluntário de apoio antes do fim do semestre, com base nos indicadores observados até a semana 4?**
- Unidade de análise e horizonte: **Um estudante fictício. A previsão é feita ao fim da semana 4 para o desfecho ao fim do semestre.**
- Atributos disponíveis no instante da previsão: **`frequencia_sem4` (% de frequência até a semana 4), `nota_sem4` (nota de 0 a 10 até a semana 4) e `entregas_sem4` (número de entregas de 0 a 8 até a semana 4). Todos são conhecidos na semana 4. Nenhum identificador entra no modelo.**
- Variável-alvo e sua natureza: **`evasao_fim_semestre`, categórica binária (0 = permaneceu, 1 = evadiu). Os números 0 e 1 apenas codificam classes, por isso a tarefa é classificação. Distribuição: 59,0% permaneceram e 41,0% evadiram.**
- Ausências e outros problemas encontrados: **30 valores ausentes em `nota_sem4` (5% dos registros), introduzidos artificialmente. Não há ausências nas demais colunas. No treino, `nota_sem4` tem 427 de 450 valores preenchidos.**
- Tratamentos e conjunto usado para aprendê-los: **Imputação pela mediana (`SimpleImputer`) dentro de um `Pipeline`. A mediana é aprendida só com a parte de treino de cada divisão, nunca com o teste. A árvore não precisa de padronização.**

## 3. Desenvolvimento e teste

- Método de divisão e justificativa: **Divisão aleatória estratificada (`train_test_split`, `test_size=0.25`, `stratify=y`). É adequada porque a simulação gera observações independentes. A estratificação mantém a proporção de classes nos dois conjuntos. Com dados reais, a divisão deveria ser temporal (treinar em turmas antigas e testar em turmas mais recentes) e separada por estudante.**
- Quantidades de treino e teste: **450 registros de treino e 150 de teste.**
- Procedimento de validação no treino: **Validação cruzada estratificada em 5 partes (`StratifiedKFold`, `shuffle=True`, semente 42), aplicada apenas ao treino. Cada parte serve uma vez como validação.**
- Parâmetros da árvore e como foram escolhidos: **`max_depth` comparado entre 2, 3, 5 e sem limite, com `min_samples_leaf=10` fixo. A profundidade 5 teve a maior acurácia média de validação (0,7222). Árvore final: `max_depth=5`, `min_samples_leaf=10`, `random_state=42`.**
- Como o teste ficou fora da seleção: **A profundidade foi escolhida só pela validação cruzada no treino. Os experimentos da seção 5 também rodaram antes da célula de teste e usaram só o treino. O teste foi usado uma única vez, para avaliar a árvore final. Não troquei a configuração depois de ver o teste.**

### Alternativa Orange

Confira o alvo como categórico. Registre as conexões: File/Select Columns → Test & Score (Data), Tree → Test & Score (Learner), Test & Score → Confusion Matrix (Evaluation Results). Data Table permite inspeção. Se usar Preprocess, conecte o preprocessor ao learner para ajustar transformações dentro do treino. Não use apenas `Test on train data` como avaliação final.

**Fluxo e método de avaliação realmente utilizados:** Não se aplica: usei o percurso em Python, e o material trata o Orange como alternativa, não como segunda prática obrigatória. A avaliação utilizada foi a descrita na seção 3: validação cruzada estratificada de 5 partes no treino e teste independente de 25%.

Se comparar configurações, use validação no treino e reserve teste independente. Documente em Test & Score as entradas Data e Test Data, quando utilizadas.

## 4. Resultados calculados de classificação

| Modelo | Configuração | Acurácia de treino | Acurácia de validação e dispersão | Acurácia de teste |
| --- | --- | --- | --- | --- |
| Referência | `DummyClassifier(strategy='most_frequent')`: sempre prevê 0 (permaneceu) | 0,5889 (média da validação cruzada) | 0,5889 ± 0,0000 | 0,5933 |
| Árvore final | `DecisionTreeClassifier(max_depth=5, min_samples_leaf=10)` com imputação pela mediana | 0,8133 (treino completo); 0,8111 (média da validação cruzada) | 0,7222 ± 0,0391 | 0,7800 |

Não invente valores. Se sua ferramenta não produziu uma medida, registre “não calculada” e explique.

**Matriz: linhas reais e colunas previstas; classe positiva = 1.**

| Real / previsto | Permaneceu (0) | Evadiu (1) |
| --- | --- | --- |
| Permaneceu (0) | 75 (TN) | 14 (FP) |
| Evadiu (1) | 19 (FN) | 42 (TP) |

- Acurácia calculada manualmente pela matriz: **(TN + TP) / total = (75 + 42) / 150 = 117 / 150 = 0,78, igual ao valor do código.**
- Sensibilidade da classe 1: **TP / (TP + FN) = 42 / (42 + 19) = 42 / 61 = 0,6885. A árvore identifica cerca de 69% dos casos de evasão do teste. Os outros 31% (19 estudantes fictícios) não seriam sinalizados.**
- Comparação com referência: **A árvore acerta 0,7800 contra 0,5933 da referência, um ganho de 18,7 pontos percentuais. Mais importante: a referência tem sensibilidade 0, porque nunca prevê evasão, enquanto a árvore encontra 42 dos 61 casos.**
- Consequências dos falsos positivos: **14 estudantes que permaneceriam receberiam um convite de apoio desnecessário. Se o convite for voluntário e respeitoso, o custo é baixo (tempo da equipe e algum desconforto). Se a sinalização virasse rótulo ou punição, o dano seria sério, e por isso o uso deve ser só de apoio.**
- Consequências dos falsos negativos: **19 estudantes que evadiriam não seriam sinalizados e poderiam ficar sem a oferta de apoio no momento em que ela mais ajudaria. Nesse contexto, é o erro mais custoso. Por isso a oferta de apoio precisa estar aberta também a quem não foi sinalizado.**
- Interpretação do gráfico e da árvore: **A matriz ([assets/lab-matriz-confusao.png](assets/lab-matriz-confusao.png)) concentra a maior parte dos casos na diagonal (75 e 42), mas há mais FN do que FP. A primeira divisão da árvore ([assets/lab-arvore.png](assets/lab-arvore.png)) usa `nota_sem4 <= 6,207`. No ramo de nota baixa, frequência até 64,4% reúne 95 evasões em 128 registros de treino. No ramo de nota alta com frequência acima de 65,5%, há só 1 evasão em 90. Esses limites foram aprendidos dos dados sintéticos e não são regras pedagógicas nem relações causais.**

## 5. Experimentos no treino

Compare parâmetros usando apenas treino/validação. Após conhecer o teste, uma nova seleção exige novo teste independente para avaliação final.

| Experimento | Alteração | Resultado de validação | Interpretação |
| --- | --- | --- | --- |
| 1 | `min_samples_leaf` = 5, 10, 20 e 40 com `max_depth=5` | 0,7222 ± 0,0298; 0,7222 ± 0,0391; 0,7267 ± 0,0480; 0,7289 ± 0,0303. Diferença treino − validação: 0,1039; 0,0889; 0,0633; 0,0467. | As médias variam 0,0067, bem menos que o desvio entre as partes, então não há configuração claramente melhor. Folhas maiores reduzem a diferença entre treino e validação, ou seja, o sobreajuste. Mantive a folha 10 porque a troca, depois de o resultado do teste já ser conhecido, exigiria um novo teste independente. A folha 40 é a candidata para uma próxima rodada. |
| 2 | Retirada de um atributo por vez (`max_depth=5`, folha 10) | Todos: 0,7222 ± 0,0391. Sem `nota_sem4`: 0,6289 ± 0,0475. Sem `entregas_sem4`: 0,7022 ± 0,0310. Sem `frequencia_sem4`: 0,7156 ± 0,0362. | A nota é o atributo que mais ajuda a prever nesta simulação: retirá-la custa 9,3 pontos. A retirada de frequência mal muda o resultado, porque as informações se sobrepõem parcialmente. Isso mostra utilidade preditiva, não causa. |

Responda:

1. Como a profundidade e o tamanho das folhas podem afetar o sobreajuste? **Mais profundidade e folhas menores permitem regras mais específicas, que podem decorar detalhes e ruído do treino. Os experimentos mostram isso: sem limite de profundidade e com folha 5, o treino chega a 0,8678, mas a validação fica em 0,7133 (diferença de 0,1544). Com profundidade 5 e folha 40, a diferença cai para 0,0467 e a validação sobe para 0,7289. Limitar profundidade e exigir folhas maiores controla a complexidade. No outro extremo, profundidade 2 é simples demais e perde desempenho (validação de 0,6844).**
2. Retirar um atributo e observar mudança no desempenho prova causalidade? **Não. A queda mostra só que o atributo carrega informação útil para prever o alvo nestes dados. Causalidade exigiria saber o que acontece com o desfecho quando se muda o atributo, o que pede desenho experimental ou análise causal específica. Além disso, nesta simulação as associações foram definidas pela fórmula. Com dados reais, um atributo pode prever por estar ligado a uma causa não medida, como trabalho, renda ou saúde.**
3. Se 95% permanecem, o que acontece com um modelo que sempre prevê permanência? **Ele teria 95% de acurácia sem identificar nenhuma evasão: TP = 0, FN = todos os casos de evasão e sensibilidade 0. A acurácia alta seria enganosa. Por isso é preciso olhar a matriz de confusão, a sensibilidade e a comparação com essa referência. No laboratório, a mesma referência tem 59,33% de acurácia no teste, também com sensibilidade 0.**

## 6. Regressão — seção independente

Execute a seção da biblioteca no notebook ou registre o procedimento equivalente em Orange. Dados também sintéticos. Alvo numérico: empréstimos por semana.

| Item | Registro |
| --- | --- |
| Atributos e alvo | Atributos: `usuarios_ativos` (100 a 1000) e `horas_abertura` (20 a 60 horas por semana). Alvo: `emprestimos_semana`, numérico contínuo. 300 registros sintéticos, com alvo gerado por 30 + 0,35 × usuários + 2,5 × horas + ruído normal (desvio 35). |
| Divisão e preparação | Divisão aleatória de 25% para teste (`random_state=42`): 225 de treino e 75 de teste. Pipeline com imputação pela mediana (não há ausências, então ela não altera nada) e `LinearRegression`. Referência: `DummyRegressor(strategy='mean')`, que prevê a média do treino. |
| MAE do modelo e unidade | 28,59 empréstimos/semana no teste. |
| MAE da referência | 84,73 empréstimos/semana no teste. O modelo reduz o erro médio para cerca de um terço. |
| R² do teste | 0,8774. A referência tem R² = -0,0037 no teste. Não dá exatamente zero porque usa a média do treino, não a do teste. |
| Interpretação do gráfico observado/previsto | Em [assets/lab-regressao-observado-previsto.png](assets/lab-regressao-observado-previsto.png), os pontos acompanham a diagonal em toda a faixa (cerca de 100 a 530), sem curvatura visível. A dispersão em torno da linha corresponde ao erro médio de cerca de 29 empréstimos. Coeficientes aprendidos: 0,348 por usuário e 2,297 por hora, com intercepto de 37,32, próximos dos valores da simulação. |
| Interpretação dos resíduos | Em [assets/lab-residuos.png](assets/lab-residuos.png), os resíduos (observado − previsto) ficam em torno de zero (média -1,28, desvio 35,47, mínimo -87,24, máximo 64,59). A dispersão é parecida em toda a faixa de previsões e não há padrão sistemático, o que é compatível com uma relação linear e ruído constante. Isso era esperado, porque a simulação foi construída assim. |
| Limitação de extrapolação | O treino cobre de 107 a 993 usuários e de 20,2 a 59,8 horas. A previsão de 303,19 empréstimos para 500 usuários e 40 horas está dentro dessa faixa. Prever para 10.000 usuários ou para 100 horas seria extrapolar: nada garante que a relação continue linear fora do intervalo observado. Com dados reais, também haveria sazonalidade, e a divisão teria de ser temporal. |

Explique por que R² não é porcentagem de acertos: **R² = 1 − (soma dos erros quadráticos do modelo) / (soma dos desvios quadráticos do alvo em relação à média do conjunto avaliado). Ele compara o erro do modelo com o erro de sempre prever essa média: 1 é ajuste perfeito, 0 equivale à média e valores negativos são piores que a média. Em regressão não existe "acerto" ou "erro" categórico, porque toda previsão erra um pouco. Um R² de 0,8774 significa que a soma dos erros quadráticos do modelo é cerca de 12% da soma que se teria prevendo sempre a média do teste, e não que 87,74% das previsões estão certas.**

## 7. Evidências e conclusão

- Link relativo do notebook/fluxo: **[notebooks/laboratorio-equipe.ipynb](notebooks/laboratorio-equipe.ipynb). Resultados em [notebooks/resultados_execucao.json](notebooks/resultados_execucao.json).**
- Links das imagens, se houver: **[Histogramas do treino](assets/lab-histogramas-treino.png), [Matriz de confusão](assets/lab-matriz-confusao.png), [Árvore](assets/lab-arvore.png), [Observado × previsto](assets/lab-regressao-observado-previsto.png), [Resíduos](assets/lab-residuos.png).**
- Principal aprendizado: **A avaliação vale tanto quanto o modelo. Separar o teste antes de qualquer escolha, ajustar a imputação dentro do pipeline e comparar com uma referência mudam o que se pode afirmar. Uma acurácia de 0,78 só tem sentido ao lado da referência (0,59) e da matriz, que mostra 19 evasões não sinalizadas.**
- Limitações de generalização e vieses possíveis: **Os dados são sintéticos, com associações definidas pela fórmula da simulação, então os resultados não valem para estudantes reais. Há uma única divisão de teste com 150 registros, o que deixa incerteza. Com dados reais, haveria mudança entre turmas e períodos (exigindo validação temporal), rótulos de evasão definidos de formas diferentes e estudantes com pouco acesso digital ou registros incompletos mal representados. Este conjunto não tem grupos e não permite avaliar equidade.**
- Cuidados com privacidade e uso responsável: **Usei apenas o conjunto sintético, sem matrícula, nome ou dado pessoal. Em aplicação real: usar só os dados necessários, restringir o acesso à equipe de apoio, definir prazo de retenção, não divulgar listas de estudantes sinalizados, manter revisão humana de cada caso, permitir contestação e recusa e usar a previsão apenas para oferecer apoio voluntário, nunca para punir ou tomar decisões automáticas.**

Para inserir uma imagem salva, use `![Matriz de confusão](assets/minha-matriz.png)` e confira se o arquivo existe. Mostre apenas dados sintéticos.

![Matriz de confusão do teste](assets/lab-matriz-confusao.png)

![Resíduos da regressão no teste](assets/lab-residuos.png)

[Voltar ao início](README.md).

