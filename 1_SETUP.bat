@echo off
title Palworld Auto-Fisher - SETUP (run this once)
cd /d "%~dp0"
echo ==================================================
echo    PALWORLD AUTO-FISHER  -  one-time setup
echo    This installs everything the fisher needs.
echo ==================================================
echo.

rem ---- Find Python ----
set "PYCMD="
py -3 --version >nul 2>&1 && set "PYCMD=py -3"
if not defined PYCMD ( python --version >nul 2>&1 && set "PYCMD=python" )

if not defined PYCMD (
    echo Python isn't installed yet. Trying to install it for you...
    echo.
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    echo.
    echo --------------------------------------------------
    echo  If Python installed: CLOSE this window and run
    echo  1_SETUP again.
    echo.
    echo  If that didn't work, install Python yourself from
    echo  https://www.python.org/downloads/  ^(tick "Add
    echo  Python to PATH" during install^), then run 1_SETUP.
    echo --------------------------------------------------
    pause
    exit /b
)

echo Found Python. Building the fisher's little environment...
%PYCMD% -m venv venv
if errorlevel 1 ( echo Could not create the environment. & pause & exit /b )

echo Installing what it needs ^(this can take a minute^)...
"venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
"venv\Scripts\python.exe" -m pip install --quiet mss numpy pynput
if errorlevel 1 ( echo Install failed - check your internet and try again. & pause & exit /b )

echo.
echo ==================================================
echo    All set!  To fish, double-click:  2_PLAY.bat
echo ==================================================
pause
