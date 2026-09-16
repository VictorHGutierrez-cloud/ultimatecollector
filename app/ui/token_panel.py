#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Painel de token / cliente / autenticação."""

from __future__ import annotations

from typing import Callable, Optional

import customtkinter as ctk

from ultimate_collector.services.sandbox_runner import SandboxRunner


class TokenPanel(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_client_changed: Optional[Callable[[str], None]] = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.on_client_changed = on_client_changed

        ctk.CTkLabel(self, text="Conexao", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=8, pady=(8, 4)
        )

        ctk.CTkLabel(self, text="Cliente").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        clients = SandboxRunner.list_clients() or ["africa"]
        self.client_var = ctk.StringVar(value=clients[0])
        self.client_menu = ctk.CTkOptionMenu(
            self,
            values=clients,
            variable=self.client_var,
            command=self._client_changed,
        )
        self.client_menu.grid(row=1, column=1, sticky="ew", padx=8, pady=4)

        ctk.CTkLabel(self, text="Auth").grid(row=1, column=2, sticky="w", padx=8, pady=4)
        self.auth_var = ctk.StringVar(value="x-api-key")
        self.auth_menu = ctk.CTkOptionMenu(
            self,
            values=["x-api-key", "bearer"],
            variable=self.auth_var,
        )
        self.auth_menu.grid(row=1, column=3, sticky="ew", padx=8, pady=4)

        ctk.CTkLabel(self, text="URL").grid(row=2, column=0, sticky="w", padx=8, pady=4)
        self.url_entry = ctk.CTkEntry(self)
        self.url_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=8, pady=4)

        ctk.CTkLabel(self, text="Token").grid(row=3, column=0, sticky="w", padx=8, pady=4)
        self.token_entry = ctk.CTkEntry(self, show="*")
        self.token_entry.grid(row=3, column=1, columnspan=3, sticky="ew", padx=8, pady=4)

        self.status_label = ctk.CTkLabel(self, text="Sem teste ainda", text_color="gray")
        self.status_label.grid(row=4, column=0, columnspan=4, sticky="w", padx=8, pady=(0, 8))

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self._load_profile_defaults(clients[0])

    def _client_changed(self, client_id: str) -> None:
        self._load_profile_defaults(client_id)
        if self.on_client_changed:
            self.on_client_changed(client_id)

    def _load_profile_defaults(self, client_id: str) -> None:
        try:
            profile = SandboxRunner.load_profile(client_id)
            api = profile.api or {}
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, api.get("base_url", ""))
            self.auth_var.set(api.get("auth_type", "x-api-key"))
            self.status_label.configure(
                text=f"{profile.name} — company {profile.company_id}",
                text_color="gray",
            )
        except Exception as exc:
            self.status_label.configure(text=f"Erro ao carregar perfil: {exc}", text_color="orange")

    def get_client_id(self) -> str:
        return self.client_var.get().strip()

    def get_token(self) -> str:
        return self.token_entry.get().strip()

    def get_auth_type(self) -> str:
        return self.auth_var.get().strip()

    def get_base_url(self) -> str:
        return self.url_entry.get().strip()

    def set_status(self, text: str, ok: bool = True) -> None:
        self.status_label.configure(text=text, text_color=("green" if ok else "orange"))

    def refresh_clients(self, select_id: Optional[str] = None) -> None:
        clients = SandboxRunner.list_clients() or ["africa"]
        self.client_menu.configure(values=clients)
        chosen = select_id if select_id in clients else clients[0]
        self.client_var.set(chosen)
        self._load_profile_defaults(chosen)
        if self.on_client_changed:
            self.on_client_changed(chosen)

    def set_token(self, token: str) -> None:
        self.token_entry.delete(0, "end")
        if token:
            self.token_entry.insert(0, token)
