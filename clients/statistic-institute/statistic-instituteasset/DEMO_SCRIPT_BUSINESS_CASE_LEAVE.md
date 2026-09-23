# STATIN Business Case — Leave Demo Script (Examples 3–4 + Extended Sick)

**Client:** Statistical Institute of Jamaica (sandbox Factorial)  
**Source:** *Statistical Institute of Jamaica Factorial Business Case* — Leave Requirements  
**Seed:** `python scripts/clients/statistic-institute/seed_business_case_leave_demos.py`  
**Log:** `clients/statistic-institute/run_log/business_case_leave_seed_latest.json`

---

## How to read this script

| Label | Meaning |
|-------|---------|
| **LIVE in Factorial** | You can open the screen and show the exact data |
| **DEMO NARRATIVE** | Say it aloud — Factorial does not automate this step |
| **SQL / PROCESS** | Use `sqlexemplo_power.txt` / `sqlexemplo_resumo.txt` or the monthly close manual |

**Goal:** Every case from Example 3 through Extended Sick Leave can be **shown faithfully** in the demo environment — either as live data or as an honest process gap with seeded evidence.

---

## Cast

| Role in Business Case | Employee in sandbox | Why |
|-----------------------|---------------------|-----|
| Example 3 (20 days/year) | **Charles Carter** | SIJ Vacation 20 days policy |
| Example 4 (retroactive sick) | **Clara Cooper** | Short sick Jun 25–26 with retro story |
| Employee A (Extended Sick) | **Steven Scott** | ESL early RTW + 60-day cascade |

---

## Example 3 — Long Vacation (LIVE)

**Business Case text**

- Annual rate: **20 days**  
- Vacation approved **December 1–18** (14 working + 4 weekend)  
- System pauses accrual **Dec 1–18**, resumes **Dec 19**  
- Accrual for December if pause: **13 × 0.0547 ≈ 0.7123** days  

### What to click

1. **Employees** → **Charles Carter** → **Time Off**
2. Open leave: **SIJ Vacation Leave** · **2026-12-01 → 2026-12-18**  
   - Leave id (seed): `6382420`  
   - Description mentions Example 3 and the math  
3. (Optional) Run SQL Power with:
   - `Data_init = 2026-12-01`
   - `Data_end = 2026-12-31`
4. Find Charles → expect:
   - `Leave_Family = vacation`
   - `Calendar_Days = 18`
   - `Annual_Entitlement_Days = 20`
   - `Absence_Above_Threshold = YES`
   - `B_Jamaica = 0` · `C_Gap ≈ 18 × (20/365) ≈ 0.986`

**About 0.7123 vs ~0.986:**  
Business Case **0.7123** = accrual for the **rest of December** after pause (13 days × 20/365).  
SQL **C_Gap** = accrual Factorial would still post **during the leave window** (18 calendar days × 20/365).  
Both are correct for different questions — use C_Gap for the month-end adjustment of the pause window.

**What to say**

> “Charles is on the 20-day tier. His vacation is exactly the Business Case window: 1–18 December.  
> Jamaica pauses accrual for those 18 calendar days and resumes on the 19th.  
> Factorial does **not** pause by itself — we prove it with SQL and correct with the month-end process.  
> The 0.7123 figure is December’s accrual **after** applying the pause (13 accruing days × 20/365).”

| Item | Status |
|------|--------|
| Dates Dec 1–18 | **LIVE** |
| Tier 20 | **LIVE** |
| 14 working + 4 weekend | **LIVE** (calendar proof + narrative) |
| Auto pause Dec 1–18 | **SQL / PROCESS** (not native) |
| Resume Dec 19 | **DEMO NARRATIVE** |

---

## Example 4 — Retroactive Leave (LIVE + narrative)

**Business Case text**

- On **July 10**, employee applies for sick **June 25–26**  
- System already credited accruals for those days  
- **No automatic change**  
- HR must **manually adjust** if reversal is required  

### What to click

1. **Employees** → **Clara Cooper** → **Time Off**
2. Open **SIJ Sick Leave** · **2026-06-25 → 2026-06-26**  
   - Leave id: `6382433`  
   - Description states applied on **2026-07-10** (retro)

**What to say**

> “This sick leave was entered after the fact. Factorial already accrued those days.  
> Nothing reverses automatically — HR posts a manual incidence if we must claw back accrual.  
> That matches Example 4 exactly.”

| Item | Status |
|------|--------|
| Sick Jun 25–26 | **LIVE** |
| Retro story in description | **LIVE** |
| Auto reversal of accrual | **Not in Factorial** — show manual incidence if asked |

---

## Extended Sick Leave — leave type + medical certificate (LIVE)

### What to click

1. **Time Off** → **Leave types**  
2. Show **SIJ Extended Sick Leave** (attachment / medical certificate flag enabled in seed)  
3. Also show supporting types created for the cascade:  
   - **SIJ Departmental Leave**  
   - **SIJ No Pay Leave**  
   - (existing) **SIJ Sick Leave**, **SIJ Vacation Leave**

**What to say**

> “Business Case asked for a dedicated Extended Sick Leave type with medical certificate.  
> That type exists here. Certificate upload is configured on the leave type.”

---

