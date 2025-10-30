@echo off
title Astronomical Watch - Desktop Widget Launcher
color 0B
echo.
echo ====================================================
echo    ASTRONOMICAL WATCH - DESKTOP WIDGET LAUNCHER
echo ====================================================
echo.
echo Zapocinje u widget mode-u sa dupli klik za normal mode!
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python nije pronađen!
    echo Instaliraj Python sa https://python.org/downloads/
    pause
    exit /b 1
)

echo Python OK
echo.

REM Test tkinter first
python -c "import tkinter; print('tkinter OK')" >nul 2>&1
if errorlevel 1 (
    echo tkinter nije dostupan - koristim console verziju
    echo.
    if exist "awatch_ultimate.py" (
        echo Pokretam ultimate verziju (console mode)...
        python awatch_ultimate.py
    ) else if exist "instant_awatch.py" (
        echo Pokretam instant console verziju...
        python instant_awatch.py
    ) else (
        echo ERROR: Nijedna console aplikacija nije pronađena!
        pause
        exit /b 1
    )
    goto :end
)

echo tkinter OK - pokrecem desktop widget aplikaciju
echo.

REM Try desktop widget versions in order
if exist "desktop_widget_app.py" (
    echo Pokretam Desktop Widget Aplikaciju...
    echo - Widget mode: Dupli klik za normal mode
    echo - Normal mode: 'Minimize to Widget' dugme
    echo.
    python desktop_widget_app.py
) else if exist "awatch_ultimate.py" (
    echo Pokretam ultimate verziju (GUI mode)...
    python awatch_ultimate.py
) else if exist "desktop_app.py" (
    echo Pokretam glavnu desktop aplikaciju...
    python desktop_app.py
) else (
    echo ERROR: Nijedna desktop aplikacija nije pronađena!
    echo.
    echo Potrebni fajlovi:
    echo - desktop_widget_app.py (WIDGET + NORMAL MODE)
    echo - awatch_ultimate.py
    echo - desktop_app.py
    echo.
    pause
    exit /b 1
)

:end
echo.
echo Desktop aplikacija zatvorena
pause