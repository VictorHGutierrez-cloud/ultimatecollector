#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventário da conta Factorial para a demo SZV (company 167952)."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from clients.szv.api_helpers import (  # noqa: E402
    DEMO_DIR,
    RUN_LOG_DIR,
    SzvApi,
    load_catalog,
    normalize_name,
    save_json,
)


def probe(api: SzvApi, path: str) -> dict:
    status, body = api.get(path, params={"limit": 5})
    count = None
    sample = []
    if status == 200 and isinstance(body, dict):
        data = body.get("data") or []
        if isinstance(data, list):
            count = len(data)
            sample = data[:3]
        elif isinstance(data, dict):
            count = 1
            sample = [data]
    return {
        "path": path,
        "status": status,
        "ok": status == 200,
        "sample_count": count,
        "error": None if status == 200 else body,
        "sample": sample,
    }


def emp_name(e: dict) -> str:
    return e.get("full_name") or f"{e.get('first_name', '')} {e.get('last_name', '')}".strip()


def json_safe_name(item: dict) -> str:
    parts = [
        str(item.get("name") or ""),
        str(item.get("label") or ""),
        str((item.get("value_competency") or {}).get("name") or ""),
    ]
    return " ".join(parts).lower()


def main() -> int:
    api = SzvApi()
    catalog = load_catalog()
    cast_names = [normalize_name(p["full_name"]) for p in catalog["cast"]]

    print("=== SZV Inventory ===")
    print(f"BASE_URL={api.config.BASE_URL}")
    print(f"API_VERSION={api.version}")
    print(f"AUTH_TYPE={api.config.AUTH_TYPE}")
    print(f"COMPANY_FOCUS={catalog.get('company_id')}")

    endpoints = [
        "api_public/credentials",
        "employees/employees",
        "teams/teams",
        "teams/memberships",
        "locations/locations",
        "companies/legal_entities",
        "ats/job_postings",
        "job_catalog/roles",
        "job_catalog/levels",
        "job_catalog/node_attributes",
        "job_catalog/tree_nodes",
        "performance/review_processes",
        "performance/review_process_targets",
        "performance/agreements",
        "performance/review_evaluations",
        "performance/company_employee_score_scales",
        "performance/employee_score_scales",
        "performance/review_questionnaire_by_strategies",
        "performance/review_process_custom_templates",
        "trainings/trainings",
        "tasks/tasks",
    ]

    probes = {ep: probe(api, ep) for ep in endpoints}

    employees = api.list_all("employees/employees") if probes["employees/employees"]["ok"] else []
    teams = api.list_all("teams/teams") if probes["teams/teams"]["ok"] else []
    locations = api.list_all("locations/locations") if probes["locations/locations"]["ok"] else []
    legal_entities = (
        api.list_all("companies/legal_entities")
        if probes["companies/legal_entities"]["ok"]
        else []
    )
    job_postings = api.list_all("ats/job_postings") if probes["ats/job_postings"]["ok"] else []
    roles = api.list_all("job_catalog/roles") if probes["job_catalog/roles"]["ok"] else []
    node_attrs = (
        api.list_all("job_catalog/node_attributes")
        if probes["job_catalog/node_attributes"]["ok"]
        else []
    )
    processes = (
        api.list_all("performance/review_processes")
        if probes["performance/review_processes"]["ok"]
        else []
    )
    trainings = api.list_all("trainings/trainings") if probes["trainings/trainings"]["ok"] else []

    cast_resolution = []
    by_name = {normalize_name(emp_name(e)): e for e in employees}
    for person in catalog["cast"]:
        emp = by_name.get(normalize_name(person["full_name"]))
        rename_from = person.get("rename_from")
        rename_emp = by_name.get(normalize_name(rename_from)) if rename_from else None
        cast_resolution.append(
            {
                "full_name": person["full_name"],
                "group": person["group"],
                "found": bool(emp),
                "rename_from_found": bool(rename_emp),
                "employee_id": emp.get("id") if emp else (rename_emp.get("id") if rename_emp else None),
                "access_id": emp.get("access_id")
                if emp
                else (rename_emp.get("access_id") if rename_emp else None),
                "manager_id": emp.get("manager_id")
                if emp
                else (rename_emp.get("manager_id") if rename_emp else None),
            }
        )

    competencies = [
        a
        for a in node_attrs
        if str(a.get("type") or a.get("attribute_type") or "").lower() == "competency"
        or a.get("value_competency")
        or "competenc" in json_safe_name(a)
    ]

    szv_processes = [p for p in processes if str(p.get("name", "")).startswith("SZV")]
    szv_jobs = [j for j in job_postings if str(j.get("title", "")).startswith("SZV")]
    szv_locations = [l for l in locations if "SZV" in str(l.get("name", "")) or "Philipsburg" in str(l.get("name", ""))]
    szv_legal = [
        le
        for le in legal_entities
        if "SZV" in str(le.get("legal_name", "")) or "Social & Health" in str(le.get("legal_name", ""))
    ]

    api_can = []
    api_needs_ui = []
    if probes["performance/review_processes"]["ok"]:
        api_can.append("Performance module readable (review_processes)")
        api_can.append("Create/start review processes via API")
    else:
        api_needs_ui.append(
            "Performance module not readable — ask Factorial AM to enable Performance on this demo"
        )
    if probes["locations/locations"]["ok"]:
        api_can.append("Locations readable/creatable via API")
    if probes["companies/legal_entities"]["ok"]:
        api_can.append("Legal entities readable/creatable via API")
    if probes["ats/job_postings"]["ok"]:
        api_can.append("ATS job postings readable/creatable via API")

    api_needs_ui.extend(
        [
            "Confirm exact weighting Staff/Manager/Leadership in UI if no dedicated weight API",
            "Polish questionnaire wording for 5 core values and rating definitions NM–SE in UI",
            "Validate dashboards, 9-box and mobile UX in the Factorial app (not seedable)",
            "Do NOT personalize time tracking / attendance for this demo",
        ]
    )

    cred = probes.get("api_public/credentials", {})
    cred_sample = (cred.get("sample") or [{}])[0] if cred.get("ok") else {}

    report_lines = [
        "# SZV Inventory Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Company focus: {catalog.get('company_id')}",
        f"Credentials company_id: {cred_sample.get('company_id')}",
        f"Company display name: {cred_sample.get('name')}",
        f"Base URL: `{api.config.BASE_URL}`",
        f"API version: `{api.version}`",
        f"Auth type: `{api.config.AUTH_TYPE}`",
        "",
        "## Endpoint probes",
        "",
    ]
    for ep, result in probes.items():
        mark = "OK" if result["ok"] else f"FAIL({result['status']})"
        report_lines.append(f"- `{ep}`: **{mark}** (sample_count={result['sample_count']})")

    report_lines += [
        "",
        "## Totals",
        "",
        f"- Employees: {len(employees)}",
        f"- Teams: {len(teams)}",
        f"- Locations: {len(locations)} (SZV/Philipsburg: {len(szv_locations)})",
        f"- Legal entities: {len(legal_entities)} (SZV-named: {len(szv_legal)})",
        f"- Job postings: {len(job_postings)} (SZV-prefixed: {len(szv_jobs)})",
        f"- Job roles: {len(roles)}",
        f"- Job node attributes (all): {len(node_attrs)}",
        f"- Competency-like attributes: {len(competencies)}",
        f"- Review processes: {len(processes)} (SZV-prefixed: {len(szv_processes)})",
        f"- Trainings: {len(trainings)}",
        "",
        "## Employees (sample)",
        "",
    ]
    for e in employees[:30]:
        report_lines.append(
            f"- id={e.get('id')} name={emp_name(e)} manager_id={e.get('manager_id')} "
            f"active={e.get('active')} location_id={e.get('location_id')}"
        )
    if len(employees) > 30:
        report_lines.append(f"- ... and {len(employees) - 30} more")

    report_lines += ["", "## Cast resolution", ""]
    for row in cast_resolution:
        status = "FOUND" if row["found"] else ("RENAME_SOURCE" if row["rename_from_found"] else "MISSING")
        report_lines.append(
            f"- {row['full_name']} ({row['group']}): **{status}** "
            f"employee_id={row['employee_id']} access_id={row['access_id']} "
            f"manager_id={row['manager_id']}"
        )

    report_lines += ["", "## Locations", ""]
    if locations:
        for loc in locations:
            report_lines.append(
                f"- id={loc.get('id')} name={loc.get('name')} country={loc.get('country')} "
                f"city={loc.get('city')} timezone={loc.get('timezone')} main={loc.get('main')}"
            )
    else:
        report_lines.append("- None")

    report_lines += ["", "## Legal entities", ""]
    if legal_entities:
        for le in legal_entities:
            report_lines.append(
                f"- id={le.get('id')} legal_name={le.get('legal_name')} "
                f"country={le.get('country')} currency={le.get('currency')} city={le.get('city')}"
            )
    else:
        report_lines.append("- None")

    report_lines += ["", "## Job postings", ""]
    if job_postings:
        for job in job_postings:
            report_lines.append(
                f"- id={job.get('id')} title={job.get('title')} status={job.get('status')}"
            )
    else:
        report_lines.append("- None yet")

    report_lines += ["", "## What API can do", ""]
    report_lines += [f"- {x}" for x in api_can] or ["- (none detected)"]
    report_lines += ["", "## What likely needs the Factorial UI", ""]
    report_lines += [f"- {x}" for x in api_needs_ui]

    report_lines += ["", "## Existing SZV review processes", ""]
    if szv_processes:
        for p in szv_processes:
            report_lines.append(
                f"- id={p.get('id')} name={p.get('name')} status={p.get('status')}"
            )
    else:
        report_lines.append("- None yet")

    report_path = DEMO_DIR / "inventory_report.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": api.config.BASE_URL,
        "api_version": api.version,
        "auth_type": api.config.AUTH_TYPE,
        "company_focus": catalog.get("company_id"),
        "credentials_company_id": cred_sample.get("company_id"),
        "probes": {k: {kk: vv for kk, vv in v.items() if kk != "sample"} for k, v in probes.items()},
        "counts": {
            "employees": len(employees),
            "teams": len(teams),
            "locations": len(locations),
            "legal_entities": len(legal_entities),
            "job_postings": len(job_postings),
            "szv_job_postings": len(szv_jobs),
            "roles": len(roles),
            "node_attributes": len(node_attrs),
            "competencies_guess": len(competencies),
            "review_processes": len(processes),
            "szv_review_processes": len(szv_processes),
            "trainings": len(trainings),
        },
        "employees": [
            {
                "id": e.get("id"),
                "full_name": emp_name(e),
                "manager_id": e.get("manager_id"),
                "active": e.get("active"),
                "location_id": e.get("location_id"),
                "legal_entity_id": e.get("legal_entity_id"),
            }
            for e in employees
        ],
        "cast_resolution": cast_resolution,
        "locations": [
            {
                "id": l.get("id"),
                "name": l.get("name"),
                "country": l.get("country"),
                "city": l.get("city"),
                "timezone": l.get("timezone"),
                "main": l.get("main"),
            }
            for l in locations
        ],
        "legal_entities": [
            {
                "id": le.get("id"),
                "legal_name": le.get("legal_name"),
                "country": le.get("country"),
                "currency": le.get("currency"),
            }
            for le in legal_entities
        ],
        "job_postings": [
            {"id": j.get("id"), "title": j.get("title"), "status": j.get("status")}
            for j in job_postings
        ],
        "teams": [{"id": t.get("id"), "name": t.get("name")} for t in teams],
        "szv_processes": [
            {"id": p.get("id"), "name": p.get("name"), "status": p.get("status")}
            for p in szv_processes
        ],
        "api_can": api_can,
        "api_needs_ui": api_needs_ui,
    }
    save_json(RUN_LOG_DIR / "inventory.json", payload)

    print(f"Wrote {report_path}")
    print(f"Wrote {RUN_LOG_DIR / 'inventory.json'}")
    print(
        f"Employees={len(employees)} Locations={len(locations)} "
        f"LegalEntities={len(legal_entities)} Jobs={len(job_postings)} "
        f"Processes={len(processes)}"
    )
    missing = [c["full_name"] for c in cast_resolution if not c["found"] and not c["rename_from_found"]]
    if missing:
        print("INFO missing cast (will be created by seed):", ", ".join(missing))
    if not probes["performance/review_processes"]["ok"]:
        print("WARNING: Performance review_processes not readable")
        return 3
    if not probes["api_public/credentials"]["ok"]:
        print("WARNING: credentials failed — check API_KEY / AUTH_TYPE")
        return 4
    print("Inventory OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
