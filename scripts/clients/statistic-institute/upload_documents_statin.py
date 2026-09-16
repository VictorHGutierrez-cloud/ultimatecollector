#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload STATIN private documents to Factorial (company_internal, public=false).

Factorial Documents has no preview for .md files, so client-facing artefacts
are uploaded as PDF.

Usage:
  python scripts/clients/statistic-institute/upload_documents_statin.py --list
  python scripts/clients/statistic-institute/upload_documents_statin.py --apply
  python scripts/clients/statistic-institute/upload_documents_statin.py --apply --file "path/to/file.pdf"
  python scripts/clients/statistic-institute/upload_documents_statin.py --trash 13201216
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("statistic-institute")

STATIN_CLIENT_DIR = ROOT / "clients" / "statistic-institute"
sys.path.insert(0, str(STATIN_CLIENT_DIR))
from api_helpers import StatinApi, normalize_name, save_json  # noqa: E402

ASSET_DIR = STATIN_CLIENT_DIR / "statistic-instituteasset"
RUN_LOG_DIR = STATIN_CLIENT_DIR / "run_log"
COMPANY_ID = "191864"

DEFAULT_UPLOADS = [
    {
        "path": ASSET_DIR / "STATIN Factorial Scope Guide.pdf",
        "filename": "STATIN Factorial Scope Guide.pdf",
        "space": "company_internal",
        "public": False,
    },
]


def author_access_id(api: StatinApi) -> str:
    preferred = ("Charles Carter", "Laura Lewis", "Hellen Howard")
    employees = api.list_all("employees/employees")
    for name in preferred:
        for emp in employees:
            full = emp.get("full_name") or f"{emp.get('first_name')} {emp.get('last_name')}"
            if normalize_name(full) == normalize_name(name) and emp.get("access_id"):
                return str(emp["access_id"])
    for emp in employees:
        if emp.get("access_id"):
            return str(emp["access_id"])
    raise RuntimeError("No employee access_id found for document author")


def content_type_for(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }.get(ext, "application/octet-stream")


def upload_file(
    api: StatinApi,
    file_path: Path,
    *,
    filename: Optional[str] = None,
    space: str = "company_internal",
    public: bool = False,
    folder_id: Optional[str] = None,
    employee_id: Optional[str] = None,
    request_esignature: bool = False,
) -> Tuple[int, Any]:
    if not file_path.exists():
        return 404, {"error": f"File not found: {file_path}"}

    url = api.client._build_url(api.resource("documents/documents"))
    headers = api.client._get_headers()
    headers.pop("Content-Type", None)

    author = author_access_id(api)
    data: Dict[str, str] = {
        "public": "true" if public else "false",
        "space": space,
        "is_pending_assignment": "false",
        "author_id": author,
        "company_id": COMPANY_ID,
        "request_esignature": "true" if request_esignature else "false",
        "file_filename": filename or file_path.name,
        "signee_ids[]": author,
    }
    if folder_id:
        data["folder_id"] = folder_id
    if employee_id:
        data["employee_id"] = employee_id

    with file_path.open("rb") as handle:
        files = {"file": (data["file_filename"], handle, content_type_for(file_path))}
        response = api.client.session.post(
            url, headers=headers, data=data, files=files, timeout=120
        )
    try:
        body = response.json() if response.content else None
    except Exception:
        body = {"raw": response.text[:1000]}
    return response.status_code, body


def delete_document(api: StatinApi, document_id: str) -> Tuple[int, Any]:
    url = api.client._build_url(api.resource(f"documents/documents/{document_id}"))
    response = api.client.session.delete(
        url, headers=api.client._get_headers(), timeout=api.config.TIMEOUT
    )
    try:
        body = response.json() if response.content else None
    except Exception:
        body = {"raw": response.text[:400]}
    return response.status_code, body


def trash_documents(api: StatinApi, document_ids: List[str]) -> int:
    """Try the bulk trash-bin endpoint, then fall back to per-document DELETE.

    The demo API key is not authorised for move_to_trash_bin (403).
    """
    status, body = api.post("documents/documents/move_to_trash_bin", {"document_ids": document_ids})
    if status in (200, 201, 204):
        print(f"Moved to trash bin: {document_ids}")
        return 0

    print(f"move_to_trash_bin unavailable ({status}); falling back to DELETE")
    failures = 0
    for doc_id in document_ids:
        del_status, del_body = delete_document(api, doc_id)
        if del_status in (200, 201, 204):
            print(f"  deleted id={doc_id}")
        else:
            failures += 1
            print(f"  FAIL id={doc_id} -> {del_status} {del_body}")
    return 1 if failures else 0


def list_documents(api: StatinApi) -> None:
    print("=== STATIN Documents ===")
    docs = api.list_all("documents/documents")
    statin_docs = [
        d
        for d in docs
        if "STATIN" in str(d.get("filename", "")).upper()
        or "SIJ" in str(d.get("filename", "")).upper()
        or "SCOPE" in str(d.get("filename", "")).upper()
    ]
    print(f"Matched docs: {len(statin_docs)} (of {len(docs)} total listed pages)")
    for doc in statin_docs[:40]:
        print(
            f"  id={doc.get('id')} file={doc.get('filename')} "
            f"space={doc.get('space')} public={doc.get('public')}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload STATIN private documents")
    parser.add_argument("--list", action="store_true", help="List STATIN-related documents")
    parser.add_argument("--apply", action="store_true", help="Upload default guide file(s)")
    parser.add_argument("--file", help="Upload a single file path")
    parser.add_argument("--space", default="company_internal", help="Document space")
    parser.add_argument(
        "--public",
        action="store_true",
        help="Mark document public (default is private/public=false)",
    )
    parser.add_argument(
        "--trash",
        nargs="+",
        metavar="DOCUMENT_ID",
        help="Move the given document ids to the Factorial trash bin",
    )
    args = parser.parse_args()

    api = StatinApi()
    if args.list:
        list_documents(api)
        return 0
    if args.trash:
        return trash_documents(api, [str(i) for i in args.trash])
    if not args.apply and not args.file:
        parser.error("Use --list, --apply, --file, or --trash")

    uploads: List[Dict[str, Any]] = []
    if args.file:
        path = Path(args.file)
        uploads.append(
            {
                "path": path,
                "filename": path.name,
                "space": args.space,
                "public": bool(args.public),
            }
        )
    else:
        uploads = DEFAULT_UPLOADS

    log: Dict[str, Any] = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "uploads": [],
        "errors": [],
    }
    for item in uploads:
        path = Path(item["path"])
        public = bool(item.get("public", False))
        space = item.get("space", args.space)
        print(f"Uploading {path.name} -> space={space} public={public}")
        status, body = upload_file(
            api,
            path,
            filename=item.get("filename"),
            space=space,
            public=public,
        )
        entry = {"file": str(path), "status": status, "body": body}
        log["uploads"].append(entry)
        if status in (200, 201):
            doc_id = body.get("id") if isinstance(body, dict) else None
            print(f"  OK id={doc_id}")
        else:
            print(f"  FAIL {status} {body}")
            log["errors"].append(entry)

    log["finished_at"] = datetime.now(timezone.utc).isoformat()
    save_json(RUN_LOG_DIR / "documents_upload_latest.json", log)
    return 1 if log["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
