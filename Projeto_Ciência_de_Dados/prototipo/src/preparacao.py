"""
preparacao.py — CRISP-DM Fase 3: Preparação dos Dados (ETL).

Lê data/raw/, limpa, trata, sinaliza outliers, cria atributos e grava data/processed/.
Cada transformação é registrada em `log_tratamento`, que vai para o relatório final.
"""

import sqlite3
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
PASTA_RAW = RAIZ / "data" / "raw"
PASTA_PROC = RAIZ / "data" / "processed"

# Lista oficial de regiões (grafia correta) usada para padronizar o texto
REGIOES_OFICIAIS = [
    "Ceilândia", "Samambaia", "Plano Piloto", "Taguatinga", "Planaltina", "Águas Claras",
    "Gama", "Guará", "Recanto das Emas", "Santa Maria", "São Sebastião", "Sobradinho",
    "Vicente Pires", "Riacho Fundo", "SIA",
]

MIN_AVALIACOES_CONFIAVEL = 10   # nota só entra nos grupos se tiver >= 10 avaliações


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))


def padronizar_regiao(valor):
    """'  aguas claras ' -> 'Águas Claras' (compara sem acento e sem caixa)."""
    chave = sem_acento(str(valor)).strip().lower()
    mapa = {sem_acento(r).lower(): r for r in REGIOES_OFICIAIS}
    return mapa.get(chave, str(valor).strip())


def converter_preco(valor):
    """Aceita número ou texto 'R$ 1.234,56' e devolve float."""
    if pd.isna(valor):
        return np.nan
    if isinstance(valor, str) and "R$" in valor:
        valor = valor.replace("R$", "").strip().replace(".", "").replace(",", ".")
    return float(valor)


def marcar_outlier_iqr(serie):
    """True quando o valor está fora de [Q1 - 1,5*IQR ; Q3 + 1,5*IQR]."""
    q1, q3 = serie.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (serie < q1 - 1.5 * iqr) | (serie > q3 + 1.5 * iqr)


def limpar_oficinas(bruto, log):
    df = bruto.copy()
    log.append(f"Base bruta de oficinas: {len(df)} linhas.")

    # 1) Duplicidades
    n_antes = len(df)
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset="id_oficina", keep="first")
    log.append(f"Removidas {n_antes - len(df)} linhas duplicadas (mesmo id_oficina).")

    # 2) Texto da região
    n_dif = (df["regiao"] != df["regiao"].map(padronizar_regiao)).sum()
    df["regiao"] = df["regiao"].map(padronizar_regiao)
    log.append(f"Padronizada a grafia de {n_dif} regiões (caixa, espaços e acentos).")

    # 3) Preço: texto -> número; ausentes imputados pela mediana do mesmo tipo
    df["preco_medio"] = df["preco_medio"].map(converter_preco)
    n_txt = bruto["preco_medio"].astype(str).str.contains("R\\$").sum()
    n_nulo = df["preco_medio"].isna().sum()
    df["preco_imputado"] = df["preco_medio"].isna().astype(int)
    df["preco_medio"] = df["preco_medio"].fillna(df.groupby("tipo")["preco_medio"].transform("median"))
    log.append(f"Convertidos {n_txt} preços digitados como texto; {n_nulo} preços ausentes "
               "imputados pela mediana do tipo de estabelecimento (coluna preco_imputado=1).")

    # 4) Nota impossível (> 5): padrão '45' = '4.5' -> divide por 10
    impossivel = df["nota"] > 5
    df.loc[impossivel, "nota"] = df.loc[impossivel, "nota"] / 10
    log.append(f"Corrigidas {impossivel.sum()} notas fora da escala 1-5 (vírgula perdida, ex.: 45 -> 4,5).")

    # 5) Tempo de funcionamento negativo -> valor absoluto (erro de sinal)
    negativo = df["anos_funcionamento"] < 0
    df.loc[negativo, "anos_funcionamento"] = df.loc[negativo, "anos_funcionamento"].abs()
    log.append(f"Corrigidos {negativo.sum()} tempos de funcionamento negativos (erro de sinal).")

    # 6) Nota ausente: NÃO imputa — oficina sem avaliações não tem nota
    log.append(f"{df['nota'].isna().sum()} oficinas sem avaliações ficam com nota ausente "
               "(não imputada, pois 'sem nota' é informação, não erro).")

    # 7) Outliers: apenas SINALIZADOS, não removidos
    for col in ["preco_medio", "quantidade_avaliacoes", "anos_funcionamento"]:
        df[f"outlier_{col}"] = marcar_outlier_iqr(df[col]).astype(int)
        log.append(f"Outliers (IQR) em {col}: {df[f'outlier_{col}'].sum()} sinalizados e mantidos "
                   "(valores plausíveis; modelos usam log ou métodos robustos).")
    return df.sort_values("id_oficina").reset_index(drop=True)


