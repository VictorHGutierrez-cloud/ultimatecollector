/*
🎯 QUERY MÍNIMA PARA RELATÓRIOS DE SOBREAVISO
Versão simplificada para ambiente demo da Factorial
Apenas campos essenciais e compatíveis
*/

-- PARÂMETROS CONFIGURÁVEIS
WITH params AS (
    SELECT 
        9  AS turno_ini_h,           -- Início do turno normal (09:00)
        18 AS turno_fim_h,           -- Fim do turno normal (18:00)
        18 AS sobreaviso_ini_h,      -- Início do sobreaviso (18:00)
        23 AS sobreaviso_fim_h,      -- Fim do sobreaviso (23:00)
        '001' AS codigo_empresa,     -- Código da empresa para Sankhya
        'HE70' AS codigo_he_sobreaviso,  -- Código HE no sobreaviso
        'HE100' AS codigo_he_apos,   -- Código HE após sobreaviso
        'SOB50' AS codigo_sobreaviso, -- Código sobreaviso puro
        'BNC' AS codigo_banco        -- Código banco de horas
),

-- PERÍODO DE CONSULTA (usa os filtros do ambiente)
periodo AS (
    SELECT 
        CAST('{{Data_inicio}}' AS DATE) AS data_inicio,
        CAST('{{Data_fim}}' AS DATE) AS data_fim
),

-- BATIDAS REAIS DOS FUNCIONÁRIOS
batidas AS (
    SELECT 
        s.employee_id AS colaborador_id,
        s.date AS data,
        date_parse(CAST(s.date AS VARCHAR) || ' ' || s.clock_in, '%Y-%m-%d %H:%i') AS entrada,
        date_parse(CAST(s.date AS VARCHAR) || ' ' || s.clock_out, '%Y-%m-%d %H:%i') AS saida
    FROM shifts s
    JOIN employees e ON e.id = s.employee_id
    JOIN periodo p ON s.date BETWEEN p.data_inicio AND p.data_fim
    WHERE e.status = 'active'
      AND s.clock_in IS NOT NULL
      AND s.clock_out IS NOT NULL
),

-- DADOS DOS COLABORADORES (apenas campos essenciais)
colaboradores AS (
    SELECT 
        e.id AS colaborador_id,
        e.company_identifier AS id_funcionario,
        e.full_name AS nome_completo
    FROM employees e
    WHERE e.status = 'active'
),

-- JANELAS DE CÁLCULO
batidas_com_janelas AS (
    SELECT 
        b.colaborador_id,
        b.data,
        b.entrada,
        b.saida,
        -- Turno normal
        date_add('hour', (SELECT turno_ini_h FROM params), CAST(b.data AS TIMESTAMP)) AS turno_ini_ts,
        date_add('hour', (SELECT turno_fim_h FROM params), CAST(b.data AS TIMESTAMP)) AS turno_fim_ts,
        -- Sobreaviso
        date_add('hour', (SELECT sobreaviso_ini_h FROM params), CAST(b.data AS TIMESTAMP)) AS sobreaviso_ini_ts,
        date_add('hour', (SELECT sobreaviso_fim_h FROM params), CAST(b.data AS TIMESTAMP)) AS sobreaviso_fim_ts
    FROM batidas b
),

-- GERA TODOS OS DIAS DO PERÍODO
dias AS (
    SELECT d AS data
    FROM periodo p
    CROSS JOIN UNNEST(sequence(p.data_inicio, p.data_fim, INTERVAL '1' DAY)) AS t(d)
),

-- CALCULA SEGUNDOS POR INTERVALO
segundos_por_intervalo AS (
    SELECT 
        colaborador_id,
        data,
        
        -- Horas normais (dentro do turno 09:00-18:00)
        GREATEST(
            0,
            date_diff('second', greatest(entrada, turno_ini_ts), least(saida, turno_fim_ts))
        ) AS seg_trabalho_normal,

        -- HE dentro do sobreaviso (18:00-23:00)
        GREATEST(
            0,
            date_diff('second', greatest(entrada, sobreaviso_ini_ts), least(saida, sobreaviso_fim_ts))
        ) AS seg_he_no_sobreaviso,

        -- HE após o sobreaviso (após 23:00)
        CASE 
            WHEN saida > sobreaviso_fim_ts THEN
                GREATEST(0, date_diff('second', greatest(entrada, sobreaviso_fim_ts), saida))
            ELSE 0
        END AS seg_he_apos_sobreaviso,

        -- Sobreaviso puro (janela menos HE dentro da janela)
        GREATEST(0,
            date_diff('second', sobreaviso_ini_ts, sobreaviso_fim_ts) - 
            GREATEST(0, date_diff('second', greatest(entrada, sobreaviso_ini_ts), least(saida, sobreaviso_fim_ts)))
        ) AS seg_sobreaviso_puro,

        -- Banco de horas (déficit de horas normais)
        CASE 
            WHEN date_diff('second', turno_ini_ts, turno_fim_ts) > 
                 GREATEST(0, date_diff('second', greatest(entrada, turno_ini_ts), least(saida, turno_fim_ts))) THEN
                date_diff('second', turno_ini_ts, turno_fim_ts) - 
                GREATEST(0, date_diff('second', greatest(entrada, turno_ini_ts), least(saida, turno_fim_ts)))
            ELSE 0
        END AS seg_banco_horas_deficit

    FROM batidas_com_janelas
),

