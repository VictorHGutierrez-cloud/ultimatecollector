#!/usr/bin/env python3
"""Atalho na raiz: sistema financeiro completo."""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).parent / "scripts" / "entry" / "ultimate_finance_system.py"),
    run_name="__main__",
)
