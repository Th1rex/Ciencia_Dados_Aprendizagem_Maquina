"""
executar_tudo.py — roda o protótipo de ponta a ponta:
    1) gera a base simulada (data/raw)
    2) prepara os dados (data/processed + SQLite)
    3) estatística, modelos e SQL (resultados/resultados.json)
    4) figuras do documento (resultados/figuras/)

Uso:
    python src/executar_tudo.py                 # gera dados simulados e roda tudo
    python src/executar_tudo.py --dados-reais   # usa os CSVs que já estão em data/raw (pula o passo 1)
"""

import sys

import analise
import gerar_dados
import gerar_figuras
import preparacao

if __name__ == "__main__":
    usar_dados_reais = "--dados-reais" in sys.argv

    if usar_dados_reais:
        print("== 1/4 Pulando a simulação: usando os arquivos de data/raw ==")
    else:
        print("== 1/4 Gerando dados simulados ==")
        gerar_dados.main()
    print("\n== 2/4 Preparação dos dados ==")
    oficinas, base, log, cortes = preparacao.executar()
    print("\n== 3/4 Modelagem e avaliação ==")
    analise.executar(oficinas, base, log, cortes)
    gerar_figuras.executar()
    print("\nPronto. Rode a dashboard com:  python -m streamlit run dashboard/app.py")
