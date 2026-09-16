#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed demo SZV na Factorial (company 167952).

Inclui: location, legal entity, cast (create/rename), teams, managers,
performance P1/P2/P3, trainings, job postings. Não toca time tracking.

Uso:
  python scripts/szv_seed_performance.py --dry-run
  python scripts/szv_seed_performance.py --apply
"""

from __future__ import annotations

import argparse
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from clients.szv.api_helpers import (  # noqa: E402
    RUN_LOG_DIR,
    SzvApi,
    load_catalog,
    normalize_name,
    save_json,
)


def new_uuid() -> str:
    return str(uuid.uuid4())


def emp_name(e: dict) -> str:
    return e.get("full_name") or f"{e.get('first_name', '')} {e.get('last_name', '')}".strip()


def _short(body: Any, limit: int = 240) -> Any:
    text = str(body)
    return text if len(text) <= limit else text[:limit] + "..."


def build_szv_questionnaire(catalog: dict, phase_key: str) -> List[dict]:
    """Questionário com Objetivos, Core Values e Competências."""
    scale_codes = [f"{r['code']} — {r['label']}: {r['definition']}" for r in catalog["rating_scale"]]

    objective_questions = []
    for category in catalog["goal_categories"]:
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": (
                    f"[{category}] Rate goal achievement for this category. "
                    f"Use SZV scale guidance: {'; '.join(r['code'] for r in catalog['rating_scale'])}."
                ),
                "answer_type": "rating",
            }
        )
    objective_questions.append(
        {
            "uuid": new_uuid(),
            "mandatory": True,
            "with_comment": True,
            "title": (
                "List or confirm the employee's SMART goals for this cycle "
                "(include measure and due date). Align to department KPIs."
            ),
            "answer_type": "text",
        }
    )
    if phase_key == "p2":
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": "Mid-year progress notes, challenges, and any approved goal adjustments.",
                "answer_type": "text",
            }
        )
    if phase_key == "p3":
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": "Year-end evidence summary vs agreed measures and proposed next-year development focus.",
                "answer_type": "text",
            }
        )

    value_questions = []
    for value in catalog["core_values"]:
        value_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": f"{value['name']} — Observable behaviors: {value['behaviors']}",
                "answer_type": "rating",
            }
        )

    competency_names = []
    for group_key in ("all_employees", "management", "executive"):
        for name in catalog["competencies"][group_key]:
            if name not in competency_names:
                competency_names.append(name)

    competency_questions = [
        {
            "uuid": new_uuid(),
            "mandatory": True,
            "with_comment": True,
            "title": f"{name} — Rate observable competency demonstration.",
            "answer_type": "rating",
        }
        for name in competency_names
    ]

    coaching_questions = [
        {
            "uuid": new_uuid(),
            "mandatory": True,
            "with_comment": True,
            "title": "Coaching action (what), owner, and follow-up date.",
            "answer_type": "text",
        },
        {
            "uuid": new_uuid(),
            "mandatory": False,
            "with_comment": True,
            "title": "Development / training commitments for the next period.",
            "answer_type": "text",
        },
    ]

    return [
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": "SZV Performance Objectives",
            "questions": objective_questions,
        },
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": "SZV Core Values",
            "questions": value_questions,
        },
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": "SZV Competencies",
            "questions": competency_questions,
        },
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": "SZV Coaching & Development",
            "questions": coaching_questions,
        },
        {
            "uuid": new_uuid(),
            "type": "question",
            "questions": [
                {
                    "uuid": new_uuid(),
                    "mandatory": False,
                    "with_comment": False,
                    "title": "SZV rating reference (informational)",
                    "answer_type": "multiple_choice",
                    "max_choices": 1,
                    "choice_options": scale_codes,
                }
            ],
        },
    ]


class SzvSeeder:
    def __init__(self, apply: bool) -> None:
        self.apply = apply
        self.api = SzvApi()
        self.catalog = load_catalog()
        self.log: Dict[str, Any] = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "mode": "apply" if apply else "dry-run",
            "company_id": self.catalog.get("company_id"),
            "actions": [],
            "errors": [],
            "ids": {},
        }
        self.location_id: Optional[str] = None
        self.legal_entity_id: Optional[str] = None

    def action(self, name: str, detail: Any = None) -> None:
        entry = {"action": name, "detail": detail}
        self.log["actions"].append(entry)
        print(f"- {name}: {detail}")

    def error(self, name: str, detail: Any = None) -> None:
        entry = {"action": name, "detail": detail}
        self.log["errors"].append(entry)
        print(f"! ERROR {name}: {detail}")

    def ensure_location(self) -> Optional[str]:
        loc_def = self.catalog["location"]
        locations = self.api.list_all("locations/locations")
        by_name = {normalize_name(l.get("name")): l for l in locations}
        existing = by_name.get(normalize_name(loc_def["name"]))
        if not existing:
            # Prefer renaming a non-SZV office if only generic locations exist
            for loc in locations:
                name = str(loc.get("name") or "")
                if "SZV" not in name and "Philipsburg" not in name:
                    existing = loc
                    break

        if existing and normalize_name(existing.get("name")) == normalize_name(loc_def["name"]):
            self.location_id = str(existing["id"])
            self.action("location_exists", {"id": self.location_id, "name": loc_def["name"]})
            self.log["ids"]["location_id"] = self.location_id
            return self.location_id

        payload = {
            "name": loc_def["name"],
            "country": loc_def["country"],
            "timezone": loc_def["timezone"],
            "company_id": str(self.catalog["company_id"]),
            "city": loc_def.get("city"),
            "state": loc_def.get("state"),
            "postal_code": loc_def.get("postal_code"),
            "address_line_one": loc_def.get("address_line_one"),
            "phone_number": loc_def.get("phone_number"),
            "main": bool(loc_def.get("main", True)),
            "latitude": loc_def.get("latitude"),
            "longitude": loc_def.get("longitude"),
        }

        if existing and self.apply:
            # Update existing generic office into Philipsburg
            put_payload = {"id": str(existing["id"]), **payload}
            st, body = self.api.put(f"locations/locations/{existing['id']}", put_payload)
            if st in (200, 201):
                self.location_id = str(existing["id"])
                self.action("updated_location", {"id": self.location_id, "name": loc_def["name"]})
                self.log["ids"]["location_id"] = self.location_id
                return self.location_id
            self.action(
                "update_location_failed_try_create",
                {"status": st, "body": _short(body)},
            )

        if not self.apply:
            self.action("dry_create_location", payload)
            self.location_id = "dry-location"
            self.log["ids"]["location_id"] = self.location_id
            return self.location_id

        # Try preferred country/timezone, then fallbacks
        attempts = [
            dict(payload),
            {
                **payload,
                "country": loc_def.get("country_fallback", "us"),
                "timezone": loc_def.get("timezone_fallback", "America/Puerto_Rico"),
            },
        ]
        for attempt in attempts:
            st, body = self.api.post("locations/locations", attempt)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                self.location_id = str(body["id"])
                self.action("created_location", {"id": self.location_id, "payload": attempt})
                self.log["ids"]["location_id"] = self.location_id
                return self.location_id
            self.action("create_location_attempt_failed", {"status": st, "body": _short(body)})

        # Keep existing location id if update/create failed
        if existing:
            self.location_id = str(existing["id"])
            self.error(
                "location_fallback_existing",
                {"id": self.location_id, "name": existing.get("name")},
            )
            self.log["ids"]["location_id"] = self.location_id
            return self.location_id

        self.error("create_location_failed", "no location available")
        return None

    def ensure_legal_entity(self) -> Optional[str]:
        le_def = self.catalog["legal_entity"]
        entities = self.api.list_all("companies/legal_entities")
        for le in entities:
            if normalize_name(le.get("legal_name")) == normalize_name(le_def["legal_name"]):
                self.legal_entity_id = str(le["id"])
                self.action(
                    "legal_entity_exists",
                    {"id": self.legal_entity_id, "name": le_def["legal_name"]},
                )
                self.log["ids"]["legal_entity_id"] = self.legal_entity_id
                return self.legal_entity_id

        payload = {
            "company_id": str(self.catalog["company_id"]),
            "country": le_def["country"],
            "legal_name": le_def["legal_name"],
            "currency": le_def["currency"],
            "city": le_def.get("city"),
            "state": le_def.get("state"),
            "postal_code": le_def.get("postal_code"),
            "address_line_1": le_def.get("address_line_1"),
            "tin": le_def.get("tin"),
        }
        if not self.apply:
            self.action("dry_create_legal_entity", payload)
            # Prefer an existing entity for dry-run downstream refs
            if entities:
                self.legal_entity_id = str(entities[0]["id"])
            else:
                self.legal_entity_id = "dry-legal-entity"
            self.log["ids"]["legal_entity_id"] = self.legal_entity_id
            return self.legal_entity_id

        attempts = [
            dict(payload),
            {**payload, "country": le_def.get("country_fallback", "us")},
        ]
        for attempt in attempts:
            st, body = self.api.post("companies/legal_entities", attempt)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                self.legal_entity_id = str(body["id"])
                self.action("created_legal_entity", {"id": self.legal_entity_id, "country": attempt["country"]})
                self.log["ids"]["legal_entity_id"] = self.legal_entity_id
                return self.legal_entity_id
            self.action("create_legal_entity_attempt_failed", {"status": st, "body": _short(body)})

        if entities:
            # Prefer USD entity if present
            preferred = next((e for e in entities if e.get("currency") == "USD"), entities[0])
            self.legal_entity_id = str(preferred["id"])
            self.error(
                "legal_entity_fallback_existing",
                {"id": self.legal_entity_id, "name": preferred.get("legal_name")},
            )
            self.log["ids"]["legal_entity_id"] = self.legal_entity_id
            return self.legal_entity_id

        self.error("create_legal_entity_failed", "no legal entity available")
        return None

    def ensure_cast(self) -> Dict[str, dict]:
        employees = self.api.list_all("employees/employees")
        by_name = {normalize_name(emp_name(e)): e for e in employees}
        by_email = {
            normalize_name(e.get("email") or e.get("login_email") or ""): e for e in employees if e.get("email") or e.get("login_email")
        }
        resolved: Dict[str, dict] = {}

        for person in self.catalog["cast"]:
            emp = by_name.get(normalize_name(person["full_name"]))
            if not emp and person.get("email"):
                emp = by_email.get(normalize_name(person["email"]))

            # Rename path from demo default person
            if not emp and person.get("rename_from"):
                source = by_name.get(normalize_name(person["rename_from"]))
                if source:
                    payload = {
                        "id": str(source["id"]),
                        "first_name": person["first_name"],
                        "last_name": person["last_name"],
                    }
                    if not self.apply:
                        self.action("dry_rename_employee", {"from": person["rename_from"], **payload})
                        emp = {**source, **payload, "full_name": person["full_name"]}
                    else:
                        st, body = self.api.put(f"employees/employees/{source['id']}", payload)
                        if st in (200, 201):
                            self.action(
                                "renamed_employee",
                                {"from": person["rename_from"], "to": person["full_name"], "id": source["id"]},
                            )
                            emp = body if isinstance(body, dict) else {**source, **payload}
                            by_name[normalize_name(person["full_name"])] = emp
                        else:
                            self.error(
                                "rename_employee_failed",
                                {"status": st, "body": body, "payload": payload},
                            )

            if not emp:
                payload = {
                    "company_id": str(self.catalog["company_id"]),
                    "first_name": person["first_name"],
                    "last_name": person["last_name"],
                    "email": person["email"],
                    "gender": person.get("gender"),
                    "contract_starts_on": "2025-01-15",
                    "contract_effective_on": "2025-01-15",
                    "country": "us",
                    "nationality": "SX",
                    "city": "Philipsburg",
                    "state": "Sint Maarten",
                }
                if self.legal_entity_id and not str(self.legal_entity_id).startswith("dry-"):
                    payload["legal_entity_id"] = self.legal_entity_id
                if self.location_id and not str(self.location_id).startswith("dry-"):
                    payload["location_id"] = self.location_id

                if not self.apply:
                    self.action("dry_create_employee", payload)
                    resolved[person["full_name"]] = {
                        **person,
                        "employee_id": f"dry-{person['first_name'].lower()}",
                        "access_id": f"dry-access-{person['first_name'].lower()}",
                        "current_manager_id": None,
                    }
                    continue

                st, body = self.api.post("employees/employees/create_with_contract", payload)
                if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                    self.action(
                        "created_employee",
                        {"id": body.get("id"), "name": person["full_name"]},
                    )
                    emp = body
                    by_name[normalize_name(person["full_name"])] = emp
                else:
                    self.error(
                        "create_employee_failed",
                        {"status": st, "body": _short(body), "payload": payload},
                    )
                    continue

            if emp.get("active") is False or emp.get("terminated_on"):
                self.error(
                    "cast_inactive",
                    {
                        "full_name": person["full_name"],
                        "terminated_on": emp.get("terminated_on"),
                    },
                )
                continue

            # Align location / legal entity when possible
            if self.apply:
                updates = {"id": str(emp["id"])}
                if self.location_id and str(emp.get("location_id")) != str(self.location_id):
                    updates["location_id"] = self.location_id
                if self.legal_entity_id and str(emp.get("legal_entity_id")) != str(self.legal_entity_id):
                    updates["legal_entity_id"] = self.legal_entity_id
                # Ensure names match cast (in case found by email)
                if emp.get("first_name") != person["first_name"] or emp.get("last_name") != person["last_name"]:
                    updates["first_name"] = person["first_name"]
                    updates["last_name"] = person["last_name"]
                if len(updates) > 1:
                    st, body = self.api.put(f"employees/employees/{emp['id']}", updates)
                    self.action(
                        "aligned_employee_fields",
                        {"name": person["full_name"], "status": st, "updates": updates},
                    )
                    if st in (200, 201) and isinstance(body, dict):
                        emp = body

            resolved[person["full_name"]] = {
                **person,
                "employee_id": str(emp["id"]),
                "access_id": str(emp["access_id"]),
                "current_manager_id": str(emp["manager_id"]) if emp.get("manager_id") else None,
            }

        self.log["ids"]["cast"] = {
            k: {"employee_id": v["employee_id"], "access_id": v["access_id"], "group": v["group"]}
            for k, v in resolved.items()
        }
        return resolved

    def ensure_teams(self, cast: Dict[str, dict]) -> Dict[str, str]:
        teams = self.api.list_all("teams/teams")
        by_name = {normalize_name(t.get("name")): t for t in teams}
        team_ids: Dict[str, str] = {}

        for team in self.catalog["teams"]:
            existing = by_name.get(normalize_name(team["name"]))
            if existing:
                team_ids[team["key"]] = str(existing["id"])
                self.action(
                    "team_exists",
                    {"key": team["key"], "id": existing["id"], "name": team["name"]},
                )
                continue
            payload = {
                "name": team["name"],
                "description": f"SZV demo team for performance narrative ({team['key']})",
            }
            if not self.apply:
                self.action("dry_create_team", payload)
                team_ids[team["key"]] = f"dry-{team['key']}"
                continue
            status, body = self.api.post("teams/teams", payload)
            if status in (200, 201) and isinstance(body, dict) and body.get("id"):
                team_ids[team["key"]] = str(body["id"])
                self.action("created_team", {"id": body["id"], "name": team["name"]})
            else:
                self.error(
                    "create_team_failed",
                    {"status": status, "body": body, "payload": payload},
                )

        memberships = self.api.list_all("teams/memberships")
        membership_index = {
            (str(m.get("team_id")), str(m.get("employee_id"))): m for m in memberships
        }
        lead_by_team = {t["key"]: t.get("lead") for t in self.catalog["teams"]}

        for person in cast.values():
            team_key = person["team_key"]
            team_id = team_ids.get(team_key)
            if not team_id or str(team_id).startswith("dry-"):
                self.action("dry_skip_membership", person["full_name"])
                continue
            key = (team_id, person["employee_id"])
            is_lead = lead_by_team.get(team_key) == person["full_name"]
            if key in membership_index:
                self.action(
                    "membership_exists",
                    {"employee": person["full_name"], "team_id": team_id, "lead": is_lead},
                )
                continue
            payload = {
                "team_id": team_id,
                "employee_id": person["employee_id"],
                "lead": is_lead,
            }
            if not self.apply:
                self.action("dry_create_membership", payload)
                continue
            status, body = self.api.post("teams/memberships", payload)
            if status in (200, 201):
                self.action(
                    "created_membership",
                    {"employee": person["full_name"], "team_id": team_id, "lead": is_lead},
                )
            else:
                self.error(
                    "create_membership_failed",
                    {"status": status, "body": body, "payload": payload},
                )

        self.log["ids"]["teams"] = team_ids
        return team_ids

    def update_managers(self, cast: Dict[str, dict]) -> None:
        for employee_name, manager_name in self.catalog["manager_map"].items():
            emp = cast.get(employee_name)
            if not emp:
                continue
            desired_manager_id = None
            if manager_name:
                mgr = cast.get(manager_name)
                if not mgr:
                    self.error(
                        "manager_missing_in_cast",
                        {"employee": employee_name, "manager": manager_name},
                    )
                    continue
                desired_manager_id = mgr["employee_id"]
            if emp.get("current_manager_id") == desired_manager_id:
                self.action(
                    "manager_ok",
                    {"employee": employee_name, "manager_id": desired_manager_id},
                )
                continue
            payload = {"id": emp["employee_id"], "manager_id": desired_manager_id}
            if not self.apply:
                self.action("dry_update_manager", {"employee": employee_name, **payload})
                continue
            status, body = self.api.put(f"employees/employees/{emp['employee_id']}", payload)
            if status in (200, 201):
                self.action(
                    "updated_manager",
                    {"employee": employee_name, "manager_id": desired_manager_id},
                )
            else:
                self.error(
                    "update_manager_failed",
                    {"status": status, "body": body, "payload": payload},
                )

    def find_process_by_name(self, name: str) -> Optional[dict]:
        processes = self.api.list_all("performance/review_processes")
        for process in processes:
            if process.get("name") == name:
                return process
        return None

    def ensure_review_processes(self, cast: Dict[str, dict]) -> Dict[str, dict]:
        author = (
            cast.get("Margarita De Weever")
            or cast.get("Nadia Lejuez")
            or next(iter(cast.values()))
        )
        access_ids = [p["access_id"] for p in cast.values()]
        employee_ids = [p["employee_id"] for p in cast.values()]
        created: Dict[str, dict] = {}

        rating_scale = [
            {"value": idx + 1, "text": f"{item['code']} — {item['label']}: {item['definition']}"}
            for idx, item in enumerate(self.catalog["rating_scale"])
        ]

        for process_def in self.catalog["review_processes"]:
            existing = self.find_process_by_name(process_def["name"])
            if existing:
                created[process_def["key"]] = existing
                self.action(
                    "process_exists",
                    {
                        "key": process_def["key"],
                        "id": existing.get("id"),
                        "status": existing.get("status"),
                    },
                )
            else:
                payload = {
                    "author_access_id": author["access_id"],
                    "name": process_def["name"],
                    "description": process_def["description"],
                    "reviewer_strategies": process_def["reviewer_strategies"],
                    "target_strategy": "by_employees",
                    "arguments": employee_ids,
                    "ends_at": process_def["ends_at"],
                    "agreements_enabled": process_def["agreements_enabled"],
                    "employee_score_enabled": process_def["employee_score_enabled"],
                    "employee_potential_score_enabled": process_def[
                        "employee_potential_score_enabled"
                    ],
                    "competencies_assessments_enabled": process_def[
                        "competencies_assessments_enabled"
                    ],
                }
                if not self.apply:
                    self.action("dry_create_process", payload)
                    created[process_def["key"]] = {
                        "id": f"dry-{process_def['key']}",
                        "status": "draft",
                        **payload,
                    }
                    continue
                status, body = self.api.post("performance/review_processes", payload)
                if status in (200, 201) and isinstance(body, dict) and body.get("id"):
                    created[process_def["key"]] = body
                    self.action("created_process", {"key": process_def["key"], "id": body["id"]})
                else:
                    payload["target_strategy"] = "manual_selection"
                    payload["arguments"] = access_ids
                    status, body = self.api.post("performance/review_processes", payload)
                    if status in (200, 201) and isinstance(body, dict) and body.get("id"):
                        created[process_def["key"]] = body
                        self.action(
                            "created_process_manual",
                            {"key": process_def["key"], "id": body["id"]},
                        )
                    else:
                        self.error(
                            "create_process_failed",
                            {"status": status, "body": body, "payload": payload},
                        )
                        continue

            process = created[process_def["key"]]
            process_id = str(process.get("id"))
            if process_id.startswith("dry-"):
                continue

            if self.apply and process.get("status") in (None, "draft", "scheduled"):
                st, body = self.api.post(
                    "performance/review_processes/update_target_strategy",
                    {
                        "id": process_id,
                        "target_strategy": "by_employees",
                        "arguments": employee_ids,
                    },
                )
                self.action(
                    "update_target_strategy",
                    {"process_id": process_id, "status": st, "body": _short(body)},
                )

                st, body = self.api.post(
                    "performance/review_processes/update_deadline",
                    {"id": process_id, "ends_at": process_def["ends_at"]},
                )
                self.action("update_deadline", {"process_id": process_id, "status": st})

                for flag_name, enabled in [
                    ("update_agreements_configuration", process_def["agreements_enabled"]),
                    (
                        "update_competencies_assessments_configuration",
                        process_def["competencies_assessments_enabled"],
                    ),
                    ("update_employee_score_configuration", process_def["employee_score_enabled"]),
                ]:
                    payload = {"id": process_id, "enabled": bool(enabled)}
                    st, body = self.api.post(
                        f"performance/review_processes/{flag_name}",
                        payload,
                    )
                    self.action(
                        flag_name,
                        {"process_id": process_id, "status": st, "body": _short(body)},
                    )

                questionnaire = build_szv_questionnaire(self.catalog, process_def["key"])
                for strategy in process_def["reviewer_strategies"]:
                    st, body = self.api.post(
                        "performance/review_questionnaire_by_strategies/update_questionnaire_for_strategy",
                        {
                            "performance_review_process_id": process_id,
                            "strategy": strategy,
                            "questionnaire_content": questionnaire,
                        },
                    )
                    if st in (200, 201):
                        self.action(
                            "questionnaire_updated",
                            {"process_id": process_id, "strategy": strategy},
                        )
                    else:
                        self.error(
                            "questionnaire_failed",
                            {
                                "process_id": process_id,
                                "strategy": strategy,
                                "status": st,
                                "body": body,
                            },
                        )

                st, body = self.api.post(
                    "performance/review_questionnaire_by_strategies/update_default_rating_scale",
                    {
                        "performance_review_process_id": process_id,
                        "default_rating_scale": rating_scale,
                    },
                )
                self.action(
                    "rating_scale_updated",
                    {"process_id": process_id, "status": st, "body": _short(body)},
                )

                created[process_def["key"]] = (
                    self.find_process_by_name(process_def["name"]) or process
                )
            elif self.apply:
                self.action(
                    "skip_draft_config",
                    {
                        "process_id": process_id,
                        "status": process.get("status"),
                        "reason": "process already started",
                    },
                )

        self.log["ids"]["review_processes"] = {
            k: {"id": v.get("id"), "name": v.get("name"), "status": v.get("status")}
            for k, v in created.items()
        }
        return created

    def start_and_target(self, processes: Dict[str, dict], cast: Dict[str, dict]) -> None:
        access_ids = [p["access_id"] for p in cast.values()]
        for process_def in self.catalog["review_processes"]:
            process = processes.get(process_def["key"])
            if not process:
                continue
            process_id = str(process.get("id"))
            if process_id.startswith("dry-"):
                self.action("dry_start_skip", process_def["name"])
                continue
            status_now = process.get("status")
            if process_def.get("start") and status_now in ("draft", "scheduled", None):
                if not self.apply:
                    self.action("dry_start_process", process_id)
                else:
                    st, body = self.api.post(
                        "performance/review_processes/start", {"id": process_id}
                    )
                    if st in (200, 201):
                        self.action(
                            "started_process",
                            {"id": process_id, "name": process_def["name"]},
                        )
                        process = body if isinstance(body, dict) else process
                        processes[process_def["key"]] = process
                    else:
                        self.error(
                            "start_process_failed",
                            {"id": process_id, "status": st, "body": body},
                        )

            if self.apply and process.get("status") in ("active", "starting"):
                employee_ids = [p["employee_id"] for p in cast.values()]
                st, body = self.api.post(
                    "performance/review_process_targets/bulk_create",
                    {
                        "performance_review_process_id": process_id,
                        "targets_employee_ids": employee_ids,
                        "targets_access_ids": access_ids,
                    },
                )
                self.action(
                    "bulk_create_targets",
                    {"process_id": process_id, "status": st, "body": _short(body)},
                )

            if self.apply and process_def.get("agreements_enabled"):
                st, body = self.api.post(
                    "performance/agreements/bulk_initiate",
                    {"process_id": process_id},
                )
                self.action(
                    "bulk_initiate_agreements",
                    {"process_id": process_id, "status": st, "body": _short(body)},
                )

    def ensure_trainings(self, cast: Dict[str, dict]) -> None:
        existing = self.api.list_all("trainings/trainings")
        by_name = {normalize_name(t.get("name")): t for t in existing}
        author = cast.get("Nadia Lejuez") or cast.get("Margarita De Weever") or next(iter(cast.values()))
        created_ids = []
        for training in self.catalog["trainings"]:
            if normalize_name(training["name"]) in by_name:
                self.action("training_exists", training["name"])
                created_ids.append(by_name[normalize_name(training["name"])].get("id"))
                continue
            payload = {
                "name": training["name"],
                "description": training["description"],
                "external": False,
                "year": self.catalog["year"],
                "attachments": [],
                "author_id": author["access_id"],
                "company_id": str(self.catalog["company_id"]),
            }
            if not self.apply:
                self.action("dry_create_training", payload)
                continue
            status, body = self.api.post("trainings/trainings", payload)
            if status in (200, 201) and isinstance(body, dict):
                self.action("created_training", {"id": body.get("id"), "name": training["name"]})
                created_ids.append(body.get("id"))
            else:
                self.error(
                    "create_training_failed",
                    {"status": status, "body": body, "payload": payload},
                )
        self.log["ids"]["trainings"] = created_ids

    def ensure_job_postings(self, team_ids: Dict[str, str]) -> None:
        existing = self.api.list_all("ats/job_postings")
        by_title = {normalize_name(j.get("title")): j for j in existing}
        created_ids = []
        for job in self.catalog.get("job_postings", []):
            if normalize_name(job["title"]) in by_title:
                jid = by_title[normalize_name(job["title"])].get("id")
                created_ids.append(jid)
                self.action("job_posting_exists", {"title": job["title"], "id": jid})
                continue

            payload = {
                "title": job["title"],
                "description": job.get("description"),
                "status": job.get("status", "draft"),
                "category": job.get("category"),
                "contract_type": job.get("contract_type"),
                "workplace_type": job.get("workplace_type"),
                "schedule_type": job.get("schedule_type"),
                "cv_requirement": job.get("cv_requirement", "mandatory"),
                "cover_letter_requirement": job.get("cover_letter_requirement", "optional"),
                "phone_requirement": job.get("phone_requirement", "optional"),
                "photo_requirement": job.get("photo_requirement", "do_not_ask"),
                "personal_url_requirement": job.get("personal_url_requirement", "do_not_ask"),
            }
            team_id = team_ids.get(job.get("team_key"))
            if team_id and not str(team_id).startswith("dry-"):
                payload["team_id"] = team_id
            if self.location_id and not str(self.location_id).startswith("dry-"):
                payload["location_id"] = self.location_id
            if self.legal_entity_id and not str(self.legal_entity_id).startswith("dry-"):
                payload["legal_entity_id"] = self.legal_entity_id

            if not self.apply:
                self.action("dry_create_job_posting", payload)
                continue

            st, body = self.api.post("ats/job_postings", payload)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                self.action("created_job_posting", {"id": body.get("id"), "title": job["title"]})
                created_ids.append(body.get("id"))
            else:
                # Retry as draft without optional links
                retry = {
                    k: v
                    for k, v in payload.items()
                    if k
                    in (
                        "title",
                        "description",
                        "status",
                        "cv_requirement",
                        "cover_letter_requirement",
                        "phone_requirement",
                        "photo_requirement",
                        "personal_url_requirement",
                    )
                }
                retry["status"] = "draft"
                st2, body2 = self.api.post("ats/job_postings", retry)
                if st2 in (200, 201) and isinstance(body2, dict) and body2.get("id"):
                    self.action(
                        "created_job_posting_draft",
                        {"id": body2.get("id"), "title": job["title"]},
                    )
                    created_ids.append(body2.get("id"))
                else:
                    self.error(
                        "create_job_posting_failed",
                        {
                            "status": st,
                            "body": _short(body),
                            "retry_status": st2,
                            "retry_body": _short(body2),
                            "payload": payload,
                        },
                    )
        self.log["ids"]["job_postings"] = created_ids

    def ensure_onboarding_tasks(self, cast: Dict[str, dict]) -> None:
        onboarding = self.catalog.get("onboarding") or {}
        tasks_def = onboarding.get("tasks") or []
        if not tasks_def:
            return

        existing = self.api.list_all("tasks/tasks")
        by_name = {normalize_name(t.get("name")): t for t in existing}
        created_ids = []

        for task in tasks_def:
            if normalize_name(task["name"]) in by_name:
                tid = by_name[normalize_name(task["name"])].get("id")
                created_ids.append(tid)
                self.action("onboarding_task_exists", {"name": task["name"], "id": tid})
                continue

            assignee_ids = []
            for person_name in task.get("assignees") or []:
                person = cast.get(person_name)
                if person and person.get("access_id") and not str(person["access_id"]).startswith("dry-"):
                    assignee_ids.append(person["access_id"])
                elif not self.apply and person:
                    assignee_ids.append(person["access_id"])

            payload = {
                "name": task["name"],
                "content": task.get("content"),
                "due_on": task.get("due_on"),
                "status": task.get("status", "todo"),
                "assignee_ids": assignee_ids,
            }
            if not self.apply:
                self.action("dry_create_onboarding_task", payload)
                continue

            st, body = self.api.post("tasks/tasks", payload)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                self.action("created_onboarding_task", {"id": body.get("id"), "name": task["name"]})
                created_ids.append(body.get("id"))
            else:
                # Retry without assignees if validation fails
                retry = {
                    "name": task["name"],
                    "content": task.get("content"),
                    "due_on": task.get("due_on"),
                    "status": task.get("status", "todo"),
                    "assignee_ids": [],
                }
                st2, body2 = self.api.post("tasks/tasks", retry)
                if st2 in (200, 201) and isinstance(body2, dict) and body2.get("id"):
                    self.action(
                        "created_onboarding_task_no_assignee",
                        {"id": body2.get("id"), "name": task["name"]},
                    )
                    created_ids.append(body2.get("id"))
                else:
                    self.error(
                        "create_onboarding_task_failed",
                        {
                            "status": st,
                            "body": _short(body),
                            "retry_status": st2,
                            "retry_body": _short(body2),
                            "payload": payload,
                        },
                    )
        self.log["ids"]["onboarding_tasks"] = created_ids

    def ensure_candidates(self) -> None:
        candidates_def = self.catalog.get("candidates") or []
        if not candidates_def:
            return

        jobs = self.api.list_all("ats/job_postings")
        jobs_by_title = {normalize_name(j.get("title")): j for j in jobs}
        existing_candidates = self.api.list_all("ats/candidates")
        by_email = {
            normalize_name(c.get("email") or ""): c
            for c in existing_candidates
            if c.get("email")
        }
        created = []

        for cand in candidates_def:
            job = jobs_by_title.get(normalize_name(cand["job_title"]))
            if not job:
                self.error("candidate_job_missing", cand["job_title"])
                continue

            existing = by_email.get(normalize_name(cand["email"]))
            if existing:
                self.action(
                    "candidate_exists",
                    {"email": cand["email"], "id": existing.get("id")},
                )
                candidate_id = str(existing.get("id"))
            else:
                payload = {
                    "first_name": cand["first_name"],
                    "last_name": cand["last_name"],
                    "email": cand["email"],
                    "company_id": str(self.catalog["company_id"]),
                    "phone_number": cand.get("phone_number"),
                    "gender": cand.get("gender"),
                    "source": cand.get("source"),
                    "medium": cand.get("medium"),
                }
                if not self.apply:
                    self.action("dry_create_candidate", payload)
                    created.append({"email": cand["email"], "job": cand["job_title"], "mode": "dry"})
                    continue
                st, body = self.api.post("ats/candidates", payload)
                if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                    candidate_id = str(body["id"])
                    self.action(
                        "created_candidate",
                        {"id": candidate_id, "name": f"{cand['first_name']} {cand['last_name']}"},
                    )
                else:
                    # Fallback: apply endpoint creates candidate+application
                    apply_payload = {
                        "company_id": str(self.catalog["company_id"]),
                        "first_name": cand["first_name"],
                        "last_name": cand["last_name"],
                        "email": cand["email"],
                        "ats_job_posting_id": str(job["id"]),
                        "phone": cand.get("phone_number"),
                        "source": cand.get("source"),
                        "medium": cand.get("medium"),
                        "cover_letter": cand.get("cover_letter"),
                        "gender": cand.get("gender"),
                        "consent_to_talent_pool": True,
                    }
                    st2, body2 = self.api.post("ats/applications/apply", apply_payload)
                    if st2 in (200, 201):
                        self.action(
                            "applied_candidate_via_apply",
                            {"email": cand["email"], "job": cand["job_title"], "status": st2},
                        )
                        created.append({"email": cand["email"], "job": cand["job_title"], "via": "apply"})
                        continue
                    self.error(
                        "create_candidate_failed",
                        {
                            "status": st,
                            "body": _short(body),
                            "apply_status": st2,
                            "apply_body": _short(body2),
                        },
                    )
                    continue

            # Create application linked to job
            app_payload = {
                "ats_job_posting_id": str(job["id"]),
                "ats_candidate_id": candidate_id,
                "phone": cand.get("phone_number"),
                "source": cand.get("source"),
                "medium": cand.get("medium"),
                "cover_letter": cand.get("cover_letter"),
                "consent_to_talent_pool": True,
            }
            if not self.apply:
                self.action("dry_create_application", app_payload)
                continue
            st, body = self.api.post("ats/applications", app_payload)
            if st in (200, 201):
                self.action(
                    "created_application",
                    {
                        "candidate_id": candidate_id,
                        "job": cand["job_title"],
                        "id": body.get("id") if isinstance(body, dict) else None,
                    },
                )
                created.append(
                    {
                        "candidate_id": candidate_id,
                        "job": cand["job_title"],
                        "application_id": body.get("id") if isinstance(body, dict) else None,
                    }
                )
            else:
                # Maybe already applied — try apply endpoint once
                apply_payload = {
                    "company_id": str(self.catalog["company_id"]),
                    "first_name": cand["first_name"],
                    "last_name": cand["last_name"],
                    "email": cand["email"],
                    "ats_job_posting_id": str(job["id"]),
                    "phone": cand.get("phone_number"),
                    "cover_letter": cand.get("cover_letter"),
                    "consent_to_talent_pool": True,
                }
                st2, body2 = self.api.post("ats/applications/apply", apply_payload)
                if st2 in (200, 201):
                    self.action(
                        "application_via_apply",
                        {"email": cand["email"], "job": cand["job_title"]},
                    )
                    created.append({"email": cand["email"], "job": cand["job_title"], "via": "apply"})
                else:
                    self.error(
                        "create_application_failed",
                        {
                            "status": st,
                            "body": _short(body),
                            "apply_status": st2,
                            "apply_body": _short(body2),
                            "payload": app_payload,
                        },
                    )

        self.log["ids"]["candidates"] = created

    def ensure_posts(self) -> None:
        group_def = self.catalog.get("posts_group") or {}
        posts_def = self.catalog.get("posts") or []
        if not group_def or not posts_def:
            return

        groups = self.api.list_all("posts/groups")
        wanted_titles = [group_def["title"]] + list(group_def.get("fallback_titles") or [])
        group = None
        for title in wanted_titles:
            group = next(
                (g for g in groups if normalize_name(g.get("title")) == normalize_name(title)),
                None,
            )
            if group:
                break
        if not group and groups:
            # Prefer any announcements-like group
            group = next(
                (g for g in groups if "announce" in normalize_name(g.get("title"))),
                groups[0],
            )

        if group:
            group_id = str(group["id"])
            self.action(
                "post_group_exists",
                {"id": group_id, "title": group.get("title")},
            )
        else:
            payload = {
                "title": group_def["title"],
                "description": group_def.get("description"),
                "company_id": str(self.catalog["company_id"]),
            }
            if not self.apply:
                self.action("dry_create_post_group", payload)
                group_id = "dry-post-group"
            else:
                st, body = self.api.post("posts/groups", payload)
                if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                    group_id = str(body["id"])
                    self.action("created_post_group", {"id": group_id, "title": group_def["title"]})
                else:
                    self.error("create_post_group_failed", {"status": st, "body": _short(body)})
                    return

        self.log["ids"]["post_group_id"] = group_id
        # Unscoped/group list endpoints often return empty; recover known IDs from prior seed
        by_title = {}
        prior_ids = []
        latest_path = RUN_LOG_DIR / "seed_latest.json"
        if latest_path.exists():
            try:
                import json

                prior_ids = list(
                    (json.loads(latest_path.read_text(encoding="utf-8")).get("ids") or {}).get(
                        "posts"
                    )
                    or []
                )
            except Exception:
                prior_ids = []
        if prior_ids and self.apply:
            st, body = self.api.get("posts/posts", params={"ids[]": [str(x) for x in prior_ids]})
            if st == 200:
                for p in (body or {}).get("data") or []:
                    by_title[normalize_name(p.get("title"))] = p

        created_ids = []
        for post in posts_def:
            if normalize_name(post["title"]) in by_title:
                pid = by_title[normalize_name(post["title"])].get("id")
                created_ids.append(pid)
                self.action("post_exists", {"title": post["title"], "id": pid})
                continue
            payload = {
                "title": post["title"],
                "description": post["description"],
                "post_group_id": group_id,
                "allow_comments_and_reactions": bool(post.get("allow_comments_and_reactions", True)),
            }
            if not self.apply or str(group_id).startswith("dry-"):
                self.action("dry_create_post", payload)
                continue
            st, body = self.api.post("posts/posts", payload)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                self.action("created_post", {"id": body.get("id"), "title": post["title"]})
                created_ids.append(body.get("id"))
            else:
                self.error(
                    "create_post_failed",
                    {"status": st, "body": _short(body), "payload": payload},
                )
        self.log["ids"]["posts"] = created_ids

    def write_goals_pack(self, cast: Dict[str, dict]) -> Path:
        lines = [
            "# SZV SMART Goals Pack",
            "",
            "Use these goals when completing P1 agreements / objective text answers in Factorial.",
            "",
            f"Company: {self.catalog.get('company_id')} · Sint Maarten demo cast",
            "",
        ]
        for person in cast.values():
            templates = self.catalog["goal_templates"][person["group"]]
            count = min(person["goal_count"], len(templates))
            lines.append(f"## {person['full_name']} ({person['group']}) — {person.get('role_title', '')}")
            lines.append("")
            for idx, goal in enumerate(templates[:count], 1):
                lines.append(
                    f"{idx}. **[{goal['category']}] {goal['title']}**  "
                    f"Measure: {goal['measure']} | Due: {goal['due']}"
                )
            lines.append("")
        path = RUN_LOG_DIR / "goals_pack.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.action("wrote_goals_pack", str(path))
        return path

    def run(self) -> int:
        print(f"=== SZV Seed ({'APPLY' if self.apply else 'DRY-RUN'}) ===")
        print(f"BASE_URL={self.api.config.BASE_URL} VERSION={self.api.version}")
        print(f"AUTH_TYPE={self.api.config.AUTH_TYPE} COMPANY={self.catalog.get('company_id')}")

        expected = len(self.catalog["cast"])
        self.ensure_location()
        self.ensure_legal_entity()
        cast = self.ensure_cast()
        if len(cast) < expected:
            self.error("incomplete_cast", f"resolved {len(cast)}/{expected}")
            self._persist()
            return 2

        team_ids = self.ensure_teams(cast)
        self.update_managers(cast)
        processes = self.ensure_review_processes(cast)
        self.start_and_target(processes, cast)
        self.ensure_trainings(cast)
        self.ensure_job_postings(team_ids)
        self.ensure_onboarding_tasks(cast)
        self.ensure_candidates()
        self.ensure_posts()
        self.write_goals_pack(cast)

        self.log["finished_at"] = datetime.now(timezone.utc).isoformat()
        self._persist()
        print(f"Actions: {len(self.log['actions'])} | Errors: {len(self.log['errors'])}")
        return 1 if self.log["errors"] else 0

    def _persist(self) -> None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        mode = "apply" if self.apply else "dryrun"
        path = RUN_LOG_DIR / f"seed_{mode}_{stamp}.json"
        save_json(path, self.log)
        save_json(RUN_LOG_DIR / "seed_latest.json", self.log)
        print(f"Wrote {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed SZV demo data (org + performance + ATS)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Show planned actions only")
    group.add_argument("--apply", action="store_true", help="Write data to Factorial")
    args = parser.parse_args()
    return SzvSeeder(apply=args.apply).run()


if __name__ == "__main__":
    raise SystemExit(main())
