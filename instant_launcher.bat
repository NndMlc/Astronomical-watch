@echo off
title Astronomical Watch - Instant Windows Version
echo.
echo ============================================
echo   ASTRONOMICAL WATCH - INSTANT VERSION
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python nije pronađen!
    echo Instaliraj Python sa https://python.org/downloads/
    pause
    exit /b 1
)

echo Python OK - Pokretam Astronomical Watch...
echo.

REM Run instant version (no tkinter needed)
if exist "instant_awatch.py" (
    python instant_awatch.py
) else if exist "awatch_console.py" (
    python awatch_console.py
) else (
    echo ERROR: Nijedan awatch fajl nije pronađen!
    echo.
    echo Potreban fajl:
    echo - instant_awatch.py (preporučeno)
    echo - awatch_console.py
    echo.
    pause
    exit /b 1
)

echo.
echo Astronomical Watch zatvoren
pause