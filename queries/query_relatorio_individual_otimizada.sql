/*
🎯 QUERY PARA RELATÓRIO INDIVIDUAL DE SOBREAVISO
Gera dados para criar visualização similar ao demonstrativo mostrado
Estrutura: Jornada Regular | Sobreaviso | Eventos do Dia
Baseado na query de controle de jornada agrupado
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

-- INTERVALOS DO DIA (linhas originais)
intervalos AS (
    SELECT 
        s.employee_id,
        s.date,
        s.clock_in,
        s.clock_out,
        s.worked,
        s.balance
    FROM shifts s
    WHERE s.date BETWEEN CAST('{{Data_inicio}}' AS DATE) AND CAST('{{Data_fim}}' AS DATE)
),

-- SALDO MENSAL POR COLABORADOR
saldo_mensal AS (
    SELECT 
        employee_id,
        date_trunc('month', date) AS mes,
        CAST(ROUND(MAX(COALESCE(balance, 0)) * 60, 0) AS INTEGER) AS saldo_banco_minutos_mes
    FROM intervalos
    GROUP BY employee_id, date_trunc('month', date)
),

-- CLASSIFICAR INTERVALOS POR ORDEM DE ENTRADA
classificados AS (
    SELECT 
        employee_id,
        date,
        clock_in,
        clock_out,
        worked,
        balance,
        ROW_NUMBER() OVER (PARTITION BY employee_id, date ORDER BY clock_in) AS rn
    FROM intervalos
),

-- AGRUPADO DIÁRIO POR FUNCIONÁRIO E DIA
diario AS (
    SELECT 
        employee_id,
        date,
        -- até 4 pares principais
        MIN(CASE WHEN rn = 1 THEN clock_in END) AS entrada_1,
        MIN(CASE WHEN rn = 1 THEN clock_out END) AS saida_1,
        MIN(CASE WHEN rn = 2 THEN clock_in END) AS entrada_2,
        MIN(CASE WHEN rn = 2 THEN clock_out END) AS saida_2,
        MIN(CASE WHEN rn = 3 THEN clock_in END) AS entrada_3,
        MIN(CASE WHEN rn = 3 THEN clock_out END) AS saida_3,
        MIN(CASE WHEN rn = 4 THEN clock_in END) AS entrada_4,
        MIN(CASE WHEN rn = 4 THEN clock_out END) AS saida_4,
        -- total de batidas (in + out)
        SUM(CASE WHEN clock_in IS NOT NULL THEN 1 ELSE 0 END) + 
        SUM(CASE WHEN clock_out IS NOT NULL THEN 1 ELSE 0 END) AS total_batidas,
        -- soma da presença em minutos (todas as janelas válidas)
        CAST(SUM(CASE 
            WHEN clock_in IS NOT NULL AND clock_out IS NOT NULL THEN 
                date_diff('minute', 
                    date_parse(CAST(date AS VARCHAR) || ' ' || clock_in, '%Y-%m-%d %H:%i'), 
                    date_parse(CAST(date AS VARCHAR) || ' ' || clock_out, '%Y-%m-%d %H:%i')
                )
            ELSE 0
        END) AS INTEGER) AS presenca_minutos,
        -- trabalho em minutos (igual à presença válida por pares)
        CAST(SUM(CASE 
            WHEN clock_in IS NOT NULL AND clock_out IS NOT NULL THEN 
                date_diff('minute', 
                    date_parse(CAST(date AS VARCHAR) || ' ' || clock_in, '%Y-%m-%d %H:%i'), 
                    date_parse(CAST(date AS VARCHAR) || ' ' || clock_out, '%Y-%m-%d %H:%i')
                )
            ELSE 0
        END) AS INTEGER) AS trabalhados_minutos
    FROM classificados
    GROUP BY employee_id, date
),

-- CONSOLIDAR SALDO MENSAL NO DIÁRIO
diario_com_saldo AS (
    SELECT 
        d.*,
        COALESCE(sm.saldo_banco_minutos_mes, 0) AS saldo_banco_minutos
    FROM diario d
    LEFT JOIN saldo_mensal sm
      ON sm.employee_id = d.employee_id
     AND sm.mes = date_trunc('month', d.date)
),

-- DADOS DOS COLABORADORES
colaboradores AS (
    SELECT 
        e.id AS colaborador_id,
        e.full_name AS nome_completo,
        e.company_identifier AS codigo_empresa
    FROM employees e
    WHERE e.status = 'active'
),

-- CALCULAR SOBREAVISO
sobreaviso_calculado AS (
    SELECT 
        d.*,
        -- Definir janela de sobreaviso baseada no dia da semana
        CASE 
            WHEN EXTRACT(DOW FROM d.date) BETWEEN 1 AND 5 THEN -- Seg-Sex
                CASE 
                    WHEN d.entrada_1 IS NOT NULL AND d.saida_1 IS NOT NULL THEN
                        GREATEST(0, LEAST(
                            date_diff('minute', 
                                date_parse(CAST(d.date AS VARCHAR) || ' 19:00', '%Y-%m-%d %H:%i'),
                                date_parse(CAST(d.date AS VARCHAR) || ' ' || d.saida_1, '%Y-%m-%d %H:%i')
                            ),
                            date_diff('minute', 
                                date_parse(CAST(d.date AS VARCHAR) || ' ' || d.entrada_1, '%Y-%m-%d %H:%i'),
                                date_parse(CAST(d.date AS VARCHAR) || ' 22:00', '%Y-%m-%d %H:%i')
                            )
                        ))
                    ELSE 0
                END
            WHEN EXTRACT(DOW FROM d.date) IN (0, 6) THEN -- Dom-Sab
                CASE 
                    WHEN d.entrada_1 IS NOT NULL AND d.saida_1 IS NOT NULL THEN
                        GREATEST(0, LEAST(
                            date_diff('minute', 
                                date_parse(CAST(d.date AS VARCHAR) || ' 09:00', '%Y-%m-%d %H:%i'),
                                date_parse(CAST(d.date AS VARCHAR) || ' ' || d.saida_1, '%Y-%m-%d %H:%i')
                            ),
                            date_diff('minute', 
                                date_parse(CAST(d.date AS VARCHAR) || ' ' || d.entrada_1, '%Y-%m-%d %H:%i'),
                                date_parse(CAST(d.date AS VARCHAR) || ' 21:00', '%Y-%m-%d %H:%i')
                            )
                        ))
                    ELSE 0
                END
            ELSE 0
        END AS sobreaviso_minutos
    FROM diario_com_saldo d
)

-- RESULTADO FINAL
SELECT 
    c.colaborador_id,
    c.nome_completo,
    date_format(CAST(sc.date AS TIMESTAMP), '%d/%m/%Y') AS data,
    
    -- 4 pares de batidas em HH:MM
    CASE WHEN sc.entrada_1 IS NOT NULL THEN date_format(date_parse(CAST(sc.date AS VARCHAR) || ' ' || sc.entrada_1, '%Y-%m-%d %H:%i'), '%H:%i') END AS entrada_1,
    CASE WHEN sc.saida_1   IS NOT NULL THEN date_format(date_parse(CAST(sc.date AS VARCHAR) || ' ' || sc.saida_1,   '%Y-%m-%d %H:%i'), '%H:%i') END AS saida_1,
    CASE WHEN sc.entrada_2 IS NOT NULL THEN date_format(date_parse(CAST(sc.date AS VARCHAR) || ' ' || sc.entrada_2, '%Y-%m-%d %H:%i'), '%H:%i') END AS entrada_2,
    CASE WHEN sc.saida_2   IS NOT NULL THEN date_format(date_parse(CAST(sc.date AS VARCHAR) || ' ' || sc.saida_2,   '%Y-%m-%d %H:%i'), '%H:%i') END AS saida_2,
    CASE WHEN sc.entrada_3 IS NOT NULL THEN date_format(date_parse(CAST(sc.date AS VARCHAR) || ' ' || sc.entrada_3, '%Y-%m-%d %H:%i'), '%H:%i') END AS entrada_3,
    CASE WHEN sc.saida_3   IS NOT NULL THEN date_format(date_parse(CAST(sc.date AS VARCHAR) || ' ' || sc.saida_3,   '%Y-%m-%d %H:%i'), '%H:%i') END AS saida_3,
    CASE WHEN sc.entrada_4 IS NOT NULL THEN date_format(date_parse(CAST(sc.date AS VARCHAR) || ' ' || sc.entrada_4, '%Y-%m-%d %H:%i'), '%H:%i') END AS entrada_4,
    CASE WHEN sc.saida_4   IS NOT NULL THEN date_format(date_parse(CAST(sc.date AS VARCHAR) || ' ' || sc.saida_4,   '%Y-%m-%d %H:%i'), '%H:%i') END AS saida_4,
    
    c.codigo_empresa,
    
    -- HORAS REGULARES (trabalho fora da janela de sobreaviso)
    CASE 
        WHEN sc.trabalhados_minutos > 0 THEN
            CONCAT(
                LPAD(CAST(FLOOR((sc.trabalhados_minutos - sc.sobreaviso_minutos) / 60) AS VARCHAR), 2, '0'), ':',
                LPAD(CAST((sc.trabalhados_minutos - sc.sobreaviso_minutos) % 60 AS VARCHAR), 2, '0')
            )
        ELSE '00:00'
    END AS horas_regulares,
    
    -- HORAS DE SOBREAVISO
    CONCAT(
        LPAD(CAST(FLOOR(sc.sobreaviso_minutos / 60) AS VARCHAR), 2, '0'), ':',
        LPAD(CAST(sc.sobreaviso_minutos % 60 AS VARCHAR), 2, '0')
    ) AS horas_sobreaviso_regra,
    
    -- TOTAL DE BATIDAS
    sc.total_batidas AS total_batidas,
    
    -- TEMPO TOTAL DE PRESENÇA
    CONCAT(
        LPAD(CAST(FLOOR(sc.presenca_minutos / 60) AS VARCHAR), 2, '0'), ':',
        LPAD(CAST(sc.presenca_minutos % 60 AS VARCHAR), 2, '0')
    ) AS tempo_total_presenca,
    
    -- HORAS EXTRAS
    CONCAT(
        LPAD(CAST(FLOOR(GREATEST(sc.trabalhados_minutos - 480, 0) / 60) AS VARCHAR), 2, '0'), ':',
        LPAD(CAST(GREATEST(sc.trabalhados_minutos - 480, 0) % 60 AS VARCHAR), 2, '0')
    ) AS horas_extras,
    
    -- SALDO DO BANCO
    ROUND(CAST(sc.saldo_banco_minutos AS DOUBLE) / 60.0, 2) AS saldo_banco,
    
    -- STATUS DO DIA
    CASE 
        WHEN sc.trabalhados_minutos > 600 THEN 'LIMITE EXCEDIDO'
        WHEN sc.trabalhados_minutos = 600 THEN 'LIMITE MÁXIMO (10h)'
        WHEN sc.trabalhados_minutos > 480 THEN 'HORAS EXTRAS'
        WHEN sc.trabalhados_minutos = 480 THEN 'JORNADA NORMAL (8h)'
        WHEN sc.trabalhados_minutos < 480 AND sc.trabalhados_minutos >= 360 THEN 'JORNADA REDUZIDA'
        ELSE 'JORNADA MUITO REDUZIDA'
    END AS status_dia,
    
    -- DIA DA SEMANA
    CASE EXTRACT(DOW FROM sc.date)
        WHEN 0 THEN 'Domingo'
        WHEN 1 THEN 'Segunda'
        WHEN 2 THEN 'Terça'
        WHEN 3 THEN 'Quarta'
        WHEN 4 THEN 'Quinta'
        WHEN 5 THEN 'Sexta'
        WHEN 6 THEN 'Sábado'
    END AS dia_semana

FROM sobreaviso_calculado sc
JOIN colaboradores c ON c.colaborador_id = sc.employee_id
ORDER BY sc.date DESC, sc.trabalhados_minutos DESC, c.colaborador_id
