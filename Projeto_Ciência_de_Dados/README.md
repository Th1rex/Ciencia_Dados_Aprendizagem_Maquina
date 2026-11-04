# TechMotors: por que o cliente escolhe uma oficina mecânica?

> ⚠️ **Os resultados atuais usam DADOS SIMULADOS.** Eles validam o método (CRISP-DM, modelos e dashboard), mas **não** descrevem o comportamento de clientes reais. Os detalhes estão em [Limitações](docs/documentacao.md#14-limitações).

## Identificação

| Campo | Informação |
|---|---|
| Projeto | TechMotors: análise da escolha de oficinas mecânicas |
| Instituição | UDF – Centro Universitário do Distrito Federal |
| Curso / disciplina | Sistemas de Informação / Ciência de Dados e Aprendizado de Máquina |
| Equipe | Thiago Regis Vieira Rocha (gestor de projetos) · Eduardo Santos Morais (dev full stack) |
| Professor | Eliel |
| Metodologia | CRISP-DM |
| Versão | 1.0 (novembro de 2026) |

## Sobre o projeto

A **TechMotors** é uma plataforma de agendamento que liga motoristas a oficinas qualificadas e bem avaliadas. Este projeto de Ciência de Dados investiga o que pesa na escolha da oficina, para embasar o ranqueamento da plataforma e orientar as próprias oficinas.

**Problema:** o motorista tem várias oficinas por perto e pouca informação confiável para decidir. Os preços variam muito, a qualidade é difícil de verificar e muita gente só confia em indicação. As oficinas, por sua vez, não sabem em que investir para serem escolhidas: reputação, preço ou localização.

**Público e decisão apoiada:**
- **Motorista:** escolher a oficina pelo ranking de reputação da plataforma.
- **Dono de oficina:** decidir se investe em reputação (avaliações, garantia) ou em preço.

## Objetivos

**Geral:** identificar e quantificar quais características de uma oficina se associam à escolha do cliente, seguindo o CRISP-DM, e entregar a resposta em uma dashboard interativa.

**Específicos:**
1. Montar uma base de pelo menos 1.000 registros, com dicionário de dados e tratamento documentado.
2. Medir o peso relativo de nota, distância e preço na escolha, por meio de modelo de escolha discreta e modelos de aprendizado de máquina.
3. Criar um ranking de reputação das oficinas, com nota ajustada pelo volume de avaliações.
4. Descrever o que diferencia as oficinas mais bem avaliadas das demais.
5. Publicar os resultados em uma dashboard com KPIs, filtros e conclusão.

## Perguntas de negócio

- **Principal:** os clientes escolhem a oficina mais pela nota, pela distância ou pelo preço?
- **Subpergunta:** quais características separam as oficinas mais bem avaliadas das demais?

### Ajuste em relação ao documento de definição (Unidade III)

O [documento de definição v0.1](../Unidade%20_03_%20Gest%C3%A3o%20_de_%20Projetos%20_em%20_Ciencia_de_%20Dados/Template-Definicao-Projeto-Ciencia-de-Dados.md) tinha três perguntas: melhores oficinas e por quê, sazonalidade de agendamentos e ticket médio. Depois da apresentação inicial, o foco passou para a pergunta principal acima. O mapeamento ficou assim:

| Item da definição | Situação neste projeto |
|---|---|
| Pergunta 1: quais oficinas têm as melhores avaliações e por quê | ✅ Respondida pela subpergunta e pelo ranking de reputação |
| Pergunta 2: sazonalidade e dias de pico | ⏳ Fora do escopo atual: exige data e hora de agendamentos reais da plataforma |
| Pergunta 3: ticket médio por categoria | ⏳ Fora do escopo atual: exige valores cobrados por serviço |
| Objetivo específico 2: score de ranqueamento | ✅ Nota ajustada (média bayesiana) + ranking top 10 |
| H1: nota acima de 4,0 recebe pelo menos 40% mais agendamentos | ✅ Testada (na base simulada) |
| H2: mostrar o preço antes reduz cancelamentos | ❌ Não testável: a base não tem cancelamento |

> Esse ajuste ainda precisa ser registrado na seção 16 do documento de definição ("Ajustes solicitados após a apresentação inicial") e validado com o professor.

## Entregas

| Entrega | Onde está |
|---|---|
| 📄 **Documento do projeto (CRISP-DM completo)** | [`docs/documentacao.md`](docs/documentacao.md) |
| 💻 Código, dados e dashboard | [`prototipo/`](prototipo/) (instruções técnicas em [`prototipo/README.md`](prototipo/README.md)) |
| 🗃️ Dados brutos e tratados | `prototipo/data/raw/` e `prototipo/data/processed/` |
| 🧮 Consultas SQL (KPIs da pergunta) | `prototipo/sql/consultas.sql` |
| 📊 Figuras do documento | `prototipo/resultados/figuras/` |

### Requisitos da disciplina × situação

| Requisito | Situação |
|---|---|
| Amostra com pelo menos 1.000 registros | ✅ 1.200 oficinas e 16.000 pares cliente × oficina |
| Dados brutos + documento + dashboard funcional | ✅ |
| SQL no projeto, com KPI da pergunta | ✅ Ex.: % de clientes que escolheram a oficina de maior nota, a mais próxima e a mais barata |
| Estatística: regressão, aprendizado supervisionado e não supervisionado | ✅ Logit condicional e regressão logística; árvore, Random Forest e Gradient Boosting; K-Means e PCA |
| Insights e resposta da pergunta | ✅ Seções 11 e 13 do documento |
| Referências e origem dos dados | ✅ Seção 16 do documento |
| Pandas | ✅ |
| Power BI | ➖ Substituído por Streamlit (Python), que é reproduzível no próprio repositório. Justificativa na seção 12 do documento |
| PySpark | ➖ Não usado: o volume não exige processamento distribuído. Justificativa na seção 9 do documento |
| Orange Data Mining | ⚠️ Não realizado. Os CSVs tratados estão prontos para abrir no Orange; os passos estão no documento |

---

## Instalação e execução (Windows / PowerShell)

### Tecnologias necessárias

| Tecnologia | Para quê | Como instalar |
|---|---|---|
| Python 3.10 ou superior | Linguagem do projeto | `winget install -e --id Python.Python.3.12` |
| Git | Baixar o repositório | `winget install -e --id Git.Git` |
| pandas, numpy | Manipulação dos dados | pelo `requirements.txt` |
| scipy, statsmodels | Testes estatísticos e logit condicional | pelo `requirements.txt` |
| scikit-learn | Modelos de aprendizado de máquina e K-Means | pelo `requirements.txt` |
| streamlit, plotly | Dashboard interativa | pelo `requirements.txt` |
| matplotlib | Figuras do documento | pelo `requirements.txt` |
| SQLite | Banco para as consultas SQL | já vem com o Python (`sqlite3`) |
| Orange Data Mining (opcional) | Análise visual sem código | `python -m pip install orange3` |

### Passo a passo

Rode **um comando por vez** no PowerShell:

```powershell
# 1) Conferir se Python e Git já estão instalados (os dois precisam mostrar uma versão)
python --version
git --version

# 2) Se algum não existir, instalar e depois FECHAR e ABRIR o PowerShell de novo
winget install -e --id Python.Python.3.12
winget install -e --id Git.Git

# 3) Baixar o repositório e entrar na pasta do protótipo
cd $HOME\Documents
git clone https://github.com/Th1rex/Ciencia_Dados_Aprendizagem_Maquina.git
cd Ciencia_Dados_Aprendizagem_Maquina
cd (Get-ChildItem -Directory "Projeto_Ci*").FullName
cd prototipo

# 4) (Recomendado) Criar um ambiente virtual só para o projeto
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 5) Instalar as bibliotecas
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 6) Gerar dados, tratar, modelar e criar as figuras
python src\executar_tudo.py

# 7) Abrir a dashboard (deixe esta janela aberta; Ctrl+C encerra)
python -m streamlit run dashboard\app.py
```

A dashboard abre em `http://localhost:8501`.

**Se você já clonou o repositório antes,** pule o passo 3, entre na pasta dele com `cd`, rode `git pull` e continue a partir de `cd (Get-ChildItem ...)`.

### Problemas comuns

| Erro | Solução |
|---|---|
| `No such file or directory: requirements.txt` ou `can't open file ... executar_tudo.py` | Você não está na pasta `prototipo`. Rode `pwd`: o caminho precisa terminar em `\prototipo` |
| `python` abre a Microsoft Store ou não é reconhecido | Instale com o winget (passo 2) e reabra o PowerShell |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Rode uma vez `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, ou pule o passo 4 |
| `streamlit` não é reconhecido | Use `python -m streamlit run dashboard\app.py` |
| `localhost recusou a ligação` | O comando do passo 7 não está rodando. Rode de novo e não feche a janela |
| O mapa aparece vazio | Ative a chave "Mapa com fundo de ruas" na aba 1 (precisa de internet) ou use o modo de pontos |

### Orange (opcional)

```powershell
python -m pip install orange3
python -m Orange.canvas
```

Se a instalação pelo pip falhar na sua versão do Python, use o instalador oficial em [orangedatamining.com](https://orangedatamining.com/download/).
