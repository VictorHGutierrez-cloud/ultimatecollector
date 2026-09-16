#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventário da conta Factorial para a demo LIAT AIR (company 191947)."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("liat-air")

LIAT_CLIENT_DIR = ROOT / "clients" / "liat-air"
sys.path.insert(0, str(LIAT_CLIENT_DIR))
from api_helpers import (  # noqa: E402
    DEMO_DIR,
    RUN_LOG_DIR,
    LiatApi,
    load_catalog,
    normalize_name,
    save_json,
)


def probe(api: LiatApi, path: str) -> dict:
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
    api = LiatApi()
    catalog = load_catalog()

    print("=== LIAT AIR Inventory ===")
    print(f"BASE_URL={api.config.BASE_URL}")
    print(f"API_VERSION={api.version}")
    print(f"AUTH_TYPE={api.config.AUTH_TYPE}")
    print(f"COMPANY_FOCUS={catalog.get('company_id')}")

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
                "found": bool(emp),
                "rename_from_found": bool(rename_emp),
                "employee_id": emp.get("id") if emp else (rename_emp.get("id") if rename_emp else None),
            }
        )

    liat_processes = [p for p in processes if str(p.get("name", "")).startswith("LIAT")]
    liat_locations = [
        l for l in locations if "LIAT" in str(l.get("name", "")) or "VC Bird" in str(l.get("name", ""))
    ]

    report_lines = [
        "# LIAT AIR Inventory Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Company focus: {catalog.get('company_id')}",
        f"Base URL: `{api.config.BASE_URL}`",
        "",
        "## Totals",
        "",
        f"- Employees: {len(employees)}",
        f"- Teams: {len(teams)}",
        f"- Locations: {len(locations)} (LIAT: {len(liat_locations)})",
        f"- Legal entities: {len(legal_entities)}",
        f"- Review processes: {len(processes)} (LIAT-prefixed: {len(liat_processes)})",
        f"- Trainings: {len(trainings)}",
        "",
        "## Cast resolution",
        "",
    ]
    for row in cast_resolution:
        status = "FOUND" if row["found"] else ("RENAME_SOURCE" if row["rename_from_found"] else "MISSING")
        report_lines.append(
            f"- {row['full_name']} ({row['group']}): **{status}** employee_id={row['employee_id']}"
        )

    report_path = DEMO_DIR / "inventory_report.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company_focus": catalog.get("company_id"),
        "counts": {
            "employees": len(employees),
            "teams": len(teams),
            "locations": len(locations),
            "review_processes": len(processes),
            "liat_review_processes": len(liat_processes),
            "trainings": len(trainings),
        },
        "cast_resolution": cast_resolution,
        "probes": {k: {kk: vv for kk, vv in v.items() if kk != "sample"} for k, v in probes.items()},
    }
    save_json(RUN_LOG_DIR / "inventory.json", payload)

    print(f"Wrote {report_path}")
    print(f"Employees={len(employees)} Processes={len(processes)} LIAT={len(liat_processes)}")
    if not probes["performance/review_processes"]["ok"]:
        print("WARNING: Performance module not readable")
        return 3
    print("Inventory OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
