#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed STATIN Performance Management demo (company 191864).

Creates teams, three review processes (year-end / coaching / IWP),
questionnaires, trainings, announcement, and goals pack.
Does NOT rename employees or change Time Off.

Usage:
  python scripts/clients/statistic-institute/seed_pms_statin.py --dry-run
  python scripts/clients/statistic-institute/seed_pms_statin.py --apply
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

activate_client("statistic-institute")

STATIN_CLIENT_DIR = ROOT / "clients" / "statistic-institute"
sys.path.insert(0, str(STATIN_CLIENT_DIR))
from api_helpers import (  # noqa: E402
    RUN_LOG_DIR,
    StatinApi,
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


def build_statin_questionnaire(catalog: dict, phase_key: str) -> List[dict]:
    """STATIN EPM-style questionnaire: targets 60% + coaching/IDP/appeal.

    GoJ / STATIN competencies are assessed via Factorial's native
    competencies_assessments block (import Excels) — do NOT duplicate as questions.
    """
    scale_codes = [f"{r['code']} — {r['label']}: {r['definition']}" for r in catalog["rating_scale"]]
    band_codes = [f"{b['code']} — {b['label']} ({b['range']})" for b in catalog["performance_bands"]]
    core_names = ", ".join(catalog.get("core_competencies") or [])
    tech_names = ", ".join(catalog.get("technical_competencies") or [])

    objective_questions = []
    for category in catalog["goal_categories"]:
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": (
                    f"[{category}] Rate achievement of agreed performance targets. "
                    f"Weight: 60% of final rating. "
                    f"STATIN scale: {'; '.join(r['code'] + '=' + r['label'] for r in catalog['rating_scale'])}."
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
                "List or confirm Individual Work Plan performance targets and key outputs "
                "(include performance measure, weight, means of verification, and due date). "
                "Align to Division/Unit Plans."
            ),
            "answer_type": "text",
        }
    )
    if phase_key == "coaching":
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": (
                    "Coaching progress vs agreed targets: obstacles, resource gaps, "
                    "and any approved changes to performance targets."
                ),
                "answer_type": "text",
            }
        )
    if phase_key == "year_end":
        objective_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": (
                    "Year-end evidence summary vs agreed targets and key outputs "
                    "(attach or cite means of verification)."
                ),
                "answer_type": "text",
            }
        )

    coaching_questions = [
        {
            "uuid": new_uuid(),
            "mandatory": False,
            "with_comment": True,
            "title": (
                "Competencies reminder (native Factorial Competencies assessment block): "
                f"40% of final rating uses GoJ Core [{core_names}] and STATIN Technical "
                f"[{tech_names}]. Rate them in the Competencies section — not here."
            ),
            "answer_type": "text",
        },
    ]
    coaching_questions += [
        {
            "uuid": new_uuid(),
            "mandatory": True,
            "with_comment": True,
            "title": "Coaching / development action (what), owner, and by-when date.",
            "answer_type": "text",
        },
        {
            "uuid": new_uuid(),
            "mandatory": True,
            "with_comment": True,
            "title": (
                "Employee Development Needs / IDP: competencies for improvement and interventions "
                "(training, mentoring, coaching)."
            ),
            "answer_type": "text",
        },
    ]
    if phase_key == "year_end":
        coaching_questions.extend(
            [
                {
                    "uuid": new_uuid(),
                    "mandatory": True,
                    "with_comment": True,
                    "title": (
                        "Overall STATIN performance band after 60/40 scoring: "
                        "Superior 100% / Very Good 91-99% / Good 80-90% / "
                        "Satisfactory 75-79% / Unsatisfactory <75%."
                    ),
                    "answer_type": "multiple_choice",
                    "max_choices": 1,
                    "choice_options": band_codes,
                },
                {
                    "uuid": new_uuid(),
                    "mandatory": True,
                    "with_comment": True,
                    "title": (
                        "If score is below 75% or is 100%: mandatory comment. "
                        "For <75%, indicate PIP / training (competence gap) or "
                        "policy action (unwillingness)."
                    ),
                    "answer_type": "text",
                },
                {
                    "uuid": new_uuid(),
                    "mandatory": True,
                    "with_comment": False,
                    "title": "Employee decision on this review",
                    "answer_type": "multiple_choice",
                    "max_choices": 1,
                    "choice_options": [
                        "I Accept this review",
                        "I wish to appeal this review",
                    ],
                },
                {
                    "uuid": new_uuid(),
                    "mandatory": False,
                    "with_comment": True,
                    "title": (
                        "Recommended action (Section 10): Promotion / Increment / "
                        "Performance Improvement Plan / Other."
                    ),
                    "answer_type": "text",
                },
            ]
        )
    if phase_key == "iwp":
        coaching_questions.append(
            {
                "uuid": new_uuid(),
                "mandatory": True,
                "with_comment": True,
                "title": (
                    "Confirm how performance will be evaluated in FY 2026/27, "
                    "including scheduling of at least three coaching conversations."
                ),
                "answer_type": "text",
            }
        )

    sections = [
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": "STATIN Performance Targets (60%)",
            "questions": objective_questions,
        },
        {
            "uuid": new_uuid(),
            "type": "section",
            "section_title": "STATIN Coaching, Development & Outcomes",
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
                    "title": "STATIN target rating reference (informational)",
                    "answer_type": "multiple_choice",
                    "max_choices": 1,
                    "choice_options": scale_codes,
                },
            ],
        },
    ]
    return sections


