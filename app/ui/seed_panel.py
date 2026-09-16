#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Painel de seed/demo SZV."""

from __future__ import annotations

import customtkinter as ctk


class SeedPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Popular Demo", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=8, pady=(8, 4)
        )
        self.info = ctk.CTkLabel(
            self,
            text="Disponivel para clientes com seed=true (ex: SZV).",
            text_color="gray",
        )
        self.info.pack(anchor="w", padx=8)

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=8)

        self.dry_btn = ctk.CTkButton(row, text="Simular (dry-run)")
        self.dry_btn.pack(side="left", padx=(0, 8))

        self.apply_btn = ctk.CTkButton(row, text="Aplicar na API", fg_color="#b45309")
        self.apply_btn.pack(side="left", padx=(0, 8))

        self.edit_btn = ctk.CTkButton(row, text="Editar Demo")
        self.edit_btn.pack(side="left")

        self.progress = ctk.CTkLabel(self, text="", text_color="gray")
        self.progress.pack(anchor="w", padx=8, pady=(0, 8))

    def set_seed_available(self, available: bool, client_name: str = "") -> None:
        state = "normal" if available else "disabled"
        self.dry_btn.configure(state=state)
        self.apply_btn.configure(state=state)
        self.edit_btn.configure(state=state)
        if available:
            self.info.configure(text=f"Seed disponivel para {client_name}.")
        else:
            self.info.configure(text="Este cliente nao tem seed de demo.")

    def set_enabled(self, enabled: bool) -> None:
        if not enabled:
            self.dry_btn.configure(state="disabled")
            self.apply_btn.configure(state="disabled")
            self.edit_btn.configure(state="disabled")

    def set_progress(self, text: str) -> None:
        self.progress.configure(text=text)
