"""
analise.py — CRISP-DM Fases 4 e 5: Modelagem e Avaliação.

Responde:
  Pergunta principal: os clientes escolhem mais pela nota, pela distância ou pelo preço?
  Subpergunta: o que separa as oficinas mais bem avaliadas das demais?

Técnicas:
  - Estatística descritiva e correlação de Spearman (dados assimétricos)
  - Logit condicional (modelo de escolha discreta: 1 escolha entre 8 alternativas)
  - ML supervisionado: Regressão Logística, Árvore, Random Forest, Gradient Boosting
  - Permutation importance (importância das variáveis)
  - Testes de Mann-Whitney / qui-quadrado (alta avaliação x demais)
  - ML não supervisionado: K-Means + PCA
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score, silhouette_score)
from sklearn.model_selection import GroupShuffleSplit, StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text
from statsmodels.discrete.conditional_models import ConditionalLogit

SEMENTE = 42
RAIZ = Path(__file__).resolve().parents[1]
PASTA_RES = RAIZ / "resultados"

# Variáveis explicativas da escolha (nome técnico -> rótulo para gráficos)
VARIAVEIS_ESCOLHA = {
    "nota": "Nota",
    "distancia_km": "Distância (km)",
    "log_preco": "Preço (log)",
    "log_avaliacoes": "Nº de avaliações (log)",
    "garantia_estendida": "Garantia estendida",
    "quantidade_servicos": "Nº de serviços",
    "anos_funcionamento": "Anos de funcionamento",
}
TRIO = ["nota", "distancia_km", "log_preco"]   # os três fatores da pergunta principal


def padronizar(df, colunas):
    """z-score; mantém binárias em 0/1 para facilitar a leitura do coeficiente."""
    z = df[colunas].copy()
    for c in colunas:
        if set(z[c].dropna().unique()) <= {0, 1}:
            continue
        z[c] = (z[c] - z[c].mean()) / z[c].std()
    return z


# ---------------------------------------------------------------------------
# 1. Descritiva e correlação
# ---------------------------------------------------------------------------
def descritiva(oficinas, base):
    num = ["nota", "quantidade_avaliacoes", "preco_medio", "quantidade_servicos", "anos_funcionamento"]
    desc = oficinas[num].describe().T.round(2)
    desc["ausentes"] = oficinas[num].isna().sum()

    cols_corr = ["nota", "distancia_km", "preco_medio", "quantidade_avaliacoes",
                 "quantidade_servicos", "anos_funcionamento", "escolhida"]
    corr = base[cols_corr].corr(method="spearman").round(3)

    # Teste de significância das correlações pedidas no enunciado
    pares = [("nota", "preco_medio"), ("nota", "distancia_km"), ("preco_medio", "distancia_km"),
             ("quantidade_avaliacoes", "nota")]
    testes = []
    for a, b in pares:
        dados = base if "distancia_km" in (a, b) else oficinas
        d = dados[[a, b]].dropna()
        rho, p = stats.spearmanr(d[a], d[b])
        testes.append({"par": f"{a} x {b}", "rho": round(rho, 3), "p_valor": float(p), "n": len(d),
                       "nivel": "oficina" if dados is oficinas else "par cliente x oficina"})
    return desc, corr, testes


def taxa_por_faixa(base):
    """Taxa de escolha por quintil de nota, distância e preço (leitura intuitiva)."""
    saida = {}
    for col in TRIO:
        faixa = pd.qcut(base[col].rank(method="first"), 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
        tab = base.groupby(faixa, observed=True).agg(
            taxa_escolha=("escolhida", "mean"), minimo=(col, "min"), maximo=(col, "max")).reset_index()
        tab.columns = ["quintil", "taxa_escolha", "minimo", "maximo"]
        if col == "log_preco":
            tab[["minimo", "maximo"]] = np.exp(tab[["minimo", "maximo"]])
        saida[col] = tab.round(4).to_dict("records")
    return saida


# ---------------------------------------------------------------------------
# 2. Pergunta principal — Logit condicional
# ---------------------------------------------------------------------------
def logit_condicional(base, betas_verdadeiros):
    cols = list(VARIAVEIS_ESCOLHA)
    z = padronizar(base, cols)
    modelo = ConditionalLogit(base["escolhida"].values, z.values, groups=base["id_cliente"].values)
    ajuste = modelo.fit(disp=False)

    ic = ajuste.conf_int()
    tabela = pd.DataFrame({
        "variavel": cols,
        "rotulo": [VARIAVEIS_ESCOLHA[c] for c in cols],
        "coeficiente": ajuste.params,
        "erro_padrao": ajuste.bse,
        "ic95_inf": ic[:, 0],
        "ic95_sup": ic[:, 1],
        "p_valor": ajuste.pvalues,
        "odds_ratio": np.exp(ajuste.params),
    })
    tabela["peso_absoluto"] = tabela["coeficiente"].abs()
    # Só existe na base simulada; com dados reais a coluna fica vazia
    if betas_verdadeiros:
        tabela["beta_verdadeiro_simulacao"] = tabela["variavel"].map(betas_verdadeiros).fillna(0.0)
    else:
        tabela["beta_verdadeiro_simulacao"] = np.nan

    # Pseudo-R² de McFadden: compara com o modelo "escolha ao acaso" (1/8)
    ll_nulo = -base["id_cliente"].nunique() * np.log(base.groupby("id_cliente").size().mean())
    pseudo_r2 = 1 - ajuste.llf / ll_nulo
    return tabela.sort_values("peso_absoluto", ascending=False).round(4), float(pseudo_r2)


# ---------------------------------------------------------------------------
# 3. ML supervisionado — prever qual oficina é escolhida
# ---------------------------------------------------------------------------
def top1_por_cliente(grupos, y, score):
    """Em cada cliente, marca como 'escolhida' a oficina com maior probabilidade prevista."""
    df = pd.DataFrame({"g": grupos, "y": y, "s": score})
    prev = np.zeros(len(df), dtype=int)
    prev[df.groupby("g")["s"].idxmax().values] = 1
    return prev


def modelos_supervisionados(base):
    cols = list(VARIAVEIS_ESCOLHA)
    X, y, g = base[cols], base["escolhida"].values, base["id_cliente"].values

    # Divisão por CLIENTE: o mesmo cliente nunca aparece em treino e teste ao mesmo tempo
    treino, teste = next(GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=SEMENTE).split(X, y, g))
    Xtr, Xte, ytr, yte, gte = X.iloc[treino], X.iloc[teste], y[treino], y[teste], g[teste]

    candidatos = {
        "Regressão Logística": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "Árvore de Decisão": DecisionTreeClassifier(max_depth=5, min_samples_leaf=50, random_state=SEMENTE),
        "Random Forest": RandomForestClassifier(n_estimators=300, min_samples_leaf=20, n_jobs=-1,
                                                random_state=SEMENTE),
        "Gradient Boosting": HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05,
                                                            max_iter=300, random_state=SEMENTE),
    }
    resultados, ajustados = [], {}
    for nome, modelo in candidatos.items():
        modelo.fit(Xtr, ytr)
        score = modelo.predict_proba(Xte)[:, 1]
        prev = top1_por_cliente(gte, yte, score)
        resultados.append({
            "modelo": nome,
            "roc_auc": roc_auc_score(yte, score),
            "pr_auc": average_precision_score(yte, score),
            "acerto_top1": float((prev[yte == 1] == 1).mean()),   # acertou a oficina escolhida?
            "precision": precision_score(yte, prev),
            "recall": recall_score(yte, prev),
            "f1": f1_score(yte, prev),
            "matriz_confusao": confusion_matrix(yte, prev).tolist(),
        })
        ajustados[nome] = modelo

    res = pd.DataFrame(resultados).sort_values("roc_auc", ascending=False)
    melhor = res.iloc[0]["modelo"]

    # Importância por permutação no melhor modelo (queda de ROC-AUC ao embaralhar a variável)
    imp = permutation_importance(ajustados[melhor], Xte, yte, scoring="roc_auc",
                                 n_repeats=15, random_state=SEMENTE, n_jobs=-1)
    importancia = pd.DataFrame({
        "variavel": cols, "rotulo": [VARIAVEIS_ESCOLHA[c] for c in cols],
        "queda_auc_media": imp.importances_mean, "desvio": imp.importances_std,
    }).sort_values("queda_auc_media", ascending=False)

    info = {"n_treino": int(len(treino)), "n_teste": int(len(teste)),
            "clientes_teste": int(pd.Series(gte).nunique()), "linha_base_top1": 1 / 8, "melhor_modelo": melhor}
    return res.round(4), importancia.round(4), info


# ---------------------------------------------------------------------------
# 4. Subpergunta — o que separa as oficinas mais bem avaliadas
# ---------------------------------------------------------------------------
def comparar_grupos(oficinas):
    df = oficinas[oficinas["grupo_avaliacao"].isin(["Alta", "Intermediária", "Baixa"])].copy()
    df["alta"] = (df["grupo_avaliacao"] == "Alta").astype(int)

    numericas = {"preco_medio": "Preço médio (R$)", "quantidade_avaliacoes": "Nº de avaliações",
                 "quantidade_servicos": "Nº de serviços", "anos_funcionamento": "Anos de funcionamento"}
    linhas = []
    for col, rot in numericas.items():
        a, d = df.loc[df.alta == 1, col], df.loc[df.alta == 0, col]
        u, p = stats.mannwhitneyu(a, d, alternative="two-sided")
        linhas.append({"caracteristica": rot, "alta_mediana": a.median(), "demais_mediana": d.median(),
                       "efeito_rank_biserial": 2 * u / (len(a) * len(d)) - 1, "p_valor": p, "teste": "Mann-Whitney"})

    # Garantia (binária) -> qui-quadrado
    tab = pd.crosstab(df["alta"], df["garantia_estendida"])
    chi2, p, _, _ = stats.chi2_contingency(tab)
    linhas.append({"caracteristica": "Garantia estendida (%)",
                   "alta_mediana": df.loc[df.alta == 1, "garantia_estendida"].mean() * 100,
                   "demais_mediana": df.loc[df.alta == 0, "garantia_estendida"].mean() * 100,
                   "efeito_rank_biserial": np.nan, "p_valor": p, "teste": "Qui-quadrado"})
    comparacao = pd.DataFrame(linhas)

    # Tipo de estabelecimento por grupo
    tipo = (pd.crosstab(df["grupo_avaliacao"], df["tipo"], normalize="index") * 100).round(1)
    chi2_t, p_t, _, _ = stats.chi2_contingency(pd.crosstab(df["grupo_avaliacao"], df["tipo"]))

    # Árvore rasa (sem a nota!) para extrair regras interpretáveis
    feats = ["preco_medio", "quantidade_avaliacoes", "quantidade_servicos", "anos_funcionamento",
             "garantia_estendida"]
    X = df[feats].assign(concessionaria=(df["tipo"] == "Concessionária").astype(int))
    arvore = DecisionTreeClassifier(max_depth=3, min_samples_leaf=30, class_weight="balanced",
                                    random_state=SEMENTE)
    auc_cv = cross_val_score(arvore, X, df["alta"], cv=StratifiedKFold(5, shuffle=True, random_state=SEMENTE),
                             scoring="roc_auc")
    arvore.fit(X, df["alta"])
    regras = export_text(arvore, feature_names=list(X.columns), decimals=1)
    imp_arvore = dict(zip(X.columns, arvore.feature_importances_.round(3)))

    return {
        "comparacao": comparacao.round(4).to_dict("records"),
        "tipo_por_grupo": tipo.reset_index().to_dict("records"),
        "tipo_qui2_p": float(p_t),
        "arvore_auc_cv_media": float(auc_cv.mean()), "arvore_auc_cv_desvio": float(auc_cv.std()),
        "arvore_regras": regras, "arvore_importancias": imp_arvore,
        "n_alta": int(df.alta.sum()), "n_demais": int((df.alta == 0).sum()),
    }


# ---------------------------------------------------------------------------
# 5. Não supervisionado — grupos naturais de oficinas
# ---------------------------------------------------------------------------
def agrupar_oficinas(oficinas):
    cols = ["nota", "log_avaliacoes", "log_preco", "quantidade_servicos", "anos_funcionamento",
            "garantia_estendida"]
    df = oficinas.dropna(subset=["nota"]).copy()
    Z = StandardScaler().fit_transform(df[cols])

    silhuetas = {}
    for k in range(2, 8):
        rot = KMeans(n_clusters=k, n_init=10, random_state=SEMENTE).fit_predict(Z)
        silhuetas[k] = float(silhouette_score(Z, rot))
    k_melhor = max(silhuetas, key=silhuetas.get)

    df["cluster"] = KMeans(n_clusters=k_melhor, n_init=10, random_state=SEMENTE).fit_predict(Z)
    pca = PCA(n_components=2, random_state=SEMENTE)
    coords = pca.fit_transform(Z)
    df["pca1"], df["pca2"] = coords[:, 0], coords[:, 1]

    perfil = df.groupby("cluster").agg(
        oficinas=("id_oficina", "count"), nota=("nota", "median"),
        avaliacoes=("quantidade_avaliacoes", "median"), preco=("preco_medio", "median"),
        servicos=("quantidade_servicos", "median"), anos=("anos_funcionamento", "median"),
        garantia_pct=("garantia_estendida", lambda s: s.mean() * 100),
        concessionaria_pct=("tipo", lambda s: (s == "Concessionária").mean() * 100)).round(2).reset_index()

    return {
        "silhuetas": silhuetas, "k_escolhido": k_melhor,
        "variancia_pca": pca.explained_variance_ratio_.round(3).tolist(),
        "perfil": perfil.to_dict("records"),
        "pontos": df[["id_oficina", "cluster", "pca1", "pca2", "nota", "preco_medio"]].round(3).to_dict("records"),
    }


# ---------------------------------------------------------------------------
# 6. SQL de demonstração
# ---------------------------------------------------------------------------
def executar_sql():
    texto = (RAIZ / "sql" / "consultas.sql").read_text(encoding="utf-8")
    blocos = [b.strip() for b in texto.split("-- nome:") if b.strip() and not b.strip().startswith("--")]
    saida = {}
    with sqlite3.connect(RAIZ / "data" / "processed" / "oficinas.db") as con:
        for bloco in blocos:
            nome, consulta = bloco.split("\n", 1)
            saida[nome.strip()] = pd.read_sql_query(consulta, con).round(2).to_dict("records")
    return saida


# ---------------------------------------------------------------------------
# 7. Hipóteses e conclusão (geradas a partir dos números, não escritas à mão)
# ---------------------------------------------------------------------------
def avaliar_hipoteses(logit, grupos):
    c = logit.set_index("variavel")

    def veredito(var, sinal_esperado):
        coef, p = c.at[var, "coeficiente"], c.at[var, "p_valor"]
        if p >= 0.05:
            return "Não suportada (p >= 0,05)"
        return "Suportada" if np.sign(coef) == sinal_esperado else "Refutada (sinal oposto)"

    comp = {r["caracteristica"]: r for r in grupos["comparacao"]}
    dif = [k for k, r in comp.items() if r["p_valor"] < 0.05]
    return [
        {"id": "H1", "texto": "Notas mais altas aumentam a probabilidade de escolha", "resultado": veredito("nota", 1)},
        {"id": "H2", "texto": "Menor distância aumenta a probabilidade de escolha", "resultado": veredito("distancia_km", -1)},
        {"id": "H3", "texto": "Preço menor aumenta a probabilidade de escolha", "resultado": veredito("log_preco", -1)},
        {"id": "H4", "texto": "Volume de avaliações funciona como sinal de confiança",
         "resultado": veredito("log_avaliacoes", 1)},
        {"id": "H5", "texto": "Oficinas mais bem avaliadas têm características diferentes",
         "resultado": ("Suportada: " + ", ".join(dif)) if dif else "Não suportada"},
    ]


def executar(oficinas, base, log_tratamento, cortes):
    PASTA_RES.mkdir(parents=True, exist_ok=True)
    arquivo_param = RAIZ / "data" / "raw" / "parametros_simulacao.json"
    if arquivo_param.exists():
        with open(arquivo_param, encoding="utf-8") as f:
            parametros = json.load(f)
    else:   # base real: não há parâmetros "verdadeiros" para comparar
        parametros = {"aviso": "Base real", "betas_verdadeiros_padronizados": {}}

    desc, corr, testes_corr = descritiva(oficinas, base)
    faixas = taxa_por_faixa(base)
    logit, pseudo_r2 = logit_condicional(base, parametros["betas_verdadeiros_padronizados"])
    modelos, importancia, info_modelos = modelos_supervisionados(base)
    grupos = comparar_grupos(oficinas)
    clusters = agrupar_oficinas(oficinas)
    sql = executar_sql()
    hipoteses = avaliar_hipoteses(logit, grupos)

    # Ranking do trio da pergunta principal, pelas duas abordagens
    trio_logit = logit[logit["variavel"].isin(TRIO)].sort_values("peso_absoluto", ascending=False)
    trio_perm = importancia[importancia["variavel"].isin(TRIO)].sort_values("queda_auc_media", ascending=False)
    ordem_logit = trio_logit["rotulo"].tolist()
    ordem_perm = trio_perm["rotulo"].tolist()

    resultados = {
        "aviso": parametros["aviso"],
        "parametros_simulacao": parametros,
        "log_tratamento": log_tratamento,
        "cortes_grupos": cortes,
        "descritiva": desc.reset_index().rename(columns={"index": "variavel"}).to_dict("records"),
        "correlacao_spearman": corr.to_dict(),
        "testes_correlacao": testes_corr,
        "taxa_por_faixa": faixas,
        "logit_condicional": logit.to_dict("records"),
        "pseudo_r2_mcfadden": pseudo_r2,
        "modelos": modelos.to_dict("records"),
        "info_modelos": info_modelos,
        "importancia_permutacao": importancia.to_dict("records"),
        "grupos": grupos,
        "clusters": clusters,
        "sql": sql,
        "hipoteses": hipoteses,
        "resposta_principal": {
            "ordem_logit": ordem_logit, "ordem_permutacao": ordem_perm,
            "concordam": ordem_logit == ordem_perm,
        },
    }
    with open(PASTA_RES / "resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2, default=float)

    # Resumo no terminal
    print("\nLogit condicional (variáveis padronizadas):")
    print(logit[["rotulo", "coeficiente", "p_valor", "beta_verdadeiro_simulacao"]].to_string(index=False))
    print(f"Pseudo-R² McFadden: {pseudo_r2:.3f}")
    print("\nModelos supervisionados (teste):")
    print(modelos[["modelo", "roc_auc", "pr_auc", "acerto_top1"]].to_string(index=False))
    print("\nImportância por permutação:")
    print(importancia[["rotulo", "queda_auc_media"]].to_string(index=False))
    print("\nOrdem (logit):", " > ".join(ordem_logit), "| (permutação):", " > ".join(ordem_perm))
    print(f"Clusters: k={clusters['k_escolhido']} (silhuetas {clusters['silhuetas']})")
    for h in hipoteses:
        print(f"{h['id']}: {h['resultado']}")
    return resultados
