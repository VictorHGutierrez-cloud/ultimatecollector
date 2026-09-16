# STATIN Recruitment (ATS) — Setup Summary

**Client:** Statistical Institute of Jamaica (STATIN)  
**Company ID:** `191864`  
**Seed date:** 2026-09-15  

## Job postings created

| Title | ID | Status | Team story |
|-------|-----|--------|------------|
| STATIN Statistical Officer | 291862 | published | Economic and Social Statistics |
| STATIN Field Interviewer (Special Project) | 291863 | published | Field Services |
| STATIN Personnel / Staffing Officer | 291864 | published | Human Resources |
| STATIN Executive Secretary, ODG | 291865 | draft | Office of the Director General |

## Candidates + applications

| Candidate | ID | Applied to |
|-----------|-----|------------|
| Marcia Bennett | 5149324 | Statistical Officer |
| Omar Reid | 5149325 | Field Interviewer (Special Project) |
| Keisha Campbell | 5149326 | Personnel / Staffing Officer |
| Andre Williams | 5149327 | Executive Secretary, ODG |

## How to re-run

```text
python scripts/clients/statistic-institute/seed_recruitment_statin.py --dry-run
python scripts/clients/statistic-institute/seed_recruitment_statin.py --apply
```

## Scope guide (private document)

Uploaded to Factorial Documents:

- Filename: `STATIN Factorial Scope Guide.pdf`
- Document ID: `13202622`
- Space: `company_internal`
- Public: `false`

Client-facing user manual. Recruitment chapters cover all five STATIN staffing processes phase-by-phase (from `recruitment.txt` BRD). No internal seed/API/operator content.

Local files:

- Source: `statistic-instituteasset/FACTORIAL_SCOPE_GUIDE_STATIN.md`
- PDF: `statistic-instituteasset/STATIN Factorial Scope Guide.pdf`

```text
python scripts/clients/statistic-institute/build_scope_guide_pdf.py
python scripts/clients/statistic-institute/upload_documents_statin.py --apply
python scripts/clients/statistic-institute/upload_documents_statin.py --list
python scripts/clients/statistic-institute/upload_documents_statin.py --trash <document_id>
```

Note: the demo API key is not authorised for `documents/documents/move_to_trash_bin` (403);
the script falls back to `DELETE /documents/documents/{id}`.

## Honest gaps

- IRHC / MoFPS / POC vacancy approvals stay outside Factorial.
- Shortlist matrix 70%/60% is a process rule — configure scoring in ATS UI / interview notes.
- Special project onboarding forms (Oath of Secrecy, TRN, NIS) live in Documents + HR process, not fully automated.
