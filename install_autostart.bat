@echo off
REM Astronomical Watch - Windows Autostart Installer
REM Automatically installs widget to Windows Startup folder

echo ========================================
echo  ASTRONOMICAL WATCH AUTOSTART INSTALLER
echo ========================================
echo.

REM Navigate to application directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    echo Please install Python 3.6+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if widget script exists
if not exist "astronomical_watch_widget_only.py" (
    echo Error: Widget script not found!
    echo Please run this from the Astronomical Watch directory
    echo.
    pause
    exit /b 1
)

echo [OK] Widget script found
echo.

REM Get Startup folder path
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
echo Startup folder: %STARTUP_FOLDER%
echo.

REM Create VBScript launcher (silent, no console window)
set "VBS_FILE=%~dp0launch_widget_silent.vbs"
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.CurrentDirectory = "%~dp0"
echo WshShell.Run "pythonw.exe astronomical_watch_widget_only.py", 0, False
echo Set WshShell = Nothing
) > "%VBS_FILE%"

echo [OK] Created silent launcher
echo.

REM Create shortcut using PowerShell
echo Creating startup shortcut...
powershell -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTUP_FOLDER%\Astronomical Watch Widget.lnk'); $s.TargetPath = '%VBS_FILE%'; $s.WorkingDirectory = '%~dp0'; $s.Description = 'Astronomical Watch Widget - Universal Time Display'; $s.WindowStyle = 7; if (Test-Path '%~dp0icons\astronomical_watch.ico') { $s.IconLocation = '%~dp0icons\astronomical_watch.ico' }; $s.Save()"

if errorlevel 1 (
    echo.
    echo Warning: Could not create shortcut automatically
    echo.
    echo Manual installation steps:
    echo 1. Press Win+R and type: shell:startup
    echo 2. Create a shortcut to: %VBS_FILE%
    echo.
    pause
    exit /b 1
)

echo [OK] Shortcut created
echo.
echo ========================================
echo   INSTALLATION SUCCESSFUL!
echo ========================================
echo.
echo The Astronomical Watch widget will now:
echo   * Start automatically when Windows boots
echo   * Run silently in the background (no console)
echo   * Stay always on top (visible on desktop)
echo.
echo To test now, run:
echo   python astronomical_watch_widget_only.py
echo.
echo To remove autostart:
echo   1. Press Win+R
echo   2. Type: shell:startup
echo   3. Delete 'Astronomical Watch Widget.lnk'
echo.
pause
