#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed Business Case Leave demos (Examples 3–4 + Extended Sick Leave cascade).

Faithful sandbox reproduction of STATIN Factorial Business Case — Leave Requirements
from Example 3 through Extended Sick Leave / Return to Office.

Usage (repo root):
  python scripts/clients/statistic-institute/seed_business_case_leave_demos.py
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
(ROOT / "logs").mkdir(parents=True, exist_ok=True)

from ultimate_collector.core.api_client import APIClient
from ultimate_collector.core.client_config import activate_client
from ultimate_collector.core.config import Config

CLIENT_ID = "statistic-institute"
COMPANY_ID = "191864"
RUN_LOG = ROOT / "clients" / CLIENT_ID / "run_log"

# SIJ Vacation policy IDs (15/20/21/25) + legacy
SIJ_POLICY_IDS = ("367078", "367079", "367080", "367081", "366459")
POLICY_20 = "367079"  # Charles Carter tier

# Demo cast
CHARLES = {"name": "Charles Carter", "id": "6375931"}  # Example 3 — 20 days/year
CLARA = {"name": "Clara Cooper", "id": "6375951"}  # Example 4 — retro sick (also tier 20)
EMPLOYEE_A = {"name": "Steven Scott", "id": "6376052"}  # Extended Sick cascade (tier 20)


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


def cents(days: float) -> int:
    return int(round(days * 100))


def find_by_name(items: List[Dict], name: str) -> Optional[Dict]:
    name_l = name.lower().strip()
    for it in items:
        if (it.get("name") or "").lower().strip() == name_l:
            return it
    return None


def find_employee(emps: List[Dict], hint: Dict[str, str]) -> Optional[Dict]:
    for e in emps:
        if str(e.get("id")) == hint["id"]:
            return e
    for e in emps:
        full = (e.get("full_name") or f"{e.get('first_name', '')} {e.get('last_name', '')}").strip()
        if full.lower() == hint["name"].lower():
            return e
    return None


def ensure_leave_type(
    api: Api,
    name: str,
    color: str = "07A2AD",
    *,
    attachment: bool = False,
    attachment_mandatory: bool = False,
) -> Dict:
    existing = find_by_name(api.list_all("timeoff/leave_types"), name)
    if existing:
        return existing
    payload = {
        "name": name,
        "identifier": "custom",
        "color": color,
        "company_id": COMPANY_ID,
        "accrues": True,
        "approval_required": True,
        "workable": False,
        "payable": name != "SIJ No Pay Leave",
        "visibility": True,
        "editable": True,
        "details_required": False,
        "attachment": attachment,
        "is_attachment_mandatory": attachment_mandatory,
        "allow_endless": False,
        "half_days_units_enabled": True,
    }
    status, body = api.post("timeoff/leave_types", payload)
    if status not in (200, 201) or not isinstance(body, dict):
        raise RuntimeError(f"leave_type {name} failed {status}: {body}")
    data = body.get("data") or body
    if isinstance(data, list):
        data = data[0]
    return data


def ensure_allowance_on_policies(
    api: Api,
    *,
    name: str,
    leave_type_id: str,
    days: float,
    policy_ids: Tuple[str, ...] = SIJ_POLICY_IDS,
) -> List[Dict[str, Any]]:
    existing = api.list_all("timeoff/allowances")
    out: List[Dict[str, Any]] = []
    for policy_id in policy_ids:
        found = None
        for a in existing:
            if a.get("name") == name and str(a.get("timeoff_policy_id")) == str(policy_id):
                found = a
                break
        if found:
            out.append({"policy_id": policy_id, "id": found.get("id"), "action": "exists"})
            continue
        payload = {
            "name": name,
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
            "holiday_allowance_in_cents": cents(days),
            "maximum_amount_in_cents": cents(days),
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


def find_allowance(api: Api, name: str, policy_id: str) -> Optional[Dict]:
    for a in api.list_all("timeoff/allowances"):
        if a.get("name") == name and str(a.get("timeoff_policy_id")) == str(policy_id):
            return a
    return None


def is_approved(leave: Dict) -> bool:
    if leave.get("approved") is True:
        return True
    return str(leave.get("status") or "").lower() in ("approved", "accepted")


def overlaps(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    return a_start <= b_end and b_start <= a_end


def find_existing_leave(
    leaves: List[Dict],
    *,
    employee_id: str,
    leave_type_id: str,
    start_on: str,
    finish_on: str,
) -> Optional[Dict]:
    for leave in leaves:
        if str(leave.get("employee_id")) != str(employee_id):
            continue
        if str(leave.get("leave_type_id")) != str(leave_type_id):
            continue
        start = (leave.get("start_on") or "")[:10]
        finish = (leave.get("finish_on") or "")[:10]
        if not start or not finish:
            continue
        if overlaps(start, finish, start_on, finish_on) and is_approved(leave):
            return leave
    return None


def create_leave(
    api: Api,
    *,
    employee_id: str,
    leave_type_id: str,
    start_on: str,
    finish_on: str,
    description: str,
) -> Dict[str, Any]:
    description = (description or "")[:255]
    leaves = api.list_all("timeoff/leaves")
    existing = find_existing_leave(
        leaves,
        employee_id=employee_id,
        leave_type_id=leave_type_id,
        start_on=start_on,
        finish_on=finish_on,
    )
    if existing:
        return {
            "action": "skipped_exists",
            "id": existing.get("id"),
            "start_on": existing.get("start_on"),
            "finish_on": existing.get("finish_on"),
            "approved": existing.get("approved"),
            "description": existing.get("description"),
        }

    payload = {
        "employee_id": str(employee_id),
        "leave_type_id": str(leave_type_id),
        "start_on": start_on,
        "finish_on": finish_on,
        "description": description,
    }
    status, body = api.post("timeoff/leaves", payload)
    leave = None
    if isinstance(body, dict):
        leave = body.get("data") or body
        if isinstance(leave, list):
            leave = leave[0] if leave else None

    if status not in (200, 201) or not leave or not leave.get("id"):
        return {"action": "create_failed", "status": status, "body": body, "req": payload}

    leave_id = str(leave["id"])
    # Refresh — some types auto-approve
    refreshed = next((x for x in api.list_all("timeoff/leaves") if str(x.get("id")) == leave_id), leave)
    approve_status = None
    if not is_approved(refreshed):
        approve_status, _ = api.post("timeoff/leaves/approve", {"id": leave_id})
        refreshed = next((x for x in api.list_all("timeoff/leaves") if str(x.get("id")) == leave_id), refreshed)

    return {
        "action": "created",
        "id": leave_id,
        "status": status,
        "approve_status": approve_status,
        "approved": refreshed.get("approved"),
        "start_on": start_on,
        "finish_on": finish_on,
        "days_taken": refreshed.get("days_taken"),
        "req": payload,
    }


def create_incidence(
    api: Api,
    *,
    employee_id: str,
    allowance_id: str,
    days: float,
    description: str,
) -> Dict[str, Any]:
    payload = {
        "employee_id": str(employee_id),
        "timeoff_allowance_id": str(allowance_id),
        "days_in_cents": cents(days),
        "effective_on": date.today().isoformat(),
        "target_balance": "available",
        "description": (description or "")[:255],
        "_skip_notifications": True,
    }
    status, body = api.post("timeoff/allowance_incidences", payload)
    return {"status": status, "body": body, "req": payload}


def daterange_days(start: str, finish: str) -> int:
    return (date.fromisoformat(finish) - date.fromisoformat(start)).days + 1


def add_days(iso: str, n: int) -> str:
    return (date.fromisoformat(iso) + timedelta(days=n)).isoformat()


def main() -> int:
    activate_client(CLIENT_ID)
    Config.reload()
    api = Api()

    result: Dict[str, Any] = {
        "client": CLIENT_ID,
        "company_id": COMPANY_ID,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "scenarios": {},
        "honest_gaps": [
            "Factorial does NOT auto-pause vacation accrual during LOA >14 calendar days.",
            "Factorial does NOT auto-run Return-to-Work cancel of remaining ESL days.",
            "Factorial does NOT auto-cascade Extended Sick across Sick/Departmental/past years/Vacation/No Pay.",
            "Demo reproduces the Business Case with leave types + dated approved leaves + incidences + SQL/demo script.",
        ],
    }

    emps = api.list_all("employees/employees")
    charles = find_employee(emps, CHARLES)
    clara = find_employee(emps, CLARA)
    employee_a = find_employee(emps, EMPLOYEE_A)
    if not charles or not clara or not employee_a:
        result["error"] = {
            "charles": bool(charles),
            "clara": bool(clara),
            "employee_a": bool(employee_a),
        }
        _write(result)
        print("ERROR: missing demo employees", result["error"])
        return 1

    # --- Leave types ---
    vacation = ensure_leave_type(api, "SIJ Vacation Leave", "07A2AD")
    sick = ensure_leave_type(api, "SIJ Sick Leave", "EF4444")
    esl = ensure_leave_type(
        api,
        "SIJ Extended Sick Leave",
        "B91C1C",
        attachment=True,
        attachment_mandatory=True,
    )
    departmental = ensure_leave_type(api, "SIJ Departmental Leave", "F97316")
    no_pay = ensure_leave_type(api, "SIJ No Pay Leave", "6B7280")

    result["leave_types"] = {
        "vacation": {"id": vacation.get("id"), "name": vacation.get("name")},
        "sick": {"id": sick.get("id"), "name": sick.get("name")},
        "extended_sick": {"id": esl.get("id"), "name": esl.get("name")},
        "departmental": {"id": departmental.get("id"), "name": departmental.get("name")},
        "no_pay": {"id": no_pay.get("id"), "name": no_pay.get("name")},
    }

    # Allowances so employees can request these types
    result["allowances"] = {
        "extended_sick": ensure_allowance_on_policies(
            api, name="SIJ Extended Sick Allowance", leave_type_id=str(esl["id"]), days=14
        ),
        "departmental": ensure_allowance_on_policies(
            api, name="SIJ Departmental Allowance", leave_type_id=str(departmental["id"]), days=17
        ),
        "no_pay": ensure_allowance_on_policies(
            api, name="SIJ No Pay Allowance", leave_type_id=str(no_pay["id"]), days=60
        ),
        # ensure sick exists (may already from pause demo)
        "sick": ensure_allowance_on_policies(
            api, name="SIJ Sick Allowance", leave_type_id=str(sick["id"]), days=14
        ),
    }

    # ========== Example 3: Long Vacation Dec 1–18 (Charles, 20 days/year) ==========
    # Calendar 18 days; weekends=4; working≈14 — matches Business Case
    ex3 = create_leave(
        api,
        employee_id=str(charles["id"]),
        leave_type_id=str(vacation["id"]),
        start_on="2026-12-01",
        finish_on="2026-12-18",
        description=(
            "Business Case Example 3 — Long Vacation. "
            "Tier 20 days/year. Dec 1–18 (14 working + 4 weekend). "
            "Jamaica: pause accrual Dec 1–18; resume Dec 19. "
            "Dec accrual if pause: 13 × (20/365) ≈ 0.7123 days."
        ),
    )
    result["scenarios"]["example_3_long_vacation"] = {
        "employee": CHARLES,
        "annual_rate_days": 20,
        "start_on": "2026-12-01",
        "finish_on": "2026-12-18",
        "calendar_days": daterange_days("2026-12-01", "2026-12-18"),
        "expected_working_days_approx": 14,
        "expected_weekend_days": 4,
        "jamaica_pause": "Dec 1–18",
        "jamaica_resume": "Dec 19",
        "december_accrual_if_pause": "13 × (20/365) ≈ 0.7123",
        "leave": ex3,
        "sql_filters": {"Data_init": "2026-12-01", "Data_end": "2026-12-31"},
    }

    # ========== Example 4: Retroactive sick Jun 25–26 (Clara) ==========
    ex4 = create_leave(
        api,
        employee_id=str(clara["id"]),
        leave_type_id=str(sick["id"]),
        start_on="2026-06-25",
        finish_on="2026-06-26",
        description=(
            "Business Case Example 4 — Retroactive Leave. "
            "Applied on 2026-07-10 for dates Jun 25–26. "
            "Factorial already credited accrual for those days; "
            "no automatic reversal — HR manual adjustment if required."
        ),
    )
    result["scenarios"]["example_4_retroactive_sick"] = {
        "employee": CLARA,
        "leave_dates": "2026-06-25 .. 2026-06-26",
        "applied_on": "2026-07-10",
        "calendar_days": 2,
        "leave": ex4,
        "demo_note": "Show leave + explain HR incidence if reversing accrued days.",
    }

    # ========== Extended Sick — early Return to Work (Employee A / Steven) ==========
    rtw = create_leave(
        api,
        employee_id=str(employee_a["id"]),
        leave_type_id=str(esl["id"]),
        start_on="2025-12-01",
        finish_on="2025-12-14",
        description=(
            "BC ESL early RTW: requested Dec1-18 2025; RTW Dec15 approved; "
            "Dec15-18 cancelled. Stored Dec1-14. Cert required. Pause=process/SQL."
        ),
    )
    result["scenarios"]["extended_sick_early_rtw"] = {
        "employee": EMPLOYEE_A,
        "original_request": "2025-12-01 .. 2025-12-18",
        "return_to_work_date": "2025-12-15",
        "stored_leave_after_cancel": "2025-12-01 .. 2025-12-14",
        "approvals": "Employee → Supervisor → Admin (demo narrative)",
        "leave": rtw,
    }

    # Seed balances BEFORE cascade (Departmental needs 10+7=17)
    incidences = []
    for allowance_name, days, desc in [
        ("SIJ Extended Sick Allowance", 14.0, "BC: ESL balance 14"),
        ("SIJ Departmental Allowance", 17.0, "BC: Dept 10 + past-2y 7"),
        ("SIJ Sick Allowance", 5.0, "BC: past-2y sick offset +5"),
        ("SIJ No Pay Allowance", 14.0, "BC: No Pay pool 14"),
    ]:
        allow = find_allowance(api, allowance_name, POLICY_20)
        if not allow:
            incidences.append({"allowance": allowance_name, "action": "allowance_missing"})
            continue
        incidences.append(
            create_incidence(
                api,
                employee_id=str(employee_a["id"]),
                allowance_id=str(allow["id"]),
                days=days,
                description=desc,
            )
        )

    # ========== Extended Sick — 60-day cascade (Employee A) ==========
    start = "2026-01-05"
    segments = [
        ("SIJ Extended Sick Leave", str(esl["id"]), 14, "ESL current year 14"),
        ("SIJ Departmental Leave", str(departmental["id"]), 10, "Dept current year 10"),
        ("SIJ Sick Leave", str(sick["id"]), 5, "Past-2y sick offset 5"),
        ("SIJ Departmental Leave", str(departmental["id"]), 7, "Past-2y departmental 7"),
        ("SIJ Vacation Leave", str(vacation["id"]), 10, "Vacation current year 10"),
        ("SIJ No Pay Leave", str(no_pay["id"]), 14, "No Pay remainder 14"),
    ]

    cascade_leaves = []
    cursor = start
    for type_name, type_id, days, note in segments:
        finish = add_days(cursor, days - 1)
        leave = create_leave(
            api,
            employee_id=str(employee_a["id"]),
            leave_type_id=type_id,
            start_on=cursor,
            finish_on=finish,
            description=f"BC 60-day cascade — {note}. Steven Scott (Employee A). Order ESL→Dept→sick→dept→Vac→NoPay.",
        )
        cascade_leaves.append(
            {
                "leave_type": type_name,
                "days": days,
                "start_on": cursor,
                "finish_on": finish,
                "note": note,
                "leave": leave,
            }
        )
        cursor = add_days(finish, 1)

    result["scenarios"]["extended_sick_60_day_cascade"] = {
        "employee": EMPLOYEE_A,
        "total_days": 60,
        "covered_before_no_pay": 46,
        "no_pay_days": 14,
        "segments": cascade_leaves,
        "incidences": incidences,
        "order": [
            "Current year Extended Sick 14",
            "Current year Departmental 10",
            "Past 2y sick 5",
            "Past 2y departmental 7",
            "Current year vacation 10",
            "No Pay 14",
        ],
    }

    result["api_log_tail"] = api.log[-40:]
    _write(result)

    print("=== Business Case Leave demos seeded ===")
    print("Example 3 (Charles Dec 1-18):", ex3.get("action"), ex3.get("id"))
    print("Example 4 (Clara Jun 25-26):", ex4.get("action"), ex4.get("id"))
    print("ESL early RTW:", rtw.get("action"), rtw.get("id"))
    ok_seg = sum(1 for s in cascade_leaves if s["leave"].get("action") in ("created", "skipped_exists"))
    print(f"60-day cascade segments OK: {ok_seg}/{len(cascade_leaves)}")
    return 0


def _write(result: Dict[str, Any]) -> None:
    RUN_LOG.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RUN_LOG / f"business_case_leave_seed_{ts}.json"
    latest = RUN_LOG / "business_case_leave_seed_latest.json"
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    out.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    raise SystemExit(main())
