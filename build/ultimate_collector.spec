# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec — Ultimate Collector Desktop (onedir)."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None
ROOT = Path(SPECPATH).resolve().parent

datas = []
binaries = []
hiddenimports = [
    "customtkinter",
    "darkdetect",
    "pandas",
    "openpyxl",
    "requests",
    "dotenv",
    "urllib3",
    "ultimate_collector",
    "ultimate_collector.core",
    "ultimate_collector.core.api_client",
    "ultimate_collector.core.client_config",
    "ultimate_collector.core.config",
    "ultimate_collector.core.paths",
    "ultimate_collector.collectors",
    "ultimate_collector.collectors.hr_data_masterultimate",
    "ultimate_collector.senders",
    "ultimate_collector.senders.attendance_sender",
    "ultimate_collector.senders.ultimate_sender",
    "ultimate_collector.services",
    "ultimate_collector.services.sandbox_runner",
    "app",
    "app.ui",
    "app.ui.app_window",
    "app.ui.token_panel",
    "app.ui.collect_panel",
    "app.ui.send_panel",
    "app.ui.seed_panel",
    "app.ui.log_panel",
    "app.ui.catalog.catalog_editor_window",
    "app.services.threading_runner",
    "app.services.catalog_service",
]

# CustomTkinter assets
ctk_datas, ctk_binaries, ctk_hidden = collect_all("customtkinter")
datas += ctk_datas
binaries += ctk_binaries
hiddenimports += ctk_hidden
hiddenimports += collect_submodules("ultimate_collector")

a = Analysis(
    [str(ROOT / "app" / "main.py")],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="UltimateCollector",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="UltimateCollector",
)
