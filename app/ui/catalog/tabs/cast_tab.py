#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aba do cast (funcionarios demo)."""

from __future__ import annotations

from typing import Any, Dict, List

import customtkinter as ctk


class CastTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(
            self,
            text="Cast (um por linha: full_name | email | team_key | role_title | gender)",
            font=ctk.CTkFont(weight="bold"),
        ).pack(anchor="w", padx=8, pady=(8, 4))
        self.text = ctk.CTkTextbox(self, wrap="none")
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def load(self, catalog: Dict[str, Any]) -> None:
        cast: List[Dict[str, Any]] = catalog.get("cast", []) or []
        lines = ["full_name|email|team_key|role_title|gender"]
        for person in cast:
            lines.append(
                "|".join(
                    [
                        str(person.get("full_name", "")),
                        str(person.get("email", "")),
                        str(person.get("team_key", "")),
                        str(person.get("role_title", "")),
                        str(person.get("gender", "")),
                    ]
                )
            )
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "\n".join(lines))

    def apply_to(self, catalog: Dict[str, Any]) -> None:
        existing = {p.get("email"): p for p in (catalog.get("cast") or []) if p.get("email")}
        raw = self.text.get("1.0", "end").strip().splitlines()
        cast: List[Dict[str, Any]] = []
        for i, line in enumerate(raw):
            line = line.strip()
            if not line or i == 0 and line.lower().startswith("full_name|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            while len(parts) < 5:
                parts.append("")
            full_name, email, team_key, role_title, gender = parts[:5]
            names = full_name.split(" ", 1)
            first = names[0] if names else ""
            last = names[1] if len(names) > 1 else ""
            base = dict(existing.get(email, {}))
            base.update(
                {
                    "full_name": full_name,
                    "first_name": first,
                    "last_name": last,
                    "email": email,
                    "team_key": team_key,
                    "role_title": role_title,
                    "gender": gender or base.get("gender", "female"),
                    "group": base.get("group", "staff"),
                    "goal_count": base.get("goal_count", 7),
                    "rename_from": base.get("rename_from"),
                }
            )
            cast.append(base)
        catalog["cast"] = cast
