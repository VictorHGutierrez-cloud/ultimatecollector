#!/usr/bin/env python3
"""Atalho na raiz: menu do Ultimate Sender (OAS)."""
import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).parent / "scripts" / "entry" / "ultimate_sender.py"),
    run_name="__main__",
)
