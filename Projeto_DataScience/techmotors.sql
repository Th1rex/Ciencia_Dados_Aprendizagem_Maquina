/* =====================================================================
   TechMotors – Análise CRISP-DM (dados simulados: 1.000 agendamentos)
   Dialeto: PostgreSQL (compatível também com DuckDB)

   Estrutura:
     0. Tabelas (modelo relacional do TCC TechMotors)
     1. Validações de qualidade (V1–V6)     -> Fase 2 do CRISP-DM
     2. View agendamento_limpo             -> Fase 3 do CRISP-DM
     3. KPIs (KPI 1–KPI 7)                 -> Fase 2 (exploração)
     4. Consultas de apoio (A e B)         -> Fases 3 e 2
   ===================================================================== */


-- =====================================================================
-- 0. TABELAS
-- =====================================================================
CREATE TABLE "TipoServico" (
    "idTipoServico"       INTEGER PRIMARY KEY,
    "tipoServico"         VARCHAR(60) NOT NULL,
    "categoriaManutencao" VARCHAR(20) NOT NULL,      -- Preventiva | Corretiva
    "valorBase"           DECIMAL(10,2) NOT NULL
);

CREATE TABLE "Oficina" (
    "idOficina"       INTEGER PRIMARY KEY,
    "nomeOficina"     VARCHAR(80) NOT NULL,
    "regiao"          VARCHAR(40) NOT NULL,
    "capacidadeBoxes" INTEGER NOT NULL,
    "planoOficina"    VARCHAR(10) NOT NULL           -- basico | pro
);

CREATE TABLE "CanalAgendamento" (
    "idCanal" INTEGER PRIMARY KEY,
    "canal"   VARCHAR(40) NOT NULL
);

CREATE TABLE "Cliente" (
    "idCliente"           INTEGER PRIMARY KEY,
    "emailCliente"        VARCHAR(120) NOT NULL,
    "idade"               INTEGER NOT NULL,
    "planoFidelidade"     VARCHAR(20) NOT NULL,      -- padrao | clube_tech
    "anoVeiculo"          INTEGER NOT NULL,
    "kmAtual"             INTEGER NOT NULL,
    "pontuacaoFidelidade" INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE "Agendamento" (
    "idAgendamento"     INTEGER PRIMARY KEY,
    "idCliente"         INTEGER NOT NULL REFERENCES "Cliente",
    "idOficina"         INTEGER NOT NULL REFERENCES "Oficina",
    "idTipoServico"     INTEGER NOT NULL REFERENCES "TipoServico",
    "idCanal"           INTEGER NOT NULL REFERENCES "CanalAgendamento",
    "dataAgendamento"   DATE NOT NULL,
    "diasAntecedencia"  INTEGER NOT NULL,
    "valorEstimado"     DECIMAL(10,2),
    "confirmouWhatsapp" INTEGER,
    "faltasAnteriores"  INTEGER NOT NULL DEFAULT 0,
    "noShow"            INTEGER NOT NULL
);

-- Carga no PostgreSQL (psql), a partir da pasta do repositório:
-- \copy "TipoServico"      FROM 'techmotors_data/tipo_servico.csv'      CSV HEADER
-- \copy "Oficina"          FROM 'techmotors_data/oficina.csv'           CSV HEADER
-- \copy "CanalAgendamento" FROM 'techmotors_data/canal_agendamento.csv' CSV HEADER
-- \copy "Cliente"          FROM 'techmotors_data/cliente.csv'           CSV HEADER
-- \copy "Agendamento"      FROM 'techmotors_data/agendamento.csv'       CSV HEADER


-- =====================================================================
-- 1. VALIDAÇÕES DE QUALIDADE (base bruta)
-- =====================================================================

-- V1. Campos obrigatórios nulos em Agendamento (valorEstimado e confirmouWhatsapp)
SELECT SUM(CASE WHEN "valorEstimado" IS NULL THEN 1 ELSE 0 END) AS nulos_valor,
       SUM(CASE WHEN "confirmouWhatsapp" IS NULL THEN 1 ELSE 0 END) AS nulos_whatsapp
FROM "Agendamento";

-- V2. Valores não positivos (valorEstimado <= 0 e quilometragem negativa em Cliente)
SELECT (SELECT COUNT(*) FROM "Agendamento" WHERE "valorEstimado" <= 0) AS valores_nao_positivos,
       (SELECT COUNT(*) FROM "Cliente"     WHERE "kmAtual" < 0)        AS km_negativa;

-- V3. Agendamentos com data futura (extração em 31/12/2026)
SELECT COUNT(*) AS datas_futuras
FROM "Agendamento"
WHERE "dataAgendamento" > DATE '2026-12-31';

-- V4. Veículos com ano impossível no cadastro (> 2026)
SELECT COUNT(*) AS anos_invalidos
FROM "Cliente"
WHERE "anoVeiculo" > 2026;

-- V5. Possíveis erros de digitação: valorEstimado > 10x a mediana do tipo de serviço
WITH med AS (
    SELECT "idTipoServico",
           percentile_cont(0.5) WITHIN GROUP (ORDER BY "valorEstimado") AS mediana
    FROM "Agendamento"
    WHERE "valorEstimado" > 0
    GROUP BY "idTipoServico"
)
SELECT COUNT(*) AS suspeitas_digitacao
FROM "Agendamento" a
JOIN med m ON m."idTipoServico" = a."idTipoServico"
WHERE a."dataAgendamento" <= DATE '2026-12-31'
  AND a."valorEstimado" > 10 * m.mediana;

-- V6. Agendamentos de Oficinas Básicas sem confirmação registrada no WhatsApp
SELECT COUNT(*) AS basico_sem_whatsapp,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*)
                                 FROM "Agendamento" a2
                                 JOIN "Oficina" o2 ON o2."idOficina" = a2."idOficina"
                                 WHERE o2."planoOficina" = 'basico'), 1) AS perc_do_basico
