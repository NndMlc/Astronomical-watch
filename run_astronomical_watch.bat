@echo off
REM Astronomical Watch Desktop Launcher for Windows
echo ========================================
echo  ASTRONOMICAL WATCH DESKTOP LAUNCHER
echo ========================================
echo.
echo New widget features:
echo - 160x90 compact size
echo - Dies.miliDies format (with dot)
echo - DejaVu Sans Mono font, 28px, black border
echo - mikroDies progress bar (0-999)
echo - Localized title
echo.
echo Checking Python version...
python --version
echo.
echo Starting Astronomical Watch...
python astronomical_watch_desktop.py
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✓ Application started successfully!
) else (
    echo ✗ Application failed to start.
    echo.
    echo Troubleshooting tips:
    echo - Make sure Python 3.6+ is installed
    echo - Check that tkinter is available
    echo - Try running: python -m tkinter
)
echo.
pause