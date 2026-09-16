#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Camada de serviço sem argparse — usada pela CLI e pelo app desktop.
"""

from __future__ import annotations

import os
import subprocess
import sys
from typing import Callable, List, Optional

from ultimate_collector.core.client_config import (
    activate_client,
    apply_session_credentials,
    create_client_from_token,
    list_clients,
    load_profile,
    save_client_token,
    verify_client_token,
    verify_session_token,
)
from ultimate_collector.core.config import Config
from ultimate_collector.core.paths import PROJECT_ROOT

LogFn = Callable[[str], None]


def _log(on_log: Optional[LogFn], message: str) -> None:
    if on_log:
        on_log(message)
    else:
        print(message)


class SandboxRunner:
    """Executa ações de sandbox com logs opcionais."""

    @staticmethod
    def list_clients() -> List[str]:
        return list_clients()

    @staticmethod
    def load_profile(client_id: str):
        return load_profile(client_id)

    @staticmethod
    def create_from_token(
        api_key: str,
        display_name: Optional[str] = None,
        client_id: Optional[str] = None,
        auth_type: str = "x-api-key",
        base_url: str = "https://api.eu2.demo.factorial.dev",
    ) -> dict:
        return create_client_from_token(
            api_key=api_key,
            display_name=display_name,
            client_id=client_id,
            auth_type=auth_type,
            base_url=base_url,
        )

    @staticmethod
    def activate(
        client_id: str,
        api_key: Optional[str] = None,
        auth_type: str = "x-api-key",
        base_url: Optional[str] = None,
    ):
        if api_key:
            return apply_session_credentials(client_id, api_key, auth_type, base_url)
        return activate_client(client_id)

    @staticmethod
    def save_token(client_id: str, api_key: str):
        return save_client_token(client_id, api_key)

    @staticmethod
    def verify_token(
        client_id: str,
        api_key: Optional[str] = None,
        auth_type: str = "x-api-key",
        base_url: Optional[str] = None,
        on_log: Optional[LogFn] = None,
    ) -> dict:
        if api_key:
            result = verify_session_token(client_id, api_key, auth_type, base_url)
        else:
            result = verify_client_token(client_id)

        _log(on_log, f"Cliente: {result['client_name']} ({result['client_id']})")
        _log(on_log, f"URL: {result['base_url']}")
        _log(on_log, f"Auth: {result['auth_type']}")
        _log(on_log, f"Token: {'sim' if result['has_token'] else 'NAO'}")
        _log(on_log, f"Company esperado: {result['expected_company_id']}")
        _log(on_log, f"Company no token: {result['token_company_id']}")
        _log(on_log, f"Match: {'OK' if result['match'] else 'FALHOU'}")
        _log(on_log, f"Conexao: {'OK' if result['connection_ok'] else 'FALHOU'}")
        return result

    @staticmethod
    def collect(
        client_id: str,
        categories: Optional[List[str]] = None,
        api_key: Optional[str] = None,
        auth_type: str = "x-api-key",
        base_url: Optional[str] = None,
        on_log: Optional[LogFn] = None,
    ) -> int:
        SandboxRunner.activate(client_id, api_key, auth_type, base_url)
        from ultimate_collector.collectors.hr_data_masterultimate import HRDataMasterUltimate

        collector = HRDataMasterUltimate()
        cats = categories or Config.AUTO_COLLECT_CATEGORIES
        _log(on_log, f"Coletando para '{client_id}': {', '.join(cats)}")
        _log(on_log, f"Pasta destino: {os.getenv('RAW_DATA_DIR') or Config.RAW_DATA_DIR}")
        for category in cats:
            cat = category.strip()
            if not cat:
                continue
            _log(on_log, f"  -> {cat}")
            try:
                collector.collect_category(cat)
                _log(on_log, f"     OK: {cat}")
            except Exception as exc:
                _log(on_log, f"     ERRO ({cat}): {exc}")
                return 1
        _log(on_log, "Coleta concluida.")
        return 0

    @staticmethod
    def send_attendance(
        client_id: str,
        employee_ids: Optional[List[int]] = None,
        api_key: Optional[str] = None,
        auth_type: str = "x-api-key",
        base_url: Optional[str] = None,
        on_log: Optional[LogFn] = None,
    ) -> int:
        SandboxRunner.activate(client_id, api_key, auth_type, base_url)
        from ultimate_collector.senders.attendance_sender import AttendanceSender

        config = Config()
        employees = employee_ids or config.AUTO_ATTENDANCE_EMPLOYEES
        if not employees:
            _log(on_log, "Nenhum funcionario informado.")
            return 1

        sender = AttendanceSender()
        for employee_id in employees:
            _log(on_log, f"Clock in/out funcionario {employee_id}...")
            try:
                sender.clock_in(employee_id=employee_id)
                sender.clock_out(employee_id=employee_id)
                _log(on_log, f"  OK: {employee_id}")
            except Exception as exc:
                _log(on_log, f"  ERRO ({employee_id}): {exc}")
                return 1
        _log(on_log, "Envio de presenca concluido.")
        return 0

    @staticmethod
    def seed_demo(
        client_id: str,
        apply: bool = False,
        api_key: Optional[str] = None,
        auth_type: str = "x-api-key",
        base_url: Optional[str] = None,
        on_log: Optional[LogFn] = None,
    ) -> int:
        profile = SandboxRunner.activate(client_id, api_key, auth_type, base_url)
        if not profile.features.get("seed"):
            _log(on_log, f"Cliente '{client_id}' nao suporta seed.")
            return 1
        if client_id != "szv":
            _log(on_log, "Seed automatico disponivel apenas para SZV por enquanto.")
            return 1

        mode = "apply" if apply else "dry-run"
        _log(on_log, f"Executando seed SZV ({mode})...")

        # Preferir import direto; fallback para subprocess
        try:
            if str(PROJECT_ROOT) not in sys.path:
                sys.path.insert(0, str(PROJECT_ROOT))
            scripts_dir = PROJECT_ROOT / "scripts" / "clients" / "szv"
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))

            import szv_seed_performance as seed_mod  # type: ignore

            seeder = seed_mod.SzvSeeder(apply=apply)
            code = seeder.run()
            _log(on_log, f"Seed finalizado com codigo {code}")
            return int(code)
        except Exception as import_exc:
            _log(on_log, f"Import direto falhou ({import_exc}); usando subprocess...")
            script = PROJECT_ROOT / "scripts" / "clients" / "szv" / "szv_seed_performance.py"
            cmd = [sys.executable, str(script), "--apply" if apply else "--dry-run"]
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=str(PROJECT_ROOT),
            )
            assert proc.stdout is not None
            for line in proc.stdout:
                _log(on_log, line.rstrip())
            return int(proc.wait())
