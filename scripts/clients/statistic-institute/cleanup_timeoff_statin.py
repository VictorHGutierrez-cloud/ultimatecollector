#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STATIN sandbox cleanup:
  1) DELETE every timeoff leave (all employees)
  2) Remove duplicate vacation counters ("Time off allowance" 23d)
     on SIJ policies, migrating incidences to SIJ Vacation Allowance

Usage (repo root):
  python scripts/clients/statistic-institute/cleanup_timeoff_statin.py
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.api_client import APIClient
from ultimate_collector.core.client_config import activate_client
from ultimate_collector.core.config import Config

CLIENT_ID = "statistic-institute"
RUN_LOG = ROOT / "clients" / CLIENT_ID / "run_log"

# SIJ vacation policies → keep SIJ Vacation Allowance, delete duplicate "Time off allowance"
SIJ_POLICY_VACATION_ALLOWANCE = {
    "367078": "617645",  # 15d
    "367079": "617647",  # 20d
    "367080": "617649",  # 21d
    "367081": "617651",  # 25d
}


class Api:
    def __init__(self) -> None:
        self.config = Config()
        self.client = APIClient()
        self.prefix = f"api/{self.config.API_VERSION}/resources"
        self.log: List[Dict[str, Any]] = []

    def _url(self, path: str) -> str:
        return self.client._build_url(f"{self.prefix}/{path.lstrip('/')}")

    def get(self, path: str, params: Optional[Dict] = None) -> Tuple[int, Any]:
        r = self.client.session.get(
            self._url(path),
            headers=self.client._get_headers(),
            params=params,
            timeout=self.config.TIMEOUT,
        )
        try:
            body = r.json() if r.content else None
        except Exception:
            body = {"raw": r.text[:1000]}
        return r.status_code, body

    def delete(self, path: str) -> Tuple[int, Any]:
        r = self.client.session.delete(
            self._url(path),
            headers=self.client._get_headers(),
            timeout=self.config.TIMEOUT,
        )
        try:
            body = r.json() if r.content else None
        except Exception:
            body = {"raw": r.text[:1000]}
        self.log.append({"method": "DELETE", "path": path, "status": r.status_code})
        return r.status_code, body

    def post(self, path: str, data: Optional[Dict] = None) -> Tuple[int, Any]:
        r = self.client.session.post(
            self._url(path),
            headers=self.client._get_headers(),
            json=data,
            timeout=self.config.TIMEOUT,
        )
        try:
            body = r.json() if r.content else None
        except Exception:
            body = {"raw": r.text[:1000]}
        self.log.append({"method": "POST", "path": path, "status": r.status_code, "req": data})
        return r.status_code, body

    def list_all(self, path: str) -> List[Dict]:
        items: List[Dict] = []
        page = 1
        while page <= 50:
            status, body = self.get(path, params={"limit": 100, "page": page})
            if status != 200 or not isinstance(body, dict):
                break
            data = body.get("data") or []
            if isinstance(data, dict):
                data = [data]
            items.extend(data)
            if len(data) < 100:
                break
            page += 1
        return items


def main() -> int:
    activate_client(CLIENT_ID)
    Config.reload()
    api = Api()

    result: Dict[str, Any] = {
        "client": CLIENT_ID,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "leaves_deleted": [],
        "leaves_failed": [],
        "allowances_deleted": [],
        "allowances_failed": [],
    }

    # ----- 1) Delete ALL leaves -----
    leaves = api.list_all("timeoff/leaves")
    print(f"Found {len(leaves)} leaves — deleting all…")
    for i, leave in enumerate(leaves, 1):
        lid = str(leave.get("id") or "")
        if not lid:
            continue
        try:
            status, body = api.delete(f"timeoff/leaves/{lid}")
        except Exception as exc:  # noqa: BLE001
            result["leaves_failed"].append({"id": lid, "error": str(exc)[:300]})
            print(f"  FAIL leave {lid}: {exc}")
            time.sleep(0.2)
            continue
        if status in (200, 204):
            result["leaves_deleted"].append(lid)
        else:
            result["leaves_failed"].append({"id": lid, "status": status, "body": body})
            print(f"  FAIL leave {lid}: {status}")
        if i % 25 == 0:
            print(f"  … {i}/{len(leaves)}")
            time.sleep(0.3)

    # Refresh count
    remaining = api.list_all("timeoff/leaves")
    result["leaves_remaining_after"] = len(remaining)
    print(f"Leaves deleted: {len(result['leaves_deleted'])} · failed: {len(result['leaves_failed'])} · remaining: {len(remaining)}")

    # ----- 2) Delete duplicate "Time off allowance" on SIJ policies -----
    allowances = api.list_all("timeoff/allowances")
    extras = []
    for a in allowances:
        name = (a.get("name") or "").strip()
        policy_id = str(a.get("timeoff_policy_id") or "")
        aid = str(a.get("id") or "")
        if name == "Time off allowance" and policy_id in SIJ_POLICY_VACATION_ALLOWANCE:
            extras.append(
                {
                    "id": aid,
                    "policy_id": policy_id,
                    "alt": SIJ_POLICY_VACATION_ALLOWANCE[policy_id],
                    "name": name,
                }
            )

    print(f"Found {len(extras)} duplicate Time off allowance on SIJ policies…")
    for ex in extras:
        # Prefer migrate-then-delete endpoint
        status, body = api.post(
            "timeoff/allowances/delete_with_alt_allowance",
            {"id": ex["id"], "alt_allowance_id": ex["alt"]},
        )
        if status not in (200, 201, 204):
            status2, body2 = api.delete(f"timeoff/allowances/{ex['id']}")
            if status2 in (200, 204):
                result["allowances_deleted"].append({**ex, "method": "DELETE", "status": status2})
                print(f"  Deleted {ex['id']} (Time off allowance) via DELETE → keep {ex['alt']}")
            else:
                result["allowances_failed"].append(
                    {**ex, "migrate_status": status, "migrate_body": body, "delete_status": status2, "delete_body": body2}
                )
                print(f"  FAIL allowance {ex['id']}: migrate={status} delete={status2}")
        else:
            result["allowances_deleted"].append({**ex, "method": "delete_with_alt", "status": status})
            print(f"  Deleted {ex['id']} (Time off allowance) → migrated to {ex['alt']}")

    allowances_after = api.list_all("timeoff/allowances")
    result["allowances_after"] = [
        {
            "id": a.get("id"),
            "name": a.get("name"),
            "policy_id": a.get("timeoff_policy_id"),
            "days_cents": a.get("holiday_allowance_in_cents"),
        }
        for a in allowances_after
    ]
    result["finished_at"] = datetime.now().isoformat(timespec="seconds")

    RUN_LOG.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RUN_LOG / f"timeoff_cleanup_{ts}.json"
    latest = RUN_LOG / "timeoff_cleanup_latest.json"
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    out.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")
    print("=== Cleanup done ===")
    return 0 if not result["leaves_failed"] and not result["allowances_failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
