/*
🎯 QUERY SIMPLES PARA RELATÓRIOS DE SOBREAVISO
Versão otimizada para usar diretamente no ambiente demo da Factorial
Atende todos os requisitos: separação de eventos, visualização detalhada, exportação
*/

-- PARÂMETROS CONFIGURÁVEIS (ajuste conforme necessário)
WITH params AS (
    SELECT 
        9  AS turno_ini_h,           -- Início do turno normal (09:00)
        18 AS turno_fim_h,           -- Fim do turno normal (18:00)
        18 AS sobreaviso_ini_h,      -- Início do sobreaviso (18:00)
        23 AS sobreaviso_fim_h,      -- Fim do sobreaviso (23:00)
        22 AS hora_noturna_ini,      -- Início do adicional noturno (22:00)
        6  AS hora_noturna_fim,      -- Fim do adicional noturno (06:00)
        '001' AS codigo_empresa,     -- Código da empresa para Sankhya
        'HE70' AS codigo_he_sobreaviso,  -- Código HE no sobreaviso
        'HE100' AS codigo_he_apos,   -- Código HE após sobreaviso
        'SOB50' AS codigo_sobreaviso, -- Código sobreaviso puro
        'NOT20' AS codigo_noturno,   -- Código adicional noturno
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

-- DADOS DOS COLABORADORES
colaboradores AS (
    SELECT 
        e.id AS colaborador_id,
        e.company_identifier AS id_funcionario,
        e.full_name AS nome_completo,
        element_at(split(e.full_name, ' '), 1) AS nome,
        element_at(split(e.full_name, ' '), cardinality(split(e.full_name, ' '))) AS sobrenome,
        e.email
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
        date_add('hour', (SELECT sobreaviso_fim_h FROM params), CAST(b.data AS TIMESTAMP)) AS sobreaviso_fim_ts,
        -- Adicional noturno (considera virada de dia)
        CASE 
            WHEN (SELECT hora_noturna_ini FROM params) > (SELECT hora_noturna_fim FROM params) THEN
                date_add('hour', (SELECT hora_noturna_ini FROM params), CAST(b.data AS TIMESTAMP))
            ELSE
                date_add('hour', (SELECT hora_noturna_ini FROM params), CAST(b.data AS TIMESTAMP))
        END AS noturno_ini_ts,
        CASE 
            WHEN (SELECT hora_noturna_ini FROM params) > (SELECT hora_noturna_fim FROM params) THEN
                date_add('hour', (SELECT hora_noturna_fim FROM params), date_add('day', 1, CAST(b.data AS TIMESTAMP)))
            ELSE
                date_add('hour', (SELECT hora_noturna_fim FROM params), CAST(b.data AS TIMESTAMP))
        END AS noturno_fim_ts
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
        entrada,
        saida,
        
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

        -- Horas noturnas (22:00-06:00)
        CASE 
            WHEN entrada < noturno_fim_ts AND saida > noturno_ini_ts THEN
                GREATEST(0, date_diff('second', 
                    greatest(entrada, noturno_ini_ts), 
                    least(saida, noturno_fim_ts)
                ))
            ELSE 0
        END AS seg_horas_noturnas,

        -- Banco de horas (déficit de horas normais)
        CASE 
            WHEN date_diff('second', turno_ini_ts, turno_fim_ts) > 
                 GREATEST(0, date_diff('second', greatest(entrada, turno_ini_ts), least(saida, turno_fim_ts))) THEN
                date_diff('second', turno_ini_ts, turno_fim_ts) - 
                GREATEST(0, date_diff('second', greatest(entrada, turno_ini_ts), least(saida, turno_fim_ts)))
            ELSE 0
        END AS seg_banco_horas_deficit,

        date_diff('second', turno_ini_ts, turno_fim_ts) AS seg_total_turno,
        date_diff('second', sobreaviso_ini_ts, sobreaviso_fim_ts) AS seg_total_janela_sobreaviso
    FROM batidas_com_janelas
),

-- AGREGA POR DIA E COLABORADOR
calc_por_dia AS (
    SELECT 
        colaborador_id,
        data,
        MAX(seg_total_turno) AS seg_total_turno,
        SUM(seg_trabalho_normal) AS seg_trabalho_normal,
        SUM(seg_he_no_sobreaviso) AS seg_he_no_sobreaviso,
        SUM(seg_he_apos_sobreaviso) AS seg_he_apos_sobreaviso,
        SUM(seg_sobreaviso_puro) AS seg_sobreaviso_puro,
        SUM(seg_horas_noturnas) AS seg_horas_noturnas,
        SUM(seg_banco_horas_deficit) AS seg_banco_horas_deficit,
        MAX(seg_total_janela_sobreaviso) AS seg_total_janela_sobreaviso
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
        SUM(seg_horas_noturnas) AS seg_horas_noturnas_mes,
        SUM(seg_banco_horas_deficit) AS seg_banco_horas_deficit_mes
    FROM calc_por_dia
    GROUP BY colaborador_id, EXTRACT(YEAR FROM data), EXTRACT(MONTH FROM data)
)

-- 🎯 RELATÓRIO FINAL COMPLETO
SELECT 
    -- DADOS BÁSICOS DO COLABORADOR
    c.id_funcionario,
    c.colaborador_id,
    c.nome_completo,
    c.nome,
    c.sobrenome,
    c.email,
    
    -- DADOS DO PERÍODO
    d.data,
    EXTRACT(YEAR FROM d.data) AS ano,
    EXTRACT(MONTH FROM d.data) AS mes,
    EXTRACT(DAY FROM d.data) AS dia,
    EXTRACT(DOW FROM d.data) AS dia_semana,
    
    -- HORÁRIOS DE REFERÊNCIA
    format_datetime(
        from_unixtime(((SELECT turno_ini_h FROM params) * 3600)),
        'HH:mm:ss'
    ) AS turno_ini_horario,
    format_datetime(
        from_unixtime(((SELECT turno_fim_h FROM params) * 3600)),
        'HH:mm:ss'
    ) AS turno_fim_horario,
    format_datetime(
        from_unixtime(((SELECT sobreaviso_ini_h FROM params) * 3600)),
        'HH:mm:ss'
    ) AS sobreaviso_ini_horario,
    format_datetime(
        from_unixtime(((SELECT sobreaviso_fim_h FROM params) * 3600)),
        'HH:mm:ss'
    ) AS sobreaviso_fim_horario,
    
    -- HORAS NORMAIS
    format_datetime(from_unixtime(COALESCE(cp.seg_trabalho_normal, 0)), 'HH:mm:ss') AS horas_normais_trabalhadas,
    ROUND(COALESCE(cp.seg_trabalho_normal, 0) / 3600.0, 2) AS horas_normais_h,
    
    -- EVENTOS DE HORA EXTRA
    format_datetime(from_unixtime(COALESCE(cp.seg_he_no_sobreaviso, 0)), 'HH:mm:ss') AS he_no_sobreaviso,
    ROUND(COALESCE(cp.seg_he_no_sobreaviso, 0) / 3600.0, 2) AS he_no_sobreaviso_h,
    
    format_datetime(from_unixtime(COALESCE(cp.seg_he_apos_sobreaviso, 0)), 'HH:mm:ss') AS he_apos_sobreaviso,
    ROUND(COALESCE(cp.seg_he_apos_sobreaviso, 0) / 3600.0, 2) AS he_apos_sobreaviso_h,
    
    -- Total de hora extra
    ROUND((COALESCE(cp.seg_he_no_sobreaviso, 0) + COALESCE(cp.seg_he_apos_sobreaviso, 0)) / 3600.0, 2) AS total_he_h,
    
    -- EVENTOS DE SOBREAVISO
    format_datetime(from_unixtime(COALESCE(cp.seg_sobreaviso_puro, 0)), 'HH:mm:ss') AS sobreaviso_puro,
    ROUND(COALESCE(cp.seg_sobreaviso_puro, 0) / 3600.0, 2) AS sobreaviso_puro_h,
    
    -- EVENTOS DE BANCO DE HORAS
    format_datetime(from_unixtime(COALESCE(cp.seg_banco_horas_deficit, 0)), 'HH:mm:ss') AS banco_horas_deficit,
    ROUND(COALESCE(cp.seg_banco_horas_deficit, 0) / 3600.0, 2) AS banco_horas_deficit_h,
    
    -- HORAS NOTURNAS
    format_datetime(from_unixtime(COALESCE(cp.seg_horas_noturnas, 0)), 'HH:mm:ss') AS horas_noturnas,
    ROUND(COALESCE(cp.seg_horas_noturnas, 0) / 3600.0, 2) AS horas_noturnas_h,
    
    -- CÓDIGOS PARA SISTEMA SANKHYA
    (SELECT codigo_empresa FROM params) AS codigo_empresa,
    (SELECT codigo_he_sobreaviso FROM params) AS codigo_he_sobreaviso,
    (SELECT codigo_he_apos FROM params) AS codigo_he_apos,
    (SELECT codigo_sobreaviso FROM params) AS codigo_sobreaviso,
    (SELECT codigo_noturno FROM params) AS codigo_noturno,
    (SELECT codigo_banco FROM params) AS codigo_banco,
    
    -- CÓDIGOS DE EVENTO ESPECÍFICOS
    CASE 
        WHEN COALESCE(cp.seg_he_no_sobreaviso, 0) > 0 THEN (SELECT codigo_he_sobreaviso FROM params)
        ELSE NULL
    END AS codigo_evento_he_sobreaviso,
    
    CASE 
        WHEN COALESCE(cp.seg_he_apos_sobreaviso, 0) > 0 THEN (SELECT codigo_he_apos FROM params)
        ELSE NULL
    END AS codigo_evento_he_apos,
    
    CASE 
        WHEN COALESCE(cp.seg_sobreaviso_puro, 0) > 0 THEN (SELECT codigo_sobreaviso FROM params)
        ELSE NULL
    END AS codigo_evento_sobreaviso,
    
    CASE 
        WHEN COALESCE(cp.seg_horas_noturnas, 0) > 0 THEN (SELECT codigo_noturno FROM params)
        ELSE NULL
    END AS codigo_evento_noturno,
    
    CASE 
        WHEN COALESCE(cp.seg_banco_horas_deficit, 0) > 0 THEN (SELECT codigo_banco FROM params)
        ELSE NULL
    END AS codigo_evento_banco,
    
    -- MÊS DE REFERÊNCIA PARA SANKHYA
    CONCAT(
        CAST(EXTRACT(YEAR FROM d.data) AS VARCHAR), 
        LPAD(CAST(EXTRACT(MONTH FROM d.data) AS VARCHAR), 2, '0')
    ) AS mes_referencia,
    
    -- ACUMULADOS MENSAIS
    ROUND(COALESCE(am.seg_trabalho_normal_mes, 0) / 3600.0, 2) AS horas_normais_mes,
    ROUND(COALESCE(am.seg_he_no_sobreaviso_mes, 0) / 3600.0, 2) AS he_no_sobreaviso_mes,
    ROUND(COALESCE(am.seg_he_apos_sobreaviso_mes, 0) / 3600.0, 2) AS he_apos_sobreaviso_mes,
    ROUND(COALESCE(am.seg_sobreaviso_puro_mes, 0) / 3600.0, 2) AS sobreaviso_puro_mes,
    ROUND(COALESCE(am.seg_horas_noturnas_mes, 0) / 3600.0, 2) AS horas_noturnas_mes,
    ROUND(COALESCE(am.seg_banco_horas_deficit_mes, 0) / 3600.0, 2) AS banco_horas_deficit_mes,
    
    -- TOTAIS MENSAIS
    ROUND((COALESCE(am.seg_he_no_sobreaviso_mes, 0) + COALESCE(am.seg_he_apos_sobreaviso_mes, 0)) / 3600.0, 2) AS total_he_mes,
    
    -- FLAGS DE CONTROLE
    CASE WHEN COALESCE(cp.seg_trabalho_normal, 0) > 0 THEN 1 ELSE 0 END AS teve_trabalho_normal,
    CASE WHEN COALESCE(cp.seg_he_no_sobreaviso, 0) > 0 OR COALESCE(cp.seg_he_apos_sobreaviso, 0) > 0 THEN 1 ELSE 0 END AS teve_hora_extra,
    CASE WHEN COALESCE(cp.seg_sobreaviso_puro, 0) > 0 THEN 1 ELSE 0 END AS teve_sobreaviso,
    CASE WHEN COALESCE(cp.seg_banco_horas_deficit, 0) > 0 THEN 1 ELSE 0 END AS teve_banco_horas,
    CASE WHEN COALESCE(cp.seg_horas_noturnas, 0) > 0 THEN 1 ELSE 0 END AS teve_horas_noturnas,
    
    -- OBSERVAÇÕES
    CASE 
        WHEN COALESCE(cp.seg_he_no_sobreaviso, 0) > 0 AND COALESCE(cp.seg_sobreaviso_puro, 0) > 0 THEN 'HE + Sobreaviso simultâneos'
        WHEN COALESCE(cp.seg_he_apos_sobreaviso, 0) > 0 THEN 'HE após sobreaviso'
        WHEN COALESCE(cp.seg_sobreaviso_puro, 0) > 0 THEN 'Sobreaviso puro'
        WHEN COALESCE(cp.seg_banco_horas_deficit, 0) > 0 THEN 'Déficit banco de horas'
        WHEN COALESCE(cp.seg_horas_noturnas, 0) > 0 THEN 'Horas noturnas'
        ELSE 'Apenas trabalho normal'
    END AS observacoes

FROM colaboradores c
CROSS JOIN dias d
LEFT JOIN calc_por_dia cp ON cp.colaborador_id = c.colaborador_id AND cp.data = d.data
LEFT JOIN acumulados_mensais am ON am.colaborador_id = c.colaborador_id 
    AND am.ano = EXTRACT(YEAR FROM d.data) 
    AND am.mes = EXTRACT(MONTH FROM d.data)
ORDER BY d.data, c.colaborador_id;
