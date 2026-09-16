# Cria atalho na Area de Trabalho para UltimateCollector.exe
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$exe = Join-Path $root "dist\UltimateCollector\UltimateCollector.exe"

if (-not (Test-Path $exe)) {
    Write-Host "ERRO: executavel nao encontrado em:"
    Write-Host "  $exe"
    Write-Host "Rode antes: build\build_exe.bat"
    exit 1
}

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Ultimate Collector.lnk"

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $exe
$shortcut.WorkingDirectory = (Split-Path $exe)
$shortcut.Description = "Ultimate Collector — Editor de Ambientes Sandbox"
$shortcut.Save()

Write-Host "Atalho criado:"
Write-Host "  $shortcutPath"
Write-Host "Aponta para:"
Write-Host "  $exe"
