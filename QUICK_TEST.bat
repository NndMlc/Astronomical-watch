@echo off
REM Quick test - does Python work?

echo ================================
echo Quick Python Test
echo ================================
echo.

REM Test Python
echo Testing Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not working!
    pause
    exit /b 1
)

echo.
echo Python works!
echo.

REM Test if package is installed
echo Checking if astronomical-watch is installed...
pip show astronomical-watch >nul 2>&1
if errorlevel 1 (
    echo.
    echo Package NOT installed.
    echo Please run INSTALL_EASY.bat first.
    echo.
    pause
    exit /b 1
)

echo.
echo Package IS installed!
echo.

REM Show package info
pip show astronomical-watch

echo.
echo ================================
echo Everything looks good!
echo ================================
echo.
echo Press any key to try launching the app...
pause >nul

echo.
echo Launching with console visible (to see any errors)...
echo.

python -m astronomical_watch.ui.main

echo.
echo.
if errorlevel 1 (
    echo Application exited with an error!
) else (
    echo Application closed normally.
)
echo.
pause
