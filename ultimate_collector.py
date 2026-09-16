#!/usr/bin/env python3
"""Atalho: menu sandbox (escolhe cliente + acoes)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ultimate_collector.cli import main

raise SystemExit(main(["menu"]))
