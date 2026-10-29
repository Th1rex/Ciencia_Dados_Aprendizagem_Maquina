"""
app.py — Dashboard do protótipo (Streamlit + Plotly).

Conta a história em 5 abas:
  1. Visão geral   -> como está o mercado analisado?
  2. Comportamento -> quais fatores se relacionam com a escolha?
  3. Comparação    -> o que diferencia as oficinas mais bem avaliadas?
  4. Modelagem     -> quais variáveis têm maior poder explicativo/preditivo?
  5. Conclusão     -> qual a resposta para a pergunta de negócio?

Rodar:  streamlit run dashboard/app.py   (depois de python src/executar_tudo.py)
"""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]

# Cor fixa para cada fator da pergunta principal (mesma cor em todos os gráficos)
CORES_FATOR = {"Nota": "#2563eb", "Distância (km)": "#ea580c", "Preço (log)": "#16a34a"}
COR_NEUTRA = "#94a3b8"
CORES_GRUPO = {"Alta": "#2563eb", "Intermediária": "#94a3b8", "Baixa": "#dc2626", "Poucas avaliações": "#e2e8f0"}

st.set_page_config(page_title="Escolha de oficinas — protótipo", page_icon="🔧", layout="wide")


# ---------------------------------------------------------------------------
# Carregamento (com cache para não reler a cada clique)
# ---------------------------------------------------------------------------
@st.cache_data
def carregar():
    oficinas = pd.read_csv(RAIZ / "data" / "processed" / "oficinas_tratadas.csv")
    escolhas = pd.read_csv(RAIZ / "data" / "processed" / "escolhas_modelagem.csv")
    with open(RAIZ / "resultados" / "resultados.json", encoding="utf-8") as f:
        res = json.load(f)
    return oficinas, escolhas, res


try:
    oficinas, escolhas, res = carregar()
except FileNotFoundError:
    st.error("Resultados não encontrados. Rode antes:  python src/executar_tudo.py")
    st.stop()

# ---------------------------------------------------------------------------
# Cabeçalho + aviso de dados simulados (sempre visível)
# ---------------------------------------------------------------------------
st.title("Os clientes escolhem a oficina pela nota, pela distância ou pelo preço?")
st.warning("**PROTÓTIPO COM DADOS SIMULADOS.** Nenhum registro representa oficina ou cliente real. "
           "Os resultados validam o método (o pipeline recupera os parâmetros usados na simulação), "
           "mas **não** podem ser usados como evidência do comportamento real de clientes.", icon="⚠️")

# ---------------------------------------------------------------------------
# Filtros (barra lateral)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Filtros")
    st.caption("Estado: DF (única UF da base simulada)")
    regioes = st.multiselect("Região administrativa", sorted(oficinas["regiao"].unique()))
    tipos = st.multiselect("Tipo de estabelecimento", sorted(oficinas["tipo"].unique()))
    pmin, pmax = float(oficinas.preco_medio.min()), float(oficinas.preco_medio.max())
    faixa_preco = st.slider("Preço médio da revisão (R$)", pmin, pmax, (pmin, pmax), step=10.0)
    faixa_nota = st.slider("Nota", 1.0, 5.0, (1.0, 5.0), step=0.1)
    min_aval = st.slider("Mínimo de avaliações", 0, int(oficinas.quantidade_avaliacoes.max()), 0, step=5)
    faixa_dist = st.slider("Distância cliente → oficina (km)", 0.0, float(escolhas.distancia_km.max()),
                           (0.0, float(escolhas.distancia_km.max())), step=0.5)
    st.caption("Os filtros afetam os gráficos descritivos. Os modelos (aba 4) foram ajustados "
               "na base completa e não mudam com os filtros.")

f = oficinas.copy()
if regioes:
    f = f[f.regiao.isin(regioes)]
if tipos:
    f = f[f.tipo.isin(tipos)]
