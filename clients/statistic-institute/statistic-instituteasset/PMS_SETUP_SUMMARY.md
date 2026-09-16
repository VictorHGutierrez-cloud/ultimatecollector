# STATIN PMS Setup Summary

**Client:** Statistical Institute of Jamaica (STATIN)  
**Company ID:** `191864`  
**Seed date:** 2026-09-15  
**Language:** English  
**Source docs:**  
- `PMS TEMPLATES & GUIDELINES_STATIN 2026.docx`  
- `Statistical Institute of Jamaica Factorial Business Case.docx`

## What was configured

### Teams (Division / Unit cascade story)
| Team | ID |
|------|-----|
| STATIN Office of the Director General | 1988314 |
| STATIN Corporate Services | 1988315 |
| STATIN Field Services | 1988316 |
| STATIN Economic and Social Statistics | 1988317 |
| STATIN Human Resources | 1988318 |

### Managers
- Laura Lewis → no manager (leadership)
- Charles Carter → Laura Lewis
- Hellen Howard → Laura Lewis
- Daisy Dawson → Charles Carter

### Review processes (active)
| Process | ID | Role |
|---------|----|------|
| STATIN FY 2025-26 Year-End Appraisal | 303500 | Close year; 60/40; bands; accept/appeal |
| STATIN FY 2025-26 Coaching Reviews | 303501 | Minimum three coaching conversations |
| STATIN FY 2026-27 Goal Setting and Individual Work Plan | 303502 | Next-year IWP (Sections 1–4) |

All four demo people are targets on each process.

### Questionnaire content
- Performance Targets (60%) with STATIN 0–5 scale (Exceeded → Met none)
- GoJ Core competencies + Technical (Information Management, Communication and Service Delivery)
- Coaching / IDP / band / accept or appeal / Section 10 actions (year-end)

### Trainings
- STATIN PMS Guidelines for Managers (`421599`)
- STATIN Performance Coaching (`421600`)

### Announcement
- STATIN PMS Cycle — Close FY 2025-26 and Open FY 2026-27 IWPs (`24960061`)

### Goals pack
- `clients/statistic-institute/run_log/goals_pack.md`

## Demo narratives
| Person | Story |
|--------|--------|
| Hellen Howard | Good (~86%) — embargoed statistical releases sample |
| Laura Lewis | Very Good / Superior — incentive recommendation |
| Charles Carter | Manager — Unit Plans + coaching cadence |
| Daisy Dawson | Unsatisfactory (&lt;75%) — PIP / training |

## GoJ competencies (native — Excel import)
API cannot create competencies. Use these files in order:

1. [`competenciesimport.xlsx`](competenciesimport.xlsx) — creates **9 GoJ Core** + **2 STATIN Technical** (Bands 1–6)
2. [`competencies_competency_assignment_importer.xlsx`](competencies_competency_assignment_importer.xlsx) — assigns them to Job Catalog **Level** nodes (Band 3)
3. Instructions: [`COMPETENCIES_IMPORT_README.md`](COMPETENCIES_IMPORT_README.md)

After import, rate competencies in Factorial’s **native Competencies assessment** block (40%). Questionnaire covers **targets (60%)** only — no duplicate competency questions.

## Honest gaps (say on the call)
1. **60/40 weighting** is stated in the process/questionnaire — Factorial does not lock it into payroll.
2. **Increment / promotion** from Section 10 is an HR outcome, not automatic.
3. **Appeals** follow STATIN / HR grievance (and labour law if escalated) — not a Factorial legal module.
4. **Division / Unit Word templates** stay on STATIN’s intranet; Factorial shows teams + individual IWP cycles.
5. Process names use **2025-26 / 2026-27** (hyphen). The API rejected names containing `/`.

## How to re-run
```text
python scripts/clients/statistic-institute/seed_pms_statin.py --dry-run
python scripts/clients/statistic-institute/seed_pms_statin.py --apply
python scripts/clients/statistic-institute/verify_pms_statin.py
```

## Related files
- Catalog: `clients/statistic-institute/catalog.json`
- Demo script: `clients/statistic-institute/statistic-instituteasset/DEMO_SCRIPT_PMS.md`
- Seed log: `clients/statistic-institute/run_log/seed_latest.json`
- Time Off (unchanged): `DEMO_SCRIPT_TIMEOFF.md`
