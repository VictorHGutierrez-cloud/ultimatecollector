#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventário da conta Factorial para a demo Kibanda (company 191232)."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("glovo-sibasi")

CLIENT_DIR = ROOT / "clients" / "glovo-sibasi"
sys.path.insert(0, str(CLIENT_DIR))
from api_helpers import (  # noqa: E402
    RUN_LOG_DIR,
    KibandaApi,
    emp_name,
    load_catalog,
    normalize_name,
    save_json,
)


def probe(api: KibandaApi, path: str) -> dict:
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


def main() -> int:
    api = KibandaApi()
    catalog = load_catalog()

    print("=== Kibanda Inventory ===")
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
        "posts/groups",
        "documents/documents",
        "documents/folders",
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
    post_groups = api.list_all("posts/groups") if probes["posts/groups"]["ok"] else []
    documents = api.list_all("documents/documents") if probes["documents/documents"]["ok"] else []

    active = [
        e
        for e in employees
        if e.get("active") is not False and not e.get("terminated_on")
    ]

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
                "found": bool(emp),
                "rename_from": rename_from,
                "rename_from_found": bool(rename_emp),
                "employee_id": emp.get("id") if emp else (rename_emp.get("id") if rename_emp else None),
            }
        )

    kibanda_locations = [l for l in locations if "Kibanda" in str(l.get("name", ""))]
    kibanda_teams = [t for t in teams if str(t.get("name", "")).startswith("Kibanda")]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company_id": catalog.get("company_id"),
        "probes": {k: {kk: vv for kk, vv in v.items() if kk != "sample"} for k, v in probes.items()},
        "counts": {
            "employees": len(employees),
            "active_employees": len(active),
            "teams": len(teams),
            "locations": len(locations),
            "legal_entities": len(legal_entities),
            "post_groups": len(post_groups),
            "documents": len(documents),
            "kibanda_locations": len(kibanda_locations),
            "kibanda_teams": len(kibanda_teams),
        },
        "active_employees": [
            {
                "id": e.get("id"),
                "name": emp_name(e),
                "email": e.get("email") or e.get("login_email"),
                "location_id": e.get("location_id"),
            }
            for e in active
        ],
        "locations": [{"id": l.get("id"), "name": l.get("name")} for l in locations],
        "teams": [{"id": t.get("id"), "name": t.get("name")} for t in teams],
        "legal_entities": [
            {"id": le.get("id"), "legal_name": le.get("legal_name"), "currency": le.get("currency")}
            for le in legal_entities
        ],
        "post_groups": [{"id": g.get("id"), "title": g.get("title")} for g in post_groups],
        "cast_resolution": cast_resolution,
    }
    save_json(RUN_LOG_DIR / "inventory.json", payload)

    lines = [
        "# Kibanda inventory report",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"Company: `{catalog.get('company_id')}` · scope `{catalog.get('scope')}`",
        "",
        "## Counts",
        "",
        "| Resource | Count |",
        "|----------|------:|",
    ]
    for k, v in payload["counts"].items():
        lines.append(f"| {k} | {v} |")

    lines.extend(["", "## Active employees (rename pool)", ""])
    for e in payload["active_employees"][:60]:
        lines.append(f"- `{e['id']}` {e['name']} ({e.get('email') or 'no email'})")

    lines.extend(["", "## Locations", ""])
    for loc in payload["locations"]:
        lines.append(f"- `{loc['id']}` {loc['name']}")

    lines.extend(["", "## Teams", ""])
    for team in payload["teams"]:
        lines.append(f"- `{team['id']}` {team['name']}")

    lines.extend(["", "## Legal entities", ""])
    for le in payload["legal_entities"]:
        lines.append(f"- `{le['id']}` {le['legal_name']} ({le.get('currency')})")

    lines.extend(["", "## Cast resolution", ""])
    for row in cast_resolution:
        status = "FOUND" if row["found"] else ("RENAME_SRC" if row["rename_from_found"] else "MISSING")
        lines.append(
            f"- [{status}] {row['full_name']} ← {row.get('rename_from') or '—'} "
            f"({row.get('role_title')})"
        )

    report = CLIENT_DIR / "inventory_report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {RUN_LOG_DIR / 'inventory.json'}")
    print(f"Wrote {report}")
    print(f"Active employees: {len(active)} | Cast missing: {sum(1 for r in cast_resolution if not r['found'] and not r['rename_from_found'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
