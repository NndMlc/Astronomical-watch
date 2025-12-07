@echo off
REM Uninstallation script for Astronomical Watch

echo ================================
echo Astronomical Watch - Uninstall
echo ================================
echo.
echo This will:
echo  - Remove the Python package
echo  - Delete the desktop shortcut
echo.

set /p CONFIRM="Are you sure you want to uninstall? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo.
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo Uninstalling package...
pip uninstall -y astronomical-watch

echo.
echo Removing desktop shortcut...

REM Get desktop path
for /f "usebackq tokens=3*" %%A in (`reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop`) do set DESKTOP=%%B
call set DESKTOP=%DESKTOP%

if exist "%DESKTOP%\Astronomical Watch.lnk" (
    del "%DESKTOP%\Astronomical Watch.lnk"
    echo Desktop shortcut removed.
) else (
    echo Desktop shortcut not found.
)

echo.
echo ================================
echo Uninstall complete!
echo ================================
echo.
pause
