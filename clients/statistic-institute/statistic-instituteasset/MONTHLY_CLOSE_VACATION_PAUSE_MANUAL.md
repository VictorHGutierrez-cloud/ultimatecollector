# Statistical Institute of Jamaica (STATIN)
## Monthly Close Manual — Vacation Accrual Pause Adjustment

**Audience:** HR / Payroll executives and Time Off administrators  
**Product:** Factorial Time Off  
**Related policy:** *Statistical Institute of Jamaica — Vacation Leave Management System Requirements*  
**Language:** English (executive)

---

## 1. Purpose

This manual explains **what STATIN must do at the end of every month** so vacation balances stay aligned with Jamaica policy, even though Factorial does **not** automatically pause vacation accrual during long absences.

### One-sentence summary

> Each month-end, identify employees with leave of absence longer than **14 consecutive calendar days**, calculate how much vacation Factorial would still have accrued in that window, and **manually adjust** that amount off their vacation balance.

---

## 2. Why this process exists

| Jamaica rule (your document) | What Factorial does today |
|------------------------------|---------------------------|
| If leave of absence exceeds **14 consecutive calendar days** (vacation, sick, maternity, study, compassionate, special, or other approved LOA), **vacation does not accrue** during that absence | Factorial continues its normal accrual engine. There is **no** native “pause accrual” switch on leaves |
| Accrual uses eligible calendar days ÷ 365 (or 366) × annual rate | Accrual is policy-driven (monthly generation, working-day charging, etc.) |
| Unused leave may accumulate up to **3 years** (15→45, 20→60, 21→63, 25→75) | Configured on SIJ Vacation policies / allowances |

**Honest product note:** Factorial covers entitlements, policies, working-day charging, and balances well. The **>14 calendar-day pause** is a **STATIN control process** (report + manual adjustment), not an automatic system behaviour.

---

## 3. Terms (plain English)

| Term | Meaning |
|------|---------|
| **Accrual** | Vacation days the employee earns over time |
| **Calendar days** | Consecutive days including weekends (used for the 14-day pause rule) |
| **Working days** | Monday–Friday; how Factorial usually charges vacation taken |
| **Leave of absence (LOA)** | Approved absence types that can trigger the pause (sick, vacation, maternity, etc.) |
| **Gap / manual adjustment** | Days Factorial would still accrue during a pause window — HR removes them with an allowance incidence (or equivalent balance correction) |
| **Tenure start / Antiquity** | Factorial employee fields for tenure — use them as shown in Factorial; do not reinvent tenure outside the product |
| **SQL Summary report** | One row per employee with the **total** to adjust |
| **SQL Power report** | One row per absence (detail / audit) |

---

## 4. Who does what

| Role | Responsibility |
|------|----------------|
| **Time Off Admin / HR Ops** | Run reports, prepare adjustment list, post corrections, archive evidence |
| **HR Manager** | Approve the month-end adjustment pack |
| **Payroll / Finance (if needed)** | Confirm balances before payroll lock if vacation affects pay |
| **Employee** | No action for this control (adjustments are admin-side) |

**Suggested owner:** one named **Month-End Time Off Controller**.

---

## 5. When to run (monthly rhythm)

| Step | Timing |
|------|--------|
| Close the calendar month | Last working day (or first 2 working days of next month) |
| Cut-off for absences in scope | All **approved** leaves that overlap the month |
| Post adjustments | Same day as report sign-off |
| Archive | Same day (PDF/Excel + sign-off note) |

**Recommended cut-off filters for the SQL tools:**

- `Data_init` = first day of the month (e.g. `2026-08-01`)  
- `Data_end` = last day of the month (e.g. `2026-08-31`)

---

## 6. Month-end checklist (do this every month)

### Step 1 — Freeze the period
1. Confirm the month you are closing (e.g. August 2026).
2. Ensure late leave requests for that month are **approved or rejected** before you run reports.
3. Do not include draft / pending leaves in the adjustment pack.

### Step 2 — Run the **Summary** report (HR totals)
1. Open Factorial **Analytics / SQL** (or your saved report).
2. Paste / run: `sqlexemplo_resumo.txt` (Employee summary).
3. Set filters:
   - **Data_init** = month start  
   - **Data_end** = month end  
4. Export to Excel/CSV.

**Focus columns:**

| Column | Use it for |
|--------|------------|
| `Pause_Absences_Count` | Who had at least one pause case |
| `Sum_C_Total_Manual_Adjustment` | **Total days to remove** from vacation |
| `Sum_C_Rounded_Jamaica_Half_Up` | Same total with Jamaica half-up rounding (≥ 0.50 up) |
| `Annual_Entitlement_Days` | Confirm employee is on the correct SIJ tier (15 / 20 / 21 / 25) |

**Rule of thumb:** If `Pause_Absences_Count` = 0 → no pause adjustment for that person this month.

### Step 3 — Spot-check with the **Power** report (audit)
1. Run `sqlexemplo_power.txt` with the **same** date filters.
2. For anyone with a material gap, open 1–2 absence rows and confirm:
   - Calendar days **> 14**
   - Leave family is an LOA type (sick, vacation, maternity, study, compassionate, special, etc.)
   - Status is approved
3. Keep the Power export as **audit evidence**.

### Step 4 — Prepare the adjustment pack
Create a short table for sign-off:

| Employee | Code | Tier (days/yr) | Pause absences | Days to adjust (Sum_C) | Rounded | Notes |
|----------|------|----------------|----------------|------------------------|---------|-------|
| Felicity Ford | EM-… | 25 | 1 | 1.10 | 1 | Sick 3–18 Aug |

