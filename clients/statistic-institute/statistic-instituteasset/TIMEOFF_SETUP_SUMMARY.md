# SIJ Vacation Leave — Setup aplicado

Fonte: `Statistical Institute of Jamaica Vacation Leave Requirements (1).docx`

Cliente: **statistic-institute** · Company ID: **191864**

## O que foi personalizado

### Leave types
| Nome | ID |
|------|-----|
| SIJ Vacation Leave | 2405344 |
| SIJ Sick Leave | 2405345 |
| SIJ Maternity Leave | 2405346 |
| SIJ Study Leave | 2405347 |
| SIJ Compassionate Leave | 2405348 |
| SIJ Special Leave | 2405349 |

### Policies + allowances (Vacation)
| Faixa | Dias/ano | Teto 3 anos | Policy ID | Allowance ID |
|-------|----------|-------------|-----------|--------------|
| Base | 15 | 45 | 367078 | 617645 |
| Intermediário | 20 | 60 | 367079 | 617647 |
| 15–25 anos serviço | 21 | 63 | 367080 | 617649 |
| Sênior | 25 | 75 | 367081 | 617651 |

### Regras aplicadas na Factorial
- Contagem em **dias úteis** (seg–sex)
- Feriados **não** descontam (`count_holiday_as_workable = false`)
- **Prorata** ligado
- Arredondamento `half_day` (≈ regra ≥0,50 sobe)
- Carry-over até **36 meses**, teto = 3× entitlement
- Accrual mensal (`generated_days_monthly_first_day`)

### Dados demo
- **42** colaboradores ativos atribuídos em rodízio 15 / 20 / 21 / 25
- **4** saldos demo (incidences): 9, 20, 40 e 50 dias
- **3** férias de exemplo (criadas no 1º seed; aprovadas quando possível)

## Limitações (demo honestamente)
A Factorial **não replica 100%** o documento da Jamaica:
1. Fórmula diária `(dias elegíveis ÷ 365 ou 366) × taxa` — aproximada pelo motor mensal
2. Pausa de accrual após **14 dias** de leave of absence — não há toggle nativo; use os leave types SIJ Sick/Maternity/etc. na conversa da demo
3. **Recall credit** (devolver dias não usados) — ajuste manual / incidence, não automático

## Como reaplicar / verificar
```text
python scripts/clients/statistic-institute/seed_timeoff_sij.py
python scripts/clients/statistic-institute/verify_timeoff_sij.py
```

Logs:
- `clients/statistic-institute/run_log/timeoff_seed_20260912.json`
- `clients/statistic-institute/run_log/timeoff_inventory_after.json`
