#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build STATIN / GoJ competency import workbooks (read catalog + live Job Catalog).

Outputs (for manual Factorial import — API cannot create competencies):
  1) competenciesimport.xlsx              — CREATE competencies + Band 1-6 levels
  2) competencies_competency_assignment_importer.xlsx — ASSIGN to Job Catalog nodes

Import order in Factorial UI:
  A) Import competenciesimport.xlsx
  B) Re-export assignment template OR use the generated assignment file
  C) Import competencies_competency_assignment_importer.xlsx
"""

from __future__ import annotations

import json
import string
import sys
from copy import copy
from pathlib import Path
from typing import Any, Dict, List

import openpyxl
from openpyxl.workbook import Workbook

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("statistic-institute")

STATIN_DIR = ROOT / "clients" / "statistic-institute"
sys.path.insert(0, str(STATIN_DIR))
from api_helpers import StatinApi, load_catalog  # noqa: E402

ASSET = STATIN_DIR / "statistic-instituteasset"
RUN_LOG = STATIN_DIR / "run_log"
TEMPLATE_CREATE = ROOT / "clients" / "szv" / "competenciesimport.xlsx"
TEMPLATE_ASSIGN = Path(
    r"c:\Users\victo\Downloads\competencies_competency_assignment_importer (1).xlsx"
)
if not TEMPLATE_ASSIGN.exists():
    TEMPLATE_ASSIGN = ROOT / "clients" / "szv" / "competencies_competency_assignment_importer.xlsx"

# GoJ Core Competency Framework (MIND / MoFPS, March 2024) — 9 cores in 3 clusters
GOJ_CORE = [
    {
        "name": "GoJ Core: Communicating Effectively",
        "group": "GoJ Inspiring Cluster",
        "description": (
            "Engage with citizens and colleagues, actively listen, and respond with respect and honesty. "
            "Includes verbal/written communication, presentation, feedback, facilitation, meetings, and IT skills."
        ),
    },
    {
        "name": "GoJ Core: Working Collaboratively",
        "group": "GoJ Inspiring Cluster",
        "description": (
            "Work inclusively with others to achieve shared outcomes; build trust, share resources, "
            "and resolve conflict constructively."
        ),
    },
    {
        "name": "GoJ Core: Developing Capability",
        "group": "GoJ Inspiring Cluster",
        "description": (
            "Build own and others' capability through learning, coaching, knowledge sharing, "
            "and creating opportunities to develop talent for the public service."
        ),
    },
    {
        "name": "GoJ Core: Seeing the Big Picture",
        "group": "GoJ Future-Oriented Cluster",
        "description": (
            "Anticipate future developments and take account of wider considerations to develop "
            "long-term strategies that add value for customers and citizens."
        ),
    },
    {
        "name": "GoJ Core: Driving Continuous Change and Improvements",
        "group": "GoJ Future-Oriented Cluster",
        "description": (
            "Seek opportunities to create effective and sustainable change; drive continuous "
            "improvement and innovation in service delivery."
        ),
    },
    {
        "name": "GoJ Core: Making Effective Decisions",
        "group": "GoJ Future-Oriented Cluster",
        "description": (
            "Make clear, timely decisions using evidence, considering risk and impact on citizens, "
            "and taking accountability for outcomes."
        ),
    },
    {
        "name": "GoJ Core: Demonstrating a Commercial and Business Mindset",
        "group": "GoJ Performance Cluster",
        "description": (
            "Apply a business mindset to public service delivery; understand markets, costs, "
            "and opportunities to improve efficiency and outcomes."
        ),
    },
    {
        "name": "GoJ Core: Ensuring Value for Taxpayers Money",
        "group": "GoJ Performance Cluster",
        "description": (
            "Understand and apply policies and financial processes; collaborate across boundaries "
            "so the Public Service achieves strategic outcomes within available resources."
        ),
    },
    {
        "name": "GoJ Core: Providing a Quality Service",
        "group": "GoJ Performance Cluster",
        "description": (
            "Provide timely, high-quality services that make a difference for citizens; "
            "sustain a quality culture using feedback and continuous improvement."
        ),
    },
]

# Technical competencies used in STATIN PMS sample (Information / Office pathway)
STATIN_TECHNICAL = [
    {
        "name": "STATIN Technical: Information Management",
        "group": "STATIN Technical Competencies",
        "description": (
            "Apply records, information management and data protection standards; handle sensitive "
            "information with judgement and confidentiality (aligned to GoJ Information Professionals pathway)."
        ),
    },
    {
        "name": "STATIN Technical: Communication and Service Delivery",
        "group": "STATIN Technical Competencies",
        "description": (
            "Use organisational knowledge to serve internal and external clients promptly and politely; "
            "communicate and enforce policies under pressure."
        ),
    },
]

# Factorial competency levels mapped to GoJ Professional Bands 1-6
BANDS = [
    ("Band 1", "Entry / foundational behaviours for the competency."),
    ("Band 2", "Applies competency with guidance; growing consistency."),
    ("Band 3", "Solid, independent demonstration in own role."),
    ("Band 4", "Advanced application; influences team practice."),
    ("Band 5", "Expert; shapes standards across unit/division."),
    ("Band 6", "Strategic mastery; organisation-wide leadership of the competency."),
]

# Default assignment level for demo roles
DEFAULT_BAND = "Band 3"


def list_all_nodes(api: StatinApi, node_type: str) -> List[dict]:
    seen: Dict[str, dict] = {}
    for q in list(string.ascii_lowercase) + [" ", "-", "&"]:
        page = 1
        while page <= 30:
            st, body = api.get(
                "job_catalog/tree_nodes",
                params={"node_type": node_type, "search": q, "limit": 100, "page": page},
            )
            if st != 200 or not isinstance(body, dict):
                break
            data = body.get("data") or []
            for n in data:
                if n.get("uuid"):
                    seen[str(n["uuid"])] = n
            meta = body.get("meta") or {}
            if not data or not meta.get("has_next_page"):
                break
            page += 1
    return list(seen.values())


def build_create_workbook(path: Path) -> None:
    wb = openpyxl.load_workbook(TEMPLATE_CREATE)
    ws = wb["factorial"]
    # clear data rows
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)

    comps = GOJ_CORE + STATIN_TECHNICAL
    for r_idx, comp in enumerate(comps, start=2):
        ws.cell(r_idx, 1, comp["name"])
        ws.cell(r_idx, 2, comp["description"])
        ws.cell(r_idx, 3, comp["group"])
        col = 4
        for band_name, band_desc in BANDS:
            ws.cell(r_idx, col, band_name)
            ws.cell(r_idx, col + 1, band_desc)
            col += 2

    if "Lang" in wb.sheetnames:
        wb["Lang"]["A1"] = "en-US"
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    print(f"Wrote CREATE importer: {path} ({len(comps)} competencies)")


def build_assignment_workbook(path: Path, inventory: Dict[str, List[dict]]) -> None:
    """Rewrite assignment file using live STATIN tree + GoJ competency names."""
    families = {n["uuid"]: n for n in inventory["jobcatalog_treefamily"]}
    functions = {n["uuid"]: n for n in inventory["jobcatalog_treefunction"]}
    roles = {n["uuid"]: n for n in inventory["jobcatalog_treerole"]}
    levels = {n["uuid"]: n for n in inventory["jobcatalog_treelevel"]}

    # Build hierarchy rows: family, function, role, level (like Factorial export)
    rows: List[List[Any]] = []
    header = [
        "Family",
        "Function",
        "Role",
        "Level",
        "Node UUID",
    ]
    # up to 11 competency slots (9 core + 2 technical)
    max_c = 11
    for i in range(1, max_c + 1):
        header.extend([f"Competency {i}", f"Competency level {i}"])

    all_comps = GOJ_CORE + STATIN_TECHNICAL
    assign_names = [c["name"] for c in all_comps]

    def family_name(uuid: str) -> str:
        return (families.get(uuid) or {}).get("name") or ""

    def function_name(uuid: str) -> str:
        return (functions.get(uuid) or {}).get("name") or ""

    def role_name(uuid: str) -> str:
        return (roles.get(uuid) or {}).get("name") or ""

    # Sort for stable output
    for fam in sorted(families.values(), key=lambda x: x.get("name") or ""):
        rows.append([fam.get("name"), "", "", "", fam["uuid"]] + [""] * (max_c * 2))
        fam_funcs = [
            f for f in functions.values() if f.get("ancestor_uuid") == fam["uuid"]
        ]
        for func in sorted(fam_funcs, key=lambda x: x.get("name") or ""):
            rows.append(
                [fam.get("name"), func.get("name"), "", "", func["uuid"]]
                + [""] * (max_c * 2)
            )
            func_roles = [
                r for r in roles.values() if r.get("ancestor_uuid") == func["uuid"]
            ]
            for role in sorted(func_roles, key=lambda x: x.get("name") or ""):
                rows.append(
                    [
                        fam.get("name"),
                        func.get("name"),
                        role.get("name"),
                        "",
                        role["uuid"],
                    ]
                    + [""] * (max_c * 2)
                )
                role_levels = [
                    lv for lv in levels.values() if lv.get("ancestor_uuid") == role["uuid"]
                ]
                for lv in sorted(role_levels, key=lambda x: x.get("name") or ""):
                    # Assign GoJ competencies on LEVEL nodes (Factorial expects this)
                    cells = [
                        fam.get("name"),
                        func.get("name"),
                        role.get("name"),
                        lv.get("name"),
                        lv["uuid"],
                    ]
                    for name in assign_names:
                        cells.extend([name, DEFAULT_BAND])
                    # pad if fewer than max_c
                    while len(cells) < 5 + max_c * 2:
                        cells.append("")
                    rows.append(cells)

    wb = Workbook()
    ws = wb.active
    ws.title = "sheet-1"
    ws.append(header)
    for row in rows:
        ws.append(row)

    # options sheet: competency x level pairs for dropdowns
    opt = wb.create_sheet("options")
    opt_header = []
    for i in range(1, max_c + 1):
        opt_header.extend([f"Competency {i}", f"Competency level {i}"])
    opt.append(opt_header)
    # one row per competency; repeat across columns like Factorial export style
    for name in assign_names:
        for band_name, _ in BANDS:
            line = []
            for _ in range(max_c):
                line.extend([name, band_name])
            opt.append(line)

    # Also keep a README sheet
    readme = wb.create_sheet("README_STATIN", 0)
    readme["A1"] = "STATIN / GoJ competency ASSIGNMENT importer"
    readme["A2"] = "Company: 191864 Statistical Institute of Jamaica"
    readme["A3"] = "STEP 1: Import competenciesimport.xlsx FIRST (creates GoJ Core + STATIN Technical)."
    readme["A4"] = "STEP 2: Import this file (assigns competencies to Job Catalog LEVEL nodes)."
    readme["A5"] = f"Default competency level used on all level nodes: {DEFAULT_BAND}"
    readme["A6"] = "Node UUIDs were pulled live from this tenant's Job Catalog."
    readme["A7"] = "After import: open a Performance review with competencies_assessments enabled."
    readme["A8"] = "Employees need a Job Catalog role/level on their profile for native assessment to show."

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    print(f"Wrote ASSIGNMENT importer: {path} ({len(rows)} tree rows)")


def write_instructions(path: Path) -> None:
    text = """# STATIN / GoJ Competencies — Import instructions

