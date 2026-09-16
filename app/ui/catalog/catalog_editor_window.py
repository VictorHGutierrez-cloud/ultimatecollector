#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Janela secundária para editar catalog.json."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Dict, Optional

import customtkinter as ctk

from app.services.catalog_service import CatalogService
from app.ui.catalog.tabs.cast_tab import CastTab
from app.ui.catalog.tabs.location_tab import LocationTab
from app.ui.catalog.tabs.raw_json_tab import RawJsonTab
from app.ui.catalog.tabs.teams_tab import TeamsTab


class CatalogEditorWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        client_id: str,
        on_saved: Optional[Callable[[], None]] = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.client_id = client_id
        self.on_saved = on_saved
        self.catalog: Dict[str, Any] = {}

        self.title(f"Editar Demo — {client_id}")
        self.geometry("900x650")
        self.minsize(700, 500)

        self.status = ctk.CTkLabel(self, text="", text_color="gray")
        self.status.pack(anchor="w", padx=12, pady=(8, 0))

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=8)

        self.location_tab = LocationTab(self.tabs.add("Location"))
        self.location_tab.pack(fill="both", expand=True)
        self.teams_tab = TeamsTab(self.tabs.add("Teams"))
        self.teams_tab.pack(fill="both", expand=True)
        self.cast_tab = CastTab(self.tabs.add("Cast"))
        self.cast_tab.pack(fill="both", expand=True)
        self.raw_tab = RawJsonTab(self.tabs.add("JSON bruto"))
        self.raw_tab.pack(fill="both", expand=True)

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=12, pady=(0, 12))
        ctk.CTkButton(buttons, text="Recarregar", command=self.reload).pack(side="left")
        ctk.CTkButton(buttons, text="Salvar", command=self.save).pack(side="right")

        self.reload()

    def reload(self) -> None:
        try:
            self.catalog = CatalogService.load(self.client_id)
            self.location_tab.load(self.catalog)
            self.teams_tab.load(self.catalog)
            self.cast_tab.load(self.catalog)
            self.raw_tab.load(self.catalog)
            self.status.configure(text="Catalog carregado.", text_color="green")
        except Exception as exc:
            self.status.configure(text=f"Erro ao carregar: {exc}", text_color="orange")

    def save(self) -> None:
        try:
            # Se a aba JSON estiver ativa, ela é a fonte da verdade
            current = self.tabs.get()
            if current == "JSON bruto":
                catalog = self.raw_tab.get_catalog()
            else:
                catalog = deepcopy(self.catalog)
                self.location_tab.apply_to(catalog)
                self.teams_tab.apply_to(catalog)
                self.cast_tab.apply_to(catalog)
                # sincroniza raw também
                self.raw_tab.load(catalog)

            path = CatalogService.save(self.client_id, catalog)
            self.catalog = catalog
            self.status.configure(text=f"Salvo em {path} (+ .bak)", text_color="green")
            if self.on_saved:
                self.on_saved()
        except Exception as exc:
            self.status.configure(text=f"Erro ao salvar: {exc}", text_color="orange")
