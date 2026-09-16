#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Painel de coleta de dados."""

from __future__ import annotations

from typing import List

import customtkinter as ctk


DEFAULT_CATEGORIES = [
    "employees",
    "finance",
    "expenses",
    "attendance",
    "performance",
    "trainings",
    "job_catalog",
    "tasks",
]


class CollectPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Coletar dados", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", padx=8, pady=(8, 4)
        )

        self.vars = {}
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=8, pady=4)
        for i, cat in enumerate(DEFAULT_CATEGORIES):
            var = ctk.BooleanVar(value=(cat == "employees"))
            self.vars[cat] = var
            ctk.CTkCheckBox(grid, text=cat, variable=var).grid(
                row=i // 4, column=i % 4, sticky="w", padx=6, pady=4
            )

        self.collect_btn = ctk.CTkButton(self, text="Coletar selecionados")
        self.collect_btn.pack(anchor="w", padx=8, pady=(4, 8))

    def selected_categories(self) -> List[str]:
        return [name for name, var in self.vars.items() if var.get()]

    def set_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.collect_btn.configure(state=state)