-- AGREGA POR DIA E COLABORADOR
calc_por_dia AS (
    SELECT 
        colaborador_id,
        data,
        SUM(seg_trabalho_normal) AS seg_trabalho_normal,
        SUM(seg_he_no_sobreaviso) AS seg_he_no_sobreaviso,
        SUM(seg_he_apos_sobreaviso) AS seg_he_apos_sobreaviso,
        SUM(seg_sobreaviso_puro) AS seg_sobreaviso_puro,
        SUM(seg_banco_horas_deficit) AS seg_banco_horas_deficit
    FROM segundos_por_intervalo
    GROUP BY colaborador_id, data
),

-- ACUMULADOS MENSAIS
acumulados_mensais AS (
    SELECT 
        colaborador_id,
        EXTRACT(YEAR FROM data) AS ano,
        EXTRACT(MONTH FROM data) AS mes,
        SUM(seg_trabalho_normal) AS seg_trabalho_normal_mes,
        SUM(seg_he_no_sobreaviso) AS seg_he_no_sobreaviso_mes,
        SUM(seg_he_apos_sobreaviso) AS seg_he_apos_sobreaviso_mes,
        SUM(seg_sobreaviso_puro) AS seg_sobreaviso_puro_mes,
        SUM(seg_banco_horas_deficit) AS seg_banco_horas_deficit_mes
    FROM calc_por_dia
    GROUP BY colaborador_id, EXTRACT(YEAR FROM data), EXTRACT(MONTH FROM data)
)

