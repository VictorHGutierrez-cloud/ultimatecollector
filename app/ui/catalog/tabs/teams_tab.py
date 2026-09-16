#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aba de times (teams)."""

from __future__ import annotations

from typing import Any, Dict, List

import customtkinter as ctk


class TeamsTab(ctk.CTkFrame):
    COLS = ("key", "name", "lead")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(
            self,
            text="Teams (um por linha: key | name | lead)",
            font=ctk.CTkFont(weight="bold"),
        ).pack(anchor="w", padx=8, pady=(8, 4))
        self.text = ctk.CTkTextbox(self, wrap="none")
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def load(self, catalog: Dict[str, Any]) -> None:
        teams: List[Dict[str, Any]] = catalog.get("teams", []) or []
        lines = ["key|name|lead"]
        for team in teams:
            lines.append(
                f"{team.get('key', '')}|{team.get('name', '')}|{team.get('lead', '')}"
            )
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "\n".join(lines))

    def apply_to(self, catalog: Dict[str, Any]) -> None:
        raw = self.text.get("1.0", "end").strip().splitlines()
        teams: List[Dict[str, str]] = []
        for i, line in enumerate(raw):
            line = line.strip()
            if not line or i == 0 and line.lower().startswith("key|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            while len(parts) < 3:
                parts.append("")
            teams.append({"key": parts[0], "name": parts[1], "lead": parts[2]})
        catalog["teams"] = teams
