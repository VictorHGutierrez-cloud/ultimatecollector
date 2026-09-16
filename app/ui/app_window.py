#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Janela principal do Ultimate Collector Desktop."""

from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox

from app.services.threading_runner import ThreadingRunner
from app.ui.catalog.catalog_editor_window import CatalogEditorWindow
from app.ui.collect_panel import CollectPanel
from app.ui.log_panel import LogPanel
from app.ui.new_client_dialog import NewClientDialog
from app.ui.seed_panel import SeedPanel
from app.ui.send_panel import SendPanel
from app.ui.token_panel import TokenPanel
from ultimate_collector.core.config import Config
from ultimate_collector.services.sandbox_runner import SandboxRunner


class AppWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Ultimate Collector — Sandbox Editor")
        self.geometry("980x780")
        self.minsize(820, 640)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.runner = ThreadingRunner()
        self._catalog_window = None

        header = ctk.CTkLabel(
            self,
            text="Ultimate Collector — Editor de Ambientes Sandbox",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        header.pack(anchor="w", padx=16, pady=(14, 6))

        self.token_panel = TokenPanel(self, on_client_changed=self._on_client_changed)
        self.token_panel.pack(fill="x", padx=12, pady=6)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=12, pady=4)
        self.test_btn = ctk.CTkButton(actions, text="Testar conexao", command=self._on_test)
        self.test_btn.pack(side="left", padx=(0, 8))
        self.save_token_btn = ctk.CTkButton(actions, text="Salvar token", command=self._on_save_token)
        self.save_token_btn.pack(side="left", padx=(0, 8))
        self.new_client_btn = ctk.CTkButton(
            actions,
            text="Novo cliente (pelo token)",
            command=self._on_new_client,
        )
        self.new_client_btn.pack(side="left")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=8)

        self.collect_panel = CollectPanel(self.tabs.add("Coletar"))
        self.collect_panel.pack(fill="both", expand=True)
        self.collect_panel.collect_btn.configure(command=self._on_collect)

        self.send_panel = SendPanel(self.tabs.add("Enviar"))
        self.send_panel.pack(fill="both", expand=True)
        self.send_panel.send_btn.configure(command=self._on_send)

        self.seed_panel = SeedPanel(self.tabs.add("Demo"))
        self.seed_panel.pack(fill="both", expand=True)
        self.seed_panel.dry_btn.configure(command=lambda: self._on_seed(apply=False))
        self.seed_panel.apply_btn.configure(command=lambda: self._on_seed(apply=True))
        self.seed_panel.edit_btn.configure(command=self._on_edit_catalog)

        self.log_panel = LogPanel(self)
        self.log_panel.pack(fill="both", expand=False, padx=12, pady=(0, 12))

        self._on_client_changed(self.token_panel.get_client_id())
        self.log_panel.append(
            "App iniciado. Use 'Novo cliente (pelo token)' para criar um ambiente so colando a API key."
        )

    def _credentials(self):
        return {
            "client_id": self.token_panel.get_client_id(),
            "api_key": self.token_panel.get_token() or None,
            "auth_type": self.token_panel.get_auth_type(),
            "base_url": self.token_panel.get_base_url() or None,
        }

    def _set_busy(self, busy: bool) -> None:
        enabled = not busy
        self.test_btn.configure(state="normal" if enabled else "disabled")
        self.save_token_btn.configure(state="normal" if enabled else "disabled")
        self.new_client_btn.configure(state="normal" if enabled else "disabled")
        self.collect_panel.set_enabled(enabled)
        self.send_panel.set_enabled(enabled)
        if enabled:
            self._refresh_seed_availability()
        else:
            self.seed_panel.set_enabled(False)

    def _ui_log(self, message: str) -> None:
        self.after(0, lambda: self.log_panel.append(message))

    def _on_client_changed(self, client_id: str) -> None:
        self._refresh_seed_availability()
        try:
            SandboxRunner.activate(client_id)
            Config.reload()
            self.send_panel.set_default_ids(list(Config.AUTO_ATTENDANCE_EMPLOYEES or []))
        except Exception:
            pass

    def _refresh_seed_availability(self) -> None:
        client_id = self.token_panel.get_client_id()
        try:
            profile = SandboxRunner.load_profile(client_id)
            self.seed_panel.set_seed_available(bool(profile.features.get("seed")), profile.name)
        except Exception:
            self.seed_panel.set_seed_available(False)

    def _on_test(self) -> None:
        if self.runner.busy:
            self.log_panel.append("Aguarde a operacao atual terminar.")
            return
        creds = self._credentials()
        if not creds["api_key"]:
            # tenta token salvo no cliente
            self.log_panel.append("Token vazio — tentando token salvo do cliente...")

        self._set_busy(True)
        self.log_panel.append(f"Testando conexao de '{creds['client_id']}'...")

        def work() -> int:
            result = SandboxRunner.verify_token(
                creds["client_id"],
                api_key=creds["api_key"],
                auth_type=creds["auth_type"],
                base_url=creds["base_url"],
                on_log=self._ui_log,
            )
            ok = bool(result.get("has_token") and result.get("connection_ok"))
            self.after(
                0,
                lambda: self.token_panel.set_status(
                    "Conexao OK" if ok else "Falha na conexao/token",
                    ok=ok,
                ),
            )
            return 0 if ok else 1

        self.runner.run(work, on_done=lambda _c: self.after(0, lambda: self._set_busy(False)))

    def _on_save_token(self) -> None:
        token = self.token_panel.get_token()
        client_id = self.token_panel.get_client_id()
        if not token:
            messagebox.showwarning("Token", "Cole um token antes de salvar.")
            return
        try:
            path = SandboxRunner.save_token(client_id, token)
            self.log_panel.append(f"Token salvo em {path}")
            messagebox.showinfo("Token", f"Token salvo em:\n{path}")
        except Exception as exc:
            messagebox.showerror("Token", str(exc))

    def _on_new_client(self) -> None:
        def after_created(result: dict) -> None:
            cid = result["client_id"]
            self.token_panel.refresh_clients(select_id=cid)
            # nao reexibir o token completo no campo se preferir; aqui deixamos vazio
            # porque ja foi salvo em secrets/
            self.token_panel.set_token("")
            action = "atualizado" if result.get("updated") else "criado"
            self.log_panel.append(
                f"Cliente {action}: {cid} (company {result['company_id']}) — token salvo."
            )
            self.log_panel.append(f"Profile: {result.get('profile_path')}")
            messagebox.showinfo(
                "Cliente pronto",
                f"Cliente '{cid}' {action}.\n"
                f"Company ID: {result['company_id']}\n"
                f"Pasta de arquivos: {result.get('asset_dir', '')}\n\n"
                "Agora clique em Testar conexao.",
            )

        NewClientDialog(
            self,
            on_created=after_created,
            default_url=self.token_panel.get_base_url()
            or "https://api.eu2.demo.factorial.dev",
            default_auth=self.token_panel.get_auth_type() or "x-api-key",
        )

    def _on_collect(self) -> None:
        if self.runner.busy:
            return
        cats = self.collect_panel.selected_categories()
        if not cats:
            messagebox.showwarning("Coletar", "Selecione ao menos uma categoria.")
            return
        creds = self._credentials()
        self._set_busy(True)
        self.log_panel.append(f"Iniciando coleta: {', '.join(cats)}")

        def work() -> int:
            return SandboxRunner.collect(
                creds["client_id"],
                categories=cats,
                api_key=creds["api_key"],
                auth_type=creds["auth_type"],
                base_url=creds["base_url"],
                on_log=self._ui_log,
            )

        self.runner.run(work, on_done=lambda _c: self.after(0, lambda: self._set_busy(False)))

    def _on_send(self) -> None:
        if self.runner.busy:
            return
        try:
            ids = self.send_panel.employee_ids()
        except ValueError:
            messagebox.showerror("Enviar", "IDs invalidos. Use numeros separados por virgula.")
            return
        if not ids:
            messagebox.showwarning("Enviar", "Informe ao menos um ID de funcionario.")
            return
        creds = self._credentials()
        self._set_busy(True)

        def work() -> int:
            return SandboxRunner.send_attendance(
                creds["client_id"],
                employee_ids=ids,
                api_key=creds["api_key"],
                auth_type=creds["auth_type"],
                base_url=creds["base_url"],
                on_log=self._ui_log,
            )

        self.runner.run(work, on_done=lambda _c: self.after(0, lambda: self._set_busy(False)))

    def _on_seed(self, apply: bool) -> None:
        if self.runner.busy:
            return
        if apply:
            ok = messagebox.askokcancel(
                "Aplicar na API",
                "ATENCAO: isso ESCREVE dados na API demo.\n\nDeseja continuar?",
            )
            if not ok:
                return
            # Pedido de confirmacao SIM
            dialog = ctk.CTkInputDialog(
                text="Digite SIM para confirmar o apply:",
                title="Confirmacao",
            )
            answer = dialog.get_input()
            if not answer or answer.strip().upper() != "SIM":
                self.log_panel.append("Apply cancelado (confirmacao != SIM).")
                return

        creds = self._credentials()
        self._set_busy(True)
        mode = "apply" if apply else "dry-run"
        self.seed_panel.set_progress(f"Executando seed ({mode})...")
        self.log_panel.append(f"Iniciando seed ({mode})...")

        def work() -> int:
            return SandboxRunner.seed_demo(
                creds["client_id"],
                apply=apply,
                api_key=creds["api_key"],
                auth_type=creds["auth_type"],
                base_url=creds["base_url"],
                on_log=self._ui_log,
            )

        def done(_code: int) -> None:
            self._set_busy(False)
            self.seed_panel.set_progress("Concluido.")

        self.runner.run(work, on_done=lambda c: self.after(0, lambda: done(c)))

    def _on_edit_catalog(self) -> None:
        client_id = self.token_panel.get_client_id()
        try:
            profile = SandboxRunner.load_profile(client_id)
            if not profile.catalog:
                messagebox.showinfo("Demo", "Este cliente nao tem catalog.json.")
                return
        except Exception as exc:
            messagebox.showerror("Demo", str(exc))
            return

        if self._catalog_window is not None and self._catalog_window.winfo_exists():
            self._catalog_window.focus()
            return

        self._catalog_window = CatalogEditorWindow(
            self,
            client_id=client_id,
            on_saved=lambda: self.log_panel.append("Catalog salvo com sucesso."),
        )
