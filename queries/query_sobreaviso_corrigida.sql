/*
🎯 QUERY CORRIGIDA PARA SOBREAVISO
Corrige o problema de sobreposição entre trabalho regular e sobreaviso
Sobreaviso = disponibilidade, não trabalho efetivo
*/

-- PARÂMETROS
WITH params AS (
    SELECT 
        '001' AS codigo_empresa,
        1 AS horas_almoco
),

-- PERÍODO DE CONSULTA
periodo AS (
    SELECT 
        CAST('{{Data_inicio}}' AS DATE) AS data_inicio,
        CAST('{{Data_fim}}' AS DATE) AS data_fim
),

-- BATIDAS DOS FUNCIONÁRIOS
batidas AS (
    SELECT 
        s.employee_id AS colaborador_id,
        s.date AS data,
        s.clock_in,
        s.clock_out,
        -- Calcular duração em horas
        CASE 
            WHEN s.clock_in IS NOT NULL AND s.clock_out IS NOT NULL THEN
                date_diff('second', 
                    date_parse(CAST(s.date AS VARCHAR) || ' ' || s.clock_in, '%Y-%m-%d %H:%i'),
                    date_parse(CAST(s.date AS VARCHAR) || ' ' || s.clock_out, '%Y-%m-%d %H:%i')
                ) / 3600.0
            ELSE 0
        END AS duracao_horas
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
        e.full_name AS nome_completo
    FROM employees e
    WHERE e.status = 'active'
),

-- NUMERAR BATIDAS POR DIA E COLABORADOR
batidas_numeradas AS (
    SELECT 
        colaborador_id,
        data,
        clock_in,
        clock_out,
        duracao_horas,
        row_number() OVER (PARTITION BY colaborador_id, data ORDER BY clock_in) AS num_batida
    FROM batidas
),

-- AGRUPAR BATIDAS POR DIA E COLABORADOR
batidas_agrupadas AS (
    SELECT 
        colaborador_id,
        data,
        -- Primeira batida
        MAX(CASE WHEN num_batida = 1 THEN clock_in END) AS clock_in_1,
        MAX(CASE WHEN num_batida = 1 THEN clock_out END) AS clock_out_1,
        -- Segunda batida
        MAX(CASE WHEN num_batida = 2 THEN clock_in END) AS clock_in_2,
        MAX(CASE WHEN num_batida = 2 THEN clock_out END) AS clock_out_2,
        -- Terceira batida
        MAX(CASE WHEN num_batida = 3 THEN clock_in END) AS clock_in_3,
        MAX(CASE WHEN num_batida = 3 THEN clock_out END) AS clock_out_3
    FROM batidas_numeradas
    GROUP BY colaborador_id, data
),

-- CALCULAR HORAS REGULARES E SOBREAVISO CORRETAMENTE
calculo_corrigido AS (
    SELECT 
        ba.colaborador_id,
        ba.data,
        ba.clock_in_1,
        ba.clock_out_1,
        ba.clock_in_2,
        ba.clock_out_2,
        ba.clock_in_3,
        ba.clock_out_3,
        
        -- JANELAS DE SOBREAVISO
        CASE 
            -- Segunda a sexta: 19h às 22h
            WHEN EXTRACT(DOW FROM ba.data) BETWEEN 1 AND 5 THEN
                date_parse(CAST(ba.data AS VARCHAR) || ' 19:00', '%Y-%m-%d %H:%i')
            -- Sábado e domingo: 9h às 21h
            WHEN EXTRACT(DOW FROM ba.data) IN (0, 6) THEN
                date_parse(CAST(ba.data AS VARCHAR) || ' 09:00', '%Y-%m-%d %H:%i')
            ELSE NULL
        END AS sobreaviso_ini_ts,
        
        CASE 
            -- Segunda a sexta: 19h às 22h
            WHEN EXTRACT(DOW FROM ba.data) BETWEEN 1 AND 5 THEN
                date_parse(CAST(ba.data AS VARCHAR) || ' 22:00', '%Y-%m-%d %H:%i')
            -- Sábado e domingo: 9h às 21h
            WHEN EXTRACT(DOW FROM ba.data) IN (0, 6) THEN
                date_parse(CAST(ba.data AS VARCHAR) || ' 21:00', '%Y-%m-%d %H:%i')
            ELSE NULL
        END AS sobreaviso_fim_ts
        
    FROM batidas_agrupadas ba
),