FROM "Agendamento" a
JOIN "Oficina" o ON o."idOficina" = a."idOficina"
WHERE o."planoOficina" = 'basico'
  AND COALESCE(a."confirmouWhatsapp", 0) = 0;


-- =====================================================================
-- 2. BASE LIMPA (Fase 3: selecionar e limpar)
--    - remove datas futuras (> 31/12/2026)
--    - substitui valores <= 0 ou nulos pela mediana do tipo de serviço
--    - corrige provável vírgula esquecida (valor > 10x mediana do serviço) dividindo por 100
--    - trata confirmouWhatsapp nulo como 0 (não confirmado)
-- =====================================================================
CREATE VIEW agendamento_limpo AS
WITH med AS (
    SELECT "idTipoServico",
           percentile_cont(0.5) WITHIN GROUP (ORDER BY "valorEstimado") AS mediana
    FROM "Agendamento"
    WHERE "valorEstimado" > 0 AND "dataAgendamento" <= DATE '2026-12-31'
    GROUP BY "idTipoServico"
)
SELECT a."idAgendamento",
       a."idCliente",
       a."idOficina",
       a."idTipoServico",
       a."idCanal",
       a."dataAgendamento",
       a."diasAntecedencia",
       CASE
           WHEN a."valorEstimado" IS NULL OR a."valorEstimado" <= 0 THEN ROUND(m.mediana, 2)
           WHEN a."valorEstimado" > 10 * m.mediana THEN ROUND(a."valorEstimado" / 100.0, 2)
           ELSE a."valorEstimado"
       END AS "valorEstimado",
       COALESCE(a."confirmouWhatsapp", 0) AS "confirmouWhatsapp",
       a."faltasAnteriores",
       a."noShow"
FROM "Agendamento" a
JOIN med m ON m."idTipoServico" = a."idTipoServico"
WHERE a."dataAgendamento" <= DATE '2026-12-31';


-- =====================================================================
-- 3. KPIs (sobre a base limpa)
-- =====================================================================

-- KPI 1. Volume financeiro previsto, receita realizada, perda por No-Show e taxa geral
SELECT COUNT(*) AS agendamentos,
       ROUND(SUM("valorEstimado"), 2) AS volume_previsto,
       ROUND(SUM(CASE WHEN "noShow" = 0 THEN "valorEstimado" ELSE 0 END), 2) AS receita_realizada,
       ROUND(SUM(CASE WHEN "noShow" = 1 THEN "valorEstimado" ELSE 0 END), 2) AS perda_noshow,
       ROUND(100.0 * AVG("noShow"), 1) AS taxa_noshow_perc
FROM agendamento_limpo;

-- KPI 2. Volume de agendamentos e taxa de confirmação no WhatsApp por plano da oficina
SELECT o."planoOficina" AS plano,
       COUNT(*) AS agendamentos,
       ROUND(100.0 * AVG(a."confirmouWhatsapp"), 1) AS perc_confirmado_wpp