f = f[f.preco_medio.between(*faixa_preco) & (f.quantidade_avaliacoes >= min_aval)]
f = f[f.nota.between(*faixa_nota) | (f.nota.isna() & (faixa_nota == (1.0, 5.0)))]
e = escolhas[escolhas.id_oficina.isin(f.id_oficina) & escolhas.distancia_km.between(*faixa_dist)]

if f.empty:
    st.info("Nenhuma oficina com esses filtros.")
    st.stop()

aba1, aba2, aba3, aba4, aba5 = st.tabs(["1 · Visão geral", "2 · Comportamento", "3 · Comparação",
                                         "4 · Modelagem", "5 · Conclusão"])

# ---------------------------------------------------------------------------
# 1. Visão geral
# ---------------------------------------------------------------------------
with aba1:
    st.subheader("Como está o mercado analisado?")
    k = st.columns(6)
    k[0].metric("Oficinas", f"{len(f):,}".replace(",", "."))
    k[1].metric("Nota média", f"{f.nota.mean():.2f}".replace(".", ","))
    k[2].metric("Preço médio", f"R$ {f.preco_medio.mean():,.0f}".replace(",", "."))
    k[3].metric("Distância média", f"{e.distancia_km.mean():.1f} km".replace(".", ",") if len(e) else "—")
    k[4].metric("Avaliações (total)", f"{int(f.quantidade_avaliacoes.sum()):,}".replace(",", "."))
    k[5].metric("Oficinas de alta avaliação", int((f.grupo_avaliacao == "Alta").sum()))

    c1, c2 = st.columns([3, 2])
    with c1:
        dados_mapa = dict(color="grupo_avaliacao", color_discrete_map=CORES_GRUPO, hover_name="nome_oficina",
                          hover_data={"nota": True, "preco_medio": ":.0f", "tipo": True,
                                      "latitude": False, "longitude": False}, height=430)
        # Mapa com fundo precisa de internet (tiles); sem internet, usa o gráfico de pontos lat/long
        if st.toggle("Mapa com fundo de ruas (requer internet)", value=False):
            mapa = px.scatter_map(f, lat="latitude", lon="longitude", zoom=9.2,
                                  map_style="carto-positron", **dados_mapa)
        else:
            mapa = px.scatter(f, x="longitude", y="latitude", **dados_mapa)
            mapa.update_yaxes(scaleanchor="x", scaleratio=1)
        mapa.update_layout(margin=dict(l=0, r=0, t=30, b=0), legend_title_text="Grupo",
                           title="Onde estão as oficinas (por grupo de avaliação)")
        st.plotly_chart(mapa, use_container_width=True)
    with c2:
        hist = px.histogram(f.dropna(subset=["nota"]), x="nota", nbins=30, height=430,
                            color_discrete_sequence=[CORES_FATOR["Nota"]],
                            title="Distribuição das notas")
        hist.update_layout(bargap=0.05, yaxis_title="Oficinas", xaxis_title="Nota")
        st.plotly_chart(hist, use_container_width=True)
        st.caption("Notas concentradas entre 4 e 5, como em plataformas de avaliação: por isso os grupos "
                   "usam quartis, e não um corte fixo.")

    c3, c4 = st.columns(2)
    with c3:
        box = px.box(f, x="tipo", y="preco_medio", height=380, color_discrete_sequence=[COR_NEUTRA],
                     title="Preço médio da revisão por tipo de estabelecimento")
        box.update_layout(xaxis_title="", yaxis_title="R$")
        st.plotly_chart(box, use_container_width=True)
    with c4:
        reg = (f.groupby("regiao").agg(oficinas=("id_oficina", "count"), nota_media=("nota", "mean"),
                                        preco_medio=("preco_medio", "mean"))
                 .sort_values("oficinas", ascending=False).round(2).reset_index())
        st.markdown("**Resumo por região** (equivalente à consulta SQL `media_por_regiao`)")
        st.dataframe(reg, hide_index=True, use_container_width=True, height=330)

