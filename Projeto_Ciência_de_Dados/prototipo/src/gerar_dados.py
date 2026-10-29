"""
gerar_dados.py — Geração da base SIMULADA do protótipo.

ATENÇÃO: todos os registros gerados aqui são SINTÉTICOS.
Eles NÃO representam oficinas, clientes ou avaliações reais.
O objetivo é testar o pipeline completo (ETL -> estatística -> modelos -> dashboard)
antes de existir uma base real. Quando a base real for coletada, basta substituir
os arquivos de data/raw/ mantendo as mesmas colunas.

Saídas (data/raw/):
    oficinas_brutas.csv      -> 1 linha por oficina (com "sujeira" proposital para o ETL)
    clientes_brutos.csv      -> 1 linha por cliente simulado
    escolhas_brutas.csv      -> 1 linha por par cliente x oficina considerada (8 por cliente)
    parametros_simulacao.json-> parâmetros "verdadeiros" usados na simulação

Como a escolha foi simulada, a ordem de importância dos fatores é DEFINIDA pelos
parâmetros abaixo. Por isso, o resultado dos modelos neste protótipo serve para
validar o método (teste de recuperação de parâmetros), e NÃO para afirmar como
clientes reais se comportam.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuração geral
# ---------------------------------------------------------------------------
SEMENTE = 42                 # semente fixa -> resultados reproduzíveis
N_OFICINAS = 1200
N_CLIENTES = 2000
ALTERNATIVAS_POR_CLIENTE = 8   # tamanho do conjunto de oficinas que cada cliente compara
VIZINHAS_CONSIDERADAS = 30     # o conjunto é sorteado entre as 30 oficinas mais próximas
FATOR_ROTA = 1.3               # distância em linha reta * 1,3 ~ distância por ruas

PASTA_RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

# Regiões administrativas do DF: centro aproximado (lat, lon), peso de população
# (aproximado) e peso de oferta de oficinas. Valores aproximados, usados apenas
# para espalhar os pontos de forma plausível no mapa.
REGIOES = {
    "Ceilândia":        (-15.8195, -48.1080, 350, 1.0),
    "Samambaia":        (-15.8760, -48.0870, 250, 0.9),
    "Plano Piloto":     (-15.7940, -47.8825, 225, 0.8),
    "Taguatinga":       (-15.8330, -48.0560, 210, 1.3),
    "Planaltina":       (-15.6200, -47.6520, 180, 0.8),
    "Águas Claras":     (-15.8400, -48.0270, 160, 0.6),
    "Gama":             (-16.0190, -48.0650, 140, 0.9),
    "Guará":            (-15.8230, -47.9800, 140, 1.1),
    "Recanto das Emas": (-15.9040, -48.0640, 130, 0.7),
    "Santa Maria":      (-16.0150, -48.0130, 130, 0.7),
    "São Sebastião":    (-15.9030, -47.7750, 115, 0.7),
    "Sobradinho":       (-15.6530, -47.7920,  85, 0.8),
    "Vicente Pires":    (-15.8030, -48.0300,  70, 1.0),
    "Riacho Fundo":     (-15.8830, -48.0170,  45, 0.7),
    "SIA":              (-15.8000, -47.9530,   5, 3.5),  # polo de oficinas
}

# Tipos de estabelecimento: proporções ancoradas na pesquisa IQA/Ipsos (2026):
# independentes 53%, concessionárias 20%, centros automotivos 17%; o restante
# foi atribuído a oficinas especializadas (suposição).
TIPOS = {
    "Independente": 0.53,
    "Concessionária": 0.20,
    "Centro automotivo": 0.17,
    "Especializada": 0.10,
}

# Pesos "verdadeiros" da utilidade de escolha (variáveis padronizadas).
# Ancoragem: IQA/Ipsos (2026) aponta confiança (33%), qualidade (17%) e garantia
# (17%) acima de preço (8%). A nota e o volume de avaliações são usados aqui como
# proxies de confiança/qualidade percebida. A pesquisa NÃO mede distância: o peso
# da distância é uma SUPOSIÇÃO do protótipo.
BETAS_VERDADEIROS = {
    "nota": 1.10,
    "distancia_km": -0.85,
    "log_avaliacoes": 0.45,
    "garantia_estendida": 0.40,
    "log_preco": -0.30,
}


def sigmoide(x):
    return 1 / (1 + np.exp(-x))


def distancia_haversine_km(lat1, lon1, lat2, lon2):
    """Distância em linha reta (km) entre pontos geográficos."""
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def gerar_oficinas(rng):
    """Cria o cadastro limpo das oficinas a partir de uma qualidade latente."""
    nomes_regioes = list(REGIOES)
    peso_oferta = np.array([REGIOES[r][2] ** 0.5 * REGIOES[r][3] for r in nomes_regioes])
    regiao = rng.choice(nomes_regioes, size=N_OFICINAS, p=peso_oferta / peso_oferta.sum())

    lat = np.array([REGIOES[r][0] for r in regiao]) + rng.normal(0, 0.018, N_OFICINAS)
    lon = np.array([REGIOES[r][1] for r in regiao]) + rng.normal(0, 0.018, N_OFICINAS)

    tipo = rng.choice(list(TIPOS), size=N_OFICINAS, p=list(TIPOS.values()))
    conc = (tipo == "Concessionária").astype(float)
    centro = (tipo == "Centro automotivo").astype(float)
    espec = (tipo == "Especializada").astype(float)

    # Qualidade latente (não observada): influencia nota, garantia e tempo de mercado
    qualidade = rng.normal(0, 1, N_OFICINAS) + 0.3 * conc

    anos = np.clip(rng.gamma(2.0, 6.0, N_OFICINAS) * np.exp(0.15 * qualidade), 0.5, 45).round(1)
    garantia = rng.random(N_OFICINAS) < sigmoide(-0.8 + 0.9 * qualidade + 1.0 * conc)
    servicos = rng.poisson(8 + 6 * (conc + centro), N_OFICINAS) + 1

    # Preço médio de uma revisão básica (R$): concessionária mais cara
    fator_regiao = np.where(np.isin(regiao, ["Plano Piloto", "SIA", "Águas Claras"]), 1.10, 1.0)
    log_preco = (np.log(450) + np.log(1 + 0.6 * conc + 0.1 * centro + 0.25 * espec)
                 + 0.06 * qualidade + rng.normal(0, 0.25, N_OFICINAS))
    preco = (np.exp(log_preco) * fator_regiao).round(2)

    # Volume de avaliações (binomial negativa -> cauda longa, como em sites de avaliação)
    media_aval = np.exp(2.8 + 0.35 * np.log1p(anos) + 0.3 * qualidade + 0.4 * centro)
    n_aval = rng.negative_binomial(1.2, 1.2 / (1.2 + media_aval))

    # Nota observada = nota "real" + ruído que diminui com o número de avaliações
    nota_real = np.clip(4.2 + 0.45 * qualidade, 1, 5)
    ruido = rng.normal(0, 1, N_OFICINAS) * 0.6 / np.sqrt(n_aval + 1)
    nota = np.clip(nota_real + ruido, 1, 5).round(1)
    nota = np.where(n_aval == 0, np.nan, nota)   # sem avaliações -> sem nota

    return pd.DataFrame({
        "id_oficina": [f"OF{i:04d}" for i in range(1, N_OFICINAS + 1)],
        "nome_oficina": [f"Oficina Simulada {i:04d}" for i in range(1, N_OFICINAS + 1)],
        "regiao": regiao,
        "estado": "DF",
        "latitude": lat.round(6),
        "longitude": lon.round(6),
        "tipo": tipo,
        "nota": nota,
        "quantidade_avaliacoes": n_aval,
        "preco_medio": preco,
        "quantidade_servicos": servicos,
        "anos_funcionamento": anos,
        "garantia_estendida": garantia.astype(int),
    })


def gerar_clientes(rng):
    nomes = list(REGIOES)
    pop = np.array([REGIOES[r][2] for r in nomes], dtype=float)
    regiao = rng.choice(nomes, size=N_CLIENTES, p=pop / pop.sum())
    return pd.DataFrame({
        "id_cliente": [f"CL{i:04d}" for i in range(1, N_CLIENTES + 1)],
        "regiao": regiao,
        "latitude": (np.array([REGIOES[r][0] for r in regiao]) + rng.normal(0, 0.02, N_CLIENTES)).round(6),
        "longitude": (np.array([REGIOES[r][1] for r in regiao]) + rng.normal(0, 0.02, N_CLIENTES)).round(6),
    })


def simular_escolhas(rng, oficinas, clientes):
    """Cada cliente compara 8 oficinas próximas e escolhe 1 (modelo logit multinomial)."""
    # Só entram no conjunto de consideração oficinas com presença digital (>= 1 avaliação)
    elegiveis = oficinas[oficinas["quantidade_avaliacoes"] > 0].reset_index(drop=True)

    linhas = []
    for _, cli in clientes.iterrows():
        dist = distancia_haversine_km(cli.latitude, cli.longitude,
                                      elegiveis.latitude.values, elegiveis.longitude.values) * FATOR_ROTA
        vizinhas = np.argsort(dist)[:VIZINHAS_CONSIDERADAS]
        conjunto = rng.choice(vizinhas, size=ALTERNATIVAS_POR_CLIENTE, replace=False)
        for idx in conjunto:
            linhas.append((cli.id_cliente, elegiveis.at[idx, "id_oficina"], round(float(dist[idx]), 2)))

    escolhas = pd.DataFrame(linhas, columns=["id_cliente", "id_oficina", "distancia_km"])
    base = escolhas.merge(elegiveis, on="id_oficina", how="left")

    # Variáveis da utilidade, padronizadas na própria base de escolhas
    x = pd.DataFrame({
        "nota": base["nota"],
        "distancia_km": base["distancia_km"],
        "log_avaliacoes": np.log1p(base["quantidade_avaliacoes"]),
        "garantia_estendida": base["garantia_estendida"],
        "log_preco": np.log(base["preco_medio"]),
    })
    z = (x - x.mean()) / x.std()
    z["garantia_estendida"] = x["garantia_estendida"]  # binária fica 0/1

    utilidade = sum(BETAS_VERDADEIROS[c] * z[c] for c in BETAS_VERDADEIROS)
    utilidade = utilidade + rng.gumbel(0, 1, len(base))  # erro do logit

    # Em cada cliente, a oficina com maior utilidade é a escolhida
    escolhida_idx = utilidade.groupby(base["id_cliente"]).idxmax()
    escolhas["escolhida"] = 0
    escolhas.loc[escolhida_idx.values, "escolhida"] = 1
    return escolhas


def sujar_oficinas(rng, oficinas):
    """Insere problemas típicos de dados reais para demonstrar a limpeza (ETL)."""
    df = oficinas.copy()
    df["preco_medio"] = df["preco_medio"].astype(object)
    df["regiao"] = df["regiao"].astype(object)
    n = len(df)

    # 1) Variações de escrita na região (caixa, espaços, sem acento)
    idx = rng.choice(n, size=int(0.05 * n), replace=False)
    variantes = [lambda s: s.lower(), lambda s: f"  {s} ",
                 lambda s: s.replace("á", "a").replace("ã", "a").replace("â", "a").replace("ç", "c")]
    for i in idx:
        df.at[i, "regiao"] = variantes[rng.integers(3)](df.at[i, "regiao"])

    # 2) Preço ausente (2%) e preço digitado como texto "R$ 1.234,56"
    df.loc[rng.choice(n, size=int(0.02 * n), replace=False), "preco_medio"] = np.nan
    for i in rng.choice(n, size=8, replace=False):
        valor = df.at[i, "preco_medio"]
        if pd.notna(valor):
            df.at[i, "preco_medio"] = "R$ " + f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # 3) Notas impossíveis (vírgula perdida: 4.5 -> 45)
    com_nota = df.index[df["nota"].notna()]
    for i in rng.choice(com_nota, size=5, replace=False):
        df.at[i, "nota"] = df.at[i, "nota"] * 10

    # 4) Tempo de funcionamento negativo (erro de digitação)
    df.loc[rng.choice(n, size=3, replace=False), "anos_funcionamento"] *= -1

    # 5) Linhas duplicadas
    dup = df.iloc[rng.choice(n, size=12, replace=False)]
    df = pd.concat([df, dup]).sample(frac=1, random_state=SEMENTE).reset_index(drop=True)
    return df


def main():
    rng = np.random.default_rng(SEMENTE)
    PASTA_RAW.mkdir(parents=True, exist_ok=True)

    oficinas = gerar_oficinas(rng)
    clientes = gerar_clientes(rng)
    escolhas = simular_escolhas(rng, oficinas, clientes)
    oficinas_sujas = sujar_oficinas(rng, oficinas)

    oficinas_sujas.to_csv(PASTA_RAW / "oficinas_brutas.csv", index=False)
    clientes.to_csv(PASTA_RAW / "clientes_brutos.csv", index=False)
    escolhas.to_csv(PASTA_RAW / "escolhas_brutas.csv", index=False)

    parametros = {
        "aviso": "DADOS SIMULADOS - não representam oficinas ou clientes reais",
        "semente": SEMENTE,
        "n_oficinas": N_OFICINAS,
        "n_clientes": N_CLIENTES,
        "alternativas_por_cliente": ALTERNATIVAS_POR_CLIENTE,
        "betas_verdadeiros_padronizados": BETAS_VERDADEIROS,
        "ancoragem": {
            "nota/avaliacoes/garantia > preco": "IQA/Ipsos (2026): confiança 33%, qualidade 17%, garantia 17%, preço 8%",
            "tipos de estabelecimento": "IQA/Ipsos (2026): independentes 53%, concessionárias 20%, centros automotivos 17%",
            "distancia": "SUPOSIÇÃO do protótipo (a pesquisa não mede proximidade)",
        },
    }
    with open(PASTA_RAW / "parametros_simulacao.json", "w", encoding="utf-8") as f:
        json.dump(parametros, f, ensure_ascii=False, indent=2)

    print(f"Oficinas brutas: {len(oficinas_sujas)} linhas | clientes: {len(clientes)} | "
          f"escolhas: {len(escolhas)} linhas ({escolhas.escolhida.sum()} escolhas)")


if __name__ == "__main__":
    main()
