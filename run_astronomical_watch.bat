@echo off
REM Astronomical Watch Desktop Launcher for Windows
echo ========================================
echo  ASTRONOMICAL WATCH DESKTOP LAUNCHER
echo ========================================
echo.
echo New widget features:
echo - 180x110 borderless overlay widget (NO title bar/navbar)
echo - Localized title ("Astronomical Watch" / "Astronomski sat")
echo - Dies.miliDies format with WHITE text + BLACK outline
echo - DejaVu Sans Mono font, 28px
echo - mikroDies progress bar (0-999) 
echo - Ultra-fast updates (86ms = 1 mikroDies)
echo - Drag widget to move (no title bar)
echo - DOUBLE-CLICK to open Normal Mode
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