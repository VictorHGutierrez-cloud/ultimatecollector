#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed demo CDH Malawi na Factorial (company 188450).

Inclui: location, legal entity, cast (rename), teams, managers,
performance Full BSC Q1–Q4, trainings, announcements, goals pack.

Uso:
  python scripts/clients/cdh-malawi/cdh_seed_performance.py --dry-run
  python scripts/clients/cdh-malawi/cdh_seed_performance.py --apply
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

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("cdh-malawi")

CDH_CLIENT_DIR = ROOT / "clients" / "cdh-malawi"
sys.path.insert(0, str(CDH_CLIENT_DIR))
from api_helpers import (  # noqa: E402
    RUN_LOG_DIR,
    CdhApi,
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


def build_cdh_questionnaire(catalog: dict, phase_key: str) -> List[dict]:
    """Questionário Full BSC: 4 perspectivas + valores + coaching.

    Competências/valores nativos vêm de competencies_assessments_enabled=true.
    """
    scale_codes = [f"{r['code']} — {r['label']}: {r['definition']}" for r in catalog["rating_scale"]]
    weighting = catalog.get("weighting", {}).get("manager", {})
    obj_w = weighting.get("objectives", 90)
    val_w = weighting.get("competencies", 10)

    perspective_weights = {
        p["name"]: p["weight_pct"] for p in catalog.get("bsc_perspectives", [])
    }

    objective_questions = []
    for category in catalog["goal_categories"]:
        pw = perspective_weights.get(category, "")
        weight_note = f" Perspective weight ~{pw}%." if pw != "" else ""
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": (
                    f"[{category}] Rate BSC objective achievement for this perspective."
                    f"{weight_note} Overall objectives weight: {obj_w}% of final rating. "
                    f"Scale: {', '.join(r['code'] for r in catalog['rating_scale'])}."
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
                "Confirm SMART goals cascaded from the CDH bank BSC scorecard "
                "(measure, owner, due date, parent objective). "
                "KPI status options: On Target / Caution / Needs Help / No Data."
            ),
            "answer_type": "text",
        }
    )
    if phase_key in ("q2", "q3"):
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": (
                    f"{phase_key.upper()} progress vs BSC measures: status per KPI, "
                    "challenges, and approved goal adjustments."
                ),
                "answer_type": "text",
            }
        )
    if phase_key == "q4":
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": (
                    "Year-end evidence summary vs agreed BSC measures "
                    "(indexed performance narrative) and next-year development focus."
                ),
                "answer_type": "text",
            }
        )

    values_list = ", ".join(v["name"] for v in catalog.get("core_values", []))
    values_questions = [
        {
            "uuid": new_uuid(),
            "mandatory": True,
            "with_comment": True,
            "title": (
                f"Core values behaviours ({values_list}). "
                f"Combined weight: {val_w}% of final rating (2% each in Excel model)."
            ),
            "answer_type": "rating",
        },
        {
            "uuid": new_uuid(),
            "mandatory": False,
            "with_comment": True,
            "title": "Evidence / examples of living CDH core values this period.",
            "answer_type": "text",
        },
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
            "mandatory": True,
            "with_comment": True,
            "title": "Development actions linked to BSC gaps (training, welfare, job evaluation, etc.).",
            "answer_type": "text",
        },
    ]
    if phase_key == "q4":
        coaching_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": "Appraiser and employee year-end comments (sign-off narrative).",
                "answer_type": "text",
            }
        )

    return [
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": f"CDH BSC Objectives ({obj_w}%)",
            "questions": objective_questions,
        },
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": f"CDH Core Values ({val_w}%)",
            "questions": values_questions,
        },
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": "CDH Coaching & Comments",
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
                    "title": "CDH rating reference (informational)",
                    "answer_type": "multiple_choice",
                    "max_choices": 1,
                    "choice_options": scale_codes,
                }
            ],
        },
    ]


