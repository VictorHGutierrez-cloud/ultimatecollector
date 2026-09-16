#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helpers HTTP para scripts da demo SZV."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ultimate_collector.core.api_client import APIClient  # noqa: E402
from ultimate_collector.core.config import Config  # noqa: E402

DEMO_DIR = Path(__file__).resolve().parent
CATALOG_PATH = DEMO_DIR / "catalog.json"
RUN_LOG_DIR = DEMO_DIR / "run_log"


class SzvApi:
    """Cliente com retorno de status/erro para seed/inventário."""

    def __init__(self) -> None:
        self.config = Config()
        self.client = APIClient()
        self.version = self.config.API_VERSION or "2026-07-01"
        self.prefix = f"api/{self.version}/resources"

    def resource(self, path: str) -> str:
        return f"{self.prefix}/{path.lstrip('/')}"

    def get(self, path: str, params: Optional[Dict] = None) -> Tuple[int, Any]:
        url = self.client._build_url(self.resource(path))
        headers = self.client._get_headers()
        response = self.client.session.get(
            url, headers=headers, params=params, timeout=self.config.TIMEOUT
        )
        try:
            body = response.json() if response.content else None
        except Exception:
            body = {"raw": response.text[:1000]}
        return response.status_code, body

    def post(self, path: str, data: Optional[Dict] = None) -> Tuple[int, Any]:
        url = self.client._build_url(self.resource(path))
        headers = self.client._get_headers()
        response = self.client.session.post(
            url, headers=headers, json=data, timeout=self.config.TIMEOUT
        )
        try:
            body = response.json() if response.content else None
        except Exception:
            body = {"raw": response.text[:1000]}
        return response.status_code, body

    def put(self, path: str, data: Optional[Dict] = None) -> Tuple[int, Any]:
        url = self.client._build_url(self.resource(path))
        headers = self.client._get_headers()
        response = self.client.session.put(
            url, headers=headers, json=data, timeout=self.config.TIMEOUT
        )
        try:
            body = response.json() if response.content else None
        except Exception:
            body = {"raw": response.text[:1000]}
        return response.status_code, body

    def list_all(self, path: str, params: Optional[Dict] = None, max_pages: int = 50) -> List[Dict]:
        items: List[Dict] = []
        page = 1
        base_params = dict(params or {})
        while page <= max_pages:
            query = {**base_params, "limit": base_params.get("limit", 100), "page": page}
            status, body = self.get(path, params=query)
            if status == 404:
                return items
            if status != 200 or not isinstance(body, dict):
                break
            data = body.get("data") or []
            if isinstance(data, dict):
                data = [data]
            items.extend(data)
            meta = body.get("meta") or {}
            has_next = bool(meta.get("has_next_page") or meta.get("next_page"))
            if not data or (not has_next and len(data) < int(query["limit"])):
                break
            if not has_next and len(data) < int(query["limit"]):
                break
            if len(data) < int(query["limit"]):
                break
            page += 1
        return items


def load_catalog() -> Dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_name(value: Optional[str]) -> str:
    return " ".join((value or "").strip().lower().split())
