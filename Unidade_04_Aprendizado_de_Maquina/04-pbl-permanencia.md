<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# PBL integrador — Apoio à Permanência

## Identificação

- Estudante ou equipe: **Thiago Regis Vieira Rocha**
- Turma: **Sistemas de Informação**
- Data de realização: **22/10/2026**
- Integrantes e contribuições (se em equipe): **Trabalho individual: delimitação, dados, execução do notebook, avaliação, análise de riscos e recomendações.**

## Contexto

Uma instituição quer compreender sinais associados à evasão e oferecer apoio antes do fim do semestre. Público-alvo: estudantes matriculados e equipe de apoio acadêmico. O cenário é didático e a prática usa dados sintéticos.

**Questão norteadora:** como identificar situações que merecem atenção e oferecer apoio, reconhecendo erros do modelo e dificuldades que os dados não capturam?

## Proposta da equipe

### 1. Delimitação

- Problema e público: **Parte dos estudantes abandona o curso durante o semestre, e a equipe de apoio acadêmico só fica sabendo quando já é tarde para ajudar. O público é formado pelos estudantes matriculados na graduação, que podem receber apoio, e pela equipe de apoio acadêmico, que tem capacidade limitada de atendimento e precisa saber por onde começar.**
- Decisão que o resultado pode apoiar: **Ao fim da semana 4, priorizar a quem a equipe de apoio envia primeiro um convite voluntário para conversa, monitoria ou orientação. O resultado não decide nada sobre notas, bolsas, matrícula ou permanência. Ele só ordena a oferta de apoio, e a oferta continua aberta a todos.**
- Definição de evasão, unidade e horizonte: **Evasão: o estudante matriculado no início do semestre deixa de estar vinculado ao fim dele (trancamento, cancelamento ou abandono sem renovação de matrícula). Reprovar não é evadir: quem reprova e continua matriculado conta como "permaneceu". Unidade: um estudante em um semestre. Horizonte: previsão ao fim da semana 4 para o desfecho ao fim do mesmo semestre.**

### 2. Perguntas de negócio

1. **Quais indicadores disponíveis até a semana 4 se associam à evasão ao fim do semestre, e com que desempenho um modelo simples consegue sinalizar esses casos em comparação com uma regra de referência?**
2. **Que proporção dos casos de evasão o modelo deixa de sinalizar, e como a oferta de apoio pode alcançar esses estudantes sem depender só do modelo?**

### 3. Dados necessários

| Dado | Papel no projeto | Disponível quando? | Origem pretendida | Necessidade e risco |
| --- | --- | --- | --- | --- |
| Frequência até a semana 4 (%) | Atributo | Fim da semana 4 | Diários de classe / sistema acadêmico | Necessário. Risco: registro inconsistente entre professores e frequência que não captura participação remota. |
| Nota até a semana 4 (0 a 10) | Atributo | Fim da semana 4 (pode faltar) | Sistema acadêmico | Necessário. Risco: avaliações diferentes entre disciplinas e ausência de nota quando ainda não houve avaliação. |
| Número de entregas até a semana 4 (0 a 8) | Atributo | Fim da semana 4 | Ambiente virtual de aprendizagem | Necessário. Risco: estudantes com pouco acesso digital ficam com registro baixo sem estar desengajados. |
| Situação ao fim do semestre (evadiu/permaneceu) | Alvo | Só depois do fim do semestre | Secretaria acadêmica | Indispensável para treinar e avaliar. Risco: definição de evasão diferente entre períodos e atraso no registro de trancamentos. |
| Identificador pseudonimizado | Controle (não é atributo) | Matrícula | Gerado pela equipe de dados | Necessário só para evitar duplicação de um mesmo estudante entre treino e teste. Risco: reidentificação; manter separado, com acesso restrito, e descartar ao fim. |
| Semestre/turma | Controle para divisão temporal | Início do semestre | Sistema acadêmico | Necessário para treinar com períodos anteriores e testar com período posterior. Risco: mudanças de currículo ou calendário. |
| Capacidade de atendimento da equipe de apoio | Restrição da decisão | Início do semestre | Coordenação de apoio | Define quantos convites podem ser feitos. Sem risco pessoal. |
| Notas finais, reprovação final, motivo do trancamento | Não usar como atributo | Só depois da previsão | — | Excluídos porque usá-los seria vazamento de dados: a informação não existe na semana 4. |
| Renda, saúde, raça, gênero, deficiência | Não coletar para o modelo | — | — | Sensíveis e desnecessários para oferecer um convite voluntário. Uma auditoria de equidade só poderia usá-los com governança específica, consentimento e base legal (LGPD), separada do modelo. |

