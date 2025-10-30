@echo off
title Astronomical Watch - Smart Windows Launcher
color 0B
echo.
echo =================================================
echo    ASTRONOMICAL WATCH - SMART WINDOWS LAUNCHER
echo =================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nije pronađen!
    echo Molimo instaliraj Python sa https://python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python pronađen
echo.

REM Test tkinter compatibility
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
        pause
        exit /b 1
    )
) else (
    echo ✓ tkinter je dostupan - koristim GUI verziju
    echo.
    echo 🖥️ Pokretam desktop Astronomical Watch...
    
    REM Try GUI versions in order of preference
    if exist "awatch_windows.py" (
        echo ▶️  Pokretam Windows GUI verziju...
        python awatch_windows.py
    ) else if exist "windows_awatch.py" (
        echo ▶️  Pokretam Windows optimizovanu verziju...
        python windows_awatch.py
    ) else if exist "standalone_desktop.py" (
        echo ▶️  Pokretam standalone verziju...
        python standalone_desktop.py
    ) else (
        echo ❌ Nijedna GUI aplikacija nije pronađena!
        echo Pokretam console verziju umesto toga...
        if exist "awatch_console.py" (
            python awatch_console.py
        ) else (
            echo ❌ Nijedna aplikacija nije pronađena!
            pause
            exit /b 1
        )
    )
)

echo.
echo 👋 Astronomical Watch zatvorena
pause