# STATIN competencies — use THIS spreadsheet

## The correct file

**`competencies_competency_assignment_importer.xlsx`**

Same format as:
`Downloads\competencies_competency_assignment_importer (1).xlsx`

Ready-to-import copies:
- `clients/statistic-institute/statistic-instituteasset/competencies_competency_assignment_importer.xlsx`
- `Downloads\STATIN_competencies_competency_assignment_importer.xlsx` (easy to find)

## What it does

Assigns competencies to Job Catalog nodes:

`Family → Function → Role → Level + Node UUID → Competency 1…10`

Filled with **GoJ Core (9)** + **STATIN Technical: Information Management**, at **Band 3**, on every **Level** row.

## Important

This importer **assigns** competencies to roles/levels.  
The names must already exist (or be accepted) in Factorial Competencies.

If import fails because GoJ names are unknown, create them once in the UI (or ask me to adjust), then re-import this file.

## Ignore for now

`competenciesimport.xlsx` — that was a different “create competencies” template (SZV style).  
**Do not use it** if your Factorial screen expects the assignment importer.

## Import steps

1. Open Factorial → Competencies / Job Catalog → Import  
2. Upload **`STATIN_competencies_competency_assignment_importer.xlsx`** (or the asset folder copy)  
3. Check a Level (e.g. Administrative Mid) — should show GoJ Core competencies  
