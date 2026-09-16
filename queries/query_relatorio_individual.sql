/*
🎯 QUERY PARA RELATÓRIO INDIVIDUAL DE SOBREAVISO
Gera dados para criar visualização similar ao demonstrativo mostrado
Estrutura: Jornada Regular | Sobreaviso | Eventos do Dia
*/

-- PARÂMETROS
WITH params AS (
    SELECT 
        '001' AS codigo_empresa,
        1 AS horas_almoco,
        8 AS jornada_padrao_horas  -- Jornada padrão de 8h
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
        -- Primeira batida (jornada regular)
        MAX(CASE WHEN num_batida = 1 THEN clock_in END) AS entrada_1,
        MAX(CASE WHEN num_batida = 1 THEN clock_out END) AS saida_1,
        -- Segunda batida (volta do almoço)
        MAX(CASE WHEN num_batida = 2 THEN clock_in END) AS entrada_2,
        MAX(CASE WHEN num_batida = 2 THEN clock_out END) AS saida_2,
        -- Terceira batida (sobreaviso)
        MAX(CASE WHEN num_batida = 3 THEN clock_in END) AS entrada_3,
        MAX(CASE WHEN num_batida = 3 THEN clock_out END) AS saida_3
    FROM batidas_numeradas
    GROUP BY colaborador_id, data
),

-- CALCULAR JORNADA REGULAR E SOBREAVISO
calculo_jornada AS (
    SELECT 
        ba.colaborador_id,
        ba.data,
        ba.entrada_1,
        ba.saida_1,
        ba.entrada_2,
        ba.saida_2,
        ba.entrada_3,
        ba.saida_3,
        
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

-- CALCULAR HORAS TRABALHADAS E INTERVALOS
calculo_horas AS (
    SELECT 
        cj.*,
        
        -- HORAS TRABALHADAS (jornada regular)
        (
            -- Período 1: entrada_1 até saida_1
            CASE 
                WHEN cj.entrada_1 IS NOT NULL AND cj.saida_1 IS NOT NULL 
                     AND cj.entrada_1 != cj.saida_1 THEN
                    date_diff('second', 
                        date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.entrada_1, '%Y-%m-%d %H:%i'),
                        date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.saida_1, '%Y-%m-%d %H:%i')
                    ) / 3600.0
                ELSE 0
            END +
            -- Período 2: entrada_2 até saida_2
            CASE 
                WHEN cj.entrada_2 IS NOT NULL AND cj.saida_2 IS NOT NULL 
                     AND cj.entrada_2 != cj.saida_2 THEN
                    date_diff('second', 
                        date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.entrada_2, '%Y-%m-%d %H:%i'),
                        date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.saida_2, '%Y-%m-%d %H:%i')
                    ) / 3600.0
                ELSE 0
            END
        ) AS hrs_trabalhadas_regular,
        
        -- INTERVALO (almoço)
        CASE 
            WHEN cj.entrada_1 IS NOT NULL AND cj.saida_1 IS NOT NULL 
                 AND cj.entrada_2 IS NOT NULL AND cj.saida_2 IS NOT NULL THEN
                date_diff('second', 
                    date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.saida_1, '%Y-%m-%d %H:%i'),
                    date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.entrada_2, '%Y-%m-%d %H:%i')
                ) / 3600.0
            ELSE 0
        END AS intervalo_horas,
        
        -- HORAS TRABALHADAS NO SOBREAVISO
        CASE 
            WHEN cj.entrada_3 IS NOT NULL AND cj.saida_3 IS NOT NULL 
                 AND cj.entrada_3 != cj.saida_3 THEN
                date_diff('second', 
                    date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.entrada_3, '%Y-%m-%d %H:%i'),
                    date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.saida_3, '%Y-%m-%d %H:%i')
                ) / 3600.0
            ELSE 0
        END AS hrs_trabalhadas_sobreaviso,
        
        -- TEMPO SOBREAVISO (disponibilidade)
        CASE 
            WHEN cj.entrada_3 IS NOT NULL AND cj.saida_3 IS NOT NULL 
                 AND cj.sobreaviso_ini_ts IS NOT NULL THEN
                GREATEST(0, 
                    date_diff('second', 
                        GREATEST(
                            date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.entrada_3, '%Y-%m-%d %H:%i'),
                            cj.sobreaviso_ini_ts
                        ),
                        LEAST(
                            date_parse(CAST(cj.data AS VARCHAR) || ' ' || cj.saida_3, '%Y-%m-%d %H:%i'),
                            cj.sobreaviso_fim_ts
                        )
                    )
                ) / 3600.0
            ELSE 0
        END AS tempo_sobreaviso
        
    FROM calculo_jornada cj
),