## Why Excel?
Factorial public API cannot create competencies (Job Catalog write endpoints are GET-only).
Import is the supported way.

## Files
1. `competenciesimport.xlsx` — **create** 9 GoJ Core + 2 STATIN Technical competencies (Bands 1–6)
2. `competencies_competency_assignment_importer.xlsx` — **assign** those competencies to every Job Catalog **Level** node

## Import order (Factorial UI)
1. Go to **Competencies** (or Job Catalog → Competencies) → **Import**
2. Upload **`competenciesimport.xlsx`** first and confirm the 11 competencies appear
3. Upload **`competencies_competency_assignment_importer.xlsx`**
4. Spot-check a Level (e.g. Administrative Mid, People Director I) — should list GoJ Core:* competencies at **Band 3**

## Then in Performance
- Reviews already have `competencies_assessments_enabled`
- Questionnaire competency *questions* were removed so you do not double-rate
- If the native block is still empty for a person: assign that employee a Job Catalog role/level in their profile

## GoJ Core (9)
Inspiring: Communicating Effectively · Working Collaboratively · Developing Capability  
Future-Oriented: Seeing the Big Picture · Driving Continuous Change and Improvements · Making Effective Decisions  
Performance: Demonstrating a Commercial and Business Mindset · Ensuring Value for Taxpayers Money · Providing a Quality Service  