FROM agendamento_limpo a
JOIN "Oficina" o ON o."idOficina" = a."idOficina"
GROUP BY 1
ORDER BY 1;

-- KPI 3. Volume financeiro estimado e participação por tipo de serviço
SELECT ts."tipoServico",
       COUNT(*) AS qtd,
       ROUND(SUM(a."valorEstimado"), 2) AS total_estimado,
       ROUND(100.0 * SUM(a."valorEstimado") / SUM(SUM(a."valorEstimado")) OVER (), 1) AS perc_volume
FROM agendamento_limpo a
JOIN "TipoServico" ts ON ts."idTipoServico" = a."idTipoServico"
GROUP BY 1
ORDER BY total_estimado DESC;

-- KPI 4. Participação de cada canal digital nos agendamentos
SELECT ca."canal",
       COUNT(*) AS agendamentos,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS perc_agendamentos
FROM agendamento_limpo a
JOIN "CanalAgendamento" ca ON ca."idCanal" = a."idCanal"
GROUP BY 1
ORDER BY 2 DESC;

-- KPI 5. Volume financeiro agendado por mês (identifica sazonalidade em 2026)
SELECT CAST(date_trunc('month', "dataAgendamento") AS DATE) AS mes,
       COUNT(*) AS agendamentos,
       ROUND(SUM("valorEstimado"), 2) AS volume_estimado
FROM agendamento_limpo
GROUP BY 1
ORDER BY 1;

-- KPI 6. Taxa de No-Show por plano da oficina
SELECT o."planoOficina" AS plano,
       COUNT(*) AS agendamentos,
       ROUND(100.0 * AVG(a."noShow"), 1) AS taxa_noshow_perc
FROM agendamento_limpo a
JOIN "Oficina" o ON o."idOficina" = a."idOficina"
GROUP BY 1
ORDER BY 1;

-- KPI 7. Ticket médio e proporção de manutenção preventiva por plano de fidelidade
SELECT c."planoFidelidade" AS plano_fidelidade,
       COUNT(*) AS agendamentos,
       ROUND(AVG(a."valorEstimado"), 2) AS ticket_medio,
       ROUND(100.0 * AVG(CASE WHEN ts."categoriaManutencao" = 'Preventiva' THEN 1 ELSE 0 END), 1) AS perc_preventiva
FROM agendamento_limpo a
JOIN "Cliente" c ON c."idCliente" = a."idCliente"
JOIN "TipoServico" ts ON ts."idTipoServico" = a."idTipoServico"
GROUP BY 1
ORDER BY 1;


-- =====================================================================
-- 4. CONSULTAS DE APOIO
-- =====================================================================

-- A. Tabela analítica por cliente (base da segmentação K-means — amostra top 10)
SELECT c."idCliente",
       c."planoFidelidade",
       COUNT(*) AS qtd_agendamentos,
       ROUND(AVG(a."valorEstimado"), 2) AS ticket_medio,
       ROUND(100.0 * AVG(CASE WHEN ts."categoriaManutencao" = 'Preventiva' THEN 1 ELSE 0 END), 1) AS perc_preventiva,
       ROUND(100.0 * AVG(a."noShow"), 1) AS taxa_noshow_perc
FROM agendamento_limpo a
JOIN "Cliente" c ON c."idCliente" = a."idCliente"
JOIN "TipoServico" ts ON ts."idTipoServico" = a."idTipoServico"
GROUP BY 1, 2
ORDER BY 1
LIMIT 10;

-- B. Hipótese H3: proporção de manutenção preventiva por faixa de pontuação de fidelidade
SELECT CASE WHEN c."pontuacaoFidelidade" < 250 THEN '1. menos de 250 pts'
            WHEN c."pontuacaoFidelidade" < 550 THEN '2. 250 a 549 pts'
            ELSE '3. 550 pts ou mais' END AS faixa_fidelidade,
       COUNT(DISTINCT c."idCliente") AS clientes,
       ROUND(100.0 * AVG(CASE WHEN ts."categoriaManutencao" = 'Preventiva' THEN 1 ELSE 0 END), 1) AS perc_preventiva
FROM agendamento_limpo a
JOIN "Cliente" c ON c."idCliente" = a."idCliente"
JOIN "TipoServico" ts ON ts."idTipoServico" = a."idTipoServico"
GROUP BY 1
ORDER BY 1;
