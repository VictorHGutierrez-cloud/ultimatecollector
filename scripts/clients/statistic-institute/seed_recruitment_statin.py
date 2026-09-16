#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed STATIN Recruitment (ATS) demo data — company 191864.

Creates STATIN-prefixed job postings + candidates/applications from catalog.json.
Does NOT change Time Off or PMS.

Usage:
  python scripts/clients/statistic-institute/seed_recruitment_statin.py --dry-run
  python scripts/clients/statistic-institute/seed_recruitment_statin.py --apply
"""

from __future__ import annotations

import argparse
import sys
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


def _short(body: Any, limit: int = 280) -> Any:
    text = str(body)
    return text if len(text) <= limit else text[:limit] + "..."


class StatinRecruitmentSeeder:
    def __init__(self, apply: bool) -> None:
        self.apply = apply
        self.api = StatinApi()
        self.catalog = load_catalog()
        self.company_id = str(self.catalog["company_id"])
        self.log: Dict[str, Any] = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "apply": apply,
            "actions": [],
            "errors": [],
            "ids": {},
        }

    def action(self, name: str, detail: Any = None) -> None:
        entry = {"action": name, "detail": detail}
        self.log["actions"].append(entry)
        print(f"  OK  {name}: {_short(detail)}")

    def error(self, name: str, detail: Any = None) -> None:
        entry = {"error": name, "detail": detail}
        self.log["errors"].append(entry)
        print(f"  ERR {name}: {_short(detail)}")

    def team_ids(self) -> Dict[str, str]:
        teams = self.api.list_all("teams/teams")
        by_name = {normalize_name(t.get("name")): t for t in teams}
        out: Dict[str, str] = {}
        for team in self.catalog.get("teams") or []:
            match = by_name.get(normalize_name(team["name"]))
            if match and match.get("id"):
                out[team["key"]] = str(match["id"])
            else:
                self.error("team_missing", team["name"])
        return out

    def ensure_job_postings(self, team_ids: Dict[str, str]) -> List[str]:
        existing = self.api.list_all("ats/job_postings")
        by_title = {normalize_name(j.get("title")): j for j in existing}
        created_ids: List[str] = []

        for job in self.catalog.get("job_postings") or []:
            title_key = normalize_name(job["title"])
            if title_key in by_title:
                jid = str(by_title[title_key].get("id"))
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
            team_id = team_ids.get(job.get("team_key") or "")
            if team_id:
                payload["team_id"] = team_id

            if not self.apply:
                self.action("dry_create_job_posting", payload)
                continue

            st, body = self.api.post("ats/job_postings", payload)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                created_ids.append(str(body["id"]))
                self.action("created_job_posting", {"id": body.get("id"), "title": job["title"]})
                continue

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
                created_ids.append(str(body2["id"]))
                self.action(
                    "created_job_posting_draft",
                    {"id": body2.get("id"), "title": job["title"]},
                )
            else:
                self.error(
                    "create_job_posting_failed",
                    {
                        "status": st,
                        "body": _short(body),
                        "retry_status": st2,
                        "retry_body": _short(body2),
                        "title": job["title"],
                    },
                )

        self.log["ids"]["job_postings"] = created_ids
        return created_ids

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
        created: List[Dict[str, Any]] = []

        for cand in candidates_def:
            job = jobs_by_title.get(normalize_name(cand["job_title"]))
            if not job:
                self.error("candidate_job_missing", cand["job_title"])
                continue

            existing = by_email.get(normalize_name(cand["email"]))
            if existing:
                candidate_id = str(existing.get("id"))
                self.action(
                    "candidate_exists",
                    {"email": cand["email"], "id": candidate_id},
                )
            else:
                payload = {
                    "first_name": cand["first_name"],
                    "last_name": cand["last_name"],
                    "email": cand["email"],
                    "company_id": self.company_id,
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
                        {
                            "id": candidate_id,
                            "name": f"{cand['first_name']} {cand['last_name']}",
                        },
                    )
                else:
                    apply_payload = {
                        "company_id": self.company_id,
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
                        created.append(
                            {"email": cand["email"], "job": cand["job_title"], "via": "apply"}
                        )
                        continue
                    self.error(
                        "create_candidate_failed",
                        {
                            "status": st,
                            "body": _short(body),
                            "retry_status": st2,
                            "retry_body": _short(body2),
                            "email": cand["email"],
                        },
                    )
                    continue

            # Ensure application link
            if not self.apply:
                continue

            apps = self.api.list_all(
                "ats/applications",
                params={"ats_candidate_id": candidate_id},
            )
            already = any(str(a.get("ats_job_posting_id")) == str(job["id"]) for a in apps)
            if already:
                self.action(
                    "application_exists",
                    {"email": cand["email"], "job": cand["job_title"]},
                )
                continue

            app_payload = {
                "ats_job_posting_id": str(job["id"]),
                "ats_candidate_id": candidate_id,
                "company_id": self.company_id,
                "cover_letter": cand.get("cover_letter"),
                "source": cand.get("source"),
                "medium": cand.get("medium"),
            }
            st, body = self.api.post("ats/applications", app_payload)
            if st in (200, 201):
                self.action(
                    "created_application",
                    {"email": cand["email"], "job": cand["job_title"], "status": st},
                )
                created.append({"email": cand["email"], "job": cand["job_title"], "via": "application"})
            else:
                apply_payload = {
                    "company_id": self.company_id,
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
                        "applied_via_apply_fallback",
                        {"email": cand["email"], "job": cand["job_title"]},
                    )
                else:
                    self.error(
                        "create_application_failed",
                        {
                            "status": st,
                            "body": _short(body),
                            "retry_status": st2,
                            "retry_body": _short(body2),
                            "email": cand["email"],
                        },
                    )

        self.log["ids"]["candidates"] = created

    def run(self) -> int:
        print(f"STATIN recruitment seed (apply={self.apply})")
        team_ids = self.team_ids()
        self.ensure_job_postings(team_ids)
        self.ensure_candidates()
        self.log["finished_at"] = datetime.now(timezone.utc).isoformat()
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mode = "apply" if self.apply else "dryrun"
        out = RUN_LOG_DIR / f"recruitment_{mode}_{stamp}.json"
        save_json(out, self.log)
        save_json(RUN_LOG_DIR / "recruitment_latest.json", self.log)
        print(f"Log: {out}")
        print(f"Errors: {len(self.log['errors'])}")
        return 1 if self.log["errors"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed STATIN ATS recruitment demo")
    parser.add_argument("--dry-run", action="store_true", help="Do not write to API")
    parser.add_argument("--apply", action="store_true", help="Create job postings and candidates")
    args = parser.parse_args()
    if not args.dry_run and not args.apply:
        parser.error("Use --dry-run or --apply")
    return StatinRecruitmentSeeder(apply=args.apply).run()


if __name__ == "__main__":
    raise SystemExit(main())
