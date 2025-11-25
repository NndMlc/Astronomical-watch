@echo off
REM Astronomical Watch Widget - Auto Startup
REM Place this file in Windows Startup folder to auto-start widget

echo ========================================
echo  ASTRONOMICAL WATCH WIDGET AUTO-START
echo ========================================
echo.

REM Navigate to application directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

echo Starting floating astronomical widget...
echo.

REM Launch widget directly
python astronomical_watch_widget_only.py

if errorlevel 1 (
    echo.
    echo Error starting widget. Press any key to exit...
    pause >nul
)