-- CALCULAR HORAS REGULARES (SEM SOBREPOSIÇÃO)
horas_regulares AS (
    SELECT 
        cc.*,
        -- HORAS REGULARES: apenas trabalho FORA da janela de sobreaviso
        (
            -- Intervalo 1 (apenas parte fora da janela de sobreaviso)
            CASE 
                WHEN cc.clock_in_1 IS NOT NULL AND cc.clock_out_1 IS NOT NULL 
                     AND cc.clock_in_1 != cc.clock_out_1 THEN
                    GREATEST(0, 
                        date_diff('second', 
                            date_parse(CAST(cc.data AS VARCHAR) || ' ' || cc.clock_in_1, '%Y-%m-%d %H:%i'),
                            LEAST(
                                date_parse(CAST(cc.data AS VARCHAR) || ' ' || cc.clock_out_1, '%Y-%m-%d %H:%i'),
                                COALESCE(cc.sobreaviso_ini_ts, date_parse(CAST(cc.data AS VARCHAR) || ' 23:59', '%Y-%m-%d %H:%i'))
                            )
                        )
                    ) / 3600.0
                ELSE 0
            END +
            -- Intervalo 2 (apenas parte fora da janela de sobreaviso)
            CASE 
                WHEN cc.clock_in_2 IS NOT NULL AND cc.clock_out_2 IS NOT NULL 
                     AND cc.clock_in_2 != cc.clock_out_2 THEN
                    GREATEST(0, 
                        date_diff('second', 
                            date_parse(CAST(cc.data AS VARCHAR) || ' ' || cc.clock_in_2, '%Y-%m-%d %H:%i'),
                            LEAST(
                                date_parse(CAST(cc.data AS VARCHAR) || ' ' || cc.clock_out_2, '%Y-%m-%d %H:%i'),
                                COALESCE(cc.sobreaviso_ini_ts, date_parse(CAST(cc.data AS VARCHAR) || ' 23:59', '%Y-%m-%d %H:%i'))
                            )
                        )
                    ) / 3600.0
                ELSE 0
            END +
            -- Intervalo 3 (apenas parte fora da janela de sobreaviso)
            CASE 
                WHEN cc.clock_in_3 IS NOT NULL AND cc.clock_out_3 IS NOT NULL 
                     AND cc.clock_in_3 != cc.clock_out_3 THEN
                    GREATEST(0, 
                        date_diff('second', 
                            date_parse(CAST(cc.data AS VARCHAR) || ' ' || cc.clock_in_3, '%Y-%m-%d %H:%i'),
                            LEAST(
                                date_parse(CAST(cc.data AS VARCHAR) || ' ' || cc.clock_out_3, '%Y-%m-%d %H:%i'),
                                COALESCE(cc.sobreaviso_ini_ts, date_parse(CAST(cc.data AS VARCHAR) || ' 23:59', '%Y-%m-%d %H:%i'))
                            )
                        )
                    ) / 3600.0
                ELSE 0
            END
        ) AS horas_fora_sobreaviso,
        
        -- Contar intervalos válidos para desconto de almoço
        (
            CASE WHEN cc.clock_in_1 IS NOT NULL AND cc.clock_out_1 IS NOT NULL AND cc.clock_in_1 != cc.clock_out_1 THEN 1 ELSE 0 END +
            CASE WHEN cc.clock_in_2 IS NOT NULL AND cc.clock_out_2 IS NOT NULL AND cc.clock_in_2 != cc.clock_out_2 THEN 1 ELSE 0 END +
            CASE WHEN cc.clock_in_3 IS NOT NULL AND cc.clock_out_3 IS NOT NULL AND cc.clock_in_3 != cc.clock_out_3 THEN 1 ELSE 0 END
        ) AS num_intervalos_validos
        
    FROM calculo_corrigido cc
),

