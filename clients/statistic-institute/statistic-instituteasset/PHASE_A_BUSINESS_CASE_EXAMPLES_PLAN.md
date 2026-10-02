# Phase A — Clean Business Case Leave Examples 1 & 2

**Client:** Statistical Institute of Jamaica (STATIN)  
**Sandbox company ID:** `191864`  
**Source:** *Statistical Institute of Jamaica Factorial Business Case* — Leave Requirements  
**Status:** Implementation plan (executed via seed + demo docs)

---

## Objective

Close **Phase A**: seed **clean, one-hero-per-example** demos for Business Case **Example 1** (Partial Working Month) and **Example 2** (Suspension), without changing Examples 3–4, Extended Sick / RTW, or the Felicity Jamaica pause SQL demo.

Daily Jamaica accrual remains **SQL / narrative** — Factorial does not pause accrual natively.

---

## Cast (locked)

| Example | Employee | ID | SIJ Vacation tier |
|---------|----------|----|-------------------|
| **1 — Partial Working Month** | **Bernarda Baker** | `6375969` | 20 days/year (policy `367079`) |
| **2 — Suspension** | **Diana Davis** | `6375987` | 20 days/year (policy `367079`) |
| 3 — Long Vacation (unchanged) | Charles Carter | `6375931` | 20 |
| 4 — Retroactive sick (unchanged) | Clara Cooper | `6375951` | 20 |
| Employee A ESL (unchanged) | Steven Scott | `6376052` | 20 |

---

## Example 1 — Partial Working Month

**Business Case**

- Annual rate: **20 days** → daily rate `20/365 ≈ 0.0547`
- June: employee works **23 of 30** days; **7 days** on extended sick leave
- Accrual for June = `23 × 0.0547 ≈ 1.2602` days

**Sandbox seed**

| Field | Value |
|-------|-------|
| Leave type | **SIJ Sick Leave** (7 days; BC text says “extended sick”; ESL leave type in this demo is reserved for ≥14-day ESL scenarios) |
| Dates | **2026-06-01 → 2026-06-07** (7 calendar days) |
| Eligible June days | 30 − 7 = **23** |
| Jamaica math (in leave description) | `23 × (20/365) ≈ 1.2602` |
| SQL filters (optional) | `Data_init=2026-06-01` · `Data_end=2026-06-30` |

**LIVE vs narrative**

- Leave + dates + description with formula → **LIVE**
- Factorial auto-computing June accrual as 1.2602 → **Not native**
- Gap while off (≈0.38) + Jamaica month accrual (≈1.26) → **SQL elegibilidade**  
  (`sqlexemplo_elegibilidade_resumo.txt` / `_detalhe.txt`, filters Jun 2026)
- Do **not** rely on `sqlexemplo_power.txt` for Ex. 1 (`C=0` when ≤14)

---

## Example 2 — Suspension

**Business Case**

- Annual rate: **20 days**
- Suspended **August 10–20** (**11** calendar days)
- Math: **11** skipped days in a 31-day August → **20** eligible → `20 × 0.0547 ≈ 1.0958`

**Sandbox seed**

| Field | Value |
|-------|-------|
| Leave type | **SIJ Suspension** (new) |
| Dates | **2026-08-10 → 2026-08-20** (**11** calendar days) |
| Note | Matches BC math: 11 skipped days → 20 eligible in August → `20 × (20/365) ≈ 1.0958` |
| SQL filters (optional) | `Data_init=2026-08-01` · `Data_end=2026-08-31` |

**LIVE vs narrative**

- Suspension leave type + approved leave → **LIVE**
- Auto skip of vacation accrual for those days → **Not native**
- Month math + gap → **SQL elegibilidade** (Aug 2026 filters)

---

## Honest gaps (unchanged for Phase A)

1. Factorial does **not** auto-pause vacation accrual on LOA / suspension days.
2. Pure daily formula `entitlement / 365` is **approximated** by policy engine + SQL gap report.
3. Examples 3–4, ESL cascade, RTW workflow gaps stay as already documented.

---

## Files to change

| File | Change |
|------|--------|
| `scripts/clients/statistic-institute/seed_business_case_leave_demos.py` | Cast Bernarda/Diana; SIJ Suspension; seed Ex. 1 & 2 before Ex. 3–4 |
| `clients/statistic-institute/statistic-instituteasset/DEMO_SCRIPT_BUSINESS_CASE_LEAVE.md` | Cover Examples **1–4** + ESL; demo order Bernarda → Diana → Charles → Clara → Steven |
| `clients/statistic-institute/statistic-instituteasset/TIMEOFF_SETUP_SUMMARY.md` | Note Ex. 1–2 + Suspension |
| This file | Plan record |

**Do not change:** Charles / Clara / Steven seeded leaves; Felicity pause demo; monthly close manual/SQL files (unless filters tip only in demo script).

---

## Seed command

```text
python scripts/clients/statistic-institute/seed_business_case_leave_demos.py
```

Verify: `clients/statistic-institute/run_log/business_case_leave_seed_latest.json`  
Expect `example_1_partial_working_month` and `example_2_suspension` with leave `action` = `created` or `skipped_exists`.

---

## Out of scope (Phase B / C)

- Rounding modes floor / ceiling / nearest at application time  
- Custom field “allow beyond max accrual cap”  
- Native RTW dual-approval workflow  
- Real past-2-year expired sick/departmental lookup engine  
