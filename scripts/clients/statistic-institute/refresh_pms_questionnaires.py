#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refresh STATIN review questionnaires (no duplicated competency questions)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("statistic-institute")

sys.path.insert(0, str(ROOT / "clients" / "statistic-institute"))
sys.path.insert(0, str(ROOT / "scripts" / "clients" / "statistic-institute"))

from api_helpers import StatinApi, load_catalog  # noqa: E402
import seed_pms_statin as seed  # noqa: E402

PROCESSES = [
    ("year_end", "303497"),
    ("coaching", "303498"),
    ("iwp", "303499"),
]


def main() -> int:
    api = StatinApi()
    catalog = load_catalog()
    for key, pid in PROCESSES:
        questionnaire = seed.build_statin_questionnaire(catalog, key)
        titles = [s.get("section_title") for s in questionnaire if s.get("type") == "section"]
        print(key, "sections:", titles)
        for strategy in ("self", "manager"):
            st, body = api.post(
                "performance/review_questionnaire_by_strategies/update_questionnaire_for_strategy",
                {
                    "performance_review_process_id": pid,
                    "strategy": strategy,
                    "questionnaire_content": questionnaire,
                },
            )
            print(f"  {strategy}: {st}")
            if st not in (200, 201):
                print("   ", str(body)[:300])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
