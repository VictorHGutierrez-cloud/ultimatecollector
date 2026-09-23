#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed — Jamaica accrual pause demo (>14 calendar days).

Creates one approved SIJ Sick Leave for Felicity Ford (2026-08-03 .. 2026-08-18)
so the SQL accrual demo can show Absence_Above_Threshold = YES.

Usage (from repo root):
  python scripts/clients/statistic-institute/seed_jamaica_pause_demo.py
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

# Ensure API file logging can open (Config default: logs/factorial_api.log)
(ROOT / "logs").mkdir(parents=True, exist_ok=True)

from ultimate_collector.core.api_client import APIClient
from ultimate_collector.core.client_config import activate_client
from ultimate_collector.core.config import Config

CLIENT_ID = "statistic-institute"
RUN_LOG = ROOT / "clients" / CLIENT_ID / "run_log"

EMPLOYEE_NAME = "Felicity Ford"
EMPLOYEE_ID_HINT = "6375958"
LEAVE_TYPE_NAME = "SIJ Sick Leave"
SICK_ALLOWANCE_NAME = "SIJ Sick Allowance"
START_ON = "2026-08-03"
FINISH_ON = "2026-08-18"
DESCRIPTION = "SIJ resim — accrual pause >14 calendar days"
# SIJ vacation policies + legacy policy Felicity may still have assigned
SIJ_POLICY_IDS = ("367078", "367079", "367080", "367081", "366459")
SICK_ALLOWANCE_DAYS = 14  # demo pool so long sick leave can be requested


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
        self.log.append({"method": "POST", "path": path, "status": r.status_code, "req": data, "res": body})
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


def find_employee(emps: List[Dict]) -> Optional[Dict]:
    for e in emps:
        if str(e.get("id")) == EMPLOYEE_ID_HINT:
            return e
    name_l = EMPLOYEE_NAME.lower()
    for e in emps:
        full = (e.get("full_name") or f"{e.get('first_name', '')} {e.get('last_name', '')}").strip()
        if full.lower() == name_l:
            return e
    return None


def find_leave_type(types: List[Dict], name: str) -> Optional[Dict]:
    name_l = name.lower().strip()
    for t in types:
        if (t.get("name") or "").lower().strip() == name_l:
            return t
    return None


