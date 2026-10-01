#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed front-facing Kibanda demo (company 191232 / client glovo-sibasi).

Includes: locations (branches), legal entity, cast rename, teams, managers, announcements.
No performance / goals.

Uso:
  python scripts/clients/glovo-sibasi/kibanda_seed_front.py --dry-run
  python scripts/clients/glovo-sibasi/kibanda_seed_front.py --apply
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("glovo-sibasi")

CLIENT_DIR = ROOT / "clients" / "glovo-sibasi"
sys.path.insert(0, str(CLIENT_DIR))
from api_helpers import (  # noqa: E402
    ASSET_DIR,
    RUN_LOG_DIR,
    KibandaApi,
    emp_name,
    load_catalog,
    normalize_name,
    save_json,
)


def _short(body: Any, limit: int = 240) -> Any:
    text = str(body)
    return text if len(text) <= limit else text[:limit] + "..."


class KibandaFrontSeeder:
    def __init__(self, apply: bool) -> None:
        self.apply = apply
        self.api = KibandaApi()
        self.catalog = load_catalog()
        self.log: Dict[str, Any] = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "mode": "apply" if apply else "dry-run",
            "company_id": self.catalog.get("company_id"),
            "actions": [],
            "errors": [],
            "ids": {},
        }
        self.location_ids: Dict[str, str] = {}
        self.main_location_id: Optional[str] = None
        self.legal_entity_id: Optional[str] = None

    def action(self, name: str, detail: Any = None) -> None:
        entry = {"action": name, "detail": detail}
        self.log["actions"].append(entry)
        print(f"- {name}: {detail}")

    def error(self, name: str, detail: Any = None) -> None:
        entry = {"action": name, "detail": detail}
        self.log["errors"].append(entry)
        print(f"! ERROR {name}: {detail}")

    def ensure_locations(self) -> Dict[str, str]:
        loc_defs: List[dict] = list(self.catalog.get("locations") or [])
        if not loc_defs and self.catalog.get("location"):
            loc_defs = [{**self.catalog["location"], "key": "main"}]

        locations = self.api.list_all("locations/locations")
        by_name = {normalize_name(l.get("name")): l for l in locations}
        unused_generics = [
            loc
            for loc in locations
            if "Kibanda" not in str(loc.get("name") or "")
        ]

        for loc_def in loc_defs:
            key = loc_def.get("key") or normalize_name(loc_def["name"]).replace(" ", "_")
            existing = by_name.get(normalize_name(loc_def["name"]))
            if existing:
                self.location_ids[key] = str(existing["id"])
                self.action("location_exists", {"key": key, "id": existing["id"], "name": loc_def["name"]})
                if loc_def.get("main"):
                    self.main_location_id = str(existing["id"])
                continue

            reuse = unused_generics.pop(0) if unused_generics else None
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
                "main": bool(loc_def.get("main", False)),
                "latitude": loc_def.get("latitude"),
                "longitude": loc_def.get("longitude"),
            }

            if not self.apply:
                self.action("dry_upsert_location", {"key": key, "reuse": bool(reuse), **payload})
                lid = str(reuse["id"]) if reuse else f"dry-{key}"
                self.location_ids[key] = lid
                if loc_def.get("main"):
                    self.main_location_id = lid
                continue

            if reuse:
                put_payload = {"id": str(reuse["id"]), **payload}
                st, body = self.api.put(f"locations/locations/{reuse['id']}", put_payload)
                if st in (200, 201):
                    self.location_ids[key] = str(reuse["id"])
                    by_name[normalize_name(loc_def["name"])] = {**reuse, **payload, "id": reuse["id"]}
                    self.action("updated_location", {"key": key, "id": reuse["id"], "name": loc_def["name"]})
                    if loc_def.get("main"):
                        self.main_location_id = str(reuse["id"])
                    continue
                self.action("update_location_failed_try_create", {"status": st, "body": _short(body)})

            created = False
            for attempt in (
                dict(payload),
                {
                    **payload,
                    "country": loc_def.get("country_fallback", "us"),
                    "timezone": loc_def.get("timezone_fallback", "Africa/Nairobi"),
                },
            ):
                st, body = self.api.post("locations/locations", attempt)
                if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                    self.location_ids[key] = str(body["id"])
                    by_name[normalize_name(loc_def["name"])] = body
                    self.action("created_location", {"key": key, "id": body["id"], "name": loc_def["name"]})
                    if loc_def.get("main"):
                        self.main_location_id = str(body["id"])
                    created = True
                    break
                self.action("create_location_attempt_failed", {"status": st, "body": _short(body)})
            if not created:
                self.error("create_location_failed", loc_def["name"])

        self.log["ids"]["locations"] = dict(self.location_ids)
        self.log["ids"]["location_id"] = self.main_location_id
        return self.location_ids

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
            self.legal_entity_id = str(entities[0]["id"]) if entities else "dry-legal-entity"
            self.log["ids"]["legal_entity_id"] = self.legal_entity_id
            return self.legal_entity_id

        for attempt in (
            dict(payload),
            {
                **payload,
                "country": le_def.get("country_fallback", "us"),
                "currency": le_def.get("currency_fallback", "USD"),
            },
        ):
            st, body = self.api.post("companies/legal_entities", attempt)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                self.legal_entity_id = str(body["id"])
                self.action("created_legal_entity", {"id": self.legal_entity_id, "country": attempt["country"]})
                self.log["ids"]["legal_entity_id"] = self.legal_entity_id
                return self.legal_entity_id
            self.action("create_legal_entity_attempt_failed", {"status": st, "body": _short(body)})

        if entities:
            preferred = next(
                (e for e in entities if e.get("currency") in (le_def.get("currency"), "KES", "USD")),
                entities[0],
            )
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
                                {"status": st, "body": _short(body), "payload": payload},
                            )

            if not emp:
                loc_key = person.get("location_key")
                location_id = self.location_ids.get(loc_key) or self.main_location_id
                payload = {
                    "company_id": str(self.catalog["company_id"]),
                    "first_name": person["first_name"],
                    "last_name": person["last_name"],
                    "email": person["email"],
                    "gender": person.get("gender"),
                    "contract_starts_on": "2025-01-15",
                    "contract_effective_on": "2025-01-15",
                    "country": "ke",
                    "nationality": "KE",
                    "city": "Nairobi",
                    "state": "Nairobi County",
                }
                if self.legal_entity_id and not str(self.legal_entity_id).startswith("dry-"):
                    payload["legal_entity_id"] = self.legal_entity_id
                if location_id and not str(location_id).startswith("dry-"):
                    payload["location_id"] = location_id

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
                    self.action("created_employee", {"id": body.get("id"), "name": person["full_name"]})
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
                    {"full_name": person["full_name"], "terminated_on": emp.get("terminated_on")},
                )
                continue

            loc_key = person.get("location_key")
            location_id = self.location_ids.get(loc_key) or self.main_location_id
            if self.apply:
                updates = {"id": str(emp["id"])}
                if location_id and not str(location_id).startswith("dry-") and str(emp.get("location_id")) != str(location_id):
                    updates["location_id"] = location_id
                if self.legal_entity_id and not str(self.legal_entity_id).startswith("dry-") and str(emp.get("legal_entity_id")) != str(self.legal_entity_id):
                    updates["legal_entity_id"] = self.legal_entity_id
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
                "access_id": str(emp.get("access_id") or ""),
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
                self.action("team_exists", {"key": team["key"], "id": existing["id"], "name": team["name"]})
                continue
            payload = {
                "name": team["name"],
                "description": f"Kibanda branch/ops team ({team['key']})",
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
                self.error("create_team_failed", {"status": status, "body": _short(body), "payload": payload})

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
        for employee_name, manager_name in (self.catalog.get("manager_map") or {}).items():
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
                self.action("manager_ok", {"employee": employee_name, "manager_id": desired_manager_id})
                continue
            payload = {"id": emp["employee_id"], "manager_id": desired_manager_id}
            if not self.apply:
                self.action("dry_update_manager", {"employee": employee_name, **payload})
                continue
            status, body = self.api.put(f"employees/employees/{emp['employee_id']}", payload)
            if status in (200, 201):
                self.action("updated_manager", {"employee": employee_name, "manager_id": desired_manager_id})
            else:
                self.error(
                    "update_manager_failed",
                    {"status": status, "body": _short(body), "payload": payload},
                )

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
                    (json.loads(latest_path.read_text(encoding="utf-8")).get("ids") or {}).get("posts")
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
            existing = by_title.get(normalize_name(post["title"]))
            cover_path = self._cover_path(post)
            if existing and existing.get("cover_image_url"):
                pid = existing.get("id")
                created_ids.append(pid)
                self.action(
                    "post_exists_with_cover",
                    {"title": post["title"], "id": pid},
                )
                if self.apply and not existing.get("published_at"):
                    self._publish_post(str(pid), post, group_id)
                continue
            if existing and self.apply:
                # Public JSON API cannot attach cover on PUT — recreate with multipart.
                self._delete_post(str(existing["id"]))
                self.action(
                    "deleted_post_missing_cover",
                    {"title": post["title"], "id": existing["id"]},
                )

            payload = {
                "title": post["title"],
                "description": post["description"],
                "post_group_id": group_id,
                "allow_comments_and_reactions": bool(post.get("allow_comments_and_reactions", True)),
                "cover_image": str(cover_path) if cover_path else None,
            }
            if not self.apply or str(group_id).startswith("dry-"):
                self.action("dry_create_post", payload)
                continue
            st, body = self._create_post_with_cover(post, group_id, cover_path)
            if st in (200, 201) and isinstance(body, dict) and body.get("id"):
                pid = str(body.get("id"))
                self.action(
                    "created_post",
                    {
                        "id": pid,
                        "title": post["title"],
                        "has_cover": bool(body.get("cover_image_url")),
                    },
                )
                created_ids.append(pid)
                self._publish_post(pid, post, group_id)
            else:
                self.error(
                    "create_post_failed",
                    {"status": st, "body": _short(body), "payload": payload},
                )
        self.log["ids"]["posts"] = created_ids

    def _cover_path(self, post: dict) -> Optional[Path]:
        rel = post.get("cover_image")
        if not rel:
            return None
        path = ASSET_DIR / rel
        return path if path.exists() else None

    def _delete_post(self, post_id: str) -> None:
        url = self.api.client._build_url(self.api.resource(f"posts/posts/{post_id}"))
        headers = self.api.client._get_headers()
        self.api.client.session.delete(url, headers=headers, timeout=60)

    def _create_post_with_cover(
        self, post: dict, group_id: str, cover_path: Optional[Path]
    ) -> tuple[int, Any]:
        """Create post; use multipart form when a cover image is available."""
        if not cover_path:
            return self.api.post(
                "posts/posts",
                {
                    "title": post["title"],
                    "description": post["description"],
                    "post_group_id": group_id,
                    "allow_comments_and_reactions": bool(
                        post.get("allow_comments_and_reactions", True)
                    ),
                },
            )

        url = self.api.client._build_url(self.api.resource("posts/posts"))
        headers = self.api.client._get_headers()
        headers.pop("Content-Type", None)
        data = {
            "title": post["title"],
            "description": post["description"],
            "post_group_id": str(group_id),
            "allow_comments_and_reactions": (
                "true" if post.get("allow_comments_and_reactions", True) else "false"
            ),
        }
        content_type = "image/jpeg" if cover_path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        with cover_path.open("rb") as handle:
            files = {"cover_image": (cover_path.name, handle, content_type)}
            response = self.api.client.session.post(
                url, headers=headers, data=data, files=files, timeout=120
            )
        try:
            body = response.json() if response.content else None
        except Exception:
            body = {"raw": response.text[:1000]}
        return response.status_code, body

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
            self.error("publish_post_failed", {"id": post_id, "status": st, "body": _short(body)})

    def run(self) -> int:
        print(f"=== Kibanda Front Seed ({'APPLY' if self.apply else 'DRY-RUN'}) ===")
        print(f"BASE_URL={self.api.config.BASE_URL} VERSION={self.api.version}")
        print(f"AUTH_TYPE={self.api.config.AUTH_TYPE} COMPANY={self.catalog.get('company_id')}")

        expected = len(self.catalog["cast"])
        self.ensure_locations()
        self.ensure_legal_entity()
        cast = self.ensure_cast()
        if len(cast) < expected:
            self.error("incomplete_cast", f"resolved {len(cast)}/{expected}")
            self._persist()
            return 2

        self.ensure_teams(cast)
        self.update_managers(cast)
        self.ensure_posts()

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
    parser = argparse.ArgumentParser(description="Seed Kibanda front-facing demo data")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Show planned actions only")
    group.add_argument("--apply", action="store_true", help="Write data to Factorial")
    args = parser.parse_args()
    return KibandaFrontSeeder(apply=args.apply).run()


if __name__ == "__main__":
    raise SystemExit(main())