-- CALCULAR SOBREAVISO PURO (APENAS DISPONIBILIDADE)
sobreaviso_puro AS (
    SELECT 
        hr.*,
        -- SOBREAVISO: apenas tempo trabalhado DENTRO da janela, SEM sobreposição com trabalho regular
        CASE 
            WHEN hr.sobreaviso_ini_ts IS NOT NULL THEN
                (
                    -- Intervalo 1 (apenas parte dentro da janela de sobreaviso)
                    CASE 
                        WHEN hr.clock_in_1 IS NOT NULL AND hr.clock_out_1 IS NOT NULL 
                             AND hr.clock_in_1 != hr.clock_out_1 THEN
                            GREATEST(0, 
                                date_diff('second', 
                                    GREATEST(
                                        date_parse(CAST(hr.data AS VARCHAR) || ' ' || hr.clock_in_1, '%Y-%m-%d %H:%i'),
                                        hr.sobreaviso_ini_ts
                                    ),
                                    LEAST(
                                        date_parse(CAST(hr.data AS VARCHAR) || ' ' || hr.clock_out_1, '%Y-%m-%d %H:%i'),
                                        hr.sobreaviso_fim_ts
                                    )
                                )
                            ) / 3600.0
                        ELSE 0
                    END +
                    -- Intervalo 2 (apenas parte dentro da janela de sobreaviso)
                    CASE 
                        WHEN hr.clock_in_2 IS NOT NULL AND hr.clock_out_2 IS NOT NULL 
                             AND hr.clock_in_2 != hr.clock_out_2 THEN
                            GREATEST(0, 
                                date_diff('second', 
                                    GREATEST(
                                        date_parse(CAST(hr.data AS VARCHAR) || ' ' || hr.clock_in_2, '%Y-%m-%d %H:%i'),
                                        hr.sobreaviso_ini_ts
                                    ),
                                    LEAST(
                                        date_parse(CAST(hr.data AS VARCHAR) || ' ' || hr.clock_out_2, '%Y-%m-%d %H:%i'),
                                        hr.sobreaviso_fim_ts
                                    )
                                )
                            ) / 3600.0
                        ELSE 0
                    END +
                    -- Intervalo 3 (apenas parte dentro da janela de sobreaviso)
                    CASE 
                        WHEN hr.clock_in_3 IS NOT NULL AND hr.clock_out_3 IS NOT NULL 
                             AND hr.clock_in_3 != hr.clock_out_3 THEN
                            GREATEST(0, 
                                date_diff('second', 
                                    GREATEST(
                                        date_parse(CAST(hr.data AS VARCHAR) || ' ' || hr.clock_in_3, '%Y-%m-%d %H:%i'),
                                        hr.sobreaviso_ini_ts
                                    ),
                                    LEAST(
                                        date_parse(CAST(hr.data AS VARCHAR) || ' ' || hr.clock_out_3, '%Y-%m-%d %H:%i'),
                                        hr.sobreaviso_fim_ts
                                    )
                                )
                            ) / 3600.0
                        ELSE 0
                    END
                )
            ELSE 0
        END AS horas_sobreaviso_calculadas
        
    FROM horas_regulares hr
),

-- GERAR TODOS OS DIAS DO PERÍODO
dias AS (
    SELECT d AS data
    FROM periodo p
    CROSS JOIN UNNEST(sequence(p.data_inicio, p.data_fim, INTERVAL '1' DAY)) AS t(d)
)

-- 🎯 RESULTADO FINAL CORRIGIDO
SELECT 
    c.colaborador_id,
    c.nome_completo,
    d.data,
    COALESCE(sp.clock_in_1, '') AS clock_in_1,
    COALESCE(sp.clock_out_1, '') AS clock_out_1,
    COALESCE(sp.clock_in_2, '') AS clock_in_2,
    COALESCE(sp.clock_out_2, '') AS clock_out_2,
    COALESCE(sp.clock_in_3, '') AS clock_in_3,
    COALESCE(sp.clock_out_3, '') AS clock_out_3,
    (SELECT codigo_empresa FROM params) AS codigo_empresa,
    -- HORAS REGULARES: trabalho fora da janela de sobreaviso - almoço se múltiplos intervalos
    ROUND(
        COALESCE(sp.horas_fora_sobreaviso, 0) - 
        CASE 
            WHEN COALESCE(sp.num_intervalos_validos, 0) > 1 THEN 1.0  -- Desconta 1h de almoço
            ELSE 0.0
        END, 
        2
    ) AS horas_regulares,
    -- HORAS SOBREAVISO: apenas tempo trabalhado dentro da janela (disponibilidade)
    ROUND(COALESCE(sp.horas_sobreaviso_calculadas, 0), 2) AS horas_sobreaviso_regra

FROM colaboradores c
CROSS JOIN dias d
LEFT JOIN sobreaviso_puro sp ON sp.colaborador_id = c.colaborador_id AND sp.data = d.data
ORDER BY d.data, c.colaborador_id;
