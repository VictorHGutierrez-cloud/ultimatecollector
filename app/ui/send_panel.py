#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Painel de envio de presença (clock in/out)."""

from __future__ import annotations

from typing import List

import customtkinter as ctk


class SendPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Enviar presenca", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=8, pady=(8, 4)
        )
        ctk.CTkLabel(self, text="IDs dos funcionarios (separados por virgula)").pack(
            anchor="w", padx=8
        )
        self.ids_entry = ctk.CTkEntry(self, placeholder_text="270105,270284")
        self.ids_entry.pack(fill="x", padx=8, pady=4)

        self.send_btn = ctk.CTkButton(self, text="Clock in / Clock out")
        self.send_btn.pack(anchor="w", padx=8, pady=(4, 8))

    def employee_ids(self) -> List[int]:
        raw = self.ids_entry.get().strip()
        if not raw:
            return []
        ids: List[int] = []
        for part in raw.split(","):
            part = part.strip()
            if part:
                ids.append(int(part))
        return ids

    def set_default_ids(self, ids: List[int]) -> None:
        if not ids:
            return
        if self.ids_entry.get().strip():
            return
        self.ids_entry.insert(0, ",".join(str(i) for i in ids))

    def set_enabled(self, enabled: bool) -> None:
        self.send_btn.configure(state="normal" if enabled else "disabled")
