@echo off
REM Test launcher to diagnose issues

echo ================================
echo Astronomical Watch - Test Launch
echo ================================
echo.

REM Find Python
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

echo Python found at:
where python
echo.

REM Try to launch with visible console
echo Attempting to launch (console will show errors)...
echo.
python -m astronomical_watch.ui.main

if errorlevel 1 (
    echo.
    echo ERROR: Launch failed!
    echo.
    echo Please check if:
    echo  1. Package is installed: pip list | findstr astronomical
    echo  2. Tkinter is available: python -m tkinter
    echo.
)

pause
