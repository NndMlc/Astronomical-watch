@echo off
setlocal enabledelayedexpansion
REM Astronomical Watch - Complete Windows Installer

cls
echo ========================================
echo   ASTRONOMICAL WATCH - INSTALLATION
echo ========================================
echo.
echo This will:
echo   1. Install Astronomical Watch Python package
echo   2. Create desktop shortcut with icon
echo   3. Verify installation
echo.
pause
echo.

REM ====================================
REM Step 1: Check Directory
REM ====================================
cd /d "%~dp0"

if not exist "pyproject.toml" (
    echo X ERROR: Installation files not found!
    echo.
    echo Please run this script from the Astronomical-watch folder
    echo where pyproject.toml is located.
    echo.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo + Installation files found
echo   Directory: %CD%
echo.

REM ====================================
REM Step 2: Check Python
REM ====================================
echo Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo X ERROR: Python not found!
    echo.
    echo Please install Python 3.11 or newer from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

for /f "delims=" %%v in ('python --version 2^>^&1') do set PYTHON_VER=%%v
echo + %PYTHON_VER% found
echo.

REM ====================================
REM Step 3: Check pip
REM ====================================
echo Checking pip...

pip --version >nul 2>&1
if errorlevel 1 (
    echo X ERROR: pip not found!
    echo.
    echo Please reinstall Python with pip included.
    echo.
    pause
    exit /b 1
)

for /f "delims=" %%v in ('pip --version 2^>^&1') do set PIP_VER=%%v
echo + %PIP_VER%
echo.

REM ====================================
REM Step 4: Install Package
REM ====================================
echo ========================================
echo Installing Astronomical Watch...
echo ========================================
echo.
echo This may take a minute...
echo.

pip install --upgrade --force-reinstall .

REM Check errorlevel IMMEDIATELY before any other command
if errorlevel 1 (
    echo.
    echo X INSTALLATION FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo.
    echo Common issues:
    echo   - No internet connection (for downloading dependencies)
    echo   - Antivirus blocking installation
    echo   - Insufficient permissions (try running as Administrator)
    echo.
    pause
    exit /b 1
)

REM If we reach here, installation was successful
echo.
cls
echo ========================================
echo Installation finished - checking result...
echo ========================================
echo.

echo.
echo ========================================
echo + INSTALLATION SUCCESSFUL!
echo ========================================
echo.

REM ====================================
REM Step 5: Create Shortcut
REM ====================================
echo ========================================
echo Creating Desktop Shortcut...
echo ========================================
echo.

REM Create shortcut in the current directory (install folder)
set SHORTCUT_DIR=%CD%
echo Creating shortcut at: %SHORTCUT_DIR%
echo.

REM ====================================
REM Step 6: Get Python Paths
REM ====================================
echo Finding Python executable...

for /f "delims=" %%i in ('python -c "import sys; print(sys.executable)" 2^>nul') do set PYTHON_PATH=%%i

if not defined PYTHON_PATH (
    echo X Could not find Python executable
    echo Shortcut not created
    goto :finish
)

set PYTHONW_PATH=!PYTHON_PATH:python.exe=pythonw.exe!

if not exist "!PYTHONW_PATH!" (
    echo ! pythonw.exe not found
    echo Using python.exe instead (will show console window)
    set PYTHONW_PATH=!PYTHON_PATH!
)

echo + Python executable: !PYTHONW_PATH!
echo.

REM ====================================
REM Step 7: Find Icon
REM ====================================
set ICON_PATH=
if exist "%CD%\icons\astronomical_watch.ico" (
    set ICON_PATH=%CD%\icons\astronomical_watch.ico
    echo + Icon found: !ICON_PATH!
) else (
    echo ! Icon not found (shortcut will use default icon)
)
echo.

REM ====================================
REM Step 8: Create Shortcut
REM ====================================
echo Creating shortcut...

REM Create VBScript to make shortcut in current directory
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "!SHORTCUT_DIR!\Astronomical Watch.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "!PYTHONW_PATH!" >> CreateShortcut.vbs
echo oLink.Arguments = "-m astronomical_watch.ui.main" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "!SHORTCUT_DIR!" >> CreateShortcut.vbs
if defined ICON_PATH (
    echo oLink.IconLocation = "!ICON_PATH!" >> CreateShortcut.vbs
)
echo oLink.Description = "Astronomical Watch - Astronomical Time System" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Execute VBScript
cscript //nologo CreateShortcut.vbs >nul 2>&1

REM Clean up
del CreateShortcut.vbs >nul 2>&1

REM Verify shortcut was created
if exist "!SHORTCUT_DIR!\Astronomical Watch.lnk" (
    echo + Shortcut created successfully!
    echo   Location: !SHORTCUT_DIR!\Astronomical Watch.lnk
    echo.
    echo   ^=^=^> You can now copy this shortcut to your Desktop!
) else (
    echo X Failed to create shortcut
    echo   You can run: astronomical-watch from Command Prompt
)

echo.

REM ====================================
REM Step 9: Verify Installation
REM ====================================
:finish
echo ========================================
echo Verifying installation...
echo ========================================
echo.

pip show astronomical-watch >nul 2>&1
if errorlevel 1 (
    echo X Package verification failed
    echo   The package was installed but pip cannot find it.
    echo   Try running: astronomical-watch
    echo.
    goto :show_final_message
)

for /f "tokens=2" %%v in ('pip show astronomical-watch ^| findstr "^Version:"') do set PKG_VER=%%v
echo + Astronomical Watch v!PKG_VER! installed

REM Get installation location
for /f "tokens=2*" %%a in ('pip show astronomical-watch ^| findstr "^Location:"') do set PKG_LOCATION=%%b
echo + Installation location: !PKG_LOCATION!
echo.

REM ====================================
REM Installation Complete
REM ====================================
echo ========================================
echo   INSTALLATION COMPLETE!
echo ========================================
echo.
echo Python: !PYTHON_VER!
echo Package: Astronomical Watch v!PKG_VER!
echo Installed at: !PKG_LOCATION!
echo.
if exist "!SHORTCUT_DIR!\Astronomical Watch.lnk" (
    echo Shortcut created: !SHORTCUT_DIR!\Astronomical Watch.lnk
    echo.
    echo ^=^=^> COPY THIS SHORTCUT TO YOUR DESKTOP!
    echo      Right-click "Astronomical Watch.lnk" in this folder
    echo      and drag it to your Desktop or any other location.
) else (
    echo Shortcut: Not created (you can run from Command Prompt)
)
echo.
echo ========================================
echo   HOW TO USE
echo ========================================
echo.
if exist "!SHORTCUT_DIR!\Astronomical Watch.lnk" (
    echo 1. Copy "Astronomical Watch.lnk" to your Desktop
    echo    Then double-click it ^(Runs without console window^)
    echo.
)
echo 2. Or from Command Prompt: astronomical-watch
echo    ^(Shows console with any error messages^)
echo.
echo 3. Widget Mode: Small floating display
echo    - Double-click to open full interface
echo    - Right-click for menu
echo.
echo To uninstall: Run uninstall.bat
echo.
echo ========================================
echo.

:show_final_message
set /p LAUNCH="Launch now? (Y/N): "
if /i "!LAUNCH!"=="Y" (
    echo.
    echo Starting Astronomical Watch...
    start "" "!PYTHONW_PATH!" -m astronomical_watch.ui.main
    echo.
    echo Application started!
    timeout /t 2 >nul
)

echo.
echo Press any key to exit...
pause >nul
