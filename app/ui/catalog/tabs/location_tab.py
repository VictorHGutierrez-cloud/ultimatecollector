#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aba location + legal_entity."""

from __future__ import annotations

from typing import Any, Dict

import customtkinter as ctk


LOCATION_FIELDS = [
    "name",
    "country",
    "timezone",
    "city",
    "state",
    "postal_code",
    "address_line_one",
    "phone_number",
]

LEGAL_FIELDS = [
    "legal_name",
    "country",
    "currency",
    "city",
    "state",
    "postal_code",
    "address_line_1",
    "tin",
]


class LocationTab(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.location_entries: Dict[str, ctk.CTkEntry] = {}
        self.legal_entries: Dict[str, ctk.CTkEntry] = {}

        ctk.CTkLabel(self, text="Location", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w", padx=8, pady=(8, 4)
        )
        for field in LOCATION_FIELDS:
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", padx=8, pady=2)
            ctk.CTkLabel(row, text=field, width=140, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row)
            entry.pack(side="left", fill="x", expand=True)
            self.location_entries[field] = entry

        ctk.CTkLabel(self, text="Legal Entity", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w", padx=8, pady=(12, 4)
        )
        for field in LEGAL_FIELDS:
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", padx=8, pady=2)
            ctk.CTkLabel(row, text=field, width=140, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row)
            entry.pack(side="left", fill="x", expand=True)
            self.legal_entries[field] = entry

    def load(self, catalog: Dict[str, Any]) -> None:
        location = catalog.get("location", {}) or {}
        legal = catalog.get("legal_entity", {}) or {}
        for field, entry in self.location_entries.items():
            entry.delete(0, "end")
            entry.insert(0, str(location.get(field, "")))
        for field, entry in self.legal_entries.items():
            entry.delete(0, "end")
            entry.insert(0, str(legal.get(field, "")))

    def apply_to(self, catalog: Dict[str, Any]) -> None:
        location = dict(catalog.get("location", {}) or {})
        legal = dict(catalog.get("legal_entity", {}) or {})
        for field, entry in self.location_entries.items():
            location[field] = entry.get().strip()
        for field, entry in self.legal_entries.items():
            legal[field] = entry.get().strip()
        catalog["location"] = location
        catalog["legal_entity"] = legal
