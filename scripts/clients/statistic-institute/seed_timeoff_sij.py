#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed Time Off — Statistical Institute of Jamaica (Vacation Leave).
Baseado em: statistic-instituteasset/...Vacation Leave Requirements.docx
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.api_client import APIClient
from ultimate_collector.core.client_config import activate_client, ensure_client_asset_dir
from ultimate_collector.core.config import Config

CLIENT_ID = "statistic-institute"
COMPANY_ID = "191864"
RUN_LOG = ROOT / "clients" / CLIENT_ID / "run_log"
ASSET = ensure_client_asset_dir(CLIENT_ID)

# Jamaica vacation tiers: days/year -> max accumulation (3 years)
TIERS = [
    {"key": "15", "days": 15, "max_days": 45, "label": "SIJ Vacation 15 days"},
    {"key": "20", "days": 20, "max_days": 60, "label": "SIJ Vacation 20 days"},
    {"key": "21", "days": 21, "max_days": 63, "label": "SIJ Vacation 21 days (15-25y)"},
    {"key": "25", "days": 25, "max_days": 75, "label": "SIJ Vacation 25 days"},
]


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


def active_employees(api: Api) -> List[Dict]:
    emps = api.list_all("employees/employees")
    out = []
    for e in emps:
        if e.get("terminated_on"):
            continue
        # skip terminated_status if present
        if e.get("terminated") is True:
            continue
        out.append(e)
    return out


def find_by_name(items: List[Dict], name: str) -> Optional[Dict]:
    name_l = name.lower().strip()
    for it in items:
        if (it.get("name") or "").lower().strip() == name_l:
            return it
    return None


def ensure_leave_type(api: Api, name: str, color: str = "07A2AD") -> Dict:
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
        "payable": True,
        "visibility": True,
        "editable": True,
        "details_required": False,
        "attachment": False,
        "is_attachment_mandatory": False,
        "allow_endless": False,
        "half_days_units_enabled": True,
    }
    status, body = api.post("timeoff/leave_types", payload)
    if status not in (200, 201) or not isinstance(body, dict):
        raise RuntimeError(f"leave_type failed {status}: {body}")
    data = body.get("data") or body
    if isinstance(data, list):
        data = data[0]
    return data


def ensure_policy(api: Api, name: str, description: str) -> Dict:
    existing = find_by_name(api.list_all("timeoff/policies"), name)
    if existing:
        return existing
    status, body = api.post(
        "timeoff/policies",
        {
            "name": name,
            "main": False,
            "description": description,
            "company_id": COMPANY_ID,
        },
    )
    if status not in (200, 201) or not isinstance(body, dict):
        raise RuntimeError(f"policy failed {status}: {body}")
    data = body.get("data") or body
    if isinstance(data, list):
        data = data[0]
    return data


def build_allowance_payload(policy_id: str, leave_type_id: str, days: int, max_days: int, name: str) -> Dict:
    return {
        "name": name,
        "timeoff_policy_id": str(policy_id),
        "leave_type_ids": [str(leave_type_id)],
        "allowance_type": "days",
        "days_type": "working_days",
        "available_days": "generated_days_monthly_first_day",
        "accrued_units_availability": "current_cycle",
        "count_holiday_as_workable": False,  # feriados NAO descontam
        "cycle_start": "jan",
        "cycle_length": 12,
        "frequency": "yearly",
        "holiday_allowance_in_cents": cents(days),
        "maximum_amount_in_cents": cents(max_days),  # teto 3 anos
        "carry_over_units_in_cents": cents(max_days),
        "expire_in_months": 36,  # acumulo ate 3 anos
        "unlimited_carry_over": False,
        "unlimited_carry_over_expiration": False,
        "unlimited_holidays": False,
        "unlimited_accrued_hours": False,
        "negative_counter_type": "negative_counter_disabled",
        "proration_type": "proration_enabled",
        "pto_proratio_enabled": True,
        "rounding": "half_day",  # >=0.5 sobe (aprox. regra SIJ)
        "source_units": "base_units",
        "tenure_periods": [],
        "tenure_periods_enabled": False,
        "tenure_period_transition": "beginning_of_cycle",
        "send_notification": False,
    }


def ensure_allowance(api: Api, payload: Dict) -> Dict:
    allowances = api.list_all("timeoff/allowances")
    for a in allowances:
        if (
            a.get("name") == payload["name"]
            and str(a.get("timeoff_policy_id")) == str(payload["timeoff_policy_id"])
        ):
            return a
    status, body = api.post("timeoff/allowances", payload)
    if status not in (200, 201) or not isinstance(body, dict):
        raise RuntimeError(f"allowance failed {status}: {body}")
    data = body.get("data") or body
    if isinstance(data, list):
        data = data[0]
    return data