# ---------------------------------------------------------------------------
# 2. Comportamento
# ---------------------------------------------------------------------------
with aba2:
    st.subheader("Quais fatores estão relacionados à escolha?")
    st.markdown("Cada cliente simulado comparou **8 oficinas próximas** e escolheu **1**. "
                "Ao acaso, a taxa de escolha seria **12,5%**. Quanto mais a barra se afasta disso, "
                "mais o fator se relaciona com a escolha.")

    s = res["sql"]
    m = st.columns(3)
    m[0].metric("Escolheu a de MAIOR NOTA do conjunto", f"{s['escolhida_melhor_nota'][0]['pct_escolheu_melhor_nota']:.1f}%")
    m[1].metric("Escolheu a MAIS PRÓXIMA", f"{s['escolhida_mais_proxima'][0]['pct_escolheu_mais_proxima']:.1f}%")
    m[2].metric("Escolheu a MAIS BARATA", f"{s['escolhida_mais_barata'][0]['pct_escolheu_mais_barata']:.1f}%")
    st.caption("Base completa, via consultas SQL com funções de janela (sql/consultas.sql).")

    cols = st.columns(3)
    nomes = {"nota": ("Nota", "Quintil de nota (Q5 = maior)"),
             "distancia_km": ("Distância (km)", "Quintil de distância (Q5 = mais longe)"),
             "log_preco": ("Preço (log)", "Quintil de preço (Q5 = mais caro)")}
    for col, (var, (rotulo, eixo)) in zip(cols, nomes.items()):
        tab = pd.DataFrame(res["taxa_por_faixa"][var])
        fig = go.Figure(go.Bar(x=tab.quintil, y=tab.taxa_escolha * 100, marker_color=CORES_FATOR[rotulo],
                               text=(tab.taxa_escolha * 100).round(1).astype(str) + "%", textposition="outside"))
        fig.add_hline(y=12.5, line_dash="dot", line_color="#475569", annotation_text="acaso (12,5%)", annotation_position="top left")
        fig.update_layout(title=rotulo.replace(" (log)", ""), height=360, yaxis_range=[0, 32],
                          yaxis_title="Taxa de escolha (%)", xaxis_title=eixo, margin=dict(t=50))
        col.plotly_chart(fig, use_container_width=True)

    st.markdown("**Relações entre as variáveis** (amostra filtrada de pares cliente × oficina)")
    amostra = e.sample(min(3000, len(e)), random_state=42) if len(e) else e
    amostra = amostra.assign(situacao=amostra.escolhida.map({1: "Escolhida", 0: "Preterida"}))
    cores_sit = {"Escolhida": "#2563eb", "Preterida": "#cbd5e1"}
    d1, d2, d3 = st.columns(3)
    for coluna, (x, y, titulo) in zip((d1, d2, d3), [("preco_medio", "nota", "Nota × preço"),
                                                      ("distancia_km", "nota", "Nota × distância"),
                                                      ("distancia_km", "preco_medio", "Preço × distância")]):
        fig = px.scatter(amostra, x=x, y=y, color="situacao", color_discrete_map=cores_sit, opacity=0.6,
                         height=340, title=titulo, category_orders={"situacao": ["Preterida", "Escolhida"]})
        fig.update_traces(marker_size=5)
        fig.update_layout(legend_title_text="", margin=dict(t=50))
        coluna.plotly_chart(fig, use_container_width=True)

    corr = pd.DataFrame(res["correlacao_spearman"])
    heat = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu", zmin=-1, zmax=1, height=420,
                     title="Correlação de Spearman (base completa de pares cliente × oficina)")
    st.plotly_chart(heat, use_container_width=True)
    st.caption("Correlação mede associação, não causa. A coluna 'escolhida' é binária; o modelo da aba 4 "
               "é o que compara os fatores controlando uns pelos outros.")

