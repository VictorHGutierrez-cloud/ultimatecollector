#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventário da conta Factorial para a demo CDH Malawi (company 188450)."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("cdh-malawi")

CDH_CLIENT_DIR = ROOT / "clients" / "cdh-malawi"
sys.path.insert(0, str(CDH_CLIENT_DIR))
from api_helpers import (  # noqa: E402
    DEMO_DIR,
    RUN_LOG_DIR,
    CdhApi,
    load_catalog,
    normalize_name,
    save_json,
)


def probe(api: CdhApi, path: str) -> dict:
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


def main() -> int:
    api = CdhApi()
    catalog = load_catalog()

    print("=== CDH Malawi Inventory ===")
    print(f"BASE_URL={api.config.BASE_URL}")
    print(f"API_VERSION={api.version}")
    print(f"AUTH_TYPE={api.config.AUTH_TYPE}")
    print(f"COMPANY_FOCUS={catalog.get('company_id')}")
    print(f"SCOPE={catalog.get('scope')} YEAR={catalog.get('year')}")

    endpoints = [
        "api_public/credentials",
        "employees/employees",
        "teams/teams",
        "locations/locations",
        "companies/legal_entities",
        "performance/review_processes",
        "performance/company_employee_score_scales",
        "trainings/trainings",
        "posts/groups",
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
                "role_title": person.get("role_title"),
                "star_scorecard": bool(person.get("star_scorecard")),
                "found": bool(emp),
                "rename_from": rename_from,
                "rename_from_found": bool(rename_emp),
                "employee_id": emp.get("id") if emp else (rename_emp.get("id") if rename_emp else None),
            }
        )

    cdh_processes = [p for p in processes if str(p.get("name", "")).startswith("CDH")]
    cdh_locations = [
        l
        for l in locations
        if "CDH" in str(l.get("name", "")) or "Lilongwe" in str(l.get("name", ""))
    ]
    cdh_teams = [t for t in teams if str(t.get("name", "")).startswith("CDH")]

    ready_to_rename = sum(1 for r in cast_resolution if r["rename_from_found"] and not r["found"])
    already_named = sum(1 for r in cast_resolution if r["found"])
    missing = sum(1 for r in cast_resolution if not r["found"] and not r["rename_from_found"])

    report_lines = [
        "# CDH Malawi Inventory Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Company focus: {catalog.get('company_id')} · {catalog.get('display_name')}",
        f"Scope: **{catalog.get('scope')}** · Year: **{catalog.get('year')}**",
        f"Base URL: `{api.config.BASE_URL}`",
        "",
        "## What this report is",
        "",
        "A snapshot of what already exists in the Factorial demo account,",
        "compared with the planned cast in `catalog.json` (the demo recipe).",
        "",
        "## Totals (current account)",
        "",
        f"- Employees: {len(employees)}",
        f"- Teams: {len(teams)} (CDH-prefixed: {len(cdh_teams)})",
        f"- Locations: {len(locations)} (CDH/Lilongwe: {len(cdh_locations)})",
        f"- Legal entities: {len(legal_entities)}",
        f"- Review processes: {len(processes)} (CDH-prefixed: {len(cdh_processes)})",
        f"- Trainings: {len(trainings)}",
        "",
        "## Planned demo (from catalog)",
        "",
        f"- Cast size: {len(catalog.get('cast', []))}",
        f"- Teams planned: {len(catalog.get('teams', []))}",
        f"- Review processes planned: {len(catalog.get('review_processes', []))}",
        f"- Star scorecard: **{catalog.get('demo_focus', {}).get('star_employee')}** "
        f"(appraiser: {catalog.get('demo_focus', {}).get('star_appraiser')})",
        f"- Weighting: {catalog.get('weighting', {}).get('manager', {})}",
        "",
        "## Cast resolution",
        "",
        f"- Already renamed to CDH names: **{already_named}**",
        f"- Ready to rename (source employee exists): **{ready_to_rename}**",
        f"- Missing source: **{missing}**",
        "",
    ]
    for row in cast_resolution:
        if row["found"]:
            status = "FOUND (already CDH name)"
        elif row["rename_from_found"]:
            status = f"READY_TO_RENAME from {row['rename_from']}"
        else:
            status = "MISSING"
        star = " ★" if row["star_scorecard"] else ""
        report_lines.append(
            f"- {row['full_name']}{star} ({row['group']} · {row.get('role_title')}): "
            f"**{status}** employee_id={row['employee_id']}"
        )

    report_lines.extend(
        [
            "",
            "## Current locations (sample)",
            "",
        ]
    )
    for loc in locations:
        report_lines.append(f"- {loc.get('name')}")

    report_lines.extend(["", "## Current review processes", ""])
    for p in processes:
        report_lines.append(f"- {p.get('name')} ({p.get('status')})")

    report_lines.extend(
        [
            "",
            "## Next step",
            "",
            "When you approve, we run the **seed** (populate CDH names, location,",
            "teams, BSC review cycles, trainings). First as `--dry-run`, then `--apply`.",
            "",
        ]
    )

    report_path = DEMO_DIR / "inventory_report.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company_focus": catalog.get("company_id"),
        "display_name": catalog.get("display_name"),
        "scope": catalog.get("scope"),
        "year": catalog.get("year"),
        "counts": {
            "employees": len(employees),
            "teams": len(teams),
            "cdh_teams": len(cdh_teams),
            "locations": len(locations),
            "cdh_locations": len(cdh_locations),
            "legal_entities": len(legal_entities),
            "review_processes": len(processes),
            "cdh_review_processes": len(cdh_processes),
            "trainings": len(trainings),
        },
        "cast_resolution": cast_resolution,
        "cast_summary": {
            "already_named": already_named,
            "ready_to_rename": ready_to_rename,
            "missing": missing,
        },
        "probes": {k: {kk: vv for kk, vv in v.items() if kk != "sample"} for k, v in probes.items()},
    }
    save_json(RUN_LOG_DIR / "inventory.json", payload)

    print(f"Wrote {report_path}")
    print(
        f"Employees={len(employees)} Processes={len(processes)} "
        f"CDH_procs={len(cdh_processes)} Rename_ready={ready_to_rename}"
    )
    if not probes["performance/review_processes"]["ok"]:
        print("WARNING: Performance module not readable")
        return 3
    print("Inventory OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
