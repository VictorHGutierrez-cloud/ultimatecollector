#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Caminhos centralizados do projeto (compatível com PyInstaller)."""

import sys
from pathlib import Path


def _resolve_project_root() -> Path:
    if getattr(sys, "frozen", False):
        # Pasta do .exe (onedir: ao lado do executável)
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = _resolve_project_root()
CLIENTS_DIR = PROJECT_ROOT / "clients"
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"
