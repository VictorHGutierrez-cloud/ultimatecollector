#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Define 2026-07-01 como versão oficial da API no projeto."""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW_VERSION = "2026-07-01"
OLD_VERSIONS = ["2025-07-01", "2026-01-01", "2026-04-01", "2026-10-01"]


def main() -> None:
    src_oas = ROOT / f"OAS Factorial {NEW_VERSION}.json"
    dst_oas = ROOT / "OAS Factorial.json"
    ontop_oas = ROOT / "Ontop" / "OAS Factorial.json"

    if not src_oas.exists():
        raise SystemExit(f"Arquivo não encontrado: {src_oas}")

    shutil.copy2(src_oas, dst_oas)
    shutil.copy2(src_oas, ontop_oas)
    oas = json.loads(dst_oas.read_text(encoding="utf-8"))
    print(f"OAS official: {oas['info']['version']} paths={len(oas['paths'])}")

    for env_path in (ROOT / "config_unificado.env", ROOT / "collector_africa" / "config_local.env"):
        if not env_path.exists():
            continue
        text = env_path.read_text(encoding="utf-8")
        if re.search(r"^API_VERSION=", text, flags=re.M):
            text = re.sub(r"^API_VERSION=.*$", f"API_VERSION={NEW_VERSION}", text, flags=re.M)
        else:
            text = f"API_VERSION={NEW_VERSION}\n{text}"
        env_path.write_text(text, encoding="utf-8")
        print(f"updated env: {env_path.relative_to(ROOT)}")

    example = ROOT / "config" / "config.example.env"
    if example.exists():
        text = example.read_text(encoding="utf-8")
        if "API_VERSION" in text:
            text = re.sub(r"^API_VERSION=.*$", f"API_VERSION={NEW_VERSION}", text, flags=re.M)
        else:
            text = text.replace(
                "AUTH_TYPE=bearer",
                f"API_VERSION={NEW_VERSION}\nAUTH_TYPE=bearer",
                1,
            )
            if "# Versão oficial" not in text and "API_VERSION=" in text:
                text = text.replace(
                    f"API_VERSION={NEW_VERSION}\nAUTH_TYPE=bearer",
                    (
                        "# Versão oficial da API Factorial\n"
                        f"API_VERSION={NEW_VERSION}\n\n"
                        "# Tipo de autenticação (bearer, x-api-key, oauth2)\n"
                        "AUTH_TYPE=bearer"
                    ),
                    1,
                )
        example.write_text(text, encoding="utf-8")
        print("updated config/config.example.env")

    changed = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "node_modules", "__pycache__", "uploads", "agent-tools"} for part in path.parts):
            continue
        if path.name.startswith("OAS Factorial"):
            continue
        if path.name == "set_api_version_2026_07_01.py":
            continue
        if path.suffix.lower() not in {".py", ".env"} and path.name != "config.example.env":
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        original = text
        for old in OLD_VERSIONS:
            text = text.replace(old, NEW_VERSION)

        text = re.sub(
            r"(os\.getenv\(\s*['\"]API_VERSION['\"]\s*,\s*['\"])1\.0\.0(['\"])",
            rf"\g<1>{NEW_VERSION}\2",
            text,
        )
        text = re.sub(
            r"(os\.getenv\(\s*['\"]API_VERSION['\"]\s*,\s*['\"])2025-07-01(['\"])",
            rf"\g<1>{NEW_VERSION}\2",
            text,
        )

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    print(f"code/env files updated: {len(changed)}")
    for item in changed:
        print(f" - {item}")

    rebuild_mappings(oas)
    print("done")


def rebuild_mappings(oas: dict) -> None:
    prefix = f"/api/{NEW_VERSION}/resources/"
    simple_get = {}
    simple_write = {}

    for path, methods in oas.get("paths", {}).items():
        if not path.startswith(prefix) or "{" in path:
            continue
        method_names = {m.lower() for m in methods.keys()}
        tail = path[len(prefix) :].strip("/")
        parts = tail.split("/")
        category = parts[0]
        name = "_".join(parts[1:]) if len(parts) > 1 else category

        if "get" in method_names:
            simple_get.setdefault(category, {})[name] = tail

        write_methods = sorted(m for m in method_names if m in {"post", "put", "patch", "delete"})
        if write_methods:
            simple_write.setdefault(category, {})[name] = tail

    get_path = ROOT / "scripts" / "_oas_mapping_get.json"
    write_path = ROOT / "scripts" / "_oas_mapping.json"
    get_path.write_text(json.dumps(simple_get, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_path.write_text(json.dumps(simple_write, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        "mappings:",
        f"GET cats={len(simple_get)} endpoints={sum(len(v) for v in simple_get.values())}",
        f"WRITE cats={len(simple_write)} endpoints={sum(len(v) for v in simple_write.values())}",
    )


if __name__ == "__main__":
    main()
