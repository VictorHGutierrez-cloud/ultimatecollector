#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload de documentos demo Kibanda (company 191232).

Uso:
  python scripts/clients/glovo-sibasi/kibanda_upload_documents.py --list
  python scripts/clients/glovo-sibasi/kibanda_upload_documents.py --apply
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("glovo-sibasi")

CLIENT_DIR = ROOT / "clients" / "glovo-sibasi"
sys.path.insert(0, str(CLIENT_DIR))
from api_helpers import ASSET_DIR, RUN_LOG_DIR, KibandaApi, normalize_name, save_json  # noqa: E402

COMPANY_ID = "191232"

DEFAULT_UPLOADS = [
    {
        "path": ASSET_DIR / "Kibanda_Employee_Handbook_Demo.pdf",
        "filename": "Kibanda_Employee_Handbook_Demo.pdf",
        "space": "company_internal",
    },
    {
        "path": ASSET_DIR / "Kibanda_Onboarding_Checklist_Tom_Sang.pdf",
        "filename": "Kibanda_Onboarding_Checklist_Tom_Sang.pdf",
        "space": "company_internal",
    },
    {
        "path": ASSET_DIR / "Kibanda_Employment_Contract_Sample_Brian_Wafula.pdf",
        "filename": "Kibanda_Employment_Contract_Sample_Brian_Wafula.pdf",
        "space": "company_internal",
    },
]


def author_access_id(api: KibandaApi) -> str:
    for name in ("Brenda Wanjiru", "Esther Nyambura"):
        for emp in api.list_all("employees/employees"):
            full = emp.get("full_name") or f"{emp.get('first_name')} {emp.get('last_name')}"
            if normalize_name(full) == normalize_name(name) and emp.get("access_id"):
                return str(emp["access_id"])
    for emp in api.list_all("employees/employees"):
        if emp.get("access_id"):
            return str(emp["access_id"])
    raise RuntimeError("No employee access_id found for document author")


def upload_file(
    api: KibandaApi,
    file_path: Path,
    *,
    filename: Optional[str] = None,
    space: str = "company_internal",
) -> Tuple[int, Any]:
    if not file_path.exists():
        return 404, {"error": f"File not found: {file_path}"}

    url = api.client._build_url(api.resource("documents/documents"))
    headers = api.client._get_headers()
    headers.pop("Content-Type", None)

    author = author_access_id(api)
    data: Dict[str, str] = {
        "public": "true",
        "space": space,
        "is_pending_assignment": "false",
        "author_id": author,
        "company_id": COMPANY_ID,
        "request_esignature": "false",
        "file_filename": filename or file_path.name,
        "signee_ids[]": author,
    }

    with file_path.open("rb") as handle:
        files = {"file": (data["file_filename"], handle, "application/pdf")}
        response = api.client.session.post(
            url, headers=headers, data=data, files=files, timeout=120
        )
    try:
        body = response.json() if response.content else None
    except Exception:
        body = {"raw": response.text[:1000]}
    return response.status_code, body


def list_documents(api: KibandaApi) -> None:
    print("=== Kibanda Documents ===")
    docs = api.list_all("documents/documents")
    kibanda_docs = [d for d in docs if "Kibanda" in str(d.get("filename", ""))]
    print("\nDocuments (Kibanda):")
    if kibanda_docs:
        for doc in kibanda_docs:
            print(
                f"  id={doc.get('id')} file={doc.get('filename')} space={doc.get('space')}"
            )
    else:
        print("  (none matched)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload Kibanda demo PDFs")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    api = KibandaApi()
    if args.list:
        list_documents(api)
        return 0

    results: List[Dict[str, Any]] = []
    for item in DEFAULT_UPLOADS:
        path: Path = item["path"]
        print(f"Uploading {path.name} ...")
        status, body = upload_file(api, path, filename=item["filename"], space=item["space"])
        ok = status in (200, 201)
        print(f"  -> {status} {'OK' if ok else body}")
        results.append(
            {
                "file": path.name,
                "status": status,
                "ok": ok,
                "id": body.get("id") if isinstance(body, dict) else None,
                "body": body if not ok else {"id": body.get("id") if isinstance(body, dict) else None},
            }
        )

    out = RUN_LOG_DIR / "documents_upload_latest.json"
    save_json(out, {"uploads": results})
    print(f"Wrote {out}")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
