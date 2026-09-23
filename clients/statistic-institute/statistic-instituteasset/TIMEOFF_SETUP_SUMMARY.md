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
- **Demo SQL pausa >14 dias:** Felicity Ford · **SIJ Sick Leave** · **2026-08-03 → 2026-08-18** (16 dias de calendário) · leave id `6347272`
- **SIJ Sick Allowance** (14 dias/ano, `all_days`) anexado às policies SIJ 15/20/21/25 (+ policy legada `366459`) para permitir pedidos de Sick
- **Manual executivo (EN) — fechamento mensal:** `MONTHLY_CLOSE_VACATION_PAUSE_MANUAL.md`
- **PDF no sandbox Factorial:** `STATIN Monthly Close Vacation Pause Manual.pdf` · document id `13589374` · space `company_internal` · public `false`
- **Business Case leave demos (Ex. 3–4 + Extended Sick):** `DEMO_SCRIPT_BUSINESS_CASE_LEAVE.md`  
  Seed: `python scripts/clients/statistic-institute/seed_business_case_leave_demos.py`

## Limitações (demo honestamente)
A Factorial **não replica 100%** o documento da Jamaica:
1. Fórmula diária `(dias elegíveis ÷ 365 ou 366) × taxa` — aproximada pelo motor mensal
2. Pausa de accrual após **14 dias** de leave of absence — não há toggle nativo; use os leave types SIJ Sick/Maternity/etc. na conversa da demo
3. **Recall credit** (devolver dias não usados) — ajuste manual / incidence, não automático

## Como reaplicar / verificar
```text
python scripts/clients/statistic-institute/seed_timeoff_sij.py
python scripts/clients/statistic-institute/verify_timeoff_sij.py
python scripts/clients/statistic-institute/seed_jamaica_pause_demo.py
```

SQL da demo:
- Detalhe (1 ausência/linha): `sqlexemplo_power.txt`
- Resumo (1 pessoa/linha, total a ajustar): `sqlexemplo_resumo.txt`  
Filtros: `Data_init = 2026-08-01` · `Data_end = 2026-08-31`  
Cerca: tenure/antiquity Factorial, faixa 15/20/21/25, 365/366, teto 3 anos, pausa LOA >14, rounding ≥0,50.

Logs:
- `clients/statistic-institute/run_log/timeoff_seed_20260912.json`
- `clients/statistic-institute/run_log/timeoff_inventory_after.json`
- `clients/statistic-institute/run_log/jamaica_pause_seed_latest.json`
- `clients/statistic-institute/run_log/jamaica_pause_gap_validated.json`