-- 🎯 RELATÓRIO FINAL SIMPLIFICADO
SELECT 
    -- DADOS BÁSICOS DO COLABORADOR
    c.id_funcionario,
    c.colaborador_id,
    c.nome_completo,
    
    -- DADOS DO PERÍODO
    d.data,
    EXTRACT(YEAR FROM d.data) AS ano,
    EXTRACT(MONTH FROM d.data) AS mes,
    EXTRACT(DAY FROM d.data) AS dia,
    
    -- HORAS NORMAIS
    format_datetime(from_unixtime(COALESCE(cp.seg_trabalho_normal, 0)), 'HH:mm') AS horas_normais_hhmm,
    ROUND(COALESCE(cp.seg_trabalho_normal, 0) / 3600.0, 2) AS horas_normais_h,
    
    -- EVENTOS DE HORA EXTRA
    format_datetime(from_unixtime(COALESCE(cp.seg_he_no_sobreaviso, 0)), 'HH:mm') AS he_no_sobreaviso_hhmm,
    ROUND(COALESCE(cp.seg_he_no_sobreaviso, 0) / 3600.0, 2) AS he_no_sobreaviso_h,
    
    format_datetime(from_unixtime(COALESCE(cp.seg_he_apos_sobreaviso, 0)), 'HH:mm') AS he_apos_sobreaviso_hhmm,
    ROUND(COALESCE(cp.seg_he_apos_sobreaviso, 0) / 3600.0, 2) AS he_apos_sobreaviso_h,
    
    format_datetime(from_unixtime(COALESCE(cp.seg_he_no_sobreaviso, 0) + COALESCE(cp.seg_he_apos_sobreaviso, 0)), 'HH:mm') AS total_he_hhmm,
    ROUND((COALESCE(cp.seg_he_no_sobreaviso, 0) + COALESCE(cp.seg_he_apos_sobreaviso, 0)) / 3600.0, 2) AS total_he_h,
    
    -- EVENTOS DE SOBREAVISO
    format_datetime(from_unixtime(COALESCE(cp.seg_sobreaviso_puro, 0)), 'HH:mm') AS sobreaviso_puro_hhmm,
    ROUND(COALESCE(cp.seg_sobreaviso_puro, 0) / 3600.0, 2) AS sobreaviso_puro_h,
    
    -- EVENTOS DE BANCO DE HORAS
    format_datetime(from_unixtime(COALESCE(cp.seg_banco_horas_deficit, 0)), 'HH:mm') AS banco_horas_deficit_hhmm,
    ROUND(COALESCE(cp.seg_banco_horas_deficit, 0) / 3600.0, 2) AS banco_horas_deficit_h,
    
    -- CÓDIGOS PARA SISTEMA SANKHYA
    (SELECT codigo_empresa FROM params) AS codigo_empresa,
    (SELECT codigo_he_sobreaviso FROM params) AS codigo_he_sobreaviso,
    (SELECT codigo_he_apos FROM params) AS codigo_he_apos,
    (SELECT codigo_sobreaviso FROM params) AS codigo_sobreaviso,
    (SELECT codigo_banco FROM params) AS codigo_banco,
    
    -- MÊS DE REFERÊNCIA PARA SANKHYA
    CONCAT(
        CAST(EXTRACT(YEAR FROM d.data) AS VARCHAR), 
        LPAD(CAST(EXTRACT(MONTH FROM d.data) AS VARCHAR), 2, '0')
    ) AS mes_referencia,
    
    -- ACUMULADOS MENSAIS (HH:MM)
    format_datetime(from_unixtime(COALESCE(am.seg_trabalho_normal_mes, 0)), 'HH:mm') AS horas_normais_mes_hhmm,
    ROUND(COALESCE(am.seg_trabalho_normal_mes, 0) / 3600.0, 2) AS horas_normais_mes,
    
    format_datetime(from_unixtime(COALESCE(am.seg_he_no_sobreaviso_mes, 0)), 'HH:mm') AS he_no_sobreaviso_mes_hhmm,
    ROUND(COALESCE(am.seg_he_no_sobreaviso_mes, 0) / 3600.0, 2) AS he_no_sobreaviso_mes,
    
    format_datetime(from_unixtime(COALESCE(am.seg_he_apos_sobreaviso_mes, 0)), 'HH:mm') AS he_apos_sobreaviso_mes_hhmm,
    ROUND(COALESCE(am.seg_he_apos_sobreaviso_mes, 0) / 3600.0, 2) AS he_apos_sobreaviso_mes,
    
    format_datetime(from_unixtime(COALESCE(am.seg_sobreaviso_puro_mes, 0)), 'HH:mm') AS sobreaviso_puro_mes_hhmm,
    ROUND(COALESCE(am.seg_sobreaviso_puro_mes, 0) / 3600.0, 2) AS sobreaviso_puro_mes,
    
    format_datetime(from_unixtime(COALESCE(am.seg_banco_horas_deficit_mes, 0)), 'HH:mm') AS banco_horas_deficit_mes_hhmm,
    ROUND(COALESCE(am.seg_banco_horas_deficit_mes, 0) / 3600.0, 2) AS banco_horas_deficit_mes,
    
    -- TOTAIS MENSAIS (HH:MM)
    format_datetime(from_unixtime(COALESCE(am.seg_he_no_sobreaviso_mes, 0) + COALESCE(am.seg_he_apos_sobreaviso_mes, 0)), 'HH:mm') AS total_he_mes_hhmm,
    ROUND((COALESCE(am.seg_he_no_sobreaviso_mes, 0) + COALESCE(am.seg_he_apos_sobreaviso_mes, 0)) / 3600.0, 2) AS total_he_mes,
    
    -- FLAGS DE CONTROLE
    CASE WHEN COALESCE(cp.seg_trabalho_normal, 0) > 0 THEN 1 ELSE 0 END AS teve_trabalho_normal,
    CASE WHEN COALESCE(cp.seg_he_no_sobreaviso, 0) > 0 OR COALESCE(cp.seg_he_apos_sobreaviso, 0) > 0 THEN 1 ELSE 0 END AS teve_hora_extra,
    CASE WHEN COALESCE(cp.seg_sobreaviso_puro, 0) > 0 THEN 1 ELSE 0 END AS teve_sobreaviso,
    CASE WHEN COALESCE(cp.seg_banco_horas_deficit, 0) > 0 THEN 1 ELSE 0 END AS teve_banco_horas,
    
    -- OBSERVAÇÕES
    CASE 
        WHEN COALESCE(cp.seg_he_no_sobreaviso, 0) > 0 AND COALESCE(cp.seg_sobreaviso_puro, 0) > 0 THEN 'HE + Sobreaviso simultâneos'
        WHEN COALESCE(cp.seg_he_apos_sobreaviso, 0) > 0 THEN 'HE após sobreaviso'
        WHEN COALESCE(cp.seg_sobreaviso_puro, 0) > 0 THEN 'Sobreaviso puro'
        WHEN COALESCE(cp.seg_banco_horas_deficit, 0) > 0 THEN 'Déficit banco de horas'
        ELSE 'Apenas trabalho normal'
    END AS observacoes

FROM colaboradores c
CROSS JOIN dias d
LEFT JOIN calc_por_dia cp ON cp.colaborador_id = c.colaborador_id AND cp.data = d.data
LEFT JOIN acumulados_mensais am ON am.colaborador_id = c.colaborador_id 
    AND am.ano = EXTRACT(YEAR FROM d.data) 
    AND am.mes = EXTRACT(MONTH FROM d.data)
ORDER BY d.data, c.colaborador_id;