def ensure_assignment(api: Api, policy_id: str, employee_id: str, effective_at: str) -> Dict:
    assignments = api.list_all("timeoff/policy_assignments")
    for a in assignments:
        if str(a.get("employee_id")) == str(employee_id) and str(a.get("timeoff_policy_id")) == str(policy_id):
            return a
    status, body = api.post(
        "timeoff/policy_assignments",
        {
            "timeoff_policy_id": str(policy_id),
            "employee_id": str(employee_id),
            "effective_at": effective_at,
        },
    )
    if status not in (200, 201) or not isinstance(body, dict):
        # pode falhar se já tiver outra policy — registra e segue
        return {"error": True, "status": status, "body": body, "employee_id": employee_id}
    data = body.get("data") or body
    if isinstance(data, list):
        data = data[0]
    return data


def create_incidence(api: Api, employee_id: str, allowance_id: str, days: float, description: str) -> Dict:
    payload = {
        "employee_id": str(employee_id),
        "timeoff_allowance_id": str(allowance_id),
        "days_in_cents": cents(days),
        "effective_on": date.today().isoformat(),
        "target_balance": "available",
        "description": description,
        "_skip_notifications": True,
    }
    status, body = api.post("timeoff/allowance_incidences", payload)
    return {"status": status, "body": body, "req": payload}


def create_leave(api: Api, employee_id: str, leave_type_id: str, start: str, finish: str, description: str) -> Dict:
    payload = {
        "employee_id": str(employee_id),
        "leave_type_id": str(leave_type_id),
        "start_on": start,
        "finish_on": finish,
        "description": description,
    }
    status, body = api.post("timeoff/leaves", payload)
    leave = None
    if isinstance(body, dict):
        leave = body.get("data") or body
        if isinstance(leave, list):
            leave = leave[0]
    # try approve
    if status in (200, 201) and leave and leave.get("id"):
        api.post("timeoff/leaves/approve", {"id": str(leave["id"])})
    return {"status": status, "body": body, "req": payload}


def extra_leave_types(api: Api) -> List[Dict]:
    """Tipos mencionados no doc (ausências que pausam accrual >14 dias)."""
    specs = [
        ("SIJ Sick Leave", "EF4444"),
        ("SIJ Maternity Leave", "EC4899"),
        ("SIJ Study Leave", "8B5CF6"),
        ("SIJ Compassionate Leave", "F59E0B"),
        ("SIJ Special Leave", "64748B"),
    ]
    created = []
    for name, color in specs:
        try:
            created.append(ensure_leave_type(api, name, color))
        except Exception as exc:
            created.append({"name": name, "error": str(exc)})
    return created


