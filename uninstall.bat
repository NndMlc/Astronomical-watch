@echo off
setlocal enabledelayedexpansion
REM Astronomical Watch - Uninstaller

cls
echo ========================================
echo   ASTRONOMICAL WATCH - UNINSTALL
echo ========================================
echo.
echo This will:
echo   - Remove the Python package
echo   - Delete the desktop shortcut (if exists)
echo.

set /p CONFIRM="Are you sure? (Y/N): "
if /i not "!CONFIRM!"=="Y" (
    echo.
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo ========================================
echo Uninstalling...
echo ========================================
echo.

REM Uninstall package
echo Removing package...
pip uninstall -y astronomical-watch >nul 2>&1

if errorlevel 1 (
    echo ! Package not found or already uninstalled
) else (
    echo + Package removed
)
echo.

REM Find and remove desktop shortcut
echo Removing desktop shortcut...

set SHORTCUT_FOUND=0

REM Try standard Desktop
if exist "%USERPROFILE%\Desktop\Astronomical Watch.lnk" (
    del "%USERPROFILE%\Desktop\Astronomical Watch.lnk" >nul 2>&1
    echo + Shortcut removed: %USERPROFILE%\Desktop
    set SHORTCUT_FOUND=1
)

REM Try OneDrive Desktop
if exist "%USERPROFILE%\OneDrive\Desktop\Astronomical Watch.lnk" (
    del "%USERPROFILE%\OneDrive\Desktop\Astronomical Watch.lnk" >nul 2>&1
    echo + Shortcut removed: %USERPROFILE%\OneDrive\Desktop
    set SHORTCUT_FOUND=1
)

REM Try Public Desktop
if exist "%PUBLIC%\Desktop\Astronomical Watch.lnk" (
    del "%PUBLIC%\Desktop\Astronomical Watch.lnk" >nul 2>&1
    echo + Shortcut removed: %PUBLIC%\Desktop
    set SHORTCUT_FOUND=1
)

REM Try registry location
for /f "usebackq tokens=3*" %%A in (`reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop 2^>nul`) do (
    set DESKTOP_REG=%%B
    call set DESKTOP_REG=!DESKTOP_REG!
    if exist "!DESKTOP_REG!\Astronomical Watch.lnk" (
        del "!DESKTOP_REG!\Astronomical Watch.lnk" >nul 2>&1
        echo + Shortcut removed: !DESKTOP_REG!
        set SHORTCUT_FOUND=1
    )
)

if !SHORTCUT_FOUND!==0 (
    echo ! Shortcut not found (may have been manually deleted)
)

echo.
echo ========================================
echo   UNINSTALL COMPLETE
echo ========================================
echo.
echo Astronomical Watch has been removed from your system.
echo.
echo You can reinstall anytime by running install.bat
echo.
pause