def overlaps(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    return a_start <= b_end and b_start <= a_end


def calendar_days(start: str, finish: str) -> int:
    s = date.fromisoformat(start)
    f = date.fromisoformat(finish)
    return (f - s).days + 1


def is_approved(leave: Dict) -> bool:
    if leave.get("approved") is True:
        return True
    status = str(leave.get("status") or "").lower()
    return status in ("approved", "accepted")


def cents(days: float) -> int:
    return int(round(days * 100))


def ensure_sick_allowances(api: Api, leave_type_id: str) -> List[Dict[str, Any]]:
    """Attach SIJ Sick Leave to SIJ policies so employees can request it."""
    existing = api.list_all("timeoff/allowances")
    out: List[Dict[str, Any]] = []
    for policy_id in SIJ_POLICY_IDS:
        found = None
        for a in existing:
            if (
                a.get("name") == SICK_ALLOWANCE_NAME
                and str(a.get("timeoff_policy_id")) == str(policy_id)
            ):
                found = a
                break
        if found:
            out.append({"policy_id": policy_id, "id": found.get("id"), "action": "exists"})
            continue
        payload = {
            "name": SICK_ALLOWANCE_NAME,
            "timeoff_policy_id": str(policy_id),
            "leave_type_ids": [str(leave_type_id)],
            "allowance_type": "days",
            "days_type": "working_days",
            "available_days": "all_days",
            "accrued_units_availability": "current_cycle",
            "count_holiday_as_workable": False,
            "cycle_start": "jan",
            "cycle_length": 12,
            "frequency": "yearly",
            "holiday_allowance_in_cents": cents(SICK_ALLOWANCE_DAYS),
            "maximum_amount_in_cents": cents(SICK_ALLOWANCE_DAYS),
            "carry_over_units_in_cents": 0,
            "expire_in_months": 12,
            "unlimited_carry_over": False,
            "unlimited_carry_over_expiration": False,
            "unlimited_holidays": False,
            "unlimited_accrued_hours": False,
            "negative_counter_type": "negative_counter_disabled",
            "proration_type": "proration_disabled",
            "pto_proratio_enabled": False,
            "rounding": "decimals",
            "source_units": "base_units",
            "tenure_periods": [],
            "tenure_periods_enabled": False,
            "tenure_period_transition": "beginning_of_cycle",
            "send_notification": False,
        }
        status, body = api.post("timeoff/allowances", payload)
        aid = None
        if isinstance(body, dict):
            data = body.get("data") or body
            if isinstance(data, list):
                data = data[0] if data else {}
            if isinstance(data, dict):
                aid = data.get("id") or body.get("id")
        out.append(
            {
                "policy_id": policy_id,
                "id": aid,
                "action": "created" if status in (200, 201) else "failed",
                "status": status,
                "body": body if status not in (200, 201) else None,
            }
        )
    return out


def main() -> int:
    activate_client(CLIENT_ID)
    Config.reload()
    api = Api()

    result: Dict[str, Any] = {
        "client": CLIENT_ID,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "target": {
            "employee_name": EMPLOYEE_NAME,
            "employee_id_hint": EMPLOYEE_ID_HINT,
            "leave_type_name": LEAVE_TYPE_NAME,
            "start_on": START_ON,
            "finish_on": FINISH_ON,
            "calendar_days": calendar_days(START_ON, FINISH_ON),
            "description": DESCRIPTION,
        },
        "action": None,
        "leave": None,
        "skipped_existing": None,
        "error": None,
    }

    emp = find_employee(api.list_all("employees/employees"))
    if not emp:
        result["error"] = f"Employee not found: {EMPLOYEE_NAME} / {EMPLOYEE_ID_HINT}"
        _write(result)
        print(result["error"])
        return 1

    lt = find_leave_type(api.list_all("timeoff/leave_types"), LEAVE_TYPE_NAME)
    if not lt:
        result["error"] = f"Leave type not found: {LEAVE_TYPE_NAME}"
        _write(result)
        print(result["error"])
        return 1

    employee_id = str(emp["id"])
    leave_type_id = str(lt["id"])
    result["resolved"] = {
        "employee_id": employee_id,
        "employee_name": emp.get("full_name") or EMPLOYEE_NAME,
        "leave_type_id": leave_type_id,
        "leave_type_name": lt.get("name"),
    }
    result["sick_allowances"] = ensure_sick_allowances(api, leave_type_id)

    existing = api.list_all("timeoff/leaves")
    for leave in existing:
        if str(leave.get("employee_id")) != employee_id:
            continue
        if str(leave.get("leave_type_id")) != leave_type_id:
            continue
        start = leave.get("start_on") or ""
        finish = leave.get("finish_on") or ""
        if not start or not finish:
            continue
        if overlaps(start[:10], finish[:10], START_ON, FINISH_ON) and is_approved(leave):
            result["action"] = "skipped_already_exists"
            result["skipped_existing"] = {
                "id": leave.get("id"),
                "start_on": start,
                "finish_on": finish,
                "approved": leave.get("approved"),
                "status": leave.get("status"),
                "description": leave.get("description"),
            }
            _write(result)
            print(f"SKIP: leave already exists id={leave.get('id')} {start}..{finish}")
            return 0

    payload = {
        "employee_id": employee_id,
        "leave_type_id": leave_type_id,
        "start_on": START_ON,
        "finish_on": FINISH_ON,
        "description": DESCRIPTION,
    }
    status, body = api.post("timeoff/leaves", payload)
    leave = None
    if isinstance(body, dict):
        leave = body.get("data") or body
        if isinstance(leave, list):
            leave = leave[0] if leave else None

    approve_status = None
    approve_body = None
    if status in (200, 201) and leave and leave.get("id"):
        # Re-fetch: some leave types auto-approve on create
        leave_id = str(leave["id"])
        all_leaves = api.list_all("timeoff/leaves")
        refreshed = next((x for x in all_leaves if str(x.get("id")) == leave_id), leave)
        if is_approved(refreshed):
            result["action"] = "created_already_approved"
            result["leave"] = {
                "status": status,
                "id": leave_id,
                "req": payload,
                "approved": refreshed.get("approved"),
                "days_taken": refreshed.get("days_taken"),
                "approve_status": "skipped_already_approved",
            }
        else:
            approve_status, approve_body = api.post("timeoff/leaves/approve", {"id": leave_id})
            result["approve"] = {"status": approve_status, "body": approve_body}
            # Re-check after approve attempt (403 can mean policy forbids explicit approve)
            all_leaves = api.list_all("timeoff/leaves")
            refreshed = next((x for x in all_leaves if str(x.get("id")) == leave_id), leave)
            if is_approved(refreshed):
                result["action"] = "created_and_approved"
            else:
                result["action"] = "created_not_approved"
                result["error"] = f"leave created but not approved; approve_status={approve_status}"
            result["leave"] = {
                "status": status,
                "id": leave_id,
                "req": payload,
                "approved": refreshed.get("approved"),
                "days_taken": refreshed.get("days_taken"),
                "approve_status": approve_status,
            }
            if result.get("error"):
                result["api_log_tail"] = api.log[-10:]
                _write(result)
                print(result["error"])
                return 1
    else:
        result["error"] = f"create leave failed status={status} body={body}"
        result["action"] = "create_failed"
        result["leave"] = {"status": status, "body": body, "req": payload}
        _write(result)
        print(result["error"])
        return 1

    result["api_log_tail"] = api.log[-10:]
    _write(result)
    print(
        f"OK: leave id={result['leave']['id']} "
        f"{START_ON}..{FINISH_ON} ({result['target']['calendar_days']} calendar days) "
        f"approved={result['leave'].get('approved')} action={result['action']}"
    )
    return 0


def _write(result: Dict[str, Any]) -> None:
    RUN_LOG.mkdir(parents=True, exist_ok=True)
    out = RUN_LOG / f"jamaica_pause_seed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    latest = RUN_LOG / "jamaica_pause_seed_latest.json"
    latest.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    raise SystemExit(main())
