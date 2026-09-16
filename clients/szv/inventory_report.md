# SZV Inventory Report

Generated: 2026-08-01T12:40:21.104338+00:00
Company focus: 167952
Credentials company_id: 167952
Company display name: Victor Gutierrez August
Base URL: `https://api.eu2.demo.factorial.dev`
API version: `2026-07-01`
Auth type: `x-api-key`

## Endpoint probes

- `api_public/credentials`: **OK** (sample_count=1)
- `employees/employees`: **OK** (sample_count=5)
- `teams/teams`: **OK** (sample_count=5)
- `teams/memberships`: **OK** (sample_count=5)
- `locations/locations`: **OK** (sample_count=2)
- `companies/legal_entities`: **OK** (sample_count=3)
- `ats/job_postings`: **OK** (sample_count=4)
- `job_catalog/roles`: **OK** (sample_count=0)
- `job_catalog/levels`: **OK** (sample_count=0)
- `job_catalog/node_attributes`: **FAIL(400)** (sample_count=None)
- `job_catalog/tree_nodes`: **FAIL(400)** (sample_count=None)
- `performance/review_processes`: **OK** (sample_count=3)
- `performance/review_process_targets`: **OK** (sample_count=5)
- `performance/agreements`: **OK** (sample_count=0)
- `performance/review_evaluations`: **OK** (sample_count=5)
- `performance/company_employee_score_scales`: **OK** (sample_count=1)
- `performance/employee_score_scales`: **OK** (sample_count=3)
- `performance/review_questionnaire_by_strategies`: **OK** (sample_count=3)
- `performance/review_process_custom_templates`: **OK** (sample_count=0)
- `trainings/trainings`: **OK** (sample_count=2)
- `tasks/tasks`: **OK** (sample_count=0)

## Totals

- Employees: 9
- Teams: 5
- Locations: 2 (SZV/Philipsburg: 1)
- Legal entities: 3 (SZV-named: 1)
- Job postings: 4 (SZV-prefixed: 4)
- Job roles: 0
- Job node attributes (all): 0
- Competency-like attributes: 0
- Review processes: 3 (SZV-prefixed: 3)
- Trainings: 2

## Employees (sample)

- id=5302596 name=Margarita De Weever manager_id=5302595 active=True location_id=550700
- id=5302595 name=Carlos Richardson manager_id=None active=True location_id=550700
- id=5302594 name=Fiona Halley manager_id=5302595 active=True location_id=550700
- id=5302593 name=Ricardo Vlaun manager_id=5302595 active=True location_id=550700
- id=5302592 name=Jamal Voges manager_id=5302595 active=True location_id=550700
- id=5302591 name=Tanya Carty manager_id=5302594 active=True location_id=550700
- id=5302590 name=Marlon Williams manager_id=5302586 active=True location_id=550700
- id=5302587 name=Keisha Peterson manager_id=5302593 active=True location_id=550700
- id=5302586 name=Nadia Lejuez manager_id=5302596 active=True location_id=550700

## Cast resolution

- Keisha Peterson (staff): **FOUND** employee_id=5302587 access_id=5715908 manager_id=5302593
- Marlon Williams (staff): **FOUND** employee_id=5302590 access_id=5715911 manager_id=5302586
- Tanya Carty (staff): **FOUND** employee_id=5302591 access_id=5715912 manager_id=5302594
- Jamal Voges (manager): **FOUND** employee_id=5302592 access_id=5715913 manager_id=5302595
- Ricardo Vlaun (manager): **FOUND** employee_id=5302593 access_id=5715914 manager_id=5302595
- Nadia Lejuez (manager): **FOUND** employee_id=5302586 access_id=5715907 manager_id=5302596
- Fiona Halley (manager): **FOUND** employee_id=5302594 access_id=5715915 manager_id=5302595
- Carlos Richardson (leadership): **FOUND** employee_id=5302595 access_id=5715916 manager_id=None
- Margarita De Weever (leadership): **FOUND** employee_id=5302596 access_id=5715917 manager_id=5302595

## Locations

- id=550700 name=SZV Philipsburg Office country=us city=Philipsburg timezone=America/Puerto_Rico main=True
- id=550683 name=New York - Office country=us city=New York timezone=Etc/UTC main=False

## Legal entities

- id=362979 legal_name=Valencia Legal entity country=es currency=EUR city=California
- id=362978 legal_name=Barcelona Legal entity country=us currency=USD city=Barcelona
- id=362982 legal_name=SZV Social & Health Insurances country=sx currency=USD city=Philipsburg

## Job postings

- id=207771 title=SZV Finance & Levy Analyst status=draft
- id=207770 title=SZV HR Coordinator status=published
- id=207769 title=SZV Control Doctor / Medical Officer status=published
- id=207768 title=SZV Customer Care Officer status=published

## What API can do

- Performance module readable (review_processes)
- Create/start review processes via API
- Locations readable/creatable via API
- Legal entities readable/creatable via API
- ATS job postings readable/creatable via API

## What likely needs the Factorial UI

- Confirm exact weighting Staff/Manager/Leadership in UI if no dedicated weight API
- Polish questionnaire wording for 5 core values and rating definitions NM–SE in UI
- Validate dashboards, 9-box and mobile UX in the Factorial app (not seedable)
- Do NOT personalize time tracking / attendance for this demo

## Existing SZV review processes

- id=243673 name=SZV P3 Year-End Review 2026 status=draft
- id=243672 name=SZV P2 Mid-Year Cycle 2026 status=active
- id=243671 name=SZV P1 Planning Cycle 2026 status=active
