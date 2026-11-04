"""
gerar_figuras.py — gera as figuras estáticas (PNG) usadas no documento do projeto.

Lê resultados/resultados.json e data/processed/ e grava em resultados/figuras/.
Mesmas cores da dashboard: nota = azul, distância = laranja, preço = verde.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # gera arquivos sem abrir janela
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
PASTA_FIG = RAIZ / "resultados" / "figuras"
CORES = {"Nota": "#2563eb", "Distância (km)": "#ea580c", "Preço (log)": "#16a34a"}
NEUTRA = "#94a3b8"

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 130, "savefig.bbox": "tight"})


def salvar(fig, nome):
    fig.savefig(PASTA_FIG / nome)
    plt.close(fig)


def executar():
    PASTA_FIG.mkdir(parents=True, exist_ok=True)
    res = json.loads((RAIZ / "resultados" / "resultados.json").read_text(encoding="utf-8"))
    oficinas = pd.read_csv(RAIZ / "data" / "processed" / "oficinas_tratadas.csv")

    # Figura 1 — distribuição das notas
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.hist(oficinas["nota"].dropna(), bins=30, color=CORES["Nota"])
    ax.set_xlabel("Nota"); ax.set_ylabel("Oficinas")
    salvar(fig, "fig1_distribuicao_notas.png")

    # Figura 2 — taxa de escolha por quintil (nota, distância, preço)
    fig, eixos = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    titulos = {"nota": ("Nota", "Quintil de nota"), "distancia_km": ("Distância (km)", "Quintil de distância"),
               "log_preco": ("Preço (log)", "Quintil de preço")}
    for ax, (var, (rot, eixo)) in zip(eixos, titulos.items()):
        tab = pd.DataFrame(res["taxa_por_faixa"][var])
        ax.bar(tab["quintil"], tab["taxa_escolha"] * 100, color=CORES[rot])
        ax.axhline(12.5, ls=":", color="#475569")
        ax.set_title(rot.replace(" (log)", "")); ax.set_xlabel(eixo + " (Q5 = maior)")
    eixos[0].set_ylabel("Taxa de escolha (%)")
    eixos[2].text(4.4, 13.2, "acaso (12,5%)", ha="right", fontsize=8, color="#475569")
    salvar(fig, "fig2_taxa_escolha_quintis.png")

    # Figura 3 — coeficientes do logit condicional x valores da simulação
    lg = pd.DataFrame(res["logit_condicional"]).sort_values("peso_absoluto")
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.barh(lg["rotulo"], lg["coeficiente"], color=[CORES.get(r, NEUTRA) for r in lg["rotulo"]],
            xerr=[lg["coeficiente"] - lg["ic95_inf"], lg["ic95_sup"] - lg["coeficiente"]], capsize=3)
    if lg["beta_verdadeiro_simulacao"].notna().any():
        ax.scatter(lg["beta_verdadeiro_simulacao"], lg["rotulo"], marker="D", color="#0f172a",
                   zorder=3, label="Valor usado na simulação")
        ax.legend(loc="lower right", frameon=False)
    ax.axvline(0, color="#475569", lw=0.8)
    ax.set_xlabel("Coeficiente padronizado (IC 95%)")
    salvar(fig, "fig3_logit_condicional.png")

    # Figura 4 — importância por permutação
    imp = pd.DataFrame(res["importancia_permutacao"]).sort_values("queda_auc_media")
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.barh(imp["rotulo"], imp["queda_auc_media"], xerr=imp["desvio"],
            color=[CORES.get(r, NEUTRA) for r in imp["rotulo"]], capsize=3)
    ax.set_xlabel("Queda no ROC-AUC ao embaralhar a variável")
    salvar(fig, "fig4_importancia_permutacao.png")

    # Figura 5 — oficinas de alta avaliação x demais
    comp = pd.DataFrame(res["grupos"]["comparacao"]).set_index("caracteristica")
    itens = ["Preço médio (R$)", "Nº de avaliações", "Anos de funcionamento", "Garantia estendida (%)"]
    fig, eixos = plt.subplots(1, 4, figsize=(11, 3))
    for ax, item in zip(eixos, itens):
        valores = [comp.at[item, "demais_mediana"], comp.at[item, "alta_mediana"]]
        ax.bar(["Demais", "Alta"], valores, color=[NEUTRA, CORES["Nota"]])
        ax.set_title(item, fontsize=9)
    salvar(fig, "fig5_alta_vs_demais.png")

    # Figura 6 — clusters (K-Means) no plano PCA
    cl = res["clusters"]; pts = pd.DataFrame(cl["pontos"])
    fig, ax = plt.subplots(figsize=(6, 4))
    for k, cor in zip(sorted(pts["cluster"].unique()), ["#2563eb", "#f59e0b", "#10b981", "#a855f7"]):
        sub = pts[pts["cluster"] == k]
        ax.scatter(sub["pca1"], sub["pca2"], s=8, alpha=0.6, color=cor, label=f"Grupo {k}")
    v = cl["variancia_pca"]
    ax.set_xlabel(f"PC1 ({v[0]:.0%})"); ax.set_ylabel(f"PC2 ({v[1]:.0%})"); ax.legend(frameon=False)
    salvar(fig, "fig6_clusters_pca.png")

    print(f"Figuras gravadas em {PASTA_FIG}")


if __name__ == "__main__":
    executar()
