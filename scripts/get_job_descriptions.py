#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baixa Job Descriptions (Job Catalog - Roles) da API Factorial
- Usa credenciais do arquivo config_unificado.env
- Salva em data/reports/job_catalog_roles.{json,csv}

Como usar:
  1) Configure BASE_URL, AUTH_TYPE e credenciais no config_unificado.env
  2) python scripts/get_job_descriptions.py
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
import pandas as pd

# Garantir import do core
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ultimate_collector.core.api_client import APIClient  # noqa: E402

OUTPUT_DIR = PROJECT_ROOT / "data" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_PREFIX = "api/2026-07-01/resources"  # manter versão usada no projeto
ENDPOINT = f"{API_PREFIX}/job_catalog/roles"


def fetch_all_roles(client: APIClient):
    """Busca todos os roles com paginação (tenta page/limit e cursor)."""
    all_records = []

    # 1) Tentativa por page/limit
    page = 1
    limit = 100
    while True:
        try:
            resp = client.get(ENDPOINT, params={"limit": limit, "page": page})
        except Exception:
            resp = None
        if not resp or "data" not in resp:
            break
        data = resp.get("data") or []
        if not data:
            break
        all_records.extend(data)
        if len(data) < limit:
            break
        page += 1
        if page > 100:
            break

    # 2) Se não retornou nada, tentar por cursor
    if not all_records:
        cursor = None
        while True:
            params = {"limit": limit}
            if cursor:
                params["cursor"] = cursor
            try:
                resp = client.get(ENDPOINT, params=params)
            except Exception:
                resp = None
            if not resp or "data" not in resp:
                break
            data = resp.get("data") or []
            all_records.extend(data)
            meta = resp.get("meta", {})
            if not meta or not meta.get("has_next_page"):
                break
            cursor = meta.get("end_cursor")
            if not cursor:
                break

    return all_records


def save_outputs(records):
    """Salva JSON e CSV em data/reports/"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = OUTPUT_DIR / f"job_catalog_roles_{timestamp}.json"
    csv_path = OUTPUT_DIR / f"job_catalog_roles_{timestamp}.csv"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    if records:
        df = pd.json_normalize(records)
        df.to_csv(csv_path, index=False, encoding="utf-8")
        cols_preview = ", ".join(df.columns[:10])
        print(f"✅ CSV salvo: {csv_path} (colunas: {cols_preview}{'...' if len(df.columns) > 10 else ''})")
    else:
        print("⚠️ Nenhum registro para salvar em CSV.")

    print(f"✅ JSON salvo: {json_path}")


def main():
    print("🗂️  Baixando Job Descriptions (Job Catalog - Roles) da API Factorial...")
    print(f"🌐 Endpoint: {ENDPOINT}")

    client = APIClient()
    ok = client.test_connection()
    if not ok:
        print("❌ Não foi possível validar a conexão. Verifique credenciais no config_unificado.env")
        return

    records = fetch_all_roles(client)
    print(f"📊 Total de roles coletados: {len(records)}")

    save_outputs(records)
    client.close()

    print("✅ Concluído.")


if __name__ == "__main__":
    main()