-- CALCULAR SALDOS E EVENTOS
calculo_eventos AS (
    SELECT 
        ch.*,
        
        -- SALDO POSITIVO/NEGATIVO (banco de horas)
        CASE 
            WHEN ch.hrs_trabalhadas_regular > (SELECT jornada_padrao_horas FROM params) THEN
                ch.hrs_trabalhadas_regular - (SELECT jornada_padrao_horas FROM params)
            ELSE 0
        END AS saldo_positivo,
        
        CASE 
            WHEN ch.hrs_trabalhadas_regular < (SELECT jornada_padrao_horas FROM params) THEN
                (SELECT jornada_padrao_horas FROM params) - ch.hrs_trabalhadas_regular
            ELSE 0
        END AS saldo_negativo,
        
        -- HORAS EXTRAS (trabalho além da jornada)
        GREATEST(0, ch.hrs_trabalhadas_regular - (SELECT jornada_padrao_horas FROM params)) AS he_horas,
        
        -- HORAS EXTRAS NOTURNAS (trabalho noturno)
        CASE 
            WHEN ch.entrada_3 IS NOT NULL AND ch.saida_3 IS NOT NULL THEN
                -- Verificar se trabalhou entre 22h e 6h
                CASE 
                    WHEN EXTRACT(HOUR FROM date_parse(CAST(ch.data AS VARCHAR) || ' ' || ch.entrada_3, '%Y-%m-%d %H:%i')) >= 22 
                         OR EXTRACT(HOUR FROM date_parse(CAST(ch.data AS VARCHAR) || ' ' || ch.entrada_3, '%Y-%m-%d %H:%i')) < 6 THEN
                        ch.hrs_trabalhadas_sobreaviso
                    ELSE 0
                END
            ELSE 0
        END AS he_noturnas
        
    FROM calculo_horas ch
),

-- GERAR TODOS OS DIAS DO PERÍODO
dias AS (
    SELECT d AS data
    FROM periodo p
    CROSS JOIN UNNEST(sequence(p.data_inicio, p.data_fim, INTERVAL '1' DAY)) AS t(d)
)

-- 🎯 RELATÓRIO INDIVIDUAL FINAL
SELECT 
    c.colaborador_id,
    c.nome_completo,
    d.data,
    
    -- JORNADA REGULAR (Esquerda)
    COALESCE(ce.entrada_1, '') AS entrada_1,
    COALESCE(ce.saida_1, '') AS saida_1,
    COALESCE(ce.entrada_2, '') AS entrada_2,
    COALESCE(ce.saida_2, '') AS saida_2,
    ROUND(COALESCE(ce.hrs_trabalhadas_regular, 0), 2) AS hrs_trabalhadas,
    ROUND(COALESCE(ce.intervalo_horas, 0), 2) AS intervalo,
    ROUND(COALESCE(ce.saldo_positivo, 0), 2) AS saldo_positivo,
    ROUND(COALESCE(ce.saldo_negativo, 0), 2) AS saldo_negativo,
    
    -- SOBREAVISO (Meio)
    COALESCE(ce.entrada_2, '') AS entrada_2_sobreaviso,
    COALESCE(ce.entrada_3, '') AS entrada_3_sobreaviso,
    COALESCE(ce.saida_3, '') AS saida_3_sobreaviso,
    ROUND(COALESCE(ce.hrs_trabalhadas_sobreaviso, 0), 2) AS hrs_trabalhadas_sobreaviso,
    ROUND(COALESCE(ce.tempo_sobreaviso, 0), 2) AS tempo_sobreaviso,
    
    -- EVENTOS DO DIA (Direita)
    ROUND(COALESCE(ce.saldo_positivo - ce.saldo_negativo, 0), 2) AS banco_horas,
    ROUND(COALESCE(ce.he_horas, 0), 2) AS he,
    ROUND(COALESCE(ce.he_noturnas, 0), 2) AS he_not,
    ROUND(COALESCE(ce.tempo_sobreaviso, 0), 2) AS sobreaviso,
    
    -- CÓDIGO DA EMPRESA
    (SELECT codigo_empresa FROM params) AS codigo_empresa

FROM colaboradores c
CROSS JOIN dias d
LEFT JOIN calculo_eventos ce ON ce.colaborador_id = c.colaborador_id AND ce.data = d.data
ORDER BY d.data, c.colaborador_id;
