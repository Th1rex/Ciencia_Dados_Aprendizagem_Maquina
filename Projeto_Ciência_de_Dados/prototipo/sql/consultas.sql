-- consultas.sql — Demonstração de SQL sobre a base SIMULADA (SQLite: data/processed/oficinas.db)
-- Tabelas: oficinas, clientes, escolhas (1 linha por par cliente x oficina considerada)
-- Cada consulta começa com uma linha de rótulo (nome) para o pipeline executá-las separadamente.

-- nome: kpis_gerais
SELECT
    COUNT(*)                                   AS oficinas,
    ROUND(AVG(nota), 2)                        AS nota_media,
    ROUND(AVG(preco_medio), 2)                 AS preco_medio,
    SUM(quantidade_avaliacoes)                 AS total_avaliacoes,
    SUM(CASE WHEN grupo_avaliacao = 'Alta' THEN 1 ELSE 0 END) AS oficinas_alta_avaliacao
FROM oficinas;

-- nome: media_por_regiao
SELECT
    regiao,
    COUNT(*)                   AS oficinas,
    ROUND(AVG(nota), 2)        AS nota_media,
    ROUND(AVG(preco_medio), 2) AS preco_medio
FROM oficinas
GROUP BY regiao
ORDER BY oficinas DESC;

-- nome: ranking_mais_escolhidas
-- Oficinas mais escolhidas, considerando quantas vezes foram comparadas
SELECT
    o.id_oficina,
    o.regiao,
    o.nota,
    o.preco_medio,
    COUNT(*)                         AS vezes_comparada,
    SUM(e.escolhida)                 AS vezes_escolhida,
    ROUND(AVG(e.escolhida) * 100, 1) AS taxa_escolha_pct
FROM escolhas e
JOIN oficinas o ON o.id_oficina = e.id_oficina
GROUP BY o.id_oficina
HAVING COUNT(*) >= 20
ORDER BY taxa_escolha_pct DESC
LIMIT 10;

-- nome: escolhida_vs_preterida
-- Compara a oficina escolhida com as preteridas no mesmo conjunto
SELECT
    CASE e.escolhida WHEN 1 THEN 'Escolhida' ELSE 'Preterida' END AS situacao,
    ROUND(AVG(o.nota), 2)          AS nota_media,
    ROUND(AVG(e.distancia_km), 2)  AS distancia_media_km,
    ROUND(AVG(o.preco_medio), 2)   AS preco_medio,
    ROUND(AVG(o.quantidade_avaliacoes), 1) AS avaliacoes_media
FROM escolhas e
JOIN oficinas o ON o.id_oficina = e.id_oficina
GROUP BY e.escolhida;

-- nome: escolhida_mais_proxima
-- Em quantos % dos casos o cliente escolheu a oficina MAIS PRÓXIMA do seu conjunto?
WITH ranking AS (
    SELECT id_cliente, escolhida,
           RANK() OVER (PARTITION BY id_cliente ORDER BY distancia_km ASC) AS pos_distancia
    FROM escolhas
)
SELECT ROUND(100.0 * SUM(CASE WHEN pos_distancia = 1 AND escolhida = 1 THEN 1 ELSE 0 END)
             / COUNT(DISTINCT id_cliente), 1) AS pct_escolheu_mais_proxima
FROM ranking;

-- nome: escolhida_melhor_nota
-- Em quantos % dos casos o cliente escolheu a oficina de MAIOR NOTA do seu conjunto?
WITH ranking AS (
    SELECT e.id_cliente, e.escolhida,
           RANK() OVER (PARTITION BY e.id_cliente ORDER BY o.nota DESC) AS pos_nota
    FROM escolhas e JOIN oficinas o ON o.id_oficina = e.id_oficina
)
SELECT ROUND(100.0 * SUM(CASE WHEN pos_nota = 1 AND escolhida = 1 THEN 1 ELSE 0 END)
             / COUNT(DISTINCT id_cliente), 1) AS pct_escolheu_melhor_nota
FROM ranking;

-- nome: escolhida_mais_barata
-- Em quantos % dos casos o cliente escolheu a oficina MAIS BARATA do seu conjunto?
WITH ranking AS (
    SELECT e.id_cliente, e.escolhida,
           RANK() OVER (PARTITION BY e.id_cliente ORDER BY o.preco_medio ASC) AS pos_preco
    FROM escolhas e JOIN oficinas o ON o.id_oficina = e.id_oficina
)
SELECT ROUND(100.0 * SUM(CASE WHEN pos_preco = 1 AND escolhida = 1 THEN 1 ELSE 0 END)
             / COUNT(DISTINCT id_cliente), 1) AS pct_escolheu_mais_barata
FROM ranking;
