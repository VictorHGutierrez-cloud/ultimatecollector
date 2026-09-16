#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dialogo: criar cliente automaticamente a partir da API key."""

from __future__ import annotations

from typing import Callable, Optional

import customtkinter as ctk

from ultimate_collector.services.sandbox_runner import SandboxRunner


class NewClientDialog(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        on_created: Optional[Callable[[dict], None]] = None,
        default_url: str = "https://api.eu2.demo.factorial.dev",
        default_auth: str = "x-api-key",
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.on_created = on_created

        self.title("Novo cliente pelo token")
        self.geometry("620x420")
        self.minsize(520, 360)
        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Cole a API key — o Company ID e lido automaticamente do token",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(16, 8))

        ctk.CTkLabel(self, text="Nome amigavel (opcional, ex: Acme Demo)").pack(
            anchor="w", padx=16
        )
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Acme Demo")
        self.name_entry.pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkLabel(self, text="ID curto (opcional, ex: acme)").pack(anchor="w", padx=16)
        self.id_entry = ctk.CTkEntry(self, placeholder_text="deixe vazio para gerar automatico")
        self.id_entry.pack(fill="x", padx=16, pady=(0, 8))

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row, text="Auth").pack(side="left")
        self.auth_var = ctk.StringVar(value=default_auth)
        ctk.CTkOptionMenu(row, values=["x-api-key", "bearer"], variable=self.auth_var).pack(
            side="left", padx=8
        )

        ctk.CTkLabel(self, text="URL da API").pack(anchor="w", padx=16)
        self.url_entry = ctk.CTkEntry(self)
        self.url_entry.pack(fill="x", padx=16, pady=(0, 8))
        self.url_entry.insert(0, default_url)

        ctk.CTkLabel(self, text="API Key / Token").pack(anchor="w", padx=16)
        self.token_entry = ctk.CTkEntry(self, show="*")
        self.token_entry.pack(fill="x", padx=16, pady=(0, 8))

        self.status = ctk.CTkLabel(self, text="", text_color="gray")
        self.status.pack(anchor="w", padx=16, pady=4)

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=16, pady=(8, 16))
        ctk.CTkButton(buttons, text="Cancelar", command=self.destroy).pack(side="left")
        ctk.CTkButton(buttons, text="Criar cliente", command=self._create).pack(side="right")

        self.after(100, lambda: self.token_entry.focus())

    def _create(self) -> None:
        token = self.token_entry.get().strip()
        if not token:
            self.status.configure(text="Cole a API key primeiro.", text_color="orange")
            return
        try:
            result = SandboxRunner.create_from_token(
                api_key=token,
                display_name=self.name_entry.get().strip() or None,
                client_id=self.id_entry.get().strip() or None,
                auth_type=self.auth_var.get(),
                base_url=self.url_entry.get().strip()
                or "https://api.eu2.demo.factorial.dev",
            )
            action = "atualizado" if result.get("updated") else "criado"
            self.status.configure(
                text=(
                    f"Cliente {action}: {result['client_id']} "
                    f"(company {result['company_id']})"
                ),
                text_color="green",
            )
            if self.on_created:
                self.on_created(result)
            self.after(400, self.destroy)
        except Exception as exc:
            self.status.configure(text=str(exc), text_color="orange")