Diferencie dados usados na simulação e dados que seriam necessários para uma investigação real: **A simulação usa só três atributos (frequência, nota e entregas até a semana 4) e um alvo sorteado de uma probabilidade definida por fórmula, em 600 estudantes fictícios independentes, de um único "semestre" e sem identificação. Uma investigação real precisaria de: definição operacional de evasão acordada com a secretaria; vários semestres, para permitir divisão temporal; identificador protegido para evitar duplicação; registro de quando cada dado fica disponível; capacidade de atendimento; e, para auditoria, informação sobre grupos tratada com governança específica. Os resultados da simulação demonstram o processo, mas não o desempenho real.**

### 4. Abordagem e algoritmo

- Classificação, regressão ou outra formulação, com justificativa: **Classificação binária supervisionada. O alvo é uma categoria (evadiu/permaneceu) em um horizonte definido e há histórico rotulado. Codificar as classes como 1/0 não torna a tarefa regressão. Agrupamento poderia explorar perfis de participação, mas não prevê evasão, porque não usa o alvo. Estimar o tempo até a saída seria outra formulação, que exigiria outro alvo.**
- Algoritmo introdutório escolhido: **Árvore de decisão (`DecisionTreeClassifier`) dentro de um pipeline com imputação pela mediana. É interpretável, já que as perguntas podem ser mostradas à equipe de apoio, aceita atributos numéricos sem padronização e a complexidade pode ser controlada pela profundidade e pelo tamanho mínimo das folhas.**
- Referência simples: **Classe majoritária (`DummyClassifier(strategy='most_frequent')`), que sempre prevê "permaneceu". Com dados reais, também compararia com uma regra sem ML, como "frequência abaixo de 60% ou nenhuma entrega", porque, se ela funcionar quase igual, é mais simples e transparente.**

### 5. Avaliação

- Preparação, divisão e validação: **Imputação pela mediana dentro do pipeline, aprendida só no treino. Divisão estratificada de 75% para treino (450) e 25% para teste (150), com semente 42. A profundidade foi escolhida por validação cruzada estratificada de 5 partes no treino (2, 3, 5 ou sem limite). O teste foi usado uma vez, só para a avaliação final. Em aplicação real, a divisão seria temporal (treinar com semestres anteriores e testar com o seguinte) e por estudante.**
- Métricas e razão da escolha: **Acurácia, para comparar com a referência; matriz de confusão, para ver os tipos de erro; e sensibilidade da classe "evadiu" (TP/(TP+FN)), porque o objetivo é não deixar sem apoio quem vai evadir. A precisão (TP/(TP+FP)) entra como complemento, porque indica quantos convites vão para quem não precisaria.**
- Resultados efetivamente calculados e link da evidência: **Profundidade escolhida no treino: 5 (validação de 0,7222 ± 0,0391). Acurácia no teste: 0,7800, contra 0,5933 da referência. Matriz no teste: TN = 75, FP = 14, FN = 19, TP = 42. Sensibilidade: 0,6885. Precisão: 0,7500. Evidência: [notebooks/laboratorio-equipe.ipynb](notebooks/laboratorio-equipe.ipynb), [notebooks/resultados_execucao.json](notebooks/resultados_execucao.json) e [assets/lab-matriz-confusao.png](assets/lab-matriz-confusao.png). Detalhes em [03-aula2-laboratorio.md](03-aula2-laboratorio.md).**
- Erros relevantes e consequências: **19 dos 61 casos de evasão do teste (31%) não foram sinalizados (FN). Se o apoio dependesse só do modelo, esses estudantes não receberiam convite, e esse é o erro mais grave aqui. 14 dos 89 que permaneceram foram sinalizados (FP) e receberiam um convite desnecessário, um custo baixo se o contato for voluntário e não estigmatizante. A referência erra todos os 61 casos de evasão (sensibilidade 0).**

