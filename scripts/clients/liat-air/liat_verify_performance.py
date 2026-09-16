#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica se o seed LIAT AIR está pronto para demo (company 191947)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("liat-air")

LIAT_CLIENT_DIR = ROOT / "clients" / "liat-air"
sys.path.insert(0, str(LIAT_CLIENT_DIR))
from api_helpers import (  # noqa: E402
    RUN_LOG_DIR,
    LiatApi,
    load_catalog,
    normalize_name,
)


def emp_name(e: dict) -> str:
    return e.get("full_name") or f"{e.get('first_name', '')} {e.get('last_name', '')}".strip()


def load_seed_ids() -> dict:
    path = RUN_LOG_DIR / "seed_latest.json"
    if not path.exists():
        return {}
    try:
        return (json.loads(path.read_text(encoding="utf-8")).get("ids") or {})
    except Exception:
        return {}


def main() -> int:
    api = LiatApi()
    catalog = load_catalog()
    seed_ids = load_seed_ids()
    print("=== LIAT AIR Verify Demo ===")
    print(f"Company focus: {catalog.get('company_id')}")

    ok = True
    employees = api.list_all("employees/employees")
    by_name = {normalize_name(emp_name(e)): e for e in employees}

    print("\nCast:")
    cast_access = []
    for person in catalog["cast"]:
        emp = by_name.get(normalize_name(person["full_name"]))
        if not emp:
            print(f"  FAIL missing {person['full_name']}")
            ok = False
            continue
        active = emp.get("active") is not False and not emp.get("terminated_on")
        cast_access.append(str(emp.get("access_id")))
        mark = "OK" if active else "FAIL inactive"
        if not active:
            ok = False
        print(
            f"  {mark} {person['full_name']} "
            f"id={emp.get('id')} manager={emp.get('manager_id')}"
        )

    print("\nLocation:")
    loc_name = catalog["location"]["name"]
    locations = api.list_all("locations/locations")
    found_loc = next((l for l in locations if l.get("name") == loc_name), None)
    if found_loc:
        print(f"  OK {loc_name} id={found_loc.get('id')}")
    else:
        print(f"  FAIL missing {loc_name}")
        ok = False

    print("\nLegal entity:")
    le_name = catalog["legal_entity"]["legal_name"]
    entities = api.list_all("companies/legal_entities")
    found_le = next((le for le in entities if le.get("legal_name") == le_name), None)
    if found_le:
        print(f"  OK {le_name} id={found_le.get('id')}")
    else:
        print(f"  WARN missing exact name '{le_name}'")

    print("\nTeams:")
    teams = api.list_all("teams/teams")
    for team in catalog["teams"]:
        found = next((t for t in teams if t.get("name") == team["name"]), None)
        if found:
            print(f"  OK {team['name']} id={found.get('id')}")
        else:
            print(f"  FAIL missing {team['name']}")
            ok = False

    print("\nReview processes:")
    processes = api.list_all("performance/review_processes")
    for process_def in catalog["review_processes"]:
        found = next((p for p in processes if p.get("name") == process_def["name"]), None)
        if not found:
            print(f"  FAIL missing {process_def['name']}")
            ok = False
            continue
        pid = str(found.get("id"))
        st, est = api.get(
            "performance/review_process_estimated_targets",
            {"performance_review_process_ids[]": [pid]},
        )
        targets = (est or {}).get("data") or [] if st == 200 else []
        target_access = {str(t.get("access_id")) for t in targets}
        coverage = sum(1 for a in cast_access if a in target_access)
        mark = "OK" if coverage >= max(1, len(cast_access) - 2) else "WARN"
        print(
            f"  {mark} {process_def['name']} id={pid} status={found.get('status')} "
            f"cast_targets={coverage}/{len(cast_access)}"
        )

    print("\nTrainings:")
    trainings = api.list_all("trainings/trainings")
    for training in catalog["trainings"]:
        found = next((t for t in trainings if t.get("name") == training["name"]), None)
        if found:
            print(f"  OK {training['name']} id={found.get('id')}")
        else:
            print(f"  FAIL missing {training['name']}")
            ok = False

    print("\nPosts:")
    known_post_ids = [str(x) for x in (seed_ids.get("posts") or []) if x]
    if known_post_ids:
        st, body = api.get("posts/posts", params={"ids[]": known_post_ids})
        for p in ((body or {}).get("data") or []) if st == 200 else []:
            print(f"  OK {p.get('title')} id={p.get('id')}")
    else:
        print("  WARN no post IDs in seed_latest.json — check Announcements UI")

    print("\nUI checklist (manual):")
    for key, value in catalog.get("ui_checklist", {}).items():
        print(f"  - {key}: {value}")

    if ok:
        print("\nVERIFY PASSED")
        return 0
    print("\nVERIFY FAILED — review items above")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
