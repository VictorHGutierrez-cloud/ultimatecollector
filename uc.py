#!/usr/bin/env python3
"""
Atalho principal na raiz do projeto.

Exemplos:
  python uc.py menu
  python uc.py clients list
  python uc.py --client africa verify-token
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ultimate_collector.cli import main

raise SystemExit(main())
