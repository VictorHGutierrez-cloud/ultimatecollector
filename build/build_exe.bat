@echo off
REM Gera o .exe do Ultimate Collector (modo onedir)
setlocal
cd /d "%~dp0\.."

echo.
echo === Ultimate Collector — Build EXE ===
echo Pasta do projeto: %CD%
echo.

python -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERRO: falha ao instalar dependencias.
  pause
  exit /b 1
)

echo.
echo Limpando builds anteriores...
if exist "dist\UltimateCollector" rmdir /s /q "dist\UltimateCollector"
if exist "build\pyi" rmdir /s /q "build\pyi"

echo.
echo Gerando executavel com PyInstaller...
python -m PyInstaller --noconfirm --clean --distpath dist --workpath build\pyi "build\ultimate_collector.spec"
if errorlevel 1 (
  echo ERRO: PyInstaller falhou.
  pause
  exit /b 1
)

echo.
echo Copiando pastas auxiliares ao lado do .exe...
set DEST=dist\UltimateCollector

REM clients (perfis; secrets podem existir localmente)
xcopy /E /I /Y "clients" "%DEST%\clients" >nul

REM config de exemplo (sem sobrescrever secrets reais se existirem)
if not exist "%DEST%\config" mkdir "%DEST%\config"
copy /Y "config\config.example.env" "%DEST%\config\config.example.env" >nul

REM assets OAS
xcopy /E /I /Y "assets" "%DEST%\assets" >nul

REM data base
if not exist "%DEST%\data" mkdir "%DEST%\data"
if not exist "%DEST%\data\clients" mkdir "%DEST%\data\clients"
if not exist "%DEST%\logs" mkdir "%DEST%\logs"

REM scripts de seed SZV (usados pelo SandboxRunner)
if not exist "%DEST%\scripts\clients\szv" mkdir "%DEST%\scripts\clients\szv"
xcopy /E /I /Y "scripts\clients\szv" "%DEST%\scripts\clients\szv" >nul
xcopy /E /I /Y "clients\szv" "%DEST%\clients\szv" >nul

echo.
echo OK! Executavel em:
echo   %CD%\%DEST%\UltimateCollector.exe
echo.
echo Dica: rode create_shortcut.ps1 para criar atalho na Area de Trabalho.
echo.
pause
