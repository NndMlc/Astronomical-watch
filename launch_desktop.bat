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

REM Try to run the main desktop app first
if exist "desktop_app.py" (
    echo Running main desktop application...
    python desktop_app.py
) else if exist "standalone_desktop.py" (
    echo Running standalone version...
    python standalone_desktop.py
) else (
    echo Error: No desktop application found!
    echo Please ensure desktop_app.py or standalone_desktop.py exists.
    pause
    exit /b 1
)

echo.
echo Desktop application closed.
pause