#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STATIN hard reset — clean Time Off for 2026 start + Bernarda worked-time vacation.

1) All employees: tenure_start_date = 2026-01-01
2) SIJ Vacation allowances: carry_over = 0
3) Wipe Available balances (negative incidences) for everyone on SIJ vacation policies
4) Bernarda: new policy with based-on-time-worked allowance + Mon–Fri shifts Jan→today 2026

Usage (repo root):
  python scripts/clients/statistic-institute/reset_timeoff_clean_2026.py
"""

from __future__ import annotations

import json
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.api_client import APIClient
from ultimate_collector.core.client_config import activate_client
from ultimate_collector.core.config import Config

CLIENT_ID = "statistic-institute"
COMPANY_ID = "191864"
RUN_LOG = ROOT / "clients" / CLIENT_ID / "run_log"

SIJ_VACATION_ALLOWANCES = {
    "367078": "617645",  # 15d
    "367079": "617647",  # 20d
    "367080": "617649",  # 21d
    "367081": "617651",  # 25d
}
SIJ_POLICY_IDS = set(SIJ_VACATION_ALLOWANCES.keys())

BERNARDA_ID = "6375969"
BERNARDA_POLICY_NAME = "SIJ Vacation Worked Time"
BERNARDA_ALLOWANCE_NAME = "SIJ Vacation by hours worked"
VACATION_LEAVE_TYPE_NAME = "SIJ Vacation Leave"

START_2026 = date(2026, 1, 1)
# Shifts through end of September 2026 (worked year for demo; Oct+ empty = no more accrual)
SHIFT_END = date(2026, 9, 30)


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
            self._url(path), headers=self.client._get_headers(), params=params, timeout=self.config.TIMEOUT
        )
        try:
            body = r.json() if r.content else None
        except Exception:
            body = {"raw": r.text[:1000]}
        return r.status_code, body

    def post(self, path: str, data: Optional[Dict] = None) -> Tuple[int, Any]:
        r = self.client.session.post(
            self._url(path), headers=self.client._get_headers(), json=data, timeout=self.config.TIMEOUT
        )
        try:
            body = r.json() if r.content else None
        except Exception:
            body = {"raw": r.text[:1000]}
        self.log.append({"method": "POST", "path": path, "status": r.status_code, "req": data})
        return r.status_code, body

    def put(self, path: str, data: Optional[Dict] = None) -> Tuple[int, Any]:
        r = self.client.session.put(
            self._url(path), headers=self.client._get_headers(), json=data, timeout=self.config.TIMEOUT
        )
        try:
            body = r.json() if r.content else None
        except Exception:
            body = {"raw": r.text[:1000]}
        self.log.append({"method": "PUT", "path": path, "status": r.status_code, "req": data})
        return r.status_code, body

    def delete(self, path: str) -> Tuple[int, Any]:
        r = self.client.session.delete(
            self._url(path), headers=self.client._get_headers(), timeout=self.config.TIMEOUT
        )
        try:
            body = r.json() if r.content else None
        except Exception:
            body = {"raw": r.text[:1000]}
        self.log.append({"method": "DELETE", "path": path, "status": r.status_code})
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


def unwrap(body: Any) -> Dict:
    if not isinstance(body, dict):
        return {}
    data = body.get("data") or body
    if isinstance(data, list):
        return data[0] if data else {}
    return data if isinstance(data, dict) else {}


def find_by_name(items: List[Dict], name: str) -> Optional[Dict]:
    name_l = name.lower().strip()
    for it in items:
        if (it.get("name") or "").lower().strip() == name_l:
            return it
    return None


def working_days(start: date, end: date) -> List[date]:
    out: List[date] = []
    cur = start
    while cur <= end:
        if cur.weekday() < 5:  # Mon–Fri
            out.append(cur)
        cur += timedelta(days=1)
    return out


def main() -> int:
    activate_client(CLIENT_ID)
    Config.reload()
    api = Api()
    result: Dict[str, Any] = {
        "client": CLIENT_ID,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "tenure_updates": [],
        "allowance_carry_zero": [],
        "balance_wipes": [],
        "bernarda": {},
    }

    employees = api.list_all("employees/employees")
    active = [
        e
        for e in employees
        if not e.get("terminated") and str(e.get("company_id") or COMPANY_ID) in (COMPANY_ID, str(e.get("company_id")))
    ]
    print(f"Employees: {len(active)}")

    # ----- 1) Tenure / contract start = 2026-01-01 for EVERYONE -----
    for e in active:
        eid = str(e.get("id"))
        payload = {
            "id": eid,
            "tenure_start_date": "2026-01-01",
            "contract_version_starts_on": "2026-01-01",
            "contract_version_effective_on": "2026-01-01",
        }
        status, body = api.put(f"employees/employees/{eid}", payload)
        result["tenure_updates"].append({"id": eid, "name": e.get("full_name"), "status": status})
        if status not in (200, 201):
            print(f"  tenure FAIL {e.get('full_name')}: {status}")
        time.sleep(0.05)
    ok_t = sum(1 for x in result["tenure_updates"] if x["status"] in (200, 201))
    print(f"Tenure → 2026-01-01: {ok_t}/{len(active)}")

    # ----- 2) SIJ Vacation allowances: carry_over = 0 -----
    for policy_id, allowance_id in SIJ_VACATION_ALLOWANCES.items():
        status, body = api.put(
            f"timeoff/allowances/{allowance_id}",
            {
                "id": allowance_id,
                "carry_over_units_in_cents": 0,
                "unlimited_carry_over": False,
                "expire_in_months": 0,
            },
        )
        result["allowance_carry_zero"].append({"allowance_id": allowance_id, "policy_id": policy_id, "status": status})
        print(f"  carry_over=0 allowance {allowance_id}: {status}")

    # ----- 3) Wipe Available via large negative incidence (all SIJ assignees) -----
    assignments = [
        a for a in api.list_all("timeoff/policy_assignments") if str(a.get("timeoff_policy_id")) in SIJ_POLICY_IDS
    ]
    print(f"SIJ policy assignments to wipe: {len(assignments)}")
    for a in assignments:
        eid = str(a.get("employee_id"))
        pid = str(a.get("timeoff_policy_id"))
        aid = SIJ_VACATION_ALLOWANCES.get(pid)
        if not aid:
            continue
        # Also refresh assignment effective date to 2026
        api.put(
            f"timeoff/policy_assignments/{a.get('id')}",
            {"id": str(a.get("id")), "effective_at": "2026-01-01"},
        )
        status, body = api.post(
            "timeoff/allowance_incidences",
            {
                "employee_id": eid,
                "timeoff_allowance_id": aid,
                "days_in_cents": -10000,  # -100 days — wipe carry + accrued bank
                "effective_on": "2026-01-01",
                "target_balance": "available",
                "description": "STATIN clean start 2026 — zero carry-over / reset balance",
                "_skip_notifications": True,
            },
        )
        result["balance_wipes"].append({"employee_id": eid, "allowance_id": aid, "status": status})
        if status not in (200, 201):
            print(f"  wipe FAIL emp {eid}: {status} {body}")
        time.sleep(0.05)
    ok_w = sum(1 for x in result["balance_wipes"] if x["status"] in (200, 201))
    print(f"Balance wipes: {ok_w}/{len(result['balance_wipes'])}")

    # ----- 4) Bernarda → based on time worked -----
    leave_types = api.list_all("timeoff/leave_types")
    vacation_lt = find_by_name(leave_types, VACATION_LEAVE_TYPE_NAME)
    if not vacation_lt:
        raise RuntimeError("SIJ Vacation Leave type missing")

    policies = api.list_all("timeoff/policies")
    pol = find_by_name(policies, BERNARDA_POLICY_NAME)
    if not pol:
        status, body = api.post(
            "timeoff/policies",
            {
                "name": BERNARDA_POLICY_NAME,
                "main": False,
                "description": "Vacation accrues from recorded worked hours (clock in/out).",
                "company_id": COMPANY_ID,
            },
        )
        pol = unwrap(body)
        print(f"Created policy {BERNARDA_POLICY_NAME}: {status} id={pol.get('id')}")
    else:
        print(f"Policy exists: {pol.get('id')}")

    allowances = api.list_all("timeoff/allowances")
    botw = None
    for a in allowances:
        if a.get("name") == BERNARDA_ALLOWANCE_NAME and str(a.get("timeoff_policy_id")) == str(pol.get("id")):
            botw = a
            break

    if not botw:
        # 8 hours leave per 40 hours worked (= 1 day per full week worked)
        payload = {
            "name": BERNARDA_ALLOWANCE_NAME,
            "timeoff_policy_id": str(pol["id"]),
            "leave_type_ids": [str(vacation_lt["id"])],
            "allowance_type": "hours",
            "source_units": "by_worked_time",
            "accrued_factor_in_cents": 800,  # +8.00 hours leave
            "accrued_denominator_in_cents": 4000,  # per 40.00 hours worked
            "available_days": "generated_days",  # release as earned
            "accrued_units_availability": "current_cycle",
            "count_holiday_as_workable": False,
            "cycle_start": "jan",
            "cycle_length": 12,
            "frequency": "yearly",
            "holiday_allowance_in_cents": 0,
            "maximum_amount_in_cents": 16000,  # max 160h ≈ 20 days
            "carry_over_units_in_cents": 0,
            "expire_in_months": 0,
            "unlimited_carry_over": False,
            "unlimited_carry_over_expiration": False,
            "unlimited_holidays": False,
            "unlimited_accrued_hours": False,
            "negative_counter_type": "negative_counter_disabled",
            "proration_type": "proration_disabled",
            "pto_proratio_enabled": False,
            "rounding": "decimals",
            "tenure_periods": [],
            "tenure_periods_enabled": False,
            "send_notification": False,
        }
        status, body = api.post("timeoff/allowances", payload)
        botw = unwrap(body)
        result["bernarda"]["allowance_create"] = {"status": status, "id": botw.get("id"), "body": body if status not in (200, 201) else None}
        print(f"BOTW allowance create: {status} id={botw.get('id')}")
        if status not in (200, 201):
            print("FAIL allowance", body)
            _write(result)
            return 1
    else:
        print(f"BOTW allowance exists: {botw.get('id')}")
        api.put(
            f"timeoff/allowances/{botw['id']}",
            {"id": str(botw["id"]), "carry_over_units_in_cents": 0, "unlimited_carry_over": False},
        )

    # Move Bernarda assignment to new policy
    bernarda_assigns = [
        a
        for a in api.list_all("timeoff/policy_assignments")
        if str(a.get("employee_id")) == BERNARDA_ID
    ]
    for a in bernarda_assigns:
        # delete old SIJ assignment(s)
        if str(a.get("timeoff_policy_id")) in SIJ_POLICY_IDS or str(a.get("timeoff_policy_id")) == str(pol.get("id")):
            st, _ = api.delete(f"timeoff/policy_assignments/{a.get('id')}")
            print(f"  deleted assignment {a.get('id')} policy {a.get('timeoff_policy_id')}: {st}")

    st, body = api.post(
        "timeoff/policy_assignments",
        {
            "employee_id": BERNARDA_ID,
            "timeoff_policy_id": str(pol["id"]),
            "effective_at": "2026-01-01",
        },
    )
    result["bernarda"]["assignment"] = {"status": st, "body": unwrap(body)}
    print(f"Bernarda assigned to worked-time policy: {st}")

    # ----- 5) Shifts Mon–Fri 09:00–17:00 for Bernarda -----
    days = working_days(START_2026, SHIFT_END)
    print(f"Creating {len(days)} shifts for Bernarda ({START_2026} → {SHIFT_END})…")
    created = 0
    failed = 0
    for i, d in enumerate(days, 1):
        # Jamaica/local: use ISO with offset -05:00 (Jamaica)
        cin = f"{d.isoformat()}T09:00:00-05:00"
        cout = f"{d.isoformat()}T17:00:00-05:00"
        st, body = api.post(
            "attendance/shifts",
            {
                "employee_id": BERNARDA_ID,
                "date": d.isoformat(),
                "clock_in": cin,
                "clock_out": cout,
                "workable": True,
                "observations": "STATIN clean demo — worked day",
            },
        )
        if st in (200, 201):
            created += 1
        else:
            failed += 1
            if failed <= 5:
                print(f"  shift FAIL {d}: {st} {body}")
        if i % 40 == 0:
            print(f"  … {i}/{len(days)}")
            time.sleep(0.4)
        else:
            time.sleep(0.05)

    result["bernarda"]["shifts"] = {"created": created, "failed": failed, "planned": len(days)}
    result["bernarda"]["policy_id"] = pol.get("id")
    result["bernarda"]["allowance_id"] = botw.get("id")
    result["finished_at"] = datetime.now().isoformat(timespec="seconds")
    _write(result)

    print("=== DONE ===")
    print(f"Shifts created: {created}/{len(days)} (failed {failed})")
    print("Refresh Bernarda Time Off + Time Tracking.")
    return 0 if failed < len(days) // 2 else 1


def _write(result: Dict[str, Any]) -> None:
    RUN_LOG.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RUN_LOG / f"timeoff_reset_clean_2026_{ts}.json"
    latest = RUN_LOG / "timeoff_reset_clean_2026_latest.json"
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    out.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    raise SystemExit(main())
