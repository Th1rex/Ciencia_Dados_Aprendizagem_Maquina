<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Autoavaliação e conferência da entrega

## Identificação

- Estudante ou equipe: **Thiago Regis Vieira Rocha**
- Turma: **Sistemas de Informação**
- Data de realização: **22/10/2026**
- Integrantes e contribuições (se em equipe): **Não se aplica: trabalho individual.**

## Checklist

- [x] Diferenciei IA, Ciência de Dados e ML com um exemplo. *(ver "O que aprendi" abaixo)*
- [x] Completei o quadro supervisionado/não supervisionado. *([01](01-aula1-conceitos.md), seção 2)*
- [x] Justifiquei pelo menos cinco situações-problema. *([01](01-aula1-conceitos.md), seção 3: casos 2, 3, 4, 5 e 7)*
- [x] Registrei a investigação da biblioteca. *([02](02-pbl-biblioteca.md))*
- [x] Identifiquei atributos, alvo, unidade e momento da previsão. *([03](03-aula2-laboratorio.md), seção 2)*
- [x] Executei e documentei a prática em Python ou Orange. *([notebook](notebooks/laboratorio-equipe.ipynb))*
- [x] Escolhi configurações usando treino/validação. *(validação cruzada de 5 partes no treino)*
- [x] Mantive o teste fora do ajuste e da seleção. *(experimentos antes da célula de teste; nenhuma troca depois)*
- [x] Interpretei acurácia, matriz, MAE e R². *([03](03-aula2-laboratorio.md), seções 4 e 6)*
- [x] Comparei com uma referência e discuti erros. *(classe majoritária e média; FP e FN)*
- [x] Registrei limitações, dados sintéticos, privacidade e vieses. *([03](03-aula2-laboratorio.md), seção 7; [04](04-pbl-permanencia.md), seção 6)*
- [x] Formulei recomendações de apoio com revisão humana. *([04](04-pbl-permanencia.md), seção 7)*
- [x] Respondi às questões individuais. *([05](05-revisao.md))*
- [x] Conferi os links e os arquivos de evidências.
- [ ] Substituí os campos PREENCHER ou justifiquei os não aplicáveis. *(pendente: o campo de feedback do [02](02-pbl-biblioteca.md) só pode ser preenchido depois da apresentação)*

## Reflexão individual

- O que aprendi e consigo explicar: **Consigo diferenciar os três conceitos com um exemplo. Inteligência Artificial é a área ampla de métodos para tarefas como reconhecer padrões e decidir: um filtro de spam é uma aplicação de IA, seja feito com regras ou com aprendizado. Machine Learning é a parte da IA em que o modelo é ajustado a partir de exemplos: o filtro aprende com mensagens já rotuladas, em vez de seguir uma lista de palavras. Ciência de Dados é o processo mais amplo de formular a pergunta, preparar e analisar os dados e comunicar o resultado: decidir que mensagens coletar, medir quantos e-mails legítimos foram bloqueados e apresentar isso à equipe. Ela pode usar ML ou apenas análise descritiva. Também consigo explicar por que a tarefa depende do alvo (classe → classificação, número → regressão, sem alvo → agrupamento) e por que o teste precisa ficar fora de qualquer escolha.**
- Qual foi minha principal dificuldade: **Entender quando um resultado justifica trocar a configuração. No experimento de folhas, a folha 40 teve a maior validação, mas a diferença (0,0067) era menor que a dispersão entre as partes, e o resultado do teste da configuração original já era conhecido. Precisei entender que trocar naquele momento contaminaria a avaliação e exigiria um novo teste.**
- Qual evidência mostra meu avanço: **O [notebook executado](notebooks/laboratorio-equipe.ipynb), com os experimentos feitos no treino antes da avaliação final, e o [relatório do laboratório](03-aula2-laboratorio.md), que separa resultado calculado, interpretação e hipótese. Na questão 6 da [revisão](05-revisao.md), identifiquei que a acurácia de 0,85 é igual à da referência trivial, o que antes eu não teria percebido.**
- Como contribuí com a equipe: **Fiz a atividade individualmente: executei o notebook, conduzi os experimentos, preenchi todos os relatórios e preparei os roteiros das apresentações. As contribuições estão registradas em [02](02-pbl-biblioteca.md) e [04](04-pbl-permanencia.md).**
- O que preciso revisar: **O percurso no Orange, que não executei (Data Sampler, Test & Score com Test Data e Preprocess ligado ao learner). Também preciso revisar métricas para classes desbalanceadas além da sensibilidade, como precisão e F1, e como fazer validação temporal na prática.**
- Ferramentas de apoio utilizadas, incluindo IA quando houver, e como verifiquei as respostas: **Jupyter com Python 3.13.16, scikit-learn 1.9.1, pandas 3.0.5, NumPy 2.5.3 e matplotlib 3.11.2. Usei o Claude (Anthropic) como apoio para redigir, organizar os relatórios e montar os experimentos adicionais do notebook. Para verificar: todos os números dos relatórios foram copiados das saídas do notebook executado e do `resultados_execucao.json`; conferi que os resultados coincidem com os publicados no material (acurácia de 0,78, matriz 75/14/19/42, MAE de 28,59 e R² de 0,8774); refiz à mão a acurácia e a sensibilidade da matriz e os cálculos das questões 6 e 7; e confrontei as definições com o material da disciplina.**

## Critérios de avaliação

Escala sugerida do material: nível 3 consistente, 2 adequado com lacunas, 1 parcial, 0 ausente/incoerente. Nota do critério = peso × nível/3. A professora pode ajustar a aplicação.

| Critério | Peso aula 1 | Peso aula 2/PBL |
| --- | --- | --- |
| Problema e conceitos | 3,0 | 2,0 |
| Dados e justificativa | 2,0 | 2,0 |
| Método e avaliação | 1,0 | 3,0 |
| Interpretação e responsabilidade | 2,0 | 2,0 |
| Clareza e colaboração | 2,0 | 1,0 |
| Total | 10,0 | 10,0 |

Na aula 1, método corresponde à avaliação proposta. Na aula 2, inclui execução e interpretação. A maior acurácia isolada não assegura a melhor avaliação da atividade.

## Fontes de apoio

- SCIKIT-LEARN. *User Guide*. https://scikit-learn.org/stable/user_guide.html.
- SCIKIT-LEARN. *Common pitfalls and recommended practices*. https://scikit-learn.org/stable/common_pitfalls.html.
- ORANGE DATA MINING. *Test and Score*. https://orangedatamining.com/widget-catalog/evaluate/testandscore/.

Referências indicadas no material didático do módulo, consultadas em 14 out. 2026. Registre a data da sua própria consulta quando utilizar novas fontes.

[Voltar ao início](README.md).