class StatinPmsSeeder:
    def __init__(self, apply: bool) -> None:
        self.apply = apply
        self.api = StatinApi()
        self.catalog = load_catalog()
        self.log: Dict[str, Any] = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "mode": "apply" if apply else "dry-run",
            "company_id": self.catalog.get("company_id"),
            "actions": [],
            "errors": [],
            "ids": {},
        }

    def action(self, name: str, detail: Any = None) -> None:
        self.log["actions"].append({"action": name, "detail": detail})
        print(f"- {name}: {detail}")

    def error(self, name: str, detail: Any = None) -> None:
        self.log["errors"].append({"action": name, "detail": detail})
        print(f"! ERROR {name}: {detail}")

    def resolve_cast(self) -> Dict[str, dict]:
        """Resolve existing employees by name — no rename, no create."""
        employees = self.api.list_all("employees/employees")
        by_name = {normalize_name(emp_name(e)): e for e in employees}
        resolved: Dict[str, dict] = {}

        for person in self.catalog["cast"]:
            emp = by_name.get(normalize_name(person["full_name"]))
            if not emp:
                self.error("cast_missing", person["full_name"])
                continue
            if emp.get("active") is False or emp.get("terminated_on"):
                self.error(
                    "cast_inactive",
                    {"full_name": person["full_name"], "terminated_on": emp.get("terminated_on")},
                )
                continue
            if not emp.get("access_id"):
                self.error("cast_no_access_id", person["full_name"])
                continue
            resolved[person["full_name"]] = {
                **person,
                "employee_id": str(emp["id"]),
                "access_id": str(emp["access_id"]),
                "current_manager_id": str(emp["manager_id"]) if emp.get("manager_id") else None,
            }
            self.action(
                "cast_resolved",
                {
                    "name": person["full_name"],
                    "employee_id": emp["id"],
                    "access_id": emp["access_id"],
                    "band": person.get("demo_band"),
                },
            )

        self.log["ids"]["cast"] = {
            k: {
                "employee_id": v["employee_id"],
                "access_id": v["access_id"],
                "group": v["group"],
                "demo_band": v.get("demo_band"),
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
                "description": (
                    f"STATIN Division/Unit for PMS cascade narrative ({team['key']}). "
                    "Aligns Division/Unit Plans to Individual Work Plans."
                ),
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
                # Some tenants wrap data
                data = body.get("data") if isinstance(body, dict) else None
                if isinstance(data, dict) and data.get("id"):
                    team_ids[team["key"]] = str(data["id"])
                    self.action("created_team", {"id": data["id"], "name": team["name"]})
                else:
                    self.error(
                        "create_team_failed",
                        {"status": status, "body": _short(body), "payload": payload},
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
                    {"status": status, "body": _short(body), "payload": payload},
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
                    {"status": status, "body": _short(body), "payload": payload},
                )

    def find_process_by_name(self, name: str) -> Optional[dict]:
        processes = self.api.list_all("performance/review_processes")
        for process in processes:
            if process.get("name") == name and not process.get("archived"):
                return process
        return None

    def _unwrap(self, body: Any) -> Any:
        if isinstance(body, dict) and body.get("data") and isinstance(body["data"], dict):
            return body["data"]
        return body

    def _apply_questionnaire(
        self,
        process_id: str,
        process_def: dict,
        rating_scale: List[dict],
    ) -> None:
        questionnaire = build_statin_questionnaire(self.catalog, process_def["key"])
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
                        "body": _short(body),
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

    def ensure_review_processes(self, cast: Dict[str, dict]) -> Dict[str, dict]:
        author = (
            cast.get("Charles Carter")
            or cast.get("Laura Lewis")
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
                body = self._unwrap(body)
                if status in (200, 201) and isinstance(body, dict) and body.get("id"):
                    created[process_def["key"]] = body
                    self.action("created_process", {"key": process_def["key"], "id": body["id"]})
                else:
                    payload["target_strategy"] = "manual_selection"
                    payload["arguments"] = access_ids
                    status, body = self.api.post("performance/review_processes", payload)
                    body = self._unwrap(body)
                    if status in (200, 201) and isinstance(body, dict) and body.get("id"):
                        created[process_def["key"]] = body
                        self.action(
                            "created_process_manual",
                            {"key": process_def["key"], "id": body["id"]},
                        )
                    else:
                        self.error(
                            "create_process_failed",
                            {"status": status, "body": _short(body), "payload": payload},
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
                    flag_payload = {"id": process_id, "enabled": bool(enabled)}
                    st, body = self.api.post(
                        f"performance/review_processes/{flag_name}",
                        flag_payload,
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
                # Only push questionnaire while still configurable; try anyway if draft/active
                if process.get("status") in (None, "draft", "scheduled", "active", "starting"):
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
                    body = self._unwrap(body)
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
                            {"id": process_id, "status": st, "body": _short(body)},
                        )

            refreshed = self.find_process_by_name(process_def["name"]) or process
            processes[process_def["key"]] = refreshed
            if self.apply and refreshed.get("status") in ("active", "starting"):
                access_ids = [p["access_id"] for p in cast.values()]
                employee_ids = [p["employee_id"] for p in cast.values()]
                st, body = self.api.post(
                    "performance/review_process_targets/bulk_create",
                    {
                        "performance_review_process_id": process_id,
                        "targets_access_ids": access_ids,
                        "targets_employee_ids": employee_ids,
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
        author = cast.get("Charles Carter") or cast.get("Laura Lewis") or next(iter(cast.values()))
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
            body = self._unwrap(body)
            if status in (200, 201) and isinstance(body, dict):
                self.action("created_training", {"id": body.get("id"), "name": training["name"]})
                created_ids.append(body.get("id"))
            else:
                self.error(
                    "create_training_failed",
                    {"status": status, "body": _short(body), "payload": payload},
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
            self.action("post_group_exists", {"id": group_id, "title": group.get("title")})
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
                body = self._unwrap(body)
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
            body = self._unwrap(body)
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
            "# STATIN Individual Work Plan — Goals Pack (English)",
            "",
            "Use these goals when completing FY 2026-27 IWP agreements / target text answers in Factorial.",
            "",
            f"Company: {self.catalog.get('company_id')} · {self.catalog.get('display_name')}",
            "Weighting guidance: **60% measurable targets / 40% GoJ core & technical competencies**.",
            "Bands: Superior 100% · Very Good 91–99% · Good 80–90% · Satisfactory 75–79% · Unsatisfactory <75% (PIP).",
            "",
            "## Demo narrative",
            "",
            "- **Hellen Howard** — Good (~86%): embargoed-release sample from PMS guidelines.",
            "- **Laura Lewis** — Very Good / Superior: incentive recommendation.",
            "- **Charles Carter** — Manager: cascade Unit Plans + 3 coaching conversations.",
            "- **Daisy Dawson** — Unsatisfactory (<75%): PIP / training path (competence gap).",
            "",
        ]
        for person in cast.values():
            templates = self.catalog["goal_templates"][person["group"]]
            count = min(person["goal_count"], len(templates))
            lines.append(
                f"## {person['full_name']} ({person['group']}) — {person.get('role_title', '')}"
            )
            lines.append(f"_Demo band: {person.get('demo_band', 'n/a')}_")
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
        print(f"=== STATIN PMS Seed ({'APPLY' if self.apply else 'DRY-RUN'}) ===")
        print(f"BASE_URL={self.api.config.BASE_URL} VERSION={self.api.version}")
        print(f"AUTH_TYPE={self.api.config.AUTH_TYPE} COMPANY={self.catalog.get('company_id')}")

        expected = len(self.catalog["cast"])
        cast = self.resolve_cast()
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


# late import for prior posts recovery
import json  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed STATIN PMS demo (Performance)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Show planned actions only")
    group.add_argument("--apply", action="store_true", help="Write data to Factorial")
    args = parser.parse_args()
    return StatinPmsSeeder(apply=args.apply).run()


if __name__ == "__main__":
    raise SystemExit(main())
