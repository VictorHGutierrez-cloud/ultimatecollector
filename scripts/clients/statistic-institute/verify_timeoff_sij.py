#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventário pós-seed Time Off SIJ + coleta leve."""

from __future__ import annotations

import json
import sys
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


class Api:
    def __init__(self) -> None:
        self.config = Config()
        self.client = APIClient()
        self.prefix = f"api/{self.config.API_VERSION}/resources"

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

    def list_all(self, path: str) -> List[Dict]:
        items: List[Dict] = []
        page = 1
        while page <= 30:
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
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    endpoints = [
        "timeoff/leave_types",
        "timeoff/policies",
        "timeoff/policy_assignments",
        "timeoff/allowances",
        "timeoff/leaves",
        "timeoff/allowance_incidences",
        "employees/employees",
    ]
    inv: Dict[str, Any] = {"client": CLIENT_ID, "collected_at": ts, "counts": {}, "sij_highlights": {}}

    for ep in endpoints:
        items = api.list_all(ep)
        inv["counts"][ep] = len(items)
        # save raw snippet for SIJ-named resources
        if ep in ("timeoff/leave_types", "timeoff/policies", "timeoff/allowances"):
            sij = [x for x in items if str(x.get("name", "")).startswith("SIJ")]
            inv["sij_highlights"][ep] = [
                {"id": x.get("id"), "name": x.get("name"), **({"holiday_allowance_in_cents": x.get("holiday_allowance_in_cents"), "maximum_amount_in_cents": x.get("maximum_amount_in_cents")} if ep.endswith("allowances") else {})}
                for x in sij
            ]
        if ep == "timeoff/leaves":
            sij_leaves = [
                {
                    "id": x.get("id"),
                    "employee_id": x.get("employee_id"),
                    "leave_type_id": x.get("leave_type_id"),
                    "start_on": x.get("start_on"),
                    "finish_on": x.get("finish_on"),
                    "approved": x.get("approved"),
                    "description": x.get("description"),
                }
                for x in items
                if "SIJ" in str(x.get("description") or "")
            ]
            inv["sij_highlights"]["sample_leaves"] = sij_leaves

    RUN_LOG.mkdir(parents=True, exist_ok=True)
    out = RUN_LOG / f"timeoff_inventory_after_{ts}.json"
    out.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    latest = RUN_LOG / "timeoff_inventory_after.json"
    latest.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(inv["counts"], indent=2))
    print("SIJ leave_types:", len(inv["sij_highlights"].get("timeoff/leave_types", [])))
    print("SIJ policies:", len(inv["sij_highlights"].get("timeoff/policies", [])))
    print("SIJ allowances:", len(inv["sij_highlights"].get("timeoff/allowances", [])))
    print("SIJ sample leaves:", len(inv["sij_highlights"].get("sample_leaves", [])))
    print("Wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
