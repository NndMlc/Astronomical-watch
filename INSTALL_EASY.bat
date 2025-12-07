@echo off
REM Easy installer that uses PowerShell for better shortcut creation

echo Starting installation...
echo.
echo This will:
echo  - Install Astronomical Watch
echo  - Create a desktop shortcut with icon
echo  - Set up the command-line tool
echo.
pause

REM Run PowerShell script
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"