# ---------------------------------------------------------------------------
# 3. Comparação
# ---------------------------------------------------------------------------
with aba3:
    st.subheader("O que diferencia as oficinas mais bem avaliadas?")
    cortes = res["cortes_grupos"]
    st.markdown(f"Grupos definidos pelos **quartis da nota** entre oficinas com pelo menos 10 avaliações: "
                f"**Alta** ≥ {cortes['q3_nota']:.1f} · **Baixa** ≤ {cortes['q1_nota']:.1f} · "
                f"Intermediária entre os dois. Oficinas com menos de 10 avaliações ficam de fora "
                f"(nota pouco confiável).")

    comp = pd.DataFrame(res["grupos"]["comparacao"])
    comp["diferença significativa?"] = comp.p_valor.map(lambda p: "Sim (p < 0,05)" if p < 0.05 else "Não")
    comp = comp.rename(columns={"caracteristica": "Característica", "alta_mediana": "Alta (mediana / %)",
                                "demais_mediana": "Demais (mediana / %)", "efeito_rank_biserial": "Tamanho do efeito",
                                "teste": "Teste"})
    st.dataframe(comp.drop(columns="p_valor").round(2).fillna("—"), hide_index=True, use_container_width=True)

    g = f[f.grupo_avaliacao.isin(["Alta", "Intermediária", "Baixa"])]
    ordem = {"grupo_avaliacao": ["Baixa", "Intermediária", "Alta"]}
    c1, c2, c3 = st.columns(3)
    for coluna, (y, titulo) in zip((c1, c2), [("preco_medio", "Preço médio (R$)"),
                                              ("quantidade_avaliacoes", "Nº de avaliações")]):
        fig = px.box(g, x="grupo_avaliacao", y=y, color="grupo_avaliacao", color_discrete_map=CORES_GRUPO,
                     category_orders=ordem, height=360, title=titulo)
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="")
        coluna.plotly_chart(fig, use_container_width=True)
    gar = g.groupby("grupo_avaliacao").garantia_estendida.mean().mul(100).reindex(ordem["grupo_avaliacao"])
    fig = go.Figure(go.Bar(x=gar.index, y=gar.values, marker_color=[CORES_GRUPO[i] for i in gar.index],
                           text=gar.round(0).astype(int).astype(str) + "%", textposition="outside"))
    fig.update_layout(title="Oferecem garantia estendida", height=360, yaxis_range=[0, 100], yaxis_title="%")
    c3.plotly_chart(fig, use_container_width=True)

    tipo = (g.groupby(["grupo_avaliacao", "tipo"]).size().groupby(level=0).transform(lambda s: s / s.sum() * 100)
              .rename("pct").reset_index())
    fig = px.bar(tipo, y="grupo_avaliacao", x="pct", color="tipo", orientation="h", height=280,
                 category_orders=ordem, title="Tipo de estabelecimento em cada grupo (%)",
                 color_discrete_sequence=["#0d9488", "#f59e0b", "#a855f7", "#64748b"])
    fig.update_layout(xaxis_title="%", yaxis_title="", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Regras da árvore de decisão (Alta × demais, sem usar a nota)"):
        st.code(res["grupos"]["arvore_regras"], language="text")
        st.caption(f"ROC-AUC em validação cruzada (5 folds): {res['grupos']['arvore_auc_cv_media']:.2f} "
                   f"± {res['grupos']['arvore_auc_cv_desvio']:.2f}")

# ---------------------------------------------------------------------------
# 4. Modelagem
# ---------------------------------------------------------------------------
with aba4:
    st.subheader("Quais variáveis têm maior poder explicativo e preditivo?")
    st.markdown("**Modelo principal: logit condicional.** É o modelo adequado quando cada cliente escolhe "
                "1 opção entre várias: ele compara a oficina escolhida com as preteridas **do mesmo cliente**. "
                "Variáveis padronizadas (z-score), então o tamanho do coeficiente é comparável entre elas.")

    lg = pd.DataFrame(res["logit_condicional"]).sort_values("peso_absoluto")
    cores = [CORES_FATOR.get(r, COR_NEUTRA) for r in lg.rotulo]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=lg.rotulo, x=lg.coeficiente, orientation="h", marker_color=cores, name="Estimado",
                         error_x=dict(type="data", symmetric=False, array=lg.ic95_sup - lg.coeficiente,
                                      arrayminus=lg.coeficiente - lg.ic95_inf)))
    fig.add_trace(go.Scatter(y=lg.rotulo, x=lg.beta_verdadeiro_simulacao, mode="markers", name="Valor usado na simulação",
                             marker=dict(symbol="diamond", size=11, color="#0f172a")))
    fig.update_layout(height=420, title="Coeficientes do logit condicional (IC 95%) × parâmetros da simulação",
                      xaxis_title="Efeito na utilidade por 1 desvio-padrão (negativo = afasta o cliente)",
                      legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Pseudo-R² de McFadden: {res['pseudo_r2_mcfadden']:.3f}. Os losangos mostram os valores usados "
               "para gerar os dados: se as barras batem com eles, o método está recuperando a verdade da simulação.")

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("**Comparação de modelos supervisionados** (teste com 25% dos clientes, separados por cliente)")
        md = pd.DataFrame(res["modelos"]).drop(columns="matriz_confusao")
        md = md.rename(columns={"modelo": "Modelo", "roc_auc": "ROC-AUC", "pr_auc": "PR-AUC",
                                "acerto_top1": "Acerto top-1", "precision": "Precision", "recall": "Recall", "f1": "F1"})
        st.dataframe(md.round(3), hide_index=True, use_container_width=True)
        st.caption("Acerto top-1 = % de clientes em que a oficina com maior probabilidade prevista foi a escolhida "
                   "(acaso = 12,5%). Como cada cliente escolhe exatamente 1, precision = recall = top-1.")
        melhor = res["info_modelos"]["melhor_modelo"]
        mc = next(m for m in res["modelos"] if m["modelo"] == melhor)["matriz_confusao"]
        st.markdown(f"Matriz de confusão — {melhor} (regra top-1)")
        st.dataframe(pd.DataFrame(mc, index=["Real: preterida", "Real: escolhida"],
                                  columns=["Previsto: preterida", "Previsto: escolhida"]), use_container_width=True)
    with c2:
        imp = pd.DataFrame(res["importancia_permutacao"]).sort_values("queda_auc_media")
        fig = go.Figure(go.Bar(y=imp.rotulo, x=imp.queda_auc_media, orientation="h",
                               marker_color=[CORES_FATOR.get(r, COR_NEUTRA) for r in imp.rotulo],
                               error_x=dict(type="data", array=imp.desvio)))
        fig.update_layout(height=420, title=f"Importância por permutação ({melhor})",
                          xaxis_title="Queda no ROC-AUC ao embaralhar a variável")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Aprendizado não supervisionado — existem grupos naturais de oficinas?**")
    cl = res["clusters"]
    pts = pd.DataFrame(cl["pontos"]).assign(cluster=lambda d: "Grupo " + d.cluster.astype(str))
    c3, c4 = st.columns([3, 2])
    with c3:
        fig = px.scatter(pts, x="pca1", y="pca2", color="cluster", opacity=0.7, height=400,
                         title=f"K-Means (k={cl['k_escolhido']}) projetado em 2 componentes principais",
                         color_discrete_sequence=["#2563eb", "#f59e0b", "#10b981", "#a855f7", "#ef4444", "#14b8a6", "#64748b"])
        fig.update_traces(marker_size=5)
        v = cl["variancia_pca"]
        fig.update_layout(xaxis_title=f"PC1 ({v[0]:.0%})", yaxis_title=f"PC2 ({v[1]:.0%})", legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        st.dataframe(pd.DataFrame(cl["perfil"]), hide_index=True, use_container_width=True)
        sil = pd.Series(cl["silhuetas"]).round(3)
        st.caption(f"k escolhido pela maior silhueta ({sil.max():.2f}). Silhueta abaixo de 0,25 indica "
                   "estrutura de grupos FRACA: os grupos existem, mas se sobrepõem bastante.")

# ---------------------------------------------------------------------------
# 5. Conclusão
# ---------------------------------------------------------------------------
with aba5:
    st.subheader("O que os dados mostram?")
    resp = res["resposta_principal"]
    lg = pd.DataFrame(res["logit_condicional"]).set_index("rotulo")
    trio = resp["ordem_logit"]
    limpo = lambda r: r.replace(" (log)", "").replace(" (km)", "").lower()   # "Distância (km)" -> "distância"
    br = lambda x, casas=2: f"{x:+.{casas}f}".replace(".", ",")
    st.markdown("#### Pergunta principal")
    artigo = lambda r: ("o " if limpo(r) == "preço" else "a ") + limpo(r)   # o preço / a nota / a distância
    st.info(f"**Na base simulada, o fator mais associado à escolha é {artigo(trio[0])}, "
            f"depois {artigo(trio[1])} e, por último, {artigo(trio[2])}.**  \n"
            + " · ".join(f"{limpo(t).capitalize()}: coeficiente {br(lg.at[t, 'coeficiente'])}" for t in trio)
            + f"  \nA importância por permutação {'confirma' if resp['concordam'] else 'NÃO confirma'} essa ordem.")
    st.markdown("Essa ordem foi **definida na simulação** (parâmetros ancorados na pesquisa IQA/Ipsos 2026, "
                "que aponta confiança, qualidade e garantia acima de preço). O que o protótipo demonstra é que "
                "o método **consegue recuperar** essa ordem. Com dados reais, a mesma análise responde à pergunta.")

    st.markdown("#### Subpergunta")
    comp = [c for c in res["grupos"]["comparacao"] if c["p_valor"] < 0.05]
    linhas = [f"- **{c['caracteristica']}**: {c['alta_mediana']:.1f} nas de alta avaliação × "
              f"{c['demais_mediana']:.1f} nas demais".replace(".", ",") for c in comp]
    st.markdown("Diferenças estatisticamente significativas (p < 0,05) entre oficinas de alta avaliação e as demais:\n"
                + "\n".join(linhas))

    st.markdown("#### Hipóteses")
    st.dataframe(pd.DataFrame(res["hipoteses"]).rename(columns={"id": "ID", "texto": "Hipótese", "resultado": "Resultado"}),
                 hide_index=True, use_container_width=True)

    st.markdown("#### Limitações")
    st.markdown("""
- **Dados simulados**: a ordem dos fatores reflete os parâmetros escolhidos, não clientes reais.
- **Associação ≠ causa**: mesmo com dados reais, uma nota alta pode ser consequência de mais clientes, e não causa.
- **Escolha observada não existe em fontes públicas**: plataformas mostram nota e avaliações, não quem comparou o quê.
  Com dados reais será preciso pesquisa de escolha (questionário com cenários) ou usar uma variável-alvo substituta
  (ex.: volume de avaliações como proxy de procura), com a limitação documentada.
- **Viés de sobrevivência e seleção**: só entram oficinas com presença digital; oficinas sem avaliação ficaram de fora da escolha.
- **Preço** foi modelado como preço médio de revisão; na prática varia por serviço e por carro.
- **Grupos (K-Means)** com silhueta baixa: separação fraca, interpretar com cuidado.
""")
    with st.expander("Tratamentos aplicados na preparação dos dados"):
        for linha in res["log_tratamento"]:
            st.markdown(f"- {linha}")
