#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI unificado do Ultimate Collector.

Exemplos:
  python -m ultimate_collector clients list
  python -m ultimate_collector --client africa verify-token
  python -m ultimate_collector --client africa collect employees
  python -m ultimate_collector --client szv seed --dry-run
  python -m ultimate_collector menu
"""

from __future__ import annotations

import argparse
import sys

from ultimate_collector.core.client_config import (
    activate_client,
    list_clients,
    load_profile,
)
from ultimate_collector.core.paths import PROJECT_ROOT


def _ensure_project_root() -> None:
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)


def cmd_clients_list(_args: argparse.Namespace) -> int:
    clients = list_clients()
    if not clients:
        print("Nenhum cliente encontrado em clients/*/profile.json")
        return 1
    print("Clientes sandbox disponíveis:\n")
    for cid in clients:
        profile = load_profile(cid)
        seed = "sim" if profile.features.get("seed") else "nao"
        print(f"  {cid:12} {profile.name} (company {profile.company_id}) [seed: {seed}]")
    return 0


def cmd_clients_create(args: argparse.Namespace) -> int:
    from ultimate_collector.services.sandbox_runner import SandboxRunner

    try:
        result = SandboxRunner.create_from_token(
            api_key=args.token,
            display_name=args.name or None,
            client_id=args.client_id or None,
            auth_type=args.auth,
            base_url=args.url,
        )
    except Exception as exc:
        print(f"ERRO: {exc}")
        return 1

    action = "atualizado" if result.get("updated") else "criado"
    print(f"Cliente {action}: {result['client_id']}")
    print(f"Company ID: {result['company_id']}")
    print(f"Profile: {result['profile_path']}")
    print(f"Token:   {result['token_path']}")
    return 0


def cmd_verify_token(args: argparse.Namespace) -> int:
    from ultimate_collector.services.sandbox_runner import SandboxRunner

    result = SandboxRunner.verify_token(args.client)
    return 0 if result["has_token"] and result["match"] and result["connection_ok"] else 1


def cmd_collect(args: argparse.Namespace) -> int:
    from ultimate_collector.services.sandbox_runner import SandboxRunner

    return SandboxRunner.collect(args.client, categories=args.categories or None)


def cmd_send(args: argparse.Namespace) -> int:
    from ultimate_collector.services.sandbox_runner import SandboxRunner

    return SandboxRunner.send_attendance(args.client, employee_ids=args.employees)


def cmd_seed(args: argparse.Namespace) -> int:
    from ultimate_collector.services.sandbox_runner import SandboxRunner

    return SandboxRunner.seed_demo(args.client, apply=bool(args.apply))


def cmd_menu(_args: argparse.Namespace) -> int:
    from ultimate_collector.sandbox_menu import run_sandbox_menu

    return run_sandbox_menu()


def cmd_info(args: argparse.Namespace) -> int:
    profile = activate_client(args.client)
    print(f"ID:       {profile.id}")
    print(f"Nome:     {profile.name}")
    print(f"Company:  {profile.company_id}")
    print(f"API:      {profile.api.get('provider')} @ {profile.api.get('base_url')}")
    print(f"Dados:    {profile.data_path}")
    print(f"Collect:  {', '.join(profile.features.get('collect', []))}")
    print(f"Send:     {', '.join(profile.features.get('send', []))}")
    print(f"Seed:     {'sim' if profile.features.get('seed') else 'nao'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ultimate_collector",
        description="Ultimate Collector - sandbox editor CLI",
    )
    parser.add_argument(
        "--client", "-c",
        help="ID do cliente sandbox (africa, szv, ibero, presales)",
    )

    sub = parser.add_subparsers(dest="command")

    clients_parser = sub.add_parser("clients", help="Gerenciar clientes")
    clients_sub = clients_parser.add_subparsers(dest="clients_cmd")
    cl = clients_sub.add_parser("list", help="Listar clientes")
    cl.set_defaults(func=cmd_clients_list)

    cc = clients_sub.add_parser("create", help="Criar cliente a partir da API key")
    cc.add_argument("--token", required=True, help="API key JWT")
    cc.add_argument("--name", default="", help="Nome amigavel")
    cc.add_argument("--id", dest="client_id", default="", help="ID curto opcional")
    cc.add_argument("--auth", default="x-api-key", choices=["x-api-key", "bearer"])
    cc.add_argument("--url", default="https://api.eu2.demo.factorial.dev")
    cc.set_defaults(func=cmd_clients_create)

    sub.add_parser("menu", help="Menu interativo").set_defaults(func=cmd_menu)

    p = sub.add_parser("verify-token", help="Validar token")
    p.set_defaults(func=cmd_verify_token)

    p = sub.add_parser("info", help="Perfil do cliente")
    p.set_defaults(func=cmd_info)

    p = sub.add_parser("collect", help="Coletar dados")
    p.add_argument("categories", nargs="*", help="Categorias")
    p.set_defaults(func=cmd_collect)

    p = sub.add_parser("send", help="Enviar presenca")
    p.add_argument("--employees", type=lambda s: [int(x) for x in s.split(",")])
    p.set_defaults(func=cmd_send)

    p = sub.add_parser("seed", help="Popular sandbox demo")
    p.add_argument("--dry-run", action="store_true", help="Simular (padrao)")
    p.add_argument("--apply", action="store_true", help="Aplicar de verdade")
    p.set_defaults(func=cmd_seed)

    return parser


def main(argv: list[str] | None = None) -> int:
    _ensure_project_root()
    argv = list(argv if argv is not None else sys.argv[1:])

    if not argv:
        build_parser().print_help()
        return 0

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "clients":
        if args.clients_cmd == "list":
            return cmd_clients_list(args)
        if args.clients_cmd == "create":
            return cmd_clients_create(args)
        parser.parse_args(["clients", "--help"])
        return 0

    needs_client = {"verify-token", "info", "collect", "send", "seed"}
    if args.command in needs_client and not args.client:
        print(f"ERRO: comando '{args.command}' requer --client")
        return 1

    if hasattr(args, "func"):
        return args.func(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