Attach:
- Summary export  
- Power export (or filtered rows)  
- Month / cut-off dates  

### Step 5 — Get approval
1. HR Manager reviews and signs (email or signed PDF is enough).
2. Do **not** post adjustments before approval if your internal control requires dual control.

### Step 6 — Post corrections in Factorial
For each approved line:

1. Open the employee → **Time Off**.
2. Apply a **manual balance correction** on the **SIJ Vacation** allowance  
   (Factorial: allowance **incidence** / adjustment — negative days equal to `Sum_C` or the rounded value your policy adopts).
3. Description example:  
   `Month-end Jamaica pause adjustment — Aug 2026 — LOA >14 calendar days — see SQL summary`
4. Save / confirm.

**Policy choice (document once and keep stable):**

- Use **exact** `Sum_C_Total_Manual_Adjustment`, **or**  
- Use **rounded** `Sum_C_Rounded_Jamaica_Half_Up`  

STATIN should pick one method and apply it consistently.

### Step 7 — Verify
1. Re-open 2–3 adjusted employees and confirm vacation balance moved as expected.
2. Optionally re-run Summary: gaps already adjusted will still *appear* in SQL as theoretical gaps unless you track posted adjustments separately — so keep an **Adjustment Log** (Step 8).

### Step 8 — Archive
Store in your HR shared drive / DMS:

- `YYYY-MM_STATIN_Vacation_Pause_Summary.xlsx`  
- `YYYY-MM_STATIN_Vacation_Pause_Detail.xlsx`  
- `YYYY-MM_Adjustment_Log.xlsx` (employee, days adjusted, date posted, approver, Factorial reference)  
- Approval email / PDF  

Retention: follow STATIN records policy (recommend minimum **3 years**, aligned with leave accumulation horizon).

---

## 7. What “good” looks like (acceptance criteria)

At month-end close, all of the following are true:

- [ ] All relevant leaves for the month are approved or rejected  
- [ ] Summary report run for the full calendar month  
- [ ] Every employee with `Pause_Absences_Count` > 0 is either adjusted or explicitly waived with reason  
- [ ] Adjustments posted only to **SIJ Vacation** balances  
- [ ] Manager approval recorded  
- [ ] Exports + adjustment log archived  

---

## 8. Exceptions & edge cases

| Situation | What to do |
|-----------|------------|
| Absence spans two months (e.g. 25 Jul–10 Aug) | Include in **both** month reports if the leave overlaps; adjust **once** for the full pause window (prefer adjusting in the month the leave **ends**, and note “multi-month LOA” in the log to avoid double-counting) |
| Two overlapping long absences | Prefer Power report to understand windows; adjust the **sum of gaps** from Summary unless overlaps double-count — if unsure, adjust from Power line items once |
| Pending leave approved after close | Run a **supplemental** mini-close or fold into next month with label `late approval — prior month` |
| Employee on wrong SIJ tier (15/20/21/25) | Fix **policy assignment** first, then recalculate gap |
| Working-from-home absences | **Out of scope** for pause (excluded in reports) |
| Recall from vacation | Separate process: credit unused approved days back (manual incidence). Not the same as the >14 pause |

---

## 9. Roles of the two SQL reports

| Report file | Grain | Best for |
|-------------|-------|----------|
| `sqlexemplo_resumo.txt` | **1 row = 1 employee** | Month-end pack, totals to adjust |
| `sqlexemplo_power.txt` | **1 row = 1 absence** | Audit, demo, dispute resolution |

You do **not** need both every conversation with leadership — Summary is enough for the monthly pack; Power is the evidence pack.

---

## 10. Executive talking points (if asked in a meeting)

> “Factorial manages our SIJ vacation tiers, working-day charging, and balances.  
> Jamaica also requires accrual to **stop** when someone is off more than **14 calendar days**.  
> That pause is not automatic in Factorial, so every month we run a control report and post a small manual correction.  
> Summary tells us **who** and **how much**; Power shows **which leave** caused it.”

---

## 11. Related configuration (reference only)

Already configured in the STATIN Factorial demo / workspace:

- Leave types: SIJ Vacation, Sick, Maternity, Study, Compassionate, Special  
- Vacation policies: **15 / 20 / 21 / 25** days per year with **3-year caps** 45 / 60 / 63 / 75  
- Working-day charging; public holidays do not consume vacation balance  

These settings support day-to-day Time Off. They **do not** replace this monthly pause control.

---

## 12. Document control

| Item | Value |
|------|--------|
| Document title | Monthly Close Manual — Vacation Accrual Pause Adjustment |
| Client | Statistical Institute of Jamaica (STATIN) |
| Version | 1.0 |
| Status | Executive operating procedure |
| Companion files | `sqlexemplo_resumo.txt`, `sqlexemplo_power.txt`, `TIMEOFF_SETUP_SUMMARY.md`, `DEMO_SCRIPT_TIMEOFF.md` |
| PDF (sandbox) | `STATIN Monthly Close Vacation Pause Manual.pdf` · Factorial document id **13589374** (`company_internal`, private) |

---

## 13. Quick one-page card (print / pin)

**Every month-end**

1. Approve/reject all leaves for the month  
2. Run **Summary** SQL (`Data_init`–`Data_end` = that month)  
3. Spot-check big gaps with **Power** SQL  
4. Get HR Manager sign-off  
5. Post negative vacation adjustments = `Sum_C` (or rounded)  
6. Save exports + adjustment log  

**Success =** no employee with a >14-day LOA still carrying unadjusted vacation accrual for that window.
