Metodologia: https://www.ibm.com/docs/pt-br/SS3RA7_18.5.0/nl/pt/BR/pdf/ModelerCRISPDM.pdf

Definição do Negócio 28/10: PIZZA HUT Pergunta: Investir em uma franquia da Pizza Hut no UDF é uma oportunidade de negócio?
Referência

PRASHANTRIX. PizzaHut-Sales-Analysis. GitHub, [s. l.], [s. d.]. Disponível em: https://github.com/prashantrix/PizzaHut-Sales-Analysis/tree/main. Acesso em: 28 out. 2026.


1 - Entendimento do Negócio: 
Problema do Negocio: Uma oficina recebe varios clientes, mas os clientes voltam somente uma vez. 
Objetivo do Negocio: Saber como os clientes podem retornar a utilizar os serviços mecanicos e tornar a oficina mais bem avaliada.
Criterio de Sucesso: Esclarecer quais criterios tendem a fortalecer a escolha de uma oficina pelos clientes.

Extração de Dados:
Coleta Inicial: Pesquisa de Campo (Criterios de Escolhas, Grau de Idade, Utilização de Serviços) e resultados em pesquisas nominais. 
Exploração: Similaridade na escolha dos criterios. 


Preparação dos Dados: 
Limpeza: Realizer o Tratamento das respostas, e definição das porcentagens.
Transformação: Após o tratamento, tornar as respostas variaveis agregadas "nome_vinculo"
Formatação: Organização da base no formato adequado para algoritmos de associação ou recomendação.

Modelagem: • Seleção de técnicas: Aplicação de algoritmos de mineração e Machine Learning compatíveis com a ferramenta (como Kohonen, C5.0 para árvores de decisão ou modelos de sequência/associação).

Execução: Treinamento dos modelos para identificar quais produtos são frequentemente comprados juntos e gerar regras de recomendação em tempo real.


 Avaliação (Evaluation)

• Verificação técnica: O modelo de recomendação acerta quais produtos o cliente tem probabilidade de levar? A precisão atinge o limite esperado?

• Validação com o negócio: Comparação dos resultados do modelo com os critérios definidos no início (se não atingir os 10% de cross-selling, a equipe retorna à fase de preparação ou modelagem). Decisão de "go/no-go" para produção.


Implantação (Deployment)

• Colocação em prática: Integração do algoritmo de recomendação na página de checkout/carrinho do e-commerce.

• Monitoramento: Acompanhamento contínuo das métricas de clique na recomendação, conversão de vendas e realimentação do modelo com novos dados de compra.

• Revisão final: Entrevista com as partes interessadas para documentar lições aprendidas (o que deu certo e onde houve gargalos).

Y = B0 . B1X1 + 
Valor que eu quero prever = Variavel Explicativa . Variavel Contra
