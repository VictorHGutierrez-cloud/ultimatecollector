#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu interativo do editor de ambientes sandbox (Fase 4).
"""

from __future__ import annotations

import subprocess
import sys

from ultimate_collector.core.client_config import activate_client, list_clients, load_profile
from ultimate_collector.core.config import Config
from ultimate_collector.core.paths import PROJECT_ROOT


def _pick_client() -> str | None:
    clients = list_clients()
    if not clients:
        print("Nenhum cliente configurado.")
        return None
    print("\nClientes sandbox:")
    for i, cid in enumerate(clients, 1):
        p = load_profile(cid)
        print(f"  {i}. {cid} — {p.name} (company {p.company_id})")
    print(f"  0. Sair")
    try:
        choice = input("\nEscolha o cliente (numero): ").strip()
    except (EOFError, KeyboardInterrupt):
        return None
    if choice == "0":
        return None
    try:
        idx = int(choice) - 1
        return clients[idx]
    except (ValueError, IndexError):
        print("Opcao invalida.")
        return None


def _show_actions(client_id: str) -> None:
    profile = load_profile(client_id)
    print(f"\n{'=' * 60}")
    print(f"SANDBOX: {profile.name} [{client_id}]")
    print(f"Company ID: {profile.company_id}")
    print(f"Dados em:   {profile.data_path}")
    print("=" * 60)
    print("1. Verificar token / conexao")
    print("2. Ver perfil do cliente")
    print("3. Coletar dados (employees)")
    print("4. Coletar categoria especifica")
    print("5. Enviar presenca (clock in/out)")
    if profile.features.get("seed"):
        print("6. Seed demo (dry-run)")
        print("7. Seed demo (APPLY — escreve na API!)")
    print("8. Menu completo Ultimate Collector (28 funcoes)")
    print("9. Ultimate Sender (OAS)")
    print("0. Trocar cliente / Sair")


def run_sandbox_menu() -> int:
    print("\n" + "=" * 60)
    print("  EDITOR DE AMBIENTES SANDBOX — Ultimate Collector")
    print("=" * 60)

    client_id = _pick_client()
    if not client_id:
        return 0

    activate_client(client_id)

    while True:
        _show_actions(client_id)
        try:
            choice = input("\nOpcao: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAte logo!")
            return 0

        if choice == "0":
            new_client = _pick_client()
            if not new_client:
                return 0
            client_id = new_client
            activate_client(client_id)
            continue

        if choice == "1":
            from ultimate_collector.cli import cmd_verify_token
            import argparse

            cmd_verify_token(argparse.Namespace(client=client_id))
        elif choice == "2":
            from ultimate_collector.cli import cmd_info
            import argparse

            cmd_info(argparse.Namespace(client=client_id))
        elif choice == "3":
            from ultimate_collector.cli import cmd_collect
            import argparse

            cmd_collect(argparse.Namespace(client=client_id, categories=["employees"]))
        elif choice == "4":
            cat = input("Categoria (ex: finance, attendance): ").strip()
            if cat:
                from ultimate_collector.cli import cmd_collect
                import argparse

                cmd_collect(argparse.Namespace(client=client_id, categories=[cat]))
        elif choice == "5":
            from ultimate_collector.cli import cmd_send
            import argparse

            ids_raw = input(
                f"IDs funcionarios [{','.join(str(x) for x in Config.AUTO_ATTENDANCE_EMPLOYEES) or 'vazio'}]: "
            ).strip()
            employees = (
                [int(x) for x in ids_raw.split(",") if x.strip()]
                if ids_raw
                else None
            )
            cmd_send(argparse.Namespace(client=client_id, employees=employees))
        elif choice == "6":
            from ultimate_collector.cli import cmd_seed
            import argparse

            cmd_seed(argparse.Namespace(client=client_id, dry_run=True, apply=False))
        elif choice == "7":
            confirm = input("ATENCAO: vai escrever na API! Digite SIM para confirmar: ")
            if confirm.upper() == "SIM":
                from ultimate_collector.cli import cmd_seed
                import argparse

                cmd_seed(argparse.Namespace(client=client_id, dry_run=False, apply=True))
        elif choice == "8":
            script = PROJECT_ROOT / "scripts" / "entry" / "ultimate_collector.py"
            subprocess.call([sys.executable, str(script)])
        elif choice == "9":
            script = PROJECT_ROOT / "scripts" / "entry" / "ultimate_sender.py"
            subprocess.call([sys.executable, str(script)])
        else:
            print("Opcao invalida.")

        try:
            input("\nEnter para continuar...")
        except (EOFError, KeyboardInterrupt):
            return 0


if __name__ == "__main__":
    raise SystemExit(run_sandbox_menu())