class CdhSeeder:
    def __init__(self, apply: bool) -> None:
        self.apply = apply
        self.api = CdhApi()
        self.catalog = load_catalog()
        self.log: Dict[str, Any] = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "mode": "apply" if apply else "dry-run",
            "company_id": self.catalog.get("company_id"),
            "scope": self.catalog.get("scope"),
            "year": self.catalog.get("year"),
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

    def _pick_author(self, cast: Dict[str, dict]) -> dict:
        return (
            cast.get("Chisomo Banda")
            or cast.get("Thandiwe Phiri")
            or next(iter(cast.values()))
        )

    def ensure_location(self) -> Optional[str]:
        loc_def = self.catalog["location"]
        locations = self.api.list_all("locations/locations")
        by_name = {normalize_name(l.get("name")): l for l in locations}
        existing = by_name.get(normalize_name(loc_def["name"]))
        if not existing:
            for loc in locations:
                name = str(loc.get("name") or "")
                if "CDH" not in name and "Lilongwe" not in name:
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
        }

        if existing and self.apply:
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

        attempts = [
            dict(payload),
            {
                **payload,
                "country": loc_def.get("country_fallback", "us"),
                "timezone": loc_def.get("timezone_fallback", "Africa/Johannesburg"),
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
            if entities:
                self.legal_entity_id = str(entities[0]["id"])
            else:
                self.legal_entity_id = "dry-legal-entity"
            self.log["ids"]["legal_entity_id"] = self.legal_entity_id
            return self.legal_entity_id

        attempts = [
            dict(payload),
            {
                **payload,
                "country": le_def.get("country_fallback", "us"),
                "currency": le_def.get("currency_fallback", "USD"),
            },
        ]
        for attempt in attempts:
            st, body = self.api.post("companies/legal_entities", attempt)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                self.legal_entity_id = str(body["id"])
                self.action(
                    "created_legal_entity",
                    {"id": self.legal_entity_id, "country": attempt["country"]},
                )
                self.log["ids"]["legal_entity_id"] = self.legal_entity_id
                return self.legal_entity_id
            self.action(
                "create_legal_entity_attempt_failed",
                {"status": st, "body": _short(body)},
            )

        if entities:
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
            normalize_name(e.get("email") or e.get("login_email") or ""): e
            for e in employees
            if e.get("email") or e.get("login_email")
        }
        resolved: Dict[str, dict] = {}

        for person in self.catalog["cast"]:
            emp = by_name.get(normalize_name(person["full_name"]))
            if not emp and person.get("email"):
                emp = by_email.get(normalize_name(person["email"]))

            if not emp and person.get("rename_from"):
                source = by_name.get(normalize_name(person["rename_from"]))
                if source:
                    payload = {
                        "id": str(source["id"]),
                        "first_name": person["first_name"],
                        "last_name": person["last_name"],
                    }
                    if not self.apply:
                        self.action(
                            "dry_rename_employee",
                            {"from": person["rename_from"], **payload},
                        )
                        emp = {**source, **payload, "full_name": person["full_name"]}
                    else:
                        st, body = self.api.put(f"employees/employees/{source['id']}", payload)
                        if st in (200, 201):
                            self.action(
                                "renamed_employee",
                                {
                                    "from": person["rename_from"],
                                    "to": person["full_name"],
                                    "id": source["id"],
                                },
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
                    "contract_starts_on": "2026-01-15",
                    "contract_effective_on": "2026-01-15",
                    "country": "us",
                    "nationality": "MW",
                    "city": "Lilongwe",
                    "state": "Central Region",
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

            if self.apply:
                updates = {"id": str(emp["id"])}
                if self.location_id and str(emp.get("location_id")) != str(self.location_id):
                    updates["location_id"] = self.location_id
                if self.legal_entity_id and str(emp.get("legal_entity_id")) != str(
                    self.legal_entity_id
                ):
                    updates["legal_entity_id"] = self.legal_entity_id
                if emp.get("first_name") != person["first_name"] or emp.get("last_name") != person[
                    "last_name"
                ]:
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
            k: {
                "employee_id": v["employee_id"],
                "access_id": v["access_id"],
                "group": v["group"],
                "star_scorecard": bool(v.get("star_scorecard")),
            }
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
                "description": f"CDH demo team for Full BSC narrative ({team['key']})",
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
            if process.get("name") == name and not process.get("archived"):
                return process
        return None

    def _apply_questionnaire(
        self,
        process_id: str,
        process_def: dict,
        rating_scale: List[dict],
    ) -> None:
        questionnaire = build_cdh_questionnaire(self.catalog, process_def["key"])
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
                    {"process_id": process_id, "strategy": strategy, "status": st, "body": _short(body)},
                )

            # Rating scale endpoint varies by API version; scale text is also
            # embedded in questionnaire choice_options / question titles.
            _ = rating_scale

    def ensure_review_processes(self, cast: Dict[str, dict]) -> Dict[str, dict]:
        author = self._pick_author(cast)
        access_ids = [p["access_id"] for p in cast.values()]
        employee_ids = [p["employee_id"] for p in cast.values()]
        created: Dict[str, dict] = {}

        rating_scale = [
            {
                "value": idx + 1,
                "text": f"{item['code']} — {item['label']}: {item['definition']}",
            }
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

            if self.apply and not process_id.startswith("dry-"):
                self._apply_questionnaire(process_id, process_def, rating_scale)
                created[process_def["key"]] = (
                    self.find_process_by_name(process_def["name"]) or process
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
        author = self._pick_author(cast)
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
            existing_post = by_title.get(normalize_name(post["title"]))
            if existing_post:
                pid = str(existing_post.get("id"))
                created_ids.append(pid)
                self.action("post_exists", {"title": post["title"], "id": pid})
                if self.apply and not existing_post.get("published_at"):
                    self._publish_post(pid, post, group_id)
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
                pid = str(body.get("id"))
                self.action("created_post", {"id": pid, "title": post["title"]})
                created_ids.append(pid)
                self._publish_post(pid, post, group_id)
            else:
                self.error(
                    "create_post_failed",
                    {"status": st, "body": _short(body), "payload": payload},
                )
        self.log["ids"]["posts"] = created_ids

    def _publish_post(self, post_id: str, post: dict, group_id: str) -> None:
        published_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        payload = {
            "id": post_id,
            "title": post["title"],
            "description": post["description"],
            "post_group_id": str(group_id),
            "allow_comments_and_reactions": bool(post.get("allow_comments_and_reactions", True)),
            "published_at": published_at,
        }
        st, body = self.api.put(f"posts/posts/{post_id}", payload)
        if st in (200, 201):
            self.action("published_post", {"id": post_id, "title": post["title"]})
        else:
            self.error(
                "publish_post_failed",
                {"id": post_id, "status": st, "body": _short(body)},
            )

    def write_goals_pack(self, cast: Dict[str, dict]) -> Path:
        lines = [
            "# CDH Malawi Full BSC — SMART Goals Pack 2026",
            "",
            "Use these goals when completing Q1 agreements / BSC objective text answers in Factorial.",
            "",
            f"Company: {self.catalog.get('company_id')} · {self.catalog.get('display_name')}",
            f"Weighting: 90% objectives / 10% core values · Perspectives: Financial 30% / Customer 15% / Internal 25% / L&G 30%",
            "",
        ]

        star = self.catalog.get("star_scorecard_nqabile") or {}
        if star:
            lines.extend(
                [
                    "## ★ Star scorecard — Nqabile Medi (from client Excel)",
                    "",
                    f"- Employee: **{star.get('employee')}**",
                    f"- Appraiser: **{star.get('appraiser')}**",
                    f"- Business unit: {star.get('business_unit')}",
                    f"- Financial year: {star.get('financial_year')}",
                    "",
                ]
            )
            for block in star.get("objectives", []):
                lines.append(f"### {block.get('perspective')} — {block.get('objective')}")
                lines.append("")
                for m in block.get("measures", []):
                    lines.append(
                        f"- **{m['title']}** · Weight {m['weight_pct']}% · Cadence: {m.get('cadence')}"
                    )
                lines.append("")
            lines.extend(
                [
                    "### Core values (10%)",
                    "",
                ]
            )
            for v in self.catalog.get("core_values", []):
                lines.append(f"- {v['name']} ({v['weight_pct']}%)")
            lines.append("")

        for person in cast.values():
            templates = self.catalog["goal_templates"][person["group"]]
            count = min(person["goal_count"], len(templates))
            star_mark = " ★" if person.get("star_scorecard") else ""
            lines.append(
                f"## {person['full_name']}{star_mark} ({person['group']}) — {person.get('role_title', '')}"
            )
            lines.append("")
            if person.get("star_scorecard"):
                lines.append(
                    "_Prefer the star scorecard measures above for demo; templates below are a shorter set._"
                )
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
        print(f"=== CDH Malawi Seed ({'APPLY' if self.apply else 'DRY-RUN'}) ===")
        print(f"BASE_URL={self.api.config.BASE_URL} VERSION={self.api.version}")
        print(
            f"AUTH_TYPE={self.api.config.AUTH_TYPE} COMPANY={self.catalog.get('company_id')} "
            f"SCOPE={self.catalog.get('scope')} YEAR={self.catalog.get('year')}"
        )

        expected = len(self.catalog["cast"])
        self.ensure_location()
        self.ensure_legal_entity()
        cast = self.ensure_cast()
        if len(cast) < expected:
            self.error("incomplete_cast", f"resolved {len(cast)}/{expected}")
            self._persist()
            return 2

        self.ensure_teams(cast)
        self.update_managers(cast)
        processes = self.ensure_review_processes(cast)
        self.start_and_target(processes, cast)
        self.ensure_trainings(cast)
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
    parser = argparse.ArgumentParser(description="Seed CDH Malawi demo (Full BSC performance)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Show planned actions only")
    group.add_argument("--apply", action="store_true", help="Write data to Factorial")
    args = parser.parse_args()
    return CdhSeeder(apply=args.apply).run()


if __name__ == "__main__":
    raise SystemExit(main())
