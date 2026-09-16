#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formata JSONs de job_catalog roles para leitura (indentação)
e gera uma versão simplificada (id, name, description).

Como usar:
  python tools/format_job_roles.py
Opcionalmente, passe caminhos específicos:
  python tools/format_job_roles.py data/reports/job_catalog_roles_*.json
"""

import sys
import json
from pathlib import Path
from typing import List

DEFAULT_GLOB = "data/reports/job_catalog_roles_*.json"


def find_files(args: List[str]) -> List[Path]:
    if args:
        files = []
        for pattern in args:
            files.extend(Path().glob(pattern))
        return sorted(set(files))
    return sorted(Path().glob(DEFAULT_GLOB))


def pretty_format(path: Path) -> Path:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        # pode ser linha única vazia
        try:
            content = path.read_text(encoding="utf-8").strip()
            if not content:
                data = []
            else:
                data = json.loads(content)
        except Exception as e:
            print(f"❌ Falha ao ler {path.name}: {e}")
            return path

    # sobrescrever com indentação
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Formatado (indentado): {path}")
    return path


def write_simple(path: Path) -> Path:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Falha ao ler (simple) {path.name}: {e}")
        return path

    simple = []
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            simple.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "description": item.get("description"),
            })
    else:
        # estrutura inesperada
        simple = data

    out = path.with_name(path.stem + "_simple" + path.suffix)
    out.write_text(json.dumps(simple, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Versão simples salva: {out}")
    return out


def main():
    files = find_files(sys.argv[1:])
    if not files:
        print("⚠️ Nenhum arquivo encontrado para formatar.")
        return

    for f in files:
        pretty_format(f)
        write_simple(f)


if __name__ == "__main__":
    main()
