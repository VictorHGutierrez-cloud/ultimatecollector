#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate Sender - envia dados para a API Factorial baseado no OAS
"""

import json
import random
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from ultimate_collector.core.api_client import APIClient
from ultimate_collector.core.config import Config


class UltimateSender(APIClient):
    """Sender genérico baseado no OAS para operações de escrita"""

    def __init__(self, oas_path: Optional[Path] = None):
        super().__init__()
        self.config = Config()
        root = Path(__file__).resolve().parents[2]
        default_oas = root / "assets" / "oas" / "OAS Factorial.json"
        if not default_oas.exists():
            default_oas = root / "OAS Factorial.json"
        self.oas_path = oas_path or default_oas
        self._oas = json.loads(self.oas_path.read_text(encoding="utf-8"))
        self._components = self._oas.get("components", {})
        self._write_map = self._build_write_map()

    def _build_write_map(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Lê o OAS e cria o mapa de endpoints de escrita"""
        paths = self._oas.get("paths", {})

        version = self.config.API_VERSION or "2026-07-01"
        prefix = f"/api/{version}/resources/"

        write_map: Dict[str, Dict[str, Dict[str, Any]]] = {}
        for path, methods in paths.items():
            if not path.startswith(prefix):
                continue
            # Pular endpoints com parâmetros de path por enquanto (ex: {id})
            if "{" in path or "}" in path:
                continue

            available_methods = [m.lower() for m in methods.keys()]
            write_methods = [m for m in available_methods if m in ("post", "put", "patch", "delete")]
            if not write_methods:
                continue

            tail = path[len(prefix):].strip("/")
            if not tail:
                continue

            parts = tail.split("/")
            category = parts[0]
            endpoint_name = "_".join(parts[1:]) if len(parts) > 1 else category

            path_params = re.findall(r"\{([^}]+)\}", path)
            method_defs = {m.lower(): methods[m] for m in methods}
            write_map.setdefault(category, {})[endpoint_name] = {
                "path": tail,
                "methods": sorted(set(write_methods)),
                "path_params": path_params,
                "method_defs": method_defs,
            }

        return write_map

    def list_categories(self) -> List[str]:
        return sorted(self._write_map.keys())

    def list_endpoints(self, category: str) -> Dict[str, Dict[str, Any]]:
        return self._write_map.get(category, {})

    def resolve_endpoint(self, category: str, endpoint_name: str) -> Optional[Dict[str, Any]]:
        return self._write_map.get(category, {}).get(endpoint_name)

    def build_endpoint_path(self, endpoint_def: Dict[str, Any],
                            param_values: Optional[Dict[str, str]] = None) -> str:
        path = endpoint_def["path"]
        if not param_values:
            return self._with_api_prefix(path)
        for key, value in param_values.items():
            path = path.replace("{" + key + "}", str(value))
        return self._with_api_prefix(path)

    def _with_api_prefix(self, path: str) -> str:
        """Garante prefixo /api/{version}/resources/"""
        if path.startswith("http"):
            return path
        if path.startswith("api/") or path.startswith("/api/"):
            return path.lstrip("/")
        version = self.config.API_VERSION or "2026-07-01"
        return f"api/{version}/resources/{path.lstrip('/')}"

    def send(self, method: str, endpoint: str,
             params: Optional[Dict] = None,
             data: Optional[Dict] = None) -> Optional[Dict]:
        return self.request(method, endpoint, params=params, data=data)

    def build_random_payload(self, endpoint_def: Dict[str, Any],
                             method: str) -> Optional[Dict[str, Any]]:
        """Gera payload aleatório baseado no schema do OAS"""
        method_def = endpoint_def.get("method_defs", {}).get(method.lower())
        if not method_def:
            return None
        request_body = method_def.get("requestBody", {})
        content = request_body.get("content", {})
        schema = None
        if "application/json" in content:
            schema = content["application/json"].get("schema")
        elif content:
            first_key = next(iter(content.keys()))
            schema = content[first_key].get("schema")
        if not schema:
            return None
        return self._random_from_schema(schema)

    def _resolve_ref(self, ref: str) -> Dict[str, Any]:
        """Resolve $ref do OAS"""
        if not ref.startswith("#/"):
            return {}
        parts = ref.lstrip("#/").split("/")
        current: Any = self._oas
        for part in parts:
            current = current.get(part, {})
        return current if isinstance(current, dict) else {}

    def _random_from_schema(self, schema: Dict[str, Any], depth: int = 0) -> Any:
        """Gera dado aleatório respeitando limites do schema"""
        if depth > 4:
            return None

        if "$ref" in schema:
            resolved = self._resolve_ref(schema["$ref"])
            return self._random_from_schema(resolved, depth + 1)

        if "oneOf" in schema and schema["oneOf"]:
            return self._random_from_schema(schema["oneOf"][0], depth + 1)
        if "anyOf" in schema and schema["anyOf"]:
            return self._random_from_schema(schema["anyOf"][0], depth + 1)
        if "allOf" in schema and schema["allOf"]:
            base: Dict[str, Any] = {}
            for s in schema["allOf"]:
                value = self._random_from_schema(s, depth + 1)
                if isinstance(value, dict):
                    base.update(value)
            return base

        if "enum" in schema:
            return random.choice(schema["enum"])

        if "default" in schema:
            return schema["default"]

        schema_type = schema.get("type")
        if isinstance(schema_type, list):
            schema_type = schema_type[0]

        if schema_type == "object" or "properties" in schema:
            properties = schema.get("properties", {})
            required = set(schema.get("required", []))
            result: Dict[str, Any] = {}
            for key, prop_schema in properties.items():
                if key in required or random.random() < 0.6:
                    result[key] = self._random_from_schema(prop_schema, depth + 1)
            return result

        if schema_type == "array":
            items = schema.get("items", {})
            min_items = int(schema.get("minItems", 1))
            max_items = int(schema.get("maxItems", min_items + 2))
            count = max(min_items, min(max_items, min_items + 1))
            return [self._random_from_schema(items, depth + 1) for _ in range(count)]

        if schema_type == "integer":
            minimum = int(schema.get("minimum", 1))
            maximum = int(schema.get("maximum", minimum + 10))
            return random.randint(minimum, maximum)

        if schema_type == "number":
            minimum = float(schema.get("minimum", 1.0))
            maximum = float(schema.get("maximum", minimum + 10.0))
            return round(random.uniform(minimum, maximum), 2)

        if schema_type == "boolean":
            return random.choice([True, False])

        if schema_type == "string" or schema.get("format"):
            fmt = schema.get("format")
            if fmt == "date-time":
                return datetime.now(timezone.utc).isoformat()
            if fmt == "date":
                return datetime.now().date().isoformat()
            if fmt == "uuid":
                return str(uuid.uuid4())
            if fmt == "email":
                return f"teste{random.randint(1,9999)}@exemplo.com"
            max_len = int(schema.get("maxLength", 12))
            min_len = int(schema.get("minLength", 4))
            length = max(min_len, min(max_len, min_len + 4))
            return "x" * length

        return None