### 6. Limites e proteção

- Por que os resultados não demonstram causalidade? **O modelo encontra associações entre os atributos e o desfecho, não efeitos. Nota baixa ou frequência baixa podem acompanhar a evasão porque ambas decorrem de uma terceira causa, como necessidade de trabalhar, problema de saúde, mudança de cidade ou dificuldade financeira. Na simulação, as associações foram escritas na fórmula. Mostrar que retirar `nota_sem4` piora a validação (de 0,7222 para 0,6289) só prova utilidade preditiva. Saber se melhorar a nota reduz a evasão exigiria um estudo com desenho causal.**
- Por que dados sintéticos não validam uso institucional? **Porque a relação entre atributos e evasão foi definida por quem fez a simulação, e o modelo apenas a recupera. Os dados não têm as falhas de registro, as mudanças entre semestres, as diferenças entre cursos e a população real da instituição. O desempenho de 0,78 diz respeito à fórmula simulada, não aos estudantes reais.**
- Que grupos podem ser mal representados? Como investigar isso com evidências apropriadas? **Estudantes com pouco acesso à internet (poucas entregas registradas no ambiente virtual sem estarem desengajados), estudantes que trabalham e faltam em horários fixos, ingressantes por transferência ou em período irregular (com histórico curto), estudantes com deficiência que usam formas alternativas de entrega e cursos noturnos ou EAD, com padrões de frequência diferentes. Para investigar: com dados reais e governança aprovada, calcular sensibilidade e taxa de FP separadas por grupo no teste temporal, comparar com a proporção de cada grupo na população, verificar onde há mais ausências de registro e ouvir os próprios estudantes. Este conjunto sintético não tem grupos, então não permite afirmar nada sobre equidade.**
- Como minimizar dados, restringir acesso e definir retenção? **Usar só os atributos necessários para a semana 4 e não coletar dados sensíveis para o modelo. Pseudonimizar o identificador e guardá-lo separado. Dar acesso à lista de sinalizados só aos profissionais de apoio, sem professores, colegas ou setores financeiros. Não divulgar listas nem escores. Manter os escores só durante o semestre em curso e apagá-los ao fim, guardando apenas dados agregados para reavaliar o modelo. Registrar quem acessou e justificar a finalidade conforme a LGPD.**
- Como garantir revisão humana e contestação? **Um profissional de apoio revisa cada sinalização antes de qualquer contato e pode descartá-la com base no que conhece do caso. O convite explica de forma acolhedora que se trata de uma oferta de apoio, sem dizer que a pessoa "vai evadir". O estudante pode recusar sem consequência, pedir para não ser contatado de novo e solicitar explicação ou correção dos dados usados. Ao fim de cada semestre, a equipe revisa os erros (FN e FP) e decide se o modelo continua útil.**

### 7. Recomendações de apoio

