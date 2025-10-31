@echo off
REM Astronomical Watch Desktop Launcher for Windows
echo Starting Astronomical Watch...
echo Checking Python version...
python --version
echo.
echo Trying python astronomical_watch_desktop.py...
python astronomical_watch_desktop.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying python3 instead...
    python3 astronomical_watch_desktop.py
)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying py launcher...
    py astronomical_watch_desktop.py
)
pause