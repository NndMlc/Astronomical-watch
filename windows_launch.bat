@echo off
title Astronomical Watch mikroDies - Windows Launch
color 0B
echo.
echo ================================================
echo    ASTRONOMICAL WATCH DESKTOP - WINDOWS
echo ================================================
echo.
echo 🌟 Launching mikroDies precision desktop widget...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nije pronađen!
    echo.
    echo Molimo instaliraj Python sa https://python.org/downloads/
    echo Tokom instalacije štikliraj "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✓ Python pronađen
echo.

REM Test tkinter compatibility FIRST
echo 🔍 Testiram tkinter kompatibilnost...
python -c "import tkinter; print('tkinter OK')" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  tkinter nije dostupan - koristim console verziju
    echo.
    echo 📟 Pokretam console Astronomical Watch...
    if exist "awatch_console.py" (
        python awatch_console.py
    ) else (
        echo ❌ awatch_console.py nije pronađen!
        echo Molimo kopiraj awatch_console.py u isti folder
        pause
        exit /b 1
    )
    goto :end
)

echo ✓ tkinter je dostupan - mogu koristiti GUI verziju
echo.

REM Try to run the Windows optimized version first
if exist "awatch_windows.py" (
    echo ▶️  Pokretam Windows kompatibilnu verziju...
    python awatch_windows.py
) else if exist "windows_awatch.py" (
    echo ▶️  Pokretam Windows optimizovanu verziju...
    python windows_awatch.py
) else if exist "standalone_desktop.py" (
    echo ▶️  Pokretam standalone verziju...
    python standalone_desktop.py
) else if exist "desktop_app.py" (
    echo ▶️  Pokretam glavnu desktop aplikaciju...
    python desktop_app.py
) else (
    echo ❌ Nijedna desktop aplikacija nije pronađena!
    echo.
    echo Potrebni fajlovi:
    echo - awatch_windows.py (PREPORUČENO za Windows)
    echo - windows_awatch.py 
    echo - standalone_desktop.py 
    echo - desktop_app.py
    echo.
    pause
    exit /b 1
)

:end
echo.
echo 👋 Desktop aplikacija zatvorena
pause