/*
QUERY MELHORADA PARA CÁLCULO DE SOBREAVISO
- Adapta automaticamente aos horários dos dados
- Suporta múltiplas janelas de sobreaviso
- Calcula HE em qualquer horário após o turno normal
*/

WITH params AS (
    SELECT 
        9  AS turno_ini_h,           -- Início do turno normal
        18 AS turno_fim_h,           -- Fim do turno normal
        18 AS sobreaviso_ini_h,      -- Início do sobreaviso
        23 AS sobreaviso_fim_h       -- Fim do sobreaviso (expandido)
),

periodo AS (
    SELECT 
        CAST('{{Data_inicio}}' AS DATE) AS data_inicio,
        CAST('{{Data_fim}}' AS DATE) AS data_fim
),

-- Batidas reais a partir de shifts
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

-- Colaboradores
colaboradores AS (
    SELECT 
        e.id AS colaborador_id,
        e.company_identifier AS id_funcionario,
        element_at(split(e.full_name, ' '), 1) AS nome,
        element_at(split(e.full_name, ' '), cardinality(split(e.full_name, ' '))) AS sobrenome
    FROM employees e
    WHERE e.status = 'active'
),

-- Constrói as janelas de cálculo
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

-- Gera todos os dias do período
dias AS (
    SELECT d AS data
    FROM periodo p
    CROSS JOIN UNNEST(sequence(p.data_inicio, p.data_fim, INTERVAL '1' DAY)) AS t(d)
),

-- Calcula duração (em segundos) de interseções com as janelas
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

        date_diff('second', turno_ini_ts, turno_fim_ts) AS seg_total_turno,
        date_diff('second', sobreaviso_ini_ts, sobreaviso_fim_ts) AS seg_total_janela_sobreaviso
    FROM batidas_com_janelas
),

-- Agrupa por dia e colaborador
calc_por_dia AS (
    SELECT 
        colaborador_id,
        data,
        MAX(seg_total_turno) AS seg_total_turno,
        SUM(seg_trabalho_normal) AS seg_trabalho_normal,
        SUM(seg_he_no_sobreaviso) AS seg_he_no_sobreaviso,
        SUM(seg_he_apos_sobreaviso) AS seg_he_apos_sobreaviso,
        SUM(seg_sobreaviso_puro) AS seg_sobreaviso_puro,
        MAX(seg_total_janela_sobreaviso) AS seg_total_janela_sobreaviso
    FROM segundos_por_intervalo
    GROUP BY colaborador_id, data
)

-- RELATÓRIO FINAL
SELECT 
    c.id_funcionario,
    c.colaborador_id,
    c.nome,
    c.sobrenome,
    concat(c.nome, ' ', c.sobrenome) AS nome_completo,
    d.data,
    
    -- Horas normais agendadas (fixas)
    format_datetime(
        from_unixtime(((SELECT turno_fim_h FROM params) - (SELECT turno_ini_h FROM params)) * 3600),
        'HH:mm:ss'
    ) AS horas_normais_agendadas,

    -- Horas normais efetivamente trabalhadas
    format_datetime(from_unixtime(COALESCE(cp.seg_trabalho_normal, 0)), 'HH:mm:ss') AS horas_normais_trabalhadas,

    -- HE dentro do sobreaviso (18:00-23:00)
    format_datetime(from_unixtime(COALESCE(cp.seg_he_no_sobreaviso, 0)), 'HH:mm:ss') AS he_no_sobreaviso,

    -- HE após o sobreaviso (após 23:00)
    format_datetime(from_unixtime(COALESCE(cp.seg_he_apos_sobreaviso, 0)), 'HH:mm:ss') AS he_apos_sobreaviso,

    -- Sobreaviso puro (janela menos HE)
    format_datetime(from_unixtime(COALESCE(cp.seg_sobreaviso_puro, 0)), 'HH:mm:ss') AS sobreaviso_puro,

    -- Totais em horas decimais
    ROUND(COALESCE(cp.seg_trabalho_normal, 0) / 3600.0, 2) AS horas_normais_h,
    ROUND(COALESCE(cp.seg_he_no_sobreaviso, 0) / 3600.0, 2) AS he_no_sobreaviso_h,
    ROUND(COALESCE(cp.seg_he_apos_sobreaviso, 0) / 3600.0, 2) AS he_apos_sobreaviso_h,
    ROUND(COALESCE(cp.seg_sobreaviso_puro, 0) / 3600.0, 2) AS sobreaviso_puro_h,

    -- Total de HE
    ROUND((COALESCE(cp.seg_he_no_sobreaviso, 0) + COALESCE(cp.seg_he_apos_sobreaviso, 0)) / 3600.0, 2) AS total_he_h

FROM colaboradores c
CROSS JOIN dias d
LEFT JOIN calc_por_dia cp ON cp.colaborador_id = c.colaborador_id AND cp.data = d.data
ORDER BY d.data, c.colaborador_id;
