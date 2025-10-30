@echo off
title Astronomical Watch mikroDies Desktop
echo.
echo ========================================
echo   ASTRONOMICAL WATCH DESKTOP LAUNCHER
echo ========================================
echo.
echo Launching mikroDies precision desktop widget...
echo.

cd /d "%~dp0"

REM Try to run the most compatible version first
if exist "instant_awatch.py" (
    echo Running instant console version...
    python instant_awatch.py
) else if exist "awatch_console.py" (
    echo Running console version...
    python awatch_console.py
) else if exist "desktop_app.py" (
    echo Running main desktop application...
    python desktop_app.py
) else if exist "standalone_desktop.py" (
    echo Running standalone version...
    python standalone_desktop.py
) else (
    echo Error: No desktop application found!
    echo Please ensure one of these files exists:
    echo - instant_awatch.py (most compatible)
    echo - awatch_console.py
    echo - desktop_app.py
    echo - standalone_desktop.py
    pause
    exit /b 1
)

echo.
echo Desktop application closed.
pause