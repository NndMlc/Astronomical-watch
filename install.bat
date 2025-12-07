@echo off
REM Windows Installation Script for Astronomical Watch

echo ================================
echo Astronomical Watch - Installation
echo ================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if pyproject.toml exists in current directory
if not exist "pyproject.toml" (
    echo ERROR: pyproject.toml not found!
    echo Please run this script from the Astronomical-watch directory.
    echo.
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.11 or newer from https://www.python.org
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed.
    echo Please reinstall Python with pip included.
    pause
    exit /b 1
)

echo Found pip:
pip --version
echo.

REM Install the package
echo Installing Astronomical Watch...
echo Installing from: %CD%
echo.
pip install --upgrade .
if errorlevel 1 (
    echo.
    echo ERROR: Installation failed.
    echo Please check the error messages above.
    echo.
    echo Make sure you are running this script from the Astronomical-watch directory.
    pause
    exit /b 1
)

echo.
echo ================================
echo Installation complete!
echo ================================
echo.
echo You can now run the application by typing:
echo   astronomical-watch
echo.
echo Or create a desktop shortcut:
echo   1. Right-click on Desktop - New - Shortcut
echo   2. Enter: pythonw -m astronomical_watch.ui.main
echo   3. Name it "Astronomical Watch"
echo.
echo To uninstall: pip uninstall astronomical-watch
echo.
pause
