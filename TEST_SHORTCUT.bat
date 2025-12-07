@echo off
REM Test if desktop shortcut exists and where

echo ================================
echo Desktop Shortcut Test
================================
echo.

REM Get desktop path
set DESKTOP=%USERPROFILE%\Desktop

echo Checking for shortcut...
echo Desktop path: %DESKTOP%
echo.

if exist "%DESKTOP%\Astronomical Watch.lnk" (
    echo ✓ Shortcut found: %DESKTOP%\Astronomical Watch.lnk
    echo.
    echo Shortcut properties:
    powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\Astronomical Watch.lnk'); Write-Host 'Target:' $s.TargetPath; Write-Host 'Arguments:' $s.Arguments; Write-Host 'Icon:' $s.IconLocation"
    echo.
    echo Testing launch...
    echo (This will start the application - close it to continue)
    echo.
    pause
    start "" "%DESKTOP%\Astronomical Watch.lnk"
) else (
    echo ✗ Shortcut NOT found at: %DESKTOP%\Astronomical Watch.lnk
    echo.
    echo Let me check other possible locations...
    echo.
    
    REM Try OneDrive Desktop
    if exist "%USERPROFILE%\OneDrive\Desktop\Astronomical Watch.lnk" (
        echo ✓ Found in OneDrive: %USERPROFILE%\OneDrive\Desktop\Astronomical Watch.lnk
    )
    
    REM List all .lnk files on desktop
    echo.
    echo Files on your Desktop:
    dir /b "%DESKTOP%\*.lnk" 2>nul
    if errorlevel 1 (
        echo   (No .lnk files found)
    )
)

echo.
echo ================================
pause