def criar_atributos(df, log):
    """Engenharia de atributos (nível oficina)."""
    df = df.copy()
    df["log_avaliacoes"] = np.log1p(df["quantidade_avaliacoes"])
    df["log_preco"] = np.log(df["preco_medio"])

    # Nota bayesiana: puxa para a média geral as notas com poucas avaliações
    # nota_aj = (n * nota + m * media) / (n + m), com m = mediana de avaliações
    media = df["nota"].mean()
    m = df["quantidade_avaliacoes"].median()
    n = df["quantidade_avaliacoes"]
    df["nota_ajustada"] = ((n * df["nota"] + m * media) / (n + m)).round(3)
    log.append(f"Criada nota_ajustada (média bayesiana, m={m:.0f} avaliações, média geral={media:.2f}).")

    df["faixa_preco"] = pd.qcut(df["preco_medio"], 4, labels=["Q1 (mais barato)", "Q2", "Q3", "Q4 (mais caro)"])

    # Grupos de avaliação: quartis da nota entre oficinas com avaliações suficientes.
    # Justificativa: as notas ficam concentradas entre 4 e 5, então um corte fixo
    # (ex.: 4,5) seria arbitrário; quartis comparam o topo 25% com a base 25%.
    confiavel = df["quantidade_avaliacoes"] >= MIN_AVALIACOES_CONFIAVEL
    q1, q3 = df.loc[confiavel, "nota"].quantile([0.25, 0.75])
    df["grupo_avaliacao"] = np.select(
        [~confiavel, df["nota"] >= q3, df["nota"] <= q1],
        ["Poucas avaliações", "Alta", "Baixa"], default="Intermediária")
    log.append(f"Grupos de avaliação por quartis da nota (oficinas com >= {MIN_AVALIACOES_CONFIAVEL} "
               f"avaliações): Alta >= {q3:.1f}; Baixa <= {q1:.1f}.")
    return df, {"q1_nota": float(q1), "q3_nota": float(q3)}


def montar_base_escolhas(escolhas, oficinas, log):
    """Junta cada par cliente x oficina com os atributos da oficina."""
    base = escolhas.merge(oficinas, on="id_oficina", how="inner", validate="many_to_one")
    base["faixa_distancia"] = pd.cut(base["distancia_km"], [0, 2, 4, 7, 12, np.inf],
                                     labels=["até 2 km", "2-4 km", "4-7 km", "7-12 km", "> 12 km"])
    log.append(f"Base de modelagem: {len(base)} pares cliente x oficina, "
               f"{base['id_cliente'].nunique()} clientes, taxa de escolha {base['escolhida'].mean():.1%}.")
    return base


def gravar_sqlite(oficinas, clientes, escolhas):
    """Estrutura relacional simples para as consultas SQL de demonstração."""
    caminho = PASTA_PROC / "oficinas.db"
    caminho.unlink(missing_ok=True)
    with sqlite3.connect(caminho) as con:
        colunas = ["id_oficina", "nome_oficina", "regiao", "estado", "latitude", "longitude", "tipo",
                   "nota", "quantidade_avaliacoes", "preco_medio", "quantidade_servicos",
                   "anos_funcionamento", "garantia_estendida", "grupo_avaliacao"]
        oficinas[colunas].to_sql("oficinas", con, index=False)
        clientes.to_sql("clientes", con, index=False)
        escolhas.to_sql("escolhas", con, index=False)
    return caminho


def executar():
    PASTA_PROC.mkdir(parents=True, exist_ok=True)
    log = []

    oficinas_brutas = pd.read_csv(PASTA_RAW / "oficinas_brutas.csv")
    clientes = pd.read_csv(PASTA_RAW / "clientes_brutos.csv")
    escolhas = pd.read_csv(PASTA_RAW / "escolhas_brutas.csv")

    oficinas = limpar_oficinas(oficinas_brutas, log)
    oficinas, cortes = criar_atributos(oficinas, log)
    base = montar_base_escolhas(escolhas, oficinas, log)

    oficinas.to_csv(PASTA_PROC / "oficinas_tratadas.csv", index=False)
    base.to_csv(PASTA_PROC / "escolhas_modelagem.csv", index=False)
    gravar_sqlite(oficinas, clientes, escolhas)

    for linha in log:
        print(" -", linha)
    return oficinas, base, log, cortes


if __name__ == "__main__":
    executar()