- Ação voluntária proposta: **Na semana 5, a equipe de apoio envia aos estudantes sinalizados e revisados um convite pessoal e discreto para uma conversa de acompanhamento, com opções concretas: monitoria nas disciplinas, orientação de estudos, flexibilização de prazos quando cabível e encaminhamento a serviços institucionais (assistência estudantil, apoio psicológico, ouvidoria). Participar é opcional e não afeta notas nem registros acadêmicos.**
- Como acolher estudantes não sinalizados pelo modelo: **Como cerca de 31% das evasões não seriam sinalizadas, o apoio não pode depender só do modelo. Propostas: divulgar a todos os estudantes, no início do semestre, como pedir ajuda; deixar um canal de autoindicação sempre aberto; permitir que professores e coordenadores indiquem casos que observam; e reservar parte da capacidade de atendimento para quem chega por esses caminhos.**
- O que precisa ser verificado antes de aplicação real: **(1) definição de evasão e dados de vários semestres, validados com a secretaria; (2) avaliação temporal mostrando que o modelo supera a referência e uma regra simples sem ML em período futuro; (3) sensibilidade e falsos positivos por grupo, com governança aprovada; (4) capacidade da equipe de atender os convites; (5) avaliação de impacto e base legal sob a LGPD e aprovação das instâncias institucionais; (6) piloto pequeno, com acompanhamento e participação dos estudantes, antes de ampliar.**

Previsões não são certezas. Priorize apoio e revisão humana, sem punições ou decisões automáticas prejudiciais.

## Apresentação de cinco minutos

| Tempo | Conteúdo | Responsável |
| --- | --- | --- |
| 1 minuto | Problema e dados | Thiago Regis Vieira Rocha |
| 2 minutos | Método e resultados | Thiago Regis Vieira Rocha |
| 1 minuto | Limitações | Thiago Regis Vieira Rocha |
| 1 minuto | Recomendações de apoio | Thiago Regis Vieira Rocha |

### Roteiro da apresentação

**Problema e dados (1 min).** Parte dos estudantes evade durante o semestre, e o apoio chega tarde. A proposta é, ao fim da semana 4, priorizar convites voluntários de apoio. Evasão é deixar de estar vinculado ao fim do semestre; reprovar não é evadir. Na prática, usamos 600 estudantes fictícios, com frequência, nota e entregas até a semana 4 e o desfecho no fim do semestre. São dados sintéticos e 5% das notas estão ausentes.

**Método e resultados (2 min).** É classificação, porque o alvo é evadiu/permaneceu. Separamos 25% para teste antes de tudo, imputamos a mediana dentro do pipeline e escolhemos a profundidade da árvore por validação cruzada só no treino; ficou profundidade 5. No teste, a árvore acertou 78%, contra 59% de sempre prever "permaneceu". A matriz mostra o que importa: dos 61 que evadiram, o modelo sinalizou 42 e deixou 19 de fora. Dos 89 que ficaram, 14 receberiam convite sem precisar. Nos experimentos no treino, folhas maiores reduziram o sobreajuste sem perder validação.

**Limitações (1 min).** O modelo mostra associação, não causa. Os dados são sintéticos, então 78% descreve a simulação, não a instituição. Não conseguimos avaliar equidade, e estudantes com pouco acesso digital poderiam ser sinalizados de forma injusta ou nem aparecer nos dados.

**Recomendações (1 min).** Usar o modelo só para ordenar convites voluntários, sempre com revisão humana e direito de recusa. Manter o apoio aberto a todos, porque 31% das evasões escapariam do modelo. Antes de qualquer uso real: dados de vários semestres, teste temporal, auditoria por grupos e piloto.

## Contribuições

| Integrante | Contribuição verificável |
| --- | --- |
| Thiago Regis Vieira Rocha | Execução e documentação do notebook ([notebooks/laboratorio-equipe.ipynb](notebooks/laboratorio-equipe.ipynb)), experimentos no treino, preenchimento do relatório [03-aula2-laboratorio.md](03-aula2-laboratorio.md), delimitação, dados, avaliação, limites e recomendações deste documento e roteiro da apresentação. |

**Dúvida que ainda exige investigação:** se a sensibilidade de cerca de 69% se manteria em uma divisão temporal com dados reais e se ela seria parecida entre grupos de estudantes, especialmente os com pouco acesso digital.

[Voltar ao início](README.md).
