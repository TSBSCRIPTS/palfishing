@echo off
title Palworld Auto-Fisher
rem Auto-elevate to administrator (needed so the game accepts the mouse control).
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo It looks like setup hasn't been run yet.
    echo Please double-click 1_SETUP.bat first.
    pause
    exit /b
)
"venv\Scripts\python.exe" fisher.py
echo.
pause
