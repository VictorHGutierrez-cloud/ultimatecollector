#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point do app desktop Ultimate Collector.

Uso:
  python app/main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    from app.ui.app_window import AppWindow

    app = AppWindow()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
