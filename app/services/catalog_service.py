#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Serviço de leitura/gravação do catalog.json de demo."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ultimate_collector.core.client_config import load_profile


class CatalogService:
    @staticmethod
    def catalog_path(client_id: str) -> Path:
        profile = load_profile(client_id)
        if not profile.catalog_path:
            raise FileNotFoundError(f"Cliente '{client_id}' nao tem catalog configurado.")
        return profile.catalog_path

    @staticmethod
    def load(client_id: str) -> Dict[str, Any]:
        path = CatalogService.catalog_path(client_id)
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def validate(catalog: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        if "company_id" not in catalog:
            errors.append("Campo obrigatorio ausente: company_id")
        if "teams" not in catalog or not isinstance(catalog.get("teams"), list):
            errors.append("Campo obrigatorio ausente ou invalido: teams")
        if "cast" not in catalog or not isinstance(catalog.get("cast"), list):
            errors.append("Campo obrigatorio ausente ou invalido: cast")
        return (len(errors) == 0, errors)

    @staticmethod
    def save(client_id: str, catalog: Dict[str, Any]) -> Path:
        ok, errors = CatalogService.validate(catalog)
        if not ok:
            raise ValueError("; ".join(errors))

        path = CatalogService.catalog_path(client_id)
        backup = path.with_suffix(path.suffix + ".bak")
        if path.exists():
            shutil.copy2(path, backup)
        path.write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return path
