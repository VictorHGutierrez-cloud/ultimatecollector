#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carregamento de perfis de clientes sandbox.
"""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from .paths import CLIENTS_DIR, CONFIG_DIR, PROJECT_ROOT


@dataclass
class ClientProfile:
    id: str
    name: str
    company_id: int
    api: Dict[str, Any]
    secrets: Dict[str, Any]
    data_dir: str
    features: Dict[str, Any] = field(default_factory=dict)
    catalog: Optional[str] = None
    client_dir: Path = field(default_factory=Path)

    @property
    def data_path(self) -> Path:
        return PROJECT_ROOT / self.data_dir

    @property
    def catalog_path(self) -> Optional[Path]:
        if not self.catalog:
            return None
        return self.client_dir / self.catalog


def _read_token_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return ""
    if "=" in text and not text.startswith("eyJ"):
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return text


def _decode_jwt_payload(token: str) -> Optional[Dict[str, Any]]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload_part = parts[1]
        padded = payload_part + "=" * (4 - len(payload_part) % 4)
        return json.loads(base64.urlsafe_b64decode(padded))
    except Exception:
        return None


def _decode_jwt_company_id(token: str) -> Optional[int]:
    data = _decode_jwt_payload(token)
    if not data:
        return None
    cid = data.get("company_id")
    try:
        return int(cid) if cid is not None else None
    except Exception:
        return None


def _slugify_client_id(value: str) -> str:
    import re

    text = (value or "").strip().lower()
    text = re.sub(r"[^a-z0-9_-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-_")
    return text or "cliente"


def client_asset_dir(client_id: str) -> Path:
    """Pasta de materiais do cliente: clients/{id}/{id}asset/"""
    return CLIENTS_DIR / client_id / f"{client_id}asset"


def ensure_client_asset_dir(client_id: str) -> Path:
    """Garante que a pasta {client_id}asset existe."""
    path = client_asset_dir(client_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def find_client_by_company_id(company_id: int) -> Optional[str]:
    for cid in list_clients():
        try:
            if load_profile(cid).company_id == int(company_id):
                return cid
        except Exception:
            continue
    return None


def create_client_from_token(
    api_key: str,
    display_name: Optional[str] = None,
    client_id: Optional[str] = None,
    auth_type: str = "x-api-key",
    base_url: str = "https://api.eu2.demo.factorial.dev",
    api_version: str = "2026-07-01",
    update_if_exists: bool = True,
) -> Dict[str, Any]:
    """
    Cria (ou atualiza) um cliente a partir da API key.
    O company_id é lido automaticamente do JWT.
    """
    token = (api_key or "").strip()
    if not token:
        raise ValueError("Cole uma API key / token.")

    payload = _decode_jwt_payload(token)
    company_id = _decode_jwt_company_id(token)
    if company_id is None:
        raise ValueError(
            "Nao foi possivel ler company_id do token. "
            "Confirme que e uma API key JWT da Factorial."
        )

    existing_id = find_client_by_company_id(company_id)
    if existing_id and update_if_exists:
        token_path = save_client_token(existing_id, token)
        profile = load_profile(existing_id)
        asset_path = ensure_client_asset_dir(existing_id)
        return {
            "created": False,
            "updated": True,
            "client_id": existing_id,
            "name": profile.name,
            "company_id": company_id,
            "token_path": str(token_path),
            "profile_path": str(profile.client_dir / "profile.json"),
            "asset_dir": str(asset_path),
            "jwt_cell": (payload or {}).get("cell"),
        }

    if existing_id and not update_if_exists:
        raise ValueError(
            f"Ja existe cliente '{existing_id}' para company_id {company_id}."
        )

    slug = _slugify_client_id(client_id or display_name or f"company-{company_id}")
    if slug in list_clients():
        slug = f"{slug}-{company_id}"

    name = (display_name or "").strip() or f"Company {company_id}"
    client_dir = CLIENTS_DIR / slug
    secrets_dir = client_dir / "secrets"
    secrets_dir.mkdir(parents=True, exist_ok=True)

    profile_data = {
        "id": slug,
        "name": name,
        "company_id": company_id,
        "api": {
            "provider": "factorial",
            "base_url": base_url,
            "version": api_version,
            "auth_type": auth_type,
        },
        "secrets": {
            "token_files": ["secrets/seutoken.txt"],
            "env_file": "secrets/secrets.env",
        },
        "data_dir": f"data/clients/{slug}",
        "features": {
            "collect": ["employees", "finance", "expenses", "attendance"],
            "send": ["attendance"],
            "seed": False,
        },
    }

    profile_path = client_dir / "profile.json"
    profile_path.write_text(
        json.dumps(profile_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    token_path = secrets_dir / "seutoken.txt"
    token_path.write_text(token + "\n", encoding="utf-8")

    data_path = PROJECT_ROOT / f"data/clients/{slug}/raw"
    data_path.mkdir(parents=True, exist_ok=True)
    asset_path = ensure_client_asset_dir(slug)

    return {
        "created": True,
        "updated": False,
        "client_id": slug,
        "name": name,
        "company_id": company_id,
        "token_path": str(token_path),
        "profile_path": str(profile_path),
        "asset_dir": str(asset_path),
        "jwt_cell": (payload or {}).get("cell"),
    }


def list_clients() -> List[str]:
    if not CLIENTS_DIR.exists():
        return []
    return sorted(
        p.name
        for p in CLIENTS_DIR.iterdir()
        if p.is_dir() and (p / "profile.json").exists()
    )


def load_profile(client_id: str) -> ClientProfile:
    client_dir = CLIENTS_DIR / client_id
    profile_path = client_dir / "profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"Cliente '{client_id}' não encontrado em {profile_path}")

    raw = json.loads(profile_path.read_text(encoding="utf-8"))
    return ClientProfile(
        id=raw["id"],
        name=raw["name"],
        company_id=int(raw["company_id"]),
        api=raw.get("api", {}),
        secrets=raw.get("secrets", {}),
        data_dir=raw.get("data_dir", f"data/clients/{client_id}"),
        features=raw.get("features", {}),
        catalog=raw.get("catalog"),
        client_dir=client_dir,
    )


def _load_global_config() -> None:
    for path in (
        CONFIG_DIR / "unificado.env",
        PROJECT_ROOT / "config_unificado.env",
        CONFIG_DIR / ".env",
        CONFIG_DIR / "config.example.env",
    ):
        if path.exists():
            load_dotenv(path, override=False)
            break


def _prepare_client_dirs(profile: ClientProfile) -> None:
    data_path = profile.data_path
    data_path.mkdir(parents=True, exist_ok=True)
    (data_path / "raw").mkdir(parents=True, exist_ok=True)
    os.environ["RAW_DATA_DIR"] = str(data_path / "raw")
    os.environ["DATA_DIR"] = str(data_path)


def activate_client(client_id: str) -> ClientProfile:
    """Carrega perfil do cliente e aplica credenciais no ambiente."""
    profile = load_profile(client_id)
    os.environ["UC_CLIENT"] = client_id
    os.environ["UC_CLIENT_DIR"] = str(profile.client_dir)

    _load_global_config()

    api = profile.api
    os.environ.setdefault("BASE_URL", api.get("base_url", ""))
    os.environ.setdefault("API_VERSION", api.get("version", "2026-07-01"))
    os.environ.setdefault("AUTH_TYPE", api.get("auth_type", "bearer"))
    os.environ["COMPANY_ID"] = str(profile.company_id)

    token_loaded = False
    for rel in profile.secrets.get("token_files", []):
        token_path = profile.client_dir / rel
        if token_path.exists():
            token = _read_token_file(token_path)
            if token:
                os.environ["API_KEY"] = token
                token_loaded = True
                break

    env_file = profile.secrets.get("env_file")
    if env_file:
        env_path = profile.client_dir / env_file
        if env_path.exists() and env_path.suffix in (".env", ".txt"):
            load_dotenv(env_path, override=True)
            if os.getenv("API_KEY"):
                token_loaded = True

    if not token_loaded and profile.secrets.get("fallback_global_config"):
        _load_global_config()

    _prepare_client_dirs(profile)

    # Pasta de materiais do cliente (docs, time off, etc.)
    ensure_client_asset_dir(client_id)

    from .config import Config

    Config.reload()
    return profile


def apply_session_credentials(
    client_id: str,
    api_key: str,
    auth_type: str = "x-api-key",
    base_url: Optional[str] = None,
) -> ClientProfile:
    """Ativa cliente usando token da UI (prioridade sobre arquivos)."""
    profile = load_profile(client_id)
    os.environ["UC_CLIENT"] = client_id
    os.environ["UC_CLIENT_DIR"] = str(profile.client_dir)

    api = profile.api
    os.environ["BASE_URL"] = base_url or api.get("base_url", "")
    os.environ["API_VERSION"] = api.get("version", "2026-07-01")
    os.environ["AUTH_TYPE"] = auth_type or api.get("auth_type", "bearer")
    os.environ["COMPANY_ID"] = str(profile.company_id)
    os.environ["API_KEY"] = (api_key or "").strip()

    _prepare_client_dirs(profile)
    ensure_client_asset_dir(client_id)

    from .config import Config

    Config.reload()
    return profile


def save_client_token(client_id: str, api_key: str) -> Path:
    """Salva token em clients/{id}/secrets/seutoken.txt."""
    profile = load_profile(client_id)
    secrets_dir = profile.client_dir / "secrets"
    secrets_dir.mkdir(parents=True, exist_ok=True)
    token_path = secrets_dir / "seutoken.txt"
    token_path.write_text((api_key or "").strip() + "\n", encoding="utf-8")
    return token_path


def verify_client_token(client_id: str) -> Dict[str, Any]:
    """Valida token do cliente e compara company_id do JWT com o perfil."""
    profile = activate_client(client_id)
    from .config import Config

    config = Config()
    token = config.API_KEY or ""
    result: Dict[str, Any] = {
        "client_id": client_id,
        "client_name": profile.name,
        "expected_company_id": profile.company_id,
        "base_url": config.BASE_URL,
        "auth_type": config.AUTH_TYPE,
        "has_token": bool(token),
        "token_company_id": None,
        "match": False,
        "connection_ok": False,
    }

    if token:
        result["token_company_id"] = _decode_jwt_company_id(token)
        result["match"] = result["token_company_id"] == profile.company_id

    from .api_client import APIClient

    client = APIClient()
    result["connection_ok"] = client.test_connection()
    return result


def verify_session_token(
    client_id: str,
    api_key: str,
    auth_type: str = "x-api-key",
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Valida token colado na UI (sem depender de arquivos)."""
    profile = apply_session_credentials(client_id, api_key, auth_type, base_url)
    token = (api_key or "").strip()
    result: Dict[str, Any] = {
        "client_id": client_id,
        "client_name": profile.name,
        "expected_company_id": profile.company_id,
        "base_url": os.getenv("BASE_URL", ""),
        "auth_type": os.getenv("AUTH_TYPE", auth_type),
        "has_token": bool(token),
        "token_company_id": None,
        "match": False,
        "connection_ok": False,
    }
    if token:
        result["token_company_id"] = _decode_jwt_company_id(token)
        result["match"] = result["token_company_id"] == profile.company_id

    from .api_client import APIClient

    client = APIClient()
    result["connection_ok"] = client.test_connection()
    return result

