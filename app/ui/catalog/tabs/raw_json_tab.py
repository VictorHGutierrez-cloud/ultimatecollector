#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aba JSON bruto do catalog."""

from __future__ import annotations

import json
from typing import Any, Dict

import customtkinter as ctk


class RawJsonTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(
            self,
            text="JSON bruto (secoes avancadas: job_postings, trainings, etc.)",
            font=ctk.CTkFont(weight="bold"),
        ).pack(anchor="w", padx=8, pady=(8, 4))
        self.text = ctk.CTkTextbox(self, wrap="none")
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def load(self, catalog: Dict[str, Any]) -> None:
        self.text.delete("1.0", "end")
        self.text.insert("1.0", json.dumps(catalog, ensure_ascii=False, indent=2))

    def get_catalog(self) -> Dict[str, Any]:
        raw = self.text.get("1.0", "end").strip()
        return json.loads(raw)
