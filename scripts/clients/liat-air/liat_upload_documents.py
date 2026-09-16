#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload de documentos para a demo LIAT AIR (company 191947).

Uso:
  python scripts/clients/liat-air/liat_upload_documents.py --list
  python scripts/clients/liat-air/liat_upload_documents.py --apply
  python scripts/clients/liat-air/liat_upload_documents.py --apply --file "caminho/arquivo.pdf"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ultimate_collector.core.client_config import activate_client  # noqa: E402

activate_client("liat-air")

LIAT_CLIENT_DIR = ROOT / "clients" / "liat-air"
sys.path.insert(0, str(LIAT_CLIENT_DIR))
from api_helpers import LiatApi, normalize_name, save_json  # noqa: E402

ASSET_DIR = LIAT_CLIENT_DIR / "liat-airasset"
RUN_LOG_DIR = LIAT_CLIENT_DIR / "run_log"
COMPANY_ID = "191947"
FOLDER_NAME = "LIAT Staff Travel"

DEFAULT_UPLOADS = [
    {
        "path": ASSET_DIR / "LIAT HRIS Vendor Framework.pdf",
        "filename": "LIAT HRIS Vendor Framework.pdf",
        "space": "company_internal",
    },
]


def author_access_id(api: LiatApi) -> str:
    for name in ("Denise Antoine", "Marcus Williams"):
        for emp in api.list_all("employees/employees"):
            full = emp.get("full_name") or f"{emp.get('first_name')} {emp.get('last_name')}"
            if normalize_name(full) == normalize_name(name) and emp.get("access_id"):
                return str(emp["access_id"])
    for emp in api.list_all("employees/employees"):
        if emp.get("access_id"):
            return str(emp["access_id"])
    raise RuntimeError("No employee access_id found for document author")


def ensure_folder(api: LiatApi, space: str) -> Optional[str]:
    """Custom folders work for employee_my_documents; company_internal uses upload root."""
    if space != "employee_my_documents":
        return None
    folders = api.list_all("documents/folders", params={"name": FOLDER_NAME})
    for folder in folders:
        if folder.get("name") == FOLDER_NAME and folder.get("space") == space:
            return str(folder["id"])
    status, body = api.post(
        "documents/folders",
        {"name": FOLDER_NAME, "space": space, "company_id": COMPANY_ID},
    )
    if status in (200, 201) and isinstance(body, dict) and body.get("id"):
        return str(body["id"])
    raise RuntimeError(f"Could not create folder: {status} {body}")


def upload_file(
    api: LiatApi,
    file_path: Path,
    *,
    filename: Optional[str] = None,
    space: str = "company_internal",
    folder_id: Optional[str] = None,
    employee_id: Optional[str] = None,
    request_esignature: bool = False,
    signee_access_id: Optional[str] = None,
) -> Tuple[int, Any]:
    if not file_path.exists():
        return 404, {"error": f"File not found: {file_path}"}

    url = api.client._build_url(api.resource("documents/documents"))
    headers = api.client._get_headers()
    headers.pop("Content-Type", None)

    author = author_access_id(api)
    signee = signee_access_id or author
    data: Dict[str, str] = {
        "public": "true",
        "space": space,
        "is_pending_assignment": "false",
        "author_id": author,
        "company_id": COMPANY_ID,
        "request_esignature": "true" if request_esignature else "false",
        "file_filename": filename or file_path.name,
        "signee_ids[]": signee,
    }
    if folder_id:
        data["folder_id"] = folder_id
    if employee_id:
        data["employee_id"] = employee_id

    content_type = "application/pdf"
    if file_path.suffix.lower() in (".doc", ".docx"):
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    with file_path.open("rb") as handle:
        files = {"file": (data["file_filename"], handle, content_type)}
        response = api.client.session.post(
            url, headers=headers, data=data, files=files, timeout=120
        )
    try:
        body = response.json() if response.content else None
    except Exception:
        body = {"raw": response.text[:1000]}
    return response.status_code, body


def list_documents(api: LiatApi) -> None:
    print("=== LIAT Documents ===")
    folders = api.list_all("documents/folders")
    liat_folders = [f for f in folders if "LIAT" in str(f.get("name", ""))]
    print("\nFolders (LIAT):")
    for folder in liat_folders:
        print(f"  id={folder.get('id')} name={folder.get('name')} space={folder.get('space')}")

    docs = api.list_all("documents/documents")
    liat_docs = [
        d
        for d in docs
        if "LIAT" in str(d.get("filename", ""))
        or str(d.get("folder_id")) in {str(f.get("id")) for f in liat_folders}
    ]
    print("\nDocuments (LIAT):")
    if liat_docs:
        for doc in liat_docs:
            print(
                f"  id={doc.get('id')} file={doc.get('filename')} "
                f"space={doc.get('space')} folder_id={doc.get('folder_id')}"
            )
    else:
        print("  (none matched)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload documents to LIAT Factorial demo")
    parser.add_argument("--list", action="store_true", help="List LIAT documents/folders")
    parser.add_argument("--apply", action="store_true", help="Upload default LIAT asset files")
    parser.add_argument("--file", help="Upload a single file path")
    parser.add_argument("--employee-id", help="Target employee_id for employee_my_documents")
    parser.add_argument("--space", default="company_internal", help="Document space")
    parser.add_argument("--esign", action="store_true", help="Request e-signature")
    args = parser.parse_args()

    api = LiatApi()

    if args.list:
        list_documents(api)
        return 0

    if not args.apply and not args.file:
        parser.error("Use --list, --apply, or --file")

    folder_id = None
    if args.space == "employee_my_documents" and args.employee_id:
        folder_id = ensure_folder(api, args.space)
        print(f"Folder: {FOLDER_NAME} id={folder_id}")

    uploads: List[Dict[str, Any]] = []
    if args.file:
        path = Path(args.file)
        uploads.append({"path": path, "filename": path.name, "space": args.space})
    else:
        uploads = DEFAULT_UPLOADS

    log = {"uploads": [], "errors": []}
    for item in uploads:
        path = Path(item["path"])
        print(f"Uploading {path.name}...")
        status, body = upload_file(
            api,
            path,
            filename=item.get("filename"),
            space=item.get("space", args.space),
            folder_id=folder_id,
            employee_id=args.employee_id,
            request_esignature=args.esign,
        )
        entry = {"file": str(path), "status": status, "body": body}
        log["uploads"].append(entry)
        if status in (200, 201):
            doc_id = body.get("id") if isinstance(body, dict) else None
            print(f"  OK id={doc_id}")
        else:
            print(f"  FAIL {status} {body}")
            log["errors"].append(entry)

    save_json(RUN_LOG_DIR / "documents_upload_latest.json", log)
    return 1 if log["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