def main() -> int:
    activate_client(CLIENT_ID)
    Config.reload()
    api = Api()

    result: Dict[str, Any] = {
        "client": CLIENT_ID,
        "company_id": COMPANY_ID,
        "started_at": date.today().isoformat(),
        "actions": [],
    }

    print("=== SIJ Time Off Seed ===")
    print(f"Company {COMPANY_ID}")

    # 1) Leave type Vacation
    vacation = ensure_leave_type(api, "SIJ Vacation Leave", "07A2AD")
    result["vacation_leave_type"] = {"id": vacation.get("id"), "name": vacation.get("name")}
    print("Leave type:", vacation.get("id"), vacation.get("name"))

    # 2) Extra leave types from doc
    result["extra_leave_types"] = [
        {"id": x.get("id"), "name": x.get("name"), "error": x.get("error")} for x in extra_leave_types(api)
    ]

    # 3) Policies + allowances
    tier_map = {}
    for tier in TIERS:
        policy = ensure_policy(
            api,
            tier["label"],
            (
                f"Statistical Institute of Jamaica — Vacation Leave {tier['days']} working days/year. "
                f"Max accumulation 3 years = {tier['max_days']} days. "
                "Weekends/public holidays excluded. Accrual prorated; stops at max balance."
            ),
        )
        allowance = ensure_allowance(
            api,
            build_allowance_payload(
                policy["id"],
                vacation["id"],
                tier["days"],
                tier["max_days"],
                f"SIJ Vacation Allowance {tier['days']}d",
            ),
        )
        tier_map[tier["key"]] = {
            "policy_id": policy.get("id"),
            "allowance_id": allowance.get("id"),
            "days": tier["days"],
            "max_days": tier["max_days"],
        }
        print(
            f"Tier {tier['key']}: policy={policy.get('id')} allowance={allowance.get('id')} "
            f"({tier['days']}/{tier['max_days']})"
        )
    result["tiers"] = tier_map

    # 4) Assign policies to active employees (4 buckets)
    emps = active_employees(api)
    emps_sorted = sorted(emps, key=lambda e: str(e.get("id")))
    keys = ["15", "20", "21", "25"]
    assignments = []
    for i, emp in enumerate(emps_sorted):
        key = keys[i % 4]
        policy_id = tier_map[key]["policy_id"]
        # use existing effective_at from current assignment if any, else today-1y
        effective = (date.today() - timedelta(days=365)).isoformat()
        for a in api.list_all("timeoff/policy_assignments"):
            if str(a.get("employee_id")) == str(emp.get("id")) and a.get("effective_at"):
                effective = a["effective_at"]
                break
        row = ensure_assignment(api, policy_id, emp["id"], effective)
        assignments.append(
            {
                "employee_id": emp.get("id"),
                "name": f"{emp.get('first_name')} {emp.get('last_name')}",
                "tier": key,
                "result": {
                    "id": row.get("id"),
                    "error": row.get("error"),
                    "status": row.get("status"),
                },
            }
        )
    result["assignments"] = assignments
    print(f"Assignments attempted: {len(assignments)}")

    # 5) Demo balances (incidences) — exemplo do doc (~9 dias) + outros
    incidences = []
    if emps_sorted:
        # exemplo doc: 9 days prorated
        e0 = emps_sorted[0]
        incidences.append(
            create_incidence(
                api,
                e0["id"],
                tier_map["15"]["allowance_id"],
                9.0,
                "SIJ demo: prorated first year (doc example ~9 days after rounding)",
            )
        )
        if len(emps_sorted) > 1:
            e1 = emps_sorted[1]
            incidences.append(
                create_incidence(
                    api,
                    e1["id"],
                    tier_map["20"]["allowance_id"],
                    20.0,
                    "SIJ demo: full year entitlement 20 days",
                )
            )
        if len(emps_sorted) > 2:
            e2 = emps_sorted[2]
            incidences.append(
                create_incidence(
                    api,
                    e2["id"],
                    tier_map["21"]["allowance_id"],
                    40.0,
                    "SIJ demo: accumulated balance toward 3-year cap (63)",
                )
            )
        if len(emps_sorted) > 3:
            e3 = emps_sorted[3]
            incidences.append(
                create_incidence(
                    api,
                    e3["id"],
                    tier_map["25"]["allowance_id"],
                    50.0,
                    "SIJ demo: accumulated balance toward 3-year cap (75)",
                )
            )
    result["incidences"] = [
        {"status": x.get("status"), "employee_id": x.get("req", {}).get("employee_id"), "days": (x.get("req") or {}).get("days_in_cents")}
        for x in incidences
    ]

    # 6) Sample vacation leaves (next weeks)
    leaves = []
    today = date.today()
    # next Monday-ish window
    start1 = today + timedelta(days=(7 - today.weekday()) % 7 or 7)
    finish1 = start1 + timedelta(days=4)  # Mon-Fri week
    start2 = start1 + timedelta(days=14)
    finish2 = start2 + timedelta(days=2)
    start3 = start1 + timedelta(days=28)
    finish3 = start3 + timedelta(days=9)

    samples = [
        (0, start1, finish1, "SIJ Vacation — family holiday (demo)"),
        (1, start2, finish2, "SIJ Vacation — short break (demo)"),
        (2, start3, finish3, "SIJ Vacation — extended leave (demo)"),
    ]
    for idx, start, finish, desc in samples:
        if idx >= len(emps_sorted):
            break
        emp = emps_sorted[idx]
        leaves.append(
            create_leave(
                api,
                emp["id"],
                vacation["id"],
                start.isoformat(),
                finish.isoformat(),
                desc,
            )
        )
    result["leaves"] = [
        {
            "status": x.get("status"),
            "employee_id": (x.get("req") or {}).get("employee_id"),
            "start_on": (x.get("req") or {}).get("start_on"),
            "finish_on": (x.get("req") or {}).get("finish_on"),
        }
        for x in leaves
    ]

    result["api_log_tail"] = api.log[-30:]
    RUN_LOG.mkdir(parents=True, exist_ok=True)
    out = RUN_LOG / f"timeoff_seed_{date.today().strftime('%Y%m%d')}.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = ASSET / "TIMEOFF_SETUP_SUMMARY.md"
    summary.write_text(
        "\n".join(
            [
                "# SIJ Vacation Leave — Setup aplicado",
                "",
                "Fonte: Statistical Institute of Jamaica Vacation Leave Requirements",
                "",
                "## O que foi configurado",
                "",
                f"- Leave type: **SIJ Vacation Leave** (id `{vacation.get('id')}`)",
                "- Leave types extras: Sick, Maternity, Study, Compassionate, Special",
                "- Policies + allowances:",
                "  - 15 dias/ano — teto 45 (3 anos)",
                "  - 20 dias/ano — teto 60",
                "  - 21 dias/ano — teto 63 (faixa 15–25 anos de serviço)",
                "  - 25 dias/ano — teto 75",
                "- Dias úteis (seg–sex); feriados **não** contam como workable (`count_holiday_as_workable=false`)",
                "- Prorata ligado; rounding half_day; carry-over até 36 meses",
                f"- Assignments em {len(emps_sorted)} colaboradores ativos (rodízio 15/20/21/25)",
                "- Saldos demo (incidences) + leaves de exemplo",
                "",
                "## Limitações da Factorial vs documento",
                "",
                "- Fórmula exata `(dias/365)×taxa` e pausa de accrual após 14 dias: aproximadas pelo motor da Factorial",
                "- Recall credit: não automatizado pela API — regra documentada para demo verbal",
                "",
                f"Log técnico: `{out.relative_to(ROOT)}`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out}")
    print(f"Wrote {summary}")
    ok_leaves = sum(1 for x in leaves if x.get("status") in (200, 201))
    ok_inc = sum(1 for x in incidences if x.get("status") in (200, 201))
    print(f"Leaves OK: {ok_leaves}/{len(leaves)} | Incidences OK: {ok_inc}/{len(incidences)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
