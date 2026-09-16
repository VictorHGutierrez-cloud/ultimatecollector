#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica se o seed SZV está pronto para a demo (company 167952)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from clients.szv.api_helpers import (  # noqa: E402
    RUN_LOG_DIR,
    SzvApi,
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
        import json

        return (json.loads(path.read_text(encoding="utf-8")).get("ids") or {})
    except Exception:
        return {}


def main() -> int:
    api = SzvApi()
    catalog = load_catalog()
    seed_ids = load_seed_ids()
    print("=== SZV Verify Demo ===")
    print(f"Company focus: {catalog.get('company_id')}")
    print(f"AUTH_TYPE={api.config.AUTH_TYPE}")

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
            f"id={emp.get('id')} access={emp.get('access_id')} manager={emp.get('manager_id')}"
        )

    print("\nLocation:")
    locations = api.list_all("locations/locations")
    loc_name = catalog["location"]["name"]
    found_loc = next((l for l in locations if l.get("name") == loc_name), None)
    if found_loc:
        print(
            f"  OK {loc_name} id={found_loc.get('id')} "
            f"city={found_loc.get('city')} country={found_loc.get('country')}"
        )
    else:
        print(f"  FAIL missing {loc_name}")
        ok = False

    print("\nLegal entity:")
    entities = api.list_all("companies/legal_entities")
    le_name = catalog["legal_entity"]["legal_name"]
    found_le = next((le for le in entities if le.get("legal_name") == le_name), None)
    if found_le:
        print(
            f"  OK {le_name} id={found_le.get('id')} "
            f"country={found_le.get('country')} currency={found_le.get('currency')}"
        )
    else:
        # Soft warn — create may fall back to existing entity
        print(f"  WARN missing exact name '{le_name}' (may have used fallback entity)")
        for le in entities:
            print(f"       existing: {le.get('legal_name')} ({le.get('id')})")

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
        status = found.get("status")
        archived = found.get("archived")
        st, est = api.get(
            "performance/review_process_estimated_targets",
            {"performance_review_process_ids[]": [pid]},
        )
        targets = (est or {}).get("data") or [] if st == 200 else []
        target_access = {str(t.get("access_id")) for t in targets}
        coverage = sum(1 for a in cast_access if a in target_access)
        min_cov = max(1, len(cast_access) - 2)
        mark = "OK" if coverage >= min_cov and not archived else "WARN"
        if archived or coverage < min_cov - 1:
            ok = False
        print(
            f"  {mark} {process_def['name']} id={pid} status={status} "
            f"archived={archived} cast_targets={coverage}/{len(cast_access)}"
        )

        st, q = api.get(
            "performance/review_questionnaire_by_strategies",
            {"performance_review_process_ids[]": [pid], "limit": 10},
        )
        qdata = (q or {}).get("data") or [] if st == 200 else []
        print(f"       questionnaires={len(qdata)}")

    print("\nTrainings:")
    trainings = api.list_all("trainings/trainings")
    for training in catalog["trainings"]:
        found = next((t for t in trainings if t.get("name") == training["name"]), None)
        if found:
            print(f"  OK {training['name']} id={found.get('id')}")
        else:
            print(f"  FAIL missing {training['name']}")
            ok = False

    print("\nJob postings:")
    jobs = api.list_all("ats/job_postings")
    for job in catalog.get("job_postings", []):
        found = next((j for j in jobs if j.get("title") == job["title"]), None)
        if found:
            print(f"  OK {job['title']} id={found.get('id')} status={found.get('status')}")
        else:
            print(f"  FAIL missing {job['title']}")
            ok = False

    print("\nOnboarding tasks:")
    tasks = api.list_all("tasks/tasks")
    onboarding_tasks = (catalog.get("onboarding") or {}).get("tasks") or []
    for task in onboarding_tasks:
        found = next((t for t in tasks if t.get("name") == task["name"]), None)
        if found:
            print(f"  OK {task['name']} id={found.get('id')} status={found.get('status')}")
        else:
            print(f"  FAIL missing {task['name']}")
            ok = False

    print("\nCandidates:")
    candidates = api.list_all("ats/candidates")
    by_email = {normalize_name(c.get("email") or ""): c for c in candidates}
    for cand in catalog.get("candidates", []):
        found = by_email.get(normalize_name(cand["email"]))
        if found:
            print(
                f"  OK {cand['first_name']} {cand['last_name']} "
                f"id={found.get('id')} job={cand['job_title']}"
            )
        else:
            # applications/apply may create without listing immediately by email
            print(f"  WARN missing candidate email {cand['email']} (check Applications UI)")

    print("\nPosts:")
    groups = api.list_all("posts/groups")
    group_def = catalog.get("posts_group") or {}
    group = next((g for g in groups if g.get("title") == group_def.get("title")), None)
    if group_def:
        if group:
            print(f"  OK group {group_def.get('title')} id={group.get('id')}")
        else:
            print(f"  FAIL missing post group {group_def.get('title')}")
            ok = False
    # Unscoped posts list is often empty; resolve via seed ids or title match on id fetch
    known_post_ids = [str(x) for x in (seed_ids.get("posts") or []) if x]
    posts_by_title = {}
    if known_post_ids:
        st, body = api.get("posts/posts", params={"ids[]": known_post_ids})
        for p in ((body or {}).get("data") or []) if st == 200 else []:
            posts_by_title[normalize_name(p.get("title"))] = p
    if group and not posts_by_title:
        for p in api.list_all("posts/posts", params={"groups[]": [str(group.get("id"))]}):
            posts_by_title[normalize_name(p.get("title"))] = p

    for post in catalog.get("posts", []):
        found = posts_by_title.get(normalize_name(post["title"]))
        if found:
            print(f"  OK {post['title']} id={found.get('id')}")
        else:
            # Soft warn: API may hide unpublished posts from list endpoints
            print(
                f"  WARN post '{post['title']}' not listed "
                f"(open Announcements UI; create via seed if missing)"
            )

    print("\nUI checklist (manual):")
    for key, value in catalog.get("ui_checklist", {}).items():
        print(f"  - {key}: {value}")

    print("\nAgreements note:")
    print(
        "  API key often cannot initiate action plans (403 policy). "
        "Initiate agreements in the Factorial UI as admin if needed."
    )
    print("\nOut of scope:")
    print("  Time tracking / attendance was intentionally NOT personalized.")

    if ok:
        print("\nVERIFY PASSED")
        return 0
    print("\nVERIFY FAILED / WARNINGS — review items above")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