## Extended Sick — unclear return date + pause (LIVE leave + narrative)

**Business Case**

- Apply **≥14 days** even if return date is unclear  
- Stop vacation accruals until resumption letter  
- Block further leave in the same period  
- Extension if still out after initial end  

### What to show

1. Steven Scott’s ESL / cascade segments (≥14 day blocks) — **LIVE**  
2. Pause of vacation accrual → **SQL / month-end process** (same as Jamaica >14 rule)  
3. “No other leave during ESL” / “extension request” → **DEMO NARRATIVE** (process control; not a hard Factorial lock in this demo)

---

## Return to Work — early return cancels remaining days (LIVE evidence)

**Business Case example**

- ESL requested **Dec 1–18 2025**  
- RTW date **Dec 15** approved (Supervisor → Admin)  
- Days **Dec 15–18** cancelled  

### What to click

1. **Employees** → **Steven Scott** → **Time Off**  
2. Open **SIJ Extended Sick Leave** · **2025-12-01 → 2025-12-14**  
   - Leave id: `6382947`  
   - Stored as **Dec 1–14** = post-cancellation state after RTW Dec 15  

**What to say**

> “Original request was Dec 1–18. Return-to-work on Dec 15 was approved in the Business Case flow (Supervisor then Admin).  
> Remaining Dec 15–18 were cancelled — what you see stored is Dec 1–14.  
> Factorial does not run that RTW workflow natively here; we reproduce the **outcome** for the demo.”

| Item | Status |
|------|--------|
| Post-cancel leave Dec 1–14 | **LIVE** |
| 2-level RTW approvals | **DEMO NARRATIVE** |
| Auto-cancel remaining days | **DEMO NARRATIVE** (outcome seeded) |

---

## Employee A — 60-day cascade (LIVE segments)

**Business Case order & balances**

| Step | Leave type | Days | Running total |
|------|------------|------|---------------|
| 1 | Current year Extended Sick | 14 | 14 |
| 2 | Current year Departmental | 10 | 24 |
| 3 | Past 2y unused sick | 5 | 29 |
| 4 | Past 2y unused departmental | 7 | 36 |
| 5 | Current year vacation | 10 | 46 |
| 6 | No Pay | 14 | **60** |

### What to click

1. **Steven Scott** → **Time Off** → list leaves starting **2026-01-05**  
2. Walk the chain in order (each segment has description `BC 60-day cascade — …`):

| Segment | Dates (seed) | Type |
|---------|--------------|------|
| 14 ESL | 2026-01-05 → 01-18 | SIJ Extended Sick Leave |
| 10 Departmental | 2026-01-19 → 01-28 | SIJ Departmental Leave |
| 5 past sick | 2026-01-29 → 02-02 | SIJ Sick Leave |
| 7 past departmental | 2026-02-03 → 02-09 | SIJ Departmental Leave |
| 10 Vacation | 2026-02-10 → 02-19 | SIJ Vacation Leave |
| 14 No Pay | 2026-02-20 → 03-05 | SIJ No Pay Leave |

**What to say**

> “For a 60-day extended absence, STATIN’s rule allocates balances in this exact order until No Pay.  
> Factorial does not auto-split one request across six buckets.  
> In the demo we seeded **six consecutive approved leaves** so you can walk the same order on screen — 46 days paid from leave pots, then 14 No Pay.”

| Item | Status |
|------|--------|
| Six segments in correct order | **LIVE** |
| Totals 46 + 14 No Pay = 60 | **LIVE** |
| Auto-cascade from one ESL request | **Not native** — seeded as ordered leaves |
| Past-2y lookup of expired sick/dept | **Illustrative** (shown as Sick/Departmental segments) |

---

## Quick demo path (≈ 10 minutes)

1. **Charles** — Example 3 Dec vacation + optional SQL Dec filters  
2. **Clara** — Example 4 retro sick  
3. **Leave types** — Extended Sick (+ Departmental, No Pay)  
4. **Steven** — ESL early RTW Dec 1–14 2025  
5. **Steven** — walk 60-day cascade Jan–Mar 2026  
6. Close: “Native gaps = auto pause, auto RTW cancel, auto cascade → covered by process + SQL monthly close”

---

## Honest gaps (say this if challenged)

1. **Daily accrual only on “active” days** — Factorial policy engine ≠ pure Jamaica daily formula; SQL approximates the gap.  
2. **Auto pause >14 calendar days** — not native; monthly close manual.  
3. **Return-to-Work workflow with dual approval + auto cancel** — outcome seeded; workflow is narrative.  
4. **Single ESL request auto-cascading across 6 balances** — reproduced as ordered leaves, not one magic request.  
5. **Past 2 years expired leave lookup** — illustrated with Sick/Departmental segments, not a historical archive engine.

---

## Re-seed / verify

```text
python scripts/clients/statistic-institute/seed_business_case_leave_demos.py
python scripts/clients/statistic-institute/verify_timeoff_sij.py
```

SQL companions:

- Detail: `sqlexemplo_power.txt`  
- Totals: `sqlexemplo_resumo.txt`  
- Month-end ops: `MONTHLY_CLOSE_VACATION_PAUSE_MANUAL.md` (+ PDF in Documents)