## STATIN Technical (2)
Information Management · Communication and Service Delivery  

Source: GOJ Competency Model (MIND/MoFPS, March 2024) + STATIN PMS guidelines sample.
"""
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path}")


def main() -> int:
    api = StatinApi()
    inventory = {
        "jobcatalog_treefamily": list_all_nodes(api, "jobcatalog_treefamily"),
        "jobcatalog_treefunction": list_all_nodes(api, "jobcatalog_treefunction"),
        "jobcatalog_treerole": list_all_nodes(api, "jobcatalog_treerole"),
        "jobcatalog_treelevel": list_all_nodes(api, "jobcatalog_treelevel"),
    }
    RUN_LOG.mkdir(parents=True, exist_ok=True)
    ASSET.mkdir(parents=True, exist_ok=True)
    (RUN_LOG / "job_catalog_inventory.json").write_text(
        json.dumps(
            {k: [{"uuid": n.get("uuid"), "name": n.get("name"), "ancestor_uuid": n.get("ancestor_uuid")} for n in v]
             for k, v in inventory.items()},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    for n, c in [(k, len(v)) for k, v in inventory.items()]:
        print(f"inventory {n}: {c}")

    create_path = ASSET / "competenciesimport.xlsx"
    assign_path = ASSET / "competencies_competency_assignment_importer.xlsx"
    build_create_workbook(create_path)
    build_assignment_workbook(assign_path, inventory)
    # also copy to Downloads-friendly run_log
    build_create_workbook(RUN_LOG / "competenciesimport.xlsx")
    build_assignment_workbook(RUN_LOG / "competencies_competency_assignment_importer.xlsx", inventory)
    write_instructions(ASSET / "COMPETENCIES_IMPORT_README.md")

    # update catalog competency lists for docs/seed alignment
    catalog = load_catalog()
    catalog["core_competencies"] = [c["name"] for c in GOJ_CORE]
    catalog["technical_competencies"] = [c["name"] for c in STATIN_TECHNICAL]
    catalog["competency_bands"] = [b[0] for b in BANDS]
    (STATIN_DIR / "catalog.json").write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("Updated catalog.json competency names")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
