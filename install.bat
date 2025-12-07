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

REM Create desktop shortcut
echo Creating desktop shortcut...

REM Get Python path
for /f "delims=" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%i
set PYTHONW_PATH=%PYTHON_PATH:python.exe=pythonw.exe%

REM Get desktop path
for /f "usebackq tokens=3*" %%A in (`reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop`) do set DESKTOP=%%B
call set DESKTOP=%DESKTOP%

REM Get current directory (where script is)
set INSTALL_DIR=%CD%

REM Create VBScript to make shortcut with icon
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\Astronomical Watch.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%PYTHONW_PATH%" >> CreateShortcut.vbs
echo oLink.Arguments = "-m astronomical_watch.ui.main" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.IconLocation = "%INSTALL_DIR%\icons\astronomical_watch.ico" >> CreateShortcut.vbs
echo oLink.Description = "Astronomical Watch - Astronomical Time Tracking" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Execute VBScript
cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo Desktop shortcut created!
echo.
echo You can now:
echo   1. Double-click "Astronomical Watch" on your Desktop
echo   2. Or type: astronomical-watch in Command Prompt
echo.
echo To uninstall: pip uninstall astronomical-watch
echo (and delete the desktop shortcut)
echo.
pause